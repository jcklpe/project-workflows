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
- Verified the current-only updater with 22 offline integration tests covering pin updates, asset reconciliation, conflict/nonmutation guards, unsupported layouts, private-file nonloading and concurrent edits.
## In progress
- Complete the authorized outgoing-history security/privacy review and publish reviewed shared changes before selected consumer pins. Other consumers remain outside the rollout.
