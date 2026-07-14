# ruff: noqa: F401,F841
from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from knowledge_agent.config import get_settings
from knowledge_agent.eval.runner import run_evaluation
from knowledge_agent.runtime import create_runtime

app = typer.Typer(help="Knowledge agent CLI.")


def _runtime():
    return create_runtime(settings=get_settings())


def _echo_json(payload: dict) -> None:
    typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))


@app.command()
def ingest(
    recreate: Annotated[
        bool,
        typer.Option(
            help="Recreate the Qdrant collection before indexing.",
        ),
    ] = False,
) -> None:
    runtime = _runtime()
    result = runtime.ingest(recreate_collection=recreate)
    _echo_json(result)


@app.command()
def reindex() -> None:
    runtime = _runtime()
    result = runtime.ingest(recreate_collection=True)
    _echo_json(result)


@app.command("chat-demo")
def chat_demo(
    question: Annotated[str, typer.Option("--question")] = "How do I enable MFA?",
) -> None:
    runtime = _runtime()
    try:
        result = runtime.answer(session_id="cli-demo", message=question, filters=None)
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    _echo_json(result)


@app.command()
def eval(
    output_path: Annotated[
        Path,
        typer.Option(help="Where to save eval."),
    ] = Path("reports/eval_report.json"),
) -> None:
    runtime = _runtime()
    settings = get_settings()
    report = run_evaluation(runtime=runtime, dataset_path=settings.eval_dataset_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _echo_json(report["summary"])


if __name__ == "__main__":
    app()
