from mcp.server.mcpserver import Context

from auth import AuthManager


def register_audit_tools(server):
    @server.tool()
    async def get_audit_logs(
        ctx: Context,
        page: int = 1,
        page_size: int = 50,
        action: str | None = None,
        resource_type: str | None = None,
    ) -> dict:
        """Get tenant audit logs with optional action and resource type filters."""
        auth: AuthManager = ctx.request_context.lifespan_context["auth"]

        params: dict[str, str | int] = {
            "page": page,
            "page_size": page_size,
        }

        if action is not None:
            params["action"] = action

        if resource_type is not None:
            params["resource_type"] = resource_type

        response = await auth.request(
            "GET",
            "/audit",
            params=params,
        )
        response.raise_for_status()
        return response.json()