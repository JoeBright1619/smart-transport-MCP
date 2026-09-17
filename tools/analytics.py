from datetime import date

from mcp.server.fastmcp import Context

from auth import AuthManager


def register_analytics_tools(server):
    @server.tool()
    async def get_fleet_analytics(
        ctx: Context,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> dict:
        """Get fleet analytics for a date range. Defaults to the last 7 days."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params = {}

        if from_date is not None:
            params["from"] = from_date.isoformat()

        if to_date is not None:
            params["to"] = to_date.isoformat()

        response = await auth.request(
            "GET",
            "/analytics",
            params=params,
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_filtered_analytics_report(
        ctx: Context,
        report_type: str,
        route_id: str | None = None,
        vehicle_id: str | None = None,
        driver_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> dict:
        """Get a filtered analytics report."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params = {
            "report_type": report_type,
        }

        if route_id is not None:
            params["route_id"] = route_id

        if vehicle_id is not None:
            params["vehicle_id"] = vehicle_id

        if driver_id is not None:
            params["driver_id"] = driver_id

        if date_from is not None:
            params["date_from"] = date_from.isoformat()

        if date_to is not None:
            params["date_to"] = date_to.isoformat()

        response = await auth.request(
            "GET",
            "/analytics/report",
            params=params,
        )

        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_passenger_trip_report(
        ctx: Context,
        passenger_id: str,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> dict:
        """Get the trip history report for a specific passenger."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params = {
            "passenger_id": passenger_id,
        }

        if date_from is not None:
            params["date_from"] = date_from.isoformat()

        if date_to is not None:
            params["date_to"] = date_to.isoformat()

        response = await auth.request(
            "GET",
            "/analytics/passenger-report",
            params=params,
        )

        response.raise_for_status()
        return response.json()