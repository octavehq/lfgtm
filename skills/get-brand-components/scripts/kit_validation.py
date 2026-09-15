"""Validation shared by brand rendering and cache verification."""
import hashlib
import math
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET


def asset_path(root, name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or '\\' in str(name):
        raise ValueError(f'kit asset path escapes root: {name}')
    target = root / p
    for part in [target, *target.parents]:
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError(f'kit asset symlink: {name}')
    if not target.resolve().is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f'missing or escaping kit asset: {name}')
    return target


def safe_url(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError('link requires a nonempty href')
    decoded = unquote(value)
    if re.search(r'[\x00-\x20\x7f\\]', decoded) or decoded.startswith('//'):
        raise ValueError('ambiguous link destination')
    parsed = urlsplit(decoded)
    if parsed.scheme and parsed.scheme.lower() not in ('https', 'http', 'mailto', 'tel'):
        raise ValueError('unsupported link scheme')
    if parsed.scheme in ('https', 'http') and (not parsed.hostname or parsed.username or parsed.password):
        raise ValueError('invalid HTTP destination')
    return value


def css_value(value):
    value = str(value)
    if re.search(r'[<>;{}\\]|/\*|@import|url\s*\(|expression\s*\(', value, re.I):
        raise ValueError('unsafe CSS token value')
    return value


ELEMENTS = set('svg g path rect circle ellipse line polyline polygon defs linearGradient radialGradient stop clipPath mask title desc use'.split())
ATTRS = set('id viewBox width height x y x1 y1 x2 y2 cx cy r rx ry d points fill fill-rule fill-opacity stroke stroke-width stroke-linecap stroke-linejoin stroke-miterlimit stroke-dasharray stroke-dashoffset stroke-opacity opacity transform gradientTransform gradientUnits offset stop-color stop-opacity clip-path clip-rule mask maskUnits preserveAspectRatio href role aria-label'.split())


def svg_root(raw):
    if re.search(r'<!DOCTYPE|<!ENTITY', raw, re.I):
        raise ValueError('SVG declarations are not allowed')
    tree = ET.fromstring(raw)
    for el in tree.iter():
        tag = el.tag.split('}')[-1]
        if tag not in ELEMENTS:
            raise ValueError(f'unsupported SVG element: {tag}')
        for key, value in el.attrib.items():
            key = key.split('}')[-1]
            if key not in ATTRS:
                raise ValueError(f'unsupported SVG attribute: {key}')
            if key == 'href' and not re.fullmatch(r'#[\w.-]+', value):
                raise ValueError('SVG references must be internal fragments')
            if re.search(r'url\s*\(', value, re.I) and not re.fullmatch(r'url\(#[\w.-]+\)', value):
                raise ValueError('external SVG paint reference')
            if re.search(r'javascript:|data:|https?:|[<>]', value, re.I):
                raise ValueError('unsafe SVG attribute value')
    return tree


def validate_manifest(root, man, expected_domain=None, workspace=None):
    if expected_domain and man.get('canonicalDomain') != expected_domain.lower().rstrip('.'):
        raise ValueError('brand domain identity mismatch')
    if workspace and man.get('workspaceOId') != workspace:
        raise ValueError('brand workspace identity mismatch')
    render = man.get('render')
    if not isinstance(render, dict) or not isinstance(render.get('tokens'), dict):
        raise ValueError('manifest requires render.tokens')
    required = {'--brand-bg', '--brand-ink', '--brand-primary', '--brand-font-heading', '--brand-font-body'}
    if required - render['tokens'].keys():
        raise ValueError('missing required render tokens: ' + ', '.join(sorted(required - render['tokens'].keys())))
    width = render.get('docWidth', 880)
    if not isinstance(width, (int, float)) or not math.isfinite(width) or width <= 0:
        raise ValueError('docWidth must be a positive finite number')
    if render.get('webfonts'):
        if urlsplit(safe_url(render['webfonts'])).scheme not in ('http', 'https'):
            raise ValueError('webfonts requires an HTTP(S) stylesheet')
    for group in ('tokens', 'tokensDark', 'tokensLight'):
        for key, value in render.get(group, {}).items():
            if not re.fullmatch(r'--brand-[\w-]+', key):
                raise ValueError(f'invalid token name: {key}')
            css_value(value)
    for font in render.get('fonts', []):
        asset_path(root, font['file'])
        if font.get('format', Path(font['file']).suffix.lstrip('.')) not in ('woff', 'woff2', 'ttf', 'opentype'):
            raise ValueError('unsupported font format')
        for key in ('family', 'weight', 'style', 'format'):
            if key in font:
                css_value(font[key])
        if "'" in font.get('family', ''):
            raise ValueError('font family must not contain CSS quotes')
    logo = render.get('logo') or {}
    for name in [logo.get('onDark'), logo.get('onLight'), *((logo.get('lockup') or {}).get(k) for k in ('mark', 'markImg'))]:
        if name:
            p = asset_path(root, name)
            if p.suffix.lower() == '.svg':
                svg_root(p.read_text())
    for name, digest in man.get('assetChecksums', {}).items():
        if hashlib.sha256(asset_path(root, name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'asset checksum mismatch: {name}')
    return render
