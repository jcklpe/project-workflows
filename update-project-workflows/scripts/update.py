#!/usr/bin/env python3
"""Preview or apply a bounded adoption merge; standard library and Git only."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

try:
    import tomllib
except ImportError:
    sys.exit("Optional updater requires an existing Python 3.11+ interpreter; use the skill's manual Git route otherwise.")

sys.dont_write_bytecode = True
RECEIPT = ".project-workflows-assets.json"  # Legacy consumer storage only.
ASSETS_START = "# project-workflows-assets:start"
ASSETS_END = "# project-workflows-assets:end"
STARTERS = {
    ".github/ISSUE_TEMPLATE/contribution.md": "setup-project-workflows/assets/templates/github/ISSUE_TEMPLATE/contribution.md.template",
    ".github/PULL_REQUEST_TEMPLATE.md": "setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template",
    ".github/workflows/project-lifecycle.yml": "setup-project-workflows/assets/templates/github/project-lifecycle.yml.template",
    ".github/project-workflows/lifecycle.cjs": "setup-project-workflows/assets/templates/github/lifecycle.cjs",
}


class Stop(Exception):
    pass


def git(root, *args, allowed=(0,)):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_MERGE_AUTOEDIT="no", GIT_LITERAL_PATHSPECS="1")
    if args[0] == "check-ignore":
        env.pop("GIT_LITERAL_PATHSPECS", None)
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, env=env)
    if result.returncode not in allowed:
        raise Stop(f"git {args[0]} failed: {result.stderr.decode(errors='replace').strip()}")
    return result


def out(root, *args):
    return git(root, *args).stdout.decode().strip()


def revision(root, ref):
    return out(root, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")


def local_path(root, name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or any(ord(c) < 32 or c == "\\" for c in name) or any(p in ("..", ".git") for p in path.parts) or str(path) != name:
        raise Stop(f"Unsafe relative path: {name}")
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise Stop(f"Symlink requires manual reconciliation: {name}")
    return current


def blob(root, tree, path):
    row = out(root, "ls-tree", tree, "--", path)
    if not row or row.split()[0] not in ("100644", "100755"):
        raise Stop(f"Missing or non-file source at {tree}: {path}")
    return git(root, "show", f"{tree}:{path}").stdout


def config(root, tree):
    return validate_tables(tomllib.loads(blob(root, tree, "workflow.toml").decode()))


def validate_tables(settings):
    for name in ("project", "adoption", "documents", "coordination", "workflows", "assets", "references"):
        if name in settings and not isinstance(settings[name], dict):
            raise Stop(f"{name} must be a TOML table")
    return settings


def preserve_settings(before, after, prefix=""):
    for key, value in before.items():
        name = f"{prefix}.{key}" if prefix else key
        if key not in after:
            raise Stop(f"Project setting removed: {name}")
        if isinstance(value, dict) and isinstance(after[key], dict):
            preserve_settings(value, after[key], name)
        elif value != after[key]:
            raise Stop(f"Project setting changed: {name}; reconcile this setting explicitly")


def workflow_notes(parent, settings):
    notes = settings.get("workflows", {})
    if not isinstance(notes, dict):
        raise Stop("workflows must be a table mapping skill names to local note paths")
    for name, value in notes.items():
        if not isinstance(value, str):
            raise Stop(f"Local workflow note must be a relative path: {name}")
        path = local_path(parent, value)
        if value == "project-workflows" or value.startswith("project-workflows/"):
            raise Stop(f"Local workflow notes must belong to the parent project: {name}")
        if not path.is_file():
            raise Stop(f"Required local workflow note is missing: {value}")
    return notes


def shared_config(child, tree):
    settings = config(child, tree)
    project = settings.get("project", {})
    adoption_settings = settings.get("adoption", {})
    if project.get("name") or settings.get("workflows") or any(adoption_settings.values()):
        raise Stop("Shared mode requires neutral package configuration; preserve the localized child and use a separately reviewed migration")
    return settings


def snapshot(parent, names):
    state = {}
    staged = set(out(parent, "diff", "--cached", "--name-only").splitlines())
    for name in names:
        if name in staged:
            raise Stop(f"Selected parent path is staged: {name}")
        path = local_path(parent, name)
        if git(parent, "check-ignore", "-q", "--", name, allowed=(0, 1)).returncode == 0:
            raise Stop(f"Selected asset path is ignored: {name}")
        if path.exists() and not path.is_file():
            raise Stop(f"Expected a file: {name}")
        state[name] = path.read_bytes() if path.exists() else None
    return state


def adoption(project, config_name=None):
    parent = Path(project).resolve()
    if Path(out(parent, "rev-parse", "--show-toplevel")).resolve() != parent:
        raise Stop("--project must name the actual parent Git root")
    row = out(parent, "ls-files", "--stage", "--", "project-workflows")
    if not row.startswith("160000 ") or row.split()[2] != "0":
        raise Stop("Expected an initialized root project-workflows gitlink; use the exceptional/manual route")
    child = local_path(parent, "project-workflows")
    if Path(out(child, "rev-parse", "--show-toplevel")).resolve() != child:
        raise Stop("Workflow submodule is not initialized")
    if out(parent, "diff", "--cached", "--name-only", "--", "project-workflows"):
        raise Stop("Parent workflow pin is staged; preserve it and reconcile explicitly")
    if out(child, "status", "--porcelain", "--untracked-files=all"):
        raise Stop("Workflow child is dirty; checkpoint or reconcile its owned work first")
    for name in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if Path(out(child, "rev-parse", "--path-format=absolute", "--git-path", name)).exists():
            raise Stop("Workflow child has an operation in progress")
    head = revision(child, "HEAD")
    branch = git(child, "symbolic-ref", "--quiet", "--short", "HEAD", allowed=(0, 1)).stdout.decode().strip()
    if config_name:
        selected_config = local_path(parent, config_name)
        if not selected_config.is_file():
            raise Stop(f"Declared project configuration is missing: {config_name}")
        external = config_name
    else:
        candidates = [name for name in ("docs/project-workflows.toml", "_meta/project-workflows.toml", "project-workflows.toml", "docs/workflow.toml", "_meta/workflow.toml", "workflow.toml") if local_path(parent, name).exists()]
        if len(candidates) > 1:
            raise Stop("Multiple project configurations exist; select the AGENTS-declared path with --config")
        external = candidates[0] if candidates else None
    if external:
        selected_config = local_path(parent, external)
        settings = validate_tables(tomllib.loads(selected_config.read_text()))
        if type(settings.get("schema_version")) is not int or settings["schema_version"] != 1:
            raise Stop("Project workflow configuration requires schema_version = 1")
        if settings.get("adoption", {}).get("mode") != "shared" or settings["adoption"].get("project_branch"):
            raise Stop('Project pinned configuration requires adoption.mode = "shared" and no project_branch; reconcile an existing adoption explicitly')
        relative_root = settings.get("project", {}).get("root")
        if not isinstance(relative_root, str) or not relative_root or Path(relative_root).is_absolute() or (selected_config.parent / relative_root).resolve() != parent:
            raise Stop("Project workflow configuration project.root must resolve from its directory to the selected parent")
        shared_config(child, head)
        if branch:
            raise Stop("Shared mode requires a detached shared pin; preserve existing branches and select the intended layout explicitly")
    else:
        settings = config(child, head)
        expected = settings.get("adoption", {}).get("project_branch")
        if not expected or branch != expected:
            raise Stop("Select the declared project branch first; canonical/global-only sources use the manual route")
        if (child / settings.get("project", {}).get("root", "..")).resolve() != parent:
            raise Stop("workflow.toml does not resolve to the selected parent")
    workflow_notes(parent, settings)
    return parent, child, head, settings, external


def receipt(parent, settings=None, external=None):
    path = local_path(parent, RECEIPT)
    if external:
        if path.exists():
            raise Stop("Legacy asset manifest exists; preview migrate-assets before updating this shared consumer")
        data = {"schema_version": 1, "files": dict(settings.get("assets", {}))}
    else:
        data = json.loads(path.read_text()) if path.exists() else {"schema_version": 1, "files": {}}
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), dict):
        raise Stop("Unsupported asset baseline file")
    for dest, entry in data["files"].items():
        if not isinstance(entry, dict) or set(entry) != {"source", "revision"}:
            raise Stop(f"Asset baseline requires source and revision only: {dest}")
        local_path(parent, dest)
        if dest in (RECEIPT, "project-workflows") or dest.startswith("project-workflows/"):
            raise Stop("An installed asset must belong to the parent")
        local_path(parent, entry["source"])
        commit = entry["revision"]
        if not isinstance(commit, str) or len(commit) not in (40, 64) or any(c not in "0123456789abcdef" for c in commit):
            raise Stop("Asset baseline requires an exact source commit")
    return data


def encode_baselines(parent, data, external):
    if not external:
        return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    # Replace only the managed section; retain all other settings, comments and formatting.
    text = local_path(parent, external).read_bytes().decode()
    original = tomllib.loads(text)
    lines = text.splitlines(keepends=True)
    starts = [position for position, line in enumerate(lines) if line.strip() == ASSETS_START]
    ends = [position for position, line in enumerate(lines) if line.strip() == ASSETS_END]
    block = ASSETS_START + "\n"
    for dest, entry in sorted(data["files"].items()):
        block += f"[assets.{json.dumps(dest)}]\n"
        block += f"source = {json.dumps(entry['source'])}\nrevision = {json.dumps(entry['revision'])}\n\n"
    block += ASSETS_END + "\n"
    if starts or ends:
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
            raise Stop("Malformed asset-section markers; reconcile the selected TOML manually")
        encoded = "".join(lines[:starts[0]]) + block + "".join(lines[ends[0] + 1:])
    else:
        if "assets" in original:
            raise Stop("Existing assets table has no managed markers; reconcile it manually")
        encoded = text + ("" if text.endswith("\n") else "\n") + "\n" + block
    after = tomllib.loads(encoded)
    if after.pop("assets", {}) != data["files"]:
        raise Stop("Rendered asset baselines differ from the selected records")
    original.pop("assets", None)
    if original != after:
        raise Stop("Asset section would alter other project settings; reconcile its boundaries")
    return encoded.encode()


def migrate_assets(args):
    parent, child, head, settings, external = adoption(args.project, args.config)
    if not external:
        raise Stop("Asset consolidation requires an existing parent-owned shared configuration")
    before = snapshot(parent, [RECEIPT, *project_state_paths(settings, external)])
    if before[RECEIPT] is None:
        receipt(parent, settings, external)
        return {"operation": "migrate-assets", "configuration": external, "changed": False, "applied": args.apply}
    data = receipt(parent)
    existing = settings.get("assets", {})
    if existing and existing != data["files"]:
        raise Stop("TOML and legacy asset baselines disagree; reconcile before migration")
    for dest, entry in data["files"].items():
        guard_project_asset(dest, entry["source"], settings, external)
        blob(child, revision(child, entry["revision"]), entry["source"])
        if not local_path(parent, dest).is_file():
            raise Stop(f"Installed destination is missing: {dest}")
    encoded = encode_baselines(parent, data, external)
    if args.apply:
        adoption(args.project, args.config)
        if snapshot(parent, before) != before or revision(child, "HEAD") != head:
            raise Stop("State changed after migration preview")
        local_path(parent, external).write_bytes(encoded)
        local_path(parent, RECEIPT).unlink()
    return {"operation": "migrate-assets", "configuration": external, "files": sorted(data["files"]),
            "changed": True, "applied": args.apply, "staged": False}


def changed(root, base, tip):
    return set(git(root, "diff", "--name-only", "-z", base, tip).stdout.decode().strip("\0").split("\0")) - {""}


def merge_copy(local, base, incoming, name):
    if local == base:
        return incoming
    if incoming == base or local == incoming:
        return local
    if any(b"\0" in value for value in (local, base, incoming)):
        raise Stop(f"Edited binary asset requires manual reconciliation: {name}")
    with tempfile.TemporaryDirectory(prefix="pw-asset-") as temp:
        paths = [Path(temp) / n for n in ("local", "base", "incoming")]
        for path, data in zip(paths, (local, base, incoming)):
            path.write_bytes(data)
        result = subprocess.run(["git", "merge-file", "-p", *map(str, paths)], capture_output=True)
        if result.returncode:
            raise Stop(f"Copied asset conflict; nothing applied: {name}")
        return result.stdout


def guard_policy_asset(dest, source, settings):
    policy_root = settings.get("documents", {}).get("agent_policies", "docs/agent-policies")
    if not isinstance(policy_root, str) or not policy_root:
        raise Stop("Invalid agent policy directory; reconcile configuration explicitly")
    policy_root = str(PurePosixPath(policy_root))
    if (PurePosixPath(dest).name == "policy.index.md" or dest == policy_root or dest.startswith(policy_root + "/")
            or dest.startswith("docs/agent-policies/") or source.startswith("adopt-agent-policies/assets/kernel/")):
        raise Stop(f"Agent policy copies require explicit adoption, not automatic asset refresh: {dest}")


def guard_project_asset(dest, source, settings, external):
    guard_policy_asset(dest, source, settings)
    if (external and dest == external) or dest in settings.get("workflows", {}).values():
        raise Stop(f"Project configuration and local workflow notes are not automatically refreshed assets: {dest}")


def project_state_paths(settings, external):
    return ([external] if external else []) + list(settings.get("workflows", {}).values())


def record(args):
    parent, child, head, settings, external = adoption(args.project, args.config)
    source_revision = revision(child, args.revision)
    data = receipt(parent, settings, external)
    baseline_path = external or RECEIPT
    before = snapshot(parent, [baseline_path, *project_state_paths(settings, external)])
    for dest, entry in data["files"].items():
        guard_project_asset(dest, entry["source"], settings, external)
    for mapping in args.asset:
        dest, sep, source = mapping.partition("=")
        if not sep:
            raise Stop("--asset uses DESTINATION=SOURCE")
        local_path(parent, source)
        guard_project_asset(dest, source, settings, external)
        target = local_path(parent, dest)
        if dest == RECEIPT or dest == "project-workflows" or dest.startswith("project-workflows/"):
            raise Stop("An installed asset must belong to the parent")
        if not target.is_file():
            raise Stop(f"Installed destination is missing: {dest}")
        snapshot(parent, [dest])
        blob(child, source_revision, source)
        entry = {"source": source, "revision": source_revision}
        if dest in data["files"] and data["files"][dest] != entry:
            raise Stop(f"Baseline already exists; do not replace its history: {dest}")
        data["files"][dest] = entry
    encoded = encode_baselines(parent, data, external)
    if args.apply and before[baseline_path] != encoded:
        adoption(args.project, args.config)
        if snapshot(parent, before) != before or revision(child, "HEAD") != head:
            raise Stop("State changed after baseline preview")
        local_path(parent, baseline_path).write_bytes(encoded)
    return {"operation": "record-assets", "applied": args.apply, "changed": before[baseline_path] != encoded,
            "baseline": source_revision, "files": sorted(data["files"]), "staged": False}


def update(args):
    parent, child, head, settings, external = adoption(args.project, args.config)
    if args.fetch:
        git(child, "fetch", "--", args.fetch)
    target = revision(child, args.revision)
    bases = out(child, "merge-base", "--all", head, target).splitlines()
    if len(bases) != 1:
        raise Stop("Missing or ambiguous ancestry; reconcile history explicitly")
    base = bases[0]
    if external and base != head:
        raise Stop("Shared mode requires forward shared ancestry; preserve divergent or newer work and reconcile explicitly")
    if base == target:
        tree, mode = out(child, "rev-parse", head + "^{tree}"), "unchanged"
    elif base == head:
        tree, mode = out(child, "rev-parse", target + "^{tree}"), "fast-forward"
    else:
        preview = git(child, "merge-tree", "--write-tree", "--name-only", head, target, allowed=(0, 1))
        if preview.returncode:
            raise Stop("Textual merge conflict; nothing applied: " + preview.stdout.decode().split("\n\n")[0].partition("\n")[2].strip())
        tree, mode = preview.stdout.decode().splitlines()[0], "merge"
    if external:
        shared_config(child, tree)
    else:
        preserve_settings(settings, config(child, tree))
    effective_settings = settings if external else config(child, tree)
    workflow_notes(parent, effective_settings)
    git(child, "diff", "--check", head, tree)
    overlaps = changed(child, base, head) & changed(child, base, target) - {"workflow.toml"}
    review = {p for p in overlaps if out(child, "ls-tree", head, "--", p) != out(child, "ls-tree", target, "--", p)}
    data = receipt(parent, settings, external)
    baseline_path = external or RECEIPT
    for dest, entry in data["files"].items():
        guard_project_asset(dest, entry["source"], effective_settings, external)
    for dest in STARTERS:
        if local_path(parent, dest).exists() and dest not in data["files"]:
            raise Stop(f"Installed starter has no recorded baseline: {dest}; use record-assets with its actual installed revision")
    before = snapshot(parent, [baseline_path, *data["files"], *project_state_paths(effective_settings, external)])
    writes, advanced = {}, []
    for dest, entry in data["files"].items():
        source = entry["source"]
        old = blob(child, revision(child, entry["revision"]), source)
        new = blob(child, tree, source)
        local = before[dest]
        if local is None:
            raise Stop(f"Installed asset is missing; reconcile deliberate deletion: {dest}")
        if old != new:
            merged = merge_copy(local, old, new, dest)
            if local != old and local != new:
                review.add(dest)
            if local != merged:
                writes[dest] = merged
            advanced.append(dest)
    if advanced:
        encode_baselines(parent, data, external)  # Validate managed boundaries before advancing the child.
    pending = sorted(review - set(args.reviewed))
    summary = {"operation": "update", "mode": mode, "old": head, "accepted": target,
               "branch": None if external else settings["adoption"]["project_branch"], "review_required": pending,
               "configuration": external if external else "project-workflows/workflow.toml",
               "source_mode": "shared" if external else "adaptation", "local_workflows": effective_settings.get("workflows", {}),
               "assets_changed": sorted(writes), "baselines_advanced": advanced,
               "parent_pin": {"recorded": out(parent, "rev-parse", "HEAD:project-workflows"), "staged": False},
               "merge_message": args.message if mode == "merge" else None,
               "merge_message_required": mode == "merge" and not args.message,
               "applied": False}
    if not args.apply or pending or summary["merge_message_required"]:
        summary["blocked"] = bool(pending) or bool(args.apply and summary["merge_message_required"])
        return summary
    # Recheck selected state immediately before mutation. No stash, reset or implicit staging.
    adoption(args.project, args.config)
    if revision(child, "HEAD") != head or snapshot(parent, before) != before:
        raise Stop("Selected state changed after preview; nothing applied")
    if mode != "unchanged":
        if external:
            git(child, "checkout", "--detach", target)
        else:
            message = ["-m", args.message] if mode == "merge" else []
            git(child, "-c", "merge.autoStash=false", "merge", "--no-edit", "--no-autostash", "--ff", *message, target)
    result = revision(child, "HEAD")
    if out(child, "rev-parse", "HEAD^{tree}") != tree:
        raise Stop("Merge result differs from preview; inspect before continuing, no asset writes attempted")
    git(child, "merge-base", "--is-ancestor", target, result)
    if external:
        shared_config(child, result)
    else:
        preserve_settings(settings, config(child, result))
    if snapshot(parent, before) != before:
        raise Stop("Parent project files changed during update; child advanced but assets were left alone")
    for dest in advanced:
        data["files"][dest]["revision"] = result
    if advanced:
        writes[baseline_path] = encode_baselines(parent, data, external)
    # These are local, unstaged writes, not a cross-repository transaction. Failures are never retried.
    for dest, content in writes.items():
        local_path(parent, dest).write_bytes(content)
    summary.update(applied=True, result=result, changed=mode != "unchanged" or bool(writes))
    summary["parent_pin"]["working"] = result
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    for name in ("update", "record-assets", "migrate-assets"):
        sub = commands.add_parser(name)
        sub.add_argument("--project", required=True, help="Explicit parent repository root")
        sub.add_argument("--config", help="Project-relative config path declared by AGENTS; otherwise select one docs/, _meta/ or root project-workflows.toml (legacy workflow.toml also supported)")
        sub.add_argument("--revision", required=name != "migrate-assets", help="Accepted upstream revision, or actual installed asset baseline")
        sub.add_argument("--apply", action="store_true", help="Apply the previewed local scope; never push or stage parent files")
        if name == "update":
            sub.add_argument("--fetch", metavar="REMOTE", help="Fetch selected remote before resolving revision")
            sub.add_argument("--reviewed", action="append", default=[], metavar="PATH", help="Specific customized overlap the agent has reviewed")
            sub.add_argument("--message", help="Reviewed merge commit message, including any required spike trailer; required for a divergent apply")
        elif name == "record-assets":
            sub.add_argument("--asset", action="append", required=True, metavar="DEST=SOURCE")
    args = parser.parse_args()
    try:
        result = {"update": update, "record-assets": record, "migrate-assets": migrate_assets}[args.operation](args)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if result.get("blocked") else 0
    except (Stop, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error), "complete": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
