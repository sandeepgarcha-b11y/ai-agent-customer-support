"""Passenger support agent — CLI entrypoint."""

import os
import uuid
from langchain_core.messages import HumanMessage, AIMessage

from graph import build_graph


def run_conversation():
    graph = build_graph()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("Passenger Support Agent")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    while True:
        try:
            user_input = input("Customer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", ""}:
            print("Agent: Thanks for reaching out to Passenger. Take care!")
            break

        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        messages = result.get("messages", [])
        ai_message = next(
            (m for m in reversed(messages) if isinstance(m, AIMessage) and m.content),
            None,
        )

        if ai_message:
            print(f"\nAgent: {ai_message.content}\n")
        else:
            print("\nAgent: Sorry, something went wrong — could you try again?\n")


if __name__ == "__main__":
    required = ["OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    run_conversation()
