# SemanticCompute v1.23.0 — licensed distribution, exact audit families, and live verification

SemanticCompute 1.23.0 turns the post-1.22 engineering work into a coherent commercial release. It adds five
catalogued exact-integer/storage families, including three complete-audit families, a bounded Live byte-parity service,
typed MacResilience MCP adapters, a hash-only entitlement control plane, and fail-closed licensing in every native
distribution executable. The catalogue now contains **188 families** and the MCP server exposes **20 tools**.

The native release remains a numerical verification substrate. It does not claim that arbitrary Swift, arbitrary
MSL, recursive documents, filesystem traversal, or remote repositories can be converted into safe GPU kernels.
Host work remains explicit, CPU reference truth remains authoritative, and every GPU family retains a stated
semantic contract and parity gate.

## Commercial distribution and entitlement lifecycle

The public `semanticcompute-parity`, `semanticcompute-mcp`, and `semanticcompute-live` binaries are compiled with
`SC_COMMERCIAL_DISTRIBUTION`. Compute operations fail closed unless all of the following are true:

- `SEMANTICCOMPUTE_LICENCE_KEY` contains an active `sc_lic_…` entitlement;
- the binary carries the exact 40-character source commit stamped during the release build;
- the entitlement has not expired or been disabled;
- a metered plan has remaining credits;
- the persistent installation identity is within the entitlement's device ceiling; and
- the licence service can authorise the named executable and operation.

Help, version output, MCP initialization/tool discovery, and Live health remain available for diagnosis. The key
is sent only in an HTTPS `Authorization` header to the configured SemanticCompute licence service. The server
stores a peppered key hash and SHA-256 device hashes, never the plaintext key. The plaintext key appears once in
the authenticated issue response.

The sales-assisted administration API can now issue, inspect, renew, reactivate, disable, and reset device
bindings. Renewal extends from the later of the current expiry or the current time, can add bounded credits, and
refuses to lower the device ceiling beneath current usage. Issue, renewal, disable, and device-reset operations
are recorded in the `licence_admin_events` audit table. Key rotation remains explicit: issue a replacement, deliver
it securely, then disable the old entitlement.

The release gate runs both sides of the contract against the exact packaged bytes:

1. no licence key must refuse CLI, MCP, and Live execution; and
2. a dedicated internal release-canary entitlement must authorise and execute all three products.

Source builds do not define `SC_COMMERCIAL_DISTRIBUTION` and continue to follow the repository's Business Source
License terms. This technical gate controls 1.23.0 and later distribution builds; it cannot revoke legacy binaries
that were already downloaded.

## New exact families for storage, checkout, and resilience analysis

The catalogue grows from 183 to 188 families with exact evidence lanes designed for large checkout/storage data
sets:

- `APFSMetadataChecksum` validates APFS object-block Fletcher-64 checksums from explicit byte spans, excluding the
  stored checksum field and reporting valid, mismatch, invalid-span, or invalid-length status.
- `VariableSpanSetOverlap` compares host-normalised sorted spans and produces exact overlap evidence without
  converting offsets or counts through floating point.
- `BatchedSourceLineLexicalEvidence` scans explicit byte-rule tables over bounded source lines.
- `SegmentedStableUInt64OrderingRanks` assigns deterministic ranks with path and input-order tie breaks.
- `BatchedNormalisedByteSpanSearch` searches host-normalised byte spans without materialising enormous UI trees.

Existing family surfaces also gain exact variants: `GraphAdjacencyCSR` adds UInt32 degree and neighbor operations,
linear assignment adds a sparse lexicographic evidence variant, and rolling statistics exposes irregular-time
growth analysis. Host-side `CSRGraphComponents` supplies stable weak/strong components, condensation edges,
topological strata, and cycle witnesses; `IrregularTimeGrowthBurst` abstains explicitly on insufficient coverage,
identity changes, long gaps, and counter decreases.

Filesystem traversal, Unicode normalisation, persistence, deletion policy, and UI virtualization remain host
responsibilities. The families consume bounded, explicit buffers and return inspectable evidence.

`SLUInt64Pair` defines a stable two-UInt32 ABI for exact offsets, checksums, and byte counts. The compatibility
doctor and `sc_check_integer_parity` compare these values bit-for-bit without JSON/Double precision loss.

## MacResilience and typed MCP integration

The MCP server adds bounded typed adapters for APFS checksum validation, CBOR preflight, CDDL validation,
variable-span overlap, sparse assignment, graph components/layout, and irregular growth evidence. The current
20-tool manifest is generated from one source for both release packaging paths, declares the licence key as a
sensitive required input, and is validated before the MCPB is accepted.

`sc_detect_in_code` now reports the rule-set digest, SemanticCompute version/build, exact matched line, family
symbols, and a reason when it abstains. `sc_list_families` includes the full registered catalogue, including the
previously omitted whole-token family.

## Correlation contract fix for DICOM perfusion callers

`BatchedCorrelation` now exposes the same canonical binding names through discovery, semantic contracts, the CPU
reference, and Metal lowering: `ref`, `signals`, `refLength`, `signalLength`, `numLags`, and `batchCount`. Tests pin
the mirrored contract and the existing perfusion-safe role ordering, preventing callers from silently reversing
the reference curve and signal batch.

## SemanticCompute Live and hosted-trial boundary

`semanticcompute-live` provides a bounded bearer-protected `POST /v1/check/bytes` endpoint. It validates a strict
JSON/canonical-Base64 envelope, executes the catalogued exact byte comparison, localises the first mismatch, and
returns a `semanticcompute.live.byte-parity-receipt/1` receipt containing service, engine, build, input digest, and
result identity. The current attestation is deliberately labelled `digest-only`; it detects later modification
but is not a server signature.

The Cloudflare Worker/D1 control plane adds hash-only trial tokens, fixed credits and byte limits, atomic credit
reservation, idempotent replay, runner-credential isolation, receipt/input binding, and refunds for runner or
receipt failure. Twenty Worker unit tests and a real local Wrangler + D1 + Swift-runner integration cover the
control plane and entitlement lifecycle.

The deployed public endpoint currently reports `control-plane-only`. No public CPU runner, NVIDIA runner, or
paid hosted execution is claimed by this release. Enabling the browser trial remains gated on a pinned runner and
a successful public canary receipt.

## Docker MCP distribution

`Integrations/DockerMCP/Dockerfile` builds a non-root, statically linked, licensed MCP image for Linux/amd64 and
Linux/arm64. It requires and embeds the exact release commit, persists only the installation identifier in a named
volume, and needs access only to the licence host. `server.yaml` declares the sensitive Docker MCP secret, named
device volume, and host allow-list.

The tag workflow publishes `ghcr.io/entertrainment/semanticcompute-mcp:1.23.0` as a multi-architecture image with
BuildKit SBOM/provenance attestations and signs the immutable digest through GitHub OIDC/cosign. Production Docker
MCP catalogs should pin that digest after the workflow completes.

The private Cloudflare Live runner image is a separate metered execution component and is not published as an
unrestricted customer binary.

## CUDA evidence

The recorded CUDA evidence remains scoped to the emitted specimens that actually executed. The 1.23 evidence
records 17 optional CUDA-package tests across three suites on an RTX 4070 Ti SUPER, including odd extents, folded
4D coordinate payloads, early returns, NaN/infinity handling, UInt marshalling, loop accumulation, and Float-vector
helpers under the documented precise-math flags. This is device parity for the covered kernels and configuration;
it is not a claim that every family has a CUDA runtime adapter.

## Release artifacts

The GitHub release helper requires and checksums the same 15 native/evidence assets:

- macOS universal, Developer-ID signed and notarised: MCP tarball, MCPB, parity CLI, and Live tarball;
- Linux x86-64: MCP, parity, and Live tarballs;
- Linux AArch64: MCP, parity, and Live tarballs;
- `NOTICE`, CycloneDX SBOM, CUDA compile evidence, CUDA device-parity evidence, and `SHA256SUMS.txt`.

Release automation verifies version/tag/source alignment, universal architectures, signatures, notarisation,
archive payload identity, Linux architecture, exact checksums, MCPB manifest/tool coverage, fail-closed behavior,
and licensed execution before publication. It then downloads the published macOS assets and byte-compares them
with the reviewed local candidates.

## Agent setup

All clients launch the same stdio executable and receive the same 20 tools. Set the key through the client's
secret/environment facility, then restart the client and call `sc_version`. A release artifact must report
`1.23.0` and a non-`unknown` build commit.

Claude Code:

```bash
claude mcp add --transport stdio --scope user \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  semanticcompute -- /absolute/path/semanticcompute-mcp
```

Codex:

```bash
codex mcp add semanticcompute \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY" \
  -- /absolute/path/semanticcompute-mcp
```

Gemini CLI:

```bash
gemini mcp add semanticcompute /absolute/path/semanticcompute-mcp --scope user \
  --env SEMANTICCOMPUTE_LICENCE_KEY="$SEMANTICCOMPUTE_LICENCE_KEY"
```

Never commit a real key to a project-scoped MCP configuration. See `MCP.md`, `DOCKER_MCP.md`,
`LIVE_VERIFICATION.md`, `MACRESILIENCE_AGENT_NOTE.md`, and `PRICING.md` for the detailed contracts and limits.
