# Digest format routing

Route the approved digest brief into the appropriate renderer.

## Executive brief

Create a reading-first HTML document using the shared HTML-document principles. Use a strong executive summary, 3 to 6 analytical sections, evidence notes, recommendations, and source links.

## Editorial swipe magazine

This is a digest-native format. Do not invoke `/octave:deck` or reuse its slide DOM, fixed-stage scaffold, or slide templates.

Create a single horizontal-swipe HTML file:

- Each spread is `100vw × 100vh`
- Horizontal scroll snap, no vertical page scrolling
- Full-bleed, edge-to-edge editorial compositions
- Narrative-driven spread count
- Start with a cover showing the reporting window. Omit the timezone for ordinary day- or week-based windows; show it only when an exact timestamp boundary materially affects scope.
- For multi-report digests, follow the cover with a contents spread naming the included reports or insight threads
- Cover and back cover may be sparse; analytical spreads should pair a dominant claim with inspectable evidence
- Give every spread its own explicit background. Because spreads alternate between light and dark surfaces, a spread that inherits the page or `body` background instead of declaring its own will paint dark text on a dark field (or the reverse) and its content disappears. Set the surface and the foreground color together on each spread.
- Add bottom navigation, ArrowLeft/ArrowRight, Home/End, touch swipe, reduced motion, and one-spread-per-page print styles. The navigation chrome is fixed over spreads of both polarities, so it must stay legible on light and dark surfaces alike: do not use white-on-transparent controls that vanish on a white spread. Use control and active-state colors that hold contrast against every surface in the magazine.
- Do not use experimental canvas or shader effects

### Art direction contract

Treat the brand kit as source material for an editorial system, not as a logo-and-color skin. Reuse its actual typefaces, palette, marks, image treatment, and signature moves.

- **Set the digest in the brand kit's own typefaces, and actually load them.** Resolve the workspace brand kit first and read its real fonts from its `tokens.css` / manifest, then set the digest in those faces. Defaulting to a generic editorial pairing when a brand kit exists is the failure to avoid: the output must look like the brand, not a stock magazine template. Naming a font in `font-family` does not load it either, so the brand faces have to actually be delivered: because a digest is usually hosted or shared, **self-contain them** with `@font-face` and base64 `src` rather than a remote `@import`/CDN `<link>` that can be blocked in the hosted context. Only when no brand kit exists, choose a deliberate editorial pairing and load it the same way. A generic-instead-of-brand typeface, or a declared-but-unloaded one that falls back to a system font, is a defect, not a style choice.
- Give every spread a deliberate composition. Use split color fields, asymmetric columns, viewport-filling grids, 2×2 quadrants, oversized typography, edge-bound rules, full-bleed imagery, and annotated diagrams.
- Do not place a centered stack of padded cards on a decorative background. When cards are semantically necessary, integrate them into a full-width grid or editorial evidence table.
- Make important verified statistics visual anchors. On desktop, the primary statistic should usually render at least 100px tall; use responsive constraints so it still fits shorter viewports.
- Label every oversized numeral by meaning. Structural numbers must visibly say `REPORT`, `SECTION`, `ISSUE`, or `PAGE` in the same composition; never let a chapter number resemble an evidence count or performance metric.
- Label every evidence count with a reader-understandable unit such as calls, companies, deals, or buyer quotes. State the period and scope nearby, and disclose overlap when one source can support multiple categories. Do not use internal labels such as “receipt set.”
- When defensible totals are available, include a compact sample-size line on the title or opening spread: calls, companies, evidence excerpts, and completed reports. Keep the reporting window separately visible.
- Use high contrast rhythm. Make the cover and closing dark, add at least one dark interior spread, and use dark or saturated fields for roughly one-third of a longer magazine.
- Change the dominant surface, composition, or color field between consecutive spreads. Avoid a sequence of white pages with interchangeable content blocks.
- Give analytical spreads at least two information layers, such as claim plus evidence, prose plus data, comparison plus annotation, or quote plus source context.
- Treat evidence as editorial material, not filler. Use only items that pass the evidence-worthiness gate in [evidence-and-links.md](evidence-and-links.md), and design their source context into the composition.
- Use the full viewport. Intentional negative space should focus attention; it must not make evidence spreads feel unfinished or underfilled.
- Favor a few bold, brand-specific moves over many generic effects. Decoration must improve hierarchy, comprehension, or pacing.

The magazine is not a reskinned deck:

- Write magazine-specific markup and layouts instead of reusing slide DOM
- Use editorial pacing: opener, contents, section openers, reported features, evidence sidebars, pull quotes, annotated comparisons, and a closing
- Allow more prose and evidence than the deck while keeping each spread legible without vertical scrolling
- Use side-by-side compositions where one field carries the main argument and the other carries evidence, context, or source notes
- Preserve meaningful negative space, but do not leave analytical spreads underfilled
- Vary density intentionally: sparse cover and section openers, medium-density reported features, and dense but legible evidence or comparison spreads
- Vary the prose cadence. Do not open every chapter with the same device (a before/after "last period, this period" turn) or lean on the same rhythm section after section (anaphora, rule-of-three, two-beat reversals). A uniform punchy cadence reads as machine-written even when the vocabulary is clean and the facts are real; a strong editor breaks the pattern deliberately.
- Titles carry the finding. Every chapter, section, and spread title is held to the editorial standard: an intelligible sentence that states the actual finding, or, if a short label, one that is clearly decipherable on its own. A vague evocative fragment that could headline any report ("The Pressure," "The Wall") does not pass. Put the claim in the title itself, not only in a subhead beneath it.
- Frame findings for a reader who was not there. Write like a dispatch that sets the scene before making its point, not like an inside note between people who shared the week. An elliptical, knowing line that is true but assumes context ("buyers stopped asking why," "the conversation moved") forces the reader to reconstruct the meaning; state plainly what happened and why it matters, then add the turn. Favor the sentence a smart colleague who missed the period would understand on first read.

### Detailed magazine mode

When content density is `detailed`:

- Give each selected report enough room to preserve its section-level reasoning; add spreads based on narrative need
- Use reported features with a claim, 2 to 4 short paragraphs, and a separate evidence or context field
- Keep body copy comfortably readable, generally 18 to 24px on a 1080px-tall desktop viewport
- Split long sections across spreads by idea; never reduce body type to fit
- Carry concrete examples and caveats forward when they change the interpretation
- Remove repeated setup across reports and use cross-references to connect overlapping themes
- Retain cover, contents, section openers, evidence treatments, synthesis, and closing so the result still reads like a magazine

### Motion

- Use native scroll snap for direct manipulation and interruptibility
- For programmatic page changes, target roughly 280 to 360ms with `cubic-bezier(0.2, 0, 0, 1)`; avoid slow cinematic transitions
- Stagger optional content entrances by about 80 to 100ms and keep them under 400ms
- Respect `prefers-reduced-motion` by removing smooth scrolling and entrance motion
- Controls need at least a 40×40px hit area

### Responsive review gate

Before delivery, inspect the cover, contents, densest editorial spread, and closing at:

- 16:9 desktop
- 16:10 desktop
- Ultrawide, at least 21:9
- A narrower tablet or mobile landscape viewport

Use width-and-height-constrained type sizing such as `min(vw, vh)` or container queries. Pure `vw` display type is not acceptable because it can collide vertically on ultrawide screens. Check for overlap, clipping, unreadably small type, and unexpected vertical scrolling at every viewport.

Also inspect every composition where a light panel is nested inside a dark or saturated spread, and every dark panel nested inside a light spread. Container background changes must explicitly reset the foreground color instead of inheriting it from the parent spread.

Confirm that every spread renders on its own surface and that the fixed navigation chrome is visible on all of them. Step to each spread and check that its background is the intended light or dark field, not the page default showing through, and that no heading, body copy, or evidence text has dropped out against it. Then confirm the navigation controls and page indicators are visible on both the lightest and the darkest spread; controls that only show up over dark spreads are a defect.

Run a computed-style contrast check on rendered text elements before delivery:

- Resolve each text element's effective foreground color and the painted background of its nearest opaque ancestor
- Flag white or near-white text on white or near-white surfaces, and dark text on dark surfaces
- Treat text that becomes readable only when selected or highlighted as a hard failure
- Re-render and visually confirm every flagged spread after fixing it

Confirm every title states its finding:

- Read each chapter, section, and spread title on its own. It must convey the actual finding as an intelligible sentence, or be a short label that is decipherable without the body beneath it.
- A vague evocative fragment that could sit on any report is a failure. Rewrite it to carry the claim, then re-render.

Confirm the copy frames its findings:

- Read the cover lede and each opening paragraph as a reader who was not on the calls. If a line is true but only decipherable to someone who shared the week's context, it fails. Rewrite it to set the scene and state the point plainly, then keep any clever turn as a follow-on rather than the lead.

Confirm the intended typefaces actually rendered:

- In the rendered screenshot, check that the display and body faces are the ones the composition specifies, not a system fallback. A serif that paints as Georgia or a sans that paints as the default UI font means the font never loaded.
- Verify computationally where possible: the resolved `font-family` on a heading and on body text should be a loaded face, and `document.fonts` should report it ready. A declared-but-unloaded font is a hard failure. Fix the load or embed, then re-render and confirm the correct face paints.

## Presentation deck

Hand off to `/octave:deck` with the approved narrative, evidence packet, audience, reporting window, source timezone, and brand kit. The source timezone controls evidence selection but should not be displayed unless an exact timestamp boundary materially affects scope. Do not repeat its intake. Use a fixed 1920×1080 stage and its mandatory review loop. For multi-report digests, require a dated title slide followed by an agenda that names the included reports or insight threads.

For `detailed` density, select the deck skill's reading-first mode. Preserve report reasoning by splitting each major section into its own slide or tightly related two-section comparison. Do not paste paragraphs into a speaker-led layout or shrink body copy below the deck's readable limits.

## Source appendix

For internal deck and magazine output, offer a compact appendix after the recommendations and before the closing:

- Name and link every included Octave report
- Show the reporting window. Show a timezone only when an exact timestamp boundary materially affects scope.
- State the selected evidence depth and any privacy limitation
- Include a copyable **Chat with this insight** prompt

The prompt should direct the reader to use the Octave MCP and fetch the named reports by stable identifier when available. Give it a specific analytical starting point, but make clear the reader can replace that question. Keep the appendix visually secondary to the narrative; it should not become a dense evidence dump.

## Interactive microsite

Hand off to `/octave:microsite`. Favor a scannable landing-page narrative, anchored navigation, interactive evidence details, and a clear final action. Do not turn it into a dashboard unless the content requires data exploration.

## One-page summary

Hand off to `/octave:one-pager`. Compress to the conclusion, 3 to 5 key findings, the most credible evidence, and specific recommendations.

## Markdown digest

Produce portable Markdown with:

- Title and reporting window
- Executive summary
- Findings ordered by impact
- Evidence and source links
- Recommendations
- Method and privacy note when evidence was hydrated

## Multiple formats

Approve one content brief first. Render the densest reading format before adapting to lower-density presentation formats, so evidence is not lost during synthesis.

When producing an Executive and Detailed pair:

- Build the Detailed narrative first from the shared report and evidence packet
- Derive the Executive narrative by compression, not by running a separate synthesis
- Preserve the same report inventory, reporting window, source links, and central recommendation
- Let page or slide counts differ; visual parity does not require structural parity
- Use the same appendix source inventory in both variants, with shorter methodology copy in the Executive version
