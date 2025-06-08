import pytest
from episteme.cli.main import main
from episteme.models import Concept

def test_cli_task_flow(monkeypatch):
    prompts = iter([
        "learn LangGraph",  # task
        True,               # Do you know concept A? (yes)
        "",                 # notes for concept A
        False,              # concept B
        "I need to study this",  # notes for concept B
    ])

    def mock_ask(*args, **kwargs):
        return next(prompts)

    monkeypatch.setattr("questionary.text", lambda *a, **kw: type("Q", (), {"ask": mock_ask})())
    monkeypatch.setattr("questionary.confirm", lambda *a, **kw: type("Q", (), {"ask": mock_ask})())

    # patch planner.add_task to return mock concepts
    from episteme.logic import Planner
    monkeypatch.setattr(Planner, "add_task", lambda self, task: [Concept("A"), Concept("B")])

    main()
