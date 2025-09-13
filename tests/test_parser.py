from parser import parse_wikipedia_dump


def test_parse():
    count = 0
    for title, text in parse_wikipedia_dump(limit=5):
        assert title is not None
        assert text is not None
        count += 1
    assert count == 5
