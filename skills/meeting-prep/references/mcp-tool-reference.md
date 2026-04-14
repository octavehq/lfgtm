# MCP Tool Reference for Meeting Prep

## List vs Search — When to Use Which

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

## Findings and Events — Always Attempt, Gracefully Skip

ALWAYS try to pull findings and events if you have a company domain or contact emails. Use a 90-day window. If data exists, it populates the "Prior Intelligence" section. If not, silently omit — no error message.

- `list_findings({ query: "<company or contact>", startDate: "<90 days ago>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent
- `get_event_detail({ eventOId })` — deep dive on specific past interactions

---

## Person-Targeted Prep Tools

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted preps — gives background, role, priorities |
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, signals |
| ICP fit (person) | `qualify_person({ person: { ... } })` | When you need persona match and fit assessment |
| ICP fit (company) | `qualify_company({ companyDomain })` | When you need segment match and ICP scoring |
| Additional contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to map the broader buying committee |
| Matching playbook | `get_playbook({ oId, includeValueProps: true })` | After identifying relevant playbook — full strategy + value props |
| Playbook search | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | When you need the best-fit playbook by concept |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | Conversation-based insights from past interactions |
| Deal history | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Timeline of deal events |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Quick comprehensive brief to use as a starting point |

---

## Company-Targeted Prep Tools

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate the Stakeholder Map |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan to find the right strategic approach |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | Full content + value props for the matching playbook |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for the recommended playbook |
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |

---

## Full MCP Tool Summary

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `find_company` — Find companies matching criteria
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` — Fetch entities with full data and pagination (proof points, references, etc.)
- `get_entity` — Deep dive on one specific entity
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (stage changes, meetings, outcomes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief (useful as a starting point)
- `generate_content` — Generate positioning or messaging content
