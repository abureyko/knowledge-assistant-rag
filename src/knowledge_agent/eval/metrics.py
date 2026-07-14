# ruff: noqa: F401,F841
from __future__ import annotations


def score_example(example: dict, result: dict) -> dict:
    expected_status = example["expected_status"]
    actual_status = result.get("status")
    status_match = actual_status == expected_status

    expected_doc_ids = example.get("expected_doc_ids", [])
    citations = result.get("citations", [])
    if expected_doc_ids:
        citation_match = any(
            expected_doc_id in citation
            for expected_doc_id in expected_doc_ids
            for citation in citations
        )
    else:
        citation_match = not citations

    passed = status_match and (citation_match if expected_status == "ok" else True)
    return {
        "question_id": example.get("question_id"),
        "expected_status": expected_status,
        "actual_status": actual_status,
        "status_match": status_match,
        "citation_match": citation_match,
        "passed": passed,
        "expected_doc_ids": expected_doc_ids,
        "citations": citations,
    }


def summarize(scores: list[dict]) -> dict:
    total = len(scores)
    passed = sum(1 for score in scores if score["passed"])
    status_matches = sum(1 for score in scores if score["status_match"])
    citation_scored = [score for score in scores if score["expected_status"] == "ok"]
    citation_matches = sum(1 for score in citation_scored if score["citation_match"])

    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0.0,
        "status_accuracy": status_matches / total if total else 0.0,
        "citation_accuracy": citation_matches / len(citation_scored)
        if citation_scored
        else 0.0,
    }
