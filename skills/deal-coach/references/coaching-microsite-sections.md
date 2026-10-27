# Coaching Microsite — the Six Jobs

The microsite does six jobs, in this order. Each is one section. Cut nothing and add nothing: if a job has no grounded content, say so honestly rather than pad. Every section is scannable in about three seconds.

Headers are **conclusion-carrying plain English**: one sentence that states the finding ("Pain is agreed, and the champion has not yet named who signs"), NOT a two-word label and NOT theatrical/clickbait framing ("Where you're exposed", "The two things that stall this deal", "Have the counter ready before the next call" are all rejected; see editorial-rules on theatrical vs conclusion headers).

Hard rules that apply everywhere: no em-dashes or en-dashes (use commas, colons, "to", or middle dots). No emoji. One idea per line. Fixed card shapes with the density caps below. Every named person, quote, competitor, and count traces to a real tool result.

---

## Hero (chrome, not a job)

Workspace-company logo (verified real asset). Eyebrow "Deal coaching plan". H1 is a claim about this deal, with the pivotal words in color emphasis (e.g. "Acme: convert agreed pain into internal urgency"). Then meta chips: **Buyer** (real name + title), **Persona**, **Segment**.

The methodology badge and the **stage rail** (current stage highlighted) appear only when a methodology is the workspace's own or the user asked for one by name ([information principles #18](../../shared/information-principles.md#reading-calls-and-deals)), and they carry that methodology's step names and objectives. Resonate → Elevate → Compel is used only when the workspace has it on file or the user asks for that framing. With none, omit both; Job 1 reads the CRM stage and demonstrated readiness, Job 4 previews the next CRM stages, and the Job 6 rubric uses the stage's own definition of good.

## Job 1 — Where this deal stands

The stage read. Answers: what stage is this, how sure are we, and what is the single most important move.

- **Gloss (`.stage-gloss`):** two to three sentences defining the current stage in plain English, so a reader who does not know the methodology understands it. What the stage's job is, and what it is not.
- **Verdict (`.verdict`):** one headline sentence stating where the deal is stuck, plus one "The move" line. This is the TL;DR.
- **Stage read (`.card`):** confidence label (honest: "Medium confidence, inferred from call signals, not a CRM record") + an evidence list, at most 4 rows (Agreement / Objection / Competitors / Activity), one line each, drawn from real findings.
- **Deal record:** with a CRM opportunity, a `.card` beside the stage read (`.stand.has-deal`) shows its stage, amount and close date from the record. With none, one line under the stage read (`.no-crm`): "No CRM opportunity on file, so stage, amount and close date are not shown." Never invent the fields, and never render an empty or dashed deal-record card.

## Job 2 — Where the buyer's head is

The current stage's Buyer Mindset (from the Motion ICP `salesMethodology` block), matched to what the buyer actually said.

- **Mindset (`.mindset`):** the stage Buyer Mindset in two short paragraphs, rewritten tight, in the buyer's world.
- **Heard on the call (`.heard-list`):** at most 4 real findings, one line each, with a `.who` attribution (real name, or "team pain, confirmed" when the finding was unattributed). Never attach a name to a finding the tool did not attribute.

## Job 3 — What to do now

The concrete aims for the current stage, then how to hit them. This is the meat.

- **Goals (`.goals`, numbered):** one outcome per grounded priority for this stage, at most 5. Each one line. Draw from the stage Talking Points, made specific to this account.
- **Value props to land (`.vp-list`):** 3 to 4 belief statements to plant (from the stage Value Propositions). A clean bulleted list, NOT pills/chips (chips read as raw-metadata badges).
- **Talk tracks (`.tt`):** 3 cards, each = a label that maps to a goal ("Talking point › goal 4 · expose the hidden cost"), a verbatim thing to say (in quotes), and a one-line note. **Weave the account's real named pains into the talk tracks** (e.g. "regional content fragmentation", "e-learning isn't landing") — this is what separates it from a generic methodology handout.

## Job 4 — The path to close

How the rep knows it is time to advance, and what to prove at each stage ahead. Keeps the reader oriented on the arc without jumping ahead.

- **Readiness (`.ready`):** a "You're ready for [next stage] when" card, 4 concrete tells (from the next stage's buyer mindset or definition). Green-tinted, check bullets.
- **Forward stages (`details.path`, collapsed):** one collapsible per stage ahead, using the workspace's own stages (the methodology's next steps when one is on file, else the next CRM stages). Each = the stage's buyer mindset or definition (short) + a "Prove these" list of 3. Collapsed by default because they are previews of later work; they show where the deal evolves and what is NOT yet in play.

## Job 5 — Top risks

The biggest risks already live in the account, each with its counter. **Not locked to a fixed number** — render one `.risk-pair` per real risk, typically 2 to 4. Do not invent a risk to fill a slot, and do not drop a real one to fit a layout.

- **Header:** de-numbered and calm ("The risks in play here, and the counter for each"), lead names them plainly. No theatrical framing, no urgency commands.
- **Each risk (`.risk-pair`):** a full-width row, risk on the left (red accent), counter on the right (green accent), equal height per row (grid stretch), stacks on mobile. Risk = one to two lines grounded in the calls (a named competitor, a stated objection, a build-it-ourselves signal). Counter = the sharp answer, one to three lines.

## Job 6 — Practice and what good looks like

A quick self-check and the bar for a strong stage.

- **Quiz (`.quiz`):** 3 questions on this stage's judgment. Each = a question, 3 options, and an explanation revealed on click. Native `<button>`s, keyboard-reachable, works without JS. Ground the scenarios in this deal (the real objection, the real competitor, the stage-transition tell).
- **Rubric (`.card` + `.rubric`):** 4 rows, criterion + what good looks like, one line each, from the workspace methodology's description of good for this stage (the `coaching-agents.md` rubric only under Resonate/Elevate/Compel framing).

## Footer

Provenance line (which calls, which buyer, which Motion ICP cell; note where deal-record fields were left blank) + "Octave · Deal Coach".

---

## Density caps (summary)

| Section | Cap |
|---|---|
| Job 1 evidence rows | ≤ 4, one line each |
| Job 1 deal record | one card from the CRM opportunity, or one `.no-crm` line |
| Job 2 heard-on-call | ≤ 4, one line each |
| Job 3 goals | one per grounded priority, at most 5 |
| Job 3 value props | 3 to 4 |
| Job 3 talk tracks | 3 |
| Job 4 readiness tells | 4 |
| Job 4 forward stages | one collapsible per stage ahead |
| Job 5 risks | 2 to 4 (one per real risk) |
| Job 6 quiz | 3 questions |
| Job 6 rubric | 4 rows |

## Review checklist (run against the generated file)

- [ ] Six jobs present, in order; hero has verified real logo + real buyer name/title.
- [ ] Methodology badge and rail show the workspace's own steps, or are absent; no Resonate/Elevate/Compel unless it is on file or was requested.
- [ ] Personal facts from calls left out and counted in the delivery message; each heard-on-call line and risk traces to a quote or record.
- [ ] Headers are conclusion-carrying, none theatrical or clickbait.
- [ ] Zero em/en-dashes (lint passes).
- [ ] Every capability, security, data-handling or results claim in a talk track or proof line has a record behind it, or carries "confirm with product" (rule 21).
- [ ] Every named person, quote, competitor, and count traces to a real tool result; deal fields come from the CRM opportunity or are replaced by the one-line no-CRM note, never invented or shown as an empty card.
- [ ] Job 3 goals number one per grounded priority, at most 5; value props are a clean list, not chips; talk tracks name the account's real pains and map to goals.
- [ ] Job 5 renders one card per real risk (not forced to two); no invented risk, none dropped for layout.
- [ ] Responsive at 375px (no horizontal overflow); print flattens (details open, nav hidden, cards avoid breaks); keyboard focus visible.
- [ ] Any CSS-grid list item wrapping an inline `<em>` keeps it inline (item text in a `<span>`).
