#!/usr/bin/env python3
"""check_adherence.py — deterministic brand-adherence lint for generated HTML.

Answers "did this output actually use the kit?" WITHOUT spending model tokens:
scans a rendered HTML file for colors and font families that are not part of
the kit's token contract, plus a few structural tells (inline style overrides,
hotlinked assets). Run it BEFORE the visual fidelity gate — it catches drift
cheaply so the (expensive) multimodal scoring pass starts from a clean base.

  python3 check_adherence.py --file out.html --kit <slug|path> [--kit-dir <path>]

Exit codes: 0 = clean, 1 = violations found, 2 = usage/kit error.

What it checks
  colors   every #hex / rgb() literal in the file must be a kit color, a
           near-match of one (small RGB distance, covers AA-tweaked tints),
           or neutral (white/black/greys, transparent). Named CSS colors
           (`color:red`, `background:teal`) are always flagged.
  fonts    every font-family stack must lead with a kit family (or a declared
           fallback / generic).
  hotlink  remote image/media/script sources, stylesheets, and CSS URLs.
           A webfont stylesheet is allowed only when its URL matches
           render.webfonts; this exception does not certify self-containment.

Allowed values come only from the kit, including its theme overrides.
Output-defined custom properties cannot extend the allowed palette.
This is a source lint, not a CSS engine: it does not resolve the cascade,
variable references, arbitrary color syntax, or runtime-inserted assets.
The browser-based visual gate is still required.
"""
import argparse, json, pathlib, re, sys
from html.parser import HTMLParser

NEUTRAL_MAX_SPREAD = 16   # max(channel)-min(channel) ≤ this → grey/neutral, always allowed
NEAR_MATCH_DIST = 30      # euclidean RGB distance to a kit color that still counts as "on palette"
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "system-ui", "ui-sans-serif",
                    "ui-serif", "ui-monospace", "cursive", "fantasy", "emoji", "math",
                    "-apple-system", "blinkmacsystemfont", "segoe ui", "helvetica neue",
                    "helvetica", "arial", "georgia", "times new roman", "courier new",
                    "sf pro text", "sf pro display", "roboto", "inherit", "initial", "unset"}

HEX_RE = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b')
RGB_RE = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([\d.]+)\s*)?\)')
FAMILY_RE = re.compile(r'font-family\s*:\s*((?:"[^"]*"|\'[^\']*\'|[^;}"\'])+)')
VAR_RE = re.compile(r'(--[\w-]+)\s*:\s*([^;}]+)')
# named CSS colors that never belong in kit output (white/black/greys are fine)
NAMED_RE = re.compile(r'(?:^|[;:{\s"(])(?:color|background(?:-color)?|border-color|fill|stroke)\s*:\s*'
                      r'(red|blue|green|orange|purple|pink|yellow|teal|cyan|magenta|salmon|coral|'
                      r'gold|crimson|indigo|violet|lime|olive|navy|maroon|aqua|brown|tomato|'
                      r'orchid|plum|khaki|turquoise|steelblue|slateblue|seagreen|hotpink)\b')


def to_rgb(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def is_neutral(rgb):
    return max(rgb) - min(rgb) <= NEUTRAL_MAX_SPREAD


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def collect_colors(text):
    """All rgb tuples mentioned in a blob of CSS/JSON text."""
    out = set()
    for m in HEX_RE.finditer(text):
        out.add(to_rgb(m.group(0)))
    for m in RGB_RE.finditer(text):
        out.add(tuple(int(m.group(i)) for i in (1, 2, 3)))
    return out


def collect_families(text):
    """Lowercased first-position family names from font-family declarations."""
    fams = set()
    for m in FAMILY_RE.finditer(text):
        for fam in m.group(1).split(","):
            fams.add(fam.strip().strip("'\"").lower())
    return fams


def load_kit(slug_or_dir, kit_dir):
    if not (kit_dir or slug_or_dir):
        raise ValueError("provide --kit <slug|path> or --kit-dir <path>")
    d = pathlib.Path(kit_dir or slug_or_dir or "").expanduser()
    if not kit_dir and not d.exists() and not d.is_absolute() and '..' not in d.parts:
        d = pathlib.Path.home() / ".octave" / "brands" / (slug_or_dir or "")
    man_path = d / "manifest.json"
    if (d / "current.json").is_file():
        from brand_cache import resolve
        return resolve(d)
    if not man_path.exists():
        raise ValueError(f"no manifest.json under {d}")
    return d, json.loads(man_path.read_text())


class AssetScanner(HTMLParser):
    """Collect resource URLs and CSS without treating ordinary links as assets."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.assets = []
        self.css = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]
        if tag == "style":
            self.in_style = True
        if attrs.get("style"):
            self.css.append((line, attrs["style"]))
        for key in ("src", "poster"):
            if attrs.get(key):
                self.assets.append((line, attrs[key], False))
        # Remote srcset candidates, including extensionless image endpoints.
        for url in re.findall(r"(?:https?://|//)[^\s,]+", attrs.get("srcset") or "", re.I):
            self.assets.append((line, url, False))
        if tag == "link" and attrs.get("href"):
            rel = (attrs.get("rel") or "").lower().split()
            if any(r in rel for r in ("stylesheet", "icon", "preload", "modulepreload")):
                self.assets.append((line, attrs["href"], "stylesheet" in rel))
        if tag in ("image", "use"):
            for key in ("href", "xlink:href"):
                if attrs.get(key):
                    self.assets.append((line, attrs[key], False))

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.css.append((self.getpos()[0], data))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="rendered HTML to check")
    ap.add_argument("--kit", help="kit slug (~/.octave/brands/<slug>) or kit directory path")
    ap.add_argument("--kit-dir", dest="kit_dir", help="explicit kit directory (overrides --kit)")
    ap.add_argument("--max-report", type=int, default=25, help="cap reported violations per class")
    args = ap.parse_args()

    try:
        kitdir, man = load_kit(args.kit, args.kit_dir)
        html_text = pathlib.Path(args.file).read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # ---- build the allowed sets from the kit ----
    allowed_text = json.dumps(man.get("render", {}).get("tokens", {})) + json.dumps(man.get("tokens", {}))
    for theme in ("tokensDark", "tokensLight"):
        allowed_text += json.dumps(man.get("render", {}).get(theme, {}))
    tokens_css = kitdir / "tokens.css"
    if tokens_css.exists():
        allowed_text += tokens_css.read_text(errors="replace")
    allowed_colors = collect_colors(allowed_text)

    allowed_fams = set(GENERIC_FAMILIES)
    render = man.get("render", {})
    for f in render.get("fonts", []) or []:
        allowed_fams.add(str(f.get("family", "")).lower())
    fonts_meta = man.get("fonts", {}) or {}
    for k in ("heading", "body"):
        if fonts_meta.get(k):
            allowed_fams.add(str(fonts_meta[k]).lower())
    for tok_src in (render.get("tokens", {}), man.get("tokens", {})):
        for key, val in (tok_src or {}).items():
            if "font" in key:
                for fam in str(val).split(","):
                    allowed_fams.add(fam.strip().strip("'\"").lower())
    if tokens_css.exists():
        css = tokens_css.read_text(errors="replace")
        allowed_fams |= collect_families(css)
        for key, val in VAR_RE.findall(css):
            if key in ("--brand-font-heading", "--brand-font-body", "--brand-font-mono"):
                allowed_fams.update(f.strip().strip("'\"").lower() for f in val.split(","))

    violations = {"colors": [], "fonts": [], "hotlink": []}

    # ---- colors: skip data: URIs (embedded assets carry their own pixels) ----
    scannable = re.sub(r'url\(data:[^)]*\)|src="data:[^"]*"', "", html_text)
    seen = {}
    for m in HEX_RE.finditer(scannable):
        seen.setdefault(m.group(0).lower(), m.start())
    for m in RGB_RE.finditer(scannable):
        rgb = tuple(int(m.group(i)) for i in (1, 2, 3))
        seen.setdefault("rgb" + str(rgb), m.start())
    for literal, pos in seen.items():
        rgb = to_rgb(literal) if literal.startswith("#") else tuple(
            int(x) for x in re.findall(r"\d{1,3}", literal)[:3])
        if is_neutral(rgb):
            continue
        if any(dist(rgb, a) <= NEAR_MATCH_DIST for a in allowed_colors):
            continue
        line = scannable.count("\n", 0, pos) + 1
        violations["colors"].append(f"line {line}: {literal} is not in the kit palette")
    for m in NAMED_RE.finditer(scannable):
        line = scannable.count("\n", 0, m.start()) + 1
        violations["colors"].append(f"line {line}: named color '{m.group(1)}' — use a kit token")

    # ---- fonts ----
    for m in FAMILY_RE.finditer(scannable):
        first = m.group(1).split(",")[0].strip().strip("'\"").lower()
        if first.startswith("var(") or first in allowed_fams:
            continue
        line = scannable.count("\n", 0, m.start()) + 1
        violations["fonts"].append(f"line {line}: font-family leads with '{first}' (not a kit family)")

    # ---- remote resources in HTML attributes and CSS ----
    scanner = AssetScanner()
    scanner.feed(html_text)
    for line, css in scanner.css:
        css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group().count("\n"), css, flags=re.S)
        for m in re.finditer(r'''url\(\s*["']?((?:https?://|//)[^\s)'";]+)|@import\s+["']((?:https?://|//)[^"']+)''', css, re.I):
            scanner.assets.append((line + css.count("\n", 0, m.start()), m.group(1) or m.group(2), False))
    for line, url, stylesheet in scanner.assets:
        if stylesheet and url == render.get("webfonts"):
            continue
        if re.match(r"^(?:https?:)?//", url, re.I):
            violations["hotlink"].append(f"line {line}: hotlinked asset {url[:80]}")

    # ---- report ----
    total = sum(len(v) for v in violations.values())
    label = {"colors": "OFF-PALETTE COLORS", "fonts": "OFF-KIT FONTS",
             "hotlink": "HOTLINKED ASSETS"}
    print(f"adherence check — {args.file} vs kit '{kitdir.name}'")
    if total == 0:
        print("  CLEAN: no violations detected by source lint. Verify rendered fonts, styles, and asset loading in the visual gate.")
        return 0
    for key, items in violations.items():
        if not items:
            continue
        print(f"  {label[key]} ({len(items)}):")
        for v in items[:args.max_report]:
            print(f"    - {v}")
        if len(items) > args.max_report:
            print(f"    … and {len(items) - args.max_report} more")
    print(f"  TOTAL: {total} violation(s). Fix or justify each before the visual gate.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
