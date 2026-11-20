---
attention: live
---
# Consolidate workflow configuration
Keep shared consumer settings and copied-asset baselines in the selected parent-owned project-workflows.toml. Private lookup paths use an optional ignored sibling project-workflows.local.toml; it overrides reference keys only, never authority or shared workflow settings. The user authorized implementation and separate local commits on shared main, with publication and consumer rollout discussed afterward.

Use a managed TOML asset section to preserve unrelated settings and comments without adding a parser/writer dependency. Use a clean cutover: only parent-owned project-workflows.toml is runtime configuration. Remove child-config, old filename, JSON storage and old policy-location compatibility. The root example.workflow.md is documentation only. Preserve actual baseline revisions, source/asset validation, staged-file guards and repeatability. Do not infer a baseline from the current pin.

The current reconciliation includes review and publication of the preserved reusable changes. Preserve source history and unrelated work; child publication precedes containing pins. Consumer migration remains bounded to explicitly selected projects. The standalone shared change contains no private paths.

The authorized follow-up clarifies documentation ownership and navigation, separates shared tooling facts from explanatory guides, and preserves project-selected branch arrangements. Contributor prefixes are optional; branches can describe work and be shared by multiple people and agents. Solo work needs no contribution branch or PR unless that workflow is selected. Optional document catalogs link existing owners instead of duplicating them. Personal attribution policy remains with the user’s global instruction owner.

Generated-file handling is part of that ownership boundary: tools use private per-run OS temporary directories, track useful synthetic verification, and explicitly designate persistent private state. Authored scratch documentation remains separate. Existing state migration must preserve unresolved operations and coordinate all writers; an ignore rule or age alone is not a disposal decision. The setup skill owns this procedure, with a link from spike execution.
