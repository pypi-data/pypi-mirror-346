import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp import ClientSession

async def main():
    server_params = StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp-yahoo-finance:latest"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Found {len(tools.tools)} tools")
            for tool in tools.tools:
                print(f"- {tool.name}")

asyncio.run(main())
