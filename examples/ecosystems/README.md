# Verifying output from Triton / vLLM / PyTorch / CUDA / FlashAttention

SemanticCompute is **provenance‑agnostic** — it verifies two float arrays, whatever produced them. These worked
examples verify the *characteristic* numerical failure each ecosystem is publicly documented to hit, so the
claim *"verifies numerics from X"* is **demonstrated** (verification of their output), not implied.

Each scenario reproduces the documented **mechanism** (cited below) — no captured tensor, no GPU — so it runs
anywhere. On a real case, feed the actual output tensor (`out.detach().cpu().numpy()`).

| Ecosystem | Documented failure | Reproduced here | SemanticCompute diagnosis |
|---|---|---|---|
| **Triton** | TF32 rounding (`allow_tf32`) — [triton#6054] | 10‑bit‑mantissa products vs fp32 | numeric divergence (~1e‑3 rel, ~10⁴ ULP) |
| **vLLM** | different GPUs → different output — [vllm#11526] | same logits, two reduction orders | numeric divergence (reassociation) |
| **FlashAttention** | varlen vs reference, causal mask — [#581] / [#1772] | masked‑position `0 * inf` | NaN generation (finite → NaN) |

(PyTorch + CUDA are covered by the KernelBench closed‑loop demo in [`../kernelbench-loop/`](../kernelbench-loop/) —
a PyTorch reference vs a generated kernel, diagnosed and fixed in a loop.)

## Run
Download the released `semanticcompute-parity` binary from the [Releases](../../releases) page (macOS universal,
signed + notarised; or the Linux x86-64 tarball), then point `SC_PARITY` at it:
```bash
SC_PARITY=/path/to/semanticcompute-parity  python3 examples/ecosystems/verify_output.py
```
(With a source licence, `BIN="$(swift build -c release --product semanticcompute-parity --show-bin-path)/…"` builds it instead.)

Add `--html report.html` to also write a self‑contained **verification report** (one section per ecosystem, each
divergence mapped by cause) — a shareable audit artifact, no source or browser tooling needed.

## What this backs — and what it doesn't
- **Does:** SemanticCompute verifies output produced by these tools and classifies the exact failure each is
  documented to hit. Provenance‑agnostic; no CUDA/Triton backend needed or implied. This is the honest basis for
  *"verifies numerics from Triton · vLLM · PyTorch · CUDA · FlashAttention"* — as verification of their **output**.
- **Doesn't:** integrate with, partner with, run inside, or claim endorsement from any of them. These reproduce
  the documented mechanism; they are not captured production tensors.

[triton#6054]: https://github.com/triton-lang/triton/issues/6054
[vllm#11526]: https://github.com/vllm-project/vllm/issues/11526
[#581]: https://github.com/Dao-AILab/flash-attention/issues/581
[#1772]: https://github.com/Dao-AILab/flash-attention/issues/1772

