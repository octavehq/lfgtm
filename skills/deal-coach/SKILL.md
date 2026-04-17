---
name: deal-coach
description: "Deal coaching — role-play, coaching microsites, decks, and quizzes built around the Resonate → Elevate → Compel methodology and grounded in your Octave library. Use when user says 'deal coaching', 'deal coach role play', 'coaching quiz', 'coaching deck', 'deal-coach', 'practice deal coaching', 'coaching microsite', 'sales methodology training', or asks for deal coaching."
---

# /octave:deal-coach — Deal Coaching

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
| **Buyer Mindset** | String | Buyer psychology — fears, motivations, awareness level |
| **Value Propositions** | Array | Which value props to deploy and why they fit this stage |
| **Talking Points** | Array | Specific things to say, grounded in deal context |

This skill reads coaching reference files at runtime:
- `references/frameworks.md` — Resonate / Elevate / Compel methodology
- `references/coaching-agents.md` — 3 coaching agent personas + 2 cross-stage + scoring rubrics
- `references/stage-mapping.md` — Buyer's Journey → coaching stage mapping + inference rules
- `references/html-templates.md` — HTML section/slide templates per output mode
- `references/messaging-narratives.md` — How coaching grounds in GTM context
- `references/roleplay-templates.md` — Role play scenario setup, buyer behavior, scorecard templates
- `references/microsite-templates.md` — Microsite outline, structural rules, content density limits
- `references/deck-templates.md` — Slide outlines per stage, viewport/animation/navigation rules
- `references/quiz-templates.md` — Quiz types, question bank structure, results template

If reference files are not found, fall back to general coaching methodology and note the limitation.

**How this differs from `/octave:train`:**
- `/octave:train` is generic sales training (objection handling, personas, product knowledge)
- `/octave:deal-coach` is methodology-specific — every output is structured around Resonate/Elevate/Compel, scored against coaching rubrics, and coached by stage-specific agents

**How this differs from `/octave:meeting-prep`:**
- `/octave:meeting-prep` produces a strategic battle plan for an upcoming meeting
- `/octave:deal-coach` produces training and coaching materials organized around the three coaching stages

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
    question: "What kind of deal coaching output do you want?",
    header: "Output Mode",
    options: [
      { label: "Role Play", description: "Practice a coaching-backed conversation (8-12 exchanges + scorecard)" },
      { label: "Coaching Microsite", description: "HTML coaching page with Buyer Mindset / Value Props / Talking Points" },
      { label: "Coaching Deck", description: "Slide presentation walking through the coaching framework" },
      { label: "Interactive Quiz", description: "Test methodology knowledge with deal-grounded scenarios" }
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
      { label: "Specific Deal", description: "Ground coaching in a real account using CRM data, findings, and playbook" },
      { label: "Generic Practice", description: "Practice with library-level data only (personas, playbook, proof points)" }
    ],
    multiSelect: false
  }]
})
```

If **Generic Practice**: Skip to Step 2c.

If **Specific Deal**: Ask for domain or email, then proceed to 2b.

#### 2b. Gather deal-specific context

Run these MCP tool calls to build a complete picture. Run independent calls in parallel:

**Company & CRM Context (parallel):**
```
enrich_company({ domain: "<domain>" })
find_crm_records({ domain: "<domain>" })
find_crm_activities({ domain: "<domain>" })
generate_crm_context({ domain: "<domain>" })
```

**Library Context (parallel):**
```
search_knowledge_base({ query: "<company name> OR <industry>" })
list_findings({ domain: "<domain>" })
list_events({ domain: "<domain>" })
list_all_entities({ entityType: "persona" })
list_all_entities({ entityType: "competitor" })
list_all_entities({ entityType: "proofPoint" })
```

**Playbook (after knowledge base search returns):**
```
get_playbook({ oId: "<matched_playbook_oId>" })
```

If any tool call fails, note the gap and continue with available data.

#### 2c. Generic practice mode context

```
search_knowledge_base({ query: "playbook" })
list_all_entities({ entityType: "persona" })
list_all_entities({ entityType: "competitor" })
list_all_entities({ entityType: "proofPoint" })
get_playbook({ oId: "<default_playbook_oId>" })
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
| Deal activity patterns | 20% | `list_events` — discovery (→Resonate), demo (→Elevate), proposal (→Compel) |
| Time in stage | 10% | Days in current stage vs. expectation |

**For generic practice mode:** Skip inference. Let the user choose a stage:

```
AskUserQuestion({
  questions: [{
    question: "Which coaching stage do you want to practice?",
    header: "Stage",
    options: [
      { label: "Resonate", description: "Discovery principles, building trust through understanding" },
      { label: "Elevate", description: "Disrupt status quo, differentiate on value, build credibility" },
      { label: "Compel", description: "Business case, Why Now, champion enablement" }
    ],
    multiSelect: false
  }]
})
```

#### 3b. Present inference and allow override

**Confidence calibration:** CRM absence is a data hygiene issue, not a deal health signal. If CRM data is missing but activity signals are strong, redistribute CRM weight across other signals.

Present the inference summary (stage, confidence, buyer's journey phase, evidence breakdown), then confirm:

```
AskUserQuestion({
  questions: [{
    question: "Does this stage assessment look right?",
    header: "Confirm Stage",
    options: [
      { label: "Yes — proceed with [Stage]", description: "Generate [mode] coaching for [Stage]" },
      { label: "No — let me pick", description: "Override and choose a different stage" },
      { label: "Show all stages", description: "See all 3 stages before choosing" }
    ],
    multiSelect: false
  }]
})
```

If user overrides, present the full stage list (same as generic mode).

#### 3c. Stall detection

If time-in-stage indicates a stalled deal (>2x expected time), add stall diagnosis: identify the root cause stage gap, explain why, cite evidence, and recommend focusing coaching on that stage instead of the nominal CRM stage.

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

Load the agent's persona, coaching criteria, scoring rubric, and grounding instructions from the reference file. Use the grounding map from `references/messaging-narratives.md` to connect outputs to Octave library data.

---

### Step 5: Generate Output (CT-5)

Branch based on the output mode selected in Step 1. Each mode has detailed templates in its reference file.

---

#### Mode 1: Role Play

Follow the full workflow in `references/roleplay-templates.md` (RP-1 through RP-4):

1. **RP-1 — Setup:** Ask for scenario type (single stage vs. full journey), difficulty, and buyer persona
2. **RP-2 — Load Intelligence:** Load coaching rubric, grounding map, and stage-specific buyer behavior rules
3. **RP-3 — Run Role Play:** Set the scene, play the buyer persona with stage-appropriate behavior and difficulty-adjusted resistance. 8-12 exchanges for single stage; sequential stages for full journey.
4. **RP-4 — Scorecard:** Score across Buyer Mindset, Value Propositions, Talking Points (stage-specific criteria), and General Selling Skills. Include key moments, coaching advice, and unused value props.

Post-scorecard: offer replay, harder difficulty, next stage, objection handling, microsite, mode switch, or done.

---

#### Mode 2: Coaching Microsite

Follow the full workflow in `references/microsite-templates.md` (MS-1 through MS-3):

1. **MS-1 — Style:** Select style preset (stage defaults: Resonate→soft-light, Elevate→midnight-pro, Compel→executive-dark) with override option
2. **MS-2 — Outline:** Present content plan (header, priority actions, deal activity, journey map, 6-7 coaching sections, the play) for approval
3. **MS-3 — Generate HTML:** Build self-contained HTML using `references/html-templates.md`, following structural rules and content density limits from the microsite templates reference

---

#### Mode 3: Coaching Deck

Follow the full workflow in `references/deck-templates.md` (DK-1 through DK-3):

1. **DK-1 — Style:** Same as microsite style selection
2. **DK-2 — Outline:** Present stage-specific slide outline (Resonate ~7, Elevate ~9, Compel ~9 slides) for approval
3. **DK-3 — Generate HTML:** Build scroll-snap HTML deck using `references/html-templates.md`, following viewport fitting, animation, and navigation rules from the deck templates reference

---

#### Mode 4: Interactive Quiz

Follow the full workflow in `references/quiz-templates.md` (QZ-1 through QZ-4):

1. **QZ-1 — Setup:** Choose quiz type (stage recognition, methodology application, talk track completion, full review) and length (5/10/15 questions)
2. **QZ-2 — Load Material:** Build question bank by category, grounded in deal or playbook data
3. **QZ-3 — Run Quiz:** Present questions one at a time with immediate feedback and running score
4. **QZ-4 — Results:** Score breakdown by stage, coaching dimension, and category. Identify strengths, gaps, and recommended next steps.

Post-quiz: offer retake, focused quiz on weakest area, role play practice, microsite, mode switch, or done.

---

### Step 6: Delivery + Next Actions (CT-6)

For **Role Play** and **Quiz**: Next actions are included in RP-4 and QZ-4 templates.

For **Microsite** and **Deck**: After opening the HTML file, present:

```
Coaching [microsite/deck] generated and opened in your browser.

File: [file path]
Company: [Company Name or "Generic Practice"]
Stage: [Stage] — [subLabel]
Coaching Agent: [Agent Name]
Style: [Preset Name]

Want to:
1. Practice this stage with a role play
2. Add MEDDPICC deal gap analysis [if not included]
3. Move to the next stage ([Next Stage])
4. Try a different output mode
5. Regenerate with a different style
6. Done
```

If the user picks next stage, return to Step 3b with next stage pre-selected and flow through Steps 4-5.

---

## Output Directory

All HTML outputs go to `.octave-deal-coach/` in the project root (should be in `.gitignore`):

```
.octave-deal-coach/
  [company-kebab]-[stage]-[YYYY-MM-DD]/
    [company-kebab]-[stage].html            # Microsite
  [company-kebab]-deck-[stage]-[YYYY-MM-DD]/
    [company-kebab]-deck-[stage].html       # Deck
```

For generic mode, use `practice` instead of company name.

---

## MCP Tools Used

### Research & Enrichment
| Tool | Purpose |
|------|---------|
| `enrich_company` | Company profile, industry, tech stack |
| `find_crm_records` | Deal stage, amount, close date |
| `find_crm_activities` | Recent interactions |
| `generate_crm_context` | AI-synthesized CRM narrative |

### Library
| Tool | Purpose |
|------|---------|
| `get_playbook` | Full playbook with value props, messaging, positioning |
| `get_entity` | Individual entity details |
| `search_knowledge_base` | Find matching playbooks, guides, research |
| `search_resources` | Find relevant resources |
| `list_all_entities` | List personas, competitors, proof points, references |
| `list_findings` | Objections, pain points, competitor mentions |
| `list_events` | Deal history, stage changes, activity timeline |

### Content Generation
| Tool | Purpose |
|------|---------|
| `generate_content` | Generate supporting content if needed |

---

## Error Handling

| Condition | Response |
|-----------|----------|
| No CRM data | Proceed with library data; inference relies on findings/events; offer manual stage selection |
| No playbook | Use general methodology; note missing playbook-specific grounding; suggest `/octave:library` |
| No findings/events | Inference relies primarily on CRM stage; recommend syncing conversation data |
| Reference file missing | Fall back to general methodology; note the limitation |
| Low confidence inference | Recommend manual stage selection; present all three stages |
| MCP connection failed | Direct user to `/octave:workspace` to check connection |
| HTML write failed | Suggest `mkdir -p .octave-deal-coach` |

---

## Related Skills

- `/octave:train` — Generic sales training without deal coaching methodology
- `/octave:meeting-prep` — Strategic meeting battle plan as HTML
- `/octave:deck` — General-purpose slide deck builder
- `/octave:pipeline` — Deal coaching and pipeline management
- `/octave:enablement` — Sales enablement materials
- `/octave:battlecard` — Competitive intelligence and battlecards
- `/octave:research` — Account and person research
