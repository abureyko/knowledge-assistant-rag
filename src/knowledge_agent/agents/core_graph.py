# ruff: noqa: F401,F841
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from knowledge_agent.agents.guardrails import (
    build_clarification_message,
    build_refusal_message,
    ensure_citations,
    is_insufficient_answer,
)
from knowledge_agent.agents.state import AgentState
from knowledge_agent.retrieval.retriever import is_grounded_match, supporting_citations


def build_core_graph(*, retriever, model_gateway, settings):
    """Compile the deterministic supervisor-to-guardrails RAG workflow."""

    def supervisor_node(state: AgentState) -> AgentState:
        route = model_gateway.route(state["user_message"])
        next_state = dict(state)
        next_state["route"] = route
        next_state["trace"] = [*state["trace"], f"supervisor:{route}"]
        if route == "clarify":
            next_state["draft_answer"] = build_clarification_message()
            next_state["final_answer"] = next_state["draft_answer"]
            next_state["status"] = "clarify"
        elif route == "refuse":
            next_state["draft_answer"] = build_refusal_message()
            next_state["final_answer"] = next_state["draft_answer"]
            next_state["status"] = "refuse"
        return next_state

    def research_node(state: AgentState) -> AgentState:
        if state["route"] != "research":
            return state

        chunks = retriever.retrieve(
            state["user_message"],
            filters=state["filters"] or None,
            top_k=settings.top_k,
        )
        next_state = dict(state)
        next_state["retrieved_chunks"] = chunks
        next_state["citations"] = supporting_citations(state["user_message"], chunks)
        next_state["trace"] = [*state["trace"], f"research:{len(chunks)}"]
        if not chunks or not is_grounded_match(state["user_message"], chunks):
            next_state["route"] = "refuse"
            next_state["draft_answer"] = build_refusal_message()
            next_state["final_answer"] = next_state["draft_answer"]
            next_state["status"] = "refuse"
        return next_state

    def writer_node(state: AgentState) -> AgentState:
        if state["route"] == "clarify":
            return state
        if state["route"] == "refuse":
            return state

        draft = model_gateway.draft_answer(state["user_message"], state["retrieved_chunks"])
        reviewed = model_gateway.review_answer(
            state["user_message"],
            draft,
            state["retrieved_chunks"],
        )
        next_state = dict(state)
        next_state["draft_answer"] = draft
        next_state["final_answer"] = reviewed
        next_state["status"] = "ok"
        next_state["trace"] = [*state["trace"], "writer:ok"]
        return next_state

    def guardrails_node(state: AgentState) -> AgentState:
        next_state = dict(state)
        if state["route"] == "clarify":
            next_state["final_answer"] = build_clarification_message()
            next_state["status"] = "clarify"
        elif state["route"] == "refuse" or is_insufficient_answer(state["final_answer"]):
            next_state["final_answer"] = build_refusal_message()
            next_state["status"] = "refuse"
        elif not state["citations"]:
            next_state["final_answer"] = build_refusal_message()
            next_state["status"] = "refuse"
        else:
            next_state["final_answer"] = ensure_citations(state["final_answer"], state["citations"])
            next_state["status"] = "ok"
        next_state["trace"] = [*state["trace"], f"guardrails:{next_state['status']}"]
        return next_state

    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_node)
    graph.add_node("writer", writer_node)
    graph.add_node("guardrails", guardrails_node)
    # Nodes always run in this order; route values decide which nodes perform work.
    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "research")
    graph.add_edge("research", "writer")
    graph.add_edge("writer", "guardrails")
    graph.add_edge("guardrails", END)
    return graph.compile()
