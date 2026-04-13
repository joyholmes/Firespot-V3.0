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
  新特性：多平台热点研究 + 图片资产锚点工作流 + 自动草稿发布
  输出：800-1500字微信公众号推文 + 图片资产锚点 + 自动草稿发布
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

你通过激活此技能，化身为**专业的微信公众号内容运营专家**。
给定选题和思考方向，你将按照**标准化 7 阶段工作流**完成高质量文章创作、审核与草稿发布。

## Architecture

```text
firespot/
├── SKILL.md                              ← 主流程、门禁、阶段说明
├── templates/
│   ├── stage1_research.md                ← 阶段1研究模板
│   ├── stage2_analysis.md                ← 阶段2分析模板
│   ├── stage3_outline.md                 ← 阶段3规划与图片资产模板
│   └── stage4_writer.md                  ← 阶段4写作模板
├── scripts/
│   ├── stage5_validate.py                ← 阶段5结构化校验逻辑
│   ├── stage6_review.py                  ← 阶段6审核 HTML 生成逻辑
│   └── stage7_publish.py                 ← 阶段7发布逻辑模块
└── references/
    └── workflow-contract.md              ← 工件契约、门禁、图片链路约束
```

开始执行前，先读取：
1. `references/workflow-contract.md`
2. 当前阶段所需的 `templates/*` 或 `scripts/*`

## 核心工作流程

```text
阶段0：参数收集 → 阶段1：多平台热点研究 → 阶段2：内容分析
→ 阶段3：内容规划+图片资产规划 → 阶段4：内容创作+图片锚点
→ 阶段5：合规校验 → 阶段6：人工审核 → 阶段7：自动发布草稿
```

## 全局硬规则

1. 必须按 0→1→2→3→4→5→6→7 顺序推进，禁止跳阶段。
2. 每阶段必须落盘工件，不能只口头说明“完成了”。
3. 进入下一阶段前，必须先检查上一阶段工件是否存在且可读。
4. 阶段1与阶段4推荐使用 `task` 拉起子 Agent。
5. 阶段5必须执行结构化校验，不要只做口头审稿。
6. 阶段6展示审核 HTML 后必须停住，等待用户明确回复。
7. 阶段7只有在用户明确回复 `approve` 后才能执行。
8. 图片链路必须保留：阶段3产出资产规划，阶段4保留锚点，阶段7完成图片准备与锚点替换。

## 阶段0：参数收集

### 目标
识别和收集本次内容创作所需参数。

### 最少确认参数
- 选题词
- 思考方向
- 目标字数（默认 1200）
- 品牌人设（可选）
- 发布平台（默认微信公众号）
- 图片需求（默认包含封面 + 3-5 处内容配图）

### 执行规则
- 如果用户输入已明确，直接提取参数并进入阶段1。
- 如果输入模糊或不完整，先按原始 FireSpot 的参数确认格式与用户确认，再进入阶段1。
- 用户回复“继续 / 开始”或明确补充参数后再推进。

## 阶段1：多平台热点研究

### 目标
使用多渠道搜索工具收集热点数据，产出研究工件。

### 读取模板
- `templates/stage1_research.md`

### 工具要求
- 优先使用 MCP 搜索工具。
- MCP 不可用时，回退到 DeerFlow 内置搜索工具。
- 推荐使用 `task` 启动研究子 Agent。

### 输出工件
- `/mnt/user-data/workspace/stage1_research.json`

### 完成后输出

```text
[FIRESPOT | 阶段1完成] 多平台热点研究
✅ 研究文件：/mnt/user-data/workspace/stage1_research.json
✅ 覆盖平台：{实际搜索到的平台列表}
✅ 总数据源：{总来源数}个
✅ 核心发现：{1-2个关键发现}
✅ 差异化机会：{识别出的独特角度}
```

## 阶段2：内容分析

### 目标
读取阶段1研究结果，生成结构化分析。

### 读取模板
- `templates/stage2_analysis.md`

### 输入工件
- `/mnt/user-data/workspace/stage1_research.json`

### 输出工件
- `/mnt/user-data/workspace/stage2_analysis.json`

### 完成后输出

```text
[FIRESPOT | 阶段2完成] 内容分析
✅ 核心主张：{core_thesis}
✅ 差异化角度：{unique_angle}
✅ 三大论据：{论据1、论据2、论据3}
✅ 分析文件：/mnt/user-data/workspace/stage2_analysis.json
```

## 阶段3：内容规划 + 图片规划

### 目标
生成文章结构框架与可执行图片资产规划。

### 读取模板
- `templates/stage3_outline.md`

### 输入工件
- `/mnt/user-data/workspace/stage2_analysis.json`

### 输出工件
- `/mnt/user-data/workspace/stage3_outline.json`

### 关键要求
- 必须保留 `publishing_plan.cover` 与 `publishing_plan.images`
- 必须保留图片字段：`asset_id / role / insert_anchor / description / style / aspect_ratio / required / upload_policy / source_type / source_ref / prompt`

### 完成后输出

```text
[FIRESPOT | 阶段3完成] 内容规划+图片规划
✅ 推荐标题：{recommended_title}
✅ 图片资产规划：cover_01 + inline_xx + quote_01
✅ 规划文件：/mnt/user-data/workspace/stage3_outline.json
```

## 阶段4：内容创作 + 图片锚点

### 目标
根据研究、分析和框架，撰写文章并保留稳定图片锚点。

### 读取模板
- `templates/stage4_writer.md`

### 输入工件
- `/mnt/user-data/workspace/stage1_research.json`
- `/mnt/user-data/workspace/stage2_analysis.json`
- `/mnt/user-data/workspace/stage3_outline.json`

### 输出工件
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`

### 关键要求
- 推荐使用 `task` 启动写作子 Agent。
- 必须保留稳定图片锚点：`{{IMG:cover_01}}` / `{{IMG:inline_01}}` / `{{IMG:inline_02}}` / `{{IMG:quote_01}}`
- `stage4_article.json` 必须与 markdown 对齐，供阶段5、6、7使用。

### 完成后输出

```text
[FIRESPOT | 阶段4完成] 内容创作+图片锚点
✅ 文章草稿：/mnt/user-data/outputs/stage4_draft.md
✅ 发布数据：/mnt/user-data/workspace/stage4_article.json
✅ 图片锚点：cover_01 / inline_xx / quote_01
```

## 阶段5：合规校验

### 目标
执行结构化校验，并生成 `stage5_validation.json` 供阶段6使用。

### 输入工件
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`

### 输出工件
- `/mnt/user-data/workspace/stage5_validation.json`

### 执行方式
- 按 `scripts/stage5_validate.py` 的校验逻辑执行。
- 如果用户后续在阶段6选择 `revise`，阶段4重写后必须重新执行阶段5，不要复用旧校验结果。

### 完成后输出

```text
[FIRESPOT | 阶段5完成] 合规校验
✅ 综合评分：{score}/100
✅ 字数：{word_count}字
✅ 图片锚点：{image_token_count}个
✅ 图片资产：{asset_count}个
✅ 校验文件：/mnt/user-data/workspace/stage5_validation.json
```

## 阶段6：人工审核

### 目标
生成真实待发布 HTML，并在展示后停下来等待用户明确回复。

### 输入工件
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`
- `/mnt/user-data/workspace/stage5_validation.json`

### 输出工件
- `/mnt/user-data/outputs/stage6_review.html`
- `/mnt/user-data/workspace/stage6_review_summary.json`

### 执行方式
- 按 `scripts/stage6_review.py` 的逻辑生成审核 HTML。
- 阶段6必须复用 `scripts/wechat_body_formatter.py` 生成接近最终微信稿的 inline-style 正文 HTML，不能只生成依赖外层 CSS 的浏览器预览。
- 生成后必须用 `present_files(["/mnt/user-data/outputs/stage6_review.html"])` 展示。
- 展示后立即停止继续发布，等待用户命令。

### 阶段6用户命令
- `approve`
- `revise [意见]`
- `detail`
- `cancel`

### 阶段6用户响应规则
1. `approve`
   - 视为用户允许尝试进入阶段7
   - 若阶段5存在阻断性 error，仍不得进入阶段7，必须要求 `revise` 或 `cancel`
2. `revise` 或 `revise [意见]`
   - 回到阶段4重写
   - 重新执行阶段5、阶段6
3. `detail`
   - 重新展示 `/mnt/user-data/outputs/stage6_review.html`
   - 然后继续等待用户回复
4. `cancel`
   - 结束任务，保留中间文件，不进入阶段7

### 完成后输出

```text
[FIRESPOT | 阶段6完成] 已生成审核 HTML，请等待用户回复 approve / revise / detail / cancel。
```

## 阶段7：自动发布到草稿箱

### 目标
仅在阶段0~6都已经跑过，且用户在阶段6明确回复 `approve` 后，再调用 wechat-publisher MCP 创建草稿。

### 输入工件
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`
- `/mnt/user-data/workspace/stage3_outline.json`
- `/mnt/user-data/outputs/stage6_review.html`
- `/mnt/user-data/workspace/stage5_validation.json`

### 输出工件
- `/mnt/user-data/workspace/stage7_publish_assets.json`

### 执行方式
- 按 `scripts/stage7_publish.py` 中的 `publish_draft(call_tool)` 逻辑执行。
- 阶段7必须复用与阶段6相同的 `scripts/wechat_body_formatter.py` 正文渲染逻辑，不能直接发布默认 markdown 转换结果。
- 进入阶段7前，必须确认：
  - `/mnt/user-data/outputs/stage6_review.html` 已存在
  - 用户在阶段6明确回复了 `approve`
  - 阶段5不存在阻断性 error
  - `wechat-publisher` MCP 可用（必须先探活 `http://localhost:3101/sse` 或等价 MCP 连通性检查；若不可用，停止发布并明确报错）
- 发布时必须保留图片链路：
  - 根据 `source_type` 与 `upload_policy` 准备图片
  - 生成类图片的临时文件必须落到可写路径（如 `/tmp`），不要写到 `/mnt/user-data/outputs/*.png`
  - 封面图得到 `thumb_media_id`
  - 正文图片替换所有 `{{IMG:asset_id}}` 锚点
  - 再调用草稿创建 MCP

### 完成后输出

```text
[FIRESPOT | 阶段7完成] 微信草稿已创建
✅ 审核 HTML：/mnt/user-data/outputs/stage6_review.html
✅ 发布摘要：/mnt/user-data/workspace/stage7_publish_assets.json
✅ 草稿标题：{title}
✅ 草稿状态：draft
```

## 状态恢复与续跑规则

当流程被打断、续跑或用户回到已有线程时：

1. 若 `stage7_publish_assets.json` 已存在且发布成功，仅展示结果，不重复发布。
2. 若 `stage6_review.html` 已存在，则停留在阶段6，等待用户命令：`approve / revise / detail / cancel`。
3. 若存在 `stage5_validation.json`，则进入阶段6。
4. 若存在 `stage4_draft.md` 或 `stage4_article.json`，则进入阶段5。
5. 若存在 `stage3_outline.json`，则进入阶段4。
6. 若存在 `stage2_analysis.json`，则进入阶段3。
7. 若存在 `stage1_research.json`，则进入阶段2。
8. 若没有阶段工件，则从阶段0开始。
