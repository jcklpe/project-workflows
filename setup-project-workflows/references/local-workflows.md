# Local workflow notes
Use a local note when a project has an actual procedural difference, relevant context or concrete QA instructions for a shared skill. First check whether the difference is still useful. Obsolete instructions should be retired under their owner's authority rather than copied into a new extension merely because they existed.

## Location and discovery
Keep notes in the project, outside the shared collection. `docs/workflows/` is a useful default when the project has no existing convention; custom folders and directly declared local guidance remain valid. The selected root or legacy configuration can map a skill name to its note in `[workflows]`. The project's AGENTS identifies that configuration. Agents read the note for the current skill and applicable policy prerequisites before applying the shared procedure.

## Format
Use ordinary Markdown with one descriptive title. State the shared skill and when the note applies, then the concrete local procedure. Link relevant standing policy owners when the steps rely on them, and include meaningful checks or human QA where needed. Name any common step being supplemented, replaced or omitted so an agent can compare the instructions. A short note can express these in a few paragraphs; headings and the [starter template](../assets/templates/local-workflow.md.template) are optional aids, not a schema. Preserve the project's existing frontmatter convention; no new YAML fields, status system or executable hook is required.

Keep actual decisions distinguishable from experiments or proposals. A local note does not silently adopt policy changes, expand action permission or settle a contradiction between adopted obligations. Project-owned policies govern the procedure. When a policy explicitly delegates a note/data contract to a named local skill, follow that bounded declaration rather than inferring independent authority for every skill.

## Review and update
Check the actual local need, the selected skill, scope, policy links, changed steps and acceptance evidence. If an upstream improvement makes the variation unnecessary, propose its retirement rather than treating divergence as permanent. Updates preserve local note bytes; the agent still reviews relevant upstream behavior against the note because file preservation does not prove semantic compatibility.

The proposed distribution amendment to [ADOPT-POLICIES](../../adopt-agent-policies/assets/kernel/_ADOPT-POLICIES-require-explicit-adoption.md) records this authority boundary. It remains candidate source; it does not change a project's adopted kernel copy without that project's actual adoption decision.
