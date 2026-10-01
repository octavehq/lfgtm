#!/usr/bin/env python3
"""render_gallery.py — build a kit's components.html mechanically from its manifest.

The capture model writes manifest.json (with the render contract), tokens.css
and brand-kit.md; this post-step composes the gallery through the skill's
shared renderer so the gallery is always renderable, consistent across brands,
and never hand-written. Also prepends a token/type swatch strip so humans can
read the palette and faces at a glance.

  render_gallery.py <kit-dir> [--skill-scripts <path to get-brand-components/scripts>]
"""
import argparse, html, json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
SPEC = HERE.parent / "assets" / "gallery_spec.json"


def swatches(man):
    r = man.get("render", {})
    toks = r.get("tokens", {})
    color_keys = [k for k in toks if any(x in k for x in ("-bg", "-ink", "-primary", "-accent", "-surface", "-muted", "-border", "-on-dark", "-band", "-canvas", "-link", "-positive", "-negative", "-success", "-warning", "-error")) and "font" not in k]
    cells = ""
    for k in color_keys[:24]:
        v = toks[k]
        cells += (f'<div style="width:112px"><div style="height:44px;border-radius:8px;border:1px solid #e5e5e5;background:{html.escape(v)}"></div>'
                  f'<div style="font:11px/1.3 ui-monospace,monospace;color:#444;margin-top:4px;word-break:break-all">{html.escape(k.replace("--brand-", ""))}<br>{html.escape(v[:28])}</div></div>')
    fh = toks.get("--brand-font-heading", "inherit"); fb = toks.get("--brand-font-body", "inherit")
    wh = toks.get("--brand-weight-heading", "600"); wb = toks.get("--brand-weight-body", "400")
    fonts = ", ".join(f"{f.get('family')} {f.get('weight')}" for f in r.get("fonts", [])[:8]) or "none embedded"
    rules = "".join(f"<li>{html.escape(str(x))}</li>" for x in (man.get("rules") or [])[:6])
    return (f'<section style="background:#fff;color:#111;padding:28px 40px;border-bottom:1px solid #e5e5e5;font-family:system-ui">'
            f'<div style="font:600 12px/1 system-ui;letter-spacing:.08em;text-transform:uppercase;color:#777;margin-bottom:12px">Kit reference: {html.escape(man.get("company", ""))} ({html.escape(man.get("domain", ""))})</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px">{cells}</div>'
            f'<div style="font-family:{html.escape(fh)};font-weight:{html.escape(str(wh))};font-size:40px;line-height:1.1;letter-spacing:{html.escape(toks.get("--brand-tracking-heading", "0"))}">Heading face at real size</div>'
            f'<div style="font-family:{html.escape(fb)};font-weight:{html.escape(str(wb))};font-size:17px;line-height:1.6;max-width:640px;margin-top:8px">Body face at real size. Embedded: {html.escape(fonts)}.</div>'
            f'{"<ul style=\"font:13px/1.5 system-ui;color:#333;margin-top:14px\">" + rules + "</ul>" if rules else ""}'
            f'</section>')


SURFACE_BLOCKS = ("hero", "stats", "quote", "cta", "footer", "comparison", "logos")


def composed_spec(man, tmp_path):
    """Apply the kit's optional `render.gallery` composition (which bands are dark or light) to the fixed spec."""
    spec = json.loads(SPEC.read_text())
    g = (man.get("render") or {}).get("gallery") or {}
    surfaces = g.get("surfaces") or {}
    for block in spec["blocks"]:
        s = surfaces.get(block["type"])
        if block["type"] in SURFACE_BLOCKS and s in ("dark", "light"):
            block["surface"] = s
    tmp_path.write_text(json.dumps(spec))
    return tmp_path


def swap_bespoke_hero(doc, kit):
    """If the capture wrote an optional hero.html (a self-contained section in the site's own section
    grammar, styled only with --brand-* tokens), it replaces the mechanical hero block. Kit-relative
    <img src> paths are inlined as data URIs so the gallery stays self-contained; remote URLs are refused."""
    import base64, re
    hero = kit / "hero.html"
    if not hero.is_file():
        return doc
    frag = hero.read_text()
    if re.search(r"(?:src|href)\s*=\s*['\"]?(?:https?:)?//", frag) or "@import" in frag or "<script" in frag.lower():
        print("hero.html refused: external resource or script"); return doc
    def inline(m):
        p = (kit / m.group(2)).resolve()
        if not p.is_file() or kit.resolve() not in p.parents: return m.group(0)
        mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(p.suffix.lstrip(".").lower(), "application/octet-stream")
        return f'src={m.group(1)}data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}{m.group(1)}'
    frag = re.sub(r'src=(["\'])([^"\']+)\1', inline, frag)
    m = re.search(r'<div class="hero[^"]*".*?(?=<div class="(?:stats|wrap|band|cta|footer)[\s"])', doc, re.S)
    if not m:
        print("mechanical hero not found; hero.html ignored"); return doc
    return doc[:m.start()] + frag + doc[m.end():]


def composition_css(man):
    """Layout knobs the renderer has no token for: heading alignment, card style, nav style."""
    g = (man.get("render") or {}).get("gallery") or {}
    css = []
    if g.get("headingAlign") == "center":
        css.append(".hero .copy,.section,.cta,.quote{text-align:center}.hero .copy{margin:0 auto;max-width:760px}"
                   ".hero .actions,.section h2,.section p{margin-left:auto;margin-right:auto}.section p{max-width:640px}.feat{justify-content:center}")
    card = g.get("cardStyle")
    if card == "hairline":
        css.append(".fcard,.plan,.cmp-soft,.about{box-shadow:none;border:1px solid var(--brand-border)}")
    elif card == "flat":
        css.append(".fcard,.plan,.about{box-shadow:none;border:0;background:var(--brand-bg-alt,var(--brand-surface))}")
    elif card == "shadow":
        css.append(".fcard,.plan{border:0;box-shadow:var(--brand-shadow-md,var(--brand-shadow))}")
    if g.get("navStyle") == "floating":
        css.append(".topbar{margin:14px 18px 0;padding:10px 18px;border-radius:var(--brand-radius-pill,999px);"
                   "background:var(--brand-surface);color:var(--brand-ink);box-shadow:var(--brand-shadow-sm,0 1px 2px rgba(0,0,0,.08))}"
                   ".is-dark .topbar .nav a{color:var(--brand-ink)}")
    if g.get("sectionFrame") == "hairline":
        css.append(".wrap > *{border-top:1px solid var(--brand-border);padding-top:28px}")
    return ("<style data-composition>" + "".join(css) + "</style>") if css else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit", type=pathlib.Path)
    ap.add_argument("--skill-scripts", type=pathlib.Path, default=HERE)
    args = ap.parse_args()
    kit = args.kit
    man = json.loads((kit / "manifest.json").read_text())
    out = kit / "components.html"
    spec_path = composed_spec(man, kit / ".gallery_spec.json")
    r = subprocess.run([sys.executable, str(args.skill_scripts / "render_kit.py"), "--kit-dir", str(kit), "--spec", str(spec_path), "--out", str(out)],
                       capture_output=True, text=True)
    spec_path.unlink(missing_ok=True)
    if r.returncode != 0:
        print("render_kit failed:", (r.stderr or r.stdout)[-800:]); sys.exit(1)
    doc = out.read_text()
    doc = swap_bespoke_hero(doc, kit)
    # composition overrides go after the renderer's stylesheet; the reference strip at the end of <body>
    head_end = doc.find("</head>")
    if head_end > 0:
        doc = doc[:head_end] + composition_css(man) + doc[head_end:]
    j = doc.rfind("</body>")
    if j > 0:
        doc = doc[:j] + swatches(man) + doc[j:]
    out.write_text(doc)
    print(f"components.html {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
