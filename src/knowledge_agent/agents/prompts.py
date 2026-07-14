"""Prompt contracts used by the model gateway."""

SUPERVISOR_PROMPT = """Route the user question for an internal knowledge-base RAG system.
Return exactly one route token: research, clarify, or refuse."""

WRITER_PROMPT = """Answer only from the retrieved internal context.
Do not add facts that are not supported by the context. Keep the answer concise and cite sources."""

REVIEWER_PROMPT = """Review whether the draft answer is grounded in the retrieved context.
Return the answer unchanged when it is grounded; otherwise say that the context is insufficient."""
