# ruff: noqa: F401,F841
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from knowledge_agent.retrieval.filters import build_payload_filter


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    score: float
    metadata: dict[str, Any]
    citation: str


STOPWORDS = {
    "about",
    "after",
    "before",
    "being",
    "does",
    "from",
    "give",
    "have",
    "help",
    "into",
    "more",
    "only",
    "policy",
    "process",
    "question",
    "recipe",
    "system",
    "that",
    "their",
    "them",
    "this",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "your",
    "tell",
    "guide",
    "runbook",
    "faq",
}


def format_citation(metadata: dict[str, Any]) -> str:
    doc_id = metadata.get("doc_id", "unknown-doc")
    title = metadata.get("title", "Untitled")
    section = metadata.get("section")
    return f"{doc_id} | {title} | {section}" if section else f"{doc_id} | {title}"


def extract_keywords(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9-]{2,}", text.lower())
    return {token for token in tokens if token not in STOPWORDS}


def is_grounded_match(query: str, chunks: list[RetrievedChunk]) -> bool:
    return any(lexical_overlap(query, chunk) > 0 for chunk in chunks)


def lexical_overlap(query: str, chunk: RetrievedChunk) -> int:
    query_keywords = extract_keywords(query)
    chunk_keywords = extract_keywords(chunk.text)
    metadata_keywords = extract_keywords(
        " ".join(
            str(chunk.metadata.get(field, ""))
            for field in ("doc_id", "title", "doc_type", "topic", "section")
        )
    )
    return len(query_keywords & (chunk_keywords | metadata_keywords))


def supporting_citations(
    query: str,
    chunks: list[RetrievedChunk],
    *,
    max_items: int = 4,
) -> list[str]:
    ranked = sorted(chunks, key=lambda chunk: lexical_overlap(query, chunk), reverse=True)
    citations: list[str] = []
    seen: set[str] = set()
    for chunk in ranked:
        if chunk.citation in seen:
            continue
        if lexical_overlap(query, chunk) <= 0 and citations:
            continue
        citations.append(chunk.citation)
        seen.add(chunk.citation)
        if len(citations) >= max_items:
            break
    return citations


def payload_to_chunk(
    payload: dict[str, Any],
    *,
    score: float = 0.0,
    chunk_id: str | None = None,
) -> RetrievedChunk:
    metadata = dict(payload)
    text = str(metadata.pop("text", ""))
    resolved_chunk_id = str(metadata.get("chunk_id") or chunk_id or "")
    if resolved_chunk_id:
        metadata["chunk_id"] = resolved_chunk_id
    return RetrievedChunk(
        chunk_id=resolved_chunk_id,
        text=text,
        score=score,
        metadata=metadata,
        citation=format_citation(metadata),
    )


class Retriever:
    def __init__(self, *, store, embeddings, default_top_k: int = 4) -> None:
        self.store = store
        self.embeddings = embeddings
        self.default_top_k = default_top_k

    def retrieve(
        self,
        query: str,
        *,
        filters: dict[str, Any] | None = None,
        top_k: int | None = None,
    ) -> list[RetrievedChunk]:
        limit = top_k or self.default_top_k
        payload_filter = build_payload_filter(filters)
        query_vector = self.embeddings.embed_query(query)
        # Fetch extra vector candidates, then let lexical evidence improve final ordering.
        search_limit = max(limit * 5, limit)
        hits = self.store.search(
            query_vector=query_vector,
            payload_filter=payload_filter,
            limit=search_limit,
        )
        chunks = [
            payload_to_chunk(
                hit.payload or {},
                score=float(getattr(hit, "score", 0.0) or 0.0),
                chunk_id=str(getattr(hit, "id", "")),
            )
            for hit in hits
        ]
        # Lexical overlap is the primary signal; vector similarity breaks ties.
        chunks.sort(key=lambda chunk: (lexical_overlap(query, chunk), chunk.score), reverse=True)
        return chunks[:limit]
