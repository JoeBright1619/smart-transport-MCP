from mcp.server.mcpserver import MCPServer
import httpx
from auth import AuthManager

auth = AuthManager()

mcp = MCPServer("Smart Transport")


BACKEND_URL = "http://localhost:8000/api/v1"


@mcp.tool()
async def get_all_routes() -> dict:
    """Get all routes available to the current user's tenant."""

    response = await auth.request(
        "GET",
        "/routes",
    )

    response.raise_for_status()

    return response.json()
    
@mcp.tool()
async def get_route(route_id: int) -> dict:
    """Get information about a bus route."""

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/routes/{route_id}"
        )

        response.raise_for_status()

        return response.json()


if __name__ == "__main__":
    mcp.run()