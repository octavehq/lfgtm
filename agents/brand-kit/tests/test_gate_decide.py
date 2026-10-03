"""gate_decide.py: the gate's thresholds live in one script and the decision comes from the files."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import gate_decide  # noqa: E402


def card(artifact, total, dims=None, hard="no", looks="yes", fixes=()):
    dims = dims or [4] * 8
    rows = "\n".join(f"| {i + 1} | {name} | {dims[i]} | seen |" for i, name in enumerate(gate_decide.DIMS))
    fx = "\n".join(fixes) if fixes else "none"
    return (f"BRAND KIT SCORECARD — acme.com — {artifact}\n| # | Dimension | Score | Evidence |\n|---|---|---|---|\n{rows}\n"
            f"frames_read: top, s1\ntotal: {total}/40\nhard_fail: {hard}\nlooks_good: {looks}\nreasons: fine\nfixes: {fx}\n")


GATE_OK = {"pass": True, "checks": []}


class GateDecide(unittest.TestCase):
    def test_pass_when_everything_clears(self):
        out = gate_decide.decide([gate_decide.parse_scorecard(card("gallery", 36)), gate_decide.parse_scorecard(card("one-pager", 34))],
                                 [{"file": "g", "pass": True}, {"file": "o", "pass": True}], 1)
        self.assertEqual(out["next"], "pass"); self.assertEqual(out["gallery"], 36); self.assertEqual(out["onepager"], 34)

    def test_borderline_single_judge_asks_for_a_tiebreak_then_averages(self):
        g1 = gate_decide.parse_scorecard(card("gallery", 34)); one = gate_decide.parse_scorecard(card("one-pager", 33))
        gates = [{"file": "g", "pass": True}, {"file": "o", "pass": True}]
        first = gate_decide.decide([g1, one], gates, 1)
        self.assertTrue(first["borderline"]); self.assertEqual(first["next"], "tiebreak")
        g2 = gate_decide.parse_scorecard(card("gallery", 33))
        second = gate_decide.decide([g1, g2, one], gates, 1)
        self.assertEqual(second["gallery"], 33.5); self.assertFalse(second["borderline"]); self.assertEqual(second["next"], "repair")

    def test_floor_hard_fail_and_pre_gate_block_a_pass(self):
        dims = [4, 4, 4, 2, 4, 4, 4, 4]
        low = gate_decide.decide([gate_decide.parse_scorecard(card("gallery", 37, dims))], [{"file": "g", "pass": True}], 2)
        self.assertEqual(low["next"], "repair"); self.assertEqual(low["failingDimensions"], ["Contrast/legibility"])
        hard = gate_decide.decide([gate_decide.parse_scorecard(card("gallery", 37, hard="yes"))], [{"file": "g", "pass": True}], 2)
        self.assertEqual(hard["next"], "repair"); self.assertIn("hard fail (logo)", hard["blocking"])
        gate = gate_decide.decide([gate_decide.parse_scorecard(card("gallery", 37))], [{"file": "g", "pass": False, "notRun": "no browser"}], 2)
        self.assertEqual(gate["next"], "repair"); self.assertFalse(gate["preGatePass"])

    def test_round_three_failure_stops_and_renderer_fixes_are_collected(self):
        fixes = ("Spacing: renderer: the stats band ignores the gutter (kit_base.css)", "Typography: --brand-weight-h1 400")
        out = gate_decide.decide([gate_decide.parse_scorecard(card("gallery", 31, fixes=fixes)), gate_decide.parse_scorecard(card("one-pager", 30, looks="no"))],
                                 [{"file": "g", "pass": True}, {"file": "o", "pass": True}], 3)
        self.assertEqual(out["next"], "stop"); self.assertEqual(len(out["rendererFixes"]), 1); self.assertEqual(out["looksGood"], "yes")  # the one-pager's no does not fail the gallery

    def test_cli_exit_codes_follow_the_decision(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            (d / "judge-v1-r1-gallery.md").write_text(card("gallery", 36)); (d / "judge-v1-r1-onepager.md").write_text(card("one-pager", 35))
            (d / "gate.json").write_text(json.dumps(GATE_OK)); (d / "gate-onepager.json").write_text(json.dumps(GATE_OK))
            r = subprocess.run([sys.executable, str(SKILL / "scripts/gate_decide.py"), "--round", "1", "--scorecards", str(d / "judge-v1-r1-gallery.md"), str(d / "judge-v1-r1-onepager.md"),
                                "--gates", str(d / "gate.json"), str(d / "gate-onepager.json"), "--json", str(d / "decision.json")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout); self.assertEqual(json.loads((d / "decision.json").read_text())["next"], "pass")
            (d / "judge-v1-r1-gallery.md").write_text(card("gallery", 34))
            r = subprocess.run([sys.executable, str(SKILL / "scripts/gate_decide.py"), "--round", "1", "--scorecards", str(d / "judge-v1-r1-gallery.md"),
                                "--gates", str(d / "gate.json"), str(d / "gate-onepager.json")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 3)  # tiebreak


    def test_feedback_file_collects_renderer_fixes_once(self):
        with tempfile.TemporaryDirectory() as d:
            fb = pathlib.Path(d) / "reports" / "renderer-feedback.md"
            added = gate_decide.merge_feedback(fb, ["Spacing: renderer: stats band ignores the gutter (kit_base.css)", "Depth: renderer: footer corners (kit_base.css)"])
            again = gate_decide.merge_feedback(fb, ["spacing: RENDERER: stats band ignores the gutter (kit_base.css)", "Edges: renderer: pricing card radius"])
            lines = fb.read_text().strip().splitlines()
        self.assertEqual(len(added), 2); self.assertEqual(again, ["Edges: renderer: pricing card radius"])
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
