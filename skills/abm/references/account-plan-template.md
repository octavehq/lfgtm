# Account Plan — Document Structure

Structure and content spec for the account plan HTML document. Visual/CSS rules come from the shared layers (`../../shared/presentation-principles.md`, `../../shared/formats/html-document.md`) plus the workspace company's brand kit. The locked CSS, section skeleton, and card vocabulary live in `html-scaffold.md` (reproduce it) — a family with meeting-prep: sidebar nav dots, one card type per section, `role-badge`s, `talk-track` cards, a two-column `risk-grid`, the persona selector, and the `.unconfirmed` tag.

## What this document is

A tight, account-level **plan a rep acts on**: is this account worth it and why now, what happened before, what's likely driving them, who to engage, how to position to each persona, the engagement plan, and what could go wrong. Seven jobs, seven sections. It is a plan, not a reference dump — it advises (that's the point), but at the account level. (Coaching for one scheduled meeting lives in `/octave:meeting-prep`; single-asset copy lives in `/octave:generate`.)

**The tight test:** every section does one of the seven jobs, and within a section every line either tells the rep something they don't know or tells them what to do. Fixed card shapes with hard density caps. If a card wants a fourth line or a section wants a seventh item, cut. A rep scans this in two to three minutes.

## Groundedness — hard rule

Every named person, title, prior employer, tenure, and LinkedIn URL must come from a real tool result (`find_person` / `enrich_person` / `resolve_profile_from_email`). **Never synthesize a person or a LinkedIn slug.** If a role is empty, say so ("no economic buyer identified yet") — an honest gap beats a plausible invention. Tag anyone not tool-confirmed with `.unconfirmed`. This section-3 rule is the one that failed a prior run; treat it as non-negotiable.

## Section headers

Headers are **plain English but conclusion-carrying** — a short claim, not a two-word label and not a cute brand name. Good: "Strong fit, and the timing is live." "One champion engaged; no economic buyer yet." Bad: "Fit & timing" (too bare), "The Take" (cute). Write the header as the takeaway of the section.

## Section Order

| # | Section (job) | Condition |
|---|---------------|-----------|
| 1 | Masthead | Always |
| 2 | Fit & timing — is this worth it, why now | Always |
| 2b | What happened before | Always (one line when there is no history) |
| 3 | What's likely driving them / what to explore | Always |
| 4 | Buying committee — who to engage | Always |
| 5 | How to position per persona | When a Motion ICP cell match exists (almost always) |
| 6 | Engagement plan | Always |
| 7 | What could go wrong | When real risks exist |
| 8 | Footer (research used) | Always |

## Section Specs

### 1. Masthead
Workspace-company chrome; the target account's logo appears here as the account. Account name, one-line descriptor, date. No run metadata (no Depth/Motion/Stage chips — that's tool internals).

### 2. Fit & timing (job: is this account worth it, and why now)
- **Verdict:** 2-3 sentences — the fit call, why now (or honestly "no live trigger; this is proactive"), and the single recommended play. Lead with it.
- **Stat strip** (`deal-intel-grid` cards, 4): ICP fit score · Segment match · Motion · Status (warm/cold + one word on what's happened).
- **Fit reasons / watch-outs:** 2-3 reasons it fits, 1-2 watch-outs. One line each. This OWNS the fit judgment — no other section re-argues it.

### 2b. What happened before (job: where the relationship stands)
The header states the play in plain words ("They evaluated in July and paused on budget", "No one here has heard from us"). Then:
- **History:** two to six lines: when and around what they evaluated, their situation in their words, what held them back, where it ended. People are named with titles.
- **In their words:** up to four quoted lines from calls, each with speaker and title, the one that best shows why they engaged first.
- **The objection:** the main objection raised on a call and how the team answered it, both quoted, when there was one.
- Unanswered outreach is a short dated list (at most five). No history is one line. Nothing here is inferred from contact counts.

### 3. What's likely driving them / what to explore (job: why they'd buy)
Not a signals dump. What pains probably drive this account and what to dig into.
- 3-4 items, one line each: the likely pain or pressure → why it points to us.
- **Buying signals:** one row per trigger that hit, freshest first, each with its date, one or two sentences a rep could repeat, and a link to the page it is on. A signal older than about four months is labelled as older and is never the why-now.
- **Buying triggers:** show the library definition separately from dated account occurrence. Known requires account evidence or attributed operator confirmation; otherwise use Trigger to validate and a confirming question.
- Be honest about what's unknown. A short "worth confirming" note is fine; do not manufacture certainty.

### 4. Buying committee (job: who to engage) — GROUNDEDNESS-CRITICAL
- For each relevant **persona type** (from the library), call `find_person` and surface **1-2 strong-match real people** — strong match only, real only.
- **Order:** people the team has already spoken with first (on a call, then in an email thread, then other CRM contacts), then the best match per persona. Each card says how the team knows them ("On the July call", "Replied in March", "New").
- **Stakeholder cards** (`grid-2`, meeting-prep pattern): avatar initials, name, current title, `role-badge` (champion / budget-owner / evaluator / gatekeeper), one line on what this role at this company worries about (two to four priorities, no pitch), real LinkedIn link if returned. `.unconfirmed` tag on anyone not tool-confirmed.
- **Coverage-gap line:** which roles should be engaged now and are not ("Acme's buying committee is missing 2 people"), then the roles needed later with the stage they join ([information principles](../../shared/information-principles.md#reading-calls-and-deals) rule 23). Identification is fine here; the "what to do about it" lives in the engagement plan.
- Default primary view: up to five people; full mode honors the requested scope with additional supported people in an appendix or an honest shortfall.

### 5. How to position per persona (job: what to say so it lands) — the Octave-native centerpiece

**Select the personas per account — do not default to a fixed triad.** Pick the personas relevant to the requested scope most relevant to THIS account's mapped committee and segment, chosen from the library's actual personas (`list_entities({ entityType: "persona" })`), not a standing eng/CISO/GRC set. Match them to the committee you found in section 4 and to the segment: e.g. swap in **Privacy / Data Protection Officer** for a regulated healthcare or finance account, **Procurement / Vendor Risk Reviewer** for a late-stage or enterprise-procurement motion, **VP of IT / Head of IT** for a lean mid-market buyer. If the account genuinely is a classic security-org committee, eng/CISO/GRC is a fine choice — but it must be a *choice* driven by this account, and it should visibly differ when the account differs.

Interactive **persona selector**: tabs/toggle across the selected personas; selecting one shows its panel. Per persona panel, pulled from the Motion ICP persona×segment cell (`find_motion_icp`):
- **Their main concerns** — 2-3 bullets, what this persona actually cares about.
- **Their status quo** — one line on how they handle this today (the thing we displace).
- **Lead with** — the angle + the one value prop to open on.
- **Proof that fits** — one reference/proof point matched to this persona.
Default primary view: three persona panels; add others to cover requested scope, the four fields above, tight lines. Competitive counter folds into "Lead with" where a competitor is in play. This section is why Octave beats a generic template — the messaging is grounded in the cell, not invented.

### 6. Engagement plan (job: what to do next) — quick and tight
- **Entry point:** one featured card — who to reach first, why them, the hook.
- **Outreach per person:** for the entry person (Quick) or each person on the primary committee (Full), one `talk-track`-style card holding how to frame the product for them, the opening move, the email (subject and body) and the three-beat talk track (opener, value in one sentence, question). All follow [outreach copy](outreach-copy.md). Real and specific, never a template with the name swapped.
- **Approach:** one or two sentences on the sequencing strategy, above the steps.
- **Sequence** (`game-plan-phase` timeline): three to five steps. Each is one action to one named person on the committee over one channel, saying what to send or say and why, written so the rep can act on it without reading anything else. This is the overall strategy, NOT a 37-step project plan.
- **Fold in real CRM engagement** (`find_crm_activities` / `generate_crm_context`) if any exists — prior touches, owner, last activity — and build the plan off it. Ignore dummy/seed pipeline values.

### 7. What could go wrong (job: what could blow it up)
Two-column **`risk-grid`**: each row is a risk → the move that de-risks it. ≤4 pairs. Real risks only, no padding. (This is the one place mitigation guidance is welcome — paired, one line each.)

### 8. Footer
**Research used:** every fact the plan, an email or a talk track relies on that is not already a signal or a line of history, one plain sentence each with its date and a link to its source. Then sources in human-analyst language (company & stakeholder research, ICP/persona qualification, the motion cell, proof points, any call/email/CRM history). Small, muted. No internal tool names.

## Density Rules
- **Vertical compression is a feature** — tight rows, small gaps, no hero spacing between sections.
- **Fixed card shapes.** Every card has a named shape with a line cap; do not free-form prose inside a card.
- **No dramatic lead-ins** ("The opportunity:", "The central thesis:") — start with the content.
- **Don't pad to look complete.** Fewer strong items beat more weak ones. Omit empty sections silently (except section 4's honest gap line).
- **Persona is the spine.** Sections 4, 5, and 6 all organize around the same persona set — keep the names and roles consistent across them.

## Review Checklist
- [ ] Headers are conclusion-carrying plain English (not bare labels, not cute names)
- [ ] Section 2 owns the fit judgment; stat strip present; verdict leads
- [ ] Section 3 frames pains/triggers as known (from library) vs. likely/to-explore — honest about unknowns, not a signals dump
- [ ] **Section 4: every person, title, and LinkedIn URL traces to a real `find_person`/`enrich_person` result; zero synthesized people or slugs; `.unconfirmed` on anything unconfirmed; coverage-gap line present**
- [ ] Section 4 has 1-2 strong-match people per relevant persona, requested count or explicit shortfall
- [ ] Section 5 persona selector works; each panel = concerns + status quo + lead-with + proof, from the motion cell; personas relevant to the requested scope
- [ ] Section 2b states the history from logged two-way contact only; quotes are verbatim with speakers; no history is one line
- [ ] Every buying signal has a date and a source link; the why-now is a dated signal no more than about four months old, or the plan says it is proactive
- [ ] People the team has spoken with lead the committee, each checked against a current profile
- [ ] Section 6 is tight (3 to 5 steps, each naming a person and a channel), has entry point + an email and talk track per person per [outreach copy](outreach-copy.md), folds in real CRM history, ignores dummy pipeline
- [ ] Every number in the plan, emails and talk tracks is visible as a signal, a line of history or research used
- [ ] Section 7 is a two-column risk → mitigation grid, ≤4 pairs
- [ ] Personas are consistent across sections 4/5/6
- [ ] No dummy/seed pipeline numbers rendered as real
- [ ] Footer sources in human language, no internal tool names

## Persona selector — implementation note
Self-contained, no framework. Radio-input + label tabs, or buttons toggling `.active` on panels via a tiny inline script. Respect `prefers-reduced-motion`, keyboard-focusable tabs, and make sure ALL persona panels are visible when printed (`@media print { .persona-panel { display:block !important } }`).
