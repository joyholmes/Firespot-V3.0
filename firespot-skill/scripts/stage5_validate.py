#!/usr/bin/env python3
import json
import re
from pathlib import Path

DRAFT_PATH = Path("/mnt/user-data/outputs/stage4_draft.md")
ARTICLE_PATH = Path("/mnt/user-data/workspace/stage4_article.json")
OUTPUT_PATH = Path("/mnt/user-data/workspace/stage5_validation.json")


def main() -> None:
    content = DRAFT_PATH.read_text(encoding="utf-8")
    article_meta = json.loads(ARTICLE_PATH.read_text(encoding="utf-8"))

    issues = []
    score = 100
    warnings = []

    body = content.split("---")
    main_body = max(body, key=len)
    word_count = len(main_body)
    full_word_count = len(content)

    if word_count < 800:
        issues.append({"level": "error", "category": "字数不足", "msg": f"正文字数不足：{word_count}字（最低800字）", "suggestion": "建议增加论证"})
        score -= 20
    elif word_count > 2000:
        warnings.append({"level": "warning", "category": "字数偏多", "msg": f"字数偏多：{word_count}字（建议≤2000字）", "suggestion": "考虑精简，突出核心观点"})
        score -= 5

    forbidden_patterns = [
        (r"大家好，今天给大家分享", "陈词滥调的开场白"),
        (r"首先.*?其次.*?最后", "机械的过渡词"),
        (r"相信很多小伙伴", "套话表达"),
        (r"话不多说，直接上干货", "网络用语"),
        (r"让我们一起来看看", "无意义的过渡"),
        (r"众所周知", "缺乏具体性"),
        (r"毋庸置疑", "缺乏论证"),
    ]

    for pattern, description in forbidden_patterns:
        if re.search(pattern, content):
            count = len(re.findall(pattern, content))
            issues.append({"level": "warning", "category": "禁用句式", "msg": f"发现{description}（出现{count}次）", "suggestion": "替换为更具体的表达"})
            score -= 5 * count

    image_tokens = re.findall(r"\{\{IMG:([a-zA-Z0-9_-]+)\}\}", content)
    if len(image_tokens) == 0:
        issues.append({"level": "error", "category": "缺少图片锚点", "msg": "未发现图片锚点", "suggestion": "至少插入 cover 和 2-3 个正文图片锚点"})
        score -= 15

    images = article_meta.get("images", [])
    asset_ids = [img.get("asset_id") for img in images if img.get("asset_id")]
    unique_asset_ids = set(asset_ids)
    if len(asset_ids) != len(unique_asset_ids):
        issues.append({"level": "error", "category": "资产重复", "msg": "stage4_article.json 中存在重复 asset_id", "suggestion": "确保每张图使用唯一 asset_id"})
        score -= 15

    if "cover_01" not in asset_ids:
        issues.append({"level": "error", "category": "缺少封面资产", "msg": "stage4_article.json 未包含 cover_01", "suggestion": "必须在 publishing_plan 中保留封面图资产"})
        score -= 15

    missing_tokens = [token for token in image_tokens if token not in unique_asset_ids]
    if missing_tokens:
        issues.append({"level": "error", "category": "锚点未定义", "msg": f"以下锚点未在 stage4_article.json 中声明：{', '.join(missing_tokens)}", "suggestion": "让 markdown 中的锚点与 images[] 一一对应"})
        score -= 15

    if len([token for token in image_tokens if token.startswith("inline_")]) < 2:
        warnings.append({"level": "warning", "category": "正文配图不足", "msg": "正文配图少于2张", "suggestion": "建议至少保留2-3张正文配图"})
        score -= 5

    if "quote_01" not in image_tokens:
        warnings.append({"level": "info", "category": "金句图缺失", "msg": "未发现 quote_01 锚点", "suggestion": "建议保留1张金句图强化传播"})

    paragraphs = [p.strip() for p in main_body.split("\n\n") if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p) > 300]
    if len(long_paragraphs) > 3:
        warnings.append({"level": "info", "category": "段落节奏", "msg": f"{len(long_paragraphs)}个长段落", "suggestion": "建议拆分"})

    headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match and len(title_match.group(1)) > 64:
        warnings.append({"level": "warning", "category": "标题过长", "msg": f"标题：{len(title_match.group(1))}字", "suggestion": "精简标题"})
        score -= 5

    result = {
        "score": max(0, score),
        "word_count": word_count,
        "full_word_count": full_word_count,
        "paragraph_count": len(paragraphs),
        "heading_count": len(headings),
        "image_token_count": len(image_tokens),
        "asset_count": len(images),
        "issues": issues,
        "warnings": warnings,
        "status": "pass" if score >= 80 and len([i for i in issues if i["level"] == "error"]) == 0 else "review",
    }

    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
