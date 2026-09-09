# rustdesk-mcp-bridge

MCP server for RustDesk remote desktop automation (screen capture, keyboard, mouse)

## Installation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

## Usage

```python
from rustdesk_mcp_bridge import __version__

print(__version__)
```

## Development

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/mypy src
```

## License

MIT
