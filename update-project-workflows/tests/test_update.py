"""Offline integration tests against real temporary repositories, not a mocked Git."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update.py"
SOURCE = "setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template"
DEST = ".github/PULL_REQUEST_TEMPLATE.md"
RECEIPT = ".project-workflows-assets.json"
TEMPLATE = "Heading\n\nfirst paragraph\n\nmiddle paragraph\n\nlast paragraph\n"


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pw-update-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / "upstream"
        self.parent = self.root / "project"
        self.child = self.parent / "project-workflows"
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        for root in (self.upstream, self.parent):
            root.mkdir()
            self.git(root, "init", "--template=", "-b", "main")
            self.identity(root)
        self.write(self.upstream, "workflow.toml", '[project]\nname = ""\nroot = ".."\n[adoption]\nproject_branch = ""\n[coordination]\nmode = "local"\n')
        self.write(self.upstream, "example/SKILL.md", "Heading\n\nshared first\n\nmiddle\n\nshared last\n")
        self.write(self.upstream, SOURCE, TEMPLATE)
        self.base = self.commit(self.upstream, "initial shared source")
        self.write(self.parent, "README.md", "project\n")
        self.commit(self.parent, "parent baseline")
        self.git(self.parent, "-c", "protocol.file.allow=always", "submodule", "add", str(self.upstream), "project-workflows")
        self.identity(self.child)
        self.git(self.child, "switch", "-c", "project/example")
        self.write(self.child, "workflow.toml", '[project]\nname = "Example"\nroot = ".."\n[adoption]\nproject_branch = "project/example"\n[coordination]\nmode = "local"\n')
        self.local = self.commit(self.child, "project settings")
        self.commit(self.parent, "adopt workflows")

    def git(self, root, *args):
        result = subprocess.run(["git", "-C", str(root), *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def identity(self, root):
        self.git(root, "config", "user.email", "fixture@example.invalid")
        self.git(root, "config", "user.name", "Fixture")

    def write(self, root, name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, root, message):
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", message)
        return self.git(root, "rev-parse", "HEAD")

    def incoming(self, name="new.md", text="new shared procedure\n"):
        self.write(self.upstream, name, text)
        revision = self.commit(self.upstream, "upstream improvement")
        self.git(self.child, "fetch", "origin")
        return revision

    def run_helper(self, operation="update", revision="origin/main", *options, code=0):
        message = ["--message", "Merge accepted Project Workflows\n\nSpike: fixture-update"] if operation == "update" and "--apply" in options else []
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), operation, "--project", str(self.parent), "--revision", revision, *message, *options], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout if result.stdout else result.stderr)

    def install(self):
        self.write(self.parent, DEST, TEMPLATE)
        self.run_helper("record-assets", self.base, "--asset", f"{DEST}={SOURCE}", "--apply")
        self.commit(self.parent, "install copied template with actual baseline")

    def shared(self):
        self.git(self.child, "checkout", "--detach", self.base)
        self.write(self.parent, "workflow.toml", 'schema_version = 1\n[project]\nname = "Example"\nroot = "."\n[documents]\nactive_spikes = "work-notes/active"\nagent_policies = "rules/agents"\n[adoption]\nmode = "shared"\n[coordination]\nmode = "local"\n[workflows]\nexample = "work-notes/workflows/example.md"\n')
        self.write(self.parent, "work-notes/workflows/example.md", "Keep this project's local review examples.\n")
        self.write(self.parent, "rules/agents/READ-SAFE.md", "Existing adopted project rule.\n")
        self.commit(self.parent, "select unchanged shared source and project-owned context")

    def test_config_only_merge_preserves_history_and_unrelated_parent_state(self):
        self.write(self.parent, "unrelated.txt", "staged\n")
        self.git(self.parent, "add", "unrelated.txt")
        self.write(self.parent, "README.md", "unrelated dirty\n")
        index = self.git(self.parent, "ls-files", "--stage")
        accepted = self.incoming()
        plan = self.run_helper()
        self.assertEqual(plan["mode"], "merge")
        self.assertEqual(plan["review_required"], [])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)
        result = self.run_helper("update", accepted, "--apply")
        self.assertTrue(result["changed"])
        self.assertIn('name = "Example"', (self.child / "workflow.toml").read_text())
        for original in (self.local, accepted):
            self.git(self.child, "merge-base", "--is-ancestor", original, "HEAD")
        self.assertEqual(index, self.git(self.parent, "ls-files", "--stage"))
        self.assertEqual((self.parent / "README.md").read_text(), "unrelated dirty\n")
        self.assertEqual(self.git(self.child, "status", "--porcelain"), "")
        repeated = self.run_helper("update", accepted, "--apply")
        self.assertFalse(repeated["changed"])
        self.assertEqual(repeated["result"], result["result"])
        self.git(self.parent, "commit", "-m", "record workflow pin", "--", "project-workflows")
        self.assertEqual(self.git(self.parent, "rev-parse", "HEAD:project-workflows"), result["result"])
        self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])
        self.assertEqual(self.git(self.child, "log", "-1", "--format=%(trailers:key=Spike,valueonly)"), "fixture-update")

    def test_fast_forward(self):
        self.git(self.upstream, "fetch", str(self.child), "project/example")
        self.git(self.upstream, "merge", "--ff-only", "FETCH_HEAD")
        accepted = self.incoming()
        result = self.run_helper("update", accepted, "--apply")
        self.assertEqual(result["mode"], "fast-forward")
        self.assertEqual(result["result"], accepted)

    def test_customized_overlap_requires_focused_review_even_for_clean_merge(self):
        self.write(self.child, "example/SKILL.md", "Heading\n\nlocal first\n\nmiddle\n\nshared last\n")
        local = self.commit(self.child, "project procedure")
        accepted = self.incoming("example/SKILL.md", "Heading\n\nshared first\n\nmiddle\n\nnew shared last\n")
        result = self.run_helper("update", accepted, "--apply", code=2)
        self.assertEqual(result["review_required"], ["example/SKILL.md"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), local)
        self.run_helper("update", accepted, "--reviewed", "example/SKILL.md", "--apply")
        text = (self.child / "example/SKILL.md").read_text()
        self.assertIn("local first", text)
        self.assertIn("new shared last", text)

    def test_textual_conflict_is_previewed_without_worktree_or_index_changes(self):
        self.write(self.child, "example/SKILL.md", "local replacement\n")
        local = self.commit(self.child, "conflicting local procedure")
        index = self.git(self.child, "ls-files", "--stage")
        accepted = self.incoming("example/SKILL.md", "upstream replacement\n")
        result = self.run_helper("update", accepted, "--apply", code=1)
        self.assertIn("Textual merge conflict", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), local)
        self.assertEqual(self.git(self.child, "ls-files", "--stage"), index)
        self.assertEqual(self.git(self.child, "status", "--porcelain"), "")

    def test_unchanged_copy_updates_and_repeat_is_noop(self):
        self.install()
        accepted = self.incoming(SOURCE, TEMPLATE.replace("last paragraph", "new last paragraph"))
        result = self.run_helper("update", accepted, "--apply")
        self.assertEqual(result["assets_changed"], [DEST])
        self.assertIn("new last paragraph", (self.parent / DEST).read_text())
        self.assertEqual(json.loads((self.parent / RECEIPT).read_text())["files"][DEST]["revision"], result["result"])
        index = self.git(self.parent, "ls-files", "--stage")
        self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])
        self.assertEqual(index, self.git(self.parent, "ls-files", "--stage"))

    def test_edited_copy_uses_three_way_merge_and_review(self):
        self.install()
        self.write(self.parent, DEST, TEMPLATE.replace("first paragraph", "project first paragraph"))
        accepted = self.incoming(SOURCE, TEMPLATE.replace("last paragraph", "new last paragraph"))
        self.run_helper("update", accepted, "--apply", code=2)
        result = self.run_helper("update", accepted, "--reviewed", DEST, "--apply")
        self.assertIn("project first paragraph", (self.parent / DEST).read_text())
        self.assertIn("new last paragraph", (self.parent / DEST).read_text())
        self.assertTrue(result["changed"])

    def test_asset_conflict_blocks_collection_merge_too(self):
        self.install()
        self.write(self.parent, DEST, "local replacement\n")
        accepted = self.incoming(SOURCE, "upstream replacement\n")
        before = (self.parent / RECEIPT).read_bytes()
        result = self.run_helper("update", accepted, "--apply", code=1)
        self.assertIn("Copied asset conflict", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)
        self.assertEqual((self.parent / DEST).read_text(), "local replacement\n")
        self.assertEqual((self.parent / RECEIPT).read_bytes(), before)

    def test_missing_baseline_is_not_guessed(self):
        self.write(self.parent, DEST, TEMPLATE)
        self.incoming()
        result = self.run_helper("update", "origin/main", "--apply", code=1)
        self.assertIn("no recorded baseline", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)

    def test_dirty_child_and_staged_selected_parent_paths_are_preserved(self):
        self.write(self.child, "new.txt", "unfinished\n")
        self.assertIn("dirty", self.run_helper(code=1)["error"])
        (self.child / "new.txt").unlink()
        self.install()
        self.write(self.parent, DEST, "staged copy\n")
        self.git(self.parent, "add", DEST)
        index = self.git(self.parent, "ls-files", "--stage")
        self.assertIn("staged", self.run_helper(code=1)["error"])
        self.assertEqual(index, self.git(self.parent, "ls-files", "--stage"))

    def test_setting_change_requires_explicit_reconciliation(self):
        accepted = self.incoming("workflow.toml", '[project]\nname = ""\nroot = ".."\n[adoption]\nproject_branch = ""\n[coordination]\nmode = "forge"\n')
        self.assertIn("Project setting changed", self.run_helper("update", accepted, "--apply", code=1)["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)

    def test_symlink_and_traversal_baselines_are_rejected(self):
        self.install()
        (self.parent / DEST).unlink()
        outside = self.root / "outside.md"
        outside.write_text("preserve\n")
        (self.parent / DEST).symlink_to(outside)
        self.assertIn("Symlink", self.run_helper(code=1)["error"])
        self.assertEqual(outside.read_text(), "preserve\n")
        (self.parent / DEST).unlink()
        self.write(self.parent, DEST, TEMPLATE)
        data = json.loads((self.parent / RECEIPT).read_text())
        data["files"]["../outside.md"] = data["files"].pop(DEST)
        (self.parent / RECEIPT).write_text(json.dumps(data))
        self.assertIn("Unsafe", self.run_helper(code=1)["error"])

    def test_failed_fetch_stops_without_merge(self):
        result = self.run_helper("update", "origin/main", "--fetch", "missing-remote", "--apply", code=1)
        self.assertIn("fetch failed", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)

    def test_new_config_keys_are_merged_without_rewriting_project_values(self):
        incoming = (self.upstream / "workflow.toml").read_text() + '[new_section]\nfeature = "available"\n'
        accepted = self.incoming("workflow.toml", incoming)
        self.run_helper("update", accepted, "--apply")
        text = (self.child / "workflow.toml").read_text()
        self.assertIn('name = "Example"', text)
        self.assertIn('feature = "available"', text)

    def test_unchanged_source_preserves_edited_copy_and_baseline(self):
        self.install()
        self.write(self.parent, DEST, "project-specific template\n")
        baseline = (self.parent / RECEIPT).read_bytes()
        accepted = self.incoming()
        result = self.run_helper("update", accepted, "--apply")
        self.assertEqual(result["assets_changed"], [])
        self.assertEqual((self.parent / DEST).read_text(), "project-specific template\n")
        self.assertEqual((self.parent / RECEIPT).read_bytes(), baseline)

    def test_baseline_preview_and_repeat_are_nonmutating(self):
        self.write(self.parent, DEST, TEMPLATE)
        mapping = f"{DEST}={SOURCE}"
        self.run_helper("record-assets", self.base, "--asset", mapping)
        self.assertFalse((self.parent / RECEIPT).exists())
        self.run_helper("record-assets", self.base, "--asset", mapping, "--apply")
        self.assertFalse(self.run_helper("record-assets", self.base, "--asset", mapping, "--apply")["changed"])

    def test_merge_requires_an_explicit_reviewed_message(self):
        self.incoming()
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "update", "--project", str(self.parent), "--revision", "origin/main", "--apply"], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(json.loads(result.stdout)["merge_message_required"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)

    def test_staged_pin_and_in_progress_merge_are_rejected(self):
        self.write(self.child, "local.md", "project-specific\n")
        self.commit(self.child, "project-only change")
        self.git(self.parent, "add", "project-workflows")
        self.assertIn("pin is staged", self.run_helper(code=1)["error"])
        self.git(self.parent, "commit", "-m", "record local pin", "--", "project-workflows")
        merge_head = Path(self.git(self.child, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD"))
        merge_head.write_text(self.base + "\n")
        self.assertIn("operation in progress", self.run_helper(code=1)["error"])

    def test_ignored_baseline_file_is_not_created(self):
        self.write(self.parent, ".gitignore", RECEIPT + "\n")
        self.write(self.parent, DEST, TEMPLATE)
        result = self.run_helper("record-assets", self.base, "--asset", f"{DEST}={SOURCE}", "--apply", code=1)
        self.assertIn("ignored", result["error"])
        self.assertFalse((self.parent / RECEIPT).exists())

    def test_mutable_baseline_ref_is_not_accepted_as_installed_provenance(self):
        self.install()
        data = json.loads((self.parent / RECEIPT).read_text())
        data["files"][DEST]["revision"] = "origin/main"
        (self.parent / RECEIPT).write_text(json.dumps(data))
        self.assertIn("exact source commit", self.run_helper(code=1)["error"])


    def test_agent_policy_destinations_cannot_be_registered_for_auto_refresh(self):
        for dest in ("docs/agent-policies/EDIT-SAFE-preserve-edits.md", "other/policy.index.md"):
            with self.subTest(dest=dest):
                self.write(self.parent, dest, TEMPLATE)
                result = self.run_helper("record-assets", self.base, "--asset", f"{dest}={SOURCE}", "--apply", code=1)
                self.assertIn("explicit adoption", result["error"])
                self.assertFalse((self.parent / RECEIPT).exists())

    def test_kernel_source_cannot_be_registered_under_an_arbitrary_destination(self):
        source = "adopt-agent-policies/assets/kernel/_ADOPT-POLICIES-require-explicit-adoption.md"
        accepted = self.incoming(source, "New kernel candidate.\n")
        self.write(self.parent, "rules.md", "Existing adopted rule.\n")
        result = self.run_helper("record-assets", accepted, "--asset", f"rules.md={source}", "--apply", code=1)
        self.assertIn("explicit adoption", result["error"])
        self.assertFalse((self.parent / RECEIPT).exists())

    def test_existing_policy_receipt_blocks_before_collection_merge(self):
        self.write(self.child, "workflow.toml", (self.child / "workflow.toml").read_text() + '[documents]\nagent_policies = "rules/agents"\n')
        local = self.commit(self.child, "select existing policy location")
        self.commit(self.parent, "record selected location")
        dest = "rules/agents/EDIT-SAFE-preserve-edits.md"
        self.write(self.parent, dest, "Existing adopted rule.\n")
        data = {"schema_version": 1, "files": {dest: {"source": SOURCE, "revision": self.base}}}
        self.write(self.parent, RECEIPT, json.dumps(data))
        baseline = (self.parent / RECEIPT).read_bytes()
        accepted = self.incoming()
        result = self.run_helper("update", accepted, "--reviewed", dest, "--apply", code=1)
        self.assertIn("explicit adoption", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), local)
        self.assertEqual((self.parent / dest).read_text(), "Existing adopted rule.\n")
        self.assertEqual((self.parent / RECEIPT).read_bytes(), baseline)

    def test_package_kernel_update_preserves_frozen_project_policy_and_repeat(self):
        dest = "docs/agent-policies/ADOPT-POLICIES-require-explicit-adoption.md"
        self.write(self.parent, dest, "Existing explicitly adopted project obligation.\n")
        body = (self.parent / dest).read_bytes()
        accepted = self.incoming("adopt-agent-policies/assets/kernel/_ADOPT-POLICIES-require-explicit-adoption.md", "New proposed kernel source.\n")
        result = self.run_helper("update", accepted, "--apply")
        self.assertTrue(result["changed"])
        self.assertEqual((self.parent / dest).read_bytes(), body)
        self.assertEqual(result["assets_changed"], [])
        self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])
        self.assertEqual((self.parent / dest).read_bytes(), body)

    def test_shared_update_uses_exact_source_and_preserves_parent_context_and_refs(self):
        self.shared()
        protected = {p: (self.parent / p).read_bytes() for p in ("workflow.toml", "work-notes/workflows/example.md", "rules/agents/READ-SAFE.md")}
        self.write(self.parent, "unrelated.txt", "staged unrelated work\n")
        self.git(self.parent, "add", "unrelated.txt")
        self.write(self.parent, "README.md", "unfinished parent work\n")
        index = self.git(self.parent, "ls-files", "--stage")
        refs = self.git(self.child, "show-ref", "--heads")
        accepted = self.incoming("example/SKILL.md", "Improved shared procedure.\n")
        plan = self.run_helper("update", accepted)
        self.assertEqual(plan["source_mode"], "shared")
        self.assertEqual(plan["configuration"], "workflow.toml")
        self.assertEqual(plan["local_workflows"], {"example": "work-notes/workflows/example.md"})
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)
        result = self.run_helper("update", accepted, "--apply")
        self.assertEqual(result["result"], accepted)
        self.assertIsNone(result["branch"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD^{tree}"), self.git(self.upstream, "rev-parse", accepted + "^{tree}"))
        self.assertEqual(self.git(self.child, "show-ref", "--heads"), refs)
        self.assertEqual(self.git(self.parent, "ls-files", "--stage"), index)
        self.assertEqual(self.git(self.parent, "rev-parse", "HEAD:project-workflows"), self.base)
        self.assertEqual(self.git(self.child, "status", "--porcelain"), "")
        for p, body in protected.items():
            self.assertEqual((self.parent / p).read_bytes(), body)
        self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])
        self.assertEqual(self.git(self.parent, "ls-files", "--stage"), index)

    def test_shared_neutral_default_changes_do_not_replace_project_settings(self):
        self.shared()
        before = (self.parent / "workflow.toml").read_bytes()
        accepted = self.incoming("workflow.toml", (self.upstream / "workflow.toml").read_text().replace('mode = "local"', 'mode = "forge"'))
        self.assertEqual(self.run_helper("update", accepted, "--apply")["result"], accepted)
        self.assertEqual((self.parent / "workflow.toml").read_bytes(), before)

    def test_docs_and_meta_configuration_preserve_exact_source_and_repeat(self):
        self.shared()
        previous = "workflow.toml"
        for selected in ("docs/workflow.toml", "_meta/workflow.toml"):
            with self.subTest(selected=selected):
                content = (self.parent / previous).read_text().replace('root = "."', 'root = ".."')
                self.write(self.parent, selected, content)
                (self.parent / previous).unlink()
                accepted = self.incoming(text=selected + "\n")
                before = (self.parent / selected).read_bytes()
                index = self.git(self.parent, "ls-files", "--stage")
                result = self.run_helper("update", accepted, "--apply")
                self.assertEqual(result["configuration"], selected)
                self.assertEqual(result["result"], accepted)
                self.assertEqual((self.parent / selected).read_bytes(), before)
                self.assertEqual(self.git(self.parent, "ls-files", "--stage"), index)
                self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])
                rejected = self.run_helper("record-assets", self.base, "--config", selected, "--asset", f"{selected}={SOURCE}", "--apply", code=1)
                self.assertIn("not automatically refreshed", rejected["error"])
                previous = selected

    def test_ambiguous_config_requires_explicit_declared_selection(self):
        self.shared()
        content = (self.parent / "workflow.toml").read_text().replace('root = "."', 'root = ".."')
        self.write(self.parent, "docs/workflow.toml", content)
        accepted = self.incoming()
        self.assertIn("Multiple project configurations", self.run_helper("update", accepted, "--apply", code=1)["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)
        result = self.run_helper("update", accepted, "--config", "docs/workflow.toml", "--apply")
        self.assertEqual(result["configuration"], "docs/workflow.toml")

    def test_custom_declared_config_is_bounded_and_resolves_actual_parent(self):
        self.shared()
        original = (self.parent / "workflow.toml").read_text()
        self.write(self.parent, "work-notes/settings/workflow.toml", original.replace('root = "."', 'root = "../.."'))
        for selected, message in [("missing.toml", "missing"), ("../outside.toml", "Unsafe")]:
            self.assertIn(message, self.run_helper("update", self.base, "--config", selected, code=1)["error"])
        self.write(self.parent, "docs/workflow.toml", original)
        self.assertIn("project.root", self.run_helper("update", self.base, "--config", "docs/workflow.toml", code=1)["error"])
        result = self.run_helper("update", self.base, "--config", "work-notes/settings/workflow.toml", "--apply")
        self.assertEqual(result["configuration"], "work-notes/settings/workflow.toml")

    def test_shared_copied_assets_use_existing_baselines_and_repeat(self):
        self.shared()
        self.install()
        self.write(self.parent, DEST, TEMPLATE.replace("first paragraph", "local first paragraph"))
        accepted = self.incoming(SOURCE, TEMPLATE.replace("last paragraph", "new shared last paragraph"))
        self.run_helper("update", accepted, "--apply", code=2)
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)
        result = self.run_helper("update", accepted, "--reviewed", DEST, "--apply")
        self.assertEqual(result["result"], accepted)
        self.assertIn("local first paragraph", (self.parent / DEST).read_text())
        self.assertIn("new shared last paragraph", (self.parent / DEST).read_text())
        self.assertFalse(self.run_helper("update", accepted, "--apply")["changed"])

    def test_root_config_cannot_silently_migrate_an_existing_adaptation(self):
        self.write(self.parent, "workflow.toml", 'schema_version = 1\n[project]\nroot = "."\n[adoption]\nmode = "shared"\n')
        accepted = self.incoming()
        index = self.git(self.child, "ls-files", "--stage")
        result = self.run_helper("update", accepted, "--apply", code=1)
        self.assertIn("localized child", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.local)
        self.assertEqual(self.git(self.child, "ls-files", "--stage"), index)
        self.assertEqual(self.git(self.child, "branch", "--show-current"), "project/example")

    def test_shared_divergence_is_refused_without_discarding_local_work(self):
        self.shared()
        self.write(self.child, "example/SKILL.md", "Experiment still owned by this checkout.\n")
        local = self.commit(self.child, "unpublished experiment")
        accepted = self.incoming()
        self.assertIn("forward shared ancestry", self.run_helper("update", accepted, "--apply", code=1)["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), local)

    def test_shared_mode_does_not_switch_or_advance_a_named_branch(self):
        self.shared()
        self.git(self.child, "switch", "-c", "keep-this-branch")
        accepted = self.incoming()
        self.assertIn("detached shared pin", self.run_helper("update", accepted, "--apply", code=1)["error"])
        self.assertEqual(self.git(self.child, "branch", "--show-current"), "keep-this-branch")
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)

    def test_root_declaration_and_local_note_errors_are_nonmutating(self):
        self.shared()
        original = (self.parent / "workflow.toml").read_text()
        for text, message in [(original.replace('mode = "shared"', 'mode = "adapted"'), "adoption.mode"),
                              (original.replace('root = "."', 'root = ".."'), "project.root"),
                              (original.replace('schema_version = 1', 'schema_version = 2'), "schema_version"),
                              (original.replace('"work-notes/workflows/example.md"', '"../outside.md"'), "Unsafe"),
                              (original.replace('"work-notes/workflows/example.md"', '"missing.md"'), "missing"),
                              (original.replace('"work-notes/workflows/example.md"', '"project-workflows/example/SKILL.md"'), "parent project")]:
            with self.subTest(message=message):
                self.write(self.parent, "workflow.toml", text)
                self.assertIn(message, self.run_helper(code=1)["error"])
                self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)
        self.write(self.parent, "workflow.toml", original)
        note = self.parent / "work-notes/workflows/example.md"
        note.unlink()
        note.symlink_to(self.parent / "README.md")
        self.assertIn("Symlink", self.run_helper(code=1)["error"])

    def test_project_context_and_root_policy_cannot_be_auto_refreshed(self):
        self.shared()
        for dest, message in [("workflow.toml", "not automatically refreshed"),
                              ("work-notes/workflows/example.md", "not automatically refreshed"),
                              ("rules/agents/READ-SAFE.md", "explicit adoption")]:
            with self.subTest(dest=dest):
                before = (self.parent / dest).read_bytes()
                result = self.run_helper("record-assets", self.base, "--asset", f"{dest}={SOURCE}", "--apply", code=1)
                self.assertIn(message, result["error"])
                self.assertEqual((self.parent / dest).read_bytes(), before)
                self.assertFalse((self.parent / RECEIPT).exists())

    def test_existing_context_receipt_blocks_before_shared_pin_advance(self):
        self.shared()
        accepted = self.incoming()
        for dest in ("workflow.toml", "work-notes/workflows/example.md", "rules/agents/READ-SAFE.md"):
            with self.subTest(dest=dest):
                data = {"schema_version": 1, "files": {dest: {"source": SOURCE, "revision": self.base}}}
                self.write(self.parent, RECEIPT, json.dumps(data))
                body = (self.parent / dest).read_bytes()
                self.run_helper("update", accepted, "--reviewed", dest, "--apply", code=1)
                self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)
                self.assertEqual((self.parent / dest).read_bytes(), body)
                self.assertEqual(json.loads((self.parent / RECEIPT).read_text()), data)

    def test_local_note_drift_after_checkout_stops_assets_and_reports_partial_update(self):
        self.shared()
        self.install()
        accepted = self.incoming(SOURCE, TEMPLATE.replace("last paragraph", "incoming last paragraph"))
        before = (self.parent / RECEIPT).read_bytes()
        note = self.parent / "work-notes/workflows/example.md"
        hook = Path(self.git(self.child, "rev-parse", "--path-format=absolute", "--git-path", "hooks/post-checkout"))
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/bin/sh\nprintf '%s\\n' 'Concurrent local review edit.' > " + shlex.quote(str(note)) + "\n")
        hook.chmod(0o755)
        result = self.run_helper("update", accepted, "--apply", code=1)
        self.assertIn("child advanced but assets were left alone", result["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), accepted)
        self.assertEqual(note.read_text(), "Concurrent local review edit.\n")
        self.assertEqual((self.parent / DEST).read_text(), TEMPLATE)
        self.assertEqual((self.parent / RECEIPT).read_bytes(), before)

    def test_shared_target_cannot_introduce_another_projects_configuration(self):
        self.shared()
        accepted = self.incoming("workflow.toml", (self.upstream / "workflow.toml").read_text().replace('name = ""', 'name = "Another project"'))
        self.assertIn("neutral package configuration", self.run_helper("update", accepted, "--apply", code=1)["error"])
        self.assertEqual(self.git(self.child, "rev-parse", "HEAD"), self.base)

if __name__ == "__main__":
    unittest.main()
