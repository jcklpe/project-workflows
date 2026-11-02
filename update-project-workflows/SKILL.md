---
name: update-project-workflows
description: "Reconcile adopted Project Workflows with shared upstream, contribute reusable improvements, rename project branches, and update consumer pins while preserving project-specific changes. Use for an existing adoption or copied-skill migration."
---

# Update Project Workflows
Resolve the actual requested project using [target resolution](../README.md#resolve-the-target). Read its instructions, selected config and Git policy. Global invocation does not select the installed collection as the target. Preserve local adaptations, original commits, unrelated working/index state, privacy rules and existing publication holds. Updating is not authority to push, rewrite history, change coordination mode or enable automation.

## Routine pinned update
Use this path for an initialized `project-workflows/` adoption on its intended project branch. Canonical collection maintenance, global-only use, migration and retirement use the selected [exceptional route](references/exceptional-updates.md). Plain folders need no repository or collection.

1. Establish the authorized parent and child roots, current branches/HEADs, parent pin, remotes, relevant dirty/staged state and outgoing commits. Follow the actual target's policies. Resolve detached/mismatched branches and unfinished adoption before continuing; do not switch an active checkout, stash, reset or hide work. For several consumers, keep a bounded inventory and pilot one representative adoption before proceeding deepest child first.
2. Select the exact accepted shared revision and its source. Fetch only through an authorized route. Use its real merge base: fast-forward when possible, otherwise preview an ordinary history-preserving three-way merge. Never reset an adaptation to shared main or copy over it from a global installation. An unaccepted candidate remains a candidate in the report.
3. Preserve project-only `workflow.toml` settings mechanically. Review incoming changes only where they intersect customized procedures, plus actual textual/semantic conflicts. A clean merge is not evidence that two customized instructions agree. Metadata-only variation needs no broad reread of unchanged skills. Upstream contributions and layout/mode changes are separate routes, not prerequisites for routine updates.
4. Reconcile installed parent assets from their **actual previous template baseline**. The submodule merge does not update copied `.github/` files. Unchanged copies take the new source; edited copies use a three-way comparison and focused review. Missing baselines, deletions or real conflicts require explicit reconciliation; do not infer a baseline from today's shared main or overwrite local edits.
5. Apply the reviewed fast-forward/merge under the child's commit policy, then the planned asset changes. A Git merge records its merge commit; do not attempt a partial pathspec commit during it. Preserve every original commit. Verify accepted-revision ancestry, retained settings, focused resources/syntax and the project's relevant checks. Treat configured validation commands as data to inspect, never commands to execute blindly.
6. Checkpoint the parent's exact gitlink with directly affected assets, baseline file and routing/docs under [Commit Work](../commit-work/SKILL.md). The branch setting is not the pin. Check working HEAD, index and committed tree separately at every boundary. Leave unrelated files/index entries alone. Repeating a completed update should produce no new commits or file edits.

Use the optional [Git/standard-library helper](scripts/update.py) and its [usage and baseline format](references/updater.md) for steps 1–5. It previews by default, surfaces focused review paths, preserves settings, reconciles copied assets, and never stages/commits parent files or pushes. It needs an **existing** Python 3.11+ and Git 2.38+; do not create an environment or install dependencies merely to use this collection. The same procedure can be performed with ordinary Git and document access. No service credentials are required for local merging.

## Focused verification and result
Check changed skill frontmatter/resources, TOML, copied-asset syntax and relevant behavior. Inspect the merged patch and only affected local customizations; retain project-specific policies, disabled/local coordination and complete supporting files. Shared defaults are not authority to replace deliberate local decisions. An unresolved behavioral decision goes to the human while independent authorized work continues.

Report old/accepted/result revisions, branch and retained differences, focused review/conflicts, checks, asset/baseline changes and parent pin state. Distinguish local reconciliation, a committed pin, accepted shared integration, remote retrievability, fresh clone and actual client/live behavior. No token-savings benchmark is implied. Record the bounded result in the existing spike/index, not a new update ledger.

## Selected exceptional routes
Load only the applicable section of [Exceptional updates](references/exceptional-updates.md):

- [Bounded multi-project inventory](references/exceptional-updates.md#bound-the-adoption-inventory), [reusable upstream contributions](references/exceptional-updates.md#classify-and-upstream-reusable-changes), or [publication and fresh-clone verification](references/exceptional-updates.md#upstream-contributions-and-publishing).
- [Branch rename](references/exceptional-updates.md#rename-an-existing-project-branch-when-requested), [canonical checkout/retirement](references/exceptional-updates.md#canonical-installation-and-branch-retirement), or [global-only migration](references/exceptional-updates.md#move-an-adoption-to-global-only-use).
- [Collection layout changes](references/exceptional-updates.md#collection-layout-changes), [existing copied skills](references/exceptional-updates.md#existing-copied-skills), [requested legacy-note migration](references/exceptional-updates.md#requested-legacy-note-migration), or [overlapping parent documentation](references/exceptional-updates.md#incomplete-parent-documentation).

For existing global-only use, compare only the target's declared overrides/configuration with relevant installed changes; skip child branches and pins. Global-only maintenance does not authorize adopting or retiring a collection. For canonical shared maintenance, keep shared main and neutral configuration; use the collection's instructions rather than creating a project adaptation.
