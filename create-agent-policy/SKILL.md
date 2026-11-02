---
name: create-agent-policy
description: "Decide whether a new durable agent policy is needed, locate existing owners and overlapping obligations, and draft its initial scope and mnemonic identity. Use edit-agent-policy for changes to an existing obligation."
---

# Create Agent Policy
Resolve the actual project through [target resolution](../README.md#resolve-the-target), then read its instructions, policy index and applicable adopted kernel. In the shipped kernel, `ADOPT-POLICIES` defines the policy/skill distinction and decision authority; `PRESERVE-IDENTITY` governs identity. Bundled candidates remain proposals until adopted. Use existing project authority when proposing an initial adoption; this procedure adds none.

## Establish the need and owner
Read the request and existing policy bodies, skills, adapters and relevant history. Identify the durable obligation, the agent activity it governs and the actual owning project. Apply the kernel's policy/skill distinction: if the need is a way to perform a task, route it to the appropriate skill within the authorized scope. A skill's inconvenience is not itself a reason for a new policy.

If an existing obligation already covers the need, reuse it or use [Edit Agent Policy](../edit-agent-policy/SKILL.md) to propose the actual change. Do not create a parallel owner or a new ID just to avoid reviewing an existing policy.

## Draft the initial obligation
1. Establish the proposed scope, obligation, exceptions and useful rationale. Keep unresolved alternatives in the owning spike rather than presenting them as operative policy.
2. Search indexed active/proposed/retired IDs and available history, then choose a mnemonic that identifies the obligation without encoding rank. Read the selected project’s adopted PRESERVE-IDENTITY metadata contract; use the [format/checker notes](../review-agent-policies/references/policy-format.md) for supported representation and checks.
3. Apply the kernel’s naming convention to the proposed role: `type: kernel` uses an underscore filename prefix; `type: operational` is unprefixed. Neither makes the policy more authoritative. Use the inline creation example below in the actual project-owned directory; replace its example values rather than creating another template file. Record only real prerequisite and related edges. Draft the durable rule; leave execution walkthroughs to their skill owner.
4. Use [Review Agent Policies](../review-agent-policies/SKILL.md) for the complete set, dependency impact and index reconciliation. Hand a concrete candidate to [Adopt Agent Policies](../adopt-agent-policies/SKILL.md) only when adoption is requested/authorized under the applicable policy. Creation itself produces a proposal.

Report the need/owner assessment, candidate scope/ID, reused obligations and any procedure work routed elsewhere. Follow the project's spike and commit conventions; this skill does not authorize unrelated changes or publication.

## Creation example
The selected project’s adopted kernel defines the record contract. This example is part of the creation procedure, not a separate source of policy requirements. Replace the ID, title, scope, date and actual prerequisite/related IDs; keep status proposed and authority empty until an actual adoption decision.

```md
---
id: EDIT-SAFE
type: operational
scope: "Agent edits in this project checkout."
status: proposed
authority: ""
revised: "YYYY-MM-DD"
depends_on: []
related_to: []
---
# Preserve concurrent edits
State the durable obligation, scope and real exceptions. Keep the execution walkthrough in its owning skill. Add only the rationale, references and boundaries needed to apply this rule.
```
