"""Tests for the embeddings wrapper, with the model mocked out.

No download or GPU needed -- these just check that embed()/embed_one()
shape their inputs and outputs correctly.
"""

from unittest.mock import MagicMock, patch

from src.embeddings import embed, embed_one


@patch("src.embeddings._get_model")
def test_embed_returns_one_vector_per_text(mock_get_model):
    mock_model = MagicMock()
    mock_model.encode.return_value.tolist.return_value = [[0.1, 0.2], [0.3, 0.4]]
    mock_get_model.return_value = mock_model

    vectors = embed(["hello", "world"])

    assert len(vectors) == 2
    mock_model.encode.assert_called_once()


@patch("src.embeddings._get_model")
def test_embed_one_returns_single_vector(mock_get_model):
    mock_model = MagicMock()
    mock_model.encode.return_value.tolist.return_value = [[0.5, 0.6]]
    mock_get_model.return_value = mock_model

    vector = embed_one("hello")

    assert vector == [0.5, 0.6]
