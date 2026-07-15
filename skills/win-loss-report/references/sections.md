# Sections (Full Report)

Generate 4 sections in order. Every metric shows **both volume and rate** with an explicit axis label — "12 deals (34% of closed)" not just "34%." Weave Octave taxonomy (segments, personas, use cases, competitors) into every section — these aren't abstract statistics, they're grounded in the library's structure.

---

**Section 1: Scorecard**

The numbers at a glance. Three tiers of information:

- **Headline metrics** — win rate ring + 3 large metric cards in a responsive grid:
  - Win rate ring (conic-gradient donut showing win percentage and "N of M deals")
  - Deals won (volume)
  - Deals lost (volume)
  - Calls analyzed (volume)

- **Segment breakdown** — mini horizontal bar chart with a prominent dimension label (`.dim-label` in accent color) above it reading "WIN RATE BY SEGMENT":
  - Each segment: name, deals won, deals lost, win rate
  - Sorted by deal volume (most active segment first)

- **Persona breakdown** — same format as segments, with dimension label "WIN RATE BY PERSONA":
  - Each persona: name, deals won, deals lost, win rate
  - Sorted by deal volume

- **Competitor breakdown** — horizontal stacked bar chart with dimension label "WIN RATE BY COMPETITOR":
  - Each competitor: green (wins) + red (losses) bars with both volume and win rate
  - Sorted by total deal volume

Every percentage must state what it's a percentage OF. "69% win rate (20 of 29 deals)" not just "69%."

---

**Section 2: Win Analysis <-> Loss Analysis (TABBED PAIR)**

Two tabs, same structure mirrored. The reader flips between tabs to see the contrast.

#### Win Tab

**Use Cases Where We Win**
- Cards for each use case, sorted by win rate (highest first)
- Each card shows:
  - Use case name
  - Volume: "N deals"
  - Win rate: "N% win rate (X of Y deals involving this use case)"
  - Top segment(s) where this use case wins
  - Top persona(s) driving these wins
  - 1-2 sentence evidence summary from conversations (what specifically made us win here)

**What to Keep Doing**
- 3-5 items in a compact action list (`.action-list` > `.action-item`), each showing a rank number, the pattern text, and a frequency line ("Appeared in N of M wins")
- Framing: "When we win, it's because..."
- Sorted by frequency/impact
- No evidence quotes or blockquotes — keep it compact

#### Loss Tab

**Use Cases Where We Lose**
- Same card format as win use cases
- Each card shows:
  - Use case name
  - Volume: "N deals"
  - Loss rate: "N% loss rate (X of Y deals involving this use case)"
  - Top segment(s) where this use case loses
  - Top persona(s) involved in these losses
  - 1-2 sentence evidence summary

**What to Stop Doing / Changes to Make**
- 3-5 items in a compact action list with rank number, the loss pattern, frequency, and the specific change to make (messaging, positioning, enablement, materials — not generic advice)
- Framing: "When we lose, it's because..." -> "To fix this..."
- No evidence quotes or blockquotes — keep it compact
- These absorb what would have been a standalone "Recommendations" section
- **Optional "Winnable if:" callout**: for a loss pattern or competitor grouping with a clear turning point, add one sharp line under the action item, "Winnable if: [X]." One sentence, no elaboration. Example: "Winnable if: we had addressed price earlier with a TCO story." Use it where the evidence supports a single clean condition, not on every item, it's a callout, not a new required field.

**No Decision / Stalled (optional pattern category)**
- Gate this on the data: only include if `list_events` loss records or CRM fields actually distinguish "lost to competitor" from "no decision / stalled" outcomes. If the workspace doesn't tag this distinction, skip the category entirely, do not infer or fabricate a no-decision bucket from competitor losses.
- When the data supports it, treat "No Decision" as its own pattern grouping inside the Loss tab (same use-case-card / action-list format as competitor losses), with volume + rate: "N deals (X% of losses)."
- Diagnose with engagement signals, each stated as volume + rate, not vibes:
  - Avg days between meetings (stalled deals vs. active deals)
  - Single-threaded vs. multi-threaded stakeholder count, wins vs. no-decision losses (e.g., "No-decision losses averaged 1.4 stakeholders engaged vs. 3.2 in wins")
  - Leadership change during the deal cycle (N deals, % of no-decision losses)
  - Budget reallocation / freeze signals (N deals, % of no-decision losses)
- These are diagnostics, not excuses. Pair with a "Winnable if:" callout where the evidence points to a specific save (e.g., "Winnable if: we'd multi-threaded past the single champion before Q4 budget lockup").

**Objections**
- Table format (`.obj-table`) sorted by loss correlation (highest loss rate first, not frequency)
- Columns: Objection | Loss Rate | Frequency | Who Raises It | Counter
- Each row shows:
  - The objection text
  - Loss rate when raised: "N%" (styled as loss-rate-badge)
  - Frequency: "N deals (X lost, Y won)"
  - Which personas/segments raise it most
  - Recommended counter / response
- The sorting by loss correlation is key — an objection raised in 5 deals with 80% loss rate matters more than one raised in 20 deals with 30% loss rate

---

**Section 3: Head-to-Head Deals (TABBED BY DIMENSION)**

Three tabs: **By Competitor** | **By Segment** | **By Persona**

Each tab shows aggregate win/loss patterns per grouping. For each grouping (e.g., "vs [Competitor A]" or "Enterprise"), show two side-by-side columns of common patterns:

```
+------------------------------------------------------------+
|  [Grouping label, e.g. "vs [Competitor A]" or "Enterprise"]         |
+--------------------------+---------------------------------+
|  WON 20 — Why we won     |  LOST 9 — Why we lost           |
|                          |                                 |
|  * Common pattern 1      |  * Common pattern 1             |
|  * Common pattern 2      |  * Common pattern 2             |
|  * Common pattern 3      |  * Common pattern 3             |
+--------------------------+---------------------------------+
```

The reader sees aggregate patterns — "why we won the 20 deals" and "why we lost the 9 deals" as bulleted lists of common themes, NOT individual deal stories. Each column header is a flex container (`.h2h-pattern-header`) with a badge ("WON N" or "LOST N") plus "Why we won" / "Why we lost" text.

The power of this section: same variable held constant (same competitor, or same segment, or same persona), so the reader sees what patterns differentiate wins from losses across all deals in that grouping.

If only wins or only losses exist for a grouping, show only the relevant column but note the gap: "No losses recorded against [X] — 4 wins in this period."

---

**Section 4: Data Sources**

What fed this report:
- Date range covered
- Total deals analyzed (won + lost + open if relevant)
- Total calls/conversations analyzed
- Total CRM records referenced
- Segments represented
- Competitors represented
- Personas represented
- Data completeness notes (e.g., "No conversation data for 12 deals — metrics only")
- Generation date and branding footer

---

#### Executive Summary Report (Condensed)

When the user selects "Executive Summary" depth, generate only:

1. Scorecard (Section 1) — headline metrics only, no segment/persona/competitor breakdowns
2. Win tab content — top 3 use cases, top 3 action items, no evidence quotes
3. Loss tab content — top 3 use cases, top 3 action items + changes, top 3 objections (table)
4. Data Sources (Section 4) — condensed

Single-column layout, no sidebar navigation, no tabs (flatten inline). Target a single printable page.
