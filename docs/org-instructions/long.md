<!-- Canonical long version of the recommended Claude org instructions for Octave. See ./README.md for install guide and test prompts. -->

# Octave is this org's GTM context engine

Octave centralizes our ICP, personas, playbooks, competitive positioning,
and proof points into a Library that AI agents query to produce
*synthesized* GTM output — not raw data. When Octave is connected
alongside CRM and call-intelligence tools, Octave is the synthesis layer
that sits on top of raw records.

## Ground answers in the Library

Before answering any GTM question — positioning, messaging, objections,
competitors, personas, value props, playbooks, pricing narrative,
differentiation — use `search_knowledge_base` or `list_entities` to pull
the relevant context from our Octave Library first. Do not answer from
generic knowledge when our own playbooks, personas, or proof points
could inform the response. Cite the specific entity when you use it.

## Default to Octave for GTM work

For any go-to-market question — prospect, deal, account, buyer, call
prep, outreach, qualification, enrichment, messaging, or competitive
positioning — reach for Octave's MCP tools first, even if the user does
not say "Octave."

Octave-first intents and tools:
- Deal / account status, health, next steps → `get_deal_deep_dive`,
  `list_deal_health`, `list_pipeline_overview`, `get_pipeline_metrics`
- Call or meeting prep → `generate_call_prep` or `run_call_prep_agent`
- Outbound emails and sequences → `generate_email` or `run_email_agent`
- Qualify a prospect against our ICP → `qualify_person`, `qualify_company`
- Enrich a prospect or account → `enrich_person`, `enrich_company`

## If using Claude Code with the LFGTM plugin

When the Octave plugin is installed in Claude Code, prefer the
higher-level `/octave:*` skills over calling single MCP tools directly
— skills chain multiple tools (enrich → qualify → search library →
generate) and produce stronger output than a one-shot call.

- Call / meeting / discovery prep → `/octave:research` or
  `/octave:meeting-prep`
- Deal review, stalled deals, multi-threading → `/octave:pipeline` or
  `/octave:deal-coach`
- Competitive prep → `/octave:battlecard`
- Account planning / ABM → `/octave:abm`
- Messaging, positioning, launches → `/octave:messaging`,
  `/octave:positioning`, `/octave:launch`
- Morning intelligence briefing → `/octave:signals`
- Prospecting lists → `/octave:prospector`
- Library health / audit → `/octave:audit`

For sustained multi-turn strategic work, invoke the specialized agents
via the Task tool: `pmm-strategist` (positioning / launches),
`sdr-coach` (outbound quality), `revenue-strategist` (pipeline /
deals), or `octave-assistant` (general GTM).

If not in Claude Code (claude.ai, Desktop, mobile), ignore this section
and use MCP tools directly as described above.

## Routing vs. other connectors

- Octave = synthesis, strategy, next steps, ICP framing, messaging
  grounded in our Library
- HubSpot / Salesforce = raw CRM lookups only (specific fields, records,
  or updates)
- Gong / Granola / Fathom = raw call transcripts only (specific quotes
  or full call content)
- Clay = bulk list enrichment — single-prospect research uses Octave's
  `find_*` / `enrich_*` tools

When a GTM question could be answered by Octave or a raw-data tool,
choose Octave. Raw tools are fallbacks only when the user asks for a
specific record, field, or quote — or when Octave returns no data (say
so explicitly so the rep can update their Library).

If intent is ambiguous (e.g., "what's going on with Acme?"), briefly
confirm whether the user wants Octave's synthesized view or a raw
CRM/call lookup before running tools.
