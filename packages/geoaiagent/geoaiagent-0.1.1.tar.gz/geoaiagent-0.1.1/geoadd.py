from mcp.server import FastMCP
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions


server = FastMCP("geoadd")
    
@server.tool()
async def add_geo(lat: float, lon: float) -> float:
    """
    Adds a new geolocation to the database.
    """
    return lat + lon
@server.tool()
async def sub_geo(lat: float, lon: float) -> float:
    """
    Subtracts a geolocation from the database.
    """
    return lat - lon

# @server.list_tools()
# async def list_tools() -> list:
#     """
#     Lists all available tools.
#     """
#     return ["add_geo", "sub_geo"]

def main():
    server.run()
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()