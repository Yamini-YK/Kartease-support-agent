"""Milestone 1: one successful call to Gemini."""
import os

from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise SystemExit("GOOGLE_API_KEY is missing. Copy .env.example to .env and paste your key.")

llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-3.7-flash"))
response = llm.invoke("In one sentence, what is an online store?")
print(response.text)
