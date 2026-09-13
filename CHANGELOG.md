# Changelog

All notable changes to SemanticCompute are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows semantic versioning
(see `SLVersion` and `RELEASING.md`). The **top `## [x.y.z]` heading must equal `SLVersion.string`** — a
governance test (`GovernanceGateTests`) and the CI doc-sync step both enforce it, so version notes can never
ship out of step with the code.

## [1.22.1] — 2026-09-13

### Changed

- **The public distribution is complete and commit-identifiable again.** Tag CI now runs natively on Linux
  x86-64 and AArch64, stamps the exact source commit into both MCP and parity binaries after the source-integrity
  suite, smoke-tests the failure lab, verifies archive payload architecture, and publishes the same twelve-asset
  matrix as 1.20.0. The macOS products remain universal, Developer-ID signed and notarised. Publication refuses
  a missing Linux archive, notice, SBOM, CUDA evidence file or checksum manifest instead of creating a plausible
  partial release.
- **The public landing page and distribution documentation advance with the product.** The GitHub Pages source
  had stopped at the 1.13.0 landing commit even though the private source document was current. It now presents
  the full 1.22 surface: Imager's complete-MSL texture validator, executable semantic texture kernels, FDN late
  reverb, the adversarial stress lab and all twelve structured-data/CBOR-LD families. The historical 1.13 badge no
  longer reads as the product version.

### Fixed

- **The 1.22.0 public cut contained only the three macOS deliverables.** Linux x86-64 and AArch64 MCP/parity
  archives, `NOTICE`, the CycloneDX SBOM, CUDA compile/parity evidence and `SHA256SUMS.txt` were absent. The
  release helper now collects the successful tag-CI archives, checks every required byte-bearing asset and uses
  the detailed versioned release note for both release creation and repair.
- **The parity CLI now reports its embedded source commit.** `semanticcompute-parity --version` prints
  `SLVersion.buildCommit` alongside the semantic version and licence marker, so release automation and users can
  verify the exact build without starting an MCP client.

## [1.22.0] — 2026-09-12

### Added

- **Structured-data execution lane and twelve CBOR-LD support families.** Added a bounded flat document ABI
  (`SLStructuredValue` to fixed-width nodes, child indices, and byte pool), exact byte/UInt32 parity in the doctor,
  batched SHA-256, byte diff, CBOR structural scan, UInt scan/compaction, byte histogram/entropy, canonical key
  ordering, UTF-8 validation, Base58/multibase, unsigned varint, and frozen table probes. Whole-document CBOR-LD
  preparation resolves async contexts on the host, applies inherited term maps, flattens recursively under
  explicit limits, performs an exact output-allocation pass, and writes canonical RFC 8949 CBOR. CDDL parsing,
  AST construction, recursive validation, regex controls, and path diagnostics remain CPU reference work;
  supported root constraints compile to a bounded exact-integer validation VM for batch execution. A release
  benchmark compares the same flat instruction stream on CPU and Metal with a dead-code-elimination barrier.
  See `STRUCTURED_DATA.md` and `CBORLD_SWIFT_PACKAGE_AGENT_NOTE.md`.

## [1.21.1] — 2026-09-12

### Fixed
- **The BatchedDTFT parity contract now states the error actually measured across Foundation and Metal
  transcendental implementations.** The 64-tap, 256-frequency CI fixture reached a 2.78e-5 maximum difference;
  the former package-default 1e-6/1e-5 bar and “≤1 ULP” rationale described only FMA contraction and ignored
  `sin`/`cos` approximation drift. The family now uses an explicit 5e-5 absolute/relative contract with the
  measured result and both causes in its rationale. The package-wide default tolerance is unchanged.
- **The full Swift 6.2 Linux test target compiles reliably.** Four deterministic test-data expressions in the
  Constant-Q, Conv3D/transposed-Conv3D, and RLS suites are split into typed intermediate operations, avoiding
  compiler type-check timeouts on the official `swift:6.2` runner without changing their inputs or assertions.

## [1.21.0] — 2026-09-12

### Added
- **External Metal RGBA texture validation for complete consumer-owned shaders.** The additive Swift API
  `SLExternalMSLTextureValidator` and MCP tool `sc_validate_metal_texture` accept complete MSL, raw buffer bindings,
  an output texture description, and an independently supplied CPU reference. They compile, dispatch, read back
  `rgba16Float` or `rgba32Float`, and compare row-major RGBA channels through `SLCompatibilityDoctor`. Preflight,
  compilation, dispatch, readback, and parity each return machine-readable `executed` / `skipped` / `unavailable` /
  `failed` status with a reason. Missing Metal is an unavailable result, and a compile-only/runtime-only observation
  cannot become a pixel-parity claim. This is a validation bridge for bodies such as Imager's procedural phase-scope
  shaders; it does not claim arbitrary MSL is represented by the semantic IR. The MCP surface remains Float32 with
  explicit reference-narrowing evidence; `sc_check_parity` retains Float32/Float64 discovery and full-Double doctor mode.
  `sc_version.features` advertises `externalMSLTextureValidation` as a string identifier, preserving exhaustive
  switches over the stable public `SLCapability` enum.
- FDN late-reverb family: configurable Householder feedback network, per-line decay gains, one-pole
  damping, wet/dry mix, and explicit state across blocks. Includes a deterministic CPU reference,
  validated semantic IR, derived read/write contract, generic Metal lowering, and audio/state parity tests.
- **Generic Metal lowering and runtime dispatch for texture-writing pointwise2D kernels.** A legal semantic
  `SLKernel` using `texture2D<Float4>` read/write nodes now compiles through the same optimisation front door to
  executable `texture2d<float>` MSL. Texture indices are preserved, Metal's texture argument namespace is
  modelled in `SLBackendBinding`, and `MetalRuntimeAdapter` binds caller-owned `MTLTexture` resources. Dispatch
  derives from the writable texture's intrinsic extent and rejects mismatched texture shapes. The existing CPU
  texture executor and an exact CPU↔Metal passthrough test close the parity loop. A contract alone still does not
  invent computation: the `SLKernel.body` is the executable source and its derived contract supplies access/effect
  facts. The supported subset is pointwise2D Float4 read/write; samplers, filtered coordinates, other texture
  dimensions/formats, and non-Metal texture backends remain explicit gaps.
- **Recursive stress lab** (`Tests/SemanticComputeTests/StressLab`, driver `Tools/stress.sh`, doc `STRESS_LAB.md`) —
  an opt-in (`SC_STRESS=quick|full`) sweep of the WHOLE family library rather than one family's fixture. Four
  tiers: (A) every catalogued lowering × an adversarial shape ladder — binding table audited against the MSL
  signature, dispatch geometry, real Metal compile, emission determinism, failing shapes bisected; (B) CPU
  reference vs Metal under every `SLInputBattery` hazard × shape for the families with an execution adapter,
  divergences shrunk (ddmin) to the minimal poisoned elements and diagnosed by `SLDivergenceDoctor`, with a
  flush-to-zero re-check that names platform FTZ as the cause when it is; (C) random well-typed `SLKernel` IR
  through legality → optimiser → Metal + C → differential execution, failing kernels shrunk; (D) catalogue ↔
  usage guide ↔ symbol index ↔ lab-coverage integrity, reporting what the lab does NOT cover. Reports land in
  `stress-reports/` (gitignored). The ordinary `swift test` is unaffected (the suite is skipped unless enabled).

### Changed
- **The 1.21 texture path preserves the complete 1.20 public API.** Texture-aware dispatch is an overload, the
  original buffer-only `dispatch` / `dispatchBatch` methods and `SLBackendProgram` initializer remain available,
  and texture validation uses additive error types. Backend bindings reuse the existing semantic `SLBinding.Kind`
  texture case rather than adding a case to `SLBackendBinding.Kind`. `swift package
  diagnose-api-breaking-changes v1.20.0` reports no breaking changes.
- **`MetalRuntimeAdapter`'s comment said `mathMode = .safe` forbids fused multiply-add. Measured, it only SCOPES it** —
  `out = a*b + c` fused on 14,269 of 65,536 random inputs, `float p = a*b; out = p + c;` on none: ISO C's `FP_CONTRACT`
  rule, which MSL inherits. Several families inherited the false premise as a bit-exactness claim. `BACKENDS.md` gains a
  "Measured backend facts" section: contraction scope, the toward-zero `Float.pi`, the GPU's subnormal-equals-zero compare,
  the `atan2` collapse threshold, encoder lifetime on error, and why an undispatchable geometry is never catchable.
- The stress lab sweeps the Kaiser window at β ∈ {0, 2, 20, 100} in tiers A and B, and its FFT butterfly entry now states
  the `n ≥ 2` contract instead of logging `n = 1` as an informational rejection.

### Known validation gaps
- The ordinary 1.21 macOS suite and supported family fixtures are green, but the opt-in adversarial stress lab is
  intentionally still red. The 2026-09-12 quick run found 394 tier-B and 3 tier-C criticals, concentrated in
  intermediate-denormal behaviour, extreme-value Sobel/matmul overflow, crossfade drift, and three Metal-vs-C IR
  cases. These findings remain visible in `STRESS_LAB.md`; they have not been hidden by weaker tolerances.
- Linux source and artifact validation is pending a local Docker disk-image migration. The CUDA evidence committed
  in the repository records an older source revision, so it is historical hardware evidence rather than a fresh
  1.21 NVIDIA run.

### Fixed
- **Stress-lab continuation (2026-09-10): VOI LUT no longer converts an unbounded Float to Int.** NaN offsets
  select the first LUT entry; infinities and out-of-range offsets select the corresponding edge, on CPU and Metal.
  The reference requires a nonempty LUT; a zero runtime LUT length performs no GPU reads or writes. Existing
  in-range rounding is unchanged. CPU fixtures, explicit Metal parity rows, and a DICOM VOI stress adapter cover it.
- **The hand-written quantisation lowering now uses `fmin(fmax(q, qMin), qMax)`**, matching the already-pinned
  reference and generic emitter for inverted and NaN bounds. Both lowerings are checked against an explicit truth table.
- **The stress driver preserves failures rather than inferring success from old reports.** Fresh per-run/per-case
  directories, actual build/test exit codes, mandatory reports, executable isolation inventories, exact case selection,
  empty-filter rejection, and hexadecimal seed parsing replace false-green paths. Twelve subprocess-fixture scenarios
  cover build/test failures, a crash followed by continued execution, stale reports, missing reports and invalid arguments.
- **Two Metal-only test references are now compile-guarded**, leaving C execution available to the IR fuzzer without
  Metal. The CI test steps explicitly use Bash so a failing `swift test` cannot be hidden by the logging pipeline.
- **One IR operation, four NaN answers: `clamp`, `min` and `max` disagreed across the backends.** The stress
  lab's IR fuzzer shrank two independent failing kernels to a single line — `out[idx] = clamp(in0[idx], -1, 1)`
  — where the C backend returned NaN and Metal returned the low bound. Tracing it found five implementations of
  the ordering intrinsics that had never been reconciled: the C emitter's comparison chains propagate NaN, MSL's
  `min`/`max` are documented UNDEFINED for NaN, WGSL's are indeterminate, and the CPU interpreter's
  `Swift.max(lo, Swift.min(v, hi))` returns the low bound only by accident of Swift's tie-break — reverse the
  nesting, as two shipping families did, and the same three arguments give NaN. The package had already decided
  this question twice with tests (`PointwiseBinaryOp.minimum`/`.maximum` and `CPUReferenceExecution.Reduction`
  both skip NaN, lowering to `fmin`/`fmax`), so the generic IR is now pinned to the same IEEE-754 minNum/maxNum
  contract and it is written down in `SLIntrinsics` rather than delegated to whatever the driver does. Two
  shipping families were already wrong against their OWN kernels and are fixed with it: `PointwiseUnaryOp
  .saturate` returned NaN where its MSL `saturate` returns 0, and `QuantiseTransitionReference` returned NaN
  where its MSL `clamp` floors to `qMin` (an int8/uint8 fake-quant golden reference — not the medical-imaging
  display lane, as this entry first said). Review then found the first version of that fix still wrong: a NaN shortcut in
  front of `Swift.min`/`Swift.max` disagreed with the kernel whenever the bounds were inverted or a bound was NaN, so the
  reference is now the kernel's `fmin(fmax(..))` composition. Two things the NaN rule does not settle are now stated rather
  than inferred: INVERTED bounds give `hi` on every path — a deliberate change for finite input too, since the old
  interpreter gave `lo`, and the one that matches C and Metal — and the SIGN of a zero result on a ±0 tie is not pinned
  (IEEE-754 minNum leaves it open). Metal now spells float `clamp` as `fmin(fmax(..))`, because MSL leaves its builtin
  undefined for `lo > hi`, and float vectors follow the scalar rule. Only the C emitter's source text had been guarded by
  the ordinary suite; the interpreter, constant folder, Metal and WGSL routing are now pinned there too.
- **`ComplexPolar.phase` returned NaN or a sign-flipped angle on the GPU across the whole degenerate atan2
  quadrant.** Metal's `atan2` is evaluated through a division, so 0/0 and inf/inf come back NaN where IEEE-754
  defines ±0, ±pi, ±pi/4 and ±3pi/4, and a signed-zero or infinite denominator makes the result take the sign of
  the QUOTIENT rather than of `im`. The lowering now reconstructs all nine IEEE rows itself and only pairs where
  both operands are finite and non-zero reach the builtin, so no ordinary bin moves. `magnitudeDB` had the same
  root cause one level up — its reference floored with `Swift.max` (propagates NaN) while its kernel used
  `fmax` (skips it) — and now floors to the same value as its kernel. Stress-lab criticals for this family: 54 → 0. The first version of the row table was
  one ULP off on every ±π row — it used `M_PI_F` (nearest) where libm returns π rounded toward zero — and the regression
  test, comparing at `.defaultFloat`, could not see it; the ±π rows now use `0x40490FDA` and degenerate rows are compared by
  bit pattern. Two corrections to the header: the builtin's large-magnitude collapse begins near FLT_MAX/4, not ~1e19; and
  inside the subnormal regime the reconstruction now returns a finite zero-row angle where the builtin returned NaN, because
  the GPU compares a flushed subnormal equal to 0.
- **`Kuramoto` and `Reservoir` emitted undispatchable kernels above 1024 elements.** Both set
  `threadgroupSize = (N,1,1)` with no upper bound, so above `maxTotalThreadsPerThreadgroup` the programme
  compiled but could never run correctly — and that is never a catchable error: without Metal API validation
  (every CLI and release build) the dispatch completes and silently writes nothing, and with validation it asserts. (This
  entry first called it "a validation abort", which is true only with validation on.) The runtimes were already capped
  at 1024 and Kuramoto's GPU band was disabled outright, so the exposure was direct callers of the public lowerings. N
  genuinely has to fit one threadgroup — the kernels share threadgroup memory, and splitting N corrupts every output — so
  rejection, not a smaller threadgroup, is the right fix. Kuramoto at N = 4097 also
  exceeded the 32768-byte threadgroup-memory limit (2 × 4 × 4097 = 32776) and failed to compile outright. Both
  now declare the ceiling (`KuramotoLowering.maxOscillators`, `ReservoirLowering.maxUnits`) and reject above it
  at construction; the runtime band gates derive from those constants — `gpuMinOsc` included, so raising the ceiling cannot silently
  switch on an unbenchmarked band. The
  unbounded CPU references are untouched and remain the supported path above the ceiling.
- **`FFTLowering.butterflyStageMSL(n: 1)` emitted a zero-sized grid.** `gridShape` was `(0,1,1)` — a dispatch that silently does nothing without Metal API validation and asserts with it — because a length-1 radix-2 transform has log2(1) = 0 butterfly stages and
  an empty twiddle table. It is now rejected with a typed error; the identity halves of a length-1 transform
  stay expressible through `bitReversalMSL` and `scaleMSL`.
- **Every symmetric window returned NaN at length 1 while its kernel returned a number.** `hann`, `hamming` and
  `blackman` divide by `length - 1`, which is zero at length 1: the reference computed 0/0 → NaN while the GPU
  returned 0.5 / 0.54 / 0.42, because Metal's `cos` does not propagate that NaN. Two different wrong answers to
  a question nobody had answered. Both sides now return the conventional `w[0] = 1` (NumPy's
  `hanning`/`hamming`/`blackman` and SciPy's `_len_guards`), off a single shared predicate so they cannot drift.
  `hannPeriodic` (÷ N) and `sineTaper` (÷ N + 1) have no zero denominator and keep their exact formula values.
  Periodic Hann's 0 matches vDSP, which that op exists to match, while SciPy, PyTorch and MATLAB return 1 — a genuine
  convention split, now pinned by test along with the predicate itself. `kaiser` reaches 1 by construction.
- **`FamilySymbolIndex` was blind to every symbol declared in an extension in another file.** The scanner only
  opened a group on `public enum X…`, so the 24 `public extension` sites — and their implicitly-public
  `static func` members — were dropped entirely: `Pointwise{1,2,3}DLowering.unaryOpMSL`/`binaryOpMSL`/`lerpMSL`,
  `ConnectedComponentsLowering.gradientPropagateMSL`, and every contract in `NewFamilyContracts.swift`. That is
  why six catalogue families claimed `hasContract: true` with no recorded contract, and why `sc_list_families`
  could not show those lowerings. The scanner now attributes extension members to the extended type regardless
  of file and accumulates `sourceFiles` instead of freezing them at first sight, recovering 33 selectors with none removed — 27 from public
  extensions and 6 explicitly `public` helpers in a non-public extension of `NormalisationReference`, which Swift's access
  rules make public. Review found the scanner still blind to attribute-prefixed or conformance-declaring extensions and to
  `@inline(__always)`/`nonisolated` members (two more selectors recovered: `LevelSetReinitReference.sgn`,
  `PeronaMalikReference.conductance`), and attributing a nested type's members to the enclosing type; members are now
  recorded only at depth 1. `FamilySymbolIndexTests` gained an actual regenerator
  (`SC_UPDATE_SYMBOL_INDEX=1 swift test --filter FamilySymbolIndexTests`) — the index said "regenerate rather
  than hand-edit" but no generator existed, which is how it went stale.

- **`Resize2D.linear` and `Resize3D.linear` disagreed with their own reference by hundreds of ULP on ordinary input — the
  stress lab's one benign-input P0.** The first hypothesis, a different weight form or half-pixel mapping, was ruled out by
  reading: the two sides were textually identical. Metal was fusing `x*y + z` under `mathMode = .safe` — the mapping
  `(o+0.5)·s − 0.5` and the LEFT product of every lerp — while Swift fuses nothing. A reference fusing exactly those sites
  reproduced the shipped kernel bit-for-bit, against 27,098 of 65,535 elements and a worst 30,858 ULP for the unfused one;
  cancellation between opposite-signed neighbours is what turned 1 ULP into hundreds, and a 1-ULP-different `fx` is what
  turned the reference's `inf·0 = NaN` into the kernel's `inf·tiny = inf`. Both sides now spell `fma`/`addingProduct`.
  Bit-exact on ordinary and inf/NaN input; the lab's Resize adapters went from 42 criticals to 0 (896 of 896 cases).
- **Box blurs ran with taps that were not their reference's, and every 3×3/3×3×3 stencil accumulation could fuse.** The
  shared stencil builders rendered tap literals with `%g` — six significant digits — so `1/9` and `1/27` reached the kernel
  as `0.111111` and `0.037037`, and a field of 1 blurred to 0.999999. Literals are now round-trip, and each `x * tap` is its
  own statement. Every stencil op is bit-exact against its reference, including the 1×1×1 cancellation case the lab had
  flagged as a sign flip (tier B for stencils: 672 of 672 cases).
- **`Crossfade` did not end on pure `b`, and its two backends disagreed about θ itself.** Swift's `Float.pi` is rounded
  toward zero (`0x40490FDA`) while the kernel's decimal literal parses to the nearest float (`0x40490FDB`), so every sample
  ran a ULP of θ apart; at the last sample `cos(θ)` was +7.55e-8 on the CPU and −4.37e-8 on Metal, which is how an infinite
  `a` came out +∞ and −∞. The reference now uses the nearest float, and both endpoints are pinned — `cos(π/2)` is not 0 in
  Float, and `b·sin(0)` is NaN for an infinite `b`.
- **Seven more family references propagated NaN where their kernels skip it, and one trapped.** The same
  `Swift.min(Swift.max(v, lo), hi)` idiom sat in SpectrogramDisplay (with the identical `magnitudeDB` floor defect),
  Wong–Wang, ForceDirectedLayout, SpringElectricalLayout, PolarResample, SpatialGrid and MoireGrating; in
  `SpatialGridReference` a NaN coordinate reached `Int(_:)` and crashed the process. All ten references now share
  `SLOrdering`, the one CPU implementation of the ordering contract, which the interpreter and constant folder use too.
- **A missing binding killed the process instead of throwing.** `MetalRuntimeAdapter.dispatch` and `dispatchBatch` threw
  out of the binding loop with a live encoder, which Metal answers with a `Command encoder released without endEncoding`
  assertion — signal 6 for a whole test run. Bindings are now resolved before any encoder exists.
- **Seven families claimed bit-exact CPU↔GPU agreement "because `mathMode = .safe` disables FMA contraction" — and the
  premise was false.** An audit of every such claim found single-expression multiply-adds against unfused references in
  the DICOM value transforms, Fisher–KPP, Pennes bioheat, Poisson relaxation, the ODE bank, Wong–Wang and the FFT
  butterflies (the 1D stage and the 3D line FFT). Most of their tests compared at `.defaultFloat`, which absorbed the
  drift. DICOM rescale's `.exact` test passed only because it used slope 1, which makes every product exact: with a
  non-dyadic slope of 0.1 and intercept −1, a stored value of 10 rescaled to 0 on the CPU and 1.49e-8 on the GPU. Every
  float product in those kernels is now its own statement, in the reference's association, so `.safe` has nothing to
  fuse, and all seven are tested at `.exact` on fixtures chosen so contraction would be visible. DICOM gains non-dyadic
  slopes and a fractional window, and window/level moves from the default tolerance to `.exact`. Fisher–KPP's ρ and
  Pennes's α moved off dyadic values that had made their products exact. The FFT gains random complex input — the existing
  `.exact` test used an integer ramp with a zero imaginary part. Spring-electrical layout was split the same way but keeps
  its tolerance, because it calls `sqrt`. Marching cubes and the nearest-feature transform were audited and are genuinely
  safe, though not for the reasons their comments gave; those are corrected.
- **`DivergenceZoo` gains specimen 15, `clamp(NaN, lo, hi)`**, so `sc_zoo` and `--zoo all` now count fifteen.

## [1.20.0] — 2026-09-09

### Added
- **The FIR design lane — `Equiripple FIR design (Parks–McClellan/Remez exchange, Type I/II)` and
  `Windowed-sinc FIR design`, plus a Kaiser window and the Bessel I₀ underneath it (168 → 170
  families).** Requested by the FIRFilters/RemezEngine consumer, whose survey found zero hits for
  remez, chebyshev, equiripple, minimax or alternation anywhere in the catalogue, and zero for
  `bessel` — while their own engine reported `delta = 8.9e-16` on a filter measured **+22.6 dB off
  spec**. That is the shape of the whole lane: a designer cannot check itself.
  - `RemezReference.design` is the optimal designer — barycentric δ in closed form, a barycentric
    Lagrange interpolant on a dense band grid, and an alternation set taken as the peak of every
    constant-sign run of the weighted error. **Fewer than r+2 alternations is REFUSED**, never padded
    out of the grid: padding is precisely how a tiny δ gets reported on a filter that misses its spec.
    Measured on a 61-tap lowpass: δ = 0.0014995 against realised band deviations of 0.0015113 and
    0.0015070, and a realised stopband of −56.44 dB against the −56.48 dB δ claims.
  - `RemezReference.amplitudeResponse` / `bandDeviations` are the EXTERNAL check, evaluated through
    `BatchedDTFTReference` at frequencies the caller chooses rather than the grid the design already
    agreed with itself about. `amplitudeResponse` also returns the imaginary residual, which is a free
    linear-phase assertion: measured 2.6e-6 worst on a 61-tap design.
  - A correction to the request as filed: the report proposed routing the Chebyshev system through
    the Householder-QR family to avoid squaring a cosine-Vandermonde's condition number. Right
    instinct, wrong step — the classical method never forms that system, so there is no matrix to
    condition badly and QR would be a step backwards.
  - `WindowedSincReference` is the predictable designer, host-only like the RRC family. **Kaiser's own
    order formula is an estimate and measurably undershoots** — 59.3 dB for a 60 dB ask, 79.9 for 80 —
    so `kaiserDesignMeetingSpec` designs, MEASURES, and grows the filter until the spec is actually
    met (60 dB → 77 taps, 80 dB → 111, 100 dB → 139) or refuses. The raw formula is left as Kaiser's
    formula rather than quietly fudged.
  - `WindowOp.kaiser` and `BesselReference`. I₀ ships in two implementations that deliberately
    disagree: A&S 9.8.1/9.8.2 in Float is the PARITY SURFACE, and `i0Exact` is the ascending series in
    Double, run to convergence — the oracle, and the direct fix for a caller whose own `besseli0`
    truncated that series at three terms. Measured: A&S's published bounds hold comfortably in exact
    arithmetic (3.3e-8 and 8.4e-8) but the Float evaluation is ~8× worse (2.77e-7, 2.84e-7), so what
    ships is dominated by the EVALUATION, not the approximation. The Kaiser ratio is formed scaled,
    `(i0e(a)/i0e(β))·e^{a−β}`, because I₀(β) leaves Float's range near β ≈ 91.
  - Both designers refuse an even-length highpass or bandstop: Type II carries a forced zero at
    Nyquist, so that filter does not exist and saying so beats returning one that misses its spec.
  - Equiripple against windowed-sinc at 61 taps, same transition: **−56.4 dB vs −36.7 dB**.

### Changed
- `Window generators` is renamed to include Kaiser, and **its `dpss`/`slepian` keywords are removed**.
  The `sineTaper` op is a Riedel–Sidorenko sine taper — related to the Slepian sequences, not one of
  them — but the old "DPSS-like" wording plus those keywords led a consumer surveying the catalogue to
  report DPSS as shipped. There is still no DPSS/Slepian window; the file now says so where it cannot
  be missed. The family also gains a `parityContract`, which it never had: measured worst-ULP and
  worst-absolute per op, and the two columns rank the ops in OPPOSITE orders — which is the argument
  for a combined absolute/relative bar over a scale-free ULP one, written down.
- `SuggestionAbstentionTests` **flips**. It asserted "SC ships FIR APPLY, not FIR design — the top hit
  must sit below the abstention floor rather than masquerade as an answer", and that was true. The
  lane closes the gap, so the gate now asserts the opposite and the flip is the evidence. A gate that
  encodes an absence gets flipped when the absence is filled, not deleted.
- `sc_detect_in_code` learns three shapes it was blind to: a named Remez/Parks–McClellan exchange, a
  windowed-sinc designer (requiring a band-spec term alongside the sinc, so a resampling kernel does
  not fire), and a hand-rolled Kaiser or Bessel I₀.

### Fixed
- **`HarmonicFreqEKF` walked its amplitude state negative and could never recover** — two defects
  compounding, both reported with measurements by an audio consumer activating the family on real
  material. (1) The measurement prediction was `log(|a| + eps)` while callers supply `log(amplitude)`,
  so a state that was EXACTLY consistent still carried a permanent innovation — at a = 1e-6 with
  eps = 1e-6 that is log(1e-6) − log(2e-6) = −0.693 every frame, against a Jacobian of 500,000.
  (2) The Jacobian was `1/(|a| + eps)`, always POSITIVE, where d(log|a|)/da = 1/a is NEGATIVE for
  a < 0 — so once (1) pushed the state below zero every correction pushed it further out. Measured by
  the consumer: |a| = 16.3 after one dropped frame, 37 over 40 frames, 30,044 over a four-minute
  track, surfacing downstream as a phantom partial that INVERTED per-partial amplitude ordering. The
  prediction now clamps the magnitude instead of offsetting it (a consistent state has exactly zero
  innovation) and the Jacobian carries `a`'s sign. Verified against the pre-fix code: the
  constant-amplitude fixture returned **−252.7** for a truth of 1e-6.
- **`HarmonicF0EKF` tracked f0 in linear Hz against a log2 measurement, and a single outlier killed
  the track permanently** — on clean input this works; on real polyphonic material the fused
  observation jumps (octave flips, competing sources) and one large negative innovation drove f0 ≤ 0.
  After that the clamped Jacobian 1/(eps·ln2) ≈ 1.4e6 makes the gain pp00·h/(h²·pp00 + r) → 1/h → 0,
  so the filter stops correcting and **never returns**: the consumer measured output positive in 0.2%
  of frames while 38.8% were confidently voiced, yielding a vocal at −15.4 dB SDR — worse than
  passing the mixture through untouched. The state is now log2(f0), which makes the measurement the
  IDENTITY (the observation is already log2(f0) — no linearisation at all), makes positivity
  structural via f0 = 2^L, and makes constant velocity mean a constant glissando rate in cents.
  Verified against the pre-fix code: the octave-flip fixture left only **40 of 120 frames positive**.
  - **PARAMETER SEMANTICS CHANGED**: `initVarF` is now the variance of log2(f0) in octaves² (default
    4 ≈ ±2 octaves at 1σ), `initVarV` is octaves/frame², `accelVar` is octaves/frame². `baseMeasVar`
    is unchanged — it always described the log2 observation, and the output is still f0 in Hz.
    Callers passing Hz-domain variances must retune.
- Both fixes are mirrored into the Metal lowerings, so CPU↔GPU parity holds on the corrected maths
  rather than on the old.
- **`MarchingCubesMesh.surface` returned a closed but INCONSISTENTLY WOUND mesh** — reported by a
  radiomics consumer verifying against the IBSI-1 digital phantom (divergence volume 437 mm³ against
  IBSI's 556 ± 4, while the AREA agreed at 386.31 vs 388 ± 3). Their diagnosis was holes; it was not.
  Closure was already perfect — every segment shared by exactly two triangles — and the fault was
  orientation: 158 directed edges per random-mask mesh had no opposite twin, so neighbouring facets
  disagreed about which side was out. **Area is unsigned and survives that untouched, which is exactly
  why it hid the fault**, and their per-triangle field-sampling re-orientation could not have fixed it:
  orientation consistency is a topological property of the adjacency graph, not a per-facet vote.
  `surface(...)` now propagates winding across shared edges and fixes each connected component's sign
  to outward; `enclosedVolume` is added for the divergence-theorem volume this unlocks. The sphere
  fixture went from 40% of its analytic volume to 99.6%.
  - **A second defect found while fixing the first, preserved in the header:** the first
    implementation welded vertices by quantised POSITION, which splits shared crossings that two cubes
    compute 1 ULP apart, fragments the adjacency graph and strands the propagation — that draft
    returned the 40% figure. Identity is now grid-edge PROVENANCE, which the record already carries and
    which the project's own metric tests had long since named "the geometric truth".
  - The header's WATERTIGHT claim is corrected to say what it means: closed is not oriented, and a
    closed mesh you cannot take a volume from is a trap when a header says watertight.

## [1.19.0] — 2026-09-02

### Added
- **Spectral correlation + coherence (the cyclostationary lane)** (167 → 168) — a PSD says "there
  is power at f"; only cyclostationary analysis says "there is a MODULATED signal with symbol rate
  α". SCF by cyclic-periodogram averaging over STFT frames (composes with the STFT family), with
  spectral coherence as the scale-free [0,1] surface. Pinned: α in EVEN integer bins (half-bin
  shifts refused, not interpolated away); α = 0 IS the averaged periodogram — the scale anchor that
  catches a mis-shift instantly; no wraparound; zero-power coherence is 0, never NaN. Measured on
  the fixture: BPSK's symbol-rate coherence 1.0 against 0.10 off-cycle and 0.19 for noise at the
  same α — the modulation-vs-noise discrimination the lane exists for.
- **The SDR lane** (163 → 167) — built for HackRF-class operations: ultrafast scanning, RX/TX, and
  full waveform analysis:
  - **Polyphase filterbank channeliser** — the ultrafast-scanning primitive: one pass splits a
    wideband block into N simultaneously-analysed channels (polyphase arms as the new kernel; the
    across-arms DFT composes with the FFT family). Forward-sign DFT pinned by a tone test — which
    caught this very family's first draft using the mirrored sign before it shipped. Startup
    transient reported by the plan. Measured 62 dB channel rejection with the shipped prototype.
  - **CFAR detection (CA + OS variants)** — per-cell adaptive floors from guard-skipped training
    cells. The variants ship together because their failures differ: one fixture pins BOTH that CA
    masks a weaker target inside a stronger one's training ring AND that OS at a stated rank detects
    it — the reason OS exists. The floor output is exactly peak picking's floor buffer:
    CFAR ∘ PeakPicking is the detect-then-refine chain, tested as a composition.
  - **Quadrature FM discriminator** — instantaneous frequency as the angle of x[i]·conj(x[i−1]),
    conjugate order pinned (the other order decodes inverted FSK bits from a system that "works"),
    amplitude immunity pinned, radians/sample with Hz left to the caller.
  - **Root-raised-cosine tap design** (host-only, apply via Batched FIR) — the zero-ISI matched
    cascade is the defining test; singular points use analytic limits; unit-energy normalisation and
    integer group delay stated. The truncation-limited residual ISI is stated in the test rather
    than hidden behind a lucky span.

## [1.18.0] — 2026-09-01

### Added
- **The suggestion abstention floor** — `sc_suggest_families` now labels its own confidence regime: a
  top hit below 40% query coverage returns `confidence: "low"` with an abstention-grade note, because
  "a confident wrong answer is indistinguishable from a confident right one, so a detector that
  guesses costs more than one that abstains" (the consumer who left a resampler unmapped for a week
  on a top-ranked nonsense hit at 30). The floor is honest about its limits — the same 28–36 band has
  held both nonsense and CORRECT top hits in the consumer's evidence, so below it the claim is "rank
  carries little signal here", never "this is wrong". The consumer's FIR-designer case is the pinned
  below-floor test (SC ships FIR apply, not FIR design; the honest answer is that no family covers it).
- **The landing page's live numbers are now gated** (`LandingNumbersSyncTests`) — family count in the
  stats strip, library headline, and the full kind-distribution bars are checked against the
  catalogue, killing the drift class found at the v1.15.0 cut the same way the README table gate
  killed its sibling. Runtime totals (tests/suites) stay hand-trued at cuts, deliberately: a gate
  that guesses is worse than no gate.

### Fixed
- **Two v1.17.0 float64 findings from the requesting consumer's verification, both accepted:**
  - **`precision` was absent from `sc_check_parity`'s declared JSON schema** — the runtime accepted
    and validated it, but a client discovering the tool by schema introspection (the normal MCP
    route) could not find it: "a fix that exists but is not reachable by the normal route", the
    consumer's third instance of that pattern and the argument that has moved every change in this
    thread. Declared, with the same scope wording as the runtime.
  - **The float64 path reported `maxAbsoluteError: 0` on a PASSING check** whose true observed
    maximum was 3.55e-15 — max-over-mismatched-only semantics, a divergence from the float32 doctor
    (which always reported the observed maximum over ALL elements) introduced with the float64 path
    itself. Same misreading as the original narrowing bug by a new route: a pass beside a zero error
    figure reads as bit-identity. The float64 path now mirrors float32 exactly, including the
    relative-error denominator; pinned by a passing-check-reports-true-max test.

## [1.17.0] — 2026-09-01

### Added
- **Doctor-level float64 comparison** — the DECIDED answer (2026-09-01) to the longest-standing
  consumer question, asked three times by the FIRFilters mapping session: every reference value in a
  Double-native package is a Double, and the float32 surface correctly refuses to compare bits it
  would discard, so none of their 20+ mappings could be parity-checked end to end. The decision:
  `SLCompatibilityDoctor.compareDoubleBuffers` judges two float64 buffers at FULL precision — bit
  identity under `exact`, Double bars, and `ulp(n)` counted in DOUBLE ULPs (`slDoubleULPDistance`) —
  while families and lowerings remain float32, a scope the result states in its own `precision`
  field rather than leaving to inference. `sc_check_parity` gains `precision: "float64"`; the
  float32 exact-refusal now names it as the first remedy; unknown precisions refuse per the house
  rule. The pinned defining case is the consumer's own: a 6.66e-16 difference — invisible to any
  float32 path — is seen, measured, and tolerable only under a knowingly-stated double bar.

## [1.16.0] — 2026-09-01

### Added
- **The tracking lane** (159 → 163) — the estimator consumer's full outstanding queue, built in one
  cycle with their own trap characterisations pinned as tests:
  - **Linear assignment (gated bipartite matching)** — three consumers hand-roll this shape. The
    OBJECTIVE is the family: maximise feasible pairs first, minimise cost second, with gating
    STRUCTURAL (forbidden = absent edge, never big-M, which only makes bad assignments expensive).
    Ships its own brute-force oracle whose lexicographic ordering forbids the zero-cost empty
    matching — the consumer's reference trap. A THIRD trap surfaced during construction and is
    preserved as a fixture: row-by-row shortest-path assignment steals contested columns under
    gating (max cardinality survives, min cost does not); the solver augments globally from every
    unmatched row, which the 60-trial brute-force cross-check now confirms. Host-only by design —
    the solve is sequential; the parallel work is the caller's cost matrix, which composes.
  - **Spectral peak picking** — floored local maxima with log-parabolic refinement. The floor is
    LOAD-BEARING (without it a tracker can never miss a detection and a dead track gets dragged by
    noise at shrinking covariance — the consumer's failure statement, kept); the plateau test is
    asymmetric so a flat top is one peak; an exact log-parabola's position is recovered to float
    precision, test-pinned. Finds WHICH frequencies to point Goertzel/BatchedDTFT at.
  - **Batched EKF predict (per-track transition)** — the narrowed remainder after the consumer's own
    correction (their glide model fits BatchedEKF as shipped). Same conventions verbatim, F becomes
    a per-track buffer; bit-exact agreement with BatchedEKF under a replicated F is a test.
  - **Phase unwrap (predictive + sequential)** — both forms because they fail DIFFERENTLY: a glitch
    corrupts one predictive output and every later sequential output, pinned side by side as facts
    of the forms. princarg round-half-to-even, shared with the complex-onset family.

## [1.15.0] — 2026-09-01

### Added
- **Savitzky–Golay smooth/derivative** (158 → 159) — batched, with POLYNOMIAL-CONSISTENT edges. The
  requested Hampel companion turned out to be half-shipped: the Hampel identifier has been in the
  catalogue since the robust lane, so the genuine gap was S–G itself. The consumer's own upgrade doc
  had correctly ruled the single-signal interior "Correlation with time-reversed taps — never a gap";
  what no family covered was the edges (a different weight row per boundary position — not a
  fixed-tap correlation) and the batch fused with them. Pinned: degree-≤p polynomials pass through
  EXACTLY including edges; a ramp's edge derivative is exact where the common reflection policy
  collapses it toward zero; d!/h^d scaling with h a real parameter; measured 1.85× peak retention vs
  a same-width boxcar. Robust smoothing = Hampel ∘ SavitzkyGolay by composition, no fused kernel.

### Fixed
- **`ResamplePolyphase`'s GPU kernel could overflow its position product** — `i·M` in 32-bit
  overflows once outCount·M exceeds 2³², i.e. a long file resampled at a large reduced M (a
  ten-minute render through the VoiceMorph pitch path's rational approximations is enough). Found
  while wiring the consumer estate; the CPU reference always used 64-bit positions, so the two sides
  were identical only until the file got long. The kernel now computes positions in `ulong`;
  parity re-verified (1.2e-6 maxAbs, unchanged).
- **The README family table had rotted to the point of misinformation** — a consumer diffing
  `sc_list_families` against it found 141 of 158 canonical family names absent (the table had 73 rows
  of mostly non-canonical shorthand). Regenerated mechanically from `KernelFamilyCatalogue.all` (158
  rows, canonical names, kind/dims/variants from code) and GATED: `ReadmeFamilyTableSyncTests` now
  requires every catalogue name to appear verbatim and the stated count to match — the same medicine
  as the symbol index and the landing-page zoo matrix. Reported by a consumer; the gate is the fix,
  the regeneration only the symptom relief.


## [1.14.0] — 2026-09-01

### Added
- **The audio-estate lane** (151 → 158): seven families from a file-level survey of the consumer audio
  estate (a 32k-line memo editor, a stem splitter, two AUv3s, a masker engine, a synth) — each traced to
  hand-rolled call sites or a consumer roadmap's explicit ask before being declared a gap:
  - **Batched LPC (Levinson–Durbin + all-pole envelope)** — the estate hand-rolls it FIVE times; the
    train↔infer conformance contract names LPC-24. Sign convention pinned by an AR(2) test that cannot
    pass negated; silence yields zeros not NaN; an unstable reflection coefficient freezes the recursion
    at the last stable order.
  - **Sobel 2D magnitude** — a consumer plan's top priority verbatim: its MPS onset detector was "the
    only unverified GPU path". Replicate borders stated and pinned (the convention that silently
    diverges between implementations).
  - **Polyphase windowed-sinc resample** — five linear-interpolation resamplers replaced by one with
    exact rational positions (no phase drift, pinned on 100k samples), per-position kernel normalisation
    (DC at unity), and 99.7 dB measured interior SNR at 44100→48000.
  - **True peak (BS.1770-4 method)** — the estate meters LUFS twice and inter-sample peaks nowhere. 4×
    oversampling via the SAME windowed-sinc kernel — one interpolator, two families — with the honesty
    note that the informative Annex 2 filter is not claimed. The fs/4-at-π/4 case (0.707 sample peak,
    1.0 true peak) is pinned.
  - **Batched attack/release envelope follower** — the recurrence rewritten across vocoder banks, the
    cochlear analyser, and a synth's carrier gate; previous-envelope branch choice, zero initial state,
    and the coefficient formula all pinned.
  - **Gammatone/ERB band energies** — roadmap-requested, with the requester's own −24 dB
    normalisation surprise as the cautionary tale: ERB(1 kHz) = 132.639 Hz asserted to the digit,
    ERB-rate spacing, Patterson's 1.019 factor, area normalisation an explicit option.
  - **Nearest-centroid assignment** — asked for independently by two consumers (DUET spatial
    clustering; drum-piece peeling). Lowest-index tie-break by construction; the update step is
    deliberately absent because assignments are labels and labels feed the fused labelwise scatter.

## [1.13.0] — 2026-09-01

### Added
- **The audio-analysis lane for percussion discrimination** (149 → 151), requested by a drum-classification
  consumer whose two independent models failed the same held-out kick/conga discrimination — traced to
  linear-frequency smearing below 100 Hz, not to either model:
  - **Constant-Q / Variable-Q spectrogram** — per-bin Q-matched window lengths on a log-frequency axis;
    the principled fix for the fixed-window STFT's single time-frequency tradeoff. γ = 0 is constant-Q
    BIT-EXACTLY (test-pinned); the `maxWindow` clamp is honest (clamped bins are reported and run at
    reduced Q rather than silently pretending). The binding-gap check is recorded in the header:
    `BatchedDTFT` (unframed, one length), `Goertzel`/`Chromagram` (framed, one shared length) and `STFT`
    all near-miss this shape. The marquee test resolves 55 Hz and 65.4 Hz simultaneous tones — three
    semitones, kick-versus-conga territory — into distinct local maxima. GPU parity measured:
    3.0e-7 absolute / 2.9e-5 relative; the contract states a 5e-5/5e-4 bar with the measurement in its
    rationale.
  - **Complex-domain onset functions (pd / wpd / nwpd / cd / rcd)** — the five classical phase-aware
    ODFs over a complex STFT, for the magnitude-flux blind spot: a second hit entering DURING another's
    ring. princarg-wrapped (a steady tone crossing ±π never fires, test-pinned); rectification pinned
    (an offset that plain cd counts, rcd must ignore); frames 0–1 are 0 by definition rather than
    fabricated history. GPU parity measured across all five variants: 4.8e-7 relative.
  - **A trap found by the family's own tests, stated rather than patched:** the atan2 phase of an
    EXACTLY-zero bin is sign-bit garbage (0, π or −π), and pd — the one unweighted variant — reads it
    at full scale. That is pd's documented weakness in the onset literature, reproduced faithfully and
    pinned by a test that also shows wpd staying clean on the same spectrum; the guide steers
    silent-bin spectra to the weighted variants.

## [1.12.0] — 2026-08-31

### Added
- **The fused labelwise scatter** (148 → 149) — per-label bounding box + centroid + voxel count + intensity
  statistics from ONE traversal of a label volume; the highest-value outstanding consumer request, with the
  measurement attached: the requesting audit found the same 512³ labelmap swept 5–6 times per refresh and one
  site recomputing a per-label bbox inside a per-label loop, ~8×10⁹ voxel reads for what a single pass yields.
  `LabelwiseReduction` covered the intensity half; the geometric half is what kept forcing traversals.
  - **Wanted labels are explicit** — background (id 0) has no hidden special case; ask for it and it is
    counted. A host-built dense id→slot table routes each voxel in O(1).
  - **An absent label reports nil bbox and NIL CENTROID — never (0, 0, 0)**, which is a plausible position at
    the volume origin that downstream code will happily draw a marker at. Same reasoning as `SurfaceDistance`
    returning nil for an empty mask; pinned by a test.
  - **Bbox and centroid are in ABSOLUTE volume voxel coordinates — a contract, pinned by a test with the
    label in the far octant of an asymmetric volume.** The consumer pattern is crop-to-bbox-then-compute;
    positions computed on the crop are crop-relative and the bbox min is the origin that restores them, so
    the origin must be recoverable from this output alone. (Requested by the NeuroAtlas consumer after
    fixing exactly this class of bug — a discarded crop origin rendering the wrong anatomy at full
    confidence.)
  - **Exact and inexact fields are stated per field and TESTED to the claim:** count and bbox are
    blocking-invariant and bit-exact; centroid and intensity sums are fixed-order float folds, deterministic
    per blocking. Variance is clamped at zero (the `RollingStats` trap).
  - **The GPU form is two stages with NO atomics** — per-block private partials (each voxel read once,
    nothing shared), then a fixed ascending-block fold per label. Float atomics would make the result depend
    on thread completion order; this is reproducible by construction, and the CPU reference computes the
    blocked form identically so parity is not an accident of ordering. Exact fields verified bit-equal on GPU.

### Fixed
- **`LabelwiseReduction` emitted NEGATIVE variance on near-constant input** — latent since the family shipped,
  found by the fused scatter's cross-validation against it. `E[x²] − mean²` cancels below zero in float32; a
  negative variance is impossible as a statistic and becomes NaN at the consumer's first sqrt. Clamped at zero
  in both the CPU reference and the GPU lowering, with a regression test. (The same cross-validation first
  caught this changelog's author misreading the family's own output layout — the accumulator comment says
  sum/sumSq, the finalisation divides to mean/variance. Both catches are what cross-validating against the
  existing family is FOR.)


## [1.11.0] — 2026-08-28

Minor, by the rule: four additive families (the convolution-inference lane, 144 → 148) plus new public
API (`match:` on `sc_list_families`, the retrofitted detection parityContracts).

### Added
- **`sc_list_families` gains `match: "wholeToken"`** — exact token equality alongside the default prefix
  matching, for NEGATIVE claims, where a prefix hit is a false verdict: a consumer's doc checker asked "is
  there an LU family?" and got seven prefix hits back (Lucas-Kanade, Lucy, luminance, `lut`) as evidence
  against a true claim. Whole-token takes LU 7 → 1, and the 1 is the genuine falsifier. Tokens are maximal
  alphanumeric runs, deliberately NOT hump-split — the first draft split camelCase and manufactured a phantom
  "LU" from Leaky·Re·LU, the exact false-verdict class being removed. Unknown match modes refuse.
- **The convolution-inference lane** (144 → 148) — the ops a ported nnU-Net / nnDetection trunk runs through,
  so detection can run locally on Metal through verified kernels. PyTorch conventions throughout, and the two
  that kill ports SILENTLY are test-pinned rather than documented:
  - **Conv3D** — multi-channel dense, channels-first `[Cout][Cin][kD][kH][kW]` weights so checkpoint tensors
    drop in without a transpose pass; CROSS-CORRELATION (kernel not flipped), which is what PyTorch's "conv"
    is — a flipped implementation passes every symmetric test ever written, so the pin uses an asymmetric
    delta. Zero padding, floor-division extents, per-output-channel bias.
  - **Transposed Conv3D** — ConvTranspose semantics including `outputPadding` (dropping it shifts every
    skip-connection concat by a voxel in a network that still runs), weights `[Cin][Cout][k…]` — Cin FIRST,
    PyTorch's own asymmetry, kept because "normalising" it is how a decoder produces plausible garbage.
    Gather form: same arithmetic as the textbook scatter, no atomics, no races. The load-bearing test is the
    ADJOINT IDENTITY ⟨conv(x),y⟩ = ⟨x,convᵀ(y)⟩ on a non-square, strided, padded, multi-channel
    configuration — it caught its own author before anyone else: a "helpful" weight permutation in the first
    draft broke it by 100%, because ConvTranspose's `[in][out]` IS conv's `[out][in]` and the same bytes serve
    both.
  - **Instance norm 3D** — nnU-Net's normaliser: per-channel spatial statistics, **eps inside the sqrt** and
    **biased variance**, both pinned by arithmetic chosen so no tolerance can blur which convention is
    implemented (σ²=3, ε=1 separates the eps conventions by 37%). A constant channel yields β, finite. The
    eps test also caught its author: the first "variance 3" vector had variance 10/3.
  - **LeakyReLU** — slope as a real parameter (0 = ReLU, 1 = identity, both asserted). Exact GPU parity,
    truthfully for once: no accumulation, a compare and a multiply round identically.
- **Measured parity contracts retrofitted to `BoxIoU3D` and `ROIAlign3D`** — requested by the adopter wiring
  the detection bridge, who found the house rule (gate every adopted op behind a stated tolerance)
  unfollowable for the two v1.7.0 families that predate `SLParityContract`. The bars are measured, not
  reasoned: IoU came back **bit-exact over 90,000 pairs** (fixed-order per-pair arithmetic, no reduction),
  stated as default-float anyway because FMA contraction is compiler-discretionary; ROI-Align measured
  **9.5e-7 absolute / 256 ULP** at samplingRatio 2 — inside default float's absolute bound and two orders of
  magnitude past "≤1 ULP, it's just FMA", which is why the rationale warns against a ULP-tier bar.


## [1.10.4] — 2026-08-28

### Added
- **The mirrored `BatchedCorrelation` binding** — `crossCorrelationBatchMirrored`: the SHARED reference on `a`
  (unshifted), each per-row signal shifted, which is the single-pair consumer convention batched. Built to a
  consumer's falsifiable acceptance criterion, which is the test verbatim: every row **bit-identical** (`==`,
  not tolerance) to `CorrelationReference.crossCorrelation(a: sharedReference, b: signal_j)`. Their pinned
  delay-convention test is included batched — shared AIF, signal row d delayed by d, row d's argmax == d — and
  the footgun this variant removes is kept as an executable demonstration in the same test: the ORIGINAL
  binding on identical data pins every argmax to 0, silently. Asked for independently by two consumers
  (perfusion Tmax: shared AIF × per-voxel TACs). GPU parity is the family's own stated bar (default float,
  FMA-drift expected cause), measured at ≤1.7e-6 — the consumer explicitly declined the forbid-FMA trade,
  since an integer-lag argmax cannot move at that delta except on a pathological tie.


## [1.10.3] — 2026-08-28

Fixes to fixes: everything here was found by consumers deliberately attacking the 1.10.2 cut, some of it
within hours of the guard it attacks being written. 1.10.2 shipped mid-stream, so these landed one release
later than intended — the honest sequencing, since a published tag is never moved.

### Fixed
- **The `exact` narrowing guard's own defects.** It refused two IDENTICAL Double arrays (it keyed on
  float32-representability; it now keys on CONCEALMENT — pairs that differ as supplied and become equal as
  float32, the only pairs the narrowing can hide; identical inputs pass, visible differences fail honestly).
  Its prescribed remedy was unfollowable — the `absrel` bounds existed under `absolute:`/`relative:` but other
  spellings were silently dropped, so a working feature read as missing: aliases accepted, effective bounds
  echoed in every result (`absoluteBound`/`relativeBound`, `ulps`), unread arguments named in
  `ignoredArguments`, refusal text names the parameters. And an empty comparison now refuses instead of
  returning the `compatible: true` that hides a harness which failed to populate its arrays.
- **`sc_detect_in_code` could not see stateful recurrences, and misprescribed one.** A per-bin Kalman loop (an
  exact match for `Spectral Kalman denoiser`) was silent; an array-form IIR Direct Form I returned `MatMul`
  at 68 — a wrong prescription, since an IIR cannot be parallelised that way. Two shape signatures added (the
  scalar Kalman recurrence; Direct Form I by feedforward-plus-feedback-subtract) and a matmul veto on `-=` of
  products: a dense product never subtract-accumulates, and never reads its own output at a negative offset.
  The three consumer repros are the regression tests, verbatim.
- **`BatchedCorrelation`'s operand roles stated where they bite.** The batched family shifts the SHARED
  reference; the single-pair consumer convention shifts the per-signal operand, and the two are not related by
  swapping arguments. A consumer adopting it for perfusion Tmax — the use its own keywords advertise — got
  argmax 0 for every voxel, silently. Guide entry, family header and this line now say which operand shifts;
  a mirrored-binding variant is the top open consumer request, now asked for by two consumers independently.
- **`sc_suggest_families` score semantics stated in the tool description:** normalised query-token→keyword
  coverage, comparable across queries as coverage — NOT shape exactness; a verbatim matchedShape hit can score
  low. Rank is the signal. (A consumer misread 24-on-an-exact-match as a weak match and had to correct a
  committed doc.)
- **The 1.10.1 build-ambiguity note**, offered by the consumer who nearly recorded the ambiguity as normal:
  two differently-behaving binaries both reported `1.10.1` during that release's re-cut. `buildCommit`
  prevents recurrence; binaries predating it cannot be disambiguated retroactively — upgrade rather than
  reason about which build you hold.

### Added
- `CONSUMER_FEEDBACK_INBOX.md` brought fully current: the Kalman audit and the narrowing bug resolved with
  attribution and four independent reproductions; the guard-defect trio resolved; new OPEN entries for the
  detector's remaining filter-shape silences, the FIR-design misranking, the `contains` substring collisions,
  three estimation gaps (per-track transition EKF predict, windowed argmax, phase unwrap against a
  prediction), and the float64 roadmap question — escalated as a product decision.

## [1.10.2] — 2026-08-28

### Added
- **`CONSUMER_FEEDBACK_INBOX.md`** — the standing consumer-feedback queue, authored by the AssistantApp
  consumer session and landed here with its history: bugs and requests with repro and downstream cost
  attached, resolved entries kept rather than deleted so a recurring defect class is visible as one.
  `AGENTS.md` points at it. The Kalman audit (five defects, one class, one retraction with its lesson) and
  the narrowing bug are filed as resolved against this release.
- **Seven estimation/tracking families** (137 → 144), requested by a consumer auditing a Kalman/prosody
  package. Each exists because its naive form fails in a specific, silent way:
  - **Batched small-dense EKF** — the generalisation of the hard-coded 2-state `Harmonic-frequency EKF`. The
    update is in **Joseph form**, and that is the family: the textbook `P⁺ = (I − KH)P` is algebraically
    correct and not symmetric by construction, so rounding drifts the covariance indefinite, the gain is then
    computed from a negative variance, and the filter diverges while every intermediate value still looks like
    a number. Joseph form is a sum of congruence products — symmetric and PSD for ANY gain, not just the
    optimal one.
  - **IMM mixing step** — including the between-mode **spread term**, which is dropped often because the mixed
    mean looks right without it. Dropping it makes the filter report the average of the modes' confidences
    while ignoring that they disagree, so it is overconfident exactly when an IMM should be widening. Measured:
    an order of magnitude too narrow on conflicting modes. A mode whose probability collapses keeps its own
    state rather than taking every other mode down with a NaN.
  - **Particle resampling** — systematic and stratified (genuinely different: one draw versus one per stratum),
    with the **ESS gate that decides not to resample**, since resampling is variance-increasing and a healthy
    cloud loses diversity for nothing. The cumulative-weight walk is clamped and the final value forced to
    exactly 1 — in float it lands a few ULP either side, and below 1 the last threshold walks off the array.
    Total depletion is reported rather than divided.
  - **RTS smoother backward step** — the predicted-covariance inverse fails where the filter is working BEST,
    since a confident prediction drives it towards singular, so a smoother tested only on noisy data never
    sees it. The smoothed variance is floored at zero: unlike Joseph form this expression has no congruence
    structure, and float underflow on a legitimate reduction in uncertainty can take it negative.
  - **Hampel identifier** — and the failure that matters: on a flat stretch every sample equals the median, MAD
    is exactly zero, the threshold is zero, and every sample differing by one ULP becomes an outlier. The
    filter deletes the quietest parts of the signal, hardest where the data is cleanest. Zero dispersion is
    absence of evidence, not evidence of a spike. The 1.4826 Gaussian consistency constant is applied and
    documented — without it a caller's `sigmas` means something 1.5× tighter than they think.
  - **Scaled sigma points + unscented transform** — reporting that W₀ᶜ is NEGATIVE for the usual small α, which
    is what lets the reconstruction go indefinite where Joseph form cannot.
  - **Square-root covariance update** — the structural answer: carry S with P = S·Sᵀ and a covariance
    **cannot** be indefinite, and a downdate that would create one fails visibly instead of producing a
    negative variance downstream.

  **A measurement that came out of testing, not from the literature:** at the textbook α = 1e-3 the sigma-point
  weights reach ±9.7×10⁵ and must sum to exactly 1. In float32 they sum to **0.969 — a 3% error before any data
  is touched**; in Double, 1.0000000001. That is not a defect in this implementation, it is what α = 1e-3 costs
  in single precision, and it is a concrete answer to the float64 constituency question a consumer raised.
  α ≈ 1 keeps the magnitudes near unity and the sum exact to 1e-7.

### Fixed
- **Five MCP-surface defects, all one failure wearing five hats: answering a question that was not asked,
  without saying so.** Reported by two consumer sessions against shipped 1.10.1, each verified here before
  being acted on.
  - **A false PASS on narrowed Doubles.** JSON numbers arrive as Double; the whole parity surface is Float.
    Two Doubles differing at 2e-16 became the same Float, and the doctor then reported bit-identity with
    `maxAbsoluteError: 0` **under `exact`** — a pass manufactured by discarding the bits in question.
    Reproduced independently three times, once from a real float64-vs-float32 Kalman recurrence rather than a
    synthetic pair. This was the sharpest possible contradiction of the substrate's own position, since the
    same binary refuses an unknown tolerance with *"silently substituting one would report a pass under a bar
    you did not ask for"*. Now: **refused under `exact`** — bits discarded on the way in cannot be compared, so
    a pass would mean "identical as far as I looked" — and under any other policy the response carries
    `precisionWarning` and `maxTrueDifferenceBeforeNarrowing`, the number the float32 path can no longer see.
    Values that ARE exactly representable are not flagged, so the warning stays a signal.
  - **`sc_emit_kernel` silently ignored `family`**, returning the affine specimen for any name including a
    nonsense one, while the `kernel` path refused unknown names helpfully. Now refused, pointing at
    `sc_list_families` and the `symbols` field that names the real lowering entry point.
  - **`sc_verification_report` silently ignored `subject`**, captioning every report "reference vs candidate".
    Now honoured, and any argument the tool does not read is named back in `ignoredArguments` — an argument
    that vanishes without trace is how this and `family` went unnoticed for a release.
  - **One report stated two different mismatch counts**, and eight of the nine rows it flagged as divergences
    carried text saying they agreed under the applied policy. Two different questions were being answered with
    one number: `diagnoseBuffers` enumerates every element that is not BIT-IDENTICAL (it applies no policy —
    explaining a cause is useful either way), while `compareFloatBuffers` applies the stated tolerance.
    `mismatchedElementCount` is now the policy-filtered count, matching `sc_check_parity` on identical input;
    the enumeration is reported as `nonIdenticalElementCount`; and rows that differ but pass now say
    "within tolerance" instead of being flagged.
  - **The second hat, caught by the reporting consumer's own reframing and missed by the first fix:**
    `sc_ulp_distance` returned `ulpDistance: 0` — documented as IDENTICAL — for two genuinely distinct
    Doubles, echoing both back as the same narrowed float. The float32 answer is legitimate; the silence was
    not. It now reports `identicalAtSuppliedPrecision: false` with the true difference when 0-as-float32
    covers values that differ as supplied. Exactly-representable inputs stay silent, so the warning remains a
    signal.
  - **The `?? Float.nan` fallback is gone.** A non-numeric array element used to become NaN silently, moving
    the error from "your input was not numeric" to a numeric diagnostic blaming values the caller never sent.
    A non-numeric element now refuses the whole array. Named by the consumer who read the function: it was
    called `doubles`, returned `[Float]`, and invented NaNs — three lies in four lines.
  - **`ulp1` was emitted by `sc_zoo` and refused by `sc_check_parity`.** The `ulpN` spelling is now accepted —
    refusing an unknown policy is a principle, refusing your own output is a bug wearing that principle's
    clothes. A genuinely unknown policy is still refused, and the message now names the spelling it accepts.


## [1.10.1] — 2026-08-28

Patch, deliberately: the two families catalogued here were already IMPLEMENTED and shipping in
1.10.0 — their code, contracts, tests and compile-sweep coverage all went out in that release. What
changed is catalogue metadata, so nothing was added to the public `SL*` surface. A metadata correction
plus a bug fix is what patch means. (1.10.0 was a minor for the opposite reason: twenty families whose
implementations were genuinely new.)

### Added
- **`BoundsReduce` and `SpringElectricalLayout` are now catalogue families** (130 → 132). Both shipped in
  1.10.0 as complete implementations — contract, tests, compile-sweep coverage — that the catalogue could not
  see, and both were held in `FamilySymbolIndex.pendingCatalogue` with a stated reason rather than quietly
  omitted. They are the reason that list existed; **it is now empty**, which under the gate means every
  kernel-emitting implementation in the package is accounted for by exactly one catalogue entry.
  - **Bounds reduce 2D** — the axis-aligned bounding box of a scattered point set, for zoom-to-fit and
    viewport culling. NaN coordinates are skipped rather than poisoning the result, and an empty input yields
    `[+inf, +inf, -inf, -inf]` rather than a silently plausible zero box.
  - **Spring-electrical layout step** — one annealed force step: all-pairs repulsion, CSR-neighbour
    attraction, gravity toward a centre so disconnected components cannot drift off, and a clamp to the canvas.
    Catalogued as its own family rather than folded into `Force-directed graph layout`, because it is not the
    same operation: that one takes an edge list and has neither gravity nor bounds.


- **Five families from a consumer build queue** (132 → 137), each verified absent from the catalogue AND the
  source before being written — the last four defects were families that existed but were invisible, so
  "grep-confirmed absent" now means both lists.
  - **Dense optical flow (Lucas–Kanade)** — per-pixel motion, gated on the structure tensor's smaller
    eigenvalue, composing on the existing `Symmetric 2×2 analytic eigenvalues`. The gate is the family: on an
    edge the flow ALONG the edge is physically unrecoverable (the aperture problem), and solving anyway divides
    by a near-zero determinant and returns a large, confident, meaningless velocity — which downstream reads as
    fast motion rather than as no information. Invalid pixels report zero and say so; on a real frame pair most
    of the image is untrackable, and `validFraction` states that rather than filling it in.
  - **N-channel beamforming** — the M-microphone generalisation of the two-channel MVDR pair. Delay-and-sum
    with interpolated fractional delays (nearest-sample rounding costs ~30° of steering phase at 8 kHz), plus
    superdirective weights with diagonal loading. Measured on 4 sensors at 3 cm and 150 Hz, all three regimes
    are pinned: unregularised it **refuses** (R is not positive-definite at float precision) rather than
    fabricating a design; barely regularised it returns weights of ±111 for a unit-response array with
    white-noise gain ≈ 0 — the classic superdirective disaster, a beautiful beampattern that amplifies sensor
    noise ~100×; sensibly loaded the weights sum to 1 and the noise gain turns favourable. The gain is returned
    because a design cannot be judged without it.
  - **Discrete wavelet transform** — orthonormal filter bank, forward/inverse/multilevel, Haar and D4. Perfect
    reconstruction depends on the filters AND the boundary convention AND the decimation together; getting one
    wrong is correct in the middle and wrong at the edges, which a round-trip checked only in aggregate passes.
    The round-trip test therefore asserts the boundary samples by name.
  - **Analytic signal / Hilbert transform** — and the bug it exists to prevent: **DC and Nyquist must not be
    doubled.** They are their own conjugate mirror, and doubling them adds an offset that looks like a
    plausible slow drift rather than a mistake. Tested with a large DC term, where a doubled bin is unmissable.
  - **2D phase correlation** — normalised cross-power, with the circular peak **unwrapped** to a signed shift.
    Returning the raw index is right for small positive shifts and wrong for every negative one, and being
    right half the time is what lets it survive a careless test.

### Fixed
- **`sc_version` now reports the BUILD, not just the version.** Two sessions in one day lost time to a question
  the tool could not answer: *which build am I talking to?* The semantic version does not settle it — a binary
  reporting 1.10.1 may predate a fix that also shipped in 1.10.1, and a running MCP server keeps whatever
  binary it started with, so a rebuild on disk changes nothing for an already-connected client. The response
  now carries `buildCommit` and `familyCount`. `buildCommit` is stamped into the source immediately before a
  release build and reverted after, so the committed value is always `"unknown"` — and `"unknown"` is not a
  gap in the answer, it IS the answer: you are running a local build, not a released artefact.
- **`sc_detect_in_code` was prescribing the wrong family, and was blind to most of the catalogue.** Both
  reported by the AssistantApp DICOM/NeuroAtlas consumer, who scored the detector against the shapes their
  codebase actually contains and got **1 correct hit in 7**. Verified here before being acted on.
  - **The wrong prescription.** A canonical clamped 3×3 convolution — the `Stencil` family's own documented
    `matchedShape`, verbatim — came back as `MatMul (naive + threadgroup-tiled)` at 68%, with `Stencil`
    absent. Worse than a miss: acting on it replaces a convolution with a matrix multiply. The cause is that
    a stencil genuinely CONTAINS a matmul's `+= a[…]·b[…]`, so requiring more of the matmul cannot separate
    them. Signatures now carry a **veto**: a dense product never clamps its indices, so a clamped source index
    rules the matmul out, and a shape-based `Stencil` signature recognises the convolution that names itself
    nothing. The name-based signature only ever fired on code that said "sobel" or "gaussian blur".
  - **The coverage bias.** Signatures were almost all 1-D signal shapes, so pointing the detector at a
    medical-imaging codebase returned near-silence — which reads as "nothing here to replace" rather than
    "the detector cannot see this", and is why that consumer's audit had to be done by hand. Added shape-based
    signatures for `Pairwise squared-distance`, `Resize`, `Resample affine`, `Connected components 2D`,
    `HU-band classification cascade`, `Bounds reduce 2D` and `Integer-exact histogram` — every one already
    catalogued, none previously visible. The consumer's seven probes now score **7 of 7**, and are kept as a
    regression set rather than scattered cases, because the failure was coverage.
  - A family is now reported **once**, on its strongest evidence, rather than once per matching signature.
  - Widening coverage introduced a false positive of exactly the kind being fixed — `counts[p.group]++`
    matched the histogram signature, which would prescribe a GPU intensity histogram for tallying objects by
    a field. Caught by a false-positive control, not by review; `counts` is no longer accepted as a histogram
    array name while `hist`/`bins` still are.

- **A single-channel FIR was still being prescribed as a matmul.** Reported against v1.10.1 — not a stale
  binary; the consumer had already ruled that out and I wrongly assumed otherwise — with a verbatim
  Savitzky–Golay smoother that came back as `MatMul` at 68% and nothing else. The 1.10.1 veto keys on a
  clamped index, and a 1-D filter has no clamped 2-D neighbourhood to trip it. Meanwhile the existing
  Correlation signature keys on the literal token `lag`, so it only ever fired on code that already used that
  word, and a textbook FIR calls its index `k`. This is the most common 1-D signal shape in existence, on the
  filtering code the detector should be strongest on.
  The shape signal is a **symmetric offset range** — `for k in -m...m` — which a dense product never has: a
  matmul indexes with a row stride, a filter slides by pure addition. That now both recognises the filter and
  vetoes the matmul, with a further veto keeping it apart from the stencil, which also loops symmetrically but
  clamps.
- **Compile-sweep coverage now has a gate.** It had none, and lapsed twice in one day — sixteen lowerings
  outside it when the medical-imaging lane landed, five more with the tracking lane. Adding a family does not
  force its registration and the sweep reports a healthy-looking number either way. The new assertion is the
  same shape as the catalogue gate: every kernel-emitting type must appear in `KernelCompileAllTests`. It
  matters most where nobody looks — a family's GPU parity test dispatches through a harness that returns nil
  without a Metal device, so on Linux CI an unregistered lowering has no compile coverage at all. Verified to
  fail on a deliberately unregistered lowering. Sweep: 192 lowerings, 333 programs.
- `TermMatchTests` asserted that "hilbert" returns nothing, as its proof that a negative answer is
  trustworthy. It went red the moment the analytic-signal family landed — the test doing its job. Re-pointed at
  `hough` and `ransac`, verified absent from catalogue and guide, and it now also asserts that "hilbert" IS
  findable.

## [1.10.0] — 2026-08-27

### Added
- **`FamilySymbolIndex` — the map from a catalogue family to the code that implements it, and a gate on the axis
  nothing was watching.** Two things, and the second is why it is a test rather than a document.

  **Discovery.** `sc_suggest_families` could say WHICH family fits and then left the caller to grep for the entry
  point. Both it and `sc_list_families` now return the call signatures — reference, contract and lowering — so a
  suggestion carries the call you actually write.

  **A gate on catalogue↔implementation drift.** The catalogue was found to have drifted from the source in both
  directions, four times, and none of it was catchable by an existing guard:
  - `DistanceTransform` catalogued **twice** under two different names — one implementation, two families
    reported by `sc_list_families`, shipped that way for months.
  - `AnisotropicEDT3D` catalogued **zero** times despite a contract, three lowerings, three compile-all
    registrations and its own tests.
  - Then, hours after that fix, two sessions independently catalogued it **again** under different wording and
    nearly shipped the first defect a second time.
  - `BoundsReduce` and `SpringElectricalLayout` — found by this index's own check, and `Gather3D`,
    `Scatter1D`, `Scatter2D`, `Scatter3D`, found only after the check itself was widened, and now listed in
    `pendingCatalogue` with reasons rather than silently ignored, awaiting a decision on whether each is a
    public family or an internal primitive.

  `FamilyUsageGuideTests` checks catalogue↔guide in both directions and is structurally blind to all of it: a
  PAIR of entries describing nothing is perfectly self-consistent, and an implementation with NEITHER entry has
  nothing to contradict. Text cannot watch the axis either — three name/description-similarity sweeps were tried
  and all three were wrong in both directions, one flagging 22 mostly-false candidates while missing the real
  defect. The near-miss is the clearest case: the two duplicate names shared no distinctive substring, so no
  `uniq` check could ever have seen it. **The duplication was semantic, not textual.**

  The gate asserts every catalogue entry resolves to declared types with the recorded signatures, every
  KERNEL-EMITTING implementation is claimed by exactly one entry, and nothing is claimed twice.

  **"Emits a kernel" rather than "declares a contract" is load-bearing, and the first version got it wrong.**
  Keying on the contract walked straight past four stranded gather/scatter lowerings: they emit real kernels,
  declare no contract, and the catalogue NAMED them all along — the entries read `Gather1D / Scatter1D` and
  `Gather2D/3D / Scatter2D/3D` while the index claimed one implementation of each pair. Emitting a program is
  the property that makes the catalogue responsible for something; declaring a contract is a narrower habit
  that not every kernel follows. Found by auditing every function in the package that returns an
  `SLBackendProgram` — 188 of them — against both the catalogue and the compile sweep, rather than trusting
  the gate that had just gone green. An
  implementation that is deliberately not a family must be listed with a REASON — silence is not an option, so a
  new family cannot be added without the catalogue noticing. All three assertions were **verified to fail on the
  defect they claim to catch** before being committed against the fix.

  Signatures are generated by the same scanner the test re-runs, so a renamed argument label makes the file stale
  and the build red. Building it caught a bug in the scanner itself: a defaulted tuple parameter
  (`spacing: (x: Float, y: Float, z: Float) = (1, 1, 1)`) contains closing parens that are not the end of the
  parameter list, and terminating on the first `)` had silently recorded a ten-parameter function as a
  six-parameter one — the exact confident-wrong output the index exists to prevent, found only by deliberately
  breaking it.

- **Three FIR design/analysis families** (for the FIRFilters package — filter design, multichannel convolution
  and response grading). Catalogue 127 → 130:
  - **`BatchedFIR`** — many signals through ONE shared FIR filter, one thread per (output sample, channel).
    This is a **binding** gap, not a new arithmetic, and the family says so: a *single-channel* FIR convolution
    is already expressible with the shipped `Correlation` family by correlating the TIME-REVERSED taps against
    the signal — exactly what a vDSP-based direct-form convolver does when it hands reversed taps to
    `vDSP_conv`. What no shipped family expresses is the batch axis: `BatchedCorrelation` binds the per-row
    buffer as the SHORT operand against one shared LONGER reference, and multichannel FIR needs the inverse —
    shared SHORT filter, per-row LONG signal. So filtering B channels through one filter meant B host
    dispatches, precisely the case where the GPU pays off (HRTF/ambisonic decode banks, multiband splits).
    Each row is pinned **bit-identical** to the reversed-tap `CorrelationReference`, which is what lets the
    family inherit that family's tolerance story rather than argue a weaker one of its own — and that required
    accumulating the taps **descending**, since ascending k visits the same products in the opposite order and
    measured ~1 ULP away (float addition is not associative). Boundary stated plainly: taps reading before the
    row start are skipped, not zero-padded from a history buffer, so a streaming caller still owns its overlap.
  - **`BatchedDTFT`** — the DTFT on an **arbitrary** frequency grid, one thread per frequency, plus the group
    delay τ(ω) = Re{H_d/H} built on the same kernel via optional `n`-weighting. The gap is the grid: the FFT
    family evaluates a uniform power-of-two grid (you take the points it gives you), and Goertzel evaluates a
    handful of single frequencies by a sequential recurrence. Neither serves a dense grid of *chosen*
    frequencies — log-spaced points, exact band edges, or a zoom into one transition region. Pinned against
    the shipped FFT on the one grid where they overlap, which is what proves it is the same transform sampled
    elsewhere. Honest scope: it is O(N·numFreqs) and therefore the **wrong** tool for a uniform full-length
    spectrum — use the FFT for that. Tolerance is the default float bar and **bit-exactness is explicitly not
    claimed**: a sum of float products over per-term transcendentals is exactly the shape a GPU contracts into
    FMAs. At a spectral null the group delay returns 0 as a documented "undefined" rather than dividing by
    ~zero — a stated substitution, not a silent fix.
  - **`PartitionedSpectralMAC`** — the UPOLS inner sum `Y[k] = Σ_p H_p[k]·X_{m−p}[k]` over a frequency-domain
    delay line, one thread per bin. Same shape of gap as `BatchedFIR`: the arithmetic already exists — a
    single complex product is `ComplexMix.multiply`, exactly one term of this sum — but nothing accumulated a
    complex product across a PARTITION axis, so a partitioned convolver ran it as a host loop (the FIRFilters
    implementation this is drawn from does, with an in-source note that it "vectorises cleanly with
    `vDSP_zvmaD`"). Scope is stated rather than implied: the family owns ONLY the parallel core; the FDL
    write, head advance, per-block FFTs and overlap-save tail are sequential and stay on the host, so
    `fdlHead` is a parameter rather than owned state. Positioning is stated too — for ONE stream at typical
    block sizes this is **not** a GPU win, since a command-buffer round-trip costs more than the vDSP MAC it
    replaces; it pays off for long impulse responses (P in the hundreds), offline render, or many
    convolutions at once.
- **Seven volumetric medical-imaging families** for the NeuroAtlas/DICOM modules. Each one exists because its
  naive form fails in a specific way, and each carries a test that pins that failure:
  - **Surface distance metrics (HD / HD95 / ASSD)** — the validation ruler Dice cannot replace. Both point sets
    are supplied in MILLIMETRES, so anisotropic spacing cannot be silently dropped; measuring in voxel units on
    a 0.4/0.4/1.0 mm CT understates a through-plane error by 2.5×. Hausdorff is the max of BOTH directed maxima,
    because a spur of B outside A is invisible from A's side. HD95's two convention axes — scope and
    interpolation rule — are exposed and defaulted to what the clinical literature quotes; a test shows the four
    combinations spanning 0.5 mm to 10 mm on identical inputs. An empty mask returns nil, never the 0 that would
    read as a perfect score.
  - **Joint histogram + mutual information** — the CT↔MR metric. A test demonstrates why it is needed: on an
    inverted-contrast pair that is perfectly aligned, NCC reports −0.99, so a registration maximising NCC moves
    AWAY from the right answer, while MI reports the maximum. Empty bins contribute zero by construction rather
    than the log(0) → NaN the naive expression produces — and since a joint histogram is mostly empty bins, that
    is the normal case, not an edge case. Computed with no atomics: one thread per row, nothing shared.
  - **Oblique ray-cast projection** — the family `VolumeProjection` names in its own header and defers. Fixed
    sample count rather than marching until the ray exits, because a data-dependent trip count makes the fold
    order stop being a function of the parameters. Out-of-volume samples are skipped, not edge-clamped (clamping
    paints a bright rim onto every MIP), and `mean` divides by the in-bounds count (dividing by the requested
    count adds a vignette that is not in the data). Verified to reproduce `VolumeProjection` exactly when the
    ray is set to the Z axis. `samples: 1` makes it a plain oblique reslice, so CPR and rendering share a kernel.
  - **Watershed** — splitting touching structures. Marker-controlled immersion, with the parallel core (the
    steepest-descent pointer field) lowered to a kernel and the flood left as a host priority queue, stated
    plainly: parallel watershed variants do not reproduce the immersion result, and a segmentation that changes
    with scheduling cannot be validated. Ties break on lowest linear index; plateaus flood FIFO within a
    priority level, so a flat region splits down the middle instead of wherever the heap happened to pop.
  - **3D skeletonisation** — vessel centrelines without the Python sidecar. Topology-preserving thinning built
    on a simple-point test computed by direct connected-component labelling inside the 3×3×3 block rather than
    the usual 256-entry octant LUT, which cannot be checked by eye. Six subiterations, because deleting every
    simple point at once removes a two-voxel-wide bar entirely even though each of its voxels is individually
    simple — `simultaneousDeletionSeversBar` keeps that failure as a demonstration.
  - **Mesh decimation (quadric error metric)** — the other half of mesh conditioning; Taubin fixes shape, not
    count. Three traps pinned: the 3×3 optimal-position solve is singular on flat and symmetric geometry (most
    of a medical mesh) and inverting it anyway puts a vertex at 1e18, so it falls back to the midpoint;
    zero-area faces — which marching cubes emits routinely — give a NaN normal that contaminates every incident
    vertex, so they contribute nothing instead; and vᵀQv comes out at −1e−7 in float32 on flat regions, which
    makes a greedy queue rank numerical noise above real candidates, so costs are clamped at zero.
  - **Richardson–Lucy deconvolution** — undoing a known PSF. The denominator is floored: it is exactly zero
    wherever the estimate is zero (every volume border, all the air around the patient), so without the floor
    the method is NaN on iteration one of essentially every real image. The second correlation uses the MIRRORED
    PSF — with the symmetric Gaussian everyone tests with the mirror is a no-op, so a version that forgets it
    passes every test and then shifts the image on the first asymmetric PSF; the tests here therefore use an
    asymmetric one. Documented, and measured by a test, that more iterations is not better: RL fits the noise,
    so the iteration count is a regularisation choice. Frequency-domain Wiener deconvolution is explicitly NOT
    included, and the note says why.

  Catalogue: **114 → 121**.

- **Separable 3D FFT**, and **Wiener deconvolution** on top of it — closing the one gap the Richardson–Lucy
  family explicitly declined to cover.
  - **Separable 3D FFT** applies the existing radix-2 1D transform along x, then y, then z. Axis order is part
    of the contract and is tested bit-identical, because each pass rounds and rounding does not commute: two
    implementations that both "do a 3D FFT" can disagree in the last ULPs with neither being wrong. Verified
    against a direct O(N²) 3D DFT — an independent oracle summing in a completely different order, which is the
    only thing that catches a transposed axis or a wrong stride, since a broken separable transform still
    round-trips perfectly and still looks like a spectrum. GPU parity is **bit-exact**: twiddles are precomputed
    host-side, so the device does only IEEE-safe complex butterflies. Carries the padding helpers, since padding
    for the power-of-two extent and padding for a linear convolution are the same operation.
  - **Wiener deconvolution** — `conj(H)/(|H|² + NSR)`, single-shot where Richardson–Lucy iterates. NSR is
    supplied as a MODEL, not a knob: flat, from measured variances, or per-frequency. Three traps pinned:
    the FFT's convolution is **circular**, so without a guard band bright structure at one face ghosts onto the
    opposite face and looks like anatomy near the edge; the PSF must be **wrapped to the origin**, since
    centring it applies a linear phase ramp that shifts the whole result by half the volume; and the result
    **can go negative**, so the ringing around a high-contrast edge shows as a dark rim that is not tissue —
    the clamp is opt-in, because clamping hides the ringing rather than removing it.
    The regularisation test is the useful one: it shows that on a gentle 5-tap blur an unregularised filter
    behaves perfectly well, and only a PSF with a genuine near-null (a box blur, a defocus, a slice profile)
    exposes the 10× gain blow-up. The failure is invisible on exactly the test PSF someone reaches for first,
    which is how NSR came to be treated as a fudge factor.
    Also documented where each belongs: Wiener is the least-squares step for Gaussian noise, Richardson–Lucy the
    maximum-likelihood step for Poisson — so photon-limited data wants RL, and a known noise floor wants Wiener.

  Catalogue: **121 → 123**.

- **3D overlap-add (OLA / WOLA / COLA)** and **Separable 3D STFT** — the block lane on top of the 3D FFT.
  - **COLA is treated as a condition you can CHECK, not just an operation you run**, which is the point of
    putting it here. `colaReport` measures how far the shifted window copies are from summing to a constant, so
    "will this window and hop reconstruct?" becomes an assertion instead of a hope. A pair that fails does not
    error — it lays a periodic banding over the volume at the hop spacing, a texture that was never in the data.
  - The window trap is pinned: **symmetric Hann does not satisfy COLA at hop N/2; periodic Hann does, exactly.**
    `numpy.hanning` and MATLAB's `hann(N)` are the symmetric ones. They differ by a single sample in a
    denominator, both are correct windows, and only one of them overlap-adds.
  - **The boundary ramp is not a COLA failure.** The outer blocks have fewer neighbours, so the window sum ramps
    at each end however good the window is — a verifier checking the whole field rejects every valid window, one
    that never checks the interior misses a bad one. The report returns interior and boundary separately.
  - **WOLA's division is what frees it from COLA**, and that is now stated where it matters: WOLA needs the
    overlap energy to be non-zero, not constant, so it reconstructs exactly even with the window that fails OLA.
    Voxels below the coverage threshold are masked to zero rather than divided — dividing turns the uncovered
    rim into a bright frame.
  - **Separable 3D STFT** cuts a volume into overlapping windowed blocks and 3D-FFTs each: local spectra for
    orientation estimation, volumetric texture, block-matching denoisers. The size expansion is reported rather
    than discovered — `(block/hop)³ × 2`, a factor of 16 at half overlap, so a 256³ volume at 32³ blocks is
    3.5 GB from a 67 MB source. A streaming per-block entry point exists for that reason and is tested
    bit-identical to the materialised transform.
  - **`ifft3D` by name**, since a 3D inverse transform is what people search for even though `fft3D(inverse:)`
    already was one.
  - One more association hazard pinned, the same class as the FFT's axis order: the separable window factorises
    **exactly**, but only under the stated grouping `(wz·wy)·wx`. `(wx·wy)·wz` disagrees in the last ULP on
    ordinary window values — same product, different float — and the test asserts the hazard is real on its own
    data rather than hypothetical.

  Catalogue: **123 → 125**. 974 tests in 218 suites.

- **Four 1D streaming / SDR families**, closing every gap a coverage sweep found against the 110-family
  catalogue. Each exists because its naive implementation has a specific numerical failure, and each test
  pins that failure rather than merely exercising the happy path:
  - **SDR overlap** — sparse-binary set intersection by two-pointer merge, one thread per stored column. The
    hot loop of a Thousand-Brains / HTM cognition layer. Integer arithmetic throughout, so CPU and GPU agree
    `.exact` — there is no rounding to diverge over.
  - **Rolling statistics** — causal stride-1 mean / SD / z-score. Recomputes each window instead of carrying
    a running sum, because the running-sum form drifts in float32 and can drive the variance NEGATIVE on
    near-constant input, returning **NaN from sqrt() on perfectly well-behaved data**. Clamped at zero, a
    flat window scores z = 0 rather than ±∞.
  - **Complex multiply / NCO mix** — phase is closed-form per sample, never accumulated. An accumulated NCO
    is strictly sequential and drifts with how the buffer was chunked. The API takes a sample `startIndex`
    rather than a pre-multiplied `phase0`, which is what makes a chunk boundary **bit-exact instead of one
    ULP adrift** — the shape of the call guarantees the property, not a warning in a comment.
  - **Resample 1D** — endpoint-preserving linear resample, the 1D case `Resize` (2D/3D only) never covered.
    The mapping convention is stated explicitly because implementations silently differ: this preserves
    endpoints exactly, unlike the pixel-centre convention image resizing uses, and the two disagree by half
    a sample at the ends.

  Catalogue: **110 → 114**.

- **Batched least squares by Householder QR — a *correctness* fix, not a speed one.** `BatchedSPDSolve` recommends
  least squares "via the normal equations (AᵀA)x = Aᵀb", and forming AᵀA **squares the condition number**
  (κ(AᵀA) = κ(A)²). In single precision that is a cliff, not a rounding nicety: once κ(A)² passes ~1/εₘ
  (εₘ ≈ 1.19e-7) the normal-equation matrix is numerically singular and the solve returns a **finite,
  plausible-looking, wrong** answer — the silent-failure class this package exists to catch. The new family solves
  min‖Ax − b‖₂ directly by Householder QR (never forming AᵀA), so it works at κ(A) instead of κ(A)². The
  justification is **measured, not asserted**: on the Läuchli matrix (ε = 1e-4, so ε² is lost against 1 in Float)
  the test shows AᵀA collapsing to the exactly singular `[[1,1],[1,1]]`, the normal-equation route returning
  x = [1, 0] against an **analytic** truth of ≈[0.5, 0.5] (error ≈0.5, every component finite), while QR recovers
  it to ≈1e-7 — graded against the closed-form solution, not against another SemanticCompute path, so the two
  solvers are not marked by a correlated oracle. One thread per system, `rows`/`cols` baked (keep them small);
  rank-deficient columns are skipped and a near-zero R pivot is floored magnitude-preservingly, a **documented**
  fallback rather than a silent fix — such a system has no unique least-squares solution.
- **`SLParityContract` — a parity check whose tolerance is stated *and justified*, as one value.** The package's
  central claim is "tolerance is stated, never hidden", but `compareFloatBuffers` has a *default* profile, so the
  easiest call to write is the one that states nothing — it reads as verified while silently inheriting a bar that
  may be too loose to catch a defect or too tight for a reduction whose order legitimately differs, and a later
  auditor cannot tell which because the reasoning was never written down. `SLParityContract` makes the
  justification a **required** part of constructing the check (subject + profile + non-empty `rationale`, plus
  optional `expectedCauses` so an *unexpected* divergence cause stays visible). It adds no numerics — it calls the
  same doctor — but the outcome carries the contract, so a failure reports what was compared, the bar, the stated
  reason, and the measured error. Standard tiers (`.bitExact`, `.floatDefault`, `.ulp(n)`) each force a `because:`.
  Written for adopters wiring GPU paths into production: gate the route with a contract and the tolerance decision
  is documented where the check lives instead of in a reviewer's memory.
- **Batched correlation family — many signals against one shared reference, over lags.** `out[j, τ] = Σ_i a[j, i]·b[i+τ]`
  in a single 2D dispatch (one thread per signal × lag). The shipped `Correlation` family handles a single (a, b)
  *pair*, so a caller with thousands of signals to correlate against one reference had to loop on the host — one
  dispatch per signal — which is why whole-volume work (every voxel time-course cross-correlated against an
  arterial-input/reference curve) stayed on the CPU. Batching is a **dispatch** change, not a numeric one: the
  batch index only offsets the read base and never reorders a sum, pinned by a test asserting each row is
  **bit-identical** to the single-pair `CorrelationReference` on that row. It therefore inherits the pairwise
  family's tolerance story rather than needing a weaker one, and ships its own stated bar via
  `BatchedCorrelationFamily.parityContract()` (default float; expected cause: ULP drift from the dot-product FMA),
  which the on-device Metal parity test uses as its gate. Scope stated plainly: ONE shared reference for the batch
  (the perfusion/AIF shape); per-batch reference signals are a different binding layout and are not claimed.

### Changed
- **The catalogue had drifted from the source in BOTH directions, and neither guard could see it.** Established
  from the code — which types exist, which declare a contract, which have lowerings, tests and compile-all
  registrations — rather than from the descriptions, because name and `useWhen` similarity gave wrong answers in
  both directions on three separate attempts.
  - **One implementation was catalogued twice.** `"Euclidean distance transform (separable, exact)"` and
    `"Distance transform (exact Euclidean, per-pixel nearest foreground)"` both resolve to the single
    `DistanceTransform` group — there is no second 2D implementation in Sources, and the nearest-feature
    transform is a separate family with its own entry. `sc_list_families` was reporting a family that does not
    exist. The duplicate is removed and its distinct keywords folded into the survivor so nothing becomes less
    findable.
  - **One built family was invisible.** `AnisotropicEDT3D` has a reference, a contract, three lowerings, three
    compile-all registrations and its own tests — and had no catalogue or guide entry, so the 3D anisotropic EDT
    that the DICOM vessel/centreline path exists to serve could not be listed or recommended. Now catalogued.
  - Net count effect: **−1 +1 = 127, unchanged.** The catalogue simply became true.
  - Neither defect was catchable by the existing guard, which checks catalogue↔guide in both directions: a
    *pair* of entries describing nothing is self-consistent, and an implementation with *neither* entry has
    nothing to be inconsistent with. Both are catalogue↔**implementation** mismatches, and nothing checks that
    axis yet.

### Fixed
- **Sixteen shipped MSL lowerings were never compile-verified — the systemic guard had a hole.**
  `KernelCompileAllTests` exists to compile EVERY catalogued lowering to a real Metal pipeline, because a kernel
  that never compiles otherwise hides indefinitely behind a GPU test that silently falls back to CPU, leaving
  its parity test vacuously green — exactly how the `MVDRWeights` `half` reserved-word bug survived for months.
  The guard had the same hole again: every family added in this release landed with a working lowering and no
  entry here, and their parity tests dispatch through `GPUHarness`, which returns nil when there is no Metal
  device — so on Linux CI those lowerings had **no compile coverage at all**. Also caught `QuantiseTransition`,
  outside the guard since 2026-08-11.

  Found by enumerating lowering entry points from the SOURCE and diffing against the registrations, rather than
  by reading either list — the same code-first method that found the catalogue drift above, and it works for the
  same reason: it does not depend on anything being described correctly.

  All sixteen are now registered, with op enums (`ObliqueRayOp`, `WatershedConnectivity`, and the OLA/WOLA
  `normalise` branch) fanned over their cases so every branch of a shared body is compiled:
  **299 → 325 programs across 168 → 184 lowerings, 0 failed.** No broken kernel was found — the point is that a
  future edit to any of them can no longer break silently.

- `Level-set PDE reinitialisation` keywords narrowed. It claimed "implicit surface" and "segmentation" broadly
  enough that "hausdorff surface distance" scored **67** against it — a confident-looking number for entirely
  the wrong family, and the likely cause of a coverage sweep mis-reading which families already existed.
- **`sc_suggest_families` scores are normalised to 0…100.** The raw hit-sum measured how VERBOSE the query
  was, not how well the family matched: the same correct answer scored 3 for "int8 IQ packing" and 14 for
  "convert float IQ to int8 with scale and zero point". Ranking was right in both cases, but any caller
  thresholding on the absolute number would discard the terse query's correct top hit — which is exactly the
  misreading it produced in the field. The score is now match coverage, comparable across queries; the raw
  sum is retained as `rawScore` for tie-breaking. Genuine gaps now score ~25 where a real match scores 100.
- **A stranded second `## [Unreleased]` heading had release notes filed between two shipped versions.** The 1.9.3
  cut *inserted* a new `## [1.9.3]` heading above the existing `## [Unreleased]` instead of **promoting** it, so
  the old heading survived below — sitting between `[1.9.3]` and `[1.9.2]` and holding the 88→110 catalogue-backfill
  notes. Those notes are now filed under **`[1.9.3]`**, which is where the code actually shipped: the pinned
  catalogue count is 88 at the v1.9.2 tag and 110 at v1.9.3. The version↔top-heading gate passed green the whole
  time, because it only ever inspects the FIRST versioned heading — so `GovernanceGateTests` gains two checks that
  would have caught it: **at most one `## [Unreleased]` heading**, and **version headings strictly descending by
  semver with no duplicates**. Both were verified to fail on the artifact before being committed against the fix.
  Reported by a peer session reviewing release history.
- **`sc_list_families(contains:)` invented matches and missed real ones — so neither answer could be trusted.**
  The filter was a bare `String.range(of:)` over the family *name* only, which failed in both directions:
  - **False positives.** Searching `"RMS"` returned **"DICOM value transfo*rms*"** — an interior-of-word hit.
    Once a filter invents matches, a *negative* result stops meaning "not present", which is the property
    discovery actually depends on. (Exactly the trap fixed in `FamilyCodeDetector`, where `hann` matched inside
    "c*hann*el" and `yin` inside "pla*yin*g".)
  - **False negatives.** Only names were searched, so `"beamforming"` matched **nothing** while
    `sc_suggest_families` recommended the two MVDR families on that very keyword — discovery disagreed with
    recommendation.
  A new `SLTermMatch` matches at **term boundaries** (string start, after a non-alphanumeric, or a camelCase
  hump) across **name *and* discovery keywords**. Prefix-within-word matching is deliberately kept, so `conv`
  still finds `Convolution` and `mul` still finds `MatMul`; only interior hits are rejected. Pinned in both
  directions by `TermMatchTests`, including the end-to-end catalogue checks that `"RMS"` no longer returns the
  DICOM transform family, that `"beamforming"` now reaches MVDR, and that an absent capability (`"hilbert"` —
  there is no analytic-signal family yet) still returns **empty**, so a negative answer stays meaningful.

## [1.9.3] — 2026-08-26

### Added
- **Both advertised MatMul variants are now emissible.** The catalogue calls the family "naive +
  threadgroup-tiled", but `sc_emit_kernel` could only reach the naive one — so the name promised something
  the tool could not deliver. `kernel: "matmul_tiled"` now returns the real tiled Metal kernel (threadgroup
  memory, barriers), and says plainly what it is: a **hand-written Metal specialisation, not an IR lowering**
  (`irLowered: false`), because threadgroup memory and barriers have no representation in the semantic IR.
  Requesting it for portable-C / WGSL / CUDA is refused with that explanation rather than silently handed the
  naive kernel under the tiled name. Reported by an agent working against 1.9.2.

### Fixed
- **`sc_emit_kernel` ignored the `kernel` argument.** Any name other than `matmul` fell through to the affine
  specimen — and the response then echoed the requested name back, so asking for `NOT_A_REAL_FAMILY` returned
  affine source labelled as that family. It now refuses an unknown name and says what exists: the tool lowers
  the two built-in SPECIMENS (`affine`, `matmul`), not catalogue families. A tool that answers a question it
  did not understand is worse than one that refuses.
- **An unrecognised `tolerance` was silently replaced by the default profile** — and echoed back in the
  result, so a caller asking for `"strict"` was told `"strict"` and given the default bar. A typo became a
  pass under a policy that does not exist, which is the false-green class this package exists to prevent.
  Unknown policies, and non-string values, are now refused with a message naming the valid ones. The
  whitelist moved into the library (`SLTolerancePolicyNames`) because it describes what
  `SLCompatibilityProfile` supports; the MCP server is a caller of that, not its owner.

### Added
- **A reverse coverage test for the family usage guide.** The existing test asked "does every catalogue family
  have guidance?" — it could not see a guide entry naming a family the catalogue does not list. That
  asymmetry let **22 orphan entries** accumulate, and `sc_suggest_families` recommended them by name: names
  `sc_list_families` cannot find, `sc_emit_kernel` cannot emit, and nothing can verify against.

  The 22 are **real families** — each has a source file and tests (`BatchedSPDSolve`, `SeparableMedian`,
  `MVDRCovariance`, `Crossfade`, …) — so the suggester is right and the *catalogue is incomplete*. Recorded as
  an exact, shrink-only baseline rather than closed here: reconciling them requires choosing between the
  catalogue's descriptive names and the guide's PascalCase identifiers, and authoring
  `kind`/`dimensions`/`variants`/`hasContract` per family — metadata no test currently verifies and which must
  not be guessed. A new orphan now fails the build, and so does a stale entry left behind once a family is
  catalogued.

### Fixed
- **The family catalogue was a 88/110 subset of the usage guide, so `sc_suggest_families` recommended names
  `sc_list_families` could not show.** Twenty-two families — `BatchedSPDSolve`, `GeodesicDistance`,
  `DistanceTransform`, the MVDR pair, the audio-display set and others — had full guidance, working
  implementations and (for 20 of them) semantic contracts, but no catalogue entry. An agent could be told to
  use a family it could then neither list, inspect, nor verify against.

  All 22 are now catalogued, every field read from the family's own source rather than guessed: declared
  kernel form → `dimensions`, `form:` → `kind`, presence of `semanticContract(...)` → `hasContract` (true for
  20; `GraphAdjacencyCSR` and `SpatialGrid` genuinely have none). The guide's keys were renamed from
  PascalCase to the catalogue's descriptive convention at the same time, so the two indexes finally share one
  vocabulary — which is what makes the suggest → list → emit → verify chain work end to end.

  The coverage test's allowlist is now **empty** and shrink-only, so the asymmetry cannot silently return.
  Catalogue: **88 → 110** families.

## [1.9.2] — 2026-08-26

### Fixed
- **`FamilyCodeDetector` matched its terms inside ordinary words — two traps, both severe in audio code.**
  The window rule was a bare alternation, so `hann` matched the interior of "c-**hann**-el"; the pitch rule
  matched `yin` inside "pla-**yin**-g", "tr-**yin**-g", "appl-**yin**-g" — every `-ying` word in the language.
  "Channel" and "playing" are two of the most common words in the domain this detector exists to read.

  Terms must now begin at a word boundary **or** a camelCase hump, the latter matched case-*sensitively* via
  `(?-i:…)` since the pattern runs case-insensitive — so `applyHann`, `makeHamming`, `hann_window` and
  `yinBuffer` still match while `channel` and `underlying` no longer do. Regression tests pin both directions:
  rejection *and* recall, because a boundary fix that quietly broke real matches would be its own trap.

  Measured on a 2,522-file audio codebase: **1,188 leads → 209**, eliminating **979 false positives** (82% of
  all hits were noise). YIN 593 → 20, window generators 437 → 31. A lead generator's false positives cost more
  than its misses — a tool that fires on prose teaches people to ignore it.

## [1.9.1] — 2026-08-25

### Fixed
- **The verification report's detail panel overprinted its neighbouring column.** The diff table sets
  `white-space: nowrap` on `th`/`td` so a float never wraps mid-number — correct for the numeric columns, and
  wrong for the prose panel added in 1.9.0, which inherited it: the diagnosis ran on a single line and
  overprinted the prescription beside it. Detail cells now set `white-space: normal` with
  `overflow-wrap: anywhere`, and the panel grid's minimum track is `min(240px, 100%)` so it can never exceed
  the table's scroll container.

  Found by pointing `sc_verification_report` at a real divergence — AssistantApp's shipping `SoundBoxBiquad`
  (Float, transposed direct form II) against the same filter in Double — and looking at the rendered output
  rather than trusting the markup. The tests asserted the panels were present and wired; none asserted they
  were legible. A reminder that "the element exists" and "a person can read it" are different claims.

## [1.9.0] — 2026-08-25

### Added
- **`sc_verification_report` — the diagnosis loop, delivered to the client.** The doctor already localised
  every divergence with a typed cause and a mechanical remedy, and `SLVerificationReport` already rendered
  it; what was missing was a path from the MCP server to something a person can look at. The new tool renders
  the report and returns it as an **embedded `text/html` resource** — a client that renders HTML displays it —
  alongside a text verdict and structured `remediesByCause`, so an agent can act without parsing HTML. An MCP
  server cannot open a window; it returns content and the client decides how to show it. Writing to disk is
  opt-in via `path` (a server that silently drops files in someone's tree is a bad guest), and the returned
  `uri` becomes `file://…` when it does.
- **The report's divergences are selectable.** Each divergent row is a keyboard-operable disclosure carrying
  that element's diagnosis, its prescribed fix, and the re-verify step — the diagnose → prescribe → re-verify
  loop closed inside the artifact instead of asking the reader to hold "row 3 was a denormal" in their head
  while scrolling to a separate fixes block. Progressive enhancement: without JavaScript every panel stays
  visible, so a printed or archived report loses nothing.

- **Landing page: alternating section bands, scroll brakes, and animated evidence.** The page now alternates
  ground → tint → ink surfaces (local token overrides, so every component re-grounds itself), with an eased
  scroll-lock engine that settles onto section seams and disables itself under `prefers-reduced-motion`. The
  contract section replays the published `cuda-parity-evidence.txt` verbatim, the metric tiles count up to the
  published figures, and an Apple-HIG pass moved typography to `rem` (text-size preference, not just zoom),
  added safe-area insets and 44pt touch targets, and made the header height measured rather than assumed.
- **Hero scope corrected.** The reference trace used identical maths to the candidate and was painted over
  completely — the legend named a trace nobody could see, on a page about reference vs candidate. It is now a
  tolerance corridor the candidate visibly rides inside and leaves; markers moved onto the candidate curve
  (they were positioned from the reference); the fourth culprit (FMA contraction) was missing and is now
  shown; and the red special-value marker finally has a legend entry, because NaN is a different KIND of
  failure — no ULP distance exists and no tolerance can help.

### Changed
- The report's HTML-injection test asserted `!contains("<script>")`, which was a sound proxy for "no label
  injected a script" only while the generator emitted zero scripts. It now asserts the label never appears
  unescaped **and** that the document contains exactly one script element — strictly stronger, since an
  injected script pushes the count to two.

## [1.8.0] — 2026-08-24

### Added
- **CUDA roadmap stage 2 — float-vector values, lowered through synthesised device helpers.** The provable
  subset of the vector/matrix ABI: `float2/3/4` construct, elementwise `+ − ×` with scalar broadcast on either
  side, `dot`, and `normalize`, as kernel-body VALUES (buffers stay scalar — that is the ABI boundary). The CPU
  reference executor now defines these semantics down to the bit: dot's association is pinned left-to-right
  (a `2²⁴+1+1` test distinguishes the orders bitwise), normalize is `v / sqrt(dot(v,v))` with every op
  correctly rounded, and broadcast matches per-lane scalar arithmetic. CUDA C++ vector types are bare structs —
  no operators, no `dot()` (probe-verified under NVRTC, include-free) — so `SLCUDAEmitter` synthesises
  `sl_vadd/sl_vsub/sl_vmul/sl_vdot/sl_vnorm` device helpers spelling exactly the reference's operation order,
  emitting only the overloads a kernel uses. Scalar expressions still print through the C printer verbatim
  (via a new `render:` injection point), so the scalar subset remains byte-identical to C. Legality now admits
  the float-vector scalar-broadcast shape the reference always implemented. **Proof state:** all shapes
  compile under the real NVIDIA compiler (NVRTC gate, run include-free with `--fmad=false`); Metal executes
  the same kernels on-device bit-exact for construct/arith/dot and within 4 ULP for library `normalize`;
  and the CUDA on-device specimens ran green on two independent RTX 5080 boards (driver 570.211.01) — three
  vector specimens each: the helper pipeline bit-exact, the 2²⁴+1+1 association discriminator holding under
  `.exact` (rounding-ACTIVE data, added after review found the original data FMA-blind), and normalize
  bit-exact. Outside the
  subset, loud emission failures: integer vectors, matrices, vector division, and vector-element buffers are
  rejected on CUDA and C — and on WGSL, which previously declared a `float2`-element buffer as `array<f32>`
  silently (wrong stride, no diagnostic).
- **`cuda-verify.sh --compile-only` now runs the NVRTC gate too** (a compiler library needs no GPU), with a
  toolkit-present false-green check; on driverless hosts the loader is satisfied by a scoped `libcuda.so.1`
  symlink to the link stub — the one sanctioned run-time use, where there is no real driver to shadow. The
  compile gate writes its own artefact (`cuda-compile-gate.txt`) and never overwrites the on-device parity
  evidence.
- **NVIDIA runner kit — the hardware half of the CUDA checkpoint.** Everything needed to run the on-device
  parity gate on a real GPU, and nothing that pretends to have run it: a Swift 6.2 + CUDA Toolkit image
  (`Tools/cuda/Dockerfile`), a one-command gate with an evidence log (`Tools/cuda-verify.sh` — container,
  `--native`, or GPU-free `--compile-only`), an idempotent host provisioner (`Tools/cuda/provision-gpu-host.sh`:
  driver → Docker → NVIDIA Container Toolkit → optional Actions runner), a self-hosted CI job
  (`.github/workflows/cuda-parity.yml`, gated on `CUDA_RUNNER_ONLINE` so a missing runner never leaves checks
  pending), and `CUDA_RUNNER.md` covering routes, costs and failure modes. A `CUDA-DEVICE-ABSENT` marker plus
  greps in both the script and the workflow make a skip on a GPU host a hard failure — the same no-false-green
  discipline as the C-backend and WGSL gates. `Tools/cuda/aws-gpu-runner.sh` rents an EC2 GPU for the length of
  one run and gives it back — throwaway key, security group admitting only the operator's IP, Deep Learning AMI,
  verify, fetch evidence, and terminate from an `EXIT` trap so a failure cannot leave an instance billing.
  `Tools/cuda/bootstrap-swift.sh` covers the container-based providers (RunPod, Vast), where a pod cannot run
  Docker inside itself: it installs Swift — and the CUDA dev files if the image is a runtime one — so
  `Tools/cuda-verify.sh --remote <pod> --native --bootstrap` does the whole job in one command. Verified from a
  bare `ubuntu:24.04` container: Swift installed, toolkit installed, adapter and test bundle compiled and
  linked.

### Changed
- **CUDA is now an EXECUTED backend, not an emission target — and the run that proved it found a real bug.**
  On an RTX 5060 Ti (sm_120, driver 595.71.05, CUDA 12.8), the emitted kernels compiled under NVRTC, launched
  through the Driver API, and matched the CPU reference: **affine bit-exact (`.exact`)**, **matmul under the
  default float profile**, both reported `.executed` rather than `.skipped`. The first attempt on hardware
  failed outright: `SLCUDAEmitter` emitted `#include <math.h>` in its preamble, copied from the C backend, and
  NVRTC compiles device code with **no include search path**, so every kernel was a hard compile error. CUDA
  needs no such include — `fminf`/`fmaxf`/`roundf` are device built-ins — so the preamble now omits it while the
  body printer stays the C one, keeping the numerics identical by construction. The whole structural test suite
  had passed on that unusable source; only a GPU disagreed. Evidence log committed alongside the package.
- **Adversarial execution matrix + NVRTC compile gate, green on two independent GPUs.** Beyond the two canonical
  specimens, a 13-test matrix now executes on device and matches the CPU reference: affine at bounds-hostile
  extents (1×1, 7×13, 257×3), 3D (5×3×7), the folded-4D dispatch (3×4×2×5, every element covered exactly once),
  per-thread `if` + early `return`, ties-away `round`, NaN-skipping `fmin`/`fmax`, ∞ and 0·∞→NaN propagation —
  all `.exact` — plus loop-accumulation matmuls under the float profile and the uint buffer/scalar marshalling
  path. A dedicated NVRTC gate compiles every specimen exactly as the runtime will (same NVRTC, `--fmad=false`,
  no host include paths) and needs only the toolkit, not a GPU — the checkpoint the `math.h` defect proved
  necessary. `cuda-verify.sh` re-runs the whole matrix on a second device when present (`SC_CUDA_DEVICE`):
  13/13 on both RTX 5060 Ti boards. The evidence log now records the git SHA and the exact NVRTC options, and
  strips board UUIDs (they identify the rented machine, not the claim).
- **Single-writable-output + element-type guards on the CUDA *and* portable-C emitters.** Both previously took
  `outputs.last`, silently dropping any second writable buffer from the signature while the body could still
  reference it; and their float-vs-uint parameter split silently REINTERPRETED `.int`/`.bool` elements rather
  than rejecting them (an int buffer came through as `const float*`, bit pattern intact). Both now fail at
  emission — on every host — matching the WGSL rule, with regression tests for the rejection *and* an
  over-rejection guard proving the supported shapes still emit. An adversarial review pass then tightened three
  more seams: extents are classified by NAME, so a float-typed `width` binding bypassed the scalar guard and was
  emitted as `unsigned` — both emitters now reject non-uint extents; the runtime adapter now **sentinel-fills
  the output allocation** (0xCB) because `cuMemAlloc` contents are undefined and stale plausible values could
  have masked a coverage hole; and the 4D specimen writes a coordinate-derived payload, since a read-modify-write
  at the same index cannot detect a bijective-but-wrong z/t recovery. `Package.swift` now also carries `lib64/stubs` on the **link**
  path, without which `-lcuda` cannot resolve inside a CUDA container.
- **`SemanticComputeCUDA` now builds — and building it for the first time found three defects.** Running the
  GPU-free compile check (x86-64 Linux, emulated) revealed that the package had never compiled at all: its
  manifest referenced the core by a name a *path* dependency does not have (identity comes from the directory
  basename, so a worktree checkout broke it — now `.package(name:path:)`), `-lcuda` could not link without the
  driver stub path, and the adapter carried two deprecated `String(cString:)` array initialisers that would have
  included the NVRTC log's NUL padding, plus a needless `var`. Adapter and parity test bundle now compile and
  link cleanly against real `libcuda`/`libnvrtc`, warning-free. **STATUS UNCHANGED WHERE IT COUNTS: CUDA remains
  an emission target — no kernel has yet executed on an NVIDIA GPU.**
- **CUDA runtime foundation — the contract an on-device adapter consumes.** The CUDA backend's names-only metadata
  is replaced by typed, positional launch metadata: `SLCUDAParameter` carries each argument's role, element type,
  buffer/scalar kind, access, byte size, alignment and position, so a runtime marshals `cuLaunchKernel`'s `void**`
  directly rather than re-deriving the ABI from the `SLKernel`. `SLCUDALaunch` adds the verified **physical** grid —
  `ceil(logical / block)` per axis, overflow-safe, validated against CUDA device limits (grid ≤ 2³¹−1 / 65535,
  block ≤ 1024) — with the 4D `depth×time` fold applied explicitly. The name-order arrays remain as derived
  projections, so existing callers are unchanged. Apple-safe and fully macOS-tested.
- **Unified backend identity — `SLBackend`.** One coherent model of three orthogonal axes — lowering language
  (MSL / C / WGSL / CUDA C++), executable target (Metal GPU / CUDA GPU / CPU / WebGPU), and optional accelerated
  implementation (MPS now; cuBLAS/cuDNN/cuFFT later) — with host executability single-sourced through
  `SLBackendAvailability`. `SLBackendKind` and `SLExecutionModel.Backend` are kept as source-compatible façades
  that map onto it, so the two no longer drift as CUDA execution lands (non-breaking; a clean unification would be
  a later 2.0 concern).
- **`SemanticComputeCUDA` — optional NVIDIA-host runtime (companion package).** A separate, build-gated package
  (kept out of the Apple-safe core, which never links the CUDA Toolkit): NVRTC compile under `--fmad=false`
  (IEEE-safe, no fast-math) → PTX → CUDA Driver-API load/launch, marshalling from `SLCUDAParameter`; plus a parity
  harness (`SLCUDAParityHarness`) that classifies no-device → `.skipped`, compile/launch error → `.failed`, and a
  device run → `.executed`, and on-device parity tests (affine `.exact`, matmul float profile). **STATUS: written
  against the Driver API + NVRTC but NOT yet compiled or run on an NVIDIA GPU** — the on-device parity gate on a
  self-hosted NVIDIA runner is the checkpoint that makes it trustworthy, and remains outstanding.

## [1.7.0] — 2026-08-24

### Added
- **Fourth backend — CUDA C++ emission (`SLCUDAEmitter`).** Lowers the generic buffer subset (pointwise 2D/3D/4D)
  of the SLKernel IR to NVIDIA CUDA C++, consuming the same `SLBackendABI` as C/WGSL and reusing the portable-C
  backend's expression/intrinsic printer verbatim — so the body arithmetic, and therefore the numerics, is
  identical to C (`fminf`/`fmaxf` NaN-skipping, `roundf` ties-away, ternary `min`/`max`, no fma contraction, and
  **no helper synthesis** unlike WGSL, since CUDA's device functions already have the right semantics) — combined
  with Metal's one-thread-per-element prologue (global thread id + bounds guard + the folded-4D `t` recovery).
  Wired into the compiler front door as `SLKernelCompiler.compileToCUDA` (the first target to carry `time` for a
  real 4D dispatch). **EMISSION STAGE ONLY:** it produces CUDA C++ + a launch layout and is structurally
  validated; on-device execution parity needs an NVIDIA runtime adapter (a separate optional target), a GPU CI
  runner, and the `--fmad=false` (no-fast-math) compile flag — the CUDA analogue of Metal's `mathMode = .safe`.
  `.cuda` is a lowering target in `SLBackendKind` and `SLVersion.backends` (documented as the languages the IR
  lowers to), while **executability is gated separately and honestly**: `SLBackendAvailability.cuda` reports
  unavailable ("emission available, but this build has no CUDA runtime adapter") and `SLParityRunner.run` takes an
  `availability:` parameter so a skipped CUDA parity attempt reports the CUDA reason, not Metal's — so listing CUDA
  as a target is not an execution overclaim. Out-of-subset forms throw `SLCUDAEmitterError`, never a false-green. Enabled by the
  `SLBackendABI` + logical-4D work above. The "numerics identical to C by construction" claim is now **tested, not
  merely asserted**: a byte-identity test proves `SLCUDAEmitter`'s emitted body arithmetic is character-identical
  to the CPU-executed portable-C backend for every arithmetic statement (both delegate every expression to the
  same printer), and a companion test pins the sole intentional divergence to the value-free `.return` (per-thread
  `return;` vs C's loop `goto` — control flow, no expression). Since portable-C is executed and parity-verified on
  CPU, this is the strongest correctness evidence obtainable without an NVIDIA device. 10 emission tests, plus a
  CUDA availability/skip test covering the emit/execute gate above.
- **3D detection-geometry families** (for 3D object detection / nnDetection / RetinaNet-3D — the AssistantApp
  detection lane). Three new families, catalogue 86 → 88:
  - **`BoxIoU3D`** — pairwise axis-aligned 3D intersection-over-union, one thread per (boxA, boxB): intersection
    is `∏ max(0, min(a₁,b₁) − max(a₀,b₀))` over union, `numA × numB` matrix. Bit-exact CPU↔GPU.
  - **`ROIAlign3D`** — aligned trilinear region pooling (Detectron2/torchvision `aligned=True`, clamp-to-border),
    one thread per output cell averaging `samplingRatio³` trilinearly-sampled points per bin. Bit-exact CPU↔GPU.
  - **`NMS3D`** — greedy 3D non-maximum suppression. Inherently sequential, so the parity-provable parallel core
    is `BoxIoU3D` (GPU-or-CPU) and the greedy walk is a host step — the "family owns the parallel core, sequential
    tail host-side" pattern (as with marching-cubes triangle assembly). Host helper, not catalogued.

### Changed
- **`SLBackendABI` — one canonical binding layout.** A new `SLBackendABI` derives the backend-neutral binding
  classification once from an `SLKernel`: buffers (with element / access / address-space) split into outputs vs
  inputs, extent scalars in canonical order, non-extent scalars, coordinate names skipped, and textures rejected.
  The C and WGSL emitters now *project* this ABI instead of each independently re-deriving classification + extent
  lists; the Metal emitter and `SLResources.extentSource(for:)` share the same canonical extent contract via
  `SLBackendABI.canonicalExtentNames`, so the backends can no longer drift on extent naming. Behaviour-preserving —
  emitted source is byte-identical (823 tests green); each emitter keeps its own native ordering projection
  (Metal's declaration-order slots, C's float/uint arrays, WGSL's storage buffers + packed uniform). This is the
  prerequisite for a fourth backend (e.g. CUDA): it consumes the same ABI rather than duplicating the existing
  emitters' assumptions.
- **Logical 4D dispatch model — `SLGridSize.time`.** `SLGridSize` gains a real `time` axis (defaulting to 1, so
  1D/2D/3D constructions are unchanged), making a 4D logical extent (width, height, depth, time) independently
  representable instead of smuggling time into a pre-folded `depth`. The logical→physical fold — a 4D dispatch
  launches a physical 3D grid whose z carries `depth × time` — is now a single declared transform
  (`SLGridSize.physicalDepth`) consumed by `SLExecutionDerivation`'s 4D branch, `SLMetalEmitter`'s gridShape, and
  `Volume4D.foldedDepth`, replacing three independent inline `depth * time` expressions. Behaviour-preserving: a
  pre-folded caller has `time == 1` (depth × 1 == depth), so existing dispatch is identical (824 tests green). With
  `SLBackendABI`, this completes the two prerequisites for a generic CUDA backend — a 4D dispatch is now expressible
  without assuming Metal's fold.

### Fixed
- **Marching-cubes mesh is now watertight.** `MarchingCubesMesh.triangles`/`surface` fan each intersection
  polygon from its own CENTROID (a new interior vertex) instead of the first polygon vertex. A first-vertex fan
  could place a diagonal ON a shared cube face at ambiguous voxels, and two neighbours choosing different
  diagonals left holes; the centroid fan removes that class of diagonal, so the assembled mesh is a closed
  manifold — verified boundary=0 with χ=2 (sphere), χ=0 (torus), and boundary=0 on a *closed* ambiguity-dense
  field (`MarchingCubesWatertightProbe`). Host-side assembly only — the parity-proven per-cube family record is
  unchanged. This also corrects the earlier `MarchingCubesMeshTests` "~4.4% holes" figure, which was a
  `Float.bitPattern` weld metric artifact (a shared crossing computed as `a+t·(b−a)` vs `b+(1−t)·(a−b)` differs by
  1 ULP), not real holes; the mesh tests now weld by exact grid-edge identity. Adds `triPolygons` (the polygon
  primitive) alongside the low-level `triTable` (first-vertex fan, kept for diagnostics — not watertight).

## [1.6.1] — 2026-08-22

### Added
- **DivergenceZoo specimen `14-large-magnitude-ulp`** — a 2-ULP drift at magnitude 1e6 (absolute error 0.125).
  It is the first specimen where `.default` and `.ulp(1)` *disagree*: the relative tolerance (1.25e-7) waves it
  through, while `ulp(1)` flags it as more than one representable float apart — demonstrating that ULP is
  scale-free where abs/rel is not. Closes a real gap (previously no specimen separated the two policies) and lets
  the landing-page kill-shot demo teach why `ulp` exists (its 4th row now flips between tolerated/FAIL across the
  two policies). CI-locked via `LandingPageZooSyncTests` (now 4 showcased specimens).

## [1.6.0] — 2026-08-22

### Added
- **Prescribed fixes — diagnose → prescribe → re-verify.** Every classified divergence cause now carries a known,
  mechanical `remedy` (`SLDivergenceCause.remedy` / `SLDivergenceDiagnosis.remedy`): overflow → max-shift, NaN →
  guard the divide, reassociation → pin order / compensate, FTZ → disable flush, ULP drift → force/disable FMA or
  state a `ulp(n)` policy, etc. Surfaced everywhere: `sc_diagnose_divergence` (MCP) and the parity CLI `--json`
  gain a per-element `remedy` + a `remediesByCause` map; the HTML report renders a "Prescribed fixes" block; a new
  `verify-and-prescribe` MCP prompt closes the loop for agents. HONEST SCOPE: it prescribes the standard fix and
  re-verifies — it does **not** rewrite your kernel — and where the divergence is legitimate approximation the
  remedy says to state a tolerance instead.
- **Self-contained HTML verification report (`SLVerificationReport`).** Any check — any two float arrays under a
  stated tolerance — can now emit a shareable, single-file audit artifact: the parity verdict, the per-element
  diff table with each divergence's diagnosed cause and ULP distance, and a "Prescribed fixes" block (one remedy
  per distinct cause). It renders exactly what `SLCompatibilityDoctor` + `SLDivergenceDoctor` compute — no new
  numerics — and is deterministic (no timestamps) so a committed sample stays byte-stable. Emitted from the parity
  CLI via `--report <file.html>`. The shipped sample `docs/verification-report.html` shows the diagnose → prescribe
  → re-verify loop closing: a generated softmax kernel that overflows to `∞/∞ = NaN`, then the max-shift fix
  re-verified compatible. A sync test (`VerificationReportTests`) fails CI if the committed artifact drifts from
  the generator — the same no-drift discipline as the landing page ↔ DivergenceZoo check.
- **Numerics-hardening suite — beyond a benign sample.** Four utilities motivated by the "correctness illusion"
  finding (that fixed-shape, small-sample `allclose` checks certify buggy kernels because they never reach the
  dangerous regions):
  - `SLInputBattery` — deterministic adversarial input generation across numeric hazards (large-magnitude /
    overflow, subnormals, exact ties, special values, catastrophic cancellation, sign-mix, boundary values),
    with a seedable SplitMix64. A parity check can now sweep the regions that break implementations instead of a
    benign random sample. Demonstrated: the large-magnitude hazard catches the naive-softmax overflow-to-NaN that
    an ordinary sample calls "correct".
  - `SLDivergenceConcentration` — triage context: is a divergence concentrated in a few elements (defect-like) or
    diffuse across all of them (rounding-like)? Surfaced in the parity CLI (`distribution:` line + `--json`) and
    the HTML report. Context, not a verdict.
  - `SLErrorBound` — a-priori worst-case rounding bounds (`γ_k`, recursive/pairwise summation, dot product) so an
    observed ULP gap can be read against what accumulation *legitimately* produces. Informational — it does not
    decide bug-vs-tolerance, and applies only to ops with known error structure.
  - `SLNumericProfile` / `SLNumericProbe` — measured (not assumed) host FP behaviour: subnormal support and
    whether `a*b+c` fuses to a single rounding. Reported by the parity CLI `--profile`. The struct also represents
    a backend's profile for a device harness to populate.
- **Higher-precision accuracy oracles for softmax & standardise (layer-norm core)** — the "right, not just
  reproducible" pattern extended to the two most-requested ML kernels. `NormalisationReference` gains `Double`
  ground truths (`groundTruthSoftmax`, `groundTruthStandardise`) and the naive counter-examples they beat
  (`naiveSoftmax` overflows to `∞/∞ = NaN` — the FlashAttention/vLLM masked-softmax failure; `naiveStandardise`'s
  one-pass `E[x²]−E[x]²` variance cancels to `NaN` at a large mean). Plus a **transcendental** accuracy pattern
  (Float `exp`/`log` vs the `Double` truth — the CUDA-`log()` "which do I trust?" case). Three new measured
  `AccuracyPatternTests` join summation / log-sum-exp / matmul / L2 — the differentiator is now numbers across
  seven families, not one anecdote. (Softmax, standardise and matmul kernels already shipped; this adds the
  oracle layer, not duplicate families.)
- **Pointwise `divide` + `sqrt` / `reciprocal` / `rsqrt`** — extends the existing `PointwiseBinary` (now
  add/sub/mul/**div**/min/max) and `PointwiseUnary` (now abs/negate/saturate/square/**sqrt**/**recip**/**rsqrt**)
  families. All correctly-rounded under `mathMode = .safe` (rsqrt composed as `1/sqrt(v)`, not the approximate
  builtin), so they stay BIT-EXACT CPU↔GPU. Closes the elementwise-divide/sqrt micro-gap a DiplopiaCorrection
  coverage audit surfaced: it is what lets a fused Adam/AdamW step, a divide-by-norm, and RBF `1/(…)` compose from
  families instead of each needing a bespoke kernel. Parity tests use op-aware input domains (positive for
  sqrt/recip/rsqrt, non-zero divisor for divide).
- **PLL phase-tracker family** (`PLLTrackerReference` / `…Family` / `…Lowering` / `…Runtime`) — batched PI-controlled
  phase-locked loops: one thread per loop tracks a periodic signal's phase/frequency over time (`e = y·cosθ`,
  `ω += ki·e·dt`, `θ += (ω+kp·e)·dt`, wrap), emitting the 2π-robust phasor (cosθ, sinθ) + tracked ω so CPU↔GPU parity
  is clean across the phase-wrap discontinuity. Authored for the DiplopiaCorrection vergence tracker (`VPPLL`) — one of
  the module's GPU-roadmap catalogue gaps. CPU reference + `SLSemanticContract` + MSL lowering + Metal runtime (CPU
  below `gpuMinPLLs`), GPU parity at a stated looser recurrence tolerance.
- **Kuramoto oscillator family** (`KuramotoReference` / `…Family` / `…Lowering` / `…Runtime`) — N all-to-all
  coupled phase oscillators via the mean-field identity, run in ONE threadgroup with **index-order** coupling sums
  so the CPU↔GPU coupling reduction can't reassociate; outputs the 2π-robust phasor (synchronisation order
  parameter host-derivable). The DiplopiaCorrection entrainment gap.
- **Recursive-least-squares family** (`RLSReference` / `…Family` / `…Lowering` / `…Runtime`) — batched adaptive
  readouts with a forgetting factor; keeps the rank-1 covariance correction (whose omission overflowed
  DCESNModule's readout after ~82k steps) and **re-symmetrises P each step** so CPU/GPU covariance stays
  parity-stable; emits ŷ + error, per-thread w/P. The GPU path is for MANY SMALL readouts (`dim ≤
  RLSLowering.maxDim`, register-resident); one LARGE readout (an ESN's `s=[1,u,x]`, `dim≈417`) exceeds the cap,
  so `RLSRuntime.track` opts the GPU out (`gpuSupportsDim(_:)` is `false`) and runs the unbounded CPU reference —
  the intended offline parity-oracle use for the ESN readout, not a fast path (the DC loop is per-tick and
  unbatchable).
- **ESN reservoir family** (`ReservoirReference` / `…Family` / `…Lowering` / `…Runtime`) — leaky-tanh all-to-all
  recurrent state `x = (1−a)x + a·tanh(Wres·x + Win·u)`, one threadgroup with index-order matvecs; the
  DCESNModule reservoir step. GPU parity at a stated recurrence tolerance for all three, per the module's §3.4.
- **Moiré-grating dichoptic-stimulus family** (`MoireGratingReference` / `…Family` / `…Lowering` / `…Runtime`) — a
  per-pixel procedural generator (no input buffer): two rotated spatial sinusoids f0 and f0+Δf summed into a carrier,
  an analytic `0.5+0.5·cos(Δω·u)` beat envelope, and a `tanh` soft-contrast tone-map — the visible core of the
  DiplopiaCorrection therapy shader (`DCMoireEye.metal`). Surfaced by the module coverage audit as a genuine gap (no
  family generates 2D gratings — window generators are 1D tapers). Ports the stimulus faithfully (closed-form
  envelope) while omitting the fragment-only screen-derivative flow proxy and texture blur. Verified under a STATED
  absolute+relative tolerance, not bit-exact, because sin/cos/tanh are not bit-identical Metal↔libm even under
  `mathMode = .safe` — the point being that a therapy device's rendered stimulus becomes *verifiable* CPU↔GPU.
- **`ReservoirRuntime.gpuSupportsUnits(_:)`** — a dispatch predicate reporting whether a reservoir size takes the
  GPU single-threadgroup path (`gpuMinUnits…gpuMaxUnits`) or falls to the CPU reference, mirroring
  `RLSRuntime.gpuSupportsDim(_:)`. Lets a consumer wiring a parity oracle assert the GPU path is actually
  exercised (not a vacuous CPU-vs-CPU comparison) — `gpuSupportsUnits(400)` is `true` for the DCESNModule default.
- **Robust per-column standardise family** (`RobustStandardiseReference` / `…Family` / `…Lowering` / `…Runtime`) —
  per-column median/MAD z-score `(x − median)/max(1.4826·MAD, eps)`, the float selection/quantile primitive the
  DiplopiaCorrection coverage audit flagged as genuinely uncovered (distinct from mean/std `Normalisation` and the
  integer-histogram `Trimmed quantile`). **BIT-EXACT** CPU↔GPU: the only data-dependent step is a comparison-only
  sort, and median/MAD/z are correctly-rounded under `mathMode = .safe`. One thread per column sorts in private
  memory, so the GPU kernel is bounded to `RobustStandardiseLowering.maxRows`; taller columns run the unbounded CPU
  reference (`gpuSupportsRows(_:)`), the RLS pattern.
- **KernelBench-style demo** (`examples/kernelbench-loop/`) — a runnable generate → verify → fix loop with
  SemanticCompute as the correctness layer. The candidate is provenance-agnostic (no CUDA backend needed); a
  planted naive-softmax bug overflows `exp()`, gets diagnosed, is fixed from the cause, and re-verifies. Ships a
  CLI variant (`demo.py`, via the `sc_verify` wrapper) and an MCP agent-loop variant (`demo_mcp.py`) that
  branches on the server's typed `structuredContent` (`causeHistogram`, `compatible`) — no prose parsing.
- **Licence marker + forensic detection** (`SCLicenceMarker`, `Tools/sc-scan`, `docs/COMPLIANCE.md`) — every
  build embeds a stable, self-documenting commercial-licence marker (`SEMANTICCOMPUTE-LICENCE-MARKER/1 …`,
  queryable via `semanticcompute-parity --marker` / `--version`, exposed as `SLVersion.licenceMarker`). A
  dependency-free scanner (`Tools/sc-scan`) detects the marker + distinctive Swift symbol signatures in any
  shipped binary/app/dir (exit 1 on detection, for compliance CI). Plus an SCA-registration package
  (`Tools/sca/NOTICE`, `Tools/sca/semanticcompute.cdx.json` — CycloneDX component,
  `LicenseRef-SemanticCompute-Commercial` + `disclosureRequired`) so a customer's own SCA tooling surfaces it.
  Forensic and honest: it detects and proves undisclosed use, it does not prevent it (only a hosted service
  does), and `COMPLIANCE.md` states that ceiling explicitly.
- **HTML verification reports** (`Integrations/python/sc_report.py`) — a stdlib, dependency-free *pure renderer*
  that turns parity `--json` output into a self-contained, shareable HTML audit artifact: a per-element cause
  map + histogram + summary, light/dark, no source or browser tooling needed. Wired into both demos via
  `--html report.html` (the KernelBench one shows the loop close: v1 diverged → v2 verified). `sc_verify` gained
  a `limit=` argument so the report gets the complete mismatch list; `sc_report` refuses to paint a truncated
  map as agreeing.
- **Ecosystem worked examples** (`examples/ecosystems/`) — runnable demonstrations that SemanticCompute verifies
  the *characteristic* numerical failure each ecosystem is documented to hit: Triton TF32 rounding (triton#6054),
  vLLM cross-GPU reduction order (vllm#11526), FlashAttention causal-mask NaN (#581/#1772). Provenance-agnostic
  (no CUDA/Triton backend needed or implied); the honest basis for "verifies numerics from X" as verification of
  their output.
- **Marching-cubes isosurface family** (`MarchingCubesReference` / `…Family` / `…Lowering` + `MarchingCubesMesh`) —
  the parity-provable numeric core of turning a 3D scalar field (a segmented/greyscale DICOM volume, for NeuroAtlas)
  into a surface mesh: per cube, an 8-bit `cubeIndex` and the linearly-interpolated crossing point on each of the 12
  edges that straddle `iso`, emitted as a dense fixed record so it stays a single float buffer. IEEE-safe (no
  reassociation, no fma) so CPU↔GPU agree to the ULP; host-side triangle-table connectivity assembles a watertight
  mesh (verified: sphere χ=2, torus χ=0 under grid-edge weld). Family #86.

### Changed
- **GPU runtime consolidation.** The single-dispatch family runtimes (YIN, Chromagram-Goertzel, SoftMaskRatio,
  SeparableMedian, SpectralKalman, RobustStandardise, HarmonicFreqEKF / F0EKF, Reservoir, MoiréGrating, PLLTracker,
  MVDR weights / covariance, Kuramoto, RLS) now route through one shared `SLGPURunner` — a single compile / buffer /
  dispatch path with a cached `MetalRuntimeAdapter` — instead of each re-implementing the Metal dance. Behaviour and
  CPU↔GPU parity are unchanged (covered by the existing per-family parity tests); this is an internal consolidation
  that removes duplicated dispatch code, adds gate-crossover benchmarks (`GateCrossoverBench`) and compile-all
  coverage (`KernelCompileAllTests`). Iterated / ping-pong kernels keep their own loop (a `runIterated` helper is
  parked for the second such family).
- **Release plumbing + metadata integrity.** A `ReleaseIntegrityTests` gate fails the build if `server.json`'s
  version ≠ `SLVersion` or any doc's "N families" figure ≠ `KernelFamilyCatalogue.all.count` — release metadata is
  now held to the same no-false-green standard as parity. Linux release binaries (x86-64 + aarch64, static-stdlib,
  stripped) are built with SHA-256 checksums and the CycloneDX SBOM and published to the public `semanticcompute-dist`
  release next to the signed / notarised macOS universal binaries + `.mcpb` — all via the local `dist-sign-release.sh`
  flow (no CI secrets; the private source repo hosts no public releases). `server.json`'s download + repository URLs
  point at the dist repo. The landing page's WGSL claim is narrowed to "validated on every specimen, specimen-executed"
  to match `BACKENDS.md` (full-family WGSL execution parity is still in progress, not claimed).

### Fixed
- **Review hardening — no silent wrong dispatch / invalid module (a verifier must never do the thing it catches).**
  (1) `GPUExecutionDescriptor.derive` folded 4D through to a 1D strategy of `width` threads only — a silent
  under-dispatch; it now folds time into the z axis (`explicit3D`, `depth × time`), matching `SLMetalEmitter`.
  (2) `SLWGSLEmitter` accepted kernels it can't legally emit and produced invalid WGSL — it now **rejects**
  more-than-one writable output (`multipleWritableOutputs`) and non-Float/UInt scalar fields
  (`unsupportedScalarType`, previously mis-declared `Int`/`Bool` as `u32`) rather than emitting a broken module.
  (3) `README` catalogue count corrected (79 → 85). Regression tests added (`ReviewGuardTests`); real naga/tint
  WGSL validation still accepts every specimen. 788 tests green.
- `sc_verify` (Python wrapper) now serialises non-finite values as the CLI's `"nan"/"inf"/"-inf"` tokens, so
  NaN/Inf candidates diagnose correctly instead of failing strict-JSON parsing.
- `Tools/release.sh` verifies the CHANGELOG is in step **before** bumping `SLVersion` (previously the bump ran
  first, so a CHANGELOG mismatch aborted with the version already stranded ahead of the notes → governance red).
- **Usage metrics register across processes.** The default metrics path moved from the temp dir (which differs
  between an MCP-server subprocess and the menu-bar monitor, and is wiped on reboot) to a stable per-user
  location shared by writer and reader — `~/Library/Application Support/SemanticCompute/usage.jsonl` (macOS),
  `$XDG_DATA_HOME/semanticcompute/usage.jsonl` (Linux). The JSONL sink now creates its parent directory (the
  first write couldn't, so a non-temp default would have failed silently). The `semanticcompute-metrics-monitor`
  menu-bar app is refreshed: a version badge, a live/idle recording indicator, an actionable "how to enable"
  empty state, and the by-version / by-platform breakdowns.

## [1.5.0] — 2026-08-14

> **Platforms & verification.** SemanticCompute is **multi-platform and heavily verified**. The CLI, MCP server,
> and library build and pass their test suite on **macOS** (universal, signed + notarised) and **Linux** (x86-64,
> Swift 6.2), with **CI on both**. ~**750 tests** across **170 suites**; the platform-independent suite runs on
> both OSes (the Metal/GPU-*execution* tests are macOS-only by nature). Every kernel family is proven to agree
> with a deterministic **CPU reference** across all three backends it emits — **Metal (MSL) · portable C ·
> WebGPU (WGSL)** — under a stated ULP/tolerance policy, and the **DivergenceZoo** ships **13** canonical
> silent-divergence specimens, each asserting its declared cause (`--zoo all` self-test). Evaluator takeaway:
> it runs, and is proven correct, on macOS *and* Linux — no single-vendor lock-in.

### Changed
- **MCP server upgrades** (`semanticcompute-mcp`), following the `mcp-builder` skill. Every tool now returns
  `structuredContent` (typed) alongside its text, with an `outputSchema` on `sc_check_parity`, so agents branch
  on results instead of re-parsing prose — reinforcing the agent/closed-loop use case. `destructiveHint: false`
  added to all nine tools (the default is `true`); input schemas gained size limits (`maxItems`) and ranges;
  `sc_check_parity` / `sc_diagnose_divergence` reject oversized arrays with actionable errors; `sc_list_families`
  is now paginated (`limit`/`offset` → `hasMore`/`nextOffset`/counts); and `initialize` negotiates the protocol
  version (up to `2025-06-18`) rather than echoing the client's.

### Added
- **MCP Resources & Prompts** (`semanticcompute-mcp`) — a new capability surface beyond tools. Resources expose
  the kernel-family catalogue and the DivergenceZoo as browsable context (`semanticcompute://families`,
  `semanticcompute://zoo`, `semanticcompute://version`, plus `/{name}` and `/{id}` URI templates); three prompts
  ship reusable workflows (`verify-kernel`, `diagnose-divergence`, `find-existing-family`). `initialize` now
  advertises the `resources` and `prompts` capabilities and handles `resources/list`, `resources/templates/list`,
  `resources/read`, `prompts/list`, `prompts/get`.
- **MCP evaluation set** (`evals/mcp/`): 10 read-only, verifiable question/answer pairs (`questions.xml`) plus a
  `verify.sh` regression check that replays the canonical tool calls (and the resources/prompts) and asserts the
  answers — the `mcp-builder` Phase-4 quality gate.

## [1.4.0] — 2026-08-14

### Added
- **Python wrapper `sc_verify`** (`Integrations/python/sc_verify.py`) — a stdlib-only helper so NumPy/PyTorch
  users can feed two arrays straight to the parity doctor: `verify(reference, candidate, tolerance="ulp:1")`
  returns `{agree, diverged, exit_code, report}`. The doctor is provenance-agnostic (the candidate can come from
  CUDA/Triton/Metal/CPU), so this is all a Python user needs; it shells out to the `semanticcompute-parity` CLI.
- **`verify-numerics` SwiftPM command plugin** (`Integrations/VerifyNumericsPlugin`) — `swift package
  verify-numerics --reference ref.json --candidate cand.json [--tolerance ulp:1]` runs the parity doctor and
  surfaces any divergence as an IDE diagnostic (Xcode Issue Navigator) with CI-friendly exit codes (`0` agree /
  `1` diverged / `2` usage) — the deterministic in-editor "results + compare" surface, no MCP/agent required. It
  shells out to the `semanticcompute-parity` CLI (so every flag works, `--zoo` included) and is cross-platform.
  Shipped as a small wrapper package because a SwiftPM command plugin resolves its executable tool dependency by
  a product named after the target, which the hyphenated `semanticcompute-parity` product name otherwise blocks.
- **Linux support for the library, the CLI (`semanticcompute-parity`), and the MCP server
  (`semanticcompute-mcp`).** The verification core — CPU reference, portable-C backend, WGSL emitter, and the
  full divergence-diagnosis engine — now builds and runs on Linux (Swift 6.2), extending reach beyond the
  Apple/WebGPU niche to the CUDA / Triton / PyTorch / vLLM audience the macOS-only binaries could not serve.
  The Metal backend stays Apple-only and compiles away behind `#if canImport(Metal)`; GPU parity tests skip
  cleanly on hosts without a Metal device. Verified end-to-end by building and running the full suite in the
  official `swift:6.2` Linux container — **591 tests / 167 suites green on Linux** (the 155 Metal-only parity
  tests are conditionally excluded), macOS unchanged at **746 / 170** — and the `--zoo all` failure-lab
  self-test passes **13/13** on Linux. Reproduce locally with `Tools/linux-verify.sh`; a new Linux CI job
  (`.github/workflows/ci.yml`) makes it continuous.

### Changed
- **DSL arithmetic operators (`+ - * /`, unary `-`) are now anchored on a symbolic operand type
  (`SLSymbolicExpr`: `SLExpr` / `SLValueRef` / `SLValueHandle`) instead of `SLExprConvertible`.** Previously
  `Float`/`Double`/`Int` also satisfied the operator's parameter type, so plain numeric arithmetic in ordinary
  (non-DSL) code could resolve to the IR-building operator and silently produce an `SLExpr`. macOS's overload
  resolution happened to prefer the stdlib operator, but the Linux compiler did not — surfacing the latent
  ambiguity across ~20 families. Numeric-only arithmetic now always uses Swift's own operators; every
  expression that involves a symbol lowers to identical IR (the full 746-test macOS suite confirms zero
  behavioural change). Source-compatible for all intended DSL usage.

### Fixed
- Parallel reference loops using `DispatchQueue.concurrentPerform` (Perona–Malik, CLAHE, display-enhancement
  blur, spectral-median mask, and the chunked-STFT test) now rebind their buffer pointers as
  `nonisolated(unsafe)` locals, resolving `@Sendable`-capture errors under Linux's libdispatch. The loops
  already write disjoint output ranges, so behaviour is unchanged on every platform.

## [1.3.0] — 2026-08-13

### Added
- **Compensated (Kahan/Neumaier) summation family** (`CompensatedSumFamily`) — an accurate batched reduction,
  lowered and parity-tested (GPU Kahan reproduces the CPU reference bit-for-bit under FMA-off), plus **DivergenceZoo
  specimen #9**: a *real algorithm* where a naive/reassociated reduction silently loses the low-order bits
  (`1e8 + 100×1 − 1e8` → 0 instead of 100) and `SLDivergenceDoctor` catches it. The first family whose naive port
  genuinely diverges — the sharpest "it caught a real bug" demo.
- **Mel spectrogram + DCT-II / MFCC families** (`MelSpectrogramFamily`, `DCT2Family`, `MFCCReference`) — the
  audio-ML / MIR front end STFT alone doesn't reach: a triangular mel filterbank + log-mel, and an orthonormal
  DCT-II for cepstral coefficients. Each has a CPU reference, contract, MSL lowering, and on-device parity test
  (the cos-heavy DCT under a stated, honest tolerance).
- **`SLAccuracy` — quantified accuracy vs a higher-precision ground truth.** A product-level primitive (max abs /
  rel error, RMSE, worst ULP) that is the accuracy counterpart to the parity doctor: parity asks whether two Float
  backends *agree*; `SLAccuracy` asks how far a Float result is from a `Double` truth. `CompensatedSum`, the new
  `LogSumExp`, and `MatMul` now ship a `Double` `groundTruth`, and `AccuracyPatternTests` **measures** the pattern
  across all three (naive summation ~100 % wrong vs exact; naive log-sum-exp overflowing to ∞ vs stable; length-512
  matmul accumulation quantified at ~7e-7 relative). "Accuracy, not just parity" is now numbers, not one anecdote.
- **Log-sum-exp family** (`LogSumExpFamily`) — the overflow-safe `m + log(Σ exp(x − m))` (softmax / attention /
  logistic denominator), with a `Double` ground truth and DivergenceZoo specimen #13 (naive `log(Σ exp(x))`
  overflowing to +∞ where the stable form returns the right answer). CPU reference + contract + MSL lowering +
  on-device parity under a stated transcendental tolerance.
- Catalogue now **79 families**.
- **Directional infinity causes.** `SLDivergenceCause` now distinguishes `overflowToPositiveInfinity`,
  `overflowToNegativeInfinity`, `infinitySignFlip` (+∞ vs −∞) and `infinityCollapse` (reference ∞ → candidate
  finite) instead of one umbrella `.infinity`, and the classifier no longer mislabels a candidate that *saturated*
  an infinity as "the reference overflowed". Three new DivergenceZoo specimens (10–12) cover them, and the CLI
  `--zoo all` self-test asserts every specimen still diagnoses to its declared cause. Diagnostic labels only — no
  pass/fail verdict changes (the tolerance doctor already separated +∞/−∞/∞-vs-finite via IEEE comparison). The
  legacy `.infinity` case is retained for source/`Codable` compatibility but is no longer emitted.
- **Cause classifier over MCP.** New read-only tools `sc_diagnose_divergence` (per-element cause + ULP distance +
  hedged explanation + a cause histogram) and `sc_zoo` (list or run a `DivergenceZoo` failure specimen), so the
  "it tells you *why* it diverged" logic is reachable from any MCP agent, not just the CLI and tests.
- **CLI `--zoo all`** runs every failure specimen, asserts each diagnoses to its declared cause, and exits
  non-zero on a mismatch — a demo and a CI self-test in one; `--zoo --json` / `--zoo all --json` for machine output.
- **DivergenceZoo is now the single source of truth for the demo.** `DivergenceZoo.exportJSON()` (and
  `semanticcompute-parity --zoo export`) emit a canonical per-specimen / per-tolerance table, and
  `LandingPageZooSyncTests` pins the landing page's interactive kill-shot matrix to the live doctor — so the
  published demo can no longer silently drift from the code it demonstrates.

### Changed
- **Positioning: parity vs numerics.** README hero, the landing page, `MCP.md`, and the launch/pricing copy now
  distinguish *parity* (two backends **agree** — necessary, not sufficient, since they can agree on the same wrong
  answer) from *numerics* (the answer is **right** against a higher-precision ground truth). `sc_check_parity`'s
  comparator is provenance-agnostic, so with a ground-truth reference it is an accuracy check; `CompensatedSum` is
  the shipped exemplar. Dropped the "parity measures correctness" conflation.
- **Claims made test-backed + a doc-accuracy pass.** Added `CompensatedSumTests.doctorAsAccuracyCheck`, which
  routes the `Double` ground truth *through* `SLCompatibilityDoctor` as the reference — so "the same doctor becomes
  an accuracy check" is now proved by an executing test, not merely asserted in the docs; and tightened the GPU
  Kahan parity assertion to the **exact** tolerance so the "bit-for-bit" wording is earned. Corrected stale/
  understated docs: version strings → 1.2.0 (README + landing page), source/test counts, the WGSL "cross-vendor"
  wording → "a second, independent toolchain", and the landing hero "to the last bit" → "to the ULP".

### Fixed
- **L2-normalise is now overflow-safe** (`NormalisationFamily`). The reduction uses the divide-by-max / hypot form
  (`m = max|x|; ‖x‖ = m·√Σ(x/m)²`) in both the CPU reference and the MSL lowering (changed identically, so CPU↔GPU
  parity still holds), so a large-magnitude row no longer overflows `Σx²` to +∞ and silently collapses to
  all-zeros. Sub-ULP-identical for normal magnitudes; tiny near-zero vectors now return the true unit vector rather
  than the old `eps`-damped result (softmax / standardise unchanged). `groundTruthL2` / `naiveL2` added, and L2 is
  folded into the measured accuracy pattern (`AccuracyPatternTests`) with a regression test for the |x|=1e20
  overflow the fix closes.

## [1.2.0] — 2026-08-12

### Added
- **Divergence cause diagnosis** (`SLDivergenceDoctor` / `SLDivergenceCause`) — infers the *likely cause* of a
  CPU↔backend divergence (FMA/rounding ULP drift, denormal flush, NaN generation, overflow, signed zero,
  sign-flip/reassociation, numeric divergence), so the doctor explains *why*, not only *where*. Heuristic and
  honestly hedged; unit-tested.
- **DivergenceZoo** — a typed catalogue of the canonical silent GPU↔CPU divergences (the "failure lab"), one
  source of truth consumed by the tests, the CLI, and the landing page.
- **`semanticcompute-parity` CLI** — run the parity doctor on your OWN reference/candidate arrays (JSON files or
  stdin) with per-element cause diagnosis and CI-friendly exit codes (0 agree / 1 diverged / 2 error); `--zoo`
  runs a failure-lab specimen. Attached to releases alongside the other binaries.
- **Interactive kill-shot** on the landing page — clicking a tolerance policy (`.exact` / `.default` / `.ulp(1)`)
  re-classifies the divergence table live (self-contained JS; verified in-DOM).

### Changed
- **Repositioned as "numerical verification for heterogeneous compute"** (README + landing hero) — leading with
  the parity doctor as the product rather than "GPU compute".
- **Pricing** (`PRICING.md`): Pro £25 → £49, Enterprise "from £15k" → "from £20k"; Team/Business/Hosted listed as
  early access (not priced until the hosted service exists).
- Moved the Apache-2.0 Change-Licence text to `licenses/Apache-2.0.txt` and corrected stale Apache-2.0 / v1.0.0
  claims on the Pages site (BSL 1.1 throughout).

## [1.1.0] — 2026-08-12

### Added
- **Usage-metrics monitor** — `SCMetricsReader` (tested JSONL parse + aggregation of the opt-in metrics) plus
  `semanticcompute-metrics-monitor`, a macOS menu-bar applet that tracks the metrics file live (totals broken
  down by tool / backend / outcome / kind / family / tolerance). Reads only the local operator-enabled file; no
  network, no PII. See `METRICS.md`.
- **Distribution & launch prep** — `.spi.yml` (Swift Package Index docs), `server.json` (MCP registry manifest,
  pointing at the latest release's `.mcpb`), `Tools/make-mcpb.sh` (builds a **universal** MCP binary + a `.mcpb`
  bundle + a Homebrew/direct tarball) and `Tools/make-metrics-app.sh` (bundles the metrics monitor as a menu-bar
  `.app`) — both **attached to every GitHub Release** by `release.yml`. Plus launch + blog copy under `marketing/`.
- **Harmonic-frequency EKF family** (`HarmonicFreqEKFReference` / `…Family` / `…Lowering` / `…Runtime`) — a
  batched per-track Extended Kalman tracker with state `[A, ω]` (linear amplitude, angular frequency), random-walk
  dynamics, and a nonlinear log-magnitude measurement plus a direct frequency measurement (the row that makes ω
  observable). It is exactly the `[A, ω]` marginal of `KalmanHarmonics.HarmonicFreqEKFModel`'s per-partial block —
  that model's block-diagonal F/H/Q/R and the φ→(A,ω) decoupling let the joint 3P EKF factorise into independent
  2-state trackers, one GPU thread each (data-parallel over sources/partials, sequential over frames). CPU
  reference + `SLSemanticContract` + MSL lowering + Metal runtime (CPU fallback below `gpuMinTracks`), with GPU
  parity under a stated looser recurrence tolerance. Backs the Acoustician "studio"-tier per-partial refinement.
- **Harmonic-fused f0 EKF family** (`HarmonicF0EKFReference` / `…Family` / `…Lowering` / `…Runtime`) — the studio
  "comb centre" refiner: a batched per-series constant-velocity EKF with state `[f0, f0dot]` that fuses K
  per-harmonic log2-f0 observations (weighted mean, in the perceptually-uniform log/cents domain) into a single
  scalar nonlinear `log2(f0)` measurement update. The CV state tracks glissando/vibrato with low lag — the studio
  upgrade over a plain per-frame f0. Complements the per-partial `HarmonicFreqEKF` (different pipeline stage: this
  is the fundamental trajectory, that is each partial's amplitude+frequency). CPU reference + contract + MSL
  lowering + Metal runtime (few sources ⇒ CPU path; GPU for large batches), GPU parity at a stated tolerance.

## [1.0.0] — 2026-08-11

First tagged release. One semantic IR (`SLKernel`) lowered through one optimising front door
(`SLKernelCompiler`) to three backends, each proven to agree with a deterministic CPU reference under a
stated tolerance (`SLCompatibilityDoctor`).

### Added
- **Three backends over one IR**: Metal (`SLMetalEmitter`), portable-C (`SLCEmitter`), and WGSL/WebGPU
  (`SLWGSLEmitter`). WGSL is naga-validated and execution-parity-tested on a real WebGPU device (wgpu → Metal),
  diffed against the CPU reference — the same contract Metal/C satisfy.
- **Tolerance policy** `SLNumericTolerance` including scale-free **ULP** distance, plus shape-aware mismatch
  reporting from `SLCompatibilityDoctor`.
- **Version + capability manifest** `SLVersion` (backends, capabilities), for dependency pinning and gating.
- **MCP substrate** — the `semanticcompute-mcp` stdio server exposing `sc_check_parity`, `sc_ulp_distance`,
  `sc_list_families`, `sc_emit_kernel`, `sc_version`, `sc_suggest_families`, `sc_detect_in_code`; annotated
  read-only. See `MCP.md`.
- **Discovery** — `FamilyUsageGuide` (deterministic family suggestion) and `FamilyCodeDetector` (heuristic
  code→family shape match).
- **Opt-in usage metrics** (`SCUsageMetrics`) — privacy-by-design adoption measurement: off by default, PII-free
  by construction, operator opt-in only. See `METRICS.md`.
- **Governance** — CI parity-ran false-green gate, `GovernanceGateTests` (catalogue/guide integrity +
  version↔changelog sync), PR checklist, `RELEASING.md`, and the `Tools/vet_family.sh` / `Tools/release.sh`
  helpers.
- **Business Source License 1.1** (source-available): free for evaluation and non-production use plus a 7-day
  production trial; continued production use then requires a commercial licence; each version converts to
  **Apache-2.0** (kept as `licenses/Apache-2.0.txt`) on its Change Date. Contributor CLA (`CONTRIBUTING.md`, `NOTICE`)
  preserves the relicensing path; commercial tiers in `PRICING.md`.

### Changed
- **UK English throughout** — docs, comments, and public identifiers/rawValues/filenames (e.g.
  `KernelFamilyCatalogue`, `SLKernelOptimiser`, `SLKernelLegaliser`, `NormalisationFamily`,
  `QuantiseTransitionFamily`, `NormOp.standardise`). Deliberate exceptions kept for correctness: the GPU builtin
  `normalize` the `SLIntrinsic` mirrors, and Apple APIs (`vDSP.hanningDenormalized`, `String.capitalized`,
  `JSONSerialization`).

[Unreleased]: https://github.com/entertrainment/semanticcompute/compare/v1.22.1...HEAD
[1.22.1]: https://github.com/entertrainment/semanticcompute/compare/v1.22.0...v1.22.1
[1.22.0]: https://github.com/entertrainment/semanticcompute/compare/v1.21.1...v1.22.0
[1.21.1]: https://github.com/entertrainment/semanticcompute/compare/v1.21.0...v1.21.1
[1.21.0]: https://github.com/entertrainment/semanticcompute/compare/v1.20.0...v1.21.0
[1.20.0]: https://github.com/entertrainment/semanticcompute/releases/tag/v1.20.0
[1.3.0]: https://github.com/entertrainment/semanticcompute/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/entertrainment/semanticcompute/releases/tag/v1.2.0
[1.1.0]: https://github.com/entertrainment/semanticcompute/releases/tag/v1.1.0
[1.0.0]: https://github.com/entertrainment/semanticcompute/releases/tag/v1.0.0


---

<!-- FINDER-STATUS:BEGIN (auto) -->
> 📊 **Doc status:** 🟢 Complete · **100%** complete · top = 1.22.1; links and SLVersion are governance-aligned
> <sub>Finder tags: `Complete`, `▓▓▓▓ 75–100%` · auto-assessed 2026-09-13</sub>
<!-- AGENTS: after materially changing this module, refresh status+tag → `python3 Tools/MarkdownStatusQuickLook/tagkit.py set <THIS_FILE> <status> <percent> "<note>"` (status: complete|complete_improvable|in_progress|not_done|superseded|irrelevant). Protocol: Tools/MarkdownStatusQuickLook/DOC-STATUS-AGENTS.md -->
<!-- FS-HASH:9da99c6b -->
<!-- FINDER-STATUS:END -->
