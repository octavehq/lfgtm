---
name: qual-doctor
description: Diagnose and tune qualification agents by testing against known-fit prospects, analyzing per-question scoring patterns, and recommending specific changes to questions, weights, and entity descriptions. Use when user says "tune my qualification", "qual doctor", "fix qualification scores", "qualification isn't working", "scores are off", "tune scoring", or asks to improve how qualification agents score prospects.
argument-hint: "[no args — the skill is fully interactive and walks through agent selection, section picking, test case collection, and diagnosis]"
---

# /qual-doctor - Qualification Agent Tuner

Diagnose why your qualification agent scores prospects the way it does, then tune it with targeted changes to questions, weights, entity descriptions, and rationales. Think of it as a doctor's visit for your qualification setup: examine, diagnose, prescribe, verify.

## Instructions

When the user runs `/qual-doctor`:

### Phase 1: Setup

#### 1a: Resolve MCP Server

The Octave MCP server provides tools like `verify_connection`, `get_entity`, `qualify_person`, `qualify_company`, `run_qualify_person_agent`, `run_qualify_company_agent`. From your tool list, identify the active Octave MCP server name (e.g. `octave-acme`, `octave-octave-clean`).

#### 1b: Determine Execution Mode

Ask: **How do you want to run qualification?**

```
AskUserQuestion({
  questions: [{
    question: "How should I run qualification?",
    header: "Run mode",
    options: [
      { label: "Saved agent (Recommended)", description: "Use a specific qualification agent — tests exact production config including which sections are active" },
      { label: "Raw qualify tool", description: "Use qualify_person/qualify_company directly — tests against your full library" }
    ],
    multiSelect: false
  }]
})
```

**If "Saved agent":**
1. List qualification agents for BOTH types:
   ```
   list_agents({ type: "QUALIFY_COMPANY" })
   list_agents({ type: "QUALIFY_PERSON" })
   ```
2. Present the combined list — the agent type determines person vs company mode.
3. User picks one. Then fetch full config:
   ```
   get_agent({ oId: "<selected_agent_id>" })
   ```

**If "Raw qualify tool":**
Ask person or company mode:
```
AskUserQuestion({
  questions: [{
    question: "Are you tuning qualification for people or companies?",
    header: "Qual type",
    options: [
      { label: "Company", description: "Tune how companies are scored (qualify_company)" },
      { label: "Person", description: "Tune how individuals are scored (qualify_person)" }
    ],
    multiSelect: false
  }]
})
```

#### 1c: Display Agent/Tool Config

For saved agents, parse `data.commonContext.entities.{type}.strategy` and `data.scoringContext` to show active sections:

```
QUAL DOCTOR SETUP
=================
Mode:       Company qualification
Run via:    "Qualify Company Agent" (ca_xxx)
Model:      PULSE
Sections:
  Product  → BEST_MATCH (scores, contributes to overall)
  Segment  → BEST_MATCH (scores, contributes to overall)
  Playbook → BEST_MATCH (scores, DOES NOT contribute to overall)
  Persona  → OFF
```

For raw tools, all sections are active by default.

#### 1d: Select Sections to Tune

Ask which section(s) to tune:
```
AskUserQuestion({
  questions: [{
    question: "Which section(s) do you want to tune today?",
    header: "Sections",
    options: [
      { label: "Product/Offering", description: "Tune product-fit scoring (does this company need our product?)" },
      { label: "Segment", description: "Tune segment matching + scoring" },
      { label: "Playbook", description: "Tune playbook ICP matching + scoring" },
      { label: "All active sections", description: "Tune all sections that are enabled" }
    ],
    multiSelect: true
  }]
})
```

Dynamically build the options list from the agent's active sections only — do not show disabled sections. If using raw tools, show all.

#### 1e: Identify Target Entities + Determine Tuning Mode

For each selected section, list the entities in the library:
- Product/Offering → `list_all_entities({ entityType: "product" })`
- Persona → `list_all_entities({ entityType: "persona" })`
- Segment → `list_all_entities({ entityType: "segment" })`
- Playbook → `list_all_entities({ entityType: "playbook" })`

**Determine tuning mode based on entity count:**

- **Single entity** (e.g., 1 product): **Score-only mode** — we're tuning the scoring questions on that one entity. Routing is trivial since there's only one option.
- **Multiple entities** (e.g., 3 personas, 2 segments): **Routing + Scoring mode** — we're tuning both *which entity gets matched* AND *the score it receives*. This is the more common case for personas, segments, and playbooks.

For **Routing + Scoring mode**, show all entities with brief descriptions so the user understands the routing landscape:

```
ENTITIES IN THIS SECTION
=========================
Personas (3 active):
  1. VP of Sales — "Sales leader focused on forecast accuracy and team performance..."
  2. RevOps Leader — "Revenue operations professional responsible for GTM infrastructure..."
  3. SDR Manager — "Frontline manager coaching outbound reps on messaging and pipeline..."

Tuning mode: ROUTING + SCORING
  - We'll test whether the right persona gets matched for each test case
  - AND whether the score is correct once matched
```

Pull each entity's full details via `get_entity` to examine qualifying questions and descriptions across all entities in the section. In Routing + Scoring mode, the user will specify expected entity matches per test case in Phase 2.

#### 1f: Review Current Questions

Display a summary of active qualifying questions (where `archivedAt` is null), grouped by fitType:

```
Current Qualifying Questions for "Your Product" (product)
====================================================

GOOD FIT questions (should answer YES for good fits):
  #1  [HIGH]    "Is the company operating in a B2B motion..."
  #2  [HIGH]    "Does the company have multiple GTM motions..."
  #3  [MEDIUM]  "Does the company actively run outbound..."
  ...

BAD FIT questions (should answer YES for bad fits):
  #12 [INSTANT_DISQUALIFIER] "Is the company an AI tool for GTM..."
  #13 [HIGH]    "Is the company primarily focused on B2C..."
  ...

Summary: 11 GOOD fit, 8 BAD fit (19 active total)
Weights: 4 HIGH, 6 MEDIUM, 5 LOW, 1 INSTANT_DISQUALIFIER
Archived: 3 questions
```

Also display a relevant snippet of the entity description (first ~200 chars) since the description shapes how the LLM interprets every question.

Ask if the user wants to proceed or if anything looks off before testing.

### Phase 2: Collect Test Cases

Present both options:

```
AskUserQuestion({
  questions: [{
    question: "How do you want to build the test set?",
    header: "Test cases",
    options: [
      { label: "I have companies/people in mind", description: "Provide names/domains with expected score bands" },
      { label: "Help me find test cases", description: "I'll search for good and bad fit examples" },
      { label: "Mix of both", description: "I have some, help me find the rest" }
    ],
    multiSelect: false
  }]
})
```

#### Option A: User provides test cases

Ask for names/domains with expected score bands:

```
I need test cases in three bands to diagnose your scoring:

1. GOOD FIT (should score 8-10): "If I had 10 more of these, life would be great"
2. BORDERLINE (should score 4-6): "Could go either way"
3. BAD FIT (should score 1-3): "We'd waste each other's time"

For company qual: name + domain
For person qual: name + company + domain (and job title if known)
```

**For Routing + Scoring mode** (multi-entity sections), also ask which entity each test case should match:

```
I also need to know which [persona/segment/playbook] each test case should be
routed to. For each, tell me:
- The expected entity match (which one SHOULD be selected)
- The expected score band (how well they should score against that entity)

Example format:
  Jane Doe (VP Sales @ Snowflake)    → VP of Sales persona,    8-10
  Bob Smith (RevOps @ Shopify)       → RevOps Leader persona,  8-10
  Lisa Chen (SDR Mgr @ Notion)       → SDR Manager persona,    4-6
  Mark Lee (Engineer @ DoorDash)     → None / bad fit,          1-3
```

Accept "any / whatever it picks" for cases where the user doesn't have a strong routing expectation — we'll still capture which entity was selected and can surface surprises.

#### Option B: Help find test cases

**For company qualification:**
1. Ask for 1-2 known good fits → use `find_similar_companies({ referenceCompany: { domain: "..." } })` to seed more
2. Ask for 1-2 known bad fits → use `find_company` with contrasting filters
3. Present candidates, user tags them GOOD/BORDERLINE/BAD

**For person qualification:**
1. Ask for 1-2 known good fits (name + company + title) → use `find_similar_people({ referencePerson: { linkedInProfile: "..." } })` to seed more
2. Ask for 1-2 known bad fits → use `find_person` with contrasting filters
3. Present candidates, user tags them GOOD/BORDERLINE/BAD

#### Both paths converge on:

A confirmed test set of 3-15 cases with expected score bands. Minimum: 1 GOOD + 1 BAD. Ideal: 2 GOOD + 1 BORDERLINE + 2 BAD.

**Calculate cost and confirm before execution.**

Calculate credits per run from the agent config (or raw tool defaults):

| Component | Credits | How to check |
|-----------|---------|-------------|
| Base (includes product/offering) | 1 | Always included |
| + Segment section | +1 | `entities.segment.strategy === "BEST_MATCH"` |
| + Persona section | +1 | `entities.persona.strategy === "BEST_MATCH"` |
| + Playbook section | +1 | `entities.playbook.strategy === "BEST_MATCH"` |
| + High effort mode | +4 | `tools.highEffortMode.enabled === true` |
| + Deep research | +8 | `tools.parallelWebSearch.enabled === true` |
| + CRM activity | +10 | `tools.crmActivity.enabled === true` |
| + Custom task | +5 | `tools.customTask.enabled === true` |

For raw tools (no saved agent), skip the cost estimate entirely — just confirm the test case count and proceed.

**For saved agents**, show the calculated cost:
```
Ready to run N test cases.
Cost per run: X credits (base 1 + [active sections/tools])
Total for this round: X × N = Y credits
Proceed?
```

**For raw tools:**
```
Ready to run N test cases. Proceed?
```

### Phase 3: Run + Annotate

Execute qualification for each test case.

**If using a saved agent:**
```
run_qualify_company_agent({ agent: "<agent_oId>", company: { domain: "...", name: "..." } })
```
or
```
run_qualify_person_agent({ agent: "<agent_oId>", person: { firstName: "...", lastName: "...", jobTitle: "...", companyDomain: "..." } })
```

**If using raw tools:**
```
qualify_company({ companyDomain: "..." })
```
or
```
qualify_person({ person: { firstName: "...", lastName: "...", jobTitle: "...", companyDomain: "..." } })
```

Show progress. **IMPORTANT: Always show the SUB-SCORE for the section being tuned, NOT the overall score.** If tuning product fit, show the product section score. The overall score is influenced by other sections (segment, playbook, persona) that we're not tuning right now — showing it would be misleading.

```
Running qualification...
  Test 1: Snowflake (snowflake.com)... done (product sub-score: 9, expected: 8-10) OK
  Test 2: Acme Corp (acme.com)... done (product sub-score: 8, expected: 4-6) TOO HIGH ←
  Test 3: Mom's Pizza (momspizza.com)... done (product sub-score: 2, expected: 1-3) OK
```

**Store the full response for each test case** — especially the per-question `answers[]` array within the target section's `qualification` object. Extract the section-level score from the target section, not the top-level overall score.

**For persona/segment/playbook sections**, also store which entity was selected to evaluate selection accuracy separately.

#### Present Results Grid

Always label the score column with the section name to make clear this is a sub-score.

**Score-only mode** (single entity):
```
RESULTS (Product Fit Sub-Score)
===============================
#   Company              Score   Expected   Verdict
1   Snowflake              9     8-10       OK
2   Acme Corp              8     4-6        TOO HIGH ←
3   Mom's Pizza            2     1-3        OK
4   DataDog                7     8-10       LOW ←
```

**Routing + Scoring mode** (multi-entity):
```
RESULTS (Persona Fit — Routing + Score)
========================================
#   Person              Matched Persona    Score   Expected Match      Exp. Score   Verdict
1   Jane Doe            VP of Sales          9     VP of Sales         8-10         OK
2   Bob Smith           VP of Sales          7     RevOps Leader       8-10         WRONG MATCH ←
3   Lisa Chen           SDR Manager          3     SDR Manager         4-6          LOW ←
4   Mark Lee            VP of Sales          2     None / bad fit      1-3          OK (low score = correct)
```

In Routing + Scoring mode, mismatches fall into three categories:
- **WRONG MATCH** — agent selected the wrong entity (routing problem)
- **SCORE** — right entity selected but score is out of band (scoring problem)
- **BOTH** — wrong entity AND score is off

If tuning multiple sections, show a separate grid per section — never combine them into one overall number.

#### Collect Mismatch Annotations

For EACH mismatch, ask the user WHY they expected something different.

**Score mismatches** (same as score-only mode):
```
#3 Lisa Chen — scored 3, you expected 4-6:
  → Why should this be higher?
```

**Routing mismatches** — these need different questions:
```
#2 Bob Smith — matched "VP of Sales" but you expected "RevOps Leader":
  → What makes Bob a RevOps fit rather than VP of Sales?
  → Is the line between these two personas clear to you, or is it fuzzy?
```

These "why" annotations are critical for diagnosis — they tell us whether the issue is a missing question, a bad question, an entity description gap, or overlapping entity definitions.

If no mismatches, congratulate the user and skip to Phase 5 (or offer to stress-test with more cases).

### Phase 4: Diagnose + Fix

#### 4a: Per-Mismatch Deep Dive

For EACH mismatched test case, show the question-level breakdown that explains the score (or the routing decision) using the patterns below.

See [per-mismatch-deep-dive-templates.md](references/per-mismatch-deep-dive-templates.md) for the score-mismatch and routing-mismatch deep dive templates.

For each mismatch, surface:
1. **Which questions are causing the wrong score OR wrong routing** (with actual answers from the response)
2. **What's missing** (tied to the user's "why" annotation)
3. **Specific recommendations** — add a question, reweight, archive, sharpen entity descriptions, or differentiate between similar entities

#### 4b: Cross-Case Pattern Analysis

After per-mismatch breakdowns, look across ALL test cases for systemic patterns:
- Questions that answer the same for good AND bad fits (non-differentiating → archive or sharpen)
- Questions with LOW confidence across the board (info gap → rewrite rationale or reduce weight)
- Entity description gaps surfaced by multiple mismatches

**Routing-specific cross-case patterns** (Routing + Scoring mode only):
- **Entity A always wins**: One entity's questions are systematically easier to answer YES to, so it wins routing even when it shouldn't. Fix: sharpen that entity's questions or strengthen the competing entity.
- **Overlapping descriptions**: Two entities have descriptions so similar the agent can't distinguish them. Fix: differentiate descriptions by adding explicit "this persona is X, NOT Y" language.
- **Missing differentiating questions**: The entities lack questions that create separation between them. A VP of Sales and a CRO might score identically if neither has questions about what makes them distinct. Fix: add questions that are uniquely YES for one entity and NO for the other.

#### 4c: Entity Description Analysis

Compare user annotations against the entity description:
- If user says "should be lower because they're B2C" but entity description doesn't mention B2B → description gap
- If user says "should be higher because of their engineering team" but description focuses on sales → description mismatch
- Surface as "ENTITY DESCRIPTION ISSUE" distinct from question issues

#### 4d: Ranked Recommendations Summary

Consolidate all recommendations into a ranked list:

```
RECOMMENDATIONS (ranked by expected impact)
============================================

1. [HIGH IMPACT] Add question: competitive tool usage
   Type: New BAD fit question, weight HIGH
   Fixes: Acme Corp (#2), SimilarCo (#5)
   Expected effect: Drops competitor-users by 1-2 points

2. [MEDIUM IMPACT] Update entity description: add competitive landscape
   Type: Entity description change
   Fixes: Supports recommendation #1, improves edge case interpretation
   Expected effect: Better context for all competitive questions

3. [MEDIUM IMPACT] Archive Q7: "50+ employees"
   Type: Remove non-differentiating question
   Fixes: Reduces noise across all cases
   Expected effect: Slightly lowers scores for very large companies

4. [LOW IMPACT] Reweight Q4: "Uses no-code automation tools" → MEDIUM
   Type: Weight change
   Fixes: Reduces score volatility from low-confidence answers
```

#### 4e: Apply Changes

```
AskUserQuestion({
  questions: [{
    question: "Which changes should I apply?",
    header: "Changes",
    options: [
      { label: "Apply all", description: "Make all recommended changes at once" },
      { label: "Let me pick", description: "I'll choose which changes to apply" },
      { label: "None", description: "Just the diagnosis — I'll make changes manually" }
    ],
    multiSelect: false
  }]
})
```

If "Let me pick": show each recommendation individually and let user approve/skip.

**Apply changes via `update_entity` with natural language instructions, ONE at a time:**

For question changes:
```
update_entity({
  entityType: "product",
  oId: "px_xxx",
  instructions: "Add a new BAD fit qualifying question: 'Does the company currently use a direct competitor product in the same category?' with weight HIGH and fitType BAD. Rationale: 'Companies already using a direct competitor are less likely to switch. Check for mentions of competitor tools on their website, job postings, or integration pages.'",
  keyContext: "Testing revealed borderline prospects who use competitor tools score identically to good fits because no existing question captures competitive tool usage."
})
```

For entity description changes:
```
update_entity({
  entityType: "product",
  oId: "px_xxx",
  instructions: "Update the entity description to mention that companies already using a direct competitor in the same category are lower priority prospects. Add this context naturally into the existing description without removing anything.",
  keyContext: "Multiple test cases showed the agent has no context about competitive landscape, leading to inflated scores for prospects using rival tools."
})
```

Confirm each change:
```
Applied change 1 of 3: Added BAD fit question about competitor tools
Applied change 2 of 3: Updated entity description with competitive context
Applied change 3 of 3: Archived Q7 "50+ employees"
```

### Phase 5: Verify

Re-run ALL test cases with updated questions. Again, show the **sub-score** for the section being tuned.

**Score-only mode:**
```
BEFORE / AFTER (Product Fit Sub-Score)
======================================
#   Company         Before   After   Expected    Change
1   Snowflake         9       9      8-10        — stable
2   Acme Corp         8       5      4-6         ↓3 FIXED
3   Mom's Pizza       2       1      1-3         — stable
4   DataDog           7       9      8-10        ↑2 FIXED
```

**Routing + Scoring mode:**
```
BEFORE / AFTER (Persona Fit — Routing + Score)
===============================================
#   Person          Before Match → After Match    Before → After   Expected              Verdict
1   Jane Doe        VP Sales → VP Sales             9 → 9          VP Sales, 8-10        stable
2   Bob Smith       VP Sales → RevOps Leader         7 → 8          RevOps Leader, 8-10   ROUTING FIXED
3   Lisa Chen       SDR Mgr → SDR Mgr                3 → 5          SDR Mgr, 4-6          SCORE FIXED
4   Mark Lee        VP Sales → VP Sales               2 → 2          bad fit, 1-3          stable
```

If still mismatches:
```
AskUserQuestion({
  questions: [{
    question: "Scores are closer but not perfect. Want another round?",
    header: "Next",
    options: [
      { label: "Another round", description: "Diagnose again with the updated questions" },
      { label: "Good enough", description: "Scores are acceptable — wrap up" }
    ],
    multiSelect: false
  }]
})
```

If "Another round": loop back to Phase 4 with new results.

### Wrap Up

Display final summary:

See [wrap-up-summary-templates.md](references/wrap-up-summary-templates.md) for the score-only and routing+scoring wrap-up templates plus the additional-insights callout.

## Cost Reference

Credits per qualification run = sum of active components:

| Component | Credits |
|-----------|---------|
| Base (includes product/offering) | 1 |
| + Segment section | +1 |
| + Persona section | +1 |
| + Playbook section | +1 |
| + High effort mode | +4 |
| + Deep research | +8 |
| + CRM activity | +10 |
| + Custom task | +5 |

`update_entity` is free (no credit cost).

**Example**: Agent with product + segment active, no tools = 2 credits/run. 7 cases × 2 rounds = 28 credits.

Always calculate and show exact cost before executing test runs.

## MCP Tools Used

### Read
- `verify_connection` — workspace check
- `list_agents` (QUALIFY_COMPANY + QUALIFY_PERSON) — find qual agents
- `get_agent` — full agent config (sections, model, strategy)
- `list_all_entities` — list entities by type
- `get_entity` — full entity with qualifying questions + description
- `find_company` / `find_similar_companies` — find test case companies
- `find_person` / `find_similar_people` — find test case people

### Execute
- `qualify_company` / `qualify_person` — raw qualification
- `run_qualify_company_agent` / `run_qualify_person_agent` — agent-based qualification

### Write
- `update_entity` — modify qualifying questions, weights, entity descriptions

## Entity qualifyingQuestions Structure

Each entity's `qualifyingQuestions[]` array contains objects with:
- `question` (string) - The question text
- `weight` (string) - "HIGH" | "MEDIUM" | "LOW" | "INSTANT_DISQUALIFIER"
- `fitType` (string) - "GOOD" (should answer Yes for good fits) | "BAD" (should answer Yes for bad fits)
- `rationale` (string) - Guides the agent's interpretation of the question
- `archivedAt` (string|null) - null = active, timestamp = archived (used as negative example)

## Qualification Response Structure

Each qualification response includes per-section results. Each section contains:
- `oId`, `name`, `description` - The selected entity
- `qualification.score` (number 1-10) - Section score
- `qualification.rationale` (string) - Section-level explanation
- `qualification.answers[]` - Per-question breakdown:
  - `question` (string) - Question text
  - `answer` (string) - "Yes" or "No"
  - `rationale` (string) - Why the agent answered this way
  - `confidence` (string) - "HIGH" | "MEDIUM" | "LOW"
  - `weight` (string) - "HIGH" | "MEDIUM" | "LOW" | "INSTANT_DISQUALIFIER"

## Agent Configuration Reference

Saved qualification agents have these tuning-relevant settings:
- `data.commonContext.entities.{type}.strategy` - "BEST_MATCH" (active) or "NONE" (disabled)
- `data.scoringContext.{section}.skipContributingToOverallScore` - Exclude from overall score
- `data.tools.parallelWebSearch.enabled` - Deep research (checks news, articles, job postings)
- `data.tools.highEffortMode.enabled` - More compute for matching/scoring
- `data.model` - NOTE/PULSE/ECHO/HARMONY/CHORUS/SYMPHONY

## Error Handling

**No qualifying questions on entity:**
> This entity has no qualifying questions yet. You can add starter questions now via `update_entity`, or run qualification once — Octave will auto-generate questions from the entity description.

**Empty qualification response:**
Retry once. If still empty:
> Qualification returned empty. This can happen with lighter models. If using a saved agent, try switching the model to SYMPHONY or enabling high effort mode.

**Agent not found:**
Show available agents and ask user to pick.

**Insufficient test cases:**
> I need at least 2 test cases (one good fit, one bad fit) to diagnose anything. 3-5 is ideal.

## Examples

```
/qual-doctor
```

The skill is fully interactive — it walks you through agent selection, section picking, test case collection, and diagnosis.

## Related Skills

- `/octave:audit` - Broader library health check (includes qualification gaps)
- `/octave:library` - Browse and update entities directly
- `/octave:explore-agents` - View and manage qualification agent configs
- `/octave:prospector` - Find prospects to use as test cases
