#!/usr/bin/env python3
import re

import markdown

ROOT_SECTION_STYLE = "font-size:17px;line-height:1.8;color:#222;word-break:break-word;"
PARAGRAPH_STYLE = "margin:16px 0;font-size:17px;line-height:1.8;color:#222;text-align:justify;word-break:break-word;"
HEADING_2_STYLE = "margin:32px 0 16px;font-size:24px;line-height:1.4;font-weight:700;color:#111827;"
HEADING_3_STYLE = "margin:24px 0 12px;font-size:19px;line-height:1.5;font-weight:700;color:#1f2937;"
LIST_STYLE = "margin:16px 0;padding-left:24px;color:#222;"
LIST_ITEM_STYLE = "margin:8px 0;font-size:17px;line-height:1.8;color:#222;"
BLOCKQUOTE_STYLE = "margin:24px 0;padding:16px 18px;border-left:4px solid #3b82f6;background:#f8fafc;color:#334155;border-radius:8px;"
BLOCKQUOTE_PARAGRAPH_STYLE = "margin:10px 0;font-size:16px;line-height:1.8;color:#334155;"
HR_STYLE = "border:none;border-top:1px solid #e5e7eb;margin:32px 0;"
IMAGE_TOKEN_RE = re.compile(r"^\s*\{\{IMG:[a-zA-Z0-9_-]+\}\}\s*$")
TOP_LEVEL_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
METADATA_SPLIT_RE = re.compile(r"\n---\n", re.MULTILINE)


def split_markdown_body(markdown_body: str) -> tuple[str, str]:
    parts = METADATA_SPLIT_RE.split(markdown_body, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return markdown_body.strip(), ""


def strip_top_level_title(markdown_body: str, title: str) -> str:
    match = TOP_LEVEL_TITLE_RE.search(markdown_body)
    if not match:
        return markdown_body.strip()

    heading_text = match.group(1).strip()
    if title and heading_text != title.strip():
        return markdown_body.strip()

    start, end = match.span()
    stripped = (markdown_body[:start] + markdown_body[end:]).lstrip("\n")
    return stripped.strip()


def _style_opening_tag(html: str, tag: str, style: str) -> str:
    return re.sub(fr"<{tag}(\s+[^>]*)?>", f'<{tag} style="{style}">', html)


def _style_paragraphs(html: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if IMAGE_TOKEN_RE.fullmatch(inner):
            return f"<p>{inner}</p>"
        return f'<p style="{PARAGRAPH_STYLE}">{inner}</p>'

    return re.sub(r"<p>(.*?)</p>", replacer, html, flags=re.DOTALL)


def apply_inline_styles(html_body: str) -> str:
    html_body = _style_opening_tag(html_body, "h1", HEADING_2_STYLE)
    html_body = _style_opening_tag(html_body, "h2", HEADING_2_STYLE)
    html_body = _style_opening_tag(html_body, "h3", HEADING_3_STYLE)
    html_body = _style_opening_tag(html_body, "ul", LIST_STYLE)
    html_body = _style_opening_tag(html_body, "ol", LIST_STYLE)
    html_body = _style_opening_tag(html_body, "li", LIST_ITEM_STYLE)
    html_body = _style_opening_tag(html_body, "blockquote", BLOCKQUOTE_STYLE)
    html_body = re.sub(r"<blockquote>\s*<p style=\"([^\"]+)\">", f'<blockquote style="{BLOCKQUOTE_STYLE}"><p style="{BLOCKQUOTE_PARAGRAPH_STYLE}">', html_body)
    html_body = re.sub(r"<blockquote>\s*<p>", f'<blockquote style="{BLOCKQUOTE_STYLE}"><p style="{BLOCKQUOTE_PARAGRAPH_STYLE}">', html_body)
    html_body = re.sub(r"<blockquote style=\"([^\"]+)\">\s*<p>(.*?)</p>", lambda m: f'<blockquote style="{BLOCKQUOTE_STYLE}"><p style="{BLOCKQUOTE_PARAGRAPH_STYLE}">{m.group(2)}</p>', html_body, flags=re.DOTALL)
    html_body = re.sub(r"<blockquote style=\"([^\"]+)\">(.*?)</blockquote>", lambda m: re.sub(r"<p>(.*?)</p>", lambda pm: f'<p style="{BLOCKQUOTE_PARAGRAPH_STYLE}">{pm.group(1).strip()}</p>', f'<blockquote style="{BLOCKQUOTE_STYLE}">{m.group(2)}</blockquote>', flags=re.DOTALL), html_body, flags=re.DOTALL)
    html_body = re.sub(r"<hr\s*/?>", f'<hr style="{HR_STYLE}" />', html_body)
    html_body = _style_paragraphs(html_body)
    return html_body


def build_wechat_body_html(markdown_body: str, *, title: str, preview_mode: bool) -> str:
    del preview_mode
    article_body, _metadata = split_markdown_body(markdown_body)
    article_body = strip_top_level_title(article_body, title)
    html_body = markdown.markdown(article_body, extensions=["extra", "sane_lists"])
    html_body = apply_inline_styles(html_body)
    return f'<section style="{ROOT_SECTION_STYLE}">{html_body}</section>'
