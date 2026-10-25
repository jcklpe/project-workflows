# Project Workflows
Reusable agent skills for organizing project documentation, working through implementation spikes, reviewing proposed changes, and making scoped commits. Keep the procedures alongside your code so someone cloning the project can understand how its documentation and development workflow operate.

Adopt this collection as a root-level `project-workflows/` Git submodule. Each project gets its own branch from the start, while the parent repository pins an exact revision. Project-specific procedures can evolve freely, with Git ancestry available when reconciling improvements upstream or downstream.

## Get started
You can clone the collection to inspect it first:

```sh
git clone https://github.com/jcklpe/project-workflows.git
```

Point your agent at [setup-project-workflows](skills/setup-project-workflows/SKILL.md), for example:

> Read skills/setup-project-workflows/SKILL.md and help me adopt this collection in my project. Preserve its existing documentation and local conventions, create a project-specific branch, and configure the project to use its adopted skills.

For an existing project, the setup procedure reviews its current instructions and copied skills before adding the submodule or adapting templates. It establishes the project branch, fills in `workflow.toml`, and adds routing in the parent's instructions. It does not assume an empty repository or overwrite existing documents.

If you prefer to start the Git setup yourself, run this from the adopting repository's root, using your platform-neutral project branch name in place of `project/example`:

```sh
git submodule add -b main https://github.com/jcklpe/project-workflows.git project-workflows
git -C project-workflows switch --no-track -c project/example main
```

Then follow the setup skill to configure and review the adoption. These two commands alone do not configure the workflow or publish the project branch. For project-specific changes, choose a remote you can publish to and collaborators can access, such as your own fork. The public upstream URL does not grant permission to push branches here. Keep private project information out of public branches.

## Included skills
| Skill | Purpose |
| --- | --- |
| [setup-project-workflows](skills/setup-project-workflows/SKILL.md) | Adopt the submodule, establish a project branch, configure documentation, and migrate existing copied skills. |
| [update-project-workflows](skills/update-project-workflows/SKILL.md) | Compare against shared ancestry and reconcile upstream improvements while preserving intentional project differences. |
| [run-project-spike](skills/run-project-spike/SKILL.md) | Keep reasoning and task documents together, track QA, and preserve closure history. |
| [triage-project-misc](skills/triage-project-misc/SKILL.md) | Route loose scratch observations into the appropriate project records. |
| [draft-approval-slate](skills/draft-approval-slate/SKILL.md) | Present concrete external or hard-to-reverse changes for human review. |
| [commit-work](skills/commit-work/SKILL.md) | Review scope and make coherent commits under the project's actual policy. |
| [pin-issue](skills/pin-issue/SKILL.md) | Preserve unresolved issues without prematurely adopting a solution or creating a backlog item. |
| [log-future-idea](skills/log-future-idea/SKILL.md) | Retain future infrastructure and workflow ideas outside active work. |

The collection contains procedures and templates, not an autonomous project manager. The current project's instructions and authorized task determine which procedures apply. Installing these skills does not authorize publication or external writes.

## Where things live
An adopted project might look like this; existing project conventions can use different document locations:

```text
your-project/
  README.md
  AGENTS.md
  TODO.md
  docs/
    active-spikes/
    scratch/
    archive/
    policies/
  project-workflows/          # Git submodule; parent pins an exact commit
    workflow.toml            # tracked project choices on the project branch
    .workflow.env.example    # optional private-context template
    .workflow.env            # optional local values; ignored, never committed
    skills/
      setup-project-workflows/
        assets/templates/
      update-project-workflows/
      ...
```

Actual project documents stay in the parent repository. The submodule contains the operating procedures, their templates, and configuration. It should not accumulate another project's narrative, document history, credentials, or private context.

### Configuration
[workflow.toml](workflow.toml) holds tracked choices such as the project's name, document locations, adoption metadata, and optional validation commands. Resolve `project.root` relative to the adopted collection, then document locations relative to that root. The default `..` fits a submodule at the parent's root. Parent instructions identify the adopted collection and can override seed conventions.

[.workflow.env.example](.workflow.env.example) describes optional private context pointers. Real `.workflow.env` values stay ignored inside the submodule. Treat them as literal configuration, not shell code; a pointer grants neither access nor permission. A global skill installation must never infer the current project from its own source directory.

The [setup templates](skills/setup-project-workflows/assets/templates/) provide starting points for agent routing, the task index, and ignore rules. Adapt them to the project rather than replacing existing instructions wholesale.

## Project branches and updates
Shared `main` is the reusable baseline. Create a project-specific branch at adoption even if it initially points at the same commit; no artificial localization commit is necessary. Commit tracked project choices and procedural adaptations on that branch. Configuration supports routine variation, but projects can also change the procedures themselves.

Use [update-project-workflows](skills/update-project-workflows/SKILL.md) for the full contribution and adoption cycle. Separate reusable improvements onto the shared `main` baseline without project-only configuration, integrate them through the authorized upstream route, then merge accepted `main` into each project branch while preserving its customization. Review complete outgoing commit ranges before publication and update exact consumer pins from the deepest child outward. The update procedure also covers branch renames, tracking metadata, blocked publication, and fresh recursive-clone verification.

Ordinary submodule checkout restores the parent's recorded commit and may leave a detached HEAD. Select the intended project branch before editing. A branch name in `.gitmodules` does not replace the exact commit pin, and configuring `origin` does not publish local commits. Before publishing a parent pin, make the required child commit available from the submodule URL collaborators will use. Project branches such as `project/configs` belong to their own adoptions, not to unrelated projects. An outer repository may remain on `main` or `master` while its workflow submodule uses `project/<project-slug>`.

Use platform-neutral branch names. Renaming a local project branch requires reconciling `workflow.toml`, consumer metadata, current routing, and its remote upstream; it does not require renaming the `project-workflows/` folder or deleting the old remote branch. Keep historical references identifiable as history.

For a project that already includes the submodule, clone with submodules or initialize them after cloning:

```sh
# In the already-cloned parent repository:
git submodule update --init --recursive
```

See [Git's submodule reference](https://git-scm.com/docs/git-submodule) and [gitmodules reference](https://git-scm.com/docs/gitmodules) for the Git mechanics.

## Dependencies and client installation
These are Markdown procedures with supporting templates. They need ordinary document access and Git for versioning; no Python, uv, service account, personal vault, or Agent Hands installation is required. All eight project procedures travel together, without unrelated personal or service skills.

Project adoption and global client installation are separate choices. A project can route agents directly to these files through its instructions; do not assume every agent client automatically discovers nested `skills/` folders. Use the project's adopted version when available so its procedures match its pinned history and local choices. Verify routing in the actual client after adoption.

## License
Published at [jcklpe/project-workflows](https://github.com/jcklpe/project-workflows) under [AGPL-3.0-only](LICENSE). See [NOTICE.md](NOTICE.md) for retained source attribution.
