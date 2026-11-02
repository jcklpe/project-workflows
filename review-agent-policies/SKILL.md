---
name: review-agent-policies
description: "Review agent policies for scope, identity, dependency impact, contradictions and policy/skill boundaries; run structural checks and reconcile their index. Use for policy review, graph failures or an adoption-readiness assessment."
---

# Review Agent Policies
Resolve the actual project through [target resolution](../README.md#resolve-the-target). Read its applicable instructions and declared policy index. Review the operative policies and selected candidate set separately; use the actual adopted kernel when present and existing project authority for initial proposals. The shipped [kernel candidates](../adopt-agent-policies/assets/kernel/policy.index.md) are proposed source, not authority conferred by this skill.

## Review meaning and ownership
Read the actual adopted PRESERVE-IDENTITY frontmatter contract; the technical reference and checker implement that contract rather than defining policy obligations. Use `ADOPT-POLICIES` to assess the policy/skill boundary, actual decision authority and operative status. Does the policy state a durable obligation, scope and exceptions, while the skill supplies the task procedure? Identify any rule invented only in a skill, procedural walkthrough embedded in policy, duplicated rule body or conflicting owner. Report the exact affected spans and a concrete correction within the authorized scope.

Use `PRESERVE-IDENTITY` to assess continuity, retired-ID reuse and incoming dependent/reference impact. Use `RESOLVE-DEPENDENCIES` to assess prerequisite meaning, applicable closure and contradictions. Structural loading order is not semantic precedence. Compare the complete actual/candidate set with project instructions and relevant tool guards; the checker cannot make those judgments. A review is not an adoption decision.

## Structural checks and index
The [format/loading contract](references/policy-format.md) owns technical representation. With an **existing Python 3.11+** and either existing PyYAML or Ruby/Psych YAML support, use the single [optional tool](scripts/policies.py) from this selected skill folder. No package/environment installation is needed or implied. Ordinary reading/editing and semantic review do not require this tool. Resolve these placeholder paths explicitly:

```sh
python3 <selected-review-skill>/scripts/policies.py check --policies <actual-project-agent-policy-directory>
python3 <selected-review-skill>/scripts/policies.py check --policies <actual-project-agent-policy-directory> --root EDIT-SAFE
python3 <selected-review-skill>/scripts/policies.py index --policies <actual-project-agent-policy-directory>
python3 <selected-review-skill>/scripts/policies.py index --policies <actual-project-agent-policy-directory> --write
```

`check` is read-only and returns no loading plan on failure. `index` previews by default; when index maintenance is authorized, `--write` updates only the marked generated table after selected-file rechecks, preserving surrounding prose. Reruns are no-ops. Do not redirect output over an existing index or repair malformed markers/concurrent edits by overwriting them. The tool never adopts/edits policies, commits, fetches remote links, installs dependencies or changes permissions. Use the contract's [manual checks](references/policy-format.md#manual-checks) when no compatible interpreter exists, and report that the tool did not run.

Report structural results separately from semantic/authority questions, actual agent loading/compliance and tool enforcement. Route candidate changes to [Create](../create-agent-policy/SKILL.md) or [Edit](../edit-agent-policy/SKILL.md), explicit adoption to [Adopt](../adopt-agent-policies/SKILL.md), and retirement to [Retire](../retire-agent-policy/SKILL.md). These links select procedures; they add no authority or mandatory new approval gate.
