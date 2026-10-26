# Agent Instructions
This repository owns reusable project workflow skills and their templates. An adopting project's actual documents stay in its parent repository. When working on an adopted copy, read the parent instructions and workflow.toml; never infer the current project from a global installation path.

## Maintaining this collection
When the selected task is development of Project Workflows itself, this repository is the project root. Use the skill directories directly, [TODO.md](TODO.md) as the index, and `docs/active-spikes/` for the collection's own concept/task pairs. Add scratch, archive, or policy directories only when there is content. These are ordinary tracked documents, not another repository or a recursive `project-workflows/` submodule.

The neutral `workflow.toml` describes an adopted collection's default consumer location; its `project.root = ".."` must not redirect collection-maintenance documents into a containing checkout. This maintenance rule does not make the global installation the target of unrelated requests. For work in an adopting project, its instructions and configured destinations remain authoritative; its actual project narrative stays outside this collection.

## Changes and verification
Preserve intentional project divergence, complete supporting files, license notices, and source attribution. Keep prose paragraphs on single lines and avoid unrelated reformatting. Read commit-work/SKILL.md before checkpoints. Use scoped pathspec commits, guard new-file additions with ignore checks, never add co-author trailers, and never push. Preserve concurrent work and do not rewrite history without explicit authorization.

Validate changed frontmatter, relative resources, TOML configuration, ignores, and relevant workflow behavior. No runtime or service credentials are required. Do not add tests solely to mirror prose. Keep real private configuration ignored; public branches must not contain private project details, credentials, or personal paths. Templates are inputs to adapt, not instructions to overwrite an existing project.
