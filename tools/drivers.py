from mcp.server.mcpserver import Context

from auth import AuthManager


def register_driver_tools(server):
    @server.tool()
    async def get_all_drivers(ctx: Context) -> dict:
        """Get information on all drivers."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/drivers",
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_driver_details(driver_id: str, ctx: Context) -> dict:
        """Get information about a specific driver."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/drivers/{driver_id}",
        )

        response.raise_for_status()
        return response.json()