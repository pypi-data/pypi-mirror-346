import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
import dns.resolver

# DNS服务器配置
DNS_SERVER = "119.29.29.29"

def query_dns(domain: str, dns_server: str = DNS_SERVER) -> dict:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    try:
        answer = resolver.resolve(domain, 'A')
        ips = [rdata.to_text() for rdata in answer]
        return {"domain": domain, "ips": ips}
    except Exception as e:
        return {"error": f"查询失败： {e}"}
from typing import Any

def format_dns_result(data: dict[str, Any] | str) -> str:
    if isinstance(data, str):
        import json
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析结果：{e}"
    if isinstance(data, dict):
        if "error" in data:
            return f"{data['error']}"
        domain = data.get("domain", "未知")
        ips = data.get("ips", [])
        if not ips:
            return f"未查询到{domain}的 IP 地址"
        ip_list = "\n".join(f" - {ip}" for ip in ips)
        return f"域名： {domain}\n IP 地址：\n{ip_list}"
    else:
        return "数据格式错误"

async def query_ip_tool(domain: str) -> list[types.TextContent]:
    data = query_dns(domain)
    result = format_dns_result(data)
    return [types.TextContent(type="text", text=result)]

@click.command()
@click.option("--port", default=9000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("dns-query-server")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        if name != "query_ip":
            raise ValueError(f"Unknown tool: {name}")
        if "domain" not in arguments:
            raise ValueError("Missing required argument 'domain'")
        return await query_ip_tool(arguments["domain"])

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="query_ip",
                description="查询域名的A记录（IPV4地址）",
                inputSchema={
                    "type": "object",
                    "required": ["domain"],
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "要查询的域名",
                        }
                    },
                },
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0
