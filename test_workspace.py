
import asyncio
import httpx
from pathlib import Path
from fastmcp.client import Client

async def main():
    client = Client("http://127.0.0.1:8000/mcp")
    http_client = httpx.AsyncClient()

    async with client:
        # 1. List initial files
        print("--- Listing initial files ---")
        initial_files = await client.call_tool("list_files")
        print(initial_files)

        # 2. Upload a new file
        print("\n--- Uploading a new file ---")
        with open("test_upload.txt", "w") as f:
            f.write("This is a test file.")
        with open("test_upload.txt", "rb") as f:
            files = {"file": f}
            response = await http_client.post("http://127.0.0.1:8000/files/upload", files=files)
            print(response.json())

        # 3. List files again
        print("\n--- Listing files after upload ---")
        files_after_upload = await client.call_tool("list_files")
        print(files_after_upload)

        # 4. Download the uploaded file
        print("\n--- Downloading the uploaded file ---")
        response = await http_client.get("http://127.0.0.1:8000/files/download/test_upload.txt")
        with open("test_download.txt", "wb") as f:
            f.write(response.content)
        with open("test_download.txt", "r") as f:
            print(f.read())

        # 5. Delete the uploaded file
        print("\n--- Deleting the uploaded file ---")
        delete_result = await client.call_tool("delete_file", {"filename": "test_upload.txt"})
        print(delete_result)

        # 6. List files again
        print("\n--- Listing files after delete ---")
        files_after_delete = await client.call_tool("list_files")
        print(files_after_delete)

        # 7. Test code completion
        print("\n--- Testing code completion ---")
        completion_result = await client.call_tool("code_completion", {"code": "import num", "cursor_pos": 10})
        print(completion_result)

        # 8. Test object inspection
        print("\n--- Testing object inspection ---")
        inspection_result = await client.call_tool("inspect_object", {"code": "import numpy as np; np.array", "cursor_pos": 28})
        print(inspection_result)

        # Clean up local files
        Path("test_upload.txt").unlink()
        Path("test_download.txt").unlink()

if __name__ == "__main__":
    asyncio.run(main())
