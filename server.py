from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer

from auth import AuthManager
from tools.routes import register_route_tools
from tools.vehicles import register_vehicle_tools
from tools.stops import register_stop_tools

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

register_route_tools(mcp)
register_vehicle_tools(mcp)
register_stop_tools(mcp)
    

if __name__ == "__main__":
    mcp.run()