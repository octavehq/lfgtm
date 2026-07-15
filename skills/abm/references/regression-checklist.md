# ABM Regression Checklist

Issues found during testing, kept as a living checklist. Every item was a real failure in a real output. Run this against any new generation before delivering. New items go at the bottom of the relevant section with the date and test case.

The account plan is a tight, account-level **plan** organized as six jobs (fit & timing / what's driving them / buying committee / how to position per persona / engagement plan / what could go wrong). It DOES advise at the account level — that is intended. The checks below protect tightness and truth, not a no-advice rule.

---

## Groundedness (highest priority)

- [ ] **No invented people.** Every name, title, employer, tenure, and LinkedIn URL in the buying committee traces to a real `find_person`/`enrich_person` result. Zero synthesized profiles or slugs. *(2026-07-08, Coinbase — a prior run fabricated a 4-person committee with fake LinkedIn URLs like `in/jeremy-ciso` and the review pipeline rubber-stamped it. Verify names against an actual `find_person` call, not the generator's self-reported source list.)*
- [ ] **Honest gaps.** Unfilled buying roles are named as gaps ("no economic buyer identified yet"), never papered over with a plausible invention. `.unconfirmed` tag on anyone not tool-confirmed.
- [ ] **No dummy pipeline as real.** Seed/dummy CRM deal values (provider "generic", `seed-*` ids) are never rendered as real pipeline. Engagement history comes from real calls/emails/CRM activity only. *(2026-07-08, Coinbase)*

## Section structure

- [ ] **Six jobs, in order.** Fit & timing → what's driving them / to explore → buying committee → how to position per persona → engagement plan → what could go wrong. No stray extra sections.
- [ ] **Headers are conclusion-carrying plain English.** A short claim ("One champion engaged; no economic buyer yet"), not a bare label ("Buying committee") and not a cute name ("The Take"). *(2026-07-08, Coinbase)*
- [ ] **Persona is the spine.** The persona set and role labels are consistent across the committee (4), positioning (5), and engagement plan (6). No persona named one way in one section and another elsewhere.
- [ ] **Section 3 is pains/triggers, not a signals dump.** Real library buying-triggers are marked Known; everything else is framed Likely / To explore, honest about what's unknown. No manufactured certainty.
- [ ] **Section 5 is grounded in the motion cell.** Per-persona concerns / status quo / lead-with / proof come from `find_motion_icp`, not generic invention. Persona selector works and all panels print.
- [ ] **Section 5 personas are selected by relevance to THIS account**, from the library's actual personas, not a standing eng/CISO/GRC default. They should visibly differ when the account/segment differs (e.g. Privacy/DPO for regulated health/finance, Procurement for enterprise/late-stage, VP of IT for lean mid-market). *(2026-07-09, COUNTRY Financial — positioning defaulted to the same eng/CISO/GRC triad as the Coinbase run even though a finance-specific Privacy/DPO persona existed and the plan flagged the privacy seat as an open gap.)*
- [ ] **Section 6 is quick.** Entry point + ≤6 sequenced steps + 1-2 real sample emails. Not a 37-step project plan. Sample emails are real and specific, not lorem.

## Tightness & language

- [ ] **Fixed card shapes, capped.** Stat strip (4), committee (≤5 people, 1-2 per persona), positioning (≤3 personas), risk grid (≤4 pairs). Nothing overruns its cap.
- [ ] **No dramatic lead-ins.** "The pattern is clear:", "The opportunity:", "The central thesis:" — delete and start with the content.
- [ ] **No run metadata in the masthead.** No Depth/Motion/Stage chips — tool internals stay out.
- [ ] **Vertical compression.** Tight rows, small gaps, no hero spacing between sections. A rep scans it in 2-3 minutes.
- [ ] **Proof relevance stated once.** No "Evidence that lands" / "Why this lands" wrapper blocks; the relevance is in the line.
- [ ] **No em-dashes or en-dashes** anywhere in generated content (commas, periods, or "to").

## Section 7 (risks)

- [ ] **Two-column risk → mitigation grid, ≤4 pairs.** Real risks only, no padding. This is the one place paired mitigation guidance belongs (one line each).

---

## Adding new items

```markdown
- [ ] **Short description of the check.** What to look for and why it matters. *(YYYY-MM-DD, test case)*
```
