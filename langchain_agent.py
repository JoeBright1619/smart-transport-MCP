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

    try:
        result = await agent.ainvoke(
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
        )

        print("\nFinal answer:")
        print(result["messages"][-1].content)

    except GraphRecursionError:
        print("\nAgent stopped: recursion limit reached.")
    
if __name__ == "__main__":
    asyncio.run(main())