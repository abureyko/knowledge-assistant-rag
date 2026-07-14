# ruff: noqa: F401,F841
from __future__ import annotations

from pathlib import Path

from knowledge_agent.ingestion.chunking import chunk_documents
from knowledge_agent.ingestion.loader import load_markdown_documents
from knowledge_agent.ingestion.metadata import normalize_metadata


def run_ingestion(
    *,
    corpus_path: Path,
    store,
    embeddings,
    chunk_size: int,
    chunk_overlap: int,
    recreate_collection: bool = False,
) -> dict[str, int]:
    documents = load_markdown_documents(corpus_path)
    normalized = [normalize_metadata(document) for document in documents]
    chunks = chunk_documents(
        normalized,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])

    store.ensure_collection(recreate=recreate_collection)
    store.upsert_documents(chunks=chunks, vectors=vectors)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "collection_size": store.count(),
    }
