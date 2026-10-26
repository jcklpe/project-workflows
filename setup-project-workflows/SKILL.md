---
name: setup-project-workflows
description: "Set up or retrofit a project's documentation and reusable operating skills. Use for initial project-workflows submodule adoption, creating a project branch, migrating copied skills, or establishing README, agent routing, spike/scratch/archive/policy locations, and project configuration."
---

# Setup Project Workflows
## Scope and authority
Read the target project's instructions, current documents, commit policy, and existing skill sources first. A setup request authorizes its stated local scope, not external repository creation, publication, a push, or an unrelated reorganization. Honor review holds; do not add another approval ritual for already-authorized setup. Preserve existing human content and deliberate local conventions.

This combines documentation setup with workflow distribution. If the request is documentation-only, adapt the bundled templates without forcing a submodule adoption. If a collection already exists, use `update-project-workflows`; do not overwrite it. Dependencies are Git for versioned adoption and ordinary filesystem/document access, not global general skills or service tools.

## Inspect and select
1. Resolve the actual parent repository from the request and its instructions, never from the location of a global skill. Inspect working-tree/index changes, current docs, local skills, existing submodules, and tracked/ignored configuration. Preserve concurrent work; do not stash, reset, or force checkout to make adoption easier.
2. Identify the selected source repository and reviewed revision, using its actual remote/default branch. Require a public-safe, collaborator-usable URL before recording `.gitmodules`; never put credentials or a private machine path there. Confirm license compatibility and retained notices. An available folder is not automatically an independent repository or permission to republish it.
3. Identify the scope to adopt. The collection's eight project procedures travel together; unrelated personal/service skills do not. Preserve any existing project-specific procedure differences. Missing required sources are an explicit setup gap, not permission to invent their content.

## Adopt and branch
Use a root-level `project-workflows/` submodule. Inspect any existing destination before changing it. Record the reviewed source URL in the parent's submodule metadata and pin the exact child commit. Follow the parent's Git policy, including ignore checks and scoped commits; submodule setup can stage metadata, so inspect its complete effect and do not sweep unrelated index content into a commit.

For an adopting project, create/select a project-specific branch inside the workflow submodule from the reviewed shared branch, normally `main`, immediately, even with no content changes. Do not use another project's adaptation as the baseline. Follow the user's naming choice or a local platform-neutral convention; absent one, use `project/<project-slug>`. The adopting repository's own branch is separate and need not be renamed. Do not create a fake localization commit. If the name exists, verify its ancestry and intended ownership before selecting it; do not repoint or reset it. Record the selected branch and upstream in `workflow.toml`; `.gitmodules` may also record the project's tracking branch when appropriate. The parent commit pin remains authoritative.

An explicitly designated canonical maintenance/global installation is the exception: select shared `main`, keep neutral `workflow.toml` defaults, and use the containing project instructions for its own workflow. A global client link alone does not establish canonical ownership. Do not create a project branch merely to label that installation. Ordinary adopting projects still get a branch before they diverge.

For an existing adoption's branch rename, canonical-checkout migration, metadata repair, or shared/project reconciliation, use [update-project-workflows](../update-project-workflows/SKILL.md). Keep a correctly placed `project-workflows/` folder; a branch rename alone does not call for a folder move.

Keep public-safe project configuration in `workflow.toml` on the adaptation branch; the canonical installation retains the shared defaults. No workflow env file is required. Preserve any existing project-declared private-context mechanism and its access rules instead of adding an unused example or a speculative setting. Verify ignores before creating any real private configuration and parse it as data, not executable shell. Keep actual project documents in the parent, not on a shared skill branch.

For an existing copied-skills project, compare complete folders and supporting files before cutover. Preserve the local procedure in the project branch, record which source comparison is known, and repair routing before retiring old copies. Without a recoverable shared ancestor, mark the first import as a manually reconciled baseline; never fabricate ancestry or silently declare the local version equivalent to upstream.

## Documentation and routing
Use [the agent-routing template](assets/templates/AGENTS.md.template), [the index template](assets/templates/TODO.md.template), and [the ignore baseline](assets/templates/default.gitignore) as inputs to adapt, not files to overwrite existing documents with. Create only needed structure:
- Root README: purpose, how to start, relevant validation, and clone/submodule instructions.
- Root AGENTS: current authority, project-specific rules, validation, privacy, and the actual adopted skill/configuration location.
- Optional CLAUDE symlink: point to AGENTS only when requested or already conventional; preserve existing real files and unrelated links.
- TODO: short active-work/QA/history coordination index, not a task dump.
- Active spikes: paired conceptual/task documents under the resolved location, using `run-project-spike`.
- Scratch: provisional working notes and a misc inbox only when useful; not standing policy.
- Archive: closed/superseded history with the project's attention and continuation conventions.
- Policies: maintained current rules with useful rationale; Git carries their evolution. Preserve existing vocabulary and do not force ADR chains or a numbered template.

Do not add redundant READMEs inside documentation folders. Create pinned issues or future-ideas files when there is material for them. Preserve existing paths unless migration is authorized. A scaffold does not establish a product specification or capture unwritten project reasoning.

Skill directories live directly under the collection root: `project-workflows/<skill-name>/SKILL.md`. Preserve each complete folder, including assets and client metadata. Parent routing must prefer the adopted project version over global seeds. Explain how to read the project configuration and load required skills. Do not claim automatic discovery in an agent client unless it has actually been configured. Do not implicitly copy Kaizen, authoring, LifeOS, or service capabilities to make the project work.

## Verification and handoff
Verify the adopted revision, initial project branch, parent pin, required files, relative references, and configuration/ignore behavior. Inspect staged and unstaged effects in both repositories. Confirm project-specific conventions and validation are actually documented rather than inferred from folder names.

For a claimed shareable adoption, verify a fresh clone with recursive submodules can obtain the pinned child commit from the recorded remote under collaborator access. A local-only fixture is useful evidence but not remote-access verification. If commits are not published, label the adoption locally ready and explicitly state that collaborator cloning remains unverified. Never push as a side effect of setup; follow the human publication boundary.

Report the selected source/revision and project branch, created/adapted files, preserved divergence, ignored local configuration without values, and remaining access or content gaps. Checkpoint coherent authorized changes under the project's commit policy.
