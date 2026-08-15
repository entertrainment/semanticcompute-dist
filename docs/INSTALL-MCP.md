# Add SemanticCompute to your assistant (MCP)

SemanticCompute ships an MCP server (`semanticcompute-mcp`) that gives Claude — and any MCP client — nine
verification tools (`sc_check_parity`, `sc_diagnose_divergence`, `sc_list_families`, …) plus resources and
prompts. Pick the path for your client; all three take under a minute.

## Claude Desktop — double-click, no JSON

Download **`semanticcompute-mcp.mcpb`** from the [Releases](../../releases) page and double-click it. Claude
Desktop installs it under Settings ▸ Extensions. That's it. (`.mcpb` is Anthropic's Desktop-extension bundle —
one file, no config.)

## One command (macOS / Linux)

Installs the signed, notarised server to `~/.local/bin`, verifies it, and registers it with Claude Code if the
`claude` CLI is present:

```bash
curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
```

## Claude Code — one line

If you have the `claude` CLI:

```bash
claude mcp add semanticcompute -s user -- ~/.local/bin/semanticcompute-mcp
```

Or add it to a project `.mcp.json` (or `~/.claude.json`) yourself:

```json
{
  "mcpServers": {
    "semanticcompute": { "type": "stdio", "command": "~/.local/bin/semanticcompute-mcp" }
  }
}
```

Use an **absolute** path (config files don't expand `~`). Restart Claude Code, then `/mcp` should list
`semanticcompute` with 9 tools.

## Any other MCP client (Cursor, Windsurf, …)

It's a plain stdio JSON-RPC server. Point the client at the binary as the `command`; no arguments needed:

```
command: /absolute/path/to/semanticcompute-mcp
```

## If it doesn't show up

- **Restart the client** — MCP servers load at startup, not live.
- **Use an absolute path** in any JSON config; `~` and relative paths are the usual culprit.
- **macOS "cannot be opened"** — the binaries are Developer-ID-signed and notarised, so this is rare; if a
  browser download was quarantined, clear it: `xattr -d com.apple.quarantine ~/.local/bin/semanticcompute-mcp`.
- **Verify the server itself** is fine, independent of any client:
  ```bash
  echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' | ~/.local/bin/semanticcompute-mcp
  ```
  A JSON reply with `"serverInfo"` means the server is healthy and the problem is client config.

Still stuck? douglas@entertrainment.co.uk.
