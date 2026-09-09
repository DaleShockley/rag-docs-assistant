[rag-docs-assistant-spec.md](https://github.com/user-attachments/files/32015044/rag-docs-assistant-spec.md)
# rag-docs-assistant# RAG Docs Assistant — Project Spec

## The problem

Point this at a real project's documentation and ask it plain-English questions, get an answer grounded in the actual docs with a citation back to the source file. Suggested corpus: the tutorial section of FastAPI's docs (`tiangolo/fastapi`, `docs/en/docs/tutorial/`), a well-known public repo, MIT licensed, markdown-based, and small enough (a few dozen files) to keep embedding costs and demo runtime reasonable. Any other public markdown doc set works the same way if you'd rather use something else.

## Why this project, specifically

This is the RAG fundamentals project, kept deliberately separate from the agent project so the two don't blur together in an interview. It has to show you understand what's actually happening inside a RAG pipeline, not just that you can call a vector database:

- **Chunking is a real design decision, not a default.** The project builds two chunking strategies and measures which one retrieves better, instead of picking one and hoping.  
- **Retrieval is evaluated, not assumed.** A small hand-written set of questions with known-correct source sections gets used to compute hit-rate at k for each strategy.  
- **Answers are grounded and citable.** Every answer names which doc it came from, so a reviewer can see the system isn't just making things up.

## A note on embeddings vs. generation

Claude doesn't have a first-party embeddings endpoint, so this project uses two different tools for two different jobs: a local, free, open-source embedding model (`sentence-transformers`, no API key required) for turning text into vectors, and Claude for actually reading the retrieved chunks and writing the answer. Worth being able to explain that distinction clearly, it's a common point of confusion and knowing it cold is a small but real signal.

## Architecture

```
Markdown docs ──> Chunking (2 strategies) ──> Embeddings (sentence-transformers)
                                                        │
                                                        ▼
                                                 Chroma vector store
                                                        │
                                     query ──> top-k retrieval ──┘
                                                        │
                                                        ▼
                                        Claude reads chunks + writes
                                        a grounded, cited answer
```

Chunking strategies to compare:

1. **Fixed-size** — split every N characters with some overlap. The naive baseline.  
2. **Header-aware** — split on markdown headers (`##`, `###`) so each chunk is a coherent section instead of an arbitrary character window.

## Tech stack

- Python 3.11+  
- `sentence-transformers` for embeddings (local, free, no API key)  
- `chromadb` for the vector store (runs locally, no external service to stand up)  
- Anthropic SDK for the generation step  
- `streamlit` for a minimal UI (ask a question, see the answer \+ cited sources)  
- `pytest` for tests  
- GitHub Actions for CI

## Retrieval eval (the part that matters most)

- Write \~15 questions you know the answer to from the source docs, each paired with which file/section should contain the answer.  
- For each chunking strategy, run all 15 questions through retrieval only (no generation), and check whether the correct section shows up in the top-k results.  
- Report hit-rate@3 and hit-rate@5 for both strategies side by side.  
- Write one paragraph on why one strategy won, e.g. "header-aware chunking beat fixed-size on 4 questions where the answer spanned a full section that fixed-size chunking split awkwardly across two chunks." A specific example beats a bare percentage.

## Repo structure

```
rag-docs-assistant/
├── README.md
├── data/
│   └── docs/                    # the markdown source files (a bounded subset, committed)
├── src/
│   ├── ingest.py                 # pulls docs, both chunking strategies
│   ├── embeddings.py              # wraps sentence-transformers
│   ├── vector_store.py             # Chroma wrapper: add, query
│   ├── rag.py                       # retrieve + build prompt + call Claude
│   └── app.py                         # Streamlit UI
├── eval/
│   ├── qa_set.json                     # 15 questions + expected source section
│   └── score_retrieval.py               # hit-rate@k per chunking strategy
├── tests/
│   └── test_ingest.py, test_vector_store.py, test_rag.py (all mocked, no keys needed)
├── .github/workflows/ci.yml
└── requirements.txt
```

## Milestones

1. **Ingestion \+ chunking** — download/commit the doc subset, implement both chunking strategies, tested independently.  
2. **Embeddings \+ vector store** — wire up sentence-transformers and Chroma, verify a query returns sane nearest neighbors on a tiny fixture set.  
3. **RAG pipeline** — retrieve top-k chunks for a question, build a grounded prompt, call Claude, return an answer with citations.  
4. **Retrieval eval** — the 15-question set, hit-rate@k scoring, strategy comparison.  
5. **Polish** — Streamlit UI, README with a real sample Q\&A exchange, the eval table, architecture diagram, CI.

## README outline (for the finished repo)

- One-paragraph problem statement  
- A real sample question \+ answer \+ citation (so a reviewer sees the payoff immediately)  
- Architecture diagram  
- Retrieval eval table (fixed-size vs. header-aware, hit-rate@3 and @5) plus the one-paragraph "why" writeup  
- How to run it locally  
- What you'd build next

## Stretch goals (only after the above works)

- A third chunking strategy (semantic chunking via embedding similarity) added to the comparison  
- Swap Chroma for pgvector to show you can work with a real database instead of an embedded one  
- Multi-turn conversation instead of single-question Q\&A  
- Answer confidence / "I don't know" handling when retrieval comes back weak

