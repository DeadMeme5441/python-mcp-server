# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: FastMCP server exposing tools and routes.
- `workspace/`: Runtime artifacts (images, uploads, temp files). Do not commit.
- `test_client.py`, `test_workspace.py`: Example scripts to exercise the server/tools.
- `pyproject.toml`, `uv.lock`: Project metadata and locked dependencies.

## Build, Test, and Development Commands
- Setup: `uv sync` (installs deps into `.venv` from `pyproject.toml/uv.lock`).
- Run server: `uv run python main.py` (or `python main.py` with the venv activated).
- Exercise tools: `uv run python test_client.py` (plots via `run_python_code`).
- Workspace flow: `uv run python test_workspace.py` (upload/download/list/delete).

## Coding Style & Naming Conventions
- Python 3.12, 4‑space indentation, PEP 8/257 docstrings.
- Prefer type hints and explicit returns.
- Module layout: keep new tools in `main.py` or a small helper module; name tools with snake_case (e.g., `list_files`).
- Avoid side effects at import time; keep startup in `if __name__ == "__main__":`.

## Testing Guidelines
- Current tests are example scripts (no pytest). Keep new examples as `test_*.py` at repo root for easy discovery.
- Validate: start server, run example scripts, and confirm outputs in `workspace/` and console.
- Aim for clear, minimal repros when adding new tests (inputs, expected outputs).

## Commit & Pull Request Guidelines
- Commits: imperative, present tense, focused (e.g., "add list_files tool"). Group related changes.
- PRs: include a brief description, how to run locally, and screenshots/log snippets when applicable. Link related issues.
- Keep diffs minimal; avoid committing `workspace/` artifacts or virtualenvs.

## MCP/Agent Notes
- Tools: annotate with `@mcp.tool` and return JSON‑serializable data. Example: `@mcp.tool\nasync def list_files(ctx: Context) -> dict: ...`.
- Custom routes: use `@mcp.custom_route("/path", methods=["GET","POST"])` for uploads/downloads.
- Kernel: code executes in a persistent Jupyter kernel; prefer writing binary outputs to `workspace/` and return file names.
- Safety: avoid reading/writing outside `workspace/`; handle errors with clear JSON responses and status codes.
