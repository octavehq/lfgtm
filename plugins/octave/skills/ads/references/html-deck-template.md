# Visual Campaign Deck — HTML Template

When the user chooses **Generate visual campaign deck**, ask where they'd like the file saved (suggest `~/Desktop/` as a default). Produce a self-contained HTML file named after the campaign.

## Deck Structure

### Title Slide
- Campaign configuration summary: platform, objective, budget, voice, ad set count

### Per ICP / Ad Set Sections
Each ad set gets its own section containing:

- **Persona & segment context** — description of the target audience
- **Theme & positioning card** — primary/secondary use case, core pain, competitive angle
- **Source Cards section** — collapsible/expandable cards showing the full analytical artifact for each variant type (Pain Language Audit, Proof Chain, Self-Selection Matrix, Compounding Cost Model, Contrarian Thesis, Social Proof Hierarchy, Metric Defensibility). Each card shows the derivation chain from raw data → insight → headline. Color-coded to match their variant type. Include a "headline derivation" highlight showing the exact path from source data to final headline.
- **Ad variant grid** — cards laid out in a responsive grid, color-coded by variant type:
  - Pain = red
  - Outcome = green
  - Question = yellow
  - Status quo = orange
  - Social proof = teal
  - Authority = purple
  - Data-driven = blue
  - Competitive = pink

  Each card shows headlines as pills with character counts, descriptions with counts, and a link/reference back to its source card.
- **Permutation Preview** — a toggleable section (collapsed by default, "Show all ad permutations" button) that renders every possible headline × description combination for the ad set as simulated ad previews. Implementation:
  - For **Google Search RSAs**: Generate all valid combinations of 2-3 headlines + 1-2 descriptions from the full set across all variants in this ad set. Render each combo as a mock SERP snippet (blue headline links, green display URL, gray description text). Show character counts per line. Group by which headlines are paired — this lets the user see how Google might combine headlines from *different* variants in rotation.
  - For **Meta/LinkedIn**: Simpler — show each variant's primary text + headline as a mock feed card (image placeholder, intro text, headline, CTA button).
  - Add a **filter bar** at the top of the permutation grid: filter by variant type (pain, outcome, competitive, etc.) to see only combos that include a headline from that variant.
  - Add a **count badge** on the toggle button showing total permutations (e.g., "Show all 84 ad permutations").
  - Each permutation card should show a subtle tag indicating which variant types contributed its headlines (e.g., "Pain + CTA" or "Outcome + Competitive + CTA").
- **Source provenance table** — phrase, source, type badge
- **Audience targeting card** — job titles, keywords, negative keywords

### Campaign-Level Sections

- **Competitive narrative gap cards** — one card per competitor with their narrative, prospect quotes, the gap, exploit angle, sample headline
- **Keyword strategy table** — competition estimates and ad set mapping
- **Budget allocation** — visual allocation bars and phasing recommendations
- **Field intelligence coverage table** — which ad sets have prospect language data vs. library-only creative
- **Next steps** checklist

## Visual Design

- **Theme**: Dark (navy/charcoal backgrounds, clean typography, accent colors for variant types)
- **Animations**: Scroll-triggered fade-in
- **Navigation**: Sticky nav with section jump links
- **Layout**: Responsive grid layouts
- **Typography**: Import Inter + JetBrains Mono from Google Fonts
- **Self-contained**: No external dependencies beyond Google Fonts
