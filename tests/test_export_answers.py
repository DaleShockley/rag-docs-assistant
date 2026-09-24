from src.export_answers import parse_cited_sources


def test_parses_single_source():
    assert parse_cited_sources("Don't set a default.\n\nSources: query-params.md") == [
        "query-params.md"
    ]


def test_parses_multiple_sources_and_markdown_bold():
    answer = "Use a Pydantic model.\n\n**Sources:** body.md, query-params.md"
    assert parse_cited_sources(answer) == ["body.md", "query-params.md"]


def test_last_sources_line_wins():
    answer = "Sources: first-steps.md\nActually...\nSources: path-params.md"
    assert parse_cited_sources(answer) == ["path-params.md"]


def test_no_sources_line():
    assert parse_cited_sources("The docs don't cover this.") == []


def test_prose_on_sources_line_is_not_a_source():
    assert parse_cited_sources("Sources: None of the provided excerpts contain this.") == []
    answer = "Sources: first-steps.md (only shows development server usage, not production)"
    assert parse_cited_sources(answer) == ["first-steps.md"]
