from mcp.server.mcpserver import Context
from auth import AuthManager


def register_trip_tools(server):

    @server.tool()
    async def get_all_trips(ctx: Context) -> dict:
        """Get trips available to the current user's tenant."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/trips",
        )

        response.raise_for_status()

        return response.json()

    @server.tool()
    async def get_trip_details(
        trip_id: str,
        ctx: Context,
    ) -> dict:
        """Get details about a specific trip."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/trips/{trip_id}",
        )

        response.raise_for_status()

        return response.json()