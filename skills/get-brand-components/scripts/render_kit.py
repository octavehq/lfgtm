#!/usr/bin/env python3
"""render_kit.py — compose on-brand HTML collateral from a cached brand kit.

The renderer is generic: ALL styling comes from the kit (token contract in
manifest.json -> `render`, + the shared assets/kit_base.css). Content is a
declarative JSON spec of blocks. One renderer, every brand — no per-asset CSS.

  python3 render_kit.py --kit acme --spec case_study.json --out out.html

Kit dir: ~/.octave/brands/<slug>/ with manifest.json containing a `render` block:
  render: {
    hasDarkBand: bool, docWidth: px, heroVisual: "chips"|"masonry"|"none",
    tokens: { "--brand-*": "value", ... },          # the token contract
    fonts:  [ {family,weight,style?,file,format} ],  # embedded base64 @font-face
    logo:   { onDark: file|null, onLight: file|null, lockup: {...}|null }
  }

Spec: { title, blocks: [ {type: hero|stats|about|quote|section|features|comparison|checklist|cta|footer, ...} ] }
Emphasis: wrap a word in **double asterisks** -> <span class="hl">.
comparison: defaults to a gradient-band header table; on light brands (no dark band)
  it auto-falls back to a soft table; set "variant":"diptych" for the luminous split panel.
"""
import argparse, base64, html, json, os, pathlib, re, sys

BRANDS = pathlib.Path.home() / ".octave" / "brands"
SKILL = pathlib.Path(__file__).resolve().parent.parent
WRAP_BLOCKS = {"about", "quote", "section", "features", "comparison", "checklist",
               "split", "logos", "pricing"}  # go inside .wrap


def load_kit(slug_or_dir):
    """Accept a slug (-> ~/.octave/brands/<slug>) or an explicit kit directory path."""
    d = pathlib.Path(slug_or_dir).expanduser()
    if not (d.is_absolute() or d.exists()):
        d = BRANDS / slug_or_dir
    man = json.loads((d / "manifest.json").read_text())
    if "render" not in man:
        sys.exit(f"ERROR: {d}/manifest.json has no `render` block. Add the token contract first.")
    return d, man["render"]


def b64_file(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def font_faces(kitdir, fonts):
    out = []
    fmt_mime = {"woff2": "font/woff2", "woff": "font/woff", "ttf": "font/ttf"}
    for f in fonts or []:
        p = kitdir / f["file"]
        if not p.exists():
            continue
        fmt = f.get("format") or p.suffix.lstrip(".")
        uri = b64_file(p, fmt_mime.get(fmt, "font/woff2"))
        style = f.get("style", "normal")
        out.append(f"@font-face{{font-family:'{f['family']}';src:url({uri}) format('{fmt}');"
                   f"font-weight:{f['weight']};font-style:{style};font-display:swap;}}")
    return "\n".join(out)


def logo_img(kitdir, render, dark, height=None):
    """Return an <img>/lockup for the right surface, or '' if none."""
    lg = render.get("logo") or {}
    fname = lg.get("onDark") if dark else lg.get("onLight")
    style = f'style="height:{height}px;width:auto;display:block;"' if height else 'style="display:block;"'
    if fname:
        p = kitdir / fname
        mime = "image/svg+xml" if p.suffix == ".svg" else f"image/{p.suffix.lstrip('.')}"
        return f'<img src="{b64_file(p, mime)}" alt="logo" {style}>'
    lk = lg.get("lockup")
    if lk:  # mark + wordmark text in heading font
        h = height or 28
        if lk.get("markImg"):  # raster/colored mark used as an <img> (keeps its real colors)
            mp = kitdir / lk["markImg"]
            mime = "image/svg+xml" if mp.suffix == ".svg" else f"image/{mp.suffix.lstrip('.')}"
            mark_html = f'<img src="{b64_file(mp, mime)}" alt="" style="height:{h}px;width:auto;display:block;">'
        else:  # single-path svg mark, recolored per surface
            mark = (kitdir / lk["mark"]).read_text()
            fill = "#fff" if dark else lk.get("markFill", "currentColor")
            d = re.search(r'd="([^"]+)"', mark)
            vb = re.search(r'viewBox="([^"]+)"', mark)
            mark_html = (f'<svg viewBox="{vb.group(1) if vb else "0 0 24 24"}" width="{h}" height="{h}" '
                         f'aria-label="logo"><path fill="{fill}" d="{d.group(1)}"/></svg>')
        wc = ("#fff" if dark else lk.get("wordmarkColor", "var(--brand-ink)"))
        tt = lk.get("wordmarkTransform", "none")
        return (f'<span style="display:inline-flex;align-items:center;gap:10px;">{mark_html}'
                f'<span style="font-family:var(--brand-font-heading);font-weight:{lk.get("wordmarkWeight",700)};'
                f'font-size:{round(h*0.82)}px;letter-spacing:-0.01em;text-transform:{tt};color:{wc};">{lk["wordmark"]}</span></span>')
    return ""


def inline_img(kitdir, ref, attrs=""):
    """Inline an image as a data-URI so the output stays self-contained.
    Kit-relative paths are read from disk; remote URLs are downloaded and inlined
    (never hotlinked). Returns '' with a stderr warning if the image can't be sourced."""
    if ref.startswith("http"):
        import urllib.request
        try:
            req = urllib.request.Request(ref, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
                mime = r.headers.get_content_type() or "image/png"
            uri = f"data:{mime};base64," + base64.b64encode(data).decode()
            return f'<img src="{uri}" {attrs} alt="">'
        except Exception as e:
            print(f"WARNING: could not download image {ref} ({e}) — omitted to keep output self-contained.",
                  file=sys.stderr)
            return ""
    p = kitdir / ref
    mime = "image/svg+xml" if p.suffix == ".svg" else f"image/{p.suffix.lstrip('.')}"
    return f'<img src="{b64_file(p, mime)}" {attrs} alt="">'


def icon_svg(kitdir, name_or_raw, kit_icons):
    if isinstance(name_or_raw, dict):  # raw {viewBox, inner}
        vb, inner = name_or_raw.get("viewBox", "0 0 24 24"), name_or_raw["inner"]
    elif name_or_raw in kit_icons:
        vb, inner = kit_icons[name_or_raw]["viewBox"], kit_icons[name_or_raw]["inner"]
    else:
        return ""  # unknown icon -> empty (tile still renders)
    return (f'<svg viewBox="{vb}" width="22" height="22" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')


ARROW = ('<svg class="arw" viewBox="0 0 16 17" fill="none" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M0.6 8.5H15.4"/>'
         '<path d="M11.4 12.5L15.4 8.5 11.4 4.5"/></svg>')

# soft wave divider so a dark band curves into the light body (fill set via CSS to --brand-bg)
WAVE = ('<svg class="wave" viewBox="0 0 1440 44" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0,44 V20 C480,0 960,0 1440,20 V44 Z"/></svg>')


def emph(text):
    """**word** -> <span class=hl>word</span>; escape the rest."""
    parts = re.split(r'\*\*(.+?)\*\*', text)
    out = ""
    for i, seg in enumerate(parts):
        out += f'<span class="hl">{html.escape(seg)}</span>' if i % 2 else html.escape(seg)
    return out


def para(text):  # body copy: escape, keep simple
    return html.escape(text)


# ---- block renderers ----
def r_hero(b, ctx):
    dark = b.get("surface", "dark" if ctx["darkband"] else "light") == "dark"
    cls = "hero is-dark" if dark else "hero"
    kd, render = ctx["kitdir"], ctx["render"]
    brand = logo_img(kd, render, dark, height=28)
    nav = ""
    if b.get("nav"):
        items = "".join(f'<span>{html.escape(x)}</span>' for x in b["nav"].get("links", []))
        if b["nav"].get("cta"):
            items += f'<span class="cta-pill">{html.escape(b["nav"]["cta"])}</span>'
        nav = f'<div class="nav">{items}</div>'
    top = f'<div class="topbar"><div class="brand">{brand}</div>{nav}</div>'
    cta = f'<a class="btn btn-primary">{html.escape(b["cta"]["label"])} {ARROW}</a>' if b.get("cta") else ""
    eyebrow = f'<div class="eyebrow">{html.escape(b["eyebrow"])}</div>' if b.get("eyebrow") else ""
    copy = (f'<div class="copy">{eyebrow}<h1>{emph(b["title"])}</h1>'
            f'<p class="lead">{para(b["lead"])}</p>'
            f'<div class="actions">{cta}</div></div>') if b.get("lead") else \
           (f'<div class="copy">{eyebrow}<h1>{emph(b["title"])}</h1><div class="actions">{cta}</div></div>')
    # featured customer logo (possibly from another kit) — degrade gracefully if that kit is missing
    cust = ""
    if b.get("featured"):
        fk = b["featured"].get("logoKit", ctx["slug"])
        try:
            fkd, frender = load_kit(fk)
            flogo = logo_img(fkd, frender, dark=True, height=30)
            cust = (f'<div class="cust"><span class="lab">{html.escape(b["featured"].get("label","Customer"))}</span>{flogo}</div>')
        except (Exception, SystemExit) as e:
            print(f"WARNING: featured logo kit '{fk}' unavailable ({e}) — omitting the featured customer logo.",
                  file=sys.stderr)
    # visual
    visual = ""
    vis = b.get("visual", render.get("heroVisual", "none"))
    if vis == "chips" and b.get("chips"):
        chips = ""
        for i, c in enumerate(b["chips"]):
            ico = icon_svg(ctx["kitdir"], c.get("icon", {}), ctx["icons"])
            chips += (f'<div class="chip{" off" if i==1 else ""}"><div class="ci">{ico}</div>'
                      f'<div><div class="ct">{html.escape(c["title"])}</div>'
                      f'<div class="cs">{html.escape(c.get("sub",""))}</div></div></div>')
        visual = f'<div class="chips">{chips}</div>'
    elif vis == "masonry":
        cells = "".join(f'<div class="m" style="height:{h}px;background:{bg}"></div>'
                        for h, bg in b.get("masonry", []))
        visual = f'<div class="masonry">{cells}</div>'
    inner = f'<div class="lede">{copy}<div class="visual">{visual}</div></div>' if visual else copy
    return f'<div class="{cls}">{top}{inner}{cust}</div>'


def r_stats(b, ctx):
    on_light = b.get("surface") == "light"
    wave = b.get("divider") == "wave"
    cells = "".join(f'<div class="stat"><div class="n">{html.escape(s["n"])}'
                    f'<span class="u">{html.escape(s.get("u",""))}</span></div>'
                    f'<div class="l">{html.escape(s["l"])}</div></div>' for s in b["items"])
    cls = "stats" + (" on-light" if on_light else "") + (" has-wave" if wave else "")
    return f'<div class="{cls}">{cells}{WAVE if wave else ""}</div>'


def r_about(b, ctx):
    facts = "".join(f'<dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd>' for k, v in b.get("facts", []))
    dl = f'<dl>{facts}</dl>' if facts else ""
    title = f'<div class="k">{html.escape(b["title"])}</div>' if b.get("title") else ""
    return f'<div class="about">{title}<p>{para(b["body"])}</p>{dl}</div>'


def r_quote(b, ctx):
    who = f'<div class="who"><b>{html.escape(b.get("name",""))}</b>{html.escape(b.get("role",""))}</div>'
    return (f'<div class="quote is-dark"><div class="mark">&ldquo;</div>'
            f'<p>{para(b["text"])}</p>{who}</div>')


def r_section(b, ctx):
    k = f'<div class="k">{html.escape(b["kicker"])}</div>' if b.get("kicker") else ""
    h = f'<h2>{emph(b["heading"])}</h2>' if b.get("heading") else ""
    ps = "".join(f'<p>{para(p)}</p>' for p in b.get("paras", []))
    return f'<div class="section">{k}{h}{ps}</div>'


def r_features(b, ctx):
    cards = ""
    for it in b["items"]:
        ico = icon_svg(ctx["kitdir"], it.get("icon", {}), ctx["icons"])
        cards += (f'<div class="fcard"><div class="tile">{ico}</div>'
                  f'<h3>{html.escape(it["title"])}</h3><p>{para(it["text"])}</p></div>')
    return f'<div class="feat">{cards}</div>'


def _cmp_band(bad, good, rows):  # B1 — gradient-band header table (dark-band brands)
    head = (f'<div class="head"><div class="c bad">{bad}</div>'
            f'<div class="c good"><span class="gdot"></span>{good}</div></div>')
    body = ""
    for i, r in enumerate(rows):
        last = " last" if i == len(rows) - 1 else ""
        body += (f'<div class="r{last}"><div class="c bad"><span class="m">&times;</span>{para(r[0])}</div>'
                 f'<div class="c good"><span class="m">&#10003;</span>{para(r[1])}</div></div>')
    return f'<div class="cmp cmp-band">{head}{body}</div>'


def _cmp_soft(bad, good, rows):  # B2 — refined soft table (light-brand fallback)
    body = (f'<div class="r head"><div class="c bad">{bad}</div><div class="c good">{good}</div></div>')
    for i, r in enumerate(rows):
        z = " alt" if i % 2 else ""
        body += (f'<div class="r{z}"><div class="c bad"><span class="m">&times;</span>{para(r[0])}</div>'
                 f'<div class="c good"><span class="m">&#10003;</span>{para(r[1])}</div></div>')
    return f'<div class="cmp cmp-soft">{body}</div>'


def _cmp_diptych(bad, good, rows):  # D1 — luminous diptych (variant)
    L = "".join(f'<li><span class="m">&times;</span>{para(r[0])}</li>' for r in rows)
    R = "".join(f'<li><span class="m">&#10003;</span>{para(r[1])}</li>' for r in rows)
    return (f'<div class="cmp cmp-diptych"><div class="side left"><div class="lab">{bad}</div><ul>{L}</ul></div>'
            f'<div class="side right"><div class="lab">{good}</div><ul>{R}</ul></div></div>')


def r_comparison(b, ctx):
    """Default B1 gradient-band table; B2 soft table when the kit has no dark band;
    D1 diptych when the block opts in with variant:"diptych" (falls back to B2 on light brands)."""
    bad = html.escape(b.get("badHead", "Without"))
    good = html.escape(b.get("goodHead", "With"))
    rows = b["rows"]
    dark = ctx["darkband"]
    if not dark:
        return _cmp_soft(bad, good, rows)
    if b.get("variant") == "diptych":
        return _cmp_diptych(bad, good, rows)
    return _cmp_band(bad, good, rows)


def r_checklist(b, ctx):
    items = "".join(f'<li><span class="c">&#10003;</span>{para(x)}</li>' for x in b["items"])
    return f'<ul class="chk">{items}</ul>'


def r_cta(b, ctx):
    dark = b.get("surface", "dark" if ctx["darkband"] else "light") == "dark"
    cls = "cta is-dark" if dark else "cta"
    cta = f'<a class="btn btn-primary">{html.escape(b["cta"]["label"])} {ARROW}</a>' if b.get("cta") else ""
    sub = f'<p>{para(b["sub"])}</p>' if b.get("sub") else ""
    cust = f'<div class="cust-line">{emph(b["custLine"])}</div>' if b.get("custLine") else ""
    return f'<div class="{cls}"><h2>{emph(b["heading"])}</h2>{sub}{cta}{cust}</div>'


def r_footer(b, ctx):
    dark = b.get("surface", "dark" if ctx["darkband"] else "light") == "dark"
    cls = "footer is-dark dark" if dark else "footer light"
    logo = logo_img(ctx["kitdir"], ctx["render"], dark, height=24)
    links = "".join(f'<a>{html.escape(l)}</a>' for l in b.get("links", []))
    return f'<div class="{cls}">{logo}<div class="links">{links}</div></div>'


def r_split(b, ctx):
    rev = b.get("imageSide", "right") == "left"
    img = inline_img(ctx["kitdir"], b["image"], 'class="shot"') if b.get("image") else ""
    k = f'<div class="k">{html.escape(b["kicker"])}</div>' if b.get("kicker") else ""
    h = f'<h2>{emph(b["heading"])}</h2>' if b.get("heading") else ""
    ps = "".join(f'<p>{para(p)}</p>' for p in b.get("paras", []))
    bullets = ('<ul class="chk">' + "".join(f'<li><span class="c">&#10003;</span>{para(x)}</li>'
               for x in b["bullets"]) + '</ul>') if b.get("bullets") else ""
    cta = f'<a class="btn btn-primary">{html.escape(b["cta"]["label"])} {ARROW}</a>' if b.get("cta") else ""
    copy = f'<div class="split-copy">{k}{h}{ps}{bullets}{cta}</div>'
    media = f'<div class="split-media">{img}</div>'
    return f'<div class="split{" rev" if rev else ""}">{(media + copy) if rev else (copy + media)}</div>'


def r_logos(b, ctx):
    label = f'<div class="logos-label">{html.escape(b["label"])}</div>' if b.get("label") else ""
    mono = " mono" if b.get("mono") else ""
    items = ""
    for it in b["items"]:
        if it.get("img"):
            items += f'<div class="logo-item">{inline_img(ctx["kitdir"], it["img"])}</div>'
        else:
            items += f'<div class="logo-item txt">{html.escape(it.get("text",""))}</div>'
    return f'<div class="logos{mono}">{label}<div class="logos-row">{items}</div></div>'


def r_pricing(b, ctx):
    cards = ""
    for p in b["plans"]:
        feats = "".join(f'<li><span class="c">&#10003;</span>{para(f)}</li>' for f in p.get("features", []))
        badge = f'<span class="plan-badge">{html.escape(p.get("badge","Most popular"))}</span>' if p.get("featured") else ""
        cta = (f'<a class="btn {"btn-primary" if p.get("featured") else "btn-secondary"} plan-cta">'
               f'{html.escape(p.get("cta","Get started"))}</a>') if p.get("cta", True) else ""
        price = (f'<div class="plan-price">{html.escape(str(p.get("price","")))}'
                 f'<span>{html.escape(p.get("period",""))}</span></div>') if p.get("price") else ""
        cards += (f'<div class="plan{" featured" if p.get("featured") else ""}">{badge}'
                  f'<div class="plan-name">{html.escape(p["name"])}</div>{price}'
                  f'<p class="plan-blurb">{para(p.get("blurb",""))}</p>{cta}'
                  f'<ul class="chk plan-feats">{feats}</ul></div>')
    return f'<div class="pricing">{cards}</div>'


RENDERERS = {"hero": r_hero, "stats": r_stats, "about": r_about, "quote": r_quote,
             "section": r_section, "features": r_features, "comparison": r_comparison,
             "checklist": r_checklist, "cta": r_cta, "footer": r_footer,
             "split": r_split, "logos": r_logos, "pricing": r_pricing}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", help="kit slug (~/.octave/brands/<slug>) OR a path to a kit directory")
    ap.add_argument("--kit-dir", dest="kit_dir", help="explicit kit directory (overrides --kit)")
    ap.add_argument("--spec", required=True, help="content spec JSON file (or - for stdin)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme", choices=["light", "dark"],
                    help="render a specific theme (needs manifest.render.tokensDark/tokensLight overrides)")
    ap.add_argument("--format", default="doc",
                    help="output canvas: doc (default) | og (1200x630) | social-square (1080) | social-story (1080x1920) | email (600w)")
    args = ap.parse_args()
    target = args.kit_dir or args.kit
    if not target:
        sys.exit("ERROR: provide --kit <slug|path> or --kit-dir <path>")
    args.kit = pathlib.Path(target).name  # slug used for icons/featured lookups
    kitdir, render = load_kit(target)
    spec = json.loads(sys.stdin.read() if args.spec == "-" else pathlib.Path(args.spec).read_text())
    icons = {}
    if (kitdir / "icons.json").exists():
        icons = json.loads((kitdir / "icons.json").read_text())
    ctx = {"kitdir": kitdir, "render": render, "icons": icons, "slug": args.kit,
           "darkband": render.get("hasDarkBand", True)}

    # resolve theme: base tokens + optional light/dark override map
    tok = dict(render.get("tokens", {}))
    theme = args.theme or render.get("defaultTheme")
    if theme == "dark" and render.get("tokensDark"):
        tok.update(render["tokensDark"])
    elif theme == "light" and render.get("tokensLight"):
        tok.update(render["tokensLight"])

    # output format → canvas size
    FORMATS = {"doc": (None, None), "og": (1200, 630), "social-square": (1080, 1080),
               "social-story": (1080, 1920), "email": (600, None)}
    fw, fh = FORMATS.get(args.format, (None, None))
    docw = fw or render.get("docWidth", 880)

    # build <style>: tokens + fonts + base css + format override
    tokens = "".join(f"{k}:{v};" for k, v in tok.items()) + f"--brand-doc-width:{docw}px;"
    faces = font_faces(kitdir, render.get("fonts"))
    base = (SKILL / "assets" / "kit_base.css").read_text()
    fmt_css = ""
    if fh:  # fixed-size canvas (og / social) — fill the frame, no floating sheet
        fmt_css = (f"@media screen{{body{{padding:0;background:var(--brand-bg);}}"
                   f".doc{{width:{fw}px;height:{fh}px;max-width:none;margin:0;border-radius:0;"
                   f"box-shadow:none;overflow:hidden;display:flex;flex-direction:column;justify-content:center;}}}}")
    elif args.format == "email":
        fmt_css = "@media screen{body{padding:0;}.doc{border-radius:0;box-shadow:none;margin:0;}}"
    style = f"{faces}\n:root{{{tokens}}}\n{base}\n{fmt_css}"

    # render blocks, grouping consecutive wrap-blocks into one .wrap
    parts, buf = [], []
    def flush():
        if buf:
            parts.append('<div class="wrap">' + "".join(buf) + "</div>")
            buf.clear()
    for blk in spec["blocks"]:
        t = blk["type"]
        renderer = RENDERERS.get(t)
        if renderer is None:
            sys.exit(f"ERROR: unknown block type '{t}'. Known types: {', '.join(sorted(RENDERERS))}")
        rendered = renderer(blk, ctx)
        if t in WRAP_BLOCKS and blk.get("surface") == "dark":
            # break a content block out of the light .wrap into a full-bleed dark band
            flush()
            parts.append(f'<div class="band is-dark">{rendered}</div>')
        elif t in WRAP_BLOCKS:
            buf.append(rendered)
        else:
            flush()
            parts.append(rendered)
    flush()

    title = html.escape(spec.get("title", "Brand asset"))
    wf = render.get("webfonts")
    link = (f'<link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="{html.escape(wf)}" rel="stylesheet">') if wf else ""
    doc = (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
           f'{link}<style>{style}</style></head><body><div class="doc">{"".join(parts)}</div></body></html>')
    pathlib.Path(args.out).write_text(doc, encoding="utf-8")
    print(args.out, f"({len(doc)} bytes)")


if __name__ == "__main__":
    main()
