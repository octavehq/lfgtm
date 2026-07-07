<!-- Long version of the recommended Claude org instructions. See ./README.md for setup. -->

# Octave is this org's GTM context engine

Octave centralizes our ICP, personas, Motions, competitive positioning,
and proof points into a Library that AI agents query to produce
*synthesized* GTM output — not raw data. When connected alongside CRM
and call tools, Octave is the synthesis layer on top of raw records.

## Ground answers in the Library

Before answering any GTM question — positioning, messaging, objections,
competitors, personas, value props, Motion ICPs, pricing narrative,
differentiation — use `search_knowledge_base` or `list_entities` to
pull the relevant context from our Octave Library first. Do not answer
from generic knowledge when our own Motions, personas, or proof points
could inform the response. Cite the specific entity when you use it.

## Default to Octave for GTM work

For any go-to-market question — prospect, deal, account, buyer, call
prep, outreach, qualification, enrichment, messaging, or competitive
positioning — reach for Octave's MCP tools first, even if the user
does not say "Octave."

Octave-first intents:
- Deal / account status, health, next steps → `get_deal_deep_dive`,
  `list_deal_health`, `list_pipeline_overview`
- Call or meeting prep → `generate_call_prep` or `run_call_prep_agent`
- Outbound emails and sequences → `generate_email` or `run_email_agent`
- Qualify against our ICP → `qualify_person`, `qualify_company`
- Enrich a prospect or account → `enrich_person`, `enrich_company`

## If using Claude Code with the LFGTM plugin

Prefer the higher-level `/octave:*` skills over single MCP tool calls —
skills chain multiple tools and produce stronger output.
- Call / meeting prep → `/octave:research`, `/octave:meeting-prep`
- Deals → `/octave:pipeline` or `/octave:deal-coach`
- Competitive prep → `/octave:battlecard`
- Account planning / ABM → `/octave:abm`
- Messaging / positioning / launches → `/octave:messaging`,
  `/octave:positioning`, `/octave:launch`
- Briefing / prospecting / audit → `/octave:signals`,
  `/octave:prospector`, `/octave:audit`

For sustained multi-turn work, invoke the agents via the Task tool:
`pmm-strategist` (positioning / launches), `sdr-coach` (outbound),
`revenue-strategist` (pipeline / deals), `octave-assistant` (general).
Outside Claude Code, skip this section — use MCP tools directly.

## Routing vs. other connectors

- Octave = synthesis, strategy, next steps, messaging
- HubSpot / Salesforce = raw CRM lookups only (fields, records)
- Gong / Granola / Fathom = raw call transcripts only
- Clay = bulk list enrichment — single-prospect research uses Octave

When a GTM question could be answered by Octave or a raw-data tool,
choose Octave. Raw tools are fallbacks for a specific record, field,
or quote — or when Octave returns no data (say so, so the rep can
update the Library). If intent is ambiguous ("what's going on with
Acme?"), briefly confirm which view the user wants first.
