#!/usr/bin/env python3
"""Validate shipped dependency closure and public package hygiene."""
import argparse
import json
from pathlib import Path
import re
import sys
import yaml


def validate(root):
    root=Path(root).resolve();errors=[]
    skills=list((root/'skills').glob('*/SKILL.md'))
    if len(skills)!=29:errors.append(f'expected 29 skills, found {len(skills)}')
    if len(list((root/'agents').glob('*.md')))!=7:errors.append('expected seven agent resources')
    for name in ('scripts/export-pdf.sh','scripts/deploy.sh','scripts/extract-pptx.py','LICENSE','skills/shared/host-runtime.md'):
        if not (root/name).is_file():errors.append('missing runtime resource: '+name)
    for path in skills:
        text=path.read_text()
        match=re.match(r'---\n(.*?)\n---\n',text,re.S)
        try:
            data=yaml.safe_load(match[1]) if match else None
            if not isinstance(data,dict) or not re.fullmatch(r'[a-z0-9-]+',data.get('name','')) or not isinstance(data.get('description'),str) or not 1 <= len(data['description']) <= 1024:
                raise ValueError('invalid name or description')
            if (root/'.codex-plugin').exists() and 'argument-hint' in data:
                raise ValueError('Claude argument-hint must be removed from Codex frontmatter')
        except (ValueError,yaml.YAMLError) as error:
            errors.append(f'invalid skill frontmatter: {path.relative_to(root)}: {error}')
    for path in [*(root/'skills').rglob('*.md'),*(root/'agents').rglob('*.md')]:
        text=path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'(?:[a-z][\w+.-]*:|#|/|<)',target,re.I) or any(x in target for x in ('<','>','{','}')):continue
            base=target.split('#')[0]
            if not base:continue
            resolved=(path.parent/base).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():errors.append(f'{path.relative_to(root)}: missing link {target}')
        if re.search(r'/Users/(?!<)[^/\s]+/|/home/(?!<)[^/\s]+/',text):errors.append(f'personal filesystem path: {path.relative_to(root)}')
    plugin=root/'.claude-plugin/plugin.json'
    marketplace=root/'.claude-plugin/marketplace.json'
    if plugin.exists() and marketplace.exists():
        version=json.loads(plugin.read_text())['version']
        for item in json.loads(marketplace.read_text())['plugins']:
            if item['name']=='octave' and item.get('version')!=version:errors.append('plugin/marketplace version mismatch')
    return errors


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path,nargs='?',default=Path(__file__).resolve().parents[1])
    args=ap.parse_args();errors=validate(args.root)
    for error in errors:print('FAIL:',error)
    print(f'{"FAIL" if errors else "PASS"}: package structure and resource links ({len(errors)} issues)')
    sys.exit(bool(errors))
