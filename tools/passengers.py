from mcp.server.mcpserver import Context

from auth import AuthManager


def register_passenger_tools(server):
    @server.tool()
    async def get_my_passenger_profile(ctx: Context) -> dict:
        """Get the current passenger's profile."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/passengers/me",
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_my_passenger_stats(ctx: Context) -> dict:
        """Get the current passenger's journey statistics."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/passengers/me/stats",
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_my_passenger_notifications(ctx: Context) -> dict:
        """Get notifications for the current passenger's favourite stops."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/passengers/me/notifications",
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_transport_operators(ctx: Context) -> dict:
        """Get all active transport operators."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/passengers/operators",
        )

        response.raise_for_status()
        return response.json()