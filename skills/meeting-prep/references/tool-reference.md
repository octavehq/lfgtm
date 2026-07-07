# Tool Reference — meeting prep

For list-vs-search guidance and the common tool tables, see [../../shared/octave-research-toolkit.md](../../shared/octave-research-toolkit.md). The tables below follow the prep's research order: verify first, then fit, then positioning, proof, and deal state.

## 2a. Verify the people and the company (do this first)

Grounding starts here. Before anything names a person or states a "fact," confirm it:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Confirm a person exists + get LinkedIn | `resolve_profile_from_email({ email })` / `resolve_email_from_profile({ ... })` | For every named attendee — confirm identity and capture the real LinkedIn URL to link |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | After confirming — background, role, priorities, persona match |
| Map the buying committee | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When attendees are unknown, or to find who else should be in the room |
| Company profile | `enrich_company({ companyDomain })` | Always — industry, size, tech stack, funding, signals |
| Company logo + domain check | `get_external_brand_logo({ domain })` | For the header, and to confirm the domain resolves to a real company |

> **Internal-vs-customer check — do this before flagging anyone.** Resolve each name. If it belongs to your own team (your company domain / the CRM deal owner / AE / SE), it is **internal**: name them in the header as the deal owner, keep them out of the customer stakeholder list, and never put a ⚠ on them. Only genuinely external, unconfirmable people get the **⚠ Unconfirmed** flag — or are left out. Do not invent a contact to fill a slot.

## 2b. Why this company, why now (fit + live intel)

| What you need | Tool | When to use |
|---------------|------|-------------|
| ICP fit + reasons | `qualify_company({ companyDomain })` | Always — segment match, fit score, and the 3-5 fit reasons that answer "why them" |
| Person fit | `qualify_person({ person: { ... } })` | Persona match and individual fit |
| Recent news (company) | `deep_web_research({ query: "<Company> news funding launches leadership 90 days" })` | Surface dated, linkable company news — fold the *so-what* for this meeting |
| Segment/market research | `deep_web_research({ query: "<their industry/segment> trends <relevant theme>" })` | Segment-level intel: what's moving in their category that maps to our value |
| Verified site facts | `scrape_website({ url })` | Pull linkable facts from their own site / newsroom |
| Similar customers we've won | `list_entities({ entityType: "reference" })` | Pull the library's **reference customers** and pick the ones most like this account (industry, size, use case) for "companies like you chose us." Do **not** use `find_similar_companies` here — it returns lookalike *prospects*, not customers with deals. |

## 2c. Why us, for each persona (positioning + use cases)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Motions for the offering | `list_motions()` | Always — find the Motion(s) covering this offering / motion type |
| Persona × segment matrix | `list_motion_icps({ motionOId })` | See which Motion ICP cells exist; pick the cell **per persona** at the table |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Per-persona narrative: Target ICP overview, Operating landscape, Strategic narrative, **Pains and consequences**, **Benefits and impacts**, Methodology, References + Learning Loop learnings |
| Persona definitions | `list_entities({ entityType: "persona" })` | Why each persona type cares — priorities, language, what they're measured on |
| Value props per persona | (from `find_motion_icp` → **Benefits and impacts**) | The current source for value props is the Motion ICP cell narrative — outcomes, not features. Do **not** use `list_value_props` (deprecated; reads old playbooks). |
| Top use cases | `list_entities({ entityType: "use_case" })` | The use cases that matter most — per persona and for this company |
| Custom Motion Playbook | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` | Thematic / Milestone / Account / Competitive angles layered on the Motion |

## 2d. Proof, objections, competitors

| What you need | Tool | When to use |
|---------------|------|-------------|
| Proof points | `list_entities({ entityType: "proof_point" })` | Metrics, quotes, logos — for the winning story's proof and similar customers |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Topic-matched proof | `search_knowledge_base({ query: "<industry> <use case> results", entityTypes: ["proof_point", "reference"] })` | Find proof relevant to *their* specific situation |
| Known objections | `list_entities({ entityType: "objection" })` | Likely objections + grounded counters |
| Competitors (scan) | `list_all_entities({ entityType: "competitor" })` | Who's in the landscape |
| Competitor deep-dive | `get_entity({ oId })` / `get_competitive_insights({ ... })` | Where they win, where we win, the one differentiator that matters here |

## 2e. Deal state & conversation history (for the Snapshot)

ALWAYS try to pull deal context and findings if you have a company domain or contact emails. Use a 90-day window. If data exists, it feeds the **Snapshot**; if not, silently omit — no error message.

| What you need | Tool | When to use |
|---------------|------|-------------|
| Deal deep-dive | `get_deal_deep_dive({ ... })` / `list_deal_health({ ... })` | Stage, risk, compelling event, next milestone — feeds the Snapshot strip |
| Recent findings | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | What was actually said in calls: objections raised, features requested, pain confirmed, competitors mentioned |
| Deal events | `list_events({ filters: { companyDomains: ["<domain>"] } })` | Deal stage changes, meetings held, emails sent |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific past interaction |
| Synthesized starting point | `generate_call_prep({ companyDomain })` | A quick comprehensive brief to use as a starting point (still verify its claims) |
