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
    ap.add_argument("--full", "--full-page", dest="full", action="store_true", default=True)
    ap.add_argument("--no-full-page", dest="full", action="store_false", help="capture exactly the viewport; use --scale 1 for OG pixels")
    ap.add_argument("--clip", help="fractional crop 'x,y,w,h' in 0..1 of full image (post-shot)")
    args = ap.parse_args()
    if min(args.width, args.height, args.scale) <= 0 or args.wait < 0:
        ap.error('dimensions/scale must be positive and wait nonnegative')
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")

    target = pathlib.Path(args.file).resolve().as_uri() if args.file else args.url
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": args.width, "height": args.height},
                        device_scale_factor=args.scale)
        errors = []
        pg.on('pageerror', lambda err: errors.append(str(err)))
        pg.on('requestfailed', lambda req: errors.append('failed resource: ' + req.url.split('?')[0]))
        pg.on('response', lambda res: errors.append(f'HTTP {res.status}: {res.url.split("?")[0]}') if res.status >= 400 else None)
        pg.emulate_media(reduced_motion='reduce')
        pg.goto(target, wait_until='load', timeout=30000)
        pg.evaluate('''async () => {
          await Promise.race([
            Promise.all([document.fonts.ready, ...Array.from(document.images, img => img.decode())]),
            new Promise((_, reject) => setTimeout(() => reject(new Error('fonts/images timed out')), 10000))
          ]);
          for (const font of document.fonts) if (font.status === 'error') throw new Error('font failed');
          for (const a of document.getAnimations()) { try { a.finish(); } catch (_) { a.cancel(); } }
        }''')
        pg.wait_for_timeout(args.wait)
        if errors:
            b.close()
            sys.exit('ERROR: render failed: ' + '; '.join(errors))
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
        except Exception as e:
            sys.exit(f'ERROR: crop failed: {e}')

    print(args.out)


if __name__ == "__main__":
    main()
