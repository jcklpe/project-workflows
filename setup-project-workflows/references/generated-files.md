# Generated files and private state
Use this procedure when implementing a tool, choosing an output destination or retiring an installation. Git ignores prevent accidental staging; they do not define storage ownership or retention. Authored `docs/scratch/` notes are project documentation, not runtime scratch space.

Before writing, classify the file and use the owning project's existing conventions:

| Kind | Destination and tracking | Lifetime |
| --- | --- | --- |
| Disposable run files | A newly created owner-only directory from the platform's temporary-directory API, outside source checkouts; never tracked | Remove the tool's own run directory after use. On failure retain only necessary diagnostics, with an explicit short expiry and cleanup owner. OS cleanup is a backstop, not the plan. |
| Reusable verification | Test procedure, expected result and useful synthetic fixture or sanitized readback beside the owning implementation; tracked after review | Maintain with the behavior it verifies. Do not retain routine raw responses or intermediates. |
| Explicitly retained private evidence | An authorized private artifact destination outside a public checkout; never tracked | State what the original proves, who needs it and the deletion condition. Retention is an exception requiring a reason, not the default for every test. |
| Persistent runtime state | A designated private user-state/configuration location outside source checkouts; never tracked | Document purpose, owner, override, recovery behavior and safe removal. Sign-ins, settings, locks and unresolved operation journals are not disposable files. |

Use safe random names, restrictive permissions and cleanup scoped to the directory this run created. Reject unsafe temp overrides instead of falling back into the checkout. Do not recursively sweep a shared temp directory, rely on ignore patterns to protect secrets, or upload raw diagnostics automatically. Record cleanup failures without dumping secret-bearing contents.

Keep each tool's file inventory with its maintained documentation: what it writes, default and configured locations, whether it is tracked, and when it may be removed. Track fake example configuration, never real credentials, browser profiles or account-specific settings. A journal can be sensitive without containing a token: private resource IDs, exact before/after content and action history can reveal private work.

For existing installations, inspect the writer and recovery semantics before classifying files. Preserve unresolved writes until read-only reconciliation establishes their outcome. A stale-looking lock is not proof its writer is dead. Stop or coordinate all writers before migrating state, preserve the complete journal and ownership checks, and switch every consumer together. Do not create two independently writable copies, adopt an ordinary personal browser profile, or expire unresolved receipts to enable a retry. A migration needs a verified source/destination and an explicit recovery plan; documentation changes alone do not migrate state.

When retiring files, distinguish generated intermediates from authored work, retained evidence and required state. Follow the project's deletion-consent rules, itemize uncertain groups and preserve unique content until disposition is established. Removing a working file does not remove it from Git history, backups or remotes; verify those separately when historical removal is in scope.
