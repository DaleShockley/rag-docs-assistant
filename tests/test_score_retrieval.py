"""Tests for the hit-rate@k scoring math, using a fake store so this
runs with no embedding model and no network involved.
"""

from eval.score_retrieval import hit_rate_at_k


class _FakeStore:
    def __init__(self, responses: dict[str, list[str]]):
        # responses: {question: [doc_names_in_rank_order]}
        self._responses = responses

    def query(self, text, n_results=5):
        docs = self._responses.get(text, [])[:n_results]
        return [{"metadata": {"doc": d}} for d in docs]


def test_hit_rate_at_k_counts_correct_and_missed():
    qa_set = [
        {"question": "q1", "expected_doc": "a.md"},
        {"question": "q2", "expected_doc": "b.md"},
    ]
    store = _FakeStore({"q1": ["a.md", "c.md"], "q2": ["c.md", "d.md"]})

    result = hit_rate_at_k(store, qa_set, k=2)

    assert result["hits"] == 1
    assert result["total"] == 2
    assert result["hit_rate"] == 0.5
    assert result["misses"] == ["q2"]


def test_hit_rate_at_k_perfect_score():
    qa_set = [{"question": "q1", "expected_doc": "a.md"}]
    store = _FakeStore({"q1": ["a.md"]})

    result = hit_rate_at_k(store, qa_set, k=3)

    assert result["hit_rate"] == 1.0
    assert result["misses"] == []


def test_hit_rate_at_k_respects_k_cutoff():
    # expected doc is retrieved, but only at rank 3 -- shouldn't count for k=2
    qa_set = [{"question": "q1", "expected_doc": "a.md"}]
    store = _FakeStore({"q1": ["x.md", "y.md", "a.md"]})

    result = hit_rate_at_k(store, qa_set, k=2)

    assert result["hit_rate"] == 0.0
    assert result["misses"] == ["q1"]
