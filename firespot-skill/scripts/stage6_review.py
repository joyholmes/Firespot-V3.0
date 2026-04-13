#!/usr/bin/env python3
import json
import re
from pathlib import Path

from wechat_body_formatter import build_wechat_body_html

DRAFT_PATH = Path("/mnt/user-data/outputs/stage4_draft.md")
ARTICLE_PATH = Path("/mnt/user-data/workspace/stage4_article.json")
VALIDATION_PATH = Path("/mnt/user-data/workspace/stage5_validation.json")
OUTLINE_PATH = Path("/mnt/user-data/workspace/stage3_outline.json")
REVIEW_HTML_PATH = Path("/mnt/user-data/outputs/stage6_review.html")
REVIEW_SUMMARY_PATH = Path("/mnt/user-data/workspace/stage6_review_summary.json")


def build_review() -> tuple[str, dict]:
    article = DRAFT_PATH.read_text(encoding="utf-8")
    article_meta = json.loads(ARTICLE_PATH.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
    json.loads(OUTLINE_PATH.read_text(encoding="utf-8"))

    markdown_body = article_meta.get("markdown_body", article)
    title = article_meta.get("title") or re.search(r"^#\s+(.+)$", article, re.MULTILINE).group(1)
    html_body = build_wechat_body_html(markdown_body, title=title, preview_mode=True)

    review_meta = {
        "title": title,
        "summary": "阶段6审核稿已生成，请先审核 HTML 再决定是否发布。",
        "score": validation.get("score"),
        "word_count": validation.get("word_count"),
        "issue_count": len(validation.get("issues", [])),
        "warning_count": len(validation.get("warnings", [])),
        "asset_count": len(article_meta.get("images", [])),
        "validation_status": validation.get("status"),
    }

    review_html = f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{title} - FireSpot 审核稿</title>
    <style>
      body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }}
      .wrap {{ max-width: 900px; margin: 0 auto; padding: 32px 20px 64px; }}
      .card {{ background: #fff; border-radius: 16px; box-shadow: 0 8px 30px rgba(15, 23, 42, 0.08); padding: 28px; margin-bottom: 24px; }}
      h1 {{ font-size: 32px; line-height: 1.25; margin: 0 0 16px; }}
      img {{ max-width: 100%; height: auto; border-radius: 8px; }}
      ul {{ padding-left: 20px; }}
      .meta {{ color: #475569; }}
      .badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; background: #e0f2fe; color: #0369a1; font-size: 13px; margin-right: 8px; }}
    </style>
  </head>
  <body>
    <div class=\"wrap\">
      <div class=\"card\">
        <div class=\"meta\"><span class=\"badge\">FireSpot Stage 6</span>待审核 HTML</div>
        <h1>{title}</h1>
        <ul>
          <li><strong>合规评分：</strong>{review_meta['score']}</li>
          <li><strong>正文字数：</strong>{review_meta['word_count']}</li>
          <li><strong>问题数：</strong>{review_meta['issue_count']}</li>
          <li><strong>警告数：</strong>{review_meta['warning_count']}</li>
          <li><strong>图片资产数：</strong>{review_meta['asset_count']}</li>
          <li><strong>校验状态：</strong>{review_meta['validation_status']}</li>
        </ul>
      </div>
      <div class=\"card content\">{html_body}</div>
    </div>
  </body>
</html>
"""
    return review_html, review_meta


def main() -> None:
    review_html, review_meta = build_review()
    REVIEW_HTML_PATH.write_text(review_html, encoding="utf-8")
    REVIEW_SUMMARY_PATH.write_text(json.dumps(review_meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
