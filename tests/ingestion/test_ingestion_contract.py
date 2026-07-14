from pathlib import Path

from knowledge_agent.ingestion.chunking import chunk_documents
from knowledge_agent.ingestion.loader import load_markdown_documents
from knowledge_agent.ingestion.metadata import normalize_metadata


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_ingestion_contract() -> None:
    root = project_root()
    documents = load_markdown_documents(root / "data" / "starter_corpus")
    normalized = [normalize_metadata(document) for document in documents]
    chunks = chunk_documents(normalized, chunk_size=180, chunk_overlap=20)

    assert len(documents) >= 10
    assert chunks
    assert "chunk_id" in chunks[0].metadata
    assert "section" in chunks[0].metadata
