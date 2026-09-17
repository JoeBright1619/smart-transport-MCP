import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

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

    for tool in tools:
        print(f"\nTool: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Schema: {tool.args_schema}")
    
if __name__ == "__main__":
    asyncio.run(main())