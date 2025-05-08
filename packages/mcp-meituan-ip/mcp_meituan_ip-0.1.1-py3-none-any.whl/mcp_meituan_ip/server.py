import asyncio
import json

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from dataclasses import dataclass, asdict
from typing import Dict, Any
import requests
from fastapi import Request,FastAPI
# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

loc_url = 'https://apimobile.meituan.com/locate/v2/ip/loc'

server = Server("mcp-meituan-ip")


@dataclass
class RGeo:
    country: str
    province: str
    adcode: str
    city: str
    district: str


@dataclass
class LocationData:
    lng: float
    fromwhere: str
    ip: str
    rgeo: RGeo
    lat: float


@dataclass
class CityDetailData:
    detail: str
    parentArea: int
    cityPinyin: str
    lng: float
    isForeign: bool
    dpCityId: int
    country: str
    isOpen: bool
    city: str
    id: int
    openCityName: str
    originCityID: int
    area: int
    areaName: str
    province: str
    district: str
    lat: float

child_app=FastAPI()
###
#根据ip获取经纬度信息
###
def get_ip_loc(ip: str) -> LocationData:
    params = {
        "rgeo": True,
        "ip": ip
    }
    response = requests.get(loc_url, params=params)

    response.raise_for_status()  # 检查请求是否成功（4xx/5xx 会抛出异常）

    data = response.json()["data"]  # 解析 JSON

    # 构建 RGeo 对象
    rgeo = RGeo(
        country=data["rgeo"]["country"],
        province=data["rgeo"]["province"],
        adcode=data["rgeo"]["adcode"],
        city=data["rgeo"]["city"],
        district=data["rgeo"]["district"],
    )

    # 构建 LocationData 对象
    location = LocationData(
        lng=data["lng"],
        fromwhere=data["fromwhere"],
        ip=data["ip"],
        rgeo=rgeo,
        lat=data["lat"],
    )

    return location

###
#根据经纬度获取位置信息
###
def get_latlng(lat: str, lng: str) -> CityDetailData:
    api_url = f'https://apimobile.meituan.com/group/v1/city/latlng/{lat},{lng}'
    params = {
        "tag": 0
    }
    response = requests.get(api_url, params=params)

    response.raise_for_status()  # 检查请求是否成功（4xx/5xx 会抛出异常）

    data = response.json()["data"]  # 解析 JSON



    # 构建 CityDetailData 对象
    location = CityDetailData(
        detail= data["detail"],
        parentArea= data["parentArea"],
        cityPinyin= data["cityPinyin"],
        lng= data["lng"],
        isForeign= data["isForeign"],
        dpCityId= data["dpCityId"],
        country= data["country"],
        isOpen= data["isOpen"],
        city= data["city"],
        id= data["id"],
        openCityName= data["openCityName"],
        originCityID= data["originCityID"],
        area= data["area"],
        areaName= data["areaName"],
        province= data["province"],
        district= data["district"],
        lat= data["lat"]
    )

    return location




@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    列出可用的 note 资源。
    每个注释都作为具有自定义 note:// URI 方案的资源公开.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    按 URI 读取特定注释的内容。
    注释名称是从 URI 主机组件中提取的.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="美团IP查询工具",
            description="使用美团暴露的接口开发的IP与位置信息转换",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "美团IP查询工具":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="使用美团暴露的接口开发的IP与位置信息转换",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                         + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-ip-loc",
            description="获取指定ip的大致位置与经纬度信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip": {"type": "string"},
                },
                "required": ["ip"],
            },
        ),
        types.Tool(
            name="get-latlng",
            description="根据经纬度获取详细位置信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "lat": {"type": "string"},
                    "lng": {"type": "string"},
                },
                "required": ["lat", "lng"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
        name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    try:
        match name:
            case 'get-ip-loc':
                ip = arguments.get("ip")
                if not ip:
                    raise ValueError("缺少ip信息")
                result = get_ip_loc(ip=ip)
                # 转换为字典后序列化
                location_dict = asdict(result)
                # Notify clients that resources have changed
                await server.request_context.session.send_resource_list_changed()
            case 'get-latlng':
                if not all(
                        k in arguments
                        for k in ["lat", "lng"]
                ):
                    raise ValueError("Missing required arguments")
                result = get_latlng(lat= arguments['lat'], lng= arguments['lng'])
                # 转换为字典后序列化
                location_dict = asdict(result)
                # Notify clients that resources have changed
                await server.request_context.session.send_resource_list_changed()
            case _:
                raise ValueError(f"Unknown tool: {name}")

        return [
            types.TextContent(type="text", text=json.dumps(location_dict, indent=2))
        ]

    except Exception as e:
        raise ValueError(f"Error processing mcp-meituan-ip query: {str(e)}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-meituan-ip",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
