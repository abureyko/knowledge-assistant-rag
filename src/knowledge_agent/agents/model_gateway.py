# ruff: noqa: F401,F841
from __future__ import annotations

import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import OpenAIError

from knowledge_agent.agents.prompts import REVIEWER_PROMPT, SUPERVISOR_PROMPT, WRITER_PROMPT
from knowledge_agent.retrieval.retriever import RetrievedChunk, extract_keywords, lexical_overlap


class ModelGateway:
    def __init__(self, *, settings) -> None:
        self.settings = settings
        self._chat_model = None
        if settings.llm_model != "offline-rule-based" and settings.llm_api_key:
            self._chat_model = ChatOpenAI(
                model=settings.llm_model,
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url,
                temperature=0,
            )

    def _invoke(self, system_prompt: str, user_prompt: str) -> str:
        if self._chat_model is None:
            return ""
        try:
            response = self._chat_model.invoke(
                [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            )
        except OpenAIError:
            return ""
        return str(response.content).strip()

    def route(self, question: str) -> str:
        normalized = question.strip().lower()
        if _is_ambiguous_question(normalized):
            return "clarify"
        if self._chat_model is None:
            return "research" if _looks_like_internal_question(normalized) else "refuse"
        response = self._invoke(SUPERVISOR_PROMPT, _build_supervisor_prompt(question))
        return _parse_route_response(response)

    def draft_answer(self, question: str, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "I do not have enough retrieved context to answer this question."
        if self._chat_model is not None:
            context = _format_retrieved_context(chunks)
            response = self._invoke(
                WRITER_PROMPT,
                f"Question:\n{question}\n\nRetrieved context:\n{context}",
            )
            if response:
                return response

        candidate_chunks = chunks
        normalized_question = question.lower()
        if "when" in normalized_question or "start" in normalized_question:
            trigger_chunks = [
                chunk for chunk in chunks if "trigger condition" in chunk.text.lower()
            ]
            candidate_chunks = trigger_chunks or chunks

        best_chunk = max(
            candidate_chunks,
            key=lambda chunk: (lexical_overlap(question, chunk), chunk.score),
        )
        snippet = _first_relevant_sentences(best_chunk.text)
        return snippet or best_chunk.text.strip()

    def review_answer(self, question: str, draft_answer: str, chunks: list[RetrievedChunk]) -> str:
        if self._chat_model is None:
            return draft_answer
        context = _format_retrieved_context(chunks)
        response = self._invoke(
            REVIEWER_PROMPT,
            f"Question:\n{question}\n\nDraft answer:\n{draft_answer}\n\nContext:\n{context}",
        )
        if not response or _looks_like_review_commentary(response):
            return draft_answer
        return response


def _build_supervisor_prompt(question: str) -> str:
    return (
        "Question:\n"
        f"{question}\n\n"
        "Choose route:\n"
        "- research: internal policy, guide, FAQ, runbook, release note question\n"
        "- clarify: too broad or missing a specific topic\n"
        "- refuse: outside the internal knowledge base\n"
        "Return only the route token."
    )


def _parse_route_response(response: str) -> str:
    normalized = response.strip().lower()
    for route in ("clarify", "research", "refuse"):
        if re.search(rf"\b{route}\b", normalized):
            return route
    return "refuse"


def _format_retrieved_context(chunks: list[RetrievedChunk]) -> str:
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(
            f"[{index}] {chunk.citation}\n"
            f"score={chunk.score:.4f}\n"
            f"{chunk.text.strip()}"
        )
    return "\n\n".join(blocks)


def _looks_like_review_commentary(answer: str) -> bool:
    normalized = answer.strip().lower()
    commentary_markers = (
        "the draft",
        "the answer is",
        "grounded",
        "not grounded",
        "review",
    )
    return any(marker in normalized for marker in commentary_markers)


def _is_ambiguous_question(normalized_question: str) -> bool:
    words = re.findall(r"[a-z0-9-]+", normalized_question)
    if len(words) <= 3 and any(
        topic in normalized_question
        for topic in ("access", "billing", "deployments", "integrations", "security")
    ):
        return True
    broad_patterns = (
        r"^what about\b",
        r"^tell me about\b",
        r"^explain\b",
        r"^help me with\b",
        r"\bprocess work\b",
        r"\bthis .+ thing\b",
    )
    return any(re.search(pattern, normalized_question) for pattern in broad_patterns)


def _looks_like_internal_question(normalized_question: str) -> bool:
    internal_terms = {
        "access",
        "admin",
        "api",
        "audit",
        "billing",
        "contracted",
        "customer",
        "deploy",
        "deployment",
        "deployments",
        "dispute",
        "feature",
        "flag",
        "github",
        "hotfix",
        "invoice",
        "invoices",
        "logs",
        "monthly",
        "key",
        "keys",
        "maintenance",
        "multi-factor",
        "overage",
        "preview",
        "pull",
        "mfa",
        "production",
        "rollback",
        "runbook",
        "secret",
        "security",
        "service",
        "severity",
        "slack",
        "sso",
        "usage",
        "webhook",
    }
    outside_terms = {"weather", "stock", "sports", "recipe", "movie", "flight"}
    keywords = extract_keywords(normalized_question)
    return bool(keywords & internal_terms) and not bool(keywords & outside_terms)


def _first_relevant_sentences(text: str, *, max_sentences: int = 3) -> str:
    cleaned = re.sub(r"^#+\s+.*$", "", text.strip(), flags=re.MULTILINE)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    selected = [sentence.strip() for sentence in sentences if sentence.strip()]
    return " ".join(selected[:max_sentences])
