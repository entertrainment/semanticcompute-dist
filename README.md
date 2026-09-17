# SemanticCompute — distribution

**Numerical verification for heterogeneous compute.** Bring any two arrays — a CUDA, Metal, Triton, or
hand-written kernel result and the reference you trust — and prove they agree under a tolerance you state, or get
an exact account of where and why they diverge. SemanticCompute classifies FMA contraction, denormal flushing,
NaN/infinity differences, reduction order, and ULP drift, and measures accuracy against a higher-precision truth
where a family supplies one. Verification is the product; SemanticCompute is not a general GPU framework.

This is the **public binary distribution** repository: signed/notarised macOS and native Linux artifacts,
checksums, SBOM, evidence, release notes, and the commercial licence. Source is not distributed here; source
review is available under NDA.

The current **v1.23.0** release contains 188 verified families and 20 MCP tools. It includes exact audit/storage
families, DICOM/perfusion correlation contract alignment, the bounded Live byte-parity service, MacResilience
typed adapters, and licensed Docker MCP distribution.

- **Licence-gated binaries.** CLI, MCP, and Live compute operations require an active expiring/revocable
  entitlement. Trial keys can have execution-credit and installation ceilings; paid keys follow their plan.
  Help, version, MCP discovery, and health remain available for activation diagnosis.
- **Complete native cut.** macOS is universal, Developer-ID signed, and notarised. Linux x86-64 and AArch64
  archives are built natively by tag CI. The 15-asset release also carries SHA-256 checksums, CycloneDX SBOM,
  notice, and scoped CUDA compile/device evidence.
- **Agent-ready.** One MCPB or stdio executable exposes the same 20 tools to Claude, Codex, Gemini, VS Code,
  Cursor, Windsurf, and other MCP clients. The MCPB requests the licence key as a masked required field.
- **Docker MCP.** The tag also produces a signed Linux/amd64 + Linux/arm64 image with SBOM and provenance at
  `ghcr.io/entertrainment/semanticcompute-mcp:1.23.0`.
- **Hosted-trial boundary.** The public Cloudflare entitlement/control plane is online, while browser execution
  stays disabled until a pinned runner passes its public canary. No hosted CPU or NVIDIA execution is implied.
- **Legacy boundary.** Licence terms still apply to v1.22.1 and earlier copies that were already downloaded, but
  those executables predate online enforcement and are no longer distributed.

Start here:

- **[v1.23.0 release notes](RELEASE_NOTES_1.23.0.md)** — capabilities, evidence, assets, setup, and limits.
- **[CHANGELOG.md](CHANGELOG.md)** — complete version history.
- **[QUICKSTART.md](QUICKSTART.md)** — verify a kernel result in ten minutes.
- **[docs/INSTALL-MCP.md](docs/INSTALL-MCP.md)** — Claude, Codex, Gemini, and editor-agent setup.
- **[TRUST.md](TRUST.md)** — how to evaluate a closed-source verifier.
- **[EULA.md](EULA.md)** — binary licence and production-use boundary.
- **[NOTICE](NOTICE)** and **[SBOM](semanticcompute.cdx.json)** — composition and licence metadata.
- **[Live product page](https://entertrainment.github.io/semanticcompute-dist/)**.
- **[Licence-service privacy](https://entertrainment.github.io/semanticcompute-dist/licence-privacy.html)**.

Install after receiving a trial or paid key:

```bash
export SEMANTICCOMPUTE_LICENCE_KEY='sc_lic_…'
curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
```

The installer is pinned to 1.23.0, downloads all three native products plus `SHA256SUMS.txt`, verifies each asset,
and only then installs. Commercial licensing and design partnerships: **douglas@entertrainment.co.uk**.
