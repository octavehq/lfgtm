# Format: Story mode

A buyer-facing page told as six to eight full-viewport screens, one idea each, stepped with the keyboard or scrolled. Huge, confident type carries the claim on every screen and one signature visual explains the mechanism. It replaces the long scrolling report for anything a buyer or champion opens on their own.

**Skills that produce this format:** champion-deal-room, one-pager (web leave-behind), deck (async, link-shared), microsite. It is the default for their buyer-facing outputs; document mode ([html-document.md](html-document.md)) stays available on request and stays the default for internal reports.

These principles supplement the universal visual rules in `presentation-principles.md` (one directory up) and build on the [visual kit](visual-kit.md), whose CSS and runtime are pasted into every story page. The finished reference is [`examples/acme-story.html`](examples/acme-story.html).

## Principles

1. **One idea per screen.** A screen carries one claim, stated in its headline as one sentence, and one visual or one block of support. When a screen needs a second visual or a second heading, it is two screens.

2. **A screen budget replaces a section count.** Six screens is the floor, eight is the ceiling. The skill's content rules still decide what earns space; the budget decides how it is cut. Map the skill's sections to screens before writing, and merge or drop until the count fits. Length is measured in screens, never in pixels.

3. **The arc is fixed.** Opening claim with the signature visual, the one number, the mechanism, the change (today against with), who reads it or the proof, the plan, the ask. A skill reshapes its sections onto this arc rather than inventing a new one.

4. **Type carries the screen.** The headline uses `.vk-display`: 2.2rem to 5rem, the brand's display weight (light unless the kit says otherwise), balanced wrapping, at most 16 words. A lede of one or two sentences sits under it in `.vk-lede`. Body text appears only inside a component (a split panel, a plan row, a stat basis), never as paragraphs under the headline.

5. **One signature visual that explains.** Each page has one visual that shows the mechanism or the data (a signal flow, an orbit, a card grid, a plan timeline) and that visual sits on the opening or mechanism screen. Other screens use the smaller components (stat, split, stages) or nothing. A visual that could be removed without the reader losing a fact is decoration and goes.

6. **Surfaces alternate.** Dark band and light page alternate screen to screen; the opening and the ask are dark. The grid texture and glow belong to dark screens only and come from the kit, never from a hand-written gradient.

7. **Motion explains.** Bars grow to their length, dots travel the path they describe, lit tiles light after the rest, a number counts to its value, and everything plays once as the screen enters. Nothing starts hidden: the page reads the same with scripts off, in print and in a full-page capture taken without scrolling.

8. **Presenter keys with a scroll fallback.** Arrow keys, Page Up and Down, Space, Home, End and the digits step screens. Scrolling, the pips in the bar and the skip link reach every screen without the keys. The key hint fades after the first move and never shows on touch screens.

9. **Chrome stays out of the content box.** The fixed bar (brand, page title, "Screen n of N", pips) and the key hint carry `data-chrome`; screens reserve their height. A screen that grows past the viewport at 1280x800 is over budget: cut copy or split it.

10. **Every number has a basis on the screen that shows it.** Period, denominator and source sit under the stat in `.vk-stat-basis` or in the caption of the visual, in the same words the skill's evidence rules require.

11. **The ask is a screen, with the stage.** The last screen states the next step as one sentence with a date, a primary button and a contact line, and the stage strip with the condition that moves the deal written as text.

12. **Share metadata and a single file.** `og:title` and `og:description` describe the page for a stranger; everything is inline except Google Fonts and, when published, the sibling `assets/og.png` ([social-meta.md](../social-meta.md)).

## Screen plan template

Before writing, fill this table from the skill's section list and the evidence gathered:

| Screen | Idea (one sentence) | Component | Surface |
|---|---|---|---|
| 1 | The opening claim | `.vk-tiles` or the signature visual | dark |
| 2 | The one number | `.vk-stat` | light |
| 3 | How it works | `.vk-flow` or `.vk-orbit` | dark |
| 4 | What changes first | `.vk-split` | light |
| 5 | Who reads it, or the proof | `.vk-orbit`, `.vk-quotes` or `.vk-stat-row` | dark |
| 6 | The plan | `.vk-gantt` | light |
| 7 | The ask | `.vk-stages` + buttons | dark |

Six screens drop screen 5; eight screens add one proof or one objection screen after 5, never a second mechanism.

## Scaffold

```html
<body class="vk-story">
<a class="vk-skip" href="#s1">Skip to content</a>
<div class="vk-loader" aria-hidden="true"></div>
<header class="vk-bar" data-chrome>…brand, title, "Screen n of N", <ol class="vk-pips"></ol>…</header>
<main class="vk-screens">
  <section class="vk-screen is-dark" id="s1" data-pane aria-label="Opening">
    <svg class="vk-ghost" viewBox="0 0 520 240" aria-hidden="true"><text x="0" y="200">01</text></svg>
    <div class="vk-screen-inner is-two">
      <div>
        <span class="vk-kicker vk-rise">Prepared for Acme · date</span>
        <h1 class="vk-display vk-rise" style="--d:.08s">One sentence that states the claim.</h1>
        <p class="vk-lede vk-rise" style="--d:.16s">One or two sentences of support.</p>
      </div>
      <div class="vk-rise" style="--d:.2s"><!-- the signature visual and its .vk-cap --></div>
    </div>
  </section>
  <!-- screens 2 to 7 -->
</main>
<footer class="vk-keys" data-chrome aria-hidden="true"><kbd>&larr;</kbd><kbd>&rarr;</kbd> step &middot; <kbd>1</kbd> to <kbd>7</kbd> jump</footer>
<script>/* visual-kit.js, pasted in full */</script>
</body>
```

The `<head>` carries the brand kit's `:root`, the full `visual-kit.css`, and the page's own rules, in that order.

---

## Review Checklist

Format-specific audit for story pages. Run alongside the universal presentation checklist.

Run the render gate first. Screens are panes, the bar and the key hint are chrome, and the gate reports text under either, text cut off, low contrast and sideways scroll at 375px:

```bash
node <skill-dir>/../shared/scripts/render-gate.js <story.html> \
  --chrome ".vk-bar,.vk-keys,[data-chrome]" --viewports 1440x900,1280x800,375x812
```

- [ ] **Six to eight screens.** Count the `.vk-screen` elements; the arc runs opening, number, mechanism, change, proof or readers, plan, ask.
- [ ] **One idea per screen.** Each screen has one headline (one sentence, at most 16 words) and one visual or one support block.
- [ ] **One signature visual.** Exactly one component explains the mechanism or the data at full size, on the opening or mechanism screen; every other visual is a stat, a split, a strip or a plan.
- [ ] **Every visual is captioned or labelled.** Tiles, flows, orbits and plans say what their units are; every stat shows its basis.
- [ ] **Surfaces alternate** and the kit paints the dark screens (no hand-written gradients).
- [ ] **Fits the viewport.** No `under-fixed-chrome` at 1280x800; a screen that grows past the viewport is cut or split.
- [ ] **Keys and scroll both work.** Arrow keys step, pips jump, the skip link lands, the hint fades after the first move and hides on touch.
- [ ] **Readable without scripts.** With JavaScript off every screen's text and visual is visible; the key hint and pips are hidden.
- [ ] **Reduced motion and print.** `document.getAnimations()` is empty under `prefers-reduced-motion`; print shows every screen light, one per page, without chrome.
- [ ] **375px.** No sideways scroll, 16px gutters, the two-column screens and the split stack, the plan labels sit above their tracks.
- [ ] **Brand faces loaded** at the display weight; the gate's font line shows the heading face loaded.
- [ ] **Share metadata** per [social-meta.md](../social-meta.md).
