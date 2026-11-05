---
attention: live
---
# Workflow configuration tasks
## Done
- Added purpose-based documentation placement, optional docs.index.md navigation, structured tool-source facts and human-selected contributor prefixes to setup guidance/templates. Shared consumer pins remain held.
- Consolidated settings and asset baselines in parent-owned project-workflows.toml with an optional ignored project-workflows.local.toml for private references.
- Removed old config-name discovery, child configuration, adapted-branch updates, JSON baseline storage/migration and legacy policy-location guidance. Replaced the source repository’s runtime example with example.workflow.md.
- Verified the current-only updater with 22 offline integration tests covering pin updates, asset reconciliation, conflict/nonmutation guards, unsupported layouts, private-file nonloading and concurrent edits.
## Ready for review
- The scoped main checkpoint is authorized; inspect its final commit before discussing publication. Unrelated policy work and remote divergence remain outside this change.
## Later
- Discuss publication, divergent main history and consumer rollout with the user. No push or broad rollout is authorized by this local implementation.
