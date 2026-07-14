from __future__ import annotations

import hashlib
import math
from typing import Protocol

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


class SizedEmbeddings(Protocol):
    embedding_size: int | None


class HashEmbeddings(Embeddings):
    def __init__(self, *, embedding_size: int = 48) -> None:
        self.embedding_size = embedding_size
        self.backend_name = "hash"

    def _embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.embedding_size
        tokens = text.lower().split()
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % self.embedding_size
            sign = -1.0 if digest[1] % 2 else 1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)


def build_embeddings_backend(settings) -> Embeddings:
    if settings.embedding_model.startswith("hash://"):
        backend = HashEmbeddings(embedding_size=settings.embedding_size)
        backend.embedding_size = settings.embedding_size
        return backend
    backend = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
    )
    backend.backend_name = "openai-compatible"
    return backend
