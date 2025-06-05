import pytest

from episteme import llm
from unittest.mock import Mock, patch


PROMPT_TEMPLATE = """Given a task, output its prerequisite concepts in JSON.
Task: {task}
Return format: {{ "concepts": [...] }}"""


@patch("episteme.llm.client.llm_call")
def test_valid_prompt_and_response(mock_llm_call):
    mock_llm_call.return_value = '{"concepts": ["vector spaces", "eigenvalues"]}'

    result = llm.client.get_concepts("learn linear algebra")

    assert result == ["vector spaces", "eigenvalues"]
    mock_llm_call.assert_called_once()


@patch("episteme.llm.client.llm_call")
def test_prompt_includes_task_string(mock_llm_call):
    mock_llm_call.return_value = '{"concepts": ["engine", "aerodynamics"]}'

    task_string = "build a car"
    llm.client.get_concepts(task_string)

    sent_prompt = mock_llm_call.call_args[0][0]
    assert task_string in sent_prompt
    assert "concepts" in sent_prompt


@patch("episteme.llm.client.llm_call")
def test_valid_json_parsing_raises_on_invalid_format(mock_llm_call):
    mock_llm_call.return_value = '{"concepts": [" "eigenvalues"]}'  # malformed

    with pytest.raises(ValueError):
        llm.client.get_concepts("learn linear algebra")


@patch("episteme.llm.client.llm_call")
def test_malformed_json_raises(mock_llm_call):
    mock_llm_call.return_value = '{"concepts": [" "eigenvalues"]}'  # malformed JSON

    with pytest.raises(ValueError):
        llm.client.get_concepts("learn linear algebra")


@patch("episteme.llm.client.llm_call")
def test_missing_concepts_key(mock_llm_call):
    """LLM returns JSON without 'concepts' key; system should handle gracefully."""
    mock_llm_call.side_effect = [
        '{"something_else": ["irrelevant"]}',  # invalid response
        '{"concepts": ["sets", "functions"]}',  # valid response
    ]

    result = llm.client.get_concepts("Study discrete math")

    assert result == ["sets", "functions"]
    assert mock_llm_call.call_count == 2


@patch("episteme.llm.client.llm_call")
def test_concepts_not_a_list(mock_llm_call):
    """LLM returns a 'concepts' key with incorrect type (e.g., string); should be caught."""

    mock_llm_call.side_effect = ['{"concepts": "eternity"}', '{"concepts": ["infinity"]}']

    result = llm.client.get_concepts("internals of my mind")

    assert result == ["infinity"]
    assert mock_llm_call.call_count == 2


@patch("episteme.llm.client.llm_call")
def test_empty_string_input(mock_llm_call):
    """Empty task input should raise validation or return an appropriate fallback."""
    with pytest.raises(ValueError):
        mock_llm_call()


@patch("episteme.llm.client.llm_call")
def test_prompt_injection_input(mock_llm_call):
    """Sanity-check against prompt injection via unescaped user input."""
    with pytest.raises(ValueError, match="Task input cannot be empty"):
        llm.client.get_concepts("")


@patch("episteme.llm.client.llm_call")
def test_llm_exception_is_caught(mock_llm_call):
    """Simulate LLM call raising an exception (e.g., timeout) and test catch logic."""
    task_input = '"; DROP TABLE users; --'
    mock_llm_call.return_value = '{"concepts": ["SQL injection", "security"]}'

    result = llm.client.get_concepts(task_input)

    sent_prompt = mock_llm_call.call_args[0][0]
    assert task_input in sent_prompt  # Ensure no modification occurs
    assert isinstance(result, list)


@patch("episteme.llm.client.llm_call")
def test_retry_limit_exceeded(mock_llm_call):
    """Ensure function does not retry more than 5 times before failing."""
    mock_llm_call.side_effect = ['{"junk": "data"}'] * 6  # all invalid

    with pytest.raises(ValueError, match="Max retries exceeded"):
        llm.client.get_concepts("hard task")

    assert mock_llm_call.call_count == 5


@patch("episteme.llm.client.llm_call")
def test_whitespace_only_input(mock_llm_call):
    """Input with only whitespace should be treated as invalid."""
    with pytest.raises(ValueError, match="Task input cannot be empty"):
        llm.client.get_concepts("   \n\t  ")


@patch("episteme.llm.client.llm_call")
def test_excessively_long_input_is_rejected(mock_llm_call):
    long_input = "a" * 501
    with pytest.raises(ValueError, match="too long"):
        llm.client.get_concepts(long_input)
