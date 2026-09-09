from src.ingest import _clean, chunk_by_headers, chunk_fixed


def test_clean_strips_template_syntax():
    raw = (
        "Some text\n\n"
        "{* ../../docs_src/foo.py hl[1] *}\n\n"
        "More text\n\n"
        "/// tip\n\n"
        "Do this.\n\n"
        "///"
    )
    cleaned = _clean(raw)
    assert "{*" not in cleaned
    assert "///" not in cleaned
    assert "Some text" in cleaned
    assert "More text" in cleaned


def test_chunk_fixed_respects_size_and_overlap():
    text = "a" * 2000
    chunks = chunk_fixed(text, size=800, overlap=100)
    assert len(chunks) == 3
    assert all(len(c) <= 800 for c in chunks)


def test_chunk_by_headers_splits_on_headers():
    text = (
        "# Title\n\nintro text\n\n"
        "## Section One\n\ncontent one\n\n"
        "## Section Two\n\ncontent two"
    )
    chunks = chunk_by_headers(text)
    assert len(chunks) == 3
    assert chunks[0].startswith("# Title")
    assert chunks[1].startswith("## Section One")
    assert chunks[2].startswith("## Section Two")


def test_chunk_by_headers_handles_no_headers():
    text = "just a paragraph, no headers at all"
    assert chunk_by_headers(text) == [text]


def test_chunk_by_headers_handles_empty_text():
    assert chunk_by_headers("") == []
