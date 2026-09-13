# SemanticCompute v1.22.1 — texture truth, FDN reverb, bounded CBOR-LD, and the complete binary cut

SemanticCompute 1.22.1 is the complete public distribution of the work shipped since 1.20.0: the Imager
texture-validation lane, executable semantic texture kernels, an FDN late-reverb family, the adversarial stress
lab, and twelve structured-data families for CBOR-LD consumers. The catalogue moves from 170 families in 1.20.0
to 183. The patch number records a distribution repair: 1.22.0's source was tagged and its macOS binaries were
signed and notarised, but its public release omitted both Linux architectures, checksums, the SBOM, notice and
CUDA evidence, while the public landing page still presented the 1.13.0 surface.

This cut makes source commit and artifact identity one contract. Each Linux binary is built natively by the tag
CI job, stamped with that exact commit, smoke-tested before packaging, and rejected if its payload architecture
does not match its filename. The macOS pair is built universal, signed on a system-volume copy, verified across
both slices, notarised, and checked again after archive extraction. Publication refuses an incomplete asset set.

## Added

### External texture validation for complete consumer shaders

`SLExternalMSLTextureValidator` and the MCP tool `sc_validate_metal_texture` accept complete consumer-owned MSL,
raw input buffers, an output texture description and an independently supplied CPU reference. They compile,
dispatch, read back `rgba16Float` or `rgba32Float`, and compare row-major RGBA channels through
`SLCompatibilityDoctor`. Preflight, compilation, dispatch, readback and parity each report `executed`, `skipped`,
`unavailable` or `failed` with a reason, so a compile-only observation cannot turn into a pixel-parity claim.

The lane came from Imager's procedural phase-scope and texture-writing kernels. Those kernels already contain
their computation in MSL; their problem was the absence of a substrate-level way to execute the complete shader
and compare its pixels. The validator is that bridge. It does not claim an arbitrary semantic contract can invent
an executable body, and it does not smuggle consumer-specific shader meaning into the semantic IR.

### Generic pointwise2D texture-writing execution

A legal `SLKernel` whose body reads or writes `texture2D<Float4>` now passes through the normal optimisation and
lowering front door to executable `texture2d<float>` MSL. Texture indices survive lowering, Metal's texture
argument namespace is represented in `SLBackendBinding`, and `MetalRuntimeAdapter` binds caller-owned
`MTLTexture` objects. Dispatch derives from the writable texture's intrinsic extent and refuses mismatched shapes.
The CPU texture executor and an exact CPU-to-Metal passthrough fixture close the reference-to-device loop.

The supported semantic subset is deliberately stated: pointwise2D Float4 reads and writes. Samplers, filtered
coordinates, other texture dimensions and formats, and texture execution on non-Metal backends remain explicit
gaps. A contract describes access and effects; `SLKernel.body` remains the executable source.

### FDN late reverb

The new FDN late-reverb family is a configurable feedback-delay network built around a Householder feedback
matrix. It carries per-line decay gains, one-pole damping, wet/dry mix and explicit state across processing
blocks. The state boundary is part of the family rather than hidden in a host object: callers can prove a split
block and a continuous block mean the same thing under the stated contract.

The family ships through the full SemanticCompute path: deterministic CPU reference, semantic contract,
legality, derived read/write effects, generic Metal lowering, catalogue and usage-guide discovery, and audio/state
parity tests. It extends the signal/DSP lane without introducing a second audio engine.

### Recursive adversarial stress lab

`SC_STRESS=quick|full Tools/stress.sh` sweeps the entire family library rather than replaying one friendly fixture.
Its four tiers cover every catalogued lowering over an adversarial shape ladder; CPU-to-Metal execution under
input hazards with automatic divergence shrinking; random well-typed IR through Metal and portable C; and
catalogue-to-guide-to-symbol-index coverage. Reports state what did not execute as well as what failed.

The first quick run found 394 tier-B and three tier-C criticals. They were not converted into green by widening a
tolerance. The lab instead drove fixes for NaN ordering, degenerate `atan2`, FMA association, undispatchable
threadgroups, singleton windows, binding lifetime, resize interpolation, stencil literals and family discovery.

### Twelve CBOR-LD and structured-data families

Whole JSON/CBOR documents are recursive, allocate dynamically and may load remote contexts asynchronously. Those
operations do not fit a dense GPU dispatch. The new lane therefore introduces `SLStructuredValue` at the host
boundary and freezes it into fixed-width nodes, child indices and a byte pool under explicit depth, node and byte
limits. Device work sees bounded buffers; the CPU reference remains the authority for recursion, I/O and rich
diagnostics.

The twelve catalogued families are:

1. **Batched SHA-256 (variable byte spans).** One bounded sequential SHA-256 walk per record, producing eight
   exact UInt32 digest words. The batch dimension is parallel; block order within a digest is not reassociated.
2. **Byte diff (mismatch mask / count / first mismatch).** Exact unsigned-byte comparison with a per-byte mask,
   mismatch count and first divergent offset, so encoded output failures are localised rather than reported as a
   single false value.
3. **Batched CBOR structural scan.** A bounded parser for definite-length records that reports token count,
   maximum nesting depth and malformed status. Indefinite and reserved lengths refuse instead of being guessed.
4. **UInt prefix scan and stream compaction.** Exact UInt32 exclusive scan plus a stable keep-mask compaction,
   used by measured-size and output-offset stages.
5. **Byte histogram and Shannon entropy.** A 256-bin exact byte histogram with host-side entropy derived from the
   counts, keeping the integer accumulation separate from its floating-point interpretation.
6. **Segmented canonical CBOR key ordering.** RFC 8949 deterministic length-first unsigned-byte ordering with
   input position as the exact-duplicate tie-break.
7. **Batched UTF-8 validation.** A strict state walk that catches overlong forms, surrogate encodings, truncation
   and invalid continuation bytes before text enters CBOR-LD processing.
8. **Batched Base58 / multibase codec.** Bitcoin-alphabet Base58 plus the `z` multibase prefix, using bounded
   grade-school conversion and a caller-supplied output stride. The device encoder refuses records beyond its
   declared ceiling rather than overwriting the next lane.
9. **Batched unsigned varint codec.** Exact variable-width UInt encoding/decoding with explicit per-value lengths.
10. **Frozen context / type-table probe.** Deterministic lookups against a table frozen before dispatch, with an
    explicit missing sentinel instead of mutable dictionary state.
11. **Whole-document CBOR-LD plan.** `CBORLDDocumentReference.prepare` loads supplied contexts asynchronously,
    inherits term maps, rewrites known keys, flattens under limits, performs an exact measure/scan/allocation pass
    and writes deterministic RFC 8949 CBOR. Its device lowering operates only on the already-frozen key plan.
12. **CDDL parse + flat validation VM.** Grammar parsing, AST construction, recursive validation, regex controls
    and path-rich diagnostics stay on the CPU. Supported root-kind, required-key and signed-32-bit range checks
    compile to a bounded exact-integer instruction stream for batch execution.

Every device stage has a deterministic CPU reference, exact Byte/UInt32 comparison, semantic contract, legality,
Metal lowering, catalogue and usage-guide entries, compile-sweep coverage and bit-exact Apple-GPU fixtures. The
release benchmark runs the same flat CDDL instruction stream over 32K documents with a dead-code-elimination
barrier: 240.9 microseconds, 136.0 million elements per second and 4.93x over the matching CPU flat-plan oracle on
the release machine. That number is evidence for this bounded plan, not a promise for arbitrary document loading.

## Changed

The 1.21 texture work preserves the complete 1.20 public API. Texture dispatch is an overload; existing
buffer-only `dispatch`, `dispatchBatch` and `SLBackendProgram` initialisers remain. The backend reuses the existing
semantic texture binding kind, and `swift package diagnose-api-breaking-changes v1.20.0` found no breaking API.

The backend contract now records what Metal actually did rather than what its `.safe` label appeared to promise.
In a 65,536-input probe, the single expression `a*b+c` fused on 14,269 inputs while a separately stored product
fused on none. `BACKENDS.md` records contraction scope, the toward-zero Float representation of pi, subnormal
comparison behaviour, the degenerate `atan2` boundary, encoder lifetime on errors and undispatchable geometry.

Linux releases now use native tag-CI jobs for both x86-64 and AArch64. Both products statically link the Swift
runtime, keep glibc dynamic, run the failure lab before packaging and expose their exact source commit through
`--version`/`sc_version`. The public installer selects the matching architecture instead of silently labelling an
emulated or native-only fallback as another platform.

The public landing page, install guide, quickstart, SBOM and release metadata now advance with the source release.
The old `v1.13.0` global identity was a deployment failure: the private source page had already reached 1.22, but
the distribution repository that GitHub Pages serves had not received the later document.

## Fixed

`BatchedDTFT`'s old tolerance described only FMA contraction and ignored cross-library `sin`/`cos` drift. A
64-tap, 256-frequency fixture measured 2.78e-5 maximum difference, so the family now states a 5e-5 combined
absolute/relative contract with the measurement and causes. The package-wide default remains unchanged.

The stress lab reduced two Metal-versus-C failures to `clamp(NaN, -1, 1)`. Five implementations had different
answers: comparison chains propagated NaN, backend built-ins were undefined or indeterminate, and Swift's answer
depended on nesting order. Generic IR now uses one IEEE-754 minNum/maxNum contract, the constant folder and CPU
interpreter share it, and Metal spells float clamp as `fmin(fmax(value, low), high)`. Inverted bounds deliberately
produce `high`; the sign of a zero tie remains unpinned.

`ComplexPolar.phase` used Metal's division-based `atan2` over the 0/0 and infinity/infinity quadrants, returning
NaN or a sign-flipped angle where the CPU defined zero, pi or quarter-pi values. The lowering now reconstructs all
nine degenerate rows and only sends finite non-zero pairs to the built-in. A first fix was still one ULP wrong on
the ±pi rows because it used nearest pi instead of the platform's toward-zero float; the final rows are bit-pinned.
The family's stress criticals fell from 54 to zero.

`Kuramoto` and `Reservoir` emitted one-threadgroup kernels beyond Metal's 1,024-thread ceiling. Those programs can
compile and then silently write nothing without API validation. Their lowerings now expose and enforce maximum
sizes; the unbounded CPU references remain available. `FFTLowering.butterflyStageMSL(n: 1)` similarly refuses its
zero-grid non-operation, while the valid length-one identity stages remain expressible.

Symmetric Hann, Hamming and Blackman windows divided by `length-1` at length one. The CPU returned NaN and Metal
returned three unrelated finite values. Both now return the conventional singleton `[1]`; periodic Hann,
`sineTaper` and Kaiser retain their own well-defined singleton conventions.

`Resize2D.linear` and `Resize3D.linear` differed by as much as 30,858 ULP because Metal fused the coordinate map
and left side of each interpolation while Swift did not. Both sides now spell the same fused operations and agree
bit-for-bit on ordinary and inf/NaN fixtures; 896 resize stress cases now pass. Box-blur literals had separately
been rounded to six significant digits (`1/9` became `0.111111`) and their multiply-adds were contractible; the
emitters now use round-trip literals and reference association, closing all 672 stencil cases.

`Crossfade` used two different float values of pi, so its last sample did not land on pure `b` and infinite inputs
could change sign between CPU and Metal. The constant and endpoint behaviour are now pinned. Seven other family
references that used Swift min/max now share the same ordering contract as their kernels; this also prevents a NaN
coordinate from reaching `Int(_:)` and trapping inside `SpatialGridReference`.

`MetalRuntimeAdapter` previously created an encoder before resolving all bindings. A missing binding then threw
with a live encoder, turning a typed error into a process assertion. Bindings are resolved before encoder creation.

`FamilySymbolIndex` ignored members declared in public extensions and misattributed nested declarations. It now
collects extension members across files, handles attributes and conformances, records only the correct declaration
depth and has an executable regeneration path. Thirty-five selectors became discoverable without hand-editing the
index.

## Verification and evidence boundary

- The 1.22 source gate passed 1,335 tests in 286 suites.
- The compile sweep covered 384 programs across 242 lowerings with zero failures.
- All twelve structured-data stages have bit-exact Apple-GPU fixtures for their bounded device work.
- The tag CI builds and tests native Linux x86-64 and AArch64 artifacts independently.
- The published CUDA log records real NVRTC compilation and on-device execution on NVIDIA hardware. If the
  self-hosted runner is offline for this tag, that file remains historical, commit-identified evidence; it is not
  represented as a fresh 1.22.1 device run.
- The adversarial stress lab remains a separate opt-in surface. Its unresolved cases stay visible rather than being
  absorbed into the ordinary green suite.

## Assets

The release contains twelve uploaded assets, plus GitHub's two automatic snapshots of this public distribution
repository:

- `cuda-compile-gate.txt`
- `cuda-parity-evidence.txt`
- `NOTICE`
- `semanticcompute-mcp-linux-aarch64.tar.gz`
- `semanticcompute-mcp-linux-x86_64.tar.gz`
- `semanticcompute-mcp-macos-universal.tar.gz`
- `semanticcompute-mcp.mcpb`
- `semanticcompute-parity-linux-aarch64.tar.gz`
- `semanticcompute-parity-linux-x86_64.tar.gz`
- `semanticcompute-parity-macos-universal`
- `semanticcompute.cdx.json`
- `SHA256SUMS.txt`

