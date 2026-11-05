---
attention: live
---
# Consolidate workflow configuration
Keep shared consumer settings and copied-asset baselines in the selected parent-owned project-workflows.toml. Private lookup paths use an optional ignored sibling project-workflows.local.toml; it overrides reference keys only, never authority or shared workflow settings. The user authorized implementation and separate local commits on shared main, with publication and consumer rollout discussed afterward.

Use a managed TOML asset section to preserve unrelated settings and comments without adding a parser/writer dependency. Use a clean cutover: only parent-owned project-workflows.toml is runtime configuration. Remove child-config, old filename, JSON storage and old policy-location compatibility. The root example.workflow.md is documentation only. Preserve actual baseline revisions, source/asset validation, staged-file guards and repeatability. Do not infer a baseline from the current pin.

The canonical main checkout contains unrelated policy work and differs from its remote-tracking ref. Preserve those files and commits; do not merge, rewrite, push or roll out other consumers. The receiving project's local output migration is a separate commit. The standalone shared change contains no private paths.

The authorized follow-up clarifies documentation ownership and navigation, separates shared tooling facts from explanatory guides, and carries human-selected branch prefixes through configuration and AGENTS. Optional document catalogs link existing owners instead of duplicating them. Personal attribution policy remains with the user’s global instruction owner.
