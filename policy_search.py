"""Milestone 3: answer policy questions ONLY from the retrieved policy chunks."""
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from ingest import get_vectorstore

load_dotenv()

SORRY_MESSAGE = "Sorry, I can only help with KartEase orders and policies."
TOP_K = 3

PROMPT = """You are KartEase customer support. Answer the question using ONLY the context below.

Rules:
- Keep the answer short and friendly.
- Name the source file(s) you used, for example: (Source: returns_and_refunds.md).
- If the context does not contain the answer, reply exactly: {sorry}

Context:
{context}

Question: {question}
Answer:"""

_store = None
_llm = None


def _get_store():
    global _store
    if _store is None:
        _store = get_vectorstore()
    return _store


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-3.7-flash"), temperature=0
        )
    return _llm


def search_policies(question: str) -> str:
    """Answer a question about KartEase policies (returns, refunds, shipping, delivery,
    warranty, payments, COD, EMI, coupons) using only the policy documents."""
    docs = _get_store().similarity_search(question, k=TOP_K)
    context = "\n\n".join(f"[Source: {d.metadata['source']}]\n{d.page_content}" for d in docs)
    prompt = PROMPT.format(sorry=SORRY_MESSAGE, context=context, question=question)
    return _get_llm().invoke(prompt).text.strip()


if __name__ == "__main__":
    # Milestone 3 check: 3 policy questions + 2 unrelated questions
    for q in [
        "What is the return window for phones?",
        "How much is the delivery charge on a small order?",
        "Is cash on delivery available?",
        "Who won the World Cup?",
        "Write me a poem about Diwali.",
    ]:
        print(f"Q: {q}\nA: {search_policies(q)}\n")
