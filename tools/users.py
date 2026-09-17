from mcp.server.fastmcp import Context

from auth import AuthManager


def register_user_tools(server):
    @server.tool()
    async def get_all_users(
        ctx: Context,
        role: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Get a paginated list of users in the current tenant."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str | int] = {
            "page": page,
            "page_size": page_size,
        }

        if role is not None:
            params["role"] = role

        response = await auth.request(
            "GET",
            "/users",
            params=params,
        )
        response.raise_for_status()
        return response.json()

    @server.tool()
    async def get_user_details(
        ctx: Context,
        user_id: str,
    ) -> dict:
        """Get information about a specific user."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        response = await auth.request(
            "GET",
            f"/users/{user_id}",
        )
        response.raise_for_status()
        return response.json()