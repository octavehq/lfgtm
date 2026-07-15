# One-Pager Regression Checklist

Issues found during testing, kept as a living checklist. Every item here was a real failure in a real output. Run this list against any new generation before delivering.

New items go at the bottom of the relevant section with the date and test case that surfaced them.

---

## Section Labels

- [ ] **Labels are plain and conversational.** Not academic ("The Challenge", "Our Approach"), not cheeky ("Sound Familiar?"), not aggressive/declarative ("What You're Up Against"). Good: "The Problem Today", "How [Product] Helps", "What Teams Are Seeing." *(2026-06-24, Crexi → CommonWealth)*
- [ ] **Labels use label voice.** Uppercase, letterspaced, visually distinct from body text and headings. *(2026-06-23, Crexi → CommonWealth)*

## Typography

- [ ] **No orphan words.** Headings use `text-wrap: balance`, body text uses `text-wrap: pretty`. No single short word alone on a final line, especially in headings and card descriptions. *(2026-06-23, Crexi → CommonWealth)*
- [ ] **Font is correct.** If branded, the font-family matches what the target company actually uses on their site (verify against the Google Fonts link or @font-face in their HTML). Don't guess — DM Sans and Inter look similar but render differently. *(2026-06-24, Crexi → CommonWealth)*
- [ ] **Font weights match the brand.** Many brands use medium (500) or semibold (600) for headings, not bold (700). Check the actual weight from the site's CSS. *(2026-06-23, Crexi → CommonWealth)*

## Content Structure

- [ ] **No text walls.** No single `<p>` exceeds ~2 sentences. Long content split at natural thought breaks. *(2026-06-23, Crexi → CommonWealth)*
- [ ] **Problem section is lede + cards, not paragraphs.** One-sentence lede (~20 words), then pain points as cards with short subheaders ("Signals go undetected" pattern). No 2-3 sentence prose runs. *(2026-07-02, Crexi → CommonWealth)*
- [ ] **Lede renders a tier above card body text.** Section intro is visually superior (size/weight) to the card copy below it — not the same size. *(2026-07-02, Crexi → CommonWealth)*
- [ ] **CTA is two action bullets, not a paragraph.** Next Step block reads as actions and outcomes, not a product description. Roughly a third shorter than the drafted prose version. *(2026-07-02, Crexi → CommonWealth)*
- [ ] **Proof section keeps the transformation-metric format.** Big before → after numbers ("$14M → $3M", "3×", "11 → 22") + one-line context + named customer attribution. This format is validated — don't drift from it. *(2026-07-02, Crexi → CommonWealth — flagged as best-in-class)*
- [ ] **Sibling cards vary their cadence.** Cards in the same grid don't all use the same rhetorical template (e.g., "X, not Y" headers on every card). Max one contrast-construction header per grid. *(2026-07-02, Crexi → CommonWealth)*
- [ ] **No raw metadata as UI elements.** Research/enrichment data (deal range, strategy type, market names) woven into prose, not displayed as standalone chips, badges, or pill labels. *(2026-06-23, Crexi → CommonWealth)*
- [ ] **How It Works / approach headings are short.** 4-6 words max. Not full sentences. The body text carries the detail. *(2026-06-23, Crexi → CommonWealth)*

## Layout & Spacing

- [ ] **Card spacing uses a single mechanism.** Flexbox `gap` or uniform margin — not mixed individual margins that drift out of sync. *(2026-06-23, Crexi → CommonWealth)*
- [ ] **Card text edges aligned.** When a card heading has a marker (number badge, icon), body text below aligns with the heading text start, not the card edge. *(2026-06-23, Crexi → CommonWealth)*
- [ ] **Page background provides contrast.** White background works with dark hero/CTA bands and colored section surfaces. Gray-50 (#f8fafc) can look washed out. *(2026-06-24, Crexi → CommonWealth)*

## Brand Fidelity

- [ ] **Logo is the real asset.** Inline SVG from the brand kit or downloaded from the site — not a text approximation or a generic placeholder. Verified to be the correct brand (not a stale CDN asset or client logo). *(2026-06-24, Crexi → CommonWealth)*
- [ ] **Logo uses correct fill per surface.** White/light text on dark hero, dark text on light surface. Brand mark icon keeps its brand color on both. Never use `filter:brightness(0) invert(1)` to recolor. *(2026-06-24, Crexi → CommonWealth)*
- [ ] **Brand colors from the actual site.** Extracted from the page's CSS/HTML, not approximated from a screenshot. Confirm hex values against the scrape data. *(2026-06-23, Crexi → CommonWealth)*

---

## Adding new items

When you find a new issue during testing:

```markdown
- [ ] **Short description of the check.** What to look for and why it matters. *(YYYY-MM-DD, target → recipient)*
```

Put it under the most relevant section. If no section fits, add a new one.
