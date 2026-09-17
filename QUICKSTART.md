# SemanticCompute 1.23 — binary quickstart

SemanticCompute compares a candidate numerical result with a reference you trust under an explicit tolerance.
The commercial distribution is closed source and ships as signed binaries for macOS universal, Linux x86-64,
and Linux AArch64. Paid tool execution requires an active `sc_lic_…` entitlement through
`SEMANTICCOMPUTE_LICENCE_KEY`.

## Install the three command-line products

The installer downloads the version-pinned parity CLI, MCP server, and Live verifier, verifies every release
checksum before installing, and verifies Apple signatures on macOS. It does not edit agent configuration.

```bash
curl -fsSL https://raw.githubusercontent.com/entertrainment/semanticcompute-dist/main/install.sh | bash
export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"
```

The default destination is `~/.local/bin`. Set `SC_INSTALL_DIR` or `SC_VERSION` before running the installer to
choose another destination or an explicitly supported version.

## Register the MCP server

Use the absolute installed path and pass the key through the client's protected environment configuration:

```bash
claude mcp add semanticcompute -s user \
  -e SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  -- "$HOME/.local/bin/semanticcompute-mcp"

codex mcp add semanticcompute \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  -- "$HOME/.local/bin/semanticcompute-mcp"

gemini mcp add semanticcompute "$HOME/.local/bin/semanticcompute-mcp" --scope user \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY"
```

Cursor, VS Code/Copilot, Windsurf/Cascade, and any stdio MCP client are covered in
[`docs/INSTALL-MCP.md`](docs/INSTALL-MCP.md). Restart the client after changing its MCP configuration.

Call `sc_version` and require version `1.23.0`, an exact non-`unknown` build commit, 188 families, and 20 tools
before relying on a newly installed process. Then begin with:

- `sc_check_parity` for floating-point parity under `exact`, `default`, `ulp`, or `absrel` tolerance;
- `sc_check_integer_parity` for exact UInt64 values without JSON floating-point loss;
- `sc_list_families` before implementing numerical, DSP, graph, storage, or structured-data work;
- `sc_validate_metal_texture` for an executed, read-back Metal texture comparison;
- `sc_diagnose_divergence` and `sc_verification_report` for inspectable failure evidence.

## Use the parity CLI

```bash
export SEMANTICCOMPUTE_LICENCE_KEY="sc_lic_…"

printf '%s\n' '{"reference":[1,2,3],"candidate":[1,2,3.0000002]}' \
  | semanticcompute-parity --tolerance default

semanticcompute-parity --zoo
semanticcompute-parity --zoo 09-naive-vs-kahan-sum
```

Exit status is `0` for agreement, `1` for a numerical divergence, and `2` for invalid input or an operational
error. The cause classifier supplies diagnostic leads rather than mathematical proof. SemanticCompute produces
verification evidence; it does not provide regulatory certification.

Request a bounded trial or paid entitlement at **douglas@entertrainment.co.uk**.
