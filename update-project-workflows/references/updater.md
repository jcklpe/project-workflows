# Routine updater
The optional [helper](../scripts/update.py) uses an existing Python 3.11+ interpreter and Git 2.38+; no packages, environment, service credentials or installation are needed. Core skills remain ordinary Markdown. If those tools are unavailable or a project forbids scripted merges, follow the same comparison with ordinary Git and document access. The helper is for an initialized root `project-workflows/` adoption, not shared-source maintenance, global-only targets or migration.

## Preview and apply
Run from the actual parent project after reading its instructions and checking the authorized upstream, branch, outgoing commits, dirty state and commit policy. Substitute the existing interpreter if `python3` is older than 3.11. The script path below uses that project's selected collection; a reviewed newer helper can also be invoked directly when an older adoption does not yet contain it.

```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py update --project . --revision origin/main --fetch origin
```

`--fetch` is explicit and optional. Resolve and retain the returned full `accepted` SHA; use that exact revision for apply so a moving remote ref cannot change the reviewed input. A preview can write Git objects/fetched refs, but does not change the child branch, index, working files or parent pin. Exit 0 is a plan/success, 2 reports focused `review_required` paths or a missing merge message, and 1 is a failed check. A failed fetch or read is not success. Do not continue on nonzero exit without resolving its reported condition.

```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py update --project . --revision ACCEPTED_COMMIT --apply
```

An adaptation with only project settings normally merges without further procedure review. A divergent apply also requires `--message` with the exact reviewed merge commit message, including any required `Spike:` trailer. Show that message in chat and follow the target's commit/review policy before applying. A fast-forward creates no commit and needs no message. For a procedure customized on both sides, inspect the merge-base→local and merge-base→accepted patches and their combined behavior. For an edited copied asset, compare the installed file with its recorded source baseline and incoming source. After resolving the actual semantic decision, add `--reviewed relative/path` for each reported overlap; this acknowledges that specific review, not blanket acceptance of arbitrary conflicts. Textual conflicts cannot be bypassed by this flag: reconcile them explicitly with the project's normal Git/document workflow, preserve history, and repeat the checks.

The helper refuses dirty child files, staged selected parent paths, a detached/mismatched child branch, missing/ambiguous ancestry, changed existing TOML values and missing asset baselines. A clean three-way merge preserves local TOML values and accepts new upstream keys. A deliberate upstream default change to an existing value requires explicit reconciliation. Other unstaged/staged parent work is left alone. Ignored private journals are outside its work; symlinked/escaping asset paths are rejected.

Apply performs a normal fast-forward or Git merge, verifies the preview tree, accepted ancestry and preserved settings, then updates only planned installed assets and their baselines. A merge commit is permitted only when the target policy permits it. Hooks, signing and ordinary Git errors remain real failures. No parent staging/commit or push is performed. Use Commit Work for the parent gitlink, directly affected assets, baseline file and routing/docs. Report pending and committed pin states separately. Run relevant frontmatter/resource/asset and project checks; the helper parses TOML and checks whitespace, not every project behavior.

There is no cross-repository transaction. A Git/hook/filesystem failure after apply begins can leave a completed child merge or some parent writes. The helper reports failure, does not retry, and never stashes/resets work. Inspect actual HEAD/index/files before recovery. A completed second run with the same accepted revision and baseline has no new merge commit or edits. Exact overlapping paths are a focused review aid; they cannot discover every behavioral interaction between different customized files. An actual known semantic conflict still requires attention.

## Copied asset baselines
When setup installs selected copies, record each destination's actual source path and full installed commit in the parent's tracked `.project-workflows-assets.json`. This is a small source-baseline file, not a task ledger or runtime configuration. Preserve its mapping when upgrading the collection; custom destination names and selected profile copies can be recorded too. A submodule pin alone does not prove which source was copied into a parent file.

```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py record-assets --project . --revision INSTALLED_COMMIT --asset .github/PULL_REQUEST_TEMPLATE.md=setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template
```

Preview first, then repeat with `--apply` to write the baseline file. Repeat `--asset DEST=SOURCE` for the other selected copies. Local edits to an installed copy are allowed; the revision describes its **source baseline**, not a claim of byte identity. Establish that revision from the installation commit/record and source comparison, not a guess. Existing entries cannot be silently rebased by `record-assets`. If no trustworthy baseline is recoverable, compare and reconcile the old copy manually, establish a reviewed new installed baseline, and record that limited provenance honestly before routine updates.

The file can be maintained by hand with ordinary text/Git access using the same format:

```json
{
  "schema_version": 1,
  "files": {
    ".github/PULL_REQUEST_TEMPLATE.md": {
      "source": "setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template",
      "revision": "FULL_INSTALLED_SOURCE_COMMIT"
    }
  }
}
```

An unchanged copy takes the incoming source mechanically; an edited copy uses Git's three-way file merge and focused review when both source and copy changed. A conflict, missing source/destination or symlink stops before the collection merge. If upstream source bytes are unchanged, keep the local copy and its existing baseline. Baselines advance to the resulting child commit only for changed sources, preventing unnecessary file churn. The helper recognizes the four standard `.github` destinations and refuses to skip existing unrecorded copies; nonstandard destinations must be inventoried and registered explicitly. Keep original baseline commits retrievable in the adaptation history before publishing the parent.

## Offline checks
From this collection's root, use an existing interpreter:

```sh
python3 -B -m unittest discover -s update-project-workflows/tests -v
```

Tests create isolated Git repositories and exercise actual merges, retained configuration/history/index state, focused review, copied-file reconciliation, rejected conflicts, failure propagation and repeat no-op. They require no network, service credentials, project mutation or dependency download. They do not prove consumer rollout, remote retrievability, fresh-client discovery, live automation or measured token savings.
