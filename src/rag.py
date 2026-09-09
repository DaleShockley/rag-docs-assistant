"""RAG pipeline: retrieve relevant chunks, then ask Claude to answer
grounded in them, with citations back to the source doc.
"""

import anthropic

from src.vector_store import VectorStore

MODEL = "claude-sonnet-4-5"  # swap for whatever model your key has access to

SYSTEM_PROMPT = """You answer questions using only the documentation excerpts you're given.

Rules:
- Base your answer only on the provided excerpts. Don't use outside knowledge.
- If the excerpts don't contain enough information to answer, say so plainly instead of guessing.
- After your answer, list the source file(s) you used, on a line starting with "Sources:".
"""


def answer_question(question: str, store: VectorStore, n_results: int = 5) -> dict:
    """Retrieves relevant chunks and asks Claude to answer, grounded and cited."""
    hits = store.query(question, n_results=n_results)

    if not hits:
        return {"answer": "No documents have been indexed yet.", "sources": [], "hits": []}

    context = "\n\n---\n\n".join(
        f"[Source: {hit['metadata'].get('doc', 'unknown')}]\n{hit['text']}" for hit in hits
    )

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Documentation excerpts:\n\n{context}\n\nQuestion: {question}",
            }
        ],
    )

    answer_text = "".join(block.text for block in response.content if block.type == "text")
    sources = sorted({hit["metadata"].get("doc", "unknown") for hit in hits})

    return {"answer": answer_text, "sources": sources, "hits": hits}


if __name__ == "__main__":
    import sys

    from src.ingest import build_chunks

    strategy = sys.argv[1] if len(sys.argv) > 1 else "header"
    question = sys.argv[2] if len(sys.argv) > 2 else "How do I declare a required query parameter?"

    chunks = build_chunks()[strategy]
    store = VectorStore(collection_name=f"docs_{strategy}")
    store.add(
        ids=[f"{c.doc}-{c.chunk_id}" for c in chunks],
        texts=[c.text for c in chunks],
        metadatas=[{"doc": c.doc, "chunk_id": c.chunk_id} for c in chunks],
    )

    result = answer_question(question, store)
    print(result["answer"])
    print(f"\nSources: {', '.join(result['sources'])}")
