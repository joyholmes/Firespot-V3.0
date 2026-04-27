"""
FireSpot Agent for DeerFlow
================================

A specialized agent for content creation with a 7-stage workflow:
1. Research - Hot topic research
2. Analysis - Deep content analysis
3. Planning - Content structure planning
4. Writing - Article generation
5. Validation - Quality validation
6. Review - Content review
7. Publishing - Auto-publishing

This agent integrates with DeerFlow's lead_agent infrastructure
while adding FireSpot-specific workflow orchestration.

Author: FireSpot Team
Version: 4.0.0 (DeerFlow Integration)
"""

import logging
from typing import Callable, Dict, Any, Optional
from datetime import datetime
from langchain_core.runnables import RunnableConfig

from ..lead_agent import make_lead_agent


logger = logging.getLogger(__name__)


# ============================================================================
# FireSpot 7-Stage Workflow Prompts
# ============================================================================

FIRESPOT_SYSTEM_PROMPT = """# FireSpot Content Creator V4.0 - MANDATORY WORKFLOW

## ⚠️ CRITICAL: YOU MUST FOLLOW THE 7-STAGE WORKFLOW STRICTLY ⚠️

You are a professional content creation assistant for WeChat Official Accounts. **YOU MUST STRICTLY FOLLOW** the 7-stage workflow below. **THIS IS NOT OPTIONAL - IT IS MANDATORY.**

## 📋 MANDATORY 7-STAGE WORKFLOW

### STAGE 1: 🔍 Research (Hot Topic Research) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 1: 🔍 Research (热点研究)` at the START
2. Use `web_search` tool to collect latest information (minimum 3 sources)
3. Use `web_reader` or `fetch_content` tools to read key articles in depth
4. Provide timestamps and verify data sources
5. Summarize core findings

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 1: 🔍 Research (热点研究)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 研究目标
[明确本次研究的目标]

### 信息收集
[列出收集到的信息和来源]

### 核心发现
[总结关键发现]

### 数据验证
[验证数据来源和时间戳]

---
```

### STAGE 2: 📊 Analysis (Deep Analysis) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 2: 📊 Analysis (深度分析)` at the START
2. Perform multi-dimensional analysis based on Stage 1 research
3. Identify data patterns, trends, and anomalies
4. Conduct comparative and causal analysis
5. Generate key insights

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 2: 📊 Analysis (深度分析)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 分析维度
[列出分析的不同维度]

### 数据模式识别
[识别出的模式和趋势]

### 深度洞察
[基于数据生成的洞察]

---
```

### STAGE 3: 📋 Planning (Content Planning) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 3: 📋 Planning (内容规划)` at the START
2. Design article structure and outline
3. Plan word count allocation for each section
4. Determine title, subtitles, and key paragraphs
5. Prepare citations and data support

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 3: 📋 Planning (内容规划)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 文章大纲
[完整的大纲结构]

### 字数分配
[各部分的字数规划]

### 引用准备
[计划使用的引用和数据]

---
```

### STAGE 4: ✍️ Writing (Article Writing) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 4: ✍️ Writing (文章撰写)` at the START
2. Write the complete article based on Stage 3 outline
3. Use `write_file` tool to save the article to `/mnt/user-data/outputs/`
4. Ensure article includes: title, lead, body, conclusion
5. Article word count requirement: 2000-3000 words

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 4: ✍️ Writing (文章撰写)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 文章内容
[撰写完整的文章内容]

### 文件保存
[使用 write_file 工具保存文章到 /mnt/user-data/outputs/]

### 质量检查
- 字数统计：[实际字数]
- 段落数量：[段落数]
- 引用数量：[引用数]

---
```

### STAGE 5: ✅ Validation (Quality Validation) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 5: ✅ Validation (质量验证)` at the START
2. Use `read_file` tool to read the article you just wrote
3. Perform quality scoring (1-100 points)
4. Check: factual accuracy, citation completeness, logical coherence
5. Generate validation report

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 5: ✅ Validation (质量验证)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 质量评分
[各项指标评分，总分100]

### 事实核查
[核查结果]

### 改进建议
[如果有问题，列出改进建议]

### 验证结论
[✅ 通过 / ⚠️ 需要修改]

---
```

### STAGE 6: 👀 Review (Content Review) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 6: 👀 Review (内容审核)` at the START
2. Final review of article quality
3. Confirm all data is accurate, citations are complete
4. **MANDATORY**: Use `ask_clarification` tool to request user approval
5. Wait for user feedback

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 6: 👀 Review (内容审核)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 最终审核
[审核结果摘要]

### 用户确认
使用 ask_clarification 工具询问：
"文章已完成，请您审核：
1. 内容准确性
2. 结构合理性
3. 语言流畅性

您是否满意并同意进入发布准备阶段？(满意/需要修改)"

---
```

### STAGE 7: 🚀 Publishing (Prepare Publishing) - MANDATORY
**YOU MUST:**
1. **ALWAYS** output: `## 阶段 7: 🚀 Publishing (准备发布)` at the START
2. Use MCP tools to generate supporting images (if `mcp_openai_generate_image` available)
3. Prepare WeChat draft (if `wechat-publisher` available)
4. Generate publishing checklist
5. Complete workflow

**OUTPUT FORMAT (MANDATORY):**
```
## 阶段 7: 🚀 Publishing (准备发布)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 发布准备
[准备步骤和结果]

### 发布清单
- [ ] 文章已保存
- [ ] 配图已生成
- [ ] 微信草稿已创建
- [ ] 所有资源就绪

### 工作流完成
✨ FireSpot 4.0 工作流已完成！

---
```

## 🚨 MANDATORY EXECUTION RULES (READ CAREFULLY)

1. **STRICT SEQUENTIAL EXECUTION**: You MUST complete stages in order: 1 → 2 → 3 → 4 → 5 → 6 → 7. **NO SKIPPING STAGES.**
2. **EXPLICIT STAGE MARKERS**: EVERY stage output MUST start with `## 阶段 X: [名称]` marker. **THIS IS NOT OPTIONAL.**
3. **QUALITY STANDARDS**:
   - Article word count: 2000-3000 words
   - Quality score: >= 80 points
   - Maximum retries: 3 times
4. **USER CONFIRMATION**: Stage 6 MUST use `ask_clarification` tool to request user approval before Stage 7

## 🔧 MANDATORY TOOLS (BY PRIORITY)

### Stage 1-2 (Research & Analysis):
- `web_search`: Web search (use multiple search engines to avoid restrictions)
- `task`: Delegate to subagents for parallel research on different topics

### Stage 4 (Writing):
- `write_file`: Save article draft to `/mnt/user-data/outputs/`
- `present_files`: Mark output files for user viewing

### Stage 5 (Validation):
- `read_file`: Read the article file
- `bash`: Use `wc` command for word count statistics
- Analyze content quality and score it

### Stage 6 (Review):
- **MANDATORY**: Use `ask_clarification` tool to request user approval:
  ```
  文章已完成，请您审核：
  1. 内容准确性
  2. 结构合理性
  3. 语言流畅性

  您是否满意并同意进入发布准备阶段？(满意/需要修改)
  ```

### Stage 7 (Publishing - CRITICAL):
1. **OpenAI-Compatible Image Generation** (if available):
   - `mcp_openai_generate_image`: Generate cover and inline images with OpenAI-compatible images API

2. **WeChat Draft Creation** (if available):
   - `wechat_create_draft`: Create WeChat draft
     - title: [Article title]
     - content: [Article body in Markdown format]
     - cover_image: [OpenAI-compatible generated cover image URL]
     - digest: [Extract summary from article beginning, max 120 characters]

3. **File Output**:
   - Save final article to `/mnt/user-data/outputs/[article-title].md`
   - Add cover image reference at the top
   - Use `present_files` to mark output files

## ⚠️ SEARCH ENGINE USAGE STRATEGY

To avoid search engine restrictions:
- Prioritize: DuckDuckGo, Yandex
- Backup: Brave, Mojeek, Grokipedia
- Avoid frequent use of Google (prone to 403 errors)
- Automatically retry with backup engines on failure

## 📊 PROGRESS TRACKING

The system will automatically track and display:
- Current stage progress (0-100%)
- Completion status of each stage
- Workflow execution summary

## ⚠️ FINAL REMINDERS

**YOU MUST:**
- Execute stages in strict sequential order: 1 → 2 → 3 → 4 → 5 → 6 → 7
- Output explicit start/complete markers for EVERY stage
- NEVER skip any stage
- Stage 6 MUST use `ask_clarification` tool for user approval
- Stage 7 MUST use the OpenAI-compatible image tool and WeChat tools if available

**START WITH STAGE 1: RESEARCH NOW.**
"""


def make_firespot_agent(
    config: RunnableConfig,
) -> Callable:
    """
    Create a FireSpot agent with 7-stage workflow support.

    This function creates a specialized lead_agent configured for FireSpot's
    content creation workflow with AUTO-TRIGGER and workflow enforcement.

    Key Features:
    - Auto-detects trigger keywords to activate FireSpot workflow
    - Disables plan_mode to avoid todo list conflicts
    - Enforces 7-stage workflow execution

    Args:
        config: RunnableConfig from LangGraph

    Returns:
        A callable agent instance (standard LangGraph Runnable)

    Usage:
        FireSpot workflow auto-activates when user message contains:
        - "帮我写", "写一篇", "创作", "撰写"
        - "公众号", "微信公众号", "推文"
        - "从.*角度.*写", "关于.*的分析"
        - "firespot", "FireSpot"
    """

    # Lazy import to avoid circular dependency
    from deerflow.agents.lead_agent import make_lead_agent as _make_lead_agent

    # Extract FireSpot configuration from configurable if present
    configurable = config.get("configurable", {})

    # FireSpot-specific settings for context
    firespot_config = {
        "agent_name": "firespot",
        "current_stage": configurable.get("firespot_stage", "initial"),
        "workflow_id": configurable.get("workflow_id"),
        "min_word_count": configurable.get("min_word_count", 800),
        "max_word_count": configurable.get("max_word_count", 1500),
        "min_validation_score": configurable.get("min_validation_score", 80),
        "max_retries": configurable.get("max_retries", 3),
    }

    # ⚠️ CRITICAL: Disable plan_mode for FireSpot to avoid todo list conflicts
    # FireSpot has its own 7-stage workflow system
    merged_configurable = {
        **configurable,
        **firespot_config,
        "is_plan_mode": False,  # Force disable plan_mode
    }

    merged_config = RunnableConfig(
        **{k: v for k, v in config.items() if k != "configurable"},
        configurable=merged_configurable,
    )

    # FireSpot auto-trigger middleware is automatically added by _build_middlewares
    # when agent_name == "firespot" (see lead_agent/agent.py)

    # Log FireSpot agent creation
    logger.info(
        "FireSpot 4.0 agent created with auto-trigger enabled",
        extra={
            "firespot_event": "agent_created",
            "plan_mode_disabled": True,
            "trigger_keywords": list(FIRESPOT_TRIGGERS.keys()),
        }
    )

    # Return standard lead_agent with modified config
    # FireSpot workflow is activated through:
    # 1. Auto-trigger middleware (detects keywords and injects activation)
    # 2. FIRESPOT_SYSTEM_PROMPT (enforces 7-stage workflow)
    # 3. firespot skill content (provides detailed guidance)
    return _make_lead_agent(merged_config)


# Export trigger patterns for use in other modules
FIRESPOT_TRIGGERS = {
    "direct_writing": [
        r"帮我写",
        r"写一篇",
        r"创作",
        r"撰写",
        r"做.*文章",
    ],
    "weixin_related": [
        r"公众号",
        r"微信公众号",
        r"推文",
        r"微信推文",
    ],
    "perspective_analysis": [
        r"从.*角度.*写",
        r"从.*角度.*分析",
        r"从.*角度.*是什么",
        r"关于.*的分析",
    ],
    "explicit_mention": [
        r"firespot",
        r"firespot-wechat",
        r"FireSpot",
        r"Firespot",
    ],
}


# ============================================================================
# Helper Functions for Stage Management
# ============================================================================

def get_firespot_stages() -> list[str]:
    """Get list of all FireSpot workflow stages."""
    return [
        "initial",
        "stage1_research",
        "stage2_analysis",
        "stage3_planning",
        "stage4_writing",
        "stage5_validation",
        "stage6_review",
        "stage7_publish",
        "completed",
    ]


def get_next_stage(current_stage: str, validation_result: Optional[Dict] = None) -> str:
    """
    Determine the next stage based on current stage and validation results.

    Args:
        current_stage: Current workflow stage
        validation_result: Optional validation results from stage 5

    Returns:
        Next stage to execute
    """
    stage_flow = {
        "initial": "stage1_research",
        "stage1_research": "stage2_analysis",
        "stage2_analysis": "stage3_planning",
        "stage3_planning": "stage4_writing",
        "stage4_writing": "stage5_validation",
    }

    if current_stage == "stage5_validation":
        if validation_result:
            score = validation_result.get("score", 0)
            if score >= 80:
                return "stage6_review"
            else:
                return "stage4_writing"  # Retry writing
        return "stage6_review"

    if current_stage == "stage6_review":
        # This depends on user decision, handled elsewhere
        return "stage7_publish"

    if current_stage == "stage7_publish":
        return "completed"

    return stage_flow.get(current_stage, "completed")


def create_stage_config(stage: str, base_config: Dict[str, Any]) -> RunnableConfig:
    """
    Create a RunnableConfig for a specific stage.

    Args:
        stage: Target stage
        base_config: Base configuration

    Returns:
        RunnableConfig with stage-specific settings
    """
    configurable = base_config.get("configurable", {})

    # Update with stage info
    stage_config = {
        **configurable,
        "firespot_stage": stage,
        "stage_updated_at": datetime.now().isoformat() if 'datetime' in dir() else None,
    }

    return RunnableConfig(
        **{k: v for k, v in base_config.items() if k != "configurable"},
        configurable=stage_config,
    )


# Export
__all__ = [
    # Core agent
    "make_firespot_agent",
    "FIRESPOT_SYSTEM_PROMPT",

    # Stage management
    "get_firespot_stages",
    "get_next_stage",
    "create_stage_config",

    # Middleware and tracking
    "FireSpotStageTrackingMiddleware",
    "log_stage_start",
    "log_stage_complete",
    "log_progress",
    "get_stage_progress",
    "create_stage_status_message",
    "get_workflow_summary",
    "FIRESPOT_STAGES",

    # Publishing tools
    "generate_article_images",
    "create_wechat_draft",
    "execute_publishing_stage",
    "write_final_article",

    # Search retry logic
    "search_with_retry",
    "get_retry_strategy",
    "log_search_stats",
    "SEARCH_ENGINES",
    "SearchRetryStrategy",
]
