from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class BatchText:
    """A utility class for handling a long list of texts with potentially duplicated."""

    unique_text: dict[str, int] = field(default_factory=dict)
    text_index: list[int] = field(default_factory=list)

    @staticmethod
    def from_list_str(texts: list[str] | np.ndarray) -> BatchText:
        batch_text = BatchText()
        for text in texts:
            batch_text.add_text(text)
        return batch_text

    def add_text(self, text: str):
        """Add text to this batch and return its position"""
        if text not in self.unique_text:
            index = len(self.unique_text)
            self.unique_text[text] = index
        else:
            index = self.unique_text[text]

        self.text_index.append(index)
        return index

    def add_repeated_text(self, text: str, n: int):
        if text not in self.unique_text:
            index = len(self.unique_text)
            self.unique_text[text] = index
        else:
            index = self.unique_text[text]

        self.text_index.extend([index] * n)
        return index

    def __len__(self):
        return len(self.text_index)


@dataclass
class BatchTextEmbedding:
    unique_text: dict[str, int]
    text_index: list[int]
    embeddings: np.ndarray

    @staticmethod
    def from_batch_text(texts: list[str] | BatchText, embs: np.ndarray):
        if not isinstance(texts, BatchText):
            batch_text = BatchText.from_list_str(texts)
        else:
            batch_text = texts
        return BatchTextEmbedding(batch_text.unique_text, batch_text.text_index, embs)

    def get_embedding(self, text: str):
        return self.embeddings[self.text_index[self.unique_text[text]]]
