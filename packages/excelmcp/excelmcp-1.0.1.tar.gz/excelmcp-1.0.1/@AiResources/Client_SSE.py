import asyncio
from fastmcp import Client, FastMCP
from fastmcp.client.transports import SSETransport
sse_url = "http://localhost:8000/sse"  
print(sse_url)
#client = Client(sse_url)#SSETransport(url=sse_url))
client = Client(SSETransport(url=sse_url))
async def main():
     async with client:
        print(client.transport)
        tools = await client.list_tools()
        #print(f"Available tools: {tools}")
        #await client.call_tool("Visible", {"tobe": True})
        result = await client.call_tool("Launch", {"visible": True})
        result = await client.call_tool("Demostrate")
        result = await client.call_tool("ActiveWorkbook")
        print(result)
        result = await client.call_tool("ActiveSheet")
        print(result)
if __name__ == "__main__":
    asyncio.run(main())