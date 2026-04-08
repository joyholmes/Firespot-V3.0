"""
Firespot — 微信公众号 MCP 发布服务器
运行方式：python server.py
监听端口：3101
DeerFlow 通过 SSE 连接此服务，调用微信发布工具
"""

import os
import time
import json
import base64
import httpx
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Mount, Route

# ── 配置（从环境变量读取）──────────────────────────────────────
WECHAT_APPID = os.environ["WECHAT_APPID"]
WECHAT_APPSECRET = os.environ["WECHAT_APPSECRET"]
API_BASE = "https://api.weixin.qq.com/cgi-bin"

# ── Token 缓存（内存，生产环境建议用 Redis）──────────────────
_token_cache: dict = {"token": None, "expires_at": 0}


def tool_result(payload: dict) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]


async def load_image_bytes(client: httpx.AsyncClient, arguments: dict) -> tuple[bytes, str, str]:
    """加载图片字节，返回 (bytes, content_type, filename)。"""
    if arguments.get("image_url"):
        img_resp = await client.get(arguments["image_url"], follow_redirects=True)
        img_resp.raise_for_status()
        image_data = img_resp.content
        content_type = img_resp.headers.get("content-type", "image/jpeg").split(";")[0].strip()
    elif arguments.get("image_base64"):
        image_data = base64.b64decode(arguments["image_base64"])
        content_type = arguments.get("content_type", "image/jpeg")
    else:
        raise ValueError("必须提供 image_url 或 image_base64")

    ext_map = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }
    ext = ext_map.get(content_type.lower(), "jpg")
    filename = arguments.get("filename") or f"cover.{ext}"
    return image_data, content_type, filename


async def upload_permanent_material(
    client: httpx.AsyncClient, token: str, image_data: bytes, content_type: str, filename: str
) -> dict:
    """上传永久图片素材，返回可用于 draft/add 的 thumb_media_id。"""
    resp = await client.post(
        f"{API_BASE}/material/add_material",
        params={"access_token": token, "type": "image"},
        files={"media": (filename, image_data, content_type)},
    )
    data = resp.json()
    if "errcode" in data and data["errcode"] != 0:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data


async def get_access_token() -> str:
    """获取或刷新 access_token，提前 5 分钟刷新"""
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 300:
        return _token_cache["token"]

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/token", params={
            "grant_type": "client_credential",
            "appid": WECHAT_APPID,
            "secret": WECHAT_APPSECRET
        })
        data = resp.json()
        if "errcode" in data:
            raise RuntimeError(f"获取 token 失败: {data}")
        _token_cache["token"] = data["access_token"]
        _token_cache["expires_at"] = time.time() + data["expires_in"]

    return _token_cache["token"]


# ── MCP 服务器定义 ────────────────────────────────────────────
server = Server("wechat-publisher")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="mcp_wechat_upload_media",
            description="上传微信公众号封面素材（永久图片素材），返回可用于 thumb_media_id 的 media_id",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {"type": "string", "description": "图片的网络 URL（jpg/png/gif，建议≤2MB）"},
                    "image_base64": {"type": "string", "description": "图片的 Base64 编码（与 image_url 二选一）"},
                    "content_type": {"type": "string", "description": "image_base64 时可传 MIME 类型，如 image/png"},
                    "filename": {"type": "string", "description": "可选文件名，如 cover.jpg"}
                }
            }
        ),
        Tool(
            name="mcp_wechat_upload_thumb",
            description="上传微信公众号图文封面素材，返回可直接传给 draft/add 的 thumb_media_id",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {"type": "string", "description": "图片的网络 URL（jpg/png/gif，建议≤2MB）"},
                    "image_base64": {"type": "string", "description": "图片的 Base64 编码（与 image_url 二选一）"},
                    "content_type": {"type": "string", "description": "image_base64 时可传 MIME 类型，如 image/png"},
                    "filename": {"type": "string", "description": "可选文件名，如 cover.jpg"}
                }
            }
        ),
        Tool(
            name="mcp_wechat_create_draft",
            description="创建微信公众号图文草稿",
            inputSchema={
                "type": "object",
                "required": ["title", "thumb_media_id", "content"],
                "properties": {
                    "title": {"type": "string"},
                    "thumb_media_id": {"type": "string", "description": "封面图素材 ID（请优先用 mcp_wechat_upload_thumb 或 mcp_wechat_upload_media 获取）"},
                    "content": {"type": "string", "description": "HTML 格式正文"},
                    "digest": {"type": "string", "description": "摘要，≤120字"},
                    "need_open_comment": {"type": "integer", "default": 1}
                }
            }
        ),
        Tool(
            name="mcp_wechat_publish",
            description="发布或定时发布微信公众号草稿",
            inputSchema={
                "type": "object",
                "required": ["media_id"],
                "properties": {
                    "media_id": {"type": "string", "description": "草稿 media_id"},
                    "schedule_time": {"type": "integer", "description": "定时发布时间戳（Unix秒），0=立即发布", "default": 0}
                }
            }
        ),
        Tool(
            name="mcp_wechat_get_status",
            description="查询微信公众号发布状态",
            inputSchema={
                "type": "object",
                "required": ["publish_id"],
                "properties": {
                    "publish_id": {"type": "string"}
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    token = await get_access_token()

    async with httpx.AsyncClient(timeout=30.0) as client:

        if name in ("mcp_wechat_upload_media", "mcp_wechat_upload_thumb"):
            try:
                image_data, content_type, filename = await load_image_bytes(client, arguments)
                data = await upload_permanent_material(client, token, image_data, content_type, filename)
                return tool_result({
                    "ok": True,
                    "media_id": data["media_id"],
                    "thumb_media_id": data["media_id"],
                    "type": "image",
                    "source": "material/add_material",
                    "warning": "请将 thumb_media_id 传给 mcp_wechat_create_draft，不要再使用旧的临时 media/upload 返回值。"
                })
            except Exception as e:
                return tool_result({"ok": False, "error": str(e), "tool": name})

        elif name == "mcp_wechat_create_draft":
            payload = {
                "articles": [{
                    "title": arguments["title"],
                    "thumb_media_id": arguments["thumb_media_id"],
                    "content": arguments["content"],
                    "digest": arguments.get("digest", ""),
                    "need_open_comment": arguments.get("need_open_comment", 1),
                    "content_source_url": ""
                }]
            }
            resp = await client.post(
                f"{API_BASE}/draft/add",
                params={"access_token": token},
                json=payload
            )
            data = resp.json()
            if "errcode" in data and data["errcode"] != 0:
                return tool_result({
                    "ok": False,
                    "error": data,
                    "hint": "如果是 40007 invalid media_id，请改用 mcp_wechat_upload_thumb / mcp_wechat_upload_media 获取新的 thumb_media_id，再重试。"
                })
            return tool_result({"ok": True, **data})

        elif name == "mcp_wechat_publish":
            media_id = arguments["media_id"]
            schedule_time = arguments.get("schedule_time", 0)

            if schedule_time and schedule_time > 0:
                resp = await client.post(
                    f"{API_BASE}/freepublish/submit",
                    params={"access_token": token},
                    json={"media_id": media_id}
                )
            else:
                resp = await client.post(
                    f"{API_BASE}/freepublish/submit",
                    params={"access_token": token},
                    json={"media_id": media_id}
                )
            data = resp.json()
            return tool_result(data)

        elif name == "mcp_wechat_get_status":
            resp = await client.get(
                f"{API_BASE}/freepublish/get",
                params={"access_token": token, "publish_id": arguments["publish_id"]}
            )
            data = resp.json()
            return tool_result(data)

    return tool_result({"error": f"Unknown tool: {name}"})


# ── SSE 传输层（DeerFlow 兼容）────────────────────────────────
sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())
    # 必须返回 Response；否则 Starlette 在连接结束时会报 NoneType is not callable
    return Response()

app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse, methods=["GET"]),
    Mount("/messages/", app=sse.handle_post_message),
    Mount("/messages", app=sse.handle_post_message),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3101)
