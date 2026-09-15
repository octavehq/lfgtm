#!/usr/bin/env python3
"""Complete a generated plugin and map resource references to installed paths."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def complete(source, output, prefix):
    names = {p.name for p in (source / 'skills').iterdir() if (p / 'SKILL.md').is_file()}

    def mapped(path):
        parts = list(path.parts)
        if len(parts) > 1 and parts[0] == 'skills' and parts[1] in names:
            parts[1] = prefix + parts[1]
        return Path(*parts)

    for folder in ('agents',):
        shutil.copytree(source / folder, output / folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (output / 'scripts').mkdir(exist_ok=True)
    for name in ('export-pdf.sh', 'deploy.sh', 'extract-pptx.py'):
        shutil.copy2(source / 'scripts' / name, output / 'scripts' / name)
    shutil.copy2(source / 'LICENSE', output / 'LICENSE')
    shutil.copy2(source / 'requirements-validation.txt', output / 'requirements-validation.txt')
    for name in ('package.json', 'package-lock.json'):
        shutil.copy2(source / name, output / name)
    for folder in ('skills', 'agents'):
        for path in (source / folder).rglob('*.md'):
            relative = path.relative_to(source)
            destination = output / mapped(relative)
            if not destination.exists():
                continue
            text = destination.read_text()
            if prefix and path.name == 'SKILL.md':
                # Retain Claude autocomplete hints in source; Codex uses its own metadata.
                front, body = text.split('\n---\n', 1)
                front = re.sub(r'^argument-hint:.*\n?', '', front, flags=re.M)
                text = front + '\n---\n' + body

            def link(match):
                target = match.group(1)
                if re.match(r'(?:[a-z]+:|#|/|<)', target, re.I):
                    return match.group(0)
                base, sep, fragment = target.partition('#')
                resolved = (path.parent / base).resolve()
                if not resolved.exists() or not resolved.is_relative_to(source):
                    return match.group(0)
                new = os.path.relpath(output / mapped(resolved.relative_to(source)), destination.parent)
                return '](' + new + (sep + fragment if sep else '') + ')'

            text = re.sub(r'\]\(([^)]+)\)', link, text)
            if prefix:
                # Map only literal directory components, never ordinary prose.
                for name in sorted(names, key=len, reverse=True):
                    text = re.sub(r'(?<![\w-])((?:\.\./|skills/))' + re.escape(name) + r'(?=/)',
                                  lambda m: m[1] + prefix + name, text)
                text = re.sub(r'/octave:([a-z][a-z0-9-]*)', r'/octave-\1', text)
            destination.write_text(text)
    for path in list(output.rglob('__pycache__')):
        shutil.rmtree(path)
    for path in output.rglob('*.pyc'):
        path.unlink()
    manifest = {
        'schemaVersion': 1,
        'version': json.loads((source / '.claude-plugin/plugin.json').read_text())['version'],
        'sourceCommit': subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip(),
        'sourceDirty': bool(subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip()),
        'skillPaths': {f'skills/{n}': f'skills/{prefix}{n}' for n in sorted(names)},
        'resources': ['scripts', 'agents', 'LICENSE', 'requirements-validation.txt', 'package.json', 'package-lock.json'],
        'reviewFallback': 'skills/shared/host-runtime.md',
    }
    (output / 'package-resources.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--prefix', default='')
    args = parser.parse_args()
    complete(args.source.resolve(), args.output.resolve(), args.prefix)
