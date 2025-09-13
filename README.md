
# Wikipedia Search Engine

This project is a simple search engine for Wikipedia articles. It parses a Wikipedia XML dump, preprocesses the text, builds an index, and allows users to search for articles via a command-line interface or a modern web UI.

## Features
- Parse Wikipedia XML dumps
- Preprocess and clean text (tokenization, stopword removal, formatting preserved)
- Build an inverted index for fast search
- Command-line and Streamlit web search interfaces

## Project Structure

```
search-engine/
├── main.py
├── pyproject.toml
├── README.md
├── uv.lock
├── data/
│   └── raw/
│       └── enwiki-latest-pages-articles.xml.bz2
├── src/
│   ├── __init__.py
│   ├── app.py            # Main CLI application
│   ├── app_streamlit.py  # Streamlit web app
│   ├── config.py         # Configuration settings
│   ├── indexer.py        # Index building and saving
│   ├── parser.py         # Wikipedia dump parser
│   ├── preprocess.py     # Text cleaning and preprocessing
│   ├── search.py         # Search logic
│   └── __pycache__/
└── tests/
		└── test_parser.py    # Unit tests for parser
```

## Setup

1. **Install dependencies**
	 - This project uses [uv](https://github.com/astral-sh/uv) for Python package management.
	 - Run:
		 ```zsh
		 uv sync
		 ```

2. **Download Wikipedia Dump**
	 - Place the `enwiki-latest-pages-articles.xml.bz2` file in `data/raw/`.
	 - Download from [Wikipedia Dumps](https://dumps.wikimedia.org/enwiki/latest/).

## Usage

### Command-Line Search

Run the main application:

```zsh
uv run src/app.py
```

You will be prompted to enter search queries. Type `exit` to quit.

### Web Search (Streamlit)

Run the Streamlit app:

```zsh
uv run streamlit run src/app_streamlit.py
```

This launches a web interface for searching and viewing articles visually. Results are shown as cards with titles, snippets, and a "Read More" button for full articles.

## How It Works

1. **Parsing:** Extracts article titles and text from the Wikipedia XML dump.
2. **Preprocessing:** Cleans and tokenizes text, removes stopwords, preserves formatting.
3. **Indexing:** Builds an inverted index mapping tokens to document IDs.
4. **Searching:** Accepts user queries, preprocesses them, and returns matching articles.

## Testing

Run unit tests:

```zsh
PYTHONPATH=src uv run pytest tests
```

## Requirements
- Python 3.12+
- uv
- nltk
- streamlit (for web UI)

## Notes
- The first run will download NLTK stopwords automatically.
- The index is built from the first 1000 articles for demonstration (see `src/app.py`).
- The processed directory is auto-created and used for storing cleaned articles.

## License

MIT License
