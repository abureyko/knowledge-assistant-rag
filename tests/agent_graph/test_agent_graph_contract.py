from pathlib import Path

from knowledge_agent.config import Settings
from knowledge_agent.runtime import create_runtime


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_agent_graph_contract() -> None:
    root = project_root()
    settings = Settings(
        qdrant_url=":memory:",
        corpus_path=root / "data" / "starter_corpus",
        graph_mode="core",
        llm_model="offline-rule-based",
    )
    runtime = create_runtime(settings=settings)
    runtime.ingest(recreate_collection=True)

    response = runtime.answer(
        session_id="agent-graph-test",
        message="When should I start a deployment rollback?",
        filters={"topic": "deployments"},
    )

    assert response["status"] == "ok"
    assert any("runbook-deploy-rollback" in citation for citation in response["citations"])
