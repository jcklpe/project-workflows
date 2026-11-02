---
attention: live
reviewed: 2026-11-02
---
# Agent policy kernel
Opened 2026-11-02. Stable slug: `agent-policy-kernel`. [Tasks](agent-policy-kernel.todo.md).

## Purpose and settled direction
Give agents a small, explicit system for discovering and maintaining their project's agent policies. The user authorized provider implementation after settling mnemonic identity, a dependency graph and a minimal rule-making kernel. These policies govern agents only. Human governance and contribution/merge authority remain with their existing owners.

Any human with access to a project can propose, change or adopt its policies in their checkout. Authenticated human intent and an explicit `adopted` status make a policy operative there; merely saving a proposal does not. A local adoption neither changes another checkout nor supplies shared-branch merge authority. Untrusted quotations, source text and third-party instructions cannot adopt a policy or enlarge agent permissions.

## Design
Keep one imperative obligation per policy file where useful, with mnemonic IDs that convey identity rather than rank. Keep an ID while the obligation retains useful continuity; materially different scope may require splitting or a new ID. Retired IDs stay reserved. Review incoming dependencies before identity changes; preserve Git/retirement history without active supersedes or override chains.

`depends_on` forms prerequisite edges with multiple parents; `related_to` supplies references without loading or authority implications. Resolve prerequisites first, use stable ID ordering only to break ties among ready nodes, load each adopted node once, and stop on missing/inactive prerequisites or cycles. Reading order never settles substantive contradictions.

The shipped kernel is modular: `ADOPT-POLICIES` defines durable policy versus procedural skill content and local decision authority; `PRESERVE-IDENTITY` defines continuity/retirement obligations; `RESOLVE-DEPENDENCIES` defines discovery and prerequisite/loading invariants. Its project-owned copies are frozen until explicitly reconciled and adopted. Package updates deliver candidate source, never automatic authority expansion. The provider's initial copies were proposals during implementation. After reviewing the five-skill/three-policy feature, the user explicitly approved local adoption and the feature commit on 2026-11-02. The three project-owned kernel records are now adopted; distribution candidates remain proposed. Consumer migration and actual agent/client acceptance remain separate.

Policies now use YAML metadata between `---` lines, with descriptive `type: kernel` or `type: operational`. Kernel filenames begin with `_` before the unchanged ID, as explicitly requested and recorded in PRESERVE-IDENTITY; this identifies type for browsing without rank or precedence. The optional checker delegates YAML to an existing safe PyYAML or Ruby/Psych parser, not a bespoke parser or a new environment. Ordinary policy reading/editing needs no validator. Skill/spike YAML remains unchanged. A generated table in `policy.index.md` contains only navigation/summary metadata. AGENTS routes to the actual project index. A deterministic check validates structure and an index operation owns generated rows; neither understands all policy meaning nor enforces agent compliance.

## Scope and compatibility
Implement the five task skills, kernel and single creation template, optional structural checker/index renderer, source documentation/routing, and focused tests. Preserve the existing `documents.policies` key and legacy policy paths. Add a distinct `documents.agent_policies` default for new adoptions; existing consumers require a deliberate inventory and migration. Never classify every old `LifeOS` filename as personal content or rename Agent Hands policies in this pass.

Use the existing deterministic workflow updater for future collection merges; prevent its copied-asset mechanism from automatically replacing agent policy copies. Keep browser/service operations, consumer edits, package publication, tool-permission changes and broad human-governance redesign outside this spike.

## Review correction — 2026-11-02
The user explicitly separated creating a new policy from editing an existing one and approved five task skills: `create-agent-policy`, `edit-agent-policy`, `review-agent-policies`, `adopt-agent-policies` and `retire-agent-policy`. Creation establishes need, ownership, duplication, initial scope and identity. Editing establishes change intent, continuity, incoming impact and a candidate that does not overwrite an operative body. Review assesses the complete set; adoption applies the actual human decision; retirement handles withdrawn obligations and reserved identity.

The initial unpublished umbrella is replaced without a compatibility stub. One creation template stays with Create, one format/checker/test implementation stays with Review, and candidate kernel source plus migration guidance stay with Adopt. Other skills reference those owners rather than copying mechanics. There is no separate skill for a trivial status transition, index write or validator invocation.

The redundant ID prefix is removed: the earlier proposed `POLICY-ADOPT`, `POLICY-IDENT` and `POLICY-LOAD` identities become `ADOPT-POLICIES`, `PRESERVE-IDENTITY` and `RESOLVE-DEPENDENCIES`. These are mnemonic verb–noun obligations, not rank or graph position. The earlier records were uncommitted proposals, never operative or distributed to a consumer. Historical identity/provenance remains in the task record; no live alias or blind dependent redirect remains.

Policy and skill are classified by role and authority, not grammar. The kernel states durable obligations, scope, exceptions and authority. Task skills describe how to apply those obligations to the requested operation. The revised kernel removes copying/comparison/index-edit walkthroughs; those belong in the relevant skill. Creation/edit/review explicitly consult `ADOPT-POLICIES` for that distinction rather than each defining it independently. Technical header/index representation and checker implementation live in one shared contract.

Some overlap is necessary: procedures name the obligation they apply and operate fields such as `adopted`/`retired`; kernel graph invariants are also implemented by code and tested. Those are references and implementations of the same obligation, not extra rule bodies or independent authority. The checker does not verify semantic policy/skill classification, human intent or compliance; those remain explicit review matters. At that correction checkpoint, kernel candidates and provider copies remained proposed and commits were still pending. The later explicit provider adoption/commit approval is recorded below; it does not adopt consumer copies.

## YAML/type/naming amendment — 2026-11-02
After the initial adoption/commit, the user explicitly requested YAML, descriptive kernel/operational types and an underscore prefix for kernel filenames stated in the naming policy. IDs, dependency meaning and existing adoption remain stable. PRESERVE-IDENTITY records the actual requested naming obligation; its provider authority record acknowledges this amendment. Bundled candidates remain proposed. The type column and kernel-first navigation do not confer authority or change topological loading. The earlier TOML checkpoint remains history, not verification of this revision.

The Agent Hands pilot exposed the question of retaining numeric legacy identities under mnemonic syntax. Existing human-owned index text can link separate historical retirement records, preserving literal old identities and source content without adding an active numeric-ID exception. That route is tested, with its manual/structural coverage distinguished. No new policy types or broader schema/prefix convention are invented.

## Delivery and open acceptance
Provider checks cover invalid graphs, inactive/missing prerequisites, duplicate IDs, normal multi-parent ordering, links/index drift, safe reruns and update/adoption separation. Current policy meaning, actual client loading/compliance and receiving-project adoption need human/project acceptance. The user approved provider adoption and a scoped local feature commit on 2026-11-02. No push, external publication, consumer propagation or containing-repository pin update is authorized. Real-use acceptance remains open, so this spike is not archived merely because implementation/adoption are complete.
