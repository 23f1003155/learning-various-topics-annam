# server.py — MCP Server (the tools live here)
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

if __name__ == "__main__":
    mcp.run()