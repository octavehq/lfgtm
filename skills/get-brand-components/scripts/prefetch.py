#!/usr/bin/env python3
"""prefetch.py — deterministic brand evidence pack.

Does the plumbing the capture model currently improvises every run: walk the
homepage + up to 5 high-signal pages, pull the stylesheet bundles and the real
@font-face files, rank colors / radii / shadows / containers, lift nav and
footer logo candidates with provenance, dedupe inline icons, take full-page
screenshots, and (when Playwright is available) read COMPUTED styles off the
rendered page — body/heading/button anatomy, section rhythm, and the
emphasized-word device inside headings, which is what CSS grepping misses.

  prefetch.py --domain acme.com --out <evidence-dir> [--firecrawl <tsx-runner>] [--no-playwright] [--max-pages 5]

Fetch tiers: Firecrawl (via the tsx runner; anti-bot, raw HTML + screenshot)
→ Playwright rendered DOM + screenshot → plain HTTP (no screenshot).
Output: <evidence-dir>/evidence.json + pages/ fonts/ logos/ screenshots/ css/.
Needs: python3, bs4; optional playwright (computed styles + fallback shots), Pillow (crops).
"""
import argparse, base64, collections, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time, urllib.request, urllib.parse
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
RGB = re.compile(r"rgba?\([^)]*\)")


def http_get(url, binary=False, timeout=25):
    headers = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
    try:
        import requests  # carries its own CA bundle; macOS python's urllib often has none
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.content if binary else r.text
    except ImportError:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return data if binary else data.decode("utf-8", errors="replace")


def slug_of(url):
    p = urllib.parse.urlparse(url).path.strip("/")
    return (re.sub(r"[^a-z0-9]+", "-", p.lower()) or "home")[:60]


def same_site(url, host):
    h = urllib.parse.urlparse(url).netloc.lower()
    core = host.lower().removeprefix("www.")
    return h == core or h == "www." + core or h.endswith("." + core)


class Fetcher:
    """Three tiers. Firecrawl runner = a tsx script taking <out-dir> <url>... and writing firecrawl.json."""

    def __init__(self, out, firecrawl_runner, use_playwright, log):
        self.out, self.runner, self.log = out, firecrawl_runner, log
        self.pw = None
        if use_playwright:
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

    def firecrawl(self, urls):
        """Returns {url: {html, screenshot_path, links, status, final_url}}"""
        if not self.runner: return {}
        fdir = self.out / "firecrawl"; fdir.mkdir(exist_ok=True)
        cmd = self.runner.split() + [str(fdir)] + urls
        t0 = time.time()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=240, cwd=os.environ.get("FIRECRAWL_CWD"))
        except Exception as e:
            self.log(f"firecrawl runner failed: {e}"); return {}
        self.log(f"firecrawl: {len(urls)} urls in {time.time()-t0:.1f}s rc={r.returncode}")
        if r.returncode != 0:
            self.log((r.stderr or r.stdout)[-600:]); return {}
        res = {}
        try:
            for row in json.loads((fdir / "firecrawl.json").read_text()):
                if not row.get("ok") or not row.get("htmlFile"): continue
                res[row["url"]] = {"html": (fdir / row["htmlFile"]).read_text(errors="replace"),
                                   "screenshot": str(fdir / row["screenshotFile"]) if row.get("screenshotFile") else None,
                                   "links": row.get("links") or [], "status": row.get("status"),
                                   "final_url": row.get("finalUrl") or row["url"], "via": "firecrawl"}
        except Exception as e:
            self.log(f"firecrawl.json unreadable: {e}")
        return res

    def playwright_page(self, url, shot_path):
        if not self.pw: return None
        pg = self.pw.new_page()
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            try: pg.wait_for_load_state("networkidle", timeout=15000)
            except Exception: pass
            pg.wait_for_timeout(1500)
            html = pg.content()
            try:
                pg.screenshot(path=str(shot_path), full_page=True); shot = str(shot_path)
            except Exception: shot = None
            links = pg.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.href).slice(0, 600)")
            return {"html": html, "screenshot": shot, "links": links, "status": 200, "final_url": pg.url, "via": "playwright"}
        except Exception as e:
            self.log(f"playwright fetch failed {url}: {str(e)[:120]}"); return None
        finally:
            pg.close()

    def http(self, url):
        try:
            html = http_get(url)
            return {"html": html, "screenshot": None, "links": [], "status": 200, "final_url": url, "via": "http"}
        except Exception as e:
            self.log(f"http fetch failed {url}: {str(e)[:120]}"); return None

    def fetch(self, urls):
        got = self.firecrawl(urls)
        for u in urls:
            if u in got: continue
            r = self.playwright_page(u, self.out / "screenshots" / f"{slug_of(u)}.png") or self.http(u)
            if r: got[u] = r
        return got


def pick_pages(home_links, base):
    host = urllib.parse.urlparse(base).netloc
    chosen, seen_roles = [], set()
    cands = []
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
        if best and best[1] not in [c for c in chosen]:
            chosen.append(best[1]); seen_roles.add(role)
    return chosen


def css_of_page(html, page_url, out_css, log, budget=6):
    """Download linked stylesheets (+ @import) and gather inline <style>. Returns (css_text, sheets)."""
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("link"):
        rel = " ".join(link.get("rel") or []).lower()
        href = link.get("href")
        if href and ("stylesheet" in rel or (rel == "preload" and link.get("as") == "style")):
            urls.append(urllib.parse.urljoin(page_url, href))
    inline = "\n".join(s.get_text() for s in soup.find_all("style"))
    inline = re.sub(r"url\(\s*(['\"]?)(?!data:|https?://|//)([^'\")]+)\1\s*\)",
                    lambda m: "url(" + urllib.parse.urljoin(page_url, m.group(2)) + ")", inline)
    text, sheets = inline, []
    for u in urls[:budget]:
        try:
            css = http_get(u)
        except Exception as e:
            log(f"css fetch failed {u[:80]}: {str(e)[:80]}"); continue
        for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css)[:4]:
            try: css += "\n" + http_get(urllib.parse.urljoin(u, imp))
            except Exception: pass
        # absolutize url(...) against the SHEET url, so relative font/image paths survive concatenation
        css = re.sub(r"url\(\s*(['\"]?)(?!data:|https?://|//)([^'\")]+)\1\s*\)",
                     lambda m: "url(" + urllib.parse.urljoin(u, m.group(2)) + ")", css)
        name = hashlib.sha1(u.encode()).hexdigest()[:10] + ".css"
        (out_css / name).write_text(css)
        sheets.append({"url": u, "bytes": len(css), "file": f"css/{name}"})
        text += "\n" + css
    return text, sheets


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
        srcs = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)(?:\s*format\(['\"]?(\w+)['\"]?\))?", block)
        if not fam or not srcs: continue
        src = next((s for s in srcs if "woff2" in s[0] or s[1] == "woff2"), srcs[0])
        faces.append({"family": fam.group(1).strip(), "displayFamily": display_family(fam.group(1)), "weight": (wt.group(1).strip() if wt else "400"),
                      "style": (st.group(1).strip() if st else "normal"), "src": src[0], "format": src[1] or src[0].rsplit(".", 1)[-1][:5]})
    # dedupe by (family, weight, style)
    seen, uniq = set(), []
    for f in faces:
        k = (f["family"].lower(), f["weight"], f["style"])
        if k in seen or f["src"].startswith("data:"): continue
        seen.add(k); uniq.append(f)
    # rank faces by how much the CSS actually uses the family (so a brand's display
    # face wins over a bundled Inter), prefer upright text weights, download the top 10
    usage = collections.Counter()
    for m in re.finditer(r"font-family\s*:\s*([^;}]+)", css):
        first = m.group(1).split(",")[0].strip().strip("'\"").lower()
        usage[first] += 1
    def wt_num(w):
        try: return int(str(w).split()[0])
        except ValueError: return 400
    uniq.sort(key=lambda f: (-usage.get(f["family"].lower(), 0), f["style"] != "normal", abs(wt_num(f["weight"]) - 500)))
    # download: the top 5 families by usage, up to 3 upright faces each (nearest 400/500/700),
    # so a display face used on few selectors (next/font hashed families) is never crowded out
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
    for f in to_get:
        u = urllib.parse.urljoin(base_url, f["src"])
        try:
            data = http_get(u, binary=True)
            if len(data) > 600_000: raise ValueError("too large")
            ext = f["format"] if f["format"] in ("woff2", "woff", "ttf", "otf") else "woff2"
            name = re.sub(r"[^a-z0-9]+", "-", f"{f['displayFamily']}-{f['weight']}-{f['style']}".lower()).strip("-") + "." + ext
            (out_fonts / name).write_bytes(data)
            f["file"] = f"fonts/{name}"; f["bytes"] = len(data)
        except Exception as e:
            f["file"] = None; f["error"] = str(e)[:80]
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
        if re.search(r"btn|button|cta", sel, re.I) and re.search(r"border-radius|padding|background", m.group(2)):
            btns.append({"selector": sel[-120:], "rules": re.sub(r"\s+", " ", m.group(2).strip())[:400]})
        if len(btns) >= 24: break
    ev["buttonRules"] = btns
    # section rhythm from CSS
    ev["sectionPadding"] = collections.Counter(v.strip() for v in re.findall(r"(?:section|hero|container)[^{}]{0,80}\{[^}]*padding(?:-top|-block)?\s*:\s*([^;}]+)", css, re.I)).most_common(8)
    return ev


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
                raw = str(el)
                if len(raw) < 200 or len(raw) > 60000: continue
                # an inline SVG is a logo candidate only inside the home link or when its own attributes say so
                if region != "home-link" and not LOGO_HINT.search(" ".join(el.get("class") or []) + " " + (el.get("aria-label") or "") + " " + (el.title.get_text() if el.title else "")):
                    continue
                h = hashlib.sha1(raw.encode()).hexdigest()[:10]
                if h in seen: continue
                seen.add(h)
                cands.append({"region": region, "kind": "svg-inline", "hash": h, "class": " ".join(el.get("class") or [])[:80],
                              "ariaLabel": el.get("aria-label"), "title": (el.title.get_text() if el.title else None),
                              "viewBox": el.get("viewBox"), "bytes": len(raw), "suspectWall": in_wall, "_raw": raw})
    out = []
    for i, c in enumerate(cands[:16]):
        try:
            if c["kind"] == "img":
                data = http_get(c["src"], binary=True)
                ext = c["src"].split("?")[0].rsplit(".", 1)[-1].lower()
                ext = ext if ext in ("svg", "png", "jpg", "jpeg", "webp") else "bin"
                name = f"logo-{i}-{c['region']}.{ext}"
                (out_logos / name).write_bytes(data); c["file"] = f"logos/{name}"; c["bytes"] = len(data)
            else:
                name = f"logo-{i}-{c['region']}.svg"
                (out_logos / name).write_text(c.pop("_raw")); c["file"] = f"logos/{name}"
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


def lift_icons(html):
    soup = BeautifulSoup(html, "html.parser")
    icons, seen = [], set()
    for el in soup.find_all("svg"):
        vb = el.get("viewBox") or ""
        raw = str(el)
        if not vb or len(raw) > 6000 or len(raw) < 80: continue
        try:
            w, h = [float(x) for x in vb.split()[2:4]]
        except Exception: continue
        if not (12 <= w <= 64 and 12 <= h <= 64): continue
        inner = re.sub(r"^<svg[^>]*>|</svg>$", "", raw, flags=re.S).strip()
        key = hashlib.sha1(inner.encode()).hexdigest()[:8]
        if key in seen: continue
        seen.add(key)
        name = el.get("aria-label") or (el.title.get_text() if el.title else None) or f"icon-{len(icons)+1}"
        icons.append({"name": name[:40], "viewBox": vb, "inner": inner[:3000]})
        if len(icons) >= 30: break
    return icons


COMPUTED_JS = r"""
() => {
  const cs = (el) => el ? getComputedStyle(el) : null;
  const pick = (el, keys) => { const s = cs(el); if (!s) return null; const o = {}; for (const k of keys) o[k] = s[k]; return o; };
  const T = ["fontFamily","fontSize","fontWeight","lineHeight","letterSpacing","color","textTransform"];
  const B = ["backgroundColor","backgroundImage","color","borderRadius","padding","fontFamily","fontSize","fontWeight","height","boxShadow","border","textTransform","letterSpacing"];
  const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const q = (sel) => Array.from(document.querySelectorAll(sel)).find(vis) || null;
  const out = {};
  out.body = pick(document.body, ["backgroundColor","color","fontFamily","fontSize","lineHeight"]);
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


def computed_styles(fetcher, url, log, extras_dir=None, is_home=False, dark_capable=True):
    """Computed styles off the rendered page. For the homepage also: a second viewport shot 4 s later
    (animated banners, cycling headline words) and a dark-mode pass when the site honours prefers-color-scheme."""
    if not fetcher.pw: return None
    pg = fetcher.pw.new_page()
    try:
        pg.goto(url, wait_until="load", timeout=45000)
        pg.wait_for_timeout(1200)
        dismiss_consent(pg)
        # scroll through once so lazy sections mount, then back to the top
        pg.evaluate("() => new Promise(r => { let y=0; const t=setInterval(()=>{ window.scrollBy(0,900); y+=900; if (y>document.body.scrollHeight) {clearInterval(t); window.scrollTo(0,0); r();} }, 90); })")
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
                pg.screenshot(path=str(extras_dir / "home-t0.png"), full_page=False)
                pg.wait_for_timeout(4000)
                pg.screenshot(path=str(extras_dir / "home-t1.png"), full_page=False)
                out["animatedShots"] = ["screenshots/home-t0.png", "screenshots/home-t1.png"]
                # second pass of the emphasis probe after the delay: catches cycling word treatments
                later = pg.evaluate(COMPUTED_JS)
                out["emphasisLater"] = [e for e in later.get("emphasis", []) if e not in out.get("emphasis", [])][:8]
            except Exception as e:
                log(f"animated shots failed: {str(e)[:80]}")
            try:
                if not dark_capable: raise StopIteration("no dark-scheme rules in the CSS")
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
            except StopIteration:
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
    counts = collections.Counter()
    for r, g, b in small.getdata():
        counts[(r // 16 * 16 + 8, g // 16 * 16 + 8, b // 16 * 16 + 8)] += 1
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--firecrawl", help="runner command, e.g. 'node_modules/.bin/tsx --env-file=.env docs/local/brand-kit-bakeoff/firecrawl_fetch.ts' (run with cwd=FIRECRAWL_CWD)")
    ap.add_argument("--no-playwright", action="store_true")
    ap.add_argument("--max-pages", type=int, default=5)
    args = ap.parse_args()
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    for d in ("pages", "fonts", "logos", "screenshots", "css"): (out / d).mkdir(exist_ok=True)
    logl = []
    def log(msg): logl.append(msg); print(msg, file=sys.stderr)
    t0 = time.time()
    timings = {}
    def mark(k): timings[k] = round(time.time() - t0, 1)
    f = Fetcher(out, args.firecrawl, not args.no_playwright, log)
    try:
        base = f"https://www.{args.domain}/"
        home = f.fetch([base]).get(base)
        if not home:
            base = f"https://{args.domain}/"
            home = f.fetch([base]).get(base)
        if not home:
            log("homepage unreachable"); (out / "evidence.json").write_text(json.dumps({"error": "homepage unreachable", "log": logl})); sys.exit(2)
        base = home.get("final_url") or base
        mark("home")
        links = home["links"] or [urllib.parse.urljoin(base, a["href"]) for a in BeautifulSoup(home["html"], "html.parser").find_all("a", href=True)]
        extra = pick_pages(links, base)[: args.max_pages]
        log(f"pages: {base} + {extra}")
        others = f.fetch(extra) if extra else {}
        pages = [(base, home)] + [(u, others[u]) for u in extra if u in others]
        mark("pages")
        # CSS from home + first two other pages (bundles are shared; keep budget)
        css_text, sheets = "", []
        for u, p in pages[:3]:
            t, s = css_of_page(p["html"], u, out / "css", log); css_text += "\n" + t; sheets += s
        log(f"css: {len(sheets)} sheets, {len(css_text)//1024} KB")
        ev = {"domain": args.domain, "seedUrl": base, "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "stylesheets": sheets}
        mark("css")
        ev.update(mine_css(css_text, base, out / "fonts", log))
        mark("fonts")
        logos, meta = lift_logos(home["html"], base, out / "logos", log)
        ev["logoCandidates"], ev["meta"] = logos, meta
        # footer logo from the footer of any page if the homepage had none
        ev["icons"] = lift_icons(home["html"])
        (out / "icons.json").write_text(json.dumps(ev["icons"]))
        ev["icons"] = [{"name": i["name"], "viewBox": i["viewBox"]} for i in ev["icons"]]
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
                              "screenshot": shot["full"].replace(str(out) + "/", "") if shot else None,
                              "screenshotTop": shot["top"].replace(str(out) + "/", "") if shot and shot["top"] else None,
                              "screenshotSize": shot.get("size") if shot else None,
                              "screenshotPalette": shot.get("palette") if shot else None,
                              "screenshotStrips": [s.replace(str(out) + "/", "") for s in (shot.get("strips") or [])] if shot else []})
        ev["pages"] = page_rows
        mark("logos_icons_shots")
        comp = {}
        # computed styles: the homepage plus the article page (body type) or, failing that, the next page
        article = next((u for u, _ in pages[1:] if re.search(r"blog|resources|learn|guides|insights|articles|news", u)), None)
        comp_pages = [pages[0]] + [(u, pp) for u, pp in pages[1:] if u == article][:1] or pages[:2]
        if len(comp_pages) < 2 and len(pages) > 1: comp_pages = pages[:2]
        dark_capable = bool(re.search(r"prefers-color-scheme\s*:\s*dark|data-theme|\.dark\b|color-scheme", css_text))
        for u, p in comp_pages:
            c = computed_styles(f, u, log, extras_dir=out / "screenshots", is_home=(u == base), dark_capable=dark_capable)
            if c: comp[slug_of(u)] = c
        ev["computed"] = comp
        mark("computed")
        ev["timings"] = timings
        ev["capabilities"] = {"firecrawl": any(p.get("via") == "firecrawl" for _, p in pages), "playwright": bool(f.pw), "screenshots": sum(1 for r in page_rows if r["screenshot"])}
        ev["elapsedSeconds"] = round(time.time() - t0, 1)
        ev["log"] = logl[-30:]
        (out / "evidence.json").write_text(json.dumps(ev, indent=1))
        log(f"done in {ev['elapsedSeconds']}s: {len(page_rows)} pages, {len(ev['fontFaces'])} faces, {len(logos)} logo candidates, {ev['capabilities']['screenshots']} screenshots, evidence.json {os.path.getsize(out/'evidence.json')//1024} KB")
    finally:
        f.close()


if __name__ == "__main__":
    main()
