import asyncio
import json
import os

import httpx
from dotenv import load_dotenv
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

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


def convert_mcp_tools(tools):
    result = []

    for tool in tools:
        result.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema,
                },
            }
        )

    return result


async def ask_llm(
    client: httpx.AsyncClient,
    messages: list[dict],
    tools: list[dict],
):
    response = await client.post(
        f"{OMNIROUTE_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OMNIROUTE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OMNIROUTE_MODEL,
            "messages": messages,
            "tools": tools,
        },
    )

    response.raise_for_status()

    return response.json()

async def run_agent(
    session: ClientSession,
    http_client: httpx.AsyncClient,
    messages: list[dict],
    mcp_tools: list[dict],
    max_iterations: int = 5,
):
    for iteration in range(max_iterations):
        print(f"\n--- Agent iteration {iteration + 1} ---")

        result = await ask_llm(
            http_client,
            messages,
            mcp_tools,
        )

        message = result["choices"][0]["message"]

        # No tool call means the LLM is ready to answer the user.
        if not message.get("tool_calls"):
            return message.get("content", "")

        # Add the assistant's tool-call message to the conversation.
        messages.append(message)

        for tool_call in message["tool_calls"]:
            tool_name = tool_call["function"]["name"]

            arguments = json.loads(
                tool_call["function"]["arguments"]
            )

            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")

            try:
                tool_result = await session.call_tool(
                    tool_name,
                    arguments=arguments,
                )

                tool_content = tool_result.content[0].text

                print("Tool result received.")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": tool_content,
                    }
                )

            except Exception as exc:
                print(f"Tool error: {exc}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": f"Tool execution failed: {exc}",
                    }
                )

    messages.append(
    {
        "role": "user",
        "content": (
            "You have reached the maximum number of tool-use "
            "iterations. Please answer the original request "
            "using the information you have already collected. "
            "Do not call any more tools."
        ),
    }
    )

    result = await ask_llm(
        http_client,
        messages,
        [],
    )

    return result["choices"][0]["message"].get(
        "content",
        "I couldn't complete the request.",
    )

async def main():
    server_params = StdioServerParameters(
        command=".venv\\Scripts\\python.exe",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            mcp_tools = convert_mcp_tools(
                tools_result.tools
            )

            print(
                f"Loaded {len(mcp_tools)} MCP tools."
            )

            user_message = input("\nYou: ")

            messages = [
                {
                    "role": "user",
                    "content": user_message,
                }
            ]

            async with httpx.AsyncClient(timeout=120.0) as http_client:
                final_answer = await run_agent(
                    session,
                    http_client,
                    messages,
                    mcp_tools,
                )

            print("\nFinal answer:")
            print(final_answer)
if __name__ == "__main__":
    asyncio.run(main())