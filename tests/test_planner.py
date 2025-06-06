import pytest
from unittest.mock import Mock

from episteme.logic import Planner


def test_add_task_returns_concepts():
    mock_client = Mock()
    mock_client.get_concepts.return_value = ["engine", "aerodynamics"]

    planner = Planner(client=mock_client)
    result = planner.add_task("build a car")

    assert result == ["engine", "aerodynamics"]
    mock_client.get_concepts.assert_called_once_with("build a car")


def test_add_task_handles_empty_response():
    mock_client = Mock()
    mock_client.get_concepts.return_value = []

    planner = Planner(client=mock_client)
    result = planner.add_task("nonsense task")

    assert result == []
    mock_client.get_concepts.assert_called_once()
