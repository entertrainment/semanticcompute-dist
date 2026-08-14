# KernelBench‑style verify loop — SemanticCompute as the correctness layer

KernelBench and NVIDIA SOL‑ExecBench give an agent a reference implementation and ask it to generate a faster
kernel that stays *functionally correct*. The correctness gate is usually `torch.allclose` → a boolean. This
demo replaces that boolean with a **diagnosis**: when the generated kernel's output diverges, SemanticCompute
reports *where* and *why* (per‑element ULP + cause), the fix is applied from the cause, and it re‑verifies — a
generate → verify → fix loop that closes automatically.

**No CUDA backend required.** SemanticCompute has no CUDA backend and does not need one: the doctor is
*provenance‑agnostic* — it compares two arrays as Float32, whatever produced them. That's exactly why it fits
KernelBench (which generates *CUDA* kernels). The "generated kernel" here is synthetic — a planted bug (a naive
softmax missing its max‑shift, one of the most common generated‑kernel mistakes, which overflows `exp()` to
`inf`/`NaN`) — so the demo runs with **no GPU**. On a real run, replace `generated_v1(...)` with your generated
CUDA kernel's output copied to the host (`out.detach().cpu().numpy()`).

## Run
```bash
BIN="$(swift build -c release --product semanticcompute-parity --show-bin-path)/semanticcompute-parity"
SC_PARITY="$BIN" python3 examples/kernelbench-loop/demo.py
```
(or point `SC_PARITY` at a released binary; omit it if `semanticcompute-parity` is on `PATH`.)

Output: **v1 DIVERGED** with the localised per‑element cause → fix applied → **v2 VERIFIED** → loop closed.

## The agent version — `demo_mcp.py` (structured MCP output)
`demo_mcp.py` runs the same loop over the **`semanticcompute-mcp`** server (JSON‑RPC/stdio) with a tiny
stdlib MCP client, reading the typed `structuredContent`: the agent branches on the `causeHistogram` and
`compatible` **fields**, not on prose.
```bash
MCP="$(swift build -c release --product semanticcompute-mcp --show-bin-path)/semanticcompute-mcp"
SC_MCP="$MCP" python3 examples/kernelbench-loop/demo_mcp.py
```
Output: `[diagnose] causeHistogram={"nanGeneration":14,…} → [decide] apply max‑shift → [verify] compatible=True → loop closed`.
This is the closed loop as an MCP workflow — the shape KernelBench / SOL‑ExecBench are moving toward. (`demo.py`
above is the CLI variant, via the stdlib wrapper in `Integrations/python/sc_verify.py`.)


---

<!-- FINDER-STATUS:BEGIN (auto) -->
> 📊 **Doc status:** 🟢 Complete · **100%** complete · CLI + MCP agent-loop KernelBench demos, both tested
> <sub>Finder tags: `Complete`, `▓▓▓▓ 75–100%` · auto-assessed 2026-08-14</sub>
<!-- AGENTS: after materially changing this module, refresh status+tag → `python3 Tools/MarkdownStatusQuickLook/tagkit.py set <THIS_FILE> <status> <percent> "<note>"` (status: complete|complete_improvable|in_progress|not_done|superseded|irrelevant). Protocol: Tools/MarkdownStatusQuickLook/DOC-STATUS-AGENTS.md -->
<!-- FS-HASH:89625bb9 -->
<!-- FINDER-STATUS:END -->
