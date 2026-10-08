"""Milestone 4: the agent that chooses between the two tools."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from policy_search import SORRY_MESSAGE, search_policies
from tools import get_order_status

load_dotenv()

# Turn the plain functions into tools. The docstrings are the descriptions the
# agent reads to decide which tool to use.
search_policies_tool = tool(search_policies)
get_order_status_tool = tool(get_order_status)

SYSTEM_PROMPT = f"""You are KartEase customer support.
- Use the tools to answer. Never guess.
- Use get_order_status when the customer gives an order ID.
- Use search_policies for questions about policies (returns, refunds, shipping, warranty, payments).
- If a question needs both an order's details and a policy, use both tools.
- For questions unrelated to KartEase orders and policies, reply exactly: {SORRY_MESSAGE}
- Keep answers short and friendly."""


def build_agent():
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.7-flash"), temperature=0
    )
    return create_agent(
        llm,
        tools=[search_policies_tool, get_order_status_tool],
        system_prompt=SYSTEM_PROMPT,
    )


def ask(agent, question):
    """Ask the agent one question. Returns (answer_text, list_of_tools_used)."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    tools_used = []
    for m in messages:
        for call in getattr(m, "tool_calls", None) or []:
            if call["name"] not in tools_used:
                tools_used.append(call["name"])
    return messages[-1].text, tools_used
