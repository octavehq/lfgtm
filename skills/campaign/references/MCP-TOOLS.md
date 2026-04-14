# MCP Tools Reference

Tools used by the `/octave:campaign` skill, organized by function.

## Library Context

| Tool | Purpose |
|------|---------|
| `list_all_entities` | List available personas, products, playbooks |
| `get_entity` | Get full entity details (persona, product, competitor) |
| `get_playbook` | Get playbook with value props |
| `list_value_props` | Get value propositions |
| `search_knowledge_base` | Find proof points, references, messaging, objections |
| `list_brand_voices` | Get brand voice for consistency |
| `list_writing_styles` | Get writing style guidelines |

## Content Generation

| Tool | Purpose |
|------|---------|
| `generate_email` | Email sequence generation (supports `sequenceType`: COLD_OUTBOUND, WARM_OUTBOUND) |
| `generate_content` | All other content types — ads, social, blog, landing page, LinkedIn |

## Agent Discovery

| Tool | Purpose |
|------|---------|
| `list_agents` | Check for saved agents that match the campaign context |
