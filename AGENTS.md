# rustdesk-mcp-bridge — Development Guidelines

- Follow `docs/PROJECT_WORKFLOW.md` for branch lifecycle, Conventional Commits, validation, releases, tags and cleanup.
- Keep `main` stable. After the documented validation succeeds, commit directly to `main`; do not create pull requests.
- Keep commits atomic and use Conventional Commits.
- Run the commands documented in `docs/TESTING.md` before each direct commit. Do not weaken tests to hide regressions.
- Keep `pyproject.toml` as the authoritative project version. Keep detailed release history in `CHANGELOG.md` and GitHub Releases.
- Never expose RustDesk credentials, remote IDs, passwords, API keys, or user secrets in the repository.

## Versioning

- `fix:` → patch (`vX.Y.Z+1`).
- `feat:` → minor (`vX.Y+1.0`).
- `!` or `BREAKING CHANGE:` → major (`vX+1.0.0`), requires explicit maintainer approval.
- Expected progression: `0.1.0 → 0.1.1 (patch) → 0.2.0 (minor) → 1.0.0 (major)`.

## Plan document naming convention

When creating a plan document (session plan, roadmap, migration plan, etc.), always include a random 8-character hexadecimal identifier in the filename, using hyphens instead of spaces. Format: `PLAN-<8-char-hex-id>-<short-title>.md`. Example: `PLAN-06a4a12b-nota.md`.
Generate the ID with `openssl rand -hex 4`.
