# Design judgement for a brand kit

Fidelity gets a kit to "recognisably this brand". This reference is about the second question every capture must answer: does it look good? The analyst, the author and the judge all read it. The source brand is the brief, and the brief's own words always win: a treatment the site uses is reproduced exactly, a treatment it lacks is never added, and the gallery's own defaults must not be the generic ones.

## 1. Evidence decides every device

For each device below the analyst reports **yes or no with a source** (a computed style, a stylesheet rule, a screenshot). The author turns every "no" into the matching renderer knob or token, and the judge treats any device without that evidence as a tell. "The site is dark, so a glow would look nice" is not evidence.

## 2. The generic-defaults list

These are the traits generated pages cluster around. All are legitimate for some brands; none is a choice unless the source made it.

| Device | Where it shows in a kit | Evidence that allows it |
|---|---|---|
| A single accented word in a headline (color, italic, weight) | `emph-*` tokens, `gallery.emphasis` | `computed.<home>.emphasis` lists styled words inside display text |
| Tracked-out all-caps eyebrow above every heading | `gallery.eyebrow`, `label-transform`, `tracking-label` | an eyebrow or overline element in the hero or section headers |
| Kickers and labels that add no information | `kicker` in sections | section headers on the site open with a label |
| `→` appended to buttons and links | `gallery.arrow` / `render.buttonArrow` | the primary CTA on the site carries an arrow glyph or icon |
| Identical rounded cards, one radius everywhere, the same soft grey shadow | `radius-*`, `shadow-*`, `cardStyle` | cards on the site share that radius and shadow |
| Gradient washes and glows as decoration | `glow`, `texture`, `*-glow` surface tokens | the hero or a band on the site paints a gradient or glow |
| Meta strings joined with middle dots, labels built as "WORD — fragment" | copy in `brand-kit.md` examples | the site writes its labels that way |
| Numbered markers (01 / 02 / 03) on content that is not a sequence | feature or step blocks | the site numbers a real sequence |
| Tinted near-black (#0B0B0B, #111) standing in for black | `ink`, `band` | the measured value on the site |
| Monospace for small data labels | `font-label` | the site sets labels in a monospace face |
| One of the known palettes: cream with a terracotta accent, near-black with one acid accent, broadsheet hairlines with zero radius | the whole palette | the site's own palette |

Where the source uses one of these, the kit shows it and `brand-kit.md` says so in one line. Where it does not, the gallery must not.

## 3. Spend boldness in one place

The hero carries the memorable treatment. Every other band stays quiet: solid fills, the brand's radii, no repeated glow. A glow or texture painted on more than one band, a blotch behind a small component (a quote, a table header, the footer), or a muddy gradient is the first thing a judge marks down. Before returning, the author looks at the render once and removes one decoration the source does not justify.

## 4. Type and measure

Headings at the brand's real sizes and weights (a medium display face set bold is the commonest miss). Body measure under 80 characters a line; a serif body may run slightly longer and needs a little more line-height. One or two families; when two, clearly distinct. Type is part of the design, not a neutral vehicle: the heading face at the hero's size is the second most recognisable thing after the logo.

## 5. Copy is design content

The gallery and one-pager copy reads as a plain product page, not as a description of itself. Sentence case; a headline that says what the product does; cards with one concrete benefit each; a CTA that names the action ("Book a demo", not "Primary action"); a quote that sounds like a customer. Brand-agnostic, never meta. The judge ignores copy when scoring the visual system but marks "placeholder-looking" copy as a tell, because it makes the system itself read as templated.

## 6. The quality floor, without announcing it

AA contrast on every surface (the pre-gate measures it), a visible focus ring, no motion in the kit, symmetric gutters, bands clear of the page edges unless the brand runs full-bleed, and a palette that is harmonious on its own.

## 7. The craft verdict

Every judge scorecard ends with:

```
looks_good: yes | no
reasons: up to three lines, each naming what you saw and where (a band, a component, a surface)
```

A "no" from both gallery judges (or from the single gallery judge in later rounds) fails the round even above the numeric pass mark. Reasons that name the stylesheet or a spec become renderer items for the orchestrator; reasons that name a token go to the author. The author views both PNGs after rendering and reports what it sees as an advisory `author view` (it is not a verdict; the judges decide), and fixes what it can at the kit level before returning.
