# Asset review pass (runs by default)

A post-generation QA pass for any asset produced from a brand kit (deck, one-pager, microsite, battlecard, proposal, brief, meeting-prep, etc.). It **runs by default** — the user opts out with `--skip-review` or "skip review". In interactive mode, mention at intake that you'll review before finishing (recommended), so it isn't a surprise at the end. The pass has two parts: an always-on deterministic **preflight**, then the **visual pass**.

## Preflight — always, even when the visual pass is skipped

A cheap, deterministic sweep that runs **every time** (including in `--research fast` and even if the user skips the *visual* pass — these mechanical defects aren't worth shipping). Scan the rendered output and fix in place:
- **Em dashes** — banned in asset copy (`—` and `&mdash;`); replace with a comma, colon, period, or two sentences. Generation drifts here constantly (one run shipped 87), so a literal sweep is the reliable backstop, not a re-read.
- **Broken / failed images and logos** — no `<img>` that fails to load or embed (e.g. a hotlinked Clearbit raster) and no broken-image box. Prefer the brand-kit SVG or a clean wordmark; if a logo can't be sourced cleanly, fall back to text — never ship a broken mark.
- **Links** — every external `<a>` carries `target="_blank" rel="noopener noreferrer"` (in-page `#` anchors excepted).
- **Scrollbars** — themed, never the bare default OS scrollbar on a styled surface.
- **Leaked internals / placeholders** — no tool/function names, version or stream IDs, or unfilled `[…]` brackets in the rendered output.

## Visual pass — default on (off by default only in a `--research fast` run)

The full multimodal render-and-inspect. Default-on for a normal run; if the skill ran in `--research fast`, default it off (still one word to run). Skip only if the user opted out. Run all five dimensions below, then report **one short scorecard** of specific, located findings (e.g. `slide 2: bottom card row clipped`), fix what you can, and **re-verify** (re-render and re-check the dimensions you changed). Don't claim a clean pass without actually rendering and looking.

---

## How to run it

1. **Render the actual output**, don't review the spec/source. Screenshot it:
   - Docs (one-pager, proposal, brief, microsite, battlecard): full-page PNG via `../get-brand-components/scripts/render.py --file <out.html> --out <png> --width <docwidth+60>`. The script captures with reduced motion so scroll-triggered reveals (elements held at `opacity:0` until an IntersectionObserver fires) don't screenshot as blank below-the-fold content — if you capture another way, emulate `prefers-reduced-motion: reduce` or force the animated elements visible first, and treat "everything below the fold is missing" as a capture artifact to rule out before calling it a content defect.
   - Decks: the fixed 1920×1080 stage means each slide must fit its own canvas. **Measure every slide's content height** (load the deck, set slides to `position:static;height:auto`, read each `.inner` `scrollHeight`); anything `> 1080` is clipped at runtime by `overflow:hidden`. Then screenshot a stacked-verify (all slides `position:static`, natural height) to eyeball them. Reveal animations start at `opacity:0`, so drive the headless capture with a virtual-time budget (e.g. Chrome `--virtual-time-budget=2500`) or the screenshot catches a half-faded slide and reads as a false "missing content" defect.
   - **Shareable decks:** if the deck will be delivered as a link (GCS, email, etc.), embed fonts and images as base64 data URIs so the single HTML renders with no `assets/` folder beside it. Verify by rendering a copy from a directory that has no `assets/`.
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
- **Logos & brand marks (look at every logo in the render — these fail silently in source):**
  - **The mark is the real mark.** A logo drawn from an inline SVG path can be silently corrupted: if a generated/edited path has coordinates outside its `viewBox`, it renders as garbled scribbles, not the logo. Never retype a brand's SVG path. Copy it verbatim from a known-good source (or `cp` a shell that already contains it), and confirm in the render that each logo reads as the actual mark. A fast guard is to grep the output for a fingerprint substring of the correct path.
  - **Resolution.** No low-res raster logo stretched to fill a tile. A 32px favicon blown up to a 150px tile reads as garbage. Prefer a vector (SVG) brand mark (e.g. the company's brand SVG or a simple-icons mark in the brand color); a genuinely high-res PNG is acceptable; a favicon is not.
  - **No broken image / wrong fallback.** A logo that fails to load or embed shows a broken-image icon. If a real logo cannot be sourced cleanly, fall back to the company name set as clean text, never ship a broken `<img>`, an empty tile, or a wrong-brand-color text block.
- **Known deck render traps (verify each):**
  - **Background specificity.** `viewport-base.css` sets `.slide{background:var(--slide-bg)}` and is pasted AFTER the preset CSS, so at equal specificity it overrides a slide's themed background. Theme slide backgrounds with a higher-specificity selector (`.slide.gradient`, `.slide.dark`), or gradient/dark bands silently render as flat `--slide-bg`.
  - **Equal-height card rows.** In a grid card row the tallest card sets the row height; shorter siblings get a dead band of bottom padding. Balance the copy to similar length, or vertically center the card content.
  - **Stat numbers with arrows/symbols.** Put spaces around arrows (`6mo → 3wk`, not `6mo→3wk`), set `white-space:nowrap`, and size the number for its column so it does not wrap or cramp. A lone symbol (e.g. a bare `↓`) reads as a glyph, not a metric; give it a worded value or move it to a callout line.
  - **Brandmark vs eyebrow.** A top-left logo collides with a top-left eyebrow on content slides. Put the brandmark top-right when slide content is left-aligned.

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

### 4. Groundedness & verification
The single highest-stakes dimension for any asset that names a real person, company, or number — and the one a confident model fails silently. Treat an invented "fact" as a hard defect, not a stylistic nit.
- Every metric, quote, customer name, and capability traces to **real source material** (the Octave MCP data gathered for this asset, or the kit's real assets). Flag anything invented.
- **People and identities must be verified, not assumed.** Any named person, title, or "who you'll meet" traces to a real Octave/enrichment result (`resolve_profile_from_email`, `enrich_person`, `find_person`). Confirm the person exists, link their real profile, and get the title right. A fabricated contact — a hallucinated seller, a guessed buyer, a wrong title — is the most damaging defect an asset can ship. If a person can't be confirmed, the asset must flag them as unverified, not state them as fact.
- **News, events, and "recently…" claims carry a date and a source link** (`deep_web_research`, `scrape_website`). No undated, unsourced recency claims.
- **Cited library entities link back to their source — internal assets only.** In an *internal/seller-facing* asset (meeting-prep, brief, battlecard, deal coaching), a cited proof point, reference, persona, competitor, objection, use case, or Motion ICP cell should link to `https://app.octavehq.com/entity/{oId}` so the reader can verify. In a *customer-facing* asset (deck, one-pager, microsite, proposal) this is a **defect** — flag any `app.octavehq.com` link as internal-tooling leakage that must be removed.
- No hallucinated proof points, fake logos, paraphrases passed off as verbatim quotes, or capabilities not in the product data.
- **Imagery is earned** (see the get-brand-components skill → "Imagery is earned, not defaulted"): screenshots truthfully illustrate their section; no logo-soup filler; no placeholder tiles posing as content.

### 5. Slop (write like a human)
Scan the asset's copy against the ruleset below. Flag specific offending phrases and **rewrite them before delivery.** The only exemption is a format token the renderer literally requires (e.g. the `**emphasis**` spans the schema parses). Everything a reader sees as words is prose and must pass, **including deck headlines, captions, and pills.** Two misses get waved through constantly and must instead be fixed, never justified as "headline style":

- **Em dashes are banned in all asset copy, headlines included** (`&mdash;` and the literal `—`). Replace with a comma, colon, period, or two sentences. Hyphenated compounds (`go-to-market`) and arrows (`6mo → 3wk`) are fine.
- **At most ONE negative-contrast construction in the whole asset.** "It's not X, it's Y", "this isn't about X, it's Y", "The X wasn't the hard part. The Y was." Keep the single strongest one (usually the title hook) and state every other point positively. A second one is a finding to rewrite.

A clean pass here means the offenders were actually rewritten, not listed with a reason to keep them.

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
4. Groundedness ... <PASS | findings: "10x faster" metric not in source data — cut or source it; "Jordan Lee, VP Eng" unverified — confirm or flag>
5. Slop ........... <PASS | findings: "seamless", "leverage", one "it's not X it's Y" — rewrites below>

Fixing: <what you'll change>  →  re-verify.
```

Keep it tight. Specific findings beat a generic "looks good."
