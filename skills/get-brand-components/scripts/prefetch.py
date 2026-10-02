#!/usr/bin/env python3
"""prefetch.py — deterministic brand evidence pack (the miner).

Pages are fetched by the caller (the skill through the Octave `scrape_website`
tool with `fullDocument: true`, or a headless runner through the crawler) and
saved into a pages dir. This script never walks a site itself. It mines what
the capture model used to improvise every run: the stylesheet bundles and the
real @font-face files, colors / radii / shadows / containers, nav and footer
logo candidates with provenance, inline icons, screenshot strips and pixel
palettes, and (when Playwright is available) COMPUTED styles off the rendered
page: body/heading/button anatomy, section rhythm, and the emphasized-word
device inside headings, which is what CSS grepping misses.

  prefetch.py ingest     --pages-dir <dir> <scrape-result.json | ->   # save one scrape_website result
  prefetch.py pick-pages --pages-dir <dir> [--max-pages 5]           # which pages to fetch next
  prefetch.py mine       --pages-dir <dir> --out <evidence-dir> [--no-playwright] [--domain acme.com]
  prefetch.py fetch-asset --out <dir> <url>...                       # site-declared fonts/icons/images, capped

Pages dir contract: <dir>/firecrawl.json is a list of rows
  {"url", "ok": bool, "status": int, "finalUrl", "title"?, "htmlFile", "screenshotFile"?, "links"?: [str]}
where htmlFile / screenshotFile are paths relative to <dir>. `ingest` writes rows from
`scrape_website` results (downloading `contentUrl` and `screenshotUrl`); any other producer
that writes the same files works too.

Output of `mine`: <evidence-dir>/evidence.json + pages/ fonts/ logos/ images/ icons.json screenshots/ css/.
Needs: python3, bs4; optional playwright (computed styles + fallback shots), Pillow (crops).
"""
import argparse, collections, hashlib, json, os, pathlib, re, shutil, sys, time, urllib.request, urllib.parse
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
PAGE_PREFS = [  # (role, keywords in path) in the skill's priority order
    ("product", ["product", "platform", "features", "solutions", "how-it-works"]),
    ("pricing", ["pricing", "plans"]),
    ("article", ["blog/", "resources/", "learn/", "guides/", "insights/", "articles/", "news/"]),
    ("customers", ["customers", "case-stud", "success", "stories"]),
    ("about", ["about", "company"]),
]
LOGO_HINT = re.compile(r"logo|brand|wordmark|lockup", re.I)
WALL_HINT = re.compile(r"customers?|partners?|trusted|clients?|logos|logo-wall|marquee|carousel|press", re.I)
HEX = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")
LATIN_RANGE = re.compile(r"U\+0{0,2}(?:0|00|000)-0{0,2}(?:FF|0FF|00FF)\b", re.I)  # a unicode-range that covers basic latin
MAX_FONT_BYTES = 600_000
MAX_LOGO_BYTES = 2_000_000
MAX_ICON_BYTES = 200_000
MAX_IMAGE_BYTES = 5_000_000
MAX_PAGE_BYTES = 8_000_000
MAX_SCREENSHOT_BYTES = 25_000_000
PAGES_INDEX = "firecrawl.json"
# declared @font-face format() or URL extension -> file extension; file extension -> the renderer's format vocabulary
FORMAT_EXT = {"woff2": "woff2", "woff": "woff", "truetype": "ttf", "ttf": "ttf", "opentype": "otf", "otf": "otf"}
EXT_FORMAT = {"woff2": "woff2", "woff": "woff", "ttf": "truetype", "otf": "opentype"}
RESET_SELECTOR = re.compile(r"input|select|textarea|optgroup|::file-selector-button|::-webkit|::-moz", re.I)
STYLED_BUTTON = re.compile(r"background(?:-color)?\s*:\s*(?!transparent|none|inherit|0)|border-radius\s*:\s*(?!0(?:px)?\s*[;}])|padding\s*:\s*(?!0(?:px)?\s*[;}])|border\s*:\s*\d", re.I)


def http_fetch(url, timeout=25, max_bytes=None):
    """GET url. Returns (body: bytes, final_url, status). http(s) only; raises on error status."""
    scheme = urllib.parse.urlparse(url).scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"unsupported URL scheme: {scheme or 'none'}")
    headers = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
    try:
        import requests  # carries its own CA bundle; macOS python's urllib often has none
    except ImportError:
        requests = None
    if requests is not None:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        body, final_url, status = r.content, r.url, r.status_code
    else:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body, final_url, status = r.read(), r.geturl(), r.status
    if max_bytes is not None and len(body) > max_bytes:
        raise ValueError(f"too large: {len(body)} bytes")
    return body, final_url, status


def http_get(url, binary=False, timeout=25, max_bytes=None):
    body, _, _ = http_fetch(url, timeout=timeout, max_bytes=max_bytes)
    return body if binary else body.decode("utf-8", errors="replace")


def slug_of(url):
    p = urllib.parse.urlparse(url).path.strip("/")
    return (re.sub(r"[^a-z0-9]+", "-", p.lower()) or "home")[:60]


def same_site(url, host):
    h = urllib.parse.urlparse(url).netloc.lower()
    core = host.lower().removeprefix("www.")
    return h == core or h == "www." + core or h.endswith("." + core)


class Browser:
    """Optional Playwright session for the enrichment pass (computed styles, hover, dark theme, missing shots)."""

    def __init__(self, enabled, log):
        self.log = log
        self.pw = None
        if enabled:
            try:
                from playwright.sync_api import sync_playwright
                self._p = sync_playwright().start()
                self._b = self._p.chromium.launch()
                self.pw = self._b.new_context(viewport={"width": 1280, "height": 900}, user_agent=UA)
            except Exception as e:
                self.log(f"playwright unavailable: {e}")

    def close(self):
        if self.pw:
            try: self._b.close(); self._p.stop()
            except Exception: pass


# ---- pages dir: ingest scrape results, pick pages, load rows ----

def read_index(pages_dir):
    p = pages_dir / PAGES_INDEX
    return json.loads(p.read_text()) if p.is_file() else []


def write_index(pages_dir, rows):
    (pages_dir / PAGES_INDEX).write_text(json.dumps(rows, indent=1))


def ingest_result(result, pages_dir, log, fetch=http_fetch):
    """Save one `scrape_website` result into the pages dir and return the row written.

    Downloads `contentUrl` (the full HTML document) and `screenshotUrl`; an inline HTML `content`
    string is accepted when there is no contentUrl (older tool builds), markdown content is ignored.
    A failed scrape or an error status is recorded as an `ok: false` row and raises ValueError."""
    pages_dir.mkdir(parents=True, exist_ok=True)
    url = result.get("finalUrl") or result.get("url") or ""
    status = result.get("statusCode")
    row = {"url": result.get("url") or url, "ok": False, "status": status, "finalUrl": url,
           "title": result.get("title"), "htmlFile": None, "screenshotFile": None, "links": result.get("links") or []}
    def commit(r):
        rows = [x for x in read_index(pages_dir) if x.get("finalUrl") != r["finalUrl"]]
        rows.append(r); write_index(pages_dir, rows); return r
    if not url:
        commit(row); raise ValueError("scrape result has no url")
    if result.get("found") is False or (isinstance(status, int) and status >= 400):
        commit(row); raise ValueError(f"scrape of {url} failed: {result.get('error') or f'HTTP {status}'}")
    slug = slug_of(url)
    html = None
    if result.get("contentUrl"):
        body, _, _ = fetch(result["contentUrl"], max_bytes=MAX_PAGE_BYTES)
        html = body.decode("utf-8", errors="replace")
    elif isinstance(result.get("content"), str) and result["content"].lstrip().startswith("<"):
        html = result["content"]
    if not html:
        commit(row); raise ValueError(f"scrape result for {url} carries no HTML (no contentUrl, content is not HTML)")
    (pages_dir / f"{slug}.html").write_text(html)
    row.update({"ok": True, "status": status if isinstance(status, int) else 200, "htmlFile": f"{slug}.html"})
    if result.get("screenshotUrl"):
        try:
            shot, _, _ = fetch(result["screenshotUrl"], max_bytes=MAX_SCREENSHOT_BYTES)
            (pages_dir / f"{slug}.png").write_bytes(shot); row["screenshotFile"] = f"{slug}.png"
        except Exception as e:
            log(f"screenshot download failed for {url}: {str(e)[:100]}")
    return commit(row)


def load_pages(pages_dir, log):
    """[(final_url, page)] for the usable rows, in index order. page = {html, screenshot, links, status, via}."""
    pages = []
    for row in read_index(pages_dir):
        url = row.get("finalUrl") or row.get("url")
        if not row.get("ok") or not row.get("htmlFile"):
            log(f"skipped {url}: not fetched"); continue
        if isinstance(row.get("status"), int) and row["status"] >= 400:
            log(f"skipped {url}: HTTP {row['status']}"); continue
        f = pages_dir / row["htmlFile"]
        if not f.is_file():
            log(f"skipped {url}: {row['htmlFile']} missing"); continue
        shot = pages_dir / row["screenshotFile"] if row.get("screenshotFile") else None
        pages.append((url, {"html": f.read_text(errors="replace"), "screenshot": str(shot) if shot and shot.is_file() else None,
                            "links": row.get("links") or [], "status": row.get("status"), "via": "pages-dir"}))
    return pages


def homepage_first(pages):
    """The row with the shortest path is the homepage; it leads so the rest of the miner can rely on pages[0]."""
    return sorted(pages, key=lambda up: (len(urllib.parse.urlparse(up[0]).path.strip("/")), pages.index(up)))


def page_links(url, page):
    return page["links"] or [urllib.parse.urljoin(url, a["href"]) for a in BeautifulSoup(page["html"], "html.parser").find_all("a", href=True)]


def pick_pages(home_links, base):
    host = urllib.parse.urlparse(base).netloc
    chosen, cands = [], []
    for l in home_links:
        try:
            u = urllib.parse.urljoin(base, l.split("#")[0])
        except Exception: continue
        if not u.startswith("http") or not same_site(u, host): continue
        path = urllib.parse.urlparse(u).path.lower()
        if re.search(r"\.(pdf|png|jpg|svg|zip|xml)$|/(login|signin|signup|legal|privacy|terms|careers|jobs|cookie)", path): continue
        cands.append((u, path))
    for role, kws in PAGE_PREFS:
        best = None
        for u, path in cands:
            if any(k in path for k in kws):
                depth = path.count("/")
                # article: prefer a deep, slug-like path (an actual post); others: prefer shallow
                score = depth if role == "article" else -depth
                if best is None or score > best[0]:
                    best = (score, u)
        if best and best[1] not in chosen:
            chosen.append(best[1])
    return chosen


def absolutize_css_urls(css, base_url):
    """Rewrite relative url(...) references in a stylesheet against the URL it was served from."""
    return re.sub(r"url\(\s*(['\"]?)(?!data:|https?://|//)([^'\")]+)\1\s*\)",
                  lambda m: "url(" + urllib.parse.urljoin(base_url, m.group(2)) + ")", css)


HEAD_RE = re.compile(r"<head\b.*?</head>", re.S | re.I)


def recover_head(page_url, log, fetch=http_fetch):
    """Some scraped documents arrive without <head> (the crawler drops it on certain pages), which loses the
    stylesheet links and @font-face. One plain GET of the page recovers just that section; failure is logged."""
    try:
        body, _, _ = fetch(page_url, max_bytes=MAX_PAGE_BYTES)
        m = HEAD_RE.search(body.decode("utf-8", errors="replace"))
        return m.group(0) if m else None
    except Exception as e:
        log(f"head recovery failed {page_url[:80]}: {str(e)[:80]}"); return None


def css_of_page(html, page_url, out_css, log, budget=6, fetch_head=recover_head):
    """Download linked stylesheets (+ @import) and gather inline <style>.
    Returns (css_text, sheets, head_recovered)."""
    head_recovered = False
    if not re.search(r"<head\b", html, re.I):
        head = fetch_head(page_url, log)
        if head:
            html = head + html; head_recovered = True
            log(f"head recovered for {page_url[:80]}")
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("link"):
        rel = " ".join(link.get("rel") or []).lower()
        href = link.get("href")
        if href and ("stylesheet" in rel or (rel == "preload" and link.get("as") == "style")):
            urls.append(urllib.parse.urljoin(page_url, href))
    inline = absolutize_css_urls("\n".join(s.get_text() for s in soup.find_all("style")), page_url)
    text, sheets = inline, []
    for u in urls[:budget]:
        try:
            css = http_get(u)
        except Exception as e:
            log(f"css fetch failed {u[:80]}: {str(e)[:80]}"); continue
        # absolutize url(...) against the SHEET url, so relative font/image paths survive concatenation;
        # each @import is resolved against ITS OWN url before being appended, not the parent sheet's
        css = absolutize_css_urls(css, u)
        for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css)[:4]:
            imp_url = urllib.parse.urljoin(u, imp)
            try: css += "\n" + absolutize_css_urls(http_get(imp_url), imp_url)
            except Exception as e: log(f"css import failed {imp_url[:80]}: {str(e)[:80]}")
        name = hashlib.sha1(u.encode()).hexdigest()[:10] + ".css"
        (out_css / name).write_text(css)
        sheets.append({"url": u, "bytes": len(css), "file": f"css/{name}", "headRecovered": head_recovered})
        text += "\n" + css
    return text, sheets, head_recovered


def font_ext(declared, url, data=b""):
    """File extension for a downloaded face: declared format(), else the URL, else the magic bytes."""
    d = (declared or "").lower().strip("'\" ")
    if d in FORMAT_EXT:
        return FORMAT_EXT[d]
    u = urllib.parse.urlparse(url).path.rsplit(".", 1)[-1].lower()
    if u in EXT_FORMAT:
        return u
    head = data[:4]
    if head == b"wOF2": return "woff2"
    if head == b"wOFF": return "woff"
    if head == b"OTTO": return "otf"
    if head in (b"\0\1\0\0", b"true"): return "ttf"
    return "woff2"


def wt_num(w):
    try: return int(str(w).split()[0])
    except ValueError: return 400


def download_faces(faces, base_url, out_fonts, log):
    """Download the given @font-face entries into out_fonts, recording file, bytes and the renderer format
    on each entry (in place). Names are <family>-<weight>-<style>.<ext>, kept unique across calls."""
    used = {p.name for p in out_fonts.iterdir()} if out_fonts.is_dir() else set()
    for f in faces:
        u = urllib.parse.urljoin(base_url, f["src"])
        try:
            data = http_get(u, binary=True, max_bytes=MAX_FONT_BYTES)
            ext = font_ext(f.get("format"), u, data)
            stem = re.sub(r"[^a-z0-9]+", "-", f"{f['displayFamily']}-{f['weight']}-{f['style']}".lower()).strip("-")
            name = f"{stem}.{ext}"
            if name in used:  # same face from a second source (e.g. a non-latin subset survived): keep both apart
                name = f"{stem}-{hashlib.sha1(u.encode()).hexdigest()[:6]}.{ext}"
            used.add(name)
            (out_fonts / name).write_bytes(data)
            f["file"] = f"fonts/{name}"; f["bytes"] = len(data); f["format"] = EXT_FORMAT[ext]
        except Exception as e:
            f["file"] = None; f["error"] = str(e)[:80]
    return faces


def faces_for_weights(faces, wanted):
    """Upright faces not yet downloaded whose (family, weight) a computed style actually uses.
    `wanted` is a set of (lower-case family, weight int)."""
    out = []
    for f in faces:
        if f.get("file") or f["style"] != "normal":
            continue
        fams = {f["displayFamily"].lower(), f["family"].lower().strip("'\"")}
        if any((fam, wt_num(f["weight"])) in wanted for fam in fams):
            out.append(f)
    return out


def computed_weights(comp):
    """(family, weight) pairs used by the computed styles: headings, body copy and the button groups."""
    wanted = set()
    for page in (comp or {}).values():
        els = [page.get(k) for k in ("body", "h1", "h2", "h3", "p", "eyebrow")] + list(page.get("buttons") or [])
        for el in els:
            if not el or not el.get("fontFamily") or not el.get("fontWeight"):
                continue
            fam = display_family(el["fontFamily"].split(",")[0]).lower()
            w = {"normal": 400, "bold": 700}.get(str(el["fontWeight"]).lower(), wt_num(el["fontWeight"]))
            wanted.add((fam, w))
    return wanted


def display_family(name):
    """next/font and similar emit hashed families ('__affairs_726c9c', '__Inter_Fallback_ab12cd'); recover the readable name."""
    n = name.strip().strip("'\"")
    m = re.fullmatch(r"__([A-Za-z][\w ]*?)(?:_Fallback)?_[0-9a-f]{6}", n)
    if m:
        return m.group(1).replace("_", " ").title() if m.group(1).islower() else m.group(1).replace("_", " ")
    return n


def mine_css(css, base_url, out_fonts, log):
    ev = {}
    # @font-face
    faces = []
    for block in re.findall(r"@font-face\s*\{([^}]*)\}", css, re.I):
        fam = re.search(r"font-family\s*:\s*['\"]?([^;'\"]+)", block)
        wt = re.search(r"font-weight\s*:\s*([^;]+)", block)
        st = re.search(r"font-style\s*:\s*([^;]+)", block)
        ur = re.search(r"unicode-range\s*:\s*([^;]+)", block, re.I)
        srcs = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)(?:\s*format\(['\"]?(\w+)['\"]?\))?", block)
        if not fam or not srcs: continue
        src = next((s for s in srcs if "woff2" in s[0] or s[1] == "woff2"), srcs[0])
        faces.append({"family": fam.group(1).strip(), "displayFamily": display_family(fam.group(1)), "weight": (wt.group(1).strip() if wt else "400"),
                      "style": (st.group(1).strip() if st else "normal"), "src": src[0], "format": src[1] or src[0].rsplit(".", 1)[-1][:5],
                      "unicodeRange": re.sub(r"\s+", "", ur.group(1)).upper() if ur else None})
    # dedupe by (family, weight, style, unicode-range), then keep ONE face per (family, weight, style):
    # the subset that covers basic latin (hosted font CSS lists latin last), else a face with no range
    seen, by_face = set(), collections.OrderedDict()
    for f in faces:
        if f["src"].startswith("data:"): continue
        k = (f["family"].lower(), f["weight"], f["style"], f["unicodeRange"])
        if k in seen: continue
        seen.add(k); by_face.setdefault(k[:3], []).append(f)
    def latin_first(f):
        r = f["unicodeRange"]
        return (0 if (r and LATIN_RANGE.search(r)) else 1 if r is None else 2)
    uniq = [sorted(group, key=latin_first)[0] for group in by_face.values()]
    # rank faces by how much the CSS actually uses the family (so a brand's display
    # face wins over a bundled Inter), prefer upright text weights, download the top 10
    usage = collections.Counter()
    for m in re.finditer(r"font-family\s*:\s*([^;}]+)", css):
        first = m.group(1).split(",")[0].strip().strip("'\"").lower()
        usage[first] += 1
    uniq.sort(key=lambda f: (-usage.get(f["family"].lower(), 0), f["style"] != "normal", abs(wt_num(f["weight"]) - 500)))
    for f in uniq:  # normalize the declared format to the renderer's vocabulary (download may refine it from the bytes)
        ext = FORMAT_EXT.get((f["format"] or "").lower().strip("'\" "))
        f["format"] = EXT_FORMAT[ext] if ext else None
    # download: the top 5 families by usage, up to 3 upright faces each (nearest 400/500/700), so a display
    # face used on few selectors (next/font hashed families) is never crowded out. `mine` downloads the
    # weights the computed styles actually use afterwards (see faces_for_weights).
    by_fam = collections.OrderedDict()
    for f in uniq:
        by_fam.setdefault(f["displayFamily"].lower(), []).append(f)
    to_get = []
    for fam_faces in list(by_fam.values())[:5]:
        upright = [f for f in fam_faces if f["style"] == "normal"] or fam_faces
        picked = []
        for target in (400, 500, 700):
            best = min(upright, key=lambda f: abs(wt_num(f["weight"]) - target))
            if best not in picked: picked.append(best)
        to_get += picked[:3]
    download_faces(to_get, base_url, out_fonts, log)
    ev["fontFaces"] = sorted(uniq, key=lambda f: (f.get("file") is None, uniq.index(f)))[:40]
    # font-family usage ranked + by heading/body context
    fams = collections.Counter()
    ctx = collections.defaultdict(collections.Counter)
    for m in re.finditer(r"([^{}]{0,200})\{([^}]*font-family\s*:\s*([^;}]+)[^}]*)\}", css):
        sel, decl, fam = m.group(1).strip()[-160:], m.group(2), m.group(3).strip().strip("'\"")
        first = display_family(fam.split(",")[0])
        if first.startswith("var("): continue
        fams[first] += 1
        for key, pat in (("heading", r"\bh[1-3]\b|heading|title|display"), ("body", r"\bbody\b|\bhtml\b|\bp\b|paragraph|text"), ("button", r"btn|button"), ("label", r"eyebrow|label|caption|overline|mono")):
            if re.search(pat, sel, re.I): ctx[key][first] += 1
    ev["fontFamiliesRanked"] = fams.most_common(12)
    ev["fontFamilyByContext"] = {k: v.most_common(4) for k, v in ctx.items()}
    # custom properties (root-ish blocks)
    props = {}
    dark = {}
    for m in re.finditer(r"([^{}]{0,120})\{([^}]*--[\w-]+\s*:[^}]*)\}", css):
        sel = m.group(1).strip()
        is_dark = bool(re.search(r"dark|theme=\"?dark|\.dark|night", sel, re.I))
        for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(2)):
            v = v.strip()
            if len(v) > 160: continue
            (dark if is_dark else props).setdefault(k, v)
        if len(props) > 500: break
    ev["customProperties"] = dict(list(props.items())[:400])
    ev["customPropertiesDark"] = dict(list(dark.items())[:150])
    # colors ranked, and by property
    colors = collections.Counter(c.lower() for c in HEX.findall(css))
    byprop = collections.defaultdict(collections.Counter)
    for prop, val in re.findall(r"(background(?:-color)?|color|border(?:-color)?|fill|stroke)\s*:\s*([^;}]+)", css):
        for c in HEX.findall(val): byprop[prop.split("-")[0]][c.lower()] += 1
    ev["colorsRanked"] = colors.most_common(40)
    ev["colorsByProperty"] = {k: v.most_common(10) for k, v in byprop.items()}
    ev["gradients"] = list(dict.fromkeys(re.findall(r"(?:linear|radial|conic)-gradient\([^;}]{0,220}\)", css)))[:12]
    ev["radii"] = collections.Counter(v.strip() for v in re.findall(r"border-radius\s*:\s*([^;}]+)", css)).most_common(12)
    ev["shadows"] = collections.Counter(v.strip()[:120] for v in re.findall(r"box-shadow\s*:\s*([^;}]+)", css) if v.strip() != "none").most_common(8)
    ev["maxWidths"] = collections.Counter(v.strip() for v in re.findall(r"max-width\s*:\s*(\d{3,4}px|\d{2,3}rem)", css)).most_common(6)
    ev["letterSpacingHeadings"] = collections.Counter(v.strip() for v in re.findall(r"letter-spacing\s*:\s*(-?[\d.]+(?:em|px))", css)).most_common(6)
    ev["transitions"] = collections.Counter(v.strip()[:80] for v in re.findall(r"transition\s*:\s*([^;}]+)", css)).most_common(5)
    # button rules
    btns = []
    for m in re.finditer(r"([^{}]{1,160})\{([^}]{20,600})\}", css):
        sel = m.group(1).strip()
        # real button rules only: framework resets (`button,input,select…`, ::file-selector-button) say nothing about the brand
        if re.search(r"btn|button|cta", sel, re.I) and not RESET_SELECTOR.search(sel) and STYLED_BUTTON.search(m.group(2)):
            btns.append({"selector": sel[-120:], "rules": re.sub(r"\s+", " ", m.group(2).strip())[:400]})
        if len(btns) >= 24: break
    ev["buttonRules"] = btns
    # section rhythm from CSS
    ev["sectionPadding"] = collections.Counter(v.strip() for v in re.findall(r"(?:section|hero|container)[^{}]{0,80}\{[^}]*padding(?:-top|-block)?\s*:\s*([^;}]+)", css, re.I)).most_common(8)
    return ev


SVG_TAG = re.compile(r"<(/?)svg\b[^>]*>", re.I)
VIEWBOX = re.compile(r"""\bviewBox\s*=\s*(['"])([^'"]*)\1""", re.I)


def raw_svg(html, el):
    """The exact <svg>…</svg> source text for a parsed element.

    html.parser lowercases tag and attribute names (viewBox -> viewbox, linearGradient -> lineargradient),
    which makes str(el) an invalid standalone SVG. Locate the element in the raw markup by its parse
    position instead and return the original text, matching nested <svg> with a depth counter."""
    if el.sourceline is None or el.sourcepos is None:
        return None
    lines = html.split("\n")
    start = sum(len(l) + 1 for l in lines[: el.sourceline - 1]) + el.sourcepos
    if html[start:start + 4].lower() != "<svg":
        return None
    depth = 0
    for m in SVG_TAG.finditer(html, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return html[start:m.end()]
    return None


def svg_viewbox(raw):
    m = VIEWBOX.search(raw[: raw.find(">") + 1] if raw else "")
    return m.group(2).strip() if m else ""


def svg_document(text):
    """The <svg>…</svg> part of a standalone SVG file (skips the XML prolog, comments and doctype)."""
    m = re.search(r"<svg\b", text, re.I)
    if not m: return None
    end = text.lower().rfind("</svg>")
    return text[m.start(): end + 6] if end > m.start() else None


# ---- logo ink: which surface a logo is for, by the color of its marks rather than where it sat on the page ----

def luminance(rgb):
    r, g, b = (c / 255 for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def parse_color(value):
    v = value.strip().lower()
    if v in ("white", "#fff", "#ffffff"): return (255, 255, 255)
    if v in ("black", "#000", "#000000"): return (0, 0, 0)
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4): h = "".join(c * 2 for c in h[:3])
        if len(h) >= 6: return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", v)
    if m: return tuple(min(255, int(x)) for x in m.groups())
    return None


def saturation(rgb):
    hi, lo = max(rgb), min(rgb)
    return (hi - lo) / hi if hi else 0.0


def ink_stats(colors):
    """(mean luminance, mean saturation) of a list of RGB tuples, or (None, None)."""
    if not colors: return None, None
    return round(sum(luminance(c) for c in colors) / len(colors), 3), round(sum(saturation(c) for c in colors) / len(colors), 3)


def svg_ink_stats(raw):
    """Luminance and saturation of the fills/strokes an SVG declares; (None, None) when it relies on currentColor or CSS."""
    colors = []
    for v in re.findall(r"""(?:fill|stroke|stop-color)\s*[:=]\s*["']?([^"';)\s>]+(?:\([^)]*\))?)""", raw, re.I):
        c = parse_color(v)
        if c: colors.append(c)
    return ink_stats(colors)


def svg_ink_luminance(raw):
    return svg_ink_stats(raw)[0]


def raster_ink_stats(data):
    """Luminance and saturation of the opaque pixels of a raster logo; (None, None) when Pillow is missing or nothing is opaque."""
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(data)).convert("RGBA")
        im.thumbnail((96, 96))
        return ink_stats([p[:3] for p in im.getdata() if p[3] > 128])
    except Exception:
        return None, None


def raster_ink_luminance(data):
    return raster_ink_stats(data)[0]


def suggested_surface(lum, sat=0.0):
    """Light marks belong on dark surfaces and dark marks on light ones. Saturated marks (a colored wordmark,
    a gradient logo) read on either surface, and mid-tones are left to the eye: both return None."""
    if lum is None or (sat or 0) >= 0.35: return None
    return "dark" if lum >= 0.6 else "light" if lum <= 0.4 else None


def rendered_ink_luminance(browser, svg_path):
    """Rasterize an SVG logo on a transparent page and measure its opaque pixels: the declared fills are a
    weak proxy (a dark wordmark with white knockout shapes averages light), the rendered marks are the truth."""
    if not browser.pw: return None
    pg = browser.pw.new_page()
    try:
        svg = pathlib.Path(svg_path).read_text(errors="replace")
        pg.set_content(f'<!DOCTYPE html><html><body style="margin:0;background:transparent">'
                       f'<div style="width:480px;padding:8px">{svg_document(svg) or svg}</div></body></html>')
        pg.add_style_tag(content="svg{width:464px;height:auto;display:block}")
        pg.wait_for_timeout(100)
        data = pg.locator("svg").first.screenshot(omit_background=True)
        return raster_ink_stats(data)
    except Exception:
        return None, None
    finally:
        pg.close()


def lift_logos(html, page_url, out_logos, log):
    soup = BeautifulSoup(html, "html.parser")
    cands = []
    regions = [("header", soup.find("header")), ("nav", soup.find("nav")), ("footer", soup.find("footer"))]
    home_links = [a for a in soup.find_all("a", href=True) if a["href"] in ("/", page_url, page_url.rstrip("/")) or a["href"].rstrip("/") == page_url.rstrip("/")]
    for a in home_links[:6]:
        regions.append(("home-link", a))
    seen = set()
    for region, node in regions:
        if node is None: continue
        wall = bool(WALL_HINT.search(" ".join(node.get("class") or []) + " " + (node.get("id") or "")))
        for el in node.find_all(["img", "svg"]):
            container_cls = " ".join(" ".join(p.get("class") or []) for p in el.parents if p.name in ("div", "section", "ul", "li", "a"))[:300]
            in_wall = bool(WALL_HINT.search(container_cls)) or wall
            if el.name == "img":
                src = el.get("src") or el.get("data-src") or ""
                if not src or src.startswith("data:image/gif"): continue
                alt = el.get("alt") or ""
                hinted = bool(LOGO_HINT.search(src + " " + alt + " " + " ".join(el.get("class") or [])))
                if not hinted and region not in ("home-link",): continue
                if re.search(r"facebook|twitter|linkedin|instagram|youtube|tiktok|github|x \(formerly", alt + " " + src, re.I): continue
                u = urllib.parse.urljoin(page_url, src)
                if u in seen: continue
                seen.add(u)
                cands.append({"region": region, "kind": "img", "src": u, "alt": el.get("alt"), "class": " ".join(el.get("class") or [])[:80],
                              "width": el.get("width"), "height": el.get("height"), "suspectWall": in_wall})
            else:
                raw = raw_svg(html, el) or str(el)
                if len(raw) < 200 or len(raw) > 60000: continue
                # an inline SVG is a logo candidate only inside the home link or when its own attributes say so
                if region != "home-link" and not LOGO_HINT.search(" ".join(el.get("class") or []) + " " + (el.get("aria-label") or "") + " " + (el.title.get_text() if el.title else "")):
                    continue
                h = hashlib.sha1(raw.encode()).hexdigest()[:10]
                if h in seen: continue
                seen.add(h)
                cands.append({"region": region, "kind": "svg-inline", "hash": h, "class": " ".join(el.get("class") or [])[:80],
                              "ariaLabel": el.get("aria-label"), "title": (el.title.get_text() if el.title else None),
                              "viewBox": svg_viewbox(raw) or None, "bytes": len(raw), "suspectWall": in_wall, "_raw": raw})
    out = []
    for i, c in enumerate(cands[:16]):
        try:
            if c["kind"] == "img":
                data = http_get(c["src"], binary=True, max_bytes=MAX_LOGO_BYTES)
                ext = c["src"].split("?")[0].rsplit(".", 1)[-1].lower()
                ext = ext if ext in ("svg", "png", "jpg", "jpeg", "webp") else "bin"
                name = f"logo-{i}-{c['region']}.{ext}"
                (out_logos / name).write_bytes(data); c["file"] = f"logos/{name}"; c["bytes"] = len(data)
                lum, sat = svg_ink_stats(data.decode("utf-8", errors="replace")) if ext == "svg" else raster_ink_stats(data)
            else:
                raw = c.pop("_raw")
                name = f"logo-{i}-{c['region']}.svg"
                (out_logos / name).write_text(raw); c["file"] = f"logos/{name}"
                lum, sat = svg_ink_stats(raw)
            c.update({"inkLuminance": lum, "inkSaturation": sat, "suggestedSurface": suggested_surface(lum, sat),
                      "inkMethod": "declared" if c["file"].endswith(".svg") else "raster"})
        except Exception as e:
            c.pop("_raw", None); c["file"] = None; c["error"] = str(e)[:80]
        out.append(c)
    meta = {}
    for l in soup.find_all("link"):
        rel = " ".join(l.get("rel") or []).lower()
        if "icon" in rel and l.get("href"): meta.setdefault("icons", []).append(urllib.parse.urljoin(page_url, l["href"]))
    og = soup.find("meta", property="og:image")
    if og and og.get("content"): meta["ogImage"] = og["content"]
    tc = soup.find("meta", attrs={"name": "theme-color"})
    if tc and tc.get("content"): meta["themeColor"] = tc["content"]
    return out, meta


def icon_entry(raw, name, seen):
    """One icons.json entry from standalone <svg>…</svg> text, or None when it is not icon-sized or a duplicate."""
    vb = svg_viewbox(raw)
    if not vb or len(raw) > 6000 or len(raw) < 80: return None
    try:
        w, h = [float(x) for x in vb.split()[2:4]]
    except Exception: return None
    if not (12 <= w <= 64 and 12 <= h <= 64): return None
    inner = re.sub(r"^<svg[^>]*>|</svg>$", "", raw, flags=re.S).strip()
    key = hashlib.sha1(inner.encode()).hexdigest()[:8]
    if key in seen: return None
    seen.add(key)
    return {"name": name[:40], "viewBox": vb, "inner": inner[:3000]}


def lift_icons(html, page_url=None, log=None):
    """The page's own icons: inline <svg> elements, plus <img src="*.svg"> icons when a page_url is given
    (sites that ship icons as files rather than inline markup). Deduped across both."""
    log = log or (lambda m: None)
    soup = BeautifulSoup(html, "html.parser")
    icons, seen = [], set()
    for el in soup.find_all("svg"):
        raw = raw_svg(html, el)
        if raw is None: continue  # position unknown (markup too malformed to slice): skip rather than emit lowercased SVG
        name = el.get("aria-label") or (el.title.get_text() if el.title else None) or f"icon-{len(icons)+1}"
        entry = icon_entry(raw, name, seen)
        if entry:
            icons.append({**entry, "source": "inline"})
        if len(icons) >= 30: break
    if page_url:
        fetched = set()
        for img in soup.find_all("img", src=True):
            src = urllib.parse.urljoin(page_url, img["src"])
            if not urllib.parse.urlparse(src).path.lower().endswith(".svg") or src in fetched: continue
            try:
                w, h = int(img.get("width") or 0), int(img.get("height") or 0)
            except ValueError: w = h = 0
            if (w and w > 64) or (h and h > 64): continue  # an <img> SVG that big is artwork, not an icon
            fetched.add(src)
            try:
                raw = svg_document(http_get(src, max_bytes=MAX_ICON_BYTES))
            except Exception as e:
                log(f"icon fetch failed {src[:80]}: {str(e)[:60]}"); continue
            if not raw: continue
            name = img.get("alt") or urllib.parse.urlparse(src).path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            entry = icon_entry(raw, name, seen)
            if entry:
                icons.append({**entry, "source": "img", "src": src})
            if len(icons) >= 30: break
    return icons


def lift_images(html, page_url, out_images, log):
    """Hero imagery the tokens cannot express: the <video> poster (and the video URL for the record), the
    largest image in the opening section, and og:image. Saved under images/ for manifest.render.heroImage."""
    soup = BeautifulSoup(html, "html.parser")
    cands = []
    for v in soup.find_all("video")[:2]:
        if v.get("poster"): cands.append({"kind": "poster", "src": urllib.parse.urljoin(page_url, v["poster"])})
        vsrc = v.get("src") or next((s.get("src") for s in v.find_all("source") if s.get("src")), None)
        if vsrc: cands.append({"kind": "video", "src": urllib.parse.urljoin(page_url, vsrc), "file": None})
    main = soup.find("main") or soup.body or soup
    opening = [c for c in main.find_all(["section", "header", "div"], recursive=False)][:2]
    imgs = [im for sec in opening for im in sec.find_all("img", src=True)]
    def declared_width(im):
        try: return int(im.get("width") or 0)
        except ValueError: return 0
    big = [im for im in imgs if declared_width(im) >= 600 or (not im.get("width") and im.find_parent(["header", "nav", "footer"]) is None)]
    if big:
        im = max(big, key=declared_width)
        cands.append({"kind": "hero-img", "src": urllib.parse.urljoin(page_url, im["src"]), "alt": im.get("alt")})
    og = soup.find("meta", property="og:image")
    if og and og.get("content"): cands.append({"kind": "og", "src": urllib.parse.urljoin(page_url, og["content"])})
    out, seen = [], set()
    for c in cands:
        if c["src"] in seen: continue
        seen.add(c["src"])
        if c["kind"] == "video" or len([o for o in out if o.get("file")]) >= 4:
            out.append(c); continue
        try:
            data = http_get(c["src"], binary=True, max_bytes=MAX_IMAGE_BYTES)
            head = data[:12]
            ext = ("png" if head.startswith(b"\x89PNG") else "jpg" if head.startswith(b"\xff\xd8") else "webp" if head[8:12] == b"WEBP"
                   else "svg" if b"<svg" in data[:600].lower() else urllib.parse.urlparse(c["src"]).path.rsplit(".", 1)[-1].lower()[:4] or "bin")
            name = f"{c['kind']}-{len(out)}.{ext}"
            (out_images / name).write_bytes(data)
            c["file"] = f"images/{name}"; c["bytes"] = len(data)
        except Exception as e:
            c["file"] = None; c["error"] = str(e)[:80]
        out.append(c)
    return out


COMPUTED_JS = r"""
() => {
  const cs = (el) => el ? getComputedStyle(el) : null;
  const pick = (el, keys) => { const s = cs(el); if (!s) return null; const o = {}; for (const k of keys) o[k] = s[k]; return o; };
  const T = ["fontFamily","fontSize","fontWeight","lineHeight","letterSpacing","color","textTransform"];
  const B = ["backgroundColor","backgroundImage","color","borderRadius","padding","fontFamily","fontSize","fontWeight","height","boxShadow","border","textTransform","letterSpacing"];
  const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const q = (sel) => Array.from(document.querySelectorAll(sel)).find(vis) || null;
  const out = {};
  out.body = pick(document.body, ["backgroundColor","color","fontFamily","fontSize","fontWeight","lineHeight"]);
  for (const h of ["h1","h2","h3","p"]) { const el = q(h); out[h] = el ? { ...pick(el, T), text: (el.innerText||"").trim().slice(0,120) } : null; }
  const nav = q("header, nav, [role=banner]"); out.nav = nav ? { ...pick(nav, ["backgroundColor","color","height","position","backdropFilter"]) } : null;
  const foot = q("footer"); out.footer = foot ? pick(foot, ["backgroundColor","color","paddingTop","paddingBottom"]) : null;
  // buttons: visible <a>/<button> with a solid background, ranked by count of identical (bg, radius)
  // a button is the element that carries the fill: the <a>/<button> itself, or its single styled child
  const btnEls = [];
  for (const el of Array.from(document.querySelectorAll("a, button, [class*=btn], [class*=button]")).filter(vis)) {
    const t = (el.innerText||"").trim(); const r = el.getBoundingClientRect();
    if (!(t.length > 0 && t.length <= 40 && !t.includes("\n") && r.height <= 80 && r.width <= 420)) continue;
    let carrier = el; let s = cs(el);
    if (s.backgroundColor === "rgba(0, 0, 0, 0)" && s.backgroundImage === "none" && (s.border === "" || s.borderStyle === "none")) {
      const kid = el.children.length === 1 ? el.children[0] : null;
      if (kid) { const ks = cs(kid); if (ks.backgroundColor !== "rgba(0, 0, 0, 0)" || ks.borderStyle !== "none") { carrier = kid; s = ks; } }
    }
    const filled = s.backgroundColor !== "rgba(0, 0, 0, 0)" || s.backgroundImage !== "none" || (s.borderStyle !== "none" && parseFloat(s.borderWidth) > 0);
    if (filled && parseFloat(s.paddingLeft) >= 8) btnEls.push({ el: carrier, textEl: el, s });
  }
  const btns = btnEls;
  const groups = {};
  for (const x of btns) { const k = x.s.backgroundColor + "|" + x.s.borderRadius; (groups[k] = groups[k] || []).push(x); }
  const ranked = Object.values(groups).sort((a,b)=>b.length-a.length).slice(0,5);
  ranked.forEach((g, i) => { g[0].textEl.setAttribute("data-bk-btn", String(i)); g[0].el.setAttribute("data-bk-btn-fill", String(i)); });  // lets the host hover each group and read the fill carrier
  out.buttons = ranked.map(g => ({ count: g.length, text: (g[0].textEl.innerText||"").trim().slice(0,40), ...pick(g[0].el, B), heightPx: Math.round(g[0].el.getBoundingClientRect().height), hasArrowSvg: !!g[0].textEl.querySelector("svg") }));
  // sections: direct children of main/body that are tall
  // descend through framework wrapper divs: a child taller than 55% of the page is a wrapper, not a section
  const total = document.body.scrollHeight;
  const secs = [];
  const walk = (el, depth) => {
    for (const c of Array.from(el.children)) {
      const r = c.getBoundingClientRect(); if (r.height < 200) continue;
      if (r.height > total * 0.55 && depth < 4) { walk(c, depth + 1); continue; }
      const s = cs(c); const head = c.querySelector("h1,h2");
      secs.push({ tag: c.tagName.toLowerCase(), cls: (c.className||"").toString().slice(0,60), height: Math.round(r.height), bg: s.backgroundColor, bgImage: s.backgroundImage.slice(0,80), padTop: s.paddingTop, padBottom: s.paddingBottom, radius: s.borderRadius, heading: head ? (head.innerText||"").trim().slice(0,80) : null });
      if (secs.length >= 14) return;
    }
  };
  walk(document.querySelector("main") || document.body, 0);
  out.sections = secs;
  // emphasis device: styled inline children inside any large display text (h1/h2/h3 or any element with font-size >= 28px)
  const emph = [];
  const heads = Array.from(document.querySelectorAll("h1, h2, h3, p, div, span")).filter(el => vis(el) && parseFloat(cs(el).fontSize) >= 28 && (el.innerText||"").trim().length > 0 && (el.innerText||"").trim().length < 140 && !el.querySelector("h1,h2,h3,p,div")).slice(0, 30);
  for (const h of heads) {
    const hs = cs(h);
    // the display element itself may be the device (a highlight box, a gradient-text word)
    const selfDiff = {};
    if (hs.backgroundColor !== "rgba(0, 0, 0, 0)") { selfDiff.backgroundColor = hs.backgroundColor; selfDiff.borderRadius = hs.borderRadius; selfDiff.padding = hs.padding; }
    if (hs.backgroundImage !== "none") selfDiff.backgroundImage = hs.backgroundImage.slice(0,120);
    if (hs.webkitTextFillColor === "rgba(0, 0, 0, 0)" || hs.webkitTextFillColor === "transparent") selfDiff.gradientText = true;
    if (h.querySelector("svg, img")) selfDiff.hasInlineIcon = true;
    // a short display word wrapped in a styled box (highlighter chip) usually carries the box on its parent
    const par = h.parentElement; const ps = par ? cs(par) : null;
    if (ps && (h.innerText||"").trim().length <= 24 && (ps.backgroundColor !== "rgba(0, 0, 0, 0)" || ps.backgroundImage !== "none" || (ps.borderStyle !== "none" && parseFloat(ps.borderWidth) > 0)) && par.getBoundingClientRect().width < 700)
      selfDiff.parentBox = { backgroundColor: ps.backgroundColor, backgroundImage: ps.backgroundImage.slice(0,120), borderRadius: ps.borderRadius, padding: ps.padding, border: ps.border, display: ps.display, animated: ps.animationName !== "none" || (h.className||"").toString().toLowerCase().includes("animat") };
    if (Object.keys(selfDiff).length && (h.innerText||"").trim().length >= 2 && (h.innerText||"").trim().length <= 40) emph.push({ heading: (h.parentElement && (h.parentElement.innerText||"").trim().slice(0,80)) || "", headingTag: h.tagName.toLowerCase(), headingSize: hs.fontSize, word: (h.innerText||"").trim().slice(0,40), self: true, ...selfDiff });
    for (const c of Array.from(h.querySelectorAll("span, em, strong, mark, b, i, a")).filter(vis)) {
      if ((c.innerText||"").trim().length < 2 && !c.querySelector("svg, img")) continue; // per-letter animation spans
      const s = cs(c);
      const diff = {};
      if (s.color !== hs.color) diff.color = s.color;
      if (s.backgroundColor !== "rgba(0, 0, 0, 0)" && s.backgroundColor !== hs.backgroundColor) diff.backgroundColor = s.backgroundColor;
      if (s.backgroundImage !== "none") diff.backgroundImage = s.backgroundImage.slice(0,120);
      if (s.fontWeight !== hs.fontWeight) diff.fontWeight = s.fontWeight;
      if (s.fontStyle !== hs.fontStyle) diff.fontStyle = s.fontStyle;
      if (s.fontFamily !== hs.fontFamily) diff.fontFamily = s.fontFamily;
      if (s.textDecorationLine && s.textDecorationLine !== "none") diff.textDecoration = s.textDecorationLine + " " + s.textDecorationColor;
      if (s.webkitTextFillColor === "rgba(0, 0, 0, 0)" || s.webkitTextFillColor === "transparent") diff.gradientText = true;
      if (parseFloat(s.borderRadius) > 0 && diff.backgroundColor) diff.borderRadius = s.borderRadius;
      if (parseFloat(s.paddingLeft) > 2 && diff.backgroundColor) diff.padding = s.padding;
      if (c.querySelector("svg, img")) diff.hasInlineIcon = true;
      if (Object.keys(diff).length) emph.push({ heading: (h.innerText||"").trim().slice(0,80), headingTag: h.tagName.toLowerCase(), headingSize: hs.fontSize, word: (c.innerText||"").trim().slice(0,40), headingColor: hs.color, ...diff });
      if (emph.length >= 20) break;
    }
  }
  out.emphasis = emph;
  const eyebrow = q("[class*=eyebrow], [class*=overline], [class*=kicker], [class*=label]");
  out.eyebrow = eyebrow ? { ...pick(eyebrow, T), text: (eyebrow.innerText||"").trim().slice(0,40) } : null;
  const wrap = q("[class*=container], [class*=wrapper], [class*=wrap]"); out.container = wrap ? { maxWidth: cs(wrap).maxWidth, paddingLeft: cs(wrap).paddingLeft } : null;
  return out;
}
"""


def dismiss_consent(pg):
    """Click the first visible cookie-consent accept button so overlays don't pollute computed styles or screenshots."""
    try:
        pg.evaluate("""() => {
          const re = /^(accept( all)?( cookies)?|allow all|i agree|agree|got it|ok(ay)?|accept & close)$/i;
          for (const b of document.querySelectorAll('button, a[role=button], [class*=consent] button, [id*=cookie] button')) {
            const t = (b.innerText||'').trim();
            const r = b.getBoundingClientRect();
            if (re.test(t) && r.width > 0 && r.height > 0) { b.click(); return t; }
          }
          return null;
        }""")
        pg.wait_for_timeout(500)
    except Exception:
        pass


def computed_styles(browser, url, log, extras_dir=None, is_home=False, dark_capable=True, missing_shot=None):
    """Computed styles off the rendered page. For the homepage also: a second viewport shot 4 s later
    (animated banners, cycling headline words) and a dark-mode pass when the site honours prefers-color-scheme.
    `missing_shot`: path for a full-page screenshot when the pages dir had none for this page."""
    if not browser.pw: return None
    pg = browser.pw.new_page()
    try:
        pg.goto(url, wait_until="load", timeout=45000)
        pg.wait_for_timeout(1200)
        dismiss_consent(pg)
        if missing_shot is not None:
            try:
                pg.screenshot(path=str(missing_shot), full_page=True)
            except Exception as e:
                log(f"fallback screenshot failed {url[:80]}: {str(e)[:80]}")
        # scroll through once so lazy sections mount, then back to the top. Bounded by step count AND
        # elapsed time: an infinite-scroll page grows scrollHeight faster than we scroll, and page.evaluate
        # has no deadline of its own, so an unbounded loop would hang the run.
        pg.evaluate("""() => new Promise(r => {
          let y = 0, steps = 0; const t0 = Date.now();
          const t = setInterval(() => {
            window.scrollBy(0, 900); y += 900; steps += 1;
            if (y > document.body.scrollHeight || steps >= 40 || Date.now() - t0 > 6000) { clearInterval(t); window.scrollTo(0, 0); r(); }
          }, 90);
        })""")
        pg.wait_for_timeout(800)
        out = pg.evaluate(COMPUTED_JS)
        # hover state of the two most common button groups on the homepage (fill / ink / transform / shadow after :hover)
        for i in range(min(2, len(out.get("buttons") or [])) if is_home else 0):
            try:
                el = pg.locator(f'[data-bk-btn="{i}"]').first
                el.scroll_into_view_if_needed(timeout=3000); el.hover(timeout=3000); pg.wait_for_timeout(350)
                out["buttons"][i]["hover"] = pg.evaluate("""(i) => { const el = document.querySelector('[data-bk-btn="' + i + '"]');
                  const c = document.querySelector('[data-bk-btn-fill="' + i + '"]') || el; const s = getComputedStyle(c); const t = getComputedStyle(el);
                  return { backgroundColor: s.backgroundColor, color: s.color, transform: t.transform, boxShadow: s.boxShadow, borderColor: s.borderColor, textDecoration: s.textDecorationLine }; }""", i)
            except Exception as e:
                out["buttons"][i]["hover"] = None
        if is_home and extras_dir is not None:
            try:
                # hover probing scrolled buttons into view; the animated-hero frames must start at the top
                pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(300)
                pg.screenshot(path=str(extras_dir / "home-t0.png"), full_page=False)
                pg.wait_for_timeout(4000)
                pg.screenshot(path=str(extras_dir / "home-t1.png"), full_page=False)
                out["animatedShots"] = ["screenshots/home-t0.png", "screenshots/home-t1.png"]
                # second pass of the emphasis probe after the delay: catches cycling word treatments
                later = pg.evaluate(COMPUTED_JS)
                out["emphasisLater"] = [e for e in later.get("emphasis", []) if e not in out.get("emphasis", [])][:8]
            except Exception as e:
                log(f"animated shots failed: {str(e)[:80]}")
            if not dark_capable:  # no dark-scheme rules in the CSS: nothing to probe
                out["darkMode"] = None
            else:
                try:
                    light_bg = out.get("body", {}).get("backgroundColor")
                    pg.emulate_media(color_scheme="dark")
                    pg.reload(wait_until="load", timeout=45000); pg.wait_for_timeout(1200); dismiss_consent(pg)
                    dark = pg.evaluate(COMPUTED_JS)
                    if dark.get("body", {}).get("backgroundColor") != light_bg:
                        pg.screenshot(path=str(extras_dir / "home-dark-top.png"), full_page=False)
                        out["darkMode"] = {"body": dark.get("body"), "h1": dark.get("h1"), "p": dark.get("p"), "nav": dark.get("nav"),
                                           "footer": dark.get("footer"), "buttons": dark.get("buttons"), "shot": "screenshots/home-dark-top.png"}
                    else:
                        out["darkMode"] = None
                except Exception as e:
                    log(f"dark-mode pass failed: {str(e)[:80]}")
        return out
    except Exception as e:
        log(f"computed styles failed {url}: {str(e)[:100]}"); return None
    finally:
        pg.close()


def dominant(im, k=6):
    """Top-k quantized colors of an image region as (hex, share)."""
    small = im.convert("RGB").resize((160, max(1, int(160 * im.size[1] / max(1, im.size[0])))))
    quant = small.point(lambda v: v // 16 * 16 + 8)  # 16 levels per channel
    counts = collections.Counter()
    for n, rgb in quant.getcolors(maxcolors=quant.width * quant.height) or []:
        counts[rgb] += n
    total = sum(counts.values()) or 1
    return [("#%02x%02x%02x" % c, round(n / total, 3)) for c, n in counts.most_common(k)]


def crops(shot, out_dir, slug):
    try:
        from PIL import Image
        im = Image.open(shot)
        w, h = im.size
        top = im.crop((0, 0, w, min(h, 1600)))
        top.thumbnail((1280, 1600))
        p = out_dir / f"{slug}-top.png"; top.save(p)
        # the homepage is viewed in full: 1600px strips the Read tool can actually resolve
        strips = []
        if slug == "home":
            for i, y in enumerate(range(0, min(h, 9600), 1600)):
                s = im.crop((0, y, w, min(h, y + 1600))); s.thumbnail((1280, 1600))
                sp = out_dir / f"home-strip{i+1}.png"; s.save(sp); strips.append(str(sp))
        # pixel truth for surfaces CSS hides (canvas/video/image heroes, animated bands)
        palette = {"hero": dominant(im.crop((0, 90, w, min(h, 900)))), "page": dominant(im, 8)}
        bands = []
        step = 300
        for y in range(0, min(h, 9000), step):
            bands.append({"y": y, "colors": dominant(im.crop((0, y, w, min(h, y + step))), 2)})
        palette["bands"] = bands
        return {"full": str(shot), "top": str(p), "size": [w, h], "palette": palette, "strips": strips}
    except Exception:
        return {"full": str(shot), "top": None}


def shot_fields(shot, out):
    """Screenshot columns of a page row from a crops() result (paths relative to the evidence dir)."""
    rel = lambda s: s.replace(str(out) + "/", "")
    if not shot:
        return {"screenshot": None, "screenshotTop": None, "screenshotSize": None, "screenshotPalette": None, "screenshotStrips": []}
    return {"screenshot": rel(shot["full"]), "screenshotTop": rel(shot["top"]) if shot.get("top") else None,
            "screenshotSize": shot.get("size"), "screenshotPalette": shot.get("palette"),
            "screenshotStrips": [rel(s) for s in (shot.get("strips") or [])]}


def cmd_ingest(args):
    log = lambda m: print(m, file=sys.stderr)
    raw = sys.stdin.read() if args.result == "-" else pathlib.Path(args.result).read_text()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"ingest: not JSON ({e}); pass the scrape_website result object exactly as the tool returned it")
    if isinstance(result, dict) and "found" not in result and isinstance(result.get("structuredContent"), dict):
        result = result["structuredContent"]  # some hosts wrap the tool result
    try:
        row = ingest_result(result, args.pages_dir, log)
    except ValueError as e:
        print(f"ingest: {e}", file=sys.stderr); sys.exit(2)
    print(json.dumps({"finalUrl": row["finalUrl"], "status": row["status"], "htmlFile": row["htmlFile"],
                      "screenshotFile": row["screenshotFile"], "links": len(row["links"])}))


def cmd_pick_pages(args):
    log = lambda m: print(m, file=sys.stderr)
    pages = homepage_first(load_pages(args.pages_dir, log))
    if not pages:
        sys.exit("pick-pages: no usable page in the pages dir; ingest the homepage first")
    home_url, home = pages[0]
    have = {u.rstrip("/") for u, _ in pages}
    picked = [u for u in pick_pages(page_links(home_url, home), home_url)[: args.max_pages] if u.rstrip("/") not in have]
    for u in picked:
        print(u)
    if not picked:
        log("no further pages to fetch (single-page site, or every candidate is already in the pages dir): continue with what is there")


def cmd_fetch_asset(args):
    """Download assets the site itself declares (fonts, icons, images) with the same caps and scheme check
    as the miner, so the capture never needs curl."""
    args.out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for url in args.urls:
        try:
            data, final, _ = http_fetch(url, max_bytes=MAX_IMAGE_BYTES)
            name = re.sub(r"[^A-Za-z0-9._-]+", "-", urllib.parse.urlparse(final).path.rsplit("/", 1)[-1]).strip("-") or hashlib.sha1(url.encode()).hexdigest()[:10]
            path = args.out / name
            if path.exists():
                path = args.out / f"{hashlib.sha1(url.encode()).hexdigest()[:6]}-{name}"
            path.write_bytes(data)
            print(path)
        except Exception as e:
            failed += 1
            print(f"fetch-asset: {url}: {str(e)[:120]}", file=sys.stderr)
    if failed:
        sys.exit(1)


def cmd_mine(args):
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    for d in ("pages", "fonts", "logos", "images", "screenshots", "css"): (out / d).mkdir(exist_ok=True)
    logl = []
    def log(msg): logl.append(msg); print(msg, file=sys.stderr)
    t0 = time.time()
    timings = {}
    def mark(k): timings[k] = round(time.time() - t0, 1)
    pages = homepage_first(load_pages(args.pages_dir, log))
    if not pages:
        log("no usable pages"); (out / "evidence.json").write_text(json.dumps({"error": "no usable pages in the pages dir", "log": logl})); sys.exit(2)
    base, home = pages[0]
    domain = args.domain or urllib.parse.urlparse(base).netloc.lower().removeprefix("www.")
    log(f"pages: {base} + {[u for u, _ in pages[1:]]}")
    mark("pages")
    browser = Browser(not args.no_playwright, log)
    try:
        # CSS from home + first two other pages (bundles are shared; keep budget)
        css_text, sheets, head_recovered = "", [], []
        for u, p in pages[:3]:
            t, s, rec = css_of_page(p["html"], u, out / "css", log); css_text += "\n" + t; sheets += s
            if rec: head_recovered.append(slug_of(u))
        log(f"css: {len(sheets)} sheets, {len(css_text)//1024} KB")
        ev = {"domain": domain, "seedUrl": base, "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "stylesheets": sheets}
        mark("css")
        ev.update(mine_css(css_text, base, out / "fonts", log))
        mark("fonts")
        logos, meta = lift_logos(home["html"], base, out / "logos", log)
        ev["logoCandidates"], ev["meta"] = logos, meta
        ev["heroImages"] = lift_images(home["html"], base, out / "images", log)
        ev["icons"] = lift_icons(home["html"], base, log)
        (out / "icons.json").write_text(json.dumps(ev["icons"]))
        ev["icons"] = [{"name": i["name"], "viewBox": i["viewBox"], "source": i["source"]} for i in ev["icons"]]
        page_rows = []
        for u, p in pages:
            slug = slug_of(u)
            (out / "pages" / f"{slug}.html").write_text(p["html"])
            soup = BeautifulSoup(p["html"], "html.parser")
            h1 = soup.find("h1")
            heads = [h.get_text(" ", strip=True)[:80] for h in soup.find_all(["h2"])][:14]
            shot = None
            if p.get("screenshot"):
                dst = out / "screenshots" / f"{slug}.png"
                if str(p["screenshot"]) != str(dst): shutil.copy(p["screenshot"], dst)
                shot = crops(dst, out / "screenshots", slug)
            page_rows.append({"url": u, "slug": slug, "via": p.get("via"), "title": (soup.title.get_text(strip=True)[:100] if soup.title else None),
                              "h1": h1.get_text(" ", strip=True)[:120] if h1 else None, "h2s": heads, "htmlFile": f"pages/{slug}.html",
                              **shot_fields(shot, out)})
        ev["pages"] = page_rows
        mark("logos_icons_shots")
        comp = {}
        # computed styles: the homepage plus the article page (body type) or, failing that, the next page
        article = next((u for u, _ in pages[1:] if re.search(r"blog|resources|learn|guides|insights|articles|news", u)), None)
        comp_pages = [pages[0]] + [(u, pp) for u, pp in pages[1:] if u == article][:1]
        if len(comp_pages) < 2 and len(pages) > 1: comp_pages = pages[:2]
        dark_capable = bool(re.search(r"prefers-color-scheme\s*:\s*dark|data-theme|\.dark\b|color-scheme", css_text))
        for u, p in comp_pages:
            slug = slug_of(u)
            missing = None if p.get("screenshot") else out / "screenshots" / f"{slug}.png"
            c = computed_styles(browser, u, log, extras_dir=out / "screenshots", is_home=(u == base), dark_capable=dark_capable, missing_shot=missing)
            if c: comp[slug] = c
            if missing is not None and missing.is_file():  # the browser filled in a screenshot the pages dir lacked
                row = next(r for r in page_rows if r["slug"] == slug)
                row.update(shot_fields(crops(missing, out / "screenshots", slug), out))
        ev["computed"] = comp
        # SVG logos: replace the declared-fill estimate with the rendered one when a browser is available
        for c in logos:
            if (c.get("file") or "").endswith(".svg") and browser.pw:
                lum, sat = rendered_ink_luminance(browser, out / c["file"])
                if lum is not None:
                    c.update({"inkLuminance": lum, "inkSaturation": sat, "suggestedSurface": suggested_surface(lum, sat), "inkMethod": "rendered"})
        # the weights the rendered page actually uses (a 300 display heading, a 500 button) are downloaded too,
        # not only the nearest-to-400/500/700 defaults
        extra = faces_for_weights(ev["fontFaces"], computed_weights(comp))
        if extra:
            download_faces(extra, base, out / "fonts", log)
            ev["fontFaces"].sort(key=lambda f: f.get("file") is None)
            log(f"fonts: {len([f for f in extra if f.get('file')])} extra face(s) from computed weights")
        mark("computed")
        ev["timings"] = timings
        ev["capabilities"] = {"source": "pages-dir", "playwright": bool(browser.pw),
                              "screenshots": sum(1 for r in page_rows if r["screenshot"]), "headRecovered": head_recovered,
                              # utility-class sites (Tailwind) leave little in the stylesheet; the capture then leans on `computed`
                              "cssSignal": "low" if not (ev["buttonRules"] or ev["sectionPadding"] or ev["transitions"]) else "ok"}
        ev["elapsedSeconds"] = round(time.time() - t0, 1)
        ev["log"] = logl[-30:]
        (out / "evidence.json").write_text(json.dumps(ev, indent=1))
        log(f"done in {ev['elapsedSeconds']}s: {len(page_rows)} pages, {len(ev['fontFaces'])} faces, {len(logos)} logo candidates, "
            f"{ev['capabilities']['screenshots']} screenshots, evidence.json {os.path.getsize(out/'evidence.json')//1024} KB")
    finally:
        browser.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ingest", help="save one scrape_website result (JSON) into the pages dir")
    a.add_argument("--pages-dir", required=True, type=pathlib.Path)
    a.add_argument("result", help="path to the result JSON, or - to read it from stdin")
    a.set_defaults(fn=cmd_ingest)
    b = sub.add_parser("pick-pages", help="print the next pages to fetch, chosen from the homepage's links")
    b.add_argument("--pages-dir", required=True, type=pathlib.Path)
    b.add_argument("--max-pages", type=int, default=5)
    b.set_defaults(fn=cmd_pick_pages)
    c = sub.add_parser("mine", help="build the evidence pack from the pages dir")
    c.add_argument("--pages-dir", required=True, type=pathlib.Path)
    c.add_argument("--out", required=True, type=pathlib.Path)
    c.add_argument("--no-playwright", action="store_true", help="skip the computed-styles enrichment pass")
    c.add_argument("--domain", help="brand domain; derived from the homepage URL when omitted")
    c.set_defaults(fn=cmd_mine)
    d = sub.add_parser("fetch-asset", help="download assets the site declares (fonts, icons, images) into a directory")
    d.add_argument("--out", required=True, type=pathlib.Path)
    d.add_argument("urls", nargs="+")
    d.set_defaults(fn=cmd_fetch_asset)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
