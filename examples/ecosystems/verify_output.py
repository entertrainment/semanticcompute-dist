#!/usr/bin/env python3
"""
Worked examples — SemanticCompute verifying the *characteristic* numerical failure each ecosystem is publicly
documented to hit: Triton (TF32 rounding), vLLM (reduction order across GPUs), FlashAttention (causal-mask NaN).

Each scenario REPRODUCES THE MECHANISM from a cited issue using the same numerical mistake that project's
kernels make — the candidate is generated here (no captured tensor, no GPU), so it runs anywhere. On a real
case you feed the actual output (`out.detach().cpu().numpy()`); SemanticCompute is provenance-agnostic and needs
no backend for any of these.

What this backs: the claim "verifies numerics from Triton / vLLM / PyTorch / CUDA / FlashAttention" — as
demonstrated *verification of their output*, NOT as an integration or endorsement.

Run:
    SC_PARITY=/path/to/semanticcompute-parity  python3 examples/ecosystems/verify_output.py
"""

import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from sc_verify import verify  # noqa: E402

BINARY = os.environ.get("SC_PARITY", "semanticcompute-parity")


def show(title, cites, reference, candidate, tol, note=None):
    r = verify(reference, candidate, tolerance=tol, binary=BINARY)
    print(f"\n=== {title} ===")
    print(f"  reproduces:  {cites}")
    print(f"  tolerance:   {tol}")
    print("  " + ("AGREES with the reference." if r["agree"] else "DIVERGED — SemanticCompute diagnosis:"))
    if not r["agree"]:
        for line in r["report"].splitlines():
            if line.strip():
                print("    " + line)
    if note:
        print(f"  note:        {note}")
    return r


# ---- 1. Triton — TF32 / FP4 rounding disagreement (triton-lang/triton#6054; allow_tf32 numerical errors) ----
def _tf32(x):
    """Round a float32 to TF32 (10-bit mantissa) — the precision knob behind the allow_tf32 divergence."""
    bits = struct.unpack("<I", struct.pack("<f", float(x)))[0] & 0xFFFFE000  # drop the low 13 mantissa bits
    return struct.unpack("<f", struct.pack("<I", bits))[0]


def triton():
    xs = [1.2345679, 2.7182817, 3.1415927, 0.6931472, 1.4142135, 2.2360680]
    ys = [2.3456789, 1.6180340, 0.5772157, 3.3219281, 1.7320508, 0.4342945]
    reference = [x * y for x, y in zip(xs, ys)]                    # full fp32
    candidate = [_tf32(x) * _tf32(y) for x, y in zip(xs, ys)]      # a Triton kernel with allow_tf32=True
    show("Triton — TF32 matmul rounding", "triton#6054 / allow_tf32 numerical errors", reference, candidate,
         "default", note="TF32 drops 13 mantissa bits — a ~1e-3 relative error, far beyond a rounding residual.")


# ---- 2. vLLM — different GPUs pick different reduction kernels -> reassociated sums (vllm#11526) ----
def _sum(vals):
    s = 0.0
    for v in vals:
        s += v
    return s


def vllm():
    # Each "logit" is an accumulation with a large cancelling pair; the order the kernel sums in changes the
    # result (float addition is not associative). An A100 and an H100 legitimately pick different orders.
    bases = [
        [1.0, 1e16, -1e16],
        [2.0, 3.0, 1e16, -1e16],
        [1e15, -1e15, 4.0],
        [5.0, 1e16, -1e16, 6.0],
    ]
    reference = [_sum(b) for b in bases]                 # one kernel's reduction order
    candidate = [_sum(list(reversed(b))) for b in bases]  # another kernel's order
    show("vLLM — reduction order across GPUs", "vllm#11526 (different sampled output on different GPUs)",
         reference, candidate, "default",
         note="Same logits, two legitimate kernel orders. A 1-ULP logit difference is enough to flip an argmax "
              "-> a different sampled token, which is why vLLM's tests compare logprobs, not exact output.")


# ---- 3. FlashAttention — causal-mask NaN (Dao-AILab/flash-attention#581, #1772) ----
def flashattention():
    NEG_INF = float("-inf")
    scores = [NEG_INF, 1.0, 1.5, NEG_INF]  # two masked (causal) positions
    m = max(s for s in scores if s != NEG_INF)
    e = [0.0 if s == NEG_INF else math.exp(s - m) for s in scores]
    denom = sum(e)
    reference = [v / denom for v in e]  # correct masked softmax: 0 at masked positions
    # The flash online-softmax path hits 0 * inf in the rescale at a masked position -> NaN (the reported bug).
    candidate = [(0.0 * float("inf")) if s == NEG_INF else math.exp(s - m) / denom for s in scores]
    show("FlashAttention — causal-mask NaN", "flash-attention#581 / #1772 (varlen vs reference, causal mask)",
         reference, candidate, "default", note="Masked positions become NaN (finite -> NaN) — an unguarded 0*inf.")


def main():
    print("SemanticCompute — verifying output from Triton / vLLM / FlashAttention (provenance-agnostic, no GPU).")
    triton()
    vllm()
    flashattention()
    print("\nEach diverged and was classified. Feed a real captured tensor to run the actual case.")


if __name__ == "__main__":
    main()
