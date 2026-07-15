---
name: library
description: Browse, search, create, and update Octave library entities (personas, products, segments, competitors, proof points, references, objections, alternatives, buying triggers) and Motions / Motion Playbooks / Motion ICP cells. Use when user says "show my personas", "list products", "create a competitor", "update this segment", "search the library", "list motions", "show the motion ICP for [persona]", or references any entity type by name.
argument-hint: "[list|search|show|create|update|history] [<type>|<oId>|\"<query>\"]"
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
- `/octave:library history [<oId>]` - Browse revision history across the library or for a single entity

Or natural language like:
- "Show me all personas"
- "What Motions do we have?" (or, for legacy workspaces, "What playbooks do we have?")
- "Create a new persona for CTOs"
- "Update the enterprise segment"

## Entity Types and oId Prefixes

The canonical entity taxonomy — every entity type, its `entityType` value, and its oId prefix — lives in [entity-model.md](../shared/entity-model.md). Read it to map user language ("proof points", "buying triggers", `mp_xyz789`) to the right type and tool. Highlights:

- **Library entities:** personas (`pe_`), products/services (`px_`), segments (`sg_`), use cases (`uu_`), competitors (`cp_`), alternatives, buying triggers, objections (`oj_`), proof points (`pp_`), references (`re_`), brand voices (`bv_`), writing styles (`ws_`)
- **Motion era:** Motions (`mo_`), Motion Playbooks (`mp_`), Motion ICP cells (`mi_`)
- **Legacy (deprecated, still readable):** standalone playbooks (`pb_`), value props (`hy_`)

## Instructions

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
- For library entities: use `list_entities` for a quick slim overview (default), or `list_entities` with `includeDetails: true` for the detailed view (--detailed flag)
- For Motions: use `list_motions`
- For Motion Playbooks under a Motion: use `list_motion_playbooks({ motionOId })` — returns the Default Motion Playbook plus any Custom Motion Playbooks
- For Motion ICP cells (the persona × segment matrix) under a Motion: use `list_motion_icps({ motionOId })`

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

Present the entity with its key sections (description, pain points, objectives, responsibilities for a persona; the seven narrative sections for a Motion ICP cell), created/updated dates, and a closing pointer:

```
Use /octave:library update <oId> to modify this entity.
```

### Subcommand: create

Create a new library entity.

**Usage:**
```
/octave:library create persona "VP of Product"
/octave:library create motion-playbook "Q1 Outbound — Cost Pressure" --motion mo_abc123 --narrative-type THEMATIC --sources "https://..."
```

Follow the interactive flows in [create-update-flows.md](references/create-update-flows.md):
- **Custom Motion Playbooks** — select the parent Motion, pick a narrative type (`THEMATIC` / `MILESTONE` / `ACCOUNT` / `COMPETITIVE`), gather the angle and sources, then call `create_motion_playbook`. (Motions themselves are created in the Motion builder UI — creating one auto-generates the Default Motion Playbook.)
- **Other entities** — gather generation inputs, confirm, then call `create_entity`.

### Subcommand: update

Update an existing entity.

**Usage:**
```
/octave:library update pe_abc123
/octave:library update pe_abc123 --instructions "Add focus on AI/ML adoption"
```

Follow the interactive flow in [create-update-flows.md](references/create-update-flows.md): fetch the current entity, show its key sections, gather the requested changes in natural language, confirm, then apply:
- oIds starting with `mp_` → `update_motion_playbook` (edits narrative sections inside the playbook's Motion ICP cells)
- all other library entities → `update_entity`

### Motion / Motion Playbook / Motion ICP Handling

The Motion-era model — structure, decision logic, reading flow, editing flow, and worked examples — is documented in [motion-model.md](references/motion-model.md). Read it whenever a request touches Motions, Motion Playbooks, or Motion ICP cells.

### Subcommand: history

Browse the audit trail for library entities — who changed what, when, and what the diff looked like.

**Usage:**
```
/octave:library history                          # recent revisions across the workspace
/octave:library history pe_abc123                # all revisions for one entity
/octave:library history --type persona           # recent revisions, filtered by entity type
/octave:library history --since 2026-04-01       # revisions on or after a date
/octave:library history rv_xyz789 --diff         # full snapshot + diff for one revision
```

**Actions:**
- For a list of revisions: use `list_revisions` with any combination of `entityTypes`, `entityOIds`, `startDate`, `endDate`, `authorOId`, `includeRestored`, `limit`, `offset`. The list returns lightweight summaries (revisionOId, entity, action, author, timestamp) — no field-level diff.
- For a specific revision's full snapshot and diff: use `get_revision({ revisionOId, diffOnly: false })`. Pass `diffOnly: true` to skip the full snapshot and only return the change set.

**Use this when:**
- The user asks "what changed recently?", "who edited this persona?", "show me the history of this segment", "did anyone touch the library last week?"
- You suspect an entity was edited out from under an agent's expectations (e.g. a persona's pain points were rewritten and an email agent is now producing odd copy)
- Auditing — see CLEANUP MODE in `/octave:audit` — wants to know whether stale-looking content is actually stale or was recently revised

### Legacy playbooks (deprecated)

The legacy `get_playbook`, `list_value_props`, `create_playbook`, `update_playbook`, `add_value_props`, and `update_value_props` tools remain available for backwards compatibility with workspaces still operating on standalone playbooks. New workflows should prefer the Motion / Motion Playbook / Motion ICP tools above; legacy playbook tools should only be used when explicitly working with a workspace that hasn't migrated to Motions.

## MCP Tools Used

**Important:** Call MCP tools by name (e.g. `get_entity`, `update_entity`, `list_entities`).

### Read Operations
- `list_entities` - List entities by type; slim rows by default, `includeDetails: true` for full data (--detailed flag), plus `search`, `all`, and pagination
- `get_entity` - Full entity details
- `search_knowledge_base` - Semantic search

### Motion Read Operations
- `list_motions` - All Motions in the workspace
- `list_motion_playbooks` - Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` - Full Motion Playbook details
- `list_motion_icps` - Persona × segment matrix (Motion ICP cells) for a Motion
- `find_motion_icp` - Full Motion ICP cell narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) + Learning Loop learnings

### Revision / Audit Trail Operations
- `list_revisions` - List entity revisions across the workspace; filter by `entityTypes`, `entityOIds`, `startDate`, `endDate`, `authorOId`, `includeRestored`, with `limit` / `offset` paging. Returns lightweight summaries (no field-level diff).
- `get_revision` - Full snapshot + diff for a single revision; pass `diffOnly: true` to skip the snapshot and return only the change set.

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
> Valid library types: personas, products, segments, use-cases, competitors, alternatives, buying-triggers, objections, proof-points, references, services, brand-voices, writing-styles
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
