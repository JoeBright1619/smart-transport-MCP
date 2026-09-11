from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer

from auth import AuthManager


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


@mcp.tool()
async def get_all_routes(ctx: Context) -> dict:
    """Get information on all existing routes."""

    auth: AuthManager = ctx.request_context.lifespan_context["auth"]

    response = await auth.request(
        "GET",
        "/routes",
    )

    response.raise_for_status()

    return response.json()

    
@mcp.tool()
async def get_route(route_id: str, ctx: Context) -> dict:
    """Get information about a bus route."""
    auth: AuthManager = ctx.request_context.lifespan_context["auth"]
    response = await auth.request(
        "GET",
        f"/routes/{route_id}"
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    mcp.run()