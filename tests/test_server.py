"""Tests for the MCP server registration."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

# pyautogui requires a display; mock it before importing the server module.
sys.modules["pyautogui"] = MagicMock()

from rustdesk_mcp_bridge.server import mcp  # noqa: E402, I001


@pytest.mark.anyio
async def test_tools_registered() -> None:
    """All expected tools should be registered on the MCP server."""
    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}
    expected = {
        "get_screen_size",
        "capture_screen",
        "describe_screen",
        "locate_element",
        "move_mouse",
        "mouse_click",
        "mouse_down",
        "mouse_up",
        "type_text",
        "send_key",
    }
    assert expected.issubset(names)


@pytest.mark.anyio
@patch("rustdesk_mcp_bridge.server._get_controller")
async def test_get_screen_size_tool(mock_get_controller: MagicMock) -> None:
    """The get_screen_size tool should return width and height."""
    from rustdesk_mcp_bridge.desktop import Size

    mock_controller = MagicMock()
    mock_controller.get_screen_size.return_value = Size(1920, 1080)
    mock_get_controller.return_value = mock_controller

    result = await mcp.call_tool("get_screen_size", {})
    assert result.structured_content == {"width": 1920, "height": 1080}
