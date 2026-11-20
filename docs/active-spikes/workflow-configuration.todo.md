---
attention: live
---
# Workflow configuration tasks
## Done
- Added deliberate older-config conversion guidance preserving settings, verified baselines, source differences and policy authority; the current updater retains its refusal of implicit migration.
- Added generated-file handling to setup/spike procedures: per-run system temp, useful tracked verification and explicit private-state ownership, with no automatic cleanup of unresolved writes.
- Reproduced and repaired quoted Unicode staging detection and non-BMP TOML asset paths. NUL-delimited Git paths preserve the staged-file guard; literal Unicode round-trips through TOML and subsequent asset updates.
- Added purpose-based documentation placement, optional docs.index.md navigation, structured tool-source facts and optional contributor prefixes to setup guidance/templates. Branches can describe work and be shared; solo work needs no contribution branch or PR unless that workflow is selected. Shared consumer pins remain held.
- Consolidated settings and asset baselines in parent-owned project-workflows.toml with an optional ignored project-workflows.local.toml for private references.
- Removed old config-name discovery, child configuration, adapted-branch updates, JSON baseline storage/migration and legacy policy-location guidance. Replaced the source repository’s runtime example with example.workflow.md.
- Verified the current-only updater with 24 offline integration tests covering pin updates, asset reconciliation, conflict/nonmutation guards, unsupported layouts, private-file nonloading and concurrent edits.
- Completed the outgoing-history privacy review, published reviewed shared source and verified the selected configs/Agent Hands delivery through a fresh public recursive clone. Policy checks (30), lifecycle checks (24) and current updater checks (24) pass; other consumers remain outside this rollout.
## Remaining
- No implementation or publication gate remains in the selected scope. Archival still requires the normal closure decision and visible wording review; other consumer migrations are separately selected work.
