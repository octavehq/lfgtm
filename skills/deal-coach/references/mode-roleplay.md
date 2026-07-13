# Mode 1: Role Play (RP-1 through RP-4)

Coaching-backed conversation practice scored against Buyer Mindset, Value Propositions, and Talking Points.

The session runs on the shared role-play engine — see [roleplay-mechanics.md](../../shared/roleplay-mechanics.md) for difficulty tiers, buyer-playing rules, session length (8-12 exchanges), and scorecard mechanics. This file defines the methodology-specific layer: stage-scoped scenarios, stage-specific buyer psychology, and the coaching rubric.

## RP-1: Setup the Scenario

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
      { label: "Friendly", description: "Buyer is open and receptive. Good for learning the coaching framework." },
      { label: "Skeptical", description: "Buyer pushes back moderately. Tests methodology under pressure." },
      { label: "Hostile", description: "Buyer is resistant, dismissive, or aggressive. Tests advanced skills and composure." }
    ],
    multiSelect: false
  }]
})
```

If in specific-deal mode, identify the buyer persona from entities gathered in Step 2 of the skill. If generic, let the user choose from available personas (dynamically populated from `list_entities({ entityType: "persona" })`, up to 4 options with title/role descriptions).

## RP-2: Load Stage-Specific Intelligence

Load the coaching agent's rubric and grounding map for the selected stage (from [coaching-agents.md](coaching-agents.md) and [messaging-narratives.md](messaging-narratives.md)).

For deal-specific mode, map all Octave data to coaching output fields using [messaging-narratives.md](messaging-narratives.md). For generic mode, use the Default Motion Playbook narrative data (Motion ICP cell) to create a representative scenario.

Prepare buyer behavior rules based on stage:

| Stage | Buyer Psychology | Behavior Rules |
|-------|-----------------|---------------|
| Resonate | Exploratory, guarded | Shares surface problems, tests whether seller digs deeper. Friendly: volunteers info. Hostile: one-word answers. |
| Elevate | Status quo defender / comparison shopper | Resists change, references competitors. Friendly: open to new perspective. Hostile: "We've been doing fine for years" / "Your competitor does that too." |
| Compel | Analytical, needs numbers, risk-averse | Asks about ROI, pushes back on vague claims. Friendly: engages with data. Hostile: "Those numbers don't apply to us" / "Now is not the right time." |

## RP-3: Run the Role Play

Set the scene — see [mode-output-templates.md](mode-output-templates.md) for the role play scene setup template.

Then begin as the buyer persona, following the shared engine's buyer-playing rules with these methodology-specific additions:

- Apply the stage-appropriate behavior from the table above
- Drop stage-relevant cues that a well-trained seller should pick up on

For **Full Journey Simulation**:
- Start at Resonate and progress through each stage
- After each stage, pause: "Good — let's fast-forward. [Context for next stage]."
- Score each stage independently, then provide a cumulative scorecard

## RP-4: Coaching Scorecard

After the role play ends:

See [mode-output-templates.md](mode-output-templates.md) for the full coaching scorecard template with stage-specific talking points rubrics. Score the three coaching dimensions — Buyer Mindset, Value Propositions, Talking Points — using the active coaching agent's rubric from [coaching-agents.md](coaching-agents.md).

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
