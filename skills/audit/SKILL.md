---
name: audit
description: Audit your Octave library for gaps, stale content, duplicates, language issues, and strategic design quality. Use when user says "audit my library", "check for gaps", "library health check", "find duplicates", or asks about library quality and completeness.
argument-hint: "[--type <entity-type>] [--fix] [--migrate] [--detailed]"
---

# /octave:audit - Library Health Check

Comprehensive audit of your Octave GTM library. This skill operates as three things:

1. **Gap analyzer** — what's missing that would make agents smarter
2. **Overlap ID'er** — what's redundant or splitting hairs unnecessarily
3. **Strategic thought partner** — push and challenge on design choices

The goal is not just "is the library complete?" but "is the library well-designed for what agents need to do?"

**Core operating principle:** The audit is a coach, not a builder. Push the user to think deeper about their GTM design rather than auto-generating content. Opinions are good — but only the USER's well-considered opinions. More entities isn't better. Better entities are better. The audit's job is to ask the questions that draw out the right design, not to fill templates.

## Usage

```
/octave:audit [--type <entity-type>] [--fix] [--migrate]
```

## Options

- `--type <type>` - Focus on specific entity type (personas, products, segments, motions, etc.)
- `--fix` - Interactive mode to address issues as they're found
- `--detailed` - Show full details for each issue (default: summary view)
- `--migrate` - Legacy playbook → Motions migration mode

## Instructions

When the user runs `/octave:audit`:

### Step 1: Gather Library State

**Resolve Octave MCP server first:** The Octave MCP server provides tools like `verify_connection`, `get_entity`, `list_entities`. From your tool list, get the server name.

**Fetch entities using MCP tools:**

```
1. list_entities({ entityType: "persona" })
2. list_entities({ entityType: "product" })
3. list_entities({ entityType: "segment" })
4. list_entities({ entityType: "use_case" })
5. list_entities({ entityType: "competitor" })
6. list_entities({ entityType: "alternative" })
7. list_entities({ entityType: "buying_trigger" })
8. list_entities({ entityType: "objection" })
9. list_entities({ entityType: "proof_point" })
10. list_entities({ entityType: "reference" })
11. list_entities({ entityType: "playbook" }) — legacy standalone playbooks, if any remain
12. list_motions() — all Motions in workspace
13. For each Motion: list_motion_icps({ motionOId }) — Motion ICP cell state
```

Then use `get_entity` for entities that need deeper inspection (qualifying questions, field completeness), and `find_motion_icp({ motionIcpOId, includeLearnings: true })` for any specific Motion ICP cell you need full narrative context on.

If `--type` is specified, only fetch that type (but still need related types for relationship checks).

**Optional — surface what's changed recently.** When the user is asking about staleness ("what hasn't been touched in a while?", "show me what's been changing"), or you suspect an entity is mid-edit, use the revision tools:

- `list_revisions({ startDate, entityTypes, limit })` — recent edits across the workspace (or filtered by entity type / author). Returns lightweight summaries (no field-level diff).
- `get_revision({ revisionOId, diffOnly: true })` — full diff for a specific revision when you need to know exactly what changed.

This is especially useful in cleanup mode, where staleness (e.g. competitors not updated in 30+ days) and recent churn (e.g. a persona that was rewritten twice last week) are both audit signals.

### Step 2: Determine Mode

After gathering the library state, ask the user:

```
I can see your library has [X] total active entities across [Y] types,
[Z] Motions, and [W] legacy standalone playbooks.

How would you like to approach this?

1. Onboarding review — I'm building this library out. Help me figure out
   what to build next and how to design it for the Motions world.

2. Cleanup audit — This library has been around. Find what's broken,
   redundant, stale, or poorly written. Check my Motions setup too.

3. Legacy playbook → Motions migration — I have old-style playbooks. Help
   me translate my setup to the new world and re-wire my agents.
```

**Auto-detect hints:**
- <10 entities, missing products/personas → default-suggest onboarding
- Legacy playbooks exist but zero Motions → default-suggest migration
- Motions exist, 30+ entities → default-suggest cleanup

Present all three options regardless.

### Step 3: Run the Selected Mode

Each mode has its own reference file with the complete flow — read it and follow it:

| Mode | Reference | What it covers |
|------|-----------|----------------|
| **Onboarding** | [onboarding-mode.md](references/onboarding-mode.md) | Assess what exists, build the 5-tier priority roadmap, run the design challenge pass (personas, segments, Motion architecture, use cases, competitors/alternatives, objections, evidence), light checks on existing content, onboarding report, and Socratic `--fix` flows |
| **Cleanup** | [cleanup-checks.md](references/cleanup-checks.md) | The full check suite — coverage, completeness, Motions readiness, qualifying questions, language & voice, strategic design review, freshness, duplicates, consistency — plus the interactive `--fix` and duplicate-resolution flows |
| **Migration** | [migration-mode.md](references/migration-mode.md) | Gather legacy + Motion state, categorize old playbooks, map them to Default / Custom Motion Playbooks, re-wire agents, coverage summary, and interactive `--fix` build |

For cleanup mode, render the report with [cleanup-report-template.md](references/cleanup-report-template.md) and compute the score per [health-score.md](references/health-score.md).

**Qualifying question tuning is out of scope for the audit.** The audit identifies weight-distribution and fit-type issues (see the Qualifying Questions Audit section in cleanup-checks.md); actual tuning — testing against known-fit prospects and adjusting weights — always routes to `/octave:qual-doctor`.

## MCP Tools Used

### Read Operations
- `list_entities` - Get all entities of each type (quick scan)
- `get_entity` - Get full details for specific entities (qualifying questions, field data, links)
- `get_playbook` - Get a legacy standalone playbook with its linked personas, segments, and value props (migration mode only)
- `list_value_props` - Read value props on a legacy playbook (migration mode only)
- `list_revisions` / `get_revision` - Recent edits and per-revision diffs (staleness vs churn signals)

### Motions Operations
- `list_motions` - Get all Motions in workspace
- `get_motion` - Full details for a Motion
- `list_motion_icps` - List Motion ICP cells for a Motion (shows which persona × segment intersections have narratives)
- `find_motion_icp` - Get full cell narrative for a specific Motion ICP — structured sections (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus optional learnings and report context
- `list_motion_playbooks` - List Motion Playbooks (Default + Custom) under a Motion
- `get_motion_playbook` - Full details for one Motion Playbook

### Offering Linkage
- `link_entities_to_offering` - Link personas, segments, and other entities to an offering (determines what appears in the Motion matrix)

### Agent Operations (migration mode)
- `list_agents` - Get all saved agents with their configurations (offering, motion type, playbook/Motion references)

### Write Operations (--fix mode only)
- `update_entity` - Fix incomplete entities, language issues
- `create_entity` - Create missing entities (onboarding mode)
- `create_motion_playbook` - Create a Custom Motion Playbook (narrative type `THEMATIC`, `MILESTONE`, `ACCOUNT`, or `COMPETITIVE`) during migration
- `update_motion_playbook` - Edit Motion Playbook narrative sections to carry over nuance from a legacy playbook

## Examples

### Basic Audit
```
/octave:audit
```
Runs full audit — asks if you're onboarding, cleaning up, or migrating, then proceeds accordingly.

### Focused Audit
```
/octave:audit --type personas
```
Audits only personas (completeness, duplicates, staleness, role relevance, qualifying question weights).

### Interactive Fix
```
/octave:audit --fix
```
Runs audit then walks through each issue for resolution. In onboarding mode, also offers to walk through design challenges interactively.

### Legacy Playbook Migration
```
/octave:audit --migrate
```
Reads legacy playbooks and existing Motions, categorizes playbooks, maps to new world, re-wires agents.

### Migration with Interactive Build
```
/octave:audit --migrate --fix
```
Same as migration, but walks through each step interactively — comparing legacy playbook nuance to Motion ICP cells, co-creating custom Motion Playbooks, and confirming agent re-wiring.

## Error Handling

**Empty Library:**
> Your library is empty — looks like we're starting fresh. Let me walk you through what to build first.
> (Automatically enters onboarding mode)

**API Error:**
> Could not fetch library data. Check your connection and try again.
> If the issue persists, verify your workspace with /octave:workspace.

## Related Skills

- `/octave:library` - Browse and manage individual entities
- `/octave:qual-doctor` - Deep-dive qualification scoring tuner (test against real prospects, tune weights)
- `/octave:brainstorm` - Generate ideas to fill gaps
- `/octave:icp-refine` - Refine ICP definitions from deal data
- `/octave:enablement` - Generate enablement content from library
