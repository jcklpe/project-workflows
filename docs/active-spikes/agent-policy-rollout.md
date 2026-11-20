---
attention: live
reviewed: 2026-11-02
---
# Agent policy rollout
Opened 2026-11-02. Stable slug: `agent-policy-rollout`. [Tasks](agent-policy-rollout.todo.md). Continues the [provider kernel](agent-policy-kernel.md) and the completed Agent Hands migration exercise. This tracker coordinates prepared receiving-project handoffs; it does not perform or adopt their migrations.

## Current reconciliation scope
This record preserves the receiving handoffs prepared on 2026-11-02. Revalidate each receiving owner before acting; the inventory and local commit identifiers below are dated evidence, not current delivery pins. The 2026-11-20 reconciliation covers the provider, Agent Hands and configs only. It does not launch or authorize migrations in the other listed consumers. Current provider delivery uses unchanged shared source and the documented deliberate conversion route for older configurations.

## Baseline and launch model — 2026-11-02
Target provider `79dddf9742c282d184c65d5c5ef87a142900897f` supplies the reviewed YAML/type/underscore system and five policy skills. Agent Hands locally committed its receiving pilot as `9b210f96e6d2ccc5f0b6870a068f0160b138797f`, with workflow adaptation `0ed5ac87980ec9557302fa52e9f765a93a122ce9`. Three kernel and eight operational records are adopted there, with eight exact sanitized retirement blocks, the old folder removed, 184 prior privacy-preservation hashes retained and 53 policy/updater tests passing. These are local-only records; publication, remote retrievability and fresh-client acceptance are not established.

The 2026-11-02 bounded live scan covers canonical installations/declared adoptions under the existing configs and work roots, plus the known configured private global-only workspace. It finds ten remaining pinned checkouts (nine canonical receiving owners, because Wireframe has a nested second checkout), configs in canonical/global-only mode, and one private global-only target. Agent Hands and the provider’s own adoption are already complete for migration; their observed-use acceptance remains separate. Other unknown/global consumers are not claimed inventoried.

## Receiving owners
Every public receiving owner uses `docs/active-spikes/agent-policy-migration.md` and its paired task file, with the local TODO index. The private target retains its own configured local path. Existing completed policies-migration records and original adoption/design/GitHub spikes are linked for provenance and retained QA, rather than reopened or silently closed. All new pairs have bounded receiving scope and no implementation/adoption performed.

| Receiving owner | Handoff | Mode/current source snapshot | Preparation status |
| --- | --- | --- | --- |
| [configs](https://github.com/jcklpe/configs) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | Canonical/global-only target; no adaptation | Handoff prepared; no migration/adoption |
| [Wireframe Workflows](https://github.com/jcklpe/wireframe-workflows) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/wireframe-workflows at c949eb8456e7 | Handoff prepared; no migration/adoption |
| [Agentic Wiki](https://github.com/Agentic-Collaborative-Wiki-HAI/agentic-wiki) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/agentic-wiki at 4af8662e6707 | Prepared outside checkout: explicit dirty-worktree hold pending |
| [Enzo](https://github.com/jcklpe/enzo-lang) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/enzo-lang at ff8de60e837f | Handoff prepared; no migration/adoption |
| [Website](https://github.com/jcklpe/my-website) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/my-website at e80f92300715 | Handoff prepared; no migration/adoption |
| [Open Austin Org](https://github.com/open-austin/org) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/org at 9ec77be0459f | Handoff prepared; no migration/adoption |
| [ResearchOps maintainer](https://github.com/jcklpe/researchOps-dev) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/researchops-dev at edf447894eaf | Handoff prepared; no migration/adoption |
| [Texas LandlordMapper design](https://github.com/open-austin/Texas-LandlordMapper-design) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/texas-landlordmapper-design at 5e616cfcb31c | Handoff prepared; no migration/adoption |
| [DesignOps HackPack](https://github.com/jcklpe/designOps-hackpack) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/designops-hackpack at 5a3d7ff4e8cf | Handoff prepared; no migration/adoption |
| [Barkonomics](https://github.com/Barkonomics-DataWrangling/barkonomics-pet-names) | `docs/active-spikes/agent-policy-migration.md` + `.todo.md` | project/barkonomics at a362492eecb6 | Handoff prepared; no migration/adoption |
| Private global-only workspace | Private handoff retained with its local system owner | Global-only; no collection updater/pin | Ready privately; no inventory exported |
| Agentic Wiki → nested Wireframe Workflows | Delivery owned by Agentic Wiki’s handoff after canonical Wireframe work | Separate checkout/adaptation, same Wireframe source repository | Dependent; no duplicate policy-authoring spike |

## Independence and ordering
Configs, Enzo, Website, Open Austin, ResearchOps maintainer, Texas design, DesignOps and Barkonomics can be pursued as separate workstreams after their local authority/concurrency checks. Canonical Wireframe policy authoring can run independently too. Agentic Wiki’s top-level workflow/policy inventory can proceed once its explicit dirty-worktree hold is resolved; nested Wireframe delivery waits for the canonical Wireframe result and stays with that same receiving owner. Do not launch another agent to rewrite the same seven canonical policies in the nested checkout. The private global-only target has no Git dependency on these consumers and keeps its decisions/data private.

One agent owns each receiving pair. Work stays in the receiving repository; no per-consumer project narratives belong inside its Project Workflows child. Agents must recheck live status and preserve concurrent edits, not reset/stash/overwrite for a clean preview. Each receiving owner updates only its own pair/index. A single rollout coordinator folds receipts into this central tracker, avoiding all agents editing the same file. Shared TODO snapshots follow Commit Work’s understood-index exception, not blanket permission to commit referenced implementation.

## Adoption and delivery gates
Package source availability is distinct from project-owned adopted policy copies. A future “pursue this spike till done” starts bounded work but does not manufacture human approval of unseen substantive obligations. Each receiving handoff requires an exact candidate comparison and actual adoption decision, preserving operative text pending approval. Policies govern agents; human governance, design agreements and product requirements retain their actual owners. YAML/type/prefix, identity/dependency, private-preservation and actual enforcement checks follow the selected five skills and single shared contract. A semantic conflict is reported for resolution, never decided by lexical ordering or a successful parser.

Use the deterministic updater for applicable pinned delivery, obtaining the exact locally committed source object through an authorized local route if it is not remotely available. Global-only targets compare selected instructions/configuration and do not create a collection. Source updates do not auto-refresh adopted policies. Align legacy/current policy locators deliberately; do not erase human governance by mechanically selecting the pilot’s directory everywhere. Commit/pin rights follow the target, child first. Source/consumer local commits are not publication authority. No pushes, PR/issue mutations, notifications, tool installation, service permissions or browser fallback are authorized by this preparation.

## Pilot lessons and outstanding acceptance
The migration exercise actually used creation/owner review, eight edits, semantic/graph review, explicit adoption and numeric retirement. It satisfies that lifecycle/migration part of provider real-use evaluation. It does not establish spontaneous fresh-agent retrieval, ordinary service-policy compliance, UI rendering, provider grants or ongoing client behavior. Agent Hands keeps one concrete next ordinary-authorized-task loading/safeguard check under its pilot; do not issue service writes solely as a smoke test. Provider acceptance and receiving acceptance are separate records.

The November 2 preparation also identified five Agent Hands imported records and two configs policy-migration archive files with navigation repairs. Their preservation and publication belong to the owning repository’s reconciliation, not this rollout. Receiving-project publication decisions remain separate.

## Reusable launch instruction
Open the actual receiving checkout, then say:

> Pursue `docs/active-spikes/agent-policy-migration.md` and its task pair until the bounded migration is verified. Read AGENTS and preserve concurrent work. Use the exact provider revision and deterministic updater where applicable. Honor the recorded adoption/commit gates; present the concrete decision if one is missing, continue independent work, and report exact blockers. Do not publish, push, mutate external systems or migrate other projects.

Use the private target’s configured system-spike path in its own workspace. Do not launch the nested Wireframe checkout separately. Initial startup must report if a prepared handoff has not yet been applied because of an explicit local hold.
