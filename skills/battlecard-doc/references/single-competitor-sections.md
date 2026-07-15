# Deal Card -- Document Sections (v3)

The Deal Card is the default battlecard-doc output. It's deal-specific, handles 1-N competitors, and organized for a seller who needs a weapon before the next call.

## Structure

```
Topbar → Hero → Deal Situation → [Competitor Section(s)] → Our Pitch → Footer
```

## Competitor Count Handling

The document adapts to the number of named competitors:

- **1 competitor** -- No tab bar. Render the competitor section directly as a bordered panel (use `.tab-panel` styling but skip the `.tab-bar`).
- **2-3 competitors** -- Tabbed interface. One tab per competitor, ARIA-compliant with keyboard navigation.
- **4+ competitors** -- Tabs still work, but consider whether all competitors deserve equal depth. Lead with primary threats, condense secondary ones.

### Status Quo / Incumbent Handling

The buyer's current state (homegrown, legacy vendor, "doing nothing") is **context in Deal Situation**, not a competitor tab -- UNLESS:

- The buyer is genuinely undecided about moving (status quo IS the competition)
- The incumbent is also a named competitor being evaluated (e.g., already on Auth0 and evaluating alternatives)

When status quo deserves a tab, frame strengths as "Why they might stay" and weaknesses as "Why that breaks down."

When there is no incumbent (greenfield / new capability), the "Current State" sub-card should describe what they're doing without the capability and why that's no longer tenable.

---

**1. Topbar**
- Seller brand logo (left) + "Battle Card" label
- "prepared for [Account]" + account logo (right)
- Both logos as base64 data URIs (use `get_external_brand_logo` or scrape from website)

**2. Hero**
- Eyebrow: "Competitive Intelligence"
- Title: "[Account Name] Deal Card"
- Sub: One-sentence deal summary. Adapt framing:
  - Replacing incumbent: "[Company] replacing [X] -- [why]"
  - Greenfield: "[Company] building [capability] for the first time"
  - Undecided: "[Company] evaluating whether to modernize [X]"
- Metadata chips: each competitor, deal stage, key contacts

**3. Deal Situation** (canvas background section)

Break the deal context into scannable sub-cards using a 2-column grid. Each card has a bold label and concise content. No walls of text.

Sub-cards:
- **Company Profile** -- Who they are, business type, size, what they care about. One paragraph max.
- **Current State** -- What they're running today, what's broken, pain points from the call. Use direct quotes where available. If greenfield, describe what they're doing without the capability.
- **Requirements** -- What they need. Bullet list of must-haves (technical and business).
- **Deal Logistics** -- Key contacts (name, title, role), timeline, procurement path, channel partner if any.
- **Competitive Landscape** -- Who's being evaluated, incumbent situation, primary vs secondary threats. Full-width card (spans both grid columns).

CSS: `.deal-grid` (2-column grid) of `.deal-card` elements. Each card has an `.eyebrow` label. Competitive Landscape card uses `style="grid-column:1/-1"` to span full width.

**4. Competitor Sections**

One panel per competitor. Tab bar if 2+, no tab bar if 1. Each panel contains the core sub-sections (a-e) plus one optional card (f) when the evidence supports it:

### a. Their Strengths → Our Counter (comparison grid)

Side-by-side grid. Left: "What they'll say." Right: "What you say back."

Each row is a `.cmp-row` with `.cmp-them` and `.cmp-us` cells. Typically 3 rows.

### b. Their Weaknesses → How We Pounce (comparison grid)

Same layout. Left: "Where they're exposed." Right: "Our move." Typically 3-4 rows.

### c. Proof (standalone)

Green-accented list. 1-3 entries. Each entry explains WHY the proof point matters for this deal, not just a name-drop.

### d. Win Rate (if data available)

CSS bar showing wins vs losses. Include trending context (direction + why).

### e. Watch-out (standalone)

Amber callout. Bold lead-in is a **named risk pattern**, not a quoted prospect line, e.g. `<strong>They anchor on price.</strong>`, `<strong>Incumbent inertia.</strong>`, `<strong>They equate scale with quality.</strong>`. The pattern names the situation the deal is walking into, never what the prospect said.

Structure after the lead-in:
- **You'll hear:** the signal that this objection is coming -- the phrasing, question, or behavior that tips you off, paraphrased as a pattern (e.g. "budget owner starts comparing per-seat cost before scoping requirements"), not a verbatim quote.
- **Response:** the counter-move, tied to this account's specific situation.
- **Proof:** the evidence that makes the counter-move credible here (a metric, a reference, a switch story) -- omit if none exists rather than inventing one.
- **Timing:** when to raise it (proactively, or only if asked).

### f. Trap Questions (optional, compact card)

Include when you have enough competitor-weakness intel to make the questions sharp. Skip if the objection/comparison content already covers the same ground and a trap-questions card would just repeat it.

A trap question is a discovery question that surfaces the competitor's weak spot **without naming them**. Unlike the rest of the battlecard, which is talking points to adapt in your own words, trap questions are meant to be asked **near-verbatim** -- the exact phrasing is doing the work of steering the conversation without sounding like an attack.

Each entry:
- **The question** -- asked near-verbatim, framed as ordinary discovery, no competitor name.
- **Why this works** -- what it exposes and why the competitor's answer (or non-answer) reveals the gap.
- **If they say X, follow up with Y** -- the likely response and the sharper follow-up that presses on the exposed weakness.

2-4 questions. Sequence them so the earlier ones establish a criterion as important before the later ones expose the gap against it.

### Content Density (critical)

Each comparison grid cell should be **2-3 sentences**. The target:

- **"Them" cell**: Bold lead-in stating the point + 1 sentence of context on why it lands with buyers.
- **"Us" cell**: Bold lead-in with the counter-point + 1 sentence tying it to this account's needs.

Bold lead-ins are **declarative statements, not quotes**. Write `<strong>Unlimited isn't free if your engineers are the runtime.</strong>` NOT `<strong>"Unlimited isn't free..."</strong>`.

Proof entries: 1-2 sentences explaining relevance to this deal. Watch-outs: named risk pattern + "You'll hear" signal + response + proof, never a quoted prospect line as the lead-in. Trap questions are the one exception to "no verbatim phrasing" -- ask them close to as written.

**5. Our Pitch** (canvas background section)

Three layers, each with a `.p-sub` label, plus one optional layer:

### a. Unified -- works against any competitor

3-4 pitch cards. The platform narrative that transcends any single matchup:
- Core product differentiation (what changes the operating model)
- Migration / speed-to-value story
- Future-proofing / vision (where the category is going)
- Credibility / proof at scale

### b. Sharpen vs [Competitor 1]

1-2 pitch cards. The specific offensive angle. Should feel like NEW points, not restated defense from the competitor tab. Focus on:
- The single most damaging framing against this competitor
- The wedge issue that moves the conversation

### c. Sharpen vs [Competitor 2]

Same structure. One sub-section per competitor.

If only one competitor, you can fold "sharpen" points into unified or keep them separate -- use judgment on whether the separation adds clarity.

Each card: declarative heading + 1-2 sentence supporting argument. No quotes.

### d. Landmines to Plant (optional)

Include when the deal is early enough that evaluation criteria are still forming. Skip once the deal is already in a formal eval with criteria locked, or for accounts where this would just restate the unified pitch.

A short list (3-5) of evaluation criteria to raise early, before the competitor gets a chance to frame the eval on their own terms. Each is a criterion that sounds like neutral, reasonable due diligence but structurally favors us. One line each: the criterion to plant + why it tilts the eval in our favor.

This section is **offense**. The competitor sections are **defense**.

**6. Footer**
- Seller brand logo (subtle, reduced opacity) + "Generated by Octave"
- Date + "Internal use only"

---

## Key Design Principles

1. **No ceremony** -- Skip outline approval, style picker, competitor picker prompts. Just output the card.
2. **Side-by-side is the default** for competitive content. Every claim about a competitor has our response alongside it.
3. **Deal Situation earns its space** by being scannable sub-cards, not prose.
4. **Proof is distributed** per-competitor, not in a generic list.
5. **Watch-outs are honest** -- buried risks lose trust. Surface them with counter-moves.
6. **Our Pitch has layers** -- unified narrative first, then sharpened per-competitor angles, then optional landmines if the deal is still early.
7. **No quotes in bold lead-ins** -- declarative statements, not quotable phrases.
8. **Objections describe the risk, they don't quote the prospect** -- lead with a named risk pattern ("They anchor on price"), not a verbatim line. Trap questions are the one deliberate exception: ask those near-verbatim.
9. **2-3 sentences per cell** -- enough to use in conversation, not a wall of text.
10. **Adapts to competitor count** -- 1 = no tabs, 2+ = tabs, status quo = context unless genuinely a competitor.
