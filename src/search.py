from indexer import load_index


def search(query_tokens):
    index = load_index()
    results = set()
    for token in query_tokens:
        postings = index.get(token, [])
        results.update(postings)
    return results
