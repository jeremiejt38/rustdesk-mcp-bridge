# rustdesk-mcp-bridge

MCP server that exposes local desktop automation tools: screen capture, mouse
movement/clicks, and keyboard input. Designed to be driven by an AI agent so it
can operate remote desktops (for example via RustDesk) by running this server on
the target machine.

## Requirements

- Python 3.11+
- A graphical session on the target machine (`pyautogui` needs an interactive
desktop on Windows; on Linux it needs an X11/Wayland session).

## Installation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

## Usage

Run the MCP server over stdio:

```bash
rustdesk-mcp-bridge
```

Available MCP tools:

- `get_screen_size` — current screen resolution.
- `capture_screen` — base64 PNG/JPEG screenshot of the full screen or a region.
- `move_mouse` — move the cursor to absolute coordinates.
- `mouse_click` — click at absolute coordinates or at the current position.
- `mouse_down` / `mouse_up` — press/release a mouse button (drag support).
- `type_text` — type a Unicode string.
- `send_key` — press a single key or a combination (e.g. `ctrl+a`).

## Windows / RustDesk target setup

1. Install the package on the Windows target (e.g. `nzxt`).
2. Run `rustdesk-mcp-bridge` from an **interactive** PowerShell session on the
   target desktop (not a plain SSH session), so `pyautogui` can send input.
3. Connect your MCP client to the server's stdio. If you run it over SSH, use a
   terminal multiplexer launched from the interactive desktop.

## Development

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/mypy src
```

## Security

Never commit RustDesk IDs, passwords, or credentials. This server can execute
arbitrary mouse and keyboard actions: only run it in trusted environments and
protect its MCP transport.

## License

MIT
