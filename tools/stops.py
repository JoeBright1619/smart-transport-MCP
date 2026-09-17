from mcp.server.fastmcp import Context
from auth import AuthManager


def register_stop_tools(server):

    @server.tool()
    async def get_public_stops(ctx: Context) -> dict:
        """Get all public bus stops across all tenants."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/stops/public",
        )

        response.raise_for_status()

        return response.json()

    @server.tool()
    async def get_all_stops(ctx: Context) -> dict:
        """Get all bus stops available to the current user's tenant."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/stops",
        )

        response.raise_for_status()

        return response.json()