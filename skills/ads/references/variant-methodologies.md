# Variant Methodologies

The eight ad variant types, each with the source card that drives it, the methodology for deriving creative from that card, and the skip condition that prevents weak variants from diluting the campaign. Every variant MUST be derived from its corresponding source card (Step 2F / 2E) — the card is the creative brief.

1. **Pain-focused** — Lead with the prospect's pain, ideally in their own words.
   - **Source Card**: Pain Language Audit (Step 2F). Use the "emotional core" and "specific dysfunction named" fields to set the angle. Use the "headline derivation" field as the starting point.
   - **Methodology**: The Pain Language Audit ranked raw prospect language by vividness. Start from the top — the most visceral quote or phrasing. Adapt for character limits but preserve the emotional core identified in the card. The data tier (FIELD vs. LIBRARY vs. INFERRED) determines your confidence level and attribution.
   - **Skip condition**: If the Pain Language Audit couldn't identify a specific dysfunction (only vague "things are hard"), skip and double up on another variant.

2. **Outcome-focused** — Lead with the transformation / result.
   - **Source Card**: Proof Chain Card (Step 2F). Use the "best available claim for this persona" field. Respect the confidence tier — don't make Named claims from Anonymized data.
   - **Methodology**: The Proof Chain Card already mapped claims → sources → confidence tiers. Pick the claim with the best combination of metric impressiveness AND persona relevance. The headline IS the number. The description provides the context the Proof Chain Card says is needed to interpret it.
   - **Skip condition**: If the Proof Chain Card found no proof points matching this persona/segment with confidence tier above Aggregate, skip and note why.

3. **Social proof** — Lead with evidence that others like them succeeded.
   - **Source Card**: Social Proof Hierarchy (Step 2F). Use the "best proof for this persona" field and respect the tier ranking.
   - **Methodology**: The Social Proof Hierarchy already ranked proof assets by strength and segment relevance. Use the highest-tier proof that actually matches this persona's segment. If there's a segment mismatch (the card flags this), acknowledge it in attribution. Best: named customer + metric. Good: anonymized + metric. Acceptable: aggregate.
   - **Skip condition**: If the Social Proof Hierarchy found no Tier 1 or Tier 2 proof for this persona, skip. Tier 3 (aggregate) rarely justifies a standalone variant.

4. **Competitive (narrative gap)** — Exploit the specific gap between what a competitor promises and what prospects actually experience.
   - **Source Card**: Narrative Gap Card (Step 2E — already built). The card's "exploit angle" and "sample displacement headline" are the starting points.
   - **Methodology**: NEVER write generic "we're better" copy. The headline should name the gap identified in the card: if they promise orchestration but prospects experience context-blindness, write "Your Workflows Are Smart. Your Context Isn't." The ad should feel like it was written by someone who's heard the prospect's frustration firsthand — because it was (or because the card honestly notes it wasn't).
   - **Skip condition**: If no Narrative Gap Card exists for a competitor relevant to this persona, skip.

5. **Question-based** — Ask a question that surfaces the pain point and makes the reader self-identify.
   - **Source Card**: Self-Selection Matrix (Step 2F). Use the question with the highest specificity score. The card's "why it works" field explains the self-selection mechanism.
   - **Methodology**: The Self-Selection Matrix already scored candidate questions by specificity. Pick the highest-scoring question. The card shows exactly who says YES (your target) and who says NO (everyone else). If the winning question scores below 7/10, consider combining elements from multiple candidates to sharpen it.
   - **Skip condition**: If no question in the Self-Selection Matrix scores above 6/10, skip. A weak question wastes the headline slot.

6. **Data-driven** — Lead with a specific stat, metric, or proof point that stops the scroll.
   - **Source Card**: Metric Defensibility Card (Step 2F). Use the number only if the card's "should we use it?" field says YES.
   - **Methodology**: The Metric Defensibility Card already stress-tested the most dramatic metric available. If it passed, the number IS the headline. The description provides the context the card says is needed. If the card flagged defensibility concerns, soften the claim in the description (e.g., "in one team's experience" vs. implied universal truth).
   - **Skip condition**: If the Metric Defensibility Card said NO (not defensible for this audience), skip this variant entirely. Do NOT fabricate or substitute a weaker metric — just skip.

7. **Status quo / cost of inaction** — Make the case that doing nothing is the riskiest option.
   - **Source Card**: Compounding Cost Model (Step 2F). Use the "rate of decay" and "tipping point" fields to frame the headline. Use the "key word" field (the repeating unit) to structure the copy.
   - **Methodology**: This is NOT pain-focused (which says "you have this problem"). The Compounding Cost Model quantifies what COMPOUNDS. Use the card's identified repeating unit ("every hire," "each week," "per quarter") as the structural element. The tipping point becomes the description's urgency driver.
   - **Skip condition**: If the Compounding Cost Model couldn't identify a specific thing that compounds (only vague "things get worse"), skip.

8. **Authority / thought leadership** — Position the company as seeing a truth the market hasn't recognized yet.
   - **Source Card**: Contrarian Thesis Card (Step 2F). Use the "reframe" field as the headline and the "what the market believes" field as the implicit foil.
   - **Methodology**: The Contrarian Thesis Card already identified the assumption, the counter-truth, and the reframe. The headline IS the reframe (or a compressed version of it). The description provides just enough context for the reader to feel the shift. The product is implied, not stated. The card's "why this is credible from your brand" field ensures you're not making a claim your brand can't back.
   - **Skip condition**: If the Contrarian Thesis Card couldn't find a genuine contrarian insight (the "what's actually true" is just a rephrased feature claim), skip. Fake thought leadership is worse than no thought leadership.

---

When `/octave:ads-resonance` reverse-infers variant types from legacy ads (campaigns not generated by this skill), it uses this taxonomy plus one extra tag: **brand-only** — a headline pool that is purely brand names and generic CTAs, indicating no angle was ever tested.
