from pathlib import Path

from knowledge_agent.config import Settings
from knowledge_agent.eval.runner import run_evaluation
from knowledge_agent.runtime import create_runtime


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_eval_contract() -> None:
    root = project_root()
    settings = Settings(
        qdrant_url=":memory:",
        corpus_path=root / "data" / "starter_corpus",
        graph_mode="core",
        llm_model="offline-rule-based",
        eval_dataset_path=root / "src" / "knowledge_agent" / "eval" / "dataset.jsonl",
    )
    runtime = create_runtime(settings=settings)
    runtime.ingest(recreate_collection=True)

    report = run_evaluation(runtime=runtime, dataset_path=settings.eval_dataset_path)

    assert report["summary"]["total"] >= 30
    assert "pass_rate" in report["summary"]
