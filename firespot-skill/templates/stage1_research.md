# 阶段1：多平台热点研究模板

你是社交媒体热点研究专家。请完成以下多平台研究任务：

**选题：** {topic}
**思考方向：** {direction}

## 工具使用要求

- 优先使用 MCP 搜索工具。
- 若 MCP 搜索不可用，回退到 DeerFlow 内置搜索工具（如 `web_search`, `web_fetch`）。
- 推荐使用 `task` 启动研究子 Agent。

## 搜索范围

### 第一优先级：国内主流平台
1. 微信公众号
   - `{topic} site:mp.weixin.qq.com`
   - `{topic} 公众号 爆文`
   - `{direction} 微信文章`
2. 小红书
   - `{topic} site:xiaohongshu.com`
   - `{topic} 小红书 笔记`
   - `{topic} 种草`
3. B站
   - `{topic} site:bilibili.com`
   - `{topic} B站 视频`
   - `{direction} B站 UP主`
4. 抖音
   - `{topic} 抖音 热门`
   - `{topic} 抖音 话题`

### 第二优先级：国际平台
5. YouTube
   - `{topic} site:youtube.com`
   - `{topic} YouTube trending`
   - `{direction} explained`
6. X (Twitter)
   - `{topic} site:twitter.com OR site:x.com`
   - `{topic} Twitter thread`
7. TikTok
   - `{topic} site:tiktok.com`
   - `{topic} TikTok trend`

### 第三优先级：行业深度内容
8. 行业报告和新闻
   - `{topic} 行业报告 2025 2026`
   - `{topic} 深度分析`
   - `{direction} 研究`

## 输出要求

将所有搜索结果整理为 JSON，保存到：
`/mnt/user-data/workspace/stage1_research.json`

JSON 至少包含：

```json
{
  "research_date": "YYYY-MM-DD",
  "topic": "{topic}",
  "direction": "{direction}",
  "platforms": {
    "wechat_mp": {"source_count": 0, "top_articles": [], "trending_keywords": [], "content_gaps": [], "unique_opportunities": []},
    "xiaohongshu": {"source_count": 0, "top_notes": [], "user_demands": [], "content_angles": []},
    "bilibili": {"source_count": 0, "top_videos": [], "up_opinions": [], "audience_questions": []},
    "douyin": {"source_count": 0, "trending_hashtags": [], "viral_content": [], "user_comments": []},
    "youtube": {"source_count": 0, "top_videos": [], "global_trends": []},
    "twitter_x": {"source_count": 0, "top_threads": [], "debate_topics": []},
    "tiktok": {"source_count": 0, "trending_sounds": [], "creative_formats": [], "gen_z_perspectives": []},
    "industry_reports": {"source_count": 0, "key_reports": []}
  },
  "cross_platform_insights": {
    "common_themes": [],
    "regional_differences": [],
    "demographic_preferences": [],
    "content_format_trends": []
  },
  "strategic_recommendations": {
    "content_angle": "",
    "target_audience": "",
    "differentiation": "",
    "timing": ""
  }
}
```

## 研究要求

- 如果某个平台搜索无结果，标注为“无相关内容”并继续。
- 优先记录具体数据和案例，避免泛泛而谈。
- 特别关注用户提问、争议点和高互动内容。
- 记录各平台独特表达方式和内容偏好。
