import os
import time
import subprocess
from typing import Iterator

import httpx
import pytest


BASE_URL = "http://127.0.0.1:8000"


def _wait_for_server(timeout: float = 20.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get(BASE_URL + "/files/download/does_not_exist.txt")
            if r.status_code in (200, 400, 404):
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


@pytest.fixture(scope="session")
def server_proc() -> Iterator[subprocess.Popen]:
    env = os.environ.copy()
    proc = subprocess.Popen([env.get("PYTHON", "python"), "main.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        ok = _wait_for_server()
        if not ok:
            # dump logs for debugging
            try:
                out = proc.stdout.read()
                print("--- server logs ---\n" + (out or ""))
            except Exception:
                pass
            raise RuntimeError("server did not start")
        yield proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


@pytest.fixture(scope="session")
def base_url(server_proc) -> str:  # noqa: ARG001 unused
    return BASE_URL


@pytest.fixture(scope="session")
def mcp_url(base_url: str) -> str:
    return base_url + "/mcp"

