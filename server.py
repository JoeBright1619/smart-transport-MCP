from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer

from auth import AuthManager
from tools.alerts import register_alert_tools
from tools.drivers import register_driver_tools
from tools.maintenance import register_maintenance_tools
from tools.passengers import register_passenger_tools
from tools.routes import register_route_tools
from tools.stops import register_stop_tools
from tools.trips import register_trip_tools
from tools.vehicles import register_vehicle_tools
from tools.analytics import register_analytics_tools
from tools.arrivals import register_arrival_tools
from tools.boardings import register_boarding_tools


@asynccontextmanager
async def lifespan(server: MCPServer) -> AsyncIterator[dict]:
    auth = AuthManager()

    await auth.start()

    try:
        yield {
            "auth": auth,
        }
    finally:
        await auth.close()


mcp = MCPServer(
    name="Smart Transport",
    lifespan=lifespan,
)

register_route_tools(mcp)
register_vehicle_tools(mcp)
register_stop_tools(mcp)
register_trip_tools(mcp)
register_driver_tools(mcp)
register_maintenance_tools(mcp)
register_passenger_tools(mcp)
register_alert_tools(mcp)
register_analytics_tools(mcp)
register_arrival_tools(mcp)
register_boarding_tools(mcp)
    

if __name__ == "__main__":
    mcp.run()