# Role Play Templates (RP-1 through RP-4)

## RP-1: Scenario Setup

Present scenario options:

```
AskUserQuestion({
  questions: [{
    question: "What kind of role play do you want?",
    header: "Scenario",
    options: [
      { label: "Single Stage Practice", description: "Practice one stage in a focused 8-12 exchange conversation" },
      { label: "Full Journey Simulation", description: "Walk through Resonate → Elevate → Compel in sequence" }
    ],
    multiSelect: false
  },
  {
    question: "How difficult should the buyer be?",
    header: "Difficulty",
    options: [
      { label: "Friendly", description: "Buyer is open and receptive" },
      { label: "Skeptical", description: "Buyer pushes back moderately" },
      { label: "Hostile", description: "Buyer is resistant or aggressive" }
    ],
    multiSelect: false
  }]
})
```

If deal-specific, identify buyer persona from entities. If generic, let user choose:

```
AskUserQuestion({
  questions: [{
    question: "Which persona should the buyer represent?",
    header: "Buyer Persona",
    options: [
      // Dynamically populated from list_all_entities({ entityType: "persona" })
      { label: "[Persona Name]", description: "[Persona title/role]" }
      // ... up to 4 personas
    ],
    multiSelect: false
  }]
})
```

## RP-2: Stage-Specific Buyer Behavior Rules

Load the coaching agent's rubric and grounding map. Map Octave data via `references/messaging-narratives.md` (deal-specific) or use playbook-level data (generic).

| Stage | Buyer Psychology | Behavior Rules |
|-------|-----------------|---------------|
| Resonate | Exploratory, guarded | Shares surface problems, tests whether seller digs deeper. Friendly: volunteers info. Hostile: one-word answers. |
| Elevate | Status quo defender / comparison shopper | Resists change, references competitors. Friendly: open to new perspective. Hostile: "We've been doing fine for years" / "Your competitor does that too." |
| Compel | Analytical, needs numbers, risk-averse | Asks about ROI, pushes back on vague claims. Friendly: engages with data. Hostile: "Those numbers don't apply to us" / "Now is not the right time." |

## RP-3: Scene Template

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
[Stage subLabel]

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

**Buyer play rules:**
- Adjust resistance based on difficulty level
- Drop stage-relevant cues a well-trained seller should pick up on
- Friendly: verbal rewards for correct methodology. Skeptical: push back on weak points. Hostile: resist aggressively, only yield to excellent execution.
- After 8-12 exchanges, signal wrap-up: "I think we're running short on time..."

**Full Journey Simulation:** Start at Resonate, progress through each stage. Pause between stages: "Good — let's fast-forward." Score each stage independently, then cumulative.

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
[Use stage-specific criteria from coaching-agents.md]

Resonate:
| Criterion | Score | Notes |
|-----------|-------|-------|
| Going wide | [1-5] | [Map the landscape — stakeholders, history, context] |
| Going deep | [1-5] | [Find root causes, not just symptoms] |
| Going high | [1-5] | [Connect to business and personal impact] |
| Problem statement quality | [1-5] | [Multi-dimensional problem articulation] |

Elevate:
| Criterion | Score | Notes |
|-----------|-------|-------|
| Case for Change delivery | [1-5] | [Three beats — Shift, Stakes, Possibility] |
| Value Framing | [1-5] | [Buyer/Executive voice, not Product voice] |
| Differentiation quality | [1-5] | [Differentiated value focus] |
| Proof point usage | [1-5] | [Specific, credible proof] |

Compel:
| Criterion | Score | Notes |
|-----------|-------|-------|
| Business case quality | [1-5] | [Co-created quantified value] |
| Value chain clarity | [1-5] | [Capability → outcome → dollars] |
| Why Now execution | [1-5] | [Business and personal urgency] |
| Champion enablement | [1-5] | [Armed the champion] |

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
[Quote from conversation + assessment — 3-5 key moments]

COACH SAYS
----------
[2-3 paragraphs of specific coaching from the stage's coaching agent persona.
Reference specific Talking Points from frameworks.md.
Ground in the seller's playbook messaging.
Identify #1 area for improvement with a concrete alternative.]

VALUE PROPS YOU COULD HAVE USED
-------------------------------
[3-5 value props from the library with:
- The prop itself
- When to deploy it (which conversation moment)
- How to frame it for this stage (Buyer/Executive voice)]
```

## Post-Scorecard Options

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
