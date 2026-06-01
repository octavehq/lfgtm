#!/usr/bin/env python3
"""Render an HTML file (or URL) to a full-page PNG with headless Chromium.

Used by the fidelity gate (Step 7.5) to screenshot generated output / the kit
gallery so it can be compared against the source. Also reusable by any skill
that needs to eyeball-verify HTML it produced.

Usage:
  python3 render.py --file /path/to/output.html --out /tmp/shot.png
  python3 render.py --url https://example.com --out /tmp/src.png --width 1280
  python3 render.py --file a.html --out a.png --clip 0,0,0,0.12   # top 12% only

Requires: playwright + chromium  (pip install playwright && playwright install chromium)
Exits non-zero with a clear message if Playwright isn't available.
"""
import argparse, pathlib, sys


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="local HTML file path")
    src.add_argument("--url", help="http(s) URL")
    ap.add_argument("--out", required=True, help="output PNG path")
    ap.add_argument("--width", type=int, default=900, help="viewport width px")
    ap.add_argument("--height", type=int, default=1200, help="viewport height px")
    ap.add_argument("--scale", type=float, default=2.0, help="device scale factor")
    ap.add_argument("--wait", type=int, default=1500, help="ms to wait for fonts/render")
    ap.add_argument("--full", action="store_true", default=True, help="full-page (default)")
    ap.add_argument("--clip", help="fractional crop 'x,y,w,h' in 0..1 of full image (post-shot)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")

    target = pathlib.Path(args.file).resolve().as_uri() if args.file else args.url
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": args.width, "height": args.height},
                        device_scale_factor=args.scale)
        pg.goto(target)
        pg.wait_for_timeout(args.wait)
        pg.screenshot(path=args.out, full_page=args.full)
        b.close()

    if args.clip:
        try:
            from PIL import Image
            im = Image.open(args.out)
            W, H = im.size
            fx, fy, fw, fh = (float(v) for v in args.clip.split(","))
            box = (int(fx * W), int(fy * H), int((fx + fw) * W) if fw else W, int((fy + fh) * H) if fh else H)
            im.crop(box).save(args.out)
        except Exception as e:  # crop is best-effort
            print(f"(clip skipped: {e})", file=sys.stderr)

    print(args.out)


if __name__ == "__main__":
    main()
