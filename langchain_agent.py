import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.errors import GraphRecursionError


load_dotenv()

OMNIROUTE_BASE_URL = os.getenv(
    "OMNIROUTE_BASE_URL",
    "http://localhost:20128/v1",
)

OMNIROUTE_API_KEY = os.getenv("OMNIROUTE_API_KEY")

OMNIROUTE_MODEL = os.getenv(
    "OMNIROUTE_MODEL",
    "auto",
)
async def generate_fallback_answer(model, messages):
    response = await model.ainvoke(
        messages
        + [
            {
                "role": "user",
                "content": (
                    "You have reached the tool execution limit. "
                    "Do not call any more tools. "
                    "Using only the information already collected "
                    "in the conversation, provide the best answer "
                    "you can to the user's original request. "
                    "If the available information is insufficient, "
                    "say so clearly instead of guessing."
                    "Do not infer a metric that was not directly provided."
                    "Distinguish facts from calculations and assumptions."
                    "If the requested metric cannot be established from the"
                    "collected data, say that it cannot be determined."
                ),
            }
        ]
    )

    return response.content

async def main():
    model = ChatOpenAI(
        model=OMNIROUTE_MODEL,
        api_key=OMNIROUTE_API_KEY,
        base_url=OMNIROUTE_BASE_URL,
        timeout=120,
    )

    mcp_client = MultiServerMCPClient(
        {
            "smart_transport": {
                "command": ".venv\\Scripts\\python.exe",
                "args": ["server.py"],
                "transport": "stdio",
            }
        }
    )

    tools = await mcp_client.get_tools()

    print(f"Loaded {len(tools)} MCP tools.")

    agent = create_agent(
        model=model,
        tools=tools,
    )
    user_message = input("\nYou: ")
    last_state = None
    try:
    
        async for state in agent.astream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ]
            },
            {
                "recursion_limit": 10,
            },
            stream_mode="values",
        ):
            last_state = state

            print("\n--- Agent state update ---")

            for message in state["messages"]:
                print(
                    f"{type(message).__name__}: "
                    f"{message.content}"
                )

        if last_state:
            print("\nFinal answer:")
            print(last_state["messages"][-1].content)

    except GraphRecursionError:
        print("\nAgent stopped: recursion limit reached.")

        if last_state:
            messages = last_state["messages"]

            print(
                f"\nCollected {len(messages)} messages "
                "before stopping."
            )

            final_answer = await generate_fallback_answer(
                model,
                messages,
            )

            print("\nFinal answer:")
            print(final_answer)
    
if __name__ == "__main__":
    asyncio.run(main())