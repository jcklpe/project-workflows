---
attention: live
reviewed: 2026-11-02
---
# Project-owned configuration — work
Opened 2026-11-02. Stable slug: `project-owned-configuration`. [Concept](project-owned-configuration.md).

## To Do
- No provider implementation remains in this slice. Observe ordinary use under the QA item; any consumer migration, branch retirement or publication is separate scope.

## Ready for Human QA
- Observe local workflow-note loading in an ordinary explicitly selected task after this feature is available. No existing consumer migration or live service action is required by the provider tests.

## Done
- Read the current provider instructions, configuration, helper/tests, setup resources and relevant private workflow concerns. The user authorized this upstream hardening, preserving consumers/branches and prohibiting pushes. Concurrent policy rollout/kernel tracking edits remain outside this implementation.
- Add explicit root shared-mode configuration and project workflow-note support to the optional updater, preserving existing adaptation behavior and actual asset/policy boundaries. — Implemented explicit parent-root shared mode, protected local workflow-note references and exact detached source advances. Existing child-config adaptations keep their branch/merge behavior. Root data cannot silently mask a localized child, and config/notes/policies cannot be auto-refreshed assets.
- Update target resolution, setup, routing templates and updater guidance for unchanged pinned source and parent-owned context; keep existing consumers and experimental branches intact. — Updated README target resolution/manual setup/layout, setup/update skills, neutral defaults and routing/root-config templates. Local notes remain ordinary project Markdown under current policy authority; existing source experiments and migration boundaries remain supported.
- Exercise real temporary repositories for shared exact-source updates, no-op reruns, root-config/local-note/policy preservation, copied assets, invalid declarations and refused implicit migrations; run existing updater/policy/lifecycle checks. — All 34 real-Git updater tests pass under both Python 3.13 and 3.14, including exact shared tree identity, preserved refs/index/config/notes/policies, copied-asset reconciliation, no-op reruns, refused implicit migration, malformed/missing references and a real post-checkout concurrent-note edit with explicit partial-state reporting. All 30 policy tests and 24 lifecycle tests pass.
- Review source, resources, portability and privacy, checkpoint only this upstream scope, and record actual verification and remaining ordinary-use acceptance. — Reviewed full selected source and documentation diffs. Ruby/Psych parsed four YAML headers; Python AST, both TOML files, 86 local resource targets and whitespace checks pass. The standard skill validator lacks PyYAML under the existing Python 3.13 runtime; no packages were installed. The scoped local implementation checkpoint excludes concurrent rollout/kernel edits and containing pins. Ordinary client loading, consumer adoption and remote retrieval remain unverified.

## Checkpoint scope
The shared TODO index contains a pre-existing rollout entry pointing to another workstream’s uncommitted handoff pair. Its current tracking edits remain intact and uncommitted rather than importing that pair or committing broken standalone navigation. The implementation, own spike pair and directly affected resources form this checkpoint; no containing-repository pin is staged or committed.
