# Project Workflows
Reusable agent skills for organizing project documentation, working through implementation spikes, reviewing proposed changes, and making scoped commits. Keep the procedures alongside your code so someone cloning the project can understand how its documentation and development workflow operate.

A Git project can pin this collection as a root-level `project-workflows/` Git submodule or explicitly use installed global skills with project-owned policy/configuration. Preserve the chosen mode; do not create or remove a submodule merely because global skills are available. For a pinned adoption, each project gets its own branch from the start, while the parent repository pins an exact revision. An explicitly designated canonical maintenance/global installation uses shared `main` directly. Project-specific procedures can evolve freely, with Git ancestry available when reconciling improvements upstream or downstream.

## Resolve the target
Resolve the requested project or folder before reading collection configuration or choosing document paths. Prefer the explicit target in the request; otherwise use the active working context and its nearest applicable instructions. Inspect the target's actual Git boundary separately from its document/workspace boundary. If several plausible targets remain, ask which one before writing; a skill's installation path is never a target-selection fallback.

Before using defaults, read the target's applicable instructions and the project policies, local adapters and configuration they declare. Follow the declared workflow source: a pinned adoption uses its own complete collection; an explicitly global-only target uses installed global procedures with its target-owned overrides. If the source is undeclared, preserve an existing adoption or local skill convention rather than silently switching it. A plain folder uses global skills and its own conventions without an automatic repository, clone or submodule. A folder inside a repository follows its applicable instructions; it is not automatically an independent adoption.

Select configuration from the target's declaration, not from the installed skill's directory. This may be `<target>/workflow.toml` for global-only use or `<target>/project-workflows/workflow.toml` for a pinned adoption. If no configuration is declared, use the target's existing documented locations; a config file is not required merely to invoke a skill. Never substitute the global installation's `workflow.toml` or its consumer-relative `..`. A declared policy, adapter or config that is unavailable is a specific gap to report, not permission to silently apply defaults. Read only relevant declared context and parse configuration as data.

When the explicit task is development of Project Workflows itself, use this repository's [maintenance instructions](AGENTS.md#maintaining-this-collection), [work index](TODO.md), and root skills. Its `docs/` is an ordinary directory in the same repository, not a copy of the workflow collection nested inside itself.

## Get started
You can clone the collection to inspect it first:

```sh
git clone https://github.com/jcklpe/project-workflows.git
```

Point your agent at [setup-project-workflows](setup-project-workflows/SKILL.md), for example:

> Read setup-project-workflows/SKILL.md and help me adopt this collection in my project. Preserve its existing documentation and local conventions, create a project-specific branch, and configure the project to use its adopted skills.

For global-only use, ask the setup skill to use installed procedures with the target's own instructions and optional root `workflow.toml`, without creating a collection or branch. This uses the installed version rather than a project pin. For a pinned adoption, the setup procedure reviews current instructions and copied skills before adding the submodule or adapting templates. It establishes the project branch, fills in `workflow.toml`, and adds routing in the parent's instructions. It does not assume an empty repository or overwrite existing documents.

If you prefer to start the Git setup yourself, run this from the adopting repository's root, using your platform-neutral project branch name in place of `project/example`:

```sh
git submodule add -b main https://github.com/jcklpe/project-workflows.git project-workflows
git -C project-workflows switch --no-track -c project/example main
```

Then follow the setup skill to configure and review the adoption. These two commands alone do not configure the workflow or publish the project branch. For project-specific changes, choose a remote you can publish to and collaborators can access, such as your own fork. The public upstream URL does not grant permission to push branches here. Keep private project information out of public branches.

## Included skills
| Skill | Purpose |
| --- | --- |
| [setup-project-workflows](setup-project-workflows/SKILL.md) | Adopt the submodule, establish a project branch, configure documentation, and migrate existing copied skills. |
| [update-project-workflows](update-project-workflows/SKILL.md) | Compare against shared ancestry and reconcile upstream improvements while preserving intentional project differences. |
| [run-project-spike](run-project-spike/SKILL.md) | Keep reasoning and task documents together, track QA, and preserve closure history. |
| [coordinate-project-contribution](coordinate-project-contribution/SKILL.md) | Link agent-owned work to contributions between people, with optional forge coordination, review and integration. |
| [triage-project-misc](triage-project-misc/SKILL.md) | Route loose scratch observations into the appropriate project records. |
| [draft-approval-slate](draft-approval-slate/SKILL.md) | Present concrete external or hard-to-reverse changes for human review. |
| [commit-work](commit-work/SKILL.md) | Review scope and make coherent commits under the project's actual policy. |
| [capture-for-later](capture-for-later/SKILL.md) | Save possibilities and deliberately parked subjects as small individual scratch notes, without starting work. |

`capture-for-later` is the sole entrypoint for saving possibilities and deliberately parked subjects. Existing notes remain valid and are not migrated by installation.

The collection contains procedures and templates, not an autonomous project manager. The current project's instructions and authorized task determine which procedures apply. Installing these skills does not authorize publication or external writes.

## Join an existing project
Start with that project's README, AGENTS, work index and relevant work records. Restore its chosen workflow source using its documented instructions; you do not need the maintainer's personal agent setup. Use your own editor or agent client, and run the project's documented checks. With an agent, a useful first prompt is:

> Read this project's README, AGENTS, work index and relevant spike records. Summarize the current contribution, acceptance checks, selected coordination route and missing access. Explain the next bounded step before changing anything. Each spike is owned by one agent and one thread; read other agents' spikes for context and keep independent work in your own spike.

Follow the humans' existing coordination and project records. [Coordinate Project Contribution](coordinate-project-contribution/SKILL.md) connects that direction to each agent's execution and review without imposing a negotiation process or prerequisite agreement checklist. Raise concrete blockers for the people involved to resolve.

Local work uses the project's existing documents, checks and QA without a forge or service tooling. If forge coordination is explicitly selected, use its shared records for cross-person agreements and meaningful updates; agent-owned spikes retain detailed execution. Tool/client choice remains personal. Agent Hands provides optional platform tooling for supported agent operations, and a human can handle a step with their own tools. Missing agent tooling calls for a specific handoff, not automatic installation or access changes.

One branch may host many agent-owned spikes, several issues and multiple eventual change requests. Use Commit Work's atomic targeted commits and spike trailers to identify reviewable groups when they are sufficiently separable; no one-issue/one-branch/one-change-request format is required. Prepare a focused review overview with evidence and links, retaining suitable tracked documents and every original atomic commit. Follow the project's authorization and human publication/integration boundaries. A merged contribution, completed shared outcome and closed spike are separate states.

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
    setup-project-workflows/
      SKILL.md
      assets/templates/
    update-project-workflows/
    ...
```

For an adoption, actual project documents stay in the parent repository. The submodule contains the operating procedures, their templates, and configuration. It should not accumulate another project's narrative, document history, credentials, or private context.

### Configuration
[workflow.toml](workflow.toml) illustrates project identity, document locations, optional adoption metadata and validation commands. Resolve `project.root` relative to the directory containing the selected config file, then document locations relative to that root. Thus a parent-root config normally uses `project.root = "."`; a config inside a root-level `project-workflows/` submodule keeps `".."`. Existing pinned configs retain their meaning. Project instructions identify the config and override seed conventions. Global-only targets omit submodule branch/pin metadata rather than inventing an adoption. Keep nonsecret project choices with the project under its tracking policy; credentials are not workflow configuration.

No workflow env file is required. If a project already declares private-context configuration, preserve its own discovery and access rules; do not invent a new pointer or read unrelated private material. A global skill installation must never infer the current project from its own source directory.

Coordination is optional and defaults to local use. A project can declare it in its maintained instructions or the selected configuration's optional `[coordination]` table: `mode` is `local` or `forge`, `repository` identifies the intended target URL, and `tooling` points to project-owned guidance naming the selected setup/use skills and their source/version. Leave `tooling` empty when a human handles platform steps. An explicit request may select one operation without persisting these choices. Credentials remain with the platform tooling owner. A remote or installed tool does not enable coordination or authorize writes; see [Coordinate Project Contribution](coordinate-project-contribution/SKILL.md).

The [setup templates](setup-project-workflows/assets/templates/) provide starting points for agent routing, the task index, and ignore rules. Adapt them to the project rather than replacing existing instructions wholesale.

## Project branches and updates
Shared `main` is the reusable baseline and the branch for an explicitly designated canonical maintenance/global installation. Such an installation keeps neutral `workflow.toml` defaults and uses its containing project instructions without creating an adaptation merely to record its name. This does not make every global skill installation canonical.

For other pinned adoptions, create a project-specific branch at adoption even if it initially points at the same commit; no artificial localization commit is necessary. Commit tracked project choices and procedural adaptations on that branch. Configuration supports routine variation, but projects can also change the procedures themselves.

Use [update-project-workflows](update-project-workflows/SKILL.md) for the full contribution and adoption cycle. Separate reusable improvements onto the shared `main` baseline without project-only configuration, integrate them through the authorized upstream route, then merge accepted `main` into each project branch while preserving its customization. Review complete outgoing commit ranges before publication and update exact consumer pins from the deepest child outward. The update procedure also covers branch renames, tracking metadata, blocked publication, and fresh recursive-clone verification.

Ordinary submodule checkout restores the parent's recorded commit and may leave a detached HEAD. Select the intended project branch, or shared `main` for the designated canonical installation, before editing. A branch name in `.gitmodules` does not replace the exact commit pin, and configuring `origin` does not publish local commits. Before publishing a parent pin, make the required child commit available from the submodule URL collaborators will use. Project branches such as `project/example` belong to their own adoptions, not to unrelated projects. An outer repository may remain on `main` or `master` while its workflow submodule uses `project/<project-slug>`.

Use platform-neutral branch names. Renaming a local project branch requires reconciling `workflow.toml`, consumer metadata, current routing, and its remote upstream; it does not require renaming the `project-workflows/` folder or deleting the old remote branch. Keep historical references identifiable as history.

For a project that already includes the submodule, clone with submodules or initialize them after cloning:

```sh
# In the already-cloned parent repository:
git submodule update --init --recursive
```

See [Git's submodule reference](https://git-scm.com/docs/git-submodule) and [gitmodules reference](https://git-scm.com/docs/gitmodules) for the Git mechanics.

## Dependencies and client installation
These are Markdown procedures with supporting templates. They need ordinary document access and Git for versioning; no Python, uv, service account, personal vault, or Agent Hands installation is required. The project procedures travel together, without unrelated personal or service skills. Optional forge operations use the selected platform tooling and its own dependencies.

Each skill is a complete top-level directory containing `SKILL.md` and any supporting assets or client metadata. Project adoption and global client installation are separate choices. A project can route agents directly to these files through its instructions; do not assume every agent client automatically discovers skill folders. Use the project's adopted version when available so its procedures match its pinned history and local choices. Verify routing in the actual client after adoption.

## License
Published at [jcklpe/project-workflows](https://github.com/jcklpe/project-workflows) under [AGPL-3.0-only](LICENSE).
