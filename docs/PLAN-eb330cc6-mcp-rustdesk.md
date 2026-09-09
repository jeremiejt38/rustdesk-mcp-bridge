# Plan — MCP bridge for remote desktop control

**ID:** eb330cc6  
**Goal:** Build a minimal MCP (Model Context Protocol) server that lets an AI agent capture the local screen, move/click the mouse, type text and press keys. The server is intended to run on the target machine (e.g. NZXT Windows box) and be driven by the agent over MCP stdio/SSE.

## Scope

- Deliver a `rustdesk-mcp-bridge` Python package.
- Provide a `mcp stdio` server exposing these tools:
  - `capture_screen` — PNG screenshot of the full screen or a region.
  - `get_screen_size` — current screen resolution.
  - `mouse_move` — move cursor to absolute coordinates.
  - `mouse_click` — click at absolute coordinates (left/right/middle, single/double).
  - `mouse_down` / `mouse_up` — drag support.
  - `type_text` — type a Unicode string.
  - `send_key` — press a single key or key combination (e.g. `ctrl+a`).
- Use `mss` for screen capture and `pyautogui` for mouse/keyboard automation.
- Add CLI entrypoint `rustdesk-mcp-bridge`.
- Write unit tests with mocked `mss` and `pyautogui`.
- Keep KSP compliance: tests pass, ruff/mypy clean, CHANGELOG updated, README updated.

## Non-goals

- Direct RustDesk protocol integration (RustDesk SDK is not exposed as a simple Python API). The project is named after the intended use case — remote desktop control — but the first version controls the local desktop via standard automation libraries.
- OCR / image understanding on the server side; the agent receives images and interprets them.
- Cross-OS input validation parity; Windows is the primary target.

## Architecture

```
src/rustdesk_mcp_bridge/
  __init__.py
  server.py      # FastMCP server + tool registration
  desktop.py     # abstraction around mss/pyautogui
  cli.py         # click/argparse entrypoint
```

## Steps

1. Add dependencies (`fastmcp`, `mss`, `Pillow`, `pyautogui`) and dev deps.
2. Implement `desktop.py` with a `DesktopController` class.
3. Implement `server.py` with FastMCP tools.
4. Implement `cli.py` and register the console script.
5. Write tests for each tool using monkeypatch.
6. Update README with installation, usage and constraints.
7. Validate with pytest/ruff/mypy and commit.

## Risks / Constraints

- `pyautogui` on Windows requires an interactive session; running inside a plain SSH session may not send input to the logged-in desktop. Document this clearly.
- `pyautogui` fails if no display is available (headless). Provide graceful errors.
- Do not embed RustDesk credentials, IDs or passwords in code/tests.
