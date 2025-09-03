"""Entry points for the python-mcp-server package.

Note: During the rename step, the actual server implementation still lives in
the project-level `main.py`. We provide lightweight wrappers that delegate to
that module for local development. In a subsequent step, we'll move the server
implementation into this package and expose a proper console script for uvx.
"""

def main() -> None:
    # Temporary shim to run the dev server via package entry-point
    try:
        import main as _main  # type: ignore
    except Exception as e:  # pragma: no cover - only hit if package used standalone
        raise SystemExit(
            "python_mcp_server.server.main(): implementation not packaged yet. "
            "Run `python main.py` for now."
        ) from e
    _main.mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":  # pragma: no cover
    main()
