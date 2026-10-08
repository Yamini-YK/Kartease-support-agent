"""Milestone 5: terminal chat loop. Type 'exit' to quit."""
from agent import ask, build_agent


def main():
    agent = build_agent()
    print("KartEase Support Agent. Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            print("Goodbye!")
            break
        try:
            answer, tools_used = ask(agent, question)
        except Exception as e:  # e.g. network error or free-tier quota
            print(f"Agent: Sorry, something went wrong ({type(e).__name__}). Please try again.\n")
            continue
        print(f"Agent: {answer}")
        print(f"[Tools used: {', '.join(tools_used) if tools_used else 'none'}]\n")


if __name__ == "__main__":
    main()
