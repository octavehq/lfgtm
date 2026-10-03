"""judge_context.py: the judge-context file is built from the reports, never typed by hand."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import judge_context  # noqa: E402

DESIGN = """BRAND DESIGN FINDINGS — acme.com
1. Fonts: Alliance 400 h1 (source computed.home.h1.fontWeight)
2. Palette (dark-only, defaultTheme dark except a white footer): bg #08062c ...
3. Emphasis mechanism: none in headlines (computed.home.emphasis empty). Headline emphasis: NO.
4. Buttons: 40px, radius 8px, arrow yes (source computed.home.buttons[0])
7. Devices:
- accented headline word: no (computed.home.emphasis)
- all-caps eyebrow: yes, chip (home-strip2.png)
- arrow on buttons: yes (computed.home.buttons[0].inner)
- glow: hero only (home-top.png)
8. Proposed tokens: --brand-weight-h1 400
"""
LOGO = """BRAND LOGO FINDINGS — acme.com
onLight: logos/logo-1.svg · https://acme.com/logo.svg · header · 0.1 · reads Acme
hero imagery: heroVisual image · images/video-frame-1.jpg (ffmpeg frame, diagram with labels) · scrim: none · frame carries UI text
icons: lifted 20
"""


class JudgeContext(unittest.TestCase):
    def test_build_carries_devices_hero_measurements_and_map(self):
        gate = {"pass": True, "checks": [{"name": "contrast .cta h2", "ok": True, "value": 8.9, "want": ">= 3"},
                                         {"name": "gutter alignment", "ok": True, "value": [56, 56, 56, 56], "want": "left edges within 2px"}]}
        text = judge_context.build(DESIGN, LOGO, gate, "shots/home-top.png",
                                   ["shots/home-strip1.png", "shots/home-strip2.png", "shots/home-strip3.png"], hero_visual="none", domain="acme.com", rnd=2)
        self.assertIn("3. Emphasis mechanism: none in headlines", text)
        self.assertIn("- glow: hero only (home-top.png)", text)
        self.assertNotIn("8. Proposed tokens", text)  # judges never see the author's inputs beyond the devices
        self.assertIn("`none`.", text); self.assertIn("frame carries UI text", text)
        self.assertIn("- contrast .cta h2: 8.9 (want >= 3)", text)
        self.assertIn("Stats, cards, comparison, quote -> shots/home-strip2.png", text)
        self.assertIn("CTA and footer -> shots/home-strip3.png", text)
        self.assertIn("Do not invent a device", text)

    def test_near_blank_last_strip_points_at_the_strip_before(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            Image.new("RGB", (400, 400), (8, 6, 44)).save(d / "s2.png")  # flat: the footer never mounted
            busy = Image.new("RGB", (400, 400)); busy.putdata([((x * 7) % 256, (x * 13) % 256, (x * 3) % 256) for x in range(160000)]); busy.save(d / "s1.png")
            text = judge_context.build(DESIGN, LOGO, None, "top.png", [str(d / "s1.png"), str(d / "s2.png")])
        self.assertIn("near-blank", text); self.assertIn(f"CTA and footer -> {d / 's1.png'}", text)
        self.assertIn("NOT RUN (no gate.json)", text)

    def test_cli_writes_the_file(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d); (d / "design.md").write_text(DESIGN); (d / "logo.md").write_text(LOGO)
            (d / "gate.json").write_text(json.dumps({"pass": False, "checks": []}))
            r = subprocess.run([sys.executable, str(SKILL / "scripts/judge_context.py"), "--design", str(d / "design.md"), "--logo", str(d / "logo.md"),
                                "--gate", str(d / "gate.json"), "--top", "top.png", "--strips", "a.png", "b.png", "--domain", "acme.com", "--out", str(d / "reports/ctx.md")],
                               capture_output=True, text=True, check=True)
            self.assertTrue((d / "reports/ctx.md").is_file()); self.assertIn("pass: False", (d / "reports/ctx.md").read_text())


    def test_bottom_strip_owns_cta_and_footer_and_contexts_are_per_artifact(self):
        text = judge_context.build(DESIGN, LOGO, {"pass": True, "checks": []}, "top.png", ["s1.png", "s2.png", "s3.png"],
                                   bottom="bottom.png", artifact="one-pager", version=2, rnd=1, domain="acme.com")
        self.assertIn("CTA and footer -> bottom.png", text)
        self.assertNotIn("CTA and footer -> s3.png", text)
        self.assertIn("# Judge context: acme.com, one-pager, kit v2, round 1", text)
        self.assertIn("## Pre-gate measurements (one-pager)", text)
        not_run = judge_context.build(DESIGN, LOGO, {"pass": False, "notRun": "browser could not run: boom", "checks": []}, "top.png", [])
        self.assertIn("NOT RUN: browser could not run: boom", not_run)


if __name__ == "__main__":
    unittest.main()
