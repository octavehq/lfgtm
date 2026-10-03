#!/usr/bin/env python3
"""Validate and promote immutable brand captures through an atomic pointer.

  brand_cache.py canonical  <url-or-domain> [--workspace <id>]           # canonical domain (no www.) and the cache root
  brand_cache.py checksums  <staging>                                    # write assetChecksums into manifest.json
  brand_cache.py promote    <staging> --domain <d> --workspace <w> [--base <dir>] [--status draft|ready] [--write-checksums]
  brand_cache.py mark-ready <cache-root> [--score 36/40]                 # after the fidelity gate passed
  brand_cache.py status     <cache-root>                                 # pointer, status, capture dir

The pointer (<cache-root>/current.json) carries a status. `promote` writes `draft`: the kit passed the
mechanical checks but not yet the fidelity gate. `mark-ready` flips it once an independent judge has
scored the rendered gallery. Consumers resolve ready kits only; the capture tooling passes
allow_draft=True. Pointers written before statuses existed count as ready.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
from urllib.parse import urlsplit
import uuid
from kit_validation import validate_manifest, asset_path

STATUSES = ('draft', 'ready')


def canonical_domain(value):
    parsed=urlsplit(value if '://' in value else 'https://'+value)
    if not parsed.hostname or parsed.username or parsed.password: raise ValueError('invalid brand domain')
    host=parsed.hostname.lower().rstrip('.').encode('idna').decode()
    host=host.removeprefix('www.')  # one cache per brand: www.acme.com and acme.com are the same kit
    if not re.fullmatch(r'[a-z0-9.-]+',host) or '..' in host:raise ValueError('invalid hostname')
    return host


def cache_root(base,domain,workspace):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}',workspace):raise ValueError('verified workspace ID required')
    return Path(base)/workspace/canonical_domain(domain)


def read_pointer(root):
    """The validated current.json of a cache root, or None when the root is a bare kit directory."""
    root=Path(root)
    if not (root/'current.json').is_file():return None
    pointer=json.loads(asset_path(root,'current.json').read_text())
    capture=pointer.get('capture')
    if not isinstance(capture,str) or not re.fullmatch(r'versions/[a-f0-9]{32}',capture):raise ValueError('invalid capture pointer')
    status=pointer.get('status','ready')
    if status not in STATUSES:raise ValueError(f'invalid capture status: {status}')
    pointer['status']=status
    return pointer


def write_pointer(root,pointer):
    root=Path(root)
    fd,ptr=tempfile.mkstemp(prefix='.pointer-',dir=root)
    try:
        with os.fdopen(fd,'w') as f:
            json.dump(pointer,f);f.flush();os.fsync(f.fileno())
        os.replace(ptr,root/'current.json')
    finally:Path(ptr).unlink(missing_ok=True)


def capture_dir(root,pointer):
    """The capture folder a pointer names, or None when it was deleted (a stale pointer is an empty cache)."""
    d=Path(root)/pointer['capture']
    return d if (d/'manifest.json').is_file() else None


def resolve(root,domain=None,workspace=None,allow_draft=False):
    root=Path(root)
    pointer=read_pointer(root)
    if pointer:
        if pointer['status']=='draft' and not allow_draft:
            raise ValueError('brand kit is a draft: run the fidelity gate, then `brand_cache.py mark-ready <cache-root>`')
        if capture_dir(root,pointer) is None:
            raise ValueError(f"stale capture pointer: {pointer['capture']} is missing; re-run the capture")
        root=root/pointer['capture']
    manifest=json.loads(asset_path(root,'manifest.json').read_text())
    validate_manifest(root,manifest,canonical_domain(domain) if domain else None,workspace)
    return root,manifest


def capture_files(staging):
    staging=Path(staging)
    for p in sorted(staging.rglob('*')):
        if p.is_symlink():raise ValueError('symlink in capture')
        rel=p.relative_to(staging)
        if p.is_file() and rel.as_posix()!='manifest.json' and not any(x.startswith('.') for x in rel.parts) and '__pycache__' not in rel.parts:
            yield rel.as_posix(),p


def write_checksums(staging):
    """Catalogue every capture file in manifest.assetChecksums. Re-run after any edit; promote verifies it."""
    staging=Path(staging)
    manifest_path=asset_path(staging,'manifest.json')
    manifest=json.loads(manifest_path.read_text())
    manifest['assetChecksums']={rel:hashlib.sha256(p.read_bytes()).hexdigest() for rel,p in capture_files(staging)}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest['assetChecksums']


def promote(staging,base,domain,workspace,status='draft',write_checksums_first=False):
    staging=Path(staging);domain=canonical_domain(domain)
    if status not in STATUSES:raise ValueError(f'status must be one of {STATUSES}')
    if write_checksums_first:write_checksums(staging)
    manifest=json.loads(asset_path(staging,'manifest.json').read_text())
    if manifest.get('schemaVersion')!=1:raise ValueError('capture requires schemaVersion 1')
    if not manifest.get('sourceUrls') or not manifest.get('capturedAt') or not manifest.get('allowedUse'):
        raise ValueError('capture requires provenance, date and allowed-use decisions')
    validate_manifest(staging,manifest,domain,workspace)
    for name in ('tokens.css','brand-kit.md','components.html'):asset_path(staging,name)
    checks=manifest.get('assetChecksums') or {}
    for rel,p in capture_files(staging):
        if checks.get(rel)!=hashlib.sha256(p.read_bytes()).hexdigest():
            raise ValueError(f'uncatalogued or changed capture file: {rel} (run `brand_cache.py checksums {staging}`)')
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
        write_pointer(target,{'capture':'versions/'+capture,'status':status,'promotedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    finally:
        if temp.exists():shutil.rmtree(temp)
    return target


def validate_score(score):
    """A fidelity score as the gate reports it: a mean such as 34.5/40 is as valid as 34/40."""
    m=re.fullmatch(r'(\d{1,2}(?:\.\d{1,2})?)/40',str(score).strip())
    if not m or float(m[1])>40:raise ValueError('score must look like 34/40 or 34.5/40')
    return m[0]


def mark_ready(root,score=None):
    """Flip the pointer to ready once the fidelity gate passed; records the score and time."""
    root=Path(root)
    pointer=read_pointer(root)
    if not pointer:raise ValueError(f'no current.json under {root}')
    if capture_dir(root,pointer) is None:raise ValueError(f"stale capture pointer: {pointer['capture']} is missing; nothing to mark ready")
    pointer.update({'status':'ready','readyAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    if score:
        pointer['fidelityScore']=validate_score(score)
    write_pointer(root,pointer)
    return pointer


def status(root):
    root=Path(root)
    pointer=read_pointer(root)
    if not pointer:
        return {'root':str(root),'status':'ready' if (root/'manifest.json').is_file() else 'missing','capture':None}
    if capture_dir(root,pointer) is None:  # the folder went away: treat the cache as empty, say what the pointer named
        return {'root':str(root),'status':'missing','capture':None,'stale':pointer['capture']}
    return {'root':str(root),'status':pointer['status'],'capture':pointer['capture'],
            'promotedAt':pointer.get('promotedAt'),'readyAt':pointer.get('readyAt'),'fidelityScore':pointer.get('fidelityScore')}


def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in ('canonical','checksums','promote','mark-ready','status','-h','--help'):
        argv.insert(0,'promote')  # the original positional form: brand_cache.py <staging> --domain .. --workspace ..
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    sub=ap.add_subparsers(dest='cmd',required=True)
    k=sub.add_parser('canonical',help='print the canonical brand domain for a URL or hostname (lowercase, no www.)');k.add_argument('target')
    k.add_argument('--base',type=Path,default=Path.home()/'.octave/brands');k.add_argument('--workspace',help='also print the cache root for this workspace')
    c=sub.add_parser('checksums',help='write assetChecksums into the staging manifest');c.add_argument('staging',type=Path)
    p=sub.add_parser('promote',help='validate a staging capture and point the cache at it (status draft)');p.add_argument('staging',type=Path)
    p.add_argument('--base',type=Path,default=Path.home()/'.octave/brands')
    p.add_argument('--domain',required=True);p.add_argument('--workspace',required=True)
    p.add_argument('--status',choices=STATUSES,default='draft');p.add_argument('--write-checksums',action='store_true')
    m=sub.add_parser('mark-ready',help='flip the pointer to ready after the fidelity gate');m.add_argument('root',type=Path);m.add_argument('--score')
    s=sub.add_parser('status',help='show the pointer status of a cache root');s.add_argument('root',type=Path)
    args=ap.parse_args(argv)
    if args.cmd=='canonical':
        domain=canonical_domain(args.target)
        print(json.dumps({'domain':domain,'cacheRoot':str(cache_root(args.base,domain,args.workspace)) if args.workspace else None}))
    elif args.cmd=='checksums':print(f'{len(write_checksums(args.staging))} files catalogued in {args.staging/"manifest.json"}')
    elif args.cmd=='promote':
        target=promote(args.staging,args.base,args.domain,args.workspace,args.status,args.write_checksums)
        print(target);print(f'status: {args.status}'+(' (run the fidelity gate, then `brand_cache.py mark-ready` to publish for consumers)' if args.status=='draft' else ''))
    elif args.cmd=='mark-ready':print(json.dumps(mark_ready(args.root,args.score)))
    elif args.cmd=='status':print(json.dumps(status(args.root)))


if __name__=='__main__':
    try:main()
    except ValueError as error:sys.exit('ERROR: '+str(error))
