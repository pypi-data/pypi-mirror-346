from fastmcp import FastMCP

mcp = FastMCP(name="mcppp") # type: ignore

@mcp.tool()
def get_db_names():
    return ["db1", "db2"]

def run():
    mcp.run()
