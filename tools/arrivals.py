from mcp.server.fastmcp import Context

from auth import AuthManager


def register_arrival_tools(server):
    @server.tool()
    async def get_public_arrivals(
        ctx: Context,
        stop_id: str,
    ) -> dict:
        """Get bus arrival predictions from all operators for a stop."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/arrivals/public",
            params={
                "stop_id": stop_id,
            },
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_arrivals(
        ctx: Context,
        stop_id: str,
    ) -> dict:
        """Get predicted bus arrivals for a stop within the current operator."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/arrivals",
            params={
                "stopId": stop_id,
            },
        )

        response.raise_for_status()
        return response.json()