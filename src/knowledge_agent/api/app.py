# ruff: noqa: F401,F841
from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from knowledge_agent.config import get_settings
from knowledge_agent.runtime import create_runtime


class ChatRequest(BaseModel):
    session_id: str = Field(..., examples=["demo-session"])
    message: str
    filters: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    status: str
    trace_id: str


@lru_cache(maxsize=1)
def get_runtime():
    # Build the Qdrant client and graph lazily, then reuse them across requests.
    return create_runtime(settings=get_settings())


app = FastAPI(title="Knowledge Agent", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    # Liveness is intentionally independent from external services.
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    # Readiness reports whether Qdrant is reachable; indexing is a separate operation.
    runtime = get_runtime()
    if not runtime.ready():
        raise HTTPException(status_code=503, detail="Runtime dependencies are not ready.")
    return {"status": "ready"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    runtime = get_runtime()
    try:
        result = runtime.answer(
            session_id=request.session_id,
            message=request.message,
            filters=request.filters,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ChatResponse(**result)
