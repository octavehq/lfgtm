# Coaching Microsite Templates (MS-1 through MS-3)

## MS-1: Style Selection

Reference the style preset system from `skills/deck/references/STYLE_PRESETS.md`.

Stage default presets:

| Stage | Default Preset | Rationale |
|-------|---------------|-----------|
| Resonate | `soft-light` | Exploratory, calm, trust-building |
| Elevate | `midnight-pro` | Urgency, disruption, bold contrast |
| Compel | `executive-dark` | Business gravitas, financial seriousness |

Present with override option:

```
AskUserQuestion({
  questions: [{
    question: "The default style for [Stage] is [preset name] ([rationale]). Want to use it or pick a different style?",
    header: "Style",
    options: [
      { label: "[Default Preset] (Recommended)", description: "[Preset description]" },
      { label: "Pick a different style", description: "Choose from available presets" },
      { label: "Auto-pick from brand", description: "Extract colors from the company's website" }
    ],
    multiSelect: false
  }]
})
```

If "Pick a different style," present mood-based preview options (follow `deck/SKILL.md` Step 4 pattern).

## MS-2: Content Outline

Present before generating HTML:

```
COACHING MICROSITE OUTLINE
==========================
Company: [Company Name]
Stage: [Resonate / Elevate / Compel] — [Stage subLabel]
Coaching Agent: [Agent Name]
Style: [Preset Name]

STRUCTURE
---------
Header + Deal Brief    — Company info, date, coaching stage badge, deal stats grid
Priority Actions       — 3 quick-hit actions before next meeting (collapsible)
Deal Activity          — Compact vertical timeline of deal events (collapsible)
Journey Map            — 3-phase coaching journey showing position + context (collapsible)
Section 01: Stage Assessment     — Inference evidence, confidence
Section 02: Buyer Mindset        — Psychology, awareness, triggers, adaptation guidance
Section 03: Value Propositions   — Stage-appropriate props with deployment + usage notes
Section 04: Talking Points       — Stage-specific talk tracks (strategic point + quote + evidence)
Section 05: Objection Handling   — Buyer decision-frame-grounded objections + responses
Section 06: Next Stage Preview   — Transition checklist + next agent preview
[Optional] Section 07: Deal Gaps (MEDDPICC) — Coverage assessment + gap-to-action mapping
The Play               — Strategic one-liner + concrete next action

OCTAVE SOURCES
--------------
- Playbook: [Name] | Personas: [N] | Proof Points: [N] | Findings: [N] | Competitors: [N]
- CRM: [Stage, Amount, Close Date or "Generic mode"]

Generate?  1. Yes  2. Adjust sections  3. Change style  4. Start over
```

## MS-3: HTML Generation Rules

Use templates from `references/html-templates.md`.

### Content Grounding (from `references/messaging-narratives.md`)
- Every Value Proposition references specific playbook messaging
- Every proof point cites a library entity inline with usage note (deploy now / save / already shared)
- Every Talking Point grounded in deal context, connected to Buyer Mindset
- Objection responses grounded in the specific decision the buyer is making
- Use "perspective-shifting question" framing — collaborative, not adversarial
- Orient language around advancing the deal

### Structural Rules
- Header + Deal Brief: NOT collapsible — full-width gradient hero with deal stats
- Priority Actions, Deal Activity, Journey Map: collapsible `<details>` with +/- toggle
- Sections 01-06 (07 if MEDDPICC): collapsible `<details>`, ALL start COLLAPSED
- The Play: NOT collapsible — full-width gradient footer
- No duplicate content between sections; evidence goes inline
- Talking Points use practical deal-specific headers (NOT framework labels like "The Shift")
- Use "Coaching Stage: [Name]" badge only (not both "Elevate" and "Evaluate")

### Content Density Limits
| Section | Limit |
|---------|-------|
| Header + Deal Brief | Company info + 4-6 deal stats + stage badge + subtitle |
| Priority Actions | Exactly 3 actions |
| Deal Activity | 3-6 timeline entries |
| Journey Map | 3 phases with generic + deal-specific context |
| Stage Assessment | 3-4 evidence cards + confidence |
| Buyer Mindset | Narrative + 3-5 signals + adaptation guidance |
| Value Propositions | 4-6 props with evidence + usage notes |
| Talking Points | 4-6 tracks (point + quote + evidence) |
| Objection Handling | 3-5 objections |
| Next Stage Preview | 1 checklist + agent preview |
| Deal Gaps (MEDDPICC) | 8 elements + gap-to-action (if included) |
| The Play | 1 strategic sentence + 1 action |

### Design Principles
- Three coaching outputs (Buyer Mindset, Value Props, Talking Points) are the organizing principle
- Talk tracks: strategic point (bold, practical) → sample quote (italic) → "Use when..." guidance
- MEDDPICC is optional, not primary structure
- No duplicate content; each piece appears once
