# SemanticCompute — Quickstart (binary, no source needed)

Prove your GPU/CUDA/ported result matches a reference you trust under a tolerance **you** state — the doctor
compares any two arrays, whatever produced them — and, where you have a higher-precision reference, measure how
*accurate* it is. You run a signed, notarised macOS binary (universal: Intel + Apple Silicon) or the prebuilt
x86-64 Linux binary — both on the Releases page (the CLI/MCP build and pass their full suite on both). The
source stays closed. Verification is the product — it is deliberately narrow (not a GPU framework, not a
Swift→GPU transpiler).

## Option A — the MCP server (for agents / Claude Code / any MCP client)

1. Download `semanticcompute-mcp.mcpb` from the latest release, or the raw binary:
   ```bash
   curl -L -o semanticcompute-mcp.tar.gz \
     https://github.com/entertrainment/semanticcompute-dist/releases/latest/download/semanticcompute-mcp-macos-universal.tar.gz
   tar xzf semanticcompute-mcp.tar.gz            # → ./semanticcompute-mcp   (universal: Intel + Apple Silicon)
   ```
2. Register it (Claude Code shown; any MCP client works):
   ```bash
   claude mcp add semanticcompute -- /ABSOLUTE/PATH/TO/semanticcompute-mcp
   ```
3. Use the tools — no source, no build:
   - `sc_check_parity` — does a candidate match a reference under `exact | default | ulp | absrel`?
   - `sc_diagnose_divergence` — *why* did it diverge (FMA drift, denormal flush, NaN, ±∞ overflow…)?
   - `sc_zoo` — run a canonical silent-divergence specimen to see it in action.
   - `sc_list_families` / `sc_suggest_families` — what compute is already covered.

## Option B — the CLI (for CI / scripts / a quick check)

```bash
curl -L -o semanticcompute-parity \
  https://github.com/entertrainment/semanticcompute-dist/releases/latest/download/semanticcompute-parity-macos-universal
chmod +x semanticcompute-parity

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

> Pre-adoption, single author. The binaries are free to evaluate; commercial production use is
> licensed (see the EULA / pricing). Source is available under commercial terms / audit under NDA.
