# Format: Editorial Swipe Magazine

Full-viewport horizontal-swipe HTML magazines: a cover, a contents spread, analytical spreads, and a closing, each a deliberate edge-to-edge composition. Reading-first density with editorial pacing, not a reskinned deck.

**Skills that produce this format:** digest (native). Any skill producing a magazine-shaped leave-behind follows this spec.

These principles supplement the universal visual rules in `presentation-principles.md` (one directory up). The universal principles are the floor; these add format-specific requirements. The mechanical scaffold (spread sizing, scroll snap, nav-safe band, surface polarity, print, reduced motion) lives in [`magazine-base.css`](magazine-base.css); **paste its full contents verbatim into the `<style>` block** of every magazine, then layer the brand system on top of its tokens.

## Structure

Create a single horizontal-swipe HTML file:

- **Emit a complete standalone document**: `<!DOCTYPE html>`, `<html lang="en">`, `<meta charset="utf-8">`, `<head>`, `<body>`. A magazine is served as-is by the asset service, not injected into a host page, so nothing supplies these for you. Without the doctype the browser renders in quirks mode, where `<table>` does not inherit `color` from its ancestor: a correct dark-spread stylesheet then paints body ink on a dark field and the table silently disappears. Belt and braces, `magazine-base.css` sets `color: inherit` on tables inside spreads.
- Each spread is `100vw × 100vh`
- Horizontal scroll snap, no vertical page scrolling
- Full-bleed, edge-to-edge editorial compositions
- Narrative-driven spread count
- Start with a cover showing the reporting window. Omit the timezone for ordinary day- or week-based windows; show it only when an exact timestamp boundary materially affects scope.
- For multi-report content, follow the cover with a contents spread naming the included reports or insight threads
- Cover and back cover may be sparse; analytical spreads should pair a dominant claim with inspectable evidence
- Give every spread its own explicit background. Because spreads alternate between light and dark surfaces, a spread that inherits the page or `body` background instead of declaring its own will paint dark text on a dark field (or the reverse) and its content disappears. Set the surface and the foreground color together on each spread (`magazine-base.css` provides the `.is-light` / `.is-dark` pairs; add saturated variants the same way, always background + foreground together).
- Add bottom navigation, ArrowLeft/ArrowRight, Home/End, touch swipe, reduced motion, and one-spread-per-page print styles. The navigation chrome is fixed over spreads of both polarities, so it must stay legible on light and dark surfaces alike: do not use white-on-transparent controls that vanish on a white spread. Use control and active-state colors that hold contrast against every surface in the magazine.
- **Reserve a bottom band for that chrome, and keep content out of it.** Legible navigation is not enough: the last line of a prose column will happily render underneath a fixed pager, and the spread's `overflow: hidden` hides the collision rather than revealing it. `magazine-base.css` defines the band once (`--navsafe`, 84px) and gives each spread `padding-block-end: max(48px, var(--navsafe))`. Full-bleed compositions that skip the padded wrapper, such as a quadrant grid, need the same reservation on the grid itself. A spread-level `padding` SHORTHAND in the brand layer silently overrides the reservation, so set per-spread padding with `padding-inline` / `padding-block-start` (or re-assert the reservation after the shorthand). The pager's own offset and height are pinned in px rather than in a viewport-derived unit, or the band and the chrome drift apart at different viewport sizes and the clearance you measured disappears.
- Do not use experimental canvas or shader effects

## Art direction contract

Treat the brand kit as source material for an editorial system, not as a logo-and-color skin. Reuse its actual typefaces, palette, marks, image treatment, and signature moves.

- **Set the magazine in the brand kit's own typefaces, and actually load them.** Resolve the brand kit first and read its real fonts from its `tokens.css` / manifest, then set the magazine in those faces. Defaulting to a generic editorial pairing when a brand kit exists is the failure to avoid: the output must look like the brand, not a stock magazine template. Naming a font in `font-family` does not load it either, so the brand faces have to actually be delivered: because a magazine is usually hosted or shared, **self-contain them** with `@font-face` and base64 `src` rather than a remote `@import`/CDN `<link>` that can be blocked in the hosted context. Only when no brand kit exists, choose a deliberate editorial pairing and load it the same way. A generic-instead-of-brand typeface, or a declared-but-unloaded one that falls back to a system font, is a defect, not a style choice.
- Give every spread a deliberate composition. Use split color fields, asymmetric columns, viewport-filling grids, 2×2 quadrants, oversized typography, edge-bound rules, full-bleed imagery, and annotated diagrams.
- Do not place a centered stack of padded cards on a decorative background. When cards are semantically necessary, integrate them into a full-width grid or editorial evidence table.
- Make important verified statistics visual anchors. On desktop, the primary statistic should usually render at least 100px tall; use responsive constraints so it still fits shorter viewports.
- Label every oversized numeral by meaning. Structural numbers must visibly say `REPORT`, `SECTION`, `ISSUE`, or `PAGE` in the same composition; never let a chapter number resemble an evidence count or performance metric.
- Label every evidence count with a reader-understandable unit such as calls, companies, deals, or buyer quotes. State the period and scope nearby, and disclose overlap when one source can support multiple categories. Do not use internal labels such as "receipt set."
- When defensible totals are available, include a compact sample-size line on the title or opening spread: calls, companies, evidence excerpts, and completed reports. Keep the reporting window separately visible.
- Use high contrast rhythm. Make the cover and closing dark, add at least one dark interior spread, and use dark or saturated fields for roughly one-third of a longer magazine.
- Change the dominant surface, composition, or color field between consecutive spreads. Avoid a sequence of white pages with interchangeable content blocks.
- Give analytical spreads at least two information layers, such as claim plus evidence, prose plus data, comparison plus annotation, or quote plus source context.
- Treat evidence as editorial material, not filler. Where the producing skill has an evidence-worthiness gate (digest: `references/evidence-and-links.md`), use only items that pass it, and design their source context into the composition.
- Use the full viewport. Intentional negative space should focus attention; it must not make evidence spreads feel unfinished or underfilled.
- Favor a few bold, brand-specific moves over many generic effects. Decoration must improve hierarchy, comprehension, or pacing.

The magazine is not a reskinned deck:

- Write magazine-specific markup and layouts instead of reusing slide DOM
- Use editorial pacing: opener, contents, section openers, reported features, evidence sidebars, pull quotes, annotated comparisons, and a closing
- Allow more prose and evidence than the deck while keeping each spread legible without vertical scrolling
- Use side-by-side compositions where one field carries the main argument and the other carries evidence, context, or source notes
- Preserve meaningful negative space, but do not leave analytical spreads underfilled
- Vary density intentionally: sparse cover and section openers, medium-density reported features, and dense but legible evidence or comparison spreads
- Vary the prose cadence. Do not open every chapter with the same device (a before/after "last period, this period" turn) or lean on the same rhythm section after section (anaphora, rule-of-three, two-beat reversals). A uniform punchy cadence reads as machine-written even when the vocabulary is clean and the facts are real; a strong editor breaks the pattern deliberately.
- Titles carry the finding. Every chapter, section, and spread title is held to the editorial standard: an intelligible sentence that states the actual finding, or, if a short label, one that is clearly decipherable on its own. A vague evocative fragment that could headline any report ("The Pressure," "The Wall") does not pass. Put the claim in the title itself, not only in a subhead beneath it.
- Frame findings for a reader who was not there. Write like a dispatch that sets the scene before making its point, not like an inside note between people who shared the week. An elliptical, knowing line that is true but assumes context ("buyers stopped asking why," "the conversation moved") forces the reader to reconstruct the meaning; state plainly what happened and why it matters, then add the turn. Favor the sentence a smart colleague who missed the period would understand on first read.

## Detailed magazine mode

When content density is `detailed`:

- Give each selected report or section enough room to preserve its section-level reasoning; add spreads based on narrative need
- Use reported features with a claim, 2 to 4 short paragraphs, and a separate evidence or context field
- Keep body copy comfortably readable, generally 18 to 24px on a 1080px-tall desktop viewport
- Split long sections across spreads by idea; never reduce body type to fit
- Carry concrete examples and caveats forward when they change the interpretation
- Remove repeated setup across sections and use cross-references to connect overlapping themes
- Retain cover, contents, section openers, evidence treatments, synthesis, and closing so the result still reads like a magazine

## Motion

- Use native scroll snap for direct manipulation and interruptibility
- For programmatic page changes, target roughly 280 to 360ms with `cubic-bezier(0.2, 0, 0, 1)`; avoid slow cinematic transitions
- Stagger optional content entrances by about 80 to 100ms and keep them under 400ms
- Respect `prefers-reduced-motion` by removing smooth scrolling and entrance motion
- Controls need at least a 40×40px hit area

A minimal navigation script (pair with `magazine-base.css`; adapt IDs/classes as needed):

```html
<script>
  const mag = document.querySelector(".mag");
  const spreads = Array.from(document.querySelectorAll(".spread"));
  const folio = document.getElementById("folio-count");
  const idx = () => Math.round(mag.scrollLeft / mag.clientWidth);
  const go = (i) => spreads[Math.max(0, Math.min(i, spreads.length - 1))]
    .scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", inline: "start" });
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") go(idx() + 1);
    else if (e.key === "ArrowLeft") go(idx() - 1);
    else if (e.key === "Home") go(0);
    else if (e.key === "End") go(spreads.length - 1);
  });
  mag.addEventListener("scroll", () => { if (folio) folio.textContent = (idx() + 1) + " / " + spreads.length; }, { passive: true });
</script>
```

## Responsive review gate

Before delivery, inspect the cover, contents, densest editorial spread, and closing at:

- 16:9 desktop
- 16:10 desktop
- Ultrawide, at least 21:9
- A narrower tablet or mobile landscape viewport

Use width-and-height-constrained type sizing such as `min(vw, vh)` or container queries. Pure `vw` display type is not acceptable because it can collide vertically on ultrawide screens. Check for overlap, clipping, unreadably small type, and unexpected vertical scrolling at every viewport.

For a full-bleed spread the binding constraint is **height**, not width: a naive `min(1vw, 1.9vh)` lets a wide, short viewport pick the width term and blow the vertical budget, which is why ultrawide is usually the worst case despite having the most pixels. Weight the scale toward the height term, then verify the budget rather than trusting it: heading + prose + evidence must fit inside `viewport height − vertical padding − running head − nav band` at every ratio you claim to support.

Run [`shared/scripts/render-gate.js`](../scripts/render-gate.js) before opening a single screenshot. It measures the four things this section asks for that need a browser but not a human eye: fonts actually loaded, text contrast against its painted background, text inside its content box, and text clear of fixed chrome. **Do not hand-roll the overflow check with `scrollHeight - clientHeight`** — on a `overflow: hidden` spread that returns 0 while content is visibly cut off, and it will report a confident pass over broken output. The gate is rectangle-based for exactly this reason. Spend screenshots on taste once it is green.

```bash
node <skill-dir>/../shared/scripts/render-gate.js <magazine.html> \
  --panes ".spread" \
  --chrome "#nav,.folio" \
  --viewports 1600x900,1680x1050,2560x1080,1180x820
```

Also inspect every composition where a light panel is nested inside a dark or saturated spread, and every dark panel nested inside a light spread. Container background changes must explicitly reset the foreground color instead of inheriting it from the parent spread.

Confirm that every spread renders on its own surface and that the fixed navigation chrome is visible on all of them. Step to each spread and check that its background is the intended light or dark field, not the page default showing through, and that no heading, body copy, or evidence text has dropped out against it. Then confirm the navigation controls and page indicators are visible on both the lightest and the darkest spread; controls that only show up over dark spreads are a defect.

Run a computed-style contrast check on rendered text elements before delivery:

- Resolve each text element's effective foreground color and the painted background of its nearest opaque ancestor
- Flag white or near-white text on white or near-white surfaces, and dark text on dark surfaces
- Treat text that becomes readable only when selected or highlighted as a hard failure
- Re-render and visually confirm every flagged spread after fixing it

Confirm every title states its finding:

- Read each chapter, section, and spread title on its own. It must convey the actual finding as an intelligible sentence, or be a short label that is decipherable without the body beneath it.
- A vague evocative fragment that could sit on any report is a failure. Rewrite it to carry the claim, then re-render.

Confirm the copy frames its findings:

- Read the cover lede and each opening paragraph as a reader who was not on the calls. If a line is true but only decipherable to someone who shared the week's context, it fails. Rewrite it to set the scene and state the point plainly, then keep any clever turn as a follow-on rather than the lead.

Confirm the intended typefaces actually rendered:

- In the rendered screenshot, check that the display and body faces are the ones the composition specifies, not a system fallback. A serif that paints as Georgia or a sans that paints as the default UI font means the font never loaded.
- Verify computationally where possible: the resolved `font-family` on a heading and on body text should be a loaded face, and `document.fonts` should report it ready. A declared-but-unloaded font is a hard failure. Fix the load or embed, then re-render and confirm the correct face paints.

## Review Checklist

Format-specific audit for swipe magazines. Run alongside the universal presentation checklist. Run the render gate first (invocation above).

- [ ] **Standalone document.** Doctype, `html lang`, charset, head, body all present; no host-page assumptions.
- [ ] **Base scaffold present.** The full `magazine-base.css` contents are in the `<style>` block; spreads use `.spread` with an explicit `.is-light` / `.is-dark` (or equivalent declared surface+ink pair).
- [ ] **No vertical page scroll; every spread fits.** Content fits inside `100vh` minus the nav band at all four gate viewports.
- [ ] **Chrome legible on every spread.** Nav and folio hold contrast on the lightest and darkest spread; nothing renders under the nav band.
- [ ] **Brand faces loaded.** `document.fonts` reports the declared brand faces ready; no silent system fallback.
- [ ] **Surface rhythm.** Dark cover and closing; at least one dark interior spread; consecutive spreads change surface, composition, or color field.
- [ ] **Anchors labeled.** Oversized numerals carry a meaning label; evidence counts carry reader units with period and scope nearby.
- [ ] **Titles state findings; copy frames them.** No vague fragments, no elliptical insider lines.
- [ ] **Two information layers per analytical spread.** Claim plus inspectable evidence, prose plus data, comparison plus annotation, or quote plus source context.
- [ ] **Keyboard, swipe, print, reduced motion.** ArrowLeft/Right, Home/End, native swipe, one-spread-per-page print, `prefers-reduced-motion` honored.
