---
name: retire-agent-policy
description: "Retire an agent policy after reviewing incoming dependencies and references, preserving its reserved identity and useful history. Use when an obligation is withdrawn, replaced or split rather than merely edited."
---

# Retire Agent Policy
Resolve the actual project through [target resolution](../README.md#resolve-the-target). Read its instructions, policy index, current obligation/history and applicable adopted kernel. `PRESERVE-IDENTITY` owns retirement and non-reuse; `ADOPT-POLICIES` owns decision authority/status; `RESOLVE-DEPENDENCIES` owns valid prerequisites. Bundled candidates are not operative project rules, and this procedure adds no authority.

## Review the impact
Establish why the obligation is being withdrawn/replaced and what the human actually authorized. Search incoming prerequisite edges and meaningful references in policy bodies, skills and project routing. Use [Review Agent Policies](../review-agent-policies/SKILL.md) to assess the result. Do not assume a replacement ID has the same meaning or automatically redirect a dependent.

Prepare necessary dependent changes through [Edit Agent Policy](../edit-agent-policy/SKILL.md), replacement obligations through [Create Agent Policy](../create-agent-policy/SKILL.md), and their adoption through [Adopt Agent Policies](../adopt-agent-policies/SKILL.md). Keep the current operative set intact while those changes are only proposals.

## Apply the authorized retirement
Recheck the exact retirement/dependent decision and current files. Keep the retirement the way the selected project’s adopted PRESERVE-IDENTITY says to; do not add a retirement record that policy does not ask for.

- **Where it retains retirement records:** record `retired`, actual human authority, substantive date and concise retirement rationale/history pointers under its metadata contract, using the [technical representation notes](../review-agent-policies/references/policy-format.md), and keep the record indexed.
- **Where it keeps retired policies only in Git:** delete the policy file and its index row, and put the human decision, date and rationale in the retiring commit.

Either way the ID stays reserved. Preserve useful history without leaving a live override chain. Reconcile the index and validate the complete resulting set using the shared tool.

For a Git-backed change, hand Commit Work the affected mnemonic policy IDs and the reviewed decision rationale under PRESERVE-IDENTITY.

Report the retired obligation, handled/remaining incoming dependencies and what remains operative. Preserve concurrent edits and follow the project's commit/publication controls.
