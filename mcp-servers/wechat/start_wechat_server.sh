#!/bin/bash
# 微信公众号 MCP 服务器启动脚本

set -euo pipefail

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

# 设置环境变量（从项目根目录的 .env 文件读取）
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
else
    echo "错误：未找到 .env 文件，请确保已配置微信公众账号凭证" >&2
    exit 1
fi

# 检查必需的环境变量
if [ -z "${WECHAT_APPID:-}" ] || [ -z "${WECHAT_APPSECRET:-}" ]; then
    echo "错误：请在 .env 文件中配置 WECHAT_APPID 和 WECHAT_APPSECRET" >&2
    exit 1
fi

if [ -x "$VENV_PYTHON" ]; then
    PYTHON_BIN="$VENV_PYTHON"
else
    PYTHON_BIN="python3"
fi

echo "微信公众号 MCP 服务器启动中..." >&2
echo "监听端口: 3101" >&2
echo "SSE 端点: http://localhost:3101/sse" >&2
echo "Python: $PYTHON_BIN" >&2

# 启动服务器
cd "$SCRIPT_DIR"
exec "$PYTHON_BIN" server.py
