# Install SemanticCompute MCP in Claude, Codex, Gemini, and editor agents

SemanticCompute 1.23 exposes 20 read-only MCP tools for numerical parity, divergence diagnosis, family discovery,
kernel inspection, and bounded structured-data verification. Tool calls do not modify caller data or a source
workspace. Commercial binaries perform an outbound HTTPS entitlement checkout and persist a random installation
identifier with owner-only permissions.

Obtain an active `sc_lic_…` key through a bounded trial or paid plan, then keep it out of repositories, command
arguments, screenshots, and logs. Pass it through `SEMANTICCOMPUTE_LICENCE_KEY`.

## Install and verify the binaries

```bash
curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"
```

The installer verifies release checksums before installing the parity CLI, MCP server, and Live verifier into
`~/.local/bin`. On macOS it also verifies the Developer ID signature. It prints registration commands and leaves
client configuration under your control.

## Claude Desktop

Download `semanticcompute-mcp.mcpb` from the 1.23 release and open it in Claude Desktop. The bundle declares the
licence key as a required masked setting and injects it through `SEMANTICCOMPUTE_LICENCE_KEY`.

## Claude Code

```bash
claude mcp add semanticcompute -s user \
  -e SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  -- "$HOME/.local/bin/semanticcompute-mcp"
```

For a manual project or user configuration, use an absolute command path:

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

## Codex

```bash
codex mcp add semanticcompute \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  -- "$HOME/.local/bin/semanticcompute-mcp"
codex mcp get semanticcompute
```

The equivalent manual entry is:

```toml
[mcp_servers.semanticcompute]
command = "/Users/YOU/.local/bin/semanticcompute-mcp"
env = { SEMANTICCOMPUTE_LICENCE_KEY = "sc_lic_…" }
```

## Gemini CLI

```bash
gemini mcp add semanticcompute "$HOME/.local/bin/semanticcompute-mcp" --scope user \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY"
gemini mcp list
```

## VS Code and GitHub Copilot

```bash
code --add-mcp '{"name":"semanticcompute","command":"/Users/YOU/.local/bin/semanticcompute-mcp","env":{"SEMANTICCOMPUTE_LICENCE_KEY":"sc_lic_…"}}'
```

You can instead run **MCP: Add Server** from the Command Palette and choose a local command/stdio server.

## Cursor

Add the following to `~/.cursor/mcp.json`, or use **Customize → MCPs**:

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

## Windsurf and Cascade

Add the same stdio server to `~/.codeium/windsurf/mcp_config.json`:

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

## Any stdio MCP client

Set the command to the absolute path of `semanticcompute-mcp`, pass no arguments, and provide
`SEMANTICCOMPUTE_LICENCE_KEY` through the client's secret/environment mechanism. Restart the client, call
`sc_version`, and require:

- semantic version `1.23.0`;
- a 40-character build commit rather than `unknown`;
- 188 registered families;
- 20 MCP tools.

Existing MCP sessions retain the process they already started, so verification must happen in a new session.

## Troubleshooting

- Permit outbound HTTPS from the executable or Docker container to
  `semanticcompute-trial.douglas-57d.workers.dev:443`.
- On a process-aware macOS firewall, allow the exact installed executables
  `semanticcompute-mcp`, `semanticcompute-parity`, and `semanticcompute-live`. A successful browser or `curl`
  request does not prove those named processes are allowed.
- Use an absolute command path. JSON and TOML clients do not consistently expand `~`.
- Keep the device-identity directory writable and private. Native binaries use `~/.semanticcompute`; the Docker
  image uses its declared `semanticcompute-device` volume.
- If a macOS browser download is quarantined, first verify its SHA-256 and signature, then run
  `xattr -d com.apple.quarantine ~/.local/bin/semanticcompute-mcp`.
- A missing, malformed, expired, disabled, device-limited, or exhausted entitlement fails closed before paid tool
  execution. Discovery remains available so a client can inspect the server and diagnose setup.

Support and entitlement requests: **douglas@entertrainment.co.uk**.
