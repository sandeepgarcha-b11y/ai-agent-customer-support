"""Passenger support agent — LangGraph ReAct implementation."""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from tools import ALL_TOOLS
from prompts import SYSTEM_PROMPT


def build_agent():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        state_modifier=SystemMessage(content=SYSTEM_PROMPT),
    )
    return agent


def run_conversation():
    agent = build_agent()
    print("Passenger Support Agent")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    history = []
    while True:
        try:
            user_input = input("Customer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", ""}:
            print("Agent: Thank you for contacting Passenger support. Have a great day!")
            break

        history.append({"role": "user", "content": user_input})

        result = agent.invoke({"messages": history})
        messages = result["messages"]

        # Last AI message is the response
        ai_message = next(
            (m for m in reversed(messages) if m.type == "ai" and m.content),
            None,
        )
        if ai_message:
            response = ai_message.content
            print(f"\nAgent: {response}\n")
            history.append({"role": "assistant", "content": response})
        else:
            print("\nAgent: I'm sorry, I wasn't able to process that. Could you try again?\n")


if __name__ == "__main__":
    # Validate required environment variables
    required = ["OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    run_conversation()
