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
        description: "Ground coaching in a real account — uses CRM data, findings, events, and your playbook to make coaching deal-specific."
      },
      {
        label: "Generic Practice",
        description: "Practice the methodology with library-level data only (personas, playbook, proof points). No specific account context."
      }
    ],
    multiSelect: false
  }]
})
```

If **Generic Practice**: Skip to Step 2c.

If **Specific Deal**: Ask for the company domain or contact email:

```
AskUserQuestion({
  questions: [{
    question: "What company domain or contact email should I research?",
    header: "Company",
    options: [
      {
        label: "Enter domain",
        description: "e.g., acme.com"
      },
      {
        label: "Enter email",
        description: "e.g., jane@acme.com"
      }
    ],
    multiSelect: false
  }]
})
```

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

If any tool call fails, note the gap and continue. Coach with available data and flag missing context.

#### 2c. Generic practice mode context

For generic mode, gather library-level data only:

```
search_knowledge_base({ query: "playbook" })
list_all_entities({ entityType: "persona" })
list_all_entities({ entityType: "competitor" })
list_all_entities({ entityType: "proofPoint" })
```

```
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
| Deal activity patterns | 20% | `list_events` — discovery call (→Resonate), demo (→Elevate), proposal (→Compel) |
| Time in stage | 10% | Days in current stage vs. expectation |

**For generic practice mode:** Skip inference. Let the user choose:

```
AskUserQuestion({
  questions: [{
    question: "Which coaching stage do you want to practice?",
    header: "Stage",
    options: [
      {
        label: "Resonate",
        description: "Understand and resonate with the buyer — discovery principles, building trust through understanding"
      },
      {
        label: "Elevate",
        description: "Confirm the fit and elevate the opportunity — disrupt status quo, differentiate on value, build credibility"
      },
      {
        label: "Compel",
        description: "Deliver the value and compel the buyer to action — business case, Why Now, champion enablement"
      }
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

Then confirm:

```
AskUserQuestion({
  questions: [{
    question: "Does this stage assessment look right?",
    header: "Confirm Stage",
    options: [
      {
        label: "Yes — proceed with [Stage]",
        description: "Generate [selected mode] coaching for [Stage]"
      },
      {
        label: "No — let me pick",
        description: "Override the inference and choose a different stage"
      },
      {
        label: "Show all stages",
        description: "See all 3 stages with descriptions before choosing"
      }
    ],
    multiSelect: false
  }]
})
```

If user picks "No" or "Show all stages," present the full stage list (same as generic mode above).

#### 3c. Stall detection

If time-in-stage signals indicate a stalled deal (>2x expected time), add stall diagnosis:

```
STALL DETECTION
===============
This deal appears stalled at [Journey Phase].
Time in stage: [X] days (expected: [Y] days)

Root Cause Hypothesis: [Stage] gap
- [Explanation of why this stage gap is likely the root cause]
- [Specific evidence from findings/activities]

Recommendation: Focus coaching on [Root Cause Stage], not the nominal CRM stage.
```

Route to the root cause stage's coaching agent, not the nominal stage.

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

Branch based on the output mode selected in Step 1.

---

#### Mode 1: Role Play (RP-1 through RP-4)

##### RP-1: Setup the Scenario

```
AskUserQuestion({
  questions: [{
    question: "What kind of role play do you want?",
    header: "Scenario",
    options: [
      {
        label: "Single Stage Practice",
        description: "Practice one stage ([Stage]) in a focused 8-12 exchange conversation"
      },
      {
        label: "Full Journey Simulation",
        description: "Walk through Resonate → Elevate → Compel in sequence, simulating the full buying journey"
      }
    ],
    multiSelect: false
  },
  {
    question: "How difficult should the buyer be?",
    header: "Difficulty",
    options: [
      {
        label: "Friendly",
        description: "Buyer is open and receptive. Good for learning the coaching framework."
      },
      {
        label: "Skeptical",
        description: "Buyer pushes back moderately. Tests methodology under pressure."
      },
      {
        label: "Hostile",
        description: "Buyer is resistant, dismissive, or aggressive. Tests advanced skills and composure."
      }
    ],
    multiSelect: false
  }]
})
```

If in specific-deal mode, identify the buyer persona from entities gathered in Step 2. If generic, let the user choose from available personas:

```
AskUserQuestion({
  questions: [{
    question: "Which persona should the buyer represent?",
    header: "Buyer Persona",
    options: [
      // Dynamically populated from list_all_entities({ entityType: "persona" })
      {
        label: "[Persona Name]",
        description: "[Persona title/role — from entity data]"
      }
      // ... up to 4 personas
    ],
    multiSelect: false
  }]
})
```

##### RP-2: Load Stage-Specific Intelligence

Load the coaching agent's rubric and grounding map for the selected stage.

For deal-specific mode, map all Octave data to coaching output fields using `references/messaging-narratives.md`.

For generic mode, use playbook-level data to create a representative scenario.

Prepare buyer behavior rules based on stage:

| Stage | Buyer Psychology | Behavior Rules |
|-------|-----------------|---------------|
| Resonate | Exploratory, guarded | Shares surface problems, tests whether seller digs deeper. Friendly: volunteers info. Hostile: one-word answers. |
| Elevate | Status quo defender / comparison shopper | Resists change, references competitors. Friendly: open to new perspective. Hostile: "We've been doing fine for years" / "Your competitor does that too." |
| Compel | Analytical, needs numbers, risk-averse | Asks about ROI, pushes back on vague claims. Friendly: engages with data. Hostile: "Those numbers don't apply to us" / "Now is not the right time." |

##### RP-3: Run the Role Play

Set the scene:

See [mode-output-templates.md](references/mode-output-templates.md) for the role play scene setup template.

Then begin as the buyer persona:
- Play the buyer with stage-appropriate behavior (see table above)
- Adjust resistance based on difficulty level
- Drop stage-relevant cues that a well-trained seller should pick up on
- **Friendly:** give verbal rewards when the seller executes methodology correctly
- **Skeptical:** push back on weak points but yield to strong methodology
- **Hostile:** resist aggressively; only yield to excellent execution
- Allow natural conversation flow — don't force every principle or beat
- After 8-12 exchanges, signal wrap-up: "I think we're running short on time..."

For **Full Journey Simulation**:
- Start at Resonate and progress through each stage
- After each stage, pause: "Good — let's fast-forward. [Context for next stage]."
- Score each stage independently, then provide a cumulative scorecard

##### RP-4: Coaching Scorecard

After the role play ends:

See [mode-output-templates.md](references/mode-output-templates.md) for the full coaching scorecard template with stage-specific talking points rubrics.

After the scorecard:

```
Want to:
1. Run this role play again (same stage, same difficulty)
2. Try a harder difficulty level
3. Practice the next stage ([Next Stage])
4. Practice objection handling for this stage
5. Get a coaching microsite for this stage
6. Switch to a different output mode
7. Done
```

---

#### Mode 2: Coaching Microsite (MS-1 through MS-3)

##### MS-1: Style Selection

Reference the style preset system from `skills/deck/references/style-presets.md`.

Each coaching stage has a default style preset:

| Stage | Default Preset | Rationale |
|-------|---------------|-----------|
| Resonate | `soft-light` | Exploratory, calm, trust-building |
| Elevate | `midnight-pro` | Urgency, disruption, bold contrast |
| Compel | `executive-dark` | Business gravitas, financial seriousness |

Present the default with option to override:

```
AskUserQuestion({
  questions: [{
    question: "The default style for [Stage] is [preset name] ([rationale]). Want to use it or pick a different style?",
    header: "Style",
    options: [
      {
        label: "[Default Preset] (Recommended)",
        description: "[Preset description]"
      },
      {
        label: "Pick a different style",
        description: "Choose from available presets"
      },
      {
        label: "Auto-pick from brand",
        description: "Extract colors from the company's website and generate a custom theme"
      }
    ],
    multiSelect: false
  }]
})
```

If user picks "Pick a different style," present mood-based preview options (follow the pattern from `deck/SKILL.md` Step 4).

##### MS-2: Generate Content Outline

Before generating HTML, present the content plan:

See [mode-output-templates.md](references/mode-output-templates.md) for the microsite content outline template with full structure, design principles, and Octave sources block.

##### MS-3: Generate HTML

Use templates from `references/html-templates.md` to generate a self-contained HTML file.

**Content grounding rules** (from `references/messaging-narratives.md`):
- Every Value Proposition must reference specific playbook messaging — never generic claims
- Every proof point must cite a specific library entity, appear inline in the section it supports, and include a usage note (deploy now / save for later / already shared)
- Every Talking Point must be grounded in the deal context (if available) and connected to the Buyer Mindset
- Every objection response must be grounded in the specific decision the buyer is making — not generic competitive objections
- Use "perspective-shifting question" framing — collaborative, not adversarial
- This is a selling tool — orient language around advancing the deal

**Structural rules:**
- Header + Deal Brief is NOT collapsible — full-width gradient hero with deal stats
- Priority Actions, Deal Activity, and Journey Map are collapsible `<details>` with +/− toggle
- Sections 01-06 (07 if MEDDPICC included) are collapsible `<details>` elements
- ALL collapsible sections start COLLAPSED by default (no `open` attribute)
- The Play is NOT collapsible — full-width gradient footer
- No duplicate content between sections
- Evidence goes inline (not standalone)
- Do NOT use framework labels as visible headers in Talking Points (e.g., "The Shift", "The Stakes"). Use practical deal-specific language. The framework informs content structure internally.
- Do NOT include both "Elevate" and "Evaluate" badges in the header — use "Coaching Stage: [Name]" only. The Journey Map section explains the buyer journey mapping.

**Content density limits:**
| Section | Limit |
|---------|-------|
| Header + Deal Brief | Company info + 4-6 deal stats + coaching stage badge + deal-specific subtitle |
| Priority Actions | Exactly 3 actions |
| Deal Activity | 3-6 timeline entries (key events + "Next" entry) |
| Journey Map | 3 phases (Resonate/Elevate/Compel), each with generic explanation + deal-specific context |
| Stage Assessment | 3-4 evidence cards + confidence calibration |
| Buyer Mindset | Mindset narrative + 3-5 buyer signals + adaptation guidance |
| Value Propositions | 4-6 props with evidence inline and usage notes |
| Talking Points | 4-6 talk tracks (strategic point + quote + evidence) organized by conversation flow |
| Objection Handling | 3-5 objections grounded in buyer's decision frame |
| Next Stage Preview | 1 transition checklist + next agent preview |
| Deal Gaps (MEDDPICC) | 8 elements + gap-to-action mapping (if included) |
| The Play | 1 strategic sentence + 1 concrete action |

**Output location:**
```
.octave-deal-coach/
  [company-kebab]-[stage]-[YYYY-MM-DD]/
    [company-kebab]-[stage].html

Example:
.octave-deal-coach/acme-corp-elevate-2026-03-03/acme-corp-elevate.html
```

For generic mode, use `practice` instead of company name:
```
.octave-deal-coach/practice-resonate-2026-03-03/practice-resonate.html
```

After writing the file, open it:
```bash
open "[file path]"
```

---

#### Mode 3: Coaching Deck (DK-1 through DK-3)

##### DK-1: Style Selection

Same as MS-1. Use stage-appropriate default presets.

##### DK-2: Generate Slide Outline

Present the slide outline for approval. Slide content varies by stage:

**Resonate (~7 slides):**
1. Title Slide — "[Company] — Resonate" + stage badge
2. Stage Context — Deal position, buyer's journey phase, buyer mindset assessment
3. Buyer Mindset Deep Dive — Awareness level, trigger, constraints, adaptation guidance
4. Discovery Principles — Go wide, go deep, go high — applied to this deal
5. Value Propositions — Stage-appropriate props with deployment guidance
6. Talking Points — Discovery questions and conversation starters with listening cues
7. Next Steps — Transition checklist to Elevate

**Elevate (~9 slides):**
1. Title Slide — "[Company] — Elevate" + stage badge
2. Stage Context — Deal position, competitive landscape, buyer mindset
3. Buyer Mindset Deep Dive — Status quo attachment, change readiness, evaluation mode
4. The Case for Change — The Shift → The Stakes → The Possibility for this deal
5. Differentiated Value — What's unique AND important to this buyer
6. Value Propositions — Value Framing examples (Product → Buyer → Executive voice)
7. Talking Points — Case for Change talk tracks + differentiation delivery
8. Proof Points — Evidence grid with deployment guidance
9. Next Steps — Transition checklist to Compel

**Compel (~9 slides):**
1. Title Slide — "[Company] — Compel" + stage badge
2. Stage Context — Decision dynamics, stakeholder positions, buyer mindset
3. Buyer Mindset Deep Dive — Decision process, champion strength, detractors, risk appetite
4. Before vs. After — Side-by-side with quantified delta
5. Value Chain — Capability → workflow improvement → business outcome → financial result
6. Value Propositions — ROI-focused props with quantified outcomes per stakeholder
7. The Why Now Case — Business urgency + personal urgency
8. Talking Points — Business case narration + champion enablement scripts
9. Next Steps — Decision pathway and timeline

Present outline and ask:

```
Generate this deck?
1. Yes — generate
2. Adjust slides
3. Change style
4. Start over
```

##### DK-3: Generate HTML Deck

Use slide templates from `references/html-templates.md` for a self-contained HTML file with scroll-snap slide architecture.

**Viewport fitting rules** (from `deck/SKILL.md`):
- ALL font sizes use `clamp()` — never fixed px
- ALL spacing uses `clamp()`
- Strict content per slide: Title = 1 heading + 1 subtitle; Content = 1 heading + 4-6 bullets; Grid = max 6 cards
- If content exceeds limits, split into additional slides
- `overflow: hidden` on every `.slide`
- Media queries at 700px, 600px, 500px for short viewports

**Animation:**
- Staggered entrance via Intersection Observer
- `.animate-in` class with opacity + translateY
- `nth-child` stagger delays
- Respect `prefers-reduced-motion`

**Navigation:**
- Keyboard: ArrowDown/Up, Space, PageDown/Up
- Scroll snap for touch/trackpad
- Progress bar + nav dots
- Print: `page-break-after: always`, remove snap

**Output location:**
```
.octave-deal-coach/
  [company-kebab]-deck-[stage]-[YYYY-MM-DD]/
    [company-kebab]-deck-[stage].html
```

After writing, open in browser:
```bash
open "[file path]"
```

---

#### Mode 4: Interactive Quiz (QZ-1 through QZ-4)

##### QZ-1: Choose Quiz Type

```
AskUserQuestion({
  questions: [{
    question: "What type of coaching quiz do you want?",
    header: "Quiz Type",
    options: [
      {
        label: "Stage Recognition",
        description: "A buyer says X — which coaching stage? Tests your ability to diagnose where a deal is."
      },
      {
        label: "Methodology Application",
        description: "You're in [Stage] — what's the right Buyer Mindset, Value Props, and Talking Points approach? Tests methodology knowledge."
      },
      {
        label: "Talk Track Completion",
        description: "Buyer says [objection/question]. Using the coaching methodology, what's your response?"
      },
      {
        label: "Full Review",
        description: "Mix of all categories covering Resonate, Elevate, and Compel. Comprehensive assessment."
      }
    ],
    multiSelect: false
  },
  {
    question: "How many questions?",
    header: "Length",
    options: [
      {
        label: "Quick (5 questions)",
        description: "Fast check — 5-10 minutes"
      },
      {
        label: "Standard (10 questions)",
        description: "Thorough assessment — 15-20 minutes"
      },
      {
        label: "Deep (15 questions)",
        description: "Comprehensive review — 25-30 minutes"
      }
    ],
    multiSelect: false
  }]
})
```

##### QZ-2: Load Quiz Material

Load coaching content from reference files. If deal-specific, ground questions in actual deal data. If generic, use playbook-level data.

Build question bank by category:

**Stage Recognition:**
- Present a buyer quote or scenario → ask which stage
- Use findings and CRM data for realistic scenarios
- Include red herrings (scenarios that seem like one stage but are actually another)

**Methodology Application:**
- Name a stage → ask for the right approach
- E.g., "You're in Elevate. What are the three beats of the Case for Change?"
- E.g., "A buyer says they're evaluating competitors. Which coaching output fields should you focus on, and what goes in each?"
- Include application questions that test Buyer Mindset → Value Props → Talking Points mapping

**Talk Track Completion:**
- Present a buyer statement → ask for the methodology-backed response
- E.g., "Buyer: 'We're happy with what we have.' Using the Elevate methodology, what do you say next?"
- Score on methodology adherence AND natural delivery

**Full Review:**
- Mix all categories
- Weight toward the selected/inferred stage
- Ensure coverage across all three stages

##### QZ-3: Run the Quiz

Present questions one at a time:

```
QUESTION [N]/[Total]
Category: [Stage Recognition / Methodology Application / Talk Track Completion]
Stage: [Resonate / Elevate / Compel]
[If deal-grounded: "Based on your [Company] deal"]

[Question text]

[For multiple choice: Present 4 options]
[For open-ended: Ask the user to type their response]
```

After each answer:

```
[Correct / Partially Correct / Incorrect]

[Brief explanation referencing specific coaching elements]
[If deal-grounded: How this applies to their specific deal]

Score so far: [X]/[N]
```

##### QZ-4: Quiz Results

See [mode-output-templates.md](references/mode-output-templates.md) for the full quiz results template with breakdowns by stage, dimension, and category.

After results:

```
Want to:
1. Retake this quiz
2. Take a quiz focused on your weakest area ([Stage])
3. Practice a role play for your weakest area
4. Get a coaching microsite for your weakest area
5. Try a different output mode
6. Done
```

---

### Step 6: Delivery + Next Actions (CT-6)

After delivering any output, offer iterations:

For **Role Play** and **Quiz**: Next actions are included in RP-4 and QZ-4 above.

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
| `get_playbook` | Full playbook with value props, messaging, positioning |
| `get_entity` | Individual entity details (persona, competitor, proof point) |

### Library — Searching
| Tool | Purpose |
|------|---------|
| `search_knowledge_base` | Find matching playbooks, guides, research |
| `search_resources` | Find relevant resources (docs, presentations) |
| `list_all_entities` | List personas, competitors, proof points, references |
| `list_findings` | Objections, pain points, competitor mentions from conversations |
| `list_events` | Deal history, stage changes, activity timeline |

### Content Generation
| Tool | Purpose |
|------|---------|
| `generate_content` | Generate supporting content if needed |

---

## Error Handling

> **No CRM data found:** "I couldn't find CRM records for [domain]. I'll proceed with library-level data only. Stage inference will rely on findings and events. You can also manually select a stage."

> **No playbook found:** "No matching playbook found. I'll use general coaching methodology without playbook-specific grounding. Talk tracks will reference the framework but won't include your specific messaging. Consider running `/octave:library` to check your playbook setup."

> **No findings/events:** "No conversation findings or events found for [domain]. Stage inference will rely primarily on CRM stage. For more accurate coaching, ensure conversation data is synced to Octave."

> **Reference file not found:** "Could not load [reference file]. Falling back to general coaching methodology. For full coaching, ensure reference files are in `skills/deal-coach/references/`."

> **Stage inference low confidence:** "I'm not confident about the coaching stage — multiple stages scored similarly. I'd recommend selecting manually. Here are all options: [present all three stages]."

> **MCP connection failed:** "Could not connect to Octave. Check your connection with `/octave:workspace`. Deal coaching requires Octave MCP tools for deal context and library data."

> **HTML write failed:** "Could not write the HTML file. Check that `.octave-deal-coach/` is writable. Try: `mkdir -p .octave-deal-coach`"

---

## Related Skills

- `/octave:train` — Generic sales training (role play, quiz, guided learning) without deal coaching methodology
- `/octave:meeting-prep` — Strategic meeting battle plan as HTML
- `/octave:deck` — General-purpose slide deck builder
- `/octave:pipeline` — Deal coaching and pipeline management
- `/octave:enablement` — Sales enablement materials (cheat sheets, objection guides)
- `/octave:battlecard` — Competitive intelligence and battlecards
- `/octave:research` — Account and person research
