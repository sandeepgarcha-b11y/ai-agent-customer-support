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

        prev_length = len(graph.get_state(config).values.get("messages", []))

        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        all_messages = result.get("messages", [])
        new_ai_messages = [
            m for m in all_messages[prev_length:]
            if isinstance(m, AIMessage) and m.content
        ]

        if new_ai_messages:
            for m in new_ai_messages:
                print(f"\nAgent: {m.content}\n")
        else:
            print("\nAgent: Sorry, something went wrong — could you try again?\n")


if __name__ == "__main__":
    required = ["OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    run_conversation()
