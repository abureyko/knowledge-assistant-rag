# ruff: noqa: F401,F841
from __future__ import annotations

import re
from pathlib import Path

import yaml
from langchain_core.documents import Document

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def _parse_frontmatter(raw_text: str, *, fallback_source: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(raw_text.strip())
    if not match:
        return {"source": fallback_source}, raw_text.strip()
    metadata_raw, body = match.groups()
    metadata = yaml.safe_load(metadata_raw) or {}
    metadata.setdefault("source", fallback_source)
    return metadata, body.strip()


def load_markdown_documents(corpus_path: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(corpus_path.glob("*.md")):
        raw_text = path.read_text(encoding="utf-8")
        metadata, body = _parse_frontmatter(raw_text, fallback_source=str(path))
        metadata["file_path"] = str(path)
        documents.append(Document(page_content=body, metadata=metadata))
    return documents
