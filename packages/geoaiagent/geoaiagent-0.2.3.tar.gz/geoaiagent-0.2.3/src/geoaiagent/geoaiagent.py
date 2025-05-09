from mcp.server import Server
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions


# server = FastMCP("geoaiagent")
    
# @server.tool()
# async def add_geo(lat: float, lon: float) -> float:
#     """
#     Adds a new geolocation to the database.
#     """
#     return lat + lon
# @server.tool()
# async def sub_geo(lat: float, lon: float) -> float:
#     """
#     Subtracts a geolocation from the database.
#     """
#     return lat - lon

# @server.list_tools()
# async def list_tools() -> list:
#     """
#     Lists all available tools.
#     """
#     return ["add_geo", "sub_geo"]
server = Server("geoaiagent")

@server.call_tool()
async def add_geo(lat: float, lon: float) -> float:
    """
    两数相加
    """
    return lat + lon

@server.list_tools()
async def list_tools() -> list:
    """
    列出所有可用工具
    """
    return ["add_geo"]

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="geotest",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def doit():
    print("Hello from aiagent!")
    run()
    

