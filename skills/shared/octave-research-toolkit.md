# Octave research toolkit

Shared reference for the Octave document and deck skills: how to choose between list and search tools, how to ground follow-up assets in what actually happened, the tool tables common to every skill, and the standard error-handling responses. Skill-specific tool tables (e.g. competitive filters, deal-outcome extraction types) live in each skill's own `references/tool-reference.md`.

## List vs Search: when to use which

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (slim rows: oId, name, description) | You want a quick inventory: "show me all our personas" |
| `list_entities({ entityType, includeDetails: true })` | Fetch entities with full data (paginated) | You need the actual content: "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question: "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

## Follow-up assets: ground them in what actually happened

If the asset follows a previous interaction with the account (demo, discovery call, QBR, deal review, renewal), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })`: surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { companyDomains: ["<domain>"] } })`: deal stage changes, meetings held, emails sent, shows the journey so far
- `get_event_detail({ eventOId })`: deep dive on specific events (e.g., the discovery call, the demo) to pull exact context

This turns a generic "here's our product" asset into "here's what we heard from you, and here's how we're addressing it," much more compelling for the audience.

## Common tool tables

### Research & enrichment

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always: industry, size, tech stack, funding, signals |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target or recipient |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Map stakeholders or the broader buying committee |
| Companies by criteria | `find_company({ ... })` | Find companies matching criteria |
| ICP fit (company) | `qualify_company({ companyDomain })` | Segment match, fit score, and the fit reasons that answer "why them" |
| ICP fit (person) | `qualify_person({ person: { ... } })` | Persona match and individual fit |

> **Reading `qualify_company` scores:** show the composite score *and* the breakdown. It returns sub-scores (product fit vs segment fit), and the composite can mislead: an account can be a strong *product* fit yet score low because it's out of the segment definition by size or model (too large, or B2C). Say which: "out-of-segment-by-size, strong product fit" reads very differently from "bad fit." Don't bury a strong product-fit signal under a low composite; if the account is out-of-segment but strategically worth pursuing, frame the wedge rather than just flashing a red number.

### Motions & Motion ICP narrative

| What you need | Tool | When to use |
|---------------|------|-------------|
| All Motions | `list_motions()` | Find the Motion(s) covering this offering / motion type |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` | Default + Custom Motion Playbooks (Thematic / Milestone / Account / Competitive) under a Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full Motion Playbook narrative content |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | The persona × segment cells under a Motion: pick the cell that matches the audience |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full per-cell narrative: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, plus Learning Loop learnings |

> **Value props** come from the Motion ICP cell narrative (*Benefits and impacts*, outcomes, not features). Do **not** use `list_value_props` (deprecated; reads old playbooks).

### Proof & social proof

| What you need | Tool | When to use |
|---------------|------|-------------|
| All proof points | `list_entities({ entityType: "proof_point" })` | Metrics, quotes, logos with full data |
| All references | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Proof by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | Proof *about* a specific topic, industry, or use case |
| Uploaded case studies | `search_resources({ query: "<topic> case study" })` | Existing case study docs or assets |

### Competitive context

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor scan | `list_entities({ entityType: "competitor" })` | Who's in the landscape |
| Competitor deep dive | `get_entity({ oId })` | Full strengths, weaknesses, positioning |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["competitor"] })` | Messaging angles when a competitor is in the deal |
| Competitive Motion Playbook | `list_motion_playbooks({ motionOId })` filtered by `narrativeType === "COMPETITIVE"` + `get_motion_playbook` | A dedicated competitive narrative layered on the Motion |

### Intelligence & signals

| What you need | Tool | When to use |
|---------------|------|-------------|
| Recent findings | `list_findings({ query: "<company or topic>", startDate: "<90 days ago>" })` | Conversation-based insights from calls |
| Deal events | `list_events({ filters: { companyDomains: ["<domain>"] } })` | Deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific past interaction |
| Synthesized prep | `generate_call_prep({ companyDomain })` | A single comprehensive brief to work from (verify its claims) |

### Verbatim call evidence: quotes, not paraphrases

`list_findings` returns the pipeline's *extracted* insights — paraphrased, classified, aggregable, best for trends and counts ("how many objections about pricing this quarter"). When you need the raw conversation instead — an exact quote, a receipt, "what did they actually say" — reach for these two:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Verbatim quotes on any topic | `search_call_transcripts({ query })` | Semantic + keyword search over indexed call transcripts. Returns speaker-attributed moments grouped per call, with `recordingUrl` + `startSec` for jump-to-moment citations, and live-hydrated linked CRM opportunities (current `stageCategory`) |
| Quotes by deal outcome | `search_call_transcripts({ query, dealOutcome: "WON" \| "LOST" \| "OPEN" })` | "Objection quotes on deals we won vs. lost" — outcome resolved live from CRM, not a stale snapshot |
| What a specific persona says | `search_call_transcripts({ attributedPersonaOIds: [...] })` | "What do CTOs or CISOs actually say" — moments spoken by contacts classified into ANY of those personas (OR across the array, one call) |
| What a specific segment says | `search_call_transcripts({ attributedSegmentOIds: [...] })` | "Quotes from within a market segment" — calls whose company is classified into any of those segments, resolved live from company classifications |
| Customer voice vs. rep talk track | `search_call_transcripts({ speakerSide: "external" \| "internal" })` | Isolate the buyer's own words from what the rep pitched |
| Moments about a library entity | `search_call_transcripts({ entityOId })` | Moments *about* a persona, competitor, or use case via pipeline finding-links |
| Exact phrase inside the quote | `search_call_transcripts({ query, contentFilter: { momentPhrases: ["..."] } })` | The returned quote itself must literally contain one of these phrases (case-insensitive, OR across the list) |
| Objections raised in a specific context | `search_call_transcripts({ query: "objections raised", contentFilter: { callPhrases: ["Loops"] } })` | "What objections came up when we talked about Loops" — the CALL must mention the phrase anywhere; the objection quote itself doesn't have to. `excludeCallPhrases` works the same way in reverse, dropping calls that mention a phrase |
| Best evidence for one entity | `get_entity_evidence({ entityOId, angle? })` | The entity-anchored version of the above: best verbatim quotes evidencing a single persona, competitor, objection, use case, or proof point. Prefers pipeline-linked moments (`linkFiltered: true`), falls back to semantic search on the entity name |

**How these relate to the tools above:**
- `list_findings` = the pipeline's extracted, paraphrased insight — best for trends and counts
- `search_call_transcripts` = the raw verbatim conversation the findings came from — best for quotes, receipts, exact customer language, and topics extractors never captured
- `get_entity_evidence` = the entity-anchored composition of both — "prove this library entity with customers' actual words," ideal for backing a battlecard claim or persona pain point
- `get_event_detail` is still the deep dive on one *known* event; `search_call_transcripts` is how you find the moment across all calls in the first place (each returned moment carries an `eventOId` to chain into `get_event_detail`)
- Recording links + `startSec` let generated collateral cite the exact moment ("jump to 12:34")
- Pass `originalQuery` with the user's verbatim message when one exists (analytics only — same convention as `search_knowledge_base`/`ask_octave`)

Requires the `CAN_ANALYTICS` entitlement and indexed transcripts (backfilled per workspace) — if a workspace has no indexed calls yet, fall back to `list_findings`/`get_event_detail` and say so.

### Content generation, brand voice & style

| What you need | Tool | When to use |
|---------------|------|-------------|
| Positioning/messaging content | `generate_content({ instructions, customContext })` | Synthesize gathered library data into structured content |
| Email content | `generate_email({ ... })` | Follow-up email copy |
| Brand voices | `list_entities({ entityType: "brand_voice" })` | Available brand voices in the workspace |
| Writing styles | `list_writing_styles()` | Available writing styles in the workspace |

## Standard error handling

Use these standard responses; keep skill-specific errors in the skill.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> I can still work without Octave: you provide the content manually, and I'll handle structure, style, and HTML generation. (Skills that depend entirely on workspace data, like briefs and reports, should say so instead.)
>
> To reconnect: check your Octave MCP configuration and reconnect

**Company/Person Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with what we have: I'll use general positioning from your library
> 2. Try a different domain or email
> 3. Provide the details manually and I'll build the asset from that

**No Matching Motion ICP Cell:**
> No Motion ICP cell matches this audience profile directly.
>
> I'll use your general positioning. Afterwards, consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) on the relevant Motion for this angle: `/octave:library create motion-playbook`

**No Proof Points Available:**
> No proof points found matching this audience.
>
> Options:
> 1. Proceed without the proof section
> 2. Use your strongest general proof points
> 3. Provide customer results manually and I'll format them

**No Findings Data:**
> No conversation signals found for [company/person] in the recent period.
>
> This may be a new prospect with no prior interactions. I'll build from enrichment data and library content instead of past conversations. You can paste meeting notes or context manually if you have them.
