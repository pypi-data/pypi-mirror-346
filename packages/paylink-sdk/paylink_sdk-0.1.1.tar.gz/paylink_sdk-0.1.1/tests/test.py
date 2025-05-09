from paylink_sdk import PayLinkClient
import asyncio

async def main():
    client = PayLinkClient("http://localhost:8050/sse")
    tools = await client.list_tools()
    for tool in tools:
        print(tool)

asyncio.run(main())