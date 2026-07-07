# Tool Reference — per deck type

For list-vs-search guidance, the follow-up-grounding tools, and the common tool tables (enrichment, Motions/Motion ICP, proof, signals), see [../../shared/octave-research-toolkit.md](../../shared/octave-research-toolkit.md). The tables below map tools to each deck type.

## For Customer-Facing Decks (pitch, demo, QBR)

Start with company and person enrichment, then pull positioning context as needed:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always — gives industry, size, tech stack, signals |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When audience includes unknown stakeholders |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target audience |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to frame "why us" for this account |
| All Motions | `list_motions()` | Quick scan of Motions to find the right one for this account |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` | Default + Custom Motion Playbooks for the selected Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full Motion Playbook narrative content |
| Motion ICP cells | `list_motion_icps({ motionOId })` | Persona × segment cells under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Cell-level Target ICP / Strategic narrative / Pains / Benefits / Methodology / References + Learning Loop learnings |
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch actual proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Find proof points by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* a specific topic or industry |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Uploaded resources | `search_resources({ query: "<topic>" })` | When the workspace has uploaded docs, one-pagers, or assets relevant to the deck |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | When you want conversation-based insights |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a single comprehensive brief to work from |

## For Internal Decks (strategy, planning, launch)

Pull from the library to ground the deck in your actual GTM data:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Personas | `list_all_entities({ entityType: "persona" })` | Quick scan of all personas |
| Persona details | `list_entities({ entityType: "persona" })` | Full persona data — pain points, priorities, messaging |
| Segments | `list_all_entities({ entityType: "segment" })` | Quick scan of market segments |
| Competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Products | `list_all_entities({ entityType: "product" })` | Quick scan of product capabilities |
| Use cases | `list_all_entities({ entityType: "use_case" })` | When deck covers how customers use the product |
| Entity details | `get_entity({ oId })` | Deep dive on any specific entity found above |
| Positioning by topic | `search_knowledge_base({ query: "<topic>", entityTypes: ["product"] })` | When you have a concept and need relevant positioning |
| Motions | `list_motions()` | Available Motions to ground the deck in |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` and `get_motion_playbook({ motionPlaybookOId })` | Default + Custom Motion Playbook narrative content |
| Motion ICP narratives | `list_motion_icps({ motionOId })` then `find_motion_icp({ motionIcpOId })` | Persona × segment narrative grounded in the library |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data for credibility slides |
| References | `list_entities({ entityType: "reference" })` | Fetch customer references for social proof slides |
| Uploaded docs | `search_resources({ query: "<topic>" })` | Find uploaded strategy docs, market research, or assets |
| Market signals | `list_findings({ query: "<topic>", startDate: "<90 days ago>" })` | Recent conversation-based trends |
| Deal outcomes | `list_events({ startDate: "<90 days ago>", filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"] } })` | Pipeline, revenue, or win/loss data |

## For Competitive Decks (battlecard presentations)

Focus on the specific competitor(s) and evidence from real deals:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of all competitors |
| Competitor full data | `list_entities({ entityType: "competitor" })` | Full competitor profiles — strengths, weaknesses, positioning |
| Competitor deep dive | `get_entity({ oId })` | Everything about one specific competitor |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["competitor"] })` | When you have a concept — "how do we beat them on security?" |
| Our products | `list_entities({ entityType: "product" })` | Full product data for side-by-side comparison slides |
| Proof points (competitive wins) | `list_entities({ entityType: "proof_point" })` | Fetch all proof points — filter for competitive wins |
| Win/loss data | `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Real deal outcomes against this competitor |
| Conversation evidence | `list_findings({ query: "<competitor>", eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Custom Motion Playbooks (COMPETITIVE) | `list_motions()` then `list_motion_playbooks({ motionOId })` filtered by `narrativeType === "COMPETITIVE"` | Competitive narrative layered onto each Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full competitive narrative content |
| Competitive resources | `search_resources({ query: "<competitor>" })` | Uploaded battlecards, analyst reports, or competitive docs |

## For Enablement Decks (training, sales kickoff)

Mix Motion ICP narrative content with real deal examples:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All Motions | `list_motions()` | Scan available Motions to decide which to teach |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` and `get_motion_playbook({ motionPlaybookOId })` | Default + Custom Motion Playbook content for training slides |
| Motion ICP narratives | `list_motion_icps({ motionOId })` then `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Cell-level narratives + Learning Loop learnings for training slides |
| Personas | `list_entities({ entityType: "persona" })` | Full persona data for "know your buyer" slides |
| Competitors | `list_entities({ entityType: "competitor" })` | Full competitor data for competitive handling slides |
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data for example slides |
| Proof points by topic | `search_knowledge_base({ query: "results metrics", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* specific outcomes |
| Recent wins | `list_events({ filters: { eventTypes: ["DEAL_WON"] } })` | Success stories to use as examples |
| Win details | `get_event_detail({ eventOId })` | Deep dive on a notable win for a case study slide |
| Training resources | `search_resources({ query: "<topic>" })` | Uploaded enablement docs, Motion Playbook reference PDFs, or training assets |
