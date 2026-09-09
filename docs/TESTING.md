# Tests — rustdesk-mcp-bridge

## Commands

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/mypy src
```

## Rules

- Do not remove or weaken tests to hide a runtime failure.
- Use temporary directories and mocked RustDesk/process calls; never send real credentials or connect to a real remote desktop in tests.
- All tests must pass before committing directly to `main`.
