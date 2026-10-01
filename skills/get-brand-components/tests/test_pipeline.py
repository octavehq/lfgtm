"""Deterministic checks for the evidence-pack + mechanical-gallery pipeline (no network, no LLM)."""
import importlib.util
import json
import os
import pathlib
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


def make_kit(root, extra_tokens=None, gallery_block=None, dark_band=True):
    root.mkdir(parents=True, exist_ok=True)
    tokens = dict(REQUIRED_TOKENS, **(extra_tokens or {}))
    render = {"hasDarkBand": dark_band, "docWidth": 880, "heroVisual": "none", "fonts": [],
              "logo": {"onLight": "logo.svg", "onDark": "logo.svg", "lockup": None}, "tokens": tokens}
    if gallery_block:
        render["gallery"] = gallery_block
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
            text, meta = prefetch.css_of_page(html, "https://a.example/", pathlib.Path(d), NOOP_LOG)
        self.assertIn("url(https://a.example/vendor/fonts/inter.woff2)", text)  # against the import, not the parent sheet
        self.assertIn("url(https://a.example/css/img/bg.png)", text)
        self.assertIn("url(https://a.example/y.png)", text)
        self.assertEqual([s["url"] for s in meta], ["https://a.example/css/main.css"])

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


class FetchTiers(unittest.TestCase):
    def test_http_tier_keeps_final_url_and_status(self):
        saved = prefetch.http_fetch
        prefetch.http_fetch = lambda url, **kw: (b"<html></html>", "https://www.acme.com/home", 200)
        try:
            f = prefetch.Fetcher(pathlib.Path("."), None, False, NOOP_LOG)
            r = f.http("https://acme.com/")
        finally:
            prefetch.http_fetch = saved
        self.assertEqual(r["final_url"], "https://www.acme.com/home")
        self.assertEqual(r["status"], 200)

    def test_runner_rows_with_error_status_are_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d)
            (out / "firecrawl").mkdir()
            (out / "firecrawl" / "ok.html").write_text("<html></html>")
            (out / "firecrawl" / "bad.html").write_text("<html>not found</html>")
            (out / "firecrawl" / "firecrawl.json").write_text(json.dumps([
                {"url": "https://acme.com/", "ok": True, "status": 200, "finalUrl": "https://www.acme.com/", "htmlFile": "ok.html"},
                {"url": "https://acme.com/gone", "ok": True, "status": 404, "finalUrl": "https://acme.com/gone", "htmlFile": "bad.html"},
            ]))
            logs = []
            f = prefetch.Fetcher(out, "true", False, logs.append)  # `true` exits 0 without touching the pre-written json
            got = f.firecrawl(["https://acme.com/", "https://acme.com/gone"])
        self.assertEqual(list(got), ["https://acme.com/"])
        self.assertEqual(got["https://acme.com/"]["final_url"], "https://www.acme.com/")
        self.assertTrue(any("404" in l for l in logs))


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


if __name__ == "__main__":
    unittest.main()
