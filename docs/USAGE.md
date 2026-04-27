# FireSpot 4.0 使用指南

## 触发方式

FireSpot 4.0 支持两种触发方式：

### 1. 自动触发（推荐）

FireSpot 会自动检测以下关键词并激活：

- **直接写作**: "帮我写", "写一篇", "创作", "撰写"
- **微信相关**: "公众号", "微信公众号", "推文"
- **视角分析**: "从.*角度.*写", "从.*角度.*分析"
- **明确提及**: "FireSpot", "firespot"

### 2. 手动选择

在 Agent 选择界面选择 "FireSpot Agent"

## 使用示例

### 示例 1: 写一篇 AI 科普文章

```
请帮我写一篇关于 AI 大模型基础知识的科普系列推文，
第一章节先建立AI世界观。第一章轻以：什么是 AI？从规则到学习的进化史为题，
从AI历史演进，重大AI科技节点事件，当前AI的市场发展状态，当前制约AI的发展瓶颈
（技术，政治，人文伦理等方面分析），最后引入到本系列推文的学习课程，
引导各位读者关注并学习AI系列课程。写一篇推文2500字推文。不用插图，
经过审核后上传至公众号草稿箱
```

### 示例 2: 热点话题分析

```
从科技发展的角度分析当前最热门的 AI 话题，
写一篇深度分析文章，发布到微信公众号
```

## 工作流程

FireSpot 会自动执行 7 个阶段：

1. **🔍 Research** - 搜索相关热点信息
2. **📊 Analysis** - 深度分析关键内容
3. **📋 Planning** - 规划文章结构
4. **✍️ Writing** - 撰写文章内容
5. **✅ Validation** - 验证质量
6. **👀 Review** - 审核内容
7. **🚀 Publishing** - 发布到草稿箱

## 输出结果

- 完整的文章内容
- 结构化的分析报告
- 自动发布到微信草稿箱（需要配置）
- 可选的 OpenAI-compatible 生图能力（依赖 DeerFlow 侧 MCP 与环境变量配置）

## 高级功能

### 搜索重试机制

FireSpot 会自动重试失败的搜索，最多 3 次。

### 自定义发布平台

详见 [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 注意事项

- 确保已配置微信 MCP 服务器
- FireSpot 仓库内置的 `mcp-servers/wechat/` 可直接作为 `wechat-publisher` SSE 服务启动
- 如需自动生图，确保 DeerFlow 侧已启用 `wechat-publisher` MCP 服务，并配置 `OPENAI_IMAGE_BASE_URL`、`OPENAI_IMAGE_API_KEY`、`OPENAI_IMAGE_MODEL`
- 首次使用需要授权微信访问
- 文章会自动保存到草稿箱，需手动审核后发布

## 常见问题

详见 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
