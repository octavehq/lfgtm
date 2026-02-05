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

### Power Skills

| Skill | Description |
|-------|-------------|
| `/octave:audit` | Library health check - find gaps, stale content, duplicates |
| `/octave:brainstorm` | Ideation for campaigns, playbooks, lead magnets, CTAs |
| `/octave:prospector` | Find, enrich, and qualify ICP-fit prospects using your library |
| `/octave:pmm` | Create sales collateral, battlecards, case studies, landing pages |
| `/octave:research` | Context-aware prep for calls, demos, outreach, deal reviews |
| `/octave:analyzer` | Analyze conversations for resonance, adherence, differentiation |

### Intelligence Skills

| Skill | Description |
|-------|-------------|
| `/octave:insights` | Surface findings, trends, and patterns from calls and emails |
| `/octave:wins-losses` | Analyze won/lost deals for patterns and learnings |
| `/octave:explore-agents` | Browse and run your saved Octave agents |

### Utility Skills

| Skill | Description |
|-------|-------------|
| `/octave:repurpose` | Repurpose existing content for a different audience, persona, or channel |

## Skill Details

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
- Searches for prospects using your library's segments and personas as criteria
- Enriches, qualifies, and scores each prospect against your ICP
- Returns qualified prospect lists with fit reasoning and recommended approaches
- Provides filter suggestions for scaling in Apollo, Clay, or LinkedIn Sales Nav

```
/octave:prospector --playbook "Enterprise Sales"
/octave:prospector --similar-to stripe.com
/octave:prospector --company acme.com
```

### /octave:pmm
Product marketing assistant for:
- One-pagers
- Battlecards
- Case studies
- Landing pages
- Sales decks
- Blog posts

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
- Differentiation: Did we effectively position against competitors and alternatives?
- Outputs: Action items, follow-up suggestions, draft responses

```
/octave:analyzer              # Paste content to analyze
/octave:analyzer --type call  # Analyze call transcript
```

### /octave:insights
Surface intelligence from your sales conversations:
- Top objections, pain points, and questions
- What's resonating vs not
- Trends over time
- Library update suggestions based on field data

```
/octave:insights                          # Overview of recent insights
/octave:insights --type objections        # Focus on objections
/octave:insights --period month           # This month's insights
/octave:insights --persona "CTO"          # Insights from CTO conversations
```

### /octave:wins-losses
Analyze deal outcomes to improve win rates:
- Win patterns (what worked)
- Loss patterns (why we're losing)
- Competitor analysis
- Deal deep dives

```
/octave:wins-losses                           # Full win/loss report
/octave:wins-losses --status lost             # Focus on losses
/octave:wins-losses --competitor "Salesforce" # Deals involving competitor
/octave:wins-losses --company acme.com        # Deep dive on specific deal
```

### /octave:explore-agents
Manage and run your saved Octave agents:
- List all agents by type
- View agent configuration
- Run agents with inputs
- Get agent suggestions for tasks

```
/octave:explore-agents                                    # List all agents
/octave:explore-agents list --type email                  # Email agents only
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
/octave:explore-agents suggest "cold email to CTO"        # Get recommendations
```

### /octave:repurpose
Transform existing content for different audiences:
- Accept text, files, or URLs as input
- Repurpose for different personas and/or segments
- Adapt messaging, positioning, and framing for the motion or playbook
- Adjust tone, format, or channel
- Apply brand voice and writing style guidelines

```
/octave:repurpose "Our platform reduces deployment time..."   # From text
/octave:repurpose ./content/whitepaper.md                     # From file
/octave:repurpose https://blog.company.com/launch-post        # From URL
```

## Configuration

### MCP Server Setup

1. Add the Octave MCP server (one connection per project):
```bash
   claude mcp add octave-acme --transport http <url>
```

2. Skills detect the Octave MCP server from your available tools. No config file is required. Use tool names directly (e.g. `verify_connection()`, `get_entity(...)`).

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
│   └── octave-assistant.md      # GTM assistant agent
├── skills/                      # Skill definitions
│   ├── analyzer/SKILL.md
│   ├── audit/SKILL.md
│   ├── brainstorm/SKILL.md
│   ├── explore-agents/SKILL.md
│   ├── generate/SKILL.md
│   ├── insights/SKILL.md
│   ├── library/SKILL.md
│   ├── pmm/SKILL.md
│   ├── prospector/SKILL.md
│   ├── repurpose/SKILL.md
│   ├── research/SKILL.md
│   ├── wins-losses/SKILL.md
│   └── workspace/SKILL.md
├── .gitignore
├── LICENSE
└── README.md
```

## Usage Examples

### Research and Outreach

```
# Research a prospect
/octave:research john@acme.com --for outreach

# Generate an email sequence
/octave:generate email --to "John Smith at Acme" --about "reducing deployment time"
```

### Sales Enablement

```
# Prep for a discovery call
/octave:research "meeting with TechCorp CTO" --for discovery

# Analyze a call transcript
/octave:analyzer --type call
[paste transcript]
```

### Content Creation

```
# Create a battlecard
/octave:pmm battlecard --competitor "Competitor X"

# Create a case study
/octave:pmm case-study
```

### Library Management

```
# Audit your library
/octave:audit

# Browse entities
/octave:library list personas
/octave:library show pe_abc123
/octave:library search "engineering leaders"

# Create new entities
/octave:library create persona "VP of Product"
/octave:library update pe_abc123 --instructions "Add AI adoption focus"
```

### Prospecting

```
# Find ICP-fit companies
/octave:prospector --playbook "Enterprise Sales"

# Find similar companies
/octave:prospector --similar-to stripe.com

# Get filter suggestions for Apollo/Clay
/octave:prospector --segment "Mid-Market SaaS"
```

### Ideation

```
# Brainstorm campaign ideas
/octave:brainstorm campaigns for healthcare segment

# Generate playbook concepts
/octave:brainstorm playbook pack

# Create lead magnet ideas
/octave:brainstorm lead magnets
```

### Field Intelligence

```
# See what objections are coming up
/octave:insights --type objections

# Analyze win/loss patterns
/octave:wins-losses

# Deep dive on a lost deal
/octave:wins-losses --company acme.com
```

### Agent Management

```
# List your saved agents
/octave:explore-agents

# Run an email agent
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com

# Get agent suggestions
/octave:explore-agents suggest "I need to follow up on a stalled deal"
```

## License

MIT - See [LICENSE](LICENSE)
