# Role-Play and Quiz Mechanics — Shared Engine

The common machinery for interactive practice sessions. `/octave:train` uses this engine for generic sales practice; `/octave:deal-coach` uses it for Resonate → Elevate → Compel methodology practice. Each skill layers its own scenario framing, scoring criteria, and grounding data on top — the mechanics below stay the same.

---

## Role-Play Engine

### 1. Scenario Setup

Collect three choices before starting (via `AskUserQuestion` when not provided as flags):

1. **Scenario** — what conversation is being practiced. The invoking skill supplies the options (e.g., discovery call, objection handling, demo pitch, competitive displacement; or a single coaching stage vs. a full journey simulation).
2. **Difficulty** — how much resistance the buyer gives (see tiers below).
3. **Buyer persona** — dynamically populated from `list_all_entities({ entityType: "persona" })`. Present up to 4 personas with title and key concern. If the invoking context already fixes the persona (e.g., a specific deal's stakeholder), skip this question.

### 2. Difficulty Tiers

| Tier | Buyer behavior |
|------|---------------|
| **Friendly** | Open and receptive. Engages, asks questions, shares information willingly. Gives verbal rewards when the seller executes well. Good for learning. |
| **Skeptical** (recommended default) | Realistic buyer. Pushes back on weak points, needs proof, asks "why should I care?" — but yields to strong execution. |
| **Hostile** | Resistant, time-pressed, dismissive. Short answers, price pressure, competitor mentions. Only yields to excellent execution. Tests composure. |

### 3. Playing the Buyer

- Ground the buyer in real data: persona pain points from the entity, real objections from `list_findings`, and any deal or Motion ICP context the invoking skill loaded.
- Respond naturally to what the seller says — don't cycle through a fixed objection list.
- If the seller makes a strong point, acknowledge it (even skeptical buyers respond to good selling). If the seller fumbles, become more distant or disengaged.
- Drop cues a well-trained seller should pick up on; let the invoking skill define which cues matter.
- Allow natural conversation flow — don't force every technique or beat.

### 4. Session Length and Wrap-Up

Run **8-12 exchanges**, then signal a natural conclusion ("I think we're running short on time..."). End states by difficulty:

- Friendly: "This sounds interesting, let's set up a follow-up"
- Skeptical: "I need to think about it" / "Send me some materials"
- Hostile: "I don't think this is for us" — unless the seller earned better

For multi-stage simulations, pause between stages ("Good — let's fast-forward. [Context for next stage]."), score each stage independently, then give a cumulative scorecard.

### 5. Scorecard

After the session ends, deliver a structured scorecard:

- **Overall score** (out of 100) with difficulty and scenario noted
- **What went well** — 2-3 specific moments, quoting the seller's actual lines
- **Areas to improve** — 2-3 missed opportunities, each with the better line the seller could have said
- **Dimension breakdown** — score each dimension the invoking skill defines (e.g., discovery depth, objection handling, proof usage; or Buyer Mindset / Value Propositions / Talking Points)
- **Next actions** — offer to rerun, raise difficulty, switch scenario, or move to a different practice mode

---

## Quiz Engine

### 1. Quiz Setup

Collect two choices before starting:

1. **Topic / type** — supplied by the invoking skill (e.g., personas, objections, competitive positioning; or stage recognition, methodology application, talk-track completion).
2. **Length / format** — quick (~5 questions), standard (~10), or deep (~15 with reasoning coached per answer).

### 2. Question Construction

- Build questions from real library data (entities, Motion ICP narratives, findings) — never invented facts.
- Mix recall questions ("What are [Persona]'s top pain points?") with scenario questions ("A prospect says X — what do you do?").
- Include plausible red herrings so questions test judgment, not pattern matching.
- If deal-grounded, tie questions to the actual account context.

### 3. Running the Quiz

Present questions **one at a time**, labeled `QUESTION [N]/[Total]` with the topic or category. After each answer:

- Grade it: Correct / Partially Correct / Incorrect
- Give a brief explanation citing the specific library content or methodology element
- Show the running score

### 4. Results

At the end, deliver:

- **Score** with percentage
- **Per-question breakdown table** (question, grade, one-line note)
- **Strengths** and **gaps**, grouped by the invoking skill's dimensions (topic areas or stages)
- **Recommended next steps** — retake, drill the weakest area, switch to role-play on the weak area, or study via guided learning
