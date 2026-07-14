from pathlib import Path

from fastapi.testclient import TestClient

from knowledge_agent.api.app import app
from knowledge_agent.config import Settings
from knowledge_agent.runtime import create_runtime


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_api_contract() -> None:
    root = project_root()
    settings = Settings(
        qdrant_url=":memory:",
        corpus_path=root / "data" / "starter_corpus",
        graph_mode="core",
        llm_model="offline-rule-based",
    )
    runtime = create_runtime(settings=settings)
    runtime.ingest(recreate_collection=True)

    from knowledge_agent.api import app as app_module

    original_get_runtime = app_module.get_runtime
    app_module.get_runtime = lambda: runtime  # type: ignore[assignment]
    try:
        client = TestClient(app)
        response = client.post(
            "/chat",
            json={
                "session_id": "api-test",
                "message": "How should API keys be stored?",
            },
        )
    finally:
        app_module.get_runtime = original_get_runtime  # type: ignore[assignment]

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert any("faq-security-api-keys" in citation for citation in payload["citations"])
