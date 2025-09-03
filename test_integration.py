import asyncio
import time
import subprocess
from pathlib import Path

import httpx
from fastmcp.client import Client


BASE_URL = "http://127.0.0.1:8000"
MCP_URL = f"{BASE_URL}/mcp"


def wait_for_server(timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            # hit a simple route to see if server is alive
            r = httpx.get(BASE_URL + "/files/download/does_not_exist.txt")
            if r.status_code in (200, 400, 404):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


async def run_client_tests():
    async with Client(MCP_URL) as client:
        tools = await client.list_tools()
        tool_names = [t.name for t in tools]
        print("Available tools:", tool_names)
        # 1) Install a small dependency
        assert "install_dependencies" in tool_names, tool_names
        res = await client.call_tool("install_dependencies", {"packages": ["tabulate==0.9.0"]})
        payload = res.data or res.structured_content or {}
        assert payload.get("returncode") == 0, payload

        # 2) Execute code that produces a plot
        code = (
            "import matplotlib.pyplot as plt\n"
            "plt.plot([1,2,3],[3,2,1])\n"
            "plt.title('it works')\n"
            "plt.show()\n"
        )
        out = await client.call_tool("run_python_code", {"code": code})
        payload = out.data or out.structured_content or {}
        assert isinstance(payload, dict)
        assert any(name.endswith((".png", ".svg")) for name in payload.get("new_files", [])), payload

        # 3) Define a variable and list it
        await client.call_tool("run_python_code", {"code": "myvar = 42"})
        check = await client.call_tool("run_python_code", {"code": "print(myvar)"})
        payload = check.data or check.structured_content or {}
        assert payload.get("stdout", "").strip() == "42", payload

        # 4) Restart kernel and ensure variable is gone
        rk = await client.call_tool("restart_kernel")
        payload = rk.data or rk.structured_content or {}
        assert payload.get("restarted") is True, payload
        check2 = await client.call_tool("run_python_code", {"code": "print('ok' if 'myvar' in globals() else 'missing')"})
        payload2 = check2.data or check2.structured_content or {}
        assert payload2.get("stdout", "").strip() == "missing", payload2

        # 5) Save and run a script
        script_body = (
            "from pathlib import Path\n"
            "print('hello from script')\n"
            "Path('hello.txt').write_text('hi')\n"
        )
        saved = await client.call_tool("save_script", {"name": "demo", "content": script_body})
        payload = saved.data or saved.structured_content or {}
        script_rel = payload.get("script")
        assert script_rel and script_rel.endswith(".py"), payload
        runres = await client.call_tool("run_script", {"path": script_rel})
        payload = runres.data or runres.structured_content or {}
        assert payload.get("returncode") == 0, payload
        assert "hello.txt" in payload.get("new_files", []), payload

        # 6) Read and write workspace files
        read1 = await client.call_tool("read_file", {"path": "hello.txt"})
        payload = read1.data or read1.structured_content or {}
        assert payload.get("text") == "hi", payload
        wr = await client.call_tool("write_file", {"path": "data/out.txt", "content": "data-123"})
        payload = wr.data or wr.structured_content or {}
        assert payload.get("path") == "data/out.txt", payload
        read2 = await client.call_tool("read_file", {"path": "data/out.txt"})
        payload = read2.data or read2.structured_content or {}
        assert payload.get("text") == "data-123", payload

        # 7) Upload and download via routes
        async with httpx.AsyncClient() as hc:
            tmp = Path("test_upload.txt")
            tmp.write_text("route-test")
            with tmp.open("rb") as f:
                r = await hc.post(BASE_URL + "/files/upload", files={"file": ("route.txt", f)})
                assert r.status_code == 200
            r2 = await hc.get(BASE_URL + "/files/download/route.txt")
            assert r2.status_code == 200 and r2.content.decode("utf-8") == "route-test"


def main():
    # ensure workspace exists
    Path("workspace").mkdir(exist_ok=True)
    # start server
    proc = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        ok = wait_for_server()
        if not ok:
            print("Server did not become ready. Logs:")
            try:
                # drain what we can
                out = proc.stdout.read()
                print(out)
            except Exception:
                pass
            raise SystemExit(1)
        asyncio.run(run_client_tests())
        print("Integration tests completed successfully.")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
