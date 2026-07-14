from pathlib import Path

from knowledge_agent.config import Settings
from knowledge_agent.runtime import create_runtime


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_indexing_contract() -> None:
    root = project_root()
    settings = Settings(
        qdrant_url=":memory:",
        corpus_path=root / "data" / "starter_corpus",
        graph_mode="core",
        llm_model="offline-rule-based",
    )
    runtime = create_runtime(settings=settings)
    result = runtime.ingest(recreate_collection=True)

    assert result["documents"] >= 10
    assert result["collection_size"] > 0


def test_docker_image_points_runtime_to_copied_corpus() -> None:
    root = project_root()
    dockerfile = (root / "Dockerfile").read_text(encoding="utf-8")
    compose = (root / "docker-compose.yml").read_text(encoding="utf-8")

    assert "COPY data ./data" in dockerfile
    assert "ENV CORPUS_PATH=/app/data/starter_corpus" in dockerfile
    assert "CORPUS_PATH: /app/data/starter_corpus" in compose
