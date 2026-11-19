#!/usr/bin/env python3
"""Fail when a skill's shipped content changed but its catalog version did not.

Octave records a release only when a skill's catalog.json version goes up. A change
to a file a skill ships with, its own files or a shared file it links to, without a
version bump is skipped by the catalog sync, so workspaces never receive it. This
follows the same references the Octave catalog follows to build a skill's bundle
(markdown links, bare ./ and ../ paths, [plugin-root]/ paths), from every file under
skills/<name>/, and compares the files reached against a base revision.

    python3 scripts/check_release_bumps.py                    # base: the PR's base branch, else origin/main
    python3 scripts/check_release_bumps.py --base-ref <ref>
    python3 scripts/check_release_bumps.py --base-dir <checkout of the base>
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys

MARKDOWN_LINK_RE = re.compile(r'\]\(([^)\s]+?)(?:#[^)\s]*)?\)')
BARE_RELATIVE_REF_RE = re.compile(r'(?<![\w\-./(])(\.{1,2}/[\w\-./]+)(?![\w\-./])')
PLUGIN_ROOT = '[plugin-root]/'
PLUGIN_ROOT_REF_RE = re.compile(r'\[plugin-root\]/([\w\-./]+\.[A-Za-z0-9]+)(?![\w\-/\[]|\.[\w\-/])')


class Tree:
    """Read-only view of one revision's files: a directory, or a git ref."""

    def __init__(self, root=None, ref=None, repo=None):
        self.root, self.ref, self.repo = root, ref, repo
        if ref:
            out = subprocess.run(['git', 'ls-tree', '-r', '--name-only', ref], cwd=repo, capture_output=True, text=True, check=True)
            self.files = set(out.stdout.split('\n')) - {''}
        else:
            self.files = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}

    def read(self, path):
        if self.ref:
            out = subprocess.run(['git', 'show', f'{self.ref}:{path}'], cwd=self.repo, capture_output=True, check=True)
            return out.stdout
        return (self.root / path).read_bytes()


def external(target):
    return bool(re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I)) or target.startswith('#') or target.startswith('/')


def refs(markdown):
    found = set()
    for m in MARKDOWN_LINK_RE.finditer(markdown):
        if not external(m[1]):
            found.add(m[1])
    for m in BARE_RELATIVE_REF_RE.finditer(markdown):
        found.add(re.sub(r'[.,;:]+$', '', m[1]))
    for m in PLUGIN_ROOT_REF_RE.finditer(markdown):
        found.add(PLUGIN_ROOT + m[1])
    return found


def closure(tree, skill):
    """Every file the skill ships with at this revision, as {path: sha256}."""
    prefix = f'skills/{skill}/'
    queue = sorted(p for p in tree.files if p.startswith(prefix))
    seen = set(queue)
    hashes = {}
    while queue:
        path = queue.pop(0)
        raw = tree.read(path)
        hashes[path] = hashlib.sha256(raw).hexdigest()
        if not path.endswith('.md'):
            continue
        for ref in refs(raw.decode('utf-8', 'replace')):
            target = ref[len(PLUGIN_ROOT):] if ref.startswith(PLUGIN_ROOT) else posixpath.join(posixpath.dirname(path), ref)
            target = posixpath.normpath(target)
            # A sibling skill's SKILL.md is an invocation, not a bundled file.
            if target.startswith('skills/') and not target.startswith(prefix) and not target.startswith('skills/shared/') and PurePosixPath(target).name == 'SKILL.md':
                continue
            if target in tree.files and target not in seen:
                seen.add(target)
                queue.append(target)
    return hashes


def version_key(version):
    return tuple(int(part) for part in re.findall(r'\d+', version or '0'))


def check(head, base):
    errors = []
    head_catalog = json.loads(head.read('catalog.json'))['skills']
    base_catalog = json.loads(base.read('catalog.json'))['skills'] if 'catalog.json' in base.files else {}
    for name, entry in sorted(head_catalog.items()):
        if name not in base_catalog or f'skills/{name}/SKILL.md' not in base.files:
            continue
        if version_key(entry.get('version')) > version_key(base_catalog[name].get('version')):
            continue
        now, before = closure(head, name), closure(base, name)
        changed = sorted(p for p in set(now) | set(before) if now.get(p) != before.get(p))
        if changed:
            shown = ', '.join(changed[:3]) + (f' and {len(changed) - 3} more' if len(changed) > 3 else '')
            errors.append(f'catalog.json {name}: {shown} changed but the version is still {entry.get("version")}; bump it so Octave releases the change')
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--base-ref')
    group.add_argument('--base-dir', type=Path)
    args = ap.parse_args()
    head = Tree(root=args.root.resolve())
    if args.base_dir:
        base = Tree(root=args.base_dir.resolve())
    else:
        ref = args.base_ref or (f'origin/{os.environ["GITHUB_BASE_REF"]}' if os.environ.get('GITHUB_BASE_REF') else 'origin/main')
        probe = subprocess.run(['git', 'rev-parse', '--verify', '--quiet', ref], cwd=args.root, capture_output=True, text=True)
        if probe.returncode:
            print(f'SKIP: release bumps (no base revision {ref} to compare with)')
            return 0
        merge_base = subprocess.run(['git', 'merge-base', ref, 'HEAD'], cwd=args.root, capture_output=True, text=True)
        base = Tree(ref=(merge_base.stdout.strip() or ref), repo=args.root)
    errors = check(head, base)
    for error in errors:
        print('FAIL:', error)
    print(f'{"FAIL" if errors else "PASS"}: release bumps ({len(errors)} issues)')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
