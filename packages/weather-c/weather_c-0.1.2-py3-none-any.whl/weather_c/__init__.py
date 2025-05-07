from mcp.server.fastmcp import FastMCP

def main():
    print("Hello from weather-c!")
    mcp = FastMCP("weather")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
