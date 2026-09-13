# SemanticCompute — distribution

**Numerical verification for heterogeneous compute.** Bring any two arrays — a CUDA, Metal, or hand-written
kernel result and the reference you trust, whatever produced them — and prove they agree under a tolerance
*you* state, or get told exactly *where* and *why* they diverge (FMA, FTZ, NaN, reduction order). Where you
have a higher-precision reference, it also measures how *accurate* the result is. Verification is the product;
it is deliberately narrow (not a GPU framework).

This is the **public distribution** repo: prebuilt macOS and Linux binaries, docs, release notes, and the licence.
The source is closed (commercial licence; source review under NDA). The current **v1.22.1** release contains 183
verified families and 11 MCP tools, including complete-MSL texture validation, FDN reverb, and twelve bounded
structured-data/CBOR-LD families.

- **Install (one command)** — the signed MCP server, checksum-verified and registered with Claude Code, Codex,
  and Gemini CLI when their CLIs are present:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
  ```
  For Claude Desktop, just double-click `semanticcompute-mcp.mcpb`. Exact setup for Claude Desktop, Claude Code,
  Codex, Gemini CLI, VS Code/Copilot, Cursor, and Windsurf is in **[docs/INSTALL-MCP.md](docs/INSTALL-MCP.md)**.
- **Download:** the MCP server (`.mcpb`) + CLI binaries are on the [Releases](../../releases) page — grab the
  `.mcpb` / `-universal` asset, **not** the auto-generated "Source code" archive (that's just these docs).
  macOS binaries are universal (Intel + Apple Silicon), **signed (Developer ID) and notarised**. Native Linux
  **x86-64 and AArch64** MCP/parity archives are on the same page. Each release also carries SHA-256 checksums,
  a CycloneDX SBOM, `NOTICE`, and separately labelled CUDA compile/device evidence.
- **[v1.22.1 release notes](RELEASE_NOTES_1.22.1.md)** — detailed, cumulative changes since 1.20.0, with evidence
  boundaries for texture execution, FDN, CBOR-LD, stress findings, Linux, Metal, and CUDA.
- **[CHANGELOG.md](CHANGELOG.md)** — the complete version history.
- **[QUICKSTART.md](QUICKSTART.md)** — run it on your own kernel in 10 minutes (no source needed).
- **[TRUST.md](TRUST.md)** — how a closed-source verifier earns trust (and how you confirm it yourself).
- **[EULA.md](EULA.md)** — the binary licence (free to evaluate; commercial for production).
- **[NOTICE](NOTICE)** + **[SBOM](semanticcompute.cdx.json)** — third-party-component notice and a CycloneDX
  descriptor for your SBOM / software-composition tooling. SemanticCompute is a **commercial** component
  (`LicenseRef-SemanticCompute-Commercial`); production use and redistribution require a licence and must be
  disclosed. Every binary carries a self-identifying licence marker (`semanticcompute-parity --marker`).
- **Live demo:** the interactive divergence "kill-shot" — https://entertrainment.github.io/semanticcompute-dist/

Pre-adoption, single author. Commercial licensing / design partnership: **douglas@entertrainment.co.uk**
