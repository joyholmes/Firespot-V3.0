# FireSpot 4.0 修复总结报告

## 执行时间
2026-04-11

## 问题描述

用户报告任务 `8d6823a5-1b5e-4d45-b324-dce1d40727b5` 未遵循 FireSpot 4.0 的 7 阶段工作流。

### 发现的问题
1. ❌ **MCP 服务器未运行** - 0 个 MCP 工具被加载
2. ❌ **firespot skill 不存在** - skills/public/ 目录下没有 firespot skill
3. ❌ **系统提示不够强制** - LLM 选择不遵循工作流
4. ❌ **Middleware 仅被动检测** - 不主动强制执行工作流
5. ❌ **无阶段标记输出** - 生成的内容没有任何阶段标记
6. ❌ **无质量评分** - 没有输出评分或验证报告

## 修复措施

### ✅ 1. 增强了 FireSpotStageTrackingMiddleware

**文件**: `/Users/garywong/deer-flow/backend/packages/harness/deerflow/agents/firespot/middleware.py`

**改进**:
- 添加了 `expected_stage` 跟踪
- 添加了 `stage_completions` 状态跟踪
- 实现了 `_inject_stage_guidance()` 方法，为每个阶段注入强制性的指导
- 实现了 `_get_expected_stage_marker()` 方法，验证阶段标记
- 实现了 `_log_stage_violation()` 方法，记录违规行为
- 实现了 `_advance_to_next_stage()` 方法，管理阶段转换
- 增强了 `before_model()` 方法，主动注入阶段指导
- 增强了 `after_model()` 方法，验证 LLM 是否遵循了阶段要求

**关键代码**:
```python
def _inject_stage_guidance(self, stage_id: str, messages: list) -> Optional[str]:
    """Inject stage-specific guidance to enforce workflow compliance."""
    stage_guidance = {
        "stage1_research": """
**【FireSpot 4.0 强制要求 - 阶段 1: Research 热点研究】**

你现在必须执行阶段 1：热点研究。这是第一阶段，不可跳过。

**你必须：**
1. 明确输出 "## 阶段 1: 🔍 Research (热点研究)" 标记
...
"""
```

### ✅ 2. 优化了 FireSpot 系统提示

**文件**: `/Users/garywong/deer-flow/backend/packages/harness/deerflow/agents/firespot/__init__.py`

**改进**:
- 将系统提示改为全英文大写警告："**YOU MUST STRICTLY FOLLOW**"
- 明确标注每个阶段为 "MANDATORY"
- 为每个阶段添加详细的输出格式要求
- 强调 "THIS IS NOT OPTIONAL - IT IS MANDATORY"
- 添加 "⚠️ FINAL REMINDERS" 部分
- 改变字数要求为 2000-3000 字（更合理）

**关键改进**:
```python
FIRESPOT_SYSTEM_PROMPT = """# FireSpot Content Creator V4.0 - MANDATORY WORKFLOW

## ⚠️ CRITICAL: YOU MUST FOLLOW THE 7-STAGE WORKFLOW STRICTLY ⚠️

You are a professional content creation assistant for WeChat Official Accounts.
**YOU MUST STRICTLY FOLLOW** the 7-stage workflow below.
**THIS IS NOT OPTIONAL - IT IS MANDATORY.**
...
"""
```

### ✅ 3. 创建了 FireSpot Skill

**文件**: `/Users/garywong/deer-flow/skills/public/firespot/SKILL.md`

**内容**:
- 完整的技能描述和触发关键词
- 详细的 7 阶段工作流说明
- 每个阶段的强制输出格式
- 执行规则和工具使用指南
- 中文说明（更适合中国用户）

**触发关键词**:
- "写一篇"
- "创作"
- "文章"
- "公众号"
- "内容创作"
- "firespot"

### ✅ 4. 更新了 firespot_agent 创建逻辑

**文件**: `/Users/garywong/deer-flow/backend/packages/harness/deerflow/agents/firespot/__init__.py`

**改进**:
- 修改 `make_firespot_agent()` 函数
- 导入 FireSpotStageTrackingMiddleware（虽然还未注入，但为未来做准备）
- 调整字数要求为 2000-3000 字
- 添加文档说明 middleware 的作用

## 预期效果

修复后，FireSpot 4.0 应该：

1. **✅ 严格遵循 7 阶段工作流**
   - 每个阶段都有明确的开始/完成标记
   - 不会跳过任何阶段
   - 按顺序执行：Research → Analysis → Planning → Writing → Validation → Review → Publishing

2. **✅ 输出标准化的阶段标记**
   ```
   ## 阶段 1: 🔍 Research (热点研究)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ...
   ```

3. **✅ 提供质量评分**
   - 阶段 5 会输出质量评分（0-100分）
   - 包含内容质量、逻辑连贯性、引用完整性等维度

4. **✅ 请求用户审核**
   - 阶段 6 必须使用 `ask_clarification` 工具
   - 等待用户批准才能进入阶段 7

5. **✅ 使用 MCP 工具**
   - 阶段 7 会使用 ModelArts 生成配图
   - 阶段 7 会创建微信草稿

## 剩余问题

### ⚠️ MCP 服务器未运行

**状态**: 未解决

**原因**: MCP 服务器配置正确（extensions_config.json），但服务器进程未启动

**影响**:
- 无法加载 OpenAI-compatible 生图工具
- 无法加载 WeChat 发布工具
- 阶段 7 的功能受限

**建议**:
1. 启动 wechat-publisher MCP 服务器: `http://localhost:3101/sse`
2. 确认 DeerFlow 侧 `wechat-publisher` MCP 服务可用，并已配置 OpenAI-compatible 生图环境变量
3. 或者修改代码，使这些工具变为可选

### ⚠️ Middleware 注入机制

**状态**: 部分完成

**当前状态**:
- FireSpotStageTrackingMiddleware 已创建
- 但尚未注入到 lead_agent 的 middleware 链中

**原因**: `make_lead_agent()` 不支持 `custom_middlewares` 参数

**建议**:
1. 修改 `make_lead_agent()` 添加 `custom_middlewares` 参数
2. 或者创建一个专门的 `make_firespot_agent()` 完整实现
3. 或者使用 agent_config 来指定要加载的 middleware

## 测试建议

1. **重新运行之前的任务**
   ```
   Thread ID: 8d6823a5-1b5e-4d45-b324-dce1d40727b5
   ```

2. **验证检查点**:
   - [ ] 阶段 1: 是否输出了 `## 阶段 1: 🔍 Research (热点研究)` 标记
   - [ ] 阶段 2: 是否输出了 `## 阶段 2: 📊 Analysis (深度分析)` 标记
   - [ ] 阶段 3: 是否输出了 `## 阶段 3: 📋 Planning (内容规划)` 标记
   - [ ] 阶段 4: 是否输出了 `## 阶段 4: ✍️ Writing (文章撰写)` 标记
   - [ ] 阶段 5: 是否输出了 `## 阶段 5: ✅ Validation (质量验证)` 标记
   - [ ] 阶段 6: 是否输出了 `## 阶段 6: 👀 Review (内容审核)` 标记
   - [ ] 阶段 6: 是否使用了 `ask_clarification` 工具
   - [ ] 阶段 7: 是否输出了 `## 阶段 7: 🚀 Publishing (准备发布)` 标记

3. **日志检查**:
   - 查看 `/Users/garywong/deer-flow/logs/langgraph.log`
   - 搜索 "FireSpot Stage Start" 确认阶段转换
   - 搜索 "FireSpot Stage Violation" 检查是否有违规

## 修改文件清单

1. `/Users/garywong/deer-flow/backend/packages/harness/deerflow/agents/firespot/middleware.py` - 增强 middleware
2. `/Users/garywong/deer-flow/backend/packages/harness/deerflow/agents/firespot/__init__.py` - 优化系统提示和 agent 创建逻辑
3. `/Users/garywong/deer-flow/skills/public/firespot/SKILL.md` - 创建新 skill 文件

## 下一步行动

1. **重启服务** - 使代码修改生效
   ```bash
   cd /Users/garywong/deer-flow
   make stop
   make dev
   ```

2. **启动 DeerFlow 侧图片/发布 MCP 能力**（可选）
   ```bash
   # 确保 wechat-publisher 已启用
   # 并在 DeerFlow 环境中配置 OPENAI_IMAGE_BASE_URL / OPENAI_IMAGE_API_KEY / OPENAI_IMAGE_MODEL
   ```

3. **测试验证**
   - 运行一个新的内容创作任务
   - 验证 7 阶段工作流是否被正确执行
   - 检查日志输出

## 总结

本次修复主要解决了 FireSpot 4.0 工作流强制执行的问题：

1. ✅ 增强了 middleware 的主动执行能力
2. ✅ 优化了系统提示，使其更加强制和明确
3. ✅ 创建了 firespot skill，提供详细的中文指导
4. ⚠️ MCP 服务器问题需要单独处理
5. ⚠️ Middleware 注入机制需要进一步完善

**预期**: 修复后，LLM 应该能够更严格地遵循 FireSpot 4.0 的 7 阶段工作流。
