# Coaching Deck Templates (DK-1 through DK-3)

## DK-1: Style Selection

Same as microsite style selection (see `references/microsite-templates.md` MS-1). Use stage-appropriate default presets.

## DK-2: Slide Outlines by Stage

### Resonate (~7 slides)
1. Title Slide — "[Company] — Resonate" + stage badge
2. Stage Context — Deal position, buyer's journey phase, buyer mindset assessment
3. Buyer Mindset Deep Dive — Awareness level, trigger, constraints, adaptation guidance
4. Discovery Principles — Go wide, go deep, go high — applied to this deal
5. Value Propositions — Stage-appropriate props with deployment guidance
6. Talking Points — Discovery questions and conversation starters with listening cues
7. Next Steps — Transition checklist to Elevate

### Elevate (~9 slides)
1. Title Slide — "[Company] — Elevate" + stage badge
2. Stage Context — Deal position, competitive landscape, buyer mindset
3. Buyer Mindset Deep Dive — Status quo attachment, change readiness, evaluation mode
4. The Case for Change — The Shift → The Stakes → The Possibility for this deal
5. Differentiated Value — What's unique AND important to this buyer
6. Value Propositions — Value Framing examples (Product → Buyer → Executive voice)
7. Talking Points — Case for Change talk tracks + differentiation delivery
8. Proof Points — Evidence grid with deployment guidance
9. Next Steps — Transition checklist to Compel

### Compel (~9 slides)
1. Title Slide — "[Company] — Compel" + stage badge
2. Stage Context — Decision dynamics, stakeholder positions, buyer mindset
3. Buyer Mindset Deep Dive — Decision process, champion strength, detractors, risk appetite
4. Before vs. After — Side-by-side with quantified delta
5. Value Chain — Capability → workflow improvement → business outcome → financial result
6. Value Propositions — ROI-focused props with quantified outcomes per stakeholder
7. The Why Now Case — Business urgency + personal urgency
8. Talking Points — Business case narration + champion enablement scripts
9. Next Steps — Decision pathway and timeline

Present outline: `Generate?  1. Yes  2. Adjust slides  3. Change style  4. Start over`

## DK-3: HTML Deck Generation

Use slide templates from `references/html-templates.md` for self-contained HTML with scroll-snap slide architecture.

### Viewport Fitting Rules (from `deck/SKILL.md`)
- ALL font sizes and spacing use `clamp()` — never fixed px
- Per-slide content limits: Title = 1 heading + 1 subtitle; Content = 1 heading + 4-6 bullets; Grid = max 6 cards
- If content exceeds limits, split into additional slides
- `overflow: hidden` on every `.slide`
- Media queries at 700px, 600px, 500px for short viewports

### Animation
- Staggered entrance via Intersection Observer (`.animate-in` with opacity + translateY)
- `nth-child` stagger delays
- Respect `prefers-reduced-motion`

### Navigation
- Keyboard: ArrowDown/Up, Space, PageDown/Up
- Scroll snap for touch/trackpad
- Progress bar + nav dots
- Print: `page-break-after: always`, remove snap
