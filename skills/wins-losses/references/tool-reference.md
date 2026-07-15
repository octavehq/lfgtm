# Tool Reference

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need actual content — "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something notable and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept — "how do we position against price objections?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need CRM exports, uploaded deal data, or reference docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Call shapes for events and findings:**

- `list_events({ startDate, endDate, limit, filters: { eventTypes, companyDomains, competitors, segments, personas, outcomeFilters, sentiments, minDealAmount, maxDealAmount } })` — event-type and entity filters always go inside `filters`.
- `list_findings({ query, startDate, endDate, limit, eventFilters: { ...same filter fields... } })` — `query` is a **required** natural-language string; describe the kind of finding you want ("objections raised by prospects", "competitor mentions") in the query rather than expecting a type parameter.

---

## Core Deal Data (Always Required)

| What you need | Tool call | When to use |
|---------------|-----------|-------------|
| Won deals | `list_events({ startDate, endDate, filters: { eventTypes: ["DEAL_WON"] } })` | Always — core data |
| Lost deals | `list_events({ startDate, endDate, filters: { eventTypes: ["DEAL_LOST"] } })` | Always — core data |
| Pipeline context | `list_events({ startDate, endDate, filters: { eventTypes: ["OPPORTUNITY_CREATED"] } })` | When you need total pipeline for win rate calculation |
| Notable deal details | `get_event_detail({ eventOId })` | Deep dive on 3-5 notable wins and 3-5 notable losses |

---

## Conversation Intelligence (Findings)

| What you need | Tool call | When to use |
|---------------|-----------|-------------|
| Objections in won deals | `list_findings({ query: "objections and pushback raised by prospects", startDate, eventFilters: { outcomeFilters: ["WON"] } })` | Objections that were overcome |
| Objections in lost deals | `list_findings({ query: "objections and pushback raised by prospects", startDate, eventFilters: { outcomeFilters: ["LOST"] } })` | Objections that killed deals |
| Value props presented | `list_findings({ query: "value props presented and how prospects responded", startDate })` | What messaging worked vs didn't |
| Competitor mentions | `list_findings({ query: "competitors mentioned or compared against our offering", startDate })` | Competitive landscape in deals |
| Feature requests | `list_findings({ query: "feature requests and product gaps raised by prospects", startDate })` | Product gaps causing losses |
| Proof points cited | `list_findings({ query: "proof points and customer stories cited in conversations", startDate })` | Social proof effectiveness |

---

## Library Context (Enrichment)

| What you need | Tool call | When to use |
|---------------|-----------|-------------|
| All competitors | `list_entities({ entityType: "competitor" })` | Quick inventory for breakdown charts |
| Competitor details | `get_entity({ oId })` | Deep dive when a competitor dominates losses |
| All segments | `list_entities({ entityType: "segment" })` | Segment breakdown analysis |
| All personas | `list_entities({ entityType: "persona" })` | Persona win rate analysis |
| Proof points | `list_entities({ entityType: "proof_point" })` | Evidence for "what's working" section |
| All Motions | `list_motions()` | Inventory of Motions for Motion-level win rate analysis |
| Motion ICP cells | `list_motion_icps({ motionOId })` | Cell-level breakdown (persona × segment) |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Recommendations grounded in Motion ICP narrative + Learning Loop learnings |
| Positioning context | `search_knowledge_base({ query: "win loss competitive positioning" })` | Semantic search for positioning across the library |
| Uploaded deal data | `search_resources({ query: "deal data CRM export" })` | Supplementary deal data from uploaded files |

---

## Competitor-Focused Data (When --competitor is specified)

| What you need | Tool call | When to use |
|---------------|-----------|-------------|
| Competitor profile | `get_entity({ oId })` | Full competitor context |
| Deals vs competitor | `list_events({ startDate, filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Win/loss record against this competitor |
| Findings mentioning competitor | `list_findings({ query: "<competitor> mentions, objections, and comparisons", startDate, eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["competitor"] })` | Existing positioning guidance |

---

## Deal Deep Dive (When --company is specified)

| What you need | Tool call | When to use |
|---------------|-----------|-------------|
| Deal timeline | `list_events({ startDate, filters: { eventTypes: ["DEAL_WON", "DEAL_LOST", "CALL_TRANSCRIPT", "EMAIL_SENT", "EMAIL_REPLY_RECEIVED"], companyDomains: ["<domain>"] } })` | Full activity history for one deal |
| Deal findings | `list_findings({ query: "objections, pain points, decision criteria, competitors, commitments", eventFilters: { companyDomains: ["<domain>"] } })` | Everything extracted from this deal's conversations |
| Key conversations | `get_event_detail({ eventOId, includeTranscript: true })` | Read the pivotal calls in full |
