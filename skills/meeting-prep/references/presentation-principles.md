# Presentation Principles

Rules for generating output documents. Any skill that produces customer-facing or seller-facing HTML should follow these.

## The Rules

### 1. Every data point gets a label
No orphan values. "$500,000" is meaningless; "Deal Value: $500,000" is information. Every number, date, name, or metric must be accompanied by a label that tells the reader what it is.

### 2. No internal tool terminology
No function names (`enrich_company`, `ask_graph`), no version numbers (`v2`), no stream identifiers (`Stream B`), no tool inventories ("Sources: Octave enrichment, qualification engine"). The reader doesn't care what built this. The output should read as if a human analyst wrote it.

### 3. No repeating data across sections
If deal stats appear in a labeled snapshot, don't also dump them in a subtitle or in prose. One canonical location per data point. When you need to reference data that lives elsewhere, point to it — don't duplicate it.

### 4. Every section earns its keep
If you can't answer "how does this help me in the call?" — cut it. No sections exist for comprehensiveness or to show off capability. An empty section is worse than no section.

### 5. Every section gets a one-line intro
Before presenting content, explain what this section is and why it's here. One sentence at the top of each section that tells the reader what they're looking at and how to use it.

### 6. Distinguish confirmed vs hypothesized
Pain from a prior call is different from pain we're guessing at. A person on the invite is different from a role we think exists. Tag the difference explicitly:
- **Confirmed** — sourced from CRM data, call transcripts, or direct input
- **Hypothesized** — inferred from enrichment, persona patterns, or industry norms

### 7. No walls of text
Scannable over readable. Bullets over paragraphs. Grids over prose. If a section can't be scanned in 10 seconds, restructure it. Three short bullets beat one long paragraph every time.

### 8. Sections connect logically
Questions should map to beliefs or pains. Talk tracks should serve specific goals. Nothing exists in isolation. If a piece of content doesn't connect to something else in the document, it probably doesn't belong.

### 9. Outcome-driven, not process-driven
Meeting goals = what to leave having accomplished, not a minute-by-minute timeline. Focus on exit criteria ("leave with a confirmed next step and a technical champion identified") not process steps ("spend 5 minutes on rapport").

### 10. Lean over comprehensive
6 sharp questions beat 12 comprehensive ones. Every item must be non-obvious and specific to this deal. Cut anything that amounts to "do your job" — generic advice like "build rapport" or "ask good questions" wastes space.

### 11. The header answers three questions
1. What is this document?
2. Who is it about?
3. What's the context?

Not branding, not tool names, not raw metadata. The header is a frame that orients the reader in under 5 seconds.

### 12. Deal risks are not customer pains
Internal deal health (single-threaded, low activity, stalled stage) belongs in deal context, not in "their pain." The customer's pain is their problem. Deal risk is your problem. Keep them separate.
