"""Tests for MCP client integration."""

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock, patch

from pne.mcp import (
    McpClient,
    build_mcp_tools,
    mcp_list_resources_tool,
    mcp_read_resource_tool,
)
from pne.types import ToolSpec


class TestMcpClient(TestCase):
    def test_mcp_client_stores_command(self) -> None:
        client = McpClient(["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"])
        self.assertEqual(client.command, ("npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"))

    def test_mcp_client_tools_empty_before_connect(self) -> None:
        client = McpClient(["echo"])
        self.assertEqual(client.tools, [])
        self.assertEqual(client.resources, [])


class TestMcpTools(TestCase):
    def test_mcp_list_resources_tool_schema(self) -> None:
        client = MagicMock()
        client.resources = [{"uri": "file:///tmp", "name": "tmp"}]

        tool = mcp_list_resources_tool(client)
        self.assertEqual(tool.name, "ListMcpResources")

        result = tool.handler({})
        self.assertEqual(1, len(result["resources"]))
        self.assertEqual("file:///tmp", result["resources"][0]["uri"])

    def test_mcp_read_resource_tool_schema(self) -> None:
        client = MagicMock()
        client.read_resource = MagicMock(return_value={"content": "test data"})

        tool = mcp_read_resource_tool(client)
        self.assertEqual(tool.name, "ReadMcpResource")
        self.assertIn("uri", tool.parameters["properties"])


class TestMcpImportFallback(TestCase):
    def test_mcp_client_raises_without_mcp_package(self) -> None:
        with patch.dict("sys.modules", {"mcp": None}):
            client = McpClient(["echo"])
            # connect() should raise when mcp is not available
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                with self.assertRaises(RuntimeError):
                    loop.run_until_complete(client.connect())
            finally:
                loop.close()


class TestBuildMcpTools(TestCase):
    def test_build_mcp_tools_returns_tools(self) -> None:
        client = MagicMock()
        client.tools = []
        client.resources = []

        tools = build_mcp_tools(client)
        names = [tool.name for tool in tools]
        self.assertIn("ListMcpResources", names)
        self.assertIn("ReadMcpResource", names)
