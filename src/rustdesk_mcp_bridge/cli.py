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
    parser.parse_args(argv)
    server_main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
