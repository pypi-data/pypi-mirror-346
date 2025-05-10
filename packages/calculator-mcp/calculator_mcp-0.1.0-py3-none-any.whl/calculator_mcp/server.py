from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator")

@mcp.tool()
def add(a: float, b: float) -> float:
    try:
        return a + b
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def subtract(a: float, b: float) -> float:
    try:
        return a - b
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def multiply(a: float, b: float) -> float:
    try:
        return a * b
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def divide(a: float, b: float) -> float:
    try:
        return a / b
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()