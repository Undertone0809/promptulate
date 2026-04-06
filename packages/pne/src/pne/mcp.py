"""MCP (Model Context Protocol) client integration for Pne."""

from __future__ import annotations

import asyncio
from typing import Any, Sequence

from .types import ToolSpec


class McpClient:
    """A lightweight MCP client wrapper.

    Uses the official `mcp` Python SDK if available, otherwise provides
    informative error messages.
    """

    def __init__(self, command: Sequence[str]) -> None:
        self.command = tuple(command)
        self._client: Any | None = None
        self._session: Any | None = None
        self._tools: list[ToolSpec] = []
        self._resources: list[dict[str, Any]] = []

    async def connect(self) -> "McpClient":
        """Connect to the MCP server and discover tools/resources."""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
        except ImportError as exc:
            raise RuntimeError(
                "The `mcp` package is required for MCP support. "
                "Install with: pip install 'pne[mcp]'"
            ) from exc

        server_params = StdioServerParameters(
            command=self.command[0],
            args=list(self.command[1:]) if len(self.command) > 1 else [],
            env=None,
        )

        self._client = stdio_client(server_params)
        read_stream, write_stream = await self._client.__aenter__()
        self._session = ClientSession(read_stream, write_stream)
        await self._session.__aenter__()
        await self._session.initialize()

        # Discover tools
        tools_response = await self._session.list_tools()
        self._tools = []
        for tool in getattr(tools_response, "tools", []):
            tool_name = tool.name
            tool_desc = tool.description or f"MCP tool: {tool_name}"
            tool_schema = tool.inputSchema or {"type": "object", "properties": {}}

            # Create an async handler that captures tool_name by value
            async def _make_handler(name: str) -> Any:
                return await self._call_tool(name, arguments)

            self._tools.append(
                ToolSpec(
                    name=f"mcp_{tool_name}",
                    description=tool_desc,
                    parameters=tool_schema,
                    handler=lambda args, _name=tool_name: self._call_tool_sync(_name, args),
                )
            )

        # Discover resources
        try:
            resources_response = await self._session.list_resources()
            self._resources = [
                {
                    "uri": getattr(r, "uri", str(r)),
                    "name": getattr(r, "name", "unknown"),
                    "mimeType": getattr(r, "mimeType", None),
                }
                for r in getattr(resources_response, "resources", [])
            ]
        except Exception:
            self._resources = []

        return self

    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self._session is not None:
            await self._session.__aexit__(None, None, None)
            self._session = None
        if self._client is not None:
            await self._client.__aexit__(None, None, None)
            self._client = None

    async def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call an MCP tool by name (async)."""
        if self._session is None:
            raise RuntimeError("MCP client not connected")
        result = await self._session.call_tool(tool_name, arguments=arguments)
        return {"result": str(result)}

    def _call_tool_sync(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call an MCP tool by name (sync wrapper for ToolSpec handlers)."""
        if self._session is None:
            raise RuntimeError("MCP client not connected")

        try:
            loop = asyncio.get_running_loop()
            # We're in an async context (agent.run_stream calls handlers via await)
            # Return a coroutine that will be awaited by the agent
            return self._call_tool(tool_name, arguments)
        except RuntimeError:
            # No event loop running, use a new one
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._call_tool(tool_name, arguments))
            finally:
                loop.close()

    async def read_resource(self, uri: str) -> dict[str, Any]:
        """Read an MCP resource by URI (async)."""
        if self._session is None:
            raise RuntimeError("MCP client not connected")
        result = await self._session.read_resource(uri)
        return {"uri": uri, "content": str(result)}

    def read_resource_sync(self, uri: str) -> dict[str, Any]:
        """Read an MCP resource by URI (sync wrapper)."""
        try:
            loop = asyncio.get_running_loop()
            # In async context, return a coroutine
            return self.read_resource(uri)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self.read_resource(uri))
            finally:
                loop.close()

    @property
    def tools(self) -> list[ToolSpec]:
        """Return the discovered MCP tools as ToolSpecs."""
        return list(self._tools)

    @property
    def resources(self) -> list[dict[str, Any]]:
        """Return the discovered MCP resources."""
        return list(self._resources)


def mcp_list_resources_tool(client: McpClient) -> ToolSpec:
    """Build a tool that lists available MCP resources."""
    return ToolSpec(
        name="ListMcpResources",
        description="List available resources from connected MCP servers.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        handler=lambda _args: {"resources": client.resources},
    )


def mcp_read_resource_tool(client: McpClient) -> ToolSpec:
    """Build a tool that reads an MCP resource."""
    return ToolSpec(
        name="ReadMcpResource",
        description="Read data from a specific MCP resource by URI.",
        parameters={
            "type": "object",
            "properties": {
                "uri": {
                    "type": "string",
                    "description": "URI of the MCP resource to read.",
                },
            },
            "required": ["uri"],
            "additionalProperties": False,
        },
        handler=lambda args: client.read_resource_sync(args["uri"]),
    )


def build_mcp_tools(client: McpClient) -> list[ToolSpec]:
    """Build all MCP-related tools for a connected client."""
    tools: list[ToolSpec] = [
        mcp_list_resources_tool(client),
        mcp_read_resource_tool(client),
    ]
    tools.extend(client.tools)
    return tools
