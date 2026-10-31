# Board and lifecycle setup
Read this only for selected project-board/lifecycle setup. Preserve the project's existing workflow source, adaptations and local/no-forge path. Project Workflows owns lifecycle meaning and optional installed automation assets; the selected platform tooling owns agent-facing service operations. This route does not authorize changing an example board or publishing automation.

## Select the project's profile
Start with the project's maintained decisions and the explicitly selected existing or new board and repository scope. A remote, board URL or installed tool does not select a profile or grant access. Keep the choices in an existing project policy/configuration owner, with a pointer from its agent instructions where useful; no new configuration schema or second task ledger is required.

Settle only the choices needed for the selected setup:

- Stage names, order and meanings, including which item kinds and views use them. A view hiding a stage does not remove it from the lifecycle.
- Entry and active stages, terminal mappings and issue-close behavior, and the destination or preservation rule for reopening. Closed outcomes such as completion and cancellation need their intended mapping; a terminal board stage does not close an agent's spike or accept an entire project.
- Enabled blocked signals: labels, dependencies or other project facts; their precedence, clearing behavior and any return stage. Decide whether closed/terminal items participate in blocked routing.
- The actor responsible for each transition, event-driven versus scheduled behavior, expected cadence/lag and the fresh-close interval. Preserve an adopted guard rather than silently shortening or removing it. For a new setup, agree the interval against expected synchronization latency.

## Configurable starting points
These ordered stage sets were inspected on October 31, 2026. Select and adapt them; their names do not prescribe universal meanings or enable automation.

| Starting point | Ordered stages |
| --- | --- |
| Agentic-wiki team Kanban | Backlog → Upcoming → On Deck → Active → Blocked → Done |
| Open Austin organization Kanban | To Do → On Deck → Blocked → In Progress → Done |

The inspected wiki configuration sends new/reopened issues to Backlog and closed issues to Done. Its blocked label routes to Blocked; label removal routes to On Deck. Dependency removal deliberately does not auto-unblock. Its scheduled reconciliation is every fifteen minutes. Open Austin's maintained policy uses Done for the organization board's close mapping and a five-minute reopen reconciliation schedule; its specialized roles board uses Filled instead. Do not infer other mappings merely from those labels. Both inspected architectures retain a ten-minute fresh-close guard. These are example settings, not a default schedule or proof of live behavior for another project.

Specialized profiles can use different vocabulary and view filters. Preserve intentional project choices rather than replacing them with the nearest example. Copy neither example IDs nor credentials into a generic profile.

Use the editable profile starters and optional repository assets in the [GitHub starter pack](github-starter-pack.md) when GitHub setup is selected. Profiles and issue/PR content need no service credentials to adapt. CI credentials are guided only for the selected forge/automation route.

## Preserve transition ownership and intent
Assign one authoritative actor to each enabled direction and transition. A native board-to-issue closer can coexist with an issue-to-board synchronizer; two writers handling the same issue-to-board transition can compete. Inspect existing native and repository automation, including defaults on newly created/copied projects. Resolve conflicting writers within the approved plan while preserving unrelated workflows, fields, views and items.

Apply entry, terminal and reopen mappings only to the events they own. An unrelated issue edit or label change must not reapply the entry stage, reset progress, or undo a deliberate board move. Explicit lifecycle mappings can move an item as selected by the project; do not broaden those mappings to every issue event.

Retain the fresh-close guard before interpreting a closed issue's nonterminal board status as a reopen request: the close-to-terminal update may still be in flight. Inside the configured interval, leave the issue closed. Afterward, follow the selected reopen policy using fresh observations. Missing close-time evidence, stale reads or uncertain ordering require inspection rather than guessing or reducing the guard. Scheduled execution has lag; record the expected cadence and a manual path when timing matters instead of promising immediate reconciliation.

Track enabled blocked signals independently. Clearing a label does not clear an outstanding dependency, and dependency removal does not clear a blocked label. Apply the chosen return-stage policy only when its conditions are satisfied; retain a project's deliberate no-auto-unblock behavior. A blocked signal alone is not a request to reopen a closed issue. Prevent blocked routing from accidentally creating a nonterminal status that triggers reopening against the project's selected terminal behavior.

## Plan through the selected tooling
Ask the provider owner to resolve identity/targets, inspect the current schema, views and automation coverage, and preview the selected service changes against current state. Request outcomes such as the agreed stage set, preserved views, exact lifecycle mappings and bounded verification. The provider owns agent-facing permission checks, service API operations, readback and recovery. Project Workflows owns the deployable repository automation and its runtime API calls/tests. Keep the provider's operational journal separate from tracked automation assets and project policy.

Read the tooling's current contract. Issue/PR support or a status-move command does not establish board provisioning support. Unsupported setup operations get a concrete manual handoff and pending status; do not invent agent-facing provider commands. Adapt the bundled repository templates for the selected project, preserving existing configuration and reporting which steps are planned, supported, manually required or verified. Execute only within the user's actual target/action scope.

## Manually verify native automation settings
For GitHub, have the human follow [Using the built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations): open the selected project's Workflows menu, edit the relevant default workflow, inspect its configuration, then save/enable the intended settings. Inspect the actual close-triggering status option and any other relevant conditions; an enabled flag alone does not establish that mapping. Check relevant native defaults for competing writers, without disabling unrelated behavior.

Record the selected project, actual native workflow settings and enabled/saved state, who checked them and when, and any remaining gap in the project's existing setup record. A provider read that exposes only workflow identity/enabled metadata does not complete this check. Missing UI access or an unverified setting remains an explicit manual requirement; do not call setup fully verified while it is pending.

## Verify and hand off
Use synthetic or staged scenarios for the plan. Live transitions need separately authorized targets and actions; inspecting example configuration does not exercise its automation. Record actual provider and CI execution/readback evidence separately from a paper walkthrough.

| Scenario | Required check |
| --- | --- |
| Local project or ordinary collaborator onboarding | No board or automation is required or enabled. |
| New item, unrelated edit and deliberate board move | Entry applies only where selected; later progress is not reset by a generic event. |
| Issue closes while its board stage is still nonterminal | The fresh-close interval prevents premature reopening; missing timing evidence does not bypass it. |
| Reopen after the guard interval | Fresh state follows the selected reopen mapping and advertised scheduling lag. |
| Label clears while a dependency remains; dependency clears while a label remains | The other enabled blocker remains effective; clearing one signal does not erase another. |
| Dependency disappears with no remaining label | Follow the selected clearing/return-stage policy, including deliberate no-auto-unblock. |
| Native workflow is enabled but its configured status is unknown | Manual settings verification remains pending. |
| Partial, drifting or uncertain platform result | Preserve evidence and use the provider's recovery route; do not blindly retry. |

Report the selected profile and its owner, preserved differences, supported and manual steps, actual verification and remaining gaps. Board semantics and local template adaptation can be settled while provisioning capabilities remain pending. Keep repository-workflow assets with Project Workflows, agent-facing service implementation with the selected tooling owner, and each agent's tasks in its own spike.
