from mcp.server.fastmcp import Context

from auth import AuthManager


def register_alert_tools(server):
    @server.tool()
    async def get_all_alerts(ctx: Context) -> dict:
        """Get information on all system alerts."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/alerts",
        )

        response.raise_for_status()
        return response.json()