# SemanticCompute — distribution

**Numerical verification for heterogeneous compute.** Prove a Metal / portable-C / WGSL-WebGPU
computation matches a deterministic CPU reference under a tolerance *you* state — and, where you
have a higher-precision reference, measure how *accurate* it is. When they diverge, it tells you
*why*. Verification is the product; it is deliberately narrow (not a GPU framework).

This is the **public distribution** repo: prebuilt macOS binaries, docs, and the licence. The source is
closed (commercial licence; source review under NDA).

- **Download:** the MCP server (`.mcpb`) + CLI binaries are on the [Releases](../../releases) page — grab the
  `.mcpb` / `-arm64` asset, **not** the auto-generated "Source code" archive (that's just these docs).
  Binaries are arm64 (Apple Silicon) and **not yet notarised** — macOS Gatekeeper will ask you to confirm; a
  universal, notarised build is the next step.
- **[QUICKSTART.md](QUICKSTART.md)** — run it on your own kernel in 10 minutes (no source needed).
- **[TRUST.md](TRUST.md)** — how a closed-source verifier earns trust (and how you confirm it yourself).
- **[EULA.md](EULA.md)** — the binary licence (free to evaluate; commercial for production).
- **Live demo:** the interactive divergence "kill-shot" — https://entertrainment.github.io/semanticcompute-dist/

Pre-adoption, single author. Commercial licensing / design partnership: **douglas@entertrainment.co.uk**
