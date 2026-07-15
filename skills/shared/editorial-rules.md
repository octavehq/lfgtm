# Editorial Rules: Octave Content

Universal language, presentation, and writing quality rules for all Octave-generated content. These rules apply regardless of document type: Beats reports, battlecards, one-pagers, microsites, briefs.

## Presentation Principles

1. **Never reference the library, source of truth, or Octave internals.** No "the library says X," "what the library doesn't capture," "no objection entities exist," or "findings analyzed." The reader sees market intelligence, not a database audit.

1a. **No internal tool terminology in output.** No function or tool names (`enrich_company`, `list_events`), version numbers, stream identifiers, or tool inventories ("Sources: Octave enrichment"). It reads as if a human analyst wrote it, not a system logging its own calls.

2. **No insight-type badges or tags.** The reader doesn't care whether something is a "Gap" or "Competitive Reframe." Those categories guide internal processes, not the reading experience.

3. **Don't surface internal maintenance as insights.** "Zero objection entities" is an internal action item, not executive intelligence. Frame operational findings as market behavior.

4. **Don't surface standard deal Q&A as insights.** If every company asks about enterprise readiness or SCIM support, that's table stakes, not a strategic finding. Only include if the pattern reveals something genuinely surprising.

5. **Frame as market intelligence, not tool output.** "Prospects are doing X" not "Findings show X." "Conversations reveal Y" not "The field data indicates Y." Never "24 findings analyzed" or "insights surfaced from workspace data." The reader should feel like they're getting a market brief from a sharp analyst, not a report from a software tool.

   Common violations and fixes:

   | Wrong | Right |
   |---|---|
   | "24 findings were analyzed across 12 conversations" | "Across a dozen recent conversations, three patterns stand out" |
   | "The library contains 4 proof points for this segment" | "Four customer stories match this profile" |
   | "No objection entities exist for this persona" | (Omit the section, or) "No recurring objections have been documented for this profile yet" |
   | "The Motion ICP cell narrative suggests..." | "For VP Engineering at mid-market companies, the positioning angle is..." |
   | "Learning Loop data shows 'compliance burden' has high confidence" | "Prospects in this segment consistently use the phrase 'compliance burden' when describing their pain" |

5b. **Weave enrichment data, don't echo it.** When using personalized data from enrichment or research (deal range, strategy type, market names, portfolio size, investment criteria), integrate it naturally into sentences that build the argument. Never drop enrichment data as raw fragments, standalone tags, or jargon the reader lacks context for. If a data point from enrichment would make the reader ask "where did that come from?" or "why is that here?", it needs more narrative context or should be cut.

## Language Rules

6. **No em-dashes.** Use colons, commas, periods, or en-dashes instead. Throughout every section, no exceptions.

7. **Implications must be actionable and specific.** Every recommendation or "what to do about it" callout must focus on messaging, positioning, enablement, or materials the team can change. Not generic advice ("follow up faster," "build relationships," "have more conversations"). The reader should finish thinking "we should update X" or "we need to build Y," not "we should try harder."

8. **Headlines state the finding, not the topic.** "AI agent identity crossed from curiosity to buying criteria in 8 weeks" is correct. "Update on AI agent identity" is wrong. Every headline is a claim the reader can agree or disagree with, never a label. This applies equally to chart titles and stat labels: "Competitor X appears in 1 of 3 calls" not "Competitor Mentions."

   **Conclusion-carrying, not theatrical.** A finding-stating header still fails if it reaches for drama, suspense, or urgency instead of just stating the conclusion. Watch the whole header stack, eyebrow + heading + lead together: a plausible-sounding claim can pass a "states a finding" check while the stack as a whole reads like a movie trailer. Worked example, a coaching doc's risk section that was wrongly approved: eyebrow "WHERE YOU'RE EXPOSED" + heading "The two things that stall this deal" + lead "Both are already live in the account. Have the counter ready before the next call." The heading is technically a claim, but "exposed", the ominous "the two things that stall this deal", and the command "have the counter ready" are theatrics. Fixed: eyebrow "TOP RISKS" + heading "The risks in play here, and the counter for each" + lead that names them plainly. Test: read the eyebrow, heading, and lead aloud as one unit. If it sounds like it wants a drumroll, or issues a command, or teases rather than tells, rewrite it to plainly state the conclusion.

9. **No redundant content across sections.** If one section covers a finding, don't repeat it elsewhere. Each section earns its space independently.

10. **Order by importance within every section.** Most impactful item first. Never chronological or alphabetical.

11. **Cut rather than expand.** When the output feels long, the answer is fewer items with sharper content, not more sections. Restraint is the product. A tight bulleted list often hits harder than explanatory prose. Leave room for the unsaid.

12. **State a distinctive concept once, then reference implicitly.** When an account has a defining characteristic (e.g., "1099 independent-contractor model"), name it with context in the Snapshot or first mention, then use plain language thereafter ("independent agents," "their agents," "the autonomy model"). Repeating the same phrase 10+ times across sections signals the model is pattern-matching, not thinking. The reader understood it the first time.

13. **Every item must serve its container's purpose.** A persona card exists to brief the seller on that person. Use cases, product features, and messaging belong in the messaging or strategy sections, not stuffed into a persona card. If content is relevant to the deal but doesn't serve the section it's in, move it or cut it. Redundancy and misplacement are separate violations, but they often appear together.

14. **Mark speculation as speculation, everywhere.** Never state inference as fact. Write "Unknown, potential: Datadog," not "Likely: Datadog" or "Competition: Datadog," unless intel confirms it. This applies to every field that gets filled from inference, not just competitors: stakeholders, pains, budget, timeline. If it wasn't confirmed, the label has to say so.

## AI-ism Kill List

These patterns make content feel machine-generated instead of analyst-written.

### Tier 1 Banned Words: Replace on Sight

| Kill | Replace with |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, market |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| leverage (verb) | use |
| seamless / seamlessly | smooth, easy, without friction |
| cutting-edge | latest, newest, advanced |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| utilize | use |
| holistic / holistically | complete, full, whole |
| actionable | practical, useful, concrete |
| impactful | effective, significant |
| learnings | lessons, findings, takeaways |
| best practices | what works, proven methods |
| synergy / synergies | (describe the actual combined effect) |
| game-changer / game-changing | describe what changed and why |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| tapestry / realm / paradigm | (use plain language) |
| embark / beacon / testament to | (rewrite entirely) |
| at its core | (cut: just state the thing) |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| embrace (metaphor) | adopt, accept, use, switch to |

### Tier 2: Flag When 2+ Appear in the Same Block

These words are legitimate individually. Two or more in the same content block signal AI generation.

| Kill | Replace with |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| empower | enable, let, allow |
| streamline | simplify, speed up |
| resonate / resonates with | connect with, appeal to, matter to |
| facilitate / facilitates | enable, help, allow |
| nuanced | specific, subtle, detailed |
| crucial | important, key, necessary |
| ecosystem (metaphor) | system, community, network, market |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| poised (to) | ready, set, about to |

### Banned Structures

**How to scan:** Read every sentence pair. Test: does the first sentence exist only to set up a negation that the second sentence "corrects"? If yes, rewrite as a direct positive statement.

| Pattern | What it looks like | What to do instead |
|---|---|---|
| **Staccato flex** | Short declarative sentences stacked back-to-back to sound punchy. Reads like a manifesto. | Vary sentence length. Mix short with long. |
| **Negation as depth** | "X isn't just about Y, it's about Z." "It's more than just a tool." Setting something up to negate past it. | Say what it IS, not what it isn't. |
| **"Wrong question" pivot** | "That's the wrong question. The real question is..." Dismisses the premise to reframe. | Lead with the better framing directly. |
| **Gerund relay** | "Managing X means navigating Y." Two -ing verbs chained, says the same thing twice. | Pick one verb, make the point. |
| **"It's not X, it's Y"** | Fake-deep rhetorical correction that restates the same point with more drama. | Make a direct positive statement. |
| **Role recitation** | "As VP Sales at [Company], you..." Reading back someone's LinkedIn headline. | Show understanding of their world, not their title. |
| **Dramatic framing** | "What separates the winners from the losers." "The one thing every successful team does." Subtitles and intros that use rhetorical drama or mystery to create artificial suspense instead of stating content directly. | State what the content covers. "Patterns from 12 accounts" not "What separates the ones who get it from the ones who don't." |
| **Objection phrasing trap** | Putting words in the prospect's mouth: `"We already use Glean for this"`, a quote nobody said. | Describe the risk, don't quote the prospect: `They position this as overlap with existing enterprise search`. |

**Concrete examples** (these are the patterns that actually slip through):

| Violation | Fix |
|---|---|
| "This is not a competitive evaluation. It is a displacement sale where..." | "Every one of these deals is a displacement sale: the buyer already feels burned..." |
| "The positioning isn't X vs. Y. It's X layered on top." | "X layers on top, filling a hole Y acknowledged." |
| "The prospect's problem isn't convincing themselves. It's convincing their CFO." | "The real friction is the CFO approving a new line item." |
| "Prospects aren't evaluating. They're recovering." | "Prospects show up pre-burned, treating the first call as triage." |
| "The objection isn't price. It's the absence of a budget line." | "The real blocker is the absence of a budget line." |

The tell: any two-sentence pair where removing the first sentence loses nothing. If the negation adds no information, cut it and lead with the positive claim.

### Banned Tone Patterns

| Pattern | What it sounds like | What to do instead |
|---|---|---|
| **Therapy-speak** | Fake-vulnerable, pseudo-therapeutic monologue voice. | Write like an analyst, not a LinkedIn influencer. |
| **Stranger diagnosis** | Telling someone exactly what's broken inside their org. | Frame as a market pattern, not a verdict. |
| **Sycophantic acknowledgment** | "Great question!", "Excellent point!" | Remove entirely. |
| **"Actually" as authority** | Dropping "actually" to imply everything else is wrong. | State the point without the credibility grab. |

### Sentence-Level AI Patterns

These aren't individual banned words: they're structural habits that make prose feel machine-generated even when every word is technically fine.

| Pattern | What it looks like | What to do instead |
|---|---|---|
| **Passive voice default** | "It was observed that pricing is being raised." "The pattern was identified." | Use active voice: "Prospects raise pricing." "We identified the pattern." Passive is fine occasionally for emphasis, but AI defaults to it constantly. |
| **Qualifier stacking** | "This potentially significant and increasingly important trend." Multiple hedges or intensifiers piled onto one noun. | Pick one qualifier. If you need two, the sentence is doing too much. |
| **Compound sentence sprawl** | Sentences with 3+ clauses joined by commas and conjunctions, trying to capture every nuance in a single breath. | Split into 2-3 shorter sentences. Each sentence carries one thought. |
| **Colon-list reflex** | Every paragraph ends with a colon and a list. Content that should flow as prose gets chopped into bullets reflexively. | Reserve lists for genuinely parallel items. If the items are sequential or argumentative, write prose. |
| **Uniform card cadence** | Every card in a grid follows the identical rhetorical template: same header construction ("X, not Y" contrast in all four), same sentence count, same rhythm. Individually fine; together they read machine-stamped. | Vary the construction across sibling cards. One contrast header per grid max. Let one card be a fragment, another a stat, another a plain claim. Read the cards in sequence aloud: if they sound like a drumbeat, rewrite. |
| **Dramatic lead-in labels** | Full sentences dressed up with portentous colon openers: "The pattern is clear:", "The opportunity: instead of...", "The central thesis:". The lead-in adds drama, not information: deleting it conveys the same thing. | Delete the lead-in and start with the content. Short structural labels in label voice are fine as design elements; rhetorical throat-clearing inside a paragraph is not. |

### List Discipline

**Lists are powerful but overused by AI.** When everything is a list, nothing stands out. Rules:
- Max 3-5 items per list. If you have 7 items, the bottom 3 probably aren't earning their space. Cut or consolidate.
- Lists of genuinely parallel items (competitors, personas, objections) are fine at any length.
- If list items require 2+ sentences each, they should probably be paragraphs or cards, not bullets.
- Never nest lists more than one level deep.

### Banned Transitions and Filler

Remove or rewrite:
- "Moreover" / "Furthermore" / "Additionally" (restructure so the connection is obvious)
- "In today's [X]" / "In an era where" (cut or state specific context)
- "It's worth noting that" / "Notably" (just state the fact)
- "Here's what's interesting" / "Here's what caught my eye" (let the content signal importance)
- "When it comes to" (just talk about the thing)
- "At the end of the day" (cut)
- "Let's explore" / "Let's take a look" / "Let's break this down" (start with the point)

## The Tests

Run these against every piece of content in the final output:

1. **"Would this surprise the team?"** If they'd say "yeah, we already know that," cut it. If they'd say "huh, I hadn't thought of it that way," keep it.

2. **"So what?" at exec level.** If a VP would read it and shrug, cut it. If they'd forward it to their team, keep it.

3. **"Bold tactical recommendation is the gold."** Recommendations are what the reader remembers and acts on. Make them specific, actionable, and concrete.

4. **"Is this actionable?"** Every recommendation must point to something the team can change: messaging, positioning, enablement, materials. Not generic advice.

---

## Review Checklist

Self-contained editorial audit. Run every check against the generated file. Fix violations inline. Three passes: mechanical, structural, and quality.

### Pass 1: Mechanical (deterministic, zero tolerance)

**1a. Em-dashes**
- [ ] Zero em-dash characters (U+2014: —) anywhere in reader-facing text
- Detection: search for `—` in all text content (skip CSS/JS). Replace with colons, commas, periods, or en-dashes.

**1b. Tier 1 Banned Words**
- [ ] Zero occurrences of any Tier 1 word in reader-facing text
- Detection: case-insensitive search in text between `>` and `<` tags
- Common survivors: "leverage," "comprehensive," "robust," "actionable," "seamlessly"

**1c. Banned Phrases**
- [ ] Zero occurrences of: "best practices," "deep dive," "dive into," "at its core," "in order to," "due to the fact that," "serves as," "testament to," "it's worth noting," "when it comes to," "at the end of the day," "let's explore," "let's take a look," "let's break this down," "here's what's interesting," "in today's," "in an era"

**1d. Banned Transitions**
- [ ] Zero occurrences of: "Moreover," "Furthermore," "Additionally," "Notably" as sentence starters

**1e. Leaked Internals**
- [ ] Zero references to Octave internals in reader-facing text. Banned terms:
  - Library references: "the library," "source of truth," "library says," "library doesn't"
  - Entity jargon: "entity type," "objection entities," "use case entities," "no [X] entities"
  - Tool-output framing: "findings" (standalone: covers "findings show," "findings analyzed," "findings surfaced," "[N] findings," etc.), "field data indicates," "the data shows," "surfaced from," "mined from," "workspace data," "knowledge base" (the Octave feature)
  - Meta-references: "Octave internals"
  - Tool/system leakage: function or tool names (e.g. `enrich_company`, `list_events`), version numbers, stream identifiers, tool inventories ("Sources: Octave enrichment")
- Detection: search text content for each term. These must be reframed as market intelligence language ("conversations reveal," "prospects report," "the pattern shows").

### Pass 2: Structure Scan (read every sentence pair)

**2a. Negation-as-depth / "It's not X, it's Y"**
- [ ] Zero instances of the negation setup pattern
- Detection: read every consecutive sentence pair. Test: does the first sentence exist only to be negated by the second? If removing the first sentence loses no information, rewrite as a direct positive claim.
- Common forms: "This is not [X]. It is [Y]." / "The [thing] isn't [X]. It's [Y]." / "[Subject] aren't [doing X]. They're [doing Y]." / "It's more than just [X]." / "[X] isn't just about [Y], it's about [Z]."

**2b. Staccato Flex**
- [ ] No runs of 3+ short declarative sentences (under ~8 words each) stacked back-to-back

**2c. Gerund Relay**
- [ ] No sentences where two -ing verbs chain and restate the same thing

**2d. Role Recitation**
- [ ] No instances of reading back someone's title: "As [Role] at [Company], you..."

**2e. Sycophantic Language**
- [ ] Zero instances of: "Great question," "Excellent point," "That's really insightful," or any conversational reward

**2e2. Dramatic Framing**
- [ ] No subtitles, intros, or headlines that use rhetorical drama or mystery framing instead of stating content directly
- [ ] Read each section's header stack (eyebrow + heading + lead) aloud as one unit: no drumroll suspense, no command to the reader ("have the counter ready"), no ominous teasing ("the things that stall this deal"). A claim-shaped heading still fails if the surrounding stack is theatrical. Rewrite to plainly state the conclusion (see rule 8, conclusion-carrying not theatrical).
- Detection: subtitles containing "What separates...", "The one thing...", "Why some succeed...", "The secret to...", or any frame that teases rather than states. Replace with a direct description of the content.

**2e3. Objection Phrasing Trap**
- [ ] No quoted prospect dialogue invented for an objection (e.g. `"We already use Glean for this"`)
- Detection: objections written as quotation-marked speech instead of described risk. Rewrite as the underlying risk: "They position this as overlap with existing enterprise search."

**2f. Tier 2 Clustering**
- [ ] No single content block contains 2+ Tier 2 words

**2g. Sentence-Level AI Patterns**
- [ ] No runs of passive voice (2+ consecutive passive sentences)
- [ ] No qualifier stacking (multiple hedges/intensifiers on one noun)
- [ ] No compound sentence sprawl (3+ clause sentences that should be split)
- [ ] No colon-list reflex (prose artificially broken into bullets)
- [ ] No uniform card cadence (sibling cards in a grid don't all follow the same rhetorical template; max one "X, not Y" contrast header per grid)
- [ ] No dramatic lead-in labels ("The pattern is clear:", "The opportunity:", "The central thesis:"): delete the lead-in, start with the content

**2h. List Discipline**
- [ ] Lists max 3-5 items (unless genuinely parallel enumeration like a competitor list)
- [ ] No nested lists beyond one level
- [ ] List items that require 2+ sentences each should be prose or cards

### Pass 3: Quality (judgment calls)

**3a. Presentation Principles**
- [ ] No references to the library, source of truth, or Octave internals
- [ ] No insight-type badges or tags ("Gap:", "Contradiction:", "Emerging Signal:")
- [ ] No internal maintenance surfaced as insights
- [ ] No standard deal Q&A surfaced as insights (unless genuinely surprising)
- [ ] Every piece framed as market intelligence, not tool output
- [ ] Enrichment data woven into prose, not echoed as raw fragments or jargon without context

**3b. Headlines**
- [ ] Every headline states a finding, not a topic, including chart titles and stat labels
- Test: can the reader agree or disagree? Yes = claim (correct). No = label (violation).

**3c. Implications / Recommendations**
- [ ] Every recommendation is specific and actionable (messaging, positioning, enablement, materials)
- [ ] No generic advice ("follow up faster," "build relationships")
- [ ] Recommendations max ~2 sentences

**3d. Content Quality**
- [ ] "So what?" test: a VP would forward it, not shrug
- [ ] "Surprise" test: team would say "huh" not "yeah, we know"
- [ ] Bold recommendations are specific, concrete, and actionable

**3e. Speculation Marking**
- [ ] Every inferred field (competitors, stakeholders, pains, budget, timeline) that isn't confirmed by intel is labeled as unconfirmed: "Unknown, potential: Datadog," not "Likely: Datadog" or "Competition: Datadog"
