# Deterministic consumer updates
Use an existing Python 3.11+ interpreter and Git. Preview before applying; the helper never stages parent files, commits or pushes.
## Required layout
The parent has an initialized root `project-workflows/` gitlink with a clean detached child. Its AGENTS declares a documentation-folder `project-workflows.toml`, normally `docs/project-workflows.toml`. Set `schema_version = 1`, `project.root = ".."` and `adoption.mode = "shared"`. The helper auto-discovers one config in docs or _meta, or accepts `--config` for a custom documentation folder with the same basename. The package’s `example.workflow.md` is documentation only.

Only the current layout is supported. Old filenames, root config files, child-config branches, `documents.policies`, the old agent-policy directory and root JSON baselines are rejected. Correct a receiving project explicitly before running the updater; no fallback or automatic migration is provided. Preserve original history and verified source baselines when doing that work. No other consumer is changed by updating this collection.
## Preview and apply
```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py update --project . --config docs/project-workflows.toml --revision ACCEPTED_COMMIT
python3 -B project-workflows/update-project-workflows/scripts/update.py update --project . --config docs/project-workflows.toml --revision ACCEPTED_COMMIT --apply
```

The accepted revision must descend from the current child. `--fetch REMOTE` is optional and must be within authorization. Shared settings and local workflow notes remain in the parent; the target package must not contain a root runtime configuration. Selected files cannot be staged, ignored or symlinked. Missing baselines, missing source/destination files and conflicts stop the update. `--reviewed PATH` records review of a copied-asset overlap; a textual conflict still requires resolution.

Exit 0 reports a plan/success, 2 reports required review, and 1 reports an error. After apply, inspect the child revision, parent pin and changed assets. An interrupted update can leave the child advanced or some asset writes completed; there is no cross-repository transaction or automatic rollback. Inspect actual state before recovery. Repeating a completed update makes no changes.
## Copied-asset records
```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py record-assets --project . --revision INSTALLED_COMMIT --asset .github/PULL_REQUEST_TEMPLATE.md=setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template
```

Preview, then repeat with `--apply`. Use the actual source revision, not today's pin. Existing baselines cannot be replaced by record-assets. The updater maintains only this section of the selected shared TOML, preserving all other settings and comments:

```toml
# project-workflows-assets:start
[assets.".github/PULL_REQUEST_TEMPLATE.md"]
source = "setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template"
revision = "FULL_INSTALLED_SOURCE_COMMIT"
# project-workflows-assets:end
```

Put the markers at table boundaries and keep unrelated settings outside them. Source paths are relative to the package; destinations are relative to the parent. Updates use the previous source, incoming source and local copy for three-way reconciliation. Only changed source baselines advance. Private project-workflows.local.toml is not an updater input and never enters its output.
## Policy and context boundaries
Shared configuration, local workflow notes and project-owned policies are not automatically refreshed assets. `documents.agent_policies` defaults to `docs/agent-policies`. The helper rejects policy-index destinations, that directory and distributed kernel sources. Source delivery does not adopt policy obligations or change permissions.
## Offline checks
```sh
python3 -B -m unittest discover -s update-project-workflows/tests
```
