from __future__ import annotations

from typing import Any, Literal, TypedDict

from knowledge_agent.retrieval.retriever import RetrievedChunk


class AgentState(TypedDict):
    session_id: str
    user_message: str
    filters: dict[str, Any]
    route: Literal["clarify", "research", "refuse", "finalize"]
    retrieved_chunks: list[RetrievedChunk]
    citations: list[str]
    draft_answer: str
    final_answer: str
    status: str
    trace: list[str]
    trace_id: str
