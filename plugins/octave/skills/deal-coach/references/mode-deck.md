# Mode 3: Coaching Deck (DK-1 through DK-3)

Slide presentation walking through the coaching framework for a specific deal, with stage-specific content and talk tracks.

## DK-1: Style Selection

Same as MS-1 in [mode-microsite.md](mode-microsite.md) — stage-appropriate default presets from [style-presets.md](../../shared/style-presets.md), brand kit preferred when available ([brand-kit-usage.md](../../shared/brand-kit-usage.md)).

## DK-2: Generate Slide Outline

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

## DK-3: Generate HTML Deck

Build the deck on the deck skill's HTML architecture — do not invent your own slide system:

- **Scaffold and viewport behavior:** follow [html-scaffold.md](../../deck/references/html-scaffold.md) and paste [viewport-base.css](../../deck/references/viewport-base.css) verbatim — fixed 1920×1080 stage scaled as a unit, px sizing against the canvas, print one-slide-per-page, reduced motion.
- **Slide composition:** use [slide-templates.md](../../deck/references/slide-templates.md) for layout patterns; use Part 2 of [html-templates.md](html-templates.md) for coaching-specific slide content, translating any fluid sizing in those snippets into fixed px against the 1920×1080 canvas per the scaffold's authoring rule.
- **Animation and navigation:** follow [animation-patterns.md](../../deck/references/animation-patterns.md) — staggered entrances, keyboard navigation, progress indicators.

**Content limits per slide:** Title = 1 heading + 1 subtitle; Content = 1 heading + 4-6 bullets; Grid = max 6 cards. If content exceeds limits, split into additional slides.

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
