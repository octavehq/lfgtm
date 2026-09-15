#!/usr/bin/env python3
"""Shared artifact I/O. Exit 3 means a write may have happened: reconcile first."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlsplit
import zipfile


class Indeterminate(Exception):
    pass


def safe_member(name):
    if not isinstance(name, str) or not name or '\\' in name or re.search(r'[\x00-\x1f\x7f]', name):
        raise ValueError('invalid member path')
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')) or ':' in p.parts[0]:
        raise ValueError(f'unsafe member path: {name}')
    return p


def checked_path(root, name):
    parts = safe_member(name).parts
    root = root.absolute()
    target = root.joinpath(*parts)
    for p in [target, *target.parents]:
        if p == root.parent:
            break
        if p.is_symlink():
            raise ValueError(f'symlink path rejected: {name}')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'path escapes root: {name}')
    return target


def files_for(root, manifest=None):
    root = root.absolute()
    if root.is_symlink():
        raise ValueError('source root must not be a symlink')
    if manifest:
        names = json.loads(manifest.read_text())
        if not isinstance(names, list) or any(not isinstance(n, str) for n in names):
            raise ValueError('publish manifest must be a JSON array of relative file paths')
    else:
        names = []
        for base, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
            for d in dirs:
                if (Path(base) / d).is_symlink():
                    raise ValueError('source contains a directory symlink')
            names.extend((Path(base) / f).relative_to(root).as_posix() for f in files if not f.startswith('.'))
    result = []
    for name in sorted(set(names)):
        path = checked_path(root, name)
        if any(p.startswith('.') for p in PurePosixPath(name).parts):
            raise ValueError(f'dotfile in publish manifest: {name}')
        if any(c in name for c in ';,"'):
            raise ValueError(f'unsupported multipart filename: {name}')
        if not path.is_file():
            raise ValueError(f'missing selected file: {name}')
        result.append((name, path))
    if not result:
        raise ValueError('publish manifest is empty')
    return result


def checked_zip(path):
    if path.is_symlink():
        raise ValueError('ZIP symlink rejected')
    with zipfile.ZipFile(path) as z:
        names = []
        for item in z.infolist():
            name = item.filename.rstrip('/')
            safe_member(name)
            if any(p.startswith('.') for p in PurePosixPath(name).parts) or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError(f'unsafe ZIP member: {name}')
            if not item.is_dir():
                names.append(name)
        if not names or len(names) != len(set(names)):
            raise ValueError('empty ZIP or duplicate members')
        if z.testzip():
            raise ValueError('corrupt ZIP member')
    return names


def request(base, token, route, method='GET', payload=None, archive=None):
    with tempfile.TemporaryDirectory(prefix='octave-http-') as tmp:
        body = Path(tmp) / 'body'
        cmd = ['curl', '--silent', '--show-error', '--max-time', '120', '--config', '-',
               '-o', str(body), '-w', '%{http_code}', '-X', method, base + route]
        if archive:
            cmd += ['--form-string', 'metadata=' + json.dumps(payload or {}), '-F', f'site=@{archive};type=application/zip']
        elif payload is not None:
            cmd += ['-H', 'Content-Type: application/json', '--data-binary', json.dumps(payload)]
        if re.search(r'[\r\n]', token):
            raise ValueError('invalid token')
        config = 'header = ' + json.dumps('Authorization: Bearer ' + token) + '\n'
        result = subprocess.run(cmd, input=config, capture_output=True, text=True)
        if result.returncode:
            error = f'{method} transport failed; remote state must be reconciled' if method != 'GET' else 'GET transport failed'
            raise (Indeterminate(error) if method != 'GET' else ValueError(error))
        if result.stdout not in ('200', '201'):
            raise ValueError(f'{method} returned HTTP {result.stdout}; response body omitted to protect credentials')
        return body.read_bytes(), result.stdout


def parse_response(raw, status, writing=False, expected=None):
    try:
        value = json.loads(raw)
        if not isinstance(value, dict) or not isinstance(value.get('uuid'), str) or not value['uuid']:
            raise ValueError('missing artifact identity')
        if expected and value['uuid'] != expected:
            raise ValueError('artifact identity mismatch')
        for field in ('identifier', 'type', 'privacy', 'status', 'previewUrl'):
            if value.get(field) is not None and not isinstance(value[field], str):
                raise ValueError(f'invalid {field}')
        return value
    except (ValueError, TypeError) as exc:
        message = f'HTTP {status}: {exc}; reconcile artifact {expected or "by the requested identifier"} before retrying'
        raise Indeterminate(message) if writing else ValueError(message)


def atomic_download(root, name, content, overwrite=False, size=None, checksum=None):
    dest = checked_path(root, name)
    if dest.exists() and not overwrite:
        raise ValueError(f'destination exists; use --overwrite for authorized replacement: {name}')
    if size is not None and len(content) != size:
        raise ValueError(f'size mismatch: {name}')
    if checksum and hashlib.sha256(content).hexdigest() != checksum:
        raise ValueError(f'checksum mismatch: {name}')
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.download-', dir=dest.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        checked_path(root, name)
        if not overwrite:
            os.link(temp, dest)  # exclusive creation; cannot replace a racing writer
        else:
            os.replace(temp, dest)
    finally:
        Path(temp).unlink(missing_ok=True)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operation', choices=['create', 'zip', 'update', 'download'])
    ap.add_argument('--src', type=Path)
    ap.add_argument('--manifest', type=Path, help='JSON array of approved bundle members; required for public directory uploads')
    ap.add_argument('--uuid')
    ap.add_argument('--type', choices=['website', 'storage'])
    ap.add_argument('--privacy', choices=['only_me', 'workspace', 'public'])
    ap.add_argument('--status', choices=['published', 'unpublished'])
    for flag in ('identifier', 'description', 'entry-point', 'note'):
        ap.add_argument('--' + flag)
    ap.add_argument('--expected-version', type=int)
    ap.add_argument('--out', type=Path, default=Path('.'))
    ap.add_argument('--version', type=int)
    ap.add_argument('--overwrite', action='store_true')
    args = ap.parse_args()
    token = os.environ.get('ARTIFACTS_ACCESS_TOKEN', '')
    base = os.environ.get('ARTIFACTS_URL', 'https://link.octavehq.com').rstrip('/')
    if not token:
        raise ValueError('set ARTIFACTS_ACCESS_TOKEN from asset_generate_access_token; token is env-only')
    if urlsplit(base).scheme not in ('http', 'https'):
        raise ValueError('ARTIFACTS_URL must be HTTP(S)')
    if args.operation in ('update', 'download') and not args.uuid:
        raise ValueError('--uuid is required')
    route = '/api/v1/artifacts' + ('/' + quote(args.uuid, safe='') if args.uuid else '')
    if args.operation == 'download':
        data = parse_response(*request(base, token, route), expected=args.uuid)
        identifier = data.get('identifier') or args.uuid
        safe_member(identifier)
        if '/' in identifier:
            raise ValueError('identifier is not a local folder name')
        if args.version is not None:
            if args.version < 1:
                raise ValueError('--version must be positive')
            raw, _ = request(base, token, route + f'/versions/{args.version}/download')
            suffix = '.zip' if raw.startswith(b'PK\x03\x04') else '.bin'
            print(atomic_download(args.out, f'{identifier}-v{args.version}{suffix}', raw, args.overwrite))
        else:
            members = (data.get('metadata') or {}).get('filesMap') or []
            if not members:
                raise ValueError('artifact has no file manifest')
            if not isinstance(members, list) or any(not isinstance(m, dict) or not isinstance(m.get('path'), str) for m in members):
                raise ValueError('malformed file manifest')
            if len({m['path'] for m in members}) != len(members):
                raise ValueError('duplicate file manifest paths')
            root = args.out / identifier
            for member in members:
                checked_path(root, member['path'])
            for member in members:
                raw, _ = request(base, token, route + '/download/' + quote(member['path'], safe='/'))
                print(atomic_download(root, member['path'], raw, args.overwrite, member.get('size'), member.get('sha256')))
        return
    creating = args.operation in ('create', 'zip')
    if creating and not args.src:
        raise ValueError('--src is required')
    if args.note and not args.src:
        raise ValueError('--note requires --src')
    meta = {key: value for key, value in {'identifier': args.identifier, 'description': args.description,
            'entryPoint': args.entry_point, 'type': args.type, 'privacy': args.privacy,
            'status': args.status, 'note': args.note}.items() if value is not None}
    if creating:
        meta = {'identifier': args.src.stem, 'type': 'website', 'privacy': 'workspace', 'status': 'published', **meta}
    if args.entry_point:
        safe_member(args.entry_point)
    if not args.src and not meta:
        raise ValueError('nothing to update')
    before = None
    if not creating:
        before = parse_response(*request(base, token, route), expected=args.uuid)
        if args.expected_version is not None and before.get('currentVersion') != args.expected_version:
            raise ValueError('remote version changed or version field unavailable; reconcile before updating')
    effective_privacy = meta.get('privacy', (before or {}).get('privacy'))
    with tempfile.TemporaryDirectory(prefix='octave-upload-') as tmp:
        archive = None
        selected = None
        if args.src:
            if args.src.is_dir():
                if effective_privacy == 'public' and not args.manifest:
                    raise ValueError('public directory uploads require --manifest with approved members')
                files = files_for(args.src, args.manifest)
                selected = {name: path.stat().st_size for name, path in files}
                archive = Path(tmp) / 'site.zip'
                with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                    for name, path in files:
                        z.write(path, name)
            else:
                checked_zip(args.src)
                archive = Path(tmp) / 'site.zip'
                shutil.copyfile(args.src, archive)
                with zipfile.ZipFile(archive) as z:
                    selected = {i.filename: i.file_size for i in z.infolist() if not i.is_dir()}
                if effective_privacy == 'public':
                    if not args.manifest or set(json.loads(args.manifest.read_text())) != set(selected):
                        raise ValueError('public ZIP uploads require a manifest matching every archive member')
            entry = meta.get('entryPoint', (before or {}).get('entryPoint'))
            if entry and entry not in selected:
                raise ValueError('entry point is absent from the selected bundle')
        if not creating:
            latest = parse_response(*request(base, token, route), expected=args.uuid)
            if any(latest.get(k) != before.get(k) for k in ('currentVersion', 'updatedAt', 'privacy', 'status', 'entryPoint', 'identifier')):
                raise ValueError('artifact changed during preparation; reconcile before updating')
        method = 'POST' if archive else 'PATCH'
        write_route = route + ('/files' if not creating and archive else '')
        result = parse_response(*request(base, token, write_route, method, meta, archive), writing=True, expected=args.uuid)
        identity = result['uuid']
        try:
            verified = parse_response(*request(base, token, '/api/v1/artifacts/' + quote(identity, safe='')), expected=identity)
            for key, value in meta.items():
                if key != 'note' and verified.get(key) != value:
                    raise ValueError(f'readback differs for {key}')
            if selected is not None:
                saved = {m['path']: m['size'] for m in verified.get('metadata', {}).get('filesMap', [])}
                if saved != selected:
                    raise ValueError('file manifest readback differs from selected files')
                if not isinstance(verified.get('currentVersion'), int):
                    raise ValueError('version readback unavailable')
                if before and verified['currentVersion'] <= before['currentVersion']:
                    raise ValueError('file replacement did not advance the version')
        except ValueError as exc:
            raise Indeterminate(f'write returned artifact {identity}, but verification is incomplete: {exc}')
        print(json.dumps({k: verified[k] for k in ('uuid', 'identifier', 'type', 'privacy', 'status', 'currentVersion') if k in verified}, indent=2))
        print('Verified metadata readback. Preview access follows the verified service policy; file/access checks remain task-specific.')


if __name__ == '__main__':
    try:
        main()
    except Indeterminate as exc:
        print('INDETERMINATE:', exc, file=sys.stderr)
        sys.exit(3)
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print('ERROR:', exc, file=sys.stderr)
        sys.exit(1)
