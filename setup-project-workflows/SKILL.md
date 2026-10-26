---
name: setup-project-workflows
description: "Set up or retrofit a project's documentation and reusable operating skills. Use for initial project-workflows submodule adoption, creating a project branch, migrating copied skills, or establishing README, agent routing, spike/scratch/archive/policy locations, and project configuration."
---

# Setup Project Workflows
Resolve the actual requested target using [target resolution](../README.md#resolve-the-target). Read its declared policies, local adapters and configuration before applying defaults, and follow its chosen global-only or pinned workflow source. Global invocation never selects the installation checkout or its config as the target. Plain folders use global skills without adding a collection or initializing Git.
## Scope and authority
Read the target project's instructions, current documents, commit policy, and existing skill sources first. A setup request authorizes its stated local scope, not external repository creation, publication, a push, or an unrelated reorganization. Honor review holds; do not add another approval ritual for already-authorized setup. Preserve existing human content and deliberate local conventions.

This combines documentation setup with workflow distribution. If the request is documentation-only, adapt the bundled templates without forcing a submodule adoption. If a collection already exists, use `update-project-workflows`; do not overwrite it. Dependencies are Git for versioned adoption and ordinary filesystem/document access, not global general skills or service tools.

## Choose the workflow source
Honor the user's or target's declared mode. For a pinned adoption, follow the branch/submodule procedure below. A Git project may instead explicitly choose global-only use; plain folders use global workflows without creating repositories. Global-only setup reads installed procedures, preserves project policies/adapters, declares the target's optional root `workflow.toml` with `project.root = "."`, and adds only the required documentation/routing. Omit adoption branch metadata and skip submodule, branch and pin steps. Do not run an installer or create a config merely because one is absent; report a missing required global skill.

An existing pinned adoption is not retired by a generic setup request. An authorized switch uses [update-project-workflows](../update-project-workflows/SKILL.md#move-an-adoption-to-global-only-use), including unique-content and reference checks. Global-only use trades a project-pinned version for the installed global version; report that limit without changing other projects' chosen modes.

## Inspect and select
1. Resolve the actual parent repository from the request and its instructions, never from the location of a global skill. Inspect working-tree/index changes, current docs, local skills, existing submodules, and tracked/ignored configuration. Preserve concurrent work; do not stash, reset, or force checkout to make adoption easier.
2. Identify the selected source repository and reviewed revision, using its actual remote/default branch. Require a public-safe, collaborator-usable URL before recording `.gitmodules`; never put credentials or a private machine path there. Confirm license compatibility and retained notices. An available folder is not automatically an independent repository or permission to republish it.
3. Identify the scope to adopt. The collection's seven project procedures travel together; unrelated personal/service skills do not. Preserve any existing project-specific procedure differences. Missing required sources are an explicit setup gap, not permission to invent their content.

## Synchronized storage
Before adopting inside a synced drive, inspect the actual Git directory and common directory, including pointer files and linked worktrees. Reuse the project's established external-metadata arrangement: repository objects, indexes, and refs must stay outside the synchronized tree, while working files remain in their selected location. Do not copy a prior machine's absolute pointer or run ordinary setup that creates an object store inside Drive. Check parent and child metadata locations and local restoration in an isolated fixture first; a linked-worktree/submodule combination must be verified, not assumed supported.

A public upstream URL identifies shared source; it does not make a private adaptation pin remotely retrievable. For an explicitly local-only private adaptation, verify a complete private recovery bundle and a restoration with Git metadata outside the synced tree. Record how to reconnect the restored child and recreate machine-local pointer files; distinguish local recovery from off-device backup and collaborator cloning. Never upload private branch history as a way to satisfy a generic reproducibility check.

Respect local-only/no-remote policies, tracking allowlists, and commit cadence. A proposed submodule may require a narrow policy/ignore exception for its gitlink and `.gitmodules`; surface that concrete conflict before changing it. Private adaptations need an authorized private persistence/recovery arrangement and must not be published to the public upstream. No plain-folder adoption is needed merely because it is stored on a synced drive.

## Adopt and branch
Use a root-level `project-workflows/` submodule. Inspect any existing destination before changing it. Record the reviewed source URL in the parent's submodule metadata and pin the exact child commit. Follow the parent's Git policy, including ignore checks and scoped commits; submodule setup can stage metadata, so inspect its complete effect and do not sweep unrelated index content into a commit.

For an adopting project, create/select a project-specific branch inside the workflow submodule from the reviewed shared branch, normally `main`, immediately, even with no content changes. Do not use another project's adaptation as the baseline. Follow the user's naming choice or a local platform-neutral convention; absent one, use `project/<project-slug>`. The adopting repository's own branch is separate and need not be renamed. Do not create a fake localization commit. If the name exists, verify its ancestry and intended ownership before selecting it; do not repoint or reset it. Record the selected branch and upstream in `workflow.toml`; `.gitmodules` may also record the project's tracking branch when appropriate. The parent commit pin remains authoritative.

An explicitly designated canonical maintenance/global installation is the exception: select shared `main`, keep neutral `workflow.toml` defaults, and use the containing project instructions for its own workflow. A global client link alone does not establish canonical ownership. Do not create a project branch merely to label that installation. Ordinary adopting projects still get a branch before they diverge.

For an existing adoption's branch rename, canonical-checkout migration, metadata repair, or shared/project reconciliation, use [update-project-workflows](../update-project-workflows/SKILL.md). Keep a correctly placed `project-workflows/` folder; a branch rename alone does not call for a folder move.

Keep public-safe project configuration in `workflow.toml` on the adaptation branch; the canonical installation retains the shared defaults. No workflow env file is required. Preserve any existing project-declared private-context mechanism and its access rules instead of adding an unused example or a speculative setting. Verify ignores before creating any real private configuration and parse it as data, not executable shell. Keep actual project documents in the parent, not on a shared skill branch.

For an existing copied-skills project, use the [copied-skill reconciliation](../update-project-workflows/SKILL.md#existing-copied-skills) before cutover, comparing complete folders and supporting files. Preserve intentional local behavior with its appropriate owner (project policy/adapter or pinned procedure), record which source comparison is known, and repair routing before retiring old copies. Without a recoverable shared ancestor, mark the first import as a manually reconciled baseline; never fabricate ancestry or silently declare the local version equivalent to upstream.

## Documentation and routing
Use [the agent-routing template](assets/templates/AGENTS.md.template), [the index template](assets/templates/TODO.md.template), and [the ignore baseline](assets/templates/default.gitignore) as inputs to adapt, not files to overwrite existing documents with. Create only needed structure:
- Root README: purpose, how to start, relevant validation, and clone/submodule instructions.
- Root AGENTS: current authority, project-specific rules, validation, privacy, and the actual adopted skill/configuration location.
- Optional CLAUDE symlink: point to AGENTS only when requested or already conventional; preserve existing real files and unrelated links.
- TODO: short active-work/QA/history coordination index, not a task dump.
- Active spikes: paired conceptual/task documents under the resolved location, using `run-project-spike`.
- Scratch: individual subject notes for possibilities or deliberately parked work, using [capture-for-later](../capture-for-later/SKILL.md), plus a misc inbox only when useful. New capture notes need only `status: captured` or `status: parked` and a short body; they are not active work or standing policy.
- Archive: closed/superseded history with the project's attention and continuation conventions.
- Policies: maintained current rules with useful rationale; Git carries their evolution. Preserve existing vocabulary and do not force ADR chains or a numbered template.

Do not add redundant READMEs inside documentation folders. Do not create catch-all pinned-issues or future-ideas lists for new capture. Keep existing notes and legacy lists where they are unless migration is requested; related existing material should be updated rather than duplicated. Preserve existing paths unless migration is authorized. A scaffold does not establish a product specification or capture unwritten project reasoning.

Skill directories live directly under the collection root: `project-workflows/<skill-name>/SKILL.md`. Preserve each complete folder, including assets and client metadata. For pinned mode, parent routing prefers the adopted project version over global seeds; global-only routing names installed procedures and the target-owned config/policy entrypoints. Explain how to read the project configuration and load required skills. Do not claim automatic discovery in an agent client unless it has actually been configured. Do not implicitly copy Kaizen, authoring, LifeOS, or service capabilities to make the project work.

## Verification and handoff
Verify the adopted revision, initial project branch, parent pin, required files, relative references, and configuration/ignore behavior. Inspect staged and unstaged effects in both repositories. Confirm project-specific conventions and validation are actually documented rather than inferred from folder names.

For a claimed shareable adoption, verify a fresh clone with recursive submodules can obtain the pinned child commit from the recorded remote under collaborator access. A local-only fixture is useful evidence but not remote-access verification. If commits are not published, label the adoption locally ready and explicitly state that collaborator cloning remains unverified. Never push as a side effect of setup; follow the human publication boundary.

Report the selected source/revision and project branch, created/adapted files, preserved divergence, ignored local configuration without values, and remaining access or content gaps. Checkpoint coherent authorized changes under the project's commit policy.
