from datetime import date

from mcp.server.mcpserver import Context

from auth import AuthManager


def register_boarding_tools(server):
    @server.tool()
    async def get_boarding_records(
        ctx: Context,
        trip_id: str | None = None,
        stop_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Get boarding records with optional trip, stop, date, and pagination filters."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str | int] = {
            "page": page,
            "pageSize": page_size,
        }

        if trip_id is not None:
            params["tripId"] = trip_id

        if stop_id is not None:
            params["stopId"] = stop_id

        if date_from is not None:
            params["dateFrom"] = date_from.isoformat()

        if date_to is not None:
            params["dateTo"] = date_to.isoformat()

        response = await auth.request(
            "GET",
            "/boardings",
            params=params,
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_my_boardings(
        ctx: Context,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Get the current passenger's recorded boarding history."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            "/boardings/me",
            params={
                "page": page,
                "pageSize": page_size,
            },
        )

        response.raise_for_status()
        return response.json()