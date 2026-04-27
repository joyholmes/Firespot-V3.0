"""
FireSpot Stage Tracking Middleware for DeerFlow
==============================================

This middleware tracks FireSpot 7-stage workflow execution,
provides progress visualization, and manages stage transitions.

Author: FireSpot Team
Version: 4.1.0 (Enhanced with Progress Tracking)
"""

import logging
from typing import Callable, Dict, Any, Optional
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, AIMessage

from ..thread_state import ThreadState


logger = logging.getLogger(__name__)


# ============================================================================
# Stage Configuration
# ============================================================================

FIRESPOT_STAGES = {
    "initial": {"name": "初始阶段", "emoji": "🎬", "progress": 0},
    "stage1_research": {"name": "Research 热点研究", "emoji": "🔍", "progress": 15},
    "stage2_analysis": {"name": "Analysis 深度分析", "emoji": "📊", "progress": 30},
    "stage3_planning": {"name": "Planning 内容规划", "emoji": "📋", "progress": 45},
    "stage4_writing": {"name": "Writing 文章撰写", "emoji": "✍️", "progress": 60},
    "stage5_validation": {"name": "Validation 质量验证", "emoji": "✅", "progress": 75},
    "stage6_review": {"name": "Review 内容审核", "emoji": "👀", "progress": 85},
    "stage7_publish": {"name": "Publishing 准备发布", "emoji": "🚀", "progress": 95},
    "completed": {"name": "完成", "emoji": "✨", "progress": 100},
}


# ============================================================================
# Progress Tracking Functions
# ============================================================================

def log_stage_start(stage_id: str, thread_id: str, run_id: str) -> None:
    """Log stage start with clear marker."""
    stage_info = FIRESPOT_STAGES.get(stage_id, {"name": stage_id, "emoji": "🔄"})
    logger.info(
        f"\n{'='*60}",
        f"\n{stage_info['emoji']} FireSpot Stage Start: {stage_info['name']}",
        f"\n{'='*60}",
        extra={
            "firespot_stage": stage_id,
            "firespot_event": "stage_start",
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
        }
    )


def log_stage_complete(stage_id: str, thread_id: str, run_id: str,
                       result: Optional[Dict] = None) -> None:
    """Log stage completion with result."""
    stage_info = FIRESPOT_STAGES.get(stage_id, {"name": stage_id, "emoji": "✅"})
    result_str = f" - Result: {result.get('summary', 'Success')}" if result else ""

    logger.info(
        f"\n{'='*60}",
        f"\n{stage_info['emoji']} FireSpot Stage Complete: {stage_info['name']}",
        f"\n{'='*60}",
        extra={
            "firespot_stage": stage_id,
            "firespot_event": "stage_complete",
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            **(result or {})
        }
    )


def log_progress(stage_id: str, thread_id: str, progress_message: str) -> None:
    """Log progress update within a stage."""
    stage_info = FIRESPOT_STAGES.get(stage_id, {"name": stage_id, "emoji": "🔄"})
    logger.info(
        f"{stage_info['emoji']} [{stage_info['name']}] {progress_message}",
        extra={
            "firespot_stage": stage_id,
            "firespot_event": "progress_update",
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat(),
        }
    )


def get_stage_progress(stage_id: str) -> int:
    """Get progress percentage for a stage."""
    return FIRESPOT_STAGES.get(stage_id, {}).get("progress", 0)


# ============================================================================
# FireSpot Stage Tracking Middleware
# ============================================================================

class FireSpotStageTrackingMiddleware:
    """
    Middleware to track and ENFORCE FireSpot 7-stage workflow execution.

    Features:
    - Automatic stage transition logging
    - Progress visualization
    - Stage completion tracking
    - User approval request handling
    - PROACTIVE stage enforcement via message injection
    """

    def __init__(self):
        self.current_stage = "initial"
        self.stage_results = {}
        self.expected_stage = "stage1_research"  # First expected stage
        self.stage_completions = {
            "stage1_research": False,
            "stage2_analysis": False,
            "stage3_planning": False,
            "stage4_writing": False,
            "stage5_validation": False,
            "stage6_review": False,
            "stage7_publish": False,
        }

    def before_model(self, state: ThreadState, config: RunnableConfig) -> Dict[str, Any]:
        """
        Called before model invocation.

        PROACTIVELY enforces FireSpot 7-stage workflow by:
        1. Detecting current stage from conversation history
        2. Injecting stage-specific guidance into state
        3. Tracking expected stage transitions
        """
        messages = state.get("messages", [])
        configurable = config.get("configurable", {})

        # Detect current stage from recent messages
        new_stage = self._detect_current_stage(messages, configurable)

        # Check if we're in the expected stage sequence
        stage_order = [
            "stage1_research",
            "stage2_analysis",
            "stage3_planning",
            "stage4_writing",
            "stage5_validation",
            "stage6_review",
            "stage7_publish",
        ]

        # If we're still in initial stage, expect research
        if self.current_stage == "initial":
            self.expected_stage = "stage1_research"

        # Validate stage transition
        if new_stage != self.current_stage:
            thread_id = configurable.get("thread_id", "unknown")
            run_id = configurable.get("run_id", "unknown")

            # Check if this is a valid transition
            if new_stage in stage_order:
                current_idx = stage_order.index(self.current_stage) if self.current_stage in stage_order else -1
                new_idx = stage_order.index(new_stage)

                # Only allow forward progression (or staying in same stage)
                if new_idx > current_idx:
                    # Mark previous stage as complete
                    if self.current_stage in stage_order:
                        self.stage_completions[self.current_stage] = True

                    log_stage_start(new_stage, thread_id, run_id)
                    self.current_stage = new_stage
                    self.expected_stage = new_stage

        # Inject stage guidance into state
        guidance = self._inject_stage_guidance(self.expected_stage, messages)
        if guidance:
            # Return guidance to be injected into the conversation
            return {"stage_guidance": guidance}

        return {}

    def after_model(self, state: ThreadState, config: RunnableConfig,
                    response: BaseMessage) -> Dict[str, Any]:
        """
        Called after model invocation.

        VALIDATES that the LLM followed the stage requirements:
        1. Checks for expected stage markers
        2. Validates stage completion
        3. Logs violations and warnings
        """
        if isinstance(response, AIMessage):
            content = response.content

            # Check if the expected stage marker is present
            expected_marker = self._get_expected_stage_marker(self.expected_stage)
            if expected_marker and expected_marker not in content:
                # LLM did not follow the stage requirement!
                thread_id = config.get("configurable", {}).get("thread_id", "unknown")
                self._log_stage_violation(self.expected_stage, expected_marker, thread_id, content)

            # Check for stage completion marker
            if "===" in content and "阶段" in content and "完成" in content:
                thread_id = config.get("configurable", {}).get("thread_id", "unknown")
                run_id = config.get("configurable", {}).get("run_id", "unknown")

                # Extract stage result
                result = self._extract_stage_result(content)
                self.stage_results[self.current_stage] = result

                log_stage_complete(self.current_stage, thread_id, run_id, result)

                # Move to next stage
                self._advance_to_next_stage()

            # Check for user approval request in stage 6
            elif self.current_stage == "stage6_review" and "Approve" in content:
                return self._handle_approval_request(state, config, content)

        return {}

    def _detect_current_stage(self, messages: list, configurable: Dict) -> str:
        """Detect current stage from message history."""
        # Check for explicit stage markers in recent messages
        for msg in reversed(messages[-10:]):  # Check last 10 messages
            if hasattr(msg, 'content'):
                content = msg.content
                if "阶段 1:" in content or "Research 阶段" in content:
                    return "stage1_research"
                elif "阶段 2:" in content or "Analysis 阶段" in content:
                    return "stage2_analysis"
                elif "阶段 3:" in content or "Planning 阶段" in content:
                    return "stage3_planning"
                elif "阶段 4:" in content or "Writing 阶段" in content:
                    return "stage4_writing"
                elif "阶段 5:" in content or "Validation 阶段" in content:
                    return "stage5_validation"
                elif "阶段 6:" in content or "Review 阶段" in content:
                    return "stage6_review"
                elif "阶段 7:" in content or "Publishing 阶段" in content:
                    return "stage7_publish"

        # Check configurable for explicit stage setting
        explicit_stage = configurable.get("firespot_stage")
        if explicit_stage and explicit_stage in FIRESPOT_STAGES:
            return explicit_stage

        # Default to current stage
        return self.current_stage

    def _inject_stage_guidance(self, stage_id: str, messages: list) -> Optional[str]:
        """
        Inject stage-specific guidance to enforce workflow compliance.

        Returns guidance text that should be added to the system message
        to force the LLM to follow the current stage's requirements.
        """
        stage_guidance = {
            "stage1_research": """
**【FireSpot 4.0 强制要求 - 阶段 1: Research 热点研究】**

你现在必须执行阶段 1：热点研究。这是第一阶段，不可跳过。

**你必须：**
1. 明确输出 "## 阶段 1: 🔍 Research (热点研究)" 标记
2. 使用 web_search 工具收集最新信息（至少3个来源）
3. 使用 web_reader 或 fetch_content 工具深入阅读关键文章
4. 提供时间戳和数据来源验证
5. 总结核心发现

**输出格式要求：**
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
""",
            "stage2_analysis": """
**【FireSpot 4.0 强制要求 - 阶段 2: Analysis 深度分析】**

你现在必须执行阶段 2：深度分析。

**你必须：**
1. 明确输出 "## 阶段 2: 📊 Analysis (深度分析)" 标记
2. 基于阶段1的研究结果进行多维度分析
3. 识别数据模式、趋势和异常
4. 进行对比分析和因果分析
5. 生成关键洞察

**输出格式要求：**
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
""",
            "stage3_planning": """
**【FireSpot 4.0 强制要求 - 阶段 3: Planning 内容规划】**

你现在必须执行阶段 3：内容规划。

**你必须：**
1. 明确输出 "## 阶段 3: 📋 Planning (内容规划)" 标记
2. 设计文章结构大纲
3. 规划每个部分的字数分配
4. 确定标题、小标题和关键段落
5. 准备引用和数据支持

**输出格式要求：**
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
""",
            "stage4_writing": """
**【FireSpot 4.0 强制要求 - 阶段 4: Writing 文章撰写】**

你现在必须执行阶段 4：文章撰写。

**你必须：**
1. 明确输出 "## 阶段 4: ✍️ Writing (文章撰写)" 标记
2. 基于阶段3的大纲撰写完整文章
3. 使用 write_file 工具将文章保存到 outputs 目录
4. 确保文章包含：标题、导语、正文、结语
5. 文章字数要求：2000-3000字

**输出格式要求：**
```
## 阶段 4: ✍️ Writing (文章撰写)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 文章内容
[撰写完整的文章内容]

### 文件保存
使用 write_file 工具保存文章到 /mnt/user-data/outputs/

### 质量检查
- 字数统计：[实际字数]
- 段落数量：[段落数]
- 引用数量：[引用数]

---
```
""",
            "stage5_validation": """
**【FireSpot 4.0 强制要求 - 阶段 5: Validation 质量验证】**

你现在必须执行阶段 5：质量验证。

**你必须：**
1. 明确输出 "## 阶段 5: ✅ Validation (质量验证)" 标记
2. 使用 read_file 工具读取刚撰写的文章
3. 进行质量评分（1-100分）
4. 检查：事实准确性、引用完整性、逻辑连贯性
5. 生成验证报告

**输出格式要求：**
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
""",
            "stage6_review": """
**【FireSpot 4.0 强制要求 - 阶段 6: Review 内容审核】**

你现在必须执行阶段 6：内容审核。

**你必须：**
1. 明确输出 "## 阶段 6: 👀 Review (内容审核)" 标记
2. 最终审核文章质量
3. 确认所有数据准确、引用完整
4. 请求用户批准：使用 ask_clarification 工具请求用户确认是否满意
5. 等待用户反馈

**输出格式要求：**
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
""",
            "stage7_publish": """
**【FireSpot 4.0 强制要求 - 阶段 7: Publishing 准备发布】**

你现在必须执行阶段 7：准备发布。

**你必须：**
1. 明确输出 "## 阶段 7: 🚀 Publishing (准备发布)" 标记
2. 使用 MCP 工具生成配套图片（如果有 mcp_openai_generate_image）
3. 准备微信公众号草稿（如果有 wechat-publisher）
4. 生成发布清单
5. 完成工作流

**输出格式要求：**
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
""",
            "initial": """
**【FireSpot 4.0 强制要求 - 初始阶段】**

欢迎使用 FireSpot 4.0 内容创作系统！

**你必须严格按照以下 7 阶段工作流执行：**

1. 🔍 **Research (热点研究)** - 收集最新信息
2. 📊 **Analysis (深度分析)** - 分析数据模式
3. 📋 **Planning (内容规划)** - 设计文章结构
4. ✍️ **Writing (文章撰写)** - 撰写完整文章
5. ✅ **Validation (质量验证)** - 验证内容质量
6. 👀 **Review (内容审核)** - 请求用户批准
7. 🚀 **Publishing (准备发布)** - 准备发布材料

**重要：**
- 每个阶段必须明确输出 "## 阶段 X: [名称]" 标记
- 不可跳过任何阶段
- 必须按顺序执行

现在开始执行 **阶段 1: Research**。
""",
        }

        # Get guidance for current stage
        guidance = stage_guidance.get(stage_id, "")

        # If no messages yet, this is the first call - show initial guidance
        if not messages and stage_id == "stage1_research":
            return stage_guidance["initial"] + stage_guidance["stage1_research"]

        return guidance if guidance else None

    def _extract_stage_result(self, content: str) -> Dict[str, Any]:
        """Extract stage result from completion message."""
        result = {
            "summary": "Stage completed",
            "timestamp": datetime.now().isoformat(),
        }

        # Try to extract specific results
        if "字数" in content:
            import re
            word_match = re.search(r'(\d+)\s*字', content)
            if word_match:
                result["word_count"] = int(word_match.group(1))

        if "评分" in content or "分数" in content:
            import re
            score_match = re.search(r'(\d+)\s*分', content)
            if score_match:
                result["score"] = int(score_match.group(1))

        return result

    def _get_expected_stage_marker(self, stage_id: str) -> Optional[str]:
        """Get the expected stage marker for a given stage."""
        markers = {
            "stage1_research": "## 阶段 1:",
            "stage2_analysis": "## 阶段 2:",
            "stage3_planning": "## 阶段 3:",
            "stage4_writing": "## 阶段 4:",
            "stage5_validation": "## 阶段 5:",
            "stage6_review": "## 阶段 6:",
            "stage7_publish": "## 阶段 7:",
            "initial": None,
        }
        return markers.get(stage_id)

    def _log_stage_violation(self, expected_stage: str, expected_marker: str,
                            thread_id: str, actual_content: str) -> None:
        """Log when LLM fails to follow stage requirements."""
        logger.warning(
            f"\n{'='*60}",
            f"\n⚠️  FireSpot Stage Violation Detected",
            f"\n{'='*60}",
            f"\nExpected Stage: {expected_stage}",
            f"\nExpected Marker: {expected_marker}",
            f"\nThread ID: {thread_id}",
            f"\n{'='*60}",
            f"\n⚠️  The LLM did not output the required stage marker.",
            f"\nThis indicates the workflow is NOT being followed correctly.",
            f"\n{'='*60}",
            extra={
                "firespot_event": "stage_violation",
                "firespot_stage": expected_stage,
                "expected_marker": expected_marker,
                "thread_id": thread_id,
                "timestamp": datetime.now().isoformat(),
                "violation_severity": "high",
            }
        )

    def _advance_to_next_stage(self) -> None:
        """Advance to the next stage in the workflow."""
        stage_order = [
            "stage1_research",
            "stage2_analysis",
            "stage3_planning",
            "stage4_writing",
            "stage5_validation",
            "stage6_review",
            "stage7_publish",
        ]

        if self.current_stage in stage_order:
            current_idx = stage_order.index(self.current_stage)
            if current_idx + 1 < len(stage_order):
                self.expected_stage = stage_order[current_idx + 1]
                logger.info(
                    f"📍 FireSpot: Advancing to next stage: {self.expected_stage}",
                    extra={
                        "firespot_event": "stage_advancement",
                        "from_stage": self.current_stage,
                        "to_stage": self.expected_stage,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

    def _handle_approval_request(self, state: ThreadState,
                                 config: RunnableConfig,
                                 content: str) -> Dict[str, Any]:
        """Handle user approval request in stage 6."""
        logger.info(
            "\n" + "="*60,
            "\n📋 FireSpot User Approval Request",
            "\n" + "="*60,
            "\nArticle draft is complete and requires user approval.",
            "\nPlease review the article and provide feedback.",
            "\n" + "="*60,
            extra={
                "firespot_event": "approval_request",
                "firespot_stage": "stage6_review",
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Inject approval request into next message if possible
        # This will be handled by ClarificationMiddleware

        return {}


# ============================================================================
# Helper Functions
# ============================================================================

def create_stage_status_message(stage_id: str, progress: int,
                                 details: Optional[str] = None) -> str:
    """Create a status message for progress visualization."""
    stage_info = FIRESPOT_STAGES.get(stage_id, {"name": stage_id, "emoji": "🔄"})

    message = f"""
{stage_info['emoji']} **FireSpot 工作流进度**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**当前阶段**: {stage_info['name']}
**总进度**: {progress}%

"""

    if details:
        message += f"**详细信息**: {details}\n"

    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    return message


def get_workflow_summary(stage_results: Dict[str, Dict]) -> str:
    """Generate workflow summary with all stages."""
    summary = "\n" + "="*60 + "\n"
    summary += "📊 FireSpot 工作流执行摘要\n"
    summary += "="*60 + "\n\n"

    for stage_id, stages in FIRESPOT_STAGES.items():
        if stage_id == "initial":
            continue

        emoji = stages["emoji"]
        name = stages["name"]

        if stage_id in stage_results:
            result = stage_results[stage_id]
            summary += f"{emoji} {name}: ✅ 完成"
            if "summary" in result:
                summary += f" - {result['summary']}"
            summary += "\n"
        elif stage_id == "completed":
            summary += f"{emoji} {name}: ✅ 完成\n"
        else:
            summary += f"{emoji} {name}: ⏳ 待执行\n"

    summary += "="*60 + "\n"

    return summary


# Export
__all__ = [
    "FireSpotStageTrackingMiddleware",
    "log_stage_start",
    "log_stage_complete",
    "log_progress",
    "get_stage_progress",
    "create_stage_status_message",
    "get_workflow_summary",
    "FIRESPOT_STAGES",
]
