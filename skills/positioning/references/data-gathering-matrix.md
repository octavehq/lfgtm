# Data Gathering Matrix

Every section needs data from the Octave library. Gather it all up front in a single pass.

## Tool Selection Guide

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all personas" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept — "how do we position for enterprise?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

## Entity-to-Section Mapping

| What you need | Tool | Sections that use it |
|---------------|------|---------------------|
| All products | `list_all_entities({ entityType: "product" })` | All 8 |
| Product deep dive | `get_entity({ oId: "<product_oId>" })` | All 8 |
| All personas | `list_entities({ entityType: "persona" })` | 1, 3, 4, 5, 7, 8 |
| All segments | `list_entities({ entityType: "segment" })` | 1, 3 |
| All use cases | `list_entities({ entityType: "use_case" })` | 1, 3, 6, 7 |
| All competitors | `list_all_entities({ entityType: "competitor" })` | 2, 3, 6 |
| Competitor details | `get_entity({ oId })` | 3, 6 |
| All playbooks | `list_all_entities({ entityType: "playbook" })` | 1, 2, 4, 5, 8 |
| Playbook + value props | `get_playbook({ oId, includeValueProps: true })` | 1, 2, 4, 5, 8 |
| Proof points | `list_entities({ entityType: "proof_point" })` | 2, 3, 5 |
| References | `list_entities({ entityType: "reference" })` | 2, 3 |
| Brand voice | `list_brand_voices()` | 8 (homepage tone) |
| Competitive positioning | `search_knowledge_base({ query: "<product> differentiation competitive advantage", entityTypes: ["competitor", "playbook"] })` | 2, 3, 6 |
| What resonates | `list_findings({ query: "value propositions positive reactions resonated", startDate: "<90 days ago>", eventFilters: { sentiments: ["POSITIVE"] } })` | 2, 5 |
| What falls flat | `list_findings({ query: "objections pushback concerns", startDate: "<90 days ago>", eventFilters: { sentiments: ["NEGATIVE"] } })` | 3, 5 |
