# Tool Reference

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need actual content -- "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something notable and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept -- "how do we position against price objections?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need CRM exports, uploaded deal data, or reference docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### Core Deal Data (Always Required)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Won deals | `list_events({ filters: { eventTypes: ["DEAL_WON"] }, startDate, endDate })` | Always -- core data |
| Lost deals | `list_events({ filters: { eventTypes: ["DEAL_LOST"] }, startDate, endDate })` | Always -- core data |
| Pipeline context | `list_events({ filters: { eventTypes: ["DEAL_CREATED"] }, startDate, endDate })` | When you need total pipeline for win rate calculation |
| Notable deal details | `get_event_detail({ eventOId })` | Deep dive on 3-5 notable wins and 3-5 notable losses |

---

#### Conversation Intelligence (Findings)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Objections in won deals | `list_findings({ opportunityStatus: ["WON"], extractionTypes: ["CALL_EXTERNAL_OBJECTIONS"], startDate })` | Objections that were overcome |
| Objections in lost deals | `list_findings({ opportunityStatus: ["LOST"], extractionTypes: ["CALL_EXTERNAL_OBJECTIONS"], startDate })` | Objections that killed deals |
| Value props presented | `list_findings({ extractionTypes: ["CALL_INTERNAL_VALUE_PROP_PRESENTATIONS"], startDate })` | What messaging worked vs didn't |
| Competitor mentions | `list_findings({ extractionTypes: ["CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"], startDate })` | Competitive landscape in deals |
| Feature requests | `list_findings({ extractionTypes: ["CALL_EXTERNAL_FEATURE_REQUESTS"], startDate })` | Product gaps causing losses |
| Proof points cited | `list_findings({ extractionTypes: ["CALL_INTERNAL_PROOF_POINTS"], startDate })` | Social proof effectiveness |

---

#### Library Context (Enrichment)

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick inventory for breakdown charts |
| Competitor details | `get_entity({ oId })` | Deep dive when a competitor dominates losses |
| All segments | `list_all_entities({ entityType: "segment" })` | Segment breakdown analysis |
| All personas | `list_all_entities({ entityType: "persona" })` | Persona win rate analysis |
| Proof points | `list_entities({ entityType: "proof_point" })` | Evidence for "what's working" section |
| Playbook strategies | `search_knowledge_base({ query: "win loss competitive positioning" })` | Recommendations grounded in existing playbooks |
| Uploaded deal data | `search_resources({ query: "deal data CRM export" })` | Supplementary deal data from uploaded files |

---

#### Competitor-Focused Data (When --competitor is specified)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor profile | `get_entity({ oId })` | Full competitor context |
| Deals vs competitor | `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Win/loss record against this competitor |
| Findings mentioning competitor | `list_findings({ entityMatches: { competitorOIds: ["<oId>"] }, startDate })` | Real objections and mentions from calls |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["playbook", "competitor"] })` | Existing positioning guidance |
