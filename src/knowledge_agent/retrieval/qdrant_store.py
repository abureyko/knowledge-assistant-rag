# ruff: noqa: F401,F841
from __future__ import annotations

import time
import uuid
from typing import Any

from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, Filter, PointStruct, VectorParams


class QdrantDocumentStore:
    def __init__(self, *, url: str, collection_name: str, vector_size: int | None = None) -> None:
        self.collection_name = collection_name
        self.vector_size = vector_size
        if url == ":memory:":
            self.client = QdrantClient(location=":memory:")
        else:
            self.client = QdrantClient(url=url)

    def ensure_collection(self, *, recreate: bool = False, vector_size: int | None = None) -> None:
        size = vector_size or self.vector_size
        if size is None:
            raise ValueError("vector_size is required to create a Qdrant collection")

        exists = self.collection_exists()
        if recreate and exists:
            self.client.delete_collection(collection_name=self.collection_name)
            exists = False

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )

    def collection_exists(self) -> bool:
        return self.collection_name in {
            collection.name for collection in self.client.get_collections().collections
        }

    def upsert_documents(self, *, chunks: list[Document], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError(
                f"chunks and vectors must have the same length: {len(chunks)} != {len(vectors)}"
            )

        points: list[PointStruct] = []
        for chunk, vector in zip(chunks, vectors, strict=True):
            payload = dict(chunk.metadata)
            payload["text"] = chunk.page_content
            chunk_id = str(payload["chunk_id"])
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

    def search(
        self,
        *,
        query_vector: list[float],
        payload_filter: Filter | None,
        limit: int,
    ) -> list[Any]:
        try:
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=payload_filter,
                limit=limit,
                with_payload=True,
                with_vectors=False,
            )
        except UnexpectedResponse as exc:
            if "doesn't exist" in str(exc).lower() or "not found" in str(exc).lower():
                raise RuntimeError(
                    f"Qdrant collection {self.collection_name!r} is missing. "
                    "Run `knowledge-agent ingest` or `knowledge-agent reindex` first."
                ) from exc
            raise
        return list(response.points)

    def fetch_all(self, *, payload_filter: Filter | None) -> list[Any]:
        records: list[Any] = []
        offset = None
        while True:
            try:
                batch, offset = self.client.scroll(
                    collection_name=self.collection_name,
                    scroll_filter=payload_filter,
                    with_payload=True,
                    with_vectors=False,
                    limit=128,
                    offset=offset,
                )
            except UnexpectedResponse as exc:
                if "doesn't exist" in str(exc).lower() or "not found" in str(exc).lower():
                    raise RuntimeError(
                        f"Qdrant collection {self.collection_name!r} is missing. "
                        "Run `knowledge-agent ingest` or `knowledge-agent reindex` first."
                    ) from exc
                raise
            records.extend(batch)
            if offset is None:
                break
        return records

    def count(self) -> int:
        return self.client.count(collection_name=self.collection_name).count

    def is_available(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False
