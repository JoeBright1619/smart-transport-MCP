from datetime import date

from mcp.server.fastmcp import Context

from auth import AuthManager

AUTH_BASE_URL = "http://localhost:8000"
def register_superadmin_tools(server):
    @server.tool()
    async def get_all_tenants(
        ctx: Context,
        is_active: bool | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Get a paginated list of all tenants on the platform."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str | int | bool] = {
            "page": page,
            "page_size": page_size,
        }

        if is_active is not None:
            params["isActive"] = is_active

        response = await auth.request(
            "GET",
            "/superadmin/tenants",
            base_url=AUTH_BASE_URL,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_tenant_details(
        ctx: Context,
        tenant_id: str,
    ) -> dict:
        """Get detailed information about a specific tenant."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/superadmin/tenants/{tenant_id}",
            base_url=AUTH_BASE_URL,
        )
        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_all_passenger_accounts(
        ctx: Context,
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Get a paginated list of passenger accounts across the platform."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str | int] = {
            "page": page,
            "pageSize": page_size,
        }

        if search is not None:
            params["search"] = search

        response = await auth.request(
            "GET",
            "/superadmin/passengers",
            base_url=AUTH_BASE_URL,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_passenger_usage_report(
        ctx: Context,
        passenger_id: str,
        date_from: date,
        date_to: date,
    ) -> dict:
        """Get a passenger's transport usage report for a date range."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str] = {
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
        }

        response = await auth.request(
            "GET",
            f"/superadmin/passengers/{passenger_id}/report",
            base_url=AUTH_BASE_URL,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_platform_analytics(
        ctx: Context,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> dict:
        """Get platform-wide analytics. Defaults to the last 7 days."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str] = {}

        if from_date is not None:
            params["from"] = from_date.isoformat()

        if to_date is not None:
            params["to"] = to_date.isoformat()

        response = await auth.request(
            "GET",
            "/superadmin/analytics",
            base_url=AUTH_BASE_URL,
            params=params,
        )
        response.raise_for_status()
        return response.json()