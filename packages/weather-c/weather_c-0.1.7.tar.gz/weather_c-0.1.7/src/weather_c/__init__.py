from .weather_c import mcp

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')