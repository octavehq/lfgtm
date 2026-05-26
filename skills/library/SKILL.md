---
name: library
description: Browse, search, create, and update Octave library entities (personas, products, segments, competitors, proof points, references) and Motions / Motion Playbooks / Motion ICP cells. Use when user says "show my personas", "list products", "create a competitor", "update this segment", "search the library", "list motions", "show the motion ICP for [persona]", or references any entity type by name.
---

# /octave:library - Library Management

Browse, search, create, and update Octave library entities.

## Trigger

User runs `/octave:library` with subcommands:
- `/octave:library list <type>` - List entities of a type
- `/octave:library search <query>` - Semantic search across library
- `/octave:library show <oId>` - Show full entity details
- `/octave:library create <type> "<name>"` - Create new entity
- `/octave:library update <oId>` - Update existing entity

Or natural language like:
- "Show me all personas"
- "What Motions do we have?" (or, for legacy workspaces, "What playbooks do we have?")
- "Create a new persona for CTOs"
- "Update the enterprise segment"

## Instructions

**Entity Type Mapping:**

```yaml
# Library entities
personas:        { prefix: pe_ }
products:        { prefix: px_ }
services:        { prefix: px_ }  # Services share the product prefix
segments:        { prefix: sg_ }
use-cases:       { prefix: uu_ }
competitors:     { prefix: cp_ }
proof-points:    { prefix: pp_ }
references:      { prefix: re_ }
brand-voices:    { prefix: bv_ }
writing-styles:  { prefix: ws_ }

# Motions and Motion Playbooks (Motion era)
motions:         { prefix: mo_ }   # Motion
motion-playbooks:{ prefix: mp_ }   # Motion Playbook (Default + Custom)
motion-icps:     { prefix: mi_ }   # Motion ICP cells (persona × segment narratives)

# Other common oId prefixes
agents:          { prefix: ca_ }   # ContentAgent - all agent types
workspaces:      { prefix: wa_ }   # Workspace
organizations:   { prefix: og_ }   # Organization

# Legacy (deprecated, still readable for back-compat)
# Note: `playbooks` is the legacy standalone Playbook entity type.
# Motions / Motion Playbooks / Motion ICPs (above) are the modern primitives — prefer them for any new work.
playbooks:       { prefix: pb_ }
value-props:     { prefix: hy_ }
```

### Subcommand: list

List entities of a specific type.

**Usage:**
```
/octave:library list personas
/octave:library list products
/octave:library list motions
/octave:library list motion-playbooks --motion mo_abc123
/octave:library list motion-icps --motion mo_abc123
```

**Actions:**
- For library entities: use `list_all_entities` for quick overview (default), or `list_entities` with pagination for detailed view (--detailed flag)
- For Motions: use `list_motions`
- For Motion Playbooks under a Motion: use `list_motion_playbooks({ motionOId })` — returns the Default Motion Playbook plus any Custom Motion Playbooks
- For Motion ICP cells (the persona × segment matrix) under a Motion: use `list_motion_icps({ motionOId })`

**Entity Types:**
- `personas` / `persona`
- `products` / `product`
- `segments` / `segment`
- `use-cases` / `use_case`
- `competitors` / `competitor`
- `proof-points` / `proof_point`
- `references` / `reference`
- `services` / `service`
- `brand-voices` / `brand-voice`
- `writing-styles` / `writing-style`
- `motions` (Motion-era top-level container)
- `motion-playbooks` (Default + Custom playbooks under a Motion)
- `motion-icps` (persona × segment narrative cells under a Motion)

**Output Format:**
```
Personas (5 total)
==================

1. CTO - Enterprise Tech
   oId: pe_abc123
   Updated: 2026-01-15

2. VP of Engineering
   oId: pe_def456
   Updated: 2026-01-20

3. Director of Platform
   oId: pe_ghi789
   Updated: 2026-01-22

...

Use /octave:library show <oId> for full details.
```

**Output Format (Motions):**
```
Motions (3 total)
=================

1. Enterprise Outbound — Platform
   oId: mo_abc123
   ICP cells: 6 (3 personas × 2 segments)
   Motion Playbooks: 1 Default + 2 Custom

2. PLG Activation — Self-Serve
   oId: mo_def456
   ICP cells: 4
   Motion Playbooks: 1 Default

...

Use /octave:library list motion-playbooks --motion mo_abc123 for the playbook list under a Motion.
Use /octave:library list motion-icps --motion mo_abc123 to see the persona × segment matrix.
```

### Subcommand: search

Semantic search across the library.

**Usage:**
```
/octave:library search "pain points for engineering leaders"
/octave:library search "security compliance" --type persona
```

**Actions:**
- Use MCP tool: `search_knowledge_base`
- Optionally filter by entity type using the `entityTypes` parameter

**Output Format:**
```
Search Results: "pain points for engineering leaders"
=====================================================

1. [Persona] VP of Engineering (pe_def456)
   Relevance: High
   Snippet: "Key pain points include developer velocity,
   technical debt management, and platform reliability..."

2. [Use Case] Developer Productivity Platform (uu_abc123)
   Relevance: Medium
   Snippet: "Addresses the challenge of tool sprawl and
   context switching that impacts engineering teams..."

Use /octave:library show <oId> for full details.
```

For Motion-era narrative content (Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References), drill into Motion ICP cells directly via `find_motion_icp` — search across these narratives is best done by first listing the relevant Motion's ICP cells and then inspecting them.

### Subcommand: show

Display full details for an entity.

**Usage:**
```
/octave:library show pe_abc123
/octave:library show mp_xyz789      # Motion Playbook (full details)
/octave:library show mi_xyz789      # Motion ICP cell (full persona × segment narrative)
```

**Actions:**
- For library entities (personas, products, segments, etc.): use `get_entity`
- For a Motion Playbook (Default or Custom): use `get_motion_playbook`
- For a Motion ICP cell (persona × segment narrative): use `find_motion_icp` (pass `includeLearnings: true` to include Learning Loop learnings)

**Output Format:**
```
Persona: CTO - Enterprise Tech
==============================
oId: pe_abc123
Created: 2026-01-10
Updated: 2026-01-15
Status: Active

## Description
Senior technology executive responsible for technical strategy
and engineering organization at enterprise companies...

## Pain Points
- Managing technical debt while delivering new features
- Balancing innovation with operational stability
- Attracting and retaining top engineering talent
- Security and compliance requirements

## Key Objectives
- Modernize technology stack
- Improve developer productivity
- Reduce operational costs
- Accelerate time to market

## Primary Responsibilities
- Technical strategy and roadmap
- Engineering team leadership
- Vendor and technology selection
- Budget management

---
Use /octave:library update pe_abc123 to modify this persona.
```

### Subcommand: create

Create a new library entity.

**Usage:**
```
/octave:library create persona "VP of Product"
/octave:library create motion-playbook "Q1 Outbound — Cost Pressure" --motion mo_abc123 --narrative-type THEMATIC --sources "https://..."
```

**Note on Motions vs Motion Playbooks:**

A **Motion** is the top-level container for a go-to-market motion (e.g., "Enterprise Outbound — Platform"). Creating a Motion is done in the Motion builder UI — it automatically generates a **Default Motion Playbook** covering the persona × segment matrix as Motion ICP cells. Once a Motion exists, this skill can layer **Custom Motion Playbooks** on top for specific angles (Thematic, Milestone, Account, Competitive).

**Interactive Flow for Custom Motion Playbooks:**

Custom Motion Playbooks always sit under an existing Motion and have a narrative type.

1. **List available Motions:**
   ```
   list_motions()
   ```

2. **Ask user to select a Motion:**
   ```
   Which Motion is this Custom Motion Playbook layered on?

   1. Enterprise Outbound — Platform (mo_abc123)
   2. PLG Activation — Self-Serve (mo_def456)
   3. Renewal & Expansion — Tier 1 (mo_ghi789)

   Your choice:
   ```

3. **Ask for the narrative type:**
   ```
   What narrative type fits this Motion Playbook?

   1. THEMATIC — built around a theme, trend, or shared pain (e.g., "Q1 Cost Pressure")
   2. MILESTONE — built around an event or trigger (e.g., "Post-Funding Outreach")
   3. ACCOUNT — built around a specific named account or tight account list
   4. COMPETITIVE — built around displacing a specific competitor

   Your choice:
   ```

4. **Gather Motion Playbook details:**
   ```
   Creating Custom Motion Playbook: "Q1 Outbound — Cost Pressure"
   Under Motion: [Selected Motion]
   Narrative type: THEMATIC

   Please provide details to generate this Motion Playbook:

   1. What's the angle (theme / milestone / account / competitor)?
   2. Which personas / segments from the Motion ICP matrix does this lean into?
   3. Any supporting context, proof, or competitive framing?
   4. Any source materials? (URLs or text to inform generation)
   ```

5. **Call `create_motion_playbook`:**
   ```
   create_motion_playbook({
     motionOId: "mo_abc123",
     narrativeType: "THEMATIC",
     name: "Q1 Outbound — Cost Pressure",
     instructions: "<detailed instructions from user input>",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

6. **Report success:**
   ```
   Created Custom Motion Playbook: Q1 Outbound — Cost Pressure
   oId: mp_new123
   Under Motion: Enterprise Outbound — Platform (mo_abc123)
   Narrative type: THEMATIC

   The Motion Playbook has been generated and saved.
   Use /octave:library show mp_new123 to view the full details.
   ```

**Interactive Flow for Other Entities:**

1. **Gather basic info:**
   ```
   Creating new persona: "VP of Product"

   Please provide details to generate this persona:

   1. What industry or company type? (e.g., B2B SaaS, Enterprise Tech)
   2. What are their main responsibilities?
   3. Any specific pain points or priorities to focus on?
   4. Any source materials? (URLs or text to inform generation)
   ```

2. **Confirm and create:**
   ```
   I'll create a VP of Product persona with:
   - Focus: B2B SaaS companies
   - Key responsibilities: Product strategy, roadmap, GTM alignment
   - Pain points: Prioritization, cross-functional alignment, metrics

   Proceed? (yes/no)
   ```

3. **Call `create_entity`:**
   ```
   create_entity({
     entityType: "persona",
     name: "VP of Product",
     instructions: "<detailed instructions from user input>",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

4. **Report success:**
   ```
   Created persona: VP of Product
   oId: pe_new123

   The persona has been generated and saved to your library.
   Use /octave:library show pe_new123 to view the full details.
   ```

### Subcommand: update

Update an existing entity.

**Usage:**
```
/octave:library update pe_abc123
/octave:library update pe_abc123 --instructions "Add focus on AI/ML adoption"
```

**Interactive Flow:**

1. **Fetch current entity:**
   ```
   Fetching: CTO - Enterprise Tech (pe_abc123)
   ```

2. **Show current state and ask for changes:**
   ```
   Current Persona: CTO - Enterprise Tech

   Key sections:
   - Pain Points: [list current]
   - Objectives: [list current]
   - Responsibilities: [list current]

   What would you like to update?
   (Describe the changes in natural language)
   ```

3. **Confirm changes:**
   ```
   I'll update the CTO persona with:
   - Add AI/ML adoption as a key objective
   - Include "evaluating AI tools" in responsibilities
   - Add "AI readiness" to pain points

   Proceed? (yes/no)
   ```

4. **Apply the update:**

   **For Motion Playbooks** (oId starts with `mp_`), use `update_motion_playbook`:
   ```
   update_motion_playbook({
     motionPlaybookOId: "mp_xyz789",
     instructions: "Sharpen the Strategic narrative for the [persona] × [segment] cell to address security concerns...",
     keyContext: "<any additional context>"
   })
   ```

   `update_motion_playbook` edits the narrative sections (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) inside the Motion Playbook's Motion ICP cells.

   **For other library entities**, use `update_entity`:
   ```
   update_entity({
     entityType: "persona",
     oId: "pe_abc123",
     instructions: "Add AI/ML adoption as a key objective...",
     keyContext: "<any additional context>"
   })
   ```

5. **Report success:**
   ```
   Updated persona: CTO - Enterprise Tech

   Changes applied:
   - Added AI/ML adoption objective
   - Updated responsibilities
   - Added AI readiness pain point

   Use /octave:library show pe_abc123 to see the updated version.
   ```

### Motion / Motion Playbook / Motion ICP Updates (Special Handling)

The Motion era replaces the standalone playbook model. A Motion is the top-level container; under it live one or more Motion Playbooks (a Default Motion Playbook is auto-generated covering the persona × segment matrix, plus any Custom Motion Playbooks). Each Motion Playbook is composed of **Motion ICP cells** — one narrative per persona × segment intersection.

**Structure:**
- **Motion** — top-level container, tied to an offering (product/service) and a motion type (Outbound, PLG, Renewal, etc.)
- **Motion Playbook** — Default (auto-generated) or Custom (THEMATIC / MILESTONE / ACCOUNT / COMPETITIVE)
- **Motion ICP cell** — per persona × segment narrative inside a Motion Playbook: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References

**Decision Logic:**

| User Request | Tools to Use |
|--------------|--------------|
| "Show me all Motions" | `list_motions` |
| "List the playbooks under the Enterprise Outbound motion" | `list_motion_playbooks({ motionOId })` |
| "Show me the full Default Motion Playbook for that Motion" | `get_motion_playbook` |
| "What's in the CTO × Mid-Market cell?" | `find_motion_icp({ motionIcpOId, includeLearnings: true })` |
| "Sharpen the Strategic narrative for the CFO × Enterprise cell" | `update_motion_playbook` |
| "Add a Custom Motion Playbook for displacing [competitor]" | `create_motion_playbook` with `narrativeType: "COMPETITIVE"` |
| "Rework the whole Default Motion Playbook" | `update_motion_playbook` on the Default Motion Playbook |

**Reading flow:**

1. `list_motions()` — find the relevant Motion for the offering / motion type
2. `list_motion_playbooks({ motionOId })` — see Default + any Custom playbooks under it
3. `list_motion_icps({ motionOId })` — see the persona × segment matrix
4. `find_motion_icp({ motionIcpOId, includeLearnings: true })` — full narrative for a cell, plus Learning Loop learnings

**Editing flow:**

Narrative edits (Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, etc.) are all done through `update_motion_playbook`. The tool re-generates affected narrative sections based on your instructions.

```
update_motion_playbook({
  motionPlaybookOId: "mp_xyz789",
  instructions: "Sharpen Strategic narrative and Benefits and impacts for the CFO × Enterprise cell. Emphasize cost-savings framing over efficiency framing. Keep Pains and consequences unchanged.",
  keyContext: "<any supporting context>"
})
```

**Example — Reframing a cell's value narrative:**
```
User: "Make the CFO cell focus more on cost savings"

1. Find the Motion: list_motions()
2. List the Motion's playbooks: list_motion_playbooks({ motionOId: "mo_abc123" })
3. Confirm the cell exists: list_motion_icps({ motionOId: "mo_abc123" })  # check for CFO × <segment> cells
4. Update: update_motion_playbook({
     motionPlaybookOId: "mp_xyz789",
     instructions: "Reframe the CFO × Enterprise cell's Strategic narrative and Benefits and impacts to lead with cost savings rather than efficiency. Leave other cells unchanged."
   })
```

**Example — Adding a Custom Motion Playbook for a new angle:**
```
User: "Add a competitive displacement Motion Playbook for [Competitor] under our Enterprise Outbound motion"

1. Confirm the Motion: list_motions()
2. Create: create_motion_playbook({
     motionOId: "mo_abc123",
     narrativeType: "COMPETITIVE",
     name: "Displace [Competitor] — Enterprise",
     instructions: "Generate a competitive displacement Motion Playbook targeting current [Competitor] customers. Cells should focus on switching pain, ROI of migration, and proof from prior displacements."
   })
```

### Legacy playbooks (deprecated)

The legacy `get_playbook`, `list_value_props`, `create_playbook`, `update_playbook`, `add_value_props`, and `update_value_props` tools remain available for backwards compatibility with workspaces still operating on standalone playbooks. New workflows should prefer the Motion / Motion Playbook / Motion ICP tools above; legacy playbook tools should only be used when explicitly working with a workspace that hasn't migrated to Motions.

## MCP Tools Used

**Important:** Call MCP tools by name (e.g. `get_entity`, `update_entity`, `list_all_entities`).

### Read Operations
- `list_all_entities` - Quick list with basic fields (default for list)
- `list_entities` - Detailed list with pagination (for --detailed flag)
- `get_entity` - Full entity details
- `search_knowledge_base` - Semantic search

### Motion Read Operations
- `list_motions` - All Motions in the workspace
- `list_motion_playbooks` - Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` - Full Motion Playbook details
- `list_motion_icps` - Persona × segment matrix (Motion ICP cells) for a Motion
- `find_motion_icp` - Full Motion ICP cell narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) + Learning Loop learnings

### Write Operations
- `create_entity` - Create new library entity (calls generate endpoints)
- `update_entity` - Update existing library entity (calls refine endpoints)
- `delete_entity` - Delete any library entity (soft delete)
- `create_motion_playbook` - Create a Custom Motion Playbook under an existing Motion with narrative type THEMATIC / MILESTONE / ACCOUNT / COMPETITIVE
- `update_motion_playbook` - Edit Motion Playbook narrative sections across its Motion ICP cells

### Legacy (deprecated)
- `get_playbook`, `list_value_props`, `create_playbook`, `update_playbook`, `add_value_props`, `update_value_props` — retained for workspaces still on standalone playbooks. Prefer the Motion tools above for new work.

### Resource Operations
- `list_resources` - List global resources (documents, websites) with filtering
- `get_resource` - Get detailed resource information by oId
- `create_resource` - Create a new resource (text, file, URL, or Google Drive)
- `delete_resource` - Delete one or more resources
- `search_resources` - Semantic search across global resources

## Error Handling

**Entity Not Found:**
> Entity "[oId]" not found in your library.
>
> This usually means the oId is wrong or the entity was deleted.
> 1. Run `/octave:library list [type]` to see available entities and their oIds
> 2. Check for typos in the oId
> 3. Search by name instead: `/octave:library search [name]`

**Invalid Entity Type:**
> Unknown entity type "[input]".
>
> Valid library types: personas, products, segments, use-cases, competitors, proof-points, references, services, brand-voices, writing-styles
> Valid Motion-era types: motions, motion-playbooks, motion-icps
>
> Check spelling and try again.

**Create/Update Failed:**
> Failed to [create/update] [type]: [error message]
>
> Options:
> 1. Check that all required fields are provided
> 2. Try again with simpler instructions
> 3. Run `/octave:workspace` to verify your connection
