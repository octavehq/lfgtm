# abm: cohort plan

Use this method when the request names a segment, a cohort or a list of accounts instead of one company ("a campaign for this segment", "plan these 40 accounts", "ABM for our top tier"). The plan answers four questions for the person running the campaign, in this order: who is in the cohort and why they belong together, the one angle they share, how the accounts are tiered, and what is run for each tier. It ends by saying how the per-account plans are made.

The rules in [the task method](task-method.md) on evidence, triggers, personal facts and review apply here unchanged. Read [gtm-context.md](../../shared/gtm-context.md) for the offering, motion and segment cells, and [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for claims and operator inputs. Load the [analytics contract](../../shared/analytics-contract.md) before stating any rate or comparison.

## 1. Resolve the cohort

Settle which of three inputs the request gave, and say which in the plan's first line.

- **A list of accounts.** Normalize each to a domain and remove duplicates. The list is the cohort. Do not add accounts to it.
- **A segment in the library.** Resolve it with `list_entities` and read it with `get_entity`. Its definition says who belongs. The members you can name are the accounts the workspace already holds in that segment: page `list_deals` with `accountSegments` set to the segment id and `openOnly` false, and collect the distinct accounts with their relationship and open or closed deals. When the user also wants accounts the workspace has never touched, say that new accounts come from `/octave:prospector` and plan the ones on hand.
- **A described cohort** ("fintechs under 500 people that use a competitor"). Translate each term into a filter the tools support (`accountSegments`, `companySizeBands`, `accountIndustries`, `accountCountries`, `accountTiers`, `relationship` on `list_deals`), state the filter you applied, and name a term you could not express as unresolved. Ask one grouped question when a missing term changes who is in the cohort; continue with the rest while waiting.

Read the CRM relationship for every member before planning. Customers, open opportunities and former customers in the cohort are listed apart from net-new accounts, because the plays differ. Never drop an account silently; an exclusion carries its reason. An account with no CRM record is net-new: say so on its row and plan it with the other net-new accounts. A missing record is expected for accounts the team has not worked and is never a reason to stop the plan or to leave an account out.

Then say why these accounts belong together. Use only traits the records show for the members (segment, size band, industry, the alternative they use, a shared trigger with dated occurrences). A trait true of some members is written with its count ("31 of 40 are in the 200 to 999 band"). When the list has nothing in common that the offering speaks to, say so and propose the split that would make two coherent cohorts.

## 2. Find the one angle

The angle is the single argument that leads every play in the cohort. It comes from won deals that look like these accounts and from what buyers said on those calls, never from the segment's name.

1. **Ask Octave first.** `ask_octave`, seeded with the segment id and the persona ids when you hold them: "What worked in won deals in this segment, who was involved, and what did buyers say they needed?" Treat the answer as a map and open what it cites with the narrow tools ([Ask Octave first](../../shared/octave-research-toolkit.md#ask-octave-first-for-questions-that-span-records)).
2. **Read the won deals that look like the cohort.** `list_deals` with `stageCategory` closed_won, the cohort's filters (`accountSegments`, plus size, industry or motion where they define the cohort), a `closeDateFrom` that covers at least the last year, sorted by close date descending. Read the lost deals the same way with closed_lost. State the filter and both counts. `groupBy` gives the whole-set counts without paging.
3. **Open the closest few.** For three to five won deals and two to three lost ones: `get_deal` for stakeholders and loss reason, `list_events` with `opportunityIds` inside `filters` and an explicit `startDate` and `endDate`, then `get_event_detail` on the calls before the deal closed.
4. **Get the words.** `search_call_transcripts` with `attributedSegmentOIds` for the segment, `speakerSide: external`, and `dealOutcome` `WON` then `LOST`. Quote buyers without their company or name.
5. **Read the authored strategy.** `list_motions` to resolve the motion, then `find_motion_icp` for the segment's cells, with the linked proof points and references. This is the seller's guidance for the kind of buyer, not a fact about these accounts.

Write the angle as one sentence a seller could say, then its support: how many of the won deals it appeared on with the base ("on 4 of the 5 won deals with call records"), one or two dated quotes, the proof that backs it, and what the lost deals show beside it. Tell comparable deals as sequence, never as the cause of a win. Other customers' names stay in the internal plan and out of anything a buyer will read.

When fewer than three won deals match, say that in the first line of the section and present the angle as the authored strategy's, labeled as guidance not yet seen in outcomes. When the won deals point to two different angles (two personas, two alternatives being replaced), say the cohort is really two and split it; do not average them into one vague line.

## 3. Tier the accounts

Tiers say how much effort an account gets. Use the workspace's own account tiers when its CRM carries them (`list_deals` with `groupBy: 'accountTier'` shows the names and their order), and say that you did. Otherwise build three tiers from what you can check for every member:

- **Fit.** `qualify_company({ companyDomain })` for each member, showing the composite and the sub-scores ([reading the scores](../../shared/octave-research-toolkit.md)). A hard disqualifier outranks a high score.
- **Likeness to the won deals.** How many of the traits the won set shares the account also shows.
- **A reason to act now.** A dated trigger, an open opportunity, recent engagement, or an existing relationship. A library trigger with no dated occurrence at the account is "to validate", not a reason.

Tier 1 has strong fit and a reason to act now. Tier 2 has strong fit and no dated reason yet. Tier 3 fits in part or has an unresolved unknown. State the rule in one line above the table and apply it to every member, so a reader can see why an account sits where it does. Unknown is not false: an account you could not qualify is listed as not assessed, never placed in the bottom tier by default. For a large cohort, qualify within the agreed budget, say how many were assessed, and tier the rest only on the traits you read.

## 4. Plays per tier

Each tier gets one play, written before rendering: who it is aimed at (the personas from the segment's cells), the channel and the number of touches, the hook (the cohort angle, cut to the tier), the proof to bring, what is personalized per account and what is shared, the commitment the play asks for, and the condition that moves an account up a tier or out of the campaign.

- **Tier 1** is worked one account at a time. The play here is a full account plan for each, and the cohort plan only names the entry persona and the hook.
- **Tier 2** is a shared sequence with one personalized line per account, drawn from a fact on that account's record.
- **Tier 3** gets the lightest touch that can surface a reason to act (a single message, an event invitation, an ad audience), and a stated signal that promotes it.

Include one complete sample message for tier 2 unless the user asks otherwise. It uses only claims the library supports and names no other customer without an approved reference. Pair each material risk to the campaign with its mitigation.

## 5. Per-account plans

Close the plan with one short section that says what happens next: the cohort plan sets the angle, the tiers and the plays, and the plan for each account (the committee, the entry person, the outreach) comes from running this skill for that account, tier 1 first. List the tier 1 accounts as ready-to-run lines (`/octave:abm <domain>`), and say that a host able to run a skill for each item in a list can take the tier 1 list as its input. Do not write committees or named contacts for individual accounts in the cohort plan.

## Output

Sections, in order: the cohort (who and why together), the angle, the tiers (rule, then the table of accounts with tier, fit, relationship and reason to act), the plays per tier, risks, next step. Headers carry the conclusion in plain words. Counts carry their base. When rendering HTML, use the card vocabulary and brand rules of the [html scaffold](html-scaffold.md) with these sections in place of the six account-plan sections; the account table stacks on narrow screens. A list of more than about 25 accounts also ships as a CSV written with a standard CSV writer.

## Before delivering

Check that every account in the table is in the resolved cohort and none was added, every tier follows the stated rule, every count names its base, the angle cites deals and calls you opened in this run, no buyer-facing line names another customer, and no person is named for an account you did not research. Report unrun checks as NOT RUN.

## Carry the work forward

Return `worklist` beside the document, following `output.schema.json`: stable action ID, account identity, owner or accountable role, status, concrete next action, observable completion signal, reopen condition and dated source references. Include deliberate holds as rows. Reuse supplied action IDs and completion reports when revising a plan; do not reopen completed work merely because the report reran. A newly supported failure can justify a new action with its own ID.

Make each row actionable without requiring another plan when the next step is already established. Propose the actual test or follow-up; execution is a separate host action. Do not turn a no-send request into a document full of approval gates. Show clickable source links when the tools supply them, preserve record IDs when no link exists, and keep missing source references null. The document and data must agree on owners, statuses and completion signals. Completed means recorded completion of that action, not an answered product question or a generated draft. Owner reports stay attributed and never become independent customer evidence.

When the host supplies verified conversation sources, copy their event IDs, dates and URLs into the matching account's worklist evidence. Preserve the supplied account identity and domain; never infer a domain from its name. If the cohort identity conflicts with a verified source, flag the conflict and resolve it before attaching the conversation. A receipt ID is not a conversation ID. Render an “Open conversation” link beside each account action or its evidence, labeled with account and source date; a source appendix alone is insufficient. Keep stable action IDs in structured data or a technical detail fold, using human-readable account/action labels in the visible table. Unknown links remain null, never constructed or guessed by the model.
