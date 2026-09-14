import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    server_params = StdioServerParameters(
        command=".venv\\Scripts\\python.exe",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tools = tools_result.tools

            available_tools = {
                tool.name: tool
                for tool in tools
            }

            print("\nAvailable tools:")
            for index, tool in enumerate(tools, start=1):
                print(f"{index}. {tool.name}")

            while True:
                tool_name = input(
                    "\nEnter tool name (or 'exit'): "
                ).strip()

                if tool_name.lower() == "exit":
                    break

                tool = available_tools.get(tool_name)

                if tool is None:
                    print("Unknown tool.")
                    continue

                print(f"\nDescription: {tool.description}")
                print(f"Input schema: {tool.input_schema}")

                properties = tool.input_schema.get("properties", {})
                required = tool.input_schema.get("required", [])

                arguments = {}

                for name, schema in properties.items():
                    is_required = name in required
                    default = schema.get("default")
                    value_type = schema.get("type")

                    if default is not None:
                        prompt = f"Enter {name} (default: {default}): "
                    elif is_required:
                        prompt = f"Enter {name} (required): "
                    else:
                        prompt = f"Enter {name} (optional): "

                    while True:
                        value = input(prompt).strip()

                        if not value:
                            if default is not None:
                                break

                            if not is_required:
                                break

                            print(f"{name} is required.")
                            continue

                        if value_type == "integer":
                            try:
                                value = int(value)
                            except ValueError:
                                print(f"{name} must be an integer.")
                                continue

                        elif value_type == "boolean":
                            if value.lower() in ("true", "yes", "1"):
                                value = True
                            elif value.lower() in ("false", "no", "0"):
                                value = False
                            else:
                                print(f"{name} must be true or false.")
                                continue

                        arguments[name] = value
                        break

                print("\nArguments:")
                print(arguments)

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                print("\nResult:")
                print(result)


if __name__ == "__main__":
    asyncio.run(main())