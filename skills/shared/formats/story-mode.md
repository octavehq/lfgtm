# Format: Story mode

A buyer-facing page told as a short run of full-viewport screens, one idea each, stepped with the keyboard or scrolled. Huge, confident type carries the claim on every screen and one hero motif explains the mechanism. It replaces the long scrolling report for anything a buyer or champion opens on their own.

**Skills that produce this format:** champion-deal-room, one-pager (web leave-behind), deck (async, link-shared), microsite. It is the default for their buyer-facing outputs; document mode ([html-document.md](html-document.md)) stays available on request and stays the default for internal reports.

These principles supplement the universal visual rules in `presentation-principles.md` (one directory up) and build on the [visual kit](visual-kit.md), whose CSS and runtime are pasted into every story page. The finished reference is [`examples/acme-story.html`](examples/acme-story.html).

## Principles

1. **One idea per screen.** A screen carries one claim, stated in its headline as one sentence, and one visual or one block of support. When a screen needs a second visual or a second heading, it is two screens.

2. **A screen budget replaces a section count, and the budget depends on the skill.** Each skill has its own budget:

   | Skill | Budget |
   |---|---|
   | one-pager (web leave-behind) | At most 3 screens, or a single scrolling page that carries one signature visual |
   | champion-deal-room | 5 to 8 screens (7 by default) |
   | microsite | 5 to 8 screens |
   | deck (read as a link) | 5 to 8 screens |

   A one-pager is read in under a minute, so its budget holds even when the evidence could fill more. A count the user asks for ("5 slides", "3 screens") replaces the budget, above or below, and the arc is cut to fit that count. The skill's content rules still decide what earns space; the budget decides how it is cut. Map the skill's sections to screens before writing, and merge or drop until the count fits. Length is measured in screens, never in pixels.

3. **The arc is fixed.** Opening claim with the signature visual, the one number, the mechanism, the change (today against with), who reads it or the proof, the plan, the ask. A skill reshapes its sections onto this arc rather than inventing a new one.

4. **Type carries the screen.** The headline uses `.vk-display`: 2.2rem to 5rem, the brand's display weight (light unless the kit says otherwise), balanced wrapping, at most 16 words. A lede of one or two sentences sits under it in `.vk-lede`. Body text appears only inside a component (a split panel, a plan row, a stat basis), never as paragraphs under the headline.

5. **One signature visual per screen, one hero motif per page.** Each screen carries at most one visual. The hero motif shows the page's mechanism or data at full size (a signal flow, an orbit, a card grid, a plan timeline) and sits on the opening or mechanism screen; no later screen repeats it or adds a second mechanism. Screen 1 always pairs its headline with a kit visual of the mechanism or the data, the signature visual or a smaller one; a two-column opening never leaves its second column empty or decorative. Other screens use the smaller components (stat, split, stages), a map of the people involved, or nothing. A visual that could be removed without the reader losing a fact is decoration and goes.

6. **Surfaces alternate.** Dark band and light page alternate screen to screen; the opening and the ask are dark. The grid texture and glow belong to dark screens only and come from the kit, never from a hand-written gradient.

7. **Motion explains.** Bars grow to their length, dots travel the path they describe, lit tiles light after the rest, a number counts to its value, and each plays once as the screen enters. The only loops are ambient ones that carry no information (the orbit ring's slow turn, the flow dots once the path is drawn), and they stop under reduced motion. Nothing starts hidden: the page reads the same with scripts off, in print and in a full-page capture taken without scrolling.

8. **Presenter keys with a scroll fallback.** Arrow keys, Page Up and Down, Space, Home, End and the digits step screens. Scrolling, the pips in the bar and the skip link reach every screen without the keys. The key hint fades after the first move and never shows on touch screens.

9. **Chrome stays out of the content box.** The fixed bar (brand, page title, "Screen n of N", pips) and the key hint carry `data-chrome`; screens reserve their height. A screen that grows past the viewport at 1280x800 is over budget: cut copy or split it.

10. **Every number has a basis on the screen that shows it.** Period, denominator and source sit under the stat in `.vk-stat-basis` or in the caption of the visual, in the same words the skill's evidence rules require. The hero number (screen 1 or the one-number screen) is the buyer's own figure or a verified record, never a vendor-reported range presented as fact, and its caption names the source ([information principle 26](../information-principles.md#claims-against-the-data)). Counts and names agree on every screen: the seats, steps or teams counted on one screen are the same number on every other ([information principle 24](../information-principles.md#claims-against-the-data)).

11. **The ask is a screen, with the path.** The last screen states the next step as one sentence with a date, a primary button and a contact line, and a strip with the condition that moves to the next step written as text. On a buyer-facing page the strip shows the buyer's own decision path or the mutual plan steps in the buyer's words ("Security review", "Board sign-off"), never CRM stage names or amounts ([information principle 22](../information-principles.md)). Only internal pages may show CRM stages.

12. **Editorial rules win over a brand kit's copy preferences.** A kit governs visuals only. When a kit prefers two-sentence or two-line headlines, the headline stays one sentence in one run of text ([editorial rule 8c](../editorial-rules.md), [brand-kit-usage.md](../brand-kit-usage.md)).

13. **Share metadata and a single file.** `og:title` and `og:description` describe the page for a stranger; everything is inline except Google Fonts and, when published, the sibling `assets/og.png` ([social-meta.md](../social-meta.md)).

## Screen plan template

Before writing, fill this table from the skill's section list and the evidence gathered:

| Screen | Idea (one sentence) | Component | Surface |
|---|---|---|---|
| 1 | The opening claim | `.vk-tiles` or the signature visual | dark |
| 2 | The one number | `.vk-stat` | light |
| 3 | How it works | `.vk-flow` or `.vk-orbit` (the hero motif) | dark |
| 4 | What changes first | `.vk-split` | light |
| 5 | Who reads it, or the proof | `.vk-quotes`, `.vk-stat-row`, or `.vk-orbit` mapping the readers when screen 3 used `.vk-flow` | dark |
| 6 | The plan | `.vk-gantt` | light |
| 7 | The ask | `.vk-stages` (buyer's path) + buttons | dark |

Six screens drop screen 5, and five screens also fold the plan into the ask. Eight screens add one proof or one objection screen after 5, never a second mechanism. For a count below five (a one-pager's three screens, or a user's count), keep the opening, the mechanism and the ask: the opening carries the one number in its kicker or visual, the mechanism screen carries the proof, and the ask carries the next step.

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

- [ ] **Screen count matches the skill's budget.** Count the `.vk-screen` elements: the count the user asked for, else the skill's budget in principle 2 (at most 3 for a one-pager, 5 to 8 for champion-deal-room, microsite and deck); the arc runs opening, number, mechanism, change, proof or readers, plan, ask, cut to fit.
- [ ] **Screen 1 carries a visual.** The opening headline sits beside or above a kit visual that explains the mechanism or the data; no empty or decorative half.
- [ ] **One idea per screen.** Each screen has one headline (one sentence, at most 16 words) and one visual or one support block.
- [ ] **One visual per screen, one hero motif.** No screen carries two visuals; exactly one component explains the mechanism or the data at full size, on the opening or mechanism screen, and no later screen repeats it or adds a second mechanism.
- [ ] **Every visual is captioned or labelled.** Tiles, flows, orbits and plans say what their units are; every stat shows its basis.
- [ ] **The hero number is the buyer's or verified, with its source on screen.** No vendor-reported range or multiplier as the hero; the caption names whose figure it is.
- [ ] **The screens agree with each other.** Every count, name and figure that appears on two screens is identical on both (seats, steps, teams, amounts).
- [ ] **The last strip speaks the buyer's words.** On a buyer-facing page the strip shows the buyer's decision path or mutual plan steps, with no CRM stage name or amount.
- [ ] **Headlines stay one sentence whatever the kit prefers.** No two-sentence or two-line headline carried over from a brand kit's copy style.
- [ ] **Surfaces alternate** and the kit paints the dark screens (no hand-written gradients).
- [ ] **Fits the viewport.** No `under-fixed-chrome` at 1280x800; a screen that grows past the viewport is cut or split.
- [ ] **Keys and scroll both work.** Arrow keys step, pips jump, the skip link lands, the hint fades after the first move and hides on touch.
- [ ] **Readable without scripts.** With JavaScript off every screen's text and visual is visible; the key hint and pips are hidden.
- [ ] **Reduced motion and print.** `document.getAnimations()` is empty under `prefers-reduced-motion`; print shows every screen light, one per page, without chrome.
- [ ] **375px.** No sideways scroll, 16px gutters, the two-column screens and the split stack, the plan labels sit above their tracks.
- [ ] **Brand faces loaded** at the display weight; the gate's font line shows the heading face loaded.
- [ ] **Share metadata** per [social-meta.md](../social-meta.md).
