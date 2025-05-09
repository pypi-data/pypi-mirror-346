from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import mcp.types as types
from mcp.server.fastmcp import Context, FastMCP

from mcp_server_copilot.router import Router


async def serve(
    config: dict[str, Any] | Path,
) -> None:
    """Run the copilot MCP server.

    Args:
        config: MCP Server config for Router
    """

    @asynccontextmanager
    async def copilot_lifespan(server: FastMCP) -> AsyncIterator[dict]:
        """Lifespan context manager for the Copilot server."""
        async with Router(config) as router:
            yield {"router": router}

    server = FastMCP("mcp-copilot", lifespan=copilot_lifespan)

    @server.tool(
        name="router servers", description="Route user query to appropriate servers."
    )
    async def route_servers(
        query: str,
        top_k: int | None,
        ctx: Context,
    ) -> types.CallToolResult:
        """Route user query to appropriate servers."""
        router = ctx.request_context.lifespan_context["router"]
        servers = await router.route_servers(query, top_k or 5)

        return servers

    @server.tool(
        name="route tools", description="Route user query to appropriate tools."
    )
    async def route_tools(
        query: str,
        top_k: int | None,
        ctx: Context,
    ) -> types.CallToolResult:
        """Route user query to appropriate tools."""
        router = ctx.request_context.lifespan_context["router"]
        tools = await router.route_tools(query, top_k or 5)

        return tools

    @server.tool(
        name="execute tool",
        description="Execute the specific tool based on routed servers or tools.",
    )
    async def execute_tool(
        server_name: str,
        tool_name: str,
        params: dict[str, Any] | None,
        ctx: Context,
    ) -> types.CallToolResult:
        """Execute the specific tool based on routed servers or tools."""
        router = ctx.request_context.lifespan_context["router"]
        result = await router.call_tool(server_name, tool_name, params)

        return result

    await server.run(transport="stdio")
