"""Cache pointer lifecycle: checksums, draft promotion, the fidelity-gate flip to ready, consumer resolution."""
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


cache = module("brand_cache")

TOKENS = {"--brand-bg": "#ffffff", "--brand-ink": "#111111", "--brand-primary": "#0055ff",
          "--brand-font-heading": "Georgia, serif", "--brand-font-body": "Arial, sans-serif"}
LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 30"><rect width="120" height="30" fill="#0055ff"/></svg>'


def staging_kit(root):
    root.mkdir(parents=True)
    (root / "logo.svg").write_text(LOGO)
    (root / "tokens.css").write_text(":root{}")
    (root / "brand-kit.md").write_text("# Acme\n")
    (root / "components.html").write_text("<html></html>")
    (root / "manifest.json").write_text(json.dumps({
        "schemaVersion": 1, "slug": "acme", "company": "Acme", "domain": "acme.com", "canonicalDomain": "acme.com", "workspaceOId": "ws1",
        "sourceUrls": ["https://www.acme.com/"], "capturedAt": "2026-10-02T00:00:00Z", "allowedUse": {"logos": "ok", "fonts": "none"},
        "render": {"hasDarkBand": True, "tokens": TOKENS, "logo": {"onLight": "logo.svg", "onDark": "logo.svg"}, "fonts": []},
    }))
    return root


class CacheLifecycle(unittest.TestCase):
    def test_checksums_then_promote_as_draft_then_mark_ready(self):
        with tempfile.TemporaryDirectory() as d:
            staging = staging_kit(pathlib.Path(d) / "staging")
            base = pathlib.Path(d) / "brands"
            with self.assertRaises(ValueError):  # nothing catalogued yet
                cache.promote(staging, base, "acme.com", "ws1")
            sums = cache.write_checksums(staging)
            self.assertEqual(set(sums), {"logo.svg", "tokens.css", "brand-kit.md", "components.html"})
            target = cache.promote(staging, base, "acme.com", "ws1")
            self.assertEqual(target, (base / "ws1" / "acme.com").absolute())
            pointer = json.loads((target / "current.json").read_text())
            self.assertEqual(pointer["status"], "draft")
            self.assertTrue(pointer["capture"].startswith("versions/"))
            # consumers refuse a draft; capture tooling may open it
            with self.assertRaises(ValueError) as ctx:
                cache.resolve(target)
            self.assertIn("draft", str(ctx.exception))
            root, man = cache.resolve(target, allow_draft=True)
            self.assertEqual(man["company"], "Acme")
            self.assertEqual(cache.status(target)["status"], "draft")
            # the gate passed
            cache.mark_ready(target, "36/40")
            root, man = cache.resolve(target, "acme.com", "ws1")
            self.assertTrue(root.is_dir())
            st = cache.status(target)
            self.assertEqual((st["status"], st["fidelityScore"]), ("ready", "36/40"))
            with self.assertRaises(ValueError):
                cache.mark_ready(target, "great")

    def test_edit_after_checksums_blocks_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            staging = staging_kit(pathlib.Path(d) / "staging")
            cache.write_checksums(staging)
            (staging / "tokens.css").write_text(":root{--brand-x:1}")
            with self.assertRaises(ValueError) as ctx:
                cache.promote(staging, pathlib.Path(d) / "brands", "acme.com", "ws1")
            self.assertIn("tokens.css", str(ctx.exception))
            # --write-checksums refreshes the catalogue in the same step
            target = cache.promote(staging, pathlib.Path(d) / "brands", "acme.com", "ws1", write_checksums_first=True)
            self.assertTrue((target / "current.json").is_file())

    def test_review_renders_inside_the_kit_do_not_block_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            staging = staging_kit(pathlib.Path(d) / "staging")
            (staging / ".review").mkdir()
            (staging / ".review" / "gallery.png").write_bytes(b"png")
            sums = cache.write_checksums(staging)
            self.assertNotIn(".review/gallery.png", sums)
            target = cache.promote(staging, pathlib.Path(d) / "brands", "acme.com", "ws1")
            root, _ = cache.resolve(target, allow_draft=True)
            self.assertFalse((root / ".review").exists())

    def test_legacy_pointer_without_status_counts_as_ready(self):
        with tempfile.TemporaryDirectory() as d:
            staging = staging_kit(pathlib.Path(d) / "staging")
            cache.write_checksums(staging)
            target = cache.promote(staging, pathlib.Path(d) / "brands", "acme.com", "ws1", status="ready")
            pointer = json.loads((target / "current.json").read_text())
            (target / "current.json").write_text(json.dumps({"capture": pointer["capture"]}))  # pre-status pointer
            root, man = cache.resolve(target)
            self.assertEqual(man["slug"], "acme")
            self.assertEqual(cache.status(target)["status"], "ready")

    def test_cli_keeps_the_positional_promote_form_and_adds_subcommands(self):
        with tempfile.TemporaryDirectory() as d:
            staging = staging_kit(pathlib.Path(d) / "staging")
            base = pathlib.Path(d) / "brands"
            script = str(SKILL / "scripts/brand_cache.py")
            r = subprocess.run([sys.executable, script, "checksums", str(staging)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr); self.assertIn("4 files catalogued", r.stdout)
            r = subprocess.run([sys.executable, script, str(staging), "--base", str(base), "--domain", "acme.com", "--workspace", "ws1"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr); self.assertIn("status: draft", r.stdout)
            target = str(base / "ws1" / "acme.com")
            r = subprocess.run([sys.executable, script, "status", target], capture_output=True, text=True)
            self.assertEqual(json.loads(r.stdout)["status"], "draft")
            r = subprocess.run([sys.executable, script, "mark-ready", target, "--score", "35/40"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr); self.assertEqual(json.loads(r.stdout)["status"], "ready")


class VerifyLogosCli(unittest.TestCase):
    def test_out_extension_is_checked_and_html_swatch_is_written(self):
        with tempfile.TemporaryDirectory() as d:
            kit = staging_kit(pathlib.Path(d) / "kit")
            script = str(SKILL / "scripts/verify_logos.py")
            r = subprocess.run([sys.executable, script, str(kit), "--out", str(kit / "x.txt")], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0); self.assertIn(".html or .png", r.stderr)
            r = subprocess.run([sys.executable, script, str(kit), "--out", str(kit / "check.html")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("<title>Logo check: Acme</title>", (kit / "check.html").read_text())
            r = subprocess.run([sys.executable, script, "not-a-dir-slug"], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0); self.assertIn("not a directory", r.stderr)

    @unittest.skipUnless(importlib.util.find_spec("playwright"), "playwright not installed")
    def test_png_out_renders_the_swatch(self):
        with tempfile.TemporaryDirectory() as d:
            kit = staging_kit(pathlib.Path(d) / "kit")
            r = subprocess.run([sys.executable, str(SKILL / "scripts/verify_logos.py"), str(kit), "--out", str(kit / "check.png")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((kit / "check.png").is_file() and (kit / "check.html").is_file())


class Canonical(unittest.TestCase):
    def test_www_and_case_collapse_to_one_domain(self):
        self.assertEqual(cache.canonical_domain("https://WWW.Acme.com/pricing"), "acme.com")
        self.assertEqual(cache.canonical_domain("acme.com"), "acme.com")
        self.assertEqual(cache.canonical_domain("www.acme.co.uk"), "acme.co.uk")

    def test_cli_prints_the_domain_and_the_cache_root(self):
        r = subprocess.run([sys.executable, str(SKILL / "scripts/brand_cache.py"), "canonical", "https://www.acme.com/", "--workspace", "wa_1", "--base", "/tmp/brands"],
                           capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(r.stdout), {"domain": "acme.com", "cacheRoot": "/tmp/brands/wa_1/acme.com"})


class Scores(unittest.TestCase):
    def test_gate_means_are_valid_scores(self):
        for s in ("34/40", "34.5/40", "40/40", "33.25/40"):
            self.assertEqual(cache.validate_score(s), s)
        for s in ("41/40", "34", "34.5", "thirty/40", ""):
            with self.assertRaises(ValueError, msg=s):
                cache.validate_score(s)


class StalePointer(unittest.TestCase):
    """A pointer whose capture folder was deleted is an empty cache, never a kit."""

    def _stale_root(self, d):
        root = pathlib.Path(d) / "wa_1" / "acme.com"; (root / "versions").mkdir(parents=True)
        (root / "current.json").write_text(json.dumps({"capture": "versions/" + "0" * 32, "status": "draft", "promotedAt": "2026-10-02T00:00:00Z"}))
        return root

    def test_status_reports_missing_and_names_the_stale_capture(self):
        with tempfile.TemporaryDirectory() as d:
            got = cache.status(self._stale_root(d))
        self.assertEqual(got["status"], "missing"); self.assertIsNone(got["capture"]); self.assertEqual(got["stale"], "versions/" + "0" * 32)

    def test_resolve_and_mark_ready_refuse_a_stale_pointer(self):
        with tempfile.TemporaryDirectory() as d:
            root = self._stale_root(d)
            with self.assertRaises(ValueError) as e:
                cache.resolve(root, allow_draft=True)
            self.assertIn("stale capture pointer", str(e.exception))
            with self.assertRaises(ValueError):
                cache.mark_ready(root, "35/40")


if __name__ == "__main__":
    unittest.main()
