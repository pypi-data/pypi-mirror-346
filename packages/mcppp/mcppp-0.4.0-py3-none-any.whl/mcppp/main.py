from fastmcp import FastMCP

mcp = FastMCP(name="mcppp") # type: ignore

@mcp.tool()
def get_db_names():
    """
    获取所有数据库名称
    """
    return ["db1", "db2"]

def run():
    mcp.run()
