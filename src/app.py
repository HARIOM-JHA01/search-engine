import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED, as_completed
from parser import parse_wikipedia_dump
from preprocess import clean_text
from indexer import save_index
from search import search
from config import PROCESSED_DIR
import time


# Worker function must be top-level (picklable)
def _preprocess_and_save(args):
    idx, title, text, processed_dir = args
    if text is None:
        return None
    tokens = clean_text(text)
    # Save processed tokens to file
    filename = f"article_{idx}.txt"
    filepath = os.path.join(processed_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        safe_title = title if title is not None else ""
        f.write(safe_title + "\n")
        f.write(" ".join(tokens))
    return idx, (title or ""), tokens, filepath


def main():
    # Step 1+2: Parse -> parallel preprocess -> incremental index
    print("Parsing, preprocessing, and indexing in parallel...")
    start_time = time.time()
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    processed_files = []
    postings = defaultdict(set)  # term -> set(doc_ids)

    max_workers = min(10, os.cpu_count() or 4)  # use up to your 10 cores
    inflight_limit = max_workers * 4

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = []
        idx = 0
        for title, text in parse_wikipedia_dump():
            # submit work
            futures.append(
                pool.submit(_preprocess_and_save, (idx, title, text, PROCESSED_DIR))
            )
            idx += 1
            # Backpressure: if too many in flight, wait for some to finish
            if len(futures) >= inflight_limit:
                done, futures = _drain_some(futures)
                for res in done:
                    if res is None:
                        continue
                    doc_id, _title, tokens, filepath = res
                    for t in set(tokens):
                        if t:
                            postings[t].add(doc_id)
                    processed_files.append(filepath)

        # Drain remaining
        for fut in as_completed(futures):
            try:
                res = fut.result()
            except Exception as e:
                print(f"Worker failed: {e}")
                continue
            if res is None:
                continue
            doc_id, _title, tokens, filepath = res
            for t in set(tokens):
                if t:
                    postings[t].add(doc_id)
            processed_files.append(filepath)

    mid_time = time.time()
    print(
        f"Preprocessing + incremental indexing completed in {mid_time - start_time:.2f} seconds."
    )
    print(f"Total processed files: {len(processed_files)}")

    # Finalize and save index
    index = {term: sorted(ids) for term, ids in postings.items()}
    save_index(index)
    print("Index built and saved!")
    end_time = time.time()
    print(f"Saving completed in {end_time - mid_time:.2f} seconds.")
    # Step 3: Interactive search
    while True:
        query = input("Enter search query (or 'exit'): ")
        if query.lower() == "exit":
            break
        tokens = clean_text(query)
        result_ids = search(tokens)
        print(f"Found {len(result_ids)} results.")
        for rid in result_ids:
            print(f"- Document ID {rid}")


def _drain_some(futures):
    """Wait until at least one future completes; return (completed_results, remaining_futures)."""
    done_set, not_done = wait(futures, return_when=FIRST_COMPLETED)
    results = []
    remaining = []
    for fut in futures:
        if fut in done_set:
            try:
                results.append(fut.result())
            except Exception as e:
                print(f"Worker failed: {e}")
        else:
            remaining.append(fut)
    return results, remaining


if __name__ == "__main__":
    main()
