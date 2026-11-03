# Project Workflows
Reusable agent skills for organizing project documentation, working through implementation spikes, reviewing proposed changes, and making scoped commits. Keep the procedures alongside your code so someone cloning the project can understand how its documentation and development workflow operate.

## Get started
Open the project in your chosen agent client. The robot icon marks prompts to copy and paste into your agent's chat. These prompts ask the agent to read the skill files, so you can begin before registering skill names in the client.

<a name="set-up-a-project"></a>
<h3><img src="assets/agent-hands-head-thumbs-up.png" height="32" alt="Robot head giving a thumbs-up"> Set up a project</h3>
When the project has not adopted a workflow source yet, use [Setup Project Workflows](setup-project-workflows/SKILL.md). **Copy and paste this prompt into your agent:**

```text
Read setup-project-workflows/SKILL.md from https://github.com/jcklpe/project-workflows and help me set up Project Workflows in this project. Inspect its existing instructions and documents first, preserve its conventions, and help me choose pinned or global-only use. Configure the selected workflow and show me how to start contribution work.
```

<a name="join-an-existing-project"></a>
<h3><img src="assets/agent-hands-head-thumbs-up.png" height="32" alt="Robot head giving a thumbs-up"> Join an existing project</h3>
The project adopts its workflow once; each collaborator gets that declared source ready in their own checkout and agent client. You do not need the maintainer's personal configs, global skills or service accounts. To use the [collaborator onboarding route](setup-project-workflows/SKILL.md#onboard-a-collaborator), **copy and paste this prompt into your agent:**

```text
Read this project's README and AGENTS. Help me get its declared Project Workflows source ready in my checkout, then read that source's setup-project-workflows/SKILL.md and follow "Onboard a collaborator". Preserve the project's pins, adaptation branch, configuration and other contributors' work. Start with direct file-based skill use and explain any optional client discovery setup. Finish by showing me how to start coordinate-project-contribution here.
```

<a name="start-contribution-work"></a>
<h3><img src="assets/agent-hands-head-thumbs-up.png" height="32" alt="Robot head giving a thumbs-up"> Start contribution work</h3>
Use **[Coordinate Project Contribution](coordinate-project-contribution/SKILL.md)** as the entry point for starting work with another person. **Copy and paste this prompt into your agent; it will ask you to describe your contribution:**

```text
Read coordinate-project-contribution/SKILL.md from this project's selected workflow source and ask me to describe the contribution I want to make, then help me start it. Read the project instructions, work index and relevant records; follow the humans' existing direction. For forge work, reconcile/reuse an existing issue or prepare an approved new one, then select/create the appropriate contribution branch before starting development spikes or implementation. Use run-project-spike for your own agent-owned thread when needed. Preserve other agents' spikes and the current branch arrangement, use commit-work for atomic checkpoints, and surface material blockers. When the work is reviewable, prepare an overview and propose contribution boundaries from the actual commits and dependencies.
```

Already set up and upgrading the workflow itself? Use [Update Project Workflows](update-project-workflows/SKILL.md) to preserve the project's adaptations and reconcile its selected source.

For optional project-board and lifecycle setup, use [Setup Project Workflows' board route](setup-project-workflows/SKILL.md#optional-board-and-lifecycle-setup). Its [GitHub starter pack](setup-project-workflows/references/github-starter-pack.md) includes issue/PR templates, editable profiles and hosted Actions automation. Setup guides credentials only for selected forge setup. Local use and collaborator onboarding require no board or language runtime.

## How collaboration fits together
[Run Project Spike](run-project-spike/SKILL.md) keeps each agent's reasoning, execution state and QA in its own spike. People coordinate shared outcomes through their existing records.

Follow the humans' existing coordination and project records. [Coordinate Project Contribution](coordinate-project-contribution/SKILL.md) connects that direction to each agent's execution and review without imposing a negotiation process or prerequisite agreement checklist. Raise concrete blockers for the people involved to resolve.

Local work uses the project's existing documents, checks and QA without a forge or service tooling. If forge coordination is explicitly selected, issues own discussion, tracking, progress and acceptance; linked PRs are discrete contribution review/integration points. Reconcile the approved issue, select/create the contribution branch, then start agent-owned development spikes/work. Several PRs can serve one issue; partial contributions leave unfinished acceptance open. Board cards represent issues by default, with linked PR information visible; PR cards require an explicit project exception. Agent-owned spikes retain detailed execution. Tool/client choice remains personal. Agent Hands provides optional platform tooling for supported agent operations, and a human can handle a step with their own tools. Missing agent tooling calls for a specific handoff, not automatic installation or access changes.

One branch may host many agent-owned spikes, several issues and multiple eventual change requests. Use Commit Work's atomic targeted commits and spike trailers to identify reviewable groups when they are sufficiently separable; no one-issue/one-branch/one-change-request format is required. Prepare a focused review overview with evidence and links, retaining suitable tracked documents and every original atomic commit. Follow the project's authorization and human publication/integration boundaries. A merged contribution, completed shared outcome and closed spike are separate states.

## Included skills
| Skill | Purpose |
| --- | --- |
| [setup-project-workflows](setup-project-workflows/SKILL.md) | Set up a project, onboard collaborators, or guide optional board/lifecycle setup; preserve existing project choices. |
| [coordinate-project-contribution](coordinate-project-contribution/SKILL.md) | Kick off contribution work, link agent-owned spikes to shared outcomes, and prepare review or integration. |
| [update-project-workflows](update-project-workflows/SKILL.md) | Compare against shared ancestry and reconcile upstream improvements while preserving intentional project differences. |
| [create-agent-policy](create-agent-policy/SKILL.md) | Assess need/ownership and draft a new obligation's initial scope and identity. |
| [edit-agent-policy](edit-agent-policy/SKILL.md) | Assess change intent, identity continuity and dependents while preserving the operative version. |
| [review-agent-policies](review-agent-policies/SKILL.md) | Review meaning/ownership and run shared graph/index checks. |
| [adopt-agent-policies](adopt-agent-policies/SKILL.md) | Apply explicit adoption, including initial kernel adoption and reviewed revisions. |
| [retire-agent-policy](retire-agent-policy/SKILL.md) | Retire an obligation with dependent review and reserved identity/history. |
| [run-project-spike](run-project-spike/SKILL.md) | Keep reasoning and task documents together, track QA, and preserve closure history. |
| [triage-project-misc](triage-project-misc/SKILL.md) | Route loose scratch observations into the appropriate project records. |
| [draft-approval-slate](draft-approval-slate/SKILL.md) | Present concrete external or hard-to-reverse changes for human review. |
| [commit-work](commit-work/SKILL.md) | Review scope and make coherent commits under the project's actual policy. |
| [capture-for-later](capture-for-later/SKILL.md) | Save possibilities and deliberately parked subjects as small individual scratch notes, without starting work. |

`capture-for-later` is the sole entrypoint for saving possibilities and deliberately parked subjects. Existing notes remain valid and are not migrated by installation.

The collection contains procedures and templates, not an autonomous project manager. The current project's instructions and authorized task determine which procedures apply. Installing these skills does not authorize publication or external writes.

## Agent policies
Five task-specific policy skills use the kernel-owned record contract and header example, with one structural/index tool. The [kernel candidates](adopt-agent-policies/assets/kernel/policy.index.md) state durable obligations, define policy metadata and distinguish policies from skills; the skills supply task procedures under those obligations. For explicit adoption, keep frozen project-owned copies in the selected agent-policy location and route AGENTS to `policy.index.md`. Only an authenticated human decision plus `adopted` status makes a policy operative in that checkout. These policies govern agents, never humans; contribution and shared-branch acceptance remain separate. IDs identify obligations, prerequisites form a graph, and reading order never confers precedence.

The new `documents.agent_policies` default is `docs/agent-policies/`; existing `documents.policies` and legacy paths remain valid. Missing new configuration does not retire old rules or adopt the new kernel. Follow the [deliberate migration route](adopt-agent-policies/references/migration.md) rather than mass-renaming consumers. A collection upgrade delivers candidates without replacing operative project copies. Policies use YAML `---` frontmatter and descriptive `type: kernel` or `type: operational` labels. Kernel filenames start with `_` before their unchanged ID, as required by the naming policy; operational filenames are unprefixed. Neither type nor prefix confers precedence. The [optional checker](review-agent-policies/scripts/policies.py) uses an existing Python 3.11+ and supported YAML parsing through existing PyYAML or Ruby/Psych; ordinary Markdown use requires no runtime or validation run. It checks structure, not policy meaning, human intent or agent/tool compliance.

## Installation choices
A Git project can pin this collection as a root-level `project-workflows/` Git submodule or explicitly use installed global skills with project-owned policy/configuration. New pinned adoptions use an unchanged shared package, a project-owned `docs/workflow.toml` (or the project’s existing documentation folder) and optional local workflow notes. The parent pins an exact shared revision; no adaptation branch or localization commit is needed. Existing branch-based adoptions retain their configuration, branches and update route until a separate migration is authorized. An explicitly designated canonical maintenance/global installation uses shared `main` directly. Local procedural experimentation can live in project-owned notes; a deliberate source experiment may retain its own reviewed adaptation.

These are Markdown procedures with supporting templates. They need ordinary document access and Git for versioning; no Python, uv, service account, personal vault, or Agent Hands installation is required. The project procedures travel together, without unrelated personal or service skills. Optional forge operations use the selected platform tooling and its own dependencies.

Each skill is a complete top-level directory containing `SKILL.md` and any supporting assets or client metadata. Project adoption and global client installation are separate choices. A project can route agents directly to these files through its instructions; do not assume every agent client automatically discovers skill folders. Use the project's adopted version when available so its procedures match its pinned history and local choices. Verify routing in the actual client after adoption.

For a global-only project, use its declared workflow source/version and target-owned instructions/configuration. If the collection is missing locally, have the setup agent retrieve the selected complete source into a location you choose outside the project. Keep its supporting resources available. A global installation does not replace a project's pinned copy or supply another project's configuration.

Your agent can read the selected `SKILL.md` files directly and follow their sibling resources. Optional client registration makes supported named invocations such as `$coordinate-project-contribution` available; verify discovery in that client before relying on the name. Service tooling is a separate choice when the work needs it.

## Manual Git setup
The setup skill handles project instructions, copied-skill reconciliation, configuration and routing. The commands here are for inspecting the collection or doing the Git portion manually.

### Inspect the collection
You can clone the collection separately to inspect it:

```sh
git clone https://github.com/jcklpe/project-workflows.git
```

### Start a pinned adoption
Run this from the adopting repository's root after selecting the exact shared revision:

```sh
git submodule add -b main https://github.com/jcklpe/project-workflows.git project-workflows
git -C project-workflows checkout --detach ACCEPTED_SHARED_COMMIT
```

Then adapt the [project configuration template](setup-project-workflows/assets/templates/workflow.toml.template) into the parent's `docs/workflow.toml` or existing documentation folder, declare its exact path in AGENTS and follow the setup skill to review routing. These commands alone do not configure a project. The shared package stays unchanged; local procedures and choices belong to the parent. Preserve an existing adapted checkout rather than running these commands over it. A separately selected source experiment follows the adaptation route and its publication/privacy rules.

### Restore a project's workflow checkout
Clone the team's project using its documented instructions. For a project with an uninitialized root-level workflow submodule, run this from the project root:

```sh
git submodule update --init --recursive -- project-workflows
```

This restores the project's recorded workflow version. Preserve an already active checkout and follow its instructions rather than rerunning setup over other work. The maintainer must make the pinned revision available at the recorded URL before another person can retrieve it; report an unavailable pin rather than substituting a different version.

See [Git's submodule reference](https://git-scm.com/docs/git-submodule) and [gitmodules reference](https://git-scm.com/docs/gitmodules) for the Git mechanics.

## Where things live
An adopted project might look like this; existing project conventions can use different document locations:

```text
your-project/
  README.md
  AGENTS.md
  TODO.md
  docs/
    workflow.toml            # Project settings; root "..", adoption.mode "shared"
    active-spikes/
    scratch/
    archive/
    policies/                # Existing legacy conventions may remain.
    agent-policies/          # Only when explicitly adopting the agent-policy system.
      policy.index.md
  project-workflows/          # Git submodule; parent pins an exact commit
    workflow.toml            # Unchanged neutral defaults/example, not project settings
    setup-project-workflows/
      SKILL.md
      assets/templates/
    update-project-workflows/
    ...
```

For an adoption, actual project documents and settings stay in the parent repository. The unchanged submodule contains common procedures, templates and neutral defaults. Existing adapted layouts remain supported. The package should not accumulate another project's narrative, document history, credentials or private context.

## Agent reference
These details explain how agents select the owning project, interpret its configuration and maintain an adoption. The starting prompts above route to the relevant skills.

### Resolve the target
The target is the project or folder the person asked the agent to work on. These instructions keep a globally installed skill from treating its own installation checkout as that project.

Resolve the requested project or folder before reading collection configuration or choosing document paths. Prefer the explicit target in the request; otherwise use the active working context and its nearest applicable instructions. Inspect the target's actual Git boundary separately from its document/workspace boundary. If several plausible targets remain, ask which one before writing; a skill's installation path is never a target-selection fallback.

Before using defaults, read the target's applicable instructions and the project policies, local adapters and configuration they declare. Follow the declared workflow source: a pinned adoption uses its own complete collection; an explicitly global-only target uses installed global procedures with its target-owned overrides. If the source is undeclared, preserve an existing adoption or local skill convention rather than silently switching it. A plain folder uses global skills and its own conventions without an automatic repository, clone or submodule. A folder inside a repository follows its applicable instructions; it is not automatically an independent adoption.

Select configuration from the target's declaration, not from the installed skill's directory. New shared-source pinned and global-only targets put configuration in `docs/workflow.toml` or their existing documentation folder, such as `_meta/workflow.toml`. AGENTS links the exact selected path. Existing root configs and adapted `<target>/project-workflows/workflow.toml` remain supported. The helper accepts an explicit `--config PROJECT_RELATIVE_PATH`; without it, one file among `docs/workflow.toml`, `_meta/workflow.toml` and legacy root `workflow.toml` may select shared mode. Multiple candidates require explicit selection. Parent configuration cannot hide a localized child or authorize an implicit migration. If no configuration is declared, use the target's existing documented locations; a config file is not required merely to invoke a skill. Never substitute the global installation's `workflow.toml` or its consumer-relative `..`. A declared policy, adapter or config that is unavailable is a specific gap to report, not permission to silently apply defaults. Read only relevant declared context and parse configuration as data.

When invoking a skill, also read its entry in the selected configuration's optional `[workflows]` table. Each key is that skill's name and each value names one project-relative Markdown note. Read that note before applying the shared procedure, together with relevant declared policy prerequisites; follow its links when required, rather than loading every project's workflow note. An unavailable required note is a gap for the affected work, not a reason to ignore it. Existing AGENTS-declared local guidance remains supported. These are instructions for agents, not automatically executed hooks or an independent policy/adoption mechanism. Report substantive contradictions for human resolution.

When the explicit task is development of Project Workflows itself, use this repository's [maintenance instructions](AGENTS.md#maintaining-this-collection), [work index](TODO.md), and root skills. Its `docs/` is an ordinary directory in the same repository, not a copy of the workflow collection nested inside itself.

### Configuration
[workflow.toml](workflow.toml) illustrates project identity, document locations, optional adoption metadata and validation commands. Resolve `project.root` relative to the directory containing the selected config file, then document locations relative to that root. Thus `docs/workflow.toml` and `_meta/workflow.toml` normally use `project.root = ".."`; an existing root config uses `"."`, and a root-level `project-workflows/` submodule config keeps `".."`. Existing pinned configs retain their meaning. Project instructions identify the config and override seed conventions. Global-only targets omit submodule branch/pin metadata rather than inventing an adoption. Keep nonsecret project choices with the project under its tracking policy; credentials are not workflow configuration.

For a new unchanged pinned adoption, adapt the [project configuration template](setup-project-workflows/assets/templates/workflow.toml.template). Parent-owned `adoption.mode = "shared"` selects the exact-source updater route. Use `project.root = ".."` for a config directly under docs or _meta and omit `project_branch`; shared-source metadata describes the intended source while the gitlink remains the exact version pin. Project document paths and coordination settings live here, rather than in the package. A plain folder/global-only project omits the adoption table.

Local procedures can use any existing project folder; `docs/workflows/` is an ordinary example, not a required scaffold. Add a reference only when the corresponding note exists:

```toml
[workflows]
run-project-spike = "docs/workflows/spikes.md"
capture-for-later = "work-notes/capture.md"
```

Notes hold concrete local procedure, context and QA examples, with links to their policy owners. Keep standing obligations, operative policy copies, private context and authorization with their existing owners. The helper validates declared note paths inside the parent, reports their mapping and preserves their bytes; it does not execute them, adopt policies or prove future agent compliance. Configuration and these notes are not auto-refreshed template assets.

Use the [local workflow-note format](setup-project-workflows/references/local-workflows.md) and optional [starter](setup-project-workflows/assets/templates/local-workflow.md.template) to state the selected skill, scope, actual changed steps and relevant checks. Reassess whether an old customization is still useful before preserving it as a note. The shared kernel candidate describes its authority boundary; operative policy copies retain their actual adoption status.

No workflow env file is required. If a project already declares private-context configuration, preserve its own discovery and access rules; do not invent a new pointer or read unrelated private material. A global skill installation must never infer the current project from its own source directory.

Coordination is optional and defaults to local use. A project can declare it in its maintained instructions or the selected configuration's optional `[coordination]` table: `mode` is `local` or `forge`, `repository` identifies the intended target URL, and `tooling` points to project-owned guidance naming the selected setup/use skills and their source/version. Leave `tooling` empty when a human handles platform steps. An explicit request may select one operation without persisting these choices. Credentials remain with the platform tooling owner. A remote or installed tool does not enable coordination or authorize writes; see [Coordinate Project Contribution](coordinate-project-contribution/SKILL.md).

The [setup templates](setup-project-workflows/assets/templates/) provide starting points for agent routing, the task index, and ignore rules. Adapt them to the project rather than replacing existing instructions wholesale.

### Project branches and updates
Shared `main` is the reusable baseline and the branch for an explicitly designated canonical maintenance/global installation. Such an installation keeps neutral `workflow.toml` defaults and uses its containing project instructions without creating an adaptation merely to record its name. This does not make every global skill installation canonical.

New shared-source pinned adoptions keep the submodule detached at the reviewed shared commit and own configuration/procedural notes in the parent. An update selects the exact forward shared revision without merging project data into the package. Existing project branches remain supported; they use the legacy ancestry-preserving merge and setting-preservation route. A project choosing a source experiment can keep an adaptation deliberately, without making every configuration-only adoption create one.

Use [update-project-workflows](update-project-workflows/SKILL.md) for routine ancestry-based updates: fast-forward or three-way merge, retained project settings, focused review of customized overlaps, copied-template reconciliation and exact parent pins. Its optional Git/standard-library helper needs an existing Python 3.11+ and Git 2.38+, with no packages or environment; ordinary Git remains available. Selected copied assets retain their source baselines in the parent’s `.project-workflows-assets.json`. Repeating a completed update is a no-op. Exceptional contribution/migration procedures are loaded only when selected. Separate reusable improvements onto the shared `main` baseline without project-only configuration, integrate them through the authorized upstream route, then merge accepted `main` into each project branch while preserving its customization. Review complete outgoing commit ranges before publication and update exact consumer pins from the deepest child outward. The update procedure also covers branch renames, tracking metadata, blocked publication, and fresh recursive-clone verification.

Ordinary submodule checkout restores the parent's recorded commit and may leave a detached HEAD. That is the intended state for unchanged shared-source adoption. Select a declared adaptation branch only for that existing layout, or shared `main` for designated canonical maintenance. Never edit a consumer's unchanged package merely to record project data. A branch name in `.gitmodules` does not replace the exact commit pin, and configuring `origin` does not publish local commits. Before publishing a parent pin, make the required child commit available from the submodule URL collaborators will use. Existing project branches such as `project/example` remain owned by their adoptions; no rename or deletion follows from the new layout.

Use platform-neutral branch names. Renaming a local project branch requires reconciling `workflow.toml`, consumer metadata, current routing, and its remote upstream; it does not require renaming the `project-workflows/` folder or deleting the old remote branch. Keep historical references identifiable as history.

## License
Published at [jcklpe/project-workflows](https://github.com/jcklpe/project-workflows) under [AGPL-3.0-only](LICENSE).
