#!/usr/bin/env node
/*
 * Shared render gate for Octave skill HTML outputs.
 *
 * The presentation checklist asks for four things that need a real browser but
 * NOT a human eye: fonts actually loaded, text contrast against its painted
 * background, text staying inside its content box, and text not sliding under
 * fixed chrome. Each is deterministic. Running them here means screenshots get
 * spent on taste (is the hierarchy right, does the rail feel airy) instead of
 * on defect discovery.
 *
 * Usage:
 *   node render-gate.js <file.html> [--panes ".spread"] [--chrome "#nav,.footer"]
 *                       [--viewports 1600x900,2560x1080] [--shots <dir>] [--json]
 *
 * Exit code is non-zero when any check fails.
 *
 * Requires playwright. If it is not installed, the gate says so and exits 2 so
 * a caller can tell "not run" apart from "ran and passed".
 *
 * ---------------------------------------------------------------------------
 * THE TRAP THIS SCRIPT EXISTS TO AVOID
 *
 * The obvious overflow check is `el.scrollHeight - el.clientHeight`. On any
 * container with `overflow:hidden` -- which every fixed-viewport pane has --
 * that returns 0 while content is visibly cut off. A gate built on it reports a
 * confident PASS over broken output. Every check below is rectangle-based
 * instead: measure where text actually landed and compare it to where it was
 * allowed to land.
 * ---------------------------------------------------------------------------
 */

const path = require('path');

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.error('render-gate: playwright not installed. Install it, or skip this gate and');
  console.error('say in the scorecard that the render checks did not run.');
  process.exit(2);
}

// --- args ---------------------------------------------------------------
const argv = process.argv.slice(2);
const FILE = argv.find((a) => !a.startsWith('--'));
const flag = (name, dflt) => {
  const i = argv.indexOf(`--${name}`);
  return i !== -1 && argv[i + 1] ? argv[i + 1] : dflt;
};
const has = (name) => argv.includes(`--${name}`);

if (!FILE) {
  console.error('Usage: node render-gate.js <file.html> [--panes SEL] [--chrome SEL] ' +
                '[--viewports WxH,...] [--shots DIR] [--json]');
  process.exit(1);
}

// A "pane" is a fixed-viewport surface: a magazine spread, a slide, a hero.
// Scrolling documents have none; the whole body is then a single pane.
const PANES = flag('panes', '.spread,.slide,section[data-pane]');
const CHROME = flag('chrome', '#nav,nav.fixed,.deck-nav,.pager,[data-chrome]');
const SHOTS = flag('shots', null);
const AS_JSON = has('json');
const VIEWPORTS = flag('viewports', '1600x900,1680x1050,2560x1080,1180x820')
  .split(',')
  .map((s) => {
    const [w, h] = s.trim().split('x').map(Number);
    return { name: s.trim(), width: w, height: h };
  });

// Minimum contrast for body text against its painted background. Deliberately
// well below WCAG AA: this gate catches invisible text (ratio near 1), not
// borderline aesthetic choices, which are the reviewer's judgment call.
const MIN_CONTRAST = 2.4;

function luminance(css) {
  const m = String(css).match(/[\d.]+/g);
  if (!m) return null;
  if (m.length > 3 && Number(m[3]) === 0) return null; // fully transparent
  const [r, g, b] = m.slice(0, 3).map(Number);
  const f = (v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || undefined,
  });
  const problems = [];
  let fontReport = null;

  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
    await page.goto('file://' + path.resolve(FILE));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);

    // --- 1. fonts actually loaded ---------------------------------------
    if (!fontReport) {
      fontReport = await page.evaluate(() => {
        const faces = [...document.fonts].map((f) => ({
          family: f.family, weight: f.weight, style: f.style, status: f.status,
        }));
        const sample = document.querySelector('h1,h2,h3') || document.body;
        const body = document.querySelector('p') || document.body;
        const resolved = (el) => getComputedStyle(el).fontFamily;
        const firstFamily = (ff) => (ff || '').split(',')[0].replace(/["']/g, '').trim();
        return {
          declaredFaces: faces,
          headingFamily: firstFamily(resolved(sample)),
          bodyFamily: firstFamily(resolved(body)),
          // A face named in font-family but never delivered falls back silently.
          headingLoaded: document.fonts.check(
            `${getComputedStyle(sample).fontWeight} 40px "${firstFamily(resolved(sample))}"`),
          bodyLoaded: document.fonts.check(`400 16px "${firstFamily(resolved(body))}"`),
        };
      });
      const unloadedDeclared = fontReport.declaredFaces.filter((f) => f.status === 'error');
      if (unloadedDeclared.length) {
        problems.push({ viewport: vp.name, check: 'font-load',
          detail: `@font-face failed to load: ${unloadedDeclared.map((f) => f.family).join(', ')}` });
      }
      if (fontReport.declaredFaces.length && !fontReport.headingLoaded) {
        problems.push({ viewport: vp.name, check: 'font-load',
          detail: `Heading resolves to "${fontReport.headingFamily}" but that face is not loaded; ` +
                  'it is painting as a system fallback.' });
      }
    }

    const paneCount = await page.evaluate((sel) => document.querySelectorAll(sel).length, PANES);
    const n = paneCount || 1;

    for (let i = 0; i < n; i++) {
      // Bring pane i into view. Horizontal decks scroll a container; vertical
      // documents scroll the window. Handle both without assuming either.
      await page.evaluate(({ sel, idx }) => {
        const panes = document.querySelectorAll(sel);
        if (!panes.length) return;
        const pane = panes[idx];
        const scroller = pane.parentElement;
        if (scroller && scroller.scrollWidth > scroller.clientWidth + 8) {
          scroller.style.scrollBehavior = 'auto';
          scroller.scrollLeft = idx * scroller.clientWidth;
        } else {
          pane.scrollIntoView({ behavior: 'instant', block: 'start' });
        }
      }, { sel: PANES, idx: i });
      await page.waitForTimeout(180);

      const report = await page.evaluate(({ sel, chromeSel, idx, minContrast }) => {
        const panes = document.querySelectorAll(sel);
        const pane = panes.length ? panes[idx] : document.body;
        const pr = pane.getBoundingClientRect();

        // The content box: the pane's own padding when it has any, else the
        // padded wrapper inside it (a common pattern for full-bleed panes).
        const padHost = parseFloat(getComputedStyle(pane).paddingBottom) > 0
          ? pane
          : (pane.querySelector('[class*="pad"]') || pane);
        const cs = getComputedStyle(padHost);
        const padB = parseFloat(cs.paddingBottom) || 0;
        const padR = parseFloat(cs.paddingRight) || 0;
        const contentBottom = pr.bottom - padB;
        const contentRight = pr.right - padR;

        // Chrome is deliberately positioned outside the content flow: page
        // folios, pagers, fixed nav. It is exempt from the content-box checks
        // but still a collision target, since content must not slide under it.
        const chromeEls = [...document.querySelectorAll(chromeSel)].filter((el) => {
          const s = getComputedStyle(el);
          return (s.position === 'fixed' || s.position === 'absolute') &&
                 s.display !== 'none' && parseFloat(s.opacity) > 0;
        });
        const chromeRects = chromeEls.map((el) => ({ el, r: el.getBoundingClientRect() }));
        const isChrome = (el) => chromeEls.some((ce) => ce === el || ce.contains(el));

        // Painted background of the nearest non-transparent ancestor.
        const paintedBg = (el) => {
          let e = el;
          while (e && e !== document.documentElement) {
            const bg = getComputedStyle(e).backgroundColor;
            const m = bg.match(/[\d.]+/g);
            if (m && (m.length < 4 || Number(m[3]) > 0.55)) return bg;
            e = e.parentElement;
          }
          return getComputedStyle(document.body).backgroundColor;
        };

        const out = { label: pane.getAttribute('aria-label') || pane.id || `pane ${idx + 1}`,
                      spillBelow: [], spillRight: [], underChrome: [], lowContrast: [] };

        const isTextLeaf = (el) => {
          if (!el.innerText || !el.innerText.trim()) return false;
          // Only leaf-ish nodes, so a wrapper div isn't reported alongside its child.
          return ![...el.children].some((c) => (c.innerText || '').trim().length > 0);
        };

        for (const el of pane.querySelectorAll('*')) {
          if (!isTextLeaf(el)) continue;
          const s = getComputedStyle(el);
          if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) continue;
          const b = el.getBoundingClientRect();
          if (!b.width || !b.height) continue;
          if (isChrome(el)) continue;

          const txt = el.innerText.trim().slice(0, 56);
          const tag = { tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 30), txt };

          if (b.bottom > contentBottom + 1.5) {
            out.spillBelow.push({ ...tag, by: Math.round(b.bottom - contentBottom) });
          }
          if (b.right > contentRight + 1.5 && !el.closest('[data-full-bleed]')) {
            out.spillRight.push({ ...tag, by: Math.round(b.right - contentRight) });
          }
          for (const { r } of chromeRects) {
            if (b.left < r.right && b.right > r.left && b.top < r.bottom && b.bottom > r.top) {
              out.underChrome.push(tag);
              break;
            }
          }

          const fg = s.color;
          const bg = paintedBg(el);
          out.lowContrast.push({ ...tag, fg, bg });
        }
        out._minContrast = minContrast;
        return out;
      }, { sel: PANES, chromeSel: CHROME, idx: i, minContrast: MIN_CONTRAST });

      const badContrast = [];
      for (const el of report.lowContrast) {
        const lf = luminance(el.fg);
        const lb = luminance(el.bg);
        if (lf === null || lb === null) continue;
        const ratio = (Math.max(lf, lb) + 0.05) / (Math.min(lf, lb) + 0.05);
        if (ratio < MIN_CONTRAST) {
          badContrast.push({ ...el, ratio: Number(ratio.toFixed(2)) });
        }
      }

      const push = (check, items) => {
        if (items.length) {
          problems.push({ viewport: vp.name, pane: i + 1, label: report.label, check,
                          items: items.slice(0, 4), total: items.length });
        }
      };
      push('spill-below', report.spillBelow);
      push('spill-right', report.spillRight);
      push('under-fixed-chrome', report.underChrome);
      push('low-contrast', badContrast);

      if (SHOTS) {
        await page.screenshot({
          path: `${SHOTS}/${vp.name}-${String(i + 1).padStart(2, '0')}.png`,
        });
      }
    }
    await page.close();
  }

  await browser.close();

  if (AS_JSON) {
    console.log(JSON.stringify({ file: FILE, fonts: fontReport, problems }, null, 2));
  } else {
    console.log('RENDER GATE');
    console.log('===========');
    console.log(`File: ${FILE}`);
    if (fontReport) {
      console.log(`Fonts: heading "${fontReport.headingFamily}" ` +
                  `(${fontReport.headingLoaded ? 'loaded' : 'NOT LOADED'}), ` +
                  `body "${fontReport.bodyFamily}" ` +
                  `(${fontReport.bodyLoaded ? 'loaded' : 'NOT LOADED'}), ` +
                  `${fontReport.declaredFaces.length} @font-face declared`);
    }
    console.log('');
    if (!problems.length) {
      console.log('─────────────────');
      console.log('PASS: text is inside its content box, clear of fixed chrome, and legible');
      console.log('      on its painted background at every viewport tested.');
    } else {
      for (const p of problems) {
        const where = p.pane ? `pane ${p.pane} (${p.label})` : '';
        console.log(`FAIL [${p.viewport}] ${p.check} ${where}`);
        if (p.detail) console.log(`   ${p.detail}`);
        for (const it of p.items || []) {
          const by = it.by !== undefined ? ` by ${it.by}px` : '';
          const ratio = it.ratio !== undefined ? ` contrast ${it.ratio}:1 (${it.fg} on ${it.bg})` : '';
          console.log(`   <${it.tag}${it.cls ? ` class="${it.cls}"` : ''}>${by}${ratio}`);
          console.log(`      "${it.txt}"`);
        }
        if (p.total > (p.items || []).length) {
          console.log(`   ... and ${p.total - p.items.length} more`);
        }
        console.log('');
      }
      console.log('─────────────────');
      console.log(`TOTAL FAILURES: ${problems.length}`);
      console.log('Fix these before spending a screenshot review on taste.');
    }
  }

  process.exit(problems.length ? 1 : 0);
})().catch((err) => {
  console.error('render-gate: ' + err.message);
  process.exit(2);
});
