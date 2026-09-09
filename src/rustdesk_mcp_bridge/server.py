"""MCP server exposing local desktop automation tools."""

from __future__ import annotations

from fastmcp import FastMCP

from .desktop import DesktopController

mcp = FastMCP("rustdesk-mcp-bridge")
_controller: DesktopController | None = None


def _get_controller() -> DesktopController:
    """Return a lazily initialized desktop controller."""
    global _controller
    if _controller is None:
        _controller = DesktopController()
    return _controller


@mcp.tool()
def get_screen_size() -> dict[str, int]:
    """Return the current screen resolution."""
    size = _get_controller().get_screen_size()
    return {"width": size.width, "height": size.height}


@mcp.tool()
def capture_screen(
    left: int = 0,
    top: int = 0,
    width: int | None = None,
    height: int | None = None,
    format: str = "png",
    quality: int = 85,
) -> str:
    """Capture the screen and return it as a base64-encoded data URI.

    If width and height are omitted, the full primary screen is captured.
    """
    region: tuple[int, int, int, int] | None
    if width is not None and height is not None:
        region = (left, top, width, height)
    else:
        region = None
    return _get_controller().capture_screen(region=region, format=format, quality=quality)  # type: ignore[arg-type]


@mcp.tool()
def move_mouse(x: int, y: int) -> str:
    """Move the mouse cursor to absolute screen coordinates."""
    _get_controller().move_mouse(x, y)
    return f"Moved mouse to ({x}, {y})"


@mcp.tool()
def mouse_click(
    x: int | None = None,
    y: int | None = None,
    button: str = "left",
    clicks: int = 1,
    interval: float = 0.0,
) -> str:
    """Click a mouse button at optional absolute coordinates."""
    _get_controller().click(x, y, button=button, clicks=clicks, interval=interval)  # type: ignore[arg-type]
    return f"Clicked {button} button"


@mcp.tool()
def mouse_down(button: str = "left") -> str:
    """Press and hold a mouse button."""
    _get_controller().mouse_down(button=button)  # type: ignore[arg-type]
    return f"Pressed {button} mouse button"


@mcp.tool()
def mouse_up(button: str = "left") -> str:
    """Release a mouse button."""
    _get_controller().mouse_up(button=button)  # type: ignore[arg-type]
    return f"Released {button} mouse button"


@mcp.tool()
def type_text(text: str, interval: float = 0.01) -> str:
    """Type a text string on the keyboard."""
    _get_controller().type_text(text, interval=interval)
    return f"Typed {len(text)} characters"


@mcp.tool()
def send_key(key: str) -> str:
    """Press a key or key combination (e.g. 'enter', 'ctrl+a', 'ctrl+shift+t')."""
    _get_controller().send_key(key)
    return f"Sent key: {key}"


def main(transport: str = "stdio", host: str = "127.0.0.1", port: int = 8765) -> None:
    """Run the MCP server.

    Args:
        transport: ``stdio`` or ``http``.
        host: HTTP bind host.
        port: HTTP bind port.
    """
    if transport == "http":
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()
