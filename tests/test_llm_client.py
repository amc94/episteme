import json
import pytest
import requests

from unittest.mock import patch, Mock
from episteme.llm.client import Client

client = Client(api_url="http://mocked")


def mock_llm_response(concepts: list[str], key: str = "concepts") -> str:
    return json.dumps({"response": json.dumps({ key : concepts})})

@patch("episteme.llm.client.requests.post")
def test_get_concepts_parses_response_correctly(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = mock_llm_response(["vector spaces", "eigenvalues"])

    result = client.get_concepts("learn linear algebra")

    assert result == ["vector spaces", "eigenvalues"]
    mock_post.assert_called_once()
    assert "vector spaces" in result and "eigenvalues" in result

@patch("episteme.llm.client.requests.post")
def test_valid_json_parsing_raises_on_invalid_format(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = '"response": {"concepts": [" "eigenvalues"]}}'  # malformed JSON

    with pytest.raises(ValueError):
        client.get_concepts("learn linear algebra")


@patch("episteme.llm.client.requests.post")
def test_malformed_json_raises(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = '"response": {"concepts": [" "eigenvalues"]}}'  # malformed

    with pytest.raises(ValueError):
        client.get_concepts("learn linear algebra")


@patch("episteme.llm.client.requests.post")
def test_missing_concepts_key(mock_post):
    mock_post.side_effect = [
        Mock(status_code=200, text=mock_llm_response(["sets", "functions"], "wrong")),
        Mock(status_code=200, text=mock_llm_response(["sets", "functions"])),
    ]

    result = client.get_concepts("Study discrete math")
    assert result == ["sets", "functions"]
    assert mock_post.call_count == 2


@patch("episteme.llm.client.requests.post")
def test_concepts_not_a_list(mock_post):
    mock_post.side_effect = [
        Mock(status_code=200, text=mock_llm_response("sets")),
        Mock(status_code=200, text=mock_llm_response(["infinity"])),
    ]

    result = client.get_concepts("internals of my mind")
    assert result == ["infinity"]
    assert mock_post.call_count == 2


@patch("episteme.llm.client.requests.post")
def test_llm_exception_is_caught(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("timeout")
    with pytest.raises(ValueError):
        client.get_concepts("edge case test")


@patch("episteme.llm.client.requests.post")
def test_retry_limit_exceeded(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = "{}"

    with pytest.raises(ValueError):
        client.get_concepts("task with invalid responses")
