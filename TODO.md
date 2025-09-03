# MCP Server Implementation Plan (FastMCP)

## Phase 1: Core Execution and Workspace

- [x] **Project Setup**:
    - [x] Update `pyproject.toml` with dependencies.
    - [x] Create a `workspace` directory.

- [x] **Initial Server (`main.py`):**
    - [x] Set up a basic `FastMCP` application.
    - [x] Implement a singleton `KernelManager`.

- [x] **Core Tools & Routes:**
    - [x] Implement `run_python_code` tool.
    - [x] Implement `/outputs/{filename}` custom route.

## Phase 2: Full Workspace Functionality

- [x] **Jupyter-Powered Tools:**
    - [x] Implement `code_completion(code: str, cursor_pos: int)` tool.
    - [x] Implement `inspect_object(code: str, cursor_pos: int)` tool.
    - [x] Add `list_variables()` and `restart_kernel()` tools.

- [x] **File Management Tools:**
    - [x] Implement `list_files()` tool.
    - [x] Implement `delete_file(filename: str)` tool.
    - [x] Implement `read_file(path)` and `write_file(path, content)` tools.

- [x] **Enhanced File Handling (Custom Routes):**
    - [x] Implement `POST /files/upload` to handle file uploads.
    - [x] Implement `GET /files/download/{filename}` route.

- [x] **Script & Dependency Management:**
    - [x] Implement `save_script(name, content)` and `run_script(path, args)` tools.
    - [x] Implement `install_dependencies(packages: list[str])` using `uv pip` or `pip`.

## Phase 3: Enhancements (Future Work)

- [ ] **Lifecycle & State**:
    - [ ] Implement a tool to restart the kernel.
    - [ ] Add a tool to inspect the kernel's state (e.g., list variables).
- [ ] **Security & Robustness**:
    - [ ] Run the kernel in a sandboxed environment (e.g., a Docker container).
    - [ ] Add request validation and richer JSON schemas for tools.
