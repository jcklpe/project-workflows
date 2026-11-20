#!/usr/bin/env python3
"""Preview or advance an unchanged-source consumer pin and its copied assets."""
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


def validate_tables(settings):
    for name in ("project", "adoption", "documents", "coordination", "workflows", "assets", "references"):
        if name in settings and not isinstance(settings[name], dict):
            raise Stop(f"{name} must be a TOML table")
    documents = settings.get("documents", {})
    if "policies" in documents or str(documents.get("agent_policies", "")).rstrip("/") == "docs/policies":
        raise Stop("Use documents.agent_policies and docs/agent-policies; the old policy location is unsupported")
    return settings


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


def check_source_layout(child, tree):
    for filename in ("workflow.toml", "project-workflows.toml"):
        if out(child, "ls-tree", tree, "--", filename):
            raise Stop("Accepted source must not contain runtime project configuration; example.workflow.md is documentation only")


def snapshot(parent, names):
    state = {}
    staged = {os.fsdecode(name) for name in git(parent, "diff", "--cached", "--name-only", "-z").stdout.split(b"\0") if name}
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
        if PurePosixPath(config_name).name != "project-workflows.toml":
            raise Stop("Select a project-workflows.toml file in the project's documentation folder")
        external = config_name
    else:
        candidates = [name for name in ("docs/project-workflows.toml", "_meta/project-workflows.toml") if local_path(parent, name).exists()]
        if len(candidates) != 1:
            raise Stop("Select exactly one project-workflows.toml with --config; no package-config fallback is supported")
        external = candidates[0]
    if len(PurePosixPath(external).parts) < 2 or external.startswith("project-workflows/"):
        raise Stop("Project configuration belongs in the parent's documentation folder")
    selected_config = local_path(parent, external)
    if not selected_config.is_file():
        raise Stop(f"Declared project configuration is missing: {external}")
    settings = validate_tables(tomllib.loads(selected_config.read_text()))
    if type(settings.get("schema_version")) is not int or settings["schema_version"] != 1:
        raise Stop("Project workflow configuration requires schema_version = 1")
    if settings.get("adoption", {}).get("mode") != "shared" or "project_branch" in settings["adoption"]:
        raise Stop('Pinned configuration requires adoption.mode = "shared" without project_branch')
    relative_root = settings.get("project", {}).get("root")
    if not isinstance(relative_root, str) or not relative_root or Path(relative_root).is_absolute() or (selected_config.parent / relative_root).resolve() != parent:
        raise Stop("Project workflow configuration project.root must resolve from its directory to the selected parent")
    if branch:
        raise Stop("Shared mode requires a detached shared pin; named branches are unsupported for consumers")
    if local_path(parent, ".project-workflows-assets.json").exists():
        raise Stop("Remove the obsolete JSON manifest after explicitly transferring verified baselines into the shared TOML")
    workflow_notes(parent, settings)
    return parent, child, head, settings, external


def receipt(parent, settings):
    data = {"schema_version": 1, "files": dict(settings.get("assets", {}))}
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), dict):
        raise Stop("Unsupported asset baseline file")
    for dest, entry in data["files"].items():
        if not isinstance(entry, dict) or set(entry) != {"source", "revision"}:
            raise Stop(f"Asset baseline requires source and revision only: {dest}")
        local_path(parent, dest)
        if dest == "project-workflows" or dest.startswith("project-workflows/"):
            raise Stop("An installed asset must belong to the parent")
        local_path(parent, entry["source"])
        commit = entry["revision"]
        if not isinstance(commit, str) or len(commit) not in (40, 64) or any(c not in "0123456789abcdef" for c in commit):
            raise Stop("Asset baseline requires an exact source commit")
    return data


def encode_baselines(parent, data, external):
    # Replace only the managed section; retain all other settings, comments and formatting.
    text = local_path(parent, external).read_bytes().decode()
    original = tomllib.loads(text)
    lines = text.splitlines(keepends=True)
    starts = [position for position, line in enumerate(lines) if line.strip() == ASSETS_START]
    ends = [position for position, line in enumerate(lines) if line.strip() == ASSETS_END]
    block = ASSETS_START + "\n"
    for dest, entry in sorted(data["files"].items()):
        block += f"[assets.{json.dumps(dest, ensure_ascii=False)}]\n"
        block += f"source = {json.dumps(entry['source'], ensure_ascii=False)}\nrevision = {json.dumps(entry['revision'])}\n\n"
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
    return [external] + list(settings.get("workflows", {}).values())


def record(args):
    parent, child, head, settings, external = adoption(args.project, args.config)
    source_revision = revision(child, args.revision)
    data = receipt(parent, settings)
    baseline_path = external
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
        if dest == "project-workflows" or dest.startswith("project-workflows/"):
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
    if git(child, "merge-base", "--is-ancestor", head, target, allowed=(0, 1)).returncode:
        raise Stop("Shared mode requires forward shared ancestry; preserve divergent or newer work")
    tree = out(child, "rev-parse", target + "^{tree}")
    mode = "unchanged" if head == target else "fast-forward"
    check_source_layout(child, tree)
    workflow_notes(parent, settings)
    git(child, "diff", "--check", head, tree)
    review = set()
    data = receipt(parent, settings)
    baseline_path = external
    for dest, entry in data["files"].items():
        guard_project_asset(dest, entry["source"], settings, external)
    for dest in STARTERS:
        if local_path(parent, dest).exists() and dest not in data["files"]:
            raise Stop(f"Installed starter has no recorded baseline: {dest}; use record-assets with its actual installed revision")
    before = snapshot(parent, [baseline_path, *data["files"], *project_state_paths(settings, external)])
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
               "branch": None, "review_required": pending,
               "configuration": external,
               "source_mode": "shared", "local_workflows": settings.get("workflows", {}),
               "assets_changed": sorted(writes), "baselines_advanced": advanced,
               "parent_pin": {"recorded": out(parent, "rev-parse", "HEAD:project-workflows"), "staged": False},
               "applied": False}
    if not args.apply or pending:
        summary["blocked"] = bool(pending)
        return summary
    # Recheck selected state immediately before mutation. No stash, reset or implicit staging.
    adoption(args.project, args.config)
    if revision(child, "HEAD") != head or snapshot(parent, before) != before:
        raise Stop("Selected state changed after preview; nothing applied")
    if mode != "unchanged":
        git(child, "checkout", "--detach", target)
    result = revision(child, "HEAD")
    if out(child, "rev-parse", "HEAD^{tree}") != tree:
        raise Stop("Merge result differs from preview; inspect before continuing, no asset writes attempted")
    git(child, "merge-base", "--is-ancestor", target, result)
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
    for name in ("update", "record-assets"):
        sub = commands.add_parser(name)
        sub.add_argument("--project", required=True, help="Explicit parent repository root")
        sub.add_argument("--config", help="Project-relative project-workflows.toml in the declared documentation folder")
        sub.add_argument("--revision", required=True, help="Accepted upstream revision, or actual installed asset baseline")
        sub.add_argument("--apply", action="store_true", help="Apply the previewed local scope; never push or stage parent files")
        if name == "update":
            sub.add_argument("--fetch", metavar="REMOTE", help="Fetch selected remote before resolving revision")
            sub.add_argument("--reviewed", action="append", default=[], metavar="PATH", help="Specific customized overlap the agent has reviewed")
        elif name == "record-assets":
            sub.add_argument("--asset", action="append", required=True, metavar="DEST=SOURCE")
    args = parser.parse_args()
    try:
        result = {"update": update, "record-assets": record}[args.operation](args)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if result.get("blocked") else 0
    except (Stop, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error), "complete": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
