# Tool Reference — one-pagers

For list-vs-search guidance, follow-up grounding (findings/events to anchor a follow-up doc in what was actually said), and the common tool tables, see [../../shared/octave-research-toolkit.md](../../shared/octave-research-toolkit.md). The tables below map tools to the two one-pager targets.

## For Account-Specific One-Pagers

Start with company and person enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always -- gives industry, size, tech stack, signals |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the recipient |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you need to identify the right stakeholder(s) |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to frame "why us" for this account |
| Motions for offering | `list_motions()` | Find the Motion(s) covering this offering |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | Pick the persona × segment cell that matches this account |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Drives the "why us / our approach" section (Strategic narrative, Benefits and impacts) |
| Custom Motion Playbooks | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` | Pull Thematic / Milestone / Account / Competitive angles layered on the Motion |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data -- metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Topic-specific proof | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* a specific topic or industry |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation-based insights for follow-up docs |
| Deal events | `list_events({ filters: { companyDomains: ["<domain>"] } })` | Deal progression for follow-up context |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific interactions |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a single comprehensive brief to work from |
| Uploaded assets | `search_resources({ query: "<topic>" })` | Relevant uploaded docs or reference materials |

## For Segment-Level One-Pagers

When the target is a segment description rather than a specific company:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Motions for offering | `list_motions()` | Find the Motion(s) covering offerings that target this segment |
| Motion ICP cells for segment | `list_motion_icps({ motionOId })` | Identify cells where this segment is the segment side of the persona × segment intersection |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full per-cell narrative for the segment-specific buyer |
| Personas | `list_entities({ entityType: "persona" })` | Understand who the typical buyer is in this segment |
| Segments | `list_all_entities({ entityType: "segment" })` | Quick scan to match the description to a defined segment |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points relevant to this segment |
| References | `list_entities({ entityType: "reference" })` | Customer references in this segment |
| Products | `list_entities({ entityType: "product" })` | Product capabilities relevant to segment needs |
| Use cases | `list_all_entities({ entityType: "use_case" })` | Use cases that resonate with this segment |
| Uploaded resources | `search_resources({ query: "<segment topic>" })` | Relevant uploaded collateral |
