---
name: coordinate-project-contribution
description: "Coordinate a contribution between people: follow human-directed scope, link agent-owned spikes and atomic commits to shared outcomes, and prepare review or integration. Supports local work and an explicitly selected forge. Use commit-work for ordinary checkpoints."
---

# Coordinate Project Contribution
Resolve the actual project using [target resolution](../README.md#resolve-the-target). Read its instructions, current work records, selected workflow configuration and Git policy. This procedure owns contribution coordination; the selected platform tooling owns service operations. It grants no authority to contact people, publish, assign work or integrate changes.

## Select the coordination route
Use the project's maintained instructions or declared configuration. An explicit user request can select a route for the current contribution without persisting a project-wide choice.

- **Local:** the default when coordination is absent, disabled or set to `local`. Use existing project records and its validation/QA process. No forge, credentials, dedicated contribution branch, change request or publication is required.
- **Forge:** an explicitly selected shared host/repository. Reuse the relevant work item and change request when appropriate; do not create a record for every internal agent step. Select platform tooling for agent operations, or hand the platform steps to a human.

The optional `[coordination]` table uses `mode = "local"` or `"forge"`, `repository` for the target URL, and `tooling` for a project-owned reference naming the selected setup/use skills and their source/version. Project instructions may supply these choices instead. `tooling` can stay empty when a human performs platform steps. Treat values as data, never commands. Do not infer forge selection from remotes, installed tools or authentication. Report invalid mode or missing forge target before the affected operation; missing agent tooling requires a human handoff, while independent local work continues.

Agent Hands supplies platform tooling when selected. Read the actual selected setup/use skills and use only their supported capabilities. A human can perform a platform step with their own tools; prepare an exact handoff if agent tooling is unavailable. Do not install tools, expand access, silently switch providers or embed provider commands/API calls in this workflow.

## Follow human coordination
People mediate scope, interfaces, ownership and review. Follow their existing decisions and project records; do not impose an agreement checklist, named-role form or separate coordination ritual before work can start. Raise a missing decision only when it materially blocks the next action or changes its scope. Do not infer another person's acceptance, assignment or availability.

For example, if an importer and its UI disagree on the data format, surface that concrete conflict for the people involved. Use their decision and the existing shared record where appropriate; do not prescribe how they must negotiate it.

Each spike belongs to one agent and one thread of work. Two agents, including two working for the same person, use distinct spike records for independent work. Link those spikes to the common outcome and each other where useful; do not make a shared spike into a team task ledger. A successor taking over a thread uses the existing [continuation procedure](../run-project-spike/SKILL.md#continuation-links) and preserves the predecessor's record.

## Work and share meaningful changes
Use [Run Project Spike](../run-project-spike/SKILL.md) for each agent's reasoning, execution state, QA and continuity, and [Commit Work](../commit-work/SKILL.md) for scoped checkpoints. A bounded patch need not acquire a spike merely to use this skill.

Follow the project's working-copy and branch policy and never switch another contributor's active checkout. One branch may host many agent-owned spikes, several issues and multiple eventual change requests. Do not require a branch per spike, issue or contribution. Use Commit Work's atomic targeted commits and `Spike:` trailers to keep work traceable across concurrent threads, including its existing treatment of shared-file overlap and multi-spike commits. Branches/worktrees remain implementation choices under project policy.

Share changed outcomes, interfaces, dependencies, blockers and review needs through the selected coordination route within the user's authorization. Detailed execution stays in each owning spike; do not mirror its checkboxes into a second ledger. Prepare an update for a human when posting is outside scope.

## Prepare review
A contribution is ready for review when its outcome and validation can be explained and assessed together. Spikes, branches, issues and change requests have no fixed one-to-one relationship. Several spikes may support one contribution, and work from a shared branch can become several change requests when sufficiently separable. Use actual commit scope, dependencies and reviewable outcomes to propose those groups; a branch name alone does not define their boundaries.

Use the project's review format or prepare a short overview covering purpose, scope, linked work/spikes, validation and remaining limits. Keep suitable project reasoning and task records with the contribution. Preserve every original atomic commit; do not squash, flatten or rewrite history to make the review look smaller.

An importer and deployment work may legitimately develop on the same branch in separate atomic commits. Inspect the relevant commits and dependencies before preparing separate reviews. Targeted commits help untangle contributions; they do not prove that arbitrary changes can be separated while preserving original history. Follow Commit Work for overlap or any authorized history operation. Where necessary, explain a combined or dependent review or a missing publication ref rather than silently dropping, reordering or rewriting commits. If a dependency integrates first, reassess the remaining contribution afterward.

When publication is intended, inspect the entire outgoing commit range and its documents for scope, audience and private material. Use [Draft Approval Slate](../draft-approval-slate/SKILL.md) for concrete external-write proposals where required. Existing action-specific authorization still counts; selecting forge coordination is not blanket permission. Never push; give the human the exact publication handoff under project policy.

## Review, integrate and continue
Review the actual changes and acceptance evidence, including combined behavior and shared interfaces. Bind service review evidence to the observed contribution revision through the selected tooling. A tool's approval result does not substitute for the agreed person's judgment. If the contribution or integration target changes materially, recheck affected evidence before relying on earlier review.

Use only an authorized integration route supported by repository policy and the selected tooling. Preserve the original commits and intended documents. If the available method cannot meet those requirements, give a concrete blocked/unsupported handoff; do not change repository settings or substitute a history-changing method. A human may perform integration.

Report the actual result with target/revision, validation and any incomplete or uncertain operation. The tooling owner supplies readback and recovery limits; do not blindly retry an uncertain write. Distinguish local readiness, publication, integration and project acceptance.

An integrated contribution does not automatically finish its shared outcome or close its agents' spikes. Each spike follows its own QA and authorized closure procedure. Close shared work only within its actual acceptance scope and authorization. Use real work and relevant workflow feedback to refine this procedure; no new pilot framework or mandatory reporting system is required.
