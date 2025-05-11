from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from sm.misc.funcs import assert_isinstance
from timer import Timer
from transformers import AutoModel, AutoTokenizer

from keyvec.embed_store import EmbeddingModel, EmbeddingModelArgs


@dataclass
class HfModelArgs(EmbeddingModelArgs):
    embedding_model: str
    customization: str = "default"

    def to_dict(self):
        return {
            "embedding_model": self.embedding_model,
            "customization": self.customization,
        }


class HfModel(EmbeddingModel[HfModelArgs]):
    def __init__(self, args: HfModelArgs):
        super().__init__(args)

        with Timer().watch_and_report("Load embedding model", preprint=True):
            self.tokenizer = AutoTokenizer.from_pretrained(args.embedding_model)
            self.model = AutoModel.from_pretrained(
                args.embedding_model, device_map="auto"
            )

        if args.embedding_model == "BAAI/bge-m3":
            if args.customization == "default":
                # use the embedding at the first cls token
                self.use_first_cls_token = True
            elif args.customization == "last-token":
                self.use_first_cls_token = False
            else:
                raise NotImplementedError(args.customization)
        else:
            raise NotImplementedError(args.embedding_model)

    def encode_texts(self, texts: list[str]) -> np.ndarray:
        if self.args.embedding_model.startswith("sentence-transformers"):
            embs = self.model.encode(texts)
            assert isinstance(embs, np.ndarray)
            return embs

        forward_args = self.tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True
        ).to(self.model.device)
        input_ids = assert_isinstance(forward_args["input_ids"], torch.Tensor)

        if self.use_first_cls_token:
            sequence_index = slice(0, None)
            sequence_lengths = 0
        else:
            pad_token_id = self.tokenizer.pad_token_id
            assert pad_token_id is not None
            # use the last token -- mean pooling ?
            is_pad_left = torch.all(input_ids[:, -1] != pad_token_id).item()
            if is_pad_left:
                sequence_index = slice(0, None)
                sequence_lengths = -1
            else:
                sequence_index = torch.arange(
                    input_ids.shape[0], device=self.model.device
                )
                sequence_lengths = (
                    torch.eq(input_ids, pad_token_id).int().argmax(-1) - 1
                )
                sequence_lengths = sequence_lengths % input_ids.shape[-1]
                sequence_lengths = sequence_lengths.to(self.model.device)

        with torch.no_grad():
            out = self.model(**forward_args)
            assert hasattr(out, "last_hidden_state")
            assert out.last_hidden_state.shape == (
                len(texts),
                input_ids.shape[1],
                out.last_hidden_state.shape[2],
            )

            return (
                out.last_hidden_state[
                    sequence_index,
                    sequence_lengths,
                ]
                .cpu()
                .numpy()
            )
