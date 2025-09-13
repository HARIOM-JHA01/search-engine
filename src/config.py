import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
INDEX_DIR = os.path.join(DATA_DIR, "index")

WIKIPEDIA_FILE = os.path.join(RAW_DIR, "enwiki-latest-pages-articles.xml.bz2")
