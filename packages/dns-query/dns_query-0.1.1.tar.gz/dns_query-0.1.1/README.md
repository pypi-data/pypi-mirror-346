# dns-query

A simple MCP server that exposes a DNS A record query tool.

## Installation

```bash
pip install dns_query
```

## Usage

Start the server using either stdio (default) or SSE transport:

```bash
# Using stdio transport (default)
dns-query

# Using SSE transport on custom port
dns-query --transport sse --port 8000
```

The server exposes a tool named `"dns-query"` that accepts one required argument:

- `domain`: The domain name to query for A records

## Usage in Claude Desktop

Add the following configuration to claude_desktop_config.json:

```json
{
  "mcpServers": {
    "dns-query": {
      "command": "dns-query",
      "args": []
    }
  }
}
```

## Dependencies

- anyio>=4.5
- click>=8.1.0
- dnspython>=2.7.0
- httpx>=0.27
- starlette>=0.46.2
- mcp

