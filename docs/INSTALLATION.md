# FireSpot 4.0 安装指南

## 前置要求

- DeerFlow 框架已安装并运行
- Python 3.12+
- LangGraph API
- 如需自动生图，DeerFlow 运行环境中需提供：
  - `OPENAI_IMAGE_BASE_URL`
  - `OPENAI_IMAGE_API_KEY`
  - `OPENAI_IMAGE_MODEL`

## 安装步骤

### 1. 安装 Agent 代码

将 `agent/` 目录复制到 DeerFlow 的 agents 目录：

```bash
cp -r agent/* /path/to/deerflow/backend/packages/harness/deerflow/agents/firespot/
```

### 2. 安装 Skills

将 `skills/firespot/` 目录复制到 DeerFlow 的 skills 目录：

```bash
cp -r skills/firespot/ /path/to/deerflow/skills/public/firespot/
```

### 3. 配置 Agent

创建 Agent 配置文件：

```bash
mkdir -p /path/to/deerflow/backend/.deer-flow/agents/firespot/
cp config/firespot.yaml /path/to/deerflow/backend/.deer-flow/agents/firespot/config.yaml
```

### 4. 注册 Graph

在 `backend/langgraph.json` 中添加：

```json
{
  "graphs": {
    "firespot_agent": "deerflow.agents:make_firespot_agent"
  }
}
```

### 5. 重启服务

```bash
# 在 DeerFlow 项目根目录执行
make stop
make dev
```

### 6. 配置 MCP 与生图环境

FireSpot 仓库已包含 `mcp-servers/wechat/`，其中提供 `wechat-publisher` SSE 服务实现。

如需在 DeerFlow 中启用它：

1. 启动 MCP server：

```bash
cd /path/to/Firespot-V3.0/mcp-servers/wechat
./start_wechat_server.sh
```

2. 在 DeerFlow 的 `extensions_config.json` 中启用：

```json
{
  "mcpServers": {
    "wechat-publisher": {
      "enabled": true,
      "type": "sse",
      "url": "http://localhost:3101/sse"
    }
  }
}
```

3. 如需启用自动生图，请在 DeerFlow 的 `.env` 或进程环境中配置：

```bash
OPENAI_IMAGE_BASE_URL=https://your-openai-compatible-gateway/v1
OPENAI_IMAGE_API_KEY=your-image-api-key
OPENAI_IMAGE_MODEL=gpt-image-2
```

## 验证安装

访问 http://localhost:2026/workspace/agents/firespot

## 故障排除

详见 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
