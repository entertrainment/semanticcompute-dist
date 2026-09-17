# SemanticCompute — distribution

**Numerical verification for heterogeneous compute.** Bring any two arrays — a CUDA, Metal, or hand-written
kernel result and the reference you trust, whatever produced them — and prove they agree under a tolerance
*you* state, or get told exactly *where* and *why* they diverge (FMA, FTZ, NaN, reduction order). Where you
have a higher-precision reference, it also measures how *accurate* the result is. Verification is the product;
it is deliberately narrow (not a GPU framework).

This is the **public distribution** repo: macOS and Linux release records, docs, release notes, and the licence.
The source is closed (commercial licence; source review under NDA). The current **v1.22.1** release contains 183
verified families and 11 MCP tools, including complete-MSL texture validation, FDN reverb, and twelve bounded
structured-data/CBOR-LD families.

- **New installation is paused.** The v1.22.1 and earlier executables predate online entitlement enforcement.
  The installer now refuses to download them while the signed, licence-gated 1.23 distribution is prepared.
  Request a bounded trial or paid key at **douglas@entertrainment.co.uk**.
- **What changes in 1.23:** CLI, MCP, and Live compute operations require an expiring, revocable online
  entitlement. Trial keys can have execution-credit and installation ceilings. Paid keys follow their
  subscription. Help, version, MCP discovery, and health remain available for activation diagnosis.
- **Legacy boundary:** licence terms still apply to v1.22.1 and earlier, but their already-downloaded copies
  cannot be remotely revoked. Release notes, checksums, SBOM, notice, and CUDA evidence remain as historical
  records while executable assets are unavailable.
- **[v1.22.1 release notes](RELEASE_NOTES_1.22.1.md)** — detailed, cumulative changes since 1.20.0, with evidence
  boundaries for texture execution, FDN, CBOR-LD, stress findings, Linux, Metal, and CUDA.
- **[CHANGELOG.md](CHANGELOG.md)** — the complete version history.
- **[QUICKSTART.md](QUICKSTART.md)** — run it on your own kernel in 10 minutes (no source needed).
- **[TRUST.md](TRUST.md)** — how a closed-source verifier earns trust (and how you confirm it yourself).
- **[EULA.md](EULA.md)** — the binary licence; new distributions also enforce an active trial or subscription key.
- **[NOTICE](NOTICE)** + **[SBOM](semanticcompute.cdx.json)** — third-party-component notice and a CycloneDX
  descriptor for your SBOM / software-composition tooling. SemanticCompute is a **commercial** component
  (`LicenseRef-SemanticCompute-Commercial`); production use and redistribution require a licence and must be
  disclosed. Every binary carries a self-identifying licence marker (`semanticcompute-parity --marker`).
- **Live demo:** the interactive divergence "kill-shot" — https://entertrainment.github.io/semanticcompute-dist/
- **Licence-service privacy:** https://entertrainment.github.io/semanticcompute-dist/licence-privacy.html

Pre-adoption, single author. Commercial licensing / design partnership: **douglas@entertrainment.co.uk**
