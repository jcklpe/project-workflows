"""Exercise policy graphs, real files and the bounded index writer without dependencies."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "policies.py"
spec = importlib.util.spec_from_file_location("policy_tool", SCRIPT)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class PoliciesTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="pw-policy-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.directory = self.root / "agent-policies"
        self.directory.mkdir()

    def policy(self, key="EDIT-SAFE", depends=(), related=(), status="adopted", slug="preserve-scoped-edits", body="Preserve scoped agent edits.\n", **extra):
        data = dict(id=key, scope="Agent edits in this checkout.", status=status,
                    authority="Human fixture adopts the exact obligation." if status != "proposed" else "",
                    revised="2026-11-02", depends_on=list(depends), related_to=list(related))
        data.update(extra)
        path = self.directory / f"{key}-{slug}.md"
        header = "\n".join(f"{k} = {json.dumps(v)}" for k, v in data.items())
        path.write_text(f"+++\n{header}\n+++\n# Preserve scoped edits\n{body}")
        return path

    def index(self):
        return tool.run(self.directory, "index", write=True)

    def invalid(self, message, operation="check", **kwargs):
        with self.assertRaisesRegex(tool.Invalid, message):
            tool.run(self.directory, operation, **kwargs)

    def test_diamond_multi_parent_order_is_deterministic_and_loads_once(self):
        self.policy("TIP-ONE", depends=["RIGHT-ONE", "LEFT-ONE"])
        self.policy("RIGHT-ONE", depends=["BASE-ONE"])
        self.policy("LEFT-ONE", depends=["BASE-ONE"])
        self.policy("BASE-ONE")
        self.policy("SIDE-ONE")
        self.index()
        expected = ["BASE-ONE", "LEFT-ONE", "RIGHT-ONE", "TIP-ONE"]
        for _ in range(3):
            result = tool.run(self.directory, roots=["TIP-ONE", "RIGHT-ONE"])
            self.assertEqual(result["load_order"], expected)
        self.assertEqual(tool.run(self.directory)["load_order"], ["BASE-ONE", "LEFT-ONE", "RIGHT-ONE", "SIDE-ONE", "TIP-ONE"])

    def test_related_cycles_are_references_and_do_not_extend_root_closure(self):
        self.policy("EDIT-SAFE", related=["READ-SAFE"])
        self.policy("READ-SAFE", related=["EDIT-SAFE"])
        self.index()
        self.assertEqual(tool.run(self.directory, roots=["EDIT-SAFE"])["load_order"], ["EDIT-SAFE"])

    def test_dependency_cycle_reports_actual_path_without_writes(self):
        self.policy("EDIT-SAFE", depends=["READ-SAFE"])
        self.policy("READ-SAFE", depends=["TEST-SAFE"])
        self.policy("TEST-SAFE", depends=["EDIT-SAFE"])
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        self.invalid("EDIT-SAFE -> READ-SAFE -> TEST-SAFE -> EDIT-SAFE", "index", write=True)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_proposed_cycle_must_be_repaired_before_adoption(self):
        self.policy("EDIT-SAFE", depends=["READ-SAFE"], status="proposed")
        self.policy("READ-SAFE", depends=["EDIT-SAFE"], status="proposed")
        self.invalid("Dependency cycle")

    def test_missing_prerequisite_is_not_dropped(self):
        self.policy(depends=["READ-SAFE"])
        self.invalid("missing depends_on target READ-SAFE")

    def test_proposed_and_retired_prerequisites_block_adopted_dependent(self):
        self.policy(depends=["READ-SAFE"])
        for status in ("proposed", "retired"):
            with self.subTest(status=status):
                self.policy("READ-SAFE", status=status)
                self.invalid("inactive prerequisite READ-SAFE")

    def test_proposed_dependencies_can_be_staged_without_becoming_operative(self):
        first = self.policy(depends=["READ-SAFE"], status="proposed")
        self.policy("READ-SAFE", status="proposed")
        before = first.read_bytes()
        self.index()
        self.assertEqual(tool.run(self.directory)["load_order"], [])
        self.assertEqual(first.read_bytes(), before)
        self.invalid("Requested root is inactive", roots=["EDIT-SAFE"])

    def test_duplicate_ids_are_rejected_even_with_different_filenames(self):
        self.policy()
        self.policy(slug="keep-safe-edits")
        self.invalid("Duplicate ID: EDIT-SAFE")

    def test_self_dependency_and_missing_related_reference_are_rejected(self):
        self.policy(depends=["EDIT-SAFE"])
        self.invalid("self-reference")
        self.policy(related=["MISSING-REF"])
        self.invalid("missing related_to target MISSING-REF")

    def test_lightweight_header_rejects_invalid_status_authority_dates_and_fields(self):
        for extras, message in [({"status": "active"}, "invalid status"), ({"authority": ""}, "recorded human"),
                                ({"revised": "2026-02-30"}, "day is out of range"), ({"id": "123"}, "invalid mnemonic"),
                                ({"supersedes": "OLD-ID"}, "unsupported fields"), ({"scope": "Agent | human"}, "table separators"),
                                ({"depends_on": ["READ-SAFE", "READ-SAFE"]}, "duplicate depends_on")]:
            with self.subTest(extras=extras):
                self.policy(**extras)
                with self.assertRaisesRegex((tool.Invalid, ValueError), message):
                    tool.run(self.directory)

    def test_filename_identity_and_single_title_are_checked(self):
        path = self.policy()
        renamed = path.with_name("OTHER-ID-preserve-scoped-edits.md")
        path.rename(renamed)
        self.invalid("filename must begin")
        renamed.rename(path)
        path.write_text(path.read_text() + "# Another title\n")
        self.invalid("exactly one level-one")

    def test_index_preview_preserves_prose_and_safe_rerun_is_noop(self):
        self.policy()
        path = self.directory / tool.INDEX
        original = "# Project agent rules\nHuman-owned context.\n\n" + tool.START + "\n" + tool.END + "\n\nKeep this footer.\n"
        path.write_text(original)
        preview = tool.run(self.directory, "index")
        self.assertTrue(preview["changed"])
        self.assertEqual(path.read_text(), original)
        self.assertTrue(self.index()["written"])
        written, mtime = path.read_bytes(), path.stat().st_mtime_ns
        self.assertTrue(written.startswith(b"# Project agent rules\nHuman-owned context."))
        self.assertTrue(written.endswith(b"Keep this footer.\n"))
        self.assertFalse(self.index()["written"])
        self.assertEqual(path.read_bytes(), written)
        self.assertEqual(path.stat().st_mtime_ns, mtime)
        self.assertTrue(tool.run(self.directory)["valid"])

    def test_index_drift_missing_index_and_malformed_markers_require_reconciliation(self):
        path = self.policy()
        self.invalid("missing or stale")
        self.index()
        path.write_text(path.read_text().replace("Agent edits in this checkout.", "Agent document edits only."))
        self.invalid("missing or stale")
        index = self.directory / tool.INDEX
        for text in ["Original unmarked index.\n", tool.START + "\n" + tool.START + "\n" + tool.END, tool.END + "\n" + tool.START]:
            index.write_text(text)
            self.invalid("marker pair", "index", write=True)
            self.assertEqual(index.read_text(), text)

    def test_local_links_and_duplicate_heading_anchors(self):
        other = self.root / "reference.md"
        other.write_text("# Reference\n## Shared name\n## Shared name\n")
        self.policy(body="Read [reference](../reference.md#shared-name-1).\n")
        self.index()
        self.policy(body="Read [missing](../reference.md#missing).\n")
        self.invalid("missing link anchor")
        self.policy(body="Read [missing](../absent.md).\n")
        self.invalid("missing link")

    def test_external_links_are_not_fetched_and_unsafe_schemes_are_rejected(self):
        self.policy(body="Read [external](https://example.invalid/unavailable).\n")
        self.index()
        self.policy(body="Read [unsafe](javascript:doThing).\n")
        self.invalid("relative local links")

    def test_explicit_html_anchor_in_existing_reference_is_supported(self):
        other = self.root / "reference.md"
        other.write_text('<a name="stable-reference"></a>\n# Reference\n')
        self.policy(body="Read [reference](../reference.md#stable-reference).\n")
        self.index()
        self.assertTrue(tool.run(self.directory)["valid"])

    def test_symlink_policy_and_index_do_not_overwrite_external_content(self):
        outside = self.root / "outside.md"
        outside.write_text("Preserve outside content.\n")
        path = self.policy()
        path.unlink()
        path.symlink_to(outside)
        self.invalid("Symlink")
        path.unlink()
        self.policy()
        (self.directory / tool.INDEX).symlink_to(outside)
        self.invalid("Symlink", "index", write=True)
        self.assertEqual(outside.read_text(), "Preserve outside content.\n")

    def test_symlink_directory_and_nested_policy_folder_are_explicit_stops(self):
        link = self.root / "linked-policies"
        link.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaisesRegex(tool.Invalid, "symlink"):
            tool.run(link)
        (self.directory / "nested").mkdir()
        self.invalid("Nested policy")

    def test_concurrent_record_change_is_preserved_and_index_is_not_written(self):
        path = self.policy()
        actual_read = tool.read
        calls = 0

        def changing_read(selected):
            nonlocal calls
            if selected == path:
                calls += 1
                if calls == 2:
                    path.write_text(path.read_text() + "Concurrent note.\n")
            return actual_read(selected)

        with patch.object(tool, "read", side_effect=changing_read):
            self.invalid("Selected file changed", "index", write=True)
        self.assertTrue(path.read_text().endswith("Concurrent note.\n"))
        self.assertFalse((self.directory / tool.INDEX).exists())

    def test_new_policy_during_index_preparation_is_not_omitted(self):
        self.policy()
        actual_table = tool.table

        def adding_table(records):
            self.policy("ADDED-RULE")
            return actual_table(records)

        with patch.object(tool, "table", side_effect=adding_table):
            self.invalid("inventory changed", "index", write=True)
        self.assertFalse((self.directory / tool.INDEX).exists())

    def test_cli_reports_failure_without_partial_loading_plan(self):
        self.policy(depends=["MISSING-RULE"])
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "check", "--policies", str(self.directory)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertFalse(report["valid"])
        self.assertEqual(report["load_order"], [])
        self.assertEqual(result.stderr, "")

    def test_shipped_kernel_is_valid_but_not_adopted(self):
        kernel = SCRIPT.parents[2] / "adopt-agent-policies" / "assets" / "kernel"
        result = tool.run(kernel)
        self.assertEqual(result["policy_count"], 3)
        self.assertEqual(result["load_order"], [])


    def test_reviewed_kernel_can_load_in_a_temporary_adopted_fixture(self):
        kernel = SCRIPT.parents[2] / "adopt-agent-policies" / "assets" / "kernel"
        for source in kernel.glob("*.md"):
            if source.name == tool.INDEX:
                continue
            body = source.read_text().replace('status = "proposed"', 'status = "adopted"').replace('authority = ""', 'authority = "Human fixture adopts these exact bodies."')
            (self.directory / source.name).write_text(body)
        self.index()
        plan = tool.run(self.directory, roots=["RESOLVE-DEPENDENCIES"])
        self.assertEqual(plan["load_order"], ["ADOPT-POLICIES", "PRESERVE-IDENTITY", "RESOLVE-DEPENDENCIES"])
        self.assertTrue(all(item["status"] == "proposed" for item in tool.collect(kernel)[0].values()))



if __name__ == "__main__":
    unittest.main()
