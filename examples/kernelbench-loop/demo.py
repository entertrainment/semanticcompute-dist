#!/usr/bin/env python3
"""
KernelBench-style closed loop with SemanticCompute as the correctness layer.

The setup KernelBench (and NVIDIA SOL-ExecBench) use: give an agent a reference implementation, have it
generate an optimised kernel, and gate on "functionally correct + faster". The correctness gate today is
usually `torch.allclose` -> a boolean. This demo replaces that boolean with a *diagnosis*: when the generated
kernel's output diverges, SemanticCompute says WHERE and WHY (per-element ULP + cause), the fix is applied from
the cause, and it re-verifies -- a generate -> verify -> fix loop that closes automatically.

Provenance-agnostic: SemanticCompute has NO CUDA backend and does not need one. It compares two arrays as
Float32 whatever produced them. Here the "generated kernel" is synthetic (a planted bug) so the demo runs with
no GPU; on a real KernelBench run, replace `generated_v1(...)` with your generated CUDA kernel's output tensor
copied to the host (e.g. `out.detach().cpu().numpy()`).

Run:
    SC_PARITY=/path/to/semanticcompute-parity  python3 examples/kernelbench-loop/demo.py
(omit SC_PARITY if `semanticcompute-parity` is on PATH.)
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from sc_verify import verify  # noqa: E402  (the stdlib-only NumPy/PyTorch wrapper)

BINARY = os.environ.get("SC_PARITY", "semanticcompute-parity")

# ---- The KernelBench task: softmax over a vector. Large logits are where generated kernels get it wrong. ----
# Logits big enough that exp() overflows even in float64 (exp(>709) -> inf), so the classic "forgot the
# max-shift" bug produces inf/NaN instead of a valid distribution. This is one of the most common real
# mistakes an AI-generated softmax/attention kernel makes.
LOGITS = [700.0 + i for i in range(24)]


def softmax_reference(x):
    """The PyTorch-style reference: numerically stable (subtract the max before exp)."""
    m = max(x)
    e = [math.exp(v - m) for v in x]
    s = sum(e)
    return [v / s for v in e]


def _exp_hw(v):
    """exp as floating-point hardware (CUDA/Metal) does it: overflow returns +inf, not a Python exception."""
    try:
        return math.exp(v)
    except OverflowError:
        return math.inf


def generated_v1(x):
    """A first-pass 'generated kernel': naive softmax, NO max-shift -> exp overflows -> inf/NaN."""
    e = [_exp_hw(v) for v in x]         # exp(723) -> +inf (hardware behaviour)
    s = sum(e)                          # inf
    return [v / s for v in e]           # inf/inf = NaN for the big ones, finite/inf = 0 for the rest


def generated_v2(x):
    """The fix the agent applies from the diagnosis (overflow in exp -> add the max-shift)."""
    return softmax_reference(x)


def run(label, candidate_fn):
    ref = softmax_reference(LOGITS)
    cand = candidate_fn(LOGITS)
    r = verify(ref, cand, tolerance="default", binary=BINARY)
    print(f"\n=== {label} ===")
    if r["agree"]:
        print("VERIFIED — agrees with the reference under the tolerance.")
    else:
        print("DIVERGED — SemanticCompute diagnosis:")
        print(r["report"].rstrip())
    return r["agree"]


def main():
    print("KernelBench-style verify loop — SemanticCompute is the correctness layer (no CUDA backend needed).")
    ok1 = run("generated kernel v1  (naive softmax, no max-shift)", generated_v1)
    # The diagnosis localises the overflow/NaN in exp(); the fix is the max-shift. The agent applies it:
    ok2 = run("generated kernel v2  (max-shift applied, from the diagnosis)", generated_v2)

    print("\n--- loop ---")
    if (not ok1) and ok2:
        print("CLOSED: v1 diagnosed (localised cause) -> fix applied -> v2 verified. That's the closed loop.")
        sys.exit(0)
    print("UNEXPECTED: the demo did not close as designed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
