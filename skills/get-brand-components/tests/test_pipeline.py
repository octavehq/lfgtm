"""Deterministic checks for the evidence-pack + mechanical-gallery pipeline (no network, no LLM)."""
import importlib.util
import json
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

REQUIRED_TOKENS = {
    "--brand-bg": "#ffffff", "--brand-ink": "#111111", "--brand-primary": "#0055ff", "--brand-primary-ink": "#ffffff",
    "--brand-font-heading": "Georgia, serif", "--brand-font-body": "Arial, sans-serif", "--brand-band": "#102030",
    "--brand-on-dark": "#ffffff", "--brand-muted": "#555555", "--brand-border": "#dddddd", "--brand-surface": "#f6f6f6",
}
LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 30" width="120" height="30"><rect x="0" y="0" width="120" height="30" fill="#0055ff"/></svg>'


def make_kit(root, extra_tokens=None, gallery_block=None):
    root.mkdir(parents=True, exist_ok=True)
    tokens = dict(REQUIRED_TOKENS, **(extra_tokens or {}))
    render = {"hasDarkBand": True, "docWidth": 880, "heroVisual": "none", "fonts": [],
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


class GalleryComposition(unittest.TestCase):
    def test_composition_css_only_emits_requested_knobs(self):
        self.assertEqual(gallery.composition_css({"render": {}}), "")
        css = gallery.composition_css({"render": {"gallery": {"headingAlign": "center", "cardStyle": "hairline", "navStyle": "floating"}}})
        self.assertIn("text-align:center", css)
        self.assertIn("border:1px solid var(--brand-border)", css)
        self.assertIn(".topbar{margin:14px 18px 0", css)

    def test_composed_spec_applies_surfaces_to_surface_blocks_only(self):
        with tempfile.TemporaryDirectory() as d:
            spec = gallery.composed_spec({"render": {"gallery": {"surfaces": {"hero": "light", "section": "dark", "footer": "dark"}}}}, pathlib.Path(d) / "s.json")
            blocks = {b["type"]: b for b in json.loads(spec.read_text())["blocks"]}
            self.assertEqual(blocks["hero"].get("surface"), "light")
            self.assertEqual(blocks["footer"].get("surface"), "dark")
            self.assertNotIn("surface", blocks["section"])

    def test_bespoke_hero_refuses_external_resources(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            (kit / "hero.html").write_text('<section class="hero-bespoke"><img src="https://evil.example/x.png"></section>')
            doc = '<html><body><div class="sheet"><div class="hero is-dark">old</div><div class="stats">s</div></div></body></html>'
            self.assertEqual(gallery.swap_bespoke_hero(doc, kit), doc)
            (kit / "hero.html").write_text('<section class="hero-bespoke"><img src="logo.svg"></section>')
            out = gallery.swap_bespoke_hero(doc, kit)
            self.assertNotIn("old", out)
            self.assertIn("data:image/svg+xml;base64,", out)

    def test_render_gallery_builds_components_html(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", gallery_block={"surfaces": {"hero": "dark"}, "headingAlign": "center"})
            r = subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            html = (kit / "components.html").read_text()
            self.assertIn("Kit reference: Acme", html)
            self.assertIn("data-composition", html)
            self.assertIn('class="hero is-dark"', html)


@unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
class RendererBands(unittest.TestCase):
    """Regression: a kit without glow/texture tokens must still paint its dark bands."""

    def test_dark_band_paints_without_glow_token(self):
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
            with sync_playwright() as p:
                b = p.chromium.launch()
                pg = b.new_page()
                pg.goto((kit / "components.html").resolve().as_uri())
                hero_bg = pg.evaluate("() => getComputedStyle(document.querySelector('.hero')).backgroundColor")
                hl_bg = pg.evaluate("() => getComputedStyle(document.querySelector('.section p')).color")
                b.close()
            self.assertEqual(hero_bg, "rgb(16, 32, 48)")  # --brand-band, not transparent
            self.assertEqual(hl_bg, "rgb(17, 17, 17)")  # body copy falls back to --brand-ink


if __name__ == "__main__":
    unittest.main()
