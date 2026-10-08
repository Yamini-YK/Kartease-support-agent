"""Milestone 2 check: top-3 chunks for a sample question, with file name and score.

Note: Chroma returns a DISTANCE, so a LOWER score means a MORE similar chunk.
(This file is not inside tests/ on purpose: it calls Gemini, pytest must not.)
"""
from ingest import get_vectorstore

QUESTION = "What is the return window for phones?"

store = get_vectorstore()
results = store.similarity_search_with_score(QUESTION, k=3)

print(f"\nQuestion: {QUESTION}\n")
for rank, (doc, score) in enumerate(results, start=1):
    print(f"--- #{rank} | {doc.metadata['source']} | score (distance): {score:.4f}")
    print(doc.page_content.strip())
    print()
