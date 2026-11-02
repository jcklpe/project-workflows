# Agent policy format and checks
This is the shared technical contract for all five policy task skills, not an additional policy body. The actual project's adopted kernel owns durable obligations and decision authority. In the [bundled candidates](../../adopt-agent-policies/assets/kernel/policy.index.md), `ADOPT-POLICIES` owns the policy/skill distinction and adoption, `PRESERVE-IDENTITY` owns continuity/retirement, and `RESOLVE-DEPENDENCIES` owns graph/loading obligations. Bundled proposals do not become operative through this reference.

## Files and metadata
Use the project's declared agent-policy directory and index; the default is a flat `docs/agent-policies/` with `policy.index.md`. Filenames combine the exact mnemonic ID with a lowercase imperative slug, for example `EDIT-SAFE-preserve-concurrent-edits.md`. The single level-one heading supplies the concise imperative title. The checker validates identifier syntax and filename association; meaning, useful continuity and imperative grammar need review.

Policies use a small TOML header between `+++` lines, allowing the optional tool to use an existing Python 3.11+ standard library without a YAML dependency. Skill/spike frontmatter remains YAML. Supported metadata:

```toml
id = "EDIT-SAFE"
scope = "Agent edits in this project checkout."
status = "proposed"
authority = ""
revised = "2026-11-02"
depends_on = []
related_to = []
```

The first six fields are required; `related_to` is optional. Scope/title/authority are plain single lines without table separators. IDs use uppercase alphanumeric words separated by hyphens. `depends_on`/`related_to` are arrays of IDs from this index. `revised` is a quoted valid ISO substantive revision date. Nested tables, speculative kind/audience fields, active supersedes/override metadata and unknown fields are rejected.

The supported statuses are `proposed`, `adopted` and `retired`. The tool requires nonempty `authority` for adopted/retired records, but does not authenticate the human decision that field records. Its presence is a structural condition, not proof of adoption. Apply the kernel's substantive-change/editorial distinction when maintaining `revised`; the tool only validates date syntax.

Use ordinary inline relative Markdown links/anchors for local references and http/https/mailto links for external context. Reference-style links/HTML link syntax and optional link-title syntax are outside this checker's supported source format. Existing Markdown headings and explicit HTML `name`/`id` anchors in target documents are supported. External references are not fetched or verified. Cross-project context uses body links rather than invented cross-repository prerequisite loading.

## Generated index contract
The index contains human-owned context and exactly one generated table between:

```md
<!-- agent-policies:start -->
| ID | Policy | Scope | Status | Revised |
| --- | --- | --- | --- | --- |
<!-- agent-policies:end -->
```

The tool emits one row per policy file, with ID, linked title, one-line scope, status and substantive revision date. Rows sort lexically for navigation, independently of loading order or authority. Bodies remain in their files. Index rendering preserves surrounding text; it does not modify policy metadata/status.

`check` fails on a stale/missing table. `index` previews; authorized `index --write` replaces only the marked table, or creates an absent index. Existing unmarked/malformed content requires manual reconciliation rather than a guessed overwrite. Selected policy/index snapshots and inventory are rechecked immediately before replacement; this is not a filesystem lock or transaction. An unchanged rerun performs no write.

## Graph and loading implementation
The checker first validates the complete declared set: unique IDs, metadata, filenames, local links, resolvable prerequisite/reference targets and table agreement. It checks adopted prerequisites for adopted status and detects a cycle path in the complete declared prerequisite graph, including proposals and retained historical edges. Related-reference cycles do not form prerequisite cycles.

With no selected roots, the plan includes all adopted policies. Repeated `check --root ID` requests an adopted root set and its prerequisite closure while still validating the complete set. Related references do not enlarge that closure. The implementation uses topological ordering with a lexical-ID ready queue and emits each selected policy once. Failure emits no partial loading plan. This implements `RESOLVE-DEPENDENCIES`; it does not rank rules, decide applicable scope or settle contradictory meaning.

Retained retired records keep their IDs resolvable and indexed. Any obsolete historical edge can be removed deliberately with retirement context; missing targets and cycles remain structural failures. The kernel and human review own whether an identity/dependency change is appropriate.

## Tool and enforcement limits
The checker verifies supported representation and graph/index properties. It does not load instructions into an agent client, prove human intent, detect all semantic conflicts, establish identity continuity/non-reuse across all Git history, verify that a revision date reflects a substantive change, or make agents comply. [Review Agent Policies](../SKILL.md) supplies the procedure for those separate assessments.

The [collection updater](../../update-project-workflows/scripts/update.py) protects known kernel-source copies, index destinations and declared/default agent-policy directories from its automatic copied-asset refresh. This is a real, narrow tool guard; it cannot identify every arbitrarily renamed paragraph or prevent a human from editing files. Kernel adoption remains the governing decision boundary. Other enforcement stays with actual CLI guards, hooks/CI or service permissions, not edits to Markdown.

## Manual checks
Without a compatible existing interpreter, compare each indexed header/body to its row, search identity/history for duplicate/retired IDs and resolve local links. Walk prerequisite edges with unvisited/visiting/done marks to find cycles. Verify adopted prerequisite statuses, then repeatedly select ready nodes in lexical order and record each once. Review human authority, continuity, policy/skill boundaries and contradictions separately. Report manual coverage and that the deterministic tool did not run; ordinary Markdown use needs no runtime installation.
