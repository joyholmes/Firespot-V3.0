"""
FireSpot Publishing Tools Handler
=================================

Automated tools for Publishing stage:
- OpenAI-compatible image generation
- WeChat draft creation
- File operations

Author: FireSpot Team
Version: 4.1.0
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# OpenAI-Compatible Image Generation
# ============================================================================

async def generate_article_images(
    article_title: str,
    article_content: str,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Generate images for article using the OpenAI-compatible image MCP tool.

    Args:
        article_title: Article title
        article_content: Article content (markdown format)
        mcp_tools: Available MCP tools

    Returns:
        Dictionary with generated image information
    """
    logger.info(f"🎨 Generating images for article: {article_title}")

    images_generated = {
        "cover_image": None,
        "inline_images": [],
        "timestamp": datetime.now().isoformat(),
    }

    image_tool = mcp_tools.get("mcp_openai_generate_image") if mcp_tools else None
    if not image_tool:
        logger.warning("⚠️  OpenAI-compatible image MCP tool not available")
        return images_generated

    try:
        # Generate cover image
        cover_prompt = f"""
Create a professional, modern cover image for a tech article about AI.
Title: {article_title}
Style: Clean, minimalist, tech-focused
Elements: Abstract AI/technology symbols, chess/game board metaphor (optional)
Colors: Blue, purple, or dark theme
Aspect ratio: 16:9
"""

        logger.info(f"📸 Generating cover image with prompt: {cover_prompt[:100]}...")
        cover_result = await image_tool(prompt=cover_prompt, aspect_ratio="16:9")
        images_generated["cover_image"] = cover_result
        logger.info(f"✅ Cover image generated: {cover_result}")

        # Generate inline images for key sections
        key_sections = _extract_key_sections(article_content)

        for i, section in enumerate(key_sections[:3]):  # Max 3 inline images
            inline_prompt = f"""
Create a simple illustration for a tech article section.
Section: {section[:100]}
Style: Minimalist, professional diagram or icon
Aspect ratio: 4:3 or 16:9
"""

            logger.info(f"📸 Generating inline image {i+1} for section: {section[:50]}...")
            inline_result = await image_tool(prompt=inline_prompt, aspect_ratio="4:3")
            images_generated["inline_images"].append({
                "section": section,
                "image": inline_result,
            })
            logger.info(f"✅ Inline image {i+1} generated")

    except Exception as e:
        logger.error(f"❌ Error generating images: {e}")
        images_generated["error"] = str(e)

    return images_generated


def _extract_key_sections(content: str, max_sections: int = 3) -> List[str]:
    """Extract key sections from article for inline images."""
    sections = []

    # Split by headers
    lines = content.split('\n')
    current_section = []

    for line in lines:
        if line.strip().startswith('#'):
            if current_section:
                section_text = ' '.join(current_section)
                if len(section_text) > 50:  # Only substantial sections
                    sections.append(section_text)
                    if len(sections) >= max_sections:
                        break
            current_section = []
        else:
            current_section.append(line.strip())

    # Add last section
    if current_section:
        section_text = ' '.join(current_section)
        if len(section_text) > 50:
            sections.append(section_text)

    return sections


# ============================================================================
# WeChat Draft Creation
# ============================================================================

async def create_wechat_draft(
    article_title: str,
    article_content: str,
    cover_image: Optional[str] = None,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Create WeChat draft article.

    Args:
        article_title: Article title
        article_content: Article content
        cover_image: Cover image URL/path
        mcp_tools: Available MCP tools

    Returns:
        Dictionary with draft creation result
    """
    logger.info(f"📝 Creating WeChat draft: {article_title}")

    draft_result = {
        "success": False,
        "draft_id": None,
        "timestamp": datetime.now().isoformat(),
    }

    if not mcp_tools or "wechat_create_draft" not in mcp_tools:
        logger.warning("⚠️  WeChat MCP tools not available")
        draft_result["error"] = "WeChat tools not configured"
        return draft_result

    try:
        # Format content for WeChat
        wechat_content = _format_for_wechat(article_content)

        # Call WeChat create_draft tool
        result = await mcp_tools["wechat_create_draft"](
            title=article_title,
            content=wechat_content,
            cover_image=cover_image,
            author="FireSpot AI",
            digest=_generate_digest(article_content),
        )

        draft_result["success"] = True
        draft_result["draft_id"] = result.get("draft_id")
        draft_result["url"] = result.get("url")

        logger.info(f"✅ WeChat draft created: {result}")

    except Exception as e:
        logger.error(f"❌ Error creating WeChat draft: {e}")
        draft_result["error"] = str(e)

    return draft_result


def _format_for_wechat(content: str) -> str:
    """Format markdown content for WeChat."""
    # WeChat prefers specific markdown format
    # Convert headers to bold
    lines = content.split('\n')
    formatted_lines = []

    for line in lines:
        # Convert # headers to bold
        if line.strip().startswith('#'):
            level = len(line.strip().split()[0])
            text = line.strip().lstrip('#').strip()
            if level == 1:
                formatted_lines.append(f"## {text}")
            else:
                formatted_lines.append(f"### {text}")
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def _generate_digest(content: str, max_length: int = 200) -> str:
    """Generate article digest for WeChat."""
    # Get first paragraph or first 200 characters
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and len(line) > 20:
            if len(line) > max_length:
                return line[:max_length-3] + "..."
            return line

    return content[:max_length-3] + "..."


# ============================================================================
# Publishing Orchestrator
# ============================================================================

async def execute_publishing_stage(
    article_title: str,
    article_content: str,
    thread_id: str,
    output_path: str,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Execute complete Publishing stage workflow.

    Args:
        article_title: Article title
        article_content: Article content
        thread_id: Thread ID
        output_path: Output file path
        mcp_tools: Available MCP tools

    Returns:
        Dictionary with publishing results
    """
    logger.info("🚀 Starting FireSpot Publishing Stage")
    logger.info("="*60)

    results = {
        "stage": "stage7_publish",
        "started_at": datetime.now().isoformat(),
        "images": {},
        "wechat_draft": {},
        "file_output": {},
    }

    # Step 1: Generate images
    logger.info("📸 Step 1/3: Generating images...")
    results["images"] = await generate_article_images(
        article_title=article_title,
        article_content=article_content,
        thread_id=thread_id,
        mcp_tools=mcp_tools,
    )

    # Step 2: Create WeChat draft
    logger.info("📝 Step 2/3: Creating WeChat draft...")
    cover_image = results["images"].get("cover_image")
    results["wechat_draft"] = await create_wechat_draft(
        article_title=article_title,
        article_content=article_content,
        cover_image=cover_image,
        mcp_tools=mcp_tools,
    )

    # Step 3: Final file output
    logger.info("💾 Step 3/3: Writing final output...")
    results["file_output"] = await write_final_article(
        article_title=article_title,
        article_content=article_content,
        images=results["images"],
        output_path=output_path,
    )

    results["completed_at"] = datetime.now().isoformat()
    results["success"] = (
        results["file_output"].get("success") and
        not results["images"].get("error")
    )

    logger.info("="*60)
    logger.info(f"✅ Publishing Stage Complete: {results.get('success', False)}")

    return results


async def write_final_article(
    article_title: str,
    article_content: str,
    images: Dict[str, Any],
    output_path: str,
) -> Dict[str, Any]:
    """Write final article with image references."""
    try:
        # Add image references to content
        final_content = article_content

        if images.get("cover_image"):
            final_content = f"\n![封面图]({images['cover_image']})\n\n" + final_content

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {article_title}\n\n")
            f.write(final_content)

        return {
            "success": True,
            "path": output_path,
            "size": len(final_content),
        }

    except Exception as e:
        logger.error(f"❌ Error writing final article: {e}")
        return {
            "success": False,
            "error": str(e),
        }


# Export
__all__ = [
    "generate_article_images",
    "create_wechat_draft",
    "execute_publishing_stage",
]
