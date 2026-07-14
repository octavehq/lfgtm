# Octave research toolkit

Shared reference for the Octave document and deck skills: how to choose between list and search tools, how to ground follow-up assets in what actually happened, the tool tables common to every skill, and the standard error-handling responses. Skill-specific tool tables (e.g. competitive filters, deal-outcome extraction types) live in each skill's own `references/tool-reference.md`.

## List vs Search — when to use which

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our personas" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

## Follow-up assets — ground them in what actually happened

If the asset follows a previous interaction with the account (demo, discovery call, QBR, deal review, renewal), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { companyDomains: ["<domain>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events (e.g., the discovery call, the demo) to pull exact context

This turns a generic "here's our product" asset into "here's what we heard from you, and here's how we're addressing it" — much more compelling for the audience.

## Common tool tables

### Research & enrichment

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always — industry, size, tech stack, funding, signals |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target or recipient |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Map stakeholders or the broader buying committee |
| Companies by criteria | `find_company({ ... })` | Find companies matching criteria |
| ICP fit (company) | `qualify_company({ companyDomain })` | Segment match, fit score, and the fit reasons that answer "why them" |
| ICP fit (person) | `qualify_person({ person: { ... } })` | Persona match and individual fit |

> **Reading `qualify_company` scores:** show the composite score *and* the breakdown. It returns sub-scores (product fit vs segment fit), and the composite can mislead — an account can be a strong *product* fit yet score low because it's out of the segment definition by size or model (too large, or B2C). Say which: "out-of-segment-by-size, strong product fit" reads very differently from "bad fit." Don't bury a strong product-fit signal under a low composite; if the account is out-of-segment but strategically worth pursuing, frame the wedge rather than just flashing a red number.

### Motions & Motion ICP narrative

| What you need | Tool | When to use |
|---------------|------|-------------|
| All Motions | `list_motions()` | Find the Motion(s) covering this offering / motion type |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` | Default + Custom Motion Playbooks (Thematic / Milestone / Account / Competitive) under a Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full Motion Playbook narrative content |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | The persona × segment cells under a Motion — pick the cell that matches the audience |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full per-cell narrative: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References — plus Learning Loop learnings |

> **Value props** come from the Motion ICP cell narrative (*Benefits and impacts* — outcomes, not features). Do **not** use `list_value_props` (deprecated; reads old playbooks).

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
> I can still work without Octave — you provide the content manually, and I'll handle structure, style, and HTML generation. (Skills that depend entirely on workspace data — briefs, reports — should say so instead.)
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company/Person Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with what we have — I'll use general positioning from your library
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
> This may be a new prospect with no prior interactions. I'll build from enrichment data and library content instead of past conversations — you can paste meeting notes or context manually if you have them.
