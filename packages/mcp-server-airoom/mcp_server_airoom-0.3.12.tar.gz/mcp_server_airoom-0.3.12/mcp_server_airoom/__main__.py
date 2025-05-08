"""MCP服务器主入口点"""

import sys
import traceback
import datetime

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误：需要安装 'mcp' 包才能运行此服务器。", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("AIROOM时间服务器")

@mcp.tool()
def get_current_time() -> str:
    now = datetime.datetime.now()
    print(f"工具 'get_current_time' 被调用", file=sys.stderr)
    return f"当前时间是: {now.strftime('%Y-%m-%d %H:%M:%S.%f')}"

@mcp.tool()
def format_date(format_string: str = "%Y年%m月%d日 %H时%M分%S秒") -> str:
    now = datetime.datetime.now()
    print(f"工具 'format_date' 被调用，格式: {format_string}", file=sys.stderr)
    return now.strftime(format_string)

@mcp.resource("time://current_iso")
def current_time_iso_resource() -> str:
    now = datetime.datetime.now()
    print(f"资源 'time://current_iso' 被访问", file=sys.stderr)
    return now.isoformat()

def main():
    try:
        print("AIROOM MCP时间服务器正在启动...", file=sys.stderr)
        mcp.run()
        print("AIROOM MCP时间服务器已停止。", file=sys.stderr)
    except Exception as e:
        print(f"运行时发生错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()