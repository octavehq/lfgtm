# Visual kit: shared components for story and document outputs

A small set of brand-token-driven components that give an HTML output a signature visual instead of another run of cards and bullets. [`visual-kit.css`](visual-kit.css) holds the styles, [`visual-kit.js`](visual-kit.js) the runtime, and [`examples/`](examples/) two finished pages built from nothing else: [`acme-story.html`](examples/acme-story.html) (story mode, buyer-facing) and [`acme-report.html`](examples/acme-report.html) (document mode, internal). Every name and number in them is invented.

**Who uses it:** any skill rendering HTML. [Story mode](story-mode.md) is built on it. Document-mode outputs ([html-document.md](html-document.md)) borrow single components where one explains a mechanism or a dataset better than prose.

## Consumption contract

1. Inline the brand kit's `tokens.css` `:root` first ([brand-kit-usage.md](../brand-kit-usage.md)), then paste the full contents of `visual-kit.css` into the same `<style>` block, then the page's own rules. Outputs are single files, so nothing is linked.
2. Paste the full contents of `visual-kit.js` into a `<script>` at the end of `<body>`.
3. Load the heading face at the display weight the kit asks for. `--vk-display-weight` reads `--brand-weight-h1` and falls back to 300, so the Google Fonts link must carry that weight (`wght@300;400;500;600`). A brand whose headings are heavy keeps its weight; the size does the work.
4. Set `--vk-bar-ink` only if the brand kit's chrome colour differs from body ink.

Every `--vk-*` token resolves from the brand kit (`--brand-*`), then from a style preset (`--bg`, `--text-primary`, `--font-display`), then from a neutral default, so the same markup renders in any captured brand. Do not restyle a component with hand-picked colours; change the token.

## Floor rules the kit enforces

- **Content is in the DOM and visible with no JavaScript.** Nothing starts hidden. With the runtime, a screen gets `.is-in` as it enters the viewport and its `.vk-rise` children play once from the invisible start to the state they already had. A full-page capture taken without scrolling, a print, a reader with scripts off: all see the whole page.
- **`prefers-reduced-motion` removes all motion**, including the loader, the count-up and smooth scrolling.
- **Print flattens**: dark screens print light, chrome disappears, each screen is one page.
- **No fixed heights or `overflow: hidden` on text containers.** Screens are `min-height: 100svh` and grow when the copy needs more; the [render gate](../scripts/render-gate.js) then reports the overflow as content under the fixed chrome, which is the signal to cut copy.
- **375px works**: gutters 16px, grids stack, the key hint hides on touch and narrow screens, nothing scrolls sideways.

## Components

The test for every component: it explains the mechanism or shows the data. A component that could be deleted without the reader losing a fact is decoration and goes.

### Card-grid hero (`.vk-tiles`)

Many muted tiles and a few lit ones: "of all of these, these are the ones". Use when the opening claim is a share of a known set (deals, accounts, calls, reps). Each tile stands for one real unit and the caption names the unit and the count, so the reader can check it. Never use it as a texture.

```html
<div class="vk-tiles" style="--cols:6" role="img" aria-label="48 tiles, one per deal, 9 lit for the wins">
  <i style="--h:60px"></i><i class="is-on" style="--h:72px;--d:.5s"></i><i style="--h:54px"></i>
  <!-- one <i> per unit; --h varies the height, --d staggers the lit ones -->
</div>
<p class="vk-cap">Each tile is one of the 48 deals worked to a decision this year. The lit tiles are the nine that closed won.</p>
```

### Big stat (`.vk-stat`)

One number carries the screen. The label says what it counts and the basis says where it comes from (period, denominator, source). `data-vk-count` makes the runtime count up to the value already in the DOM and restore the exact original text. `.vk-stat-row` sets three or four smaller stats side by side in document mode.

```html
<div class="vk-stat">
  <span class="vk-kicker">What the record shows</span>
  <span class="vk-stat-n"><span data-vk-count="19">19</span><small>%</small></span>
  <span class="vk-stat-label">of worked deals closed won.</span>
  <span class="vk-stat-basis">9 of 48 deals, January to September, from the CRM export of 3 October.</span>
</div>
```

### Signal flow (`.vk-flow`)

Sources on the left, a channel of paths in the middle, destinations on the right; dots travel the paths. Use when the point is that data moves from here to there and what each side receives. Name every node; the caption says what the dots are. On narrow screens the paths hide and the columns stack.

```html
<div class="vk-flow">
  <div class="vk-flow-col"><div class="vk-flow-node"><b>Call recordings</b><small>1,400 this year</small></div></div>
  <svg class="vk-flow-paths" viewBox="0 0 300 150" aria-hidden="true">
    <path d="M0 25 C 90 25, 110 75, 150 75 S 210 75, 300 25"/>
    <path class="dot" pathLength="100" d="M0 25 C 90 25, 110 75, 150 75 S 210 75, 300 25"/>
    <circle cx="150" cy="75" r="6" fill="currentColor"/>
  </svg>
  <div class="vk-flow-col"><div class="vk-flow-node"><b>Rep brief before each call</b><small>the move that closed deals like this one</small></div></div>
</div>
```

### Orbit (`.vk-orbit`)

A hub with the things that connect to it on rings. Use when one object (a model, a record, a team) is read or fed by several named parties. The hub label names the object, each node is labelled in the SVG and the same list repeats as text beside it. The dashed outer ring rotates slowly once the screen is in view; nothing else moves.

```html
<svg class="vk-orbit" viewBox="0 0 560 560" role="img" aria-label="A hub labelled deal model with five roles around it">
  <circle class="ring" cx="280" cy="280" r="150"/>
  <g class="spin"><circle class="ring is-dashed" cx="280" cy="280" r="230"/></g>
  <line class="spoke" x1="280" y1="280" x2="280" y2="130"/>
  <circle class="hub-halo" cx="280" cy="280" r="70"/><circle class="hub" cx="280" cy="280" r="52"/>
  <text class="hub-label" x="280" y="285">Deal model</text>
  <circle class="node" cx="280" cy="130" r="9"/><text x="280" y="112" text-anchor="middle">Rep</text>
</svg>
```

### Before and after split (`.vk-split`)

Two panels, the current way on a light surface and the proposed way on the dark band. Use when the change is best shown as the same routine run twice. Each panel carries a one-sentence heading and two to four bullets that correspond line by line. Stacks at 720px.

```html
<div class="vk-split">
  <div class="vk-split-panel"><span class="vk-kicker">Today</span><h3>Reps retell last week's calls from memory.</h3><ul class="vk-list"><li>…</li></ul></div>
  <div class="vk-split-panel is-dark"><span class="vk-kicker">With Acme</span><h3>Every call is summarised before the review.</h3><ul class="vk-list"><li>…</li></ul></div>
</div>
```

### Plan timeline (`.vk-gantt`)

Rows are steps, the track is time, bars sit on real day or week columns. Use for a proof plan, an onboarding path or a quarter's changes. Each row names its owner with a `.vk-tag`; the legend says what the bar colours mean (`is-buyer`, `is-joint`). Bars grow in once the screen is in view. Below 640px the label sits above its track.

```html
<div class="vk-gantt" style="--days:30" role="table" aria-label="Thirty-day plan">
  <div class="vk-gantt-head" role="row"><div class="vk-gantt-label" role="columnheader">Step</div>
    <div class="vk-gantt-ticks" role="columnheader"><span style="--at:1">Day 1</span><span style="--at:14">Day 14</span><span style="--at:29">Day 30</span></div></div>
  <div class="vk-gantt-row" role="row"><div class="vk-gantt-label" role="cell"><span>Connect the CRM</span><span class="vk-tag">Vendor</span></div>
    <div class="vk-gantt-track" role="cell" aria-label="Days 1 to 3"><i style="--s:1;--e:4"></i></div></div>
</div>
```

### Stage strip (`.vk-stages`)

Where something stands in a sequence and what moves it. Use for a rollout phase, the stage where losses end, the buyer's decision path or, on internal pages only, the CRM deal stage. A buyer-facing page labels the steps in the buyer's words and never shows CRM stage names ([information principle 22](../information-principles.md)). Mark `is-done` and `is-now`; the `.vk-stages-note` states the condition in words ("Moves to Proof when …"), per [presentation principle 15b](../presentation-principles.md). Stacks vertically below 640px.

```html
<ol class="vk-stages">
  <li class="is-done"><small>Done</small>Discovery</li>
  <li class="is-now" aria-current="step"><small>Now</small>Evaluation</li>
  <li><small>Next</small>Proof</li>
</ol>
<p class="vk-stages-note">Moves to <b>Proof</b> when the buyer names an owner for the pilot.</p>
```

### Chapter progress, keyboard stepping and the key hint (`.vk-bar`, `.vk-pips`, `.vk-keys`)

Story-mode chrome. The fixed bar shows the brand, the page title and "Screen n of N" with one pip per screen; the runtime fills the pips, keeps the current one lit, steps screens with the arrow keys, Page Up and Down, Space, Home, End and the digits, and skips the handling when focus is in a form field. Scrolling and the pips work without the keys. The hint under the screens fades after the first move and never shows on touch or narrow screens. Both carry `data-chrome` so the render gate treats them as chrome and reports content that slides under them.

```html
<header class="vk-bar" data-chrome>
  <div class="vk-bar-brand"><!-- logo --><span class="vk-bar-title">Prepared for Acme</span></div>
  <div class="vk-bar-chapter"><span class="vk-bar-label">Screen <b data-vk-current>1</b> of <span data-vk-total>7</span></span><ol class="vk-pips" aria-label="Screens"></ol></div>
</header>
<footer class="vk-keys" data-chrome aria-hidden="true"><kbd>&larr;</kbd><kbd>&rarr;</kbd> step &middot; <kbd>1</kbd> to <kbd>7</kbd> jump</footer>
```

### Ghost numeral (`.vk-ghost`)

The screen number drawn as an outlined numeral bleeding off the corner. It is an SVG so it can overflow the screen without being text the gate has to measure, and it is `aria-hidden`. Use one per screen in story mode and nowhere else.

```html
<svg class="vk-ghost" viewBox="0 0 520 240" aria-hidden="true"><text x="0" y="200">03</text></svg>
```

### Loader (`.vk-loader`)

A 2px line at the top that sweeps while fonts settle and finishes when `document.fonts.ready` resolves or 1.6 seconds pass. It covers nothing, so the page reads from the first paint; use it only on pages that self-host heavy fonts or images. Never put content behind a loader.

```html
<div class="vk-loader" aria-hidden="true"></div>
```

### Type scale and layout helpers

`.vk-kicker` (label voice, mono, uppercase), `.vk-display` (the screen headline, 2.2rem to 5rem, light weight unless the brand says otherwise, `.is-wide` for a full-width screen, smaller automatically inside `.is-two`), `.vk-title` (section heading in document mode), `.vk-lede`, `.vk-body`, `.vk-cap` (a caption that explains a visual), `.vk-list`, `.vk-quote` with a `footer` for attribution, `.vk-btn` and `.vk-btn.is-ghost`. Story screens are `<section class="vk-screen" data-pane>` with `.is-dark` for the band; `.vk-screen-inner` centres the content and `.is-two` makes a text-and-visual pair. Document mode uses `.vk-doc`, `.vk-doc-nav` (sticky, opaque), `.vk-doc-hero`, `.vk-section`, `.vk-grid` and `.vk-footer`.

## Motion rules

- Motion explains or it goes: bars grow to their length, dots travel the path they describe, lit tiles light after the rest, a number counts to its value. Nothing bounces, floats or pulses for its own sake.
- Everything plays once, from `.is-in`, with `--d` staggers under 2 seconds. The two continuous animations (the orbit ring, the flow dots) are slow, low-contrast and stop under reduced motion.
- No canvas or shader effects. The kit is CSS and SVG so the render gate, the print path and reduced motion all see the same page.

## Checks

Run the shared lint and the render gate with the kit's chrome before opening a screenshot:

```bash
bash <skill-dir>/../shared/scripts/lint.sh <out.html> --policy <policy.json>
node <skill-dir>/../shared/scripts/render-gate.js <out.html> \
  --chrome ".vk-bar,.vk-keys,.vk-doc-nav,[data-chrome]" --viewports 1440x900,1280x800,375x812
```

Story screens carry `data-pane`, so the gate measures each screen as a pane: text under the bar or the key hint, text cut off, low contrast, and sideways page scroll at 375px are all reported. A screen that grows past the viewport shows up as `under-fixed-chrome` at the smaller desktop size; cut copy or split the screen, never shrink the type below the scale.
