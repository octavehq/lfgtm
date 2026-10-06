#!/usr/bin/env python3
"""gate_check.py — mechanical pre-gate for a rendered kit page, run before the judges.

  gate_check.py <rendered.html> [--json <report.json>]

Measures what judges would otherwise guess from pixels, in a real browser: text contrast against the
effective background (translucent layers and gradient stops composited over what lies beneath), gutter
alignment across bands, the gap between hero buttons, both logo variants in the gallery's reference strip,
empty icon tiles, and the body measure in characters per line. Every visible match of a selector is checked
and the worst one reported. Exit 0 pass, 1 fail, 2 when no browser can run (NOT RUN; never a pass).
"""
import argparse
import json
import pathlib
import sys

JS = r"""
() => {
  const q = s => document.querySelector(s);
  const qa = (s, root) => Array.from((root || document).querySelectorAll(s));
  const visible = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (el.textContent || '').trim().length > 0; };
  const parse = c => { const m = (c || '').match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  // source-over compositing that keeps alpha, so stacked translucent layers stay translucent until an opaque one
  const over = (fg, bg) => { const a = fg.a + bg.a * (1 - fg.a); if (a === 0) return { r: 0, g: 0, b: 0, a: 0 };
    const mix = k => (fg[k] * fg.a + bg[k] * bg.a * (1 - fg.a)) / a; return { r: mix('r'), g: mix('g'), b: mix('b'), a }; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const WHITE = { r: 255, g: 255, b: 255, a: 1 };
  // colour stops of the first gradient layer, with their alpha; `transparent` keywords count as see-through stops
  const stopsOf = img => { const m = (img || '').match(/gradient\([^)]*(?:\([^)]*\)[^)]*)*\)/); if (!m) return null;
    const stops = (m[0].match(/rgba?\([^)]+\)/g) || []).map(parse).filter(Boolean);
    return { stops, seeThrough: /transparent/.test(m[0]) || stops.some(s => s.a < 0.99) || stops.length === 0 }; };
  // what text sits on: walk up through translucent fills; the first gradient's stops are composited over the fill beneath them
  const bgOf = el => {
    let node = el, acc = { r: 0, g: 0, b: 0, a: 0 }, grad = null, image = false;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node); const c = parse(s.backgroundColor);
      if (!image && /gradient|url\(/.test(s.backgroundImage || '')) { image = true; grad = grad || stopsOf(s.backgroundImage); }
      if (c && c.a > 0) { acc = over(acc, c); if (acc.a >= 0.99) break; }
      node = node.parentElement;
    }
    const base = acc.a >= 0.99 ? acc : over(acc, WHITE);
    if (!grad || !grad.stops.length) return { grounds: [base], image, note: image ? 'an image layer sits above the measured base color' : undefined };
    const grounds = grad.stops.map(s => s.a >= 0.99 ? s : over(s, base));
    if (grad.seeThrough) grounds.push(base);
    return { grounds, image, note: 'measured against the gradient\'s own colour stops (worst stop)' };
  };
  const checks = [];
  const text = [['.hero h1', 3], ['.hero .lead', 4.5], ['.hero .hl', 3], ['.section p', 4.5], ['.section h2', 3], ['.stat .n', 3], ['.stat .n .u', 3],
                ['.stat .l', 4.5], ['.fcard h3', 4.5], ['.fcard p', 4.5], ['.plan-name', 4.5], ['.plan-price', 3], ['.footer .links a', 4.5],
                ['.cta h2', 3], ['.cta p', 4.5], ['.btn', 4.5], ['.quote p', 4.5], ['.quote .who', 4.5]];
  for (const [sel, want] of text) {
    let worst = null;
    for (const el of qa(sel).filter(visible)) {
      const fg = parse(getComputedStyle(el).color); if (!fg) continue;
      const bg = bgOf(el);
      const r = Math.min(...bg.grounds.map(g => ratio(fg.a < 1 ? over(fg, g) : fg, g)));
      if (!worst || r < worst.r) worst = { r, note: bg.note };
    }
    if (worst) checks.push({ name: 'contrast ' + sel, ok: worst.r >= want, value: Math.round(worst.r * 100) / 100, want: '>= ' + want, note: worst.note });
  }
  // gutters: text containers share one left edge; an inset or light stats card is measured by its outer edge
  const stats = q('.stats');
  const statsEdge = stats ? ((stats.classList.contains('inset') || stats.classList.contains('on-light')) ? stats : q('.stats .stat:first-child .n')) : null;
  // a full-bleed closing band (--brand-cta-margin with zero inline margin) has no gutter of its own: its copy is centred
  const cta = q('.cta'), sheet = cta && (cta.closest('.doc') || document.body);
  const ctaEdge = cta && Math.abs(cta.getBoundingClientRect().left - sheet.getBoundingClientRect().left) > 2 ? cta : null;
  const lefts = [q('.hero .copy'), q('.wrap > .section'), statsEdge, ctaEdge].filter(Boolean).map(el => el.getBoundingClientRect().left);
  if (lefts.length > 1) checks.push({ name: 'gutter alignment', ok: Math.max(...lefts) - Math.min(...lefts) <= 2,
                                      value: lefts.map(v => Math.round(v)), want: 'left edges within 2px' });
  const btns = qa('.hero .actions .btn');
  for (let i = 1; i < btns.length; i++) {
    const gap = btns[i].getBoundingClientRect().left - btns[i - 1].getBoundingClientRect().right;
    checks.push({ name: 'hero button gap', ok: gap >= 8, value: Math.round(gap), want: '>= 8px' });
  }
  // the gallery's reference strip shows both logo variants (an <img> or a mark + wordmark lockup); collateral has no strip
  const strip = q('[data-kit-ref]');
  if (strip) {
    const cells = qa('[data-logo-surface]', strip).filter(c => c.querySelector('img') && c.getBoundingClientRect().height > 0);
    const surfaces = new Set(cells.map(c => c.getAttribute('data-logo-surface')));
    checks.push({ name: 'logo variants in reference strip', ok: surfaces.has('onLight') && surfaces.has('onDark'), value: Array.from(surfaces), want: 'onLight and onDark' });
  }
  const empty = qa('.fcard .tile').filter(t => !t.innerHTML.trim() && t.getBoundingClientRect().height > 0).length;
  checks.push({ name: 'empty icon tiles', ok: empty === 0, value: empty, want: '0' });
  const p = q('.section p');
  if (p) {
    const s = getComputedStyle(p); const lh = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.5;
    const lines = Math.max(1, Math.round(p.getBoundingClientRect().height / lh));
    const cpl = Math.round((p.textContent || '').trim().length / lines);
    checks.push({ name: 'body measure', ok: lines === 1 || cpl <= 85, value: cpl, want: '<= 85 characters per line' });
  }
  return checks;
}
"""


def run(html_path):
    """(checks, None) for one rendered page, or (None, reason) when no browser can run."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, "Playwright is not installed (python3 -m pip install playwright && python3 -m playwright install chromium)"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 1100, "height": 900})
                page.goto(pathlib.Path(html_path).resolve().as_uri())
                page.wait_for_timeout(200)
                checks = page.evaluate(JS)
            finally:
                browser.close()
    except Exception as e:  # no Chromium, a sandbox refusal, a crashed browser: the gate did not run
        first = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
        return None, f"browser could not run: {first[:200]}"
    return checks, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("--json", type=pathlib.Path, help="also write the report here")
    args = ap.parse_args()
    checks, reason = run(args.html)
    if checks is None:
        report = {"file": str(args.html), "pass": False, "notRun": reason, "checks": []}
        if args.json:
            args.json.write_text(json.dumps(report, indent=1))
        print(f"NOT RUN: {reason}")
        sys.exit(2)
    report = {"file": str(args.html), "pass": all(c["ok"] for c in checks), "checks": checks}
    if args.json:
        args.json.write_text(json.dumps(report, indent=1))
    for c in checks:
        note = f"; {c['note']}" if c.get("note") else ""
        print(f"{'ok  ' if c['ok'] else 'FAIL'} {c['name']}: {c['value']} (want {c['want']}){note}")
    print("PASS" if report["pass"] else "FAIL")
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
