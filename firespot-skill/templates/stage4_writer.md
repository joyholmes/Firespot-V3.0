# 阶段4：内容创作 + 图片锚点模板

推荐使用 `task` 启动写作子 Agent。

先读取：
- `/mnt/user-data/workspace/stage1_research.json`
- `/mnt/user-data/workspace/stage2_analysis.json`
- `/mnt/user-data/workspace/stage3_outline.json`

输出到：
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`

## 写作要求

- 字数控制：800-1500字
- 开篇：100-150字
- 主体：600-1000字
- 结语：100-150字
- 开篇直接进入场景或数据，不寒暄
- 段落要有呼吸感，避免大段密集文本
- 数据引用尽量标注来源

## 禁用句式

- 大家好，今天给大家分享
- 首先...其次...最后
- 相信很多小伙伴都
- 话不多说，直接上干货
- 让我们一起来看看

## 图片锚点规范

统一使用稳定锚点：
- `{{IMG:cover_01}}`
- `{{IMG:inline_01}}`
- `{{IMG:inline_02}}`
- `{{IMG:quote_01}}`

插入位置：
- `cover_01`：文章最前面，紧跟标题后
- `inline_01`：第一部分正文后
- `inline_02`：第二部分正文后
- `quote_01`：核心金句或结论处

## Markdown 模板

```markdown
# 推荐标题

{{IMG:cover_01}}

## 开篇
{100-150字钩子}

## 小标题1
{200-350字}

{{IMG:inline_01}}

## 小标题2
{200-350字}

{{IMG:inline_02}}

## 小标题3
{200-350字，包含核心金句或方法论}

{{IMG:quote_01}}

## 结语
{100-150字}

---

**封面文案：** （15字内）

**SEO关键词：** [关键词1, 关键词2, 关键词3]

**预估字数：** 约{实际字数}字
```

## 结构化 JSON 要求

```json
{
  "title": "推荐标题",
  "digest": "120字内摘要",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "markdown_body": "完整 markdown 正文",
  "images": [stage3_outline.json 中的 publishing_plan.cover + publishing_plan.images]
}
```

## 交付前检查

1. 字数符合要求
2. 段落节奏合适
3. 禁用句式已避免
4. 图片锚点完整插入
5. `stage4_article.json` 与 markdown 对齐
