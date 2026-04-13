# FireSpot Skill References

本 skill 以原始 FireSpot v3.0 设计为基线，保持 7 阶段内容生产闭环：

1. 阶段0：参数收集
2. 阶段1：多平台热点研究
3. 阶段2：内容分析
4. 阶段3：内容规划 + 图片资产规划
5. 阶段4：内容创作 + 图片锚点
6. 阶段5：合规校验
7. 阶段6：人工审核
8. 阶段7：自动发布草稿

## 固定工件路径

- `/mnt/user-data/workspace/stage1_research.json`
- `/mnt/user-data/workspace/stage2_analysis.json`
- `/mnt/user-data/workspace/stage3_outline.json`
- `/mnt/user-data/outputs/stage4_draft.md`
- `/mnt/user-data/workspace/stage4_article.json`
- `/mnt/user-data/workspace/stage5_validation.json`
- `/mnt/user-data/outputs/stage6_review.html`
- `/mnt/user-data/workspace/stage6_review_summary.json`
- `/mnt/user-data/workspace/stage7_publish_assets.json`

## 全局规则

- 必须按顺序推进，禁止跳阶段。
- 每阶段必须落盘工件，不能只做口头说明。
- 阶段1、阶段4优先使用 `task` 子 Agent。
- 阶段5必须执行结构化校验。
- 阶段6展示审核 HTML 后必须停住，等待用户回复。
- 阶段7必须在用户明确 `approve` 后才允许调用发布 MCP。

## 阶段6用户命令

- `approve`
- `revise [意见]`
- `detail`
- `cancel`

## 图片链路必须保留

- 阶段3产出 `publishing_plan.cover` 与 `publishing_plan.images`
- 阶段4正文保留稳定锚点：
  - `{{IMG:cover_01}}`
  - `{{IMG:inline_01}}`
  - `{{IMG:inline_02}}`
  - `{{IMG:quote_01}}`
- 阶段7根据 `source_type` 与 `upload_policy` 准备图片并替换锚点

## 图片来源优先级

`user_provided > search > generate`
