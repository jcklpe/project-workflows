#!/usr/bin/env python3
"""Check agent-policy structure or preview/update only its generated index table."""
import argparse
import datetime
import heapq
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    yaml = None  # Optional PyYAML; an existing Ruby/Psych can parse the same data safely.

sys.dont_write_bytecode = True
INDEX = "policy.index.md"
START = "<!-- agent-policies:start -->"
END = "<!-- agent-policies:end -->"
ID = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)+")
FIELDS = {"id", "type", "scope", "status", "authority", "revised", "depends_on", "related_to"}
REQUIRED = FIELDS - {"related_to"}


class Invalid(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def read(path):
    require(not path.is_symlink(), f"Symlink requires manual reconciliation: {path.name}")
    return path.read_bytes() if path.exists() else None


def line(value, field, path, empty=False):
    require(isinstance(value, str) and (empty or bool(value.strip())), f"{path.name}: {field} must be a {'possibly empty ' if empty else ''}string")
    require(not any(ord(c) < 32 or c == '|' for c in value), f"{path.name}: {field} must be one plain line without table separators")


def load_yaml(text):
    if yaml is not None:
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as error:
            raise Invalid(f"Invalid YAML header: {error}") from error
    ruby = shutil.which("ruby")
    require(ruby, "Optional checks need existing PyYAML or Ruby/Psych. No parser is available; use the documented manual graph/link checks without installing an environment.")
    program = "require 'yaml'; require 'json'; require 'date'; data = YAML.safe_load(STDIN.read, permitted_classes: [Date], permitted_symbols: [], aliases: false); STDOUT.write(JSON.generate(data))"
    result = subprocess.run([ruby, "-e", program], input=text, capture_output=True, text=True)
    detail = result.stderr.splitlines()[0] if result.stderr else "YAML parser failed"
    require(result.returncode == 0, "Invalid YAML header: " + detail)
    return json.loads(result.stdout)


def parse(path, raw):
    text = raw.decode("utf-8").replace("\r\n", "\n")
    lines = text.splitlines(keepends=True)
    require(lines and lines[0].rstrip("\r\n") == "---", f"{path.name}: expected a --- YAML header")
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"), None)
    require(end is not None, f"{path.name}: missing closing YAML frontmatter delimiter")
    data = load_yaml("".join(lines[1:end]))
    require(isinstance(data, dict), f"{path.name}: YAML header must be a mapping")
    if isinstance(data.get("revised"), datetime.date):
        data["revised"] = data["revised"].isoformat()
    body = "".join(lines[end + 1:])
    require(REQUIRED <= data.keys(), f"{path.name}: missing fields: {', '.join(sorted(REQUIRED - data.keys()))}")
    require(not data.keys() - FIELDS, f"{path.name}: unsupported fields: {', '.join(sorted(data.keys() - FIELDS))}")
    for field in ("id", "type", "scope", "status", "authority", "revised"):
        line(data[field], field, path, empty=field == "authority")
    require(ID.fullmatch(data["id"]), f"{path.name}: invalid mnemonic ID")
    prefix = "_" if data["type"] == "kernel" else ""
    require(re.fullmatch(re.escape(prefix + data["id"]) + r"-[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.md", path.name), f"{path.name}: filename must use its type prefix, ID and a lowercase imperative slug")
    require(data["status"] in {"proposed", "adopted", "retired"}, f"{path.name}: invalid status")
    require(data["status"] == "proposed" or data["authority"].strip(), f"{path.name}: adopted/retired status needs a recorded human decision authority")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["revised"]), f"{path.name}: revised must be a YYYY-MM-DD date")
    datetime.date.fromisoformat(data["revised"])
    for field in ("depends_on", "related_to"):
        values = data.setdefault(field, [])
        require(isinstance(values, list) and all(isinstance(v, str) and ID.fullmatch(v) for v in values), f"{path.name}: {field} must be an array of mnemonic IDs")
        require(len(set(values)) == len(values), f"{path.name}: duplicate {field} entries")
        require(data["id"] not in values, f"{path.name}: self-reference in {field}")
    titles = re.findall(r"^# (.+)$", body, re.M)
    require(len(titles) == 1, f"{path.name}: expected exactly one level-one imperative title")
    line(titles[0], "title", path)
    data.update(path=path, body=body, title=titles[0])
    return data


def collect(directory):
    require(directory.is_dir(), "--policies must name the actual existing project policy directory")
    require(not any(p.is_symlink() for p in (directory, *directory.parents)), "Policy directory must not be a symlink into a mutable package; reconcile it explicitly")
    records, snapshots = {}, {}
    for path in sorted(directory.iterdir()):
        require(not path.is_dir(), f"Nested policy directories are unsupported: {path.name}")
        if path.suffix != ".md" or path.name == INDEX:
            continue
        raw = read(path)
        require(raw is not None, f"Policy disappeared during preparation: {path.name}")
        item = parse(path, raw)
        require(item["id"] not in records, f"Duplicate ID: {item['id']}")
        records[item["id"]] = item
        snapshots[path] = raw
    return records, snapshots


def cycle_path(records):
    active, done, stack = set(), set(), []

    def visit(key):
        if key in active:
            return stack[stack.index(key):] + [key]
        if key in done:
            return None
        active.add(key)
        stack.append(key)
        for parent in sorted(records[key]["depends_on"]):
            found = visit(parent)
            if found:
                return found
        stack.pop()
        active.remove(key)
        done.add(key)
        return None

    for key in sorted(records):
        found = visit(key)
        if found:
            return found
    return None


def order(records, roots=()):
    for key, item in records.items():
        for field in ("depends_on", "related_to"):
            for parent in item[field]:
                require(parent in records, f"{key}: missing {field} target {parent}")
        if item["status"] == "adopted":
            for parent in item["depends_on"]:
                require(records[parent]["status"] == "adopted", f"{key}: inactive prerequisite {parent} ({records[parent]['status']})")
    cycle = cycle_path(records)
    require(not cycle, "Dependency cycle requires repair: " + " -> ".join(cycle or []))
    selected = set()

    def include(key):
        require(key in records, f"Unknown requested root: {key}")
        require(records[key]["status"] == "adopted", f"Requested root is inactive: {key}")
        if key in selected:
            return
        selected.add(key)
        for parent in records[key]["depends_on"]:
            include(parent)

    for key in roots or sorted(k for k, v in records.items() if v["status"] == "adopted"):
        include(key)
    degree = {k: len(records[k]["depends_on"]) for k in selected}
    ready = [k for k in selected if not degree[k]]
    heapq.heapify(ready)
    result = []
    while ready:
        key = heapq.heappop(ready)
        result.append(key)
        for dependent in sorted(selected):
            if key in records[dependent]["depends_on"]:
                degree[dependent] -= 1
                if degree[dependent] == 0:
                    heapq.heappush(ready, dependent)
    return result


def anchors(text):
    result = set(re.findall(r"<(?:a|h[1-6])\b[^>]*(?:id|name)=[\"']([^\"']+)[\"']", text, re.I))
    seen = {}
    text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M | re.S)
    for title in re.findall(r"^#{1,6} (.+?)\s*#*$", text, re.M):
        key = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        number = seen.get(key, 0)
        result.add(key + (f"-{number}" if number else ""))
        seen[key] = number + 1
    return result


def links(path, body):
    # The supported policy format uses ordinary inline Markdown links, not reference links or embedded HTML.
    text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", body, flags=re.M | re.S)
    require(not re.search(r"(?<!!)\[[^\]]+\]\[[^\]]*\]|^\[[^\]]+\]:", text, re.M), f"{path.name}: use inline Markdown links for checkable references")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        url = urlsplit(target)
        if url.scheme in {"http", "https", "mailto"}:
            continue
        require(not url.scheme and not url.netloc and not url.query and not url.path.startswith("/"), f"{path.name}: use relative local links or https/http/mailto references: {target}")
        dest = path.parent / unquote(url.path) if url.path else path
        require(dest.exists(), f"{path.name}: missing link {target}")
        if url.fragment:
            require(dest.is_file() and unquote(url.fragment) in anchors(dest.read_text()), f"{path.name}: missing link anchor {target}")


def table(records):
    rows = [START, "| ID | Policy | Type | Scope | Status | Revised |", "| --- | --- | --- | --- | --- | --- |"]
    for key, item in sorted(records.items(), key=lambda pair: (pair[1]["type"] != "kernel", pair[0])):
        rows.append(f"| {key} | [{item['title']}]({item['path'].name}) | {item['type']} | {item['scope']} | {item['status']} | {item['revised']} |")
    return "\n".join([*rows, END])


def render_index(raw, records):
    generated = table(records)
    if raw is None:
        return "# Agent policy index\nOnly explicitly adopted policies govern agents in this checkout. Human governance remains separate.\n\n" + generated + "\n"
    text = raw.decode("utf-8")
    require(text.count(START) == text.count(END) == 1 and text.index(START) < text.index(END), f"{INDEX}: exactly one ordered generated-table marker pair is required; preserve and reconcile existing content manually")
    begin, end = text.index(START), text.index(END) + len(END)
    return text[:begin] + generated + text[end:]


def run(directory, operation="check", roots=(), write=False):
    directory = Path(directory).absolute()
    records, snapshots = collect(directory)
    loading = order(records, roots)
    for item in records.values():
        links(item["path"], item["body"])
    path = directory / INDEX
    before = read(path)
    content = render_index(before, records)
    links(path, content)
    changed = before != content.encode("utf-8")
    if operation == "check":
        require(not changed, f"{INDEX}: missing or stale generated table; preview the index operation")
    elif write and changed:
        snapshots[path] = before
        expected_files = set(snapshots) - {path}

        def unchanged():
            current = set(directory.glob("*.md")) - {path}
            require(current == expected_files and not any(p.is_dir() for p in directory.iterdir()), "Policy inventory changed during index preparation; nothing written")
            for name, expected in snapshots.items():
                require(read(name) == expected, f"Selected file changed during index preparation: {name.name}; nothing written")

        # Recheck the selected records/index immediately before replacing only the generated table; this is not a filesystem transaction or lock.
        unchanged()
        descriptor, name = tempfile.mkstemp(dir=directory, prefix=".policy-index-")
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content.encode("utf-8"))
                handle.flush()
            if path.exists():
                os.chmod(temporary, path.stat().st_mode & 0o777)
            unchanged()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    result = {"valid": True, "operation": operation, "changed": changed if operation == "index" else False,
              "written": operation == "index" and write and changed, "policy_count": len(records),
              "load_order": loading, "load_files": [records[key]["path"].name for key in loading],
              "limits": "Structural checks only; human intent, substantive consistency and agent/tool compliance are not proved."}
    if operation == "index" and not write:
        result["content"] = content
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="operation", required=True)
    for operation in ("check", "index"):
        sub = subs.add_parser(operation)
        sub.add_argument("--policies", required=True, help="Explicit actual project agent-policy directory, never inferred from the installed skill")
        if operation == "check":
            sub.add_argument("--root", action="append", default=[], help="Select an adopted policy and its prerequisite closure; repeat for multiple roots")
        else:
            sub.add_argument("--write", action="store_true", help="Update only the generated index table after review; no policy edits, adoption, Git or network operations")
    args = parser.parse_args()
    try:
        result = run(args.policies, args.operation, getattr(args, "root", ()), getattr(args, "write", False))
    except (Invalid, OSError, ValueError, UnicodeError, RecursionError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)], "load_order": []}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
