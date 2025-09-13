from collections import defaultdict
import os
import json
from config import INDEX_DIR


def build_index(docs):
    index = defaultdict(list)
    for doc_id, (title, tokens) in enumerate(docs):
        unique_tokens = set(tokens)
        for token in unique_tokens:
            index[token].append(doc_id)
    return index


def save_index(index):
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)
    path = os.path.join(INDEX_DIR, "inverted_index.json")
    with open(path, "w") as f:
        json.dump(index, f)


def load_index():
    path = os.path.join(INDEX_DIR, "inverted_index.json")
    with open(path, "r") as f:
        return json.load(f)
