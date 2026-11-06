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


SVG_MARKUP_TAG = re.compile(r'<(/?)([A-Za-z][\w:.-]*)((?:\s+[^\s=>/]+(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s"\'>]+))?)*)\s*(/?)>')
SVG_MARKUP_ATTR = re.compile(r'([^\s=>/]+)(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s"\'>]+))?')


def _safe_svg_value(value):
    if re.search(r'url\s*\(', value, re.I) and not re.fullmatch(r'url\(#[\w.-]+\)', value.strip()):
        return False
    return not re.search(r'javascript:|data:|https?:|[<>]|expression\s*\(', value, re.I)


def sanitize_svg_markup(raw):
    """Icon markup the renderer accepts: style declarations it allows become presentation attributes, and style,
    class, data-* and every other attribute outside ATTRS are dropped. Raises ValueError on an element outside
    ELEMENTS, so a caller can skip that icon. svg_root still validates the result."""
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    if re.search(r'<!|<\?', raw):
        raise ValueError('SVG declarations are not allowed')

    def tag(m):
        closing, name, attrs, selfclose = m.groups()
        if name.split(':')[-1] not in ELEMENTS:
            raise ValueError(f'unsupported SVG element: {name}')
        if closing:
            return f'</{name}>'
        kept, styled = {}, {}
        for am in SVG_MARKUP_ATTR.finditer(attrs or ''):
            key, value = am.group(1), am.group(2) or ''
            if value[:1] in ('"', "'"):
                value = value[1:-1]
            if key == 'xlink:href':
                key = 'href'
            if key == 'style':
                for decl in value.split(';'):
                    prop, _, val = decl.partition(':')
                    prop, val = prop.strip(), val.strip()
                    # a CSS transform uses units and functions the transform attribute does not, so it is dropped
                    if prop in ATTRS and prop != 'transform' and val and _safe_svg_value(val):
                        styled[prop] = val
            elif key in ATTRS:
                kept[key] = value
        for prop, val in styled.items():  # an inline style beats the attribute it shadows, as in a browser
            kept[prop] = val
        out = ''.join(f' {k}="{v.replace(chr(34), "&quot;")}"' for k, v in kept.items())
        return f'<{name}{out}{"/" if selfclose else ""}>'

    return SVG_MARKUP_TAG.sub(tag, raw)


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


# ─── Surfaces ───────────────────────────────────────────────────────────

# Two colors read as different surfaces at this contrast ratio, or, between two dark colors where
# the ratio barely moves, at this distance in RGB (a raised navy card on a navy page is about 29).
SURFACE_RATIO = 1.25
SURFACE_DISTANCE = 24
# A surface with a relative luminance under this reads as dark.
DARK_LUMINANCE = 0.4
# The tokens that may carry a kit's second surface, in the order a document prefers them.
SECOND_SURFACE_TOKENS = ('--brand-band', '--brand-surface-dark', '--brand-bg-alt', '--brand-surface', '--brand-canvas')


def first_hex(value):
    """The first hex color in a token value as (r, g, b), so a gradient gives its first stop; None without one."""
    m = re.search(r'#([0-9a-f]{6}|[0-9a-f]{3})\b', str(value or ''), re.I)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def lin(c):
        v = c / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def distinct_surfaces(a, b):
    """Whether two colors read as different surfaces (see SURFACE_RATIO and SURFACE_DISTANCE)."""
    distance = sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
    return contrast(a, b) >= SURFACE_RATIO or distance >= SURFACE_DISTANCE


def surface_issues(render):
    """What keeps a kit from branding a document, as plain lines; empty when nothing does.

    A document (a deck, a magazine, a one-pager) alternates two surfaces: the page and a field for
    its cover and bands. So every kit names a second surface that visibly differs from --brand-bg,
    and a kit with any dark surface carries the mark for it (logo.onDark) and the ink on it
    (--brand-on-dark). A site captured as one dark navy throughout fails here until the author
    gives it a raised surface.
    """
    tokens = render.get('tokens') or {}
    logo = render.get('logo') or {}
    issues = []
    if not logo.get('onLight'):
        issues.append('render.logo.onLight is required: the mark for a light surface')
    bg = first_hex(tokens.get('--brand-bg'))
    if bg is None:
        return issues
    seconds = []
    for key in SECOND_SURFACE_TOKENS:
        color = first_hex(tokens.get(key))
        if color and distinct_surfaces(bg, color):
            seconds.append(color)
    if not seconds:
        issues.append('one surface only: none of ' + ', '.join(SECOND_SURFACE_TOKENS) + ' reads as a different surface from --brand-bg; a document needs a second surface for its cover and bands (a dark band for a light brand, a raised surface for a dark one)')
    if luminance(bg) < DARK_LUMINANCE or any(luminance(c) < DARK_LUMINANCE for c in seconds):
        if not logo.get('onDark'):
            issues.append('a kit with a dark surface needs render.logo.onDark, the mark for that surface')
        if '--brand-on-dark' not in tokens:
            issues.append('--brand-on-dark is required when the kit has a dark surface: the ink on it')
    return issues


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
        if font.get('format', Path(font['file']).suffix.lstrip('.')) not in ('woff', 'woff2', 'ttf', 'truetype', 'otf', 'opentype'):
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
    if render.get('heroImage'):
        p = asset_path(root, render['heroImage'])
        if p.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.svg'):
            raise ValueError('heroImage must be a png, jpg, webp or svg file')
        if p.suffix.lower() == '.svg':
            svg_root(p.read_text())
    for name, digest in man.get('assetChecksums', {}).items():
        if hashlib.sha256(asset_path(root, name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'asset checksum mismatch: {name}')
    return render


if __name__ == '__main__':
    import json
    import sys
    kit = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if kit is None or not (kit / 'manifest.json').exists():
        print('usage: kit_validation.py <kit-dir>  (prints what keeps the kit from branding a document)', file=sys.stderr)
        sys.exit(2)
    found = surface_issues(json.loads((kit / 'manifest.json').read_text()).get('render') or {})
    for line in found:
        print('- ' + line)
    print('ok: two surfaces and the logos a document needs' if not found else f'{len(found)} issue(s)')
    sys.exit(1 if found else 0)
