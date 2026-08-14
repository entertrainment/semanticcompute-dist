"""
sc_verify — feed two arrays to the SemanticCompute parity CLI from Python.

SemanticCompute's parity doctor is provenance-agnostic: it compares a *reference* array against a *candidate*
array (as Float32) and tells you, per element, the ULP distance and the likely cause (FMA contraction, denormal
flush, NaN, reduction reassociation, overflow direction). It does not care whether the candidate came from CUDA,
Metal, Triton, a CPU kernel, or anything else — so this thin wrapper is all a NumPy/PyTorch user needs.

Requirements: the `semanticcompute-parity` binary on PATH (or pass `binary=`). No Python deps beyond the stdlib;
NumPy arrays and PyTorch tensors are accepted duck-typed (no hard import).

Example
-------
    import numpy as np
    from sc_verify import verify

    ref  = np.log(x).astype(np.float32)          # your trusted reference
    cand = cuda_log(x)                            # your GPU/CUDA candidate, back on the host
    r = verify(ref, cand, tolerance="ulp:1")
    print(r["agree"], r["report"])               # -> False + the per-element ULP/cause report

CLI exit contract mirrored here: 0 = agree, 1 = diverged, 2 = usage/error.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any


def _to_floats(a: Any) -> list[float]:
    """Flatten a NumPy array, a PyTorch tensor, or a (nested) Python sequence to a flat list of floats."""
    # PyTorch tensor -> NumPy (duck-typed; no torch import required)
    if hasattr(a, "detach") and hasattr(a, "cpu"):
        a = a.detach().cpu().numpy()
    # NumPy array (or anything exposing .ravel().tolist())
    if hasattr(a, "ravel") and hasattr(a, "tolist"):
        return [float(x) for x in a.ravel().tolist()]

    def _flat(x: Any):
        if isinstance(x, (list, tuple)):
            for e in x:
                yield from _flat(e)
        else:
            yield float(x)

    return list(_flat(a))


def _json_safe(vals: list[float]) -> list:
    """Map non-finite floats to the CLI's string tokens ("nan"/"inf"/"-inf"). Standard JSON has no NaN/Infinity
    literal, and Python's json emits bare `NaN`/`Infinity` which the CLI (strict JSON) rejects; the CLI's array
    parser accepts these tokens instead."""
    out: list = []
    for v in vals:
        if v != v:                       # NaN
            out.append("nan")
        elif v == float("inf"):
            out.append("inf")
        elif v == float("-inf"):
            out.append("-inf")
        else:
            out.append(v)
    return out


def verify(
    reference: Any,
    candidate: Any,
    tolerance: str = "ulp:1",
    *,
    binary: str = "semanticcompute-parity",
    as_json: bool = False,
    limit: int | None = None,
) -> dict:
    """
    Compare `reference` vs `candidate` under `tolerance` (`exact` | `ulp:N` | `absrel:ABS,REL` | `default`).

    Returns a dict: {agree, diverged, exit_code, report, stderr}. When `as_json=True`, `report` is the CLI's
    machine-readable JSON string (pass it to json.loads). `limit` caps how many per-element mismatches the JSON
    carries (the CLI default is small); pass `limit=len(reference)` when you need the *complete* mismatch list
    (e.g. to render a per-element map). Raises ValueError on a length mismatch, FileNotFoundError if not found.
    """
    ref = _to_floats(reference)
    cand = _to_floats(candidate)
    if len(ref) != len(cand):
        raise ValueError(f"length mismatch: reference has {len(ref)} elements, candidate has {len(cand)}")

    exe = shutil.which(binary) or binary
    args = [exe, "--tolerance", tolerance]
    if as_json:
        args.append("--json")
    if limit is not None:
        args += ["--limit", str(limit)]

    payload = json.dumps({"reference": _json_safe(ref), "candidate": _json_safe(cand)})
    proc = subprocess.run(args, input=payload, text=True, capture_output=True)
    return {
        "agree": proc.returncode == 0,
        "diverged": proc.returncode == 1,
        "exit_code": proc.returncode,
        "report": proc.stdout,
        "stderr": proc.stderr,
    }


if __name__ == "__main__":
    # Tiny self-check with plain lists (no NumPy needed): index 1 diverges under an exact tolerance.
    r = verify([1.0, 2.0, 3.0], [1.0, 2.5, 3.0], tolerance="exact")
    print(f"agree={r['agree']} exit={r['exit_code']}")
    print(r["report"] or r["stderr"])
