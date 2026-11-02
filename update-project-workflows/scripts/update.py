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
RECEIPT = ".project-workflows-assets.json"
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
    return tomllib.loads(blob(root, tree, "workflow.toml").decode())


def preserve_settings(before, after, prefix=""):
    for key, value in before.items():
        name = f"{prefix}.{key}" if prefix else key
        if key not in after:
            raise Stop(f"Project setting removed: {name}")
        if isinstance(value, dict) and isinstance(after[key], dict):
            preserve_settings(value, after[key], name)
        elif value != after[key]:
            raise Stop(f"Project setting changed: {name}; reconcile this setting explicitly")


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


def adoption(project):
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
    branch = out(child, "symbolic-ref", "--quiet", "--short", "HEAD")
    settings = config(child, head)
    expected = settings.get("adoption", {}).get("project_branch")
    if not expected or branch != expected:
        raise Stop("Select the declared project branch first; canonical/global-only sources use the manual route")
    if (child / settings.get("project", {}).get("root", "..")).resolve() != parent:
        raise Stop("workflow.toml does not resolve to the selected parent")
    return parent, child, head, settings


def receipt(parent):
    path = local_path(parent, RECEIPT)
    data = json.loads(path.read_text()) if path.exists() else {"schema_version": 1, "files": {}}
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), dict):
        raise Stop("Unsupported asset baseline file")
    for dest, entry in data["files"].items():
        local_path(parent, dest)
        if dest in (RECEIPT, "project-workflows") or dest.startswith("project-workflows/"):
            raise Stop("An installed asset must belong to the parent")
        local_path(parent, entry["source"])
        commit = entry["revision"]
        if not isinstance(commit, str) or len(commit) not in (40, 64) or any(c not in "0123456789abcdef" for c in commit):
            raise Stop("Asset baseline requires an exact source commit")
    return data


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


def record(args):
    parent, child, head, _ = adoption(args.project)
    source_revision = revision(child, args.revision)
    data = receipt(parent)
    before = snapshot(parent, [RECEIPT])
    for mapping in args.asset:
        dest, sep, source = mapping.partition("=")
        if not sep:
            raise Stop("--asset uses DESTINATION=SOURCE")
        local_path(parent, source)
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
    encoded = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    if args.apply and before[RECEIPT] != encoded:
        if snapshot(parent, [RECEIPT]) != before or revision(child, "HEAD") != head:
            raise Stop("State changed after baseline preview")
        local_path(parent, RECEIPT).write_bytes(encoded)
    return {"operation": "record-assets", "applied": args.apply, "changed": before[RECEIPT] != encoded,
            "baseline": source_revision, "files": sorted(data["files"]), "staged": False}


def update(args):
    parent, child, head, settings = adoption(args.project)
    if args.fetch:
        git(child, "fetch", "--", args.fetch)
    target = revision(child, args.revision)
    bases = out(child, "merge-base", "--all", head, target).splitlines()
    if len(bases) != 1:
        raise Stop("Missing or ambiguous ancestry; reconcile history explicitly")
    base = bases[0]
    if base == target:
        tree, mode = out(child, "rev-parse", head + "^{tree}"), "unchanged"
    elif base == head:
        tree, mode = out(child, "rev-parse", target + "^{tree}"), "fast-forward"
    else:
        preview = git(child, "merge-tree", "--write-tree", "--name-only", head, target, allowed=(0, 1))
        if preview.returncode:
            raise Stop("Textual merge conflict; nothing applied: " + preview.stdout.decode().split("\n\n")[0].partition("\n")[2].strip())
        tree, mode = preview.stdout.decode().splitlines()[0], "merge"
    preserve_settings(settings, config(child, tree))
    git(child, "diff", "--check", head, tree)
    overlaps = changed(child, base, head) & changed(child, base, target) - {"workflow.toml"}
    review = {p for p in overlaps if out(child, "ls-tree", head, "--", p) != out(child, "ls-tree", target, "--", p)}
    data = receipt(parent)
    for dest in STARTERS:
        if local_path(parent, dest).exists() and dest not in data["files"]:
            raise Stop(f"Installed starter has no recorded baseline: {dest}; use record-assets with its actual installed revision")
    before = snapshot(parent, [RECEIPT, *data["files"]])
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
    pending = sorted(review - set(args.reviewed))
    summary = {"operation": "update", "mode": mode, "old": head, "accepted": target,
               "branch": settings["adoption"]["project_branch"], "review_required": pending,
               "assets_changed": sorted(writes), "baselines_advanced": advanced,
               "parent_pin": {"recorded": out(parent, "rev-parse", "HEAD:project-workflows"), "staged": False},
               "merge_message": args.message if mode == "merge" else None,
               "merge_message_required": mode == "merge" and not args.message,
               "applied": False}
    if not args.apply or pending or summary["merge_message_required"]:
        summary["blocked"] = bool(pending) or bool(args.apply and summary["merge_message_required"])
        return summary
    # Recheck selected state immediately before mutation. No stash, reset or implicit staging.
    adoption(args.project)
    if revision(child, "HEAD") != head or snapshot(parent, before) != before:
        raise Stop("Selected state changed after preview; nothing applied")
    if mode != "unchanged":
        message = ["-m", args.message] if mode == "merge" else []
        git(child, "-c", "merge.autoStash=false", "merge", "--no-edit", "--no-autostash", "--ff", *message, target)
    result = revision(child, "HEAD")
    if out(child, "rev-parse", "HEAD^{tree}") != tree:
        raise Stop("Merge result differs from preview; inspect before continuing, no asset writes attempted")
    git(child, "merge-base", "--is-ancestor", target, result)
    preserve_settings(settings, config(child, result))
    if snapshot(parent, before) != before:
        raise Stop("Parent assets changed during merge; child advanced but assets were left alone")
    for dest in advanced:
        data["files"][dest]["revision"] = result
    if advanced:
        writes[RECEIPT] = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
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
        sub.add_argument("--revision", required=True, help="Accepted upstream revision, or actual installed asset baseline")
        sub.add_argument("--apply", action="store_true", help="Apply the previewed local scope; never push or stage parent files")
        if name == "update":
            sub.add_argument("--fetch", metavar="REMOTE", help="Fetch selected remote before resolving revision")
            sub.add_argument("--reviewed", action="append", default=[], metavar="PATH", help="Specific customized overlap the agent has reviewed")
            sub.add_argument("--message", help="Reviewed merge commit message, including any required spike trailer; required for a divergent apply")
        else:
            sub.add_argument("--asset", action="append", required=True, metavar="DEST=SOURCE")
    args = parser.parse_args()
    try:
        result = update(args) if args.operation == "update" else record(args)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if result.get("blocked") else 0
    except (Stop, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error), "complete": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
