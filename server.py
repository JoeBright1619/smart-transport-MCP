from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer

from auth import AuthManager
from tools.routes import register_router_tools

@asynccontextmanager
async def lifespan(server: MCPServer) -> AsyncIterator[dict]:
    auth = AuthManager()

    await auth.start()

    try:
        yield {
            "auth": auth,
        }
    finally:
        await auth.close()


mcp = MCPServer(
    name="Smart Transport",
    lifespan=lifespan,
)

register_router_tools(mcp)

    

if __name__ == "__main__":
    mcp.run()