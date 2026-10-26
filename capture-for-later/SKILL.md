---
name: capture-for-later
description: "Save an idea, possibility, unresolved question, or deliberately parked subject for later without starting work. Use for pin issue, put a pin in that, circle back, future ideas, defer a decision, park this, or save this for later; create or update a small visible scratch note."
---

# Capture for Later
Resolve the actual requested target using [target resolution](../README.md#resolve-the-target) before selecting configuration or document paths. Global invocation does not target the installation checkout. Plain folders use global skills without adding a local collection or initializing Git.
## Scope and local authority
Capture something the user wants to remember without committing to explore, decide, or implement it now. Features, design, content, research, tooling, and other project subjects all qualify. The subject does not determine whether it is a possibility or deliberately parked; that is the note's current state.

Read the current project's instructions and adopted workflow source first. Resolve its scratch location from local conventions or `workflow.toml`; default to `docs/scratch/`. Never infer the current project from a global skill's installation directory. Capture requires ordinary document access, not external services or a personal vault.

## One visible note per subject
For a new subject, use a descriptive filename such as `docs/scratch/alternate-navigation.md`. One sentence can be the entire body. Do not create a catch-all future-ideas or pinned-issues list, require a separate proposal, or add tasks just to make the note feel complete.

First check likely related scratch notes and any relevant existing record. Update the same subject's note instead of creating a duplicate; preserve useful reasoning, references, uncertainty, and user phrasing. If the subject is already an entry in a legacy list, update that entry in place unless moving it is requested. Do not apply one entry's state to an entire list. Do not bulk migrate, split, or delete existing notes as a side effect of adopting this skill.

## Minimal state
For a new note, use one frontmatter field unless the project already has an equivalent convention:
- `status: captured` for a saved possibility or thought, without a decision to pursue it. This is the default when no deliberate pause is stated.
- `status: parked` when the user deliberately sets the subject aside or defers resolving it.

These describe the same subject's treatment, not separate subject categories or levels of commitment. Change state only when the user's direction or the recorded context supports it. Preserve existing note metadata and local conventions; do not impose a retrospective schema migration. Neither state means approved work, a backlog commitment, or an automatic reminder.

```md
---
status: captured
---
# Alternate navigation
Explore a quieter navigation layout sometime.
```

Keep the content as small as the thought warrants. Add a parking rationale, relevant context, or a revisit condition only when actually known and useful; omit unknowns instead of inventing them or asking the user to fill out a form. Do not require value statements, blockers, estimates, dates, priorities, owners, or task lists. Preserve substantial existing reasoning when it will help someone resume related work.

## Capture and handoff
1. Read the request and enough nearby context to select the owning project, subject, and existing note without auditing unrelated work.
2. Create the individual note or update its existing record. Preserve the user's intent and apply the supported state.
3. Read back the result and report its path. Do not add a TODO/backlog item, a spike pair, or an implementation plan merely because something was captured.

Capture does not start active work. When the user actually resumes a bounded workstream, use [run-project-spike](../run-project-spike/SKILL.md), which covers design, implementation, validation, and delivery as well as investigation. Its promotion procedure preserves the useful context without leaving an outdated competing copy. Raw misc-inbox triage remains with [triage-project-misc](../triage-project-misc/SKILL.md); a direct request to save something for later does not need an inbox pass first.

Keep private material in its authorized context. Permission to capture a thought is not permission to copy private sources into a public repository or publish the note. Follow the project's commit policy separately.

## Open Austin ownership
Capture this repository’s organization/tooling/process subjects here; material owned by another community project stays with that project. This is an ownership boundary, not an infrastructure-only restriction on ideas. Preserve related existing list entries without duplication. Neither capture nor parking creates a GitHub backlog item or authorizes external writes. Follow the parent privacy, governance, and reviewed-plan rules.
