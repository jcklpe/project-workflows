---
attention: live
reviewed: 2026-11-02
---
# Project-owned configuration
Opened 2026-11-02. Stable slug: `project-owned-configuration`. [Tasks](project-owned-configuration.todo.md).

## Outcome and authorized boundary
Support a pinned, unchanged shared collection with project configuration and local procedural notes owned by the parent project. Existing adaptation branches and their child configuration remain supported. This delivery changes upstream source and isolated fixtures only; it does not migrate existing consumers, change their pins, retire branches, adopt policies or publish anything.

## Chosen layout
New shared-source adoptions use `docs/workflow.toml` or the existing documentation folder, such as `_meta/workflow.toml`, with `project.root = ".."` for a single-level folder and explicit `adoption.mode = "shared"`. The submodule stays detached at an exact reviewed shared revision; it needs no project branch or localization commit. The package's neutral configuration remains a legacy/example resource rather than this project's settings.

An optional `[workflows]` table maps skill names to parent-relative Markdown files, for example `run-project-spike = "docs/workflows/spikes.md"`. Agents read only the note for the current skill, alongside existing declared policies and authority. These are ordinary project procedures, not executable hooks or another policy-adoption mechanism. Existing instructions may still declare local guidance directly. Custom document folders remain project choices.

## Update behavior
The helper selects the explicitly declared parent shared-mode config, or one unambiguous supported parent location, otherwise preserves the existing child-config adaptation route. Parent configuration is never silently layered over an existing localized child. Shared mode accepts a clean detached child with neutral package settings and a forward shared revision; it checks out the exact accepted source without a merge or branch mutation. Divergence requires separate review. Parent config, local notes, policy copies and unrelated work are preserved, while copied starter assets retain their actual baseline reconciliation.

The old branch-based path keeps its ancestry-preserving merges and setting checks. Moving an existing consumer into the new layout is separate authorized work with history, policy and reference review. Runtime checks establish Git/file behavior; ordinary agent loading and collaborator access remain separate evidence.

## Local workflow-note contract
The [note format](../../setup-project-workflows/references/local-workflows.md) and optional [starter](../../setup-project-workflows/assets/templates/local-workflow.md.template) identify the shared skill, applicable scope, concrete changed steps, relevant policy owners and meaningful checks. Projects keep ordinary Markdown and their existing metadata conventions. Review whether an old customization is still useful before relocating it; preservation is not a reason to perpetuate obsolete instructions.

Setup and update procedures apply this contract. The bundled ADOPT-POLICIES candidate records that local notes cannot silently amend adopted obligations and that policies may delegate bounded contracts to named skills. The provider's adopted copy and receiving projects' operative copies remain unchanged; the distribution amendment is proposed source.

## Client interface metadata
The collection uses SKILL.md metadata without separately maintained openai.yaml interface files. Optional presentation metadata is not selected for this distribution. Existing pinned copies retain their source state until their authorized updates; this source cleanup does not migrate them.

## Configuration discovery
Setup writes the exact configuration link into AGENTS and verifies it. The helper supports --config for that declared project-relative path and rejects ambiguous conventional discovery. Existing root configs and branch-based layouts remain supported; no consumer file is moved by this change.

## Policy record ownership followup
The explicitly approved metadata amendment makes PRESERVE-IDENTITY the canonical owner of required frontmatter fields, their meanings and descriptive type. ADOPT-POLICIES retains adoption authority and RESOLVE-DEPENDENCIES retains edge semantics. The adopted provider copy and proposed distribution source receive the same reviewed body section. Task skills reference the actual project contract, with the header example beside its definition in PRESERVE-IDENTITY; the separate template file is removed at the user’s request. Technical parser/index notes stay with Review. No schema/checker behavior or other project’s policy adoption is changed. This work stays local.

## Approved history and example ownership
The reviewed policy-history requirement is adopted in the provider’s PRESERVE-IDENTITY copy and supplied as proposed distribution source. Edit and Retire pass mnemonic policy IDs and decision rationale to Commit Work. The record definition and YAML example have one kernel owner; Create references it. Both optional interface metadata files are removed rather than expanding vendor presentation metadata across the collection. These changes remain local and do not alter any consumer’s adoption state.
