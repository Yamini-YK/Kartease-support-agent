# KartEase Support Agent

A RAG-powered customer support assistant for KartEase, a fictional Indian online store.
It runs in the terminal and answers customer questions by choosing between two tools:

- **search_policies**: finds the most relevant chunks of the policy documents in Chroma and answers only from them, naming the source file (the RAG part).
- **get_order_status**: reads `orders.csv` and returns an order's product, status, date and payment method.

The agent (Gemini) decides which tool to use, or both. For anything unrelated to KartEase it replies:
*"Sorry, I can only help with KartEase orders and policies."*

## Framework and why

**LangChain** (not mixed with LlamaIndex). Reasons: plain Python functions become tools with one `tool(...)` call, `create_agent` is synchronous (no asyncio helper needed), and the pieces map directly onto the case study.

Stack: LangChain + Google Gemini free tier (LLM and embeddings) + Chroma stored locally in `chroma_db/`.

## Project structure

| File | Purpose |
|---|---|
| `check_gemini.py` | Milestone 1: one test call to Gemini |
| `ingest.py` | Load `data/*.md`, split into chunks, embed, store in Chroma (skips embedding if already stored) |
| `test_retrieval.py` | Prints top-3 chunks (file name + score) for a sample question |
| `policy_search.py` | `search_policies(question)`: retrieval + answer-only-from-context prompt |
| `tools.py` | `get_order_status(order_id)` as a plain function |
| `agent.py` | Builds the Gemini agent with both tools; `ask()` returns the answer and the tools used |
| `app.py` | Terminal chat loop (type `exit` to quit) |
| `run_questions.py` | Runs the 14 test questions and writes `test_results.md` |
| `tests/test_order_tool.py` | pytest tests for `get_order_status` (no Gemini calls) |

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-langchain.txt
cp .env.example .env              # Windows: copy .env.example .env
```

Get a free key from [Google AI Studio](https://aistudio.google.com), paste it as `GOOGLE_API_KEY` in `.env`.
If the model names in `.env.example` are no longer free in AI Studio, use the free Flash and embedding models it lists.
`.env` is in `.gitignore`; never commit your key.

## How to run

```bash
python check_gemini.py     # 1. confirm Gemini works
python ingest.py           # 2. build the knowledge base (run twice: 2nd run must skip embedding)
python test_retrieval.py   # 3. optional: see retrieved chunks
python policy_search.py    # 4. optional: 3 policy + 2 unrelated questions
python app.py              # 5. start the chat
python -m pytest           # run the automated tests (no API key needed)
python run_questions.py    # run all 14 test questions
```

## Test results

### Automated tests (pytest)

`python -m pytest`: 5 tests for `get_order_status` (known ID, lowercase ID, unknown ID, ID with spaces, cancelled order). They do not call Gemini.

RESULT: _write your output here, e.g. "5 passed"_

### Agent test questions (14)

Run `python run_questions.py`, read each answer, then mark **Pass** only if the answer contains the expected content AND the right tool(s) were used.

| # | Question | Expected answer contains | Tool(s) | Result |
|---|---|---|---|---|
| 1 | How many days do I have to return a phone? | 10 days from delivery | Policy | |
| 2 | Can I return earbuds if I just don't like them? | No, hygiene reasons (unless damaged or defective) | Policy | |
| 3 | What is the delivery charge on a ₹350 order? | ₹40 (free from ₹499) | Policy | |
| 4 | If I order at 4 PM, when will it be dispatched? | Next working day (cut-off is 2 PM) | Policy | |
| 5 | Can I use a coupon together with a bank offer? | No | Policy | |
| 6 | How long is Extended Protection and when can I buy it? | 1 extra year; within 30 days of delivery | Policy | |
| 7 | Can I pay cash on delivery for a ₹12,000 order? | No, COD only up to ₹10,000 | Policy | |
| 8 | Where is my order KE1002? | Shipped; expected 2026-10-07 | Order | |
| 9 | What is the status of order ke1005? | Processing; expected 2026-10-08 | Order | |
| 10 | What is the status of order KE9999? | No order found | Order | |
| 11 | My return for KE1006 was picked up. When will I get my refund? | Return picked up; quality check, then 5 to 7 working days to debit card | Both | |
| 12 | I paid cash for KE1009. If I return it, how do I get my money back? | Cash on Delivery; refund to bank account or UPI within 5 to 7 working days | Both | |
| 13 | Who is the CEO of Google? | Sorry message | None | |
| 14 | Write me a poem about Diwali. | Sorry message | None | |

### One fix I tried

- **Failed question:** _# and what went wrong_
- **Fix tried:** _e.g. clearer tool description / prompt change / chunk size / top-k_
- **Result after re-running:** _what changed_

## Known limitations

1. Answers depend only on the 4 policy documents and 10 sample orders; anything else gets the sorry message, and the agent has no memory between questions.
2. The Gemini free tier has rate limits and model names change, so answers can occasionally fail or vary and may need a retry.
