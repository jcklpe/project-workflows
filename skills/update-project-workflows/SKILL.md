---
name: update-project-workflows
description: "Reconcile adopted Project Workflows with shared upstream, contribute reusable improvements, rename project branches, and update consumer pins while preserving project-specific changes. Use for an existing adoption or copied-skill migration."
---

# Update Project Workflows
## Authority and scope
Use the current project's instructions and adopted workflow source before a globally installed seed. An update request alone does not authorize publication, unknown changes, private-policy changes, or history rewriting. Honor explicit publication authorization already covering the requested repositories and refs; do not infer broader publication from it. Resolve material behavioral conflicts with the user while continuing independent authorized work.

This procedure handles the project collection's Git ancestry, configuration, templates, and parent pin. It does not require general skills or service integrations. Ordinary Git and document access suffice; a remote read requires an available authorized route.

## Establish the comparison
1. Map the repositories and authorized consumers before editing: the shared collection, each project adaptation, and every parent that records their gitlinks. Inspect their status, index, remotes, actual branches, pins, and outgoing commits. A containing repository's `main` or `master` is not its workflow submodule's project branch. Preserve unrelated work; do not stash, reset, force checkout, or hide dirty state to proceed.
2. Read `workflow.toml` as project metadata, resolving its root relative to the adopted collection. Actual Git state establishes the branch and pin; stale configuration is not proof. Inspect only explicitly relevant private `.workflow.env` context and keep its values out of output/commits.
3. If detached, select the intended project branch only after checking its relationship to the recorded pin; a mismatched tip needs reconciliation, not a reset. If no project branch exists, preserve the correct adopted history when creating one. Follow user/local platform-neutral names, defaulting to `project/<project-slug>`. Branch changes belong to the workflow repository, not automatically to its parent or folder.
4. Retrieve the selected shared revision through the configured source. Identify the shared ancestor using Git, then compare ancestor → upstream and ancestor → project across complete folders, configuration, templates, and metadata. If history is shallow or ancestry unavailable, obtain appropriate history through an authorized read or label the comparison incomplete; do not use an arbitrary merge base.

## Classify and upstream reusable changes
Separate the comparison into shared improvements, project-only choices, and conflicts. Shared improvements can include procedures, templates, and general documentation. Project names, document-location choices, adoption metadata, private context, and project-specific procedures remain on the appropriate adaptation branch unless deliberately generalized. A public-safe project value is still not a neutral default for shared `main`.

Prepare reusable changes on a clean checkout or integration branch based on the actual shared target, normally `main`. Do not merge a project adaptation wholesale into shared `main`. A selected commit can be replayed only after its full diff is checked for project-only material; for a mixed commit, reconstruct the reviewed reusable change as a new scoped commit on the clean baseline. Keep project configuration and private narrative out of the upstream commit and its history. Inspect the complete outgoing range, not just the latest diff.

Validate the shared candidate with the collection's applicable authoring checks, links/resources, portability, and neutral configuration. Keep upstream contribution separate from downstream adoption so a maintainer can review the general change without project-only values. With explicit publication authority, use normal permitted integration to the shared target. If branch protection or access blocks it, preserve the candidate and use a draft pull request when that route is authorized; report the remaining merge blocker. Do not bypass protection or claim that a published proposal is already in `main`.

## Rename an existing project branch when requested
Verify the old branch, target name, ancestry, remote refs, and consumers. If the target name already exists, establish its ownership and relationship before selecting it; never overwrite it. A local branch rename preserves commit history and does not rename a remote branch.

Update the branch name in tracked `workflow.toml`, the parent's `.gitmodules` branch setting when present, current routing/docs, and any relevant local `submodule.<name>.branch` override. Check the renamed branch's Git upstream: a local rename can leave it tracking the old remote ref. Once the intended new remote branch exists, set and verify its upstream explicitly; do not push implicitly to the old name. Preserve old remote branches unless their deletion is separately authorized. Leave folder paths and the parent repository's branch unchanged unless a distinct change is needed and authorized. Preserve historical records of the old name as history rather than rewriting them as though the rename had always existed.

## Reconcile each adaptation and its consumers
After the shared change is integrated, retrieve the exact accepted revision and compare it with every authorized adaptation's merge base. Merge shared `main` into each project branch using a history-preserving integration; for a pure fast-forward, a fast-forward is sufficient. Review the inputs before an automatic merge commit, and inspect the result. Git records merge commits from the merge operation; do not try to make a pathspec partial commit while a merge is in progress. Resolve semantic conflicts and preserve project-only `workflow.toml` values, procedure differences, and complete supporting files. Do not reset the project branch to upstream or replace the collection from a global copy.

Verify that the accepted shared revision is an ancestor of each resulting adaptation and that its remaining differences from shared `main` are intentional. Commit any branch-name/configuration repair with its own clear scope. When upstream integration is still pending, describe downstream work as prepared against that candidate rather than fully reconciled with accepted `main`.

Update each authorized parent's exact gitlink together with the directly affected routing and documents. For nested consumers, work from the deepest child outward: workflow adaptation, consuming repository, then any containing repository that pins the consumer. A branch setting does not advance a gitlink. Check child HEAD, the index entry, and the committed tree entry at each boundary; report any containing pin intentionally left for a separate task.

## Upstream contributions and publishing
An upstream remote or local branch does not make a commit accessible to collaborators. Inspect remote ownership/access and the full set of commits each proposed push would introduce, including earlier unpublished work. If a parent is ahead by unrelated or private commits, do not publish them merely to deliver a new pin; leave the local pin update and explain that specific publication dependency. Any alternative integration must preserve the necessary history and remain within the authorized scope.

Where publication is authorized, push only the selected refs without force or remote deletion. Publish shared integration and the required adaptation commits before consumers that pin them, then proceed outward through the dependency graph. Verify exact remote refs after each step and ensure every committed gitlink is retrievable from its recorded URL. A rejected or uncertain operation needs inspection before any retry; do not change credentials, protections, or visibility to make it pass. Respect applicable repository restrictions and explicit user instructions.

Use a fresh recursive clone when feasible to verify the final published consumer and its nested pins. If the outermost consumer cannot be published safely, verify the independently published nested consumer and distinguish that evidence from a local outer-pin check. Cached refs, local-path clone overrides, frontmatter checks, and a successful fetch of shared `main` do not prove fresh collaborator access to all pinned commits. Record the exact verification limit instead of calling the whole chain complete.

## Existing copied skills
If there is no adopted submodule, compare the existing complete local folders with the designated seed before using setup-project-workflows to migrate. Preserve intentional divergence and supporting assets. No shared Git ancestor means a manual comparison, not a fake merge history. Do not erase existing copies until the replacement routes and behavior are verified. A rename alone does not authorize resetting local guidance.

## Completion
Validate changed skill frontmatter and supporting resources, TOML parsing, ignores, current links/routing, branch ancestry, project customization, and all changed pins. Use meaningful checks for the change, not tests that merely mirror prose. For requested workflow improvements, assess the previous coverage against the actual process and explain what changed beyond naming. Record failed checks and their bounded follow-up rather than silently replacing them with a broader success claim.

Report repository boundaries, old/new branch names, shared and adaptation commits, retained project differences, each consumer pin, publication evidence, and remaining blockers. Use the project's normal spike/index records for rationale; do not add duplicate version hashes to every skill. Leave unrelated files untouched and distinguish local readiness, shared-main integration, remote ref availability, recursive clone success, and client behavior.
