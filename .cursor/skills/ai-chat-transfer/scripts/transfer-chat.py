#!/usr/bin/env python3
"""Copy explicitly selected Claude Code main transcripts without overwriting."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import shlex
import subprocess
import sys
import tempfile


def absolute_path(value):
    if not value.startswith('/') or posixpath.normpath(value) != value or '\x00' in value:
        raise ValueError('Use a normalized absolute POSIX path: ' + repr(value))
    return value


def session_id(value):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', value):
        raise ValueError('Invalid session ID: ' + repr(value))
    return value


def validate_transcript(data):
    if not data or not data.endswith(b'\n'):
        raise ValueError('Transcript must contain complete newline-terminated JSONL records')
    for line in data.splitlines():
        if not isinstance(json.loads(line), dict):
            raise ValueError('Transcript records must be JSON objects')


def receive(payload):
    workspace = absolute_path(payload['workspace'])
    config = Path(absolute_path(payload['config'])) if payload['config'] else Path.home() / '.claude'
    destination = config / 'projects' / workspace.replace('/', '-')
    records = payload['records']
    if not records:
        raise ValueError('No sessions selected')
    prepared = []
    seen = set()
    # Validate the entire batch before creating directories or writing files.
    for record in records:
        sid = session_id(record['id'])
        if sid in seen:
            raise ValueError('Duplicate session ID: ' + sid)
        seen.add(sid)
        target = destination / (sid + '.jsonl')
        if os.path.lexists(target):
            raise FileExistsError('Destination already exists: ' + str(target))
        data = base64.b64decode(record['data'], validate=True)
        validate_transcript(data)
        if hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('Snapshot digest mismatch: ' + sid)
        prepared.append((target, data, record['sha256']))
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    installed = []
    try:
        for target, data, digest in prepared:
            # Stage on the same filesystem; link() atomically refuses any collision,
            # including a file or dangling symlink created after the preflight.
            fd, temporary = tempfile.mkstemp(prefix='.chat-transfer-', dir=destination)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.link(temporary, target)
                installed.append(str(target))
                if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                    raise ValueError('Destination verification failed: ' + str(target))
            finally:
                os.unlink(temporary)
    except Exception:
        print('Import stopped. Files created by this attempt: ' + json.dumps(installed), file=sys.stderr)
        print('Inspect these files before retrying; no existing file was replaced.', file=sys.stderr)
        raise
    print('Copied and verified main transcripts: ' + json.dumps(installed))
    print('Companion files and interactive resume were not verified by this helper.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--to-host', help='SSH alias or user@host; omit for local copying')
    parser.add_argument('--to-path', required=True, help='Normalized absolute destination workspace')
    parser.add_argument('--from-path', default=os.getcwd(), help='Normalized absolute source workspace')
    parser.add_argument('--session', action='append', required=True, help='Selected session ID (repeatable)')
    parser.add_argument('--source-config-dir', help='Absolute local Claude config directory; default ~/.claude')
    parser.add_argument('--destination-config-dir', help='Absolute destination Claude config directory; default ~/.claude')
    args = parser.parse_args()
    source_workspace = absolute_path(args.from_path)
    absolute_path(args.to_path)
    if args.destination_config_dir:
        absolute_path(args.destination_config_dir)
    config = Path(absolute_path(args.source_config_dir)) if args.source_config_dir else Path.home() / '.claude'
    if args.to_host and not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.@:\[\]-]*', args.to_host):
        raise ValueError('Invalid SSH host; use a configured alias or user@host')
    records = []
    selected = set()
    for sid in args.session:
        session_id(sid)
        if sid in selected:
            raise ValueError('Duplicate session ID: ' + sid)
        selected.add(sid)
        source = config / 'projects' / source_workspace.replace('/', '-') / (sid + '.jsonl')
        before = source.stat()
        data = source.read_bytes()
        after = source.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError('Source changed during capture; retry with an idle session: ' + sid)
        validate_transcript(data)
        records.append({'id': sid, 'data': base64.b64encode(data).decode('ascii'),
                        'sha256': hashlib.sha256(data).hexdigest()})
    payload = {'workspace': args.to_path, 'config': args.destination_config_dir, 'records': records}
    if args.to_host:
        # Only fixed program text enters the remote shell. Paths and chat content
        # travel as JSON on stdin, never as executable command arguments.
        program = Path(__file__).read_text()
        receiver = ('import json, sys\nnamespace = {"__name__": "transfer_receiver"}\n'
                    + 'exec(' + repr(program) + ', namespace)\n'
                    + 'namespace["receive"](json.load(sys.stdin))\n')
        command = 'python3 -c ' + shlex.quote(receiver)
        subprocess.run(['ssh', '--', args.to_host, command], input=json.dumps(payload).encode(), check=True)
    else:
        receive(payload)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('Transfer failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
