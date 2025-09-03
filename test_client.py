
import asyncio
from fastmcp.client import Client

async def main():
    client = Client("http://127.0.0.1:8000/mcp")
    async with client:
        result = await client.call_tool(
            "run_python_code",
            {"code": "import matplotlib.pyplot as plt; plt.plot([1, 2, 3, 4]);"}
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
