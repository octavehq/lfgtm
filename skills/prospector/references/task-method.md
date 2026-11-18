# prospector: task method

### Choose the way in
When the request gives no explicit ICP, criteria or seed, start from lookalikes of won deals: read [lookalikes.md](lookalikes.md) and use it to build the candidate pool. A named seed company (`--similar-to`) follows the same reference with that company as the only seed. When the request names a motion, segment, persona or its own criteria, build the pool from those criteria as described below. The two can be combined: criteria given alongside a lookalike request narrow the seeds and the candidates. Whatever the way in, the rest of this method (scope and suppressions, qualification, identity, count and shortfall) applies to every candidate.

### Resolve criteria before search
Read [gtm-context.md](../../shared/gtm-context.md) for the offering, motion, persona/segment cells, and approved qualification criteria. Read [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for qualification evidence and operator constraints, and [output-readiness.md](../../shared/output-readiness.md) for the list's actual completion state. Load [analytics-contract.md](../../shared/analytics-contract.md) only when claiming historical win/loss-derived targeting or comparing a defined cohort.

Resolve requested accounts versus people, count, geography/territory, offering/motion, and exclusion policy. Read relevant CRM relationships and current opportunities before applying acquisition suppressions; do not exclude all existing customers from a cross-sell task. Ask a grouped question for missing targeting or suppression choices that materially affect eligibility. Continue supported discovery and incorporate the answer before final qualification/filtering.

Translate each selected criterion into one of: directly searchable attribute, enrichment check, buyer-validation question, or true exclusion. Record the criterion's library/user source and whether it is a must-have, weighted indicator, or hard disqualifier in the configured qualification model. A pain narrative is not automatically a searchable technology, funding, or size filter. Mark proxy filters and their known false-positive/false-negative risk.

Discover broadly enough to satisfy the requested count after deduplication and exclusions, within the agreed/requested budget. Follow the supported search tool's pagination contract when present; do not fabricate offset or cursor parameters. If continuation is unavailable, use justified alternative criteria without silently broadening the user's target. Normalize company domains and person/profile identities; retain exclusion reasons.

Use actual configured qualification results, including available question-level evidence, sub-scores, missingness, and disqualifiers. Separate company fit from person fit. Unknown is not false; a high composite does not cancel a true hard disqualifier. Do not invent scores or infer hidden candidate scores. If the response cannot explain a material decision, fetch supported detail or label the assessment's limitation.

### Octave tools for this task
On an Octave host, find companies with `find_company` and people at a company with `find_person`; take firmographics from `enrich_company`. For company fit, use the workspace's own saved qualification agent: list them with `list_agents` (type `QUALIFY_COMPANY`), and run the one the request names, or the only one when there is exactly one, with `run_qualify_company_agent`. With none, or several and no way to choose, use `qualify_company`. Person fit works the same way with `QUALIFY_PERSON`, `run_qualify_person_agent` and `qualify_person`. Report each tool's fields as returned.

### What a qualification result means
A qualification returns a score out of 10, its rationale, answers per question and whether a disqualifier was triggered. Report `not_qualified` when a disqualifier was triggered, whatever the score. Otherwise take the verdict from the qualification itself when it gives one (a pass or a fail, a tier, or its own pass mark). When it gives only a score, the pass mark is the one the request states, and 7 of 10 when it states none: say on the page that 7 was assumed. A question the qualification could not answer is unknown, not a fail: name the unanswered questions beside the score. Report `unknown` only when the qualification was not run or returned no score, and say why. Give the score on every row, and rank by it.

Return the requested number of unique eligible results or an explicit shortfall with searched/returned/qualified counts and the limiting constraint. Do not refill the list with unqualified names simply to reach N.

Read [scale-filters.md](scale-filters.md) for the applicable mode.

