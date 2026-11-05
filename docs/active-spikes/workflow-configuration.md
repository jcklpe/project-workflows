---
attention: live
---
# Consolidate workflow configuration
Keep shared consumer settings and copied-asset baselines in the selected parent-owned project-workflows.toml. Private lookup paths use an optional ignored sibling project-workflows.local.toml; it overrides reference keys only, never authority or shared workflow settings. The user authorized implementation and separate local commits on shared main, with publication and consumer rollout discussed afterward.

Use a managed TOML asset section to preserve unrelated settings and comments without adding a parser/writer dependency. Keep legacy child-config consumers working; shared consumers explicitly migrate their old JSON records before using the new helper. Preserve actual baseline revisions, source/asset validation, staged-file guards and repeatability. Do not infer a baseline from the current pin.

The canonical main checkout contains unrelated policy work and differs from its remote-tracking ref. Preserve those files and commits; do not merge, rewrite, push or roll out other consumers. The receiving project's local output migration is a separate commit. The standalone shared change contains no private paths.
