# Next best action: the strategy gap

The prep ends on one to three moves. A move exists only where the seller's strategy and the evidence disagree: the strategy for this persona, segment and stage prescribes something, and the record does not show it happened, or the lookalike deals show a path this deal is not on. No prescription means a library gap (note it, do not invent a play). No evidence either way means a question to ask, not an instruction. Both present and aligned means nothing to do, and "no move clears the bar" is a good answer. Generic advice (multi-thread, follow up, update the CRM) never qualifies.

## 1. Fix the position

One sentence: stage in the CRM, what the buyer's language says about where they are, who has been engaged and who has not, last touch and its date. A mismatch between stage and buyer language is itself a gap.

## 2. Read the prescription

Resolve the motion with `list_motions`, then call `find_motion_icp` with `motionOId`, `personaOId` and `segmentOId` for the persona and segment cell (stage objectives, buyer mindset, value propositions, talking points; add elements and learnings). When the workspace has more than one motion, use the cell from the motion whose type matches this deal (net new, displace incumbent, expansion) and say which; prefer a displacement cell only when the buyer named an incumbent; when it is the only cell near the persona, you may use it as guidance and say the buyer has named no incumbent. When the workspace has no cell for this combination, use the nearest cell and say which one and why (same persona in another segment first, then the same segment with the closest buying role). When both the segment and the persona differ, use no cell: record a gap in one line, and fall back to the authored records that still apply (the objection, competitor, use case and proof point records the buyer's own words point to, and the persona nearest by buying role) plus the lookalike evidence. A search that returns only an unrelated cell is not guidance. Use only what the cell says at this deal's stage. The cell's stages are early, mid and late: map the deal's pipeline phase (prospecting and discovery to early, evaluation to mid, negotiation and commitment to late) and say the mapping when it is not obvious. Prescription text is guidance, never a fact about this account.

## 3. Read the evidence

What happened on this deal: calls, emails, who spoke, commitments, dates. Which prescribed plays ran: `get_deal_strategy_evidence` with the cell's entity ids (seller voice) and again with buyer voice. A thin result means "not shown to have run", never proof it did not.

## 4. Gaps to look for

Walk these. A gap fires only when you can point to the result that shows it.

- **Unanswered signal.** The buyer voiced a concern, pain or question the strategy has an answer for, and nothing shows it was answered after they said it.
- **Stage mismatch.** The CRM stage runs ahead of what the buyer has confirmed (the riskier case) or behind it.
- **Missing person.** The strategy expects a persona at this stage (decision maker, user, technical gate) and nobody matching is on the deal. Only roles due at this stage, size and motion count; a role that joins later is listed as needed later, and a renewal during onboarding or a closed-won deal has no missing people ([information principles](../../shared/information-principles.md#reading-calls-and-deals) rules 23 and 24). Say it as people: "Acme's buying committee is missing 2 people". Real candidates come from the deal's stakeholders and CRM contacts first, `find_person` (an external people search, so the company link is unverified) for outside candidates, or from names the buyer mentioned; never invent a name.
- **Competitor exposed.** A competitor or alternative is live and the competitive answer has not run.
- **Proof gap.** The buyer doubted a claim we can prove and the proof was not shown after the doubt.
- **Lookalike divergence.** The deals like this one that moved did something this deal has not (a comparison, a person added, a document sent), or the ones that stalled shared a pattern this deal shows. Counts are real counts.
- **Fresh reason to act.** Something changed on our side or theirs since the last touch (a new proof point, a market event, a signal) and the buyer has not heard it. Silence alone is never the reason.

## 5. Rank and cap

Score each gap 1 to 3 for impact on the buyer's next decision, confidence in the evidence (a verbatim quote plus an authored prescription is a 3; an inference from two weak signals is a 1) and urgency (decays in days). Rank by product. A gap with confidence below 2 becomes a question inside another move. A move whose follow-through is only "ask them and write it in the CRM" is not a move: cut it or fold it into the questions section. Cap at three and never pad. One move is normal. Zero is honest: state the position, say that no move clears the bar, and name the one signal that would change that.

## 6. Anatomy of a move: all four parts, every time

1. **The move.** A verb and the outcome it should get, doable today. Names a person only if verified. The move, why now and the strategy source each get their own line, in that order, so the rep can act from the first line ([information principles](../../shared/information-principles.md#reading-calls-and-deals) rule 25).
2. **Why now.** The evidence: a dated quote, a stage fact, or a lookalike count with its base. Label lookalike-based reasons "likely".
3. **Strategy source.** What the seller's strategy says, in plain words ("our answer for marketing operations leads at discovery is to ..."), with the record linked when links are available.
4. **Follow-through.** The thing the rep can use now: a drafted email (full text, ready to send, built only from verified facts), a named person to add and how to reach them, a document to send and which one, a battlecard to open. If the follow-through is a draft, write it in full, in the rep's voice, using only verified facts; a fact the rep must confirm before sending (a date, a promised sample, a number) is a bracketed placeholder naming what to confirm. Never promise a capability, price or result the library does not support.

The last line of the section is the meeting success condition: what the rep should have in hand when the call ends.
