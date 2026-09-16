# SemanticCompute — Quickstart (binary, no source needed)

Prove your GPU/CUDA/ported result matches a reference you trust under a tolerance **you** state — the doctor
compares any two arrays, whatever produced them — and, where you have a higher-precision reference, measure how
*accurate* it is. You run a signed, notarised macOS binary (universal: Intel + Apple Silicon) or a native
x86-64/AArch64 Linux binary. New installation is paused while licence-gated 1.23 artifacts replace the ungated
1.22.1 and earlier executables. Request a bounded trial or paid build at douglas@entertrainment.co.uk. The
source stays closed. Verification is the product — it is deliberately narrow (not a GPU framework, not a
Swift→GPU transpiler).

## Option A — the MCP server (for Claude / Codex / Gemini / editor agents)

1. Receive the signed gated `semanticcompute-mcp.mcpb` or native archive and its `sc_lic_…` key through the
   licensed distribution channel. Public legacy downloads are paused.
2. Export the key and register the binary with the agents you use:
   ```bash
   export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"
   claude mcp add semanticcompute -s user -e SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" -- /ABSOLUTE/PATH/TO/semanticcompute-mcp
   codex mcp add semanticcompute --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" -- /ABSOLUTE/PATH/TO/semanticcompute-mcp
   gemini mcp add semanticcompute /ABSOLUTE/PATH/TO/semanticcompute-mcp --scope user --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY"
   ```
   Cursor and Windsurf use the global JSON locations documented in [docs/INSTALL-MCP.md](docs/INSTALL-MCP.md).
3. Use the tools — no source, no build:
   - `sc_check_parity` — does a candidate match a reference under `exact | default | ulp | absrel`?
   - `sc_diagnose_divergence` — *why* did it diverge (FMA drift, denormal flush, NaN, ±∞ overflow…)?
   - `sc_zoo` — run a canonical silent-divergence specimen to see it in action.
   - `sc_list_families` / `sc_suggest_families` — what compute is already covered.
   - `sc_validate_metal_texture` — execute complete consumer-owned MSL and compare its RGBA texture with an
     independent CPU reference, with explicit status for compile, dispatch, readback, and parity.
   - `sc_version` — confirm version `1.22.1`, exact build commit, 183 families, backends, and feature flags.

## Option B — the CLI (for CI / scripts / a quick check)

```bash
export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"

# Prove two arrays agree under a stated tolerance (exit 0 agree / 1 diverged / 2 error):
echo '{"reference":[100],"candidate":[0]}' | ./semanticcompute-parity --tolerance ulp:1

# See the failure lab of canonical silent CPU↔GPU divergences, and run one end-to-end:
./semanticcompute-parity --zoo
./semanticcompute-parity --zoo 09-naive-vs-kahan-sum
./semanticcompute-parity --zoo export        # canonical JSON table (drives your own dashboards)
```

Point it at *your own* reference/candidate data — the tolerance is explicit, the report is
reproducible, and you can drop it in an audit trail. (The cause classifier gives leads, not
proofs. It carries no certification or regulatory approval — it produces evidence, not compliance.)

> Pre-adoption, single author. Bounded trial and paid distribution keys are issued under the EULA / pricing.
> Source review is available under commercial terms / audit under NDA.
