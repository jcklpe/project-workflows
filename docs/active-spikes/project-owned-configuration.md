---
attention: live
reviewed: 2026-11-02
---
# Project-owned configuration
Opened 2026-11-02. Stable slug: `project-owned-configuration`. [Tasks](project-owned-configuration.todo.md).

## Outcome and authorized boundary
Support a pinned, unchanged shared collection with project configuration and local procedural notes owned by the parent project. Existing adaptation branches and their child configuration remain supported. This delivery changes upstream source and isolated fixtures only; it does not migrate existing consumers, change their pins, retire branches, adopt policies or publish anything.

## Chosen layout
New shared-source adoptions use a parent-root `workflow.toml` with `project.root = "."` and explicit `adoption.mode = "shared"`. The submodule stays detached at an exact reviewed shared revision; it needs no project branch or localization commit. The package's neutral configuration remains a legacy/example resource rather than this project's settings.

An optional `[workflows]` table maps skill names to parent-relative Markdown files, for example `run-project-spike = "docs/workflows/spikes.md"`. Agents read only the note for the current skill, alongside existing declared policies and authority. These are ordinary project procedures, not executable hooks or another policy-adoption mechanism. Existing instructions may still declare local guidance directly. Custom document folders remain project choices.

## Update behavior
The helper selects the explicit root shared-mode config when present, otherwise preserves the existing child-config adaptation route. Root configuration is never silently layered over an existing localized child. Shared mode accepts a clean detached child with neutral package settings and a forward shared revision; it checks out the exact accepted source without a merge or branch mutation. Divergence requires separate review. Parent config, local notes, policy copies and unrelated work are preserved, while copied starter assets retain their actual baseline reconciliation.

The old branch-based path keeps its ancestry-preserving merges and setting checks. Moving an existing consumer into the new layout is separate authorized work with history, policy and reference review. Runtime checks establish Git/file behavior; ordinary agent loading and collaborator access remain separate evidence.

## Local workflow-note contract
The [note format](../../setup-project-workflows/references/local-workflows.md) and optional [starter](../../setup-project-workflows/assets/templates/local-workflow.md.template) identify the shared skill, applicable scope, concrete changed steps, relevant policy owners and meaningful checks. Projects keep ordinary Markdown and their existing metadata conventions. Review whether an old customization is still useful before relocating it; preservation is not a reason to perpetuate obsolete instructions.

Setup and update procedures apply this contract. The bundled ADOPT-POLICIES candidate records that local notes cannot silently amend adopted obligations and that policies may delegate bounded contracts to named skills. The provider's adopted copy and receiving projects' operative copies remain unchanged; the distribution amendment is proposed source.
