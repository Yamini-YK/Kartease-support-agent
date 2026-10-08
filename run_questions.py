"""Milestone 5: run the 14 test questions and save the results to test_results.md.

The script checks the TOOL choice automatically. Whether the answer text contains
the expected content is for YOU to judge - read the answers and mark Pass / Fail.
"""
import time

from agent import ask, build_agent

QUESTIONS = [
    (1, "How many days do I have to return a phone?", "10 days from delivery", {"search_policies"}),
    (2, "Can I return earbuds if I just don't like them?", "No, hygiene reasons (unless damaged or defective)", {"search_policies"}),
    (3, "What is the delivery charge on a ₹350 order?", "₹40 (free from ₹499)", {"search_policies"}),
    (4, "If I order at 4 PM, when will it be dispatched?", "Next working day (cut-off is 2 PM)", {"search_policies"}),
    (5, "Can I use a coupon together with a bank offer?", "No", {"search_policies"}),
    (6, "How long is Extended Protection and when can I buy it?", "1 extra year; within 30 days of delivery", {"search_policies"}),
    (7, "Can I pay cash on delivery for a ₹12,000 order?", "No, COD only up to ₹10,000", {"search_policies"}),
    (8, "Where is my order KE1002?", "Shipped; expected 2026-10-07", {"get_order_status"}),
    (9, "What is the status of order ke1005?", "Processing; expected 2026-10-08", {"get_order_status"}),
    (10, "What is the status of order KE9999?", "No order found", {"get_order_status"}),
    (11, "My return for KE1006 was picked up. When will I get my refund?", "Quality check, then 5 to 7 working days to debit card", {"search_policies", "get_order_status"}),
    (12, "I paid cash for KE1009. If I return it, how do I get my money back?", "COD; refund to bank account or UPI in 5 to 7 working days", {"search_policies", "get_order_status"}),
    (13, "Who is the CEO of Google?", "Sorry message", set()),
    (14, "Write me a poem about Diwali.", "Sorry message", set()),
]

agent = build_agent()
lines = ["| # | Question | Expected answer contains | Expected tool(s) | Tool(s) used | Tools OK? | Agent answer |",
         "|---|---|---|---|---|---|---|"]
for num, question, expected, expected_tools in QUESTIONS:
    try:
        answer, used = ask(agent, question)
    except Exception as e:
        answer, used = f"ERROR: {type(e).__name__}: {e}", []
    tools_ok = "Yes" if set(used) == expected_tools else "No"
    exp = ", ".join(sorted(expected_tools)) or "none"
    got = ", ".join(used) or "none"
    answer_clean = answer.replace("\n", " ").replace("|", "/")
    print(f"\n#{num} {question}\n   tools: {got} (expected {exp}) -> {tools_ok}\n   answer: {answer_clean}")
    lines.append(f"| {num} | {question} | {expected} | {exp} | {got} | {tools_ok} | {answer_clean} |")
    time.sleep(5)  # stay under the free-tier rate limit

with open("test_results.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved test_results.md - read each answer and copy Pass/Fail into your README.")
