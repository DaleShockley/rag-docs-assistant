"""Scores retrieval quality (not generation) for each chunking strategy.

For each question in eval/qa_set.json, checks whether the expected
source doc shows up among the top-k retrieved chunks. This measures
the retrieval step in isolation -- no Claude calls or API key needed,
just the local embedding model.

Run with: python -m eval.score_retrieval
"""

import json
from pathlib import Path

from src.ingest import build_chunks
from src.vector_store import VectorStore

QA_SET_PATH = Path(__file__).parent / "qa_set.json"


def load_qa_set() -> list[dict]:
    return json.loads(QA_SET_PATH.read_text())


def build_store(strategy: str) -> VectorStore:
    chunks = build_chunks()[strategy]
    store = VectorStore(collection_name=f"eval_{strategy}")
    store.add(
        ids=[f"{c.doc}-{c.chunk_id}" for c in chunks],
        texts=[c.text for c in chunks],
        metadatas=[{"doc": c.doc, "chunk_id": c.chunk_id} for c in chunks],
    )
    return store


def hit_rate_at_k(store, qa_set: list[dict], k: int) -> dict:
    """Fraction of questions where the expected doc appears in the top-k hits."""
    hits = 0
    misses = []
    for item in qa_set:
        results = store.query(item["question"], n_results=k)
        retrieved_docs = {r["metadata"]["doc"] for r in results}
        if item["expected_doc"] in retrieved_docs:
            hits += 1
        else:
            misses.append(item["question"])
    return {
        "hit_rate": hits / len(qa_set) if qa_set else 0.0,
        "hits": hits,
        "total": len(qa_set),
        "misses": misses,
    }


def run_comparison() -> dict:
    qa_set = load_qa_set()
    results = {}
    for strategy in ("fixed", "header"):
        store = build_store(strategy)
        results[strategy] = {
            "hit_rate@3": hit_rate_at_k(store, qa_set, k=3),
            "hit_rate@5": hit_rate_at_k(store, qa_set, k=5),
        }
    return results


if __name__ == "__main__":
    for strategy, metrics in run_comparison().items():
        print(f"\n{strategy} chunking:")
        for metric_name, stats in metrics.items():
            print(f"  {metric_name}: {stats['hits']}/{stats['total']} ({stats['hit_rate']:.0%})")
            if stats["misses"]:
                print(f"    missed: {stats['misses']}")
