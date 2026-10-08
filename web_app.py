import gradio as gr
from agent import ask, build_agent

# Build the agent once at startup
agent = build_agent()

def respond(message, history):
    if not message.strip():
        return ""
    try:
        answer, tools_used = ask(agent, message)
        if tools_used:
            return answer + f"\n\n> 🔧 *Tools used: {', '.join(tools_used)}*"
        return answer
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Define a nice orange/amber theme matching the brand
custom_theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="amber",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter")
)

# Hide the footer for a cleaner look
custom_css = """
footer { display: none !important; }
.gradio-container { max-width: 800px !important; margin: auto; }
"""

# Create the ChatInterface with ONLY supported arguments
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
    ]
)

if __name__ == "__main__":
    # In Gradio 6, theme and css are passed to launch()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=custom_theme,
        css=custom_css
    )
