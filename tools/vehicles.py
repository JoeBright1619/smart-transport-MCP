from mcp.server.fastmcp import Context
from auth import AuthManager


def register_vehicle_tools(server):

    @server.tool()
    async def get_all_vehicles(ctx: Context) -> dict:
        """Get vehicles available to the current user's tenant."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/vehicles",
        )

        response.raise_for_status()

        return response.json()

    @server.tool()
    async def get_vehicle_details(vehicle_id: str, ctx: Context) -> dict:
        """Get details about a specific vehicle."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/vehicles/{vehicle_id}",
        )

        response.raise_for_status()

        return response.json()

    @server.tool()
    async def get_vehicle_occupancy(vehicle_id: str, ctx: Context) -> dict:
        """Get the current occupancy of a vehicle."""

        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/vehicles/{vehicle_id}/occupancy",
        )

        response.raise_for_status()

        return response.json()