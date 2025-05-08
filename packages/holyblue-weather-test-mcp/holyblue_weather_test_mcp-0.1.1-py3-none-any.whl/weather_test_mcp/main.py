from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP(
    name='check-weather-mcp-server',
    instructions="""\
    指定された場所の天気情報を返します。
    """
)

@mcp.tool()
async def check_weather(
    location: str
) -> str:
    """指定された場所の天気情報を返します。"""
    return f"[MCP回答] {location}は晴天です ☀️"

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()