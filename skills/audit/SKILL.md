---
name: audit
description: Audit your Octave library for gaps, stale content, duplicates, language issues, and strategic design quality. Use when user says "audit my library", "check for gaps", "library health check", "find duplicates", or asks about library quality and completeness.
---

# /octave:audit - Library Health Check

Comprehensive audit of your Octave GTM library. This skill operates as three things:

1. **Gap analyzer** — what's missing that would make agents smarter
2. **Overlap ID'er** — what's redundant or splitting hairs unnecessarily
3. **Strategic thought partner** — push and challenge on design choices

The goal is not just "is the library complete?" but "is the library well-designed for what agents need to do?"

**Core operating principle:** The audit is a coach, not a builder. Push the user to think deeper about their GTM design rather than auto-generating content. Opinions are good — but only the USER's well-considered opinions. More entities isn't better. Better entities are better. The audit's job is to ask the questions that draw out the right design, not to fill templates.

## Usage

```
/octave:audit [--type <entity-type>] [--fix]
```

## Options

- `--type <type>` - Focus on specific entity type (personas, playbooks, products, segments, etc.)
- `--fix` - Interactive mode to address issues as they're found
- `--detailed` - Show full details for each issue (default: summary view)

## Instructions

When the user runs `/octave:audit`:

### Step 1: Gather Library State

**Resolve Octave MCP server first:** The Octave MCP server provides tools like `verify_connection`, `get_entity`, `list_all_entities`. From your tool list, get the server name (e.g. `octave-acme`).

**Fetch entities using MCP tools:**

```
1. list_all_entities({ entityType: "persona" })
2. list_all_entities({ entityType: "product" })
3. list_all_entities({ entityType: "playbook" })
4. list_all_entities({ entityType: "segment" })
5. list_all_entities({ entityType: "use_case" })
6. list_all_entities({ entityType: "competitor" })
7. list_all_entities({ entityType: "alternative" })
8. list_all_entities({ entityType: "buying_trigger" })
9. list_all_entities({ entityType: "proof_point" })
10. list_all_entities({ entityType: "reference" })
```

Then use `get_entity` for entities that need deeper inspection (qualifying questions, field completeness).

If `--type` is specified, only fetch that type (but still need related types for relationship checks).

### Step 2: Determine Mode

After gathering the library state, ask the user:

```
I can see your library has [X] total active entities across [Y] types.

How would you like to approach this?

1. Onboarding review — I'm building this library out. Help me figure out
   what to build next and how to design it well.

2. Cleanup audit — This library has been around. Find what's broken,
   redundant, stale, or poorly written.
```

**Auto-detect hint:** If the library has fewer than 10 total entities, or is missing products/personas entirely, default-suggest onboarding. If it has 30+ entities across most types, default-suggest cleanup. Present both options either way.

---

## ONBOARDING MODE

When the user selects onboarding, the audit shifts from "what's wrong" to "what to build next and how to design it well." The tone is forward-looking — a strategic planning partner who challenges the user to think critically, not a template filler.

**CRITICAL PRINCIPLE:** The audit should NEVER auto-generate entity content in onboarding mode without the user's input. Its job is to push the user to think, not to think for them. The user knows their business — the audit's job is to ask the questions that draw out the right design.

### Step 3-O: Assess What Exists

Summarize the current state in plain language:

```
Here's what you have so far:

Foundation:
  Product/Service: [name(s)] / missing
  Personas: [count] — [list names]
  Segments: [count] — [list names]

Execution:
  Playbooks: [count] — [list names + what they link]
  Use Cases: [count]

Depth:
  Competitors: [count]
  Alternatives: [count]
  Buying Triggers: [count]

Evidence:
  Proof Points: [count]
  References: [count]
```

### Step 4-O: Build Priority Roadmap

Based on what exists, generate a prioritized build roadmap. The tiers represent dependency order — later tiers build on earlier ones.

**Tier 1 — Foundation (build first):**
These are the inputs everything else depends on. Agents can't do useful work without them.
- Product or service entity (the thing you sell — capabilities, differentiators, status quo it replaces)
- Core personas (the people who discover, evaluate, and champion — not everyone who touches a deal)
- Core segments (the company types where your product fits differently)

**Tier 2 — Execution (build once foundation exists):**
This is where the library becomes actionable for agents.
- Playbooks linking personas to products with specific approach angles
- Value props per persona within each playbook
- Use cases describing customer outcomes (not internal processes)

**Tier 3 — Depth (makes agents sharper):**
These enrich agent output with competitive awareness, urgency, and situational intelligence.
- Competitors (named rivals agents will encounter in deals)
- Alternatives (behavioral patterns — what teams do instead of buying, like building internally or using general AI)
- Buying triggers (organizational moments that create urgency — new hire, funding, key departure)

**Tier 4 — Evidence (makes agents credible):**
Agents can sell without these, but they sell better with them. **IMPORTANT: Never fabricate evidence entities.** Proof points and references must come from real customer outcomes.
- Proof points (pattern-based results agents can reference — the user needs to provide real examples)
- References (customer stories with enough context to tell a 2-sentence narrative — requires real customer data)

For each tier, tell the user:
1. What they already have from that tier
2. What's missing
3. Why it matters for agent output (not abstract — specific: "without segments, your email agent writes the same pitch to a 50-person startup and a 5,000-person enterprise")

**Quantity guidance:** Don't suggest target counts. Instead, frame it as: "What's the minimum set that captures how your business actually works?" A company with one product and two buyer types might need 2 personas. A company with three products and matrix selling might need 8. The right number comes from the business, not a template.

### Step 5-O: Design Challenge

Before the user starts building, run a challenge pass. These are NOT tips to follow — they're hard questions the user needs to answer. The audit's job is to push the user to make deliberate choices, not to prescribe a structure.

**PERSONA CHALLENGE:**
- "Think about the last 5-10 deals you closed. Who actually drove them forward? Not who was in the room — who found you, who evaluated you, and who pushed the deal through internally? Those are your core personas."
- "If I showed your agents two of your personas and asked them to write different emails for each — would the emails actually be different? If the pitch to 'VP Marketing' and 'CMO' would be identical, they're one persona with two titles."
- "Are any of your personas 'nice to have' rather than 'need to have'? A persona nobody playbooks against is dead weight."

**SEGMENT CHALLENGE:**
This is the most important design decision in the library. Push hard here.

- "What actually changes how you sell? Not your pitch deck's market slide — what makes a conversation with Company A fundamentally different from Company B? THAT'S your segment boundary."
- "Your segments determine how agents differentiate messaging. If you segment by industry but your pitch doesn't actually change between a tech company and a financial services company — industry isn't a real segment for you. What dimension actually changes the conversation?"
- **Do NOT prescribe a specific taxonomy.** Don't suggest maturity × vertical or stage × business model or any specific framework. Instead, press the user to discover their own natural dimensions:
  - "Walk me through how you'd describe your best customers to a new AE. What categories do you naturally reach for?"
  - "When you lose a deal, is it usually because of WHO they are (wrong type of company) or WHERE they are (wrong stage, wrong timing)? That tells you whether your primary axis is company type or company stage."
  - "Do you have explicit 'not for us' types? Companies you'd actively disqualify? Those anti-patterns can be just as valuable as your target segments — but only if they're real patterns you've seen, not theoretical."
- **Watch for over-slicing**: "If you're heading toward 10+ segments, challenge each one: does this segment change what an agent says? If removing it wouldn't change a single email or call prep, it's not a real segment."
- **Watch for under-slicing**: "If you have 1-2 segments, challenge whether you're lumping together prospects that actually need different approaches. Does your 50-person startup customer hear the same pitch as your 5,000-person enterprise customer?"

**USE CASE CHALLENGE:**
- "Name use cases as outcomes, not processes. 'Compress territory planning' sells. 'Technical onboarding flow' doesn't. Agents use these to explain what your product does for people — frame them from the customer's perspective."
- "Keep names short — under ~8 words. The description carries the detail. Names are labels, not summaries."
- "Think about the customer lifecycle: do your use cases only cover the 'doing' phase, or do they span from 'figuring out what to do' through 'doing it' to 'learning from what happened'? Most libraries over-index on execution use cases and miss the strategic layer."

**COMPETITOR & ALTERNATIVE CHALLENGE:**
- "Competitors are named rivals. But who do you ACTUALLY lose to most often? Is it a named company, or is it inertia — the prospect deciding to do nothing, build it themselves, or cobble something together?"
- "Alternatives are the real competition for most companies. What do your prospects do TODAY instead of buying your product? That behavioral pattern is what your agents need to address."
- "For competitors: don't list every company in your space. List the ones your reps actually encounter in deals. If you've never lost a deal to Competitor X, they don't belong in your library."

**EVIDENCE CHALLENGE:**
- "Proof points and references are the only entity types that MUST come from reality. I can help you think through every other entity type, but proof points need real results and references need real customer stories."
- "What results have your customers actually seen? Not what you hope — what you can point to. Think about specific outcomes, time savings, revenue impact, team efficiency gains."
- "Do you have 2-3 customers who would let you tell their story? Even anonymized, a reference with 'how they make money, how they use us, how we impacted their business' gives agents real narrative to work with."
- "If you don't have evidence yet, that's fine — skip this tier and come back when you do. Empty proof points are worse than no proof points because agents will try to use them."

**General language guidance:**
- "Write library content as operating context for AI agents, not sales copy for humans. Describe how the world works, what problems look like, what outcomes feel like. Agents produce better output from grounded context than from pre-written pitch language."
- "Pick one voice and stick with it. Third-person declarative ('teams struggle with...') is the most common choice. Mixing 'you/your' and 'they/their' across entities makes agent output inconsistent."
- "Avoid capitalizing coined terms unless they're actual branded trademarks. Agents treat capitalized multi-word phrases as proper nouns and parrot them to prospects."

### Step 6-O: Quick Check on What Exists

Even in onboarding mode, run a light version of the cleanup checks on whatever already exists:
- Completeness checks on existing entities (are they fleshed out or just stubs?)
- Language/voice consistency (catch issues early before they multiply)
- Product name leakage in use cases/alternatives
- Duplicate detection (catch overlaps before building more)
- **Qualifying question weight audit** (see Qualifying Questions Audit section — catch all-MEDIUM patterns early)

Skip freshness checks (everything is new) and skip the full strategic design review (they're still building).

### Step 7-O: Generate Onboarding Report

See [onboarding-report-template.md](references/onboarding-report-template.md) for the onboarding report template.

### Onboarding Fix Mode (--fix)

In onboarding --fix mode, offer to:
1. **Flesh out stubs** — existing entities that are just names with thin descriptions
2. **Fix early language issues** — catch voice/naming problems before they multiply
3. **Walk through design challenges interactively** — shift into Socratic mode

**IMPORTANT:** For entity creation in fix mode, prefer drawing out the user's knowledge over generating content. Shift into a guided conversation:

```
Let's build your personas. Think about the last 5 deals you closed.

1. Who found you or took the first meeting?
2. Who evaluated you against alternatives?
3. Who championed you internally and pushed the deal forward?
4. Who signed off on the budget?

These might be 2 people or 5. Let's start with whoever shows up most.
```

For segments:
```
Let's figure out your segments. Don't think about market categories —
think about your actual customers.

1. Pick your best customer. What kind of company are they?
2. Pick your second-best customer. What's different about them vs #1?
3. If you had to write a different opening line for each — what would change?

That difference is your first segment boundary. Let's see if it holds
across more examples.
```

For evidence (proof points + references):
```
Let's talk about evidence. I'm NOT going to generate these — they need
to come from reality.

1. What's the best result a customer has told you about?
2. Do you have any case studies, testimonials, or metrics you share?
3. Can you name 2-3 customers you could reference (even anonymized)?

If you don't have these yet, let's skip evidence and come back later.
Fabricated proof points are worse than none.
```

When the user provides their answers, THEN create entities using their actual input. The audit shapes and structures — it doesn't invent.

---

## CLEANUP MODE

When the user selects cleanup, run the full audit as described below. This is the standard mode for established libraries.

### Step 3-C: Run Audit Checks

Perform the following checks and categorize issues by severity:

#### Coverage Checks (CRITICAL)

**Missing Core Entities:**
- [ ] At least 1 product or service defined
- [ ] At least 1 persona defined
- [ ] At least 1 playbook defined

**Orphaned Playbooks:**
- [ ] Every playbook has at least 1 buyer persona linked
- [ ] Every playbook has a primary product linked
- [ ] Playbooks have value props for their linked personas

**Broken References:**
- [ ] Personas referenced in playbooks exist
- [ ] Products referenced in playbooks exist
- [ ] Use cases referenced exist

**Library Shape — Contextual Proportions:**

Don't enforce minimum counts. Instead, look at the library as a whole and surface imbalances that reveal what agents can and can't do. The right number of any entity type depends on the company — 2 competitors might be exactly right for a niche market, or dangerously thin for a crowded space. Think about the company and whether the proportions make sense.

Examples of observations to surface:
- "You have 9 personas targeting different buyers but only 2 segments. That means your agents differentiate by role but not by company type or stage — every persona gets the same pitch regardless of who they work for. Is that intentional?"
- "You have 20 use cases but 0 buying triggers. Your agents can explain what you do but can't recognize the moments that create urgency to buy."
- "You have 8 competitors but 0 alternatives. Your agents can handle named competitive situations but can't address the behavioral alternatives — like teams building internally or using general LLMs — that often represent the real competition."
- "You have 15 personas and 12 segments but only 1 playbook. All of that targeting intelligence has no execution vehicle."

The goal is to tell a story about what the library's shape means for agent capability, not to hit a minimum count.

#### Completeness Checks (WARNING)

**Personas:**
- [ ] Has pain points defined (not empty)
- [ ] Has key objectives defined
- [ ] Has primary responsibilities defined
- [ ] Has description (>50 chars)

**Playbooks:**
- [ ] Has strategic narrative
- [ ] Has approach angle
- [ ] Has key insights
- [ ] Has qualifying questions
- [ ] Has value props for each linked persona

**Products:**
- [ ] Has description
- [ ] Has key capabilities
- [ ] Has differentiators

**Segments:**
- [ ] Has description
- [ ] Has firmographic characteristics

**Competitors:**
- [ ] Has strengths defined
- [ ] Has weaknesses defined
- [ ] Has differentiation points

**Alternatives:**
- [ ] Has whereItWorks and whereItBreaks defined
- [ ] Has behavioral description (not just a tool/category name)

**Buying Triggers:**
- [ ] Has whoFeelsThisMost defined
- [ ] Has howWeHelpInThisMoment defined
- [ ] Has whyThisCreatesUrgency defined
- [ ] Has whatsTheCostOfInaction defined
- [ ] A trigger with just a name and one-line description gives agents nothing to work with

**Proof Points:**
- [ ] Has quantified metric/statistic
- [ ] Has source/validation

**References:**
- [ ] Has success metrics
- [ ] Has use case context

#### Qualifying Questions Audit (WARNING)

**Pull qualifying questions from all entities via `get_entity` and analyze:**

**Weight Distribution:**
For each entity type that has qualifying questions, analyze the weight distribution:
- Count questions by weight: HIGH, MEDIUM, LOW, INSTANT_DISQUALIFIER
- **Flag all-MEDIUM**: If every qualifying question on an entity (or across all entities of a type) uses MEDIUM weight, flag this explicitly:
  ```
  [FLAT-WEIGHTS] All 12 qualifying questions on personas use MEDIUM weight.
  Impact: Qualification scores become a simple yes/no count with no
  prioritization. A match on "has a defined ICP" counts the same as
  "is investing in AI tools." Agents can't tell critical signals from
  nice-to-haves.
  Fix: Run /octave:qual-doctor to tune weights based on actual predictive power.
  ```
- **Flag weight monotony per entity**: If a single entity has 5+ questions all at the same weight (any weight), note it.

**FitType Balance:**
- Check the ratio of GOOD fit vs BAD fit questions per entity
- Flag entities with NO BAD fit questions: "This entity can only score prospects UP, never DOWN. It has no way to penalize bad fits."
- Flag entities with NO GOOD fit questions (rare but possible)

**Question Quality Spot-Check:**
- Look for questions that are too vague to be useful: "Is this a good company?" or "Do they need our product?"
- Look for questions that duplicate each other within the same entity
- Look for questions with missing or empty rationale fields

**Cross-Entity Comparison:**
- In multi-entity types (personas, segments), check whether different entities have meaningfully different questions or just variations of the same ones
- If all personas ask roughly the same questions, the routing system can't differentiate between them

**IMPORTANT:** The audit identifies qualifying question issues. For actual tuning (testing against real prospects, diagnosing specific scoring patterns, applying fixes), recommend `/octave:qual-doctor`. The audit is the diagnostic scan; qual-doctor is the treatment.

#### Language & Voice Checks (WARNING)

These checks catch issues that directly affect agent output quality. The library is consumed by AI agents, not humans — language problems here become language problems in every email, call prep, and qualification an agent produces.

**Voice consistency within entity types:**
- [ ] For each entity type with 3+ entities, check if descriptions use mixed perspectives (some second-person "you/your", some third-person "teams/they"). Flag the outliers. Inconsistent voice across entities of the same type produces inconsistent agent output.

**Capitalized coined terms:**
- [ ] Scan descriptions and data fields for capitalized multi-word phrases that aren't proper nouns, company names, or acronyms (e.g., "Rebuild Debt", "Hero Dependency"). Agents treat capitalized multi-word phrases as branded proper nouns and parrot them verbatim to prospects who have no context for the jargon.
- When fixing: **replace, don't flatten.** Removing a coined term and replacing it with a vague word ("the gap") loses the sharpness of the original. Replace with language that carries equal specificity. Example: "the Context Gap" → "the disconnect between what a team knows about its market and what its tools actually use" — not just "the gap."

**Verbose entity names:**
- [ ] Check use case and buying trigger names for unnecessary length. Names over ~8 words often repeat what the description already says. Short names ("Detect Messaging Drift") work better than verbose ones ("Detect Messaging Drift And Fix It Before It Damages Pipeline") because agents use names as labels, not summaries.

**Product name in wrong entity types:**
- [ ] Check if the product or service name appears in use case, alternative, or buying trigger descriptions. Use cases describe what happens for the customer. Alternatives describe what teams do instead. Buying triggers describe organizational moments. None of these should name the product as the solution — that's what the product entity and playbooks are for. When agents pull from a use case that says "Acme solves this," the output sounds like a brochure instead of a conversation.

#### Strategic Design Review (INFO)

These are not pass/fail checks. They are guided evaluations — the audit acting as a strategic thought partner. Present findings as observations and questions, not verdicts. The user knows their business better than the audit does.

**Persona role relevance:**
Ask: "Do your personas represent the people who actually drive your buying motion — the ones who discover, evaluate, and champion?" Look at persona descriptions and note any that primarily describe roles typically outside the buying process. But present as a question, not a verdict — for some businesses, procurement IS the buyer, CS IS the champion for expansion. The trap is including everyone who touches the deal rather than the people who drive it.

**Segment design coherence:**
Three things to evaluate:

1. Do segments appear to follow an organizing principle? Look for shared naming patterns, structural grouping, or a dimensional taxonomy. If segments are a flat, unrelated list, prompt the user to consider whether a structure would sharpen agent output. But a flat list might be correct for a simple business — the value is in prompting the user to think about it.

2. If segments appear to follow a matrix taxonomy, check whether it's over-sliced. A 5x5 matrix = 25 segments, which likely means agents are trying to differentiate too many flavors and each segment gets too thin to be meaningful. Challenge whether each segment actually feels different from its neighbors.

3. **Challenge the segment axis itself:** Don't assume any particular axis is correct. Ask: "Your segments are organized by [industry/stage/size/etc.]. Does that dimension actually change how your agents should talk to prospects? Or would a different lens produce more meaningful differentiation?" The right answer depends on the business. The audit's job is to make the user justify their choice, not to prescribe an alternative.

**Use case: outcomes vs internal processes:**
Check if use case descriptions focus on customer outcomes or internal processes. Descriptions centered on setup, configuration, onboarding, or internal workflows ("Technical Onboarding", "Configure Your Dashboard") may be internal processes rather than customer-facing outcomes. Agents can sell outcomes; they can't sell internal operations. "Compress territory planning from months to weeks" is sellable. "Technical onboarding flow" is not.

**Use case lifecycle coverage:**
Check whether use cases cluster around a single phase (usually execution/doing) or span the full customer lifecycle. A library with 15 "Run X" use cases but nothing about "Figure out X" or "Learn from X" means agents can only talk about the doing — not the strategic thinking before or the optimization after. Surface this as an observation: "All your use cases describe execution. Do your prospects also need help figuring out what to do, or learning from what they've done?"

**Proof point reusability:**
Check if proof point descriptions or talk tracks reference specific customer names. Proof points that say "Acme Corp achieved X" can only be used with permission. Pattern-based proof points ("teams of one deliver full-team output") can be applied to any conversation. Flag customer-specific proof points and ask whether agents have permission to use those names.

**Alternative behavioral framing:**
Check if alternatives describe behavioral patterns (what teams do instead of buying) vs just naming a tool or category. Good alternatives paint a picture of the prospect's current world and where it breaks down. "Salesforce" as an alternative tells agents nothing. "Teams wire up CRM automations and rely on admins to maintain field logic" tells agents what the prospect's reality looks like and where to probe.

**Buying trigger narrative depth:**
Beyond the completeness check (are the fields populated?), evaluate whether triggers describe real organizational moments with enough narrative that an agent can recognize the situation AND have something useful to say. A thin trigger is worse than no trigger because the agent thinks it has context when it doesn't.

**Content as operating context vs sales copy:**
Flag descriptions that read like pitch copy rather than operating context: opening with imperatives ("Stop wasting time on...!"), rhetorical questions ("Imagine a world where..."), or heavy promotional framing. The library is consumed by AI agents — operating context that describes how the world works produces better agent output than pre-written sales language. Important caveat: precise sales terminology that describes real dynamics ("champion", "multithreading", "pipeline coverage") is fine. The flag is for tone and framing, not vocabulary.

**Evidence gap challenge:**
If the library has 0 proof points AND 0 references, don't just flag it as "missing." Challenge the user:
- "Your agents have no evidence to cite. When a prospect asks 'who else uses this?' or 'what results have you seen?' — your agent has nothing. Do you have customer results you could encode here?"
- "If you don't have proof points or references yet because you're early — that's fine, skip it. But if you have case studies sitting in a Google Doc that haven't made it into the library, that's a gap worth closing."
- **Never suggest generating fictional evidence.** If the user doesn't have real results, the answer is to skip evidence entities, not to fabricate them.

#### Freshness Checks (INFO)

- [ ] Entities updated within last 90 days (flag if older)
- [ ] Playbooks reviewed within last 60 days
- [ ] Competitor info updated within last 30 days (competitive intel goes stale fast)

#### Duplicate Detection (WARNING)

**Name Similarity:**
- [ ] Personas with similar names (>80% similarity)
- [ ] Products with similar names
- [ ] Use cases with similar names
- [ ] Segments with overlapping descriptions

**Content Overlap:**
- [ ] Personas with very similar pain points
- [ ] Use cases with near-identical descriptions
- [ ] Playbooks targeting same persona+segment combination

**Cross-Type Overlap:**
- [ ] Use cases that describe what an alternative already covers (e.g., a use case about "building internally" and an alternative about "build it ourselves")
- [ ] Alternatives that are hard to distinguish from each other (e.g., "DIY agents" vs "build your own context layer" — if a prospect wouldn't see these as different choices, they should be one entity)
- [ ] Buying triggers that overlap use cases (a trigger should describe the organizational moment, not re-describe the use case it activates)

#### Consistency Checks (WARNING)

**Messaging Alignment:**
- [ ] Product differentiators mentioned in related playbooks
- [ ] Persona pain points addressed in playbook value props
- [ ] Proof points support claims made in playbooks

**Taxonomy Health:**
- [ ] Segments have associated use cases
- [ ] Use cases link to products
- [ ] References link to products and use cases

### Step 4-C: Generate Cleanup Report

Present findings organized by severity. Language & Voice issues go with WARNINGS. Qualifying Questions issues get a dedicated section. Strategic Design Review findings get their own section with a conversational, thought-partner tone.

See [cleanup-report-template.md](references/cleanup-report-template.md) for the cleanup report template.

### Step 5-C: Interactive Fix Mode (--fix)

If `--fix` flag is provided, walk through each issue:

**For Critical and Warning issues:**
```
Issue 1 of 12: [INCOMPLETE] Persona "CTO" missing pain points
oId: pe_def456

Current state:
- Pain Points: (empty)
- Objectives: (empty)
- Description: "Chief Technology Officer..."

Options:
1. Tell me about this persona (I'll ask questions and help you write it)
2. Generate with AI (uses your library context)
3. Skip for now
4. Mark as intentional (won't flag in future)

Your choice:
```

**Prefer option 1 over option 2.** When the user chooses "Tell me about this persona," shift into challenge mode:
```
Let's flesh out this CTO persona. A few questions:

1. What's keeping this person up at night? Not generic CTO stuff —
   what specifically do YOUR CTOs worry about that leads them to you?
2. What are they trying to accomplish this quarter?
3. When they evaluate your product, what are they comparing it to?
   (Not just competitors — what's the alternative they'd choose instead?)
```

Then use their answers to draft content via `update_entity`.

**If user chooses "Generate with AI"**, that's fine — but flag that AI-generated content should be reviewed:
```
update_entity({
  entityType: "persona",
  oId: "pe_def456",
  instructions: "Add typical CTO pain points and objectives based on the existing library context."
})

NOTE: AI-generated content is a starting point. Review it to make sure
it reflects YOUR CTOs, not generic ones.
```

**For Language & Voice issues:**
These have specific, mechanical fixes. Offer:
```
Issue 5 of 12: [VOICE] "Build Your Pipeline" uses second-person while all other use cases use third-person
oId: uu_abc123

Options:
1. Fix now (shift to third-person to match other use cases)
2. Keep as-is (this is intentional)
3. Review the full text first
```

**For Qualifying Questions issues:**
```
Issue 8 of 12: [FLAT-WEIGHTS] All personas use MEDIUM weight on every question

This is better addressed with /octave:qual-doctor, which tests against
real prospects and tunes weights based on actual predictive power.

Options:
1. Run qual-doctor now (recommended — tests with real data)
2. Quick manual pass (I'll suggest weight changes based on question content)
3. Skip for now
```

If "Quick manual pass": Review each question and suggest weight adjustments based on how critical the signal seems. But note this is inferior to qual-doctor's test-based approach:
```
Persona: "VP of Sales"
  Q1 "Has a defined ICP?" — currently MEDIUM
     SUGGESTION: HIGH — this is a foundational signal
  Q2 "Is investing in AI tools?" — currently MEDIUM
     SUGGESTION: LOW — nice-to-know but not decisive
  Q3 "Has 5+ person sales team?" — currently MEDIUM
     SUGGESTION: HIGH — directly impacts product fit

Apply these suggestions? (These are heuristic-based — /octave:qual-doctor
would validate against real prospects.)
```

**For Design Review observations:**
These need human judgment, not mechanical fixes. Offer:
```
Design observation: Your segments don't appear to follow a shared taxonomy.

Options:
1. Discuss this (help me think through a structure)
2. This is intentional — skip
3. Flag for later
```

When the user chooses "Discuss this," shift into thought-partner mode — ask about their business model, how they sell, what makes their segments different, and help them reason toward a structure that fits. **Don't prescribe a specific taxonomy.** Challenge them to discover their own:

```
Let's think about your segments. Right now you have:
  - "Tech Companies"
  - "Series B Startups"
  - "Enterprise Financial Services"
  - "SMB SaaS"

These mix industry (tech, financial), stage (Series B), size (SMB, enterprise),
and business model (SaaS). That's not necessarily wrong, but let me push on it:

1. When you talk to a Series B tech company vs a Series B fintech company —
   does the conversation actually change?
2. If it doesn't, "industry" isn't a real axis for you — maybe stage/size is
   what actually matters.
3. If it does, what specifically changes? That tells us whether industry
   deserves to be a segment dimension.

What's your gut tell you?
```

### Step 6-C: Duplicate Resolution Flow

When duplicates are detected:

```
Potential Duplicates Detected
=============================

Group 1: Sales Leadership Personas
----------------------------------
A) "VP of Sales" (pe_111)
   Created: 2025-06-01
   Pain Points: 5 defined
   Used in: 3 playbooks

B) "Vice President of Sales" (pe_222)
   Created: 2025-08-15
   Pain Points: 2 defined
   Used in: 1 playbook

Similarity: 92% (based on name and content)

Options:
1. Merge B into A (keep A, archive B, update references)
2. Merge A into B (keep B, archive A, update references)
3. Keep both (they represent different personas)
4. Review side-by-side before deciding

Your choice:
```

**Note:** Actual merging requires manual updates in Octave UI or multiple API calls. The skill should:
1. Recommend which to keep
2. List what needs to be updated
3. Offer to archive the duplicate

## Health Score Calculation

```
Base Score: 100

Deductions:
- Critical issue: -15 points each (max -45)
- Warning: -5 points each (max -30)
- Language & Voice issue: -3 points each (max -15)
- Qualifying Question issue: -3 points each (max -15)
- Info: -1 point each (max -10)

Bonuses:
- All entity types have content: +5
- No stale content (>90 days): +5
- All playbooks fully linked: +5
- Clean language/voice (no issues found): +5
- Qualifying questions use varied weights: +5

Minimum score: 0
Maximum score: 100
```

**Note:** Design Review observations do NOT affect the health score. They are strategic prompts, not errors.

**Score Interpretation:**
- 90-100: Excellent - Library is well-maintained
- 70-89: Good - Minor issues to address
- 50-69: Fair - Several gaps need attention
- Below 50: Needs Work - Significant gaps affecting effectiveness

## MCP Tools Used

### Read Operations
- `list_all_entities` - Get all entities of each type (quick scan)
- `get_entity` - Get full details for specific entities (qualifying questions, full field data)
- `get_playbook` - Get playbook with linked personas and value props
- `list_value_props` - Check value prop coverage

### Write Operations (--fix mode only)
- `update_entity` - Fix incomplete entities or language issues
- `create_entity` - Create missing entities (onboarding mode)
- `add_value_props` - Add missing value props

## Examples

### Basic Audit
```
/octave:audit
```
Runs full audit — asks if you're onboarding or cleaning up, then proceeds accordingly.

### Focused Audit
```
/octave:audit --type personas
```
Audits only personas (completeness, duplicates, staleness, role relevance, qualifying question weights).

### Interactive Fix
```
/octave:audit --fix
```
Runs audit then walks through each issue for resolution. In onboarding mode, also offers to walk through design challenges interactively.

## Error Handling

**Empty Library:**
> Your library is empty — looks like we're starting fresh. Let me walk you through what to build first.
> (Automatically enters onboarding mode)

**API Error:**
> Could not fetch library data. Check your connection and try again.
> If the issue persists, verify your workspace with /octave:workspace.

## Related Skills

- `/octave:library` - Browse and manage individual entities
- `/octave:qual-doctor` - Deep-dive qualification scoring tuner (test against real prospects, tune weights)
- `/octave:brainstorm` - Generate ideas to fill gaps
- `/octave:icp-refine` - Refine ICP definitions from deal data
- `/octave:enablement` - Generate enablement content from library