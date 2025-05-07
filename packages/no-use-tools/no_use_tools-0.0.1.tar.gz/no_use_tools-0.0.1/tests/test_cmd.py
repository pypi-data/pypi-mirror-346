import asyncio
import json

import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import TextContent, Tool


@pytest.fixture
def server_params():
    return StdioServerParameters(command="mcp-yahoo-finance")


@pytest.fixture
def client_tools() -> list[Tool]:
    server_params = StdioServerParameters(command="mcp-yahoo-finance")

    async def _get_tools():
        async with (
            stdio_client(server_params) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            tool_list_result = await session.list_tools()
            return tool_list_result.tools

    return asyncio.run(_get_tools())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_name",
    [
        "get_current_stock_price",
        "cmd_run",  
    ],
)
async def test_list_tools(client_tools: list[Tool], tool_name) -> None:
    tool_names = [tool.name for tool in client_tools]
    assert tool_name in tool_names

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cmd, expect_in_output",
    [
        ("whoami", "ubuntu"),                 # 正常退出
    ],
)
async def test_cmd_run(server_params, cmd, expect_in_output):
    """
    Call the cmd_run tool and check that stdout / error information
    is returned as expected.
    """
    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        tool_result = await session.call_tool("cmd_run", {"cmd": cmd})

        assert len(tool_result.content) == 1
        assert isinstance(tool_result.content[0], TextContent)

        output_text = tool_result.content[0].text.lower()
        assert expect_in_output.lower() in output_text

