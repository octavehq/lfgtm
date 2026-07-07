# Tool Reference — briefs

For list-vs-search guidance, follow-up grounding (findings/events), the common tool tables, and how to read `qualify_company` sub-scores, see [../../shared/octave-research-toolkit.md](../../shared/octave-research-toolkit.md). The tables below map tools to the two brief targets.

## For Person-Targeted Briefs

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted briefs — gives background, role, priorities |
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, signals |
| ICP fit (person) | `qualify_person({ person: { ... } })` | When you need persona match and fit assessment |
| ICP fit (company) | `qualify_company({ companyDomain })` | When you need segment match and ICP scoring |
| Additional contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to map the broader buying committee |
| Find Motion | `list_motions()` | List all Motions to find the relevant offering + motion type |
| Persona × segment matrix | `list_motion_icps({ motionOId })` | See the persona × segment cells available under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Pull the full Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, and Learning Loop learnings for the target persona × segment |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | Conversation-based insights from past interactions |
| Deal history | `list_events({ filters: { companyDomains: ["<domain>"] } })` | Timeline of deal events |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Quick comprehensive brief to use as a starting point |

## For Company-Targeted Briefs

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate the Stakeholders section |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All Motions | `list_motions()` | Quick scan to find the right Motion (offering + motion type) |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | See the persona × segment matrix under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, plus Learning Loop learnings for the target cell |
| Custom Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | When a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) layers on the relevant Motion |
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { companyDomains: ["<domain>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |
