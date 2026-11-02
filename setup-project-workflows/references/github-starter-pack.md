# GitHub starter pack
Read this when the project selects GitHub templates or lifecycle automation. Project Workflows owns these project-operation assets; Agent Hands supplies agent-facing GitHub access/setup tools. Ordinary local work and collaborator onboarding require neither GitHub credentials nor this pack.

## Select and adapt files
Inspect the target's existing files, profile and automation first. Copy only the selected files, adapting existing content rather than replacing a whole `.github/` directory. Review the exact local diff before any authorized publication. No installation script, dependency manifest or package download is needed in the consuming folder.

| Starter | Destination in the consuming project |
| --- | --- |
| [Contribution issue](../assets/templates/github/ISSUE_TEMPLATE/contribution.md.template) | `.github/ISSUE_TEMPLATE/contribution.md` |
| [Pull request](../assets/templates/github/PULL_REQUEST_TEMPLATE.md.template) | `.github/PULL_REQUEST_TEMPLATE.md` |
| [Team Kanban profile](../assets/templates/lifecycle/team-kanban.md.template) | The project's selected lifecycle policy owner. |
| [Organization Kanban profile](../assets/templates/lifecycle/organization-kanban.md.template) | The project's selected lifecycle policy owner. |
| [Lifecycle workflow](../assets/templates/github/project-lifecycle.yml.template) | `.github/workflows/project-lifecycle.yml` |
| [Lifecycle helper](../assets/templates/github/lifecycle.cjs) | `.github/project-workflows/lifecycle.cjs` |

The two profiles propose editable meanings and transitions. They do not assert the exact policy of a reference board. Preserve an existing profile, choose only one starting point where needed, and remove unused guidance. Issue/PR content does not assign people, force an issue per spike, or automatically close umbrella work.

Record selected installed copies in the parent's tracked `.project-workflows-assets.json` using the [updater baseline format](../../update-project-workflows/references/updater.md#copied-asset-baselines): source path, destination and actual installed source commit, including adapted profile copies where selected. Use the optional standard-library helper or maintain that small file by hand. No local runtime is required to copy/adapt the assets. For an existing installation, recover its real baseline before upgrading; a current submodule pin alone does not establish it. Future updates reconcile the copies as well as the child pin, preserving local edits.

The automation's two text files run on GitHub-hosted Ubuntu through pinned official checkout, App-token and github-script actions. The helper has no package dependencies. The collection and consuming folder need no local Node/Python environment, `node_modules`, virtual environment or background service to use these assets. GitHub downloads its action runtimes on the runner. Template files can live in a synced folder; Git metadata still follows the setup skill's synchronized-storage rule. Maintainers can test the helper with an existing Node 22+ runtime using `node --test setup-project-workflows/tests/test-github-lifecycle.cjs`.

## Issue-centered tracking and PR links
Issues own discussion, tracking, progress and acceptance; PRs are discrete review/integration points. Use issue board cards and issue-only views by default, showing [Linked pull requests](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-pull-request-fields). PR cards require an explicit project exception. Keep partial PRs linked without closing unfinished acceptance; merging one of several contributions is not evidence that the issue is done.

Choose a link strategy against the actual saved [repository auto-close setting](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-auto-closing-issues). GitHub's formal [Development/closing links](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) can close issues when merged into the default branch. If partial contributions use those links, disabling repository auto-close is a setup choice requiring the actual owner's authorization; issue completion then needs an explicit acceptance/close step. Alternatively, use descriptive references such as `Refs #123` for partial work and keep direct PR links visible on the issue. Descriptive references are not a guarantee of display in the Linked pull requests field. Reserve closing links for authorized completion and verify the selected repository behavior rather than assuming keywords override its policy. Merely selecting/creating a local contribution branch does not require a formal GitHub Development link.

Native project rules are independent: a PR-linked rule can move the issue to Active, and a merged-PR rule can move it to Done even without PR cards. Inspect their actual targets/conditions and reconcile competing transitions under the approved setup. Preserve Blocked/terminal intent and unfinished acceptance. No template installation authorizes changing repository settings, native workflows or existing cards.

## Guide credentials only for selected forge setup
Template content can be adapted without service access. When the user actually selects GitHub-side setup, use the selected provider setup skill or guide the human through the required settings; do not broaden a local setup into account configuration. An agent's existing GitHub login is not the workflow runner's credential.

Follow [GitHub's Projects automation guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions). The repository `GITHUB_TOKEN` cannot access Projects. GitHub recommends an App for organization projects and a personal access token for user projects. An App needs organization Projects read/write permission and access to the selected repository's issues; issue-write permission is needed for the optional reopen operation. Install it only for the intended scope. Store its client ID as variable `PW_APP_CLIENT_ID` and its private key as secret `PW_APP_PRIVATE_KEY`, then select `PW_AUTH_METHOD=app`. Alternatively, select `token` and store the approved token as secret `PW_PROJECT_TOKEN`; the documented classic-token route uses `project` and `repo` scopes and must satisfy the owner's policy.

Use repository/organization Settings to create those secrets and variables, following the selected provider's supported setup or a human handoff. Never request credentials in chat or commit them to a template, profile or workflow configuration. The workflow selects only the chosen authentication method; it does not fall back to a different stored identity. App authentication creates a short-lived installation token even for a preview; the helper's dry run performs no issue/project mutations.

## Configure the actual board
Have the selected tooling or human resolve the actual project, field and option IDs. Keep those nonsecret values in repository/organization variables; never import example-board IDs. The starter verifies that the named single-select field and configured options belong to the selected project before planning changes.

| Variable | Meaning/default |
| --- | --- |
| `PW_PROJECT_ID`, `PW_STATUS_FIELD_ID` | Selected existing project and single-select field; required for automation. |
| `PW_STATUS_FIELD_NAME` | Actual field name; defaults to `Status`. |
| `PW_ENTRY_OPTION_ID`, `PW_DONE_OPTION_ID` | New-item entry and completed-close stage; required. |
| `PW_REOPEN_OPTION_ID` | Explicit reopen destination; defaults to entry. |
| `PW_TERMINAL_OPTION_IDS` | Comma-separated additional terminal IDs; Done is always terminal. |
| `PW_BLOCKED_LABEL` | Exact blocking label; empty disables label blocking. |
| `PW_DEPENDENCY_BLOCKING` | `true` enables dependency blocking; default `false`. |
| `PW_BLOCKED_OPTION_ID`, `PW_READY_OPTION_ID` | Required when either blocker signal is selected. |
| `PW_REOPEN_CLOSED_ISSUES` | Board-driven reopening; default `false`. |
| `PW_FRESH_CLOSE_SECONDS` | Positive fresh-close interval; starts at 600 seconds. Preserve an existing guard. |
| `PW_MAX_CHANGES` | Maximum planned item changes per run; starts at 20. |
| `PW_NATIVE_SETTINGS_VERIFIED` | Human attestation of the recorded actual native configuration; default `false`. |
| `PW_AUTOMATION_ENABLED` | Enable automatic runs/live writes only after the reviewed setup; default `false`. |

The supplied schedule is fifteen minutes; deliberately adapt it if the selected profile uses another cadence. Advertise lag. This starter handles issues in the current repository and one existing project; other repositories' cards, PRs and draft items are left alone. Existing stage names/order, field/view provisioning and native configuration are setup work, not capabilities implemented by this runtime.

Preserve the workflow's serialized `queue: max` configuration. [GitHub's concurrency queue](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) retains up to 100 pending runs; the default single-pending queue can replace required issue events. A full queue or a failed/canceled run still needs inspection and repair: scheduled reconciliation cannot reconstruct every missed issue event. Before selecting board-driven reopening, account for monitoring and recovery of those runs; keep reopening disabled when that operating expectation is unsuitable.

## Verify before enabling writes
The template owns new-issue entry, completed-close and explicit-reopen synchronization, selected blocked signals and optional scheduled reopening. It never listens to generic issue edits. New-issue reruns preserve an already assigned status; deliberate terminal statuses are preserved. Cancellation/other close reasons are left for project-specific classification and are not automatically reopened.

Retain one writer per direction. Inspect actual native settings using [GitHub's native workflow procedure](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations). Keep the selected board-to-issue close behavior and remove only overlapping issue-to-board writers, or adapt this template to preserve a different chosen authority. Include linked/merged-PR rules when they write issue status; preserve unrelated PR behavior. Record who checked the real close-triggering status, conditions and saved/enabled state; an API enabled flag is insufficient. `PW_NATIVE_SETTINGS_VERIFIED` records that human check, not an API proof or permanent guarantee against drift.

Publish the selected files only within the project's actual publication authorization, leaving automatic writes disabled. Run the manual workflow with `dry_run=true` and inspect its reconciliation proposals, warnings and access/field checks. Manual dispatch does not simulate new-issue, close, explicit-reopen or label-clear events. The helper reads all project pages before applying changes, refuses incomplete label coverage, and checks fresh issue and card state before a write. Revisit the baseline if the change limit is exceeded. Enable the two verification/automation variables only after the user accepts the plan and actual native settings. Live transition tests need their own bounded targets and scope; no example board is a test target by default. Check event queueing and both issue/card results in that hosted QA. A verified scheduled reopen proves issue state; its resulting explicit-reopen run applies and verifies the configured card destination.

Preserve the fresh-close guard, independent blocker handling and deliberate no-auto-unblock. Missing/invalid close times hold reopening; a cleared label cannot clear an active dependency. These reads and writes are not a remote transaction. A failed or denied readback can leave a partial/uncertain result: inspect the Actions log and current state, then make a new dry run rather than blindly rerunning a failed write. The helper sends no automatic mutation retries. Review failed close-sync runs before relying on scheduled reopening.

Offline tests exercise the actual helper with a synthetic GitHub client. They do not establish real App/PAT access, GitHub-hosted execution, native settings or live transition success. Keep those checks visible in the selected project's setup record.
