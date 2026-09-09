"""Tests for the RAG pipeline, with Claude mocked out and a fake vector
store standing in for Chroma. No API key or model download needed.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.rag import answer_question


class _FakeStore:
    def __init__(self, hits):
        self._hits = hits

    def query(self, text, n_results=5):
        return self._hits


def _text_response(text):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


@patch("src.rag.anthropic.Anthropic")
def test_answer_question_returns_grounded_answer_and_sources(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.create.return_value = _text_response(
        "You declare it with no default value.\n\nSources: query-params.md"
    )

    hits = [
        {
            "text": "required query parameters have no default",
            "metadata": {"doc": "query-params.md"},
            "distance": 0.1,
        },
    ]
    store = _FakeStore(hits)

    result = answer_question("How do I make a query parameter required?", store)

    assert "no default value" in result["answer"]
    assert result["sources"] == ["query-params.md"]


@patch("src.rag.anthropic.Anthropic")
def test_answer_question_handles_no_hits_without_calling_claude(mock_anthropic_cls):
    store = _FakeStore([])

    result = answer_question("anything", store)

    assert result["sources"] == []
    assert result["hits"] == []
    mock_anthropic_cls.assert_not_called()


@patch("src.rag.anthropic.Anthropic")
def test_answer_question_dedupes_sources_across_multiple_hits(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.create.return_value = _text_response("answer text")

    hits = [
        {"text": "a", "metadata": {"doc": "body.md"}, "distance": 0.1},
        {"text": "b", "metadata": {"doc": "body.md"}, "distance": 0.2},
        {"text": "c", "metadata": {"doc": "handling-errors.md"}, "distance": 0.3},
    ]
    store = _FakeStore(hits)

    result = answer_question("q", store)

    assert result["sources"] == ["body.md", "handling-errors.md"]
