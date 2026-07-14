from pathlib import Path


def project_root() -> Path:
    return next(
        path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
    )


def test_project_shape_and_imports() -> None:
    root = project_root()
    corpus = list((root / "data" / "starter_corpus").glob("*.md"))

    assert (root / ".env.example").exists()
    assert (root / "Dockerfile").exists()
    assert (root / "docker-compose.yml").exists()
    assert (root / "README.md").exists()
    assert len(corpus) >= 10

    import knowledge_agent  # noqa: F401
    import knowledge_agent.api.app  # noqa: F401
    import knowledge_agent.cli.main  # noqa: F401
