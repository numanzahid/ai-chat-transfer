"""Isolated tests: synthetic transcripts only; no real chat stores or SSH hosts."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / '.agents/skills/ai-chat-transfer/scripts/transfer-chat.py'
ENTRYPOINT = HELPER.with_suffix('.sh')
spec = importlib.util.spec_from_file_location('transfer_chat', HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class TransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source-config'
        self.destination = self.root / 'destination-config'
        self.workspace = '/source/project'
        self.target_workspace = "/destination/space ' quote $(touch SENTINEL); project"
        self.data = b'{"type":"user","message":"synthetic test"}\n'
        folder = self.source / 'projects' / self.workspace.replace('/', '-')
        folder.mkdir(parents=True)
        (folder / 'selected.jsonl').write_bytes(self.data)
        (folder / 'unselected.jsonl').write_bytes(self.data)

    def args(self):
        return ['--from-path', self.workspace, '--to-path', self.target_workspace,
                '--source-config-dir', str(self.source),
                '--destination-config-dir', str(self.destination)]

    def run_cli(self, *extra):
        return subprocess.run(['bash', str(ENTRYPOINT), *self.args(), *extra],
                              capture_output=True, text=True, cwd=self.root)

    def payload(self):
        return {'workspace': self.target_workspace, 'config': str(self.destination),
                'records': [{'id': 'selected', 'data': base64.b64encode(self.data).decode(),
                             'sha256': hashlib.sha256(self.data).hexdigest()}]}

    def target(self):
        return self.destination / 'projects' / self.target_workspace.replace('/', '-') / 'selected.jsonl'

    def test_requires_explicit_selection(self):
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_copies_only_selected_with_private_permissions(self):
        result = self.run_cli('--session', 'selected')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.target().read_bytes(), self.data)
        self.assertEqual(self.target().stat().st_mode & 0o777, 0o600)
        self.assertFalse(self.target().with_name('unselected.jsonl').exists())

    def test_collision_keeps_existing_bytes(self):
        self.target().parent.mkdir(parents=True)
        self.target().write_bytes(b'existing conversation')
        result = self.run_cli('--session', 'selected')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.target().read_bytes(), b'existing conversation')

    def test_dangling_symlink_is_a_collision(self):
        self.target().parent.mkdir(parents=True)
        self.target().symlink_to(self.root / 'absent')
        with self.assertRaises(FileExistsError):
            helper.receive(self.payload())
        self.assertTrue(self.target().is_symlink())

    def test_race_after_preflight_cannot_overwrite(self):
        real_link = helper.os.link
        def racing_link(source, destination):
            Path(destination).write_bytes(b'concurrent conversation')
            return real_link(source, destination)
        with patch.object(helper.os, 'link', side_effect=racing_link):
            with self.assertRaises(FileExistsError):
                helper.receive(self.payload())
        self.assertEqual(self.target().read_bytes(), b'concurrent conversation')
        self.assertEqual(list(self.target().parent.glob('.chat-transfer-*')), [])

    def test_missing_later_session_writes_nothing(self):
        result = self.run_cli('--session', 'selected', '--session', 'missing')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_rejects_bad_arguments_before_writing(self):
        for extra in [('--session', '../escape'), ('--session',),
                      ('--session', 'selected', '--to-path', 'relative'),
                      ('--session', 'selected', '--to-host', '-oProxyCommand=bad'),
                      ('--session', 'selected', '--session', 'selected')]:
            with self.subTest(extra=extra):
                self.assertNotEqual(self.run_cli(*extra).returncode, 0)
                self.assertFalse(self.destination.exists())

    def test_rejects_truncated_jsonl_and_bad_digest(self):
        payload = self.payload()
        payload['records'][0]['sha256'] = 'bad'
        with self.assertRaises(ValueError):
            helper.receive(payload)
        payload = self.payload()
        payload['records'][0]['data'] = base64.b64encode(b'{"incomplete":').decode()
        with self.assertRaises(ValueError):
            helper.receive(payload)
        self.assertFalse(self.destination.exists())

    def test_remote_command_keeps_paths_and_content_out_of_shell(self):
        # Execute the generated remote command through a real POSIX shell locally.
        # This validates quoting and receiver dispatch without a network connection.
        real_run = subprocess.run
        def fake_ssh(argv, **kwargs):
            self.assertEqual(argv[:3], ['ssh', '--', 'test-host'])
            self.assertNotIn(self.target_workspace, argv[3])
            return real_run(['sh', '-c', argv[3]], cwd=self.root, **kwargs)
        with patch.object(helper.subprocess, 'run', side_effect=fake_ssh), \
             patch('sys.argv', [str(HELPER), *self.args(), '--session', 'selected', '--to-host', 'test-host']):
            helper.main()
        self.assertEqual(self.target().read_bytes(), self.data)
        self.assertFalse((self.root / 'SENTINEL').exists())


if __name__ == '__main__':
    unittest.main()
