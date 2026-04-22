# Tool Reference

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content -- "get full competitor profiles" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found a competitor and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept -- "how do we compete on security?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need uploaded competitive intel docs or analyst reports |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### For Single Competitor Battlecard

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor full profile | `get_entity({ oId: "<competitor_oId>" })` | Always -- the core source |
| All competitors (context) | `list_all_entities({ entityType: "competitor" })` | Quick scan of landscape around this competitor |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> positioning", entityTypes: ["playbook", "competitor"] })` | Messaging angles and playbook positioning |
| Playbook with value props | `get_playbook({ oId, includeValueProps: true })` | After finding a relevant playbook -- gets differentiators |
| Your products | `list_entities({ entityType: "product" })` | Product capabilities for side-by-side comparison |
| Product deep dive | `get_entity({ oId: "<product_oId>" })` | Granular feature details for comparison |
| Competitive wins | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_WON"], competitors: ["<oId>"] } })` | Real deal outcomes -- wins against this competitor |
| Competitive losses | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_LOST"], competitors: ["<oId>"] } })` | Real deal outcomes -- losses to this competitor |
| Deal details | `get_event_detail({ eventOId })` | Deep dive on notable wins or losses for evidence |
| Conversation evidence | `list_findings({ query: "<competitor>", eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Proof points | `list_entities({ entityType: "proof_point" })` | Competitive win proof points, switching stories |
| References | `list_entities({ entityType: "reference" })` | Customers who switched from this competitor |
| Proof points by topic | `search_knowledge_base({ query: "<competitor> win switch", entityTypes: ["proof_point", "reference"] })` | Switching and competitive win stories |
| Uploaded intel | `search_resources({ query: "<competitor>" })` | Analyst reports, competitive docs |

---

#### For Landscape Overview

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Always -- the full inventory |
| Competitor full data | `list_entities({ entityType: "competitor" })` | Full profiles for every competitor |
| Per-competitor deep dive | `get_entity({ oId })` | Detailed data for each competitor card |
| Competitive playbooks | `search_knowledge_base({ query: "competitive positioning", entityTypes: ["playbook"] })` | Cross-competitor positioning themes |
| Your products | `list_entities({ entityType: "product" })` | Product capabilities for comparison context |
| All deal outcomes | `list_events({ startDate: "<180d ago>", filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"] } })` | Win rates across all competitors |
| Conversation evidence | `list_findings({ query: "competitive", startDate: "<90d ago>" })` | Cross-competitor objection patterns |
| Proof points | `list_entities({ entityType: "proof_point" })` | Competitive win stories across all |
| Uploaded intel | `search_resources({ query: "competitive landscape" })` | Analyst reports, market research docs |
