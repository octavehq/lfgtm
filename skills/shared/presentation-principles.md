# Presentation Principles: Octave Content

Universal **visual design** rules for all Octave-generated HTML content. These rules apply regardless of document type: Beats reports, battlecards, one-pagers, microsites, briefs, decks.

This file is one of three independent review dimensions:

| Dimension | File | What it covers | Format-dependent? |
|---|---|---|---|
| **Language** | `editorial-rules.md` | AI-isms, banned words, tone, editorial quality | No |
| **Information** | `information-principles.md` | Content structure, narrative arc, evidence, framing | No |
| **Visual design** | `presentation-principles.md` (this file) | Typography, color, layout, spacing, accessibility | No (universal floor) |

**Format-specific visual rules** live in `formats/` (relative to this file):
- `html-document.md`: scrollable docs (research, positioning, meeting-prep, battlecard, win-loss, proposal)
- `slide-deck.md`: paginated slide presentations (deck, coaching)
- `one-pager.md`: single-page leave-behinds (one-pager, proposal condensed)
- `microsite.md`: landing pages (microsite)

Skill-specific blueprints (design system CSS, document structure) add the most specific layer on top.

**Floor vs. craft.** Rules like "no emoji," "no text walls," "token-based colors," and "semantic HTML" are floor rules: violations are always wrong. Principles like "first-glance clarity," "annotate key data points," and "editorial feel" are craft standards: they improve output when applied naturally but shouldn't be forced. If applying a principle makes the output feel over-designed or mechanical, skip it.

## Text & Typography

1. **No text walls.** No single `<p>` should exceed ~2 sentences. When content runs longer, split into multiple `<p>` tags at natural thought breaks. Let CSS handle spacing between paragraphs. Same words, just paragraph breaks so the eye gets breathing room. At the section level, chunk content into distinct visual blocks: each card, callout, or content area conveys one clear idea. If a block requires the reader to hold multiple unrelated concepts simultaneously, split it.

2. **Type hierarchy must be clear and consistent.** Headings, subheadings, body text, labels, and captions each have a distinct visual role. The reader should instantly understand what level of information they're looking at. Hierarchy is built through size, weight, color, and spacing working together: if everything carries the same visual weight, nothing stands out and the eye has nowhere to land.

3. **Headings are large and confident.** Don't shrink headings to conserve space. Generous heading sizes with comfortable line-height communicate professionalism.

4. **Labels use uppercase + letterspacing.** Section labels, stat labels, category markers, and other structural signposts use the label voice: uppercase, letterspaced, smaller size. This differentiates them from body content.

4b. **No orphan words.** Prevent single short words stranding alone on a final line, especially in headings, introductory sentences, and card descriptions. Use `text-wrap: pretty` on body text and `text-wrap: balance` on headings as a CSS floor. For critical copy, verify visually that no short word hangs alone.

## Layout & Spacing

5. **Order by importance within every section.** Most impactful item first. Never chronological, never alphabetical. Position communicates priority.

6. **Cut rather than expand.** When the output feels long, fewer items with sharper content beats more sections or subsections. Restraint is the product.

7. **Generous whitespace.** Sections need breathing room: comfortable padding between major blocks. Content packed edge-to-edge looks rushed. Airy layouts look professional.

8. **No redundant content across sections.** If one section covers a finding, don't repeat it elsewhere. Each section earns its space independently.

9. **Proximity is meaning.** Elements placed close together are perceived as related. Elements separated by space are perceived as distinct. Use this deliberately: group related items tightly, separate unrelated items with whitespace. If two items are visually adjacent but conceptually unrelated, the layout is lying to the reader.

9b. **Consistent internal spacing in cards.** When a card component contains multiple text elements (number, description, attribution), use a single spacing mechanism (flexbox `gap` or uniform margin) so the distance between all adjacent pairs is identical. Mixed individual margins drift out of sync and look unfinished.

9c. **Align text edges within cards.** When a card heading has a marker element (number badge, icon, bullet) offset to the left, body text below must align with the heading text, not the card edge. Match the left margin to the marker width + gap so all readable text shares the same left edge.

9d. **Three font sizes max per visual block.** Each distinct visual section (a slide, a card cluster, a hero panel) should use at most three font sizes for its content. Persistent navigation or chrome elements shared across all sections don't count. More than three sizes creates visual noise: the eye can't establish hierarchy when too many tiers compete. Pick a headline size, a body size, and optionally a label/caption size. Everything in that block uses one of those three.

    **Bad:** A section with heading at 80px, subtitle at 26px, list items at 24px, sidebar heading at 22px, sidebar body at 18px, stat number at 36px, stat label at 12px. Seven sizes, no clear hierarchy.
    **Good:** Heading at 96px, subtitle at 32px, body at 30px. Three sizes. The section reads as a clear hierarchy: title → context → details.

9e. **Consistent horizontal margins.** All content within a layout uses the same left and right padding. Navigation bars, section labels, headlines, cards, and body content align to the same left edge. Nothing should start at a different inset unless it's intentionally nested (like a card's internal padding).

    **Bad:** Nav starts at 80px padding, section label at 100px left, content at 120px left, bullets at 140px left. Four different left edges create a ragged, undesigned feel.
    **Good:** Nav, labels, and content containers all align to the same margin. Internal elements are inset by their own padding, but the outer containers share one left edge.

9f. **Vertical alignment across repeated sections.** When a layout has multiple sections or pages that follow the same pattern, content should start at the same vertical position in each. When the viewer scrolls or navigates between sections, content shouldn't jump up and down. Define a content container with a fixed top position and reuse it consistently.

    **Bad:** Section A headline starts at y=172px, section B starts at y=200px, section C starts at y=150px. Content bounces as you navigate.
    **Good:** All sections use the same content container with a fixed top offset. Headlines start at the same vertical position. Navigation between sections feels stable.

9g. **Whitespace is structural, not leftover.** Every gap in a layout should be intentional: the space between a nav and a headline, between a headline and content, between content blocks. Use a consistent gap scale (e.g., small / medium / large at defined px values) and assign gaps deliberately. If a gap is visibly larger than the next size up in the scale, either the content above is too small or the content below needs to move up.

    **Bad:** 12px between nav and headline, 28px between headline and content, then a huge void below the content. The gaps are random and the emptiness is unplanned.
    **Good:** Nav to headline: defined gap. Headline to content: defined gap. Content fills the remaining space via vertical centering or expansion. No unexplained voids.

9h. **No text-on-visual collisions.** When placing text over a visual element (SVG, illustration, diagram, chart), verify that the text box doesn't overlap any labels, endpoints, or interactive elements in the visual. Use the coordinate system of the layout to check clearances. If a heading sits on top of a diagram label at approximately the same position, one of them must move.

## Visual Restraint

10. **Editorial, not dashboard.** Clean typography, generous whitespace, reading-first layout. The reader should feel like they're getting a brief from a sharp analyst, not a report from a software tool.

11. **No emoji.** Zero emoji characters anywhere in the document.

12. **No decorative imagery.** No generic icons, stock illustrations, or background images used for decoration. Every visual element must reinforce the message: it adds information, clarifies a concept, or anchors the intended emotion. If it doesn't strengthen the reader's understanding, it's noise. Cut it.

12b. **No raw metadata as UI elements.** Research and enrichment data (deal range, strategy type, market names, investment criteria) must be woven into prose or used to inform the narrative. Never surface enrichment data as standalone chips, badges, tags, or pill-shaped metadata labels. If the reader would ask "why am I seeing this as a label?" it belongs in a sentence, not a UI element.

13. **Restraint in effects.** Avoid stacking visual effects. One or two signature treatments (a subtle glow, a scroll-reveal) are enough. More than that becomes noise.

## Data Visualization

14. **Match the visualization to the story.** Choose the format that makes the insight self-evident:
    - **Single stat callout**: one number that makes the point ("3x," "42%"). Use when the number alone is the headline.
    - **Bar/column chart**: comparing quantities across categories. Use when relative size IS the argument.
    - **Line chart**: showing change over time. Use when the trend IS the argument.
    - **Table**: precise values that the reader needs to reference, not just scan. Use when the reader will look up specific cells.
    - **Prose**: when the insight is nuanced, contextual, or comparative in ways a chart would flatten. Not everything needs a visual.

    Don't default to charts when a sentence would be clearer. Don't default to prose when a single stat would hit harder.

15. **One chart, one message.** Each visualization makes exactly one point, stated in its title. If a chart supports two arguments, either pick the stronger one or split it into two charts. Multi-message charts confuse; the reader doesn't know what to take away.

## Self-Contained Output

16. **Single HTML file, no external dependencies** beyond web fonts (Google Fonts). All CSS inline in `<style>`, all JS inline in `<script>`. Images as data URIs or inline SVGs.

17. **Print must work.** Tabbed interfaces flatten to labeled blocks. Dark themes invert to light. Navigation chrome hidden. Cards avoid page breaks. Verify print renders correctly after any structural change.

## Accessibility

18. **Semantic HTML.** Use appropriate elements: `<nav>` for navigation, `<section>` for content sections, `<footer>` for footer, `role` and `aria-*` attributes for interactive widgets (tabs, modals).

19. **Keyboard accessible.** Tab navigation works. Modals close with Escape. Focus rings visible. Interactive elements reachable without a mouse.

20. **Reduced motion.** Animations respect `prefers-reduced-motion`. Essential content never depends on animation to be visible.

## Color & Theming

21. **Colors derive from a token system.** All colors on the page trace back to a small set of root variables. No hand-picked hex values scattered through the stylesheet. If a new color is needed, derive it from existing tokens.

22. **Accent color is semantic, not decorative.** The primary accent is reserved for elements that carry meaning: active states, callouts, stat values, interactive affordances. Never used as a decorative fill or ornamental border. In charts and data visualizations, use accent color to highlight the key data point that supports the headline: don't make every bar the same color when one bar IS the story. Use callouts or arrows to annotate the key data point when the takeaway isn't self-evident from the visual alone.

23. **Sufficient contrast.** Text meets WCAG AA contrast ratios against its background. Accent colors used as text must be legible on their surface.

---

## Review Checklist

Self-contained visual/presentation audit. Run every check against the generated HTML file. Fix violations inline.

### Text & Typography

- [ ] **No text walls.** No single `<p>` exceeds ~2 sentences. Scan for any `<p>` containing 3+ period-space-capital sequences. Multi-sentence content uses wrapper `<div>` with child `<p>` tags.
- [ ] **Type hierarchy.** At least 3 distinct type levels visible (heading, subheading, body). Each is visually differentiated by size, weight, or family.
- [ ] **Headings are large.** Main headings are at least `1.5rem` (ideally `2rem+`). Not shrunk to fit.
- [ ] **Labels use label voice.** Structural labels (section markers, stat labels, category headings) use uppercase + letterspacing, distinct from body text.
- [ ] **No orphan words.** Headings use `text-wrap: balance`, body text uses `text-wrap: pretty`. No single short word stranding alone on a final line in headings or short text blocks.

### Layout & Spacing

- [ ] **Ordered by importance.** Within each section, most impactful items appear first. Not chronological, not alphabetical.
- [ ] **No redundancy.** No finding or insight repeated across multiple sections.
- [ ] **Whitespace.** Major sections have comfortable vertical padding (`2rem+`). Content is not packed edge-to-edge.
- [ ] **Proximity matches meaning.** Related items are visually grouped. Unrelated items are separated by space. No adjacent elements that imply a relationship that doesn't exist.
- [ ] **Card spacing consistent.** Card components with multiple text elements use a single spacing mechanism (flexbox `gap` or uniform margin). No mixed individual margins creating uneven gaps.
- [ ] **Card text edges aligned.** When a card heading has a marker (number badge, icon), body text below aligns with the heading text start, not the card edge.
- [ ] **Three font sizes max per block.** Each visual section uses at most three distinct font sizes (excluding persistent nav/chrome). More than three = visual noise.
- [ ] **Horizontal margins consistent.** All content containers (nav, labels, headlines, cards, body) align to the same left and right margins. No ragged left edges from mixed insets.
- [ ] **Vertical alignment across sections.** Repeated section layouts start content at the same vertical position. No content jumping between sections.
- [ ] **Whitespace is structural.** Gaps follow a consistent scale. No unexplained voids larger than the next gap size up in the scale.
- [ ] **No text-on-visual collisions.** Overlay text (titles, labels) does not overlap labels, endpoints, or elements in underlying visuals (SVGs, diagrams, charts).
- [ ] **Reasonable length.** The document doesn't feel padded. Every section earns its space.
- [ ] **First-glance clarity.** Each section is scannable in ~3 seconds. A reader unfamiliar with the content should immediately understand what each section is about and what matters most. If a section requires study to parse, it needs clearer hierarchy or chunking.

### Visual Restraint

- [ ] **No emoji.** Zero emoji characters anywhere in reader-facing text.
- [ ] **No decorative imagery.** No generic icons or illustrations used for decoration.
- [ ] **No raw metadata UI.** No enrichment/research data displayed as standalone chips, badges, tags, or pill labels. All personalized data is woven into prose.
- [ ] **Editorial feel.** The output reads as a market brief, not a software dashboard.
- [ ] **Effects are minimal.** No more than 2-3 signature visual treatments. No stacked gradients, glows, shadows competing for attention.

### Data Visualization (where applicable)

- [ ] **Visualization matches the story.** Charts, stats, and tables use the right format for the insight type. No bar charts where a single stat callout would hit harder. No prose where a chart would be clearer.
- [ ] **One chart, one message.** Each visualization makes one point, stated in its title. No multi-message charts.
- [ ] **Key data annotated.** Accent color or callouts highlight the data point that supports the headline. Not every bar the same color.

### Self-Contained & Print

- [ ] **Single HTML file.** All CSS in `<style>`, all JS in `<script>`. No external CSS/JS files.
- [ ] **No external dependencies** beyond Google Fonts `<link>`.
- [ ] **Images are inline.** Data URIs or inline SVGs, not external URLs.
- [ ] **Print styles present.** `@media print` block exists with: light background, dark text, navigation hidden, tabs flattened to labeled blocks, cards avoid page breaks, `print-color-adjust: exact`.

### Accessibility

- [ ] **Semantic HTML.** Correct use of `<nav>`, `<section>`, `<footer>`, `<header>`.
- [ ] **ARIA attributes.** Tabs have `role="tablist"`, `role="tab"`, `aria-selected`. Modals have `aria-label` on close buttons.
- [ ] **Keyboard.** Modals close on Escape. Focus rings visible on interactive elements.
- [ ] **Reduced motion.** `@media (prefers-reduced-motion: reduce)` present. Essential content visible without animation.

### Color & Theming

- [ ] **Token-based colors.** All colors trace to CSS custom properties (`:root` variables). No hardcoded hex/rgb outside of `@media print` or `box-shadow` blacks.
- [ ] **Accent is semantic.** Primary accent used only for meaningful elements (active states, callouts, stats, interactive affordances), not decorative fills.
- [ ] **Contrast.** Body text legible against its background. Accent text legible on its surface. No low-contrast text on dark backgrounds.

### Brand & Logo

- [ ] **Logo is the workspace company's, verified on the pixels.** Every logo in the chrome (header, cover, footer, dark bands) is the workspace company's own mark, confirmed by rendering the actual image, not by trusting the manifest/filename. A white/`onDark` logo is invisible on a light preview and cached kits can carry a stray customer logo, so the dark-band logo must be checked on a dark surface specifically. A customer/partner mark on the chrome is contamination. See [brand-kit-usage.md](brand-kit-usage.md) → Logo integrity.
- [ ] **Logo inlined.** Logo is a data URI / inline SVG, not a local file path or hotlink, so the file is self-contained.
