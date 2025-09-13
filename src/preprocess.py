import re
from nltk.corpus import stopwords

# Download stopwords once
import nltk

nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    if text is None:
        return []
    text = text.lower()
    # Preserve . ; : and line breaks
    text = re.sub(r"[^a-z0-9\.\;\:\s\n]", "", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS]
    return tokens
