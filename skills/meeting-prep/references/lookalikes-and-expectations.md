# Lookalike deals and what to expect

Two sections rest on this method: "Deals like this: what worked, what didn't" and "What to expect, persona by persona". The promise to the rep: your team has been in this situation before, and there was a better path. Say what the record shows, no more.

## Building the lookalike set

A lookalike is a closed deal that matches this one on as many of these as the record supports, in this order: segment, buyer persona, motion (net new, upsell, displace incumbent), competitor or alternative in play, the main concern raised, deal size and stage reached.

1. **Seed with the graph.** `ask_octave`: "What worked in deals like this one, and who was involved?" seeded with the deal id and the resolved segment, persona and competitor ids. Note which deals, themes and people it names and what it says it could not establish.
2. **Resolve the cut.** Get the segment id from the deal's account, the persona ids from the attendees, and the competitor, alternative or objection ids from this account's calls (`get_event_detail` findings, `list_findings` scoped to the deal). Use only ids you saw.
3. **Count the cohort.** `compare_cohorts` with cohort A as the lookalike filter (segment, persona, and competitor or objection when present) against all other deals. Always set `startDate` far back (the default window is 14 days) and an `endDate`. Start with win rate; when the verdict is insufficient evidence, re-run with a leading outcome (`advanced_within_days` or `next_conversation_positive`) and say which outcome the figure is about. Pass `comparisonsDeclared` honestly. Report `observed` with its counts, then the verdict's strength; never "drives" or "causes". Check `acrossLinkScopes`: if the direction reverses under a stricter link scope, say the result is not stable. Cohort filters take library entities and deal fields, not employee count or title; for size and title cuts page `list_deals` (closed, by close date) and filter yourself, and say that you did.
4. **Make the set mechanical.** State the filter you applied (for example: closed, segment X, no renewals, 30 employees or fewer, this competitor) and apply it to the full closed-deal list (`list_deals` with `stageCategory` closed_won and closed_lost, paged; sort by close date), keeping every deal that passes. Compute every count and every sequence figure from exactly that list, never from the subset you happened to open. When you read only some of the deals' calls, say how many of the set have call records and how many you read, and keep the two bases apart.
5. **Open the deals.** `list_cohort_deals` for side A with `dealOutcome` won, then lost. Take the two to four closest of each, ranked by how many of the matching traits they share. Open each: `get_deal` (stakeholders, activity, loss reason for lost), `get_event_detail` on the calls before the deal closed, `get_deal_strategy_evidence` for which prescribed plays ran, and `search_call_transcripts` (`dealOutcome`, `attributedPersonaOIds`, `callPurposes`) for the exact words on the moment you are describing.
6. **Write sequence with counts.** For each lookalike, what happened on its calls before it moved or stalled: who joined and when, which concern came up, what the rep answered, what happened on the next call. Then the contrast across the set with its base: "In 2 of the 3 won deals with call records, the rep ran a same-data comparison before the proposal; in the 2 lost deals with call records, neither did." The base is the deals whose calls were read, with the cohort size beside it when you have it ("of 14 won and 11 lost in this segment").

## Rules for this section

- Other deals at the same account (an earlier purchase, a lost renewal, a sibling opportunity) are account history, not lookalikes: put them in the context section and say what they change (for example, "a $25,000 deal closed won earlier this year, so confirm what was sold before pitching it again").
- Group by what the rep can act on (a play, a person added, a comparison, a sequence), not by account.
- Won and lost both appear. If only one side exists, say so.
- An account name appears only in the internal comparison. Mark the section internal.
- When no play separates the deals that moved from the ones that stalled (the same rep behavior appears on both), say exactly that: "no separating play found in the N deals with call records", and give the one thing that did differ, if any (who was on the calls, how many calls, how long between them). A flat result still tells the rep not to expect a trick.
- When the set is thin (fewer than three decided deals), say that in the first line and present what exists as individual deals, not a pattern. When none exists, say what you looked for (segment, persona, competitor) and that no decided deals matched. Do not widen the cut silently; if you widen it, say how.
- Loss reasons are the CRM's recorded category in plain words, not a diagnosis.
- Verification is the point: any figure that came from the graph answer alone is marked as unverified or dropped.

## What to expect, persona by persona

One block per attendee, or per suggested role when attendees are unknown (label it "suggested, not confirmed").

1. **Who they are.** Name, title, persona and buying role as the data gives them. A derived role is labeled "likely". If the persona record exists, take the persona's stated pains and priorities from it as guidance, not as fact about this person.
2. **What this person has already said** on this account, in their words with the date. This is the strongest item.
3. **What this persona typically raises** (when no persona resolves for the attendee, use the nearest persona by buying role, label it low confidence, or write that no comparable persona was found) at this stage in this segment. Evidence: `ask_octave` for the persona (seeded with the persona id), then `search_call_transcripts` with `attributedPersonaOIds`, `attributedSegmentOIds`, `speakerSide: external` and `callPurposes` near this stage, ideally with `dealOutcome` won and lost; `get_entity_evidence` for the persona or its objections. Report the concern, the count of lookalike calls it came up on ("on 4 of the 6 calls with marketing operations leads"), and one short quote with date. Label it "likely": the evidence is other accounts.
4. **The answer that worked.** The seller's authored answer (`get_entity` on the objection or use case) and what the rep said on the lookalike deals that moved, with the count. Where no answer is authored, say so and give the question that would surface the concern.
5. **The question to ask them.** A question in their own words that would confirm or disconfirm the expected concern.

Directionally accurate is the bar. Never state an expectation as certain, never invent a quote, and never attribute a concern to a named attendee that only their persona raises elsewhere: write "people in this role tend to raise", then what this person said.
