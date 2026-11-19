# Example project workflow configuration
This is documentation, not runtime configuration. Put the project-owned configuration in `docs/project-workflows.toml` and declare its path in the project’s AGENTS.md. The root is resolved from that file’s directory. Private reference overrides belong in ignored `docs/project-workflows.local.toml`. Setup must add that filename to the project’s ignore rules.

```toml
schema_version = 1

# Project-owned settings in docs/project-workflows.toml or the existing documentation folder, outside the shared package.
[project]
name = "Example project"
root = ".."

[documents]
readme = "README.md"
instructions = "AGENTS.md"
index = "TODO.md"
# catalog = "docs/docs.index.md" # Optional supporting-document navigation; create only when useful.
active_spikes = "docs/active-spikes"
scratch = "docs/scratch"
archive = "docs/archive"
# Declare the project's actual policy location when selected; do not create empty policy folders.
# agent_policies = "docs/agent-policies"

# The parent gitlink pins the exact shared revision; no project branch is needed.
[adoption]
mode = "shared"
upstream_url = "https://github.com/jcklpe/project-workflows.git"
upstream_branch = "main"

# Optional skill-name = project-relative Markdown path. Add only notes that exist.
[workflows]
# run-project-spike = "docs/workflows/spikes.md"
# capture-for-later = "docs/workflows/capture.md"

[coordination]
mode = "local"
repository = ""
tooling = ""

# Optional shared tool facts; the guide explains their use rather than repeating pins.
# [coordination.tooling_source]
# repository = "https://example.org/workflow-tools"
# revision = "REVIEWED_SOURCE_REVISION"
# skills = ["setup-forge", "use-forge-pull-requests"]
# guide = "docs/forge-tooling.md"

# Optional contributor prefixes, only when the project selects them.
# Work-named and shared branches need no contributor-prefix table.
# [coordination.branch_prefixes]
# contributor = "contributor/"

[validation]
commands = []

# Optional nonprivate lookup paths, relative to this file's directory.
# Put machine-specific values in ignored sibling project-workflows.local.toml under [references].
# A local reference overrides only the same reference key, never shared settings or permissions.
[references]
# context = "project-context.md"
# github_tooling = "/absolute/path/to/external/github-only-bundle"

# The updater records installed copied-asset baselines here in a managed [assets] section.
```

Copied-asset baselines belong in the same shared configuration under a managed `[assets]` section, written by the updater. This example is never read or applied automatically.
