"""Workspace-bound JSON state and exclusive, deliberately non-expiring locks."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import sys


def unsafe_symlink(path):
    # macOS exposes system directories through fixed /private aliases.
    if sys.platform == 'darwin' and path in (Path('/tmp'), Path('/var'), Path('/etc')):
        return path.resolve() != Path('/private') / path.name
    return path.is_symlink()


def component(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}', value):
        raise ValueError('unsafe state identity')
    return value


def checksum(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    if any(unsafe_symlink(p) for p in (path, *path.parents)):
        raise ValueError('state path contains a symlink')
    payload = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.state-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


def read_bound(path, workspace, version=1):
    value = json.loads(Path(path).read_text())
    if value.get('workspaceOId') != component(workspace) or value.get('schemaVersion') != version:
        raise ValueError('unverified workspace or unsupported state schema')
    return value


@contextmanager
def exclusive_lock(directory, run_id):
    directory = Path(directory)
    if any(unsafe_symlink(p) for p in (directory, *directory.parents)):
        raise ValueError('lock directory contains a symlink')
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / 'run.lock'
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise RuntimeError('active or interrupted run; reconcile run.lock before retrying')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump({'runId': component(run_id), 'createdAt': datetime.now(timezone.utc).isoformat()}, f)
            f.flush(); os.fsync(f.fileno())
        yield
    except BaseException:
        # Preserve identity on interrupted or indeterminate publication.
        raise
    else:
        lock.unlink()


def digest_key(spec, report_runs):
    if not spec.get('workspaceOId') or not spec.get('digestId'):
        raise ValueError('digest identity is required')
    component(spec['workspaceOId']); component(spec['digestId'])
    if any(r.get('status') != 'completed' or not r.get('id') for r in report_runs):
        raise ValueError('only identified completed reports can be consumed')
    return checksum({'workspace': spec['workspaceOId'], 'spec': spec,
                     'reports': sorted(set(r['id'] for r in report_runs)), 'format': spec['format']})


def exception_applies(entry, workspace, entity, rule, revision, now):
    try:
        expires = datetime.fromisoformat(entry['expiresAt'].replace('Z', '+00:00'))
        return (entry['workspaceOId'] == workspace and entity in entry['entityIds']
                and entry['ruleId'] == rule and entry['sourceRevision'] == revision and now < expires)
    except (KeyError, TypeError, ValueError):
        return False
