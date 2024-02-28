from unittest.mock import patch

import pytest

from promptulate.pydantic_v1 import ValidationError
from promptulate.tools.arxiv.api_wrapper import ArxivAPIWrapper


@pytest.fixture
def mock_search():
    class MockResult:
        def __init__(self):
            self.entry_id = "1"
            self.title = "Test Title"
            self.summary = "Test Summary"

    class MockSearch:
        @staticmethod
        def results():
            return iter([MockResult()])  # Returns a single MockResult instance

    return MockSearch()


@pytest.fixture
def arxiv_api_wrapper():
    return ArxivAPIWrapper(max_num_of_result=5)


def test_validate_environment_with_installed_package(arxiv_api_wrapper):
    assert isinstance(arxiv_api_wrapper, ArxivAPIWrapper)


def test_validate_environment_with_no_installed_package():
    with pytest.raises(ValidationError):
        ArxivAPIWrapper(max_num_of_result="invalid")


@patch("promptulate.tools.arxiv.api_wrapper.ArxivAPIWrapper._query")
def test_query_with_specified_fields(mock_query, arxiv_api_wrapper, mock_search):
    mock_query.return_value = mock_search
    result = arxiv_api_wrapper.query(
        "test keyword", specified_fields=["entry_id", "title", "summary"]
    )

    assert len(result) == 1
    assert result[0] == {
        "entry_id": "1",
        "title": "Test Title",
        "summary": "Test Summary",
    }


@patch("promptulate.tools.arxiv.api_wrapper.ArxivAPIWrapper._query")
def test_query_with_no_specified_fields(mock_query, arxiv_api_wrapper, mock_search):
    mock_query.return_value = mock_search
    result = arxiv_api_wrapper.query("test keyword")

    assert len(result) == 1
    assert result[0] == {
        "entry_id": "1",
        "title": "Test Title",
        "summary": "Test Summary",
    }
