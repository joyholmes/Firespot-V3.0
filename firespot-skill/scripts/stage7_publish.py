#!/usr/bin/env python3
import json
import re
from pathlib import Path
from typing import Any, Callable

from wechat_body_formatter import build_wechat_body_html

ARTICLE_MARKDOWN_PATH = Path("/mnt/user-data/outputs/stage4_draft.md")
ARTICLE_META_PATH = Path("/mnt/user-data/workspace/stage4_article.json")
OUTLINE_PATH = Path("/mnt/user-data/workspace/stage3_outline.json")
REVIEW_HTML_PATH = Path("/mnt/user-data/outputs/stage6_review.html")
VALIDATION_PATH = Path("/mnt/user-data/workspace/stage5_validation.json")
OUTPUT_PATH = Path("/mnt/user-data/workspace/stage7_publish_assets.json")

MCPCaller = Callable[[str, str, dict[str, Any]], dict[str, Any]]


def extract_review_body(review_html: str) -> str:
    match = re.search(r'<div class="card content">([\s\S]+)</div>\s*</div>\s*</body>', review_html)
    if not match:
        raise ValueError("stage6_review.html 结构异常，不能进入发布")
    return match.group(1)


def validation_has_blocking_error(validation: dict[str, Any]) -> bool:
    return any(issue.get("level") == "error" for issue in validation.get("issues", []))


def load_publish_inputs() -> dict[str, Any]:
    article = ARTICLE_MARKDOWN_PATH.read_text(encoding="utf-8")
    article_meta = json.loads(ARTICLE_META_PATH.read_text(encoding="utf-8"))
    json.loads(OUTLINE_PATH.read_text(encoding="utf-8"))
    review_html = REVIEW_HTML_PATH.read_text(encoding="utf-8")
    validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))

    if validation_has_blocking_error(validation):
        raise ValueError("阶段5存在阻断性 error，不能进入发布")

    title_match = re.search(r"^#\s+(.+)$", article, re.MULTILINE)
    title = article_meta.get("title") or (title_match.group(1) if title_match else "")
    if not title:
        raise ValueError("无法解析文章标题，不能进入发布")

    markdown_body = article_meta.get("markdown_body", article)
    rendered_body = build_wechat_body_html(markdown_body, title=title, preview_mode=False)
    review_body = extract_review_body(review_html)

    return {
        "article": article,
        "article_meta": article_meta,
        "review_html": review_html,
        "validation": validation,
        "html_body": review_body or rendered_body,
        "rendered_body": rendered_body,
        "title": title,
        "digest": article_meta.get("digest", ""),
        "keywords": article_meta.get("keywords", []),
        "images": article_meta.get("images", []),
    }


def build_prepare_image_params(image: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    source_type = image.get("source_type", "generate")
    upload_policy = image.get("upload_policy")
    usage = "thumb" if upload_policy == "thumb" else "article"
    params: dict[str, Any] = {
        "source_type": source_type,
        "usage": usage,
        "filename": f"{image['asset_id']}.png",
    }

    if source_type == "generate":
        params.update({
            "prompt": image["prompt"],
            "aspect_ratio": image.get("aspect_ratio", "16:9"),
            "output_path": f"/tmp/firespot_{image['asset_id']}.png",
        })
    elif source_type == "search":
        image_url = image.get("image_url") or image.get("source_ref")
        if not image_url:
            raise ValueError(f"search 图片缺少 image_url/source_ref: {image['asset_id']}")
        params["image_url"] = image_url
    elif source_type == "user_provided":
        image_url = image.get("image_url")
        image_base64 = image.get("image_base64")
        source_ref = image.get("source_ref")
        if image_url:
            params["image_url"] = image_url
        elif image_base64:
            params["image_base64"] = image_base64
            params["content_type"] = image.get("content_type", "image/png")
        elif source_ref:
            if isinstance(source_ref, str) and source_ref.startswith(("http://", "https://")):
                params["image_url"] = source_ref
            else:
                params["image_base64"] = source_ref
                params["content_type"] = image.get("content_type", "image/png")
        else:
            raise ValueError(f"user_provided 图片缺少可用来源: {image['asset_id']}")
    else:
        raise ValueError(f"不支持的 source_type: {source_type}")

    return usage, params


def prepare_and_upload_assets(images: list[dict[str, Any]], call_tool: MCPCaller) -> tuple[dict[str, Any], str]:
    uploaded_assets: dict[str, Any] = {}
    thumb_media_id = ""

    for image in images:
        asset_id = image.get("asset_id")
        if not asset_id:
            raise ValueError("图片资产缺少 asset_id")

        usage, params = build_prepare_image_params(image)
        result = call_tool("wechat-publisher", "mcp_wechat_prepare_image", params)
        if not result.get("ok"):
            raise ValueError(f"图片准备失败: {asset_id} -> {result}")

        if usage == "thumb":
            thumb_media_id = result["thumb_media_id"]
            uploaded_assets[asset_id] = {
                "type": "thumb",
                "thumb_media_id": thumb_media_id,
                "source_type": image.get("source_type", "generate"),
                "file_path": result.get("file_path"),
            }
        else:
            uploaded_assets[asset_id] = {
                "type": "article_image",
                "url": result["url"],
                "source_type": image.get("source_type", "generate"),
                "origin_url": result.get("origin_url"),
                "file_path": result.get("file_path"),
            }

    if not thumb_media_id:
        raise ValueError("封面图上传失败，不能创建草稿")

    return uploaded_assets, thumb_media_id


def replace_image_tokens(html_body: str, uploaded_assets: dict[str, Any]) -> str:
    final_html = html_body
    for asset_id, asset in uploaded_assets.items():
        if asset["type"] == "thumb":
            final_html = final_html.replace(f"<p>{{{{IMG:{asset_id}}}}}</p>", "")
            final_html = final_html.replace(f"{{{{IMG:{asset_id}}}}}", "")
            continue

        image_html = (
            f'<p style="text-align:center;margin:24px 0;">'
            f'<img src="{asset["url"]}" alt="{asset_id}" '
            f'style="max-width:100%;height:auto;border-radius:8px;" />'
            f"</p>"
        )
        final_html = final_html.replace(f"<p>{{{{IMG:{asset_id}}}}}</p>", image_html)
        final_html = final_html.replace(f"{{{{IMG:{asset_id}}}}}", image_html)

    if "{{IMG:" in final_html:
        raise ValueError("仍有图片锚点未替换，不能创建草稿")

    return final_html


def publish_draft(call_tool: MCPCaller) -> dict[str, Any]:
    payload = load_publish_inputs()
    uploaded_assets, thumb_media_id = prepare_and_upload_assets(payload["images"], call_tool)
    final_html = replace_image_tokens(payload["rendered_body"], uploaded_assets)

    draft_result = call_tool(
        "wechat-publisher",
        "mcp_wechat_create_draft",
        {
            "title": payload["title"],
            "thumb_media_id": thumb_media_id,
            "content": final_html,
            "digest": payload["digest"],
            "need_open_comment": 1,
        },
    )

    summary = {
        "title": payload["title"],
        "keywords": payload["keywords"],
        "thumb_media_id": thumb_media_id,
        "review_html": str(REVIEW_HTML_PATH),
        "uploaded_assets": uploaded_assets,
        "draft_result": draft_result,
    }
    OUTPUT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    raise SystemExit(
        "该脚本保存阶段7发布逻辑，需由 skill 在运行时注入 MCP call_tool 能力后调用 publish_draft(call_tool)。"
    )


if __name__ == "__main__":
    main()
