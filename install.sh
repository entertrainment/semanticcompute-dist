#!/usr/bin/env bash
# SemanticCompute public installer pause.
set -euo pipefail

cat >&2 <<'NOTICE'
SemanticCompute public installation is temporarily paused.

The v1.22.1 and earlier binaries predate online entitlement enforcement. They are
being withdrawn while the signed, licence-gated 1.23 distribution is prepared.
Request a bounded trial or paid licence at douglas@entertrainment.co.uk.

No binary was downloaded and no MCP client configuration was changed.
NOTICE
exit 1
