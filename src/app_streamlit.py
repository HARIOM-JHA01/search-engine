import streamlit as st
import os
from search import search
from preprocess import clean_text
from indexer import load_index
from config import PROCESSED_DIR

st.title("Wikipedia Search Engine")

index = load_index()


def get_article_by_id(doc_id):
    filepath = os.path.join(PROCESSED_DIR, f"article_{doc_id}.txt")
    if not os.path.exists(filepath):
        return "", "", ""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        title = lines[0].strip() if lines else ""
        full_text = lines[1].strip() if len(lines) > 1 else ""
        snippet = full_text[:300] + ("..." if len(full_text) > 300 else "")
    return title, snippet, full_text


query = st.text_input("Enter your search query:")

if query:
    tokens = clean_text(query)
    result_ids = search(tokens)
    st.write(f"Found {len(result_ids)} results.")
    if result_ids:
        for rid in result_ids:
            title, snippet, full_text = get_article_by_id(rid)
            with st.container():
                st.markdown(
                    f"<div style='background-color:#f9f9f9;padding:20px;border-radius:10px;margin-bottom:15px;'>"
                    f"<h2 style='margin-bottom:10px;'>{title}</h2>"
                    f"<p style='font-size:16px;color:#555;'>{snippet}</p>"
                    f"<small style='color:#888;'>Document ID: {rid}</small>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                if st.button(f"Read More {rid}"):
                    st.markdown(
                        f"<div style='background-color:#fffbe6;padding:20px;border-radius:10px;'>"
                        f"<h3>{title}</h3>"
                        f"<p style='font-size:15px;color:#333;'>{full_text}</p>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
    else:
        st.write("No results found.")
