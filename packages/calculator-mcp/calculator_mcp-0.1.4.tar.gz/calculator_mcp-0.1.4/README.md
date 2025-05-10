# Calculator MCP - Learning Project

This project, `calculator-mcp`, was built for learning purposes. It provides an MCP (Multi-Agent Communication Protocol) server that exposes basic calculator tools. These tools can be integrated with other systems, such as LangGraph agents.

The server gives you access to the following calculator tools:
1.  `add(a: float, b: float) -> float`
2.  `subtract(a: float, b: float) -> float`
3.  `multiply(a: float, b: float) -> float`
4.  `divide(a: float, b: float) -> float`

## Installation

You can install the `calculator-mcp` package directly using pip:

```bash
pip install calculator-mcp
```


## Usage with LangGraph

You can use `calculator-mcp` as a tool within a LangGraph agent.

1.  **Create a Python script to run the MCP server (e.g., `cal_mcp.py`):**

    ```python
    # cal_mcp.py
    from calculator_mcp import serve

    if __name__ == "__main__":
        serve()
    ```

2.  **Configure the tool in your LangGraph agent:**

    ```python
    # Example LangGraph tool configuration
    tools_config = {
        "calculator": {
            "command": "python",
            # Replace with the absolute path to your cal_mcp.py file
            "args": ["/path/to/your/cal_mcp.py"],
            "transport": "stdio",
        }
    }
    ```

**Author:** Azam Afridi (azamafridi.ai@gmail.com)
**Version:** 0.1.4
**Python:** >=3.10