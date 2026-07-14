# ruff: noqa: F401,F841
from __future__ import annotations

import json
from pathlib import Path

from knowledge_agent.eval.metrics import score_example, summarize


def run_evaluation(*, runtime, dataset_path: Path) -> dict:
    examples: list[dict] = []
    results: list[dict] = []
    scores: list[dict] = []

    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        example = json.loads(line)
        result = runtime.answer(
            session_id=example["question_id"],
            message=example["question"],
            filters=example.get("filters"),
        )
        score = score_example(example, result)
        examples.append(example)
        results.append(
            {
                "question_id": example["question_id"],
                "question": example["question"],
                "result": result,
                "score": score,
            }
        )
        scores.append(score)

    return {
        "dataset_path": str(dataset_path),
        "summary": summarize(scores),
        "results": results,
        "examples": examples,
    }
