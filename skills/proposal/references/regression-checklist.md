# Proposal Regression Checklist

Issues found during testing, kept as a living checklist. Every item here was a real failure (or a validated win worth protecting) in a real output. Run this list against any new generation before delivering.

New items go at the bottom of the relevant section with the date and test case that surfaced them.

---

## Density

- [ ] **Exec summary is 3 paragraphs at half length.** 2-3 sentences per paragraph, and the takeaway box lands above the fold — screenshot-test the first viewport. If paragraphs push the box below, cut paragraphs. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Capability cards: one sentence after the "Solves for:" tag.** The tag carries the pain mapping; the sentence says what it does. Second sentences restate the tag and read repetitive across 6 boxes. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Investment framing prose is tight.** No trailing compound sentences stacking three benefits into one clause. One sentence setup, one sentence payoff. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Closing CTA is one snappy line.** ½-⅔ of the first draft. Two sentences is a paragraph, not a CTA. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Rollout plan is a literal placeholder, not fabricated.** Do not generate a "Connect / Validate / Roll out" phase list, weeks, or dates. The whole rollout is the seller's to build. Show one prominent "( Add your rollout plan and timeline )" panel. *(2026-07-08, Corient proposal)*

## Structure & Repetition

- [ ] **No standalone ROI section.** ROI framing lives inside Investment (1-2 lines). A late "ROI Frame" section repeats the investment math at the point of maximum reader fatigue — cut it, or if content is genuinely net-new, give it a visual treatment not yet used in the doc. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **No tile-grid fatigue.** The same card/tile treatment must not appear in section after section. By the third grid the reader stops seeing them. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **No three consecutive prose-dominant sections.** Exec Summary + Challenge + Solution as back-to-back text pages loses the reader. Move Proof of Results up (after Exec Summary is valid) or make Challenge/Solution more visual. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Standard section titles, one label per heading.** Use Executive summary / The problem / What we propose / The business case / Proof / Implementation. No casual or salesy titles, and no mono eyebrow that repeats the title directly above it. *(2026-07-08, Corient proposal)*
- [ ] **No inside-baseball on the cover.** No Stage chip or deal-process metadata; no Confidential stamp unless the operator asks. This goes to the customer. *(2026-07-08, Corient proposal)*
- [ ] **Seller-specific detail uses a LITERAL prominent placeholder.** Pricing, rollout timing, negotiated terms get a large centered "Your input goes here / ( Add your ___ )" panel, never a fabricated number/date and never a subtle note the reader can miss. The doc openly hands back the spots where the seller's judgment beats a generated guess. *(2026-07-08, Corient proposal)*

## Validated Formats — Protect These

- [ ] **"Solves for:" tags on capability cards stay.** Explicitly praised — the pain-mapping tag is the load-bearing element of each card. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Visual implementation timeline stays.** Called "EXCELLENT" — the timeline visual is required, not optional. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **"What Teams Are Seeing" proof section format stays.** The most-loved section — customer results with metrics. Candidate for early placement when the front half runs text-heavy. *(2026-07-01, Marcus & Millichap proposal)*
- [ ] **Side-by-side proof cards align their bands.** Header, body, numeric-metric row, and quote line up across adjacent cards (CSS subgrid or fixed bands), with a parallel metric count so the number row reads as one aligned strip. *(2026-07-08, Corient proposal)*

---

## Adding new items

When you find a new issue during testing:

```markdown
- [ ] **Short description of the check.** What to look for and why it matters. *(YYYY-MM-DD, test case)*
```

Put it under the most relevant section. If no section fits, add a new one.
