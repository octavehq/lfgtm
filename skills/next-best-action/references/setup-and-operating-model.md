# Setup and operating model

The NBA skill is reusable reasoning. The setup makes it specific to one workspace, and the
account ledger gives each deal continuity. Do not run recurring NBA as a generic stateless prompt.

## 1. Setup interview

Run this when the user invokes `setup`, when no workspace config exists, or when a recurring run
would otherwise rely on important defaults. Ask only for answers that cannot be discovered from
Octave or connected tools. Inspect the workspace first, present what was found, and ask the user to
confirm or correct it.

### Strategy and authority

1. Does the team run a named sales methodology (MEDDPICC, Challenger, a homegrown process)?
   If so, is it mandatory on every deal, a default reps may deviate from, or one option among
   several the team picks from per situation?
2. For each kind of question the skill will need to answer, which document or library object is
   the source of truth? Never ask this abstractly. Search the workspace first, then present what
   was found and ask the user to pick when more than one candidate exists ("stage definitions
   appear in both the CRM pipeline config and the 'Sales Process' doc — which wins?"). Pin down
   where to look for:
   - what each pipeline stage means and what qualifies a deal to advance;
   - which personas, segments, and offerings the team sells to, and the plays for each
     (usually the Octave library's Motion ICP cells and playbooks);
   - how to handle named competitors and common objections (battlecards, competitor cards);
   - which customer stories, metrics, and references are approved to cite;
   - team rules of engagement, such as discount limits, who may contact executives, or
     required process steps.
3. When two trusted sources still disagree, which one wins? Recommended default:
   - what actually happened on the deal (calls, emails, CRM activity) wins for current deal
     state;
   - the named methodology wins for definitions and prescribed steps;
   - Octave Motion ICP cells and playbooks win for company-specific strategy;
   - explicit team rules win for operating constraints;
   - a genuine conflict between any of these gets surfaced for a human decision, never
     resolved silently.
4. May the system choose among multiple frameworks per deal? If yes, every chosen framework
   needs evidence that it applies, a check for reasons it doesn't, and a stated observation
   that would prove the choice wrong.

### Data and observability

Inventory connected sources and the claims each can support:

| Source | Useful for | Never infer from absence unless |
|---|---|---|
| CRM | stage, amount, owner, next step, contacts, activities | the object/filter coverage and freshness are known |
| Calls | buyer language, commitments, objections, methodology evidence | transcript index is current through the latest call |
| Email | thread state, sent artifacts, replies, commitments | the relevant mailbox/thread was searched |
| Slack | internal deal planning and customer Slack activity | identity and channel-to-account binding use hard keys |
| Calendar | scheduled mutual steps and meeting coverage | external attendees are verified |
| Product telemetry | adoption, activation, risk, expansion signals | account identity and metric semantics are verified |
| Support / success | escalations, unresolved friction, champion health | the account and time window are explicit |
| Warehouse / BI | business outcomes and custom milestones | query lineage and refresh time are explicit |
| Market / news | perishable reasons to act | the source is current and relevant to the prescribed play |

Record `connected`, `readable`, `freshnessSignal`, and `blindSpots` separately. A connected source
is not necessarily readable in the current runtime.

### Scope, cadence, and actions

Confirm:

- target population: named accounts, open opportunities, a segment/stage filter, or a rep's book;
- ownership: workspace policy plus optional team/rep overlays;
- cadence: manual, scheduled sweep, or event-triggered after calls, replies, stage changes, product
  signals, or library revisions;
- outputs: terminal digest, standing brief, CRM next-step proposal, drafts;
- action ceiling: recommend only, draft/stage, or specific approved writes;
- required approval for customer-facing moves, economic-buyer outreach, CRM mutations, pricing,
  concessions, and stage/forecast changes;
- outcome windows and the progression signals that matter by stage/move type;
- feedback owner and the ritual for blessing, rejecting, retiring, or contradicting learned plays.

## 2. Configuration contract

Store local configuration at `~/.octave-nba/config.json`, keyed by workspace. Keep secrets and raw
source data out of it.

```json
{
  "workspaces": {
    "<workspace-id>": {
      "version": 1,
      "configuredAt": "2026-07-24T00:00:00Z",
      "methodology": {
        "mode": "situational",
        "primary": "workspace Motion ICP salesMethodology",
        "frameworks": ["MEDDPICC", "Challenger"],
        "authorityNotes": "Observed deal state wins; surface prescription conflicts."
      },
      "sources": {
        "crm": {"connected": true, "freshnessSignal": "live read", "blindSpots": []},
        "calls": {"connected": true, "freshnessSignal": "indexedThrough", "blindSpots": []},
        "email": {"connected": false, "blindSpots": ["sent follow-up may be invisible"]},
        "slack": {"connected": false},
        "calendar": {"connected": false},
        "productTelemetry": {"connected": false},
        "support": {"connected": false},
        "warehouse": {"connected": false}
      },
      "scope": {"mode": "explicit-watchlist"},
      "cadence": {"mode": "manual"},
      "approval": {
        "recommend": "FLOW",
        "draft": "GATE",
        "externalSend": "GATE",
        "crmWrite": "GATE",
        "stageOrForecastWrite": "GATE"
      },
      "outcomes": {
        "acceptanceCheckBusinessDays": 2,
        "defaultOutcomeWindowBusinessDays": 10
      }
    }
  }
}
```

Approval routes: **FLOW** means proceed and report; **GATE** means stop and get explicit human
approval first. Defaults are conservative: situational methodology, explicit watchlist, manual
cadence, recommend-only, all external writes gated, and unconfigured sources treated as unavailable.

## 3. Configuration layers

Configuration and memory live in three layers, in priority order:

1. **Workspace policy**: methodology, authority order, approval ceiling, and outcome definitions.
2. **Rep/team overlay**: book filters, voice, and working preferences. An overlay must never
   silently rewrite workspace strategy.
3. **Account/opportunity ledger**: the durable history of observations, recommendations, evidence,
   and outcomes for one selling motion. Key it by `opportunityOId` when a concrete opportunity
   exists; use an account key only for pre-opportunity work, and migrate the history when separate
   opportunities emerge.

## 4. One reasoning contract

This skill is the reasoning contract: invoked on demand, portable across runtimes, and composable
with whatever tools the caller brings (their warehouse, product telemetry, Slack, support systems).
Anything that adds persistence or initiative around it — scheduled sweeps, event listeners, staged
drafts, delayed outcome verification — must read and write the same action/ledger schema, so
recommendations never diverge by surface.

