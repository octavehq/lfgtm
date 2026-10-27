#!/usr/bin/env node
/*
 * Shared render gate for Octave skill HTML outputs.
 *
 * The presentation checklist asks for things that need a real browser but NOT
 * a human eye: fonts actually loaded, text contrast against its painted
 * background, text staying inside its content box, text not cut off by a
 * container that clips it, text not sliding under fixed chrome, and (on
 * scrolling pages) no sideways page scroll. Each is deterministic, and each is
 * measured after entrance animations are jumped to their end state. Running them here means screenshots get
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

// Only rgb()/rgba() and color(srgb ...) can be turned into a luminance here.
// Anything else the browser hands back (oklch(), oklab(), lab(), display-p3,
// which is how color-mix() often resolves) returns null and the element is
// skipped, so the gate never reports a ratio it guessed.
function parseColor(css) {
  const s = String(css).trim();
  let m = s.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/);
  let scale = 1;
  if (!m) {
    m = s.match(/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+%?))?\s*\)$/);
    scale = 255;
  }
  if (!m) return null;
  const alpha = m[4] === undefined ? 1
    : m[4].endsWith('%') ? parseFloat(m[4]) / 100 : Number(m[4]);
  return { r: m[1] * scale, g: m[2] * scale, b: m[3] * scale, a: alpha };
}

function luminance(css) {
  const c = parseColor(css);
  if (!c || c.a === 0) return null; // unknown format or fully transparent
  const { r, g, b } = c;
  const f = (v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}

// Entrance animations and transitions move and fade text while they play, so
// a screen measured mid-animation reports overflow, clipping or low contrast
// that the settled page does not have. Jump every finite animation to its end
// state, a few rounds in case finishing one starts the next, and leave
// infinite loops (a travelling dot, a slow spin) running.
async function settle(page) {
  await page.evaluate(async () => {
    const frame = () => new Promise((resolve) => requestAnimationFrame(() => resolve()));
    for (let round = 0; round < 4; round++) {
      await frame();
      await frame();
      const running = document.getAnimations().filter((a) => a.playState !== 'finished' &&
        a.effect && Number.isFinite(a.effect.getComputedTiming().endTime));
      if (!running.length) break;
      for (const a of running) {
        try { a.finish(); } catch { /* an animation that cannot finish is left as it is */ }
      }
    }
  });
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || undefined,
  });
  const problems = [];
  let fontReport = null;
  let contrastSkipped = 0;

  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
    page.on('pageerror', error => problems.push({ viewport: vp.name, check: 'script-error', detail: String(error) }));
    page.on('requestfailed', request => problems.push({ viewport: vp.name, check: 'asset-load', detail: request.url().split('?')[0] }));
    page.on('response', response => {
      if (response.status() >= 400) problems.push({ viewport: vp.name, check: 'asset-load', detail: `HTTP ${response.status()}: ${response.url().split('?')[0]}` });
    });
    await page.goto('file://' + path.resolve(FILE));
    await page.evaluate(() => Promise.race([
      Promise.all([document.fonts.ready, ...Array.from(document.images, image => image.decode().catch(() => null))]),
      new Promise((_, reject) => setTimeout(() => reject(new Error('Font/image readiness timed out')), 10000))
    ]));
    const brokenImages = await page.evaluate(() => [...document.images].filter(i => !i.complete || !i.naturalWidth).length);
    if (brokenImages) problems.push({ viewport: vp.name, check: 'asset-load', detail: `${brokenImages} images failed to decode` });
    await page.waitForTimeout(400);
    await settle(page);

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
    let vpSkipped = 0;
    let vpScrollX = false;

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
      await settle(page);

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

        // Painted background of the nearest non-transparent ancestor. A fill
        // the gate cannot compute (color-mix() resolving to oklab, oklch,
        // display-p3, or a background image or gradient) returns null, so the
        // element is skipped until an opaque fill it can read sits closer.
        const readable = /^(rgba?\(|color\(srgb\s)/;
        // Alpha is the fourth component only. Opaque fills come back as
        // rgb(r, g, b) with no alpha, so the last number is the blue channel.
        const alphaOf = (bg) => {
          const body = bg.slice(bg.indexOf('(') + 1, bg.lastIndexOf(')'));
          const parts = body.replace(/^srgb\s+/, '').split(/[\s,/]+/).filter(Boolean);
          if (parts.length < 4) return 1;
          const a = parts[3];
          return a.endsWith('%') ? parseFloat(a) / 100 : Number(a);
        };
        const paintedBg = (el) => {
          let e = el;
          while (e && e !== document.documentElement) {
            const st = getComputedStyle(e);
            if (st.backgroundImage && st.backgroundImage !== 'none') return null;
            const bg = st.backgroundColor;
            if (!readable.test(bg)) return null;
            if (alphaOf(bg) > 0.55) return bg;
            e = e.parentElement;
          }
          const bodyBg = getComputedStyle(document.body).backgroundColor;
          return readable.test(bodyBg) ? bodyBg : null;
        };

        // Text cut off by a container that clips it (fixed height plus
        // overflow hidden, line clamps, ellipsis). Rectangle-based: the text's
        // own rect against the clipping box. Returns the cut in px, or -1 when
        // the text is hidden on purpose (a clipping container under 4px, such
        // as a collapsed disclosure, or text slid fully out of view, such as a
        // carousel slide); hidden text is skipped by every check. Scroll
        // containers are meant to scroll and do not count as clipping.
        const clipsText = (st) => /hidden|clip/.test(st.overflowX + ' ' + st.overflowY);
        const clippedBy = (el, fontSize) => {
          const range = document.createRange();
          range.selectNodeContents(el);
          const t = range.getBoundingClientRect();
          if (!t.width || !t.height) return 0;
          const slackY = Math.max(2, fontSize * 0.3);
          const slackX = Math.max(2, fontSize * 0.15);
          for (let a = el; a && a !== pane && a !== document.body; a = a.parentElement) {
            const st = getComputedStyle(a);
            if (!clipsText(st)) continue;
            const ar = a.getBoundingClientRect();
            if (ar.width < 4 || ar.height < 4) return -1;
            const overlaps = t.left < ar.right && t.right > ar.left && t.top < ar.bottom && t.bottom > ar.top;
            if (!overlaps) return -1;
            const by = Math.max(t.bottom - ar.bottom - slackY, ar.top - t.top - slackY,
                                t.right - ar.right - slackX, ar.left - t.left - slackX);
            if (by > 0) return Math.round(by);
          }
          return 0;
        };
        // Content inside a horizontal scroller is meant to extend past the edge.
        const inScrollerX = (el) => {
          for (let a = el.parentElement; a && a !== pane && a !== document.body; a = a.parentElement) {
            if (/auto|scroll/.test(getComputedStyle(a).overflowX)) return true;
          }
          return false;
        };

        // Sideways page scroll is measured whenever the document itself can
        // scroll sideways: a scrolling page with or without panes (story
        // screens are panes on a vertical page). A horizontal track that
        // clips the document (a swipe magazine) is left alone.
        const docOverflowX = getComputedStyle(document.documentElement).overflowX + ' ' +
                             getComputedStyle(document.body).overflowX;
        const out = { label: pane.getAttribute('aria-label') || pane.id || `pane ${idx + 1}`,
                      spillBelow: [], spillRight: [], underChrome: [], lowContrast: [],
                      clipped: [], contrastSkipped: 0,
                      pageScrollX: /hidden|clip/.test(docOverflowX) ? 0
                        : Math.max(0, document.scrollingElement.scrollWidth - window.innerWidth) };

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
          const cut = clippedBy(el, parseFloat(s.fontSize) || 16);
          if (cut < 0) continue;
          if (cut) out.clipped.push({ ...tag, by: cut });

          if (b.bottom > contentBottom + 1.5) {
            out.spillBelow.push({ ...tag, by: Math.round(b.bottom - contentBottom) });
          }
          if (b.right > contentRight + 1.5 && !el.closest('[data-full-bleed]') && !inScrollerX(el)) {
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
          if (bg === null || !readable.test(fg)) { out.contrastSkipped++; continue; }
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
      push('clipped-text', report.clipped);
      if (report.pageScrollX > 1 && !vpScrollX) {
        vpScrollX = true;
        problems.push({ viewport: vp.name, check: 'page-scroll-x',
          detail: `The page scrolls sideways by ${Math.round(report.pageScrollX)}px at this width.` });
      }
      vpSkipped += report.contrastSkipped;

      if (SHOTS) {
        await page.screenshot({
          path: `${SHOTS}/${vp.name}-${String(i + 1).padStart(2, '0')}.png`,
        });
      }
    }
    contrastSkipped = Math.max(contrastSkipped, vpSkipped);
    await page.close();
  }

  await browser.close();

  if (AS_JSON) {
    console.log(JSON.stringify({ file: FILE, fonts: fontReport, contrastSkipped, problems }, null, 2));
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
    if (contrastSkipped) {
      console.log(`Contrast: ${contrastSkipped} text elements skipped on fills the gate cannot ` +
                  'compute (color-mix, oklch, gradients, images); check those by eye.');
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
