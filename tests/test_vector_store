"""Tests for the Chroma wrapper, with embed() mocked to a deterministic
fake so no model download is needed and results are predictable.
"""

from unittest.mock import patch

from src.vector_store import VectorStore


def _fake_vector(text: str) -> list[float]:
    # crude deterministic "embedding": more keyword overlap -> a vector
    # closer to other on-topic text. Good enough to prove retrieval
    # ordering works without a real model.
    keywords = ["fastapi", "path", "parameter"]
    score = sum(1.0 for k in keywords if k in text.lower())
    return [score, len(text) / 100]


@patch("src.vector_store.embed")
def test_add_and_query_round_trip(mock_embed):
    mock_embed.side_effect = lambda texts: [_fake_vector(t) for t in texts]

    store = VectorStore(collection_name="test_collection")
    store.add(
        ids=["a", "b"],
        texts=["FastAPI path parameters", "unrelated topic about cooking"],
        metadatas=[{"doc": "path-params.md"}, {"doc": "cooking.md"}],
    )

    assert store.count() == 2

    results = store.query("tell me about path parameters", n_results=1)

    assert len(results) == 1
    assert results[0]["metadata"]["doc"] == "path-params.md"


@patch("src.vector_store.embed")
def test_query_respects_n_results(mock_embed):
    mock_embed.side_effect = lambda texts: [_fake_vector(t) for t in texts]

    store = VectorStore(collection_name="test_collection_2")
    store.add(
        ids=["a", "b", "c"],
        texts=["FastAPI path parameters", "FastAPI query parameters", "cooking pasta"],
        metadatas=[{"doc": "1"}, {"doc": "2"}, {"doc": "3"}],
    )

    results = store.query("path parameter question", n_results=2)

    assert len(results) == 2
