---
name: audit
description: Audit your Octave library for gaps, stale content, duplicates, and inconsistencies
---

# /octave:audit - Library Health Check

Comprehensive audit of your Octave GTM library to identify gaps, stale content, duplicates, and inconsistencies.

## Usage

```
/octave:audit [--type <entity-type>] [--fix]
```

## Options

- `--type <type>` - Focus on specific entity type (personas, playbooks, products, segments, etc.)
- `--fix` - Interactive mode to address issues as they're found
- `--detailed` - Show full details for each issue (default: summary view)

## Instructions

When the user runs `/octave:audit`:

### Step 1: Gather Library State

**Resolve Octave MCP server first:** The Octave MCP server provides tools like `verify_connection`, `get_entity`, `list_all_entities`. From your tool list, get the server name (e.g. `octave-acme`).

**Fetch entities using MCP tools:**

```
1. list_all_entities({ entityType: "persona" })
2. list_all_entities({ entityType: "product" })
3. list_all_entities({ entityType: "playbook" })
4. list_all_entities({ entityType: "segment" })
5. list_all_entities({ entityType: "use_case" })
6. list_all_entities({ entityType: "competitor" })
7. list_all_entities({ entityType: "proof_point" })
8. list_all_entities({ entityType: "reference" })
```

If `--type` is specified, only fetch that type (but still need related types for relationship checks).

### Step 2: Run Audit Checks

Perform the following checks and categorize issues by severity:

#### Coverage Checks (CRITICAL)

**Missing Core Entities:**
- [ ] At least 1 product or service defined
- [ ] At least 1 persona defined
- [ ] At least 1 playbook defined

**Orphaned Playbooks:**
- [ ] Every playbook has at least 1 buyer persona linked
- [ ] Every playbook has a primary product linked
- [ ] Playbooks have value props for their linked personas

**Broken References:**
- [ ] Personas referenced in playbooks exist
- [ ] Products referenced in playbooks exist
- [ ] Use cases referenced exist

#### Completeness Checks (WARNING)

**Personas:**
- [ ] Has pain points defined (not empty)
- [ ] Has key objectives defined
- [ ] Has primary responsibilities defined
- [ ] Has description (>50 chars)

**Playbooks:**
- [ ] Has strategic narrative
- [ ] Has approach angle
- [ ] Has key insights
- [ ] Has qualifying questions
- [ ] Has value props for each linked persona

**Products:**
- [ ] Has description
- [ ] Has key capabilities
- [ ] Has differentiators

**Segments:**
- [ ] Has description
- [ ] Has firmographic characteristics

**Competitors:**
- [ ] Has strengths defined
- [ ] Has weaknesses defined
- [ ] Has differentiation points

**Proof Points:**
- [ ] Has quantified metric/statistic
- [ ] Has source/validation

**References:**
- [ ] Has success metrics
- [ ] Has use case context

#### Freshness Checks (INFO)

- [ ] Entities updated within last 90 days (flag if older)
- [ ] Playbooks reviewed within last 60 days
- [ ] Competitor info updated within last 30 days (competitive intel goes stale fast)

#### Duplicate Detection (WARNING)

**Name Similarity:**
- [ ] Personas with similar names (>80% similarity)
- [ ] Products with similar names
- [ ] Use cases with similar names
- [ ] Segments with overlapping descriptions

**Content Overlap:**
- [ ] Personas with very similar pain points
- [ ] Use cases with near-identical descriptions
- [ ] Playbooks targeting same persona+segment combination

#### Consistency Checks (WARNING)

**Messaging Alignment:**
- [ ] Product differentiators mentioned in related playbooks
- [ ] Persona pain points addressed in playbook value props
- [ ] Proof points support claims made in playbooks

**Taxonomy Health:**
- [ ] Segments have associated use cases
- [ ] Use cases link to products
- [ ] References link to products and use cases

### Step 3: Generate Report

Present findings organized by severity:

```
Library Audit Report
====================
Generated: <timestamp>
MCP Server: <mcpServerName>

Summary
-------
Total Entities: <count>
  - Personas: X
  - Products: X
  - Playbooks: X
  - Segments: X
  - Use Cases: X
  - Competitors: X
  - Proof Points: X
  - References: X

Health Score: X/100

Issues Found: X total
  - Critical: X
  - Warning: X
  - Info: X

---

CRITICAL ISSUES (X)
===================

1. [ORPHAN] Playbook "Enterprise Sales" has no linked personas
   oId: pb_abc123
   Impact: Cannot generate persona-specific messaging
   Fix: Link buyer personas to this playbook

2. [MISSING] No proof points defined
   Impact: Cannot support claims with evidence
   Fix: Add at least 3-5 proof points with metrics

---

WARNINGS (X)
============

1. [INCOMPLETE] Persona "CTO" missing pain points
   oId: pe_def456
   Fields missing: painPoints, keyObjectives
   Fix: Add pain points and objectives

2. [DUPLICATE] Similar personas detected
   - "VP of Sales" (pe_111)
   - "Vice President of Sales" (pe_222)
   Similarity: 92%
   Fix: Consider merging these personas

3. [STALE] Competitor "Acme Corp" not updated in 120 days
   oId: cp_xyz789
   Last updated: 2025-10-01
   Fix: Review and refresh competitive intelligence

---

INFO (X)
========

1. [FRESHNESS] 5 entities not updated in 90+ days
   - Persona "CFO" (95 days)
   - Use Case "Compliance" (102 days)
   - ...

---

Recommendations
===============

1. IMMEDIATE: Link personas to orphaned playbooks
2. HIGH: Add pain points to incomplete personas
3. MEDIUM: Review and merge duplicate entities
4. LOW: Refresh stale content

Run /octave:audit --fix to address issues interactively.
```

### Step 4: Interactive Fix Mode (--fix)

If `--fix` flag is provided, walk through each issue:

```
Issue 1 of 12: [INCOMPLETE] Persona "CTO" missing pain points
oId: pe_def456

Current state:
- Pain Points: (empty)
- Objectives: (empty)
- Description: "Chief Technology Officer..."

Options:
1. Add content now (I'll help you write it)
2. Generate with AI (uses your library context)
3. Skip for now
4. Mark as intentional (won't flag in future)

Your choice:
```

**If user chooses "Generate with AI":**
```
update_entity({
  entityType: "persona",
  oId: "pe_def456",
  instructions: "Add typical CTO pain points and objectives based on the existing library context. Focus on technology leadership challenges, budget management, and digital transformation."
})
```

**If user chooses "Add content now":**
Prompt for the specific content and use `update_entity` to apply.

### Step 5: Duplicate Resolution Flow

When duplicates are detected:

```
Potential Duplicates Detected
=============================

Group 1: Sales Leadership Personas
----------------------------------
A) "VP of Sales" (pe_111)
   Created: 2025-06-01
   Pain Points: 5 defined
   Used in: 3 playbooks

B) "Vice President of Sales" (pe_222)
   Created: 2025-08-15
   Pain Points: 2 defined
   Used in: 1 playbook

Similarity: 92% (based on name and content)

Options:
1. Merge B into A (keep A, archive B, update references)
2. Merge A into B (keep B, archive A, update references)
3. Keep both (they represent different personas)
4. Review side-by-side before deciding

Your choice:
```

**Note:** Actual merging requires manual updates in Octave UI or multiple API calls. The skill should:
1. Recommend which to keep
2. List what needs to be updated
3. Offer to archive the duplicate

## Health Score Calculation

```
Base Score: 100

Deductions:
- Critical issue: -15 points each (max -45)
- Warning: -5 points each (max -30)
- Info: -1 point each (max -10)

Bonuses:
- All entity types have content: +5
- No stale content (>90 days): +5
- All playbooks fully linked: +5

Minimum score: 0
Maximum score: 100
```

**Score Interpretation:**
- 90-100: Excellent - Library is well-maintained
- 70-89: Good - Minor issues to address
- 50-69: Fair - Several gaps need attention
- Below 50: Needs Work - Significant gaps affecting effectiveness

## MCP Tools Used

### Read Operations
- `list_all_entities` - Get all entities of each type
- `get_entity` - Get full details for specific entities
- `get_playbook` - Get playbook with linked personas and value props
- `list_value_props` - Check value prop coverage

### Write Operations (--fix mode only)
- `update_entity` - Fix incomplete entities
- `add_value_props` - Add missing value props

## Examples

### Basic Audit
```
/octave:audit
```
Runs full audit and displays report.

### Focused Audit
```
/octave:audit --type personas
```
Audits only personas (completeness, duplicates, staleness).

### Interactive Fix
```
/octave:audit --fix
```
Runs audit then walks through each issue for resolution.

## Error Handling

**Empty Library:**
> Your library is empty. Start creating entities with /octave:library create.

**API Error:**
> Could not fetch library data. Check your connection and try again.
> If the issue persists, verify your workspace with /octave:workspace.

## Related Skills

- `/octave:library` - Browse and manage individual entities
- `/octave:brainstorm` - Generate ideas to fill gaps
- `/octave:icp-refine` - Refine ICP definitions from deal data
- `/octave:enablement` - Generate enablement content from library
