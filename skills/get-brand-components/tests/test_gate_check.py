"""gate_check.py: the mechanical pre-gate measures what judges would otherwise guess from pixels."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "tests"))
from test_pipeline import make_kit  # noqa: E402

GATE = SKILL / "scripts" / "gate_check.py"


@unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
class GateCheck(unittest.TestCase):
    def _run(self, kit):
        subprocess.run([sys.executable, str(SKILL / "scripts/render_gallery.py"), str(kit)], check=True, capture_output=True)
        report = kit.parent / "gate.json"
        r = subprocess.run([sys.executable, str(GATE), str(kit / "components.html"), "--json", str(report)], capture_output=True, text=True)
        return r.returncode, json.loads(report.read_text()), r.stdout

    def test_fixture_kit_passes_every_check(self):
        with tempfile.TemporaryDirectory() as d:
            code, rep, out = self._run(make_kit(pathlib.Path(d) / "kit"))
        self.assertEqual(code, 0, out)
        names = {c["name"] for c in rep["checks"]}
        for name in ("contrast .section p", "contrast .hero h1", "gutter alignment", "logo variants in reference strip", "empty icon tiles", "body measure"):
            self.assertIn(name, names)
        self.assertTrue(out.strip().endswith("PASS"))

    def test_dark_only_kit_with_dark_ink_fails_contrast(self):
        tokens = {"--brand-bg": "#0b0b1e", "--brand-canvas": "#0b0b1e", "--brand-ink": "#111111", "--brand-body-ink": "#111111"}
        with tempfile.TemporaryDirectory() as d:
            code, rep, _ = self._run(make_kit(pathlib.Path(d) / "kit", extra_tokens=tokens))
        self.assertEqual(code, 1)
        failing = {c["name"]: c for c in rep["checks"] if not c["ok"]}
        self.assertIn("contrast .section p", failing)
        self.assertLess(failing["contrast .section p"]["value"], 2)

    def test_missing_onlight_logo_fails_the_logo_check(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            man = json.loads((kit / "manifest.json").read_text())
            man["render"]["logo"].pop("onLight", None)
            (kit / "manifest.json").write_text(json.dumps(man))
            code, rep, _ = self._run(kit)
        self.assertEqual(code, 1)
        logo = next(c for c in rep["checks"] if c["name"] == "logo variants in reference strip")
        self.assertFalse(logo["ok"]); self.assertEqual(logo["value"], ["onDark"])


    def test_translucent_gradient_is_composited_not_ignored(self):
        html = ('<html><body style="background:#000"><div class="cta" style="background:linear-gradient(90deg, rgba(255,255,255,.9), rgba(255,255,255,.9));padding:20px">'
                '<h2 style="color:#fff;font-size:28px">Closing band</h2></div></body></html>')
        with tempfile.TemporaryDirectory() as d:
            page = pathlib.Path(d) / "t.html"; page.write_text(html); rep = pathlib.Path(d) / "g.json"
            subprocess.run([sys.executable, str(GATE), str(page), "--json", str(rep)], capture_output=True, text=True)
            cta = next(c for c in json.loads(rep.read_text())["checks"] if c["name"] == "contrast .cta h2")
        self.assertFalse(cta["ok"]); self.assertLess(cta["value"], 1.5)  # white text over a near-white veil, whatever lies beneath

    def test_lockup_counts_as_a_logo_variant_and_inset_stats_keep_the_gutter(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit", gallery_block={"statsStyle": "inset"})
            man = json.loads((kit / "manifest.json").read_text())
            mark = man["render"]["logo"]["onLight"]
            man["render"]["logo"] = {"lockup": {"mark": mark, "wordmark": "Acme", "wordmarkWeight": 700}}
            (kit / "manifest.json").write_text(json.dumps(man))
            code, rep, out = self._run(kit)
        by = {c["name"]: c for c in rep["checks"]}
        self.assertTrue(by["logo variants in reference strip"]["ok"], out)
        self.assertTrue(by["gutter alignment"]["ok"], out)  # the inset card is measured by its outer edge
        self.assertEqual(code, 0, out)

    def test_collateral_without_a_reference_strip_skips_the_logo_check(self):
        with tempfile.TemporaryDirectory() as d:
            kit = make_kit(pathlib.Path(d) / "kit")
            one = pathlib.Path(d) / "onepager.html"
            subprocess.run([sys.executable, str(SKILL / "scripts/render_kit.py"), "--kit-dir", str(kit), "--spec", str(SKILL / "assets/onepager_spec.json"), "--out", str(one)],
                           check=True, capture_output=True)
            rep = pathlib.Path(d) / "g.json"
            r = subprocess.run([sys.executable, str(GATE), str(one), "--json", str(rep)], capture_output=True, text=True)
            names = {c["name"] for c in json.loads(rep.read_text())["checks"]}
        self.assertNotIn("logo variants in reference strip", names)
        self.assertIn("contrast .cta h2", names)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
