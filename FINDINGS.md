# Findings

## What I built

RAG Docs Assistant answers questions about FastAPI's tutorial docs, grounded in the actual text with a citation back to the source file. I built it in five stages: ingestion with two different chunking strategies, embeddings plus a Chroma vector store, a retrieval and generation pipeline using Claude, a retrieval eval comparing the two chunking strategies against a hand-labeled question set, and a final README and CI pass.

Like the first project, I worked through this step by step with Claude rather than asking for the whole repo at once. Each piece got built, tested, and verified before I moved to the next one.

## What I learned

The first real lesson was that Claude doesn't do embeddings. I didn't know that going in, and it's a distinction worth actually understanding rather than memorizing: embeddings and generation are two different jobs, and this project uses a free local model for one and Claude for the other. Knowing why they're split, not just that they are, is the kind of thing that separates "I used AI tools" from "I understand how this works."

The second lesson, and honestly the more interesting one, came from the eval. I went into this assuming header-aware chunking would win, since it respects the document's actual structure instead of cutting text at an arbitrary character count. The real numbers said otherwise: fixed-size chunking hit 100% at both k=3 and k=5, header-aware hit 93% at k=3. The docs I used have a lot of short, deeply nested subsections, so header-based chunking sometimes produced chunks too small to hold enough context, while fixed-size chunking's overlapping windows happened to blend adjacent sections together in a way that helped on at least one question. That's not a conclusion I'd have reached by reasoning about it in the abstract. It only showed up because I actually measured retrieval quality instead of assuming one strategy was obviously better and moving on. That's probably the single biggest thing I'm taking away from this project: a hypothesis about how a system should behave is not the same as evidence that it does, and building the eval is what turns a guess into a claim I can actually defend.

## Debugging notes

Most of the same GitHub web UI issues from the first project showed up again here: a capitalized `__init__.py`, a test file missing its `.py` extension, a file that landed one folder too deep. Nothing new, just confirmation that uploading files by hand through a browser is genuinely more error-prone than working from a real clone, and that a quick screenshot of the file tree before moving to the next milestone catches these fast.

The one new issue was environmental rather than code-related. Installing `sentence-transformers` pulls in PyTorch, which is a large download, and it timed out the first time I tried it, both in Claude's own sandbox and on my machine over a corporate network. It worked on a retry with a longer timeout. That turned into a real design decision rather than just an annoyance: the test suite doesn't actually need PyTorch installed at all, because `embeddings.py` only imports `sentence-transformers` lazily inside a function that the tests mock out directly. So the CI workflow deliberately installs a lean set of dependencies (`chromadb`, `anthropic`, `pytest`) instead of the full `requirements.txt`, which keeps the pipeline fast and avoids depending on a large, occasionally slow download succeeding on every single push. It's a small thing, but it's the kind of tradeoff that's worth being able to explain out loud: know which dependencies your tests actually exercise, and don't pay for the ones they don't.
