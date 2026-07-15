# Account Plan — Document Structure

Structure and content spec for the account plan HTML document. Visual/CSS rules come from the shared layers (`../shared/presentation-principles.md`, `../shared/formats/html-document.md`) plus the workspace company's brand kit. The locked CSS, section skeleton, and card vocabulary live in `html-scaffold.md` (reproduce it) — a family with meeting-prep: sidebar nav dots, one card type per section, `role-badge`s, `talk-track` cards, a two-column `risk-grid`, the persona selector, and the `.unconfirmed` tag.

## What this document is

A tight, account-level **plan a rep acts on**: is this account worth it and why now, what's likely driving them, who to engage, how to position to each persona, the engagement plan, and what could go wrong. Six jobs, six sections. It is a plan, not a reference dump — it advises (that's the point), but at the account level. (Coaching for one scheduled meeting lives in `/octave:meeting-prep`; single-asset copy lives in `/octave:generate`.)

**The tight test:** every section does one of the six jobs, and within a section every line either tells the rep something they don't know or tells them what to do. Fixed card shapes with hard density caps. If a card wants a fourth line or a section wants a seventh item, cut. A rep scans this in two to three minutes.

## Groundedness — hard rule

Every named person, title, prior employer, tenure, and LinkedIn URL must come from a real tool result (`find_person` / `enrich_person` / `resolve_profile_from_email`). **Never synthesize a person or a LinkedIn slug.** If a role is empty, say so ("no economic buyer identified yet") — an honest gap beats a plausible invention. Tag anyone not tool-confirmed with `.unconfirmed`. This section-3 rule is the one that failed a prior run; treat it as non-negotiable.

## Section headers

Headers are **plain English but conclusion-carrying** — a short claim, not a two-word label and not a cute brand name. Good: "Strong fit, and the timing is live." "One champion engaged; no economic buyer yet." Bad: "Fit & timing" (too bare), "The Take" (cute). Write the header as the takeaway of the section.

## Section Order

| # | Section (job) | Condition |
|---|---------------|-----------|
| 1 | Masthead | Always |
| 2 | Fit & timing — is this worth it, why now | Always |
| 3 | What's likely driving them / what to explore | Always |
| 4 | Buying committee — who to engage | Always |
| 5 | How to position per persona | When a Motion ICP cell match exists (almost always) |
| 6 | Engagement plan | Always |
| 7 | What could go wrong | When real risks exist |
| 8 | Footer (sources) | Always |

## Section Specs

### 1. Masthead
Workspace-company chrome; the target account's logo appears here as the account. Account name, one-line descriptor, date. No run metadata (no Depth/Motion/Stage chips — that's tool internals).

### 2. Fit & timing (job: is this account worth it, and why now)
- **Verdict:** 2-3 sentences — the fit call, why now (or honestly "no live trigger; this is proactive"), and the single recommended play. Lead with it.
- **Stat strip** (`deal-intel-grid` cards, 4): ICP fit score · Segment match · Motion · Status (warm/cold + one word on what's happened).
- **Fit reasons / watch-outs:** 2-3 reasons it fits, 1-2 watch-outs. One line each. This OWNS the fit judgment — no other section re-argues it.

### 3. What's likely driving them / what to explore (job: why they'd buy)
Not a signals dump. What pains probably drive this account and what to dig into.
- 3-4 items, one line each: the likely pain or pressure → why it points to us.
- **Buying triggers:** if the library has real buying-trigger entities that match, use them and mark them as known (`Known` tag). Otherwise frame items as hypotheses (`Likely` / `To explore` tag) grounded in the persona×segment cell — and do light research to support them where you can.
- Be honest about what's unknown. A short "worth confirming" note is fine; do not manufacture certainty.

### 4. Buying committee (job: who to engage) — GROUNDEDNESS-CRITICAL
- For each relevant **persona type** (from the library), call `find_person` and surface **1-2 strong-match real people** — strong match only, real only.
- **Stakeholder cards** (`grid-2`, meeting-prep pattern): avatar initials, name, title, `role-badge` (champion / budget-owner / evaluator / gatekeeper), one-line disposition (who they are, why they matter), real LinkedIn link if returned. `.unconfirmed` tag on anyone not tool-confirmed.
- **Coverage-gap line:** which buying roles are still unfilled. Identification is fine here; the "what to do about it" lives in the engagement plan.
- Cap: ≤5 people total. This is a coverage snapshot; the dedicated people-finder tool goes deeper.

### 5. How to position per persona (job: what to say so it lands) — the Octave-native centerpiece

**Select the personas per account — do not default to a fixed triad.** Pick the ≤3 personas most relevant to THIS account's mapped committee and segment, chosen from the library's actual personas (`list_entities({ entityType: "persona" })`), not a standing eng/CISO/GRC set. Match them to the committee you found in section 4 and to the segment: e.g. swap in **Privacy / Data Protection Officer** for a regulated healthcare or finance account, **Procurement / Vendor Risk Reviewer** for a late-stage or enterprise-procurement motion, **VP of IT / Head of IT** for a lean mid-market buyer. If the account genuinely is a classic security-org committee, eng/CISO/GRC is a fine choice — but it must be a *choice* driven by this account, and it should visibly differ when the account differs.

Interactive **persona selector**: tabs/toggle across the selected personas; selecting one shows its panel. Per persona panel, pulled from the Motion ICP persona×segment cell (`find_motion_icp`):
- **Their main concerns** — 2-3 bullets, what this persona actually cares about.
- **Their status quo** — one line on how they handle this today (the thing we displace).
- **Lead with** — the angle + the one value prop to open on.
- **Proof that fits** — one reference/proof point matched to this persona.
Cap: ≤3 persona panels, the four fields above, tight lines. Competitive counter folds into "Lead with" where a competitor is in play. This section is why Octave beats a generic template — the messaging is grounded in the cell, not invented.

### 6. Engagement plan (job: what to do next) — quick and tight
- **Entry point:** one featured card — who to reach first, why them, the hook.
- **Sample outreach:** one or two short sample emails (`generate_email`) for the entry persona, in `talk-track`-style cards. Real and specific, not lorem.
- **Sequence** (`game-plan-phase` timeline): reach out to [persona] first leading with [angle] → loop in [persona] at [stage] → etc. 4-6 steps max. This is the overall strategy, NOT a 37-step project plan.
- **Fold in real CRM engagement** (`find_crm_activities` / `generate_crm_context`) if any exists — prior touches, owner, last activity — and build the plan off it. Ignore dummy/seed pipeline values.

### 7. What could go wrong (job: what could blow it up)
Two-column **`risk-grid`**: each row is a risk → the move that de-risks it. ≤4 pairs. Real risks only, no padding. (This is the one place mitigation guidance is welcome — paired, one line each.)

### 8. Footer
Sources in human-analyst language (company & stakeholder research, ICP/persona qualification, the motion cell, proof points, any call/email/CRM history). Small, muted. No internal tool names.

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
- [ ] Section 4 has 1-2 strong-match people per relevant persona, ≤5 total
- [ ] Section 5 persona selector works; each panel = concerns + status quo + lead-with + proof, from the motion cell; ≤3 personas
- [ ] Section 6 is tight (≤6 steps), has entry point + 1-2 real sample emails, folds in real CRM history, ignores dummy pipeline
- [ ] Section 7 is a two-column risk → mitigation grid, ≤4 pairs
- [ ] Personas are consistent across sections 4/5/6
- [ ] No dummy/seed pipeline numbers rendered as real
- [ ] Footer sources in human language, no internal tool names

## Persona selector — implementation note
Self-contained, no framework. Radio-input + label tabs, or buttons toggling `.active` on panels via a tiny inline script. Respect `prefers-reduced-motion`, keyboard-focusable tabs, and make sure ALL persona panels are visible when printed (`@media print { .persona-panel { display:block !important } }`).
