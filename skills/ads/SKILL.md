---
name: ads
description: Build ad campaign plans grounded in your Octave library. Generates ad sets with platform-ready creative, audience targeting, negative keywords, and landing page recommendations — every variant derived from an auditable source card built from real prospect language and proof points. Use when user says "build an ad campaign", "create ads", "ad campaign for", "generate ad sets", or asks for paid advertising creative. Do NOT use to analyze ad performance — use /octave:ads-resonance (the resonance loop) instead.
argument-hint: "[describe the campaign target and angle]"
---

# Octave Ads — Campaign Generation

Generate platform-ready ad campaign plans grounded in your Octave library intelligence. Creates one ad set per persona or ICP, with creative variants generated from real prospect language extracted from calls and emails. Source cards are persisted to disk so `/octave:ads-resonance` can later map performance back to the exact derivation chain behind each headline.

**MCP Server**: This skill requires the Octave MCP server. Look for available MCP tools that match the Octave tool names (e.g., `list_entities`, `list_findings`, `search_knowledge_base`, `get_entity`). The MCP server prefix varies by workspace — it may be `{octave_mcp}__`, `mcp__octave_myworkspace__`, or another name. If multiple Octave-like MCP servers are available and you're unsure which to use, ask the user which workspace to target.

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

Example — user input: `generate ad campaign for VPs of Engineering at mid-market FinServ companies dealing with compliance automation gaps`. Extracted: **Target** = VPs of Engineering at mid-market Financial Services companies; **Situation** = manual compliance processes that don't scale; **Angle** = your product automates the compliance workflow they're currently doing by hand — turning audit prep from weeks to hours. This angle should appear in EVERY variant — pain-focused variants should reference "your team spends weeks preparing for audits that should take hours," outcome-focused should reference "engineering teams that automated compliance prep cut audit cycles by X%," etc.

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
→ {octave_mcp}__list_entities(entityType: "brand_voice")
→ {octave_mcp}__get_entity(oId: "{brand_voice_oId}")  // fetch full voice guidelines (tone, word choice, style rules)
```

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
  → {octave_mcp}__list_entities(entityType: "persona")

If ICP or Segment mode:
  → {octave_mcp}__list_entities(entityType: "segment")
```

Present the list to the user and ask them to confirm which ones to build ad sets for, or select "all."

### 2B: Fetch Use Cases + Competitors

Fetch all use cases and competitors — these inform creative themes and negative targeting.

```
→ {octave_mcp}__list_entities(entityType: "use_case")
→ {octave_mcp}__list_entities(entityType: "competitor")
→ {octave_mcp}__list_entities(entityType: "proof_point")
→ {octave_mcp}__list_entities(entityType: "reference")
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

Additionally, search the knowledge base for library-level intelligence (entity descriptions, Motion ICP narratives, hypotheses):
```
→ {octave_mcp}__search_knowledge_base(
    query: "{persona name} pain points challenges objections",
    includeResources: false,
    limit: 10
  )
```

**Priority**: Findings from `list_findings` (real prospect voice) should ALWAYS be preferred over library entity descriptions when writing ad creative. Library data is the fallback when no findings exist.

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

### 2F: Build Variant Source Cards

**This step is critical.** Before generating any ad creative, build a structured analytical artifact — a **Source Card** — for every variant type you intend to generate. Source cards are the creative brief for each variant. The creative is derived FROM the card. Headlines and descriptions that can't trace back to a source card don't ship.

The Narrative Gap Card (Step 2E) already serves this purpose for the competitive variant. Now build equivalent cards for every other variant type.

For EACH ad set (persona/segment), build the following source cards using the data fetched in Steps 2A-2C. Not every card is required — skip any where the underlying data doesn't exist (e.g., skip Proof Chain if no proof points match this persona). But always produce at least: Pain Language Audit, one of Proof Chain or Compounding Cost Model, and Self-Selection Matrix.

See [source-card-templates.md](references/source-card-templates.md) for the seven source card templates (Pain Language Audit, Proof Chain, Self-Selection Matrix, Compounding Cost Model, Contrarian Thesis, Social Proof Hierarchy, Metric Defensibility).

**How Source Cards flow into Step 3:**

Each variant's creative generation in Step 3 follows this process:
1. Read the source card for that variant type
2. Use the "headline derivation" field as the starting point for headline writing
3. Use the source card's data tier / confidence tier to set the right level of claim strength
4. Cite the source card in the variant's attribution

If a source card reveals that the data doesn't support a variant (e.g., Proof Chain shows no defensible metrics → skip Data-Driven; Self-Selection Matrix shows no question scores above 6/10 → skip Question-Based), skip that variant and note why. This prevents weak variants from diluting the campaign.

---

## Step 2G: Persist Source Cards to Disk

**Always do this**, immediately after building the source cards in Step 2F and before generating creative in Step 3. The persisted file is the data contract between this skill and `/octave:ads-resonance`: it's what lets the resonance loop trace performance forward from source cards → variants → headlines. Without this file, the loop falls back to reverse-inference from headlines, which is much weaker.

### Where to write

Write source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`:

- **`<workspace_slug>`** is derived from the Octave workspace name returned by `{octave_mcp}__verify_connection()` (called earlier in Step 1 Question 4 for the landing page domain). Lowercase, replace spaces and special characters with hyphens, strip everything that isn't `[a-z0-9-]`. Example: workspace "Acme Marketing" → `acme-marketing`.
- **`<campaign_slug>`** is derived from the campaign's identifying details: `<persona-slug>-<segment-slug>-<YYYY-MM-DD>`. If the user has explicitly named the campaign, use that name (slugified).

If the file already exists at the target path (re-running Step 2F for the same campaign), append a `-v2`, `-v3`, etc. suffix. Never overwrite an existing source card file — the resonance loop may have already evaluated predictions tied to it.

### What to write

The file is a single JSON object. **The schema — campaign metadata, one entry per source card, and the `headlines_by_variant` / `descriptions_by_variant` maps — is defined in [source-cards.template.json](references/source-cards.template.json)**, including a fully worked example. Copy that template's structure. The `headlines_by_variant` and `descriptions_by_variant` fields start as empty objects — **Step 3C fills them in after creative generation**, mapping each `{ad_set}/{variant_type}` key to the headlines and descriptions that were actually generated. This is what the resonance loop matches against ad-platform data later.

### How to write

1. Compute the workspace_slug and campaign_slug.
2. Check if the directory exists: `ls ~/.octave/source_cards/<workspace_slug>/ 2>/dev/null`.
3. If not, create it: `mkdir -p ~/.octave/source_cards/<workspace_slug>/`.
4. Check for existing files matching the campaign_slug. If a file exists, increment the version suffix.
5. Write the JSON file. Use `chmod 600` since it may contain prospect quotes from real calls.
6. Tell the user explicitly: "Saved source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`. The resonance loop (`/octave:ads-resonance`) will use these to map performance back to derivation chains in future runs."

### Why this is unconditional

- The directory lives under `$HOME/.octave/`, outside any repo, and is isolated per user; files are user-owned with mode 600
- The cost of storing a few KB of JSON per campaign is negligible
- The resonance loop is dramatically more useful with the forward derivation chain available

If the user explicitly objects to persistence (e.g., they don't want any local files), they can pass `--no-persist-source-cards` as an argument and Step 2G is skipped. Default is to persist.

---

## Step 3: Generate Ad Sets

**CRITICAL**: If Step 0 extracted a campaign angle from the user's arguments, that angle MUST be woven into every variant's creative. The angle is not supplementary context — it is the primary lens through which all headlines, descriptions, and keyword strategies should be written. Library data (personas, use cases, proof points) provides supporting evidence, but the user's stated angle leads.

For EACH persona/ICP/segment (based on the structure chosen), generate a complete ad set plan following the output template in [ad-set-template.md](references/ad-set-template.md).

Generate 4-8 ad variants per ad set. **Every variant MUST be derived from its corresponding Source Card built in Step 2F.** The source card is the creative brief — read it first, use its "headline derivation" field as the starting point, and cite it in attribution. The eight variant types (pain-focused, outcome-focused, social proof, competitive, question-based, data-driven, status quo, authority), each with its driving source card, methodology, and skip condition, are defined in [variant-methodologies.md](references/variant-methodologies.md) — read that file before generating creative.

Rules for variant selection:
- Apply the selected brand voice/tone from Step 1 across all variants.
- Not every variant is required — skip any where the source card flagged insufficient data (the card already explains why).
- Always include at least: pain-focused, outcome-focused, and one of status quo or question-based.
- Respect the platform constraints from Step 1 for every piece of creative (see the per-platform examples in the ad-set template).

---

## Step 3B: Headline Independence Review

After generating all ad sets, perform a dedicated review pass on EVERY headline across all variants. This is a separate, explicit step — not part of initial generation.

The generation-time rules this review enforces:
- **Every headline MUST stand completely alone.** Google Responsive Search Ads rotate and combine headlines in any order. NEVER split a sentence across two headline slots (e.g., "Signal to Campaign in Hours Not" / "Weeks" is WRONG — "Weeks" is meaningless on its own).
- **Include at least one CTA headline per variant** (e.g., "Book a Demo Today", "See How It Works", "Get a Free Assessment") so Google can pair it with any other headline. Don't make ALL headlines CTAs — one per variant is enough.

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

After Steps 3 and 3B are complete and all final headlines are settled, **update the source card file written in Step 2G** with the actual headlines that were generated for each variant. This is what closes the loop — without this update, the resonance loop has no way to match ad-platform performance back to source cards.

1. Read the source card file at `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json`.
2. Populate the `headlines_by_variant` field. The shape is `{ "<ad_set_name>": { "<variant_type>": [headline strings...], ... }, ... }` — see the worked example in [source-cards.template.json](references/source-cards.template.json).
3. Also include the descriptions in the parallel `descriptions_by_variant` field with the same shape.
4. Write the updated file back. Tell the user: "Updated source cards file at `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json` with N final headlines across M variants. The resonance loop will use these to map performance back to derivation chains."

Skipping this step means the resonance loop cannot use its forward-inference path for this campaign. It will still work by reverse-inference from headlines, but without the strong derivation chain.

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
5. Once the campaign has been running, close the loop with /octave:ads-resonance
```

---

## Step 5: Offer Follow-Up Actions

Ask the user via AskUserQuestion:

1. **Refine a specific ad set** — Regenerate creative for one ad set with different angles
2. **Add a competitive campaign** — Build ad sets specifically targeting competitor users
3. **Generate more variants** — Add more creative variants to existing ad sets
4. **Export as CSV** — Format the campaign plan for bulk upload to the ad platform
5. **Generate visual campaign deck** — Create a self-contained HTML slide deck showing the full campaign with variant grids, rationale, targeting, competitive gap cards, and budget allocation. Useful for sharing with stakeholders or reviewing the campaign visually.
6. **Run the resonance loop** — Once the campaign has performance data, run `/octave:ads-resonance` to analyze it, map winners back to source cards, and feed learnings into the library.
7. **Done** — Finished

### Export

If they choose export, ask which platform via AskUserQuestion:

- **Google Ads (Web UI)** — Separate CSV files per entity type for the Google Ads web UI bulk upload (Tools → Bulk Actions → Uploads).
- **Google Ads (Editor)** — Single file for the Google Ads Editor desktop app (tab-separated UTF-16, all entity types in one file; import via Account → Import → From file).
- **Meta Ads** — Single CSV with Primary Text, Headline, Description, Link, and Call to Action columns. One row per ad variant. Apply platform character limits (Primary Text: 125 chars, Headline: 40 chars).
- **LinkedIn Ads** — Single CSV with Intro Text, Headline, Description, Destination URL columns. One row per ad variant. Apply platform character limits (Intro Text: 150 chars, Headline: 70 chars).

**Google Ads (Web UI) export:**

1. **Collect Customer ID**: Ask the user for the Google Ads Customer ID of the **upload destination account** (the account number in the Google Ads header, e.g., `123-456-7890`). This can be either an MCC or a sub-account — whichever they'll select in the Ads UI before clicking Upload. Using an ID that doesn't match the active account in the UI causes "entity does not exist" errors.
2. **Read [google-ads-csv-format.md](references/google-ads-csv-format.md)** for the exact column layouts, quoting rules, upload order, and validation checklist — follow it exactly.
3. Ask the user where to save (suggest `~/Desktop/{campaign-name}/`), then generate the five numbered CSVs (campaign, ad groups, ads, keywords, negative keywords).
4. **Tell the user**: "Upload these files to Google Ads → Tools → Bulk Actions → Uploads, in numbered order. Wait for each to succeed before uploading the next. All campaigns are set to Paused — nothing will run until you explicitly enable them."

**Google Ads (Editor) export:**

1. **Read [google-ads-editor-format.md](references/google-ads-editor-format.md)** for the exact 144-column layout, entity type detection rules, value differences from the web UI format, and the validation checklist.
2. Generate a single tab-separated UTF-16 file via the Python snippet in that reference (Claude cannot write UTF-16 tab-separated files directly — use a Bash tool call). No Customer ID needed — it imports into whatever account is open. Save to `~/Desktop/{campaign-name}-editor.csv`.
3. **Tell the user**: "Open Google Ads Editor, sign into your account, then Account → Import → From file. All campaigns are set to Paused. Review in the Editor, then Post to push live."

If they choose **Generate visual campaign deck**, read [html-deck-template.md](references/html-deck-template.md) for the full deck structure, section layout, variant color coding, and visual design spec. Follow that template to produce the HTML file.

---

## Important Notes

### Platform & Format Rules
- **Character limits are hard constraints** — NEVER exceed the platform's character limits. Count characters for every headline and description. If a headline is 31 chars for Google Search, it's invalid. Show the character count in parentheses after each headline/description.
- **Headline independence and CTA rules** — See Step 3B: every headline must stand alone, and every variant needs exactly one CTA headline. The Step 3B review pass is mandatory, not optional.
- **Platform differences matter** — Google Search is keyword-intent-driven (people searching for solutions). Meta/LinkedIn is interruption-driven (people scrolling). Adjust tone accordingly: Google = answer the query, Meta/LinkedIn = stop the scroll.

### Creative Quality Rules
- **Each variant must have a distinct emotional register** — Pain-focused should feel urgent and visceral. Outcome-focused should feel aspirational and concrete. Status quo should feel ominous and inevitable. Authority should feel provocative and contrarian. Data-driven should feel matter-of-fact and irrefutable. Social proof should feel reassuring and credible. If two variants sound the same tonally, one of them isn't doing its job. The brand voice sets the overall register (professional, conversational, provocative), but within that, each variant should occupy its own emotional territory.
- **Never use insider jargon in headlines** — Terms like "rebuild debt", "context gap", "messaging drift" may be core to your positioning but mean nothing to someone seeing the ad for the first time. Headlines must use language the BUYER already uses, not language you're trying to teach them. Jargon is acceptable in descriptions where there's room for context, but headlines must be instantly parseable. Test: would someone who's never heard of your product understand what this headline means?
- **Never claim what you can't prove** — If a headline implies a specific timeline ("90 Days"), metric ("3x Pipeline"), or capability, there MUST be a proof point or reference customer backing it. Use case names are NOT proof points — "The 90-Day Onboarding Accelerator" is a use case, not evidence that someone actually did it in 90 days. If a proof point confirms the number, you can use it. If it doesn't, don't invent the number.
- **Specificity beats cleverness** — "45 Min Research Now Takes 3 Min" will always outperform "Smarter Research for Modern Teams." Specific numbers, specific outcomes, specific pains. If you find yourself writing a headline that could apply to any B2B SaaS product, it's too generic. Rewrite with details that only YOUR buyer would care about.
- **Questions must self-select** — A good question-based headline makes the RIGHT person stop and the WRONG person scroll past. "Want better marketing?" fails because everyone says yes. "Is your ICP in the founder's head?" works because only early-stage marketing leaders relate to it. The test: would a product manager, engineer, or accountant answer "yes" to this question? If so, it's not specific enough.

### Sourcing & Attribution Rules
- **Prospect language is gold** — Always prefer language extracted from real calls/emails over generic marketing copy. If the knowledge base search returns prospect quotes, use their exact phrasing (adjusted for length).
- **Cite your sources** — For every piece of creative, note whether it came from prospect language (calls/emails), library entities (persona, Motion ICP narrative, use case), proof points, or was generated fresh. This transparency helps the user evaluate quality and builds trust in the methodology.
- **One theme per ad set** — Each ad set should have a clear thematic focus (one primary use case). Don't mix unrelated value props in the same ad set. Variants within the set test different ANGLES on the same theme.

### Targeting Rules
- **Negative targeting is as important as positive** — Bad clicks waste budget. Be thorough about who to exclude.

### Self-Review Checklist
Before presenting each variant, verify:
1. The Headline Independence Review (Step 3B) passed: every headline stands alone, is within character limits, and exactly one CTA headline is included
2. No unsubstantiated claims (every number has a proof point source)
3. No insider jargon in headlines (descriptions are OK)
4. The variant's emotional register is distinct from other variants
5. Questions are specific enough to self-select the target buyer
6. The source attribution is honest (library-only creative is labeled as such)

## Related Skills

- `/octave:ads-resonance` - Analyze this campaign's performance, map winners back to source cards, and feed learnings into the library (the resonance loop)
- `/octave:campaign` - Multi-channel campaign content (email, LinkedIn, social, blog, landing pages)
- `/octave:brainstorm` - Ideate campaign angles before building
- `/octave:messaging` - Build the messaging framework that feeds ad creative
