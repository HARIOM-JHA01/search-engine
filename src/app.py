import os
from parser import parse_wikipedia_dump
from preprocess import clean_text
from indexer import build_index, save_index
from search import search
from config import PROCESSED_DIR


def main():
    # Step 1: Preprocess and save articles
    print("Parsing and preprocessing articles...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    processed_files = []
    for idx, (title, text) in enumerate(parse_wikipedia_dump(limit=1000)):
        print(f"Processing: {title}")
        if text is None:
            continue
        tokens = clean_text(text)
        # Save processed tokens to file
        filename = f"article_{idx}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            safe_title = title if title is not None else ""
            f.write(safe_title + "\n")
            f.write(" ".join(tokens))
        processed_files.append(filepath)

    # Step 2: Build index from processed files
    print("Building index from processed articles...")
    docs = []
    for filepath in processed_files:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            title = lines[0].strip()
            tokens = lines[1].strip().split()
            docs.append((title, tokens))

    index = build_index(docs)
    save_index(index)
    print("Index built and saved!")

    while True:
        query = input("Enter search query (or 'exit'): ")
        if query.lower() == "exit":
            break
        tokens = clean_text(query)
        result_ids = search(tokens)
        print(f"Found {len(result_ids)} results.")
        for rid in result_ids:
            print(f"- Document ID {rid}")


if __name__ == "__main__":
    main()
