# Fidelity gate: score the output against the source

Don't ship blind. Render the output, measure what can be measured, then score it against the source on a fixed rubric, so "looks close-ish" becomes a gate. Applies to the kit's `components.html` AND to any collateral generated from the kit (one-pagers, case studies, decks).

The score must come from a fresh session that has not seen the capture (an independent judge), never from the capturing session grading its own work: self-scores run several points above what a fresh session gives the same kit. In the agent capture the judges are `brand-kit-judge` instances with `Read` only.

## 0. Pre-gate (mechanical, before any judge)

```bash
python3 <plugin-root>/skills/get-brand-components/scripts/gate_check.py <components.html> --json <review-dir>/gate.json
```

In a real browser it measures text contrast against the effective background for the hero, body, stats, cards, footer, CTA and quote; gutter alignment across bands; the gap between hero buttons; both logo variants in the reference strip; empty icon tiles; and the body measure in characters per line. Exit 0 passes, 1 fails with the failing checks named, 2 means no browser (NOT RUN). A failing check that a token or asset can fix goes back to the author; one that only the stylesheet can fix is a renderer fix for the orchestrator. Judges receive the measurements, so contrast and spacing are read from numbers, not guessed from pixels.

## 1. Render

```bash
python3 <plugin-root>/skills/get-brand-components/scripts/render.py --file <output.html> --out <review-dir>/out.png
# a source frame: python3 <plugin-root>/skills/get-brand-components/scripts/render.py --url https://<domain>/ --out <review-dir>/src.png
```

Review files live outside the kit directory (the cache walk skips dot-directories, but a PNG inside the kit is still a file nobody wants in a brand kit). Without a browser the gate is NOT RUN; say so, never fabricate a scorecard.

## 2. Score

The judge gets the homepage top frame and the full-width strips the miner wrote (`home-strip*.png`), a context file, and the rendered PNG. The context file says which devices the brand uses and lacks (emphasis, eyebrow, arrow, glow, texture), what the hero is (`heroVisual`), the pre-gate measurements, and which strip each block maps to: the hero against the top frame, stats and cards against the middle strips, CTA and footer against the last strip. Ignore cookie dialogs, chat widgets and promo toasts in the source. Judge the visual system, not the placeholder copy. Do not invent a device the context says the brand lacks, and do not dock depth for product imagery when `heroVisual` is `none` or `chips`: illustrations and product shots cannot come from tokens.

Grade each dimension 0 to 5 (5 = indistinguishable from the brand):

| # | Dimension | 5 = | Common miss (0 to 2) |
|---|---|---|---|
| 1 | Typography | real face, right weight, tracking | fallback font; bold where the brand is medium |
| 2 | Color/palette | exact hexes in the right roles | approximated or off-role colors |
| 3 | Emphasis | the brand's actual mechanism (color, weight, size, chip, gradient text), or none when the brand has none | a borrowed underline or wash the brand never uses; banning a device the site uses |
| 4 | Contrast/legibility | every line at AA on its surface (use the measured ratios) | accent text on a dark band; dark muted text on a dark band |
| 5 | Spacing and rhythm | airy; symmetric gutters; bands clear of edges | cramped; flush-to-edge band; uneven padding |
| 6 | Depth | the brand's real treatment (glow, shadow, texture, imagery), in one place | flat rectangles where the brand has depth, or glows repeated on every band |
| 7 | Edges/containers | rounded to the brand's radii, or square when the brand is square | hard full-bleed corners on a rounded brand, or the reverse |
| 8 | Logo/assets | correct lockup, right brand, right surface, both variants pixel-verified | wrong or stale asset; customer-wall logo; recolored blob; unverified onDark |

The judge writes its scorecard to the `REPORT` path it was given; nobody retypes it. Report a compact scorecard and an overall /40. For every dimension below 4 give a specific fix naming the token, asset or composition knob; mark a fix `renderer` when only the stylesheet or a spec can make it. Pass: at least 34/40 and no dimension below 3. A wrong or missing logo (dimension 8 at 0) fails regardless of total. Dimension 8 cannot score above 0 on metadata alone: both logo variants must have been rendered on their intended surfaces.

### The craft verdict

Fidelity is not enough. Every scorecard ends with `looks_good: yes | no` and up to three reasons, each naming what you saw and where. The tells to look for are in [design judgement](design-judgement.md) sections 2 and 3: a glow or texture repeated on more than one band, muddy or banded gradients, a blotch behind a small component (a quote, a table header, the footer), decoration the source does not have, cramped or uneven bands, placeholder-looking copy. A `no` from both gallery judges (or from the single gallery judge in later rounds) fails the round even above 34. Reasons that name the stylesheet or a spec become renderer fixes; reasons that name a token go to the author.

Fresh sessions do not score identically; when comparing pipeline changes use the mean of the gallery judges per round, and three judgements per kit when comparing captures.

### Second judge: the one-pager

The gallery shows the system; consumers receive collateral. Render the fixed one-pager through the kit and score it on the same rubric, as a second independent judgement:

```bash
python3 <plugin-root>/skills/get-brand-components/scripts/render_kit.py --kit-dir <kit-dir> --spec <plugin-root>/skills/get-brand-components/assets/onepager_spec.json --out <review-dir>/onepager.html
python3 <plugin-root>/skills/get-brand-components/scripts/render.py --file <review-dir>/onepager.html --out <review-dir>/onepager.png
```

Each artifact has its own pre-gate (`gate.json`, `gate-onepager.json`) and its own judge context. Report both scorecards. The gate passes on the gallery score; the one-pager score is what the kit's consumers will see, so a gap of more than a few points between the two is itself a finding (usually spacing, depth or edges in the composition rather than the tokens).

## 3. Then

- Judges per round: two (one on the gallery, one on the one-pager), at most three rounds per capture. When the single gallery judge lands between 33 and 35 a second gallery judge is added for that round and the mean counts. The decision is computed by `skills/get-brand-components/scripts/gate_decide.py` from the scorecard files and both pre-gate reports, never by hand.
- Pass requires, for the same candidate: a passing pre-gate for both artifacts (a failing or NOT RUN pre-gate never becomes `ready`), the gallery mean, the per-dimension floor, no hard fail, and the craft verdict. Then promote that exact version and mark it ready, in that order: `brand_cache.py promote <kit> --domain … --workspace … --write-checksums` followed by `brand_cache.py mark-ready <brand-cache>/<workspace>/<domain> --score <mean>/40` (a mean such as 34.5/40 is valid). Nothing is promoted before the gate, so a refresh never takes a working kit away from consumers while it is judged.
- Fail: up to three repair rounds, all at the token level. The installed plugin is read-only during a capture: a fix marked `renderer` by a judge, a stylesheet-only pre-gate failure, the author's `renderer feedback` and a `looks_good` reason that names the stylesheet are collected (deduplicated, by `gate_decide.py --feedback`) into `renderer-feedback.md` for the plugin maintainers (copied into the capture report, never printed to the terminal), and the capture never waits for or applies a stylesheet fix. The author repairs with tokens, knobs and surfaces, touching only what the scorecards name, and the judges re-score. Keep whichever version scores higher on the gallery mean; the repair is not monotonic, so the keep-better guard is mandatory. After the last round without a pass: a cache with no kit gets the best candidate as `draft` so the next run can resume it with fresh evidence; a cache that already holds a kit keeps its pointer untouched (a failed refresh never replaces a working kit) and the capture report names the candidate's path. Either way the run ends with the closing in SKILL.md: three lines and the open-or-host question.
- Nothing in this gate asks the user anything. The only question a capture may ask is whether to reuse a kit found in the asset store.
