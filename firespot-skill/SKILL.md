---
name: firespot
description: |
  微信公众号内容创作专家技能（增强版）。

  适用场景：
  - "帮我写/创作/撰写一篇公众号文章"
  - "从XX角度写/分析XX（要求写成文章）"
  - "做/创作/写公众号内容"
  - "使用FireSpot/Firespot/firespot..."

  不适用场景：
  - 纯粹的简短问答（"什么是XX？"）
  - 技术问题排查
  - 数据分析任务

  工作流程：7阶段标准化流程（研究→分析→规划→创作→校验→审核→发布）
  新特性：多平台热点研究 + 图片占位符工作流 + 自动草稿发布
  输出：800-1500字微信公众号推文 + 图片占位符 + 自动草稿发布
triggers:
  - "帮我写"
  - "写一篇"
  - "创作"
  - "撰写"
  - "做.*文章"
  - "公众号"
  - "微信公众号"
  - "推文"
  - "从.*角度.*写"
  - "从.*角度.*分析"
  - "从.*角度.*是什么"
  - "关于.*的分析"
  - "firespot"
  - "firespot-wechat"
examples:
  - "帮我写一篇关于AI的公众号文章"
  - "从伦理学角度写一篇文章：AI与人类的差异"
  - "FireSpot：创作一篇关于AI伦理的公众号内容"
  - "做微信公众号内容，从哲学角度分析AI"
---

# FireSpot — 微信公众号内容创作工作流（增强版 v3.0）

## 🎯 技能定位与激活条件

### 你是谁

你通过激活此技能，化身为**专业的微信公众号内容运营专家**。
给定选题和思考方向，你将按照**标准化7阶段工作流**完成高质量文章创作。

### 核心工作流程（v3.0 新特性）

```
阶段0：参数收集 → 阶段1：多平台热点研究 → 阶段2：内容分析
→ 阶段3：内容规划+图片规划 → 阶段4：内容创作+占位符
→ 阶段5：合规校验 → 阶段6：人工审核 → 阶段7：自动发布草稿
```

### v3.0 三大核心改进

1. **🌍 多平台热点研究**：在主流社交平台搜索相关话题讨论
   - 国内：微信公众号、小红书、抖音、B站
   - 国际：YouTube、X (Twitter)、TikTok

2. **🖼️ 图片占位符工作流**：自动规划并插入图片位置
   - 封面图占位符
   - 关键内容处配图
   - 金句处的视觉强化

3. **📱 自动草稿发布**：一键发布到微信公众号草稿箱
   - 通过wechat-publisher MCP服务
   - 自动创建草稿
   - 提醒用户最终确认

---

## 📋 阶段0：参数收集

**激活技能后的第一步：识别和收集参数**

### 步骤1：判断用户意图

**如果用户输入已经明确包含所有信息：**

- 直接提取参数，进入阶段1

**如果用户输入模糊或不完整：**

```
[FIRESPOT | 参数收集]

我检测到您可能需要创作一篇公众号文章。

请提供以下信息（如使用默认配置，回复"继续"即可）：

1. **选题词**：本次内容的主题
   当前识别：{从用户输入中提取的主题}

2. **思考方向**：你的核心观点或切入角度
   当前识别：{从用户输入中提取的角度}

3. **目标字数**：建议800-1500字
   默认：1200字

4. **品牌人设**（可选）：账号语气、目标受众
   默认：专业中带亲切，面向对科技和哲学感兴趣的读者

5. **发布平台**：默认微信公众号
   默认：微信公众号

6. **图片需求**（新增）：是否需要图片占位符
   默认：是（包含封面+3-5处内容配图）

如果以上识别正确，请回复"继续"或"开始"。
如需修改，请直接告诉我。
```

---

## 🔍 阶段1：多平台热点研究（v3.0 增强版）

**动作：使用多渠道搜索工具收集热点数据**

### 步骤1：检查可用的搜索工具

首先检查是否有MCP搜索工具可用，优先使用MCP工具，回退到内置工具：

```python
# 可用工具优先级：
# 1. MCP搜索工具（如果配置）
# 2. DeerFlow内置工具（web_search, web_fetch）
```

### 步骤2：多平台搜索策略

**国内平台搜索：**

```python
task(
    description="""
你是社交媒体热点研究专家。请完成以下多平台研究任务：

**选题：** {topic}
**思考方向：** {direction}

**搜索任务列表（按优先级）：**

**第一优先级：国内主流平台**

1. **微信公众号文章搜索**
   使用web_search工具搜索：
   - "{topic} site:mp.weixin.qq.com"
   - "{topic} 公众号 爆文"
   - "{direction} 微信文章"
   目标：找到5-10篇高阅读量的相关文章，记录核心观点和数据

2. **小红书话题搜索**
   使用web_search工具搜索：
   - "{topic} site:xiaohongshu.com"
   - "{topic} 小红书 笔记"
   - "{topic} 种草"
   目标：找到用户真实讨论和痛点

3. **B站内容搜索**
   使用web_search工具搜索：
   - "{topic} site:bilibili.com"
   - "{topic} B站 视频"
   - "{direction} B站 UP主"
   目标：找到视频标题、弹幕高频词、评论热点

4. **抖音话题搜索**
   使用web_search工具搜索：
   - "{topic} 抖音 热门"
   - "{topic} 抖音 话题"
   目标：找到短视频话题标签和讨论热度

**第二优先级：国际平台**

5. **YouTube搜索**
   使用web_search工具搜索：
   - "{topic} site:youtube.com"
   - "{topic} YouTube trending"
   - "{direction} explained"
   目标：找到国际视角和视频标题关键词

6. **X (Twitter) 搜索**
   使用web_search工具搜索：
   - "{topic} site:twitter.com OR site:x.com"
   - "{topic} Twitter thread"
   目标：找到实时讨论和观点碰撞

7. **TikTok搜索**
   使用web_search工具搜索：
   - "{topic} site:tiktok.com"
   - "{topic} TikTok trend"
   目标：找到Z世代观点和创意表达

**第三优先级：行业深度内容**

8. **行业报告和新闻**
   使用web_search工具搜索：
   - "{topic} 行业报告 2025 2026"
   - "{topic} 深度分析"
   - "{direction} 研究"
   目标：找到权威数据和专业分析

**输出要求：**

将所有搜索结果整理为JSON格式，保存到：
/mnt/user-data/workspace/stage1_research.json

JSON结构：
{
  "research_date": "当前日期YYYY-MM-DD",
  "topic": "{topic}",
  "direction": "{direction}",
  "platforms": {
    "wechat_mp": {
      "source_count": 数字,
      "top_articles": [
        {
          "title": "文章标题",
          "url": "链接",
          "key_points": ["核心观点1", "观点2"],
          "data": "支撑数据",
          "engagement": "阅读量/点赞数（如有）"
        }
      ],
      "trending_keywords": ["热词1", "热词2"],
      "content_gaps": ["未被充分讨论的角度"],
      "unique_opportunities": ["差异化机会"]
    },
    "xiaohongshu": {
      "source_count": 数字,
      "top_notes": [
        {
          "title": "笔记标题",
          "url": "链接",
          "user_pain_points": ["用户痛点"],
          "engagement": "点赞/收藏数"
        }
      ],
      "user_demands": ["用户需求总结"],
      "content_angles": ["内容角度"]
    },
    "bilibili": {
      "source_count": 数字,
      "top_videos": [
        {
          "title": "视频标题",
          "url": "链接",
          "view_count": "播放数",
          "key_moments": ["高光时刻/时间戳"],
          "danmaku_keywords": ["弹幕高频词"]
        }
      ],
      "up_opinions": ["UP主观点"],
      "audience_questions": ["观众疑问"]
    },
    "douyin": {
      "source_count": 数字,
      "trending_hashtags": ["话题标签"],
      "viral_content": ["爆款内容特征"],
      "user_comments": ["用户评论"]
    },
    "youtube": {
      "source_count": 数字,
      "top_videos": [
        {
          "title": "视频标题",
          "url": "链接",
          "views": "观看数",
          "international_angle": "国际视角"
        }
      ],
      "global_trends": ["全球趋势"]
    },
    "twitter_x": {
      "source_count": 数字,
      "top_threads": [
        {
          "author": "作者",
          "url": "链接",
          "key_arguments": ["核心论点"],
          "engagement": "互动数据"
        }
      ],
      "debate_topics": ["争议话题"]
    },
    "tiktok": {
      "source_count": 数字,
      "trending_sounds": ["热门BGM"],
      "creative_formats": ["创意形式"],
      "gen_z_perspectives": ["Z世代观点"]
    },
    "industry_reports": {
      "source_count": 数字,
      "key_reports": [
        {
          "source": "报告来源",
          "url": "链接",
          "key_data": "关键数据",
          "insights": ["洞察"]
        }
      ]
    }
  },
  "cross_platform_insights": {
    "common_themes": ["跨平台共同主题"],
    "regional_differences": ["地域差异"],
    "demographic_preferences": ["人群偏好"],
    "content_format_trends": ["内容格式趋势"]
  },
  "strategic_recommendations": {
    "content_angle": "推荐内容角度",
    "target_audience": "目标受众",
    "differentiation": "差异化策略",
    "timing": "发布时机建议"
  }
}

**重要提醒：**
- 如果某个平台搜索无结果，标注为"无相关内容"并继续
- 优先记录数据和具体案例，避免泛泛而谈
- 特别关注用户提问和争议点，这些是创作的切入点
- 记录每个平台的独特表达方式和内容偏好
"""
)
```

**完成后输出：**

```
[FIRESPOT | 阶段1完成] 多平台热点研究
✅ 研究文件：/mnt/user-data/workspace/stage1_research.json
✅ 覆盖平台：{实际搜索到的平台列表}
✅ 总数据源：{总来源数}个
✅ 核心发现：
   - 微信公众号：{X}篇文章，{主要观点}
   - 小红书：{X}篇笔记，{用户痛点}
   - B站：{X}个视频，{观众关注点}
   - 国际平台：{X}个内容，{国际视角}
✅ 跨平台洞察：{1-2个跨平台的关键发现}
✅ 差异化机会：{识别出的独特角度}
```

---

## 🧠 阶段2：内容分析

**动作：读取研究文件 + LLM推理分析**

```python
# 读取研究结果
research_data = read_file("/mnt/user-data/workspace/stage1_research.json")

# 基于多平台研究结果进行深度分析
analysis = {
  "core_thesis": "核心主张（一句话，明确、有力、有价值）",
  "unique_angle": "与主流观点的差异化（你的独特视角）",
  "platform_insights": {
    "wechat_success_patterns": "微信公众号成功模式",
    "xiaohongshu_user_needs": "小红书用户需求",
    "video_content_gold": "视频内容金矿（B站/抖音/YouTube）",
    "international_perspectives": "国际视角差异"
  },
  "supporting_points": [
    {
      "point": "论据1：小标题",
      "evidence": "支撑数据或观点（来自研究数据）",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    },
    {
      "point": "论据2：小标题",
      "evidence": "支撑数据或观点",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    },
    {
      "point": "论据3：小标题",
      "evidence": "支撑数据或观点",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    }
  ],
  "tone_style": "语气风格描述（如：理性分析中带温度，学术但不晦涩）",
  "content_structure": [
    "开篇：场景/数据引入",
    "第一部分：论点1展开",
    "第二部分：论点2展开",
    "第三部分：论点3或实践建议",
    "结语：升华主题+行动号召"
  ],
  "target_audience": "目标受众描述（基于各平台用户画像）",
  "value_proposition": "这篇文章给读者带来的价值",
  "seo_keywords": ["关键词1", "关键词2", "关键词3"],
  "viral_potential": "传播潜力分析（为什么会被转发）"
}

# 保存分析结果
write_file("/mnt/user-data/workspace/stage2_analysis.json", json.dumps(analysis, ensure_ascii=False, indent=2))
```

**完成后输出：**

```
[FIRESPOT | 阶段2完成] 内容分析
✅ 核心主张：{core_thesis}
✅ 差异化角度：{unique_angle}
✅ 三大论据：{论据1、论据2、论据3}
✅ 平台洞察：{整合各平台的关键洞察}
✅ 分析文件：/mnt/user-data/workspace/stage2_analysis.json
```

---

## 📝 阶段3：内容规划 + 图片规划（v3.0 新增）

**动作：生成文章结构框架 + 图片占位符规划**

```python
# 基于分析结果，生成详细的文章框架
outline = {
  "title_options": [
    {
      "type": "悬念体",
      "title": "备选标题1（设置悬念，引发好奇）",
      "characteristics": "引人入胜，制造疑问"
    },
    {
      "type": "数字体",
      "title": "备选标题2（数字清单，清晰明确）",
      "characteristics": "结构清晰，实用性强"
    },
    {
      "type": "共情体",
      "title": "备选标题3（情感共鸣，贴近读者）",
      "characteristics": "情感连接，引发认同"
    }
  ],
  "recommended_title": "最推荐的标题（考虑传播性和点击率）",
  "hook": "开篇钩子（50-80字）：用场景、数据或金句切入",
  "sections": [
    {
      "heading": "小标题1：{论据1的提炼}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": 300-400,
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到下一段",
      "image_placeholder": {  # 新增：图片占位符
        "position": "段落后",
        "type": "配图",
        "description": "图片内容描述（详细说明画面元素、风格、色彩）",
        "purpose": "图片目的（强化论点/提供数据/场景化）",
        "suggested_style": "建议风格（如：扁平插画/数据图表/实景照片）",
        "size": "建议尺寸（如：16:9 或 4:3）"
      }
    },
    {
      "heading": "小标题2：{论据2的提炼}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": 300-400,
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到下一段",
      "image_placeholder": {
        "position": "段落中",
        "type": "数据图表",
        "description": "图表内容描述",
        "purpose": "数据可视化",
        "suggested_style": "信息图表",
        "size": "16:9"
      }
    },
    {
      "heading": "小标题3：{论据3或实践建议}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": 300-400,
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到结语",
      "image_placeholder": {
        "position": "段落后",
        "type": "金句图",
        "description": "金句文字内容+视觉设计建议",
        "purpose": "强化记忆，便于分享",
        "suggested_style": "文字海报/极简设计",
        "size": "1:1 或 4:5"
      }
    }
  ],
  "conclusion": "结语方向（50-100字）：升华主题，给出启发性思考",
  "cta": "行动号召：引导读者互动（点赞、在看、转发、评论）",
  "estimated_word_count": "预估总字数",
  "image_plan": {  # 新增：整体图片规划
    "cover_image": {
      "description": "封面图描述（主视觉+标题文字）",
      "style": "设计风格建议",
      "colors": "主色调",
      "mood": "情感氛围",
      "size": "2.35:1 (微信封面推荐比例)"
    },
    "total_images": 4-6,  # 封面+3-5处内容图
    "image_list": [
      {
        "seq": 1,
        "location": "封面",
        "description": "...",
        "purpose": "..."
      },
      {
        "seq": 2,
        "location": "第一段后",
        "description": "...",
        "purpose": "..."
      }
    ]
  }
}

# 保存框架
write_file("/mnt/user-data/workspace/stage3_outline.json", json.dumps(outline, ensure_ascii=False, indent=2))
```

**完成后输出：**

```
[FIRESPOT | 阶段3完成] 内容规划+图片规划
✅ 文章框架：3个核心段落 + 开篇 + 结语
✅ 推荐标题：{recommended_title}
✅ 标题备选：{3个方向}
✅ 图片规划：
   - 封面图：{封面描述}
   - 配图数量：{X}张
   - 占位符位置：{具体位置}
✅ 规划文件：/mnt/user-data/workspace/stage3_outline.json
```

---

## ✍️ 阶段4：内容创作 + 图片占位符（v3.0 增强版）

**动作：使用 `task` 工具启动写作子Agent**

```python
task(
    description="""
你是专业的微信公众号撰稿人。

**任务：根据研究、分析和框架，撰写一篇高质量文章（带图片占位符）**

**参考资料（用read_file读取）：**
1. 研究文件：/mnt/user-data/workspace/stage1_research.json
2. 分析文件：/mnt/user-data/workspace/stage2_analysis.json
3. 框架文件：/mnt/user-data/workspace/stage3_outline.json

**写作要求：**

1. **字数控制：** 800-1500字
   - 开篇：100-150字
   - 主体：600-1000字（3个段落，每段200-350字）
   - 结语：100-150字

2. **禁用句式（绝对禁止）：**
   - ❌ "大家好，今天给大家分享"
   - ❌ "首先...其次...最后"
   - ❌ "相信很多小伙伴都"
   - ❌ "话不多说，直接上干货"
   - ❌ "让我们一起来看看"

3. **段落节奏：**
   - 每段3-5行，有呼吸感
   - 避免"豆腐块"式密集文字
   - 关键观点单独成段

4. **图片占位符格式（新增）：**
   在文章中插入以下格式的占位符：

```

[IMAGE_PLACEHOLDER]
position: 封面/第X段后/金句处
type: 封面图/配图/数据图/金句图
description: 详细描述图片内容、元素、风格
style: 设计风格建议（色彩、构图、情感）
size: 建议尺寸比例
purpose: 此图片的作用（吸引注意/强化论点/数据可视化/便于分享)
[/IMAGE_PLACEHOLDER]

```
**占位符插入位置：**
- 封面图：文章最前面
- 内容配图：每个主要段落后
- 金句图：重要结论或金句处
- 数据图：需要数据可视化时

5. **开篇要求：**
- 直接进入场景或数据
- 不寒暄，不废话
- 3秒内抓住读者注意力

6. **数据引用：**
- 标注来源（如：根据XX报告）
- 数据要具体（不用"很多"、"大量"）

7. **语气风格：**
- 根据{tone_style}调整
- 保持专业但不晦涩
- 有观点但不说教

**输出格式：**
保存到 /mnt/user-data/outputs/stage4_draft.md

# 推荐标题

[IMAGE_PLACEHOLDER]
position: 封面
type: 封面图
description: 根据stage3_outline.json中的封面描述
style: 设计风格
size: 2.35:1
purpose: 吸引点击，传达主题
[/IMAGE_PLACEHOLDER]

## 正文

### 开篇
{50-80字钩子}

[IMAGE_PLACEHOLDER]
position: 开篇后
type: 场景图
description: 开篇场景的视觉化
style: 写实/插画
size: 16:9
purpose: 营造氛围，引发共鸣
[/IMAGE_PLACEHOLDER]

### 小标题1
{200-350字}

[IMAGE_PLACEHOLDER]
position: 第一段后
type: 配图
description: 根据论点1的图片描述
style: ...
size: 16:9
purpose: ...
[/IMAGE_PLACEHOLDER]

### 小标题2
{200-350字}

### 小标题3
{200-350字}

[IMAGE_PLACEHOLDER]
position: 金句处
type: 金句图
description: 核心金句文字内容
style: 极简/文字海报
size: 4:5
purpose: 便于保存分享
[/IMAGE_PLACEHOLDER]

### 结语
{50-100字}

---

**封面文案：** （15字内，吸引眼球）

**SEO关键词：** [关键词1, 关键词2, 关键词3]

**预估字数：** 约{实际字数}字

**图片占位符数量：** {X}个

**重要：** 撰写完成后，检查：
1. 字数是否符合要求
2. 段落节奏是否合适
3. 禁用句式是否避免
4. 图片占位符是否完整插入
5. 占位符描述是否清晰具体
"""
)
```

**完成后输出：**

```
[FIRESPOT | 阶段4完成] 内容创作+图片占位符
✅ 文章草稿：/mnt/user-data/outputs/stage4_draft.md
✅ 实际字数：{实际字数}字
✅ 段落数：{段落数}个
✅ 图片占位符：{X}个
   - 封面图：✓
   - 内容配图：{X}张
   - 金句图：{X}张
```

---

## ✅ 阶段5：合规校验（v3.0 增强版）

**动作：在sandbox中执行Python校验脚本（含图片占位符检查）**

```python
# 在sandbox中使用bash工具执行
bash(
    command="""
python3 << 'PYTHON_SCRIPT'
import json
import re

# 读取文章草稿
with open('/mnt/user-data/outputs/stage4_draft.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 校验规则
issues = []
score = 100
warnings = []

# 提取纯正文
body = content.split('---')
main_body = max(body, key=len)
word_count = len(main_body)
full_word_count = len(content)

# 1. 字数检查
if word_count < 800:
    issues.append({"level": "error", "category": "字数不足", "msg": f"正文字数不足：{word_count}字（最低800字）", "suggestion": "建议增加论证"})
    score -= 20
elif word_count > 2000:
    warnings.append({"level": "warning", "category": "字数偏多", "msg": f"字数偏多：{word_count}字（建议≤2000字）", "suggestion": "考虑精简，突出核心观点"})
    score -= 5

# 2. 禁用句式检测
forbidden_patterns = [
    (r"大家好，今天给大家分享", "陈词滥调的开场白"),
    (r"首先.*?其次.*?最后", "机械的过渡词"),
    (r"相信很多小伙伴", "套话表达"),
    (r"话不多说，直接上干货", "网络用语"),
    (r"让我们一起来看看", "无意义的过渡"),
    (r"众所周知", "缺乏具体性"),
    (r"毋庸置疑", "缺乏论证")
]

for pattern, description in forbidden_patterns:
    if re.search(pattern, content):
        count = len(re.findall(pattern, content))
        issues.append({"level": "warning", "category": "禁用句式", "msg": f"发现{description}（出现{count}次）", "suggestion": "替换为更具体的表达"})
        score -= 5 * count

# 3. 图片占位符检查（新增）
image_placeholders = re.findall(r'\[IMAGE_PLACEHOLDER\](.*?)\[/IMAGE_PLACEHOLDER\]', content, re.DOTALL)
if len(image_placeholders) == 0:
    issues.append({"level": "warning", "category": "缺少图片规划", "msg": "未发现图片占位符", "suggestion": "建议添加封面图和至少3张内容配图"})
    score -= 10
else:
    # 检查每个占位符的完整性
    required_fields = ['position', 'type', 'description', 'purpose']
    for i, placeholder in enumerate(image_placeholders, 1):
        missing_fields = [field for field in required_fields if field not in placeholder]
        if missing_fields:
            warnings.append({"level": "info", "category": "占位符不完整", "msg": f"第{i}个占位符缺少字段：{', '.join(missing_fields)}", "suggestion": "补充完整字段信息"})

# 4. 标题长度
title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
if title_match:
    title = title_match.group(1)
    if len(title) > 64:
        issues.append({"level": "warning", "category": "标题过长", "msg": f"标题：{len(title)}字", "suggestion": "精简标题"})
        score -= 5

# 5. 段落节奏
paragraphs = [p.strip() for p in main_body.split('\n\n') if p.strip()]
long_paragraphs = [p for p in paragraphs if len(p) > 300]
if len(long_paragraphs) > 3:
    warnings.append({"level": "info", "category": "段落节奏", "msg": f"{len(long_paragraphs)}个长段落", "suggestion": "建议拆分"})

# 6. 小标题
headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

result = {
    "score": max(0, score),
    "word_count": word_count,
    "full_word_count": full_word_count,
    "paragraph_count": len(paragraphs),
    "heading_count": len(headings),
    "image_placeholder_count": len(image_placeholders),  # 新增
    "issues": issues,
    "warnings": warnings,
    "status": "pass" if score >= 80 and len([i for i in issues if i['level'] == 'error']) == 0 else "review"
}

print(f"\n=== 合规校验结果 ===")
print(f"综合评分：{result['score']}/100")
print(f"正文字数：{word_count}字 | 全文：{full_word_count}字")
print(f"段落数：{len(paragraphs)}个 | 小标题：{len(headings)}个")
print(f"图片占位符：{len(image_placeholders)}个")  # 新增
print(f"问题数：{len(issues)}个 | 警告数：{len(warnings)}个")
print(f"状态：{result['status'].upper()}")

if issues:
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. [{issue['category']}] {issue['msg']}")

if warnings:
    for i, w in enumerate(warnings, 1):
        print(f"  {i}. [{w['category']}] {w['msg']}")

if not issues and not warnings:
    print("✅ 文章符合所有规范")

with open('/mnt/user-data/workspace/stage5_validation.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

PYTHON_SCRIPT
"""
)
```

**完成后输出：**

```
[FIRESPOT | 阶段5完成] 合规校验
✅ 综合评分：{score}/100
✅ 字数：{word_count}字
✅ 图片占位符：{X}个  ← 新增
✅ 问题数：{issue_count}个
✅ 警告数：{warning_count}个
✅ 校验文件：/mnt/user-data/workspace/stage5_validation.json
```

---

## 👁️ 阶段6：人工审核

**动作：展示审核界面，等待用户指令**

### 读取文章和校验结果

```python
article = read_file("/mnt/user-data/outputs/stage4_draft.md")
validation = json.loads(read_file("/mnt/user-data/workspace/stage5_validation.json"))
outline = json.loads(read_file("/mnt/user-data/workspace/stage3_outline.json"))
```

### 展示标准化审核界面（v3.0 增强版）

```
╔══════════════════════════════════════════════════════════╗
║     FIRESPOT 内容审核台 — 微信公众号文章 v3.0            ║
╠══════════════════════════════════════════════════════════╣
║ 选题：{topic}
║ 思考方向：{direction}
╠══════════════════════════════════════════════════════════╣
║ 【文章信息】
║ 推荐标题：{recommended_title}
║ 字数：{word_count}字 | 合规评分：{score}/100
║ 图片占位符：{image_count}个  ← 新增
║ 状态：{status}
║
║ 【开篇预览】
║ {hook前100字}...
║
║ 【结构概览】
║ • {heading1}
║ • {heading2}
║ • {heading3}
║
║ 【图片规划】  ← 新增
║ • 封面图：{封面描述}
║ • 配图：{X}张（{位置描述}）
║ • 金句图：{X}张
║
║ 【合规问题】
{如果有错误：}
║ ❌ 必须修复：
{issue_list}
{如果有警告：}
║ ⚠️  建议优化：
{warning_list}
{如果无问题：}
║ ✅ 文章符合所有规范
╠══════════════════════════════════════════════════════════╣
║ 【操作选项】
║   approve          — 确认无误，发布到草稿箱  ← 更新
║   revise [意见]     — 修改后重新生成
║   detail           — 查看完整文章
║   cancel           — 取消任务（保留草稿）
╚══════════════════════════════════════════════════════════╝

请输入您的选择：
```

### 等待用户响应

**根据用户指令执行：**

**选项1：`approve`**

```
[FIRESPOT | 准备发布到草稿箱]

正在连接微信公众号发布服务...
→ 进入阶段7：自动发布草稿
```

**选项2：`revise [意见]`**

```
[FIRESPOT | 重新生成]

收到修改意见：{user_feedback}

正在重新执行阶段4（内容创作）...
加入以下修改要求：
- {user_feedback}
```

**选项3：`detail`**

```
===== 完整文章内容 =====

{article_full_content}

===== 合规校验详情 =====

{validation_details}

=====
请选择操作（approve/revise/detail/cancel）：
```

**选项4：`cancel`**

```
[FIRESPOT | 任务已取消]

任务已取消，所有草稿和中间文件已保留：
- 草稿：/mnt/user-data/outputs/stage4_draft.md
- 研究数据：/mnt/user-data/workspace/stage1_research.json
- 分析结果：/mnt/user-data/workspace/stage2_analysis.json
- 文章框架：/mnt/user-data/workspace/stage3_outline.json
- 校验报告：/mnt/user-data/workspace/stage5_validation.json

如需继续，可以告诉我：
- "继续"：使用当前草稿继续
- "重新开始"：从头开始
- "修改XX"：针对某部分修改
```

---

## 📤 阶段7：自动发布到草稿箱（v3.0 新增）

**动作：通过wechat-publisher MCP服务发布到微信公众号草稿箱**

### 步骤1：检查wechat-publisher MCP服务

```python
# 检查MCP服务是否可用
# 使用mcp工具调用wechat-publisher
```

### 步骤2：提取文章内容

```python
# 读取文章
article = read_file("/mnt/user-data/outputs/stage4_draft.md")

# 提取标题
title_match = re.search(r'^#\s+(.+)$', article, re.MULTILINE)
title = title_match.group(1) if title_match else "未命名文章"

# 提取正文（去除图片占位符用于纯文本发布）
# 但保留占位符标记供后续手动配图
body = article

# 提取SEO关键词
keywords_match = re.search(r'关键词：\s*\[(.+?)\]', article)
keywords = keywords_match.group(1) if keywords_match else ""
```

### 步骤3：调用MCP发布服务

```python
# 通过MCP工具调用wechat-publisher
# 具体调用方式取决于MCP工具的接口

# 示例流程：
# 1. 上传封面图（如果有的话）
# 2. 创建文章草稿
# 3. 提取图片占位符信息，生成配图清单
```

### 步骤4：生成配图清单

```python
# 从文章中提取所有图片占位符
import re
import json

placeholders = re.findall(r'\[IMAGE_PLACEHOLDER\](.*?)\[/IMAGE_PLACEHOLDER\]', article, re.DOTALL)

image_checklist = {
  "total_images": len(placeholders),
  "images": []
}

for i, p in enumerate(placeholders, 1):
    fields = {}
    for line in p.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()

    image_checklist["images"].append({
      "seq": i,
      "position": fields.get("position", "未知"),
      "type": fields.get("type", "未知"),
      "description": fields.get("description", ""),
      "style": fields.get("style", ""),
      "size": fields.get("size", ""),
      "purpose": fields.get("purpose", "")
    })

# 保存配图清单
write_file("/mnt/user-data/workspace/stage7_image_checklist.json", json.dumps(image_checklist, ensure_ascii=False, indent=2))
```

### 步骤5：发布完成提示

```
╔══════════════════════════════════════════════════════════╗
║         📱 FIRESPOT 发布成功                              ║
╠══════════════════════════════════════════════════════════╣
║ ✅ 文章已发布到微信公众号草稿箱                         ║
╠══════════════════════════════════════════════════════════╣
║ 【文章信息】
║ 标题：{title}
║ 字数：{word_count}字
║ 状态：草稿（等待最终确认）                               ║
║                                                           ║
║ 【下一步操作】                                            ║
║ 1. 登录微信公众号后台                                    ║
║    https://mp.weixin.qq.com                              ║
║                                                           ║
║ 2. 进入"草稿箱"                                          ║
║                                                           ║
║ 3. 找到文章《{title}》                                   ║
║                                                           ║
║ 4. 根据配图清单添加图片：                                ║
║    共需要{image_count}张图片                             ║
║    配图清单：/mnt/user-data/workspace/stage7_image_checklist.json ║
║                                                           ║
║ 5. 预览文章效果                                          ║
║                                                           ║
║ 6. 确认无误后点击"发表"                                  ║
╠══════════════════════════════════════════════════════════╣
║ 【文件清单】                                              ║
║ • 文章正文：/mnt/user-data/outputs/stage4_draft.md       ║
║ • 配图清单：/mnt/user-data/workspace/stage7_image_checklist.json ║
║ • 研究数据：/mnt/user-data/workspace/stage1_research.json ║
║ • 分析报告：/mnt/user-data/workspace/stage2_analysis.json ║
║ • 文章框架：/mnt/user-data/workspace/stage3_outline.json ║
║ • 校验报告：/mnt/user-data/workspace/stage5_validation.json ║
╚══════════════════════════════════════════════════════════╝

💡 温馨提示：
- 文章中的图片占位符已标记，请根据配图清单逐个添加
- 建议图片尺寸：封面 2.35:1，配图 16:9，金句图 4:5
- 发布前请预览手机端效果
- 确认SEO关键词已正确填写
```

---

## 🎓 使用示例（v3.0）

### 示例1：标准的完整流程

**用户输入：**

```
帮我写一篇公众号文章，从伦理学角度分析AI与人类的本质差异
```

**FireSpot响应（v3.0）：**

```
[FIRESPOT | 参数收集]

✅ 已识别您的创作意图

**参数确认：**
1. 选题词：AI与人类的本质差异 ✓
2. 思考方向：从伦理学角度分析 ✓
3. 目标字数：1200字（默认）
4. 品牌人设：专业中带亲切（默认）
5. 图片需求：包含封面+内容配图（默认）← 新增

准备开始7阶段创作流程，请回复"继续"或直接开始。
```

---

## 🔧 关键提醒（v3.0 更新）

### 每个阶段必须完成

1. ✅ **输出日志标识** - `[FIRESPOT | 阶段X完成]`
2. ✅ **保存JSON数据** - 到 `/mnt/user-data/workspace/`
3. ✅ **使用task工具** - 阶段1和阶段4
4. ✅ **使用read_file/write_file** - 阶段2、3、5、7
5. ✅ **执行Python校验** - 阶段5
6. ✅ **等待用户指令** - 阶段6
7. ✅ **发布到草稿箱** - 阶段7（新增）

### 多平台研究要求（阶段1）

**国内平台（必须尝试）：**

- ✅ 微信公众号（mp.weixin.qq.com）
- ✅ 小红书（xiaohongshu.com）
- ✅ B站（bilibili.com）
- ✅ 抖音（通过web搜索）

**国际平台（如果可行）：**

- ✅ YouTube
- ✅ X (Twitter)
- ✅ TikTok

**数据要求：**

- 每个平台至少3-5个数据源
- 记录具体数据（阅读量、点赞数等）
- 提取用户真实反馈和疑问

### 图片占位符规范（阶段3、4）

**必须包含的占位符：**

1. 封面图（2.35:1）
2. 至少3张内容配图
3. 至少1张金句图

**占位符字段：**

- position：位置
- type：类型
- description：详细描述（最重要）
- style：风格建议
- size：尺寸比例
- purpose：作用

### 自动发布流程（阶段7）

**前提条件：**

- wechat-publisher MCP服务已启用
- 用户已授权微信公众号访问

**发布内容：**

- 文章正文
- 标题
- SEO关键词
- 图片占位符（保留标记）

**不包含：**

- 实际图片文件（需手动添加）
- 最终确认（需手动发布）

---

## 📝 技能使用检查清单（v3.0）

在激活此技能前，请确认：

- [ ] 用户输入包含创作意图（"写"、"创作"、"做"等）
- [ ] 或用户明确指定平台（"公众号"、"微信公众号"）
- [ ] 或用户明确指定技能（"FireSpot"、"Firespot"）
- [ ] 或用户输入包含"从XX角度"且适合深度分析
- [ ] 主题适合写800字以上完整文章
- [ ] 不是纯粹的技术问题或简短问答
- [ ] 系统已配置至少一个搜索工具（内置或MCP）
- [ ] 如需发布到草稿箱，wechat-publisher MCP已启用

如果以上有**2项以上**符合，应该激活此技能。

---

**技能版本：** v3.0 - 多平台研究 + 图片占位符 + 自动草稿发布
**最后更新：** 2026-04-02
**适用平台：** 微信公众号（WeChat Official Account）
**新增特性：**

- 🌍 7大社交平台热点研究
- 🖼️ 图片占位符工作流
- 📱 自动发布到草稿箱
