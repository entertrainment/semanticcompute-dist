#!/usr/bin/env bash
#
# SemanticCompute MCP server — one-command install.
#
#   curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
#
# Downloads the signed, notarised MCP server for your platform, installs it to ~/.local/bin, verifies it
# answers MCP, and registers it with Claude Code, Codex and Gemini CLI when their CLIs are present. Prints setup
# for every other client. Re-runnable. Override the install dir with SC_BINDIR=/somewhere.
#
set -euo pipefail

REPO="entertrainment/semanticcompute-dist"
BASE="https://github.com/$REPO/releases/latest/download"
BINDIR="${SC_BINDIR:-$HOME/.local/bin}"
DEST="$BINDIR/semanticcompute-mcp"

os="$(uname -s)"; arch="$(uname -m)"
case "$os" in
  Darwin) asset="semanticcompute-mcp-macos-universal.tar.gz" ;;
  Linux)
    case "$arch" in
      x86_64) asset="semanticcompute-mcp-linux-x86_64.tar.gz" ;;
      aarch64|arm64) asset="semanticcompute-mcp-linux-aarch64.tar.gz" ;;
      *) echo "SemanticCompute: unsupported Linux architecture '$arch' (x86_64 and aarch64 are published)." >&2; exit 1 ;;
    esac ;;
  *) echo "SemanticCompute: unsupported OS '$os' (macOS and Linux only)." >&2; exit 1 ;;
esac

echo "==> Downloading $asset"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
curl -fsSL "$BASE/$asset" -o "$tmp/mcp.tar.gz"
curl -fsSL "$BASE/SHA256SUMS.txt" -o "$tmp/SHA256SUMS.txt"
expected="$(awk -v name="$asset" '$2 == name { print $1; exit }' "$tmp/SHA256SUMS.txt")"
[ -n "$expected" ] || { echo "SemanticCompute: $asset is missing from SHA256SUMS.txt." >&2; exit 1; }
if command -v shasum >/dev/null 2>&1; then
  actual="$(shasum -a 256 "$tmp/mcp.tar.gz" | awk '{print $1}')"
else
  actual="$(sha256sum "$tmp/mcp.tar.gz" | awk '{print $1}')"
fi
[ "$actual" = "$expected" ] || { echo "SemanticCompute: checksum mismatch for $asset." >&2; exit 1; }
echo "    verified: SHA-256 $actual"
tar -xzf "$tmp/mcp.tar.gz" -C "$tmp"
bin="$(find "$tmp" -type f -name 'semanticcompute-mcp' 2>/dev/null | head -1)"
[ -n "$bin" ] || { echo "SemanticCompute: could not find semanticcompute-mcp in the archive." >&2; exit 1; }

mkdir -p "$BINDIR"
install -m 0755 "$bin" "$DEST"
[ "$os" = "Darwin" ] && xattr -d com.apple.quarantine "$DEST" 2>/dev/null || true
echo "==> Installed: $DEST"

if printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"install","version":"1"}}}' \
     | "$DEST" 2>/dev/null | grep -q '"serverInfo"'; then
  echo "    verified: the server answers MCP initialize."
else
  echo "    WARNING: the server did not respond as expected — see docs/INSTALL-MCP.md." >&2
fi

if command -v claude >/dev/null 2>&1; then
  if claude mcp get semanticcompute >/dev/null 2>&1; then
    echo "==> Claude Code: semanticcompute is already registered"
  else
    echo "==> Registering with Claude Code (user scope)"
    if claude mcp add semanticcompute -s user -- "$DEST" 2>/dev/null; then
      echo "    registered. Restart Claude Code, then run /mcp to confirm."
    else
      echo "    registration failed — use the manual command printed below." >&2
    fi
  fi
else
  echo "==> Claude Code CLI not on PATH — use the manual command printed below."
fi

if command -v codex >/dev/null 2>&1; then
  if codex mcp get semanticcompute >/dev/null 2>&1; then
    echo "==> Codex: semanticcompute is already registered"
  else
    echo "==> Registering with Codex"
    if codex mcp add semanticcompute -- "$DEST" 2>/dev/null; then
      echo "    registered. Restart Codex, then confirm with: codex mcp get semanticcompute"
    else
      echo "    registration failed — use the manual command printed below." >&2
    fi
  fi
else
  echo "==> Codex CLI not on PATH — use the manual command printed below."
fi

if command -v gemini >/dev/null 2>&1; then
  if gemini mcp list 2>/dev/null | grep -q 'semanticcompute'; then
    echo "==> Gemini CLI: semanticcompute is already registered"
  else
    echo "==> Registering with Gemini CLI (user scope)"
    if gemini mcp add semanticcompute "$DEST" --scope user 2>/dev/null; then
      echo "    registered. Restart Gemini CLI, then confirm with: gemini mcp list"
    else
      echo "    registration failed — use the manual command printed below." >&2
    fi
  fi
else
  echo "==> Gemini CLI not on PATH — use the manual command printed below."
fi

cat <<EOF

────────────────────────────────────────────────────────────────────────
 Add SemanticCompute to Claude, Codex, Gemini, or another MCP client
────────────────────────────────────────────────────────────────────────
 • Claude Desktop   Download semanticcompute-mcp.mcpb from the Releases page
                    and double-click it (Settings ▸ Extensions). No JSON.

 • Claude Code      claude mcp add semanticcompute -s user -- $DEST

 • Codex            codex mcp add semanticcompute -- $DEST

 • Gemini CLI       gemini mcp add semanticcompute $DEST --scope user

 • VS Code/Copilot  code --add-mcp '{"name":"semanticcompute","command":"$DEST"}'

 • Cursor           add the stdio command in ~/.cursor/mcp.json
 • Windsurf         add the stdio command in ~/.codeium/windsurf/mcp_config.json
                    Exact JSON for both: docs/INSTALL-MCP.md

 • Any MCP client   stdio server — command:  $DEST

 Restart the client. You get 11 tools (sc_check_parity, sc_validate_metal_texture,
 sc_diagnose_divergence, sc_list_families, …), plus resources and prompts.
 Verify the live process with sc_version: require 1.22.1, build commit
 f7dcfa2cda82b81edb4474ff3d0d0b8e6defad1d, and 183 families.
────────────────────────────────────────────────────────────────────────
EOF
