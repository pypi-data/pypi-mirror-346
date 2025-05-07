from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
def get_weather_info(name: str) -> str:
    """
    获取天气信息
    """
    print("get_weather_info" + name)
    return "天气信息"
