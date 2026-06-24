# Presentation principles (output formatting)

Generation-time rules for any skill that produces a customer-facing or seller-facing document (deck, one-pager, microsite, battlecard, proposal, brief, meeting-prep, etc.). These are the **write** standard; [`asset-review.md`](asset-review.md) is the **review** standard that QAs the rendered result. Apply both.

## The rules

### 1. Every data point gets a label
No orphan values. "$500,000" is meaningless; "Deal value: $500,000" is information. Every number, date, name, or metric is accompanied by a label that says what it is.

### 2. No internal tool terminology in the output
No function names (`enrich_company`, `ask_graph`), version numbers (`v2`), stream identifiers (`Stream B`), or tool inventories ("Sources: Octave enrichment, qualification engine"). The reader doesn't care what built it. The output reads as if a human analyst wrote it.

### 3. No repeating data across sections
One canonical location per data point. If deal stats live in a labeled snapshot, don't also dump them in a subtitle or in prose. When a later section needs data that lives elsewhere, point to it — don't restate it.

### 4. Every section earns its keep
If you can't answer "how does this help me?" — cut it. No sections for comprehensiveness or to show off capability. An empty section ("No findings in last 90 days") is worse than no section — omit it silently.

### 5. Every section gets a one-line intro
Before the content, one sentence on what this section is and how to use it.

### 6. Distinguish confirmed from hypothesized
Pain from a prior call is different from pain we're guessing at; a person on the invite is different from a role we think exists. Tag the difference explicitly:
- **Confirmed** — sourced from CRM data, call transcripts/findings, verified enrichment, or direct user input.
- **Hypothesized** — inferred from enrichment, persona patterns, or industry norms.

Verify before you assert: a named person/title traces to a real result (`resolve_profile_from_email`, `enrich_person`, `find_person`); never state speculation as fact (no "Likely: Glean" when you mean "Unknown — potential: Glean"). This is the generation-time half of `asset-review.md` → Groundedness & verification.

**Link cited entities back to source — internal/seller-facing assets ONLY.** In an internal doc (meeting-prep, brief, battlecard, deal coaching), every cited Octave library entity (proof point, reference, persona, competitor, objection, use case, segment, Motion ICP cell) can link to **`https://app.octavehq.com/entity/{oId}`** — a naked deep link (the `oId` is in every tool result) that resolves to the reader's own workspace, so the reader is one click from the source. (Supported oId prefixes: `uu, pp, pe, cp, ao, oj, bq, sg, px, sv, re, sc, pb`.) **Never put these links in a customer-facing asset** (deck, one-pager, microsite, proposal) — the customer has no Octave workspace, the link is broken for them, and it leaks internal tooling (see rule 2). If unsure whether the asset is internal or customer-facing, leave the links out.

### 7. No walls of text
Scannable over readable. Bullets and grids over paragraphs. If a section can't be scanned in ~10 seconds, restructure it. Three short bullets beat one long paragraph.

### 8. Sections connect logically
Questions map to the pains or beliefs they probe; talk tracks serve specific goals. If a piece of content doesn't connect to anything else, it probably doesn't belong. Prefer self-contained cards (a pain with its own probe + discovery questions) over scattering related content across sections.

### 9. Outcome-driven, not process-driven
Goals = what to leave having accomplished (exit criteria: "leave with a confirmed next step and a technical champion identified"), not a minute-by-minute timeline ("0-5 min rapport, 5-20 discovery"). Never ship a phase-by-phase clock.

### 10. Lean over comprehensive
6 sharp items beat 12 comprehensive ones. Every item must be non-obvious and specific to this account. Cut anything that amounts to "do your job" — generic advice ("build rapport", "ask good questions", "multi-thread") wastes space.

### 11. The header answers three questions
What is this document? Who is it about? What's the context? Not branding, not tool names, not raw metadata — a frame that orients the reader in under 5 seconds.

### 12. Keep their pain separate from your deal risk
The customer's pain is *their* problem (their world, in their words). Internal deal health (single-threaded, low activity, stalled stage) is *your* problem — it belongs in deal context/snapshot, never in "their pain."

## Two phrasing traps worth calling out
- **Objections describe the risk, they don't quote the prospect.** Write `They position this as overlap with existing enterprise search`, not `"We already use Glean for this"`. Never put words in the prospect's mouth.
- **Mark speculation as speculation, everywhere.** "Competition: Datadog" only when intel confirms it; otherwise "Unknown — potential: Datadog." Applies to every field, not just competition.

## Links and chrome
- **Every link opens in a new tab.** Give every `<a href>` in a generated asset `target="_blank" rel="noopener noreferrer"`. The reader is working from the doc — entity deep-links, LinkedIn, sources, citations should never navigate them away from it.
- **Style scrollbars to the theme.** A default OS scrollbar against a styled (especially dark) surface reads as broken. Every scrollable region and the page itself gets a themed, thin scrollbar — `scrollbar-width: thin; scrollbar-color: var(--border) transparent;` plus the `::-webkit-scrollbar` equivalent (~8-10px, rounded `--border` thumb, transparent track). Never ship a bare default scrollbar.

## Look like the brand, not like a template
The output should read as a crafted artifact in the sender's brand, not a generic doc filled into a fixed scaffold. When a brand kit exists (`~/.octave/brands/<slug>/`), inline its real logo and map its tokens to the asset's CSS variables so the palette, type, and logo are the brand's — don't fall back to a default preset when a kit is available. Reference scaffolds are **structure and component patterns to adapt**, not a literal stylesheet to reproduce verbatim; vary layout and styling to fit the brand and the occasion. A reader should be able to tell at a glance whose document this is.
