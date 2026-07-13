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

### Claude Tag (Claude in Slack)

[Claude Tag](https://claude.com/product/tag) lets a whole Slack workspace @-mention Claude in channels. It connects to Octave through an admin-provisioned **access bundle** rather than per-user OAuth, so setup differs from Claude Code:

1. **Create an Octave API key** in Octave under **Settings → API Keys**. Claude Tag credentials are shared by everyone in the bundle's scope, so we recommend a **read-only** key (create one directly, or use the row menu → "Make read-only") unless you want channel members writing to your Library.
2. **Add the credential**: in [claude.ai admin settings](https://claude.ai/admin-settings/claude-tag), open your access bundle → **Credentials → Connect another tool**. Choose credential type **Bearer**, name it "Octave MCP", set **Allowed websites** to `mcp.octavehq.com`, and paste the API key as the token. (The Octave MCP server accepts API keys via `Authorization: Bearer` or an `x-api-key` header.)
3. **Attach the plugins (recommended)**: the credential alone is enough for Claude to reach Octave — it can discover and drive the MCP server ad hoc from a channel. Attaching the plugins upgrades that to a first-class integration and is what we recommend for real rollouts:
   - **`octave-claude-tag`** — a credential-less `.mcp.json` that registers the Octave MCP server (`https://mcp.octavehq.com/mcp`) natively, so the tool list and schemas are loaded up front instead of Claude re-discovering the API every thread — faster, cheaper, and consistent across users. No `ctx` parameter is needed: the API key identifies your workspace, and the bundle's credential is injected at the network layer.
   - **`octave`** — the skills and agents in this repo, which teach Claude *when* and *how* to use those tools well.

   Claude Tag currently only accepts **private repositories** as plugin sources, so you can't point it at this public repo directly. Three ways in, easiest first:

   **Option A — download the ready-made zip (no terminal, no GitHub account):**
   Download [`octave-plugin.zip`](https://github.com/octavehq/lfgtm/releases/download/claude-tag-plugin/octave-plugin.zip) — an upload-ready bundle rebuilt automatically on every change to this repo — and upload it in the bundle's **Plugins** tab. To get updates later, re-download and re-upload the same file. (Don't use GitHub's native "Download ZIP" — it wraps everything in an `lfgtm-main/` folder, so `.claude-plugin/` isn't at the archive root where the console looks for it.)

   **Option B — private mirror in the browser (no terminal):**
   Open GitHub's [repository import](https://github.com/new/import), paste `https://github.com/octavehq/lfgtm.git` as the source, choose your organization as the owner, set visibility to **Private**, and import. Then connect `YOUR_ORG/lfgtm` in the bundle's **Plugins** tab and enable both plugins. (Imports don't auto-sync — to update later, use the CLI sync in Option C, or just switch to the zip flow.)

   **Option C — private mirror via CLI (updatable):**
   ```bash
   gh repo create YOUR_ORG/lfgtm --private
   git clone https://github.com/octavehq/lfgtm.git && cd lfgtm
   git remote add mirror https://github.com/YOUR_ORG/lfgtm.git
   git push mirror main
   ```
   Connect `YOUR_ORG/lfgtm` in the bundle's **Plugins** tab and enable both plugins. To pull future updates: `git pull origin main && git push mirror main`.
4. **Verify**: attach the bundle to a channel and send `@Claude verify your Octave connection`.

The in-app guide (Octave → Settings → API Keys → Connect MCP → **Claude Tag**) walks through the same steps with copy buttons.

> **Note:** `octave-claude-tag` is for externally injected credentials (Claude Tag), which is why it isn't part of the Claude Code install steps above. In Claude Code, keep using `claude mcp add` with your workspace URL as described below — the bare server declaration in `octave-claude-tag` has no credential and no workspace context on its own, so installing it there just produces a failing server.

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
/octave:workspace         # Check connection status
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
| `/octave:workspace` | View current Octave MCP server connection status |
| `/octave:library` | Browse, search, create, and update library entities |
| `/octave:generate` | Quick content generation (emails, LinkedIn messages) |

### Strategy & Messaging Skills

| Skill | Description |
|-------|-------------|
| `/octave:messaging` | Build messaging frameworks, positioning statements, and matrices |
| `/octave:campaign` | Plan and generate multi-channel campaign content |
| `/octave:launch` | Product and feature launch planning with full content kit |
| `/octave:battlecard` | Competitive intelligence — battlecards, displacement, trap questions. Add `--format doc` for an interactive HTML battlecard document |
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
| `/octave:enablement` | Generate sales enablement materials — cheat sheets, objection guides |
| `/octave:pmm` | Create sales collateral — one-pagers, case studies, landing pages |
| `/octave:analyzer` | Analyze conversations for resonance, adherence, differentiation |
| `/octave:train` | Practice selling — role-play simulations, quizzes, guided learning |
| `/octave:deal-coach` | Methodology-driven deal coaching — role-play, microsites, decks, and quizzes around Resonate/Elevate/Compel |

### Intelligence & Analytics Skills

| Skill | Description |
|-------|-------------|
| `/octave:insights` | Surface findings, trends, and patterns from calls and emails |
| `/octave:signals` | Morning intelligence briefing — deals, patterns, and signals demanding attention |
| `/octave:wins-losses` | Analyze won/lost deals for patterns and learnings. Add `--format report` for a visual HTML report with charts |
| `/octave:icp-refine` | Refine ICP definitions using deal outcome analysis |
| `/octave:explore-agents` | Browse and run your saved Octave agents |
| `/octave:qual-doctor` | Diagnose and tune qualification agents — test against known-fit prospects, analyze per-question scoring patterns, and recommend specific changes to questions, weights, and entity descriptions. Handles both score-only and routing+scoring tuning modes. |

### Document Builder Skills

| Skill | Description |
|-------|-------------|
| `/octave:get-brand-components` | Capture a company's brand (fonts, colors, logo, real imagery, components) from its website into a reusable kit — every Document Builder below can render **on-brand** with it; kits can be reused from and hosted to the asset store (asset-manager) |
| `/octave:meeting-prep` | Strategic meeting battle plan with coaching frameworks and talk tracks as HTML |
| `/octave:deck` | Build Octave-powered HTML slide decks with brand styling and export |
| `/octave:one-pager` | Personalized one-pager / leave-behind as self-contained HTML |
| `/octave:brief` | Internal account dossier and call prep HTML document |
| `/octave:proposal` | Formal business case and proposal as customer-facing HTML |
| `/octave:microsite` | Personalized ABM microsite / landing page as HTML |
| `/octave:positioning` | Complete visual Messaging & Positioning system (8 frameworks) as HTML |

Visual battlecards and win/loss reports are document formats of their parent skills: `/octave:battlecard … --format doc` and `/octave:wins-losses --format report`.

### Ideation & Content Skills

| Skill | Description |
|-------|-------------|
| `/octave:brainstorm` | Ideation for campaigns, Custom Motion Playbooks, lead magnets, CTAs |
| `/octave:repurpose` | Repurpose content for a different audience, persona, or channel |

### Automation Skills

| Skill | Description |
|-------|-------------|
| `/octave:workflow` | Define, run, and manage multi-step GTM workflows |
| `/octave:audit` | Library health check — find gaps, stale content, duplicates |

### Publishing Skills

| Skill | Description |
|-------|-------------|
| `/octave:asset-manager` | Publish and manage hosted assets — upload, visibility, private share links, asset registry; checks for existing assets before creating so work isn't duplicated |

## Agents

Specialized agent personas for sustained, multi-turn work sessions.

| Agent | Description |
|-------|-------------|
| `octave-assistant` | General GTM assistant with full Octave platform knowledge |
| `pmm-strategist` | Senior PMM focused on positioning, messaging, and launch strategy |
| `sdr-coach` | SDR manager focused on outreach quality, reply rates, and coaching |
| `revenue-strategist` | VP Revenue advisor for pipeline strategy and deal coaching |
| `asset-manager` | Publish and manage hosted assets: upload, visibility, private share links, persistent registry; cache-aware — reuses existing assets instead of duplicating them |

## Skill Details

### /octave:messaging
Build structured messaging artifacts from your library:
- Messaging frameworks (pillars, proof points, key messages by audience)
- Positioning statements with persona and segment variations
- Messaging matrices (persona x use case grids)
- Elevator pitches (15s / 30s / 60s / 2min)
- Narrative arcs and value prop hierarchies

```
/octave:messaging framework --product "Platform"
/octave:messaging matrix
/octave:messaging elevator
/octave:messaging positioning
```

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

### /octave:campaign
Plan and generate multi-channel campaign content:
- Email sequences, LinkedIn messages, ad copy, social posts
- Blog posts and landing page copy
- All grounded in Motions, Motion ICPs, personas, and proof points
- Campaign strategy with channel plan and timing

```
/octave:campaign "Q1 pipeline push" --persona "CTO"
/octave:campaign "feature launch" --channels email,linkedin,ads,social,blog
/octave:campaign "competitive displacement" --motion "Net New Enterprise"
```

### /octave:launch
Product and feature launch planning with content kit:
- Positioning and messaging by persona
- Channel strategy and timeline
- Content kit: announcement emails, blog, social, one-pager, FAQ, competitive talking points
- Library updates for new capabilities

```
/octave:launch "AI Analytics Dashboard" --type feature
/octave:launch "Enterprise Tier" --type product
/octave:launch "APAC Expansion" --type expansion
```

### /octave:battlecard
Competitive intelligence hub:
- Full competitive battlecards with real conversation evidence
- Displacement campaigns (email sequences for stealing competitor customers)
- Trap questions to expose competitor weaknesses
- Objection counters ("they say X, we say Y")
- Side-by-side comparisons and landscape overviews

```
/octave:battlecard battlecard --competitor "Acme"
/octave:battlecard battlecard --competitor "Acme" --format doc   # Interactive HTML document
/octave:battlecard displacement --competitor "Acme"
/octave:battlecard traps --competitor "Acme"
/octave:battlecard landscape
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

### /octave:enablement
Sales enablement materials:
- Quick reference cards, objection handling guides, discovery question banks
- Competitive cheat sheets, persona deep-dives, Motion ICP cell summaries
- New hire onboarding kits
- All grounded in library data and real conversation evidence

```
/octave:enablement objections --persona "CTO"
/octave:enablement discovery --persona "VP Sales"
/octave:enablement competitive-sheet
/octave:enablement onboarding
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

### /octave:brainstorm
GTM ideation engine for:
- Campaign concepts
- Custom Motion Playbook ideas (Thematic / Milestone / Account / Competitive angles to layer on the Default Motion Playbook)
- Lead magnet ideas
- CTA and offer variations
- Growth experiments

```
/octave:brainstorm campaigns for enterprise
/octave:brainstorm motion playbooks
/octave:brainstorm lead magnets for CTOs
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

### /octave:pmm
Product marketing assistant for collateral:
- One-pagers, battlecards, case studies, landing pages
- Sales decks, blog posts, datasheets, FAQs
- Objection handling guides

```
/octave:pmm one-pager
/octave:pmm battlecard --competitor "Salesforce"
/octave:pmm case-study
```

### /octave:research
Context-aware research and prep:
- Discovery call prep (questions, pain points, qualification)
- Demo prep (use cases, proof points, objections)
- Outreach prep (hooks, angles, personalization)
- Pipeline review (deal health, next moves, risks)

```
/octave:research john@acme.com --for discovery
/octave:research acme.com --for demo
/octave:research "Acme deal" --for pipeline-review
```

### /octave:analyzer
Conversation analysis against your library:
- Resonance: Did messaging land?
- Adherence: Did we follow the Motion ICP narrative?
- Differentiation: Did we position effectively?

```
/octave:analyzer              # Paste content to analyze
/octave:analyzer --type call  # Analyze call transcript
```

### /octave:insights
Surface intelligence from sales conversations:
- Top objections, pain points, and questions
- What's resonating vs not
- Trends over time
- Library update suggestions

```
/octave:insights --type objections
/octave:insights --persona "CTO"
```

### /octave:wins-losses
Analyze deal outcomes to improve win rates:
- Win/loss patterns and competitor analysis
- Deal deep dives

```
/octave:wins-losses
/octave:wins-losses --status lost
/octave:wins-losses --competitor "Salesforce"
/octave:wins-losses --format report   # Visual HTML report with charts
```

### /octave:explore-agents
Manage and run your saved Octave agents:

```
/octave:explore-agents
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
/octave:explore-agents suggest "cold email to CTO"
```

### /octave:workflow
Multi-step GTM workflow engine:
- Run pre-built workflow templates
- Create custom workflows
- Human-in-the-loop execution with decision points

```
/octave:workflow list
/octave:workflow run "Full Outbound Pipeline" --company acme.com
/octave:workflow create
```

### /octave:repurpose
Transform existing content for different audiences:

```
/octave:repurpose "Our platform reduces deployment time..." --persona "CFO"
/octave:repurpose ./content/whitepaper.md --channel "email"
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

### /octave:asset-manager
Publish and manage hosted assets on the Octave assets service:
- Cache-aware: lists existing assets before creating and offers matches (with links) so the same work isn't done twice
- Upload local HTML sites, docs, or file bundles (interactive identifier + visibility intake)
- Update published files or metadata; flip public/private
- Create private share links for specific emails or whole domains; add/remove recipients, revoke
- Persistent per-project registry of everything published (URLs, share links, status)

```
/octave:asset-manager publish ./use-cases-site   # Publish a folder
/octave:asset-manager share acme-use-cases       # Create/manage share links
/octave:asset-manager update acme-use-cases      # Replace files or metadata
/octave:asset-manager list                       # What have I published?
```

File uploads go through bundled curl scripts (`skills/asset-manager/scripts/`); metadata, shares, and tokens go through the `asset_*` MCP tools.

## Workflow Templates

Pre-built workflow templates for common multi-step GTM processes:

| Workflow | Description |
|----------|-------------|
| Full Outbound Pipeline | Research → qualify → find contacts → generate email |
| Account-Based Research | Deep research dossier with contact mapping and Motion ICP matching |
| Competitive Deal Prep | Research, competitive positioning, and displacement outreach |
| Persona-Targeted Outreach | Find persona matches across companies, qualify, and generate outreach |
| New Market Entry | Research → ICP → personas → messaging → Motion → outreach |
| Competitive Response | Assess → update positioning → displacement campaign → enablement |
| Deal Acceleration | Account intel → stakeholder mapping → coaching → outreach → meeting prep |
| Quarterly GTM Review | Win/loss → field intel → ICP accuracy → competitive landscape |
| Positioning Exercise | Library audit → data gathering → generate 8-framework positioning system → save back |
| Content Sprint | Messaging → emails → LinkedIn → blog → social in one sprint |

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
- `assets_list` - List your assets and workspace-shared teammates' assets, with status/visibility filters
- `asset_get_by_id` - Get one asset by uuid
- `asset_update` - Update metadata: identifier, description, entry point, visibility, status, workspace sharing
- `asset_delete` - Permanently delete an asset and its files
- `asset_share_create` - Create a private share link (emails and/or domains; the returned URL is shown only once)
- `asset_shares_list` - List an asset's share links
- `asset_share_revoke` - Revoke a share link (cuts active sessions)
- `asset_share_add_recipients` / `asset_share_remove_recipients` - Manage a share's email allowlist
- `asset_share_add_domains` / `asset_share_remove_domains` - Manage a share's domain allowlist

## Directory Structure

```
.
├── .claude/
│   └── settings.json            # Project settings
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata
│   └── marketplace.json         # Marketplace configuration
├── .github/
│   └── workflows/
│       └── sync-downstream.yml  # Builds and mirrors the Codex and Cursor plugin repos
├── agents/
│   ├── asset-manager.md         # Hosted asset publishing/sharing agent
│   ├── octave-assistant.md      # General GTM assistant agent
│   ├── pmm-strategist.md        # Product marketing strategist agent
│   ├── sdr-coach.md             # SDR coaching agent
│   └── revenue-strategist.md    # Revenue strategy advisor agent
├── docs/
│   └── org-instructions/        # Recommended Claude org preferences for Octave-first routing
├── scripts/
│   ├── build-codex.sh           # Generate the Codex plugin artifact
│   ├── build-cursor.sh          # Generate the Cursor plugin artifact
│   ├── deploy.sh                # Deploy a generated deck or page to Vercel
│   ├── export-pdf.sh            # Export an HTML presentation to PDF
│   └── extract-pptx.py          # Extract content from .pptx for /octave:deck
├── skills/                      # Skill definitions (each: SKILL.md + optional references/)
│   ├── shared/                  # Cross-skill references (entity model, presentation principles, style presets, …) — not a skill
│   ├── abm/                     # Account-based planning
│   ├── ads/                     # Ad campaign builder
│   ├── ads-resonance/           # Ad performance resonance loop + prediction cards
│   ├── analyzer/                # Conversation analysis
│   ├── asset-manager/           # Publish & manage hosted assets (bundled upload/download scripts)
│   ├── audit/                   # Library health check
│   ├── battlecard/              # Competitive intelligence (--format doc for HTML)
│   ├── brainstorm/              # GTM ideation
│   ├── brief/                   # Account dossier (HTML)
│   ├── campaign/                # Multi-channel campaigns
│   ├── deal-coach/              # Deal coaching (Resonate/Elevate/Compel)
│   ├── deck/                    # Presentation builder (HTML)
│   ├── enablement/              # Sales enablement materials
│   ├── explore-agents/          # Agent management
│   ├── generate/                # Quick content generation
│   ├── get-brand-components/    # Brand kit capture for on-brand documents
│   ├── icp-refine/              # ICP refinement
│   ├── insights/                # Field intelligence
│   ├── launch/                  # Launch planning
│   ├── library/                 # Library CRUD
│   ├── meeting-prep/            # Meeting battle plan (HTML)
│   ├── messaging/               # Messaging frameworks
│   ├── microsite/               # ABM microsite (HTML)
│   ├── one-pager/               # One-pager / leave-behind (HTML)
│   ├── pipeline/                # Deal coaching
│   ├── pmm/                     # Product marketing content
│   ├── positioning/             # Positioning system (HTML)
│   ├── proposal/                # Business case / proposal (HTML)
│   ├── prospector/              # Prospect discovery
│   ├── qual-doctor/             # Qualification agent tuning
│   ├── repurpose/               # Content repurposing
│   ├── research/                # Research & prep
│   ├── signals/                 # Morning intelligence briefing
│   ├── train/                   # Sales training & role-play
│   ├── wins-losses/             # Deal outcome analysis (--format report for HTML)
│   ├── workflow/                # Workflow engine
│   └── workspace/               # Connection status
├── workflows/                   # Workflow templates (run via /octave:workflow)
│   ├── account-based-research.workflow.md
│   ├── competitive-deal-prep.workflow.md
│   ├── competitive-response.workflow.md
│   ├── content-sprint.workflow.md
│   ├── deal-acceleration.workflow.md
│   ├── full-outbound-pipeline.workflow.md
│   ├── new-market-entry.workflow.md
│   ├── persona-targeted-outreach.workflow.md
│   ├── positioning-exercise.workflow.md
│   └── quarterly-gtm-review.workflow.md
├── EXAMPLES.md                  # Detailed usage examples
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT - See [LICENSE](LICENSE)
