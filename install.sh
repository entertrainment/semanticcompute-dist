#!/usr/bin/env bash
# Install checksum-verified SemanticCompute 1.23.0 native distribution executables.
set -euo pipefail

VERSION="${SC_VERSION:-1.23.0}"
REPOSITORY="${SC_DIST_REPOSITORY:-entertrainment/semanticcompute-dist}"
INSTALL_DIR="${SC_INSTALL_DIR:-$HOME/.local/bin}"
BASE_URL="https://github.com/${REPOSITORY}/releases/download/v${VERSION}"

case "$(uname -s):$(uname -m)" in
  Darwin:arm64|Darwin:x86_64)
    MCP_ASSET="semanticcompute-mcp-macos-universal.tar.gz"
    PARITY_ASSET="semanticcompute-parity-macos-universal"
    LIVE_ASSET="semanticcompute-live-macos-universal.tar.gz"
    LIVE_PAYLOAD="semanticcompute-live-macos-universal"
    ;;
  Linux:x86_64)
    MCP_ASSET="semanticcompute-mcp-linux-x86_64.tar.gz"
    PARITY_ASSET="semanticcompute-parity-linux-x86_64.tar.gz"
    LIVE_ASSET="semanticcompute-live-linux-x86_64.tar.gz"
    LIVE_PAYLOAD="semanticcompute-live"
    ;;
  Linux:aarch64|Linux:arm64)
    MCP_ASSET="semanticcompute-mcp-linux-aarch64.tar.gz"
    PARITY_ASSET="semanticcompute-parity-linux-aarch64.tar.gz"
    LIVE_ASSET="semanticcompute-live-linux-aarch64.tar.gz"
    LIVE_PAYLOAD="semanticcompute-live"
    ;;
  *)
    echo "Unsupported platform: $(uname -s) $(uname -m)" >&2
    exit 1
    ;;
esac

WORK="$(mktemp -d "${TMPDIR:-/tmp}/semanticcompute-install.XXXXXX")"
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

download() {
  local name="$1"
  curl --fail --location --silent --show-error "$BASE_URL/$name" --output "$WORK/$name"
}

verify() {
  local name="$1" expected actual
  expected="$(awk -v file="$name" '$2 == file || $2 == "*" file { print $1; exit }' "$WORK/SHA256SUMS.txt")"
  [[ "$expected" =~ ^[0-9a-fA-F]{64}$ ]] || {
    echo "SHA256SUMS.txt has no valid entry for $name" >&2
    exit 1
  }
  if command -v shasum >/dev/null 2>&1; then
    actual="$(shasum -a 256 "$WORK/$name" | awk '{print $1}')"
  elif command -v sha256sum >/dev/null 2>&1; then
    actual="$(sha256sum "$WORK/$name" | awk '{print $1}')"
  else
    echo "Install shasum or sha256sum before installing SemanticCompute." >&2
    exit 1
  fi
  [[ "$actual" == "$expected" ]] || {
    echo "Checksum mismatch for $name" >&2
    exit 1
  }
}

echo "Downloading SemanticCompute v${VERSION} for $(uname -s) $(uname -m)…"
download SHA256SUMS.txt
for asset in "$MCP_ASSET" "$PARITY_ASSET" "$LIVE_ASSET"; do
  download "$asset"
  verify "$asset"
done

mkdir -p "$WORK/mcp" "$WORK/parity" "$WORK/live"
tar -C "$WORK/mcp" -xzf "$WORK/$MCP_ASSET"
if [[ "$PARITY_ASSET" == *.tar.gz ]]; then
  tar -C "$WORK/parity" -xzf "$WORK/$PARITY_ASSET"
  PARITY_PAYLOAD="semanticcompute-parity"
else
  cp "$WORK/$PARITY_ASSET" "$WORK/parity/semanticcompute-parity"
  PARITY_PAYLOAD="semanticcompute-parity"
fi
tar -C "$WORK/live" -xzf "$WORK/$LIVE_ASSET"

[[ -x "$WORK/mcp/semanticcompute-mcp" || -f "$WORK/mcp/semanticcompute-mcp" ]]
[[ -f "$WORK/parity/$PARITY_PAYLOAD" ]]
[[ -f "$WORK/live/$LIVE_PAYLOAD" ]]

mkdir -p "$INSTALL_DIR"
install -m 0755 "$WORK/mcp/semanticcompute-mcp" "$INSTALL_DIR/semanticcompute-mcp"
install -m 0755 "$WORK/parity/$PARITY_PAYLOAD" "$INSTALL_DIR/semanticcompute-parity"
install -m 0755 "$WORK/live/$LIVE_PAYLOAD" "$INSTALL_DIR/semanticcompute-live"

if [[ "$(uname -s)" == Darwin ]]; then
  codesign --verify --strict --all-architectures "$INSTALL_DIR/semanticcompute-mcp"
  codesign --verify --strict --all-architectures "$INSTALL_DIR/semanticcompute-parity"
  codesign --verify --strict --all-architectures "$INSTALL_DIR/semanticcompute-live"
fi

"$INSTALL_DIR/semanticcompute-parity" --version
cat <<NOTICE

Installed checksum-verified SemanticCompute v${VERSION} executables in:
  ${INSTALL_DIR}

Before compute operations, place the key delivered after trial approval or purchase in your protected shell or
agent environment:
  export SEMANTICCOMPUTE_LICENCE_KEY='sc_lic_…'

Register the MCP executable with one or more agents:
  claude mcp add semanticcompute -s user -e SEMANTICCOMPUTE_LICENCE_KEY="\$SEMANTICCOMPUTE_LICENCE_KEY" -- ${INSTALL_DIR}/semanticcompute-mcp
  codex mcp add semanticcompute --env SEMANTICCOMPUTE_LICENCE_KEY="\$SEMANTICCOMPUTE_LICENCE_KEY" -- ${INSTALL_DIR}/semanticcompute-mcp
  gemini mcp add semanticcompute ${INSTALL_DIR}/semanticcompute-mcp --scope user --env SEMANTICCOMPUTE_LICENCE_KEY="\$SEMANTICCOMPUTE_LICENCE_KEY"

Claude Desktop can instead install semanticcompute-mcp.mcpb from the same release and will request the key in a
masked required field. Never put a real key in a repository or command-line argument to a SemanticCompute binary.
NOTICE
