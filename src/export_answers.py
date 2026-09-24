"""Runs a list of questions through the RAG pipeline and exports every
answer -- with the exact chunks it was grounded on -- as JSONL.

This is the hand-off point to downstream evaluation (e.g. an LLM judge):
the consumer only needs this file, not this codebase.

    python -m src.export_answers questions.json answers.jsonl [--strategy header] [--model ...]

questions.json is a list of {"id": ..., "question": ..., ...}; any extra
fields are passed through to the output unchanged.
"""

import argparse
import json
import re
from pathlib import Path

from src.ingest import build_chunks
from src.rag import MODEL, answer_question
from src.vector_store import VectorStore

_SOURCES_LINE = re.compile(r"^\s*\**Sources:?\**:?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
_DOC_NAME = re.compile(r"[\w.-]+\.md\b")


def parse_cited_sources(answer: str) -> list[str]:
    """Pulls the doc names out of the model's own "Sources:" line (the last one wins)."""
    matches = _SOURCES_LINE.findall(answer)
    if not matches:
        return []
    # Only filenames count: the model sometimes writes prose here ("None of the excerpts...").
    return _DOC_NAME.findall(matches[-1])


def build_store(strategy: str) -> VectorStore:
    chunks = build_chunks()[strategy]
    store = VectorStore(collection_name=f"docs_{strategy}")
    store.add(
        ids=[f"{c.doc}-{c.chunk_id}" for c in chunks],
        texts=[c.text for c in chunks],
        metadatas=[{"doc": c.doc, "chunk_id": c.chunk_id} for c in chunks],
    )
    return store


def export(questions: list[dict], store: VectorStore, strategy: str, model: str) -> list[dict]:
    records = []
    for q in questions:
        result = answer_question(q["question"], store, model=model)
        records.append(
            {
                **q,
                "answer": result["answer"],
                "cited_sources": parse_cited_sources(result["answer"]),
                "retrieved": [
                    {"doc": h["metadata"].get("doc", "unknown"), "text": h["text"]}
                    for h in result["hits"]
                ],
                "generator_model": model,
                "chunking": strategy,
            }
        )
        print(f"  {q['id']}: {q['question'][:60]}")
    return records


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("questions", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--strategy", default="header", choices=["header", "fixed"])
    parser.add_argument("--model", default=MODEL)
    args = parser.parse_args()

    questions = json.loads(args.questions.read_text(encoding="utf-8"))
    records = export(questions, build_store(args.strategy), args.strategy, args.model)
    args.output.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8"
    )
    print(f"Wrote {len(records)} answers to {args.output}")
