# Format: Slide Deck

Paginated HTML slide presentations designed for screen sharing, projection, or async viewing. One idea per slide, progressive disclosure through slide sequence.

**Skills that produce this format:** deck, coaching (deck mode)

These principles supplement the universal visual rules in `presentation-principles.md` (one directory up). The universal principles are the floor; these add format-specific requirements.

**Floor vs. craft.** Core slide rules (one idea per slide, 16:9 viewport, action titles, consistent formatting) always apply. Others (source notes, appendix, section dividers) are craft standards: use them when the deck naturally supports them. A 5-slide internal brief doesn't need section dividers or an appendix. Don't add structure to check a box.

## Principles

1. **One idea per slide.** If a slide requires the viewer to process two separate concepts, split it into two slides. Slides are cheap. Cognitive overload is expensive.

2. **Fixed viewport, no scrolling.** Each slide fills the screen at 16:9 aspect ratio. Content must work without scrolling. Everything important is visible without interaction.

3. **Larger type baseline.** Slide text must be legible on a projector or in a video call thumbnail. Body text minimum ~1.2rem equivalent. Headlines significantly larger. If you'd squint at it on a shared screen, the text is too small.

4. **Action title on every slide.** The slide headline captures the key takeaway: it's a message, not a label. "Revenue grew 3x in Q2" not "Q2 Revenue." The audience should understand the point from the headline alone.

5. **Full-slide data when it matters.** When a chart or graph carries the argument, dedicate the entire slide to it. No competing text or side panels. Let the data command full attention, with the action title providing interpretation.

6. **Progressive disclosure through sequence.** The slide order IS the narrative. Build the argument one slide at a time. Each slide is a stepping stone: the reader should feel pulled forward.

7. **Visual anchor per slide.** Every slide has one dominant visual element (a stat, a chart, a diagram, a quote) that the eye goes to first. If everything is the same size and weight, the viewer doesn't know where to start.

8. **Section dividers set context.** Title slides between major sections orient the viewer in the narrative. "Here's where we are in the story." They create breathing room and signal topic shifts.

9. **Slide navigation.** Arrow keys, click, and swipe all advance slides. Current slide indicator visible. Keyboard-driven, no mouse required.

10. **Transitions are functional, not decorative.** Slide transitions signal relationships: a fade means continuation, a cut means new topic. Don't use multiple different transition styles: pick one and use it consistently.

11. **Consistent formatting across all slides.** Same fonts, colors, and layout patterns throughout. The audience should never notice the design, only the message. Inconsistency communicates disorganization.

12. **Logical structure is independent of visual layout.** A slide can use a waterfall chart, a two-column split, a full-page graphic, or bullet points, and still follow the three-layer hierarchy (main point in the title, key arguments visible, evidence supporting each argument). Don't assume good structure requires a specific visual format. Test by asking: can I map every element on this slide to the main point?

13. **Surface variety across the deck.** A deck where every slide has the same background color feels monotone regardless of the content. Title slides, section dividers, and CTA/closing slides should have a visually distinct surface (a gradient wash, a glow orb, or an accent color shift) that separates them from content slides. Content slides between dividers can share a surface, but the overall sequence should have visible chapter breaks as the viewer navigates.

14. **Depth on components.** Cards, metric callouts, and content containers must have visible depth: box shadows, accent borders, or both. A card with only a thin border on the same background color doesn't register as a card. The component should visually lift off its surface. Accent bars (thin gradient lines at top or left of a container) add visual weight and signal importance.

15. **Source notes on data slides.** When a slide cites specific numbers, include a small source note (bottom of slide, muted text). This adds credibility and lets the viewer verify. No source note needed for obvious context or qualitative observations, only for specific data claims.

16. **Appendix holds the depth (when needed).** If the deck has supporting data, methodology details, or backup analysis that would clutter the main narrative, move it to an appendix section after the conclusion. The main deck should be lean enough to present in a meeting; the appendix absorbs the "but what about…?" questions. Not every deck needs one: short, focused decks can stand on their own.

17. **Consistent section navigation.** When a deck is divided into numbered or color-coded sections, every slide within a section should display the same section nav element: the section number and label in the section's color. This anchors the viewer's position in the narrative without requiring them to remember which section they're in. Section nav should be large enough to scan at projection distance but visually subordinate to the slide's own headline.

18. **Consistent deep-dive template.** When multiple slides within a section follow the same pattern (e.g., deep dives into individual companies, accounts, or products), they must use an identical layout template. Same content areas, same sidebar placement, same visual treatments. The viewer should recognize the pattern and focus on content differences, not adapt to a new layout on each slide.

19. **Section identity bar.** A thin vertical bar (4-8px) on the left edge of every slide within a section, in the section's color, provides a persistent visual anchor. This reinforces which section the viewer is in without competing with the slide content.

20. **Deck-level section navigation.** When a deck has two or more major sections, a persistent top bar on every slide (except title/closing) shows all section labels with the current section highlighted. This gives the viewer a map of the full presentation. The bar should be subtle (thin border-bottom, small type) so it doesn't compete with slide content.

21. **Entity names as focal headings in deep dives.** When deep-dive slides focus on specific entities (companies, accounts, products), the entity name is the visual focal point: large, bold, the first thing the eye lands on. The action-title claim lives as a subtitle below. This exception to the standard action-title rule applies when the entity identification IS the primary purpose. The claim subtitle satisfies the "every slide has a takeaway" requirement.

22. **Brand assets, not approximations.** When building a branded deck, use actual brand assets (logo files, font families, color values from a brand kit). Never create placeholder logos or approximate wordmarks. If brand assets aren't available, ask the user or run the brand component capture first.

23. **Fill the canvas.** A slide with content crammed into the top third and empty space below communicates nothing: it communicates you didn't design it. Content elements (cards, grids, bullet lists, charts) should expand to fill the available vertical space on the slide. Use `justify-content:center` on the slide body, generous padding, and large enough font sizing so the composition uses the full 1920×1080 canvas. If there's visible dead space, the type is too small or the layout needs restructuring. The slide should feel full at a glance, not like a document fragment pasted onto a dark background.

    **Bad:** Three cards in a grid at 21px body text with 36px padding, content filling the top 40% of the slide, giant dark void below.
    **Good:** Same three cards at 26px body text with 48px padding, slide body vertically centered (`justify-content:center`), content occupies the visual center of the canvas.

24. **No label tags or pills on content slides.** Small uppercase labels above headlines ("BIGGEST OPPORTUNITY", "KEY INSIGHT") are a crutch. They add visual noise without adding information: the headline itself should carry the point. Only use pills/tags on the title slide when the tag genuinely orients (e.g., a product name the audience doesn't know). Never on content slides.

    **Bad:** `<span class="label">Biggest opportunity</span>` above "Almost nobody is using the intelligence layer yet"
    **Good:** "Biggest areas of opportunity" as the headline. The label was carrying the message; make the headline carry it instead.

25. **Type scale for projection distance.** Headlines, body text, and bullets must be sized for readability when projected or in a video call thumbnail. This means starting significantly larger than web defaults. Minimum sizes on the 1920×1080 canvas:

    | Element | Minimum | Recommended |
    |---------|---------|-------------|
    | h1 (title slide) | 80px | 96–104px |
    | h2 (slide headline) | 44px | 48–56px |
    | h3 (card heading) | 28px | 30–34px |
    | body (card/paragraph) | 22px | 24–26px |
    | bullet list items | 26px | 28–30px |
    | entity name (deep dive) | 80px | 88–96px |
    | entity subtitle | 26px | 28–32px |
    | nav labels | 18px | 20px |

    **Bad:** Card headings at 22px, body at 18px, bullet items at 20px: looks like a document, not a slide.
    **Good:** Card headings at 34px, body at 26px, bullet items at 30px: reads clearly at projection distance.

26. **Subtitle is a message, not a description format.** Deep-dive slide subtitles should carry meaning. "Why they're stuck" tells the audience what to expect. "Never got past setup into actual workflows" is a narrative claim. Both work. "Sendoso overview" is dead weight.

    **Bad:** `<p class="csub">Never got past setup into actual workflows</p>`. This was the v1 approach: narrative claims as subtitles on deep dives. Fine in isolation, but when the user wants a consistent format, it creates inconsistency across slides because each subtitle is a different kind of statement.
    **Good:** `<p class="csub" style="color: var(--arch-bad);">Why they're stuck</p>`. Consistent across all deep dives in the section. The bullets below carry the specifics.

27. **Present tense for current state.** Slides describing how customers currently use the product should be in present tense. Past tense ("was," "had," "couldn't") implies the situation is over. If the account is still a customer, describe their current state.

    **Bad:** "The gap between the product and the operator was too wide"
    **Good:** "Used in a limited scope by operators without broad org influence"

28. **Deep-dive bullet format over prose sidebars.** When showing per-account details, bullet lists beat two-column layouts with prose paragraphs. Bullets are scannable at projection speed. Prose requires reading. The audience processes "Fragmented stack: haven't embraced Octave as the source of truth" faster than a paragraph making the same point in three sentences.

    **Bad:** Left column with two body-lg paragraphs + right sidebar with a heading, paragraph, and stat callout. Dense, requires reading, can't be processed during a 15-second slide view.
    **Good:** Customer name (96px) → colored subtitle "Why they're stuck" → 4-5 bullet items at 30px with section-colored dots. Scannable in 5 seconds.

29. **No text-on-visual collisions (slide application).** General principle 9h applies. On the 1920×1080 canvas, use absolute coordinates to verify clearances between overlay text and SVG/diagram elements. A title at `top:340px; left:120px` must not sit on top of a label at approximately the same coordinates.

    **Bad:** "Become the kraken" at `bottom:100px; left:120px` overlapping the "Full Team Adoption" label at y≈805px on the same side.
    **Good:** Title moved to `top:80px; left:120px`, clear of all tentacle endpoint labels. Labels repositioned to avoid the title zone.

30. **Staircase and archetype visuals: names over descriptions.** When showing a staircase, maturity model, or archetype comparison, each tier gets a big name, not a name plus subtitle plus description plus count. The visual hierarchy IS the argument (short bar = bad, tall bar = good). Adding text inside each tier dilutes the visual impact. Save the descriptions for the overview slides that follow.

    **Bad:** Each tier has: uppercase label ("THE BAD") + name ("Stuck") + description ("Can't drive change. Never gets past setup.") + account count ("2 accounts"). Four layers of text competing inside a gradient box.
    **Good:** Each tier has: a ghost number ("01") + one name ("Stuck" at 36px bold). The overview slide that follows carries the description. The staircase is visual impact, not an information dump.

31. **Navigation elements scale with the slide, not the browser.** Top nav bars, section labels, and archetype indicators are part of the slide: they must be sized for the 1920×1080 canvas, not for a browser chrome bar. Nav text below 18px disappears at projection distance. Letter-spacing below 3px makes uppercase labels feel cramped.

    **Bad:** Top nav items at 13px with 2px letter-spacing, section labels at 14px, visible only when you lean in.
    **Good:** Top nav items at 20px with 5px letter-spacing, section numbers at 52px light weight, section labels at 20px with 5px letter-spacing. Readable from the back of a room.

32. **Vertical alignment (slide application).** General principle 9f applies. On the 1920×1080 canvas, define a `.slide-body` with a fixed `top` value (e.g., 172px) and reuse it across all slide types in a section. Headlines and entity names should start at the same y-position so flipping between slides feels stable.

    **Bad:** Overview slide headline starts at y=172px, deep-dive entity name starts at y=200px, next deep dive starts at y=150px. Content bounces as you navigate.
    **Good:** All slides in a section use `.slide-body { top: 172px; left: 120px; right: 120px; }`. Headlines and entity names start at the same vertical position.

33. **Consistent horizontal margins (slide application).** General principle 9e applies. On the 1920×1080 canvas, 120px left/right is the standard margin. Top nav, section labels, slide body, cards, and bullets all align to `left: 120px` / `padding: 0 120px`. Internal elements are inset by their own padding, but outer containers share one edge.

    **Bad:** Top nav at `padding: 0 80px`, section label at `left: 100px`, slide body at `left: 120px`, bullets at `left: 140px`. Four different left edges.
    **Good:** Top nav at `padding: 0 120px`, section label at `left: 120px`, slide body at `left: 120px`. Everything snaps to the same 120px margin.

34. **Structural whitespace (slide application).** General principle 9g applies. On the 1920×1080 canvas, use a gap scale of 24px / 32px / 36px / 48px. Assign gaps deliberately: section nav to headline, headline to cards, between cards. Combine with `justify-content:center` on the slide body so content occupies the visual center with no leftover voids.

    **Bad:** 12px between section nav and headline, 28px between headline and cards, then 400px of empty space below the cards.
    **Good:** Section nav to headline: 36px. Headline to cards: 36px (flex gap). Cards fill the remaining space via vertical centering.

35. **Nav hierarchy: deck nav > section nav > content.** A slide with both deck-level navigation (top bar showing sections A/B) and section-level navigation (archetype number + label) has three tiers of information. They must be visually distinct and consistently positioned:
    - **Deck nav** (top bar): smallest type, full-width, fixed at the top edge, glass-morphism or border-bottom separation.
    - **Section nav** (archetype label): medium type, positioned just below deck nav, uses the section color.
    - **Content** (headline, cards, bullets): largest type, fills the remaining slide body.

    Each tier should be clearly separated by position and scale. If the section nav is the same size as the deck nav, or the headline is the same size as the section label, the hierarchy collapses.

    **Bad:** Deck nav at 13px, section label at 14px, headline at 36px. The top two tiers are indistinguishable; the eye skips them entirely.
    **Good:** Deck nav at 20px with letter-spacing, section number at 52px + label at 20px, headline at 52px. Three clearly distinct scales.

36. **Three font sizes max per slide (slide application).** General principle 9d applies. On slides, persistent nav elements (deck nav, section nav) that appear on every slide don't count toward the three: they're chrome. The slide's own content (headline, body, labels) should use at most three distinct sizes.

    **Bad:** Entity name at 80px, subtitle at 26px, bullet items at 24px, sidebar heading at 22px, sidebar body at 18px, stat number at 36px, stat label at 12px. Seven font sizes.
    **Good:** Entity name at 96px, subtitle at 32px, bullet items at 30px. Three sizes. Clear hierarchy: name → context → details.

---

## Review Checklist

Format-specific audit for slide deck presentations. Run alongside the universal presentation checklist.

- [ ] **One idea per slide.** No slide requires processing two unrelated concepts.
- [ ] **16:9 viewport.** Content fits without horizontal or vertical scroll at standard presentation aspect ratio.
- [ ] **Type legibility.** Body text >= 1.2rem equivalent. Headlines significantly larger. Nothing illegible at projection distance.
- [ ] **Action titles.** Every slide headline states a takeaway, not a topic label. Exception: entity deep-dive slides use the entity name as focal heading with a claim subtitle below.
- [ ] **Visual anchor.** Each slide has one dominant visual element the eye goes to first.
- [ ] **Slide navigation works.** Arrow keys advance/retreat. Click advances. Current position indicated.
- [ ] **Consistent formatting.** Same fonts, colors, layout patterns across all slides. No rogue slides with different styling.
- [ ] **Section dividers present (when deck has multiple major topics).** Major topic shifts have title/divider slides. Short decks with a single thread don't need them.
- [ ] **Section navigation consistent.** If the deck has sections, every slide within a section shows the same section nav (number + label in section color). Nav is visually subordinate to the slide headline.
- [ ] **Deep-dive template consistent.** If multiple slides follow the same pattern (entity deep dives), they use an identical layout template.
- [ ] **Section identity bar (where applicable).** Section slides have a thin vertical color bar on the left edge matching the section color.
- [ ] **Deck-level section nav (where applicable).** If the deck has multiple major sections, every non-title/closing slide has a persistent top bar showing all sections with the current one highlighted.
- [ ] **Brand assets used.** If a brand kit exists, actual logo files and brand fonts are used. No placeholder logos or approximate wordmarks.
- [ ] **Canvas filled.** No slide has content crammed into the top portion with large empty space below. Cards, grids, and lists expand to use the full vertical space. Slide body uses `justify-content:center`.
- [ ] **No stray label tags.** No small uppercase labels/pills above headlines on content slides. The headline carries the message.
- [ ] **Type scale meets minimums.** h1 ≥ 80px, h2 ≥ 44px, h3 ≥ 28px, body ≥ 22px, bullets ≥ 26px, entity names ≥ 80px. Check at 50% browser zoom to simulate projection.
- [ ] **Subtitle format consistent across deep dives.** All deep-dive slides in a section use the same subtitle pattern (e.g., "Why they're stuck" / "Why they're best in class"), not a mix of narrative claims and descriptions.
- [ ] **Present tense for current state.** Slides describing active accounts use present tense, not past tense.
- [ ] **Deep dives use bullet format.** Per-entity slides use scannable bullet lists, not prose paragraphs or two-column layouts with sidebars.
- [ ] **No text-on-visual collisions.** Overlay text (titles, subtitles) does not overlap labels, endpoints, or diagram elements in SVG/visual slides.
- [ ] **Archetype visuals are clean.** Staircase/maturity visuals have one name per tier, not name + subtitle + description + count stacked inside.
- [ ] **Nav elements sized for projection.** Top nav ≥ 18px, section numbers ≥ 44px, section labels ≥ 18px. Letter-spacing ≥ 3px on uppercase labels.
- [ ] **Vertical content alignment.** Headlines/entity names start at the same y-position across all slides in a section. No content jumping between slides.
- [ ] **Horizontal margins consistent.** All slide content (nav, section labels, headlines, cards, bullets) aligns to the same left margin (typically 120px). No ragged left edges.
- [ ] **Whitespace is intentional.** Gaps follow a consistent scale (24/32/36/48px). No unexplained voids larger than the next gap size up.
- [ ] **Nav hierarchy clear.** Deck nav, section nav, and content are three visually distinct tiers by size and position. No two tiers at the same scale.
- [ ] **Three font sizes max per slide.** Each slide uses at most three distinct font sizes. If you count more, consolidate: too many sizes creates visual noise.
- [ ] **Source notes (where applicable).** Slides citing specific quantitative data have a small source attribution. Not needed for qualitative observations or obvious context.
- [ ] **Print works.** Each slide renders as one page. No content lost or cropped.
