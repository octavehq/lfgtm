# Deck Intake Questions

Interactive intake for `/octave:deck` Step 1. Ask only what wasn't already provided via flags or the prompt, using AskUserQuestion where available.

## Purpose — "What kind of deck is this?"

```
What kind of deck are you building?

1. Customer pitch / pre-demo deck
2. Customer QBR / business review
3. Internal strategy / planning
4. Conference talk / keynote
5. Product launch / GTM plan
6. Competitive battlecard presentation
7. Sales enablement / training
8. Something else (describe it)

Your choice:
```

## Goal — "What's the outcome you want?"

```
What outcome should this deck drive?

1. Close a deal / advance an opportunity
2. Educate / enable a team
3. Get executive buy-in
4. Win a competitive deal
5. Launch a product or campaign
6. Other (describe it)

Your choice:
```

## Audience — "Who is this for?"

```
Who's the audience?

Provide any of the following:
• Company name or domain (e.g., acme.com)
• Person name or email (e.g., jane@acme.com)
• Role/title description (e.g., "VP Sales at mid-market SaaS")
• General audience (e.g., "internal sales team", "board of directors")

Target:
```

## Content readiness — "How much do you have already?"

```
How much content do you have?

1. I have content ready — I'll paste or describe it
2. I have rough notes — I'll share, you help me structure
3. Help me figure it out — Octave drives the content strategy
4. I have a PPTX file — convert and enhance it

Your choice:
```

If a `.pptx` file is provided, jump to the PPTX Conversion Path in SKILL.md before continuing.

## Length — "How long should this be?"

If the user provided existing content (PPTX, notes, or pasted content), offer to keep, shorten, or expand:

```
Your source has ~[N] slides worth of content. What length do you want?

1. Keep similar — stay around [N] slides
2. Shorter — condense to the essentials
3. Longer — expand with more detail and data
4. Custom — I have a specific slide count in mind

Your choice:
```

If starting from scratch, ask based on purpose:

```
How long should this deck be?

1. Short (5-8 slides) — punchy, high-impact, perfect for pitches and exec summaries
2. Medium (10-15 slides) — standard for most presentations
3. Long (18-25 slides) — detailed deep-dives, enablement, or QBRs
4. Custom — I have a specific slide count in mind

Your choice:
```

| Purpose | Recommended Default |
|---------|-------------------|
| Customer pitch / pre-demo | Short (5-8) |
| Customer QBR / review | Long (18-25) |
| Internal strategy | Medium (10-15) |
| Conference keynote | Medium (10-15) |
| Product launch / GTM | Long (18-25) |
| Competitive battlecard | Short (5-8) |
| Sales enablement | Long (18-25) |

Use the recommended default as the pre-selected option. If the user picks "Custom," ask for a target slide count.

## Density — "How should each slide read?"

```
How dense should each slide be?

1. Speaker-led (low density) — big ideas, generous space, 1-3 bullets max,
   more slides. Best for live pitches, keynotes, exec rooms.
2. Reading-first (high density) — self-contained, structured grids,
   4-8 bullets or 4-6 cards, tighter spacing. Best for QBRs, async/leave-behind decks.

Your choice:
```

Default by purpose: pitches/keynotes/competitive → **speaker-led**; QBRs/enablement/launch/strategy → **reading-first**. Carry this choice through generation: it drives the content density limits per slide type (split into more slides rather than shrink text or overflow). Either way, no scrolling and no cramped text — the fixed stage scales the whole slide, it does not add room.
