#!/usr/bin/env python3
"""Validate and promote immutable brand captures through an atomic pointer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit
import uuid
from kit_validation import validate_manifest, asset_path


def canonical_domain(value):
    parsed=urlsplit(value if '://' in value else 'https://'+value)
    if not parsed.hostname or parsed.username or parsed.password: raise ValueError('invalid brand domain')
    host=parsed.hostname.lower().rstrip('.').encode('idna').decode()
    if not re.fullmatch(r'[a-z0-9.-]+',host) or '..' in host:raise ValueError('invalid hostname')
    return host


def cache_root(base,domain,workspace):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}',workspace):raise ValueError('verified workspace ID required')
    return Path(base)/workspace/canonical_domain(domain)


def resolve(root,domain=None,workspace=None):
    root=Path(root)
    if (root/'current.json').is_file():
        pointer=json.loads(asset_path(root,'current.json').read_text())
        capture=pointer.get('capture')
        if not isinstance(capture,str) or not re.fullmatch(r'versions/[a-f0-9]{32}',capture):raise ValueError('invalid capture pointer')
        root=root/capture
    manifest=json.loads(asset_path(root,'manifest.json').read_text())
    validate_manifest(root,manifest,canonical_domain(domain) if domain else None,workspace)
    return root,manifest


def promote(staging,base,domain,workspace):
    staging=Path(staging);domain=canonical_domain(domain)
    manifest=json.loads(asset_path(staging,'manifest.json').read_text())
    if manifest.get('schemaVersion')!=1:raise ValueError('capture requires schemaVersion 1')
    if not manifest.get('sourceUrls') or not manifest.get('capturedAt') or not manifest.get('allowedUse'):
        raise ValueError('capture requires provenance, date and allowed-use decisions')
    validate_manifest(staging,manifest,domain,workspace)
    for name in ('tokens.css','brand-kit.md','components.html'):asset_path(staging,name)
    checks=manifest.get('assetChecksums') or {}
    for p in staging.rglob('*'):
        if p.is_symlink():raise ValueError('symlink in capture')
        if p.is_file() and p.name!='manifest.json' and not p.name.startswith('.'):
            rel=p.relative_to(staging).as_posix()
            if checks.get(rel)!=hashlib.sha256(p.read_bytes()).hexdigest():raise ValueError(f'uncatalogued or changed capture file: {rel}')
    base=Path(base).absolute()
    target=cache_root(base,domain,workspace)
    for p in (target,*target.parents):
        if p==base.parent:break
        if p.is_symlink():raise ValueError('symlink cache root')
    versions=target/'versions';versions.mkdir(parents=True,exist_ok=True)
    capture=uuid.uuid4().hex
    temp=Path(tempfile.mkdtemp(prefix='.capture-',dir=versions))
    try:
        shutil.copytree(staging,temp,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.*','__pycache__'))
        resolve(temp,domain,workspace)
        os.rename(temp,versions/capture)
        fd,ptr=tempfile.mkstemp(prefix='.pointer-',dir=target)
        try:
            with os.fdopen(fd,'w') as f:
                json.dump({'capture':'versions/'+capture},f);f.flush();os.fsync(f.fileno())
            os.replace(ptr,target/'current.json')
        finally:Path(ptr).unlink(missing_ok=True)
    finally:
        if temp.exists():shutil.rmtree(temp)
    return target


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('staging',type=Path)
    ap.add_argument('--base',type=Path,default=Path.home()/'.octave/brands')
    ap.add_argument('--domain',required=True);ap.add_argument('--workspace',required=True)
    args=ap.parse_args();print(promote(args.staging,args.base,args.domain,args.workspace))
