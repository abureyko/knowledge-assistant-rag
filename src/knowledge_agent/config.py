from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "knowledge-agent"
    graph_mode: Literal["core", "full"] = "core"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str = "offline-rule-based"
    embedding_model: str = "hash://v1"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "knowledge_agent_docs"
    langsmith_api_key: str | None = None
    langsmith_tracing: bool = False
    langsmith_project: str = "knowledge-agent-core"
    top_k: int = 4
    chunk_size: int = 500
    chunk_overlap: int = 80
    embedding_size: int = 48
    corpus_path: Path = Field(default_factory=lambda: _repo_root() / "data" / "starter_corpus")
    eval_dataset_path: Path = Field(
        default_factory=lambda: _repo_root() / "src" / "knowledge_agent" / "eval" / "dataset.jsonl"
    )

    @property
    def repo_root(self) -> Path:
        return _repo_root()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
