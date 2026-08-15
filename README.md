# SemanticCompute — distribution

**Numerical verification for heterogeneous compute.** Bring any two arrays — a CUDA, Metal, or hand-written
kernel result and the reference you trust, whatever produced them — and prove they agree under a tolerance
*you* state, or get told exactly *where* and *why* they diverge (FMA, FTZ, NaN, reduction order). Where you
have a higher-precision reference, it also measures how *accurate* the result is. Verification is the product;
it is deliberately narrow (not a GPU framework).

This is the **public distribution** repo: prebuilt macOS binaries, docs, and the licence. The CLI, MCP server,
and library also build and pass their full test suite on **Linux** (Swift 6.2) — a prebuilt Linux binary is on
request. The source is closed (commercial licence; source review under NDA).

- **Install (one command)** — the signed MCP server, installed + registered with Claude Code if the `claude`
  CLI is present:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
  ```
  For Claude Desktop, just double-click `semanticcompute-mcp.mcpb`. Per-client setup (Desktop · Claude Code ·
  Cursor) is in **[docs/INSTALL-MCP.md](docs/INSTALL-MCP.md)**.
- **Download:** the MCP server (`.mcpb`) + CLI binaries are on the [Releases](../../releases) page — grab the
  `.mcpb` / `-universal` asset, **not** the auto-generated "Source code" archive (that's just these docs).
  macOS binaries are universal (Intel + Apple Silicon), **signed (Developer ID) and notarised**. Linux:
  prebuilt **x86-64** binaries (`semanticcompute-*-linux-x86_64.tar.gz`) are on the same Releases page, or, with a source
  licence, build from source.
- **[QUICKSTART.md](QUICKSTART.md)** — run it on your own kernel in 10 minutes (no source needed).
- **[TRUST.md](TRUST.md)** — how a closed-source verifier earns trust (and how you confirm it yourself).
- **[EULA.md](EULA.md)** — the binary licence (free to evaluate; commercial for production).
- **[NOTICE](NOTICE)** + **[SBOM](semanticcompute.cdx.json)** — third-party-component notice and a CycloneDX
  descriptor for your SBOM / software-composition tooling. SemanticCompute is a **commercial** component
  (`LicenseRef-SemanticCompute-Commercial`); production use and redistribution require a licence and must be
  disclosed. Every binary carries a self-identifying licence marker (`semanticcompute-parity --marker`).
- **Live demo:** the interactive divergence "kill-shot" — https://entertrainment.github.io/semanticcompute-dist/

Pre-adoption, single author. Commercial licensing / design partnership: **douglas@entertrainment.co.uk**
