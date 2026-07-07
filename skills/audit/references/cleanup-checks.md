# CLEANUP MODE — Audit Checks and Fix Flows

When the user selects cleanup, run the full audit below. This is the standard mode for established libraries. Report findings using the template in [cleanup-report-template.md](cleanup-report-template.md).

## Step 3-C: Run Audit Checks

Perform the following checks and categorize issues by severity:

### Coverage Checks (CRITICAL)

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

### Completeness Checks (WARNING)

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

### Motions Readiness (CRITICAL)

- [ ] At least 1 Motion created per active offering
- [ ] Each Motion has a Default Motion Playbook (auto-created, but confirm)

### Motion Playbook Review (INFO)

- If they have a large number of custom Motion Playbooks: flag and challenge — "You have 15 custom Motion Playbooks on this Motion. Do you need that many, or are some redundant?"
- If they have zero custom Motion Playbooks: not an error, but surface ideas — "You're running on defaults only. That's fine for broad coverage. When you're ready, here are common patterns: `COMPETITIVE` for your top rival, `MILESTONE` for funding/hiring triggers, `ACCOUNT` for your top targets, `THEMATIC` for campaigns."
- Motion Playbook narrative-type mix — observe and note (`THEMATIC`, `MILESTONE`, `ACCOUNT`, `COMPETITIVE`)

### Legacy Playbook Awareness (INFO)

- Old standalone playbooks are deprecated but still functional via the legacy `/api/v2/playbook/*` endpoints — they continue to work with agents currently referencing them
- You can't create new standalone playbooks via the Octave plugin — new strategic work happens in Motions
- Not a "problem" to fix — but if they haven't started with Motions at all, surface the opportunity: "You have X standalone playbooks but no Motions yet. Motions are the path forward — consider running `/octave:audit --migrate` to translate your setup."
- If agents are still pointing at old playbooks when Motions cover the same offering, flag as suggestion

### Learning Loop (INFO)

- Check if learning is enabled on Motions (should be default, worth confirming)
- Note auto-update setting
- Motion ICP learning types observed: `KEY_LANGUAGE`, `INDUSTRY_TREND`, `PAIN_POINT`, `VALUE_PROP`, `OBJECTION` — flag if all learnings are AI_GENERATED with low confidence and zero user-defined pins (signals nobody is curating)

### Qualifying Questions Audit (WARNING)

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

**IMPORTANT:** The audit identifies qualifying question issues. For actual tuning (testing against known-fit prospects, diagnosing specific scoring patterns, applying weight changes), always route to `/octave:qual-doctor`. The audit is the diagnostic scan; qual-doctor is the treatment.

### Language & Voice Checks (WARNING)

These checks catch issues that directly affect agent output quality. The library is consumed by AI agents, not humans — language problems here become language problems in every email, call prep, and qualification an agent produces.

**Voice consistency within entity types:**
- [ ] For each entity type with 3+ entities, check if descriptions use mixed perspectives (some second-person "you/your", some third-person "teams/they"). Flag the outliers. Inconsistent voice across entities of the same type produces inconsistent agent output.

**Capitalized coined terms:**
- [ ] Scan descriptions and data fields for capitalized multi-word phrases that aren't proper nouns, company names, or acronyms (e.g., "Rebuild Debt", "Hero Dependency"). Agents treat capitalized multi-word phrases as branded proper nouns and parrot them verbatim to prospects who have no context for the jargon.
- When fixing: **replace, don't flatten.** Removing a coined term and replacing it with a vague word ("the gap") loses the sharpness of the original. Replace with language that carries equal specificity. Example: "the Context Gap" → "the disconnect between what a team knows about its market and what its tools actually use" — not just "the gap."

**Verbose entity names:**
- [ ] Check use case and buying trigger names for unnecessary length. Names over ~8 words often repeat what the description already says. Short names ("Detect Messaging Drift") work better than verbose ones ("Detect Messaging Drift And Fix It Before It Damages Pipeline") because agents use names as labels, not summaries.

**Offering name in wrong entity types:**
- [ ] Check if the offering name appears in use case, alternative, or buying trigger descriptions. Use cases describe what happens for the customer. Alternatives describe what teams do instead. Buying triggers describe organizational moments. None of these should name the offering as the solution — that's what the offering entity and Motions are for. When agents pull from a use case that says "the offering solves this," the output sounds like a brochure instead of a conversation.

### Strategic Design Review (INFO)

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
Check if proof point descriptions or talk tracks reference specific customer names. Proof points that name a customer can only be used with permission. Pattern-based proof points ("teams of one deliver full-team output") can be applied to any conversation. Flag customer-specific proof points and ask whether agents have permission to use those names.

**Alternative behavioral framing:**
Check if alternatives describe behavioral patterns (what teams do instead of buying) vs just naming a tool or category. Good alternatives paint a picture of the prospect's current world and where it breaks down. A vendor name alone as an alternative tells agents nothing. "Teams wire up CRM automations and rely on admins to maintain field logic" tells agents what the prospect's reality looks like and where to probe.

**Buying trigger narrative depth:**
Beyond the completeness check (are the fields populated?), evaluate whether triggers describe real organizational moments with enough narrative that an agent can recognize the situation AND have something useful to say. A thin trigger is worse than no trigger because the agent thinks it has context when it doesn't.

**Objection vs Competitor vs Alternative confusion:**
Spot-check whether the user has correctly distinguished the three. Objections are recurring concerns (e.g. "we're not ready yet"). Competitors are vendors in the deal. Alternatives are behavioral patterns (e.g. "teams build it internally"). Flag entries that look mis-categorized.

**Content as operating context vs sales copy:**
Flag descriptions that read like pitch copy rather than operating context: opening with imperatives ("Stop wasting time on...!"), rhetorical questions ("Imagine a world where..."), or heavy promotional framing. The library is consumed by AI agents — operating context that describes how the world works produces better agent output than pre-written sales language. Important caveat: precise sales terminology that describes real dynamics ("champion", "multithreading", "pipeline coverage") is fine. The flag is for tone and framing, not vocabulary.

**Evidence gap challenge:**
If the library has 0 proof points AND 0 references, don't just flag it as "missing." Challenge the user:
- "Your agents have no evidence to cite. When a prospect asks 'who else uses this?' or 'what results have you seen?' — your agent has nothing. Do you have customer results you could encode here?"
- "If you don't have proof points or references yet because you're early — that's fine, skip it. But if you have case studies sitting in a doc that haven't made it into the library, that's a gap worth closing."
- **Never suggest generating fictional evidence.** If the user doesn't have real results, the answer is to skip evidence entities, not to fabricate them.

### Freshness Checks (INFO)

- [ ] Entities updated within last 90 days (flag if older)
- [ ] Competitor info updated within last 30 days (competitive intel goes stale fast)
- [ ] Use `list_revisions({ startDate, entityTypes })` to see what's actually been edited recently — an entity with an old `updatedAt` but no revision activity is genuinely stale; one with recent revisions is being actively maintained. Use `get_revision({ revisionOId, diffOnly: true })` to inspect a specific change if a revision looks suspicious (e.g. a competitor's strengths were silently rewritten).

### Duplicate Detection (WARNING)

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

### Consistency Checks (WARNING)

**Messaging Alignment:**
- [ ] Offering differentiators reflected in related Motion ICP narratives (use `find_motion_icp` to spot-check)
- [ ] Persona pain points addressed in Motion ICP Pains and consequences sections
- [ ] Proof points support claims made in Motion ICP Benefits and impacts sections

**Taxonomy Health:**
- [ ] Segments have associated use cases
- [ ] Use cases link to offerings
- [ ] References link to offerings and use cases

---

## Step 5-C: Interactive Fix Mode (--fix)

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

Weight tuning needs testing against real prospects — that's what
/octave:qual-doctor does. It diagnoses per-question scoring patterns
and validates changes before applying them.

Options:
1. Run /octave:qual-doctor now (recommended)
2. Skip for now
```

Do not offer heuristic weight changes here — tuning without test data is guesswork, and `/octave:qual-doctor` exists precisely to do it properly.

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

## Step 6-C: Duplicate Resolution Flow

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
