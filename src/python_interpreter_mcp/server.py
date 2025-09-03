"""MCP Server entry for Python Interpreter MCP.

Provides a persistent Jupyter kernel and file/script utilities over FastMCP.
Run via: `python -m python_interpreter_mcp` or console script.
"""

from ._server_impl import create_app


def main():
    app = create_app()
    app.run(transport="http", host=app._host, port=app._port)  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()

