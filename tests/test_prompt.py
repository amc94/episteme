import pytest
from episteme.prompt import PromptBuilder


def test_task_prompt_basic_render():
    task = "Build a LangGraph-based planner"
    builder = PromptBuilder(use_cot=False)

    prompt = builder.build_prompt("task", task)

    assert "LangGraph" in prompt
    assert "concepts" in prompt
    assert '{"concepts":' not in prompt  # should not pre-fill JSON
    assert "Task:" in prompt
    assert "Response:" in prompt


def test_task_prompt_with_cot():
    task = "Build a transformer model"
    builder = PromptBuilder(use_cot=False)

    prompt = builder.build_prompt("task", task)

    assert "step by step" in prompt.lower() or "think" in prompt.lower()


def test_task_prompt_no_missing_fields():
    task = "Learn probability"
    builder = PromptBuilder(use_cot=False)

    prompt = builder.build_prompt("task", task)
    for required_phrase in ["Task:", "Response:", "Return only valid JSON"]:
        assert required_phrase in prompt
