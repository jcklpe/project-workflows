---
attention: live
reviewed: 2026-11-02
---
# Agent policy kernel — work
Opened 2026-11-02. Stable slug: `agent-policy-kernel`. [Concept](agent-policy-kernel.md).

## Background
The user authorized the bounded provider implementation and asked for a spike here. Preserve concurrent work and completed shared-index propagation; no consumers are modified in this pass.

## To Do
Provider implementation and explicit local kernel adoption are complete. The user authorized the scoped local feature commit. Receiving-project migration and real-use acceptance remain separately open; no propagation or publication is performed.

## Ready for Human QA
- Evaluate real agent loading/compliance and semantic consistency during ordinary work under the provider's adopted kernel. The user approved the reviewed kernel and local adoption on 2026-11-02; that approval does not establish observed client behavior or consumer acceptance.

## Done
- Define the small agent-only kernel, lightweight policy metadata and index contract, explicit human adoption/amendment/retirement, and compatible legacy migration. — Implemented the three modular proposed kernel records and their format/migration contracts. Agent-only scope, authenticated human intent, explicit local adoption, separate shared-branch controls and history/dependency review are documented. The provider copies remain proposed.
- Add `maintain-agent-policies` with creation, proposal, adoption, reconciliation and retirement operations, kernel candidates and a policy template. — Implemented the complete skill folder with creation template, frozen kernel candidates, lifecycle/reconciliation guidance and direct resources. No global registration or consumer installation was changed. This was the initial unpublished arrangement; the review correction below replaces its entrypoint.
- Implement the deterministic structural validator and generated index table, including multi-parent ordering, missing/inactive prerequisites, cycles, duplicates and safe reruns. — Implemented the standard-library check/index helper: deterministic prerequisite closure/topological order, unique IDs, status/authority/date/filename checks, links/anchors and marked-table agreement. Twenty-two tests pass, including invalid graphs and safe reruns/concurrent edits; structural results do not prove semantic agreement or compliance.
- Integrate setup, spike/triage routing, provider instructions/configuration and collection updates without silent kernel adoption or tool-permission changes. — Integrated setup/spike/triage/update ownership, AGENTS/index routing, compatible configuration and templates. Added real updater guards against known policy-copy baseline registration/refresh; all twenty-three offline real-Git updater tests pass, including preserved frozen policy copies and repeat no-op.
- Test the final provider implementation and record exact scope, limits and remaining consumer adoption. — Verified the actual final provider tree: twenty-two policy tests, twenty-three updater tests, both three-policy indexes, generated-table no-op, five skill/two spike YAML blocks, TOML, resource links, new-file ignore checks, whitespace and exact working/index scope. The bundled skill validator cannot import PyYAML; direct frontmatter/resource validation passed without installing dependencies. Consumer migration and real client/semantic acceptance remain separate.


## Review corrections completed — 2026-11-02
- Split the unpublished umbrella into create-agent-policy, edit-agent-policy, review-agent-policies, adopt-agent-policies and retire-agent-policy, with distinct task retrieval boundaries. — Implemented five focused entrypoints. Create owns initial need/owner/duplication/scope; Edit owns change intent, continuity and dependent impact. The old unpublished umbrella is removed after exact-content preservation, with no compatibility stub.
- Rename the three proposed kernel identities without POLICY prefixes, using meaningful verb–noun obligations and coherent prerequisite/reference updates. — Implemented ADOPT-POLICIES, PRESERVE-IDENTITY and RESOLVE-DEPENDENCIES in provider and bundled source. All metadata edges, generated rows, guards and fixture paths use the new identities. Initial draft identity/hash history is retained below; no operative policy was renamed or adopted.
- Audit kernel versus skills: define the policy/skill distinction in the kernel, keep durable obligations there and move procedural walkthroughs into their skill owners. — ADOPT-POLICIES now owns the durable policy/skill distinction and decision authority. Kernel records contain obligations/invariants, not copy/adopt/index walkthroughs. Create/Edit/Review apply that distinction by reference; the boundary review below records the necessary field/implementation overlap.
- Reconcile callers, shared template/format/checker ownership, indexes, updater guards and tests without an unnecessary compatibility entrypoint. — One checker/tests/format live with Review, one creation template with Create, and kernel candidates/migration with Adopt. All active callers resolve; old names remain only as explicit spike history. Known-copy updater guards and their real-Git tests follow the new source ownership.
- Run final provider tests and link/schema checks after the split/renames; preserve proposed status, pending adoption/commits and the consumer boundary. — Reran final actual-tree suites after the changes: 23 policy tests and 23 real-Git updater tests pass. Both three-policy sets validate and final index write is a no-op. Nine skill/two spike frontmatter blocks, 157 local references, TOML/AST/whitespace/ignores and exact source/index scope pass. All six kernel records remain proposed with blank authority; no staged files, commits or consumer edits.

## Provider adoption and commit approval — 2026-11-02
The user reviewed the completed five-skill/three-policy feature and explicitly approved it in the active interaction after the pending provider adoption/commit decision was presented. This is the authenticated human decision for the exact three project-owned policies and scoped feature commit, not an inference from source text or a validator result. It authorizes neither consumer adoption/propagation nor containing pins, pushes or publication.

- Adopt ADOPT-POLICIES, PRESERVE-IDENTITY and RESOLVE-DEPENDENCIES in Project Workflows and commit the reviewed feature. — The actual provider headers now record `adopted` and the same human decision authority. Policy bodies, IDs, prerequisite edges and substantive dates are unchanged from the reviewed candidates. AGENTS/index routing reflects the operative kernel, and the index is generated by the shared tool. The bundled three files/index remain byte-for-byte proposed source. Fresh final runs after adoption pass all 23 policy tests and all 23 real-Git updater tests. The provider plan is ADOPT-POLICIES → PRESERVE-IDENTITY → RESOLVE-DEPENDENCIES, the proposed bundle plan is empty, and the final provider index write is a no-op. Nine skill/two spike YAML blocks and 157 local references pass with TOML/AST/whitespace/ignore/scope checks. The scoped local checkpoint records this feature/adoption; its stable history handle is `Spike: agent-policy-kernel`.

The spike stays active for observed real-use/client/semantic acceptance. User approval establishes the decision to adopt and commit, not an unobserved execution result. Consumer migration remains inventoried below and is outside this delivery.

## Consumer adoption inventory
The completed shared-index rollout inventoried eleven adopted checkouts: Agent Hands, Wireframe Workflows, Agentic Wiki, its nested Wireframe Workflows, Enzo, Website, Open Austin, ResearchOps, Texas LandlordMapper, DesignOps HackPack and Barkonomics. Their existing policy locations, human/agent boundaries, numbered identities and inbound links require a separate receiving-project review before adoption. Global-only projects likewise keep target-owned instructions and policy choices. No busy consumer, global registration or containing pin is changed by this provider pass.

## Verification and delivery
The approved review correction is implemented and verified on the actual final provider tree. All 23 policy and 23 real-Git updater tests pass; both kernel indexes validate and index regeneration is a no-op. Nine skill/two spike frontmatter blocks and 157 local references pass, along with TOML, Python AST, whitespace, new-file ignore and exact scope checks. The bundled skill validator still cannot import PyYAML; direct Ruby YAML/resource checks passed without installing dependencies. The user subsequently approved the reviewed feature, provider adoption and scoped local commit on 2026-11-02. The three actual provider records are adopted; the bundled source stays proposed. The current local checkpoint includes this record and the feature, with exact results verified after commit. No browser, service operation, consumer repository or containing pin is changed.

Current commands from the collection root:

```sh
python3 -B -m unittest discover -s review-agent-policies/tests -v
python3 -B -m unittest discover -s update-project-workflows/tests -v
python3 -B review-agent-policies/scripts/policies.py check --policies adopt-agent-policies/assets/kernel
python3 -B review-agent-policies/scripts/policies.py check --policies docs/agent-policies
python3 -B review-agent-policies/scripts/policies.py index --policies docs/agent-policies --write
git diff --check
```

The helper needs an existing Python 3.11+ standard library, with no packages. The actual provider index now returns ADOPT-POLICIES, PRESERVE-IDENTITY and RESOLVE-DEPENDENCIES in that prerequisite order. Bundled source remains proposed and returns an empty operative plan. The unit-test adoption fixture is isolated; it does not alter either real set. Existing lifecycle runtime/templates are unchanged and are not evidence of new policy behavior.

## Initial draft provenance — historical
These hashes retain the initial unpublished proposal bodies before the user-approved naming/content correction. They do not identify the current candidates, create active aliases or record adoption.

| File | SHA-256 |
| --- | --- |
| `POLICY-ADOPT-adopt-agent-policy-changes.md` | `5caff0a6a4167c1cf220da415b27a04d7e9370d03dd350826d5445c9304516d3` |
| `POLICY-IDENT-preserve-obligation-identity.md` | `575524af51b67b8b096c7402947b42307d72723d6b39ec1e1c6166439abcb78e` |
| `POLICY-LOAD-resolve-policy-prerequisites.md` | `6807016c1b77f9ec002fd99519eba16b85694fa9d16df11121bec092ec8a0064` |

## Current kernel proposal provenance
These are the exact reviewed candidate-source hashes retained as the adoption baseline. Provider copies now differ only in `status` and `authority`; their rule bodies/IDs/edges/dates are unchanged. The separate bundled candidates remain proposed. The later local human adoption decision is recorded above.

| File | SHA-256 |
| --- | --- |
| `ADOPT-POLICIES-require-explicit-adoption.md` | `11fc4d5c4f1752c738fa1df6938e13de58d88f7160e2eb62263750387b4c9111` |
| `PRESERVE-IDENTITY-retain-meaning-and-history.md` | `aad2ead89530add1824f9683053444e4a85f495b41deabc3e2db4384d37ff0e0` |
| `RESOLVE-DEPENDENCIES-load-prerequisites-once.md` | `1bdd4d09782046db1c35ac8fd49ca0ad2ace379478109588aa7ea04db6f9df64` |

## Policy/skill boundary review
| Durable kernel owner | Task procedure and shared implementation |
| --- | --- |
| `ADOPT-POLICIES`: distinction, local human decision authority, operative/proposed state, editorial exception, stable project copies | Create/Edit assess what is being authored; Review examines classification/authority; Adopt/Retire apply the actual decision. No task skill defines new decision rights. |
| `PRESERVE-IDENTITY`: useful continuity, incoming impact, retired-ID reservation and history | Create searches existing owners/IDs; Edit compares changes/dependents; Retire records the approved withdrawal. |
| `RESOLVE-DEPENDENCIES`: prerequisite validity, deterministic one-time loading and non-precedence | Review owns the one checker, technical format, index generation and tests; other task skills link to that implementation. |

The overlap is a task’s reference to its governing obligation, a serialized field, or executable/tested enforcement of a structural invariant. Walkthroughs for source comparison/copying, candidate preparation, adoption edits, index writes and retirement work now live in skills rather than kernel policies. Semantic classification remains a reviewed judgment rather than a regex/test claim.

## Exact current provider path scope
Modified tracked paths:

- `AGENTS.md`
- `README.md`
- `TODO.md`
- `run-project-spike/SKILL.md`
- `setup-project-workflows/SKILL.md`
- `setup-project-workflows/assets/templates/AGENTS.md.template`
- `triage-project-misc/SKILL.md`
- `update-project-workflows/SKILL.md`
- `update-project-workflows/references/updater.md`
- `update-project-workflows/scripts/update.py`
- `update-project-workflows/tests/test_update.py`
- `workflow.toml`

New paths included in the approved feature checkpoint:

- `adopt-agent-policies/SKILL.md`
- `adopt-agent-policies/assets/kernel/ADOPT-POLICIES-require-explicit-adoption.md`
- `adopt-agent-policies/assets/kernel/PRESERVE-IDENTITY-retain-meaning-and-history.md`
- `adopt-agent-policies/assets/kernel/RESOLVE-DEPENDENCIES-load-prerequisites-once.md`
- `adopt-agent-policies/assets/kernel/policy.index.md`
- `adopt-agent-policies/references/migration.md`
- `create-agent-policy/SKILL.md`
- `create-agent-policy/assets/templates/VERB-NOUN-state-the-obligation.md.template`
- `docs/active-spikes/agent-policy-kernel.md`
- `docs/active-spikes/agent-policy-kernel.todo.md`
- `docs/agent-policies/ADOPT-POLICIES-require-explicit-adoption.md`
- `docs/agent-policies/PRESERVE-IDENTITY-retain-meaning-and-history.md`
- `docs/agent-policies/RESOLVE-DEPENDENCIES-load-prerequisites-once.md`
- `docs/agent-policies/policy.index.md`
- `edit-agent-policy/SKILL.md`
- `retire-agent-policy/SKILL.md`
- `review-agent-policies/SKILL.md`
- `review-agent-policies/references/policy-format.md`
- `review-agent-policies/scripts/policies.py`
- `review-agent-policies/tests/test_policies.py`

The earlier untracked umbrella and three old provider proposal filenames are removed from the live tree after verified preservation. They were never committed, adopted or distributed; no compatibility stubs are retained.
