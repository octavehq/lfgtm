# prospector: lookalikes of won deals

The default way in. When the request gives no explicit ICP, criteria or seed, start from the deals the workspace has won: take the best few as seeds, find companies and buyers that look like them, then qualify every candidate with the workspace's own qualification. The rules in [the task method](task-method.md) on suppressions, qualification, identity and shortfall apply unchanged.

A similar company is a candidate, not a qualified account. Likeness finds the pool; the workspace's own qualification decides who is in the list.

## 1. Read recent won deals

Page `list_deals` with `stageCategory` closed_won, a `closeDateFrom` about twelve months back and a `closeDateTo` of today, `sort` closeDate and `sortDirection` desc. Add the request's own limits as filters where it gave them (`dealMotion`, `accountSegments`, `companySizeBands`, `accountMacroRegions`, `pipeline`). Read the count from `totals`. Follow the tool's paging; do not ask for one very large page.

Leave out renewals, services, partner and non-commercial closes unless the request is about them, and count each account once however many deals it has.

## 2. Pick the seeds

Take three to five seeds. A good seed is recent, is the kind of deal the request is about (same offering and motion), has an account domain on its row, and sits in the segment the workspace sells to on purpose. Prefer deals with a named buyer and call records, since those also seed the people search. Do not pick by amount alone: one unusually large deal makes a poor pattern.

Say which deals were chosen and the rule used, in one line, in the internal summary ("5 seeds: net-new deals closed since March in the mid-market segment, one per account"). Seed customers are named only in that internal summary. They never appear in outreach copy or in anything a prospect will read.

When fewer than three won deals pass, say so, use the ones that exist as seeds, and add the criteria route from the task method so the list does not rest on one or two accounts. When there are none, or the deal tools are not available, use the criteria route alone and say what was checked.

## 3. Find similar companies

For each seed, call `find_similar_companies` with `referenceCompany: { domain }` (a `name` only when the row has no domain) and `numResults` sized to the requested count (the tool caps it at 25 per call). Pass `similarityTraits` only when the request or the seed set gives a reason to focus the match, for example `industry` and `size` when every seed shares them; otherwise leave it out. To get more for the same seed, call again with `previousResults` holding every domain already returned plus the domains you know to exclude. That is the tool's own way to continue, so do not invent an offset.

The tool searches an outside company database, so its results can include accounts the workspace already knows. Check each candidate's CRM relationship and open opportunities before keeping it, and apply the suppressions the task method resolved. Normalize domains and remove duplicates across seeds. Keep, for every candidate, which seed it came from.

## 4. Find similar buyers

Read the buyers on the seed deals: the primary contact's name and title on the `list_deals` row, and the stakeholders from `get_deal` when more than one person took part. Keep the people who were buyers on the deal, not everyone who joined a call.

For each buyer, call `find_similar_people` with the buyer's `linkedInProfile` when the record or an enrichment gives one, otherwise with `jobTitle` and the seed's `companyDomain`. `matchType` is FUZZY unless the request asks for the exact title. Resolve the tool's current schema before the first call and read what it returns before relying on a field.

Use the buyers' titles in a second way: they say which roles to look for at each similar company. When the request asks for contacts at the candidate companies, discover them with the host's person search, guided by those titles and the workspace's personas, before delivery. Company-only output has no invented contacts.

## 5. Qualify with the workspace's own model

Qualify every company candidate and every person candidate, within the agreed budget, the way [the task method](task-method.md) says: the workspace's saved qualification agent when there is one to use (`run_qualify_company_agent`, `run_qualify_person_agent`), and `qualify_company({ companyDomain })` or `qualify_person({ person: { ... } })` when there is none. Use the results as the task method says: show the composite with its sub-scores, keep unknowns as unknown, and let a true hard disqualifier outrank a high score. A candidate that is very similar to a seed and fails qualification is out, with its reason kept.

Do not add a similarity score of your own beside the configured one. The row says which seed the candidate resembles and on which traits the tool matched; fit is the qualification result.

## 6. What the list may claim

Write "similar to N recent won deals" and name the rule that chose the seeds. Do not write that these accounts are more likely to buy, and do not state a win rate, unless the cohort was defined and measured under the [analytics contract](../../shared/analytics-contract.md) as [scale filters](scale-filters.md) requires. Return the requested number of unique eligible results or a shortfall with the seeds used, candidates returned, candidates qualified, and the limiting constraint.

## Running it on a schedule or when a deal is won

Nothing in this method needs a person to start it, so a deployment that can run a skill on a schedule, or in response to an event, can use it for a standing lookalike list. The skill does not create the schedule or the trigger. It only behaves well when run that way.

- **On a schedule.** Each run reads the deals won since the last run's cutoff and uses those as seeds. Keep the earlier results and pass their domains as `previousResults`, so a run returns only accounts it has not returned before. When no deal has closed won since the cutoff, report "no new seeds" and return nothing instead of repeating the last list. Record the cutoff, the seeds and the returned domains with each run, where the deployment gives the run a place to keep them.
- **When a deal is won.** The seed is that one deal. Return a short list: companies similar to its account and people similar to its buyers, qualified as above. One deal is one seed, so say the list rests on a single account.

In both cases the run still checks CRM relationship and suppressions at run time, since an account returned last month may be an open opportunity today. An unattended run asks no questions: it uses the scope it was configured with, states the choices it made, and stops at a shortfall rather than widening the target.
