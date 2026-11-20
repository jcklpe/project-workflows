"""Exercise the supported layout with real temporary Git repositories."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import tomllib
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'update.py'
SOURCE = 'setup-project-workflows/assets/templates/github/PULL_REQUEST_TEMPLATE.md.template'
DEST = '.github/PULL_REQUEST_TEMPLATE.md'
CONFIG = 'docs/project-workflows.toml'
TEMPLATE = 'Heading\n\nfirst paragraph\n\nmiddle paragraph\n\nlast paragraph\n'


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pw-current-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / 'upstream'
        self.parent = self.root / 'project'
        self.child = self.parent / 'project-workflows'
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
        for root in (self.upstream, self.parent):
            root.mkdir()
            self.git(root, 'init', '--template=', '-b', 'main')
            self.identity(root)
        self.write(self.upstream, 'example.workflow.md', '# Example only\n')
        self.write(self.upstream, SOURCE, TEMPLATE)
        self.base = self.commit(self.upstream, 'shared source')
        self.write(self.parent, 'README.md', 'project\n')
        self.commit(self.parent, 'initial project')
        self.git(self.parent, '-c', 'protocol.file.allow=always', 'submodule', 'add', str(self.upstream), 'project-workflows')
        self.identity(self.child)
        self.git(self.child, 'checkout', '--detach', self.base)
        self.write(self.parent, CONFIG, 'schema_version = 1\n# Keep this comment.\n[project]\nname = "Example"\nroot = ".."\n[adoption]\nmode = "shared"\n[documents]\nagent_policies = "docs/agent-policies"\n[workflows]\nexample = "docs/example.md"\n')
        self.write(self.parent, 'docs/example.md', 'Local review context\n')
        self.commit(self.parent, 'adopt current layout')

    def git(self, root, *args):
        result = subprocess.run(['git', '-C', str(root), *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def identity(self, root):
        self.git(root, 'config', 'user.email', 'fixture@example.invalid')
        self.git(root, 'config', 'user.name', 'Fixture')

    def write(self, root, name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, root, message):
        self.git(root, 'add', '.')
        self.git(root, 'commit', '-m', message)
        return self.git(root, 'rev-parse', 'HEAD')

    def incoming(self, name='new.md', text='Shared improvement\n'):
        self.write(self.upstream, name, text)
        revision = self.commit(self.upstream, 'shared improvement')
        self.git(self.child, 'fetch', 'origin')
        return revision

    def helper(self, operation='update', revision='origin/main', *options, code=0):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), operation, '--project', str(self.parent), '--revision', revision, *options], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout or result.stderr)

    def install(self):
        self.write(self.parent, DEST, TEMPLATE)
        self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}', '--apply')
        self.commit(self.parent, 'record copied asset')

    def assert_pin(self, revision):
        self.assertEqual(self.git(self.child, 'rev-parse', 'HEAD'), revision)

    def test_preview_apply_repeat_preserves_parent_settings_refs_and_unrelated_index(self):
        before = (self.parent / CONFIG).read_bytes()
        self.write(self.parent, 'unrelated.txt', 'pending\n')
        self.git(self.parent, 'add', 'unrelated.txt')
        index = self.git(self.parent, 'ls-files', '--stage')
        refs = self.git(self.child, 'show-ref', '--heads')
        target = self.incoming()
        self.helper('update', target)
        self.assert_pin(self.base)
        result = self.helper('update', target, '--apply')
        self.assertTrue(result['changed'])
        self.assert_pin(target)
        self.assertEqual((self.parent / CONFIG).read_bytes(), before)
        self.assertEqual(self.git(self.child, 'show-ref', '--heads'), refs)
        self.assertEqual(self.git(self.parent, 'ls-files', '--stage'), index)
        self.assertFalse(self.helper('update', target, '--apply')['changed'])

    def test_asset_record_preview_and_repeat_preserve_comments_and_private_override(self):
        original = (self.parent / CONFIG).read_bytes()
        self.write(self.parent, '.gitignore', 'project-workflows.local.toml\n')
        private = 'Deliberately invalid TOML: this is not an updater input.\n'
        self.write(self.parent, 'docs/project-workflows.local.toml', private)
        self.write(self.parent, DEST, TEMPLATE)
        self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}')
        self.assertEqual((self.parent / CONFIG).read_bytes(), original)
        self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}', '--apply')
        self.assertTrue((self.parent / CONFIG).read_bytes().startswith(original))
        self.assertFalse(self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}', '--apply')['changed'])
        self.assertEqual((self.parent / 'docs/project-workflows.local.toml').read_text(), private)
        self.assertFalse((self.parent / '.project-workflows-assets.json').exists())

    def test_unchanged_asset_updates_baseline_and_repeats(self):
        self.install()
        target = self.incoming(SOURCE, TEMPLATE + 'New\n')
        self.helper('update', target, '--apply')
        self.assertEqual((self.parent / DEST).read_text(), TEMPLATE + 'New\n')
        self.assertEqual(tomllib.loads((self.parent / CONFIG).read_text())['assets'][DEST]['revision'], target)
        self.assertFalse(self.helper('update', target, '--apply')['changed'])

    def test_edited_asset_requires_review_and_preserves_both_changes(self):
        self.install()
        self.write(self.parent, DEST, TEMPLATE.replace('first paragraph', 'Local first'))
        target = self.incoming(SOURCE, TEMPLATE.replace('last paragraph', 'Shared last'))
        plan = self.helper('update', target, '--apply', code=2)
        self.assertEqual(plan['review_required'], [DEST])
        self.assert_pin(self.base)
        self.helper('update', target, '--reviewed', DEST, '--apply')
        self.assertIn('Local first', (self.parent / DEST).read_text())
        self.assertIn('Shared last', (self.parent / DEST).read_text())

    def test_asset_conflict_is_nonmutating(self):
        self.install()
        self.write(self.parent, DEST, TEMPLATE.replace('first paragraph', 'Local'))
        target = self.incoming(SOURCE, TEMPLATE.replace('first paragraph', 'Incoming'))
        self.assertIn('conflict', self.helper('update', target, '--apply', code=1)['error'])
        self.assert_pin(self.base)

    def test_missing_baseline_is_not_guessed(self):
        self.write(self.parent, DEST, TEMPLATE)
        self.assertIn('no recorded baseline', self.helper(code=1)['error'])

    def test_existing_baseline_cannot_be_replaced(self):
        self.install()
        target = self.incoming()
        self.assertIn('Baseline already exists', self.helper('record-assets', target, '--asset', f'{DEST}={SOURCE}', '--apply', code=1)['error'])

    def test_dirty_child_and_staged_config_stop_before_mutation(self):
        self.write(self.child, 'dirty.md', 'unfinished')
        self.assertIn('dirty', self.helper(code=1)['error'])
        (self.child / 'dirty.md').unlink()
        self.write(self.parent, CONFIG, (self.parent / CONFIG).read_text() + '\n# edit\n')
        self.git(self.parent, 'add', CONFIG)
        self.assertIn('staged', self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}', code=1)['error'])
        self.assert_pin(self.base)

    def test_old_names_and_child_config_have_no_fallback(self):
        original = (self.parent / CONFIG).read_text()
        (self.parent / CONFIG).unlink()
        for name in ('workflow.toml', 'docs/workflow.toml'):
            with self.subTest(name=name):
                self.write(self.parent, name, original)
                self.assertIn('no package-config fallback', self.helper(code=1)['error'])
                self.assertIn('Select a project-workflows.toml', self.helper('update', self.base, '--config', name, code=1)['error'])
                (self.parent / name).unlink()

    def test_staged_unicode_asset_is_preserved(self):
        dest = 'docs/review-é.md'
        self.write(self.parent, dest, TEMPLATE)
        self.git(self.parent, 'add', dest)
        before = (self.parent / CONFIG).read_bytes()
        index = self.git(self.parent, 'ls-files', '--stage')
        result = self.helper('record-assets', self.base, '--asset', f'{dest}={SOURCE}', '--apply', code=1)
        self.assertIn('staged', result['error'])
        self.assertEqual((self.parent / CONFIG).read_bytes(), before)
        self.assertEqual(self.git(self.parent, 'ls-files', '--stage'), index)

    def test_non_bmp_asset_round_trips_through_toml(self):
        dest = 'docs/review-📝.md'
        self.write(self.parent, dest, TEMPLATE)
        self.helper('record-assets', self.base, '--asset', f'{dest}={SOURCE}', '--apply')
        self.assertIn(dest, tomllib.loads((self.parent / CONFIG).read_text())['assets'])
        target = self.incoming(SOURCE, TEMPLATE + 'New\n')
        self.helper('update', target, '--apply')
        self.assertEqual((self.parent / dest).read_text(), TEMPLATE + 'New\n')

    def test_old_policy_key_and_location_are_rejected(self):
        original = (self.parent / CONFIG).read_text()
        for changed in (original.replace('agent_policies', 'policies'), original.replace('docs/agent-policies', 'docs/policies')):
            self.write(self.parent, CONFIG, changed)
            self.assertIn('old policy location is unsupported', self.helper(code=1)['error'])

    def test_json_baseline_mode_is_rejected(self):
        self.write(self.parent, '.project-workflows-assets.json', '{}')
        self.assertIn('obsolete JSON manifest', self.helper(code=1)['error'])

    def test_named_branch_is_not_switched(self):
        self.git(self.child, 'switch', '-c', 'keep-my-work')
        self.assertIn('detached shared pin', self.helper(code=1)['error'])
        self.assertEqual(self.git(self.child, 'branch', '--show-current'), 'keep-my-work')

    def test_divergent_source_is_not_discarded(self):
        self.write(self.child, 'local.md', 'experiment')
        local = self.commit(self.child, 'local experiment')
        target = self.incoming()
        self.assertIn('forward shared ancestry', self.helper('update', target, '--apply', code=1)['error'])
        self.assert_pin(local)

    def test_failed_fetch_stops(self):
        self.assertIn('fetch failed', self.helper('update', self.base, '--fetch', 'nonexistent', code=1)['error'])
        self.assert_pin(self.base)

    def test_target_runtime_config_is_rejected(self):
        target = self.incoming('workflow.toml', '[project]\nname = "Other"\n')
        self.assertIn('runtime project configuration', self.helper('update', target, '--apply', code=1)['error'])
        self.assert_pin(self.base)

    def test_custom_documentation_folder_and_ambiguity(self):
        original = (self.parent / CONFIG).read_text()
        self.write(self.parent, '_meta/project-workflows.toml', original)
        self.assertIn('Select exactly one', self.helper(code=1)['error'])
        self.helper('update', self.base, '--config', '_meta/project-workflows.toml')
        self.write(self.parent, 'notes/settings/project-workflows.toml', original.replace('root = ".."', 'root = "../.."'))
        self.helper('update', self.base, '--config', 'notes/settings/project-workflows.toml')
        self.write(self.parent, 'project-workflows.toml', original)
        self.assertIn('documentation folder', self.helper('update', self.base, '--config', 'project-workflows.toml', code=1)['error'])

    def test_config_and_required_note_failures(self):
        original = (self.parent / CONFIG).read_text()
        for changed, message in ((original.replace('root = ".."', 'root = "."'), 'project.root'), (original.replace('schema_version = 1', 'schema_version = 2'), 'schema_version'), (original.replace('mode = "shared"', 'mode = "adapted"'), 'adoption.mode'), (original.replace('docs/example.md', '../outside.md'), 'Unsafe')):
            self.write(self.parent, CONFIG, changed)
            self.assertIn(message, self.helper(code=1)['error'])
        self.write(self.parent, CONFIG, original)
        (self.parent / 'docs/example.md').unlink()
        self.assertIn('missing', self.helper(code=1)['error'])

    def test_unsafe_asset_and_policy_destinations_are_rejected(self):
        for dest, message in ((CONFIG, 'not automatically refreshed'), ('docs/example.md', 'not automatically refreshed'), ('docs/agent-policies/rule.md', 'explicit adoption'), ('../outside.md', 'Unsafe')):
            if not dest.startswith('..') and not (self.parent / dest).exists():
                self.write(self.parent, dest, 'rule')
            self.assertIn(message, self.helper('record-assets', self.base, '--asset', f'{dest}={SOURCE}', code=1)['error'])

    def test_kernel_source_cannot_be_refreshed_under_another_name(self):
        source = 'adopt-agent-policies/assets/kernel/rule.md'
        target = self.incoming(source, 'candidate')
        self.write(self.parent, 'rule.md', 'operative')
        self.assertIn('explicit adoption', self.helper('record-assets', target, '--asset', f'rule.md={source}', code=1)['error'])

    def test_invalid_baseline_revision_and_symlink_destination(self):
        self.write(self.parent, DEST, TEMPLATE)
        (self.parent / DEST).unlink()
        (self.parent / DEST).symlink_to(self.parent / 'README.md')
        self.assertIn('Symlink', self.helper('record-assets', self.base, '--asset', f'{DEST}={SOURCE}', code=1)['error'])
        (self.parent / DEST).unlink()
        self.install()
        path = self.parent / CONFIG
        path.write_text(path.read_text().replace(f'revision = "{self.base}"', 'revision = "main"'))
        self.assertIn('exact source commit', self.helper(code=1)['error'])

    def test_malformed_markers_and_unrelated_settings_stop_before_pin_advance(self):
        self.install()
        config = self.parent / CONFIG
        original = config.read_text()
        target = self.incoming(SOURCE, TEMPLATE + 'New\n')
        for changed in (original.replace('# project-workflows-assets:end', '# absent'), original.replace('# project-workflows-assets:end', '[unrelated]\nkeep = true\n# project-workflows-assets:end')):
            config.write_text(changed)
            self.helper('update', target, '--apply', code=1)
            self.assert_pin(self.base)
            self.assertEqual(config.read_text(), changed)

    def test_concurrent_note_edit_after_checkout_stops_asset_writes(self):
        self.install()
        before = (self.parent / CONFIG).read_bytes()
        target = self.incoming(SOURCE, TEMPLATE + 'New\n')
        note = self.parent / 'docs/example.md'
        hook = Path(self.git(self.child, 'rev-parse', '--path-format=absolute', '--git-path', 'hooks/post-checkout'))
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/bin/sh\nprintf '%s\\n' 'Concurrent edit' > " + shlex.quote(str(note)) + '\n')
        hook.chmod(0o755)
        self.assertIn('child advanced but assets were left alone', self.helper('update', target, '--apply', code=1)['error'])
        self.assert_pin(target)
        self.assertEqual((self.parent / CONFIG).read_bytes(), before)
        self.assertEqual((self.parent / DEST).read_text(), TEMPLATE)


if __name__ == '__main__':
    unittest.main()
