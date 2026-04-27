# FireSpot 4.0 - AI Content Creation Agent

FireSpot 4.0 是一个基于 DeerFlow 的 AI 内容创作智能体，专门用于微信公众号文章的研究、创作和发布。

## 项目概述

FireSpot 4.0 实现了一个完整的 7 阶段内容创作工作流：

1. **Research (热点研究)** - 使用 web_search 工具收集最新信息
2. **Analysis (深度分析)** - 使用 web_reader 工具深度阅读关键文章
3. **Planning (结构规划)** - 规划文章结构和大纲
4. **Writing (文章撰写)** - 生成高质量原创文章
5. **Validation (质量验证)** - 验证文章质量和准确性
6. **Review (内容审校)** - 审核和完善文章内容
7. **Publishing (自动发布)** - 自动发布到微信公众号

## 核心特性

- **自动触发机制** - 根据关键词自动激活 FireSpot 工作流
- **7 阶段工作流** - 系统化的内容创作流程
- **搜索重试机制** - 确保信息收集的可靠性
- **发布工具集成** - 支持微信公众号草稿箱自动发布与 OpenAI-compatible 生图工具
- **LangGraph 集成** - 完全集成到 DeerFlow 框架

## MCP / 生图说明

FireSpot 现已包含可直接拷贝到 DeerFlow 侧使用的 MCP server 实现，位置在 [mcp-servers/wechat/](mcp-servers/wechat/)。

运行时通常仍由 DeerFlow 侧通过 `extensions_config.json` 连接 `wechat-publisher` SSE 服务；如需自动生图，请在 DeerFlow 的 `.env` 或进程环境中配置：

```bash
OPENAI_IMAGE_BASE_URL=https://your-openai-compatible-gateway/v1
OPENAI_IMAGE_API_KEY=your-image-api-key
OPENAI_IMAGE_MODEL=gpt-image-2
```

## 项目结构

```
FireSpot_4.0/
├── README.md                    # 项目说明
├── INSTALLATION.md              # 安装指南
├── USAGE.md                     # 使用指南
├── ARCHITECTURE.md              # 架构文档
├── agent/                       # Agent 代码
│   ├── __init__.py             # Agent 工厂函数
│   ├── auto_trigger.py         # 自动触发机制
│   ├── middleware.py           # 自定义中间件
│   ├── publishing_tools.py     # 发布工具
│   └── search_retry.py         # 搜索重试
├── skills/                      # Skills 文件
│   └── firespot/
│       └── SKILL.md            # 技能描述
├── mcp-servers/                  # 微信发布 / 生图 MCP server
│   └── wechat/
│       ├── server.py             # wechat-publisher SSE server
│       └── start_wechat_server.sh # 启动脚本
```

## 安装

详见 [INSTALLATION.md](docs/INSTALLATION.md)

## 使用

详见 [USAGE.md](docs/USAGE.md)

## 架构

详见 [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 版本历史

- **4.0.0** (2025-04-13) - 完整 DeerFlow 集成版本
  - 7 阶段工作流实现
  - 自动触发机制
  - 微信公众号发布集成

## 许可证

MIT License

## 作者

FireSpot Team

## 致谢

基于 DeerFlow 框架构建
