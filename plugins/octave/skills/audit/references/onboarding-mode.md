# ONBOARDING MODE

When the user selects onboarding, the audit shifts from "what's wrong" to "what to build next and how to design it well." The tone is forward-looking — a strategic planning partner who challenges the user to think critically, not a template filler.

**CRITICAL PRINCIPLE:** The audit should NEVER auto-generate entity content in onboarding mode without the user's input. Its job is to push the user to think, not to think for them. The user knows their business — the audit's job is to ask the questions that draw out the right design.

## Step 3-O: Assess What Exists

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

## Step 4-O: Build Priority Roadmap

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

## Step 5-O: Design Challenge

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

## Step 6-O: Quick Check on What Exists

Even in onboarding mode, run a light version of the cleanup checks on whatever already exists:
- Completeness checks on existing entities (are they fleshed out or just stubs?)
- Language/voice consistency (catch issues early before they multiply)
- Offering name leakage in use cases/alternatives
- Duplicate detection (catch overlaps before building more)
- **Qualifying question weight audit** (see the Qualifying Questions Audit section in [cleanup-checks.md](cleanup-checks.md) — catch all-MEDIUM patterns early)

Skip freshness checks (everything is new) and skip the full strategic design review (they're still building).

## Step 7-O: Generate Onboarding Report

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

## Onboarding Fix Mode (--fix)

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
