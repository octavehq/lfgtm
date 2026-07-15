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

    /* === Components — reusable building blocks for slide content ===
     *
     * Component          | Purpose                                | Use on
     * -------------------|----------------------------------------|---------------------------
     * .card              | Multi-element content container         | Grid/card slides, overviews
     * .card-brand        | Highlighted card variant                | Comparison slides (winner)
     * .card-accent-left  | Card with left border accent            | Ranked/categorized items
     * .metric-card       | Single stat + label                     | Metric slides (2-4 numbers)
     * .pill              | Orienting tag / category label          | Title slide only
     * .feature-list/item | Vertical bullet stack with border       | Content slides (3-5 points)
     * .bullet-list/item  | Colored-dot bullet stack                | Deep-dive slides (scannable)
     * .entity-name       | Large focal heading for entities        | Deep-dive slides
     * .entity-subtitle   | Colored subtitle below entity name      | Deep-dive slides
     * .deck-nav          | Persistent top bar (all sections)       | Multi-section decks
     * .section-nav/num/label | Section number + label              | Every slide in a section
     * .section-bar       | Thin left-edge color stripe             | Every slide in a section
     * .slide-body        | Consistent content container            | Deep-dive, overview, content
     * .glow-orb          | Gradient blur for emphasis slides       | Title, divider, CTA slides
     * .brand-line        | Accent divider line                     | Between content blocks
     * .quote-mark        | Large decorative open-quote             | Quote slides
     * .big-number        | Oversized stat number                   | Inside .metric-card
     *
     * === */

    /* Cards — primary content container for multi-element content blocks.
       Use when: grouping related text (heading + body + details) into a
       distinct visual container. Must lift off the slide background with
       box-shadow — a card without depth doesn't register as a container.
       Variants: .card-brand (stronger shadow, highlighted option),
       .card-accent-left (left border accent for ranked/categorized items). */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 48px;
      box-shadow: 0 4px 20px var(--shadow-brand), 0 1px 4px rgba(0,0,0,0.08);
    }
    .card-brand {
      border-color: var(--border-strong);
      box-shadow: 0 4px 24px var(--shadow-brand-md), 0 1px 4px rgba(0,0,0,0.08);
    }
    .card-accent-left {
      border-left: 3px solid var(--brand-500);
      border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
    }

    /* Pills / Badges — structural labels for categories or section markers.
       Use when: title slide needs an orienting tag the audience doesn't
       already know (product name, audience). Do NOT use on content slides
       as labels above headlines — the headline should carry the message. */
    .pill {
      display: inline-block;
      padding: 10px 28px;
      border-radius: var(--radius-pill);
      font-size: 16px;
      letter-spacing: 2px;
      text-transform: uppercase;
      font-weight: 500;
      color: var(--brand-500);
      background: var(--shadow-brand-md);
      border: 1px solid var(--border);
    }

    /* Metric card — single stat + label with accent bar on top.
       Use when: a slide presents 2-4 key numbers as the visual anchor.
       Each metric card holds one .big-number and one .body-text label.
       Place in a .grid-2 or .grid-3. */
    .metric-card {
      position: relative;
      overflow: hidden;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 48px 40px;
      text-align: center;
      box-shadow: 0 4px 20px var(--shadow-brand);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }
    .metric-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--brand-primary), var(--brand-500));
    }

    /* Brand line — decorative accent divider */
    .brand-line {
      width: 80px; height: 3px;
      background: linear-gradient(90deg, var(--brand-primary), var(--brand-500));
      border-radius: 2px;
    }

    /* Quote mark — large decorative open-quote for quote slides */
    .quote-mark {
      font-size: 140px; line-height: 0.5;
      font-family: Georgia, serif;
      color: var(--brand-500); opacity: 0.25;
    }

    /* Feature list — vertical stack with left accent border.
       Use when: a content slide lists 3-5 key points with optional
       subtext. Each .feature-item gets the left border accent.
       For deep-dive slides, prefer .bullet-list instead. */
    .feature-list { display: flex; flex-direction: column; gap: 28px; }
    .feature-item {
      padding-left: 24px;
      border-left: 3px solid var(--border-strong);
    }

    /* Emphasis slide glow — radial gradient orb for title/divider/CTA slides.
       Use when: title, section divider, or CTA/closing slides need a
       visually distinct surface from content slides. Position with inline
       styles (top/right/bottom/left). Use 1-2 orbs max per slide. */
    .glow-orb {
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
      filter: blur(120px);
      opacity: 0.4;
      background: var(--brand-primary);
    }

    /* Text color utilities */
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); }
    .text-brand { color: var(--brand-500); }

    /* === Navigation Components === */

    /* Deck-level top nav — persistent bar showing all major sections.
       Use when: deck has 2+ major sections. Place at absolute top of every
       slide except title/closing. Highlights the current section. */
    .deck-nav {
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 52px;
      display: flex;
      align-items: center;
      padding: 0 120px;
      gap: 48px;
      border-bottom: 1px solid var(--border);
      font-size: 20px;
      letter-spacing: 5px;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-muted);
    }
    .deck-nav .active { color: var(--text-primary); }

    /* Section nav — section number + label, positioned below deck nav.
       Use when: slides belong to a numbered or color-coded section.
       Place at the same absolute position on every slide in that section. */
    .section-nav {
      position: absolute;
      left: 120px;
      top: 76px;        /* below .deck-nav (52px + 24px gap) */
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .section-num {
      font-size: 52px;
      font-weight: 200;
      line-height: 1;
    }
    .section-label {
      font-size: 20px;
      letter-spacing: 5px;
      text-transform: uppercase;
      font-weight: 600;
    }

    /* Section identity bar — thin vertical color stripe on the left edge.
       Use when: slides belong to a color-coded section. Reinforces section
       identity without competing with content. */
    .section-bar {
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 6px;
    }

    /* === Slide Body Container === */

    /* Slide body — absolute-positioned content area below nav elements.
       Use when: slides need consistent vertical alignment across a section
       (deep dives, overview cards, any slide with deck-nav + section-nav).
       All content starts at the same y-position; `justify-content:center`
       vertically centers content within the remaining space. */
    .slide-body {
      position: absolute;
      left: 120px;
      right: 120px;
      top: 172px;       /* below deck-nav (52px) + section-nav (~96px) + gap */
      bottom: 56px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 36px;
    }

    /* === Entity Components (deep-dive slides) === */

    /* Entity name — large bold focal heading for deep-dive slides.
       Use when: a slide is about a specific company, account, or product.
       The entity name IS the visual focal point; the action title becomes
       the subtitle below. */
    .entity-name {
      font-size: 96px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.05;
      font-family: var(--font-display);
    }
    .entity-subtitle {
      font-size: 32px;
      font-weight: 600;
      margin-top: 10px;
    }

    /* === Bullet List (scannable deep-dive content) === */

    /* Bullet list — vertical stack with colored dot markers.
       Use when: deep-dive slides need scannable per-entity details.
       Preferred over prose paragraphs or two-column sidebar layouts —
       bullets can be processed in 5 seconds at projection speed. */
    .bullet-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .bullet-item {
      display: flex;
      align-items: baseline;
      gap: 16px;
      font-size: 30px;
      line-height: 1.4;
    }
    .bullet-item::before {
      content: '';
      flex-shrink: 0;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--dot, var(--brand-primary));  /* override with --dot per section */
      margin-top: 0.4em;    /* align dot with first line of text */
    }

    /* === Spacing Utilities === */

    .mt-sm  { margin-top: 16px; }
    .mt-md  { margin-top: 32px; }
    .mt-lg  { margin-top: 48px; }
    .gap-sm { gap: 24px; }
    .gap-md { gap: 36px; }
    .gap-lg { gap: 48px; }

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

## Known render traps

Check for these before shipping a deck. Each has bitten a real deck.

1. **Background specificity.** `viewport-base.css` sets `.slide{background:var(--slide-bg)}` and is pasted after the preset CSS, so at equal specificity it wins over a themed slide background. Theme slide backgrounds with a higher-specificity selector (`.slide.gradient`, `.slide.dark`), or gradient/dark bands silently render as flat `--slide-bg`.
2. **Equal-height card rows.** In a `.grid-2`/`.grid-3` card row, the tallest card sets the row height, and shorter siblings get a dead band of bottom padding. Balance the copy across cards to similar length, or vertically center the card content instead of top-aligning it.
3. **Stat numbers with arrows or symbols.** In a `.big-number`, put spaces around arrows (`6mo -> 3wk`), set `white-space:nowrap`, and size the number for its column so it doesn't wrap or cramp. A lone symbol reads as a glyph, not a metric, so give it a worded value.
4. **Brandmark vs eyebrow.** A top-left logo collides with a top-left `.pill` or section label on content slides. Put the brandmark top-right when slide content is left-aligned.
