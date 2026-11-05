---
attention: live
---
# Workflow configuration tasks
## Done
- Implemented parent-owned project-workflows.toml asset records, explicit legacy JSON migration and project-workflows.local.toml reference conventions. Setup adds the local filename to the project's ignore rules. Existing workflow.toml names and child-config adaptations remain supported until explicit migration.
- All 43 offline updater tests pass, including new-name discovery, repeatability, source-baseline preservation, private-file nonloading, conflicting/malformed records, staged-file protection and local edits during checkout. Changed TOML, relative resource links and whitespace checks pass.
## Ready for review
- The scoped main checkpoint is authorized; inspect its final commit before discussing publication. Unrelated policy work and remote divergence remain outside this change.
## Later
- Discuss publication, divergent main history and consumer rollout with the user. No push or broad rollout is authorized by this local implementation.
