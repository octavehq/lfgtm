# prospector: task method

### Resolve criteria before search
Read [gtm-context.md](../../shared/gtm-context.md) for the offering, motion, persona/segment cells, and approved qualification criteria. Read [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for qualification evidence and operator constraints, and [output-readiness.md](../../shared/output-readiness.md) for the list's actual completion state. Load [analytics-contract.md](../../shared/analytics-contract.md) only when claiming historical win/loss-derived targeting or comparing a defined cohort.

Resolve requested accounts versus people, count, geography/territory, offering/motion, and exclusion policy. Read relevant CRM relationships and current opportunities before applying acquisition suppressions; do not exclude all existing customers from a cross-sell task. Ask a grouped question for missing targeting or suppression choices that materially affect eligibility. Continue supported discovery and incorporate the answer before final qualification/filtering.

Translate each selected criterion into one of: directly searchable attribute, enrichment check, buyer-validation question, or true exclusion. Record the criterion's library/user source and whether it is a must-have, weighted indicator, or hard disqualifier in the configured qualification model. A pain narrative is not automatically a searchable technology, funding, or size filter. Mark proxy filters and their known false-positive/false-negative risk.

Discover broadly enough to satisfy the requested count after deduplication and exclusions, within the agreed/requested budget. Follow the supported search tool's pagination contract when present; do not fabricate offset or cursor parameters. If continuation is unavailable, use justified alternative criteria without silently broadening the user's target. Normalize company domains and person/profile identities; retain exclusion reasons.

Use actual configured qualification results, including available question-level evidence, sub-scores, missingness, and disqualifiers. Separate company fit from person fit. Unknown is not false; a high composite does not cancel a true hard disqualifier. Do not invent scores or infer hidden candidate scores. If the response cannot explain a material decision, fetch supported detail or label the assessment's limitation.

### Octave tools for this task
On an Octave host, find companies with `find_company` and people at a company with `find_person`; take firmographics from `enrich_company`. For company fit, use the workspace's own saved qualification agent: list them with `list_agents` (type `QUALIFY_COMPANY`), and run the one the request names, or the only one when there is exactly one, with `run_qualify_company_agent`. With none, or several and no way to choose, use `qualify_company`. Person fit works the same way with `QUALIFY_PERSON`, `run_qualify_person_agent` and `qualify_person`. Report each tool's fields as returned.

### What a qualification result means
A qualification returns a score out of 10, its rationale, answers per question and whether a disqualifier was triggered. Report `not_qualified` when a disqualifier was triggered, whatever the score. Otherwise a score of 7 or more is `qualified` and a lower score is `not_qualified`, unless the request states a different pass score, which then decides. Report `unknown` only when the qualification was not run or returned no score, and say why. Give the score on every row, and rank by it.

Return the requested number of unique eligible results or an explicit shortfall with searched/returned/qualified counts and the limiting constraint. Do not refill the list with unqualified names simply to reach N.

Read [scale-filters.md](scale-filters.md) for the applicable mode.
