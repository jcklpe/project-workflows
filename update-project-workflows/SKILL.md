---
name: update-project-workflows
description: "Update unchanged-source consumer pins and copied assets while preserving project-owned configuration and policies."
---
# Update Project Workflows
Resolve the actual target using [target resolution](../README.md#resolve-the-target). Read its instructions, selected configuration and Git policy. Use its complete selected source, not a global installation by accident. Preserve unrelated work and publication holds. This skill does not authorize pushes or other-consumer changes.
## Consumer update
1. Establish the parent Git root, clean detached `project-workflows/` child, current parent pin and exact accepted shared revision. Configuration must be the parent-owned `project-workflows.toml` in its documentation folder, declared by AGENTS. Use `adoption.mode = "shared"`; old filenames, child-config branches and JSON manifests are unsupported.
2. Read applicable parent-owned policy prerequisites and local workflow notes. Verify required paths before acting. Agent policies use `documents.agent_policies` and their declared index. Do not refresh them as copied template assets or infer adoption from package delivery.
3. Require forward ancestry to the accepted source. Preview the exact target and copied-asset changes. Reconcile each asset against its actual `[assets]` source revision; a source pin alone does not establish the installed baseline. Review local/incoming edits and refuse conflicts or missing records rather than guessing.
4. Apply the reviewed detached pin advance and asset writes within authorization. Preserve source commits, shared settings, local notes and unrelated index state. Inspect configured validation commands as data before running them. The helper performs no parent staging, commit or push.
5. Verify exact source identity, copied-asset behavior, TOML, resources and a repeated no-op preview. Use [Commit Work](../commit-work/SKILL.md) for the parent pin, affected assets and configuration as a coherent change. Distinguish local readiness from publication and shared acceptance.

Use the optional [helper](scripts/update.py) and [usage reference](references/updater.md) with an existing Python 3.11+ and Git; no dependency installation is required. `--reviewed` acknowledges specific copied-asset overlaps, not arbitrary conflicts. Partial failures are not retried blindly: inspect the actual child and parent state first.
## Other scopes
Canonical collection maintenance and global-only use follow the [exceptional routes](references/exceptional-updates.md). Shared main changes and consumer adoption are separate work. Old consumer layouts require a deliberately scoped conversion to the current layout before this helper can be used; do not retain a fallback mode or silently switch branches to accommodate them.
