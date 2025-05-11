from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import serde.csv
import serde.json


class EmbeddingChunk:
    def __init__(
        self,
        start: int,
        end: int,
        keys: Optional[list[str]],
        data: np.ndarray,
        mem_map: bool,
    ):
        self.start = start
        self.end = end
        self.keys = keys
        self.data = data
        # data np.memmap is also a subclass of np.ndarray, it's better to just store the open mode
        self.mem_map = mem_map

    def __getitem__(self, idx: int):
        return self.data[idx]

    def __len__(self):
        return self.end - self.start

    def save(self, dir: Path):
        dir.mkdir(parents=True, exist_ok=True)
        assert not (dir / "metadata.json").exists()
        serde.json.ser(
            {
                "start": self.start,
                "end": self.end,
                "shape": list(self.data.shape),
                "dtype": self.data.dtype.name,
            },
            dir / "metadata.json",
        )
        if self.keys is not None:
            serde.json.ser(self.keys, dir / "keys.json.lz4")
        np.save(dir / "data.npy", self.data)

    @staticmethod
    def load(dir: Path, with_keys: bool = True, mem_map: bool = True) -> EmbeddingChunk:
        if with_keys:
            keys = serde.json.deser(dir / "keys.json.lz4")
        else:
            keys = None

        metadata = serde.json.deser(dir / "metadata.json")
        return EmbeddingChunk(
            metadata["start"],
            metadata["end"],
            keys,
            (
                np.lib.format.open_memmap(
                    dir / "data.npy",
                    dtype=np.dtype(metadata["dtype"]),
                    mode="r",
                    shape=tuple(metadata["shape"]),
                )
                if mem_map
                else np.load(dir / "data.npy")
            ),
            mem_map,
        )
