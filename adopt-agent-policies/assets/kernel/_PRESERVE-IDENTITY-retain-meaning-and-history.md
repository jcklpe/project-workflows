---
id: PRESERVE-IDENTITY
type: kernel
scope: "Agent continuity, dependency impact and retirement of policy identities."
status: proposed
authority: ""
revised: "2026-11-02"
depends_on: ["ADOPT-POLICIES"]
related_to: ["RESOLVE-DEPENDENCIES"]
---
# Preserve obligation identity
A mnemonic ID identifies substantially the same obligation over time; it encodes neither authority nor graph position. Keep useful identity continuity rather than assigning unrelated meaning to an old ID. A substantial scope or meaning change may require a new ID or a split. Use a concise imperative filename/title that expresses the obligation. A `type: kernel` policy filename must begin with `_` before its unchanged ID; operational policy filenames are unprefixed. This prefix identifies type for browsing, not authority, priority or graph position.

Identity changes and retirement require review of incoming prerequisites and meaningful references, including skills applying the obligation. A dependent's authority must not transfer to a replacement merely through a renamed file, redirected link or substituted ID. Changes to those obligations remain subject to `ADOPT-POLICIES`.

Retired IDs remain reserved and must never identify a different obligation. Retain an indexed retirement record with the human decision, substantive date and useful rationale/history. Preserve evolution in Git and retirement records instead of active supersedes or override chains. Historical references explain prior meaning without making it operative.

## Policy record metadata
A policy record uses YAML frontmatter between `---` delimiters. It contains these required fields:

| Field | Meaning |
| --- | --- |
| `id` | The stable mnemonic identity of the obligation. |
| `type` | A plain descriptive label. `kernel` describes policy-making, identity and loading rules; `operational` describes obligations governing project work. Type does not confer authority or precedence and is not a closed taxonomy. |
| `scope` | A concise statement of the agent activity and project boundary governed by the policy. |
| `status` | `proposed`, `adopted` or `retired`. Status and recorded metadata do not substitute for the actual human decisions required by ADOPT-POLICIES. |
| `authority` | The actual human decision authorizing adoption or retirement. It may be empty for a proposal. |
| `revised` | The substantive revision date in `YYYY-MM-DD` form. |
| `depends_on` | An array of prerequisite policy IDs, possibly empty, interpreted under RESOLVE-DEPENDENCIES. |

The optional `related_to` field contains an array of related policy IDs. These references do not add prerequisites or confer authority.

Skills provide examples and editing procedures under this contract. Validators check its representation; passing validation does not establish adoption, semantic consistency or agent compliance.
