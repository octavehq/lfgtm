# Fidelity gate: score the output against the source

Don't ship blind. Render the output and score it against a source screenshot on a fixed rubric, so "looks close-ish" becomes a measurable gate. Applies to the kit's `components.html` AND to any collateral generated from the kit (one-pagers, case studies, decks).

The score must come from a fresh session that has not seen the capture (an independent judge), never from the capturing session grading its own work: self-scores run several points above what a fresh session gives the same kit.

## 1. Render

```bash
python3 <skill-dir>/scripts/render.py --file <output.html> --out /tmp/out.png
# a source frame: python3 <skill-dir>/scripts/render.py --url https://<domain>/ --out /tmp/src.png
```

Without a browser the gate is NOT RUN; say so, never fabricate a scorecard.

## 2. Score

View the rendered PNG next to a source screenshot and grade each dimension 0 to 5 (5 = indistinguishable from the brand). Ignore cookie dialogs, chat widgets and promo toasts in the source. Judge the visual system, not the placeholder copy.

| # | Dimension | 5 = | Common miss (0 to 2) |
|---|---|---|---|
| 1 | Typography | real face, right weight, tracking | fallback font; bold where the brand is medium |
| 2 | Color/palette | exact hexes in the right roles | approximated or off-role colors |
| 3 | Emphasis | the brand's actual mechanism (color, weight, size, chip, gradient text) | a borrowed underline or wash the brand never uses; banning a device the site uses |
| 4 | Contrast/legibility | every line at AA on its surface | accent text on a dark band; dark muted text on a dark band |
| 5 | Spacing and rhythm | airy; symmetric gutters; bands clear of edges | cramped; flush-to-edge band; uneven padding |
| 6 | Depth | the brand's real treatment (glow, shadow, texture, imagery) | flat rectangles, or invented glows |
| 7 | Edges/containers | rounded to the brand's radii, or square when the brand is square | hard full-bleed corners on a rounded brand, or the reverse |
| 8 | Logo/assets | correct lockup, right brand, right surface, both variants pixel-verified | wrong or stale asset; customer-wall logo; recolored blob; unverified onDark |

Report a compact scorecard and an overall /40. For every dimension below 4 give a specific fix. Pass: at least 34/40 and no dimension below 3. A wrong or missing logo (dimension 8 at 0) fails regardless of total. Dimension 8 cannot score above 0 on metadata alone: both logo variants must have been rendered on their intended surfaces.

Judge spread between fresh sessions is 0 to 2 points; when comparing pipeline changes use the mean of three judgements per kit.

## 3. Then

- Interactive runs: present the scorecard and ask how to proceed (auto-fix loop up to 3 iterations, pick specific fixes, or ship as-is). Honor a standing preference for the session.
- Headless runs: one repair pass with the scorecard as input, then re-render and re-judge, and ship whichever of the two kits judged better. The repair is not monotonic (it regresses some kits), so the keep-better guard is mandatory.
