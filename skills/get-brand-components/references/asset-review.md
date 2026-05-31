# Asset review pass (optional)

A post-generation QA pass for any asset produced from a brand kit (deck, one-pager, microsite, battlecard, proposal, brief, etc.). It is **opt-in** — offer it, never force it.

**Offer wording (after the asset is generated):**
> "Want me to run a quick review pass over this — layout, brand, narrative, groundedness, and AI-slop? I'll render it, inspect it, and report what I'd fix."

If the user declines, skip silently. If they accept, run all five dimensions below, then report **one short scorecard** of specific, located findings (e.g. `slide 2: bottom card row clipped`), fix what you can, and **re-verify** (re-render and re-check the dimensions you changed). Don't claim a clean pass without actually rendering and looking.

---

## How to run it

1. **Render the actual output**, don't review the spec/source. Screenshot it:
   - Docs (one-pager, proposal, brief, microsite, battlecard): full-page PNG via `scripts/render.py --file <out.html> --out <png> --width <docwidth+60>`.
   - Decks: the fixed 1920×1080 stage means each slide must fit its own canvas. **Measure every slide's content height** (load the deck, set slides to `position:static;height:auto`, read each `.inner` `scrollHeight`); anything `> 1080` is clipped at runtime by `overflow:hidden`. Then screenshot a stacked-verify (all slides `position:static`, natural height) to eyeball them.
2. **Look at the pixels.** This is a multimodal check — open the screenshots and actually inspect them. The most common defects (overflow, misalignment, white-on-white) are invisible in the source and only show in the render.
3. **Score each dimension** below: pass, or a list of located findings.
4. **Fix → re-verify.** Re-render and re-measure the parts you touched.

---

## The five dimensions

### 1. Visual appearance (layout)
Most layout-focused. Check the render, not the code.
- **Overflow / clipping:** no content cut off by a slide canvas or container. For decks, every slide's content height ≤ 1080 (measure it). For docs, no element bleeding outside the sheet.
- **Alignment:** shared left edges across header/body/footer; grid columns aligned; nothing visually off-axis.
- **Scaling:** images sharp and correctly proportioned; the deck stage scales and letterboxes cleanly at multiple window aspect ratios.
- **Padding/rhythm:** consistent section padding; no cramped or colliding blocks; even gutters.
- **Surfaces:** dark text on dark band or white logo on white footer = fail (the renderer picks per-surface assets — confirm it actually did).

### 2. Brand adherence
Against the kit's `brand-kit.md` → **Signature moves** and `manifest.render.tokens`.
- Correct **fonts** rendering (the real embedded heading face, not a fallback).
- Palette matches the kit; no off-brand colors introduced.
- **Emphasis mechanism** is the brand's (color/weight/underline as the kit specifies), not invented.
- Logo, radius, shadow, texture match the kit's system.

### 3. Narrative coherence
- One clear throughline; sections in a logical order (typically hook → problem → solution → proof → ask).
- No contradictions; each section earns its place; transitions make sense.
- The title/claim matches what the body actually delivers.

### 4. Groundedness
- Every metric, quote, customer name, and capability traces to **real source material** (the Octave MCP data gathered for this asset, or the kit's real assets). Flag anything invented.
- No hallucinated proof points, fake logos, or capabilities not in the product data.
- **Imagery is earned** (see SKILL.md → "Imagery is earned, not defaulted"): screenshots truthfully illustrate their section; no logo-soup filler; no placeholder tiles posing as content.

### 5. Slop (write like a human)
Scan the asset's copy against the ruleset below. Flag specific offending phrases and rewrite. (Format affordances the asset schema requires — e.g. the renderer's `**emphasis**` spans — are exempt; the ruleset targets the prose.)

---

## WRITE_LIKE_A_HUMAN (the slop standard)

Write like a human, not a language model. The output should read like internal writing by an operator. AI patterns are obvious tells and they undermine the credibility of everything around them. Watch for and avoid the following.

**Vocabulary to replace.** Cut these words and use plain alternatives: delve, dive into, deep dive, robust, comprehensive, seamless, seamlessly, holistic, leverage (as verb), utilize, cutting-edge, state-of-the-art, world-class, actionable, impactful, learnings, best practices, thought leader, navigate (as metaphor), landscape (as metaphor), ecosystem (as metaphor), realm, paradigm, tapestry, beacon, testament to, underscores, meticulous, game-changer, watershed moment, pivotal, embrace (as metaphor), symphony (as metaphor), thriving, vibrant, bustling, nestled, ever-evolving, intricate, intricacies, daunting, in order to, due to the fact that, at its core. When two or more of these show up in the same paragraph, rewrite: harness, foster, elevate, unleash, streamline, empower, bolster, spearhead, resonate, revolutionize, facilitate, nuanced, crucial, multifaceted, myriad, plethora, encompass, catalyze, augment, cultivate, illuminate, transformative, cornerstone, paramount, poised, burgeoning, nascent, overarching.

**Sentence patterns to avoid.**
- "It's not X, it's Y" or "this isn't about X, it's about Y." State the positive directly. At most one negative contrast in the whole output, and only when the contrast carries real weight.
- Copula avoidance. Default to "is" and "has." Don't substitute "serves as," "features" (as verb), "boasts," "presents," or "represents" unless they add specific meaning.
- Rhetorical question openers ("So what does this mean for…?", "What's next?"). If you know the answer, say it.
- Filler phrases: "the reality is that," "it is important to note that," "when it comes to," "in terms of," "at the end of the day."
- Hollow intensifiers: "genuine," "real" (as adjective), "truly," "actually" (as intensifier), "quite frankly," "to be honest." If the word strengthens nothing, delete it.
- Hedging and confidence-steering: "perhaps," "could potentially," "notably," "interestingly," "surprisingly," "importantly," "it's worth noting." Make the point. Let the fact speak.
- Formulaic transitions: "Moreover," "Furthermore," "Additionally," "In today's [X]," "In an era where." Restructure so the connection is obvious.
- Engagement-bait framings: "the failure mode nobody's naming," "what nobody's telling you about," "here's what's interesting," "what stood out was." Don't pre-announce importance.

**Significance and tone.**
- No significance inflation. Cut "marking a pivotal moment," "watershed moment," "transformative," "unprecedented," "game-changing." State what is and let the reader judge.
- No tour-brochure description. Cut "thriving ecosystem," "vibrant hub," "nestled in," "bustling." Plain description only.
- No announced emotion or surprise as a structural crutch. "What surprised me most…", "I was fascinated to discover…" The content should convey the reaction.
- No generic conclusions. Cut "the future looks bright," "only time will tell," "as we move forward." If a closing thought is needed, make it specific.
- No present-participle pseudo-analysis ("…symbolizing X, reflecting Y, showcasing Z"). Replace with specific facts or cut.
- No false ranges or false concessions. Cut "from ancient civilizations to modern startups." Cut "while X is impressive, Y remains a challenge." Pick a side or name specifics.

**Formatting and rhythm.**
- Plain text. No emoji. No em dashes, use commas, periods, colons, parentheses, or rewrite as two sentences. No bolding or other formatting inside generated content unless the entity schema explicitly requires it.
- Vary sentence length. Mix short, punchy lines with longer ones. Fragments are fine. Uniform pacing is one of the strongest AI tells.
- No synonym cycling. If the same noun or verb is the right word three times, use it three times. Forced variation reads as thesaurus abuse.

---

## Scorecard format

Report concisely, located, actionable:

```
REVIEW — <asset name>
1. Visual ......... <PASS | findings: slide 2 bottom row clipped (content 1314px > 1080); footer padding uneven>
2. Brand .......... <PASS | findings: heading rendering fallback font, not Alliance>
3. Narrative ...... <PASS | findings: proof section precedes the problem — reorder>
4. Groundedness ... <PASS | findings: "10x faster" metric not in source data — cut or source it>
5. Slop ........... <PASS | findings: "seamless", "leverage", one "it's not X it's Y" — rewrites below>

Fixing: <what you'll change>  →  re-verify.
```

Keep it tight. Specific findings beat a generic "looks good."
