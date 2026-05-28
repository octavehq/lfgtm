# Deck HTML Scaffold

The deck uses a **fixed 16:9 stage**: every slide is authored at **1920×1080** and the whole stage is scaled as a unit with `transform: scale()` to fit the browser window (letterboxed/pillarboxed). Content never reflows per device — this guarantees "fits perfectly on every screen" instead of relying on `clamp()` math.

> Authoring rule: size everything in **px against the 1920×1080 canvas** (e.g. a 112px title, 72px padding). Do **not** use `clamp()`, `vw`, or `vh` for layout — the stage scaling handles responsiveness. Treat any `clamp()`/`vw` values from a style preset or custom design as design *proportions* to translate into fixed 1920×1080 coordinates.

The full contents of [`viewport-base.css`](viewport-base.css) are **mandatory** — paste them verbatim into the `<style>` block of every deck. They define the `.deck-viewport` → `.deck-stage` → `.slide` system, `.active`/`.visible` visibility (never `display:none`, so slide state and animations are preserved), print-one-slide-per-page, and reduced-motion.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Deck Title]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
    :root {
      ...                              /* colors/fonts/radius from style-presets.md */
      --stage-bg: #000;                /* letterbox color behind the stage */
      --slide-bg: var(--bg);           /* slide canvas background */
    }

    /* === Reset === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* === viewport-base.css (PASTE THE ENTIRE FILE HERE — mandatory) === */
    /* .deck-viewport, .deck-stage (1920×1080), .slide (.active/.visible),
       @media print one-slide-per-page, prefers-reduced-motion … */

    /* === Typography — authored at the 1920×1080 stage size (px, not clamp) === */
    .heading-1   { font-size: 96px;  line-height: 1.05; font-family: var(--font-display); }
    .heading-2   { font-size: 60px;  line-height: 1.1;  font-family: var(--font-display); }
    .heading-3   { font-size: 34px;  line-height: 1.2;  font-family: var(--font-display); }
    .body-lg     { font-size: 32px;  line-height: 1.4; }
    .body-text   { font-size: 24px;  line-height: 1.5; }
    .big-number  { font-size: 120px; line-height: 1;   font-family: var(--font-display); }

    /* === Layout — each slide centers a content well inside the 1920×1080 canvas === */
    .slide { display: flex; align-items: center; justify-content: center; }
    .slide-inner { width: 100%; max-width: 1600px; padding: 80px 140px; }
    .flex-center { align-items: center; justify-content: center; }
    .flex-col { display: flex; flex-direction: column; }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }

    /* === Components (cards, pills, metrics, etc.) — px-sized === */

    /* === Reveal animations: triggered by .visible on the active slide === */
    .animate-in {
      opacity: 0;
      transform: translateY(30px);
      transition: opacity 0.6s var(--ease), transform 0.6s var(--ease);
    }
    .slide.visible .animate-in { opacity: 1; transform: translateY(0); }
    .slide.visible .animate-in:nth-child(1) { transition-delay: 0.1s; }
    .slide.visible .animate-in:nth-child(2) { transition-delay: 0.2s; }
    .slide.visible .animate-in:nth-child(3) { transition-delay: 0.3s; }
    /* … up to 8 */
  </style>
</head>
<body>

  <div class="deck-viewport">
    <main class="deck-stage" id="deckStage">

      <!-- First slide carries `active visible` so it shows + animates on load -->
      <section class="slide slide-title active visible" data-slide="0">
        <div class="slide-inner flex-center flex-col">
          <!-- Slide content (see slide-templates.md) -->
        </div>
      </section>

      <!-- Subsequent slides: just `slide` -->
      <section class="slide" data-slide="1">
        <div class="slide-inner"> ... </div>
      </section>

      <!-- Repeat for each slide -->

    </main>
  </div>

  <!-- Presentation chrome lives OUTSIDE the stage so it isn't scaled -->
  <div class="deck-controls" id="deckControls"></div>

  <!-- Inline editing affordance (included by default — see SKILL.md Step 6) -->
  <div class="edit-hotzone"></div>
  <button class="edit-toggle" id="editToggle" title="Edit mode (E)">✏️</button>

  <script>
    /* === Slide controller: fixed-stage scaling + nav + .active/.visible === */
    class SlidePresentation {
      constructor() {
        this.slides = [...document.querySelectorAll('.slide')];
        this.stage = document.getElementById('deckStage');
        this.current = 0;
        this.setupStageScale();   // scale 1920×1080 stage to viewport, recenter on resize
        this.setupKeyboardNav();  // ArrowR/L, Space, PageUp/Down, Home/End
        this.setupTouchNav();     // swipe left/right on touch devices
        this.renderControls();    // "n / total" + prev/next, in #deckControls
        this.show(0);
      }
      setupStageScale() {
        const fit = () => {
          const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
          const x = (window.innerWidth  - 1920 * s) / 2;
          const y = (window.innerHeight - 1080 * s) / 2;
          this.stage.style.transformOrigin = '0 0';
          this.stage.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
        };
        fit();
        window.addEventListener('resize', fit);
      }
      show(i) {
        this.current = Math.max(0, Math.min(i, this.slides.length - 1));
        this.slides.forEach((sl, idx) => {
          const on = idx === this.current;
          sl.classList.toggle('active', on);
          sl.classList.toggle('visible', on);   // re-triggers .animate-in reveals
        });
        this.updateControls();
      }
      next() { this.show(this.current + 1); }
      prev() { this.show(this.current - 1); }
      // setupKeyboardNav / setupTouchNav / renderControls / updateControls …
    }
    new SlidePresentation();

    /* === Inline editing: JS-based hover (NOT CSS ~ sibling) + E key, strip on export === */
    // editToggle.classList.add('show') on hotzone mouseenter, 400ms grace on leave;
    // toggle contenteditable on slide text; persist to localStorage; export strips edit state.
  </script>

</body>
</html>
```

## Why fixed-canvas (not clamp reflow)

| Concern | How the stage model handles it |
|---------|--------------------------------|
| "Fits every screen" | One `scale()` on the whole 1920×1080 stage — no per-element math, no overflow surprises |
| Slide switching | `.active`/`.visible` classes toggle `visibility`/`opacity`/`pointer-events` — never `display:none`, so animations re-run and embedded state (videos, inputs) survives |
| Print / PDF | `@media print` in viewport-base.css lays each slide out at design size, one per page — `scripts/export-pdf.sh` and browser Save-as-PDF both produce clean one-slide-per-page output |
| Mobile | Stage letterboxes/pillarboxes; content never reflows or cramps |
| Reduced motion | `prefers-reduced-motion` block in viewport-base.css neutralizes animations |

This only applies to **decks** (slides). The document-style skills (one-pager, proposal, brief, microsite, win-loss-report, etc.) remain scrolling pages and keep their `clamp()`/reflow model — they share the *color/font* presets, not this stage model.
