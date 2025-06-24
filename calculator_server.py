# calculator_server.py
from fastmcp import FastMCP

mcp = FastMCP("CalculatorServer")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract_numbers(a: int, b: int) -> int:
    """Subtract second number from first number"""
    return a - b

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b

@mcp.tool()
def divide_numbers(a: int, b: int) -> float:
    """Divide first number by second number"""
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

@mcp.tool()
def calculate_power(base: int, exponent: int) -> int:
    """Calculate base raised to the power of exponent"""
    return base ** exponent

if __name__ == "__main__":
    print("🚀 Starting Calculator MCP Server on http://localhost:8001")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8001) 