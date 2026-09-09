"""Sanity tests for rustdesk-mcp-bridge."""
from rustdesk_mcp_bridge import __version__


def test_version():
    assert __version__ == "0.1.0"
