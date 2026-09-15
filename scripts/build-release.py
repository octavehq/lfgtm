#!/usr/bin/env python3
"""Build a public plugin ZIP from a deliberate runtime allowlist."""
import argparse
from pathlib import Path
import subprocess
import zipfile
from validate_package import validate

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('output',type=Path);args=ap.parse_args()
errors=validate(ROOT)
if errors:raise SystemExit('\n'.join(errors))
files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
single={'README.md','EXAMPLES.md','docs/validation.md','LICENSE','requirements-validation.txt','package.json','package-lock.json',
        'scripts/export-pdf.sh','scripts/deploy.sh','scripts/extract-pptx.py'}
selected=[p for p in files if p and (p in single or p.startswith(('.claude-plugin/','skills/','agents/','docs/org-instructions/')))
          and '/tests/' not in p and '/__pycache__/' not in p and not p.endswith('.pyc')]
args.output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(args.output,'w',zipfile.ZIP_DEFLATED) as archive:
    for name in sorted(selected):
        path=ROOT/name
        if path.is_symlink():raise ValueError('symlink in release allowlist: '+name)
        archive.write(path,name)
print(f'{args.output}: {len(selected)} tracked runtime files')
