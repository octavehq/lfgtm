# Octave Claude Code Plugin

Access Octave's GTM knowledge base directly from Claude Code for positioning, research, content generation, and sales enablement.

## About Octave

Octave is a GTM intelligence platform that helps sales and marketing teams centralize positioning, messaging, and go-to-market knowledge. This Claude Code plugin brings Octave's capabilities directly into your development workflow.

## Installation

### Prerequisites

- Claude Code CLI installed ([install guide](https://docs.anthropic.com/en/docs/claude-code))
- Claude Code authenticated — a Claude subscription (Pro/Max/Team) or an Anthropic API key both work
- An Octave workspace account

### Install via Marketplace (Recommended)

1. **Add the Octave marketplace:**
```bash
claude plugin marketplace add https://github.com/octavehq/lfgtm
```

2. **Install the Octave plugin:**
```bash
claude plugin install octave@lfgtm
```

3. **Verify installation:**
```bash
claude plugin list
```

You should see "octave" in your installed plugins.

### Other AI tools (Codex & Cursor)

This repo is the source of truth. On every push to `main`, the same skills are automatically built and mirrored into editor-specific plugin repos:

- **OpenAI Codex** → [octavehq/lfgtm-codex](https://github.com/octavehq/lfgtm-codex)
- **Cursor** → [octavehq/lfgtm-cursor](https://github.com/octavehq/lfgtm-cursor)

Install from the matching repo (see its README). Don't edit those repos directly — they're generated and overwritten. File issues and PRs here.

## Quick Start

### 1. Configure MCP Server

Add the Octave MCP server (one connection per workspace):

```bash
claude mcp add octave-acme --transport http https://mcp.octavehq.com/mcp?ctx=<context>
```

You can use any name that starts with `octave-` (e.g. `octave-acme`). Skills detect the Octave MCP server from your available tools.

> **Keep the `ctx` value private.** It is a workspace-scoped credential — treat it like an API key and never commit it to a repository or paste it into shared documents.

### 2. Start Using Octave Skills
```
/octave:library list      # Browse your library
/octave:research john@acme.com --for discovery  # Prep for a call
```

### 3. (Recommended for teams) Set Claude Org Preferences

If your team also has HubSpot, Salesforce, Gong, Granola, or Clay connected to Claude, set Claude **Organization preferences** so Claude routes GTM questions to Octave by default — reps won't need to prefix prompts with "Using Octave, …" to get the right output.

See [**docs/org-instructions/**](docs/org-instructions/) for short and long recommended instructions, admin setup, and test prompts.

**Quick test (wait up to 1 hour for propagation first):** in a new Claude conversation, ask *"What's the status of my deal with [company] and what should I be doing next?"* — without mentioning Octave. If Claude reaches for `get_deal_deep_dive` or `/octave:pipeline`, the instructions are working.

## Skills

### Core Skills

| Skill | Description |
|-------|-------------|
| `/octave:library` | Browse, search, create, and update library entities |
| `/octave:generate` | Quick content generation (emails, LinkedIn messages) |

### Strategy & Messaging Skills

| Skill | Description |
|-------|-------------|
| `/octave:product-launch` | Product and feature launch planning with full content kit |
| `/octave:battlecard-doc` | Interactive HTML competitive battlecard — single competitor or full landscape, with trap questions and objection counters grounded in real conversation evidence |
| `/octave:ads` | Build platform-ready ad campaigns with audience targeting, creative variants, and negative keywords |
| `/octave:ads-resonance` | Analyze ad performance (MCP, BigQuery Data Transfer, direct API, or manual paste), score falsifiable prediction cards against real data, and feed learnings back into the library |

### Research & Prospecting Skills

| Skill | Description |
|-------|-------------|
| `/octave:research` | Context-aware prep for calls, demos, outreach, deal reviews |
| `/octave:prospector` | Find, enrich, and qualify ICP-fit prospects using your library |
| `/octave:abm` | Account-based planning with stakeholder mapping and outreach |

### Sales Enablement Skills

| Skill | Description |
|-------|-------------|
| `/octave:pipeline` | Deal-level coaching — stalled deals, multi-threading, competitive |
| `/octave:call-analyzer` | Analyze conversations for resonance, adherence, differentiation |
| `/octave:train` | Practice selling — role-play simulations, quizzes, guided learning |
| `/octave:deal-coach` | Methodology-driven deal coaching — role-play, microsites, decks, and quizzes around Resonate/Elevate/Compel |

### Intelligence & Analytics Skills

| Skill | Description |
|-------|-------------|
| `/octave:insights` | Surface findings, trends, and patterns from calls and emails |
| `/octave:signals` | Morning intelligence briefing — deals, patterns, and signals demanding attention |
| `/octave:win-loss-report` | Visual win/loss analysis report as self-contained HTML with charts — patterns, competitor cuts, and deal deep dives |
| `/octave:icp-refine` | Refine ICP definitions using deal outcome analysis |
| `/octave:qual-doctor` | Diagnose and tune qualification agents — test against known-fit prospects, analyze per-question scoring patterns, and recommend specific changes to questions, weights, and entity descriptions. Handles both score-only and routing+scoring tuning modes. |

### Document Builder Skills

| Skill | Description |
|-------|-------------|
| `/octave:get-brand-components` | Capture a company's brand (fonts, colors, logo, real imagery, components) from its website into a reusable kit — every Document Builder below can render **on-brand** with it; kits can be reused from and hosted to the asset store (asset-manager) |
| `/octave:meeting-prep` | Strategic meeting battle plan with coaching frameworks and talk tracks as HTML |
| `/octave:deck` | Build Octave-powered HTML slide decks with brand styling and export |
| `/octave:one-pager` | Personalized one-pager / leave-behind as self-contained HTML |
| `/octave:proposal` | Formal business case and proposal as customer-facing HTML |
| `/octave:microsite` | Personalized ABM microsite / landing page as HTML |
| `/octave:champion-deal-room` | Internal deal room a rep hands a champion to run the buying-committee sell — business case, stakeholder map, objection handling, path to yes |
| `/octave:positioning` | Complete visual Messaging & Positioning system (8 frameworks) as HTML |

### Library Operations

| Skill | Description |
|-------|-------------|
| `/octave:audit` | Library health check — find gaps, stale content, duplicates |

### Publishing Skills

| Skill | Description |
|-------|-------------|
| `/octave:asset-manager` | Publish and manage hosted assets — upload, privacy tiers (only_me/workspace/public), share links, asset registry; checks for existing assets before creating so work isn't duplicated |

## Agents

Specialized agent personas for sustained, multi-turn work sessions.

| Agent | Description |
|-------|-------------|
| `octave-assistant` | General GTM assistant with full Octave platform knowledge |
| `pmm-strategist` | Senior PMM focused on positioning, messaging, and launch strategy |
| `sdr-coach` | SDR manager focused on outreach quality, reply rates, and coaching |
| `revenue-strategist` | VP Revenue advisor for pipeline strategy and deal coaching |
| `asset-manager` | Publish and manage hosted assets: upload, privacy tiers, share links, persistent registry; cache-aware — reuses existing assets instead of duplicating them |
| `octave-editorial-reviewer` | Language + information quality reviewer spawned by the review gate after a skill generates a deliverable — audits reader-facing text against the editorial rules and information principles, fixes violations inline (not invoked directly) |
| `octave-presentation-reviewer` | Visual + structural reviewer spawned by the review gate — renders the generated HTML and inspects the pixels, audits against the presentation principles, format rules, and skill blueprints, fixes CSS/layout violations inline (not invoked directly) |

## Skill Details


### /octave:positioning
Complete visual Messaging & Positioning system as a scrollable HTML document:
- Message Framework (3-layer pyramid: market → product → value props by persona)
- Positioning Anchors (primary & secondary statements with keyword highlights)
- Positioning Strategy (tactical table: buyer, use case, problems, differentiators)
- Persona-Based Messaging (core message translated per buying committee role)
- Value Prop by Awareness Stage (4-column funnel: unaware → product-aware)
- Use Case Messaging Canvas (current way vs new way per use case)
- Use Case Lifecycle (customer journey phases with touchpoints)
- Homepage Messaging (website implementation: primary vs secondary messaging)

```
/octave:positioning                           # Full 8-section exercise
/octave:positioning message-framework         # Just the message framework
/octave:positioning anchors                   # Positioning anchors only
/octave:positioning homepage                  # Homepage messaging template
/octave:positioning --product "Platform"      # Focus on specific product
```


### /octave:product-launch
Product and feature launch planning with content kit:
- Positioning and messaging by persona
- Channel strategy and timeline
- Content kit: announcement emails, blog, social, one-pager, FAQ, competitive talking points
- Library updates for new capabilities

```
/octave:product-launch "AI Analytics Dashboard" --type feature
/octave:product-launch "Enterprise Tier" --type product
/octave:product-launch "APAC Expansion" --type expansion
```

### /octave:battlecard-doc
Interactive HTML competitive battlecard grounded in real conversation evidence:
- Single-competitor deep dives with expandable sections and color-coded comparisons
- Full competitive landscape documents across every tracked competitor
- Trap questions to expose competitor weaknesses
- Objection counters ("they say X, we say Y") backed by verbatim call quotes, not paraphrases
- Displacement outreach offered as a follow-up

```
/octave:battlecard-doc --competitor "Acme"
/octave:battlecard-doc --competitor "all"   # Full competitive landscape doc
```

### /octave:abm
Account-based planning:
- Deep account research and ICP scoring
- Stakeholder mapping with persona matching
- Per-stakeholder messaging strategy
- Engagement sequence recommendations
- Initial outreach generation

```
/octave:abm acme.com
/octave:abm acme.com --stakeholders 5 --motion "Enterprise Net New"
/octave:abm "Acme Corp" --depth quick
```

### /octave:pipeline
Deal-level coaching:
- Stalled deal diagnosis and re-engagement strategy
- Multi-threading recommendations (find and engage more stakeholders)
- Competitive threat response
- Executive engagement strategy
- Closing tactics and expansion planning

```
/octave:pipeline stalled acme.com
/octave:pipeline multi-thread acme.com
/octave:pipeline competitive acme.com --competitor "Acme"
/octave:pipeline close acme.com
```


### /octave:icp-refine
ICP analysis and refinement:
- Compare defined ICP against actual deal outcomes
- Identify winning patterns and anti-patterns
- Persona and segment effectiveness analysis
- Value prop resonance from conversation data
- Recommended library updates with evidence

```
/octave:icp-refine --period 90
/octave:icp-refine --segment "Enterprise"
/octave:icp-refine --focus losses
```

### /octave:audit
Comprehensive library audit to identify:
- Missing or incomplete entities
- Orphaned personas / segments (not linked to any offering, so they don't appear in any Motion matrix)
- Missing Motions for active offerings
- Stale content (not updated recently)
- Duplicate or overlapping entities
- Broken references
- Legacy standalone playbook → Motions migration

```
/octave:audit                    # Full audit
/octave:audit --type personas    # Focus on personas
/octave:audit --fix              # Interactive fix mode
/octave:audit --migrate          # Legacy playbook → Motions migration
```


### /octave:prospector
Find and qualify companies and people matching your ICP:
- Searches using your library's segments and personas as criteria
- Enriches, qualifies, and scores each prospect
- Provides filter suggestions for Apollo, Clay, or LinkedIn Sales Nav

```
/octave:prospector --motion "Enterprise Sales"
/octave:prospector --similar-to stripe.com
/octave:prospector --company acme.com
```


### /octave:research
Context-aware research and prep:
- Discovery call prep (questions, pain points, qualification)
- Demo prep (use cases, proof points, objections)
- Outreach prep (hooks, angles, personalization)
- Pipeline review (deal health, next moves, risks)
- Recent Signals backed by verbatim call quotes with recording links, not paraphrases

```
/octave:research john@acme.com --for discovery
/octave:research acme.com --for demo
/octave:research "Acme deal" --for pipeline-review
```

### /octave:call-analyzer
Conversation analysis against your library:
- Resonance: Did messaging land?
- Adherence: Did we follow the Motion ICP narrative?
- Differentiation: Did we position effectively?

```
/octave:call-analyzer              # Paste content to analyze
/octave:call-analyzer --type call  # Analyze call transcript
```

### /octave:insights
Surface intelligence from sales conversations:
- Top objections, pain points, and questions
- What's resonating vs not
- Trends over time
- Library update suggestions
- Drill into the verbatim quote behind any finding, with recording link and timestamp

```
/octave:insights --type objections
/octave:insights --persona "CTO"
```

### /octave:win-loss-report
Visual win/loss analysis as a self-contained HTML report with charts:
- Win/loss patterns and competitor analysis
- Period, segment, and competitor cuts
- Deal deep dives
- Verbatim objection and competitor quotes split by deal outcome, not paraphrases

```
/octave:win-loss-report
/octave:win-loss-report --competitor "Salesforce"
/octave:win-loss-report --period "2025" --segment "mid-market"
```




### /octave:train
Practice selling with role-play simulations and knowledge quizzes:

```
/octave:train                                   # Interactive - pick a mode
/octave:train roleplay --persona "CTO"          # Role-play with a specific persona
/octave:train quiz --topic objections            # Quiz on objection handling
/octave:train quiz --competitor "Acme"           # Competitive knowledge check
```

### /octave:ads
Build platform-ready ad campaign plans grounded in your library intelligence:
- Ad sets structured by persona, segment, or ICP
- 8 creative variant types: pain-focused, outcome, social proof, competitive, question-based, data-driven, status quo, authority
- Source cards with full derivation chains from library data to headline
- Audience targeting with positive/negative keywords and exclusions
- Landing page recommendations from your resources
- Export as CSV for Google Ads, Meta, or LinkedIn bulk upload
- Visual campaign deck as self-contained HTML

```
/octave:ads                                              # Interactive — full campaign builder
/octave:ads "compliance automation for VP Engineering"   # Campaign with angle
/octave:ads "competitive displacement vs Acme"           # Competitive campaign
/octave:ads "Q1 product launch"                          # Launch campaign
```

### /octave:ads-resonance
Analyze ad performance and feed learnings back into your GTM library:
- Pulls performance data from an ads MCP server, BigQuery Data Transfer, direct API, or manual paste — auto-detected in that order
- Confidence-tiered findings that scale with spend, from smoke-test mode to full resonance analysis
- Falsifiable prediction cards scored on every run, accumulating a calibration track record over time
- Library update recommendations and a sales intelligence brief — applied only with your approval

```
/octave:ads-resonance         # Auto-detects the best available data source
```

### /octave:deal-coach
Methodology-driven deal coaching built around Resonate → Elevate → Compel:
- Role play with stage-specific coaching agents and scored conversations
- Coaching microsites as self-contained HTML
- Coaching decks walking through the framework for a specific deal
- Interactive quizzes with deal-grounded scenarios
- Stage inference from CRM data, findings, and activity patterns
- Talking points grounded in the buyer's own verbatim words, pulled across every call with the account

```
/octave:deal-coach                                        # Interactive — picks mode and stage
/octave:deal-coach acme.com                               # Ground coaching in a specific deal
/octave:deal-coach --mode roleplay                        # Jump to role play
/octave:deal-coach acme.com --mode microsite --stage compel  # Specific mode + stage
/octave:deal-coach --mode quiz --stage resonate           # Quiz on Resonate methodology
/octave:deal-coach acme.com --mode deck --stage elevate   # Coaching deck for Elevate
```

### /octave:deck
Build Octave-powered HTML presentations with brand styling:

```
/octave:deck "pitch for Acme Corp"                          # Customer pitch
/octave:deck "Q1 QBR for enterprise segment"                # QBR with real data
/octave:deck --for competitive "vs Gong"                     # Competitive deck
/octave:deck ~/Downloads/existing-deck.pptx                  # Convert PPTX to HTML
/octave:deck "demo day pitch" --style octave-brand           # Specific style preset
```

### /octave:champion-deal-room
Internal deal room a rep hands a champion so they can run the buying-committee sell:
- Quantified business case built from real deal data
- Stakeholder map with per-seat talking points
- Objection handling and a concrete path to yes
- Self-contained HTML — shareable inside the account

```
/octave:champion-deal-room acme.com
/octave:champion-deal-room acme.com --champion jane@acme.com
```

### /octave:asset-manager
Publish and manage hosted assets on the Octave assets service:
- Cache-aware: lists existing assets before creating and offers matches (with links) so the same work isn't done twice
- Upload local HTML sites, docs, or file bundles (interactive identifier + privacy intake — only_me / workspace / public)
- Update published files or metadata; move assets up or down the privacy ladder
- Create share links for specific emails or whole domains (never expire by default); add/remove recipients, revoke
- Persistent per-project registry of everything published (URLs, share links, status)

```
/octave:asset-manager publish ./use-cases-site   # Publish a folder
/octave:asset-manager share acme-use-cases       # Create/manage share links
/octave:asset-manager update acme-use-cases      # Replace files or metadata
/octave:asset-manager list                       # What have I published?
```

File uploads go through bundled curl scripts (`skills/asset-manager/scripts/`); metadata, shares, and tokens go through the `asset_*` MCP tools.


## Configuration

### MCP Server Setup

1. Add the Octave MCP server (one connection per project):
```bash
   claude mcp add octave-acme --transport http <url>
```

2. Skills detect the Octave MCP server from your available tools. No config file is required.

### Authentication

Authentication is handled via OAuth at the MCP server level. No API keys are stored in the plugin configuration.

## MCP Tools

The plugin uses the single Octave MCP server you configure (e.g. `octave-acme`). Call tools by name (e.g. `verify_connection()`, `get_entity(...)`, `list_entities(...)`).

### Connection
- `verify_connection` - Verify workspace connection and authentication status

### Library Read
- `list_entities` - List entities by type; slim rows by default, `includeDetails: true` for full data, plus `search`, `all`, and pagination
- `get_entity` - Full entity details
- `list_revisions` - List version history for library entities
- `get_revision` - Get a specific historical revision of an entity
- `search_knowledge_base` - Semantic search
- `ask_octave` - Natural-language questions over the typed knowledge graph (entities, events, findings, opportunities)

### Workspace Skills (managed)
Octave-hosted skill folders (Anthropic Agent Skills structure: root `SKILL.md` + optional bundled files) that teach agents reusable methods. Distinct from this plugin's own Claude Code skills — these live in your Octave workspace and are retrieved by agents at generation time. Draft skills are invisible to agents until published. All members can read skills; create/update/delete require a workspace owner.
- `find_skill` - Resolve a task to the best-fitting published skill (returns name + description + confidence; empty result = proceed without a skill)
- `list_skills` - List skills (name + description only — progressive disclosure L1)
- `get_skill` - A skill's SKILL.md instruction body + bundled-file listing (L2)
- `get_skill_file` - Fetch one bundled file's content on demand (L3)
- `create_skill` - Create a skill: authored (name/description/body), import (URL or text → drafted SKILL.md), or from_examples (example outputs → drafted SKILL.md); lands as a draft
- `update_skill` - Update frontmatter/body/publish state (publishing makes it agent-discoverable)
- `delete_skill` - Delete a skill and its stored folder

### Library Write
- `create_entity` - Create new entity (AI-generated) - excludes legacy playbooks
- `update_entity` - Update entity (AI-refined) - excludes legacy playbooks
- `delete_entity` - Delete any entity type (soft delete)
- `link_entities_to_offering` - Link or unlink library entities (personas, segments, competitors, proof points, references, etc.) to a specific offering. Drives which entities appear in each Motion's matrix.

### Motions
- `list_motions` - List all Motions in the workspace
- `get_motion` - Full details for a Motion
- `create_motion` - Create a new Motion for an offering + motion type (`NET_NEW`, `UPSELL`, `CROSS_SELL`, `CONVERT_FREE_TO_PAID`, `RENEW_AND_RETAIN`, `DISPLACE_INCUMBENT`); auto-creates the Default Motion Playbook
- `update_motion` / `delete_motion`
- `list_motion_playbooks` / `get_motion_playbook` - Browse Motion Playbooks (Default + Custom) under a Motion
- `create_motion_playbook` - Create a Custom Motion Playbook with narrative type `THEMATIC`, `MILESTONE`, `ACCOUNT`, or `COMPETITIVE`
- `update_motion_playbook` / `delete_motion_playbook`
- `list_motion_icps` - List Motion ICP cells (persona × segment) for a Motion
- `find_motion_icp` - Full Motion ICP narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus optional Learning Loop learnings and Beats report context

### Legacy Playbook Tools (deprecated)
Still available for workspaces operating on legacy standalone playbooks, but Motions and Motion Playbooks supersede them for new work. Use `/octave:audit --migrate` to translate.
- `get_playbook` - Get a legacy playbook with linked personas, segments, and value props
- `list_value_props` - List value props on a legacy playbook
- `create_playbook` / `update_playbook` - Manage legacy playbooks (avoid for new work)
- `add_value_props` / `update_value_props` - Manage value props on a legacy playbook

### Configuration
- `list_writing_styles` - List all writing style configurations

> Brand voices are retrieved via the generic entity tool: `list_entities({ entityType: "brand_voice" })`.

### Resources
- `list_resources` - List global resources (documents, websites) with filtering
- `get_resource` - Get detailed resource information by oId
- `create_resource` - Create a new resource (text, file, URL, or Google Drive)
- `delete_resource` - Delete one or more resources
- `search_resources` - Semantic search across global resources

### Research
- `find_person` / `find_company` - Search people/companies
- `find_similar_people` / `find_similar_companies` - Lookalike search
- `enrich_person` / `enrich_company` - Detailed intelligence
- `qualify_person` / `qualify_company` - ICP scoring
- `resolve_profile_from_email` / `resolve_email_from_profile` - Resolve a profile from an email (and vice versa)
- `scrape_website` - Scrape and extract structured content from a URL
- `deep_web_research` - Multi-source web research on a person, company, or topic

### Content Generation
- `generate_email` - Generate email sequences
- `generate_content` - Generate various content types
- `generate_call_prep` - Generate call preparation materials

### Events & Analytics
- `list_events` - Search calls, emails, deals
- `list_findings` - Aggregate extracted insights
- `get_event_detail` - Get detailed event info with transcript/content
- `search_call_transcripts` - Semantic + keyword search over indexed call transcripts. Returns verbatim, speaker-attributed moments grouped per call, with `recordingUrl` + `startSec` time anchors and live-hydrated linked CRM opportunities (current stage). Filterable by company, persona (`attributedPersonaOIds`), speaker side (customer vs. rep), deal outcome (WON/LOST/OPEN), sentiment, and date range. `list_findings` is the pipeline's paraphrased insight; this is the raw conversation it came from — requires `CAN_ANALYTICS` and indexed transcripts (per-workspace backfill)
- `get_entity_evidence` - Best verbatim call quotes evidencing one library entity (persona, competitor, objection, use case, proof point). Prefers pipeline-linked moments, falls back to semantic search on the entity name — the entity-anchored composition of `list_findings` and `search_call_transcripts`

### GTM Reports
Narrative GTM analyses (GTM Explorer / Beats).
- `list_gtm_reports` - List available GTM Explorer report groups
- `get_latest_gtm_report` - Get the most recent report (digest across configs in a group)
- `get_report_run` - Get the full content of a specific report run (title, summary, sections)

### Suggestions
Proposed library changes (add / edit / merge) from conversation findings, queued for human review.
- `list_suggestions` - List entity suggestions (defaults to pending, last 14 days)
- `get_suggestion` - Preview a suggestion in full (proposed entity + current-vs-after diff)
- `accept_suggestion` / `reject_suggestion` - Apply or dismiss a pending suggestion
- `create_suggestion` - Queue a new pending suggestion (does NOT apply directly)
- `update_suggestion` - Revise a pending suggestion via natural-language instructions

### Workspace Company
The workspace's own company profile (singleton).
- `get_workspace_company` - Get the workspace company (null if not yet bootstrapped)
- `update_workspace_company` - Update workspace company fields (description, positioning, etc.)

### CRM
- `find_crm_records` - Search for CRM records (accounts, contacts, leads, opportunities)
- `find_crm_activities` - Fetch activities (notes, tasks, calls, emails) for a CRM record
- `generate_crm_context` - Generate synthesized CRM context summary for a person or company
- `get_crm_entity_schema` - Introspect valid fields/properties on a CRM entity (discover field names before requesting them)

### Pipeline Analytics
- `list_pipeline_overview` - Deals grouped by stage with counts, total value, and per-deal detail
- `list_deal_health` - Assess open deals for stalled stages, expired close dates, single-threading, regressions
- `get_deal_deep_dive` - Full deal context: stage history, close-date changes, activity, benchmarks, competitive intel
- `get_pipeline_metrics` - Stage velocity, cycle time, win/loss conversion rates, deal counts

### Agents
- `list_agents` - List saved agents
- `create_agent` - Create a saved agent
- `update_agent` - Update a saved agent
- `get_agent` - Get a saved agent by oId
- `delete_agent` - Delete a saved agent
- `run_email_agent` - Run email sequence agent
- `run_content_agent` - Run content agent
- `run_call_prep_agent` - Run call prep agent
- `run_enrich_person_agent` - Run person enrichment agent
- `run_enrich_company_agent` - Run company enrichment agent
- `run_qualify_person_agent` - Run person qualification agent
- `run_qualify_company_agent` - Run company qualification agent

### Assets
- `asset_generate_access_token` - Mint the per-user access token used by the upload/download scripts (rotates the previous one)
- `asset_refresh_access_token` - Rotate the access token (e.g. after a 401)
- `assets_list` - List your assets and your workspace's assets, with status/privacy filters
- `asset_get_by_id` - Get one asset by uuid
- `asset_update` - Update metadata: identifier, description, entry point, privacy (only_me/workspace/public), status, vanity slug (pretty `/s/<handle>/<slug>/` URL)
- `asset_delete` - Permanently delete an asset and its files
- `asset_share_create` - Create a share link for a non-public asset (emails and/or domains; never expires unless set; the returned URL is shown only once)
- `asset_shares_list` - List an asset's share links
- `asset_share_revoke` - Revoke a share link (cuts active sessions)
- `asset_share_add_recipients` / `asset_share_remove_recipients` - Manage a share's email allowlist
- `asset_share_add_domains` / `asset_share_remove_domains` - Manage a share's domain allowlist
- `asset_versions_list` - List an asset's immutable file versions (every file update mints one)
- `asset_version_restore` - Roll the served files back to a version (instant repoint; newer versions stay restorable)
- `asset_version_delete` - Delete an old version to free storage (the current version can't be deleted)
- `asset_stats_get` - Per-day unique visit and download counts for an asset (owner-only)
- `asset_visitors_list` - Identified viewers: verified share recipients and workspace members (anonymous public visits are counted, never named)
- `asset_access_requests_list` - Cross-asset access-request inbox (filter by status; pending = needs action)
- `asset_access_request_grant` - Grant a request by minting a single-recipient share (the returned URL is shown only once; no email is sent)
- `asset_access_request_dismiss` - Dismiss a request ("not now" - the requester can re-request)

## Directory Structure

```
.
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata (this repo root IS the octave plugin)
│   └── marketplace.json         # Marketplace config — publishes the root plugin as octave@lfgtm
├── .claude/
│   └── settings.json            # Project settings
├── .github/
│   └── workflows/               # CI: sync-downstream (Codex/Cursor mirrors), claude-tag zip
├── docs/
│   └── org-instructions/        # Recommended Claude org preferences for Octave-first routing
├── agents/
│   ├── asset-manager.md         # Hosted asset publishing/sharing agent
│   ├── octave-assistant.md      # General GTM assistant agent
│   ├── octave-editorial-reviewer.md     # Review-gate agent: language + information quality
│   ├── octave-presentation-reviewer.md  # Review-gate agent: visual + structural quality
│   ├── pmm-strategist.md        # Product marketing strategist agent
│   ├── sdr-coach.md             # SDR coaching agent
│   └── revenue-strategist.md    # Revenue strategy advisor agent
├── scripts/                     # Runtime helpers (resolved via ${CLAUDE_PLUGIN_ROOT}) + repo CI tooling
│   ├── deploy.sh                # Deploy a generated deck or page to Vercel
│   ├── export-pdf.sh            # Export an HTML presentation to PDF
│   ├── extract-pptx.py          # Extract content from .pptx for /octave:deck
│   ├── build-codex.sh           # CI: generate the Codex plugin artifact
│   └── build-cursor.sh          # CI: generate the Cursor plugin artifact
├── skills/                      # Skill definitions (each: SKILL.md + optional references/)
│   ├── shared/                  # Cross-skill reference layer (editorial & information rules, presentation principles, review protocol, entity model, style presets, formats/) — not a skill
│   ├── abm/                     # Account-based planning
│   ├── ads/                     # Ad campaign builder
│   ├── ads-resonance/           # Ad performance resonance loop + prediction cards
│   ├── asset-manager/           # Publish & manage hosted assets (bundled upload/download scripts)
│   ├── audit/                   # Library health check
│   ├── battlecard-doc/          # Interactive HTML competitive battlecard
│   ├── call-analyzer/           # Conversation analysis
│   ├── champion-deal-room/      # Champion-facing internal deal room (HTML)
│   ├── deal-coach/              # Deal coaching (Resonate/Elevate/Compel)
│   ├── deck/                    # Presentation builder (HTML)
│   ├── generate/                # Quick content generation
│   ├── get-brand-components/    # Brand kit capture for on-brand documents
│   ├── icp-refine/              # ICP refinement
│   ├── insights/                # Field intelligence
│   ├── library/                 # Library CRUD
│   ├── meeting-prep/            # Meeting battle plan (HTML)
│   ├── microsite/               # ABM microsite (HTML)
│   ├── one-pager/               # One-pager / leave-behind (HTML)
│   ├── pipeline/                # Deal coaching
│   ├── positioning/             # Positioning system (HTML)
│   ├── product-launch/          # Launch planning
│   ├── proposal/                # Business case / proposal (HTML)
│   ├── prospector/              # Prospect discovery
│   ├── qual-doctor/             # Qualification agent tuning
│   ├── research/                # Research & prep
│   ├── signals/                 # Morning intelligence briefing
│   ├── train/                   # Sales training & role-play
│   └── win-loss-report/         # Visual win/loss analysis (HTML)
├── EXAMPLES.md                  # Detailed usage examples
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT - See [LICENSE](LICENSE)
