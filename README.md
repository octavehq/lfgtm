# Octave Claude Code Plugin

Access Octave's GTM knowledge base directly from Claude Code for positioning, research, content generation, and sales enablement.

## About Octave

Octave is a GTM intelligence platform that helps sales and marketing teams centralize positioning, messaging, and go-to-market knowledge. This Claude Code plugin brings Octave's capabilities directly into your development workflow.

## Installation

### Prerequisites

- Claude Code CLI installed ([install guide](https://docs.anthropic.com/en/docs/claude-code))
- Active Claude API key configured
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

## Quick Start

### 1. Configure MCP Server

Add the Octave MCP server (one connection per workspace):

```bash
claude mcp add octave-acme --transport http https://mcp.octavehq.com/mcp?ctx=<context>
```

You can use any name that starts with `octave-` (e.g. `octave-acme`). Skills detect the Octave MCP server from your available tools.

### 2. Start Using Octave Skills
```
/octave:workspace         # Check connection status
/octave:library list      # Browse your library
/octave:research john@acme.com --for discovery  # Prep for a call
```

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
| `/octave:battlecard` | Competitive intelligence — battlecards, displacement, trap questions |

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

### Intelligence & Analytics Skills

| Skill | Description |
|-------|-------------|
| `/octave:insights` | Surface findings, trends, and patterns from calls and emails |
| `/octave:wins-losses` | Analyze won/lost deals for patterns and learnings |
| `/octave:icp-refine` | Refine ICP definitions using deal outcome analysis |
| `/octave:explore-agents` | Browse and run your saved Octave agents |

### Ideation & Content Skills

| Skill | Description |
|-------|-------------|
| `/octave:brainstorm` | Ideation for campaigns, playbooks, lead magnets, CTAs |
| `/octave:repurpose` | Repurpose content for a different audience, persona, or channel |
| `/octave:deck` | Build Octave-powered HTML presentations with brand styling and export |

### Automation Skills

| Skill | Description |
|-------|-------------|
| `/octave:workflow` | Define, run, and manage multi-step GTM workflows |
| `/octave:audit` | Library health check — find gaps, stale content, duplicates |

## Agents

Specialized agent personas for sustained, multi-turn work sessions.

| Agent | Description |
|-------|-------------|
| `octave-assistant` | General GTM assistant with full Octave platform knowledge |
| `pmm-strategist` | Senior PMM focused on positioning, messaging, and launch strategy |
| `sdr-coach` | SDR manager focused on outreach quality, reply rates, and coaching |
| `revenue-strategist` | VP Revenue advisor for pipeline strategy and deal coaching |

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

### /octave:campaign
Plan and generate multi-channel campaign content:
- Email sequences, LinkedIn messages, ad copy, social posts
- Blog posts and landing page copy
- All grounded in playbooks, personas, and proof points
- Campaign strategy with channel plan and timing

```
/octave:campaign "Q1 pipeline push" --persona "CTO"
/octave:campaign "feature launch" --channels email,linkedin,ads,social,blog
/octave:campaign "competitive displacement" --playbook "Enterprise"
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
/octave:abm acme.com --stakeholders 5 --playbook "Enterprise"
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
- Competitive cheat sheets, persona deep-dives, playbook summaries
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
- Orphaned playbooks (no personas linked)
- Stale content (not updated recently)
- Duplicate or overlapping entities
- Broken references

```
/octave:audit                    # Full audit
/octave:audit --type personas    # Focus on personas
/octave:audit --fix              # Interactive fix mode
```

### /octave:brainstorm
GTM ideation engine for:
- Campaign concepts
- Playbook pack generation (cover your TAM)
- Lead magnet ideas
- CTA and offer variations
- Growth experiments

```
/octave:brainstorm campaigns for enterprise
/octave:brainstorm playbook pack
/octave:brainstorm lead magnets for CTOs
```

### /octave:prospector
Find and qualify companies and people matching your ICP:
- Searches using your library's segments and personas as criteria
- Enriches, qualifies, and scores each prospect
- Provides filter suggestions for Apollo, Clay, or LinkedIn Sales Nav

```
/octave:prospector --playbook "Enterprise Sales"
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
- Adherence: Did we follow the playbook?
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

### /octave:deck
Build Octave-powered HTML presentations with brand styling:

```
/octave:deck "pitch for Acme Corp"                          # Customer pitch
/octave:deck "Q1 QBR for enterprise segment"                # QBR with real data
/octave:deck --for competitive "vs Gong"                     # Competitive deck
/octave:deck ~/Downloads/existing-deck.pptx                  # Convert PPTX to HTML
/octave:deck "demo day pitch" --style octave-brand           # Specific style preset
```

## Workflow Templates

Pre-built workflow templates for common multi-step GTM processes:

| Workflow | Description |
|----------|-------------|
| Full Outbound Pipeline | Research → qualify → find contacts → generate email |
| Account-Based Research | Deep research dossier with contact mapping and playbook matching |
| Competitive Deal Prep | Research, competitive positioning, and displacement outreach |
| Persona-Targeted Outreach | Find persona matches across companies, qualify, and generate outreach |
| New Market Entry | Research → ICP → personas → messaging → playbook → outreach |
| Competitive Response | Assess → update positioning → displacement campaign → enablement |
| Deal Acceleration | Account intel → stakeholder mapping → coaching → outreach → meeting prep |
| Quarterly GTM Review | Win/loss → field intel → ICP accuracy → competitive landscape |
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

The plugin uses the single Octave MCP server you configure (e.g. `octave-acme`). Call tools by name (e.g. `verify_connection()`, `get_entity(...)`, `list_all_entities(...)`).

### Connection
- `verify_connection` - Verify workspace connection and authentication status

### Library Read
- `list_all_entities` - Quick list with basic fields
- `list_entities` - Detailed list with pagination
- `get_entity` - Full entity details
- `get_playbook` - Rich playbook with personas and value props
- `list_value_props` - List value props for a playbook
- `search_knowledge_base` - Semantic search

### Library Write
- `create_entity` - Create new entity (AI-generated) - excludes playbooks
- `update_entity` - Update entity (AI-refined) - excludes playbooks
- `delete_entity` - Delete any entity type (soft delete)
- `create_playbook` - Create new playbook with dedicated schema
- `update_playbook` - Update existing playbook
- `add_value_props` - Add value props to playbook
- `update_value_props` - Update/archive value props

### Configuration
- `list_brand_voices` - List all brand voice configurations
- `list_writing_styles` - List all writing style configurations

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

### Content Generation
- `generate_email` - Generate email sequences
- `generate_content` - Generate various content types
- `generate_call_prep` - Generate call preparation materials
- `run_*_agent` - Run saved agents

### Events & Analytics
- `list_events` - Search calls, emails, deals
- `list_findings` - Aggregate extracted insights
- `get_event_detail` - Get detailed event info with transcript/content

### Agents
- `list_agents` - List saved agents
- `run_email_agent` - Run email sequence agent
- `run_content_agent` - Run content agent
- `run_call_prep_agent` - Run call prep agent
- `run_enrich_*_agent` - Run enrichment agents
- `run_qualify_*_agent` - Run qualification agents

## Directory Structure

```
.
├── .claude/
│   └── settings.json            # Plugin settings (MCP permissions)
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata
│   └── marketplace.json         # Marketplace configuration
├── agents/
│   ├── octave-assistant.md      # General GTM assistant agent
│   ├── pmm-strategist.md       # Product marketing strategist agent
│   ├── sdr-coach.md            # SDR coaching agent
│   └── revenue-strategist.md   # Revenue strategy advisor agent
├── skills/                      # Skill definitions
│   ├── abm/SKILL.md            # Account-based planning
│   ├── analyzer/SKILL.md       # Conversation analysis
│   ├── audit/SKILL.md          # Library health check
│   ├── battlecard/SKILL.md     # Competitive intelligence
│   ├── brainstorm/SKILL.md     # GTM ideation
│   ├── campaign/SKILL.md       # Multi-channel campaigns
│   ├── enablement/SKILL.md     # Sales enablement materials
│   ├── explore-agents/SKILL.md # Agent management
│   ├── generate/SKILL.md       # Quick content generation
│   ├── icp-refine/SKILL.md     # ICP refinement
│   ├── insights/SKILL.md       # Field intelligence
│   ├── launch/SKILL.md         # Launch planning
│   ├── library/SKILL.md        # Library CRUD
│   ├── messaging/SKILL.md      # Messaging frameworks
│   ├── pipeline/SKILL.md       # Deal coaching
│   ├── pmm/SKILL.md            # Product marketing content
│   ├── prospector/SKILL.md     # Prospect discovery
│   ├── repurpose/SKILL.md      # Content repurposing
│   ├── research/SKILL.md       # Research & prep
│   ├── wins-losses/SKILL.md    # Deal outcome analysis
│   ├── workflow/SKILL.md       # Workflow engine
│   └── workspace/SKILL.md      # Connection status
├── workflows/                   # Workflow templates
│   ├── account-based-research.workflow.md
│   ├── competitive-deal-prep.workflow.md
│   ├── competitive-response.workflow.md
│   ├── content-sprint.workflow.md
│   ├── deal-acceleration.workflow.md
│   ├── full-outbound-pipeline.workflow.md
│   ├── new-market-entry.workflow.md
│   ├── persona-targeted-outreach.workflow.md
│   └── quarterly-gtm-review.workflow.md
├── EXAMPLES.md                  # Detailed usage examples
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT - See [LICENSE](LICENSE)
