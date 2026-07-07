# Mode 2: Coaching Microsite (MS-1 through MS-3)

Self-contained HTML coaching page organized around Buyer Mindset / Value Propositions / Talking Points.

## MS-1: Style Selection

Reference the style preset system in [style-presets.md](../../shared/style-presets.md). If a brand kit exists for the company, prefer it — see [brand-kit-usage.md](../../shared/brand-kit-usage.md).

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
      { label: "[Default Preset] (Recommended)", description: "[Preset description]" },
      { label: "Pick a different style", description: "Choose from available presets" },
      { label: "Auto-pick from brand", description: "Use the company's brand kit (or capture one) to generate a custom theme" }
    ],
    multiSelect: false
  }]
})
```

If the user picks "Pick a different style," present mood-based preview options from the preset system.

## MS-2: Generate Content Outline

Before generating HTML, present the content plan:

See [mode-output-templates.md](mode-output-templates.md) for the microsite content outline template with full structure, design principles, and Octave sources block.

## MS-3: Generate HTML

Use templates from [html-templates.md](html-templates.md) to generate a self-contained HTML file. Follow that file's **Design Principles** section for the section structure (hero, collapsible sections, The Play footer), collapse behavior, and no-duplicate-content rules — do not restate or deviate from them.

**Content grounding rules** (from [messaging-narratives.md](messaging-narratives.md)):
- Every Value Proposition must reference specific Motion ICP narrative content (Strategic narrative / Benefits and impacts) — never generic claims
- Every proof point must cite a specific library entity, appear inline in the section it supports, and include a usage note (deploy now / save for later / already shared)
- Every Talking Point must be grounded in the deal context (if available) and connected to the Buyer Mindset
- Every objection response must be grounded in the specific decision the buyer is making — not generic competitive objections
- Use "perspective-shifting question" framing — collaborative, not adversarial
- This is a selling tool — orient language around advancing the deal

**Presentation rules specific to this mode:**
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
