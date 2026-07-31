# Watchlist, sweep, and scheduling

The recurring half of the skill: which deals to run, the state that makes runs delta-aware, and how the caller schedules it. Everything here is **caller-side by design** — a local state file and an idempotent `sweep` entry point. Octave stores no watchlist, runs no nightly agent, and mirrors no CRM.

## State file

`~/.octave-nba/state.json`, keyed by workspace (from `verify_connection`; use the workspace name/identifier it returns, so one user can watch deals across workspaces without collisions). Create the directory on first use; the whole path stays out of any git repo. Workspace setup lives separately in `~/.octave-nba/config.json`; see
[setup-and-operating-model.md](setup-and-operating-model.md).

```json
{
  "workspaces": {
    "<workspace-identifier>": {
      "watch": [
        {
          "opportunityOId": "op_abc123",
          "account": "acme.com",
          "accountDomains": ["acme.com", "acmehq.com"],
          "label": "Acme — Platform expansion",
          "asset": true,
          "assetId": "as_xyz789",
          "assetUrl": "https://link.octavehq.com/s/<org>/nba-acme/",
          "addedAt": "2026-07-22T14:00:00Z"
        }
      ],
      "filters": [
        { "description": "open deals ≥ $50k in Mid-Market", "addedAt": "2026-07-22T14:00:00Z" }
      ],
      "runs": {
        "op_abc123": {
          "lastRunAt": "2026-07-21T07:00:00Z",
          "ledger": [
            {
              "actionId": "nba_abc123",
              "fingerprint": "G3:persona_cfo:engaged",
              "createdAt": "2026-07-14T07:00:00Z",
              "situation": {"gapType": "G3", "persona": "CFO", "...": "..."},
              "move": "Engage the economic-buyer persona with the audit-cost case",
              "lifecycle": {"status": "proposed", "supersedes": null, "supersededBy": null},
              "acceptance": {"status": "pending", "evidence": [], "checkedAt": null},
              "outcome": {"status": "pending", "evidence": [], "checkedAt": null},
              "confidence": "medium"
            }
          ]
        }
      }
    }
  }
}
```

- `ledger` is the per-opportunity memory. Each entry is the full decision record defined in
  [action-ledger-and-learning.md](action-ledger-and-learning.md) § Ledger record — the example
  above elides the `situation`, `whyNowEvidence`, `strategySources`, `reasoning`, and `execution`
  detail, but the stored record carries all of it. Fingerprints use stable semantic ids (gap +
  strategy entity + intended state change), not wording. Existing v0 `openActions` arrays may be
  read and migrated lazily on the next write.
- `filters` are stored as natural-language descriptions and re-evaluated at sweep time; there is no compiled query to go stale.
- Read-modify-write the whole file; keep it small. If it's corrupt, say so and rebuild from an empty structure rather than crashing the sweep.

## Watchlist commands

- **`watch <target>`** — resolve the target to an `opportunityOId` (SKILL.md Step 1), confirm the resolved deal back to the user, append to `watch`. `--asset` sets `asset: true` (the brief is created on the next run, not at watch time).
- **`watch --filter "<criteria>"`** — store the criteria verbatim. Tell the user how many deals it matches *right now* (evaluate immediately against `list_deal_health` / `list_pipeline_overview`) so they can sanity-check the blast radius before a sweep commits to it.
- **`unwatch <target>`** — remove from `watch` (and drop its `runs` entry). Leave any published asset alone; mention it exists and how to delete it (`/octave:asset-manager delete`).
- **`list`** — table: deal, account, watched since, asset (link if any), last run, open action fingerprints. Include how many deals the stored filters currently match.

## Sweep algorithm

1. **Resolve the run set.** Union of explicit `watch` entries + deals matching each stored filter, evaluated fresh against `list_deal_health({})` (health signals included — they feed G5) or `list_pipeline_overview`. On workspaces with 100+ open deals these outputs overflow the tool-result limit and spill to a file — plan on `jq` extraction, not on reading the result inline. Store every known domain for a watched account (`accountDomains`) and query events/findings with all of them. De-dup by `opportunityOId`. Report the set size before starting. A deal that got closed (won/lost) since the last sweep: report the outcome in the digest, drop it from `runs`, and if watched explicitly, ask (interactive) or note (headless) that it was removed.
2. **Per deal, in sequence:** run SKILL.md Steps 2–6 with the delta window set to that deal's `lastRunAt`. Sequential, not parallel — sweeps share one MCP session and per-deal ordering keeps tool volume and output attribution sane. Cap: if the run set exceeds 15 deals, run the 15 most urgent (health signal severity, then amount) and say which were deferred — never silently truncate.
3. **Reconcile the ledger.** Compare derived actions against stable fingerprints: same gap still
   open → carried (present with "still open since"); positive evidence the move ran → update
   acceptance; positive evidence the gap closed → update outcome and retire; changed world →
   superseded; blind/stale coverage → unobservable, never failed. New recommendation → append a
   complete decision record. Follow [action-ledger-and-learning.md](action-ledger-and-learning.md).
4. **Asset updates** for `asset: true` deals, honoring the stability rule (SKILL.md Step 6): no new evidence and no action change → skip the upload entirely, digest says "unchanged."
5. **Digest** (see below), most urgent deal first.

## Digest format

```
NBA SWEEP — <workspace> — <date>
Deals run: N (watched X, filter-matched Y) · Skipped unchanged: Z

1. ▲ Acme — Platform expansion ($120k, Negotiation)
   NEW  G4: Counter Gleam's accuracy claim with the Metro rollout reference
        — buyer quoted Gleam's pitch on Jul 20 call (12:41)
   OPEN G3: Economic buyer still unengaged (since Jul 14)
   Brief: <asset url> (updated)

2. ● Initech — New business ($45k, Discovery)
   No strategy-grounded action. Watching for: CFO joining the Jul 30 call.
   Brief: unchanged

RETIRED this sweep: Acme G7 (audit-cost proof presented Jul 21 — nice work)
CLOSED: Hooli ($80k) — WON Jul 19. Removed from watchlist.
```

Rank by: any perishable NEW action first, then health severity, then amount. Every line traces to the per-deal run; the digest never introduces claims of its own.

## Scheduling recipes (the caller owns the clock)

The sweep is idempotent and delta-aware, so any trigger works. In rough order of setup effort:

1. **Manual habit** — `/octave:next-best-action sweep` with the morning coffee. Zero setup; this is the default assumption.
2. **Claude Code scheduled agent** — `/schedule` a weekday-morning run of `/octave:next-best-action sweep --asset`. Runs in the cloud; needs the Octave MCP server available to the scheduled environment.
3. **cron / CI** — `claude -p "/octave:next-best-action sweep --asset"` from any box with the plugin + MCP configured. Pre-approve the needed tools via the project's `.claude/settings.json` allowlist rather than blanket permission flags.
4. **Event-triggered** — run the single-deal form right after something happens: a call recording lands, a stage changes, a Beats digest publishes. Wire it from the caller's automation (their webhook receiver invoking `claude -p "/octave:next-best-action acme.com --asset"`). This is the "more meaningful than nightly" option: the freshest possible answer, only when there's a reason.
