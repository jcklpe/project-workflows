---
name: triage-project-misc
description: "Triage a project's loose scratch inbox at docs/scratch/misc.md into addressed items, individual captured or parked scratch notes, thematic scratch docs, numbered misc buckets, active spikes, or durable docs. Use when the user asks to review misc notes, route loose observations, clean up scratch material, cluster possible future work, or process a docs/scratch/misc.md inbox."
---

# Triage Project Misc
## Local Precedence
Read the current project's instructions first. If they adopt a `project-workflows` collection, use that project's skill copy and `workflow.toml` to resolve document locations; existing local conventions override fallback paths in this procedure. Otherwise prefer an existing project-local `skills/triage-project-misc/SKILL.md` over a global seed. Never derive the target project's root from the location of a globally installed skill. Required companion project procedures ship in the same collection; general skills and service integrations are optional unless the project explicitly adopts them.

## Purpose
`docs/scratch/misc.md` is a live inbox for loose observations. Use it for observations that are real enough to keep but too raw to classify yet: small bugs noticed during another spike, QA nits, taste reactions, visual discomforts, "this should maybe be better someday" notes, and half-formed clusters not yet routed to a named subject.

`misc.md` is not a roadmap, not an archive, and not a dumping ground that should grow forever. It is an intake surface.

## Relationship To Spikes
The spike process explains how focused work gets promoted into conceptual and to-do docs, tracked through implementation and QA, and eventually archived.

This skill reviews an existing inbox. A direct request to save something for later uses `capture-for-later` without requiring an inbox or triage pass first.

The flow is:

1. A thought lands in `docs/scratch/misc.md`.
2. When the user asks for a triage pass, an agent reviews `misc.md` alongside existing scratch docs.
3. Each item is deleted, moved, clustered into a thematic scratch doc, swept into a numbered miscellaneous bucket, captured or parked for later in an individual note, promoted to active work, or recorded as a current policy.
4. Once a bucket becomes active scoped work, use `run-project-spike` to promote it into the two-doc active spike pattern.

## File Roles
- `docs/scratch/misc.md` is the live inbox for unrouted loose notes.
- Individual `docs/scratch/<subject>.md` notes preserve saved possibilities or deliberately parked subjects with `capture-for-later`.
- `docs/scratch/misc-1.md`, `misc-2.md`, and so on are numbered miscellaneous buckets for real work that does not yet form a clean thematic spike.
- `docs/policies/` is for current durable rules, defaults, and procedures.
- Thematic scratch docs such as `syntax-highlighting.md`, `brand-voice.md`, or `embed-media-support.md` are preferred when notes cluster around a coherent theme.
- Active spike docs in `docs/active-spikes/` exist only after a scratch topic becomes the active scoped work.
- Archived spike docs in `docs/archive/` are historical context after a spike closes.

## Routing Taxonomy
Use the first matching destination:

Use the collection's [capture-for-later](../capture-for-later/SKILL.md) for saved possibilities and deliberately parked subjects. Preserve existing records, including legacy lists; this triage procedure does not authorize their bulk migration. Starting active work still follows the separate spike workflow.

- If it is a durable rule the project is adopting, move it into a current policy under `docs/policies/`.
- If the user wants to save a possibility or deliberately park a subject, create or update its individual scratch note with `capture-for-later`. The same subject can be captured or parked; this is state, not a rigid subject classification.
- If it is raw observed friction, a bug, a nit, a QA reaction, or issue intake, keep or route it through `docs/scratch/misc.md`.
- If it is active scoped work, promote it into `docs/active-spikes/` with `run-project-spike`.

A saved thought need not be polished or fully formed. Misc remains an inbox for raw observations; explicitly saving a subject for later can use a one-sentence note. Do not infer priority or commitment from either destination.

## What Belongs In Misc
Good `misc.md` entries are specific enough to preserve the observation:

- a visual detail that feels off
- a bug seen while testing a different surface
- a potential feature mentioned during other work, unless the user asks to save it as its own note
- a design or taste reaction in the user's own phrasing
- a link or reference that might matter later
- a cluster seed that may become a spike after more related items appear

Bad entries are so compressed they lose the point:

- "Improve homepage"
- "Fix mobile"
- "Make embeds better"
- "Polish stuff"

If a note starts vague, keep the user's concrete phrasing around it. The rambling often contains the actual design constraint.

## Review Process
When asked to review `misc.md`:

1. Read `docs/scratch/misc.md` in full.
2. Read existing `docs/scratch/misc-*.md` numbered buckets.
3. Read likely thematic scratch docs.
4. Search current active and archived spike docs if an item looks familiar.
5. Route each `misc.md` item.
6. Preserve nuance when moving items.
7. Delete routed or addressed items from `misc.md`.
8. Replace the `Latest Routing Session` section in `misc.md` with a short summary of the current review only.

Do not keep an infinite routing history in `misc.md`. The latest routing session summary is a handoff, not an archive. The next review should replace it.

## Routing Outcomes
### Already Addressed
If an item has already been completed or captured in a durable doc, delete it from `misc.md`.

If the routing might be confusing later, mention it briefly in the latest routing session summary.

### Existing Thematic Scratch Doc
If an item clearly belongs to an existing scratch topic, move it there.

Preserve:

- the user's concrete examples
- any uncertainty or alternatives
- references and URLs
- why the thing felt wrong or worth noticing
- visual or taste language, even if informal

Clean the prose enough to make the destination doc readable, but do not flatten the item into a generic ticket.

### New Thematic Scratch Doc
If several items cluster around a clear theme, create a new scratch doc with a descriptive name.

Keep the note as small as the material warrants. Use `capture-for-later` when the intent is to save or park the subject; a sentence is enough, with useful existing context preserved. Do not require goals, value statements, blockers, work items, or a miniature spike plan. Expand the note only when there is actual material worth retaining. `run-project-spike` handles active work separately.

### Capture for Later
For a possibility or deliberately parked subject, follow `capture-for-later`: update the related note or create one visible subject file. Use `captured` or `parked` according to the supported intent, not the domain or how developed the idea is. Preserve a reason to pause or revisit condition only when known. Do not invent a trigger, convert the note into a task, or duplicate an existing legacy entry.

### Durable Policy
If an item is already settled as a project rule, add or update a current policy under `docs/policies/`.

Do not create a policy for every local implementation choice. Use policies for durable guidance that should outlive current spike context; revise them directly and let Git preserve their evolution. Respect existing project conventions unless migration is authorized.

### Numbered Miscellaneous Bucket
If an item is real but does not belong to an existing doc and does not cluster into a thematic spike, sweep it into a numbered `misc-#.md` bucket.

Use this when the work is small, mixed, or opportunistic. A numbered misc bucket can become its own active spike later, like any other scratch doc.

## Reviewing Existing Misc Buckets
Every `misc.md` review should also examine existing numbered misc docs in `docs/scratch/`.

Ask:

- Do any old misc items now cluster with the new `misc.md` items?
- Has a grab-bag item gained a clearer thematic home?
- Should an item move from `misc-#.md` into a named scratch topic?
- Has an item already been completed or superseded?

Numbered misc docs are temporary holding areas, not permanent junk drawers. If a better theme emerges, move the item out.

## Preservation Rule
Do not over-compress `misc.md` items while parting them out.

The user's loose phrasing may contain design signal: emotional reaction, uncertainty, analogy, hierarchy of importance, or a concrete example that a short task title would erase. Keep that texture in the destination doc.

The goal is not to preserve every typo or duplicate sentence. The goal is to preserve meaning, taste, references, and the reason the note existed.

## Misc Template
Use this shape:

```md
# Misc Inbox
Live inbox for loose observations.

## Unrouted Items
- ...

## Latest Routing Session
Reviewed YYYY-MM-DD.

- Moved ...
- Deleted ...
- Created ...
```

The `Latest Routing Session` section should be replaced on each review. It is only the latest handoff.
