"""Loads markdown docs and splits them into chunks using two strategies.

The comparison is the point of this project: fixed-size chunking is the
naive default, header-aware chunking respects the document's own
structure. eval/score_retrieval.py measures which one actually
retrieves better against a hand-labeled question set.
"""

import re
from dataclasses import dataclass
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "data" / "docs"


@dataclass
class Chunk:
    doc: str        # source filename
    chunk_id: int    # index within that doc
    text: str
    strategy: str      # "fixed" or "header"


def load_docs(docs_dir: Path = DOCS_DIR) -> dict[str, str]:
    """Returns {filename: cleaned_markdown_text} for every .md file in docs_dir."""
    return {path.name: _clean(path.read_text()) for path in sorted(docs_dir.glob("*.md"))}


def _clean(text: str) -> str:
    """Strips FastAPI's custom doc syntax so chunks are plain, readable prose.

    Real doc sources are messy. These particular docs use `{* file.py hl[1] *}`
    to embed code samples and `///` blocks for admonitions -- neither means
    anything outside their own doc build pipeline, so both are stripped
    before chunking rather than treated as content.
    """
    text = re.sub(r"\{\*.*?\*\}", "", text)
    text = re.sub(r"^///.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_fixed(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Naive fixed-size chunking with overlap. The baseline strategy."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if c]


_HEADER_RE = re.compile(r"^(#{1,3})\s+.*$", re.MULTILINE)


def chunk_by_headers(text: str) -> list[str]:
    """Splits on markdown headers (#, ##, ###) so each chunk is one coherent section."""
    matches = list(_HEADER_RE.finditer(text))
    if not matches:
        return [text.strip()] if text.strip() else []

    chunks = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end].strip()
        if section:
            chunks.append(section)
    return chunks


def build_chunks(docs_dir: Path = DOCS_DIR) -> dict[str, list[Chunk]]:
    """Returns {"fixed": [...], "header": [...]} chunk lists across all docs."""
    docs = load_docs(docs_dir)
    result: dict[str, list[Chunk]] = {"fixed": [], "header": []}
    for filename, text in docs.items():
        for i, chunk_text in enumerate(chunk_fixed(text)):
            result["fixed"].append(Chunk(doc=filename, chunk_id=i, text=chunk_text, strategy="fixed"))
        for i, chunk_text in enumerate(chunk_by_headers(text)):
            result["header"].append(Chunk(doc=filename, chunk_id=i, text=chunk_text, strategy="header"))
    return result


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"fixed-size chunks:   {len(chunks['fixed'])}")
    print(f"header-aware chunks: {len(chunks['header'])}")
