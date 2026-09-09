# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.0 (2026-09-09)


### Features

* add describe_screen tool with local Ollama vision support ([fbccacd](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/fbccacda04963c4565ca5a58cfe0e8a227f97e75))
* add HTTP transport option for MCP server ([5973b66](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/5973b66d75eae1c9a0c5fda441f75d271ff12908))
* add locate_element tool using Ollama vision ([8fea7dd](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/8fea7ddb486e35ae35bb9708cae89841fb2da426))
* add multi-monitor support and describe_image helper ([737c8c6](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/737c8c6de18264029c2c056e8a037137952fc626))
* implement MCP server with screen capture and input automation ([a95631e](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/a95631ed43b1eccc090c6d2e6229d9d3af5b58bc))
* improve locate_element with normalized bounding box parsing ([e1c3ae3](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/e1c3ae349abeba907cd80d8e613d986616c500b0))
* support nested and keyed bounding boxes in locate_element ([02c6afd](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/02c6afddcd5c350903aa5f809abd2c9defba22a3))


### Bug Fixes

* run Ollama vision queries in a thread to avoid blocking HTTP server ([76185d7](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/76185d712e43bcc20e9d6aedef08346d676eb149))
* tolerate vision models that omit braces in coordinate responses ([a0e63d9](https://github.com/jeremiejt38/rustdesk-mcp-bridge/commit/a0e63d9159dfa5c4b74f035ba4bcdbfe26ed0216))

## [Unreleased]

### feat

- Add `list_monitors` and `capture_monitor` tools to support multi-monitor setups.
- Add `describe_image` helper for vision analysis of a provided image.
- Add `locate_element` tool to find the screen coordinates of a UI element by label using a local Ollama vision model.
- Add `describe_screen` tool that captures the screen and asks a local Ollama vision model (e.g. `llava:7b`) to describe it.
- Add HTTP transport support with `--transport`, `--host` and `--port` CLI options.
- Add MCP server with screen capture, mouse and keyboard automation tools.

## [0.1.0] - 2026-09-09

### feat

- Initial release.
