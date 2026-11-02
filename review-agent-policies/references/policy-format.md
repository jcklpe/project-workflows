# Agent policy format and checks
The actual project’s adopted PRESERVE-IDENTITY policy owns the policy-record/frontmatter contract. This reference supplies technical representation and checker notes for the five task skills; it is not an additional policy body or an independent schema owner. The actual project's adopted kernel owns durable obligations and decision authority. In the [bundled candidates](../../adopt-agent-policies/assets/kernel/policy.index.md), `ADOPT-POLICIES` owns the policy/skill distinction and adoption, `PRESERVE-IDENTITY` owns continuity/retirement, and `RESOLVE-DEPENDENCIES` owns graph/loading obligations. Bundled proposals do not become operative through this reference.

## Files and metadata
Use the project's declared agent-policy directory and index; the default is a flat `docs/agent-policies/` with `policy.index.md`. Filenames combine the exact mnemonic ID with a lowercase imperative slug, for example `EDIT-SAFE-preserve-concurrent-edits.md`. The single level-one heading supplies the concise imperative title. The checker validates identifier syntax and filename association; meaning, useful continuity and imperative grammar need review.

Use the [inline creation example](../../create-agent-policy/SKILL.md#creation-example) after reading the actual adopted kernel contract. The [bundled PRESERVE-IDENTITY source](../../adopt-agent-policies/assets/kernel/_PRESERVE-IDENTITY-retain-meaning-and-history.md#policy-record-metadata) shows the distributed definition, but remains proposed until adopted in the receiving project.

The checker requires the kernel’s declared fields and permits omission of `related_to`. Scope/title/authority are plain single lines without table separators. IDs use uppercase alphanumeric words separated by hyphens. `depends_on`/`related_to` are arrays of IDs from this index. `revised` is an ISO substantive revision date; quoted and ordinary YAML date scalars are accepted. Nested tables, speculative kind/audience fields, active supersedes/override metadata and unknown fields are rejected.

Interpret `type` under the adopted kernel’s metadata contract. The checker accepts a plain nonempty label rather than a closed two-value enum; the creation example uses `operational`. Under `PRESERVE-IDENTITY`, kernel filenames start with `_` before the unchanged ID (for example `_ADOPT-POLICIES-require-explicit-adoption.md`); operational filenames are unprefixed. File grouping and this presentation prefix do not change prerequisite order or authority.

The supported statuses are `proposed`, `adopted` and `retired`. The tool requires nonempty `authority` for adopted/retired records, but does not authenticate the human decision that field records. Its presence is a structural condition, not proof of adoption. Apply the kernel's substantive-change/editorial distinction when maintaining `revised`; the tool only validates date syntax.

Use ordinary inline relative Markdown links/anchors for local references and http/https/mailto links for external context. Reference-style links/HTML link syntax and optional link-title syntax are outside this checker's supported source format. Existing Markdown headings and explicit HTML `name`/`id` anchors in target documents are supported. External references are not fetched or verified. Cross-project context uses body links rather than invented cross-repository prerequisite loading.

## Generated index contract
The index contains human-owned context and exactly one generated table between:

```md
<!-- agent-policies:start -->
| ID | Policy | Type | Scope | Status | Revised |
| --- | --- | --- | --- | --- | --- |
<!-- agent-policies:end -->
```

The tool emits one row per policy file, with ID, linked title, descriptive type, one-line scope, status and substantive revision date. Kernel rows appear first, with IDs sorted lexically within the kernel/other groups for navigation. This does not affect loading order or authority. Bodies remain in their files. Index rendering preserves surrounding text; it does not modify policy metadata/status.

`check` fails on a stale/missing table. `index` previews; authorized `index --write` replaces only the marked table, or creates an absent index. Existing unmarked/malformed content requires manual reconciliation rather than a guessed overwrite. Selected policy/index snapshots and inventory are rechecked immediately before replacement; this is not a filesystem lock or transaction. An unchanged rerun performs no write.

## Graph and loading implementation
The checker first validates the complete declared set: unique IDs, metadata, filenames, local links, resolvable prerequisite/reference targets and table agreement. It checks adopted prerequisites for adopted status and detects a cycle path in the complete declared prerequisite graph, including proposals and retained historical edges. Related-reference cycles do not form prerequisite cycles.

With no selected roots, the plan includes all adopted policies. Repeated `check --root ID` requests an adopted root set and its prerequisite closure while still validating the complete set. Related references do not enlarge that closure. The implementation uses topological ordering with a lexical-ID ready queue and emits each selected policy once. Failure emits no partial loading plan. This implements `RESOLVE-DEPENDENCIES`; it does not rank rules, decide applicable scope or settle contradictory meaning.

Retained retired records keep their IDs resolvable and indexed. Any obsolete historical edge can be removed deliberately with retirement context; missing targets and cycles remain structural failures. The kernel and human review own whether an identity/dependency change is appropriate.

## Tool and enforcement limits
The checker verifies supported representation and graph/index properties. It does not load instructions into an agent client, prove human intent, detect all semantic conflicts, establish identity continuity/non-reuse across all Git history, verify that a revision date reflects a substantive change, or make agents comply. [Review Agent Policies](../SKILL.md) supplies the procedure for those separate assessments.

The [collection updater](../../update-project-workflows/scripts/update.py) protects known kernel-source copies, index destinations and declared/default agent-policy directories from its automatic copied-asset refresh. This is a real, narrow tool guard; it cannot identify every arbitrarily renamed paragraph or prevent a human from editing files. Kernel adoption remains the governing decision boundary. Other enforcement stays with actual CLI guards, hooks/CI or service permissions, not edits to Markdown.

## Optional YAML parsing
Core policy reading/editing does not require running a validator. With an existing Python 3.11+ interpreter, the checker uses PyYAML `safe_load` when available, otherwise an already-installed Ruby/Psych `YAML.safe_load` passed data on stdin. It does not implement a custom YAML parser, install packages, create environments or execute YAML object tags. The supported fields are simple scalars and ID lists. If neither supported parser is available, it reports that gap and returns no loading plan; use manual review instead. Do not substitute an eyeballed pass for checks that were not executed.

## Manual checks
Without a compatible existing interpreter, compare each indexed header/body to its row, search identity/history for duplicate/retired IDs and resolve local links. Walk prerequisite edges with unvisited/visiting/done marks to find cycles. Verify adopted prerequisite statuses, then repeatedly select ready nodes in lexical order and record each once. Review human authority, continuity, policy/skill boundaries and contradictions separately. Report manual coverage and that the deterministic tool did not run; ordinary Markdown use needs no runtime installation.
