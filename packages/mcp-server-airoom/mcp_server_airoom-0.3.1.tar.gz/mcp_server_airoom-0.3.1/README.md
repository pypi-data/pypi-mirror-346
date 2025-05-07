# GXB MCP时间服务器 (v0.1.1)

这是一个实现MCP协议的时间服务器，提供获取当前时间和格式化日期等功能。
通过MCP协议，大语言模型可以使用这个服务器来获取实时时间信息。

## 安装

\`\`\`bash
pip install mcp-server-gxb
\`\`\`

## 功能

### 工具 (Tools)

-   \`get_current_time\`: 获取当前系统的精确时间。
-   \`format_date(format_string: str)\`: 按照指定格式格式化当前日期和时间。

### 资源 (Resources)

-   \`time://current_iso\`: 提供ISO格式的当前时间。

## 在阿里云百炼中使用

在阿里云百炼平台的MCP服务配置中，使用以下JSON：

\`\`\`json
{
  "mcpServers": {
    "gxb-time-server": {  // 服务名称，可自定义
      "command": "uvx",
      "args": ["mcp-server-gxb"] // 使用您在PyPI上发布的包名
    }
  }
}
\`\`\`

## 本地运行

安装后，您可以在本地通过以下方式运行：

\`\`\`bash
# 使用uvx (模拟平台行为)
uvx mcp-server-gxb

# 使用包提供的命令 (通过entry_points)
mcp-server-gxb

# 使用Python -m
python -m mcp_server_gxb
\`\`\`

按 \`Ctrl+C\` 停止服务器。

## 许可证

MIT License