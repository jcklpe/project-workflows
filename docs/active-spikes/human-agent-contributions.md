---
attention: live
reviewed: 2026-10-30
tags: [project-workflows, collaboration]
---

# Human and agent contribution workflow

**First implementation authorized on October 30, 2026.** Build a small usable contribution workflow and refine it through real work and relevant Kaizen feedback. Each spike belongs to one agent and one thread; independent agents use distinct records even when working for the same person. Current reusable guidance lives in [Coordinate Project Contribution](../../coordinate-project-contribution/SKILL.md), [Run Project Spike](../../run-project-spike/SKILL.md) and the [collaborator quick start](../../README.md#join-an-existing-project). [Tasks](human-agent-contributions.todo.md) hold implementation, review and remaining work. Publication and consumer rollout remain separate.

## Purpose
Extend Project Workflows with platform-neutral collaboration management and a usable collaborator README path. Each project spike records one agent's thread of work within a contributor's context. When a project opts into forge coordination, its work items, contribution branches and change requests coordinate work between people. GitHub is the first implementation target; the workflow must also be usable with later GitLab, Gitea, Codeberg or Forgejo routes without rewriting its collaboration semantics.

Forge coordination is optional. Private and local projects can use Project Workflows without hosted work items, a mandatory contribution branch, a pull/merge request, remote publication, credentials or a forge adapter. Keep the existing spike process and rich atomic commit history under the project's actual Git policy.

A spike is a bounded workstream owned by one agent/thread. Architecture requirements below are user decisions. The first implementation uses `coordinate-project-contribution` and a small optional coordination table; further packaging and tooling extensions remain separate work. This spike owns Project Workflows semantics, onboarding and adapter consumption. Agent Hands owns a separate implementation spike for forge setup/use capabilities.

## Coordination layers and their bridge
| Layer | Owns | Coordination audience |
| --- | --- | --- |
| Project `docs/` and spike concept/task records | Detailed reasoning, agent execution steps, checkpoints, validation evidence and local QA/handoff state | One owning agent/thread per spike, with history available to other agents and later readers |
| Optional code-forge work items, contribution branches and change requests | Shared outcomes, cross-person ownership, dependencies and interfaces, progress/blockers that affect others, review and integration decisions | People collaborating with one another, including their agents acting within authorization |

In GitHub, the second layer uses issues and PRs. Other adapters map their own terms and capabilities to the same roles. It exists only when selected for the project or explicitly requested operation. Local mode keeps collaboration agreements in the project's existing authorized records and needs no substitute hosted tracker.

The first layer's scope does not mean its files stay private or unpublished. When a contribution is published, suitable tracked project documents and every original atomic commit still travel with it; private personal context stays with its authorized owner.

For opted-in collaboration, begin from the shared outcome, link the relevant spike and contribution, work through agent steps in the spike, and share meaningful progress, changed interfaces, blockers and review requests through the selected forge. Shared records own cross-person agreements and deliverable status; the spike owns detailed execution state. Independent agents keep distinct spikes linked to the common outcome. Do not mirror every checkbox or create a second team execution ledger.

The README should explain both local operation and the opt-in bridge. A local agent checkpoint does not itself complete a shared outcome. Integrating a contribution does not automatically close a broader spike or umbrella work item.

## Workflow and adapter ownership
Follow the same separation used by [Wireframe Workflows](https://github.com/jcklpe/wireframe-workflows) and a tool skill such as Agent Hands' `use-penpot`: the workflow describes the work and required capability; the tool owner supplies platform tooling and declares supported operations.

- **Project Workflows:** contribution scope, ownership and interfaces, review readiness, linking shared outcomes to local records, history/QA/handoff requirements, optional coordination selection and collaborator onboarding.
- **Agent Hands:** platform tooling, including forge-specific setup, installation, identity/authentication, host/repository resolution, supported reads and writes, API/CLI commands, previews, execution safeguards, result verification and capability limits. GitHub is first; names such as setup/use-gitlab, setup/use-gitea, setup-codeberg and setup/use-forgejo describe possible later adapters, not existing implementations.
- **Consuming project and people:** choose coordination mode and adapter, own project-specific agreements and access, authorize particular actions, supply acceptance evidence and make human review/publication/integration decisions under local policy.

Workflow logic must request a neutral capability and expected result, then route to the selected setup/use owner. Do not embed gh, glab, forge API endpoints, provider-specific flags or account setup in the workflow skill, or silently bypass a missing adapter operation through an ad hoc shell command. A declared unsupported operation gets a precise human handoff or a separately authorized Agent Hands extension. No new daemon, generic service broker or uniform API library is required merely to define this boundary.

## User-adopted direction
- Each spike belongs to a single agent and thread of work; collaborators and independent agents do not share spikes. Link distinct spikes to optional forge records for coordination between people without checkbox mirroring or duplicate trackers.
- Keep Project Workflows platform-neutral. Consume separate Agent Hands setup/use capabilities for the selected forge; start with GitHub while allowing later forge adapters.
- Forge coordination is optional. Local/private work must remain complete without mandatory issues, contribution branches, change requests or remote publication.
- Keep suitable project reasoning and execution history in tracked documents. Preserve every small original atomic commit when publishing; do not squash, flatten or reduce history for presentation.
- Present a coherent contribution through a readable review overview when a forge is used, rather than a hosted ticket or review request for every internal agent step.
- Prepare collaborator README guidance for local use and optional shared coordination, preserving personal tool/client choice.
- Track Project Workflows and Agent Hands implementation in separate owning spike pairs so different agents can execute the workstreams. Tool implementation belongs in Agent Hands.
- After the workflow and first adapter satisfy their acceptance gates, prepare an inventory and controlled update plan for consuming repositories. Consumer rollout remains separate from the first workflow implementation.
- Humans mediate collaboration agreements; the workflow follows those decisions without a formal negotiation process. A branch can host many agent-owned spikes, several issues and multiple eventual change requests, with atomic targeted commits and spike trailers retaining traceable scope.

## Unresolved design questions
- In forge mode, what signals from actual commit scope and dependencies trigger a reviewable slice, a combined/dependent review or a linked successor?
- For a shared branch containing several spikes/issues, which actual commit groups and dependencies can become separate, combined or dependent change requests? There is no required one-issue/one-branch/one-change-request mapping.
- How should real use refine the small contribution skill while preserving existing run-project-spike, commit-work and QA/handoff ownership?
- How well does the workflow follow human-mediated decisions and surface actual interface/review blockers without imposing a negotiation process?
- Which supported integration method preserves the required original history under repository policy? The adapter reports the selected forge's actual capabilities and restrictions; do not change settings automatically.
- How much shared task tracking will collaborators actually use? A technically complete board is not evidence of adoption.

## Candidate guardrails to evaluate, not adopted policy
- In opted-in forge coordination, open or update a change request for a coherent, testable, independently explainable contribution rather than at an arbitrary commit count.
- Split a sprawling spike when purpose, dependencies or acceptance criteria change; preserve continuation links and rationale.
- Use a readable review overview covering purpose, scope, validation, decisions and open questions, with links to the tracked spike; a forge adapter maps it to the platform's change request.
- Keep cross-person review and explicit integration checks distinct from local multi-agent editing safety.
- Preserve user/repository authorization for commits, pushes, issue writes and merges. Nothing here grants remote-write permission.

## Investigation and existing coverage
The October 29 planning pass read the actual maintenance instructions, README, neutral configuration, work index, existing spike pair and owning skills. This collection's maintenance instructions place its own pair in `docs/active-spikes/`; the consumer-oriented `project.root = ".."` does not redirect it into the containing repository. The original draft consulted [shared Run Project Spike](https://github.com/jcklpe/project-workflows/blob/main/run-project-spike/SKILL.md); the current checkout is the basis for this reconciliation.

| Existing owner | Reuse instead of duplicating |
| --- | --- |
| [Run Project Spike](../../run-project-spike/SKILL.md) | Concept/task pair, index, human QA and preserved task transitions, handoff context, continuation links, closure approval and archival |
| [Commit Work](../../commit-work/SKILL.md) | Coherent atomic checkpoints, same-clone index/scope safety, privacy, trailers, review holds and history-rewrite safeguards |
| [Draft Approval Slate](../../draft-approval-slate/SKILL.md) | Concrete external-write proposals and approved scope |
| [Update Project Workflows](../../update-project-workflows/SKILL.md) | Collection-specific upstream/adoption integration, outgoing-range review and published-ref verification |

The contribution skill connects agent execution records to shared contribution ownership, cross-person review and deliberate integration. Existing QA and continuity records retain their authority. Forge coordination remains optional, and platform tooling stays with its selected owner.

## First implementation
[Coordinate Project Contribution](../../coordinate-project-contribution/SKILL.md) supports framing, coordinating, reviewing and integrating a coherent contribution in local mode or an explicitly selected forge mode. Ordinary checkpoints continue to use Commit Work directly. Each agent retains its own spike; the contribution can link several agent-owned threads.

The lifecycle reuses existing owners:
1. **Resolve context and mode.** Read target instructions, existing spike and selected configuration. Missing coordination configuration means local mode. A configured remote, installed adapter or authenticated account does not enable forge coordination or authorize writes.
2. **Follow human direction.** Use existing human decisions and project records for scope, interfaces and review. People mediate their own agreements; no role checklist or negotiation procedure is a prerequisite. Raise concrete blockers where they affect the next work. In forge mode, reuse relevant shared records and link the owning spikes without creating hosted records for internal agent steps.
3. **Use the actual work boundary.** Follow project working-copy and Git policy. A branch may host many agent-owned spikes, several issues and multiple eventual change requests. Commit Work keeps atomic scope and multi-spike overlap traceable; no branch-per-spike or branch-per-issue rule is required. Never switch another contributor's active checkout beneath their work.
4. **Use existing local workflows.** Run Project Spike owns reasoning, execution state, QA and handoff; Commit Work owns checkpoints. Preserve directly associated docs and every original atomic commit. Local mode can finish through validation and the existing QA/closure procedure without entering a forge lifecycle.
5. **Coordinate through the selected adapter when enabled.** Request only capabilities supported by that adapter: read shared context, prepare meaningful shared updates, or prepare a review request with purpose, scope, evidence and links. The adapter owns tool-specific previews/commands and reports exact targets and outcomes. Honor the user's existing action scope and project policy.
6. **Prepare publication and review.** Only when publication is actually intended, inspect the complete outgoing range for scope, privacy, tracked docs and all original commits. The human publishes under current no-push rules. Review the actual contribution and integrated meaning, not only its summary or absence of textual conflicts. If the target changes, reassess affected evidence.
7. **Integrate and verify within authority.** The selected adapter or human reports the platform's supported methods and restrictions. Choose an authorized method preserving every expected original commit; do not squash, rewrite, drop commits or change protection settings to force integration. Verify resulting records, exact reviewed head and history reachability. Local mode verifies its local result without asserting remote availability. Existing QA/closure rules still apply; shared-item closure and branch deletion are separate scoped actions.

The first version adds the contribution skill, collaborator README/setup/routing guidance, single-agent spike ownership and a small optional `[coordination]` table. It adds no board, duplicate task schema, new QA system or change to commit mechanics. The optional first platform tooling remains in Agent Hands; consumer installation and publication are separate work.

## Opt-in and configuration requirements
- **Default:** local operation when coordination is absent or disabled. Do not require a forge account, adapter, network access, issue, branch, change request or remote publication merely to run Project Workflows. Existing project Git/worktree rules remain in force.
- **Explicit selection:** the consuming project's maintained instructions or declared configuration identifies an enabled coordination mode and intended host/repository, plus the selected setup/use tooling and source/version for agent-operated steps. A human-operated platform step needs no installed adapter. An explicit current user request can select a particular operation without silently persisting a new project-wide mode.
- **Neutral configuration:** represent roles such as coordination mode, adapter reference, target repository and shared-record links without baking in GitHub-specific keys, labels, project IDs or PR commands. The first version uses `mode = "local"` or `"forge"`, a `repository` target URL and a `tooling` reference to project-owned guidance naming setup/use skills and their source/version. Maintained project instructions may supply the same selection; no config file is required merely to use the workflow. Preserve existing configured workflow sources and project overrides.
- **Provider-owned secrets:** authentication, account profiles, tokens and provider-specific settings stay with the selected setup owner in ignored/private configuration. Project Workflows stores no credentials and does not duplicate provider configuration. Keep private host/repository metadata private when the project requires it.
- **Capability checks:** the adapter declares which operations it supports for the chosen target/account. Missing adapter, unsupported operation or unavailable access blocks that operation with a precise handoff; local independent work continues. No silent provider fallback or automatic installation, authorization broadening or feature-parity assumption.
- **Authority:** enabling coordination is not blanket permission to post, assign, review, merge, publish or notify. Concrete action scope and repository policy remain authoritative; credentials prove access, not authorization.

## Change-request boundaries and sprawling spikes
These requirements apply only when forge coordination is enabled. A change request bundles a reviewable contribution; a spike holds one agent's evolving thread. One branch can host many spikes, several issues and several change requests as work becomes sufficiently separable. Use atomic targeted commits and spike trailers to find actual scope; no one-to-one mapping is required. Mixed or dependent changes may need combined/dependent review, and targeted commits alone do not prove that a separate publication ref can preserve all original history.

Proposed boundary test: can a reviewer explain the outcome, assess its evidence and accept or defer it without accepting an unrelated change? If yes, it is a candidate change request boundary regardless of the number of atomic commits. Several independently reviewable outcomes may use linked change requests within a still-coherent spike. Several spikes may support one inseparable outcome if the change request links each and carries their documents and commit history.

Revisit scope when purpose, acceptance criteria, dependencies or ownership changes; when new work repeatedly postpones an already reviewable result; or when review requires understanding unrelated systems. Keep that slice visible. Propose a split or successor through the existing continuation-link procedure when the theme itself changes. Do not silently widen agreed scope, invent commit/line-count thresholds or archive a spike merely because one change request merged.

A work item spanning several outcomes stays open until its own acceptance criteria are met. Partial change requests link it descriptively rather than using an automatic closing keyword on an unfinished umbrella work item.

## Paper walkthroughs and limits
**Two contributors in forge mode.** One shared outcome needs a data loader and a UI using its agreed interface. Contributors use separate branches/copies and agree the interface plus review responsibility in existing records. If independently reviewable, two linked change requests and separate agent-owned spikes can serve one work item. Each carries its tracked notes and every atomic commit. After the loader integrates, the UI contributor incorporates the target through a permitted history-preserving merge, resolves semantic conflicts and reruns integration checks; the reviewer assesses the updated head. Each agent updates its own spike. Shared interface or implementation files still need ownership/reconciliation; shared outcomes remain in the work item. The work item closes only when the whole outcome is accepted.

**Parallel spikes on one branch.** An importer agent and a deployment agent keep distinct spikes while their atomic targeted commits land on one branch. Several issues may describe the outcomes. When the importer is ready, inspect actual commits, shared-file overlap and dependencies to identify a reviewable contribution. Separate change requests are useful when the work can be untangled under the history policy; combined or dependent review may be appropriate when it cannot. Do not create a branch per spike as a prerequisite, silently rewrite commits to manufacture separation or close either spike merely because a change request merged.

**Local/private work.** A contributor starts from project instructions and a spike, performs scoped work, validates it and records QA/handoff or closure under existing rules. No hosted record, dedicated contribution branch, service setup or publication is required. A later choice to enable shared coordination maps the relevant outcome and evidence without mirroring the complete task list.

These are conceptual walkthroughs, not live adapter or integration tests.

## First-adapter research: GitHub, not core workflow logic
[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) describes contribution branches, separate branches for unrelated work, PR summaries, draft feedback and review updates. This proposal adapts that surface to the existing local owners; GitHub's publication/deletion steps grant no agent permission.

[GitHub's merge-method reference](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges) documents that merge commits preserve branch history, squash combines commits, and GitHub rebase-and-merge creates new commit identities and can drop originally empty commits. The merge-commit recommendation follows from preserving every original atomic commit.

Read-only `gh api` checks on October 29, 2026 found default branch `main`, merge/squash/rebase methods all enabled, and automatic branch deletion disabled. The branch summary reported `main` unprotected; effective branch rules were empty. A merge-commit route is currently available at this settings level. Recheck the actual target before eventual integration; these observations neither recommend settings changes nor prove a future PR passed its checks.

## Non-goals
- No ticket for every local step; no duplicate parallel task ledger.
- No squashed history, concealed workflow documents, or mandatory per-file commit rule.
- No automatic pushes, merges, task assignments, repository-settings changes or adoption across other projects.
- No importing private meeting notes, teammate assessments, personal paths, credentials or unrelated private context into the public repository.

## Completion shape
A focused platform-neutral contribution procedure and README path that support complete local/private operation, optional forge coordination through a selected adapter, linked local/shared records, preserved atomic history and deliberate review/integration. Check local behavior and contribution boundaries during implementation, then use the workflow in real work and refine observed friction through relevant feedback. Live platform operations and consumer changes retain their own authorization.

## First adapter and targeted capability distribution
Agent Hands owns the GitHub setup/use implementation and its separate spike. Project Workflows consumes the declared capabilities through the handoff contract below. GitHub is the first implementation target, while packaging remains open and forge coordination stays optional. The local October 30 review of [Agent Hands](https://github.com/jcklpe/agent-hands) found the following actual boundaries.

- There is no single current `use-github` skill. A likely minimum selection for this collaboration layer is `setup-github`, `use-github-issues` and `use-github-pull-requests`. Projects and Discussions are separate optional domains.
- Each selected use folder requires sibling `setup-github` provider support. Keep complete selected skill folders, scripts, references, tests and Python manifest/lock files, plus source/license notices. Bash/gh/jq handle requests; Python 3.11+ through the selected domain's uv environment or an explicit compatible interpreter handles rendering. Other providers and a personal workspace are unnecessary.
- Optional client-link installation also needs the shared `setup-agent-hands/scripts/skill_links.py` primitive and its procedure. Direct documented invocation does not require global links. Do not claim that copying just SKILL.md files supplies their runtime or that a checkout configures client discovery.
- Current Issues tooling reads/exports open issues and creates an issue after preview. It does not edit, comment on or close existing issues. Current Pull Requests tooling reads/exports open PR records and retrieved comments; it does not fetch the diff, create/review/comment on PRs, merge or push. Projects supports its bounded status move. These are useful building blocks, not a complete implementation of the collaboration lifecycle.
- Agent Hands itself adopts Project Workflows for its development docs; its GitHub runtime does not require that workflow submodule. Keep service execution with its owner and preserve the independence of reusable workflow guidance.

### Viable distribution choices, not a selected implementation
1. **Separate Agent Hands checkout with selected capabilities.** Route to the selected setup/use skills in an existing or reviewed checkout; optionally install only those skills for the chosen client. This reuses current capability selection without making every workflow consumer install a service package. The consuming project documents the expected source/version and actual access route.
2. **Consumer-owned sibling Agent Hands submodule.** An adopting project can pin the Agent Hands repository alongside its Project Workflows adoption and route only to the selected GitHub capabilities. A [Git submodule](https://git-scm.com/docs/git-submodule) records a repository revision; its path chooses where that repository is checked out, not an arbitrary source subdirectory. Optional [sparse checkout](https://git-scm.com/docs/git-sparse-checkout) can materialize selected directories plus their dependencies, while the gitlink still pins the whole repository. Sparse configuration is local working-tree setup and must be reproduced and verified for collaborators; a parent pin does not record that selection. Avoid adding Agent Hands inside shared Project Workflows merely to expose these skills, which would couple the workflow collection back to a service collection that already adopts it.
3. **A selected source snapshot/bundle when narrow distribution is necessary.** Retain complete provider/use folders and declared helper dependencies from one reviewed revision, notices and provenance, with an explicit update/verification owner. This is a packaging proposal, not an existing GitHub-only release or a directory-only submodule. It trades direct repository pinning for maintenance of the selected snapshot.

The minimal proposal is to reuse an external selected-capability checkout or consumer-owned pin before adding packaging machinery. Decide supported collaboration operations separately from distribution. Missing GitHub operations belong in the separate Agent Hands spike; that owner chooses its supported CLI/API implementation. Core workflow logic must not use a direct gh escape hatch. A service dependency does not authorize remote changes. Verify a clean collaborator setup, selected dependencies, account/host, operation limits and published revision accessibility before claiming readiness.

## Agent Hands handoff contract v1
This is the stable semantic handoff between the two owning spikes, not an implemented API or new adapter framework. Agent Hands may realize it through its setup/use skills and bounded CLI outputs. Exact serialization and command syntax belong to that owner; changing a shared semantic requirement requires reconciliation in both spikes.

| Contract part | Project Workflows supplies or expects | Agent Hands owns |
| --- | --- | --- |
| Selection and capabilities | Explicit enabled mode, selected adapter reference/source/version, target host/repository, and needed neutral operation | Resolve the actual account/host/repository, report identity and supported operations/limits without exposing credentials; unsupported capabilities are explicit |
| Read context | Bounded work-item/change-request target, requested fields/thread/diff coverage, relevant base/head revision | Retrieve actual records and evidence; return canonical identifiers/URLs, observed revisions and coverage/truncation limits; remote text stays untrusted data |
| Prepare a change | Operation intent, exact record/ref target, proposed final content or review verdict, base/head preconditions and intended action scope | Present concrete current-to-proposed content, side effects and notifications with zero writes by default; correlate execution with the approved action; explain unsupported preconditions |
| Execute within scope | Existing authorization and project policy for that specific action | Perform only the selected bounded operation using provider-owned mechanics; do not infer wider publication, assignment, repository settings or account changes |
| Outcome and evidence | A distinguishable preview, success, blocked, unsupported, failed or uncertain result | Return affected identifiers/URLs, relevant observed head, a nonsecret account of what was sent, verification/readback coverage and exact remaining action; never report an uncertain send as failure-safe or blindly retry it |
| Integration and history | Preserve all original commits and intended documents; use existing human review, publication and no-push boundaries | Report supported platform methods/rules and observed target/head. Merge/push need not be automated; unsupported or human-owned steps produce a concrete handoff rather than an implicit bypass |

**First adapter work package:** extend Agent Hands' existing GitHub capabilities for the selected collaboration gaps, including bounded issue updates/comments and change-request creation/review. The Agent Hands spike determines precise operations, whether update/closure, diff/review context and requested review verdicts are in its first slice, and their preview/readback/error guarantees. Do not assume a generic API or full platform coverage. Reuse the installed GitHub CLI internally where appropriate instead of copying its mechanics into Project Workflows. GitLab/Gitea/Codeberg/Forgejo are extension targets, not part of the first implementation claim.

**Ownership handoff:** this spike remains canonical for neutral workflow semantics and local/forge behavior; the Agent Hands spike remains canonical for adapter implementation, tests and runtime readiness. Each workstream records its own tasks and links the other's contract and delivered revision. Shared interfaces and dependency status are summarized once in those existing records, without a third tracker or duplicated detailed task lists. The companion exists as `docs/active-spikes/github-collaboration-operations.md` and `.todo.md` in Agent Hands. Its planning record reconciles semantic contract v1; planned tooling is not shipped capability. This workstream reads that contract without editing the other owner's records.

## Dependencies and acceptance gates
1. **Contract and ownership:** the two agents work from this neutral contract and their own spike pair. Project Workflows can develop local behavior and draft adapter consumption without waiting for service writes. Agent Hands can implement bounded operations without copying workflow policy.
2. **Workflow acceptance:** local/private operation completes with no forge config, adapter, network or hosted records and no newly imposed branch/change request/publication. An enabled path selects a capability owner, keeps core logic free of provider commands and preserves the two record layers. A second hypothetical forge mapping exercises terminology/capability differences without claiming a second implemented adapter.
3. **Adapter acceptance:** the Agent Hands owner records actual selected operations, account/target checks, zero-write previews, authorized execution, readback limits, stale-context handling and failed/uncertain outcomes. Offline tests are distinguished from live account and write verification. No live mutation is required merely to finish planning or install the workflow.
4. **Real use and feedback:** use the first version in ordinary project work and refine observed friction through relevant Kaizen feedback. A formal pilot or new testing framework is not a prerequisite to implementation. Live writes still require their actual targets and scope; human understanding and semantic review remain part of acceptance.
5. **README and reproducibility:** an unfamiliar contributor can follow local mode or the chosen forge path using their own supported client. Verify actual skill routing, dependencies, host/account selection and a clean accessible clone. Published-ref/recursive-clone evidence is separate from local readiness; only the human publishes under current rules.
6. **Consumer rollout gate:** accepted workflow and adapter revisions, appropriate human QA and a reviewed consumer inventory precede downstream changes. Do not update pins, instructions, README files or installations in consuming repositories as part of this first implementation.

## Later consumer inventory and rollout plan
Use the existing update/adoption procedure after the gates above; do not add another rollout framework. Inventory only owner-selected consumer roots and their actual Git/workspace boundaries. Record pinned versus global-only use, workflow source/branch/pin, local adaptations, dirty/shared-file ownership, document/routing owners, selected coordination mode, optional adapter source/version, required access, publication scope and validation. A generic update must not enable a forge for an existing local project.

Initial public collection consumers verified by this planning pass are Agent Hands (`project/agent-hands`) and Wireframe Workflows (`project/wireframe-workflows`); the designated canonical maintenance/global installation uses neutral shared main. This is not a complete consumer inventory. Additional repositories and global-only/plain-folder contexts require bounded discovery in their authorized workspace; keep private paths and project identities out of this public record.

Pilot one opted-in consumer and one local-only context, review intentional overrides through ancestry-aware updates, then stage the remaining selected consumers. Integrate and make the accepted shared revision accessible before advancing project adaptations; publish required child revisions before parent pins. Global-only consumers validate target-owned instructions/configuration and installed skill routing instead of inventing a pin. Preserve a consumer's disabled coordination mode and optional service choice. Record per-consumer readiness, actual checks and remaining publication/access gaps; a fresh clone must retrieve every promised pin before claiming collaborator availability. No automatic commits, publication or rollout is granted by this plan.

## Collaborator onboarding requirements for discussion
The October 30 direction authorizes a first version of human-facing onboarding for local work and optional platform-neutral collaboration. Only generic reusable requirements belong here; private source notes and project-specific agreements stay with their owners.

### Existing coverage and gap
The collection README explains adopting the collection, configuring its workflow source, restoring submodules and reading the included skills. Setup already requires a project README, AGENTS routing, validation and a short coordination index. Run Project Spike owns reasoning, task state, QA and handoff continuity; Commit Work owns checkpoints and same-clone scope safety. Those mechanisms remain useful.

The contribution skill links agent-owned project records to optional coordination between people through the selected forge. The README quick start orients a person joining an already configured project: read the actual instructions, agree contribution scope, keep agent work in separate spikes and prepare review evidence. Its usability with unfamiliar collaborators and their own tools remains to be observed in real work.

### Proposed minimum requirements
- **A human quick start for an existing project.** Separate joining from adopting or updating the workflow collection. Explain prerequisites, restoring the project's selected workflow source, opening the project in the contributor's chosen client, reading README/AGENTS/TODO and the relevant spike, and running the documented checks. Do not assume the maintainer's global skill installation or private configuration is available to collaborators.
- **A small first-agent prompt and visible limits.** Propose a copyable orientation prompt that asks the agent to read the actual project instructions and local/forge selection, summarize current scope and acceptance evidence, identify missing access and explain the next bounded contribution before changing anything. Explain what the human should inspect and how to resume from the saved project records. Tool/client setup and any service access remain explicit, separate choices.
- **Shared agreements with optional personal tooling.** Distinguish the team's required contribution/review agreements from a person's optional agent client, skills and service tools. Provide a usable path for someone contributing without the maintainer's personal setup. Link to a service capability only when the chosen task needs it; Project Workflows does not require Agent Hands or credentials merely to read its documents.
- **Human-mediated coordination at the right layer.** Follow people's existing decisions about scope, interfaces and review; surface concrete unresolved blockers without formalizing their negotiation or requiring an agreement checklist. In forge mode, shared records hold cross-person decisions and each linked spike holds its own agent's execution state. In local mode, use existing authorized project records. Atomic targeted commits can span many spikes/issues on a branch and support multiple later reviews when sufficiently separable. Share meaningful changes without mirroring every local step.
- **A practical contribution/review loop.** Show where to find current shared work, how the project's chosen working-copy/branch approach avoids checkout collisions, how to coordinate shared-file edits, when to ask for review, and how to reconcile a changed target. Preserve tracked workflow documents and every original atomic commit. Human review covers meaning and acceptance evidence as well as conflicts; the existing QA and closure workflow retains its authority.
- **Access, privacy and human understanding.** State the project's actual write/publication boundaries, keep private material and secrets with their authorized owners, and make missing permissions visible. A contributor should be able to explain and validate the work submitted under their name. No onboarding prompt grants remote-write permission or authorizes contacting another person.

### Proposed README boundary and acceptance check
Use the collection README for reusable orientation and links, with Setup Project Workflows teaching how to adapt a short collaborator quick start in the consuming project's README. The project README supplies its own commands, work entrypoints and team agreements; AGENTS remains the owner of agent instructions. The first version uses this two-level approach, with a short collection quick start and Setup guidance for project-specific adaptation; complete procedures stay in their owning skills.

A useful later acceptance check is an unfamiliar collaborator using a fresh accessible clone and their own supported client to find the current contribution, orient an agent, identify their scope, run the documented checks and prepare a small reviewable contribution with a usable handoff. Include a contributor who does not use the maintainer's personal agent setup. Verify published pins and actual collaborator access separately; paper walkthroughs and local links cannot prove those paths work.

### Remaining implementation choices
Platform neutrality, optional forge coordination and separate ownership are settled requirements.

1. Does the short reusable README path plus project-specific onboarding give collaborators enough orientation in real use?
2. Does the agent follow human-mediated decisions, surface only material blockers and keep many-spike branch history understandable without adding a negotiation process?
3. What friction appears in real use, and which narrow corrections does that evidence justify? A formal pilot selection is not blocking implementation.

## Implementation and live feedback
Platform-neutral workflow semantics, optional forge coordination, one agent/thread per spike, Agent Hands platform tooling ownership and separate consumer rollout are user requirements. Implement a small usable version now; improve it through observed work and relevant Kaizen evidence instead of designing a larger framework up front. The Project Workflows owner changes this collection's skill, README/setup/routing and neutral configuration. Agent Hands owns its separate implementation scope. A local Project Workflows checkpoint is explicitly authorized. No publication, external write, consumer installation/pin update or spike closure is implied; the publication hold remains in force.
