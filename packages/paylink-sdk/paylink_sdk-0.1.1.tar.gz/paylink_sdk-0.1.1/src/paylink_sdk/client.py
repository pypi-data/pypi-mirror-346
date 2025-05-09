import asyncio
from contextlib import asynccontextmanager
from mcp import ClientSession
from mcp.client.sse import sse_client


class PayLinkClient:
    """
    Client for interacting with the PayLink MCP server.
    """

    def __init__(self, server_url: str = "http://paylink-app.eastus.azurecontainer.io:8050/sse"):
        self.server_url = server_url

    @asynccontextmanager
    async def connect(self):
        """
        Async context manager to connect to the MCP server.
        """
        # Remove the 'url=' named parameter
        async with sse_client(self.server_url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session

    async def list_tools(self):
        """
        List all available tools from the server.

        Args:
            verbose (bool): If True, prints the tools.

        Returns:
            list: A list of ToolDescription objects.
        """
        async with self.connect() as session:
            tools_result = await session.list_tools()
            return tools_result.tools


# -------- Convenience Function --------

async def list_tools(server_url: str = "http://paylink-app.eastus.azurecontainer.io:8050/sse", verbose=False):
    client = PayLinkClient(server_url)
    return await client.list_tools()


# -------- Run Directly --------

if __name__ == "__main__":
    tools = asyncio.run(list_tools())
    for tool in tools:
        print(tool)
        print("\n")