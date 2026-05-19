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
/octave:audit [--type <entity-type>] [--fix] [--migrate]
```

## Options

- `--type <type>` - Focus on specific entity type (personas, products, segments, motions, etc.)
- `--fix` - Interactive mode to address issues as they're found
- `--detailed` - Show full details for each issue (default: summary view)
- `--migrate` - Legacy playbook → Motions migration mode

## Instructions

When the user runs `/octave:audit`:

### Step 1: Gather Library State

**Resolve Octave MCP server first:** The Octave MCP server provides tools like `verify_connection`, `get_entity`, `list_all_entities`. From your tool list, get the server name (e.g. `octave-acme`).

**Fetch entities using MCP tools:**

```
1. list_all_entities({ entityType: "persona" })
2. list_all_entities({ entityType: "product" })
3. list_all_entities({ entityType: "segment" })
4. list_all_entities({ entityType: "use_case" })
5. list_all_entities({ entityType: "competitor" })
6. list_all_entities({ entityType: "alternative" })
7. list_all_entities({ entityType: "buying_trigger" })
8. list_all_entities({ entityType: "proof_point" })
9. list_all_entities({ entityType: "reference" })
10. list_all_entities({ entityType: "playbook" }) — legacy standalone playbooks, if any remain
11. list_motions() — all Motions in workspace
12. For each Motion: list_motion_icps({ motionOId }) — Motion ICP cell state
```

Then use `get_entity` for entities that need deeper inspection (qualifying questions, field completeness), and `find_motion_icp({ motionIcpOId, includeLearnings: true })` for any specific Motion ICP cell you need full narrative context on.

If `--type` is specified, only fetch that type (but still need related types for relationship checks).

### Step 2: Determine Mode

After gathering the library state, ask the user:

```
I can see your library has [X] total active entities across [Y] types,
[Z] Motions, and [W] legacy standalone playbooks.

How would you like to approach this?

1. Onboarding review — I'm building this library out. Help me figure out
   what to build next and how to design it for the Motions world.

2. Cleanup audit — This library has been around. Find what's broken,
   redundant, stale, or poorly written. Check my Motions setup too.

3. Legacy playbook → Motions migration — I have old-style playbooks. Help
   me translate my setup to the new world and re-wire my agents.
```

**Auto-detect hints:**
- <10 entities, missing products/personas → default-suggest onboarding
- Legacy playbooks exist but zero Motions → default-suggest migration
- Motions exist, 30+ entities → default-suggest cleanup

Present all three options regardless.

---

## ONBOARDING MODE

When the user selects onboarding, the audit shifts from "what's wrong" to "what to build next and how to design it well." The tone is forward-looking — a strategic planning partner who challenges the user to think critically, not a template filler.

**CRITICAL PRINCIPLE:** The audit should NEVER auto-generate entity content in onboarding mode without the user's input. Its job is to push the user to think, not to think for them. The user knows their business — the audit's job is to ask the questions that draw out the right design.

### Step 3-O: Assess What Exists

Summarize the current state in plain language:

```
Here's what you have so far:

Foundation:
  Offerings: [list — Product / Service / Solution]
  Personas: [count] — [list names]
  Segments: [count] — [list names]

Execution:
  Motions: [count] — [list names + type (e.g. NET_NEW, UPSELL)]
  Use Cases: [count]

Depth:
  Competitors: [count]
  Alternatives: [count]
  Buying Triggers: [count]
  Objections: [count]

Evidence:
  Proof Points: [count]
  References: [count]

Legacy:
  Standalone Playbooks: [count] (deprecated — superseded by Motions)
```

### Step 4-O: Build Priority Roadmap

Based on what exists, generate a prioritized build roadmap. The tiers represent dependency order — later tiers build on earlier ones.

**Tier 1 — Foundation (build first):**
These are the inputs everything else depends on. Agents can't do useful work without them.
- An Offering (Product, Service, or Solution — the thing you sell)
- Core personas (the people who discover, evaluate, and champion — not everyone who touches a deal)
- Core segments (the company types where your offering fits differently)

**Tier 2 — Execution (build once foundation exists):**
This is where the library becomes actionable for agents.
- **Link entities to offerings first.** The Motion matrix is built from the personas and segments linked to the offering in your Library (`link_entities_to_offering`). If a persona or segment isn't linked to the offering, it won't appear in the Motion matrix at all. Multiple offerings can share some entities — that's fine. The check is: for each offering, are the relevant personas and segments linked?
- **Motions** — one per offering + motion type combo. Motion types include `NET_NEW`, `UPSELL`, `CROSS_SELL`, `CONVERT_FREE_TO_PAID`, `RENEW_AND_RETAIN`, `DISPLACE_INCUMBENT`. Creating a Motion auto-generates a **Default Motion Playbook** (narrative type `DEFAULT`) covering the full persona × segment matrix. Each cell — a Motion ICP — contains a structured narrative: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References.
- **Custom Motion Playbooks** are additional lenses layered on top of the default. Only create these when you have a specific angle. The four user-creatable narrative types are `THEMATIC`, `MILESTONE`, `ACCOUNT`, and `COMPETITIVE` — they correspond to WHY you'd approach someone differently (campaign theme, trigger event, named account, competitive displacement). Each custom Motion Playbook targets a specific slice of the grid (you choose scope at creation).
- Use cases describing customer outcomes (not internal processes)

**Tier 3 — Depth (makes agents sharper):**
These enrich agent output with competitive awareness, urgency, and situational intelligence.
- Competitors (named rivals agents will encounter in deals)
- Alternatives (behavioral patterns — what teams do instead of buying, like building internally or using general AI)
- Buying triggers (organizational moments that create urgency — new hire, funding, key departure)
- Objections (recurring concerns to pre-handle — distinct from competitors and alternatives)

**Tier 4 — Evidence (makes agents credible):**
Agents can sell without these, but they sell better with them. **IMPORTANT: Never fabricate evidence entities.** Proof points and references must come from real customer outcomes.
- Proof points (pattern-based results agents can reference — the user needs to provide real examples)
- References (customer stories with enough context to tell a 2-sentence narrative — requires real customer data)

**Tier 5 — Activation (after library + Motions are set up):**
The final layer that connects the library to live agent execution.
- **Agent connection** — agents configure in layers: select offering → select motion type → that narrows to available Motions → if multiple Motion Playbooks exist within a Motion, choose selection mode. The motion type selection separates Net New, Upsell, Cross Sell, etc. agent configurations.
- **Learning Loop configuration** — enabled by default on Motions, worth confirming. CRM + call recorder integration enables narrative refinement over time. Motion ICP learning types: `KEY_LANGUAGE`, `INDUSTRY_TREND`, `PAIN_POINT`, `VALUE_PROP`, `OBJECTION`. **Auto-update caveat:** if auto-update is ON, the system periodically refreshes cell narratives based on engagement data. Manually refined cells may be overwritten. Users can turn auto-update OFF for cells they've hand-tuned.

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
- "Are any of your personas 'nice to have' rather than 'need to have'? A persona nobody targets is dead weight."
- "Your personas become rows in the Motion matrix. Every persona you create gets a tailored narrative for every segment your offering is linked to. That's powerful — but it also means a persona that doesn't meaningfully differentiate is an entire row of wasted nuance."

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
- "Your segments become columns in the Motion matrix. Every segment gets a tailored narrative for every persona. If two segments would produce near-identical narratives, they should probably be one segment."
- "Segments and personas together drive the Motion ICP matrix. Getting them right is the highest-leverage design decision in the library."

**MOTION ARCHITECTURE CHALLENGE:**
- "How many offerings do you have? Each offering gets its own Motion(s). One product = typically one `NET_NEW` Motion. If you also upsell, that's a second Motion (type `UPSELL`) for the same offering. Cross-sell, free-to-paid conversion, renewal — each gets its own Motion."
- "Start with the Default Motion Playbook. It covers every cell in your matrix. Don't create custom Motion Playbooks until you've lived with the default and seen what actually needs a different angle."
- "Custom Motion Playbooks aren't replacements for the default — they're additional lenses. Think of them as campaign-specific or situation-specific overlays on the base coverage."
- "The four user-creatable narrative types are `THEMATIC`, `MILESTONE`, `ACCOUNT`, `COMPETITIVE`. A funding round (Milestone) changes the conversation. Displacing a competitor (Competitive) changes the framing. A market trend (Thematic) changes the urgency. A named account (Account) changes the depth."

**USE CASE CHALLENGE:**
- "Name use cases as outcomes, not processes. 'Compress territory planning' sells. 'Technical onboarding flow' doesn't. Agents use these to explain what your product does for people — frame them from the customer's perspective."
- "Keep names short — under ~8 words. The description carries the detail. Names are labels, not summaries."
- "Think about the customer lifecycle: do your use cases only cover the 'doing' phase, or do they span from 'figuring out what to do' through 'doing it' to 'learning from what happened'? Most libraries over-index on execution use cases and miss the strategic layer."

**COMPETITOR & ALTERNATIVE CHALLENGE:**
- "Competitors are named rivals. But who do you ACTUALLY lose to most often? Is it a named company, or is it inertia — the prospect deciding to do nothing, build it themselves, or cobble something together?"
- "Alternatives are the real competition for most companies. What do your prospects do TODAY instead of buying your product? That behavioral pattern is what your agents need to address."
- "For competitors: don't list every company in your space. List the ones your reps actually encounter in deals. If you've never lost a deal to Competitor X, they don't belong in your library."

**OBJECTION CHALLENGE:**
- "Objections are the recurring concerns prospects raise — distinct from competitors (vendor X) and alternatives (status-quo path). What pushback shows up in calls and emails over and over?"
- "Each Objection should have: the underlying concern, the assumptions and misconceptions behind it, the areas to probe, and a reframe / response. Agents can pre-handle objections in outbound and call prep when these are populated."
- "Objection-typed learnings on Motion ICPs feed back into Objection refinement — your Objections get sharper as you accumulate evidence."

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
- Offering name leakage in use cases/alternatives
- Duplicate detection (catch overlaps before building more)
- **Qualifying question weight audit** (see Qualifying Questions Audit section — catch all-MEDIUM patterns early)

Skip freshness checks (everything is new) and skip the full strategic design review (they're still building).

### Step 7-O: Generate Onboarding Report

```
Library Onboarding Report
=========================
Generated: <timestamp>
MCP Server: <mcpServerName>

Current State
-------------
Total Active Entities: <count>
  - Offerings: X (Products: X / Services: X / Solutions: X)
  - Personas: X
  - Segments: X
  - Use Cases: X
  - Competitors: X
  - Alternatives: X
  - Buying Triggers: X
  - Objections: X
  - Proof Points: X
  - References: X

Motions: X
  - [Motion name] ([type]) — [offering]

Legacy Standalone Playbooks: X (deprecated)

Readiness: <tier label>
  Tier 1 (Foundation):  <complete / partial / not started>
  Tier 2 (Execution):   <complete / partial / not started>
  Tier 3 (Depth):       <complete / partial / not started>
  Tier 4 (Evidence):    <complete / partial / not started>
  Tier 5 (Activation): <complete / partial / not started>

---

BUILD NEXT
==========

Your agents need [specific thing] to [specific capability].

Priority 1: [what to build]
  Why: [what agents can't do without it]

Priority 2: [what to build]
  Why: [what agents can't do without it]

Priority 3: [what to build]
  ...

---

DESIGN CHALLENGES
=================
[Challenge questions from Step 5-O, tailored to what the user is about to build.
These are questions for the user to answer, NOT prescriptive templates.]

Segments:
  Your [current segments] suggest [observation].
  CHALLENGE: [Specific question about their business that would
  sharpen their segment design]

Personas:
  CHALLENGE: [Question that pushes them to justify their persona choices]

Motions:
  CHALLENGE: [Question about offering coverage and Motion architecture]

...

---

QUALIFYING QUESTIONS
====================
[Weight distribution analysis from the qual questions audit check]
[If all-MEDIUM, flag it and recommend running /octave:qual-doctor]

---

EARLY ISSUES (X)
=================
[Light cleanup findings from Step 6-O on existing content]

1. [INCOMPLETE] Persona "CTO" is a stub — only has name and one-line description
   Fix: Flesh out pain points, objectives, and responsibilities

2. [VOICE] Offering description uses "you/your" while personas use "they/their"
   Fix: Align to one voice before building more entities

---

Recommendations
===============

1. NEXT SESSION: Build [Tier X items] — but think through the design
   challenges above first
2. BEFORE BUILDING MORE: Fix [early issues] so new entities match
3. DESIGN DECISION: [Most important challenge question from above]

Run /octave:audit --fix to address early issues interactively.
Run /octave:qual-doctor to tune qualifying question weights and scoring.
```

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

For Motions:
```
Let's set up your first Motion.

1. How many offerings do you sell (Products, Services, Solutions)?
   Each one gets its own Motion(s).
2. Which motion type are you starting with? `NET_NEW` is the most common;
   `UPSELL`, `CROSS_SELL`, `CONVERT_FREE_TO_PAID`, `RENEW_AND_RETAIN`,
   and `DISPLACE_INCUMBENT` are also options. Each generates fundamentally
   different narratives at every cell.
3. Before creating the Motion: are your personas and segments linked to
   the offering? The matrix is built from what's linked — unlinked
   entities won't appear. Check link_entities_to_offering.
4. Once we create the Motion, the matrix auto-generates: every persona
   gets a tailored narrative for every segment. Each Motion ICP cell has
   structured sections — Target ICP overview, Operating landscape,
   Strategic narrative, Pains and consequences, Benefits and impacts,
   Methodology, References.

Don't worry about custom Motion Playbooks yet. Live with the Default
for a while — you'll know when a specific angle needs its own lens.
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
- [ ] At least 1 offering (Product, Service, or Solution) defined
- [ ] At least 1 persona defined
- [ ] At least 1 Motion created per active offering (table stakes in the new world)
- [ ] Each Motion has a Default Motion Playbook (auto-created, but worth confirming)

**Offering Linkage:**
- [ ] For each offering with a Motion, check which personas and segments are linked vs unlinked. Cross-reference: if a persona is unlinked from Offering A, check whether it's linked to another offering (B, C, etc.). If it IS linked elsewhere, that's fine — it just doesn't buy this product. If it's NOT linked to ANY offering, that's likely an error — a persona sitting in the library with no offering connection won't appear in any Motion matrix.
- [ ] Same check for segments: unlinked from this offering but linked to another = intentional. Unlinked from everything = probably missed.
- [ ] Flag orphaned entities: "You have 3 personas not linked to any offering: [names]. They won't appear in any Motion matrix. Are these stale entities, or did they just never get connected?"
- [ ] Flag potential gaps per offering: "Your Motion for [offering] has X personas in its matrix, but your library has Y total. The missing ones are linked to other offerings — confirm that's intentional and none were accidentally left off."

**Broken References:**
- [ ] Personas referenced in Motions exist
- [ ] Offerings referenced in Motions exist
- [ ] Use cases referenced exist

**Library Shape — Contextual Proportions:**

Don't enforce minimum counts. Instead, look at the library as a whole and surface imbalances that reveal what agents can and can't do. The right number of any entity type depends on the company — 2 competitors might be exactly right for a niche market, or dangerously thin for a crowded space. Think about the company and whether the proportions make sense.

Examples of observations to surface:
- "You have 9 personas targeting different buyers but only 2 segments. That means your agents differentiate by role but not by company type or stage — every persona gets the same pitch regardless of who they work for. Is that intentional?"
- "You have 20 use cases but 0 buying triggers. Your agents can explain what you do but can't recognize the moments that create urgency to buy."
- "You have 8 competitors but 0 alternatives. Your agents can handle named competitive situations but can't address the behavioral alternatives — like teams building internally or using general LLMs — that often represent the real competition."
- "You have 15 personas and 12 segments but only 1 Motion. All of that targeting intelligence feeds into a single matrix — is this one offering, or should some of these persona/segment combinations live in a second Motion?"

The goal is to tell a story about what the library's shape means for agent capability, not to hit a minimum count.

#### Completeness Checks (WARNING)

**Personas:**
- [ ] Has pain points defined (not empty)
- [ ] Has key objectives defined
- [ ] Has primary responsibilities defined
- [ ] Has description (>50 chars)

**Offerings (Product / Service / Solution):**
- [ ] Has description
- [ ] **Product:** has key capabilities + differentiators
- [ ] **Service:** has deliverables + competencies + comparative advantage
- [ ] **Solution:** has distinct capabilities + key components + differentiated value

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

**Objections:**
- [ ] Has underlying concern defined
- [ ] Has assumptions and misconceptions
- [ ] Has areas to probe and clarify
- [ ] Has reframe and response

**Proof Points:**
- [ ] Has quantified metric/statistic
- [ ] Has source/validation

**References:**
- [ ] Has success metrics
- [ ] Has use case context

#### Motions Readiness (CRITICAL)

- [ ] At least 1 Motion created per active offering
- [ ] Each Motion has a Default Motion Playbook (auto-created, but confirm)

#### Motion Playbook Review (INFO)

- If they have a large number of custom Motion Playbooks: flag and challenge — "You have 15 custom Motion Playbooks on this Motion. Do you need that many, or are some redundant?"
- If they have zero custom Motion Playbooks: not an error, but surface ideas — "You're running on defaults only. That's fine for broad coverage. When you're ready, here are common patterns: `COMPETITIVE` for your top rival, `MILESTONE` for funding/hiring triggers, `ACCOUNT` for your top targets, `THEMATIC` for campaigns."
- Motion Playbook narrative-type mix — observe and note (`THEMATIC`, `MILESTONE`, `ACCOUNT`, `COMPETITIVE`)

#### Legacy Playbook Awareness (INFO)

- Old standalone playbooks are deprecated but still functional via the legacy `/api/v2/playbook/*` endpoints — they continue to work with agents currently referencing them
- You can't create new standalone playbooks via the Octave plugin — new strategic work happens in Motions
- Not a "problem" to fix — but if they haven't started with Motions at all, surface the opportunity: "You have X standalone playbooks but no Motions yet. Motions are the path forward — consider running `/octave:audit --migrate` to translate your setup."
- If agents are still pointing at old playbooks when Motions cover the same offering, flag as suggestion

#### Learning Loop (INFO)

- Check if learning is enabled on Motions (should be default, worth confirming)
- Note auto-update setting
- Motion ICP learning types observed: `KEY_LANGUAGE`, `INDUSTRY_TREND`, `PAIN_POINT`, `VALUE_PROP`, `OBJECTION` — flag if all learnings are AI_GENERATED with low confidence and zero user-defined pins (signals nobody is curating)

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

**Offering name in wrong entity types:**
- [ ] Check if the offering name appears in use case, alternative, or buying trigger descriptions. Use cases describe what happens for the customer. Alternatives describe what teams do instead. Buying triggers describe organizational moments. None of these should name the offering as the solution — that's what the offering entity and Motions are for. When agents pull from a use case that says "Acme solves this," the output sounds like a brochure instead of a conversation.

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

**Objection vs Competitor vs Alternative confusion:**
Spot-check whether the user has correctly distinguished the three. Objections are recurring concerns (e.g. "we're not ready yet"). Competitors are vendors in the deal (e.g. "Salesforce"). Alternatives are behavioral patterns (e.g. "teams build it internally"). Flag entries that look mis-categorized.

**Content as operating context vs sales copy:**
Flag descriptions that read like pitch copy rather than operating context: opening with imperatives ("Stop wasting time on...!"), rhetorical questions ("Imagine a world where..."), or heavy promotional framing. The library is consumed by AI agents — operating context that describes how the world works produces better agent output than pre-written sales language. Important caveat: precise sales terminology that describes real dynamics ("champion", "multithreading", "pipeline coverage") is fine. The flag is for tone and framing, not vocabulary.

**Evidence gap challenge:**
If the library has 0 proof points AND 0 references, don't just flag it as "missing." Challenge the user:
- "Your agents have no evidence to cite. When a prospect asks 'who else uses this?' or 'what results have you seen?' — your agent has nothing. Do you have customer results you could encode here?"
- "If you don't have proof points or references yet because you're early — that's fine, skip it. But if you have case studies sitting in a Google Doc that haven't made it into the library, that's a gap worth closing."
- **Never suggest generating fictional evidence.** If the user doesn't have real results, the answer is to skip evidence entities, not to fabricate them.

#### Freshness Checks (INFO)

- [ ] Entities updated within last 90 days (flag if older)
- [ ] Competitor info updated within last 30 days (competitive intel goes stale fast)

#### Duplicate Detection (WARNING)

**Name Similarity:**
- [ ] Personas with similar names (>80% similarity)
- [ ] Offerings with similar names
- [ ] Use cases with similar names
- [ ] Segments with overlapping descriptions

**Content Overlap:**
- [ ] Personas with very similar pain points
- [ ] Use cases with near-identical descriptions

**Cross-Type Overlap:**
- [ ] Use cases that describe what an alternative already covers (e.g., a use case about "building internally" and an alternative about "build it ourselves")
- [ ] Alternatives that are hard to distinguish from each other (e.g., "DIY agents" vs "build your own context layer" — if a prospect wouldn't see these as different choices, they should be one entity)
- [ ] Buying triggers that overlap use cases (a trigger should describe the organizational moment, not re-describe the use case it activates)
- [ ] Objections that re-state competitors or alternatives instead of capturing a distinct concern

#### Consistency Checks (WARNING)

**Messaging Alignment:**
- [ ] Offering differentiators reflected in related Motion ICP narratives (use `find_motion_icp` to spot-check)
- [ ] Persona pain points addressed in Motion ICP Pains and consequences sections
- [ ] Proof points support claims made in Motion ICP Benefits and impacts sections

**Taxonomy Health:**
- [ ] Segments have associated use cases
- [ ] Use cases link to offerings
- [ ] References link to offerings and use cases

### Step 4-C: Generate Cleanup Report

Present findings organized by severity. Language & Voice issues go with WARNINGS. Qualifying Questions issues get a dedicated section. Strategic Design Review findings get their own section with a conversational, thought-partner tone.

```
Library Audit Report
====================
Generated: <timestamp>
MCP Server: <mcpServerName>

Summary
-------
Total Entities: <count>
  - Personas: X
  - Offerings: X (Products / Services / Solutions)
  - Segments: X
  - Use Cases: X
  - Competitors: X
  - Alternatives: X
  - Buying Triggers: X
  - Objections: X
  - Proof Points: X
  - References: X

Health Score: X/100

Issues Found: X total
  - Critical: X
  - Warning: X
  - Info: X
  - Design observations: X

---

MOTIONS
=======
Motions: X total
  - [Motion name] (NET_NEW) — [offering]
  - [Motion name] (UPSELL) — [offering]

Motion Playbooks: X custom (+ X defaults)
  Types: THEMATIC: X, MILESTONE: X, ACCOUNT: X, COMPETITIVE: X

Legacy Playbooks: X still in workspace (deprecated)
  [If agents still wired to them, note which ones]

Learning Loop: [enabled/not configured] on X Motions

---

CRITICAL ISSUES (X)
===================

1. [ORPHAN] Motion "[name]" has no Default Motion Playbook
   Impact: No base narrative coverage for this offering
   Fix: Re-create the Motion or contact support

2. [MISSING] No Motions when offering exists
   Impact: Agents can't access the ICP matrix for this offering
   Fix: Create a Motion for [offering]

...

---

WARNINGS (X)
============

1. [INCOMPLETE] Persona "CTO" missing pain points
   oId: pe_def456
   Fields missing: painPoints, keyObjectives
   Fix: Add pain points and objectives

2. [DUPLICATE] Similar personas detected
   - "VP of Sales" (pe_111)
   - "Vice President of Sales" (pe_222)
   Similarity: 92%
   Fix: Consider merging these personas

3. [VOICE] Mixed perspectives in use cases
   - 8 use cases use third-person
   - 1 use case ("Build Your Pipeline") uses second-person "you/your"
   Impact: Agents produce inconsistent output
   Fix: Align to a consistent voice

4. [LANGUAGE] Capitalized coined term in "Data Integration Tools"
   Field: whereItBreaks #2 — "Rebuild Debt"
   Impact: Agents parrot this as a branded term prospects won't recognize
   Fix: Replace with descriptive language that carries equal specificity

5. [OFFERING-NAME] Offering name appears in use case
   "Deploy Strategy-Aware Agents" summary references "Acme" directly
   Impact: Agent output sounds like a brochure
   Fix: Describe the outcome without naming the offering

6. [STALE] Competitor "Acme Corp" not updated in 120 days
   oId: cp_xyz789
   Last updated: 2025-10-01
   Fix: Review and refresh competitive intelligence

7. [ORPHAN] Persona "Growth Marketer" not linked to any offering
   Impact: Won't appear in any Motion matrix
   Fix: Link to the relevant offering(s) via link_entities_to_offering, or archive

...

---

QUALIFYING QUESTIONS
====================
[Dedicated section for qual question analysis]

Weight Distribution:
  Personas (4 entities, 24 total questions):
    HIGH: 0 | MEDIUM: 24 | LOW: 0 | INSTANT_DISQUALIFIER: 0
    ISSUE: All MEDIUM — no weight differentiation

  Segments (4 entities, 16 total questions):
    HIGH: 0 | MEDIUM: 16 | LOW: 0 | INSTANT_DISQUALIFIER: 0
    ISSUE: All MEDIUM — no weight differentiation

  Offering (1 entity, 8 questions):
    HIGH: 3 | MEDIUM: 4 | LOW: 1 | INSTANT_DISQUALIFIER: 0
    OK — varied weights

FitType Balance:
  3 personas have NO BAD fit questions — can only score up, never down

Cross-Entity Differentiation:
  Persona questions are very similar across all 4 personas —
  agents may struggle to route to the right one

RECOMMENDATION: Run /octave:qual-doctor to tune weights with real
test cases. The audit can identify the pattern; qual-doctor can fix it.

---

DESIGN REVIEW
=============
These are observations, not errors. You know your business —
consider whether these reflect intentional choices or gaps worth addressing.

Library Shape:
  [Contextual observation about proportions]

Segment Design:
  [Challenge about whether the segment axis actually drives differentiation]

Use Case Lifecycle:
  [Observation about lifecycle coverage — execution only vs full span]

Persona Roles:
  [Question about whether personas represent deal drivers]

Evidence:
  [Challenge about proof points and references — push for real data]

Content Tone:
  [Flags for pitch copy vs operating context]

---

Recommendations
===============

1. IMMEDIATE: [Most critical fix]
2. HIGH: Tune qualifying question weights (/octave:qual-doctor)
3. HIGH: Address language/voice inconsistencies
4. MEDIUM: Review and merge duplicate entities
5. MEDIUM: Link orphaned entities to the right offerings
6. CONSIDER: Design review observations above
7. LOW: Refresh stale content

Run /octave:audit --fix to address issues interactively.
Run /octave:audit --migrate to translate legacy playbooks to Motions.
Run /octave:qual-doctor to tune qualification scoring.
```

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

**For Orphan entities:**
```
Issue 10 of 12: [ORPHAN] Persona "Growth Marketer" not linked to any offering

Options:
1. Link it to the relevant offering(s) — which ones apply?
2. Archive it (it's stale and not used)
3. Keep as-is (planning to use it soon)
```

If "Link it": ask which offerings apply, then call `link_entities_to_offering` with the persona oId and the offering(s).

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
   Used in: 3 Motion ICP cells

B) "Vice President of Sales" (pe_222)
   Created: 2025-08-15
   Pain Points: 2 defined
   Used in: 1 Motion ICP cell

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

---

## MIGRATION MODE

When the user selects migration (or uses `--migrate`), the audit reads the full current state — legacy playbooks and Motions alike — identifies the gap, and works interactively to translate the old setup into the new world.

**Auto-detect hint:** If the library has legacy playbooks but zero Motions, default-suggest migration.

Migration has two parts:
1. **Preserve and migrate your playbooks** — map legacy playbooks to the Motions world, carry over nuance
2. **Re-wire your agents** — update agent configurations from old playbook references to Motion references

### Step 1-M: Gather State

Add to existing library fetch:
```
11. list_motions() — all Motions in workspace
12. For each Motion: list_motion_icps({ motionOId }) — Motion ICP cell state
13. list_all_entities({ entityType: "playbook" }) — all standalone playbooks
14. get_playbook({ oId }) for each standalone playbook — linked personas, segments, value props, type
15. list_agents() — all saved agents with their configurations
```

### Step 2-M: Read & Categorize Old Playbooks

Categorize each standalone playbook against the Motion Playbook narrative types:
- **Sector-based** (linked to specific segments) → covered by Default Motion Playbook (segments are columns)
- **Persona-based** (linked to specific personas) → covered by Default Motion Playbook (personas are rows)
- **Sector × Persona combos** → covered by Default Motion Playbook (specific Motion ICP cells in the matrix)
- **Competitive** → Custom Motion Playbook with narrative type `COMPETITIVE`
- **Milestone / trigger-based** → Custom Motion Playbook with narrative type `MILESTONE`
- **Account-specific** → Custom Motion Playbook with narrative type `ACCOUNT`
- **Solution / general theme** → either covered by Default if the angle is broad enough, or a Custom Motion Playbook with narrative type `THEMATIC`

### Step 3-M: Present Current State

```
Here's your setup:

OLD WORLD (Standalone Playbooks):
  [X] playbooks:
  - [X] sector-based (targeting specific segments)
  - [X] persona-based (targeting specific personas)
  - [X] sector × persona combos
  - [X] competitive (vs [competitor names])
  - [X] milestone ([trigger names])
  - [X] solution/general

NEW WORLD (Motions):
  [What they've already created, or "No Motions yet"]

THE GAP:
  [What's covered only by legacy playbooks, what's already in Motions]
```

### Step 4-M: Playbook Migration — Default Motion Playbook

The bulk of migration. Most legacy playbooks (sector, persona, combos) are absorbed by the Default Motion Playbook.

Key coaching points:
- "Most of your playbooks are sector or persona combinations. All of that becomes one Default Motion Playbook per Motion. Every persona × segment intersection becomes a Motion ICP cell with its own tailored narrative."
- "The critical thing is making sure any nuance from your legacy playbooks — especially ones you've manually edited or refined — makes it into the Motion ICP narratives."
- **For each legacy playbook that maps to default:** compare its value props and key messaging to the corresponding Motion ICP narrative (use `find_motion_icp({ motionIcpOId, includeLearnings: true })`). Each cell has structured sections — Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References. Map old playbook value props to the right section. An old value prop about compliance probably belongs in Strategic narrative or Benefits and impacts. Surface anything the old playbook captured that the auto-generated narrative missed. Offer to edit the specific cell via `update_motion_playbook` to incorporate it.
- "If your 'Enterprise Sales' playbook had a specific value prop about compliance that your VP Sales × Enterprise cell doesn't mention — check the Strategic narrative and Benefits and impacts sections. That's where positioning and outcome claims live."
- **Auto-update caveat:** if Learning Loop is enabled with auto-update ON, manually edited cells may be refreshed in the next learning cycle. If the user is pulling critical nuance into cells, recommend turning auto-update OFF for those specific cells so the refinements persist. Otherwise the system may overwrite their work.

### Step 5-M: Playbook Migration — Custom Motion Playbooks

For playbooks with specific angles that don't collapse into the default:

**Competitive playbooks → Custom Motion Playbook (narrative type `COMPETITIVE`):**
- Walk through each: which grid coordinates should this target? Not all of them — where do you actually encounter this competitor?
- What's the displacement angle?
- Use `create_motion_playbook({ motionOId, narrativeType: "COMPETITIVE", ... })`

**Milestone playbooks → Custom Motion Playbook (narrative type `MILESTONE`):**
- What's the trigger event?
- Which segments/personas does this event actually change the conversation for?
- Use `create_motion_playbook({ motionOId, narrativeType: "MILESTONE", ... })`

**Account playbooks → Custom Motion Playbook (narrative type `ACCOUNT`):**
- Which named accounts?
- What grid slice?
- Use `create_motion_playbook({ motionOId, narrativeType: "ACCOUNT", ... })`

**Solution/general playbooks → evaluate:**
- Is this angle broad enough that the default covers it?
- Or is it a specific enough lens that it deserves a custom playbook with narrative type `THEMATIC`?

### Step 6-M: Agent Re-wiring

Pull all agents (`list_agents`) and analyze how they're configured:
- What playbooks are they referencing?
- What selection mode (Best Match / Best Of / Manual)?

**New agent config flow:** Agents configure in layers: offering (or auto-offering-select) → motion type (`NET_NEW`, `UPSELL`, `CROSS_SELL`, etc.) → that narrows to available Motions → if multiple Motion Playbooks exist, selection mode (auto / subset / fixed). The motion type selection is the new step — Net New, Upsell, Cross Sell agents are separated at the config level, not just by which playbooks they reference.

**Selection mode mapping (old → new):**
- Best Match → auto (agent picks the best Motion Playbook per target at runtime)
- Best Of → subset (you select which Motion Playbooks are eligible, agent picks among them)
- Manual → fixed (you link one specific Motion Playbook)

Map each to the Motions world:
- **Agents using sector/persona playbooks with Best Match** → set offering + motion type → Default Motion Playbook handles the rest. The matrix does the persona × segment matching automatically.
- **Agents using competitive/milestone playbooks** → set offering + motion type → narrow to the specific custom Motion Playbook (`COMPETITIVE` / `MILESTONE` / `ACCOUNT`) via fixed selection.
- **Agents using Best Of across mixed playbooks** → set offering + motion type → if multiple Motion Playbooks exist, use subset selection across the relevant ones.
- **Agents using Manual with a single playbook** → set offering + motion type → fixed selection on the corresponding Motion Playbook (or just the default).
- **Agents with no clear motion type distinction** → default to `NET_NEW` unless the agent is explicitly for expansion / upsell / cross-sell / renewal / displacement.

Present recommendations per agent:
```
AGENT RE-WIRING
===============

Agent: "Outbound SDR"
  Currently: Best Match across 6 playbooks (3 sector, 2 persona, 1 general)
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Default Playbook
  Why: The default covers all of this automatically. Every prospect
  gets matched to the right persona × segment Motion ICP. The motion type
  ensures narratives are calibrated for net-new acquisition.

Agent: "Competitive Takeout"
  Currently: Manual → "vs Salesforce" playbook
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Fixed → Custom Motion Playbook (COMPETITIVE) "vs Salesforce"
  Why: Same angle, same targeting, Motion-native. Motion type matters
  here — competitive displacement is usually a net-new play (or use
  DISPLACE_INCUMBENT if you're explicitly going after an incumbent).

Agent: "Expansion AE"
  Currently: Best Match across expansion playbooks
  Recommendation: Offering → [Offering] / Motion Type → UPSELL / Default Playbook
  Why: Upsell motion type generates fundamentally different narratives —
  different objections, different value framing, different buyer mindset.
  This wasn't possible before without building separate upsell playbooks.

Agent: "Enterprise AE Prep"
  Currently: Best Of → 3 enterprise playbooks
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Default Playbook
  Why: The matrix already differentiates by persona within Enterprise segment.
  If you need themed angles too, use subset selection across relevant Motion Playbooks.
```

### Step 7-M: Coverage Gain Summary

After mapping, show what they gain:
```
COVERAGE SUMMARY
================

Old world: X playbooks covered ~Y persona × segment × angle combos
New world: Default Motion Playbook covers Z base combos (every intersection
           in the matrix) + custom Motion Playbooks for COMPETITIVE /
           MILESTONE / ACCOUNT / THEMATIC angles

Coverage gains:
- [X] Motion ICP cells that no legacy playbook covered (persona × segment
  combos that fell through the cracks)
- Structured methodology, pains/benefits, and references in every cell
- Learning Loop refinement over time (KEY_LANGUAGE, INDUSTRY_TREND,
  PAIN_POINT, VALUE_PROP, OBJECTION learnings accumulate per cell)

Nuance preserved:
- [X] value props / angles from legacy playbooks verified in Motion ICPs
- [X] custom Motion Playbooks carrying competitive/milestone/account angles
```

### Step 8-M: Interactive Build (--fix)

In fix mode, walk through interactively:
1. For each legacy playbook mapped to default: pull the Motion ICP via `find_motion_icp`, compare to playbook value props, offer to edit the cell via `update_motion_playbook` if nuance is missing
2. For each competitive/milestone/account angle: co-create the custom Motion Playbook via `create_motion_playbook` (targeting, narrative type, optional additions)
3. For each agent: walk through the re-wiring recommendation, confirm or adjust

---

## Health Score Calculation

```
Base Score: 100

Deductions:
- Critical issue: -15 points each (max -45)
- Warning: -5 points each (max -30)
- Language & Voice issue: -3 points each (max -15)
- Qualifying Question issue: -3 points each (max -15)
- Info: -1 point each (max -10)
- No Motions when offering exists: -10
- Agents still on legacy playbooks when Motions cover same offering: -3 each (max -9)

Bonuses:
- All entity types have content: +5
- No stale content (>90 days): +5
- Clean language/voice (no issues found): +5
- Qualifying questions use varied weights: +5
- All offerings have Motions: +5
- Learning Loop enabled: +3
- No legacy playbook agent references remaining: +3

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
- `get_entity` - Get full details for specific entities (qualifying questions, field data, links)
- `get_playbook` - Get a legacy standalone playbook with its linked personas, segments, and value props (migration mode only)
- `list_value_props` - Read value props on a legacy playbook (migration mode only)

### Motions Operations
- `list_motions` - Get all Motions in workspace
- `get_motion` - Full details for a Motion
- `list_motion_icps` - List Motion ICP cells for a Motion (shows which persona × segment intersections have narratives)
- `find_motion_icp` - Get full cell narrative for a specific Motion ICP — structured sections (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus optional learnings and report context
- `list_motion_playbooks` - List Motion Playbooks (Default + Custom) under a Motion
- `get_motion_playbook` - Full details for one Motion Playbook

### Offering Linkage
- `link_entities_to_offering` - Link personas, segments, and other entities to an offering (determines what appears in the Motion matrix)

### Agent Operations (migration mode)
- `list_agents` - Get all saved agents with their configurations (offering, motion type, playbook/Motion references)

### Write Operations (--fix mode only)
- `update_entity` - Fix incomplete entities, language issues
- `create_entity` - Create missing entities (onboarding mode)
- `create_motion_playbook` - Create a Custom Motion Playbook (narrative type `THEMATIC`, `MILESTONE`, `ACCOUNT`, or `COMPETITIVE`) during migration
- `update_motion_playbook` - Edit Motion Playbook narrative sections to carry over nuance from a legacy playbook

## Examples

### Basic Audit
```
/octave:audit
```
Runs full audit — asks if you're onboarding, cleaning up, or migrating, then proceeds accordingly.

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

### Legacy Playbook Migration
```
/octave:audit --migrate
```
Reads legacy playbooks and existing Motions, categorizes playbooks, maps to new world, re-wires agents.

### Migration with Interactive Build
```
/octave:audit --migrate --fix
```
Same as migration, but walks through each step interactively — comparing legacy playbook nuance to Motion ICP cells, co-creating custom Motion Playbooks, and confirming agent re-wiring.

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
