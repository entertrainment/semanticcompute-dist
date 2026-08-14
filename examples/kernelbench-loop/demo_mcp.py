#!/usr/bin/env python3
"""
KernelBench agent-loop variant — driven by the semanticcompute-mcp server's STRUCTURED output.

Same softmax scenario as demo.py, but instead of the CLI + prose, this speaks MCP (JSON-RPC over stdio) to
`semanticcompute-mcp` and reads `structuredContent` — the typed diagnosis an agent branches on directly. It
calls `sc_diagnose_divergence` to get `{causeHistogram, diagnoses[...]}`, decides the fix from the cause, then
re-verifies via `sc_check_parity`'s `{compatible}` field. No prose parsing, no GPU, no CUDA backend — this is
the closed loop as an MCP workflow, the shape KernelBench / SOL-ExecBench are moving toward.

Run:
    SC_MCP=/path/to/semanticcompute-mcp  python3 examples/kernelbench-loop/demo_mcp.py
(omit SC_MCP if `semanticcompute-mcp` is on PATH.)
"""

import json
import math
import os
import subprocess
import sys

MCP = os.environ.get("SC_MCP", "semanticcompute-mcp")


class MCPClient:
    """A minimal stdlib MCP stdio client: newline-delimited JSON-RPC 2.0."""

    def __init__(self, binary):
        self.p = subprocess.Popen(
            [binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1
        )
        self._id = 0
        self._rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "kernelbench-demo", "version": "1"}})

    def _rpc(self, method, params=None):
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            msg["params"] = params
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()
        while True:  # skip any message whose id doesn't match (this server sends none, but be safe)
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed the connection")
            obj = json.loads(line)
            if obj.get("id") == self._id:
                if "error" in obj:
                    raise RuntimeError(f"MCP error: {obj['error']}")
                return obj.get("result", {})

    def call(self, name, arguments):
        """Call a tool; return its structuredContent (typed result)."""
        return self._rpc("tools/call", {"name": name, "arguments": arguments}).get("structuredContent", {})

    def close(self):
        try:
            self.p.stdin.close()
            self.p.terminate()
        except Exception:
            pass


# ---- Same KernelBench task as demo.py: softmax; the naive 'generated kernel' overflows exp(). ----
LOGITS = [700.0 + i for i in range(24)]


def softmax_reference(x):
    m = max(x)
    e = [math.exp(v - m) for v in x]
    s = sum(e)
    return [v / s for v in e]


def _exp_hw(v):
    try:
        return math.exp(v)
    except OverflowError:
        return math.inf


def generated_v1(x):
    e = [_exp_hw(v) for v in x]
    s = sum(e)
    return [v / s for v in e]


def generated_v2(x):
    return softmax_reference(x)


def json_safe(vals):
    """Non-finite -> the CLI/MCP string tokens (same as sc_verify)."""
    out = []
    for v in vals:
        if v != v:
            out.append("nan")
        elif v == float("inf"):
            out.append("inf")
        elif v == float("-inf"):
            out.append("-inf")
        else:
            out.append(v)
    return out


OVERFLOW_CAUSES = {"nanGeneration", "overflowToPositiveInfinity", "overflowToNegativeInfinity", "infinityCollapse"}


def main():
    mcp = MCPClient(MCP)
    print("KernelBench agent loop over semanticcompute-mcp (structured output, no CUDA backend needed).")

    ref = softmax_reference(LOGITS)
    cand = generated_v1(LOGITS)

    # 1) Diagnose via MCP — read the TYPED result, not prose.
    diag = mcp.call("sc_diagnose_divergence", {"reference": json_safe(ref), "candidate": json_safe(cand)})
    hist = diag.get("causeHistogram", {})
    print(f"\n[diagnose] diverged={diag.get('divergedElementCount')}/{diag.get('comparedElementCount')}  causeHistogram={json.dumps(hist)}")

    # 2) Agent decision — branch on the structured cause, not a string.
    if set(hist) & OVERFLOW_CAUSES:
        decision = "exp() overflow / NaN in the softmax → apply the max-shift"
    else:
        decision = "numeric divergence → recompute the reduction stably"
    print(f"[decide]   {decision}")
    fixed = generated_v2(LOGITS)

    # 3) Re-verify via MCP — branch on the structured `compatible` boolean.
    chk = mcp.call("sc_check_parity", {"reference": json_safe(ref), "candidate": json_safe(fixed), "tolerance": "default"})
    ok = bool(chk.get("compatible"))
    print(f"[verify]   compatible={ok}  (maxAbsoluteError={chk.get('maxAbsoluteError')})")

    mcp.close()
    print("\n--- loop ---")
    if (set(hist) & OVERFLOW_CAUSES) and ok:
        print("CLOSED: structured diagnosis → agent decision → re-verify PASS. All from typed MCP fields.")
        sys.exit(0)
    print("UNEXPECTED: the demo did not close as designed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
