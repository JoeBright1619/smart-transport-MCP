from mcp.server.mcpserver import Context

from auth import AuthManager


def register_maintenance_tools(server):
    @server.tool()
    async def get_all_maintenance_records(ctx: Context) -> dict:
        """Get information on all vehicle maintenance records."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/maintenance",
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_maintenance_details(
        maintenance_id: str,
        ctx: Context,
    ) -> dict:
        """Get information about a specific maintenance record."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/maintenance/{maintenance_id}",
        )

        response.raise_for_status()
        return response.json()