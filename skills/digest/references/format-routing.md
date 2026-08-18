# Digest format routing

Route the approved digest brief into the appropriate renderer.

## Executive brief

Create a reading-first HTML document using the shared HTML-document principles. Use a strong executive summary, 3 to 6 analytical sections, evidence notes, recommendations, and source links.

## Editorial swipe magazine

This is a digest-native format. Do not invoke `/octave:deck` or reuse its slide DOM, fixed-stage scaffold, or slide templates.

**The magazine format spec is shared:** follow [`shared/formats/magazine.md`](../../shared/formats/magazine.md) in full — structure, art direction contract, detailed mode, motion, and the responsive review gate — and paste [`shared/formats/magazine-base.css`](../../shared/formats/magazine-base.css) verbatim into the `<style>` block. Digest-specific rules that stay here:

- Evidence must pass the worthiness gate in [evidence-and-links.md](evidence-and-links.md) before it earns a place in a spread.
- `detailed` content density maps to the spec's "Detailed magazine mode."
- For internal magazines, offer the [source appendix](#source-appendix) after the recommendations and before the closing.

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
