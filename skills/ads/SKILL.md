---
name: octave:ads
description: Build ad campaign plans grounded in your Octave library, OR run the resonance loop to analyze ad performance and feed learnings back into the library. Generates ad sets with platform-ready creative, audience targeting, negative keywords, and landing page recommendations. Resonance loop pulls performance from MCP / BigQuery / direct API / manual paste, generates falsifiable prediction cards, and accumulates a calibration track record over time. Use when user says "build an ad campaign", "create ads", "ad campaign for", "generate ad sets", "analyze ad performance", "resonance loop", "/octave:ads loop", or asks for paid advertising creative or analysis.
argument-hint: "[describe the campaign target and angle | 'resonance' to run the loop | 'resonance --min-impressions N --min-clicks N --min-conversions N --mode <smoke-test|ad-group|ad|full-resonance>' to override default volume thresholds]"
---

# Octave Ads — Campaign Generation & Resonance Loop

This skill has two modes:

1. **Campaign generation** (default): Build platform-ready ad campaign plans grounded in your Octave library intelligence. Steps 0–5.
2. **Resonance loop**: Pull ad performance data, map winners back to source cards, generate library updates and a sales intelligence brief, and write falsifiable prediction cards for the next iteration. Step 6.

## Routing — read this first

Before doing anything else, scan the user's argument string and route to the correct mode:

- **If the argument contains any of: `resonance`, `resonance loop`, `loop`, `analyze performance`, `analyse performance`, `performance analysis`, `score`, `score predictions`, `evaluate`** → skip directly to **Step 6A**. Do not run Steps 0–5. Do not ask any campaign-configuration questions. The user wants to analyze existing data, not build a new campaign.
- **Otherwise** → run Steps 0–5 in order (campaign generation). Step 6 can still be offered as a follow-up action in Step 5.

If the user's intent is ambiguous (e.g. they ran `/octave:ads` with no arguments), ask:

```
AskUserQuestion({
  questions: [{
    question: "What would you like to do?",
    header: "Mode",
    options: [
      { label: "Build a new ad campaign", description: "Generate ad sets, creative variants, targeting, and landing page recommendations grounded in your Octave library" },
      { label: "Run the resonance loop", description: "Analyze ad performance from existing campaigns, update the library based on what's working, and generate prediction cards for the next iteration" }
    ],
    multiSelect: false
  }]
})
```

---

# Mode 1: Build Ad Campaign

Generate platform-ready ad campaign plans grounded in your Octave library intelligence. Creates one ad set per persona or ICP, with creative variants generated from real prospect language extracted from calls and emails.

**MCP Server**: This skill requires the Octave MCP server. Look for available MCP tools that match the Octave tool names (e.g., `list_all_entities`, `list_findings`, `search_knowledge_base`, `get_entity`, `list_brand_voices`). The MCP server prefix varies by workspace — it may be `{octave_mcp}__`, `mcp__octave_myworkspace__`, or another name. If multiple Octave-like MCP servers are available and you're unsure which to use, ask the user which workspace to target.

---

## Step 0: Campaign Angle & Creative Direction

**This step is critical.** Before asking platform/structure questions, establish the campaign's creative direction. The angle is the most important decision — it determines what every headline, description, and keyword should say.

### Step 0A: Parse user arguments

First, scan the user's freeform arguments for context they've already provided:

1. **Target audience** — persona type, seniority, company stage, industry (e.g., "VPs of Engineering at mid-market FinServ companies")
2. **Situation / context** — what the buyer is doing or experiencing that makes them a target RIGHT NOW (e.g., "evaluating compliance automation solutions after a failed audit")
3. **Campaign angle** — the specific framing or positioning the user wants (may be implicit in the situation)

### Step 0B: Ask how they want to develop the creative direction

Using AskUserQuestion, ask:

**"How do you want to approach the creative direction for this campaign?"**

1. **I have a specific angle** — "I know the exact framing and messaging I want. Let me describe it." → Collect their angle in detail (situation, framing, key phrases to include). This becomes the primary creative driver, and library data provides supporting evidence.

2. **Let's brainstorm together** — "I have some ideas but want to explore options." → Use the Octave library to surface 3-5 potential angles (derived from use cases, hypotheses, competitor gaps, and findings that match the target audience). Present them as options with a brief rationale for each. Let the user pick one or combine elements. Then proceed.

3. **Auto-generate from my Octave library** — "Just use what's in my library to find the best angle." → Analyze the target persona/segment, search for the highest-signal use cases and hypotheses, and select the strongest angle automatically. Present the chosen angle to the user for confirmation before generating creative.

If the user already provided a clear angle in their arguments, acknowledge it and ask: "You mentioned [angle]. Should I build the entire campaign around this, or do you want to explore other angles too?"

### How the angle shapes everything

The selected angle becomes the **primary creative driver** for the entire campaign. It shapes:

- **Headline language**: Headlines should reference the buyer's situation, not just generic product benefits. If the user says "VPs dealing with compliance gaps," headlines should speak to audit pain, not just "automation platform."
- **Keyword strategy**: Keywords should match what the target audience would actually search for given their situation (e.g., "compliance automation," "audit preparation software," "regulatory risk management").
- **Description copy**: Descriptions should address the specific angle, not default to generic positioning.
- **Use case selection**: Prioritize use cases that map to the buyer's stated situation.

### Example

User input: `generate ad campaign for VPs of Engineering at mid-market FinServ companies dealing with compliance automation gaps`

Extracted:
- **Target**: VPs of Engineering at mid-market Financial Services companies
- **Situation**: They're struggling with manual compliance processes that don't scale
- **Angle**: Your product automates the compliance workflow they're currently doing by hand — turning audit prep from weeks to hours

This angle should appear in EVERY variant — pain-focused variants should reference "your team spends weeks preparing for audits that should take hours," outcome-focused should reference "engineering teams that automated compliance prep cut audit cycles by X%," etc.

---

## Step 1: Campaign Configuration

Ask the user these questions using AskUserQuestion. Each question should be its own AskUserQuestion call — do NOT bundle unrelated questions together (e.g., platform and voice are independent choices and must be asked separately). Collect all answers before proceeding.

### Question 1: Ad Platform
Ask which platform they're building for. This determines creative constraints.

| Platform | Headlines | Max H Length | Descriptions | Max D Length | Notes |
|----------|-----------|-------------|--------------|-------------|-------|
| Google Search | Up to 15 | 30 chars | Up to 4 | 90 chars | Responsive Search Ads |
| Google Display | Up to 5 | 30 chars | Up to 5 | 90 chars | Responsive Display Ads |
| Meta (Facebook/Instagram) | 1 primary text | 125 chars | 1 headline | 40 chars | Single image/video ads |
| LinkedIn | 1 intro text | 150 chars | 1 headline | 70 chars | Sponsored Content |

### Question 2: Ad Set Structure
Ask how they want to structure their ad sets:

- **By ICP (Persona + Segment)** (Recommended) — One ad set per persona-segment intersection. Most targeted. Example: "VP Engineering at Enterprise FinServ"
- **By Persona only** — One ad set per persona. Broader reach. Example: "VP Engineering"
- **By Segment only** — One ad set per market segment. Broadest. Example: "Enterprise Financial Services"
- **Custom selection** — Let me pick specific personas/segments

### Question 3: Campaign Objective
Ask what their campaign goal is:

- **Lead Generation** — Drive sign-ups, demo requests, downloads
- **Brand Awareness** — Increase visibility with target audience
- **Competitive Displacement** — Target users of specific competitors
- **Product Launch** — Promote a new feature or product

### Question 3B: Product Launch Context (conditional — only if Product Launch selected)

If the user selected **Product Launch**, ask a follow-up question to collect launch details. This context shapes every variant's creative:

Ask (as a single AskUserQuestion with free-text, or prompt them to describe):
- **What is launching?** — New product, new feature, major update, pricing change, new integration, etc.
- **What's the key differentiator or angle?** — What makes this launch worth talking about? What problem does it solve that wasn't solved before?
- **Is there a launch date or urgency?** — Time-bounded campaigns can use urgency framing in creative.
- **Any specific messaging or taglines already decided?** — If the marketing team has approved language, we should use it rather than generating from scratch.

Store these answers and use them throughout Step 3 to ensure every variant is grounded in the specific launch, not generic product messaging. The launch context should be the PRIMARY creative driver — library data (personas, use cases, proof points) provides supporting evidence and targeting, but the launch angle leads.

### Question 4: Landing Page

Before asking, fetch the workspace domain:
```
→ {octave_mcp}__verify_connection()
```
Extract the workspace's website domain from the connection response (e.g., `acme.com`). Use this as the default landing page base URL.

Ask about landing pages:
- **Use my website ({domain})** — Use `https://{domain}` as the base landing page URL. Append relevant paths per ad set if the user provides them, or suggest paths based on use case (e.g., `https://{domain}/compliance`, `https://{domain}/demo`).
- **I have specific landing pages** — Collect URLs per ad set or one global URL
- **Suggest from my resources** — We'll search their Octave resources for relevant content
- **I'll figure it out later** — Skip landing page recommendations

### Question 5: Brand Voice & Tone
Ask about voice and tone for the creative:

- **Use my Octave brand voice** — We'll fetch your saved brand voice settings and apply them to all creative
- **Professional / authoritative** — Confident, direct, data-driven. Suits enterprise audiences.
- **Conversational / peer-to-peer** — Casual, relatable, sounds like a colleague. Suits growth-stage audiences.
- **Provocative / challenger** — Bold, contrarian, challenges the status quo. Suits competitive campaigns.
- **Custom** — I'll describe the voice I want

If they choose "Use my Octave brand voice", fetch it in Step 2:
```
→ {octave_mcp}__list_brand_voices()
→ {octave_mcp}__get_entity(oId: "{brand_voice_oId}")  // fetch full voice guidelines (tone, word choice, style rules)
```

Use the full brand voice definition — tone rules, word choice guidance, sentence style, things to avoid — to shape all creative. The brand voice sets the overall register across ALL variants, but does NOT override the variant-specific methodology (pain-focused still leads with pain, social proof still leads with proof points, etc.).

If they choose "Custom", ask them to describe it in 1-2 sentences (e.g., "Sharp, slightly irreverent, like a smart friend who works in the industry").

The selected voice/tone should be applied consistently across ALL variants in ALL ad sets. It shapes word choice, sentence structure, and emotional register — but does NOT override the variant-specific methodology (pain-focused still leads with pain, social proof still leads with proof points, etc.).

### Question 6: Budget Context (optional)
Ask if they want to share approximate monthly budget. This helps calibrate the number of ad sets and variants. Not required — skip if they prefer not to share.

---

## Step 2: Fetch Library Data

Based on the ad set structure chosen in Step 1, fetch the relevant data from Octave MCP.

### 2A: Fetch Personas and/or Segments

```
If ICP or Persona mode:
  → {octave_mcp}__list_all_entities(entityType: "persona")

If ICP or Segment mode:
  → {octave_mcp}__list_all_entities(entityType: "segment")
```

Present the list to the user and ask them to confirm which ones to build ad sets for, or select "all."

### 2B: Fetch Use Cases + Competitors

Fetch all use cases and competitors — these inform creative themes and negative targeting.

```
→ {octave_mcp}__list_all_entities(entityType: "use_case")
→ {octave_mcp}__list_all_entities(entityType: "competitor")
→ {octave_mcp}__list_all_entities(entityType: "proof_point")
→ {octave_mcp}__list_all_entities(entityType: "reference")
```

### 2C: Fetch Field Intelligence

Use `list_findings` to surface real prospect language from calls and emails. This is the highest-value data source for ad creative — it captures how buyers actually describe their problems in their own words.

For each selected persona/segment, fetch findings using natural language queries:

```
→ {octave_mcp}__list_findings(
    query: "what pain points are prospects mentioning",
    eventFilters: { personas: ["{persona_oId}"], segments: ["{segment_oId}"] },
    limit: 20
  )

→ {octave_mcp}__list_findings(
    query: "objections from prospects",
    eventFilters: { personas: ["{persona_oId}"], segments: ["{segment_oId}"] },
    limit: 20
  )

→ {octave_mcp}__list_findings(
    query: "what's getting customers excited about our product",
    eventFilters: { personas: ["{persona_oId}"], segments: ["{segment_oId}"] },
    limit: 20
  )
```

Also fetch competitive mentions from conversations:
```
→ {octave_mcp}__list_findings(
    query: "competitor mentions and comparisons",
    limit: 20
  )
```

Additionally, search the knowledge base for library-level intelligence (entity descriptions, hypotheses, playbooks):
```
→ {octave_mcp}__search_knowledge_base(
    query: "{persona name} pain points challenges objections",
    includeResources: false,
    limit: 10
  )
```

**Priority**: Findings from `list_findings` (real prospect voice) should ALWAYS be preferred over library entity descriptions when writing ad creative. Library data is the fallback when no findings exist.

### 2E: Competitive Narrative Gap Analysis

For EACH competitor entity, build a narrative gap analysis. This is the foundation for all competitive ad variants.

**Step 1 — Their public narrative**: Read the competitor entity description from the library. This captures their claimed positioning (e.g., "orchestrate any workflow with 100+ integrations").

**Step 2 — What prospects actually say about them**: Search for real mentions of this competitor in calls and emails using `list_findings`:
```
→ {octave_mcp}__list_findings(
    query: "what are prospects saying about {competitor name}",
    eventFilters: { competitors: ["{competitor_oId}"] },
    limit: 20
  )
```

Also search the knowledge base for library-level competitive intelligence:
```
→ {octave_mcp}__search_knowledge_base(
    query: "{competitor name} problems limitations frustrations switching",
    includeResources: false,
    limit: 10
  )
```

**Step 3 — Identify the gap**: Compare the competitor's public narrative (what they promise) with what your prospects actually experience (what they say in calls/emails). The gap between promise and reality is your competitive angle.

**Produce a Narrative Gap Card for each competitor:**

```markdown
### Competitor: {name}
- **Their narrative**: {what they claim — from library entity description}
- **What prospects actually say**: {direct quotes from calls/emails about this competitor}
- **The gap**: {one sentence: they promise X, prospects experience Y}
- **Your exploit angle**: {how to position against this specific gap}
- **Sample displacement headline**: {one headline that exploits the gap}
```

If no prospect language exists about a competitor, note: "No field intelligence on {competitor} yet — competitive variant uses library positioning only. Connect call integrations to surface real prospect frustrations with this competitor."

These narrative gap cards drive the competitive variant generation in Step 3.

### 2D: Fetch Resources for Landing Pages (if requested)

If the user chose "Suggest from my resources":
```
→ {octave_mcp}__search_knowledge_base(
    query: "{persona/use case} landing page case study datasheet",
    includeResources: true,
    limit: 5
  )
```

Suggest the most relevant resource URL as the landing page for each ad set.

### 2F: Build Variant Source Cards

**This step is critical.** Before generating any ad creative, build a structured analytical artifact — a **Source Card** — for every variant type you intend to generate. Source cards are the creative brief for each variant. The creative is derived FROM the card. Headlines and descriptions that can't trace back to a source card don't ship.

The Narrative Gap Card (Step 2E) already serves this purpose for the competitive variant. Now build equivalent cards for every other variant type.

For EACH ad set (persona/segment), build the following source cards using the data fetched in Steps 2A-2C. Not every card is required — skip any where the underlying data doesn't exist (e.g., skip Proof Chain if no proof points match this persona). But always produce at least: Pain Language Audit, one of Proof Chain or Compounding Cost Model, and Self-Selection Matrix.

See [source-card-templates.md](references/source-card-templates.md) for the seven source card templates (Pain Language Audit, Proof Chain, Self-Selection Matrix, Compounding Cost Model, Contrarian Thesis, Social Proof Hierarchy, Metric Defensibility).

---

**How Source Cards flow into Step 3:**

Each variant's creative generation in Step 3 now follows this process:
1. Read the source card for that variant type
2. Use the "headline derivation" field as the starting point for headline writing
3. Use the source card's data tier / confidence tier to set the right level of claim strength
4. Cite the source card in the variant's attribution

If a source card reveals that the data doesn't support a variant (e.g., Proof Chain shows no defensible metrics → skip Data-Driven; Self-Selection Matrix shows no question scores above 6/10 → skip Question-Based), skip that variant and note why. This prevents weak variants from diluting the campaign.

---

## Step 2G: Persist Source Cards to Disk

**Always do this**, immediately after building the source cards in Step 2F and before generating creative in Step 3. Persisting source cards is what makes the resonance loop's Path A (forward inference from cards → variants → performance) actually work in future runs. Without this step, the loop falls back to Path B (reverse-inference from headlines), which is much weaker.

### Where to write

Write source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`:

- **`<workspace_slug>`** is derived from the Octave workspace name returned by `{octave_mcp}__verify_connection()` (called earlier in Step 1 Question 4 for the landing page domain). Lowercase, replace spaces and special characters with hyphens, strip everything that isn't `[a-z0-9-]`. Example: workspace "Acme Marketing" → `acme-marketing`.
- **`<campaign_slug>`** is derived from the campaign's identifying details: `<persona-slug>-<segment-slug>-<YYYY-MM-DD>`. If the user has explicitly named the campaign, use that name (slugified). Example: `vp-engineering-enterprise-finserv-2026-04-08`.

If the file already exists at the target path (re-running Step 2F for the same campaign), append a `-v2`, `-v3`, etc. suffix. Never overwrite an existing source card file — the resonance loop may have already evaluated predictions tied to it.

### What to write

The file is a single JSON object. See `references/source-cards.template.json` for a starter. The schema:

```json
{
  "schema_version": "0.1",
  "campaign_metadata": {
    "workspace_slug": "...",
    "campaign_slug": "...",
    "campaign_name": "Human-readable name as the user would describe it",
    "generated_at": "ISO timestamp",
    "generated_by": "/octave:ads campaign generation",
    "platform": "Google Search | Google Display | Meta | LinkedIn",
    "objective": "Lead Generation | Brand Awareness | Competitive Displacement | Product Launch",
    "personas": ["..."],
    "segments": ["..."],
    "campaign_angle": "The angle from Step 0, in one sentence"
  },
  "source_cards": [
    {
      "variant_type": "pain-focused",
      "ad_set": "VP Engineering × Enterprise FinServ",
      "card_type": "Pain Language Audit",
      "fields": {
        "raw_prospect_language": ["...quotes..."],
        "emotional_core": "...",
        "specific_dysfunction": "...",
        "headline_derivation": "...",
        "data_tier": "FIELD | LIBRARY | INFERRED"
      }
    }
    // ... one entry per source card built in Step 2F (one per variant type per ad set)
  ],
  "headlines_by_variant": {}
}
```

The `headlines_by_variant` field starts as an empty object. **Step 3 fills it in after creative generation**, mapping each `{ad_set}/{variant_type}` key to the array of headlines that were actually generated. This is what the resonance loop's Path A matches against in BigQuery later.

### How to write

1. Compute the workspace_slug and campaign_slug.
2. Check if the directory exists: `ls ~/.octave/source_cards/<workspace_slug>/ 2>/dev/null`.
3. If not, create it: `mkdir -p ~/.octave/source_cards/<workspace_slug>/`.
4. Check for existing files matching the campaign_slug. If a file exists, increment the version suffix.
5. Write the JSON file. Use `chmod 600` since it may contain prospect quotes from real calls.
6. Tell the user explicitly: "Saved source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`. The resonance loop will use these to map performance back to derivation chains in future runs."

### Why this is unconditional

Source card persistence used to be optional in earlier versions of this skill. It is now mandatory because:
- The directory lives in `$HOME/.octave/`, which is gitignored in the lfgtm repo and isolated per user
- Files are user-owned with mode 600
- The cost of storing a few KB of JSON per campaign is negligible
- The resonance loop is dramatically more useful with Path A available

If the user explicitly objects to persistence (e.g., they don't want any local files), they can pass `--no-persist-source-cards` as an argument and Step 2G is skipped. Default is to persist.

---

## Step 3: Generate Ad Sets

**CRITICAL**: If Step 0 extracted a campaign angle from the user's arguments, that angle MUST be woven into every variant's creative. The angle is not supplementary context — it is the primary lens through which all headlines, descriptions, and keyword strategies should be written. Library data (personas, use cases, proof points) provides supporting evidence, but the user's stated angle leads.

For EACH persona/ICP/segment (based on the structure chosen), generate a complete ad set plan.

### Ad Set Template

For each ad set, produce:

```markdown
## Ad Set: {Persona Name} {— Segment Name if ICP mode}

### Theme & Positioning
- **Primary Use Case**: {top use case for this persona from library}
- **Secondary Use Case**: {second use case}
- **Core Pain Point**: {from knowledge base search}
- **Competitive Angle**: {if campaign is competitive displacement, or if competitor is frequently mentioned for this persona}

### Ad Creative Variants

Generate 4-8 ad variants per ad set. **Every variant MUST be derived from its corresponding Source Card built in Step 2F.** The source card is the creative brief — read it first, use its "headline derivation" field as the starting point, and cite it in attribution. If a source card revealed insufficient data for a variant type, skip that variant (the card already explains why).

Apply the selected brand voice/tone from Step 1 across all variants. Not every variant is required — skip any where the source card flagged insufficient data. But always include at least pain-focused, outcome-focused, and one of status quo or question-based.

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

For each variant, generate creative that respects the platform constraints from Step 1.

**Google Search example** (per variant):
```
Headline 1 (30 chars): "Stop Compliance Audit Panic"
Headline 2 (30 chars): "Automated Risk Monitoring"
Headline 3 (30 chars): "Trusted by 200+ FinServs"
Description 1 (90 chars): "Your security team shouldn't chase every new regulation. Get continuous compliance monitoring."
Description 2 (90 chars): "Join 200+ financial services firms who eliminated audit fire drills. Book a demo today."
```

**Meta example** (per variant):
```
Primary Text (125 chars): "Your security team is drowning in compliance audits. There's a better way."
Headline (40 chars): "End Compliance Fire Drills"
```

### Prospect Language Sources
For each variant, cite WHERE the language came from:
- "getting burned on audits" — extracted from call with VP Eng at Acme Corp (2 weeks ago)
- "board breathing down our necks" — extracted from email reply by CTO at FinCo

If no prospect language is available for this persona, note: "No field intelligence available yet — creative is based on library entity descriptions. Connect call/email integrations to generate prospect-voice creative."

### Audience Targeting Recommendations

**Positive targeting:**
- Job titles: {derived from persona definition — e.g., "VP Engineering", "Director of Engineering", "Head of Engineering"}
- Industries: {derived from segment — e.g., "Financial Services", "Banking", "Insurance"}
- Company size: {derived from segment — e.g., "500-5000 employees"}
- Interests/keywords: {derived from use cases + competitor names}
- Platform-specific:
  - Google Search keywords: {5-10 recommended keywords derived from use case language}
  - Meta interests: {interest categories matching persona}
  - LinkedIn: {job functions, seniority levels, company sizes}

**Negative targeting / exclusions:**
- Job titles to exclude: {personas NOT in the target set — e.g., if targeting VPs, exclude individual contributors, interns, students}
- Industries to exclude: {segments NOT in the target set}
- Negative keywords (Google): {keywords that would attract wrong audience — e.g., "free", "tutorial", "certification", "jobs", competitor product names if NOT doing competitive campaign}

### Landing Page Recommendation
- **Suggested URL**: {from resources search, or user-provided}
- **Why**: {which resource matches this persona/use case best}
- If no resource found: "No matching resource found. Consider creating a landing page focused on {primary use case} for {persona}."

### Estimated Keyword Competitiveness (Google only)
Based on the use case language and competitor landscape in your library, categorize keywords as:
- **High competition** (likely expensive): {generic industry terms, competitor names}
- **Medium competition**: {specific use case terms}
- **Low competition / long-tail** (best value): {prospect-specific language, niche terms from calls}
```

---

## Step 3B: Headline Independence Review

After generating all ad sets, perform a dedicated review pass on EVERY headline across all variants. This is a separate, explicit step — not part of initial generation.

### Process

1. **Extract all headlines** — Collect every headline from every variant across all ad sets into a flat list.

2. **Read each headline in complete isolation** — Cover up the variant context, the other headlines, and the descriptions. Ask: "If this headline appeared alone on a search results page with NO surrounding context, would a person in the target audience understand what it means and find it compelling?"

3. **Check against these failure modes:**

   | Failure Mode | Example | Fix |
   |-------------|---------|-----|
   | **Fragment / continuation** | "But Not Smarter. Until Now." — only makes sense paired with a preceding headline | Rewrite as standalone thought: "Fast AI Still Gets It Wrong" |
   | **Vague pronoun / "this"** | "Learn How We Fix This" — "This" refers to nothing in isolation | Replace with specific noun: "See How We Solve Manual Audit Prep" |
   | **Insider jargon in headline** | "Your Compliance Drift Is Growing" — "Compliance Drift" is your team's internal term, not buyer language | Use buyer's words: "Your Audit Prep Is Falling Behind" |
   | **Over character limit** | "Can Your Team Sell Without You?" (31 chars) — exceeds 30 char Google limit | Shorten: "Can Reps Sell Without You?" (26 chars) |
   | **Too generic** | "Better Marketing With AI" — could be any company | Add specificity: "AI That Knows Your Buyers" |

4. **CTA headlines are exempt from the standalone-meaning test** — Headlines like "Book a Demo Today" or "Get a Free Assessment" are intentionally generic CTAs. They don't need to convey a proposition on their own because Google pairs them with other headlines. But verify there is exactly ONE CTA headline per variant (not zero, not all three).

5. **Rewrite any failing headlines** — Fix the headline, recount characters, and verify the replacement also stands alone. Update both the text output and the visual deck (if generated).

6. **Present the review results** — Show the user a summary of what was changed:
   ```
   ### Headline Independence Review

   Reviewed X headlines across Y variants.

   | Original | Issue | Replacement |
   |----------|-------|-------------|
   | "But Not Smarter. Until Now." | Fragment — meaningless alone | "Fast AI Still Gets It Wrong" |
   | ... | ... | ... |

   Z headlines passed. N headlines rewritten.
   ```

This review step catches errors that are invisible during generation (when you're thinking about headlines as a set) but obvious once you read each one in isolation — which is how Google will actually serve them.

---

## Step 3C: Update Persisted Source Cards With Final Headlines

After Steps 3 and 3B are complete and all final headlines are settled, **update the source card file written in Step 2G** with the actual headlines that were generated for each variant. This is what closes the loop — without this update, Path A in the resonance loop has no way to match BigQuery performance back to source cards.

1. Read the source card file at `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`.
2. Populate the `headlines_by_variant` field. The shape is `{ "<ad_set_name>": { "<variant_type>": [headline strings...], ... }, ... }`. Example:

```json
"headlines_by_variant": {
  "VP Engineering — Enterprise FinServ": {
    "pain-focused": [
      "Still Prepping Audits By Hand?",
      "Manual Audit Prep Is Killing You",
      "Audit Prep Shouldn't Take Weeks",
      "Stop Manual Compliance Work",
      "Book a Demo Today"
    ],
    "outcome-focused": ["...", "..."],
    "social-proof": ["...", "..."]
  },
  "Director Compliance × Mid-Market": { ... }
}
```

3. Also include the descriptions in a parallel `descriptions_by_variant` field with the same shape.
4. Write the updated file back. Tell the user: "Updated source cards file at `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json` with N final headlines across M variants. The resonance loop will use these to map performance back to derivation chains."

Skipping this step means the resonance loop cannot use Path A for this campaign. It will still work in Path B (reverse-inference from headlines), but without the strong forward derivation chain.

---

## Step 4: Campaign Summary

After generating all ad sets, produce a campaign summary:

```markdown
# Campaign Plan Summary

## Overview
- **Platform**: {platform}
- **Objective**: {objective}
- **Ad Sets**: {count}
- **Total Ad Variants**: {count}
- **Personas Covered**: {list}
- **Segments Covered**: {list}

## Ad Set Breakdown
| Ad Set | Persona | Segment | Primary Theme | Variants | Landing Page |
|--------|---------|---------|---------------|----------|-------------|
| 1 | VP Eng | Enterprise FinServ | Compliance Risk | 4 | /compliance |
| 2 | CTO | Mid-Market SaaS | Dev Efficiency | 3 | /engineering |
| ... | ... | ... | ... | ... | ... |

## Negative Targeting (Campaign-Level)
- **Excluded job titles**: {combined exclusions}
- **Negative keywords**: {combined negative keywords}
- **Excluded demographics**: {age groups, locations if applicable}

## Field Intelligence Coverage
- **Personas with prospect language data**: X of Y
- **Personas using library-only creative**: X of Y
- **Recommendation**: {if low coverage, suggest connecting more integrations}

## Next Steps
1. Review and refine ad creative variants
2. Set up campaign in {platform} using the targeting recommendations
3. Upload creative variants as responsive ads
4. Set budget allocation across ad sets
5. Track performance and close the loop with your Octave library intelligence
```

---

## Step 5: Offer Follow-Up Actions

Ask the user via AskUserQuestion:

1. **Refine a specific ad set** — Regenerate creative for one ad set with different angles
2. **Add a competitive campaign** — Build ad sets specifically targeting competitor users
3. **Generate more variants** — Add more creative variants to existing ad sets
4. **Export as CSV** — Format the campaign plan for bulk upload to the ad platform
5. **Generate visual campaign deck** — Create a self-contained HTML slide deck showing the full campaign with variant grids, rationale, targeting, competitive gap cards, and budget allocation. Useful for sharing with stakeholders or reviewing the campaign visually.
6. **Resonance loop** — Analyze ad performance data, map winners back to source cards, and generate library updates + sales intelligence. Pulls data from MCP, BigQuery Data Transfer, direct API, or accepts manual paste — whichever is available.
7. **Done** — Finished

If they choose export, ask which platform:

```
AskUserQuestion({
  questions: [{
    question: "Which ad platform are you exporting for?",
    header: "Platform",
    options: [
      {
        label: "Google Ads (Web UI)",
        description: "Generates separate CSV files per entity type for the Google Ads web UI bulk upload (Tools → Bulk Actions → Uploads)."
      },
      {
        label: "Google Ads (Editor)",
        description: "Single file for the Google Ads Editor desktop app. Tab-separated UTF-16, all entity types in one file. Import via Account → Import → From file."
      },
      {
        label: "Meta Ads",
        description: "Single CSV with Primary Text, Headline, Description, Link, and Call to Action columns. One row per ad variant."
      },
      {
        label: "LinkedIn Ads",
        description: "Single CSV with Intro Text, Headline, Description, Destination URL columns. One row per ad variant."
      }
    ],
    multiSelect: false
  }]
})
```

### Google Ads Export

1. **Collect Customer ID**: Ask the user for the Google Ads Customer ID of the **upload destination account** (the account number in the Google Ads header, e.g., `123-456-7890`). For the web UI bulk upload this can be either an MCC or a sub-account — whichever you'll select in the Ads UI before clicking Upload. Using an ID that doesn't match the active account in the UI causes "entity does not exist" errors. Note: this is the upload destination, not the `login-customer-id` used by the API/MCP path — the web UI handles MCC routing automatically.

2. **Read the format reference**: Read `references/google-ads-csv-format.md` for the exact column layouts, quoting rules, and validation checklist.

3. **Generate separate CSV files**: The Google Ads web UI requires one CSV per entity type, each with its own column layout. Ask the user where to save (suggest `~/Desktop/{campaign-name}/`), then generate:

```
{campaign-name}/
├── 1-campaign.csv          # Campaign settings
├── 2-ad-groups.csv         # One row per ad set / persona
├── 3-ads.csv               # RSAs with 5+ headlines, 2+ descriptions per ad group
├── 4-keywords.csv          # All keywords with match types
└── 5-negative-keywords.csv # All negative keywords with match types and level
```

4. **Critical rules**:
   - **Double-quote every field** — prevents column shifts from pipes, apostrophes, em dashes
   - **Escape internal quotes by doubling**: `Doesn't` → `"Doesn""t"`
   - **EU political ads = `No`** — campaign upload fails without this
   - **Minimum 5 distinct headlines per RSA** — Google rejects ads with fewer
   - **Match types use full words**: `Broad match`, `Phrase match`, `Exact match` — not abbreviations
   - **Negative keywords need a `Level`**: `Ad group` or `Campaign`
   - **Upload in order**: campaign first, then ad groups, then ads, then keywords, then negatives — each depends on the previous

5. **Tell the user**: "Upload these files to Google Ads → Tools → Bulk Actions → Uploads, in numbered order. Wait for each to succeed before uploading the next. All campaigns are set to Paused — nothing will run until you explicitly enable them."

### Google Ads Editor Export

1. **Read the format reference**: Read `references/google-ads-editor-format.md` for the exact column layout, entity type detection rules, and Python generation snippet.

2. **Generate a single file**: The Ads Editor uses a tab-separated UTF-16 file with 144 columns. All entity types (campaigns, ad groups, ads, keywords) go in one file. No Customer ID needed — it imports into whatever account is open.

3. **Use Python to generate**: Claude cannot write UTF-16 tab-separated files directly. Use a Bash tool call with the Python snippet from the reference doc to generate the file. Save to `~/Desktop/{campaign-name}-editor.csv`.

4. **Critical rules**:
   - **UTF-16 encoding, tab-separated** — not comma-separated
   - **No Row Type or Action columns** — entity type inferred from populated columns
   - **EU political ads** = `Doesn't have EU political ads` (not `No`)
   - **Languages** = `en` (not `English`)
   - **Minimum 5 distinct headlines per RSA**
   - **Keyword match type via syntax**: broad = bare text, phrase = `"quoted"`, exact = `[bracketed]`
   - **Rows in dependency order**: campaigns → ad groups → ads → keywords

5. **Tell the user**: "Open Google Ads Editor, sign into your account, then Account → Import → From file. All campaigns are set to Paused. Review in the Editor, then Post to push live."

### Meta Ads Export

Single CSV with columns: Primary Text, Headline, Description, Link, Call to Action. One row per ad variant. Apply platform character limits (Primary Text: 125 chars, Headline: 40 chars).

### LinkedIn Ads Export

Single CSV with columns: Intro Text, Headline, Description, Destination URL. One row per ad variant. Apply platform character limits (Intro Text: 150 chars, Headline: 70 chars).

If they choose **Generate visual campaign deck**, read `references/html-deck-template.md` for the full deck structure, section layout, variant color coding, and visual design spec. Follow that template to produce the HTML file.

---

## Step 6: Resonance Loop — Performance → Library Intelligence

This step turns ad performance data into GTM intelligence. It can be triggered as a follow-up action after the campaign has been running (add it as option 7 in Step 5), or invoked directly:

```
/octave:ads loop
/octave:ads resonance-loop
/octave:ads analyze performance
```

### 6A: Detect Performance Data Source

Performance data can come from four places, in order of preference:

1. **MCP** (live Google Ads / Meta / LinkedIn API via an installed MCP server) — real-time, but most likely to fail at runtime
2. **BigQuery Data Transfer Service** (~24h delayed managed pipeline) — the recommended default for read-only resonance analysis, no developer token approval required
3. **Direct API** (curl/Python against the Google Ads API, no MCP) — when the user has an approved developer token but no MCP installed
4. **Manual** (paste CSV / screenshot / verbal) — last resort

**Read `references/performance-data-sources.md` for setup instructions, smoke-test queries, table layouts, and the troubleshooting table.** That doc is the source of truth for everything in this section.

**Critical principle**: never tell the user "I can pull your data" without running a smoke test first. A path that *looks* available (the MCP tool exists, the dataset exists, the dev token is set) can still fail at query time. Probe first, then commit.

Walk through the four paths in order. For each one, first detect, then smoke-test. The first path that passes its smoke test wins — use it. If all four fail, fall through to manual.

#### Detection patterns

| Path | What to look for |
|------|------------------|
| 1 — MCP | MCP tools matching `google_ads`, `googleads`, `adwords`, `google_campaigns`, `meta_ads`, `facebook_ads`, `linkedin_ads` |
| 2 — BigQuery | A BigQuery MCP tool (`bigquery`, `bq`, `mcp__bigquery*`), OR the `bq` CLI on PATH and authenticated, OR a known dataset like `google_ads` containing `ads_Campaign_*` / `ads_CampaignBasicStats_*` tables |
| 3 — Direct API | The user mentions they have an approved developer token + a refresh token, but no MCP. Or earlier in the conversation they shared API credentials |
| 4 — Manual | Always available |

#### Path 1 — MCP smoke test

If a Google Ads MCP tool is detected, before promising data:

```
→ {google_ads_mcp}__list_accessible_customers()
```

If that succeeds, pick one accessible customer ID and run the simplest possible query:

```
→ {google_ads_mcp}__search(
    customer_id: "{id}",
    query: "SELECT customer.id, customer.descriptive_name FROM customer"
  )
```

**Interpret the result:**
- Success → Path 1 is good. Use it for all subsequent queries.
- `CUSTOMER_NOT_FOUND` + "missing authentication credential" → wrong `login-customer-id`. Tell the user the exact fix (set `GOOGLE_ADS_LOGIN_CUSTOMER_ID` to the MCC, not a sub-account) and fall through to Path 2.
- `DEVELOPER_TOKEN_NOT_APPROVED` "only approved for use with test accounts" → the developer token is in Test tier and cannot query production accounts. Tell the user they need to apply for Basic Access in API Center (~3 days) and fall through to Path 2.
- `invalid_scope` or 403 → ADC missing the `adwords` scope. Reference the Python refresh-token snippet in the data sources doc and fall through to Path 2.
- `404` on a versioned path → API version sunset. Note the current version (v21 as of 2026-04) and fall through to Path 2.

For all four failure modes, the message to the user should be one sentence: what failed, what the fix is, and "I'll try BigQuery next."

#### Path 2 — BigQuery smoke test

If a BigQuery MCP tool is available, list datasets and look for `google_ads` (or any dataset containing tables prefixed `ads_Campaign_`). If `bq` CLI is available, run:

```
bq ls --project_id=<project>
bq ls <project>:google_ads
```

If you find tables matching `ads_CampaignBasicStats_<MCC>`, run a **two-stage smoke test**. The first stage proves data exists and is fresh. The second stage proves the data is *meaningful* — that it'll actually drive useful resonance analysis, not just produce empty tables.

**Stage 1 — freshness probe:**

```sql
SELECT
  COUNT(*) AS row_count,
  MIN(_DATA_DATE) AS earliest,
  MAX(_DATA_DATE) AS most_recent
FROM `<project>.google_ads.ads_CampaignBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
```

**Stage 2 — meaningful-data probe** (the ad-group-level CPC/CTR query). This is the most actionable single query at small spend and immediately exposes whether the data has signal worth analyzing.

**CRITICAL — dim-table snapshot trap.** `ads_AdGroup_<MCC>` and `ads_Campaign_<MCC>` are **daily-snapshotted dimension tables**, not static dim tables. Each ad_group_id has one row per `_DATA_DATE`. Joining to them without a snapshot-dedup step cartesian-explodes your totals: after N days the multiplier is N (or N² if you join both tables). See `references/performance-data-sources.md` § "Gotcha #4: Daily-snapshotted dim tables" for the full writeup. Every query in this skill that reads dim metadata must use the `ag_latest` / `c_latest` CTE pattern shown below — never JOIN the dim tables directly.

```sql
WITH
-- Latest snapshot of the dim tables (one row per ad_group_id / campaign_id).
-- Required: ads_AdGroup_* and ads_Campaign_* are daily-snapshotted.
-- Joining them raw cartesian-explodes totals. Never skip this CTE.
ag_latest AS (
  SELECT * FROM `<project>.google_ads.ads_AdGroup_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_id ORDER BY _DATA_DATE DESC) = 1
),
c_latest AS (
  SELECT * FROM `<project>.google_ads.ads_Campaign_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY _DATA_DATE DESC) = 1
)
SELECT
  c.campaign_name,
  ag.ad_group_name,
  COUNT(DISTINCT s._DATA_DATE) AS days_active,
  SUM(s.metrics_impressions) AS impressions,
  SUM(s.metrics_clicks) AS clicks,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_clicks), SUM(s.metrics_impressions)) * 100, 2) AS ctr_pct,
  SUM(s.metrics_conversions) AS conversions,
  ROUND(SUM(s.metrics_cost_micros) / 1000000, 2) AS cost_usd,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_cost_micros) / 1000000, SUM(s.metrics_clicks)), 2) AS cpc_usd
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>` s
JOIN ag_latest ag USING (customer_id, ad_group_id, campaign_id)
JOIN c_latest c USING (customer_id, campaign_id)
WHERE s._DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING clicks > 5
ORDER BY cpc_usd DESC
```

**Stage 2b — mandatory sanity cross-check.** Immediately after running Stage 2, run this raw-stats-only query and verify the totals match:

```sql
SELECT
  ad_group_id,
  SUM(metrics_impressions) AS impressions_raw,
  SUM(metrics_clicks) AS clicks_raw
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
```

For each `ad_group_id` present in both results, `clicks_raw` and `impressions_raw` must equal the Stage 2 values **exactly**. If any row differs, **stop the loop and report a dim-join inflation bug** — do not proceed with analysis. The most likely cause is that someone modified the Stage 2 query template and dropped the `ag_latest` / `c_latest` CTE pattern. The fix is to restore the CTEs. The second most likely cause is a new dim table being introduced upstream with the same daily-snapshot shape. Either way, the mismatch is a hard stop: inflated totals will silently corrupt every downstream conclusion (CPC comparisons, prediction cards, library recommendations).

**Interpret the result:**
- Stage 1 returns rows > 0 and `most_recent` within the last 2 days → freshness OK, continue to Stage 2.
- Stage 2 returns ≥ 2 ad groups with `clicks > 5` → Path 2 is good. Use the BigQuery queries from `references/performance-data-sources.md` for all subsequent fetches. Note in your report what the data window covers and how many ad groups have meaningful volume.
- Stage 2 returns 0 or 1 rows with meaningful volume → the data is fresh but too thin for cross-ad-group comparisons. Tell the user explicitly: "I have data, but only N days / N ad groups have enough clicks to draw real conclusions. I can run the loop in **smoke test mode** (verifies the pipes work, conclusions are unreliable) or **partial mode** (only report findings I can stand behind). Which?"
- Stage 1 returns rows == 0 or `most_recent` is more than 2 days old → the transfer exists but has stalled or hasn't backfilled yet. Tell the user and offer to either trigger a backfill (`bq mk --transfer_run ...`) or fall through to Path 3 / Path 4.
- Permission denied on either query → the calling identity (user or service account) lacks `roles/bigquery.dataViewer` on the dataset. Tell the user the exact fix and fall through.
- No matching dataset/tables → Path 2 isn't set up yet. **Offer to walk the user through setup interactively** (this is the first-run path). The full setup steps are documented in `references/performance-data-sources.md` § "Path 2: BigQuery Data Transfer Service". Read that section and execute it step by step with the user — enable the APIs, create the dataset, create the transfer in the BigQuery console (this requires the user to click through the OAuth grant), trigger a backfill, then re-run the smoke test once data starts landing. Setup is ~10 minutes of clicks plus ~17 hours for the full 30-day backfill (most-recent days land first, so analysis can begin within ~30 min). Do not skip to Path 3 or Path 4 unless the user explicitly declines the setup.

#### Path 3 — Direct API smoke test

If the user has shared API credentials earlier in the conversation (developer token + refresh token + client id/secret), or has a `~/adc-google-ads.json` ADC file, you can hit the API directly with `curl` or Python. Same smoke test as Path 1: mint an access token from the refresh token, hit `listAccessibleCustomers`, then run a `customer` query against an accessible ID.

Same failure modes as Path 1 (login-customer-id, dev token tier, scope, API version) — see the data sources doc for the curl invocations.

#### Path 4 — Manual

If all programmatic paths fail (or the user explicitly requests manual), ask:

```
AskUserQuestion({
  questions: [{
    question: "How would you like to provide ad performance data?",
    header: "Performance Data",
    options: [
      {
        label: "Paste a CSV or table",
        description: "Paste performance data from your ad platform (needs: variant/headline, impressions, clicks, conversions)"
      },
      {
        label: "Paste a screenshot",
        description: "Share a screenshot of your ad platform dashboard — I'll extract the metrics"
      },
      {
        label: "Summarize verbally",
        description: "Tell me which variants won and lost, with approximate numbers"
      },
      {
        label: "Skip — I'll come back later",
        description: "Run the resonance loop when you have performance data"
      }
    ],
    multiSelect: false
  }]
})
```

#### What to fetch (any path)

Whichever path wins, fetch these per-variant metrics so the resonance map (Step 6B) has what it needs:
- Impressions
- Clicks / CTR
- Conversions / conversion rate
- Cost per click (CPC) / cost per conversion (CPA)
- Ad creative content (RSA headlines and descriptions for matching back to source cards)
- Quality Score (Google) or Relevance Score (Meta/LinkedIn) if available

Match fetched data back to the variants generated in Step 3 by **headline text** (most reliable across paths), then by ad set name, then by campaign ID if the user stored it during export.

### 6B: Map Performance Back to Source Cards

This is the core of the resonance loop. Before generating the map, decide which **analytical mode** the data supports — the wrong mode produces confident-sounding noise. Then decide whether the campaign was generated by `/octave:ads` (source cards exist) or is legacy/external (source cards must be reverse-inferred).

#### 6B.1: Pick the analytical mode based on volume

Different volumes stabilize different metrics. **Volume — not spend — is what determines statistical confidence.** $100/day on $50 CPC enterprise keywords is 2 clicks; $100/day on $0.50 CPC long-tail keywords is 200 clicks. Same dollar amount, totally different reliability. Use the volume thresholds below as the primitives. Spend amounts are listed only as rough orientation.

**Read this table and pick the most conservative mode that fits the *unit being compared*.**

| Mode | Volume threshold (the actual gate) | Rough spend orientation | What's stable | What's still noise |
|---|---|---|---|---|
| **Smoke-test** | <500 impressions OR <20 clicks total in the window across all units | < $100/day | Almost nothing | Conversions, CTR, CPC at any level |
| **Ad-group** | ≥2 ad groups each with **500+ impressions and 20+ clicks** in the window | $100–$500/day | Ad-group-level CTR and CPC | Conversion rate at any level, ad-level metrics, CPA |
| **Ad** | Per-ad: **1,000+ impressions and 30+ clicks** for the ad in question | $500–$2,000/day | Ad-level CTR (only for ads meeting the threshold) | Conversion rate, CPA, ad-level CPC for low-volume ads |
| **Full resonance** | All ad-mode thresholds met **+ 30+ total conversions** in the window | > $2,000/day | All of the above + ad-level conversion rate | Headline-level attribution (Google does not expose this) |

The gates are AND, not OR. An ad with 5,000 impressions and 4 clicks doesn't qualify for ad mode (clicks too low). An ad group with 50,000 impressions but only 10 conversions doesn't qualify for full resonance (conversions too low).

**Default thresholds can be overridden** at runtime if the user explicitly says they know their data. Accept arguments like:
- `--min-impressions 200` (lowers the per-unit impression floor)
- `--min-clicks 10`
- `--min-conversions 10`
- `--mode ad-group` / `--mode ad` / `--mode full-resonance` (force a specific mode regardless of volume)

When the user passes an override, **state in the report what was overridden and to what value**, so the user can interpret the confidence accordingly. Do not silently use looser thresholds than the data supports.

**Hard rules — apply regardless of mode:**

1. **Never claim a "winning" or "losing" variant from N < 30 conversions** unless the user has explicitly overridden `--min-conversions`. State the conversion data, but frame any conclusion as "early signal, needs more volume to validate." A single conversion is correlation, not causation.
2. **Always report the data window, total impressions/clicks/conversions, and selected mode at the top of the resonance map.** This calibrates the reader for how much weight to give the conclusions.
3. **CPC gaps between ad groups are usually the biggest finding at small spend.** A 3x+ CPC delta between two ad groups in the same account targeting the same persona is a "rework or kill" signal even with no conversion data, because it reveals a Quality Score / keyword-creative match problem that no amount of creative iteration will fix.
4. **If the smoke test (Step 6A Stage 2) returned only 1 ad group with meaningful volume, you cannot run a real resonance loop.** Report what you have, label it explicitly as "single-ad-group early signal," and offer to re-run when more data is available.
5. **Units below the threshold for the chosen mode get N/A confidence and are excluded from winners/losers tables.** They can appear in an "FYI — insufficient volume" section, but never in the actionable findings.

Pick the mode now and **state it explicitly at the top of the resonance map output** so the user knows the confidence floor before reading the findings.

#### 6B.2: Decide whether source cards exist

Two paths into Step 6B:

**Path A — Campaign was generated by `/octave:ads`** (source cards exist):

Campaigns generated by this skill automatically persist source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json` in Step 2G, with final headlines populated in Step 3C. The file contains the campaign metadata, the full source cards built in Step 2F, and a `headlines_by_variant` mapping from each variant to the actual headlines that were generated.

To use Path A in the resonance loop:
1. Scan `~/.octave/source_cards/` for subdirectories. Each subdirectory is a workspace slug.
2. Inside each, look at every campaign file. Read the `headlines_by_variant` field.
3. Match each headline string against the headlines observed in BigQuery (via the per-ad query in `references/performance-data-sources.md`). Match by exact headline text — this is reliable because Google preserves headline strings verbatim.
4. When a match is found, you can trace forward from the BigQuery row → the headline → the variant type → the source card → the derivation chain → the original prospect language or proof point. This is the strong direction of inference.

If no source card files exist (the campaigns running in BigQuery weren't generated by this skill — e.g., they were created in the Google Ads UI directly), fall through to Path B (reverse-inference).

**Path B — Legacy or externally created campaign** (no source cards):
For everything currently running in production that wasn't generated by this skill, the resonance loop has to **reverse-infer** the variant type and source card from the headlines themselves. This is a much weaker form of analysis — you're looking at the output and guessing what the brief was. Be honest about this in the report: a winning headline tells you what *worked*, but without the original brief you can only speculate about *which underlying angle made it work*.

The reverse-inference process for legacy campaigns:

1. **Cluster headlines by inferred variant type.** Read the headline pool of each ad and tag it with the closest matching variant type from Step 3 (pain-focused, outcome-focused, social-proof, competitive, question-based, data-driven, status-quo, authority, brand-only). Most legacy ads will be brand-only or generic-benefit; that's a finding in itself.
2. **Look at headline structure and pinning.** A pinned HEADLINE_1 tells you what the ad creator believed was the lead message. A pool of 15 headlines with no pinning tells you Google was given full optimization latitude. A pool of 5 brand headlines tells you the creator never tested angles at all.
3. **Trace winners backward to *speculative* source cards.** If "Still Prepping Audits By Hand?" wins, the implicit Pain Language Audit might be: emotional core = visceral frustration with manual compliance work; specific dysfunction = audit preparation as an unautomated weeks-long process; data tier = INFERRED (no underlying field finding cited). Mark these reverse-inferred cards clearly so the user knows they're hypotheses, not derivations.
4. **The library-update recommendations are weaker in Path B.** You're recommending changes to personas/playbooks based on what *appears* to resonate from external creative — not from creative whose grounding you can verify. Lower the confidence tier on every recommendation by one level (HIGH → MEDIUM, MEDIUM → LOW).
5. **Recommend that the next campaign go through `/octave:ads`** so the next loop iteration can use Path A. The strongest version of the resonance loop requires that the campaign and the analysis share a vocabulary.

#### 6B.3: Build the resonance map

For each variant with performance data (Path A) or each ad group (Path B at small spend), produce the map. The template adapts to the mode picked in 6B.1 — at small spend, there are no per-variant winners to list; the unit of comparison is ad groups.

**Standard template (ad mode or full resonance mode):**

```markdown
## Resonance Map

**Data window**: {start} – {end} ({N} days) | **Spend**: ${X} | **Total impressions**: {N} | **Total conversions**: {N}
**Mode**: {smoke-test | ad-group | ad | full resonance}
**Path**: {A — source cards exist | B — reverse-inferred from headlines}

### Winners (top performing variants)

| Variant | Type | Ad Set | CTR | Conv Rate | Source Card | Derivation Chain | Confidence |
|---------|------|--------|-----|-----------|-------------|-----------------|------------|
| "Still Prepping Audits By Hand?" | Pain-focused | VP Eng × FinServ | 3.2% | 1.8% | Pain Language Audit | Finding F-123 (call w/ Acme, 2 weeks ago) → emotional core: "fear of failed audits" → headline | HIGH |

**What this tells us**: The pain of manual audit prep resonates more strongly than the cost-of-inaction framing for VP Engineering personas. The winning language traces to a specific finding from a real sales call — this isn't just ad performance, it's market validation of a pain point.

### Underperformers (below-average variants)

| Variant | Type | Ad Set | CTR | Conv Rate | Source Card | Hypothesis for Underperformance | Confidence |
|---------|------|--------|-----|-----------|-------------|-------------------------------|------------|
| "Every Hire Starts From Zero" | Status quo | VP Eng × FinServ | 0.4% | 0.1% | Compounding Cost Model | The compounding narrative may be too abstract for search intent — buyers searching for solutions want immediate pain acknowledgment, not long-term projections | MEDIUM |
```

**Small-spend template (ad-group mode):**

When the data only supports ad-group comparisons, lead with the CPC gap finding instead of variant-level analysis:

```markdown
## Resonance Map

**Data window**: {start} – {end} ({N} days) | **Spend**: ${X} | **Total conversions**: {N}
**Mode**: ad-group (spend too low for ad-level conclusions)
**Path**: {A | B}

### Ad Group Comparison

| Ad Group | Campaign | Impr | Clicks | CTR | Conv | Cost | CPC | Confidence |
|---|---|---|---|---|---|---|---|---|
| VP Eng × Enterprise FinServ | Compliance Automation Q1 | 1,000 | 60 | 6.00% | 1 | $180 | $3.00 | HIGH |
| Director Compliance × Mid-Market | Compliance Automation Q1 | 400 | 15 | 3.75% | 0 | $225 | $15.00 | HIGH |

**Key finding**: The Director Compliance ad group costs ~5x more per click than the VP Eng ad group and converts at 0% vs ~1.5% over the window. This is a Quality Score / keyword-creative match gap, not a creative gap alone — even rewriting the ads will not close a CPC delta this large without keyword changes.

**Actionable**: Pause or rework the Director Compliance ad group. Move budget to VP Eng. Expected effect: ~5x more clicks per dollar at the same total spend.

### Per-ad observations (FYI only — too noisy to act on)

[List ads with their headlines and metrics, but explicitly do NOT rank them or label winners/losers. The ad-group finding is the actionable one.]
```

Confidence tiers for the resonance map:
- **HIGH**: 14+ days of data, 1,000+ impressions on the unit being compared, the metric in question is one the spend tier supports as stable
- **MEDIUM**: 7–14 days, 500+ impressions, OR the metric is borderline for the spend tier
- **LOW**: < 7 days, < 500 impressions, OR the metric is one the spend tier explicitly does not support
- **N/A**: Unit has < 100 impressions or < 5 clicks — Google has not given it a fair test, do not include in winners/losers tables

### 6C: Generate Library Update Recommendations

Based on the resonance map, generate specific, actionable recommendations for the Octave library:

```markdown
## Library Update Recommendations

### Persona Updates
| Persona | Field | Current | Recommended Update | Evidence |
|---------|-------|---------|-------------------|----------|
| VP Engineering | Primary pain point | "Tool sprawl across compliance stack" | "Manual audit preparation that doesn't scale" | Pain-focused variant at 3.2% CTR vs status-quo at 0.4% — manual process pain resonates 8x stronger than tool sprawl framing |

### Playbook Updates
| Playbook | Update | Evidence |
|----------|--------|----------|
| Enterprise FinServ | Add discovery opener: "How are you handling audit prep today?" | Derived from winning headline "Still Prepping Audits By Hand?" — 3.2% CTR proves this question self-selects the right buyer |

### Value Prop Updates
| Value Prop | Update | Evidence |
|------------|--------|----------|
| Compliance Automation | Reframe from "reduce risk" to "eliminate manual audit prep" | Pain-focused (manual process) outperformed authority (risk reduction) by 4x in CTR |
```

For each recommendation, ask the user whether to apply it:

```
AskUserQuestion({
  questions: [{
    question: "Apply these library updates?",
    header: "Library Updates",
    options: [
      {
        label: "Apply all",
        description: "Update personas, playbooks, and value props based on ad performance evidence"
      },
      {
        label: "Let me pick",
        description: "Review each recommendation individually"
      },
      {
        label: "Save as findings only",
        description: "Don't update the library yet — save these as findings for later review"
      },
      {
        label: "Skip",
        description: "Review only, no changes"
      }
    ],
    multiSelect: false
  }]
})
```

If they choose to apply updates, use the appropriate MCP tools:
```
→ {octave_mcp}__update_entity(oId: "{persona_oId}", instructions: "{update}")
→ {octave_mcp}__update_playbook(oId: "{playbook_oId}", instructions: "{update}")
→ {octave_mcp}__update_value_props(oId: "{playbook_oId}", instructions: "{update}")
```

### 6D: Feed Winning Language to Sales

Generate a **Sales Intelligence Brief** — a summary designed for sales teams showing what language the market is responding to:

```markdown
## Sales Intelligence Brief — From Ad Performance

### Winning Messages (use these in conversations)
| Message | Where It Won | Suggested Sales Use |
|---------|-------------|-------------------|
| "Still prepping audits by hand?" | Google Search, 3.2% CTR, VP Eng | Discovery opener — ask this in the first 2 minutes |
| "Audit prep: 3 weeks → 2 days" | Google Search, 2.8% CTR, VP Eng | Proof point framing — lead with this specific transformation |

### Messages That Didn't Land (avoid or reframe)
| Message | Where It Failed | Why | Alternative |
|---------|----------------|-----|------------|
| "Every hire starts from zero" | Google Search, 0.4% CTR | Too abstract for search intent | Reframe to concrete: "New hires spend 6 weeks learning your compliance process" |

### Persona Insight
{Persona}: The ad data confirms this buyer responds to **immediate, tangible process pain** over **strategic risk framing**. Lead with "how are you doing X today?" not "what happens if X breaks?"
```

### 6E: Generate Next Campaign Recommendations

Based on what worked, recommend the next campaign iteration:

```markdown
## Next Campaign Recommendations

### Double Down
- **Pain-focused variants won across all ad sets** → Next campaign: allocate 60% of budget to pain-focused variants, test 3 pain sub-angles (manual process, time waste, audit failure risk)
- **VP Engineering was the top-converting persona** → Consider increasing bid/budget for this ad set

### Test Next
- **Question-based variant showed high CTR but low conversion** → The question stops the scroll but the landing page may not match. Test a dedicated landing page that mirrors the question framing.
- **No data on Meta/LinkedIn yet** → Repurpose the top 3 Google winners as Meta ads to test cross-platform resonance

### Retire
- **Status quo / cost of inaction variants underperformed everywhere** → Retire this variant type for this persona. The Compounding Cost Model may apply better to executive personas (CFO/CEO) who think in longer time horizons.
```

### 6F: Predictions & Calibration

**This step turns the resonance loop from a one-shot analyzer into an iterative scientific instrument with a verifiable track record.** Read `references/prediction-cards.md` for the full schema, prediction types, persistence model, and the empirical lessons from prior backtests. That doc is the source of truth for everything in this section.

The principle: at the end of every loop run, write down explicit, falsifiable predictions about what specific metrics will do over a specific window. The next time the loop runs, evaluate the previous predictions against actual data and report a track record. Over time, calibration accumulates and the loop tunes its own confidence based on its own history of being right and wrong.

#### 6F.1: Read previous predictions FIRST (before generating new findings)

At the start of every loop run, before producing any new resonance map:

**Determine the MCC ID and today's date** (the loop needs both to find the right file and evaluate predictions):
- The MCC ID is the numeric suffix on the BigQuery table names. Run `bq ls <project>:<dataset>` and look for tables matching `ads_Campaign_<digits>`. The digits are the MCC ID. If multiple MCCs are present, ask the user which to analyze.
- Today's date in UTC: run `date -u +%Y-%m-%d` via the Bash tool, OR use the `currentDate` value from the system context if available.

**Then read previous predictions:**

1. Read `~/.octave/predictions/<MCC_ID>.json`. If the file doesn't exist, this is the first run for this account — skip to 6F.3 (no previous predictions to evaluate). On first run, copy `references/prediction-cards.template.json` to the destination path as the starter file.
2. Find all cards with `status: PENDING` whose `evaluation_window` end date is on or before today.
3. For each such card, read its `evaluation_sql` field — the loop generates SQL queries at prediction-creation time and stores them in the card so re-evaluation is deterministic. Substitute the placeholders (`<project>`, `<dataset>`, `<MCC>`, `<window_start>`, `<window_end>`) with the actual values, then run via `bq query`.
4. Apply the card's `confirms` / `refutes` / `inconclusive` conditions to the query result. Update the card with one of: `CONFIRMED`, `REFUTED`, `INCONCLUSIVE_FAVORABLE`, `INCONCLUSIVE_UNFAVORABLE`, or leave as `PENDING` with a `partial_evaluation` block if the window data isn't fully landed yet (the BQ data only goes through yesterday — anything past that is `PENDING`).
5. **Apply the refresh-window rule**: if the prediction's `evaluation_window` end date is within the last `refresh_lag_days` (typically 7), set `tentative: true` on the card regardless of which resolution status you assigned. Both CONFIRMED and REFUTED can flip inside the refresh window — late-reported data can push rate metrics in either direction (CTR can drop if impressions grow faster than clicks; conversion rate can rise if late conversions come in; CPC can change as total cost adjusts). Only set `tentative: false` once the evaluation window has aged past `window_end + refresh_lag_days`. Tentative cards are re-evaluated on every subsequent run until they finalize. See `references/prediction-cards.md` § "Common pitfalls" #7 for the full rule and the empirical backtest evidence behind it.
5. Write `evaluated_at`, `evaluated_against`, and `evaluation_notes` for each updated card.
6. Execute the card's `action_if_<status>` instructions — most often this means promoting/demoting source cards in the library, NOT changing campaigns autonomously.

#### 6F.2: Show the user the "Previous Predictions Evaluated" panel

Before showing the new resonance map, show the user a summary of what the last run's predictions said and how they resolved:

```markdown
## Previous Predictions Evaluated

| ID | Type | Claim | Status | Notes |
|---|---|---|---|---|
| P-2026-04-03-004 | cpc-efficiency-gap | CPC gap holds at >= 3x | ✅ CONFIRMED | Held at ~5x via a new ad group that didn't exist at prediction time |
| P-2026-04-03-002 | regression-to-mean | Pilot ad group conv rate regresses to 0-3% | 🟡 INCONCLUSIVE_FAVORABLE | Volume gate failed (8 clicks); directional signal supports the prediction |
| P-2026-04-03-001 | regression-to-mean | Pilot ad group CTR regresses to 4-6% | 🟡 INCONCLUSIVE_UNFAVORABLE | Volume gate failed; CTR moved away from prediction |
| P-2026-04-03-003 | exposure-projection | Director Compliance reaches 30 clicks in 7 days | ⏳ PENDING | 4 of 7 days available; on track to refute |

**Track record so far**: 1 confirmed / 0 refuted / 2 inconclusive (1 favorable, 1 unfavorable) / 1 pending
**Strongest type**: cpc-efficiency-gap (1/1 confirmed)
```

This panel is the user-facing magic. It builds trust by being honest about what the loop got right and wrong last time.

#### 6F.3: Generate new prediction cards

After producing the new resonance map (Steps 6B–6E), generate **3–6 new prediction cards** covering the strongest claims in the current run. Read `references/prediction-cards.md` for the full taxonomy of prediction types and the rules for each.

Hard rules for prediction generation:

1. **Every prediction must be a SQL query that returns a boolean.** Vague claims ("the pain framing will keep winning") are not predictions.
2. **Every prediction must specify CONFIRMS, REFUTES, and INCONCLUSIVE conditions** as precise queries the next loop run can execute without additional human input.
3. **Prefer structural predictions over unit-specific predictions** (the structural-over-unit rule). The first backtest empirically validated this: structural predictions generalized to brand new units, unit-specific predictions failed when the named unit lost volume between windows. See `references/prediction-cards.md` § "The structural-over-unit rule" for examples.
4. **Always generate one `field-stability` prediction per run.** It's a meta-prediction about whether the cast of ad groups will change, and it's the first signal the loop has about whether to weight structural vs unit-specific claims more heavily on the next run.
5. **Don't generate `regression-to-mean` predictions for units below the volume gate.** Compute `(current run rate clicks/day) * 7 >= volume_gate`. If false, generate an `exposure-projection` instead — those can be confirmed even at low volume.
6. **Read the calibration block before generating new predictions, and apply self-tuning rules deterministically.** Don't eyeball the hit rate — apply these exact rules, in order:
   - **If a prediction type has fewer than 10 resolved cards** (CONFIRMED + REFUTED + INCONCLUSIVE_FAVORABLE + INCONCLUSIVE_UNFAVORABLE combined), use its default confidence and do not adjust. Small N is not a basis for tuning.
   - **If a prediction type has 10+ resolved cards and hit rate (CONFIRMED / resolved) ≥ 80%**, promote its default confidence by one tier (LOW → MEDIUM → HIGH). Surface findings of this type as "high-trust" in the resonance map.
   - **If a prediction type has 10+ resolved cards and hit rate ≤ 30%**, demote its default confidence by one tier and add a caveat to all findings of this type.
   - **If a prediction type has 10+ resolved cards and hit rate is 0%**, stop generating that type entirely on this run. Note in the calibration `lessons` that the type has been retired.
   - **If INCONCLUSIVE_FAVORABLE outnumbers INCONCLUSIVE_UNFAVORABLE by 3:1 or more across 10+ inconclusive cards of the same type**, the volume gate is too strict for that type. Note this in `lessons` and consider relaxing the gate (with user confirmation) on the next run.
   - **If a type has 10+ resolved with hit rate between 30% and 80%**, no adjustment — the type is calibrated reasonably.

   These rules are deterministic so two future LLM sessions reading the same calibration block will make the same tuning decisions. Always note in the loop output what tuning was applied (e.g., "cpc-efficiency-gap promoted from MEDIUM to HIGH based on 12/14 hit rate").

For each new card, fill in every field of the schema (see `references/prediction-cards.md` § "The prediction card schema"). Required fields: `id`, `generated_at`, `generated_by`, `mode`, `is_structural`, `claim`, `type`, `evaluation_window`, `evidence_at_prediction`, `confirms` (natural language), `refutes` (natural language), `inconclusive` (natural language), `evaluation_sql` (the parameterized SQL query that produces the data needed to apply the confirm/refute/inconclusive conditions — uses placeholders `<project>`, `<dataset>`, `<MCC>`, `<window_start>`, `<window_end>`), `confidence`, `rationale`, `action_if_confirmed`, `action_if_refuted`, `action_if_inconclusive`, `status: PENDING`.

The `evaluation_sql` field is what makes the loop deterministic across runs. Without it, the next session has to interpret the natural-language `confirms` field and reconstruct a query — different sessions may write different queries. Always emit the SQL at generation time so re-evaluation is mechanical, not interpretive. See `references/prediction-cards.template.json` for example schemas with `evaluation_sql` filled in.

#### 6F.4: Update the calibration block and write the file

After all evaluation and generation is complete, recompute the `calibration` block at the bottom of the JSON file:
- `total_predictions`, `evaluated`, `pending`, `confirmed`, `refuted`, `inconclusive_favorable`, `inconclusive_unfavorable`
- `directional_hit_rate`: (confirmed + inconclusive_favorable) / (resolved predictions)
- `by_type`: per-prediction-type breakdown with hit rates
- `lessons`: append any new lessons learned from this run (especially if a previously confirmed type just got refuted, or vice versa)

Write the file back to `~/.octave/predictions/<MCC_ID>.json`. Include a brief mention in the loop's user-facing output: "Updated prediction track record at `~/.octave/predictions/<MCC_ID>.json` — N new predictions generated, evaluate by [date]."

#### 6F.5: Show upcoming evaluation dates

Tell the user when the next meaningful prediction resolution will occur:

```markdown
## Upcoming Prediction Evaluation Dates

| Earliest evaluation | Predictions resolving |
|---|---|
| 2026-04-13 | P-2026-04-07-001 (CPC gap), P-2026-04-07-002 (CPC tier distribution), P-2026-04-07-003 (VP Eng ad group reaches 100 clicks) |
| 2026-04-13 | P-2026-04-07-004 (conversions reach 5), P-2026-04-07-005 (field stability) |

Re-run `/octave:ads resonance` on or after 2026-04-13 to see how these resolved.
```

This gives the user a reason to come back. It's also a hint for setting up `/schedule` (see "Scheduling" in `references/prediction-cards.md`).

#### 6F.6: Offer HTML output

After the chat-markdown resonance map, library updates, sales brief, next-campaign recommendations, and prediction cards have been generated, offer to also produce self-contained HTML reports for longitudinal consumption:

```
AskUserQuestion({
  questions: [{
    question: "Generate HTML reports alongside the chat output?",
    header: "HTML reports",
    options: [
      { label: "Both reports", description: "Resonance report (this run's findings) + Prediction dashboard (full calibration track record)" },
      { label: "Resonance report only", description: "Self-contained HTML of this run's findings, saved to ~/Desktop/" },
      { label: "Prediction dashboard only", description: "Self-contained HTML showing all active and resolved predictions with calibration stats, saved to ~/Desktop/" },
      { label: "Skip", description: "Chat output is enough" }
    ],
    multiSelect: false
  }]
})
```

- **Resonance report**: follow `references/resonance-report-template.md`. Save to `~/Desktop/resonance-report-<workspace-slug>-<YYYY-MM-DD>.html`.
- **Prediction dashboard**: follow `references/prediction-dashboard-template.md`. Save to `~/Desktop/prediction-dashboard-<workspace-slug>-<YYYY-MM-DD>.html`. Reads from `~/.octave/predictions/<MCC_ID>.json`.

Both reports are self-contained single HTML files with inline CSS and inline SVG charts — no external JS, no external images, only Google Fonts via CDN. They work offline after first load, print cleanly, and can be shared as a single file attachment.

Tell the user the path(s) after generating and suggest opening with `open <path>` (macOS) or double-click.

#### 6F.7: Failure modes

If the loop cannot read or write the predictions file (permissions, disk full, etc.):
- Continue with the rest of the resonance loop normally
- Tell the user clearly: "Unable to read/write prediction cards at `~/.octave/predictions/<MCC_ID>.json`. Calibration tracking is disabled for this run."
- Do NOT try to recreate the file from scratch (might destroy history)
- Do NOT proceed silently without telling the user the calibration system is broken

If the schema version of an existing file is NEWER than what the current loop knows about (current: v0.2):
- Refuse to write (would lose information from a future schema)
- Read PENDING predictions if possible, evaluate them, but do not append new predictions
- Tell the user the loop and the file are out of sync

---

## Important Notes

### Platform & Format Rules
- **Character limits are hard constraints** — NEVER exceed the platform's character limits. Count characters for every headline and description. If a headline is 31 chars for Google Search, it's invalid. Show the character count in parentheses after each headline/description.
- **Every headline MUST stand completely alone** — Google Responsive Search Ads rotate and combine headlines in any order. NEVER split a sentence across two headline slots (e.g., "Signal to Campaign in Hours Not" / "Weeks" is WRONG — "Weeks" is meaningless on its own). After generating all headlines for a variant, re-read each one in complete isolation. If it doesn't communicate a clear, complete idea by itself, rewrite it.
- **Include at least one CTA headline per variant** — Google needs a CTA option in the rotation. Include at least one headline like "Book a Demo Today", "See How It Works", or "Get a Free Assessment" so Google can pair it with any other headline. Don't make ALL headlines CTAs — one per variant is enough.
- **Platform differences matter** — Google Search is keyword-intent-driven (people searching for solutions). Meta/LinkedIn is interruption-driven (people scrolling). Adjust tone accordingly: Google = answer the query, Meta/LinkedIn = stop the scroll.

### Creative Quality Rules
- **Each variant must have a distinct emotional register** — Pain-focused should feel urgent and visceral. Outcome-focused should feel aspirational and concrete. Status quo should feel ominous and inevitable. Authority should feel provocative and contrarian. Data-driven should feel matter-of-fact and irrefutable. Social proof should feel reassuring and credible. If two variants sound the same tonally, one of them isn't doing its job. The brand voice sets the overall register (professional, conversational, provocative), but within that, each variant should occupy its own emotional territory.
- **Never use insider jargon in headlines** — Terms like "rebuild debt", "context gap", "messaging drift" may be core to your positioning but mean nothing to someone seeing the ad for the first time. Headlines must use language the BUYER already uses, not language you're trying to teach them. Jargon is acceptable in descriptions where there's room for context, but headlines must be instantly parseable. Test: would someone who's never heard of your product understand what this headline means?
- **Never claim what you can't prove** — If a headline implies a specific timeline ("90 Days"), metric ("3x Pipeline"), or capability, there MUST be a proof point or reference customer backing it. Use case names are NOT proof points — "The 90-Day Onboarding Accelerator" is a use case, not evidence that someone actually did it in 90 days. If a proof point confirms the number, you can use it. If it doesn't, don't invent the number.
- **Specificity beats cleverness** — "45 Min Research Now Takes 3 Min" will always outperform "Smarter Research for Modern Teams." Specific numbers, specific outcomes, specific pains. If you find yourself writing a headline that could apply to any B2B SaaS product, it's too generic. Rewrite with details that only YOUR buyer would care about.
- **Questions must self-select** — A good question-based headline makes the RIGHT person stop and the WRONG person scroll past. "Want better marketing?" fails because everyone says yes. "Is your ICP in the founder's head?" works because only early-stage marketing leaders relate to it. The test: would a product manager, engineer, or accountant answer "yes" to this question? If so, it's not specific enough.

### Sourcing & Attribution Rules
- **Prospect language is gold** — Always prefer language extracted from real calls/emails over generic marketing copy. If the knowledge base search returns prospect quotes, use their exact phrasing (adjusted for length).
- **Cite your sources** — For every piece of creative, note whether it came from prospect language (calls/emails), library entities (persona, playbook, use case), proof points, or was generated fresh. This transparency helps the user evaluate quality and builds trust in the methodology.
- **One theme per ad set** — Each ad set should have a clear thematic focus (one primary use case). Don't mix unrelated value props in the same ad set. Variants within the set test different ANGLES on the same theme.

### Targeting Rules
- **Negative targeting is as important as positive** — Bad clicks waste budget. Be thorough about who to exclude.

### Self-Review Checklist
Before presenting each variant, verify:
1. Every headline stands alone (read each in isolation)
2. No headline exceeds character limit
3. At least one CTA headline is included
4. No unsubstantiated claims (every number has a proof point source)
5. No insider jargon in headlines (descriptions are OK)
6. The variant's emotional register is distinct from other variants
7. Questions are specific enough to self-select the target buyer
8. The source attribution is honest (library-only creative is labeled as such)
