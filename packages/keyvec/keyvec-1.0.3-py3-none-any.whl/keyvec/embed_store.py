from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Generic, Optional, Sequence, TypeVar, Union

import numpy as np
import orjson
import ray
import serde.csv
import serde.json
import serde.pickle
from hugedict.sqlite import SqliteDict, SqliteDictFieldType
from loguru import logger
from sm.misc.funcs import (
    assert_all_item_not_null,
    batch,
    cluster,
    get_incremental_path,
    group_by,
)
from sm.misc.ray_helper import (
    add_ray_actors,
    get_ray_actors,
    ray_actor_map,
    ray_get_num_gpu,
)
from tqdm.auto import tqdm

from keyvec.batch_text import BatchText
from keyvec.embed_chunk import EmbeddingChunk

# text => (dataset index, example index)
EmbeddingIndex = SqliteDict[str, tuple[int, int]]
# text => (number of agreement, number of computed total)
EmbeddingQuality = SqliteDict[str, tuple[int, int]]


@dataclass
class EmbeddingModelArgs:
    def get_args(self):
        return self

    def to_dict(self):
        raise NotImplementedError()


A = TypeVar("A", bound=EmbeddingModelArgs)


class EmbeddingModel(Generic[A]):

    def __init__(self, args: A):
        self.args = args

    def get_args(self) -> A:
        return self.args

    def encode_texts(self, texts: list[str]) -> np.ndarray:
        raise NotImplementedError()


class EmbeddingManager:
    def __init__(
        self,
        dir: Path,
        index: EmbeddingIndex,
        quality: EmbeddingIndex,
        datasets: list[EmbeddingChunk],
        embedding_model: EmbeddingModel | EmbeddingModelArgs,
        chunk_size: int,
    ):
        self.dir = dir
        # mapping from the text to the index of the dataset and the index of the example
        self.index = index
        # recording the quality of the embeddings
        self.quality = quality
        self.datasets = datasets

        self.chunk_size = chunk_size
        self.index_buffer = {}
        self.data_buffer = []
        self.embedding_model = embedding_model

    @classmethod
    def from_disk(
        cls,
        dir: Path,
        embedding_model: EmbeddingModel | EmbeddingModelArgs,
        chunk_size: int = 64000,
        mem_map: bool = True,
    ):
        (dir / "datasets").mkdir(parents=True, exist_ok=True)
        if (dir / "embed_model.json").exists():
            assert (
                serde.json.deser(dir / "embed_model.json")
                == embedding_model.get_args().to_dict()
            )

        # mapping from text to (chunk, index, num_compute)
        index: EmbeddingIndex = SqliteDict(
            dir / "index.sqlite",
            SqliteDictFieldType.str,
            orjson.dumps,
            orjson.loads,
            SqliteDictFieldType.bytes,
        )
        quality: EmbeddingQuality = SqliteDict(
            dir / "quality.sqlite",
            SqliteDictFieldType.str,
            orjson.dumps,
            orjson.loads,
            SqliteDictFieldType.bytes,
        )
        start = 0
        datasets = []
        for dsdir in sorted(
            (dir / "datasets").iterdir(), key=lambda x: int(x.name.split("_")[1])
        ):
            datasets.append(EmbeddingChunk.load(dsdir, mem_map=mem_map))
            assert (
                datasets[-1].start == start
            ), f"{dsdir.name} does not start at {start}"
            start = datasets[-1].end

        assert len(index) == sum(len(d) for d in datasets)
        return EmbeddingManager(
            dir,
            index,
            quality,
            datasets,
            embedding_model,
            chunk_size,
        )

    def __contains__(self, text: str) -> bool:
        return text in self.index or text in self.index_buffer

    def retrieve(self, text: str) -> Optional[np.ndarray]:
        if text in self.index:
            dsidx, exidx = self.index[text]
            return self.datasets[dsidx][exidx]
        if text in self.index_buffer:
            return self.data_buffer[self.index_buffer[text]]
        return None

    def add_to_buffer(self, text: str, emb: np.ndarray):
        """Record a key-value pair but do not flush to disk yet."""
        assert text not in self
        self.index_buffer[text] = len(self.data_buffer)
        self.data_buffer.append(emb)

    def batch_retrieve_exist(self, texts: list[str]) -> np.ndarray:
        out = []
        for text in texts:
            if text in self.index:
                dsidx, exidx = self.index[text]
                out.append(self.datasets[dsidx][exidx])
            elif text in self.index_buffer:
                out.append(self.data_buffer[self.index_buffer[text]])
            else:
                raise KeyError(text)
        return np.stack(out)

    def batch_get(
        self,
        texts: Union[list[str], np.ndarray, BatchText],
        batch_size: int = 512,
        parallel: bool = False,
        verbose: bool = False,
    ) -> np.ndarray:
        """Get the embeddings for the given texts."""
        if not isinstance(texts, BatchText):
            batch_text = BatchText.from_list_str(texts)
        else:
            batch_text = texts

        all_embs = [
            self.retrieve(text)
            for text in tqdm(
                batch_text.unique_text.keys(),
                desc="retrieving previously computed embeddings",
                disable=not verbose,
            )
        ]
        assert all(
            i == batch_text.unique_text[text]
            for i, text in enumerate(batch_text.unique_text.keys())
        )
        unknown_texts = [
            text for text, i in batch_text.unique_text.items() if all_embs[i] is None
        ]
        if len(unknown_texts) > 0:
            # transform those unknown texts into embeddings
            unknown_texts_emb = self.encode_texts(
                unknown_texts, batch_size=batch_size, parallel=parallel, verbose=verbose
            )
            for text, emb in zip(unknown_texts, unknown_texts_emb):
                all_embs[batch_text.unique_text[text]] = emb

        new_all_embs = assert_all_item_not_null(all_embs)
        return np.stack([new_all_embs[i] for i in batch_text.text_index])

    def flush(self, soft: bool = False):
        """Flush the dataset to disk."""
        if soft and len(self.data_buffer) < self.chunk_size:
            return

        # determine the range in the buffer to save to disk, if hard flush, save everything
        assert len(self.index_buffer) == len(self.data_buffer)
        if len(self.data_buffer) == 0:
            return

        keys = [""] * len(self.index_buffer)
        for text, i in self.index_buffer.items():
            keys[i] = text
        data = self.data_buffer

        # determine if the last chunk is not full, we may need to update it.
        if len(self.datasets) > 0:
            last_chunk_size = len(self.datasets[-1])
            if last_chunk_size < self.chunk_size and (
                not soft or last_chunk_size + len(data) >= self.chunk_size
            ):
                # the last chunk isn't full and we can flush it
                newkeys = keys[: self.chunk_size - last_chunk_size]
                newdata = data[: self.chunk_size - last_chunk_size]

                ds = self.datasets[-1]
                ds_dir = self.get_chunk_dir(len(self.datasets) - 1)
                ds_metadata = serde.json.deser(ds_dir / "metadata.json")
                assert (
                    ds_metadata["start"] == ds.start and ds_metadata["end"] == ds.end
                ), "Make sure that we got the right chunk location"
                assert ds.keys is not None, "The last chunk must load keys"

                ds.end += len(newdata)
                ds.keys.extend(newkeys)
                ds.data = np.concatenate([np.load(ds_dir / "data.npy"), newdata])

                ds.save(Path(str(ds_dir) + "_tmp"))
                shutil.rmtree(ds_dir)

                new_items: list[tuple[str, tuple[int, int]]] = []
                for idx, key in enumerate(ds.keys):
                    new_items.append((key, (len(self.datasets) - 1, idx)))
                self.index.batch_insert(new_items)

                os.rename(Path(str(ds_dir) + "_tmp"), ds_dir)

                data = data[self.chunk_size - last_chunk_size :]
                keys = keys[self.chunk_size - last_chunk_size :]

        if soft:
            save_to = int(len(self.data_buffer) / self.chunk_size) * self.chunk_size
        else:
            save_to = len(self.data_buffer)

        self.data_buffer = data[save_to:]
        self.index_buffer = {k: self.index_buffer[k] - save_to for k in keys[save_to:]}

        data = data[:save_to]
        keys = keys[:save_to]
        start = len(self.index)

        # save the data to disk
        for i in tqdm(
            range(0, len(data), self.chunk_size),
            desc="saving embeddings",
            disable=len(data) <= self.chunk_size,
        ):
            chunk_dir = self.get_chunk_dir(None)
            chunk_keys = keys[i : i + self.chunk_size]
            chunk_data = np.array(data[i : i + self.chunk_size])

            ds = EmbeddingChunk(
                start,
                start + len(chunk_data),
                keys=chunk_keys,
                data=chunk_data,
                mem_map=False,
            )
            ds.save(chunk_dir)

            new_items: list[tuple[str, tuple[int, int]]] = []
            for idx, key in enumerate(chunk_keys):
                new_items.append((key, (len(self.datasets), idx)))
            self.index.batch_insert(new_items)

            self.datasets.append(ds)
            start += len(chunk_data)

    def ensure_quality(
        self,
        batch_size: int,
        verify_data: bool = False,
        resolve_conflict: bool = False,
        export_quality: bool = False,
        parallel: bool = False,
        verbose: bool = False,
    ):
        # verify the content in the data chunks and the index
        for key, (dsidx, exidx) in tqdm(self.index.items(), total=len(self.index)):
            dataset = self.datasets[dsidx]
            assert dataset.keys is not None and dataset.keys[exidx] == key

        quality_index = self.quality

        def verify_chunk_data(chunk_idx: int, chunk: EmbeddingChunk):
            assert chunk.keys is not None and not chunk.mem_map
            emb = self.encode_texts(
                chunk.keys,
                batch_size=batch_size,
                parallel=parallel,
                verbose=verbose,
                auto_shutdown=chunk_idx == len(self.datasets) - 1,
                soft_flush=False,
            )

            conflict_keys = []
            conflict_embs = []

            update_chunk = False

            for i, key in enumerate(chunk.keys):
                is_prevemb_bad = np.any(np.isnan(chunk.data[i])) or np.any(
                    np.isinf(chunk.data[i])
                )
                is_newemb_bad = np.any(np.isnan(emb[i])) or np.any(np.isinf(emb[i]))

                if is_prevemb_bad:
                    if not is_newemb_bad:
                        # the previous one is corrupted, and we have a better one, we use them directly
                        chunk.data[i] = emb[i]
                        update_chunk = True
                        logger.info(
                            "key {} is corrupted, recomputing generates a good embedding",
                            key,
                        )
                    else:
                        # both of them are bad..., we need to skip this key
                        logger.warning(
                            "key {} is corrupted, recomputing still generates a bad embedding",
                            key,
                        )
                    continue

                if is_newemb_bad:
                    # the new embedding is bad, we need to skip this key
                    logger.debug(
                        "key {} is good, but recomputing generates a bad embedding", key
                    )
                    continue

                if key not in quality_index:
                    # this is the first time we see this key
                    prev_qual = (1, 1)
                    quality_index[key] = prev_qual
                else:
                    prev_qual = quality_index[key]

                is_same = np.allclose(emb[i], chunk.data[i], rtol=0.0, atol=1e-7)
                flag_error = False
                if is_same:
                    # they are the same, we increase the quality
                    quality_index[key] = (
                        prev_qual[0] + 1,
                        prev_qual[1] + 1,
                    )

                    # however, if the quality is not 100% or embedding is bad,
                    # that means we have a bad key, so we need to store the new embeddings for quality checking later
                    if prev_qual[0] < prev_qual[1] or is_newemb_bad:
                        flag_error = True
                else:
                    quality_index[key] = (
                        prev_qual[0],
                        prev_qual[1] + 1,
                    )
                    flag_error = True

                if flag_error:
                    conflict_keys.append(key)
                    conflict_embs.append(emb[i])

                    # note that if this is the second time we recompute the key, we need to save the previous one as well
                    if prev_qual[1] == 1:
                        conflict_keys.append(key)
                        conflict_embs.append(chunk.data[i])

            conflict_file = self.get_chunk_dir(chunk_idx) / "conflict.npz"
            if conflict_file.exists():
                conflicts = np.load(conflict_file, allow_pickle=True)
                conflict_keys.extend(conflicts["keys"])
                conflict_embs.extend(conflicts["embs"])

            if len(conflict_keys) > 0:
                np.savez(
                    conflict_file,
                    keys=np.array(conflict_keys, dtype=np.object_),
                    embs=np.array(conflict_embs),
                )

            if update_chunk:
                np.save(self.get_chunk_dir(chunk_idx) / "data.npy", chunk.data)

            logger.info(
                "Chunk {} has {} conflict keys", chunk_idx, len(set(conflict_keys))
            )

        def resolve_chunk_conflict(chunk_idx: int, chunk: EmbeddingChunk):
            assert chunk.keys is not None and not chunk.mem_map
            conflict_file = self.get_chunk_dir(chunk_idx) / "conflict.npz"
            if not conflict_file.exists():
                logger.info("No conflict found!")
                return

            conflicts = np.load(conflict_file, allow_pickle=True)
            conflict_keys = conflicts["keys"]
            conflict_embs = conflicts["embs"]

            key2indexes = group_by(
                range(len(conflict_keys)), lambda i: conflict_keys[i]
            )

            for key in tqdm(
                key2indexes, desc="resolving conflicts", disable=not verbose
            ):
                values: list[np.ndarray] = [conflict_embs[i] for i in key2indexes[key]]
                same_as = []
                for i in range(len(values)):
                    for j in range(len(values)):
                        if i == j:
                            continue
                        if np.allclose(values[i], values[j], rtol=0.0, atol=1e-7):
                            same_as.append((i, j))
                groups = cluster(same_as)
                total = len(values)
                most_popular_group = max(groups, key=lambda g: len(g))

                dsidx, exidx = self.index[key]
                assert dsidx == chunk_idx
                chunk.data[exidx] = values[most_popular_group[0]]
                quality_index[key] = (len(most_popular_group), total)

            np.save(self.get_chunk_dir(chunk_idx) / "data.npy", chunk.data)

        def export_chunk_quality(chunk_idx: int, chunk: EmbeddingChunk):
            assert chunk.keys is not None and not chunk.mem_map
            out = []
            for key in chunk.keys:
                if key in quality_index:
                    freq, total = quality_index[key]
                else:
                    freq, total = 1, 1
                out.append({"key": key, "freq": freq, "total": total})
            serde.csv.ser(out, self.get_chunk_dir(chunk_idx) / "quality.csv")

        for i, chunk in enumerate(self.datasets):
            if verify_data:
                verify_chunk_data(i, chunk)

            if resolve_conflict:
                resolve_chunk_conflict(i, chunk)

            if export_quality:
                export_chunk_quality(i, chunk)

    def encode_texts(
        self,
        texts: list[str],
        batch_size: int,
        parallel: bool = False,
        verbose: bool = False,
        auto_shutdown: bool = True,
        soft_flush: bool = True,
    ) -> list[np.ndarray]:
        batched_texts: list[list[str]] = batch(batch_size, texts)
        output = []
        if parallel and len(batched_texts) > 1:
            num_gpu = int(ray_get_num_gpu())
            assert num_gpu > 1, "We need at least 2 GPUs to run in parallel mode"

            actors: Sequence[ray.ObjectRef[EmbeddingModel]] = get_ray_actors(
                "keyvec.embed_manager"
            )
            if len(actors) == 0:
                actors = add_ray_actors(
                    EmbeddingModel,
                    (self.embedding_model.get_args(),),
                    "keyvec.embed_manager",
                    size=num_gpu,
                    remote_options={"num_gpus": 1},
                )

            batched_embs: list[np.ndarray] = ray_actor_map(
                [actor.encode_texts.remote for actor in actors],  # type: ignore
                [(b,) for b in batched_texts],
                verbose=verbose,
                desc="compute text embeddings",
                postprocess=np.copy,
                auto_shutdown=auto_shutdown,
            )

            for i in range(len(batched_texts)):
                for text, emb in zip(batched_texts[i], batched_embs[i]):
                    self.index_buffer[text] = len(self.data_buffer)
                    self.data_buffer.append(emb)
                    output.append(emb)

            if soft_flush:
                self.flush(True)
        else:
            for b in tqdm(
                batched_texts,
                desc="compute text embeddings",
                disable=not verbose,
            ):
                be = self.embed_func(b)
                for text, emb in zip(b, be):
                    self.index_buffer[text] = len(self.data_buffer)
                    self.data_buffer.append(emb)
                    output.append(emb)

                if soft_flush:
                    self.flush(True)

        return output

    def get_chunk_dir(self, chunk_idx: Optional[int]):
        """Chunk index start from 1"""
        if chunk_idx is None:
            # this works because when there is no chunk, the function return 1
            chunk_dir = get_incremental_path(self.dir / f"datasets/chunks")
        else:
            chunk_dir = self.dir / f"datasets/chunks_{chunk_idx + 1:02d}"
        # print("Grant chunk dir for ", chunk_idx, "at", chunk_dir)
        return chunk_dir

    def partition(self, out_dir: Path, chunk_size: int):
        """Create a new embedding with a different chunk size. This always create a new directory"""
        manager = EmbeddingManager.from_disk(
            out_dir,
            self.embedding_model,
            chunk_size,
        )
        for text in tqdm(self.index.keys(), total=len(self.index), desc="partitioning"):
            emb = self.retrieve(text)
            assert emb is not None
            manager.add_to_buffer(text, emb)

        manager.flush()

    @cached_property
    def embed_func(self):
        if isinstance(self.embedding_model, EmbeddingModelArgs):
            from keyvec.hf_model import HfModel, HfModelArgs

            if isinstance(self.embedding_model, HfModelArgs):
                self.embedding_model = HfModel(self.embedding_model)
            else:
                raise NotImplementedError(
                    f"Unsupported embedding model {self.embedding_model}"
                )

        assert isinstance(self.embedding_model, EmbeddingModel)
        return self.embedding_model.encode_texts
