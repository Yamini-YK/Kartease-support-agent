"""Stretch Goal A: Gradio web chatbot for KartEase Support Agent."""
import gradio as gr

from agent import ask, build_agent

# Build the agent once at startup (not on every message)
agent = build_agent()


def respond(message: str, history: list):
    """Called by Gradio on every user message. Returns the agent's reply."""
    if not message.strip():
        return ""
    try:
        answer, tools_used = ask(agent, message)
        if tools_used:
            tool_note = f"\n\n> 🔧 *Tools used: {', '.join(tools_used)}*"
            return answer + tool_note
        return answer
    except Exception as e:
        return f"⚠️ Sorry, something went wrong ({type(e).__name__}). Please try again."


# ── Gradio UI ─────────────────────────────────────────────────────────────
demo = gr.ChatInterface(
    fn=respond,
    title="🛒 KartEase Support",
    description="Ask me about your orders, returns, refunds, shipping, or any KartEase policy.",
    examples=[
        "Where is my order KE1002?",
        "How many days do I have to return a phone?",
        "What is the status of order KE1005?",
        "Can I pay cash on delivery for a ₹12,000 order?",
        "My return for KE1006 was picked up. When will I get my refund?",
        "What is the delivery charge on a ₹350 order?",
    ],
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
    )
