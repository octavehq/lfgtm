# Action ledger and learning loop

Recurring NBA becomes useful when it remembers what it recommended, observes whether it happened,
and learns without grading itself. The account ledger is the minimum durable object.

## 1. Ledger record

Store one append-only decision record per surfaced action in the watch state file
(`~/.octave-nba/state.json`, see [watchlist-and-sweep.md](watchlist-and-sweep.md) § State file).

```json
{
  "actionId": "nba_<stable-id>",
  "opportunityOId": "op_123",
  "accountDomains": ["acme.com"],
  "createdAt": "2026-07-24T16:00:00Z",
  "situation": {
    "crmStage": "Negotiation",
    "methodologyStage": "Compel",
    "motion": "strategic",
    "persona": "CFO",
    "segment": "Enterprise",
    "gapType": "G7",
    "committeeGap": null,
    "whoseCourt": "us"
  },
  "move": "Send the audit-cost proof with a 20-minute validation ask",
  "whyNowEvidence": [],
  "strategySources": [],
  "reasoning": {
    "observed": [],
    "inferred": [],
    "assumed": [],
    "framesConsidered": [],
    "conflicts": [],
    "counterfactual": "",
    "falsifier": ""
  },
  "execution": {
    "hook": "generate_email",
    "channel": "email",
    "owner": "rep-id",
    "dueAt": null,
    "consequence": "medium",
    "route": "GATE"
  },
  "lifecycle": {
    "status": "proposed",
    "supersedes": null,
    "supersededBy": null
  },
  "acceptance": {"status": "pending", "evidence": [], "checkedAt": null},
  "outcome": {"status": "pending", "evidence": [], "checkedAt": null},
  "confidence": "medium"
}
```

Use a stable fingerprint based on opportunity + gap type + strategy entity + intended state change.
Do not fingerprint on prose. Rewording the same move must not create a new action.

## 2. Reconcile before prescribing

Before asserting a deal state or emitting a recommendation:

1. Re-read live CRM state and the newest observable conversation/activity in relevant channels.
2. Resolve identity with hard keys (opportunity id, CRM association, verified email domain).
3. Compare timestamps and source freshness.
4. Classify each load-bearing statement:
   - **observed**: directly supported by a cited source from this run;
   - **inferred**: derived from observed facts, with the chain named;
   - **assumed**: supplied by methodology, workspace policy, or a fallback.
5. Treat a negative search as `not observed`, not `did not happen`, unless coverage is complete,
   fresh, and the action is observable in that channel.
6. Reconcile open commitments before all other gap types. An overdue promise already made is
   normally a stronger next action than a newly invented play.

If the latest call is newer than `indexedThrough`, inspect the event directly or state that the
newest transcript is not yet searchable. Do not retire or contradict an action using a stale index.

## 3. Commitment ledger

When available, read:

- `CALL_INTERNAL_COMMITMENTS_MADE`;
- `CALL_EXTERNAL_COMMITMENTS_MADE`;
- structured `owner`, `due`, and `mutual` metadata.

Classify:

- internal open commitment: the seller owes an artifact or action;
- external open commitment: the buyer owes an artifact or action;
- mutual next step: calendar-shaped and agreed by both sides;
- fulfilled: positive delivery/completion evidence;
- superseded: later evidence changed the commitment;
- overdue: due date passed with fresh, complete observable coverage and no completion evidence;
- unobservable: completion may have occurred in a blind channel.

Never recommend a new follow-up while an internal promise is open unless the new move explicitly
fulfills or renegotiates that promise.

## 4. Reasoning discipline for non-trivial deals

Use the compact four-part action anatomy for obvious moves. For a consequential or ambiguous move,
also produce:

1. **Observe**: verified, inferred, and assumed facts.
2. **Select frames**: candidate methodology/company plays, why each applies, contraindications, and
   whether selected.
3. **Apply independently**: diagnosis, prescription, and falsifier per selected frame.
4. **Synthesize**: convergence and real conflicts. Vocabulary differences alone are not conflicts.
5. **Counterfactual**: the new evidence that would reverse the recommendation.
6. **Verdict**: move, source, consequence, approval route, and falsifier.

No framework quota. “No framework applies cleanly” is valid. The strategy-gap invariant still
applies: no prescription means a library gap; no observation means a discovery question.

## 5. Action lifecycle

`proposed -> approved|rejected -> executed|executed_modified|not_executed|superseded|unobservable`

Acceptance and outcome are independent:

```
acceptance ∈ {executed, executed_modified, not_executed, superseded, unobservable, pending}
outcome    ∈ {progressed, stalled, regressed, unobservable, pending}
```

- `executed`: positive evidence the prescribed move ran substantially as written.
- `executed_modified`: a materially similar move ran with a changed channel/tactic.
- `not_executed`: only when the due window passed and fresh, complete coverage proves the observable
  move did not run.
- `superseded`: the world changed before the move could run.
- `unobservable`: the channel, identity, or source coverage cannot support a verdict.
- `progressed`: positive buyer/deal movement in the attribution window.
- `stalled`: only when fresh coverage spans the full window and shows no progress/regression.
- `regressed`: positive regression evidence; silence is not regression.

Never collapse acceptance and outcome into one score. A rep accepting a recommendation is not proof
that it worked. An unexecuted recommendation receives no credit for unrelated progress. Acceptance
and outcome labels are always applied on a *later* run than the one that proposed the action, from
fresh evidence cited in that later run — never in the proposing run itself.

## 6. Attribution

Verification is a later run's job, never the proposing run's. Grade an action only on a subsequent
run, from fresh evidence gathered in that run, and never reword or re-derive the action being
graded — carry it by fingerprint and judge it as written. Partition time between consecutive
attributable decisions on the same opportunity so one event is not credited twice. Prefer positive
progression signals:

- stage advance or closed won;
- agreed meeting completed or new mutual step booked;
- buyer commitment fulfilled;
- verified customer response with direction understood;
- strategy gap closed after the recommended play;
- product/support milestone when configured for this workspace.

Use configurable windows by move/stage when known; otherwise start with an acceptance check near two
business days and an outcome window near ten. These are setup defaults, not universal sales laws.

## 7. Procedural memory

A learned play needs:

- stable id and title;
- problem, play, impact, and anti-pattern;
- partial situation predicate (persona, segment, motion, stages, risk/gap, whose court);
- hard exclusions;
- provenance to workspace strategy, methodology, and decision/action ids;
- lifecycle: candidate, blessed, retired, contradicted;
- derived track record, excluding pending/unobservable/superseded rows.

Retrieval is structured-first. Match on the situation fields that are known; missing fields are
unknown, not wildcards that increase confidence. Semantic search may help recall but must not erase
hard exclusions or authority.

Repeated outcomes may suggest a candidate play, or a contradiction of an existing one. Record it as
a candidate and surface it in the digest; only the user blesses, edits, retires, or rejects it. The
skill never applies an unblessed candidate as if it were workspace strategy.

## 8. Autonomy boundary

Classify each behavior by consequence and route it through a human-set ceiling. Two routes: **FLOW**
means proceed and report; **GATE** means stop and get explicit human approval first.

| Consequence | Examples | Default |
|---|---|---|
| trivial | surface a gap, rank actions, flag missing data | FLOW |
| low | create an internal brief, stage a draft | GATE until configured |
| medium | propose CRM next-step write, associate a stakeholder | GATE |
| high | send externally, contact power, alter stage/forecast, pricing/concessions | GATE |

Confidence may tighten a route but must never loosen it beyond the workspace ceiling. External-write
ceilings and outcome labels must live outside the agent's write authority before any autonomous
customer-facing phase.

