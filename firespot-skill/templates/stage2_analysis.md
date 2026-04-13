# 阶段2：内容分析模板

先读取：
- `/mnt/user-data/workspace/stage1_research.json`

基于多平台研究结果进行深度分析，并生成：
- `/mnt/user-data/workspace/stage2_analysis.json`

建议输出结构：

```python
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
    {"point": "论据1：小标题", "evidence": "", "source_platform": "", "data_backing": ""},
    {"point": "论据2：小标题", "evidence": "", "source_platform": "", "data_backing": ""},
    {"point": "论据3：小标题", "evidence": "", "source_platform": "", "data_backing": ""}
  ],
  "tone_style": "语气风格描述（理性分析中带温度，学术但不晦涩）",
  "content_structure": [
    "开篇：场景/数据引入",
    "第一部分：论点1展开",
    "第二部分：论点2展开",
    "第三部分：论点3或实践建议",
    "结语：升华主题+行动号召"
  ],
  "target_audience": "目标受众描述",
  "value_proposition": "这篇文章给读者带来的价值",
  "seo_keywords": ["关键词1", "关键词2", "关键词3"],
  "viral_potential": "传播潜力分析"
}
```

要求：
- 核心主张必须清晰、可传播。
- 三个 supporting_points 必须都能追溯到研究数据或案例。
- 输出必须能直接供阶段3和阶段4使用。
