from typer.testing import CliRunner

from knowledge_agent.cli.main import app


class FakeRuntime:
    def ingest(self, *, recreate_collection: bool = False):
        return {
            "documents": 22,
            "chunks": 70,
            "collection_size": 70,
            "recreate": recreate_collection,
        }

    def answer(self, *, session_id: str, message: str, filters):
        return {
            "answer": f"stubbed answer for {message}",
            "citations": ["doc-1 · Stub · Overview"],
            "status": "ok",
            "trace_id": session_id,
        }


def test_cli_contract(monkeypatch) -> None:
    runner = CliRunner()

    monkeypatch.setattr(
        "knowledge_agent.cli.main.create_runtime",
        lambda *args, **kwargs: FakeRuntime(),
    )
    monkeypatch.setattr("knowledge_agent.cli.main.get_settings", lambda: object())

    ingest_result = runner.invoke(app, ["ingest"])
    chat_result = runner.invoke(app, ["chat-demo", "--question", "demo"])

    assert ingest_result.exit_code == 0
    assert '"documents": 22' in ingest_result.stdout
    assert chat_result.exit_code == 0
    assert "stubbed answer for demo" in chat_result.stdout
