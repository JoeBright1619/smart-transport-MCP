import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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

    response = await model.ainvoke(
        "Explain what an MCP server is in one sentence."
    )

    print("\nResponse:")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())