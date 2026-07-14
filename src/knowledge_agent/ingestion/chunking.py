# ruff: noqa: F401,F841
from __future__ import annotations

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

HEADING_RE = re.compile(r"^(#+)\s+(.*)$", re.MULTILINE)


def _primary_section(text: str) -> str:
    match = HEADING_RE.search(text)
    return match.group(2).strip() if match else "Overview"


def chunk_documents(
    documents: list[Document],
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks: list[Document] = []
    for document in documents:
        section = _primary_section(document.page_content)
        split_texts = splitter.split_text(document.page_content)
        for index, text in enumerate(split_texts):
            metadata = dict(document.metadata)
            metadata["section"] = section
            metadata["chunk_index"] = index
            metadata["chunk_id"] = f"{metadata['doc_id']}:{index:04d}"
            chunks.append(Document(page_content=text, metadata=metadata))
    return chunks
