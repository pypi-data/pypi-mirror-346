import sys
import traceback
import datetime
# 确保安装了mcp包: pip install mcp
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误：需要安装 'mcp' 包才能运行此服务器。", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

# --- MCP服务器实现 ---
# 创建FastMCP服务器实例
mcp = FastMCP("GXB时间服务器") # 服务器名称

# 定义一个工具 (Tool)
@mcp.tool()
def get_current_time() -> str:
    now = datetime.datetime.now()
    print(f"工具 'get_current_time' 被调用", file=sys.stderr) # 增加日志
    return f"当前时间是: {now.strftime('%Y-%m-%d %H:%M:%S.%f')}"

# 定义另一个带参数的工具
@mcp.tool()
def format_date(format_string: str = "%Y年%m月%d日 %H时%M分%S秒") -> str:
    now = datetime.datetime.now()
    print(f"工具 'format_date' 被调用，格式: {format_string}", file=sys.stderr) # 增加日志
    return now.strftime(format_string)

# 定义一个资源 (Resource)
@mcp.resource("time://current_iso")
def current_time_iso_resource() -> str:
    now = datetime.datetime.now()
    print(f"资源 'time://current_iso' 被访问", file=sys.stderr) # 增加日志
    return now.isoformat()

# --- 服务器启动入口 ---
def main():
    try:
        print("GXB MCP时间服务器正在启动...", file=sys.stderr)
        # 可以在这里添加更多的启动逻辑或检查
        print("MCP服务器实例已创建，准备运行...", file=sys.stderr)
        mcp.run() # 启动服务器，此函数会阻塞直到服务器停止
        print("GXB MCP时间服务器已停止。", file=sys.stderr)
    except Exception as e:
        print(f"启动或运行时发生严重错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

# 允许直接通过 python -m mcp_server_gxb 运行
if __name__ == "__main__":
    main()