import os
import sys
import argparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

# 自动添加项目根目录到PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()


@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_directory(path: str = ""):
    # 如果路径为空，设置为当前目录
    if not path:
        path = ".."

    # 如果是根路径，检查 index.html
    if path == "." and os.path.isfile("index.html"):
        return FileResponse("index.html")

    # 如果是目录，列出内容
    if os.path.isdir(path):
        items = sorted(os.listdir(path))
        response = f"<html><body><h2>Directory listing for /{path}</h2><ul>"

        # 目录的相对路径
        parent_dir = os.path.dirname(path)
        if parent_dir:
            response += f'<li><a href="../">../ (Parent)</a></li>'

        for item in items:
            full_path = os.path.join(path, item)
            display_name = item + "/" if os.path.isdir(full_path) else item
            href = f"{path}/{item}".strip("/")
            response += f'<li><a href="/{href}">{display_name}</a></li>'

        response += "</ul></body></html>"
        return HTMLResponse(content=response)

    # 如果是文件，返回文件内容
    if os.path.isfile(path):
        return FileResponse(path)

    # 如果都不是，返回404
    raise HTTPException(status_code=404, detail="File not found")


def run_server(port: int):
    import uvicorn
    uvicorn.run("local_server.server:app", host="0.0.0.0", port=port, reload=True)


def main():
    print('local-server')
    parser = argparse.ArgumentParser(description="FastAPI HTTP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
