"""Run with: python3 -m unittest discover -s skills/get-brand-components/tests"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_adherence.py"


class AdherenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kit = Path(self.tmp.name)
        self.manifest = {
            "render": {
                "tokens": {"--brand-primary": "#123456"},
                "tokensDark": {"--brand-primary": "#abcdef"},
                "fonts": [{"family": "Example Sans"}],
                "webfonts": "https://example.com/approved-fonts.css",
            }
        }
        (self.kit / "manifest.json").write_text(json.dumps(self.manifest))

    def check(self, html, code, kit=None):
        path = self.kit / "output.html"
        path.write_text(html)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--file", str(path),
             "--kit-dir", str(kit or self.kit)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_output_variables_cannot_approve_off_palette_colors(self):
        for key in ("--arbitrary-color", "--brand-primary"):
            with self.subTest(key=key):
                self.check(f"<style>:root{{{key}:#ff00ff}}p{{color:var({key})}}</style>", 1)

    def test_kit_palette_and_theme_override_pass(self):
        self.check("<style>p{color:#123456}b{color:#abcdef}</style>", 0)

    def test_remote_resources_are_detected(self):
        for html in (
            "<img src='https://example.com/image.png'>",
            '<img src="https://example.com/image">',
            '<img src=//example.com/image>',
            '<img srcset="https://example.com/small 1x, https://example.com/large 2x">',
            "<style>@font-face{font-family:'Example Sans';src:url(https://example.com/font.woff2)}</style>",
            "<div style=\"background:url('https://example.com/image')\"></div>",
            '<style>@import "https://example.com/style.css";</style>',
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unapproved">',
            '<svg><image href="https://example.com/image.svg"/></svg>',
        ):
            with self.subTest(html=html):
                self.check(html, 1)

    def test_ordinary_links_and_embedded_assets_pass(self):
        self.check('<a href="https://example.com/report.pdf">Report</a>'
                   '<img src="data:image/png;base64,AAAA">', 0)

    def test_only_declared_webfont_stylesheet_is_exempt(self):
        self.check('<link rel="stylesheet" href="https://example.com/approved-fonts.css">', 0)
        self.check('<img src="https://example.com/approved-fonts.css">', 1)

    def test_font_from_tokens_css_passes_but_unknown_font_fails(self):
        (self.kit / "tokens.css").write_text(':root{--brand-font-heading:"Kit Display",sans-serif}')
        self.check('<style>h1{font-family:"Kit Display",sans-serif}</style>', 0)
        self.check('<style>h1{font-family:"Unknown Display",sans-serif}</style>', 1)

    def test_missing_explicit_kit_returns_usage_error(self):
        self.check("<p>Example</p>", 2, self.kit / "missing")

    def test_clean_result_does_not_claim_self_containment(self):
        output = self.check('<p>Example</p>', 0)
        self.assertNotIn("output is self-contained", output)


if __name__ == "__main__":
    unittest.main()
