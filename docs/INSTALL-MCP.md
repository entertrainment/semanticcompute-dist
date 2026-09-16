# Add SemanticCompute to Claude, Codex, Gemini, Cursor, VS Code, or Windsurf

SemanticCompute ships a local stdio MCP server (`semanticcompute-mcp`) that gives compatible agents eleven
verification tools (`sc_check_parity`, `sc_validate_metal_texture`, `sc_diagnose_divergence`,
`sc_list_families`, …) plus resources and
prompts. Pick the path for your client; each takes under a minute.

> **Distribution pause:** the published v1.22.1 and earlier binaries predate online entitlement enforcement.
> New installation is paused while the signed, licence-gated 1.23 distribution is prepared. The installer exits
> before downloading or changing client configuration. Request a bounded trial or paid key at
> **douglas@entertrainment.co.uk**. The commands below apply to the gated distribution once issued.

## Claude Desktop — double-click, no JSON

The gated `semanticcompute-mcp.mcpb` asks for the issued `sc_lic_…` key as a required masked setting and passes
it only through `SEMANTICCOMPUTE_LICENCE_KEY`. Do not place the key in command arguments or a repository.

## One command (macOS / Linux)

Installs the signed, notarised server to `~/.local/bin`, verifies its release checksum, universal Developer ID
signature and MCP handshake, and registers it with Claude Code, Codex, and Gemini CLI when their CLIs are
present. Existing registrations that point at an older binary are upgraded to the stable installed path:

```bash
export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"
curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
```

## Claude Code — one line

If you have the `claude` CLI:

```bash
claude mcp add semanticcompute -s user -e SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" -- ~/.local/bin/semanticcompute-mcp
```

Or add it to a project `.mcp.json` (or `~/.claude.json`) yourself:

```json
{
  "mcpServers": {
    "semanticcompute": {
      "type": "stdio",
      "command": "/Users/YOU/.local/bin/semanticcompute-mcp",
      "env": { "SEMANTICCOMPUTE_LICENCE_KEY": "sc_lic_…" }
    }
  }
}
```

Use an **absolute** path (config files don't expand `~`). Restart Claude Code, then `/mcp` should list
`semanticcompute` with 11 tools. Call `sc_version` and require `1.22.1`, a non-`unknown` build commit, and 183
families before relying on a newly installed process; existing MCP processes retain the executable they started.

## Codex — one line

If you have the `codex` CLI:

```bash
codex mcp add semanticcompute --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" -- /Users/YOU/.local/bin/semanticcompute-mcp
```

The one-command installer runs this automatically when Codex is present. The equivalent manual entry in
`~/.codex/config.toml` is:

```toml
[mcp_servers.semanticcompute]
command = "/Users/YOU/.local/bin/semanticcompute-mcp"
env = { SEMANTICCOMPUTE_LICENCE_KEY = "sc_lic_…" }
```

Use an absolute path, restart the Codex app or CLI session, then confirm the saved registration with
`codex mcp get semanticcompute`. In a new Codex task, call `sc_version` and require `1.22.1`, build commit
`f7dcfa2cda82b81edb4474ff3d0d0b8e6defad1d`, and 183 families. This identifies the released process instead of
an older MCP process that was already running.

## Gemini CLI — one line

Gemini CLI has its own user-scope registration command:

```bash
gemini mcp add semanticcompute /Users/YOU/.local/bin/semanticcompute-mcp --scope user \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY"
```

The one-command installer runs it automatically when `gemini` is present. Restart Gemini CLI and confirm with
`gemini mcp list`.

## VS Code / GitHub Copilot — one line

Current VS Code accepts a user-profile MCP server through its CLI:

```bash
code --add-mcp '{"name":"semanticcompute","command":"/Users/YOU/.local/bin/semanticcompute-mcp","env":{"SEMANTICCOMPUTE_LICENCE_KEY":"sc_lic_…"}}'
```

If the `code` shell command is unavailable, run **MCP: Add Server** from the Command Palette, choose a local
command/stdio server, and enter the absolute binary path. VS Code asks you to review and trust a local server the
first time it starts.

## Cursor — global `mcp.json`

Open **Customize ▸ MCPs**, or add this entry to `~/.cursor/mcp.json` for all projects:

```json
{
  "mcpServers": {
    "semanticcompute": {
      "type": "stdio",
      "command": "/Users/YOU/.local/bin/semanticcompute-mcp",
      "env": { "SEMANTICCOMPUTE_LICENCE_KEY": "sc_lic_…" }
    }
  }
}
```

Restart Cursor. Cursor CLI users can then inspect the exposed schema with
`agent mcp list-tools semanticcompute`.

## Windsurf / Cascade — global `mcp_config.json`

Open **Windsurf Settings ▸ Cascade ▸ MCP Servers**, or add the same stdio entry to
`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "semanticcompute": {
      "command": "/Users/YOU/.local/bin/semanticcompute-mcp",
      "args": [],
      "env": { "SEMANTICCOMPUTE_LICENCE_KEY": "sc_lic_…" }
    }
  }
}
```

Refresh the MCP list after saving, then enable the tools you want Cascade to use.

## Any other MCP client

It's a plain stdio JSON-RPC server. Point the client at the binary as the `command`; no arguments needed:

```
command: /absolute/path/to/semanticcompute-mcp
env: SEMANTICCOMPUTE_LICENCE_KEY=sc_lic_…
```

## If it doesn't show up

- **Restart the client** — Claude and Codex load stdio MCP servers when a session starts.
- **Use an absolute path** in any JSON config; `~` and relative paths are the usual culprit.
- **macOS "cannot be opened"** — the binaries are Developer-ID-signed and notarised, so this is rare; if a
  browser download was quarantined, clear it: `xattr -d com.apple.quarantine ~/.local/bin/semanticcompute-mcp`.
- **Verify the server itself** is fine, independent of any client:
  ```bash
  echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' | ~/.local/bin/semanticcompute-mcp
  ```
  A JSON reply with `"serverInfo"` means the server is healthy and the problem is client config.

Still stuck? douglas@entertrainment.co.uk.
