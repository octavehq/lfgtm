"""Deterministic checks for the evidence-pack + mechanical-gallery pipeline (no network, no LLM)."""
import argparse
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))


def module(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


prefetch = module("prefetch")
gallery = module("render_gallery")
kit_validation = module("kit_validation")

REQUIRED_TOKENS = {
    "--brand-bg": "#ffffff", "--brand-ink": "#111111", "--brand-primary": "#0055ff", "--brand-primary-ink": "#ffffff",
    "--brand-font-heading": "Georgia, serif", "--brand-font-body": "Arial, sans-serif", "--brand-band": "#102030",
    "--brand-on-dark": "#ffffff", "--brand-muted": "#555555", "--brand-border": "#dddddd", "--brand-surface": "#f6f6f6",
}
LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 30" width="120" height="30"><rect x="0" y="0" width="120" height="30" fill="#0055ff"/></svg>'
NOOP_LOG = lambda msg: None  # noqa: E731
PNG_1x1 = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da63f8ffff3f0300050001ff2a7a3a0000000049454e44ae426082")


def make_kit(root, extra_tokens=None, gallery_block=None, dark_band=True, render_extra=None):
    root.mkdir(parents=True, exist_ok=True)
    tokens = dict(REQUIRED_TOKENS, **(extra_tokens or {}))
    render = {"hasDarkBand": dark_band, "docWidth": 880, "heroVisual": "none", "fonts": [],
              "logo": {"onLight": "logo.svg", "onDark": "logo.svg", "lockup": None}, "tokens": tokens}
    if gallery_block:
        render["gallery"] = gallery_block
    render.update(render_extra or {})
    (root / "manifest.json").write_text(json.dumps({"slug": "acme", "company": "Acme", "domain": "acme.com", "render": render}))
    (root / "tokens.css").write_text(":root{" + "".join(f"{k}:{v};" for k, v in tokens.items()) + "}")
    (root / "brand-kit.md").write_text("# Brand Kit: Acme\n")
    (root / "logo.svg").write_text(LOGO)
    return root


class PrefetchHelpers(unittest.TestCase):
    def test_display_family_decodes_framework_hashes(self):
        self.assertEqual(prefetch.display_family("__affairs_726c9c"), "Affairs")
        self.assertEqual(prefetch.display_family("__Inter_Fallback_299230"), "Inter")
        self.assertEqual(prefetch.display_family("'PP Neue Montreal'"), "PP Neue Montreal")

    def test_pick_pages_prefers_the_skill_page_order_and_deep_articles(self):
        base = "https://www.acme.com/"
        links = ["/about", "/blog/", "/blog/2026/how-we-ship", "/pricing", "/product", "/customers",
                 "/legal/privacy", "https://other.example/x", "/careers", "/blog/2026/how-we-ship#top"]
        picked = prefetch.pick_pages(links, base)
        self.assertEqual(picked[0], "https://www.acme.com/product")
        self.assertEqual(picked[1], "https://www.acme.com/pricing")
        self.assertEqual(picked[2], "https://www.acme.com/blog/2026/how-we-ship")
        self.assertNotIn("https://www.acme.com/legal/privacy", picked)
        self.assertNotIn("https://other.example/x", picked)

    def test_dominant_colors_quantize_and_rank(self):
        from PIL import Image
        im = Image.new("RGB", (100, 100), (255, 0, 0))
        for x in range(30):
            for y in range(100):
                im.putpixel((x, y), (0, 0, 255))
        top = prefetch.dominant(im, 2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0][0], "#f80808")  # red bucket wins
        self.assertGreater(top[0][1], top[1][1])

    def test_http_fetch_rejects_non_http_schemes(self):
        for url in ("file:///etc/hosts", "ftp://x.example/a", "javascript:alert(1)", "/relative/path"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                prefetch.http_fetch(url)


class CssMining(unittest.TestCase):
    def setUp(self):
        self._http_get = prefetch.http_get

    def tearDown(self):
        prefetch.http_get = self._http_get

    def test_css_of_page_resolves_import_urls_against_the_imported_sheet(self):
        sheets = {
            "https://a.example/css/main.css": '@import url("../vendor/fonts/f.css");\n.x{background:url(img/bg.png)}',
            "https://a.example/vendor/fonts/f.css": "@font-face{font-family:F;src:url(inter.woff2) format('woff2')}",
        }
        prefetch.http_get = lambda url, **kw: sheets[url]
        html = '<html><head><link rel="stylesheet" href="/css/main.css"><style>.y{background:url(y.png)}</style></head><body></body></html>'
        with tempfile.TemporaryDirectory() as d:
            text, meta, recovered = prefetch.css_of_page(html, "https://a.example/", pathlib.Path(d), NOOP_LOG)
        self.assertIn("url(https://a.example/vendor/fonts/inter.woff2)", text)  # against the import, not the parent sheet
        self.assertIn("url(https://a.example/css/img/bg.png)", text)
        self.assertIn("url(https://a.example/y.png)", text)
        self.assertEqual([s["url"] for s in meta], ["https://a.example/css/main.css"])
        self.assertFalse(recovered)

    def test_css_of_page_recovers_a_missing_head(self):
        prefetch.http_get = lambda url, **kw: ".brand{color:#123456}"
        body_only = '<!DOCTYPE html><html><body><header>no head here</header></body></html>'
        head = '<head><link rel="stylesheet" href="/site.css"><style>.inline{color:red}</style></head>'
        calls = []
        def fake_head(url, log):
            calls.append(url); return head
        with tempfile.TemporaryDirectory() as d:
            text, meta, recovered = prefetch.css_of_page(body_only, "https://a.example/", pathlib.Path(d), NOOP_LOG, fetch_head=fake_head)
        self.assertEqual(calls, ["https://a.example/"])
        self.assertTrue(recovered)
        self.assertIn(".brand{color:#123456}", text)
        self.assertIn(".inline{color:red}", text)
        self.assertTrue(meta[0]["headRecovered"])
        # a failed recovery leaves the run alive with whatever the body carried
        with tempfile.TemporaryDirectory() as d:
            text, meta, recovered = prefetch.css_of_page(body_only, "https://a.example/", pathlib.Path(d), NOOP_LOG, fetch_head=lambda u, l: None)
        self.assertFalse(recovered)
        self.assertEqual(meta, [])

    def test_recover_head_slices_only_the_head(self):
        doc = b'<!DOCTYPE html><html><head><title>T</title><link rel="stylesheet" href="/a.css"></head><body>x</body></html>'
        head = prefetch.recover_head("https://a.example/", NOOP_LOG, fetch=lambda url, **kw: (doc, url, 200))
        self.assertTrue(head.startswith("<head>") and head.endswith("</head>"))
        self.assertNotIn("<body>", head)
        def boom(url, **kw): raise ValueError("blocked")
        self.assertIsNone(prefetch.recover_head("https://a.example/", NOOP_LOG, fetch=boom))

    def test_mine_css_keeps_the_latin_subset_and_unique_filenames(self):
        css = """
        @font-face{font-family:'Inter';font-style:normal;font-weight:400;src:url(https://f.example/cyr.woff2) format('woff2');unicode-range:U+0460-052F,U+1C80-1C88;}
        @font-face{font-family:'Inter';font-style:normal;font-weight:400;src:url(https://f.example/latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131;}
        @font-face{font-family:'Inter';font-style:normal;font-weight:700;src:url(https://f.example/cyr700.woff2) format('woff2');unicode-range:U+0460-052F;}
        @font-face{font-family:'Inter';font-style:normal;font-weight:700;src:url(https://f.example/latin700.woff2) format('woff2');unicode-range:U+0000-00FF;}
        body{font-family:Inter,sans-serif} h1{font-family:Inter}
        """
        fetched = []
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            fetched.append(url); return b"\0" * 100
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            ev = prefetch.mine_css(css, "https://a.example/", pathlib.Path(d), NOOP_LOG)
            files = sorted(os.listdir(d))
        by_weight = {f["weight"]: f for f in ev["fontFaces"]}
        self.assertEqual(set(by_weight), {"400", "700"})  # one face per (family, weight, style)
        self.assertEqual(by_weight["400"]["src"], "https://f.example/latin.woff2")
        self.assertEqual(by_weight["700"]["src"], "https://f.example/latin700.woff2")
        self.assertEqual(files, ["inter-400-normal.woff2", "inter-700-normal.woff2"])
        self.assertNotIn("https://f.example/cyr.woff2", fetched)

    def test_font_download_respects_the_size_cap(self):
        css = "@font-face{font-family:'Big';font-weight:400;src:url(https://f.example/big.woff2) format('woff2');} body{font-family:Big}"
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            if max_bytes is not None and max_bytes < 10_000_000: raise ValueError("too large: 10000000 bytes")
            return b"\0"
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            ev = prefetch.mine_css(css, "https://a.example/", pathlib.Path(d), NOOP_LOG)
            self.assertEqual(os.listdir(d), [])
        self.assertIsNone(ev["fontFaces"][0]["file"])
        self.assertIn("too large", ev["fontFaces"][0]["error"])


INLINE_LOGO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 30" aria-label="Acme"><defs>'
               '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0055ff"/><stop offset="1" stop-color="#00ccff"/></linearGradient>'
               '<clipPath id="c"><rect width="120" height="30"/></clipPath></defs>'
               '<rect width="120" height="30" fill="url(#g)" clip-path="url(#c)"/><path d="M10 15h40v5h-40z M60 10h30v10h-30z" fill="#fff"/></svg>')
ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-label="Spark">'
        '<linearGradient id="ig" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/></linearGradient>'
        '<path d="M12 2v6m0 8v6m-7-10h6m8 0h-6" stroke="url(#ig)"/></svg>')


class SvgLifting(unittest.TestCase):
    """html.parser lowercases attribute and tag names; the lifted SVG must keep the original source text."""

    def setUp(self):
        self._http_get = prefetch.http_get

    def tearDown(self):
        prefetch.http_get = self._http_get

    def test_lift_icons_keeps_viewbox_and_element_case(self):
        html = f"<html>\n<body>\r\n<main>\n  <div>{ICON}</div><div>{ICON}</div></main></body></html>"
        icons = prefetch.lift_icons(html)
        self.assertEqual(len(icons), 1)  # deduped
        self.assertEqual(icons[0]["viewBox"], "0 0 24 24")
        self.assertEqual(icons[0]["name"], "Spark")
        self.assertIn("linearGradient", icons[0]["inner"])
        kit_validation.svg_root(f'<svg viewBox="{icons[0]["viewBox"]}">{icons[0]["inner"]}</svg>')  # renderer accepts it

    def test_lift_logos_writes_a_valid_standalone_svg(self):
        html = f'<html><body><header class="site-header"><a href="/">{INLINE_LOGO}</a><nav><a href="/pricing">Pricing</a></nav></header></body></html>'
        with tempfile.TemporaryDirectory() as d:
            out, meta = prefetch.lift_logos(html, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG)
            self.assertEqual(len(out), 1)
            c = out[0]
            self.assertEqual(c["kind"], "svg-inline")
            self.assertEqual(c["viewBox"], "0 0 120 30")
            raw = (pathlib.Path(d) / "logo-0-home-link.svg").read_text()
        self.assertIn("linearGradient", raw)
        self.assertIn("clipPath", raw)
        self.assertIn('viewBox="0 0 120 30"', raw)
        kit_validation.svg_root(raw)

    def test_lift_icons_collects_img_svg_icons_too(self):
        icon_file = ('<?xml version="1.0"?><!-- c --><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58" fill="none">'
                     '<path d="M29 10v38m-14-14 14 14 14-14" stroke="#fff" stroke-width="3"/><circle cx="29" cy="29" r="27" stroke="#fff"/></svg>')
        html = (f'<html><body><main>{ICON}<img alt="arrow-down" width="58" height="58" src="/icons/arrow-down.svg">'
                '<img alt="arrow-down" width="58" height="58" src="/icons/arrow-down.svg">'
                '<img alt="hero" width="1200" height="800" src="/hero.svg"><img alt="photo" src="/p.png"></main></body></html>')
        fetched = []
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            fetched.append(url); self.assertEqual(max_bytes, prefetch.MAX_ICON_BYTES); return icon_file
        prefetch.http_get = fake_get
        icons = prefetch.lift_icons(html, "https://www.acme.com/", NOOP_LOG)
        self.assertEqual([(i["name"], i["source"]) for i in icons], [("Spark", "inline"), ("arrow-down", "img")])
        self.assertEqual(icons[1]["viewBox"], "0 0 58 58")
        self.assertEqual(fetched, ["https://www.acme.com/icons/arrow-down.svg"])  # deduped, the 1200px artwork skipped
        kit_validation.svg_root(f'<svg viewBox="{icons[1]["viewBox"]}">{icons[1]["inner"]}</svg>')

    def test_lift_images_saves_poster_hero_image_and_og(self):
        html = ('<html><head><meta property="og:image" content="/og.png"></head><body><main>'
                '<section><video poster="/media/poster.jpg" src="/media/loop.mp4"></video><img src="/hero.png" width="1600" alt="hero"></section>'
                '<section><img src="/small.png" width="40"></section></main></body></html>')
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            self.assertEqual(max_bytes, prefetch.MAX_IMAGE_BYTES)
            return b"\xff\xd8\xff" + b"\0" * 20 if url.endswith(".jpg") else PNG_1x1
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            out = prefetch.lift_images(html, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG)
            files = sorted(os.listdir(d))
        self.assertEqual([(o["kind"], o["file"]) for o in out],
                         [("poster", "images/poster-0.jpg"), ("video", None), ("hero-img", "images/hero-img-2.png"), ("og", "images/og-3.png")])
        self.assertEqual(out[1]["src"], "https://www.acme.com/media/loop.mp4")
        self.assertEqual(files, ["hero-img-2.png", "og-3.png", "poster-0.jpg"])

    def test_logo_ink_luminance_suggests_the_surface(self):
        white = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path fill="#fff" d="M0 0h10v10z"/><path fill="white" d="M0 0h5"/></svg>'
        dark = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path fill="#111" d="M0 0h10v10z"/><path fill="rgb(20, 20, 20)" d="M0 0h5"/></svg>'
        self.assertEqual(prefetch.suggested_surface(*prefetch.svg_ink_stats(white)), "dark")
        self.assertEqual(prefetch.suggested_surface(*prefetch.svg_ink_stats(dark)), "light")
        self.assertIsNone(prefetch.svg_ink_luminance('<svg><path fill="currentColor" d="M0 0"/><path fill="url(#g)" d="M1 1"/></svg>'))
        orange = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path fill="#f19143" d="M0 0h10v10z"/><path fill="#F6BF8D" d="M0 0h5"/></svg>'
        self.assertIsNone(prefetch.suggested_surface(*prefetch.svg_ink_stats(orange)))  # saturated marks read on either surface
        from PIL import Image
        import io
        im = Image.new("RGBA", (8, 8), (0, 0, 0, 0)); im.paste((250, 250, 250, 255), (0, 0, 4, 8))
        buf = io.BytesIO(); im.save(buf, "PNG")
        self.assertEqual(prefetch.suggested_surface(prefetch.raster_ink_luminance(buf.getvalue())), "dark")
        self.assertIsNone(prefetch.raster_ink_luminance(b"not an image"))

    def test_lift_logos_caps_image_downloads(self):
        html = '<html><body><header><img src="/img/logo.png" class="logo" alt="Acme logo"></header></body></html>'
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            self.assertEqual(max_bytes, prefetch.MAX_LOGO_BYTES)
            raise ValueError("too large: 3000000 bytes")
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            out, _ = prefetch.lift_logos(html, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG)
            self.assertEqual(os.listdir(d), [])
        self.assertIsNone(out[0]["file"])
        self.assertIn("too large", out[0]["error"])


HOME_HTML = ('<!DOCTYPE html><html><head><title>Acme</title><link rel="stylesheet" href="/site.css"></head><body>'
             '<header><a href="/"><img src="/logo.svg" alt="Acme logo"></a><nav><a href="/product">Product</a><a href="/pricing">Pricing</a>'
             '<a href="/blog/2026/launch">Blog</a><a href="/legal/privacy">Privacy</a></nav></header>'
             '<main><h1>Hello</h1><h2>Section</h2></main><footer><a href="/about">About</a></footer></body></html>')
PRICING_HTML = '<!DOCTYPE html><html><head><title>Pricing</title></head><body><h1>Plans</h1></body></html>'


def scrape_result(url, **extra):
    r = {"found": True, "finalUrl": url, "title": "Acme", "statusCode": 200, "content": "# Acme\n",
         "contentUrl": f"https://store.example/{prefetch.slug_of(url)}.html", "screenshotUrl": f"https://shots.example/{prefetch.slug_of(url)}.png",
         "links": ["https://www.acme.com/product", "https://www.acme.com/pricing", "https://www.acme.com/blog/2026/launch", "mailto:x@acme.com"]}
    r.update(extra)
    return r


def fake_store(url, **kw):
    if url.endswith(".html"):
        return (HOME_HTML if "home" in url else PRICING_HTML).encode(), url, 200
    if url.endswith(".png"):
        return PNG_1x1, url, 200
    raise ValueError(f"unexpected download {url}")


class Ingest(unittest.TestCase):
    def test_ingest_downloads_html_and_screenshot_and_writes_a_row(self):
        with tempfile.TemporaryDirectory() as d:
            pages = pathlib.Path(d) / "pages"
            row = prefetch.ingest_result(scrape_result("https://www.acme.com/"), pages, NOOP_LOG, fetch=fake_store)
            self.assertEqual((row["ok"], row["status"], row["htmlFile"], row["screenshotFile"]), (True, 200, "home.html", "home.png"))
            self.assertEqual((pages / "home.html").read_text(), HOME_HTML)
            self.assertEqual((pages / "home.png").read_bytes(), PNG_1x1)
            self.assertEqual(len(row["links"]), 4)
            # re-ingesting the same page replaces its row instead of duplicating it
            prefetch.ingest_result(scrape_result("https://www.acme.com/", title="Acme again"), pages, NOOP_LOG, fetch=fake_store)
            rows = prefetch.read_index(pages)
            self.assertEqual([r["title"] for r in rows], ["Acme again"])

    def test_ingest_records_failures_and_refuses_bad_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            pages = pathlib.Path(d) / "pages"
            with self.assertRaises(ValueError):
                prefetch.ingest_result({"found": False, "url": "https://www.acme.com/gone", "statusCode": 404, "error": "not found"}, pages, NOOP_LOG, fetch=fake_store)
            with self.assertRaises(ValueError):
                prefetch.ingest_result(scrape_result("https://www.acme.com/err", statusCode=500), pages, NOOP_LOG, fetch=fake_store)
            with self.assertRaises(ValueError):  # non-http contentUrl never reaches the filesystem
                prefetch.ingest_result(scrape_result("https://www.acme.com/", contentUrl="file:///etc/hosts"), pages, NOOP_LOG, fetch=prefetch.http_fetch)
            with self.assertRaises(ValueError):  # markdown content without a contentUrl is not a page
                prefetch.ingest_result(scrape_result("https://www.acme.com/md", contentUrl=None), pages, NOOP_LOG, fetch=fake_store)
            rows = {r["finalUrl"]: r for r in prefetch.read_index(pages)}
            self.assertFalse(rows["https://www.acme.com/gone"]["ok"])
            self.assertEqual(rows["https://www.acme.com/err"]["status"], 500)
            self.assertEqual(sorted(os.listdir(pages)), ["firecrawl.json"])

    def test_ingest_accepts_inline_html_content_without_contenturl(self):
        with tempfile.TemporaryDirectory() as d:
            pages = pathlib.Path(d) / "pages"
            row = prefetch.ingest_result(scrape_result("https://www.acme.com/", contentUrl=None, screenshotUrl=None, content=HOME_HTML), pages, NOOP_LOG, fetch=fake_store)
            self.assertEqual(row["htmlFile"], "home.html")
            self.assertIsNone(row["screenshotFile"])

    def test_ingest_cli_reads_stdin_and_exits_2_on_failure(self):
        with tempfile.TemporaryDirectory() as d:
            pages = pathlib.Path(d) / "pages"
            ok = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "ingest", "--pages-dir", str(pages), "-"],
                                input=json.dumps(scrape_result("https://www.acme.com/", contentUrl=None, screenshotUrl=None, content=HOME_HTML)),
                                capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(json.loads(ok.stdout)["htmlFile"], "home.html")
            bad = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "ingest", "--pages-dir", str(pages), "-"],
                                 input=json.dumps({"found": False, "url": "https://www.acme.com/x", "error": "blocked"}), capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("blocked", bad.stderr)


def seed_pages(pages, with_screenshot=True, with_pricing=True):
    pages.mkdir(parents=True, exist_ok=True)
    (pages / "home.html").write_text(HOME_HTML)
    rows = [{"url": "https://acme.com/", "ok": True, "status": 200, "finalUrl": "https://www.acme.com/", "title": "Acme", "htmlFile": "home.html",
             "screenshotFile": None, "links": []}]
    if with_screenshot:
        (pages / "home.png").write_bytes(PNG_1x1); rows[0]["screenshotFile"] = "home.png"
    if with_pricing:
        (pages / "pricing.html").write_text(PRICING_HTML)
        rows.append({"url": "https://www.acme.com/pricing", "ok": True, "status": 200, "finalUrl": "https://www.acme.com/pricing", "title": "Pricing",
                     "htmlFile": "pricing.html", "screenshotFile": None, "links": []})
    rows.append({"url": "https://www.acme.com/gone", "ok": True, "status": 404, "finalUrl": "https://www.acme.com/gone", "htmlFile": "home.html", "links": []})
    rows.append({"url": "https://www.acme.com/blocked", "ok": False, "status": None, "finalUrl": "https://www.acme.com/blocked", "htmlFile": None, "links": []})
    prefetch.write_index(pages, rows)
    return pages


class PagesDir(unittest.TestCase):
    def test_load_pages_skips_failed_rows_and_puts_the_homepage_first(self):
        with tempfile.TemporaryDirectory() as d:
            pages = seed_pages(pathlib.Path(d) / "pages")
            # the index lists pricing after home; shuffle to prove ordering is by path depth, not file order
            rows = prefetch.read_index(pages); rows.reverse(); prefetch.write_index(pages, rows)
            logs = []
            loaded = prefetch.homepage_first(prefetch.load_pages(pages, logs.append))
        self.assertEqual([u for u, _ in loaded], ["https://www.acme.com/", "https://www.acme.com/pricing"])
        self.assertTrue(loaded[0][1]["screenshot"].endswith("home.png"))
        self.assertTrue(any("404" in l for l in logs) and any("not fetched" in l for l in logs))

    def test_pick_pages_cli_uses_links_or_anchors_and_skips_fetched_pages(self):
        with tempfile.TemporaryDirectory() as d:
            pages = seed_pages(pathlib.Path(d) / "pages")  # home row has no links: falls back to <a href> in the HTML
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "pick-pages", "--pages-dir", str(pages)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.split(), ["https://www.acme.com/product", "https://www.acme.com/blog/2026/launch", "https://www.acme.com/about"])  # pricing already fetched, privacy filtered
            rows = prefetch.read_index(pages)
            rows[0]["links"] = ["https://www.acme.com/customers/acme-story", "https://www.acme.com/about"]
            prefetch.write_index(pages, rows)
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "pick-pages", "--pages-dir", str(pages), "--max-pages", "1"], capture_output=True, text=True)
            self.assertEqual(r.stdout.split(), ["https://www.acme.com/customers/acme-story"])

    def test_pick_pages_cli_says_so_on_a_single_page_site(self):
        with tempfile.TemporaryDirectory() as d:
            pages = seed_pages(pathlib.Path(d) / "pages", with_pricing=False)
            (pages / "home.html").write_text('<html><head></head><body><a href="/">Home</a><a href="mailto:x@acme.com">Mail</a></body></html>')
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "pick-pages", "--pages-dir", str(pages)], capture_output=True, text=True)
            self.assertEqual((r.returncode, r.stdout), (0, ""))
            self.assertIn("single-page site", r.stderr)

    def test_fetch_asset_cli_downloads_with_caps_and_scheme_check(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "fetch-asset", "--out", d, "file:///etc/hosts"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("unsupported URL scheme", r.stderr)
            self.assertEqual(os.listdir(d), [])

    def test_pick_pages_cli_fails_without_a_homepage(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "pick-pages", "--pages-dir", d], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("ingest the homepage first", r.stderr)


class MineEndToEnd(unittest.TestCase):
    def setUp(self):
        self._http_get = prefetch.http_get

    def tearDown(self):
        prefetch.http_get = self._http_get

    def test_mine_builds_evidence_from_the_pages_dir_without_a_browser(self):
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            if url.endswith("/site.css"):
                return "@font-face{font-family:'Acme Sans';font-weight:500;src:url(/f/acme-500.woff2) format('woff2')} h1{font-family:'Acme Sans'} .btn{border-radius:8px;padding:12px 20px;background:#0055ff}"
            if url.endswith(".woff2"):
                return b"\0" * 64
            if url.endswith("/logo.svg"):
                return LOGO.encode()
            raise AssertionError(f"unexpected fetch {url}")
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            pages = seed_pages(pathlib.Path(d) / "pages")
            out = pathlib.Path(d) / "evidence"
            prefetch.cmd_mine(argparse.Namespace(pages_dir=pages, out=out, no_playwright=True, domain=None))
            ev = json.loads((out / "evidence.json").read_text())
            self.assertEqual(ev["domain"], "acme.com")
            self.assertEqual([p["slug"] for p in ev["pages"]], ["home", "pricing"])
            self.assertEqual(ev["pages"][0]["via"], "pages-dir")
            self.assertTrue(ev["pages"][0]["screenshot"].startswith("screenshots/home"))
            self.assertIsNone(ev["pages"][1]["screenshot"])
            self.assertEqual([s["url"] for s in ev["stylesheets"]], ["https://www.acme.com/site.css"])
            self.assertEqual(ev["fontFaces"][0]["displayFamily"], "Acme Sans")
            self.assertEqual(ev["fontFaces"][0]["file"], "fonts/acme-sans-500-normal.woff2")
            self.assertEqual(ev["logoCandidates"][0]["file"], "logos/logo-0-header.svg")
            self.assertEqual(len(ev["buttonRules"]), 1)
            self.assertEqual(ev["capabilities"], {"source": "pages-dir", "playwright": False, "playwrightDisabled": True, "playwrightError": None, "screenshots": 1, "headRecovered": [], "cssSignal": "ok"})
            self.assertEqual(ev["computed"], {})
            self.assertTrue((out / "pages" / "pricing.html").is_file())
            logo = ev["logoCandidates"][0]
            self.assertEqual((logo["inkMethod"], logo["suggestedSurface"]), ("declared", None))  # a saturated #0055ff mark reads on either surface
            self.assertAlmostEqual(logo["inkSaturation"], 1.0)
            self.assertEqual([h["kind"] for h in ev["heroImages"]], [])  # fixture has no poster, hero image or og:image

    def test_mine_downloads_the_weights_computed_styles_use_and_names_otf_files(self):
        otf = b"OTTO" + b"\0" * 60
        def fake_get(url, binary=False, timeout=25, max_bytes=None):
            if url.endswith("/site.css"):
                return ("@font-face{font-family:'Acme Sans';font-weight:300;src:url(/f/AcmeLight.otf) format('opentype')}"
                        "@font-face{font-family:'Acme Sans';font-weight:400;src:url(/f/AcmeRegular.otf) format('opentype')}"
                        "@font-face{font-family:'Acme Sans';font-weight:700;src:url(/f/AcmeBold.otf) format('opentype')}"
                        "h1,body{font-family:'Acme Sans'}")
            if url.endswith(".otf"):
                return otf
            if url.endswith("/logo.svg"):
                return LOGO.encode()
            raise AssertionError(f"unexpected fetch {url}")
        prefetch.http_get = fake_get
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d) / "fonts"; out.mkdir()
            ev = prefetch.mine_css(fake_get("x/site.css"), "https://www.acme.com/", out, NOOP_LOG)
            got = sorted(os.listdir(out))
            self.assertEqual(got, ["acme-sans-400-normal.otf", "acme-sans-700-normal.otf"])  # defaults: nearest to 400/500/700
            self.assertEqual({f["format"] for f in ev["fontFaces"]}, {"opentype"})
            # the rendered h1 uses 300: that face is fetched in the second pass
            comp = {"home": {"h1": {"fontFamily": "\"Acme Sans\", sans-serif", "fontWeight": "300"}, "body": {"fontFamily": "Acme Sans", "fontWeight": "400"}}}
            wanted = prefetch.computed_weights(comp)
            self.assertEqual(wanted, {("acme sans", 300), ("acme sans", 400)})
            extra = prefetch.faces_for_weights(ev["fontFaces"], wanted)
            self.assertEqual([f["weight"] for f in extra], ["300"])
            prefetch.download_faces(extra, "https://www.acme.com/", out, NOOP_LOG)
            self.assertIn("acme-sans-300-normal.otf", os.listdir(out))

    def test_font_ext_prefers_declared_format_then_url_then_magic_bytes(self):
        self.assertEqual(prefetch.font_ext("opentype", "https://x/a.woff2"), "otf")
        self.assertEqual(prefetch.font_ext("truetype", "https://x/a"), "ttf")
        self.assertEqual(prefetch.font_ext(None, "https://x/a.woff"), "woff")
        self.assertEqual(prefetch.font_ext("", "https://x/font?id=1", b"wOF2...."), "woff2")
        self.assertEqual(prefetch.font_ext("", "https://x/font?id=1", b"OTTO...."), "otf")
        self.assertEqual(prefetch.font_ext("", "https://x/font?id=1", b"\0\1\0\0...."), "ttf")

    def test_button_rules_skip_framework_resets(self):
        css = ("button,input,optgroup,select,textarea{font:inherit;margin:0;padding:0;border:0 solid}"
               "::file-selector-button{margin-inline-end:4px;padding:0;background:none}"
               ".btn-primary{background:#0055ff;border-radius:8px;padding:12px 20px}")
        with tempfile.TemporaryDirectory() as d:
            ev = prefetch.mine_css(css, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG)
        self.assertEqual([b["selector"] for b in ev["buttonRules"]], [".btn-primary"])

    def test_mine_exits_without_usable_pages(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(SKILL / "scripts/prefetch.py"), "mine", "--pages-dir", d, "--out", str(pathlib.Path(d) / "ev"), "--no-playwright"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertIn("no usable pages", json.loads((pathlib.Path(d) / "ev" / "evidence.json").read_text())["error"])


DOC = '<html><body><div class="sheet"><div class="hero is-dark">old</div><div class="stats">s</div></div></body></html>'


class GalleryComposition(unittest.TestCase):
    def test_composition_css_only_emits_requested_knobs(self):
        self.assertEqual(gallery.composition_css({"render": {}}), "")
        css = gallery.composition_css({"render": {"gallery": {"headingAlign": "center", "cardStyle": "hairline", "navStyle": "floating"}}})
        self.assertIn("text-align:center", css)
        self.assertIn(".hero h1,.hero .lead,.hero .actions", css)  # the h1 box (max-width:20ch) is centered too
        self.assertIn("border:1px solid var(--brand-border)", css)
        self.assertIn(".topbar{margin:14px 18px 0", css)

    def test_composed_spec_applies_surfaces_to_surface_blocks_only(self):
        with tempfile.TemporaryDirectory() as d:
            spec = gallery.composed_spec({"render": {"gallery": {"surfaces": {"hero": "light", "section": "dark", "footer": "dark"}}}}, pathlib.Path(d) / "s.json")
            blocks = {b["type"]: b for b in json.loads(spec.read_text())["blocks"]}
            self.assertEqual(blocks["hero"].get("surface"), "light")
            self.assertEqual(blocks["footer"].get("surface"), "dark")
            self.assertNotIn("surface", blocks["section"])

    def test_bespoke_hero_inlines_kit_images_and_keeps_safe_markup(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            (kit / "hero.html").write_text('<!-- note -->\n<section class="hero-bespoke" style="background:var(--brand-band)">'
                                           '<h1 style="color:var(--brand-ink)">Hi <em>there</em></h1>'
                                           '<a class="btn" href="https://example.com/">Go</a><a href="#more">More</a>'
                                           '<img src="logo.svg" alt="" width="120"></section>\n')
            out = gallery.swap_bespoke_hero(DOC, kit)
        self.assertNotIn("old", out)
        self.assertIn("Hi <em>there</em>", out)
        self.assertIn('src="data:image/svg+xml;base64,', out)
        self.assertNotIn("logo.svg", out)
        self.assertNotIn("note", out)
        self.assertIn('<div class="stats">s</div>', out)

    def test_bespoke_hero_refuses_every_bypass(self):
        cases = {
            "uppercase SRC": '<section><img SRC="https://evil.example/x.png"></section>',
            "protocol-relative src": '<section><img src="//evil.example/x.png"></section>',
            "srcset": '<section><img src="logo.svg" srcset="https://evil.example/x.png 2x"></section>',
            "event handler": '<section><img src="logo.svg" onerror="alert(1)"></section>',
            "javascript href": '<section><a href="javascript:alert(1)">x</a></section>',
            "data href": '<section><a href="data:text/html,x">x</a></section>',
            "css url()": '<section style="background:url(https://evil.example/x.png)"></section>',
            "css @import": '<section style="@import url(https://evil.example/x.css)"></section>',
            "inline svg": '<section><svg viewBox="0 0 1 1"><image href="https://evil.example/x.png"/></svg></section>',
            "script": '<section><script>alert(1)</script></section>',
            "style element": '<section><style>@import url(https://evil.example/x.css)</style></section>',
            "iframe": '<section><iframe src="https://evil.example/"></iframe></section>',
            "parent traversal": '<section><img src="../outside.svg"></section>',
            "absolute path": '<section><img src="/etc/hosts"></section>',
            "missing file": '<section><img src="nope.svg"></section>',
            "non-image file": '<section><img src="manifest.json"></section>',
            "symlinked asset": '<section><img src="link.svg"></section>',
            "two roots": '<section>a</section><section>b</section>',
            "not a section": '<div>a</div>',
            "doctype": '<!DOCTYPE html><section>a</section>',
        }
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            (pathlib.Path(d) / "outside.svg").write_text(LOGO)
            os.symlink(pathlib.Path(d) / "outside.svg", kit / "link.svg")
            for name, frag in cases.items():
                with self.subTest(case=name):
                    (kit / "hero.html").write_text(frag)
                    self.assertEqual(gallery.swap_bespoke_hero(DOC, kit), DOC)
            # hero.html itself must not be a symlink, even to a valid fragment
            (kit / "hero.html").unlink()
            (pathlib.Path(d) / "hero-outside.html").write_text('<section class="hero-bespoke">ok</section>')
            os.symlink(pathlib.Path(d) / "hero-outside.html", kit / "hero.html")
            self.assertEqual(gallery.swap_bespoke_hero(DOC, kit), DOC)

    def test_render_gallery_builds_components_html(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", gallery_block={"surfaces": {"hero": "dark"}, "headingAlign": "center"})
            r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            html = (kit / "components.html").read_text()
            self.assertIn("Kit reference: Acme", html)
            self.assertIn("data-composition", html)
            self.assertIn('class="hero is-dark"', html)

    def test_gallery_knobs_drop_eyebrows_and_add_the_secondary_button(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", gallery_block={"eyebrow": False, "secondaryCta": True})
            r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            html = (kit / "components.html").read_text()
        self.assertNotIn('class="eyebrow"', html)
        self.assertNotIn('class="k"', html)
        self.assertIn('class="btn btn-secondary"', html)

    def test_image_hero_inlines_the_kit_image_behind_the_copy(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", render_extra={"heroVisual": "image", "heroImage": "images/hero.png"})
            (kit / "images").mkdir(); (kit / "images" / "hero.png").write_bytes(PNG_1x1)
            r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            html = (kit / "components.html").read_text()
        self.assertIn('<div class="hero is-dark has-image"><img src="data:image/png;base64,', html)
        self.assertIn('<div class="hero-scrim"></div>', html)
        # a heroImage that escapes the kit is refused by validation
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", render_extra={"heroVisual": "image", "heroImage": "../outside.png"})
            r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)

    def test_kit_base_css_has_no_off_palette_literal(self):
        css = (SKILL / "assets" / "kit_base.css").read_text()
        self.assertNotIn("96,110,255", css)
        for m in re.finditer(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", css):
            r, g, b = (int(x) for x in m.groups())
            self.assertLessEqual(max(r, g, b) - min(r, g, b), 20, f"non-neutral literal in kit_base.css: {m.group(0)}")

    def test_comparison_block_honors_its_surface_knob(self):
        with tempfile.TemporaryDirectory() as d:
            light = make_kit(pathlib.Path(d) / "light", dark_band=False)
            dark_cmp = make_kit(pathlib.Path(d) / "dark-cmp", dark_band=False, gallery_block={"surfaces": {"comparison": "dark"}})
            for kit in (light, dark_cmp):
                r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('<div class="cmp cmp-soft">', (light / "components.html").read_text())
            self.assertIn('<div class="band is-dark"><div class="cmp cmp-band">', (dark_cmp / "components.html").read_text())


@unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
class RendererBands(unittest.TestCase):
    """Regressions that need a real layout engine."""

    def _computed(self, html_path, probes):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(html_path.resolve().as_uri())
            out = {sel: pg.evaluate(f"() => getComputedStyle(document.querySelector('{sel}')).{prop}") for sel, prop in probes}
            b.close()
        return out

    def test_dark_band_paints_without_glow_token(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            got = self._computed(kit / "components.html", [(".hero", "backgroundColor"), (".section p", "color")])
        self.assertEqual(got[".hero"], "rgb(16, 32, 48)")  # --brand-band, not transparent
        self.assertEqual(got[".section p"], "rgb(17, 17, 17)")  # body copy falls back to --brand-ink

    def test_square_brand_and_outline_button_tokens_render(self):
        tokens = {"--brand-radius": "0", "--brand-btn-bg": "transparent", "--brand-btn-ink": "#111111", "--brand-btn-border": "#111111",
                  "--brand-btn-weight": "500", "--brand-weight-h1": "300"}
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", extra_tokens=tokens)
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            got = self._computed(kit / "components.html", [(".fcard", "borderRadius"), (".cmp-band", "borderRadius"), (".quote", "borderRadius"),
                                                            (".plan-badge", "borderRadius"), (".section .k", "color"),
                                                            (".hero h1", "fontWeight"), (".section h2", "fontWeight")])
        self.assertEqual((got[".fcard"], got[".cmp-band"], got[".quote"]), ("0px", "0px", "0px"))
        self.assertEqual(got[".plan-badge"], "999px")  # the badge keeps its own pill fallback
        self.assertEqual(got[".section .k"], "rgb(0, 85, 255)")  # kickers still use --brand-primary, not the button tokens
        self.assertEqual(got[".hero h1"], "300")
        self.assertEqual(got[".section h2"], "600")

    def test_outline_button_border_and_weight(self):
        tokens = {"--brand-btn-bg": "transparent", "--brand-btn-ink": "#111111", "--brand-btn-border": "#111111", "--brand-btn-weight": "500"}
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", extra_tokens=tokens)
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(); pg = b.new_page(); pg.goto((kit / "components.html").resolve().as_uri())
                got = pg.evaluate("() => { const s = getComputedStyle(document.querySelector('.btn-primary')); return [s.backgroundColor, s.color, s.borderTopColor, s.borderTopStyle, s.fontWeight]; }")
                b.close()
        self.assertEqual(got, ["rgba(0, 0, 0, 0)", "rgb(17, 17, 17)", "rgb(17, 17, 17)", "solid", "500"])

    def test_secondary_labels_are_legible_on_light_surfaces(self):
        spec = {"title": "t", "blocks": [
            {"type": "logos", "label": "Trusted by", "items": [{"text": "A"}, {"text": "B"}]},
            {"type": "cta", "heading": "Go", "custLine": "Used by <b>many</b>"},
        ]}
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", dark_band=False)
            (kit / "spec.json").write_text(json.dumps(spec))
            out = kit / "out.html"
            subprocess.run([sys.executable, str(SKILL / "scripts/render_kit.py"), "--kit-dir", str(kit), "--spec", str(kit / "spec.json"), "--out", str(out)],
                           check=True, capture_output=True)
            got = self._computed(out, [(".logos-label", "color"), (".cust-line", "color")])
        self.assertEqual(got[".logos-label"], "rgb(85, 85, 85)")  # --brand-muted, not a white tint
        self.assertEqual(got[".cust-line"], "rgb(85, 85, 85)")

    def test_gallery_spacing_units_icons_and_both_logos(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            man = json.loads((kit / "manifest.json").read_text())
            man["render"]["gallery"] = {"secondaryCta": True}
            (kit / "manifest.json").write_text(json.dumps(man))
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            doc = (kit / "components.html").read_text()
            self.assertIn('class="u w">min<', doc)  # word unit set apart, "%" stays tight
            self.assertIn('class="u">%<', doc)
            self.assertIn("onLight", doc); self.assertIn("onDark", doc)  # both logo variants in the reference strip
            self.assertNotIn("system-ui", doc)
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 900})
                pg.goto((kit / "components.html").resolve().as_uri())
                got = pg.evaluate("""() => {
                    const r = s => document.querySelector(s).getBoundingClientRect();
                    const n = document.querySelector('.stats .stat .n'), rg = document.createRange(); rg.selectNodeContents(n);
                    return [r('.hero .btn-secondary').left - r('.hero .btn-primary').right,
                            rg.getBoundingClientRect().left - r('.stats').left,
                            r('.hero h1').left - r('.hero').left]; }""")
                b.close()
        self.assertGreaterEqual(got[0], 10)  # hero buttons never touch
        self.assertAlmostEqual(got[1], got[2], delta=2)  # stat copy sits on the page gutter

    def test_icons_json_list_form_resolves_by_name(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            (kit / "icons.json").write_text(json.dumps([{"name": "spark", "viewBox": "0 0 24 24", "inner": '<path d="M1 1h2"/>'}]))
            (kit / "spec.json").write_text(json.dumps({"title": "t", "blocks": [
                {"type": "features", "items": [{"title": "A", "text": "b", "icon": "spark"}]}]}))
            out = kit / "out.html"
            subprocess.run([sys.executable, str(SKILL / "scripts/render_kit.py"), "--kit-dir", str(kit), "--spec", str(kit / "spec.json"), "--out", str(out)],
                           check=True, capture_output=True)
            self.assertIn('<path d="M1 1h2"/>', out.read_text())

    def test_comparison_headers_align_with_their_columns(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            self.assertNotIn("gdot", (kit / "components.html").read_text())  # no invented glow dot in the header
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(); pg = b.new_page(); pg.goto((kit / "components.html").resolve().as_uri())
                got = pg.evaluate("""() => {
                    const q = s => document.querySelector(s);
                    const text = el => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect().left; };
                    return [text(q('.cmp-band .head .bad')) - q('.cmp-band .r .bad .m').getBoundingClientRect().left,
                            text(q('.cmp-band .head .good')) - q('.cmp-band .r .good .m').getBoundingClientRect().left]; }""")
                b.close()
        for delta in got:
            self.assertLess(abs(delta), 1.0)  # each header label starts over its column's icon


class MinerSecondPass(unittest.TestCase):
    """Fixes from the octavehq.com run: widget noise, wrapped alt text, logo walls by count, video frames, Playwright diagnostics."""

    def setUp(self):
        self._http_get = prefetch.http_get

    def tearDown(self):
        prefetch.http_get = self._http_get

    def test_css_of_page_skips_third_party_widget_sheets(self):
        fetched = []
        def fake_get(url, **kw):
            fetched.append(url); return ".brand{color:#123456}"
        prefetch.http_get = fake_get
        html = ('<html><head><link rel="stylesheet" href="/css/site.css">'
                '<link rel="stylesheet" href="https://static.hsappstatic.net/MeetingsPublic/static-1.6/main.css"></head><body></body></html>')
        with tempfile.TemporaryDirectory() as d:
            text, meta, _ = prefetch.css_of_page(html, "https://a.example/", pathlib.Path(d), NOOP_LOG)
        self.assertEqual(fetched, ["https://a.example/css/site.css"])
        self.assertEqual([s["url"] for s in meta], ["https://a.example/css/site.css"])

    def test_widget_custom_properties_are_not_brand(self):
        for name in ("--hs-color-primary", "--hsfc-input-bg", "--trellis-space-1", "--cky-btn"):
            self.assertTrue(prefetch.THIRD_PARTY_PROP.match(name), name)
        for name in ("--base-color-brand--violet", "--hsl-x", "--color-primary"):
            self.assertFalse(prefetch.THIRD_PARTY_PROP.match(name), name)

    def test_lift_logos_normalizes_alt_text_and_flags_logo_walls_by_count(self):
        wall = "".join(f'<img alt="Customer {i} logo" src="/customers/c{i}.png">' for i in range(4))
        html = ('<html><body><header class="site-nav"><a href="/"><img alt="Acme\n      logo" src="/acme.png"></a>'
                f'<div class="strip">{wall}</div></header></body></html>')
        prefetch.http_get = lambda url, binary=False, timeout=25, max_bytes=None: PNG_1x1
        with tempfile.TemporaryDirectory() as d:
            out, _ = prefetch.lift_logos(html, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG)
        by_src = {c["src"]: c for c in out}
        brand = by_src["https://www.acme.com/acme.png"]
        self.assertEqual(brand["alt"], "Acme logo")  # the line break in the markup is gone, so LOGO_HINT matched
        self.assertTrue(brand["homeLink"]); self.assertFalse(brand["suspectWall"])
        self.assertTrue(all(by_src[f"https://www.acme.com/customers/c{i}.png"]["suspectWall"] for i in range(4)))

    def test_lift_images_grabs_a_frame_when_the_video_has_no_poster(self):
        html = ('<html><body><main><section><video autoplay muted><source src="/media/orb.mp4" type="video/mp4"></video>'
                '</section></main></body></html>')
        grabbed = []
        def fake_grab(url, out_path, log):
            grabbed.append(url); out_path.write_bytes(b"\xff\xd8\xff" + b"\0" * 10); return True
        with tempfile.TemporaryDirectory() as d:
            out = prefetch.lift_images(html, "https://www.acme.com/", pathlib.Path(d), NOOP_LOG, grab=fake_grab)
        self.assertEqual(grabbed, ["https://www.acme.com/media/orb.mp4"])
        self.assertEqual([(o["kind"], o["file"]) for o in out], [("video", None), ("video-frame", "images/video-frame-1.jpg")])

    def test_video_frame_refuses_non_http_sources(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(prefetch.video_frame("file:///etc/hosts", pathlib.Path(d) / "f.jpg", NOOP_LOG))

    def test_browser_records_why_playwright_is_off(self):
        b = prefetch.Browser(False, NOOP_LOG)
        self.assertTrue(b.disabled); self.assertIsNone(b.error); self.assertIsNone(b.pw)


@unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
class RendererSecondPass(unittest.TestCase):
    """Depth hygiene, the new knobs and the product-page copy."""

    def _gallery(self, d, tokens=None, gallery=None, icons=None):
        kit = make_kit(pathlib.Path(d) / "kit", extra_tokens=tokens, gallery_block=gallery)
        if icons is not None:
            (kit / "icons.json").write_text(json.dumps(icons))
        subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
        return kit

    def _eval(self, kit, js):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 900})
            pg.goto((kit / "components.html").resolve().as_uri())
            got = pg.evaluate(js); b.close()
        return got

    def test_glow_and_texture_paint_the_hero_only(self):
        tokens = {"--brand-glow": "radial-gradient(circle at 50% 0%, rgba(120,80,255,.6), transparent 60%)",
                  "--brand-texture": "radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.4px) 0 0/22px 22px"}
        with tempfile.TemporaryDirectory() as d:
            kit = self._gallery(d, tokens)
            got = self._eval(kit, """() => Object.fromEntries(['.hero', '.cta', '.footer', '.quote', '.cmp-band .head'].map(s => {
                const el = document.querySelector(s); const cs = getComputedStyle(el);
                return [s, [/gradient|url\\(/.test(cs.backgroundImage), getComputedStyle(el, '::before').content]]; }))""")
        self.assertTrue(got[".hero"][0])
        for sel in (".cta", ".footer", ".quote", ".cmp-band .head"):
            self.assertFalse(got[sel][0], sel)  # solid band, no repeated glow
        self.assertIn(got[".cmp-band .head"][1], ("none", "normal"))  # the header's glow layers are gone

    def test_stat_tokens_chip_eyebrow_inset_stats_and_no_default_arrow(self):
        tokens = {"--brand-stat-weight": "300", "--brand-stat-ink": "#ff0000"}
        gallery = {"eyebrowStyle": "chip", "statsStyle": "inset"}
        with tempfile.TemporaryDirectory() as d:
            kit = self._gallery(d, tokens, gallery)
            doc = (kit / "components.html").read_text()
            got = self._eval(kit, """() => { const n = getComputedStyle(document.querySelector('.stat .n'));
                const e = getComputedStyle(document.querySelector('.hero .eyebrow')); const s = getComputedStyle(document.querySelector('.stats'));
                return [n.fontWeight, n.color, e.borderTopStyle, e.borderTopLeftRadius, s.marginLeft]; }""")
        self.assertEqual(got[:2], ["300", "rgb(255, 0, 0)"])
        self.assertEqual(got[2], "solid"); self.assertEqual(got[3], "999px"); self.assertEqual(got[4], "56px")
        self.assertNotIn('class="arw"', doc)  # the arrow is a device the kit must ask for

    def test_arrow_knob_adds_the_trailing_arrow(self):
        with tempfile.TemporaryDirectory() as d:
            kit = self._gallery(d, gallery={"arrow": True})
            self.assertIn('class="arw"', (kit / "components.html").read_text())

    def test_two_plans_fill_the_row_and_features_take_kit_icons(self):
        icons = [{"name": n, "viewBox": "0 0 24 24", "inner": f'<path d="M{i} 1h2"/>'} for i, n in enumerate(("spark", "bolt", "ring"))]
        with tempfile.TemporaryDirectory() as d:
            kit = self._gallery(d, icons=icons)
            doc = (kit / "components.html").read_text()
            got = self._eval(kit, """() => { const r = s => document.querySelector(s).getBoundingClientRect();
                return [r('.plan').width / r('.pricing').width, Array.from(document.querySelectorAll('.fcard .tile')).filter(t => !t.innerHTML.trim()).length]; }""")
        self.assertGreater(got[0], 0.45)  # two plans share the full width instead of leaving a third column empty
        self.assertEqual(got[1], 0)  # every tile shows one of the kit's own icons
        for path in ('<path d="M0 1h2"/>', '<path d="M1 1h2"/>', '<path d="M2 1h2"/>'):
            self.assertIn(path, doc)

    def test_gallery_copy_reads_as_a_product_page(self):
        with tempfile.TemporaryDirectory() as d:
            kit = self._gallery(d)
            doc = (kit / "components.html").read_text()
        for meta in ("Heading with one", "Card one", "CTA band in the brand", "Primary action", "Stat block"):
            self.assertNotIn(meta, doc)
        self.assertIn("Book a demo", doc)

    def test_emphasis_off_keeps_the_copy_without_the_marked_word(self):
        with tempfile.TemporaryDirectory() as d:
            on = (self._gallery(d, gallery={"emphasis": True}) / "components.html").read_text()
            off = (self._gallery(d + "/off", gallery={"emphasis": False}) / "components.html").read_text()
        self.assertIn("one record", on); self.assertIn("one record", off)
        self.assertGreater(on.count('class="hl'), off.count('class="hl'))


@unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
class ThirdPassRegressions(unittest.TestCase):
    """What the second octavehq.com run found live: light closing surfaces on a dark kit, surfaces in the
    one-pager, kicker chips, stale checksums after a gallery rebuild, gradient contrast."""

    def _render_both(self, kit):
        subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
        one = kit.parent / "onepager.html"
        subprocess.run([sys.executable, str(SKILL / "scripts/render_kit.py"), "--kit-dir", str(kit), "--spec", str(SKILL / "assets/onepager_spec.json"), "--out", str(one)],
                       check=True, capture_output=True)
        return (kit / "components.html").read_text(), one.read_text(), one

    def test_dark_kit_closing_on_light_cta_and_white_footer(self):
        gallery = {"surfaces": {"cta": "light", "footer": "light"}, "eyebrowStyle": "chip"}
        tokens = {"--brand-glow": "radial-gradient(ellipse at 50% -20%, rgba(140,90,255,.75), transparent 60%)"}
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", extra_tokens=tokens, gallery_block=gallery)
            gal, one, one_path = self._render_both(kit)
            for doc, name in ((gal, "gallery"), (one, "one-pager")):
                self.assertIn('class="cta"', doc, name); self.assertNotIn('class="cta is-dark"', doc, name)  # the surface reaches both
                self.assertIn('class="footer light"', doc, name)
            self.assertIn('class="k chip"', gal)  # kickers share the hero eyebrow's chip style
            gate = subprocess.run([sys.executable, str(SKILL / "scripts/gate_check.py"), str(kit / "components.html")], capture_output=True, text=True)
            self.assertEqual(gate.returncode, 0, gate.stdout)  # light CTA copy and footer links stay legible
            gate1 = subprocess.run([sys.executable, str(SKILL / "scripts/gate_check.py"), str(one_path)], capture_output=True, text=True)
            self.assertNotIn("FAIL contrast .cta", gate1.stdout)

    def test_gallery_rebuild_refreshes_checksums(self):
        sys.path.insert(0, str(SKILL / "scripts"))
        import brand_cache
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            brand_cache.write_checksums(kit)
            before = json.loads((kit / "manifest.json").read_text())["assetChecksums"]
            man = json.loads((kit / "manifest.json").read_text()); man["render"]["gallery"] = {"arrow": True}
            (kit / "manifest.json").write_text(json.dumps(man))
            (kit / "tokens.css").write_text((kit / "tokens.css").read_text() + "\n/* repaired */\n")  # a catalogued asset edited before the render
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            after = json.loads((kit / "manifest.json").read_text())["assetChecksums"]
            self.assertIn("components.html", after)
            self.assertNotEqual(before["tokens.css"], after["tokens.css"])  # re-catalogued before the renderer validated it
            self.assertNotEqual(before.get("components.html"), after["components.html"])  # the rebuilt gallery is catalogued
            self.assertEqual(brand_cache.write_checksums(kit), after)  # and nothing else is stale

    def test_gradient_fill_is_measured_against_its_own_stops(self):
        html = ('<html><body style="background:#fff"><div class="cta" style="background:linear-gradient(90deg, rgb(168,136,248), rgb(200,184,248));padding:20px">'
                '<h2 style="color:#fff;font-size:28px">Closing band</h2></div></body></html>')
        with tempfile.TemporaryDirectory() as d:
            page = pathlib.Path(d) / "t.html"; page.write_text(html); rep = pathlib.Path(d) / "g.json"
            subprocess.run([sys.executable, str(SKILL / "scripts/gate_check.py"), str(page), "--json", str(rep)], capture_output=True, text=True)
            cta = next(c for c in json.loads(rep.read_text())["checks"] if c["name"] == "contrast .cta h2")
        self.assertGreater(cta["value"], 1.5)  # white on lavender, not white on the white page behind the gradient
        self.assertLess(cta["value"], 3)  # and honestly below the bar: the lightest stop decides
        self.assertIn("colour stops", cta["note"])


class FetchGuardAndStrips(unittest.TestCase):
    """Fetches stay on public hosts; the homepage gets a dedicated bottom strip."""

    def test_public_host_refuses_local_private_and_link_local_targets(self):
        for url in ("http://localhost/x", "http://127.0.0.1:3015/x", "http://10.0.0.5/f.mp4", "http://192.168.1.9/", "http://169.254.169.254/latest",
                    "http://[::1]/", "http://printer.local/", "http://db.internal/"):
            with self.assertRaises(ValueError, msg=url):
                prefetch.public_host(url)
        self.assertEqual(prefetch.public_host("https://8.8.8.8/logo.svg"), "8.8.8.8")

    def test_http_fetch_refuses_before_any_request(self):
        with self.assertRaises(ValueError):
            prefetch.http_fetch("http://127.0.0.1:3015/assets")
        with self.assertRaises(ValueError):
            prefetch.http_fetch("file:///etc/hosts")

    def test_video_frame_refuses_a_private_source_without_running_ffmpeg(self):
        logs = []
        with tempfile.TemporaryDirectory() as d:
            ok = prefetch.video_frame("http://10.1.2.3/hero.mp4", pathlib.Path(d) / "f.jpg", logs.append)
        self.assertFalse(ok)
        self.assertTrue(any("refused" in m for m in logs), logs)

    def test_crops_cut_a_bottom_strip_for_tall_homepages(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d); shot = d / "home.png"
            Image.new("RGB", (1200, 12000), (20, 30, 40)).save(shot)
            got = prefetch.crops(shot, d, "home")
            fields = prefetch.shot_fields(got, d)
        self.assertEqual(len(got["strips"]), 6)  # the first 9600px as before
        self.assertTrue(got["bottom"].endswith("home-bottom.png"))
        self.assertEqual(fields["screenshotBottom"], "home-bottom.png")


if __name__ == "__main__":
    unittest.main()
