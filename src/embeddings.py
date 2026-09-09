"""Wraps the embedding model used to turn text into vectors.

Uses a local, free sentence-transformers model -- no API key required.
Claude doesn't have a first-party embeddings endpoint, so embeddings
and generation are deliberately split across two different tools in
this project: this module handles embeddings, src/rag.py calls Claude
for the actual answer.
"""

from functools import lru_cache

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model():
    # imported lazily so importing this module doesn't force a model
    # download, and so tests can mock this function without needing
    # sentence-transformers installed at all.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def embed(texts: list[str]) -> list[list[float]]:
    """Embeds a batch of strings. Returns one vector per input string."""
    model = _get_model()
    return model.encode(texts, convert_to_numpy=True).tolist()


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
