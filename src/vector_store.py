"""Thin wrapper around a local Chroma collection.

Keeping this as a small add/query wrapper instead of scattering
chromadb calls throughout the codebase makes it easy to test with a
mocked embedding function, and easy to swap in a different vector
store later (pgvector, etc.) without touching the RAG pipeline.
"""

import chromadb

from src.embeddings import embed


class VectorStore:
    def __init__(self, collection_name: str = "docs", persist_dir: str | None = None):
        if persist_dir:
            self._client = chromadb.PersistentClient(path=persist_dir)
        else:
            self._client = chromadb.EphemeralClient()
        self._collection = self._client.get_or_create_collection(collection_name)

    def add(self, ids: list[str], texts: list[str], metadatas: list[dict]) -> None:
        embeddings = embed(texts)
        self._collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    def query(self, text: str, n_results: int = 5) -> list[dict]:
        query_embedding = embed([text])[0]
        results = self._collection.query(query_embeddings=[query_embedding], n_results=n_results)
        hits = []
        for i in range(len(results["ids"][0])):
            hits.append(
                {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
            )
        return hits

    def count(self) -> int:
        return self._collection.count()
