# ruff: noqa: F401,F841
from __future__ import annotations


def build_refusal_message() -> str:
    return (
        "I do not have enough grounded information in the internal knowledge base to answer "
        "that confidently."
    )


def build_clarification_message() -> str:
    return (
        "Please narrow the question to a specific topic, document type, product area, "
        "or operational procedure."
    )


def is_insufficient_answer(answer: str) -> bool:
    normalized = answer.strip().lower()
    if not normalized:
        return True
    insufficient_markers = (
        "not enough",
        "insufficient",
        "cannot answer",
        "do not have enough",
        "don't have enough",
    )
    return any(marker in normalized for marker in insufficient_markers)


def ensure_citations(answer: str, citations: list[str]) -> str:
    if not citations:
        return answer
    if "sources:" in answer.lower():
        return answer
    sources = "; ".join(citations)
    return f"{answer.rstrip()}\n\nSources: {sources}"
