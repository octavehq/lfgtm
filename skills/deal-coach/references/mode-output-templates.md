# Mode Output Templates

Large output templates the agent renders into for each deal-coach mode.

---

## RP-3: Role Play Scene Setup

```
=======================================
DEAL COACHING ROLE PLAY: [Stage]
=======================================

THE SCENE
---------
You are a seller from [company/product] meeting with [Persona Name], [Title] at [Company].
[If deal-specific: Brief deal context from CRM]
[If generic: Practice scenario description]

COACHING STAGE: [Resonate / Elevate / Compel]
[Stage subLabel — e.g., "Understand and resonate with the buyer"]

Your goal is to demonstrate strong execution across:
- Buyer Mindset — accurately read and adapt to the buyer
- Value Propositions — deploy the right props for this stage
- Talking Points — execute the stage's methodology naturally

BUYER PROFILE
- Name: [Persona Name]
- Role: [Title]
- Mindset: [Stage-appropriate psychology]
- Difficulty: [Friendly/Skeptical/Hostile]

RULES
-----
1. This is a CONVERSATION — respond naturally as the seller
2. I will play [Persona Name] with [difficulty]-level resistance
3. The conversation will run 8-12 exchanges
4. You'll be scored on Buyer Mindset, Value Props, and Talking Points
5. I'll signal when the conversation is wrapping up
6. Stay in character — no breaking the fourth wall

Ready? I'll start as [Persona Name]...
=======================================
```

---

## RP-4: Coaching Scorecard

```
DEAL COACHING SCORECARD
=======================
Stage: [Resonate / Elevate / Compel]
Coaching Agent: [Agent Name]
Difficulty: [Friendly/Skeptical/Hostile]
Persona: [Buyer Name], [Title]

BUYER MINDSET
-------------
| Criterion | Score | Notes |
|-----------|-------|-------|
| Awareness read | [1-5] | [Did they correctly assess where the buyer is?] |
| Adaptation | [1-5] | [Did they adjust their approach based on buyer signals?] |
| Psychology match | [1-5] | [Did they match the buyer's emotional state before trying to move it?] |

Buyer Mindset Score: [avg]/5

VALUE PROPOSITIONS
------------------
| Criterion | Score | Notes |
|-----------|-------|-------|
| Stage appropriateness | [1-5] | [Did they use props fitting for this stage?] |
| Selection quality | [1-5] | [Did they pick the most impactful props available?] |
| Deployment timing | [1-5] | [Did they introduce props at the right moment?] |

Value Propositions Score: [avg]/5

TALKING POINTS
--------------
[Scoring varies by stage — use the stage-specific criteria from coaching-agents.md]

[Resonate:]
| Criterion | Score | Notes |
|-----------|-------|-------|
| Going wide | [1-5] | [Did they map the landscape — stakeholders, history, context?] |
| Going deep | [1-5] | [Did they find root causes, not just symptoms?] |
| Going high | [1-5] | [Did they connect to business and personal impact?] |
| Problem statement quality | [1-5] | [Did they arrive at a crisp, multi-dimensional problem?] |

[Elevate:]
| Criterion | Score | Notes |
|-----------|-------|-------|
| Case for Change delivery | [1-5] | [Did they hit the three beats — Shift, Stakes, Possibility?] |
| Value Framing | [1-5] | [Did they translate to Buyer/Executive voice, not just Product voice?] |
| Differentiation quality | [1-5] | [Did they focus on differentiated value?] |
| Proof point usage | [1-5] | [Did they use specific, credible proof?] |

[Compel:]
| Criterion | Score | Notes |
|-----------|-------|-------|
| Business case quality | [1-5] | [Did they co-create quantified value?] |
| Value chain clarity | [1-5] | [Did they map capability → outcome → dollars?] |
| Why Now execution | [1-5] | [Both dimensions — business and personal urgency?] |
| Champion enablement | [1-5] | [Did they arm the champion?] |

Talking Points Score: [avg]/5

GENERAL SELLING SKILLS
----------------------
| Element | Score | Notes |
|---------|-------|-------|
| Opening / rapport | [1-5] | [Assessment] |
| Active listening | [1-5] | [Assessment] |
| Proof point usage | [1-5] | [Assessment] |
| Call control | [1-5] | [Assessment] |
| Natural delivery | [1-5] | [Assessment] |

OVERALL SCORE: [X]/5
Buyer Mindset: [avg]/5 | Value Props: [avg]/5 | Talking Points: [avg]/5 | General: [avg]/5

KEY MOMENTS
-----------
[Quote from conversation + assessment — what was done well or could improve]
[Repeat for 3-5 key moments]

COACH SAYS
----------
[2-3 paragraphs of specific coaching advice from the stage's coaching agent persona.
Reference specific Talking Points from frameworks.md.
Ground in the seller's playbook messaging.
Identify #1 area for improvement and give a concrete example of what to say instead.]

VALUE PROPS YOU COULD HAVE USED
-------------------------------
[List 3-5 value props from the library that would have strengthened the conversation, with:
- The prop itself
- When to deploy it (which moment in the conversation)
- How to frame it for this stage (Buyer/Executive voice, not feature pitch)]
```

---

## MS-2: Microsite Content Outline

```
COACHING MICROSITE OUTLINE
==========================
Company: [Company Name]
Stage: [Resonate / Elevate / Compel] — [Stage subLabel]
Coaching Agent: [Agent Name]
Style: [Preset Name]

STRUCTURE
---------
Header + Deal Brief    — Company name, industry, date, coaching stage badge,
                         deal-specific subtitle, deal stats grid
Priority Actions       — 3 quick-hit actions before the next meeting (collapsible)
Deal Activity          — Compact vertical timeline of deal events with dates (collapsible)
Journey Map            — 3-phase coaching journey (Resonate → Elevate → Compel) showing
                         where the deal is and why, with generic phase explanations AND
                         deal-specific context for each phase (collapsible)
Section 01: Stage Assessment     — How stage was inferred, evidence, confidence
Section 02: Buyer Mindset        — Buyer psychology assessment, awareness level, trigger,
                                   constraints, adaptation guidance
Section 03: Value Propositions   — Stage-appropriate props from library with deployment
                                   guidance, evidence inline, usage notes (deploy now vs.
                                   save for later stage vs. already shared)
Section 04: Talking Points       — Stage-specific talk tracks organized by conversation
                                   flow, with strategic point + sample quote + evidence.
                                   Do NOT use framework labels as headers (e.g., "The Shift").
                                   Use practical, deal-specific language.
Section 05: Objection Handling   — Likely objections grounded in buyer's actual decision
                                   frame, with stage-appropriate responses
Section 06: Next Stage Preview   — Transition checklist + next coaching agent preview
[Optional] Section 07: Deal Gaps (MEDDPICC) — Coverage assessment with gap-to-action mapping
The Play               — Strategic one-liner + concrete "your next move is X" action

DESIGN PRINCIPLES
-----------------
- The three coaching outputs (Buyer Mindset, Value Props, Talking Points) are the
  organizing principle
- Evidence (proof points, metrics) is folded INTO the relevant sections inline,
  not in a standalone section
- Objections go in Section 05, grounded in the buyer's actual decision frame
  (build vs. buy, do-nothing vs. act, this vendor vs. that)
- MEDDPICC is available as an optional section — not the primary structure
- Talk tracks use a two-layer structure: strategic point (bold, practical deal
  language — NOT framework labels) then sample quote (italic, one way to express it).
  Each includes "Use when..." guidance for timing.
- No duplicate content between sections. Each piece of information appears once.
- Use "perspective-shifting question" framing — tone is collaborative and consultative
- This is a selling tool. Orient language around advancing the deal.

OCTAVE SOURCES
--------------
- Playbook: [Playbook Name]
- Personas: [N] loaded
- Proof Points: [N] loaded
- Findings: [N] loaded
- Competitors: [N] loaded
- CRM: [Stage, Amount, Close Date or "Generic mode — no CRM data"]

Generate this microsite?
1. Yes — generate
2. Adjust sections
3. Change style
4. Start over
```

---

## QZ-4: Quiz Results

```
COACHING QUIZ RESULTS
=====================
Score: [X]/[Total] ([Percentage]%)
Category: [Quiz Type]
Grounding: [Deal-specific: Company Name / Generic Practice]

BREAKDOWN BY COACHING STAGE
----------------------------
| Stage | Questions | Correct | Score | Assessment |
|-------|-----------|---------|-------|------------|
| Resonate | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |
| Elevate  | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |
| Compel   | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |

BREAKDOWN BY COACHING DIMENSION
---------------------------------
| Dimension | Questions | Correct | Score |
|-----------|-----------|---------|-------|
| Buyer Mindset | [N] | [N] | [X]% |
| Value Propositions | [N] | [N] | [X]% |
| Talking Points | [N] | [N] | [X]% |

BREAKDOWN BY CATEGORY
----------------------
| Category | Questions | Correct | Score |
|----------|-----------|---------|-------|
| Stage Recognition | [N] | [N] | [X]% |
| Methodology Application | [N] | [N] | [X]% |
| Talk Track Completion | [N] | [N] | [X]% |

STRENGTHS
---------
[2-3 areas of strong knowledge with specific examples]

GAPS TO FOCUS ON
----------------
[2-3 areas needing improvement with specific coaching references]

[For each gap:]
- Recommended: Practice [Stage] role play with [difficulty]
- Study: Review [specific section] of frameworks.md
- Exercise: Try building a [Buyer Mindset / Value Props / Talking Points] for a real deal

RECOMMENDED NEXT STEPS
----------------------
1. [Primary recommendation]
2. [Secondary recommendation]
3. [Optional stretch recommendation]
```
