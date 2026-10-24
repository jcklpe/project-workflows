# Project Workflows
Reusable procedures for keeping project reasoning, work state, and implementation history usable after cloning. The collection is intended to live at `project-workflows/` in an adopting repository, with its own project-specific branch and an exact parent Git pin.

## Start here
Use [setup-project-workflows](skills/setup-project-workflows/SKILL.md) for first adoption, documentation setup, or migration from copied skills. Use [update-project-workflows](skills/update-project-workflows/SKILL.md) to reconcile the adopted version with upstream while preserving project choices.

| Procedure | Purpose |
| --- | --- |
| [run-project-spike](skills/run-project-spike/SKILL.md) | Maintain reasoning/task pairs, QA, and closure history. |
| [triage-project-misc](skills/triage-project-misc/SKILL.md) | Route loose scratch observations. |
| [draft-approval-slate](skills/draft-approval-slate/SKILL.md) | Present concrete external or hard-to-reverse changes for review. |
| [commit-work](skills/commit-work/SKILL.md) | Make coherent commits under the project's actual policy. |
| [pin-issue](skills/pin-issue/SKILL.md) | Preserve unresolved issues without prematurely adopting a solution. |
| [log-future-idea](skills/log-future-idea/SKILL.md) | Retain future infrastructure/workflow ideas outside active work. |

## Configuration and independence
`workflow.toml` holds tracked project choices. Resolve its `project.root` relative to this adopted collection, then document paths relative to that project root. The default `..` describes a collection placed at the parent's root. A globally installed copy must never choose the current project from its own source location. Parent instructions identify the adopted collection and override seed defaults when necessary.

`.workflow.env.example` defines optional private context. Real `.workflow.env` values stay ignored; parse literal key/value data without sourcing or executing it. A pointer grants neither access nor permission. Read only explicitly relevant context. Do not store project narratives, private histories, credentials, or other projects' documents in this collection.

The procedures require ordinary document access and Git for submodule operations. No Python, uv, service account, LifeOS vault, general-skill installation, or agent-hands package is required. Client installation is separate from project adoption. A project can route agents directly to these files without assuming automatic skill discovery.

## Versioning
Create the project branch at adoption, even when initially identical to shared `main`. Project-specific configuration and procedural changes can evolve on that branch; shared templates remain templates, while actual project documents stay in the parent. Preserve intentional divergence and use the shared ancestor when reconciling changes. Keep reusable improvements as focused commits that can be proposed upstream separately.

Ordinary submodule checkout restores the parent's recorded commit and may leave detached HEAD; select the intended branch before editing. Branch tracking metadata does not replace the commit pin. Required child commits must be available from a remote collaborators can access before a parent reference is published. Having an `origin` configured does not publish local commits. See [Git's submodule reference](https://git-scm.com/docs/git-submodule) and [gitmodules reference](https://git-scm.com/docs/gitmodules).

## Distribution status and license
Licensed under AGPL-3.0-only; see [LICENSE](LICENSE) and retained [source notices](NOTICE.md). The intended public origin is `https://github.com/jcklpe/project-workflows`. Remote creation/publication and live collaborator cloning remain separate cutover steps; a locally prepared checkout is not evidence that its commits are available there.
