"""Command-line entrypoint for the rustdesk-mcp-bridge server."""

from __future__ import annotations

import argparse
import sys

from .server import main as server_main


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and start the MCP server."""
    parser = argparse.ArgumentParser(
        prog="rustdesk-mcp-bridge",
        description="MCP server for local desktop automation (screen capture, mouse, keyboard).",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="MCP transport to use (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP bind host (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="HTTP bind port (default: 8765).",
    )
    args = parser.parse_args(argv)
    server_main(transport=args.transport, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
