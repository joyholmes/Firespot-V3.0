# 阶段3：内容规划 + 图片规划模板

先读取：
- `/mnt/user-data/workspace/stage2_analysis.json`

输出到：
- `/mnt/user-data/workspace/stage3_outline.json`

## 文章框架要求

至少包含：
- `title_options`
- `recommended_title`
- `hook`
- `sections`
- `conclusion`
- `cta`
- `estimated_word_count`
- `publishing_plan`

## 图片资产规划要求

必须保留以下图片资产：
- 封面图：`cover_01`
- 正文配图：至少 2 张（如 `inline_01`, `inline_02`）
- 金句图：至少 1 张（如 `quote_01`）

每个图片资产字段至少包括：
- `asset_id`
- `role`
- `insert_anchor`
- `description`
- `style`
- `aspect_ratio`
- `required`
- `upload_policy`
- `source_type`
- `source_ref`
- `prompt`

## 建议结构

```python
outline = {
  "title_options": [
    {"type": "悬念体", "title": "备选标题1", "characteristics": "引人入胜，制造疑问"},
    {"type": "数字体", "title": "备选标题2", "characteristics": "结构清晰，实用性强"},
    {"type": "共情体", "title": "备选标题3", "characteristics": "情感连接，引发认同"}
  ],
  "recommended_title": "最推荐的标题",
  "hook": "开篇钩子（50-80字）",
  "sections": [
    {"section_id": "section_1", "heading": "小标题1", "key_point": "", "word_count_target": 300-400, "content_elements": ["要点1", "要点2", "要点3"], "transition": "", "image_asset_ref": "inline_01"},
    {"section_id": "section_2", "heading": "小标题2", "key_point": "", "word_count_target": 300-400, "content_elements": ["要点1", "要点2", "要点3"], "transition": "", "image_asset_ref": "inline_02"},
    {"section_id": "section_3", "heading": "小标题3", "key_point": "", "word_count_target": 300-400, "content_elements": ["要点1", "要点2", "要点3"], "transition": "", "image_asset_ref": "quote_01"}
  ],
  "conclusion": "结语方向（50-100字）",
  "cta": "行动号召",
  "estimated_word_count": "预估总字数",
  "publishing_plan": {
    "cover": {...},
    "images": [{...}, {...}, {...}]
  }
}
```

## 图片来源策略

- `user_provided`：用户直接提供图片，优先使用
- `search`：真实世界引用图
- `generate`：抽象概念图、封面氛围图、金句图

优先级：`user_provided > search > generate`
