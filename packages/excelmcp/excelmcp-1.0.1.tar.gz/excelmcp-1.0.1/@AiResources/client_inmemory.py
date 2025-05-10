from fastmcp import FastMCP, Client
from fastmcp.client.transports import FastMCPTransport

# 1. Create your FastMCP server instance
server = FastMCP(name="ExcelMCP")
@server.tool()
def ping(): return "pong"

# 2. Create a client pointing directly to the server instance
# Option A: Inferred
client_inferred = Client(server)

## Option B: Explicit
#transport_explicit = FastMCPTransport(mcp=server)
#client_explicit = Client(transport_explicit)

# 3. Use the client (no subprocess or network involved)
async def test_in_memory():
    async with client_inferred: # Or client_explicit
        result = await client_inferred.call_tool("ping")
        print(f"In-memory call result: {result[0].text}") # Output: pong