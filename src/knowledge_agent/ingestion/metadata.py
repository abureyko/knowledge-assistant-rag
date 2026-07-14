# ruff: noqa: F401,F841
from __future__ import annotations

from datetime import date, datetime

from langchain_core.documents import Document

REQUIRED_FIELDS = ("doc_id", "title", "doc_type", "topic", "updated_at", "source")


def normalize_metadata(document: Document) -> Document:
    metadata = dict(document.metadata)
    missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
    if missing:
        joined = ", ".join(missing)
        source = metadata.get("source", "<unknown source>")
        raise ValueError(f"Document {source!r} is missing required metadata: {joined}")

    for field in ("doc_id", "title", "doc_type", "topic", "source"):
        metadata[field] = str(metadata[field]).strip()

    updated_at = metadata["updated_at"]
    if isinstance(updated_at, datetime):
        metadata["updated_at"] = updated_at.date().isoformat()
    elif isinstance(updated_at, date):
        metadata["updated_at"] = updated_at.isoformat()
    else:
        metadata["updated_at"] = str(updated_at).strip()

    return Document(page_content=document.page_content, metadata=metadata)
