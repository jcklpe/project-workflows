---
name: update-project-workflows
description: "Reconcile a project's adopted workflow collection with shared upstream changes while preserving intentional local differences. Use to update a project-workflows submodule, compare its project branch, prepare reusable upstream contributions, or migrate an existing copied-skill baseline."
---

# Update Project Workflows
## Authority and scope
Use the current project's instructions and adopted workflow source before a globally installed seed. A scoped update request authorizes the reconciliation, not overwriting unknown work, changing private policy without approval, publishing, or resetting history. Resolve material behavioral conflicts with the user while continuing independent authorized work.

This procedure handles the project collection's Git ancestry, configuration, templates, and parent pin. It does not require general skills or service integrations. Ordinary Git and document access suffice; a remote read requires an available authorized route.

## Establish the comparison
1. Inspect both parent and child status, index, remotes, current branch, parent gitlink, and child HEAD. Determine whether the child differs intentionally from the pin. Preserve unrelated work; do not stash, reset, force checkout, or hide dirty state to proceed.
2. Read `workflow.toml` as project metadata, resolving its root relative to the adopted collection. Actual Git state establishes the branch and pin; stale configuration is not proof. Inspect only explicitly relevant private `.workflow.env` context and keep its values out of output/commits.
3. If detached, create/select the intended project branch from the correct adopted commit before editing. A branch from initial adoption is expected even when initially identical to shared main. Verify an existing branch rather than resetting it to the pin.
4. Retrieve the selected shared revision through the configured source. Identify the shared ancestor using Git, then compare ancestor → upstream and ancestor → project across complete folders, configuration, templates, and metadata. If history is shallow or ancestry unavailable, obtain appropriate history through an authorized read or label the comparison incomplete; do not use an arbitrary merge base.

## Reconcile behavior
Summarize material upstream changes, deliberate local differences, and conflicts. Preserve project vocabulary, file locations, validation, privacy boundaries, and user choices. A local procedure may diverge freely; structured configuration is useful but not a prohibition on procedural changes. Do not confuse a personal hardcoded path or missing dependency with meaningful specialization.

Choose a history-preserving integration suitable for the actual changes and local policy. A reviewed merge retains both lines of development; selected reusable commits can be proposed separately. Do not rewrite existing project history or automatically replace local files with upstream. Resolve semantic conflicts as well as textual ones. Keep actual project documents and private context out of the child history.

Validate changed procedures and supporting files, configuration parsing, ignores, routing, required resources, and relevant behavior. Use meaningful checks for the change; do not add tests merely to mirror prose. A frontmatter pass does not establish successful client discovery or usability after cloning. Commit coherent child changes under the owning policy, then update the parent's exact gitlink with its directly related routing/docs changes.

## Upstream contributions and publishing
Separate reusable improvements from project-only changes in focused commits. Propose upstream contributions without including project metadata, private examples, credentials, or unrelated workflow history. An upstream remote or local branch does not make a commit accessible to collaborators.

Before publishing a parent pin, establish that the required child commit is reachable from the recorded accessible remote. Fetch/check remote state or verify a fresh clone when possible; cached refs alone do not prove current remote access. Report unpublished child commits as a publication dependency. Do not push, create remote branches/PRs, or alter repository visibility without the applicable explicit authorization; where agents may not push, leave that step to the human.

## Existing copied skills
If there is no adopted submodule, compare the existing complete local folders with the designated seed before using setup-project-workflows to migrate. Preserve intentional divergence and supporting assets. No shared Git ancestor means a manual comparison, not a fake merge history. Do not erase existing copies until the replacement routes and behavior are verified. A rename alone does not authorize resetting local guidance.

## Completion
Report the upstream revision examined, retained project differences, implemented changes, verification limits, resulting child branch/commit and parent pin, and any unpublished dependency. Use the project's normal spike/index records for rationale; do not add duplicate version hashes to every skill. Leave unrelated files untouched and distinguish local readiness from verified collaborator cloning.
