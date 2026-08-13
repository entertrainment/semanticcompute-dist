# How SemanticCompute verifies — and why you can trust the binary

The source is closed, but a verification tool has to *earn* trust. Here is exactly what it
checks, how, and how you can confirm it yourself without seeing the code.

## What it actually does

1. **Parity, under a tolerance you state.** It lowers one typed IR to Metal, portable C, and
   WGSL/WebGPU, runs each against a deterministic CPU reference, and reports whether they agree
   under an **explicit** policy you choose: `exact` (bit-identical), `default` (abs 1e-6 or rel
   1e-5), or scale-free `ulp(n)`. Nothing is "close enough" by vibe — the bound is named.
2. **Accuracy, where a higher-precision reference exists.** Parity is necessary but not
   sufficient: two backends can agree on the same wrong answer. Where a computation ships a
   `Double` ground truth, the same comparator reports the *accuracy* — max abs/rel error, RMSE,
   worst ULP — of the Float result against the truth.
3. **Cause, when it diverges.** A heuristic classifier suggests *why* (FMA/rounding drift,
   denormal flush, NaN generation, ±∞ overflow/sign-flip/collapse). These are **leads, not
   proofs** — stated as such, everywhere.

## How you confirm it yourself — no source required

- **You supply both sides.** The tool never invents your answer — you feed it *your* reference
  and *your* candidate. The verdict is about your data, checkable against your own expectations.
- **The tolerance is explicit and reproducible.** Same inputs + same stated policy → same
  verdict, every time (exit codes 0/1/2 for CI). Put it in an audit trail.
- **The failure lab is runnable.** `--zoo` ships the canonical silent CPU↔GPU divergences
  (FMA contraction, denormal flush, NaN, overflow, naive-vs-compensated sum…). Run any specimen
  and reproduce the exact divergence the tool claims to catch — a self-test you can execute.
- **`--zoo export`** emits the canonical per-specimen / per-tolerance table as JSON, so the
  demo and the shipped doctor cannot diverge (the published table is generated from the code
  that runs).
- **Source audit under NDA.** Serious evaluators / design partners can review the reference
  implementations directly under a mutual NDA, or via source escrow.

## What it is *not* (stated plainly)

- Not a certification or regulatory approval — it produces reproducible **evidence**, it does
  not confer compliance.
- Not a fast GPU framework — verification is the product; a first-party stack is faster.
- Not a general oracle — only computations that ship a ground truth have a tested *accuracy*
  claim; the rest is cross-backend parity (agreement), which is a different, weaker guarantee.
- Accuracy is certified to **Float** tolerance (the candidate is Float32), and a "ground truth"
  is a higher-precision reference, not infinite precision.

*Pre-adoption, single author. The honesty is the point — if any of the above is ever untrue,
it's a bug, and the runnable failure lab is there so you don't have to take my word for it.*
