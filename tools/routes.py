from mcp.server.mcpserver import Context
from auth import AuthManager

def register_route_tools(server):
    @server.tool()
    async def get_route_details(route_id: str, ctx: Context) -> dict:
        """Get information about a bus route."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]
        response = await auth.request(
            "GET",
            f"/routes/{route_id}"
        )

        response.raise_for_status()

        return response.json()
    
    @server.tool()
    async def get_all_routes(ctx: Context) -> dict:
        """Get information on all existing routes."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/routes",
        )

        response.raise_for_status()

        return response.json()

