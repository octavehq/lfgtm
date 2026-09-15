#!/usr/bin/env python3
"""Check logo assets and produce a swatch for visual identity review."""
import argparse
import html
import json
from pathlib import Path
import re
import sys
from kit_validation import asset_path, svg_root, validate_manifest
from render_kit import logo_img
from brand_cache import resolve


def dimensions(path):
    if path.suffix.lower() == '.svg':
        root = svg_root(path.read_text())
        if root.get('viewBox'):
            values = [float(n) for n in re.split(r'[\s,]+', root.get('viewBox').strip())]
            if len(values) != 4:
                raise ValueError('SVG viewBox must have four numbers')
            w, h = values[2:]
        else:
            def number(value):
                if not value or not re.fullmatch(r'[\d.]+(?:px)?', value):
                    raise ValueError('SVG needs viewBox or numeric pixel dimensions')
                return float(value.removesuffix('px'))
            w, h = number(root.get('width')), number(root.get('height'))
    else:
        try:
            from PIL import Image
        except ImportError:
            raise RuntimeError('Pillow is required: python3 -m pip install Pillow')
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            w, h = image.size
    if min(w, h) <= 0:
        raise ValueError('logo dimensions must be nonzero')
    return w, h


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kit', type=Path)
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    root = args.kit.expanduser()
    if not root.is_dir():
        root = Path.home() / '.octave/brands' / args.kit
    root, man = resolve(root)
    render = validate_manifest(root, man)
    logo = render.get('logo') or {}
    ratios = []
    for surface in ('onLight', 'onDark'):
        if logo.get(surface):
            w, h = dimensions(asset_path(root, logo[surface])); ratios.append(w/h)
            print(f'{surface}: {logo[surface]} ({w:g} × {h:g})')
        elif not logo.get('lockup'):
            raise ValueError(f'missing {surface} variant or verified lockup')
    if len(ratios) == 2 and abs(ratios[0]-ratios[1])/max(ratios) > .15:
        raise ValueError('logo aspect ratios differ by more than 15%; inspect variants')
    company = html.escape(man.get('company', man.get('canonicalDomain', 'Brand')))
    swatch = args.out or root / '.logo-verify.html'
    swatch.parent.mkdir(parents=True, exist_ok=True)
    swatch.write_text(f'''<!DOCTYPE html><html lang="en"><meta charset="utf-8"><title>Logo check: {company}</title>
      <style>body{{font:16px sans-serif}}section{{padding:40px;min-height:120px}}.dark{{background:#111;color:white}}img{{max-width:100%;max-height:90px}}</style>
      <h1>{company}</h1><section>{logo_img(root, render, False, 60)}</section>
      <section class="dark">{logo_img(root, render, True, 60)}</section>
      <p>Mechanical checks passed. Visually verify identity, legibility, and source fidelity on both surfaces.</p></html>''')
    print(swatch)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError) as error:
        sys.exit('ERROR: ' + str(error))
