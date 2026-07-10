---
name: deal-coach
description: "Methodology practice and coaching assets built around Resonate → Elevate → Compel — role-play, coaching microsites, coaching decks, and quizzes grounded in your Octave library. Use when user says 'deal coach role play', 'coaching quiz', 'coaching deck', 'coaching microsite', 'practice the methodology', 'sales methodology training', or asks to practice or be coached on a deal. Do NOT use for live-deal strategy and next steps — use /octave:pipeline instead."
argument-hint: "[domain|email] [--mode roleplay|microsite|deck|quiz] [--stage resonate|elevate|compel]"
---

# /octave:deal-coach — Methodology Coaching

An interactive coaching skill built around the **Resonate → Elevate → Compel** sales methodology. Choose your output mode — role play, coaching microsite, coaching deck, or interactive quiz — and get coaching grounded in deal context AND your actual GTM messaging.

**Three Stages:**
| Stage | Focus |
|-------|-------|
| **Resonate** | Understand and resonate with the buyer |
| **Elevate** | Confirm the fit and elevate the opportunity |
| **Compel** | Deliver the value and compel the buyer to action |

**Three Coaching Outputs per Stage:**
| Field | Type | Purpose |
|-------|------|---------|
| **Buyer Mindset** | String | Where the buyer's head is — psychology, fears, motivations |
| **Value Propositions** | Array | Which value props to deploy and why they fit this stage |
| **Talking Points** | Array | Specific things to say, grounded in deal context |

This skill reads five coaching reference files at runtime:
- `references/frameworks.md` — Resonate / Elevate / Compel: Buyer Mindset + Value Props + Talking Points
- `references/coaching-agents.md` — 3 coaching agent personas + 2 cross-stage + scoring rubrics
- `references/stage-mapping.md` — Buyer's Journey → coaching stage mapping + inference rules
- `references/html-templates.md` — HTML section/slide templates per output mode
- `references/messaging-narratives.md` — How coaching grounds in GTM context

If reference files are not found, fall back to general coaching methodology and note the limitation.

**How this differs from `/octave:pipeline`:**
- `/octave:pipeline` gives live-deal strategy — diagnosis and next steps to move a specific deal forward
- `/octave:deal-coach` produces practice and coaching materials organized around the three coaching stages

**How this differs from `/octave:train`:**
- `/octave:train` is generic sales training (objection handling, personas, product knowledge)
- `/octave:deal-coach` is methodology-specific — every output is structured around Resonate/Elevate/Compel, scored against coaching rubrics, and coached by stage-specific agents

**How this differs from `/octave:meeting-prep`:**
- `/octave:meeting-prep` produces a strategic battle plan for an upcoming meeting
- `/octave:deal-coach` produces training and coaching materials organized around the three coaching stages

## On-brand styling — use a brand kit if one exists

Before generating HTML output, decide whose brand this coaching asset should match (usually the **target company**; sometimes your own company), then follow [brand-kit-usage.md](../shared/brand-kit-usage.md): check for a cached kit, offer to use it, offer to capture one if missing, and fall back to a style preset if declined. The brand kit is the strongest styling signal — prefer it over generic `--style` presets.

## Review pass (runs by default)

After generating, **run the review pass by default** — don't wait to be asked. In interactive mode, tell the user at intake that you'll review before finishing (recommended) and that they can opt out with `--skip-review` or "skip review". Follow [review-pass.md](../shared/review-pass.md) for the preflight and visual pass. When generating, follow the output rules in [presentation-principles.md](../shared/presentation-principles.md) — label every value, no tool names in the output, confirmed vs hypothesized, lean and deal-specific.

## Usage

```
/octave:deal-coach
/octave:deal-coach [company domain or name]
/octave:deal-coach --mode [roleplay|microsite|deck|quiz]
/octave:deal-coach --stage [resonate|elevate|compel]
/octave:deal-coach [domain] --mode roleplay --stage elevate
```

## Examples

```
/octave:deal-coach
/octave:deal-coach acme.com
/octave:deal-coach --mode roleplay
/octave:deal-coach acme.com --mode microsite --stage compel
/octave:deal-coach --mode quiz --stage resonate
/octave:deal-coach acme.com --mode deck --stage elevate
```

## Instructions

Follow these steps precisely. Do not skip or reorder them.

---

### Step 1: Choose Output Type (CT-1)

If the user specified `--mode`, use that. Otherwise, ask:

```
AskUserQuestion({
  questions: [{
    question: "What kind of coaching output do you want?",
    header: "Output Mode",
    options: [
      {
        label: "Role Play",
        description: "Practice a coaching-backed conversation scored against Buyer Mindset, Value Props, and Talking Points. 8-12 exchanges, then a scorecard."
      },
      {
        label: "Coaching Microsite",
        description: "Self-contained HTML coaching page organized around Buyer Mindset / Value Propositions / Talking Points — with deal context, priority actions, and stage-grounded messaging."
      },
      {
        label: "Coaching Deck",
        description: "Slide presentation walking through the coaching framework for a specific deal, with stage-specific content and talk tracks."
      },
      {
        label: "Interactive Quiz",
        description: "Test coaching methodology knowledge with deal-grounded scenarios. Scoring breaks down by Resonate/Elevate/Compel."
      }
    ],
    multiSelect: false
  }]
})
```

Store the selected mode for routing in Step 5.

---

### Step 2: Identify Deal Context (CT-2)

Determine if coaching should be grounded in a specific deal or run in generic/practice mode.

If the user already provided a domain, name, or email, skip to 2b.

#### 2a. Ask for deal context

```
AskUserQuestion({
  questions: [{
    question: "Should this be grounded in a specific deal, or do you want generic practice?",
    header: "Deal Context",
    options: [
      {
        label: "Specific Deal",
        description: "Ground coaching in a real account — uses CRM data, findings, events, and the matched Motion ICP narrative to make coaching deal-specific."
      },
      {
        label: "Generic Practice",
        description: "Practice the methodology with library-level data only (personas, Motion ICP narrative, proof points). No specific account context."
      }
    ],
    multiSelect: false
  }]
})
```

If **Generic Practice**: Skip to Step 2c.

If **Specific Deal**: Ask for the company domain or contact email (e.g., `acme.com` or `jane@acme.com`).

#### 2b. Gather deal-specific context

Run these MCP tool calls to build a complete picture. Run independent calls in parallel:

**Company & CRM Context (parallel):**
```
enrich_company({ companyDomain: "<domain>" })
find_crm_records({ companyDomain: "<domain>" })
find_crm_activities({ companyDomain: "<domain>" })
generate_crm_context({ companyDomain: "<domain>" })
```

**Library Context (parallel):**
```
search_knowledge_base({ query: "<company name> OR <industry>" })
list_findings({
  query: "objections pain points competitor mentions next steps",
  eventFilters: { companyDomains: ["<domain>"] }
})
list_events({
  filters: { companyDomains: ["<domain>"] }
})
list_entities({ entityType: "persona" })
list_entities({ entityType: "competitor" })
list_entities({ entityType: "proofPoint" })
```

**Motion ICP (after enrichment / persona / segment inference):**
```
list_motions()
list_motion_icps({ motionOId: "<motion_oId>" })
find_motion_icp({ motionIcpOId: "<matched_motion_icp_oId>", includeLearnings: true })
```

If a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) applies, also fetch its narrative:
```
list_motion_playbooks({ motionOId: "<motion_oId>" })
get_motion_playbook({ motionPlaybookOId: "<custom_motion_playbook_oId>" })
```

If any tool call fails, note the gap and continue. Coach with available data and flag missing context.

#### 2c. Generic practice mode context

For generic mode, gather library-level data only:

```
list_entities({ entityType: "persona" })
list_entities({ entityType: "competitor" })
list_entities({ entityType: "proofPoint" })
```

Then load the Default Motion Playbook narrative for the most relevant Motion:
```
list_motions()
list_motion_icps({ motionOId: "<motion_oId>" })
find_motion_icp({ motionIcpOId: "<representative_motion_icp_oId>", includeLearnings: true })
```

#### 2d. Load coaching reference files

Read the references needed for the inferred or selected stage:

```
Read: references/frameworks.md
Read: references/stage-mapping.md
Read: references/coaching-agents.md
Read: references/messaging-narratives.md
```

If generating HTML output (microsite or deck), also read:
```
Read: references/html-templates.md
```

---

### Step 3: Infer Coaching Stage + User Override (CT-3)

If the user specified `--stage`, use that and skip to Step 3b.

#### 3a. Infer stage from signals

Use the weighted inference algorithm from `references/stage-mapping.md`:

| Signal | Weight | Source |
|--------|--------|--------|
| CRM deal stage | 40% | `find_crm_records` → map to Resonate/Elevate/Compel |
| Conversation findings | 30% | `list_findings` — pain points (→Resonate), competitor mentions (→Elevate), ROI/budget (→Compel) |
| Deal activity patterns | 20% | `list_events` — discovery call (→Resonate), demo (→Elevate), proposal (→Compel) |
| Time in stage | 10% | Days in current stage vs. expectation |

**For generic practice mode:** Skip inference. Let the user choose a stage:

```
AskUserQuestion({
  questions: [{
    question: "Which coaching stage do you want to practice?",
    header: "Stage",
    options: [
      { label: "Resonate", description: "Understand and resonate with the buyer — discovery principles, building trust through understanding" },
      { label: "Elevate", description: "Confirm the fit and elevate the opportunity — disrupt status quo, differentiate on value, build credibility" },
      { label: "Compel", description: "Deliver the value and compel the buyer to action — business case, Why Now, champion enablement" }
    ],
    multiSelect: false
  }]
})
```

#### 3b. Present inference and allow override

**Confidence calibration:** CRM absence is a data hygiene issue, not a deal health signal. If CRM data is missing but activity signals are strong, redistribute the CRM weight across other signals.

Present the inference:

```
STAGE INFERENCE
===============
Stage: [Resonate / Elevate / Compel]
Confidence: [High / Medium / Low]
Buyer's Journey Phase: [Phase Name]

EVIDENCE
--------
CRM Stage (40%): "[Stage Name]" → maps to [Stage]  [or "No CRM record — data gap, not deal gap"]
Findings (30%): [Key signals]
Activities (20%): [Key activities]
Time (10%): [Assessment]
```

Then confirm with the user: proceed with the inferred stage, override and pick a different one, or see all three stages with descriptions before choosing (same list as generic mode above).

#### 3c. Stall detection

If time-in-stage signals indicate a stalled deal (>2x expected time), flag it — but don't re-implement deal rescue here:

```
STALL DETECTION
===============
This deal appears stalled at [Journey Phase].
Time in stage: [X] days (expected: [Y] days)

Root Cause Hypothesis: [Stage] gap
- [Explanation of why this stage gap is likely the root cause]
- [Specific evidence from findings/activities]

For a re-engagement strategy and next steps on this deal, run:
/octave:pipeline stalled [domain]

For coaching, I'll focus on [Root Cause Stage], not the nominal CRM stage.
```

Route coaching to the root cause stage's coaching agent, not the nominal stage. Deal-rescue strategy itself belongs to `/octave:pipeline`.

---

### Step 4: Route to Coaching Agent (CT-4)

Based on the confirmed stage, activate the appropriate coaching agent from `references/coaching-agents.md`:

| Stage | Coaching Agent | Focus |
|-------|---------------|-------|
| Resonate | Resonance Coach | Discovery principles (wide, deep, high), trust building |
| Elevate | Elevation Coach | Case for Change, Value Framing, differentiated value, proof points |
| Compel | Compel Coach | Business case building, Why Now Case, champion enablement |

**Cross-stage agents** (available as supplements):
- **Negotiation Strategist** — Available when stage is Compel and negotiation dynamics surface
- **Objection Handler** — Available at any stage when objections surface in findings

Load the agent's persona, coaching criteria, scoring rubric, and grounding instructions from the reference file. Use the grounding map from `references/messaging-narratives.md` to connect the agent's outputs to the seller's Octave library data.

---

### Step 5: Generate Output (CT-5)

Branch based on the output mode selected in Step 1. Each mode has its own reference file with the full flow — read it and follow it:

| Mode | Reference | What it covers |
|------|-----------|----------------|
| Role Play | [mode-roleplay.md](references/mode-roleplay.md) | Scenario setup, stage-specific buyer psychology, running the conversation, coaching scorecard (RP-1 → RP-4) |
| Coaching Microsite | [mode-microsite.md](references/mode-microsite.md) | Style selection, content outline, HTML generation with grounding rules and density limits (MS-1 → MS-3) |
| Coaching Deck | [mode-deck.md](references/mode-deck.md) | Style selection, stage-specific slide outlines, HTML deck generation on the deck skill's architecture (DK-1 → DK-3) |
| Interactive Quiz | [mode-quiz.md](references/mode-quiz.md) | Quiz type and length, question construction, running the quiz, results (QZ-1 → QZ-4) |

Role Play and Quiz run on the shared engine in [roleplay-mechanics.md](../shared/roleplay-mechanics.md) — the mode files layer the Resonate/Elevate/Compel specifics on top.

---

### Step 6: Delivery + Next Actions (CT-6)

After delivering any output, offer iterations:

For **Role Play** and **Quiz**: Next actions are included in RP-4 and QZ-4 in the mode references.

For **Microsite** and **Deck**: After opening the HTML file, present:

```
Coaching [microsite/deck] generated and opened in your browser.

File: [file path]
Company: [Company Name or "Generic Practice"]
Stage: [Resonate / Elevate / Compel] — [Stage subLabel]
Coaching Agent: [Agent Name]
Style: [Preset Name]

Want to:
1. Practice this stage with a role play
2. Add MEDDPICC deal gap analysis [if not already included]
3. Move to the next stage ([Next Stage]: [subLabel])
4. Try a different output mode for this stage
5. Regenerate with a different style
6. Done
```

If the user picks option 3 (next stage), return to Step 3b with the next stage pre-selected and flow through Steps 4-5 again.

---

## Output Directory

All HTML outputs go to `.octave-deal-coach/` in the project root:

```
.octave-deal-coach/
  [company-kebab]-[stage]-[YYYY-MM-DD]/
    [company-kebab]-[stage].html            # Microsite
  [company-kebab]-deck-[stage]-[YYYY-MM-DD]/
    [company-kebab]-deck-[stage].html       # Deck
```

This directory should be in `.gitignore`.

---

## MCP Tools Used

### Research & Enrichment
| Tool | Purpose |
|------|---------|
| `enrich_company` | Company profile, industry, tech stack, strategic context |
| `find_crm_records` | Deal stage, amount, close date, pipeline position |
| `find_crm_activities` | Recent interactions — calls, emails, meetings |
| `generate_crm_context` | AI-synthesized CRM narrative |

### Library — Fetching
| Tool | Purpose |
|------|---------|
| `list_motions` | List all Motions in the workspace |
| `list_motion_playbooks` | List Motion Playbooks (Default + Custom) under a Motion |
| `get_motion_playbook` | Full details for a Motion Playbook |
| `list_motion_icps` | List Motion ICP cells (persona × segment intersections) for a Motion |
| `find_motion_icp` | Full Motion ICP cell narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus Learning Loop learnings |
| `get_entity` | Individual entity details (persona, competitor, proof point) |

### Library — Searching
| Tool | Purpose |
|------|---------|
| `search_knowledge_base` | Find matching guides and research |
| `search_resources` | Find relevant resources (docs, presentations) |
| `list_entities` | List personas, competitors, proof points, references |
| `list_findings` | Objections, pain points, competitor mentions from conversations |
| `list_events` | Deal history, stage changes, activity timeline |

### Content Generation
| Tool | Purpose |
|------|---------|
| `generate_content` | Generate supporting content if needed |

---

## Error Handling

> **No CRM data found:** "I couldn't find CRM records for [domain]. I'll proceed with library-level data only. Stage inference will rely on findings and events. You can also manually select a stage."

> **No Motion ICP found:** "No matching Motion ICP cell found. I'll use general coaching methodology without Motion-specific grounding. Talk tracks will reference the framework but won't include your specific Strategic narrative, Benefits and impacts, or Methodology content. Consider creating a Motion for this offering, or layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) onto an existing Motion."

> **No findings/events:** "No conversation findings or events found for [domain]. Stage inference will rely primarily on CRM stage. For more accurate coaching, ensure conversation data is synced to Octave."

> **Reference file not found:** "Could not load [reference file]. Falling back to general coaching methodology. For full coaching, ensure reference files are in `skills/deal-coach/references/`."

> **Stage inference low confidence:** "I'm not confident about the coaching stage — multiple stages scored similarly. I'd recommend selecting manually. Here are all options: [present all three stages]."

> **MCP connection failed:** "Could not connect to Octave. Check your connection with `/octave:workspace`. This skill requires Octave MCP tools for deal context and library data."

> **HTML write failed:** "Could not write the HTML file. Check that `.octave-deal-coach/` is writable. Try: `mkdir -p .octave-deal-coach`"

---

## Related Skills

- `/octave:pipeline` — Live-deal strategy: stalled-deal rescue, multi-threading, competitive threats, closing
- `/octave:train` — Generic sales training (role play, quiz, guided learning) without the coaching methodology
- `/octave:meeting-prep` — Strategic meeting battle plan as HTML
- `/octave:deck` — General-purpose slide deck builder
- `/octave:enablement` — Sales enablement materials (cheat sheets, objection guides)
- `/octave:battlecard` — Competitive intelligence and battlecards
- `/octave:research` — Account and person research
