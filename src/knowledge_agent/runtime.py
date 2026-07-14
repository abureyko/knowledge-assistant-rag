from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Any

from langsmith import traceable

from knowledge_agent.agents.core_graph import build_core_graph
from knowledge_agent.agents.model_gateway import ModelGateway
from knowledge_agent.config import Settings, get_settings
from knowledge_agent.ingestion.pipeline import run_ingestion
from knowledge_agent.retrieval.embeddings import build_embeddings_backend
from knowledge_agent.retrieval.qdrant_store import QdrantDocumentStore
from knowledge_agent.retrieval.retriever import Retriever


@dataclass
class AgentRuntime:
    settings: Settings
    store: QdrantDocumentStore
    retriever: Retriever
    model_gateway: ModelGateway
    graph_mode: str

    def __post_init__(self) -> None:
        # Compile the graph once so every answer follows the same validated workflow.
        self.graph = build_core_graph(
            retriever=self.retriever,
            model_gateway=self.model_gateway,
            settings=self.settings,
        )

    @traceable(name="knowledge-agent.ingest")
    def ingest(self, *, recreate_collection: bool = False) -> dict[str, Any]:
        return run_ingestion(
            corpus_path=self.settings.corpus_path,
            store=self.store,
            embeddings=self.retriever.embeddings,
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            recreate_collection=recreate_collection,
        )

    @traceable(name="knowledge-agent.answer")
    def answer(
        self,
        *,
        session_id: str,
        message: str,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not self.store.collection_exists():
            raise RuntimeError(
                f"Qdrant collection {self.store.collection_name!r} is missing. "
                "Run `knowledge-agent ingest` or `knowledge-agent reindex` first."
            )
        # This ID is returned even in offline mode, making each request easy to correlate.
        trace_id = str(uuid.uuid4())
        initial_state = {
            "session_id": session_id,
            "user_message": message,
            "filters": filters or {},
            "route": "research",
            "retrieved_chunks": [],
            "citations": [],
            "draft_answer": "",
            "final_answer": "",
            "status": "processing",
            "trace": [],
            "trace_id": trace_id,
        }
        result = self.graph.invoke(initial_state)
        return {
            "answer": result["final_answer"],
            "citations": result["citations"],
            "status": result["status"],
            "trace_id": result["trace_id"],
        }

    def ready(self) -> bool:
        return self.store.is_available()


def create_runtime(
    settings: Settings | None = None,
    *,
    graph_mode: str | None = None,
) -> AgentRuntime:
    """Assemble infrastructure and application services from one settings object."""
    settings = settings or get_settings()
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_TRACING"] = "true" if settings.langsmith_tracing else "false"
    os.environ["LANGCHAIN_TRACING_V2"] = "true" if settings.langsmith_tracing else "false"
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    mode = graph_mode or settings.graph_mode
    embeddings = build_embeddings_backend(settings)
    vector_size = getattr(embeddings, "embedding_size", None)
    store = QdrantDocumentStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=vector_size,
    )
    retriever = Retriever(store=store, embeddings=embeddings, default_top_k=settings.top_k)
    model_gateway = ModelGateway(settings=settings)
    return AgentRuntime(
        settings=settings,
        store=store,
        retriever=retriever,
        model_gateway=model_gateway,
        graph_mode=mode,
    )
