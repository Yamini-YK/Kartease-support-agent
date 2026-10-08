"""Milestone 2: build the knowledge base (policy docs -> chunks -> embeddings -> Chroma).

Run `python ingest.py` once. Running it again reuses the vectors already stored
in chroma_db/ and does NOT call the embedding API again.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "kartease_policies"

CHUNK_SIZE = 500      # characters
CHUNK_OVERLAP = 50    # characters


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
    )


def load_and_split():
    """Load every .md file in data/ and split it into chunks.

    Each chunk keeps the file name in metadata["source"].
    """
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    for doc in docs:
        doc.metadata["source"] = Path(doc.metadata["source"]).name  # e.g. returns_and_refunds.md

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(docs)} documents -> {len(chunks)} chunks")
    return chunks


def get_vectorstore():
    """Return the Chroma store. Embed the documents only if the collection is empty."""
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )
    existing = store._collection.count()
    if existing > 0:
        print(f"Chroma already has {existing} chunks - skipping embedding.")
        return store

    chunks = load_and_split()
    store.add_documents(chunks)
    print(f"Embedded and stored {len(chunks)} chunks in {CHROMA_DIR}")
    return store


if __name__ == "__main__":
    get_vectorstore()
