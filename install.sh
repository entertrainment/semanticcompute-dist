#!/usr/bin/env bash
#
# SemanticCompute MCP server — one-command install.
#
#   curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
#
# Downloads the signed, notarised MCP server for your platform, installs it to ~/.local/bin, verifies it
# answers MCP, and registers it with Claude Code if the `claude` CLI is present. Prints copy-paste config for
# every other client. Re-runnable. Override the install dir with SC_BINDIR=/somewhere.
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
    if [ "$arch" != "x86_64" ]; then
      echo "SemanticCompute: only Linux x86_64 prebuilt binaries are published (you have $arch)." >&2
      echo "Contact douglas@entertrainment.co.uk for another architecture." >&2; exit 1
    fi
    asset="semanticcompute-mcp-linux-x86_64.tar.gz" ;;
  *) echo "SemanticCompute: unsupported OS '$os' (macOS and Linux only)." >&2; exit 1 ;;
esac

echo "==> Downloading $asset"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
curl -fsSL "$BASE/$asset" -o "$tmp/mcp.tar.gz"
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
  echo "==> Registering with Claude Code (user scope)"
  if claude mcp add semanticcompute -s user -- "$DEST" 2>/dev/null; then
    echo "    registered. Restart Claude Code, then run /mcp to confirm."
  else
    echo "    (looks already registered, or add it manually — see below.)"
  fi
else
  echo "==> 'claude' CLI not on PATH — add SemanticCompute to your client manually (below)."
fi

cat <<EOF

────────────────────────────────────────────────────────────────────────
 Add SemanticCompute to your assistant
────────────────────────────────────────────────────────────────────────
 • Claude Desktop   Download semanticcompute-mcp.mcpb from the Releases page
                    and double-click it (Settings ▸ Extensions). No JSON.

 • Claude Code      claude mcp add semanticcompute -s user -- $DEST
                    …or add to .mcp.json / ~/.claude.json:
                      "semanticcompute": { "type": "stdio", "command": "$DEST" }

 • Any MCP client   stdio server — command:  $DEST

 Restart the client. You get 9 tools (sc_check_parity, sc_diagnose_divergence,
 sc_list_families, …), plus resources and prompts.
────────────────────────────────────────────────────────────────────────
EOF
