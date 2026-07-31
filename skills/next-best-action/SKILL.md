---
name: next-best-action
description: "Per-deal next-best-action engine driven by the strategy gap — diff what your library prescribes for this deal's persona × segment × stage against what the evidence shows actually happened, and rank the moves that close the gap. Supports a watchlist and scheduled sweeps that keep a per-deal brief updated in place. Use when user says 'next best action', 'what should I do next on this deal', 'what's my move on [account]', 'watch this deal', 'sweep my deals', 'keep this deal brief updated', or wants recurring per-deal action recommendations. Do NOT use for an interactive strategy session on one deal situation (use /octave:pipeline), a workspace-wide morning briefing (use /octave:signals), or a methodology coaching microsite (use /octave:deal-coach)."
argument-hint: "[setup | <account|email|opportunity> | watch <target> | unwatch <target> | list | sweep] [--asset]"
---

# /octave:next-best-action — Strategy-Gap Next Best Actions

Recommend the next best action on a deal by computing the **strategy gap**: the difference between what your Octave library prescribes for this deal's persona × segment × motion × stage, and what the evidence (CRM state, calls, emails, findings) shows has actually happened. Every recommended action cites both sides of that diff — the strategy source that prescribes the move and the evidence that shows the gap.

Run it on one deal for an on-demand answer, or put deals on a **watchlist** and `sweep` on a schedule to keep a per-deal brief (a hosted asset) continuously up to date. For recurring use, run `setup` once: NBA is workspace strategy + rep/team operating preferences + one durable ledger per opportunity, not one generic prompt for every seller and account.

## What this is — and is not

Generic next-best-action tools map to CRM state: they see a single-threaded deal and say "multi-thread," see silence and say "follow up." Those recommendations are table stakes and need no strategy substrate. This skill only recommends an action when the *strategy* layer makes it specific:

- Not "multi-thread" but "the Motion ICP cell for this deal requires the economic-buyer persona engaged before the Compel stage, and the stakeholder rollup shows nobody matching it — here is who to add and the value prop that lands with them."
- Not "follow up" but "they agreed on the audit-cost pain on the May 12 call, the library has a proof point that answers exactly that, and no internal finding shows it was ever presented."

Six boundaries keep this honest:

1. **State is read live, never stored.** CRM position comes through `get_deal_deep_dive` / `find_crm_records` / `find_crm_activities` at run time. Octave holds the strategy layer and the conversation evidence it already ingests — nothing else.
2. **The "calculation" is this derivation, not a scoring model.** The action is derived at read time by the agent following [action-derivation.md](references/action-derivation.md). There is no nightly scoring engine to maintain, and no claim to signals we do not have.
3. **Context the workspace doesn't have is the caller's to bring.** Product usage, warehouse data, support tickets — if the user's agent has those tools (their Snowflake MCP, their internal APIs), compose them into the same run. The skill states what it did and did not see.
4. **Reconcile before prescribing.** A cached brief is a candidate list, never current state. Re-read the live deal and latest observable threads before asserting a gap. A negative search means "not observed" unless coverage is fresh and complete.
5. **Remember actions, not prose.** Every recurring recommendation has a stable action identity, lifecycle, acceptance status, and outcome status in the account ledger. Acceptance and outcome are never collapsed into one score.
6. **The skill is the brain; an agent may be the clock.** The reasoning contract remains portable. Scheduled/event-driven runtimes handle listeners, ledger persistence, delayed verification, and explicitly approved side effects. See [setup-and-operating-model.md](references/setup-and-operating-model.md).

If no CRM is connected and no conversation evidence exists for the account, say so and stop — do not produce generic sales advice with a strategy costume on.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone, no em/en-dashes in asset copy
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims

**Presentation (asset output only):**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable internal-document specifics

**Octave data:**
- [Octave value](../shared/octave-value.md) — grounded workspace data over generic AI content
- [Octave research toolkit](../shared/octave-research-toolkit.md) — list vs search, verbatim-evidence tools, standard errors

## Usage

```
/octave:next-best-action <account|email|opportunity>       # One deal, ranked actions in the terminal
/octave:next-best-action setup                             # Configure methodology, sources, scope, and approval
/octave:next-best-action <target> --asset                  # Also publish/update the deal's hosted brief
/octave:next-best-action watch <target> [--asset]          # Add a deal to the watchlist
/octave:next-best-action watch --filter "<criteria>"       # Watch by eligibility filter (stage, amount, segment, owner)
/octave:next-best-action unwatch <target>                  # Remove from the watchlist
/octave:next-best-action list                              # Show watchlist + last-run status
/octave:next-best-action sweep [--asset]                   # Run every watched/eligible deal, print a ranked digest
```

## Examples

```
/octave:next-best-action acme.com                          # What's my move on Acme?
/octave:next-best-action jane@acme.com --asset             # Resolve deal from contact, update its brief
/octave:next-best-action watch acme.com --asset            # Keep a live brief for the Acme deal
/octave:next-best-action watch --filter "open deals over $50k in Mid-Market"
/octave:next-best-action sweep --asset                     # The scheduled entry point (cron / scheduled agent)
```

## Instructions

### Step 0: Route the mode

`setup` follows [setup-and-operating-model.md](references/setup-and-operating-model.md): inspect the workspace and connected sources first, then ask only for the operating decisions that cannot be discovered. Write no external state.

`watch` / `unwatch` / `list` manage local state only. Follow [watchlist-and-sweep.md](references/watchlist-and-sweep.md) § Watchlist commands and return. `sweep` resolves the run set per that reference, then executes Steps 1 to 7 per deal and finishes with the digest. A bare target executes Steps 1 to 7 for that one deal. If recurring mode has no workspace config, use conservative defaults and recommend `setup`; do not block a one-off answer.

### Step 1: Resolve the deal

Accept a domain, contact email, opportunity name, or `op_*` oId. Resolve to a concrete opportunity:
- **Single-deal mode: `find_crm_records` first** — search by account name/domain and take the opportunity from there. Do NOT reach for `list_deal_health` just to find one deal: on a real workspace (100+ open deals) its output overflows the tool-result limit and spills to a file. When you do need it (sweep mode, or for its health signals), expect the file-spill path and extract your deal with `jq`.
- `list_pipeline_overview({ openOnly: true })` / `list_deal_health({})` — sweep-mode resolution and health signals (these feed the momentum-decay gap, G5); both return `opportunityOId`
- An email resolves via `enrich_person` → company domain → opportunity

**Expect split domains and duplicate records.** Accounts routinely live under two domains (corp vs product domain) and duplicated CRM records; query events/findings with ALL known domains, pick the opportunity with the richer engagement as primary, and surface the duplicate as a hygiene note. If several genuinely distinct open opportunities match, ask which one (or run the largest open one and say so). If the workspace has no CRM connection, fall back to account-level mode: the "deal" is the account, position is inferred from conversation evidence only, and the output says so.

### Step 2: Observed state (read live, in parallel)

**Tell the user what you are pulling and why.** Run independent calls in parallel:

- `get_deal_deep_dive({ opportunityOId })` — stage + history, close-date changes, velocity vs workspace benchmarks, activity context, competitive mentions, **stakeholder rollup** (multi-threading, seniority, internal coverage)
- `list_findings({ eventFilters: { companyDomains: [domain] } })` — objections, pains agreed, capabilities that drew excitement, competitor mentions, internal proof-point/value-prop presentations (what the rep actually ran)
- `list_events({ filters: { companyDomains: [domain] } })` — the interaction timeline; note the *channel mix* (calls vs emails vs CRM-only)
- `search_call_transcripts({ companyDomain, query })` / `get_entity_evidence({ entityOId })` — verbatim buyer language with `recordingUrl` + `startSec` for jump-to-moment citations. **Mandatory in headless/sweep runs** — paraphrased findings alone cannot carry a "why now" citation. **Freshness check:** if the newest `CALL_TRANSCRIPT` event postdates the newest transcript-search hit, the latest call is not indexed yet — pull it via `get_event_detail` and say the index is behind.
- `find_crm_activities` / `generate_crm_context` — the no-calls fallback lane: notes, tasks, logged emails

See if these findings are available:

- `CALL_INTERNAL_COMMITMENTS_MADE` / `CALL_EXTERNAL_COMMITMENTS_MADE` with structured `owner`, `due`, and `mutual` metadata. Reconcile open promises before deriving new actions.
- `CALL_EXTERNAL_BLOCKERS_OR_DEPENDENCIES`: approval chains and external prerequisites
- `CALL_EXTERNAL_ABSENT_STAKEHOLDER_MENTIONS`: named missing committee members, one per finding
- `CALL_EXTERNAL_PRICING_OR_PACKAGING_FEEDBACK`: commercial friction without treating it as license to negotiate
- `CALL_EXTERNAL_FRUSTRATION_OR_DISAPPOINTMENT` and per-moment sentiment: urgency/relationship evidence, never a standalone verdict

If `get_deal_strategy_evidence` is registered, prefer it for coverage checks on the gaps that ask "did the play run" — G1 (unanswered strategy signal), G4 (uncountered competitor), G7 (proof gap): request the relevant library entity ids and use its timestamps/snippets as receipts. It returns evidence, not a verdict. Use `occurredAfterIso` when the question is whether a play ran after a buyer signal.

A transcript the caller pastes into the conversation is a **bonus evidence lane, not a substitute** for the tool pulls: it is the freshest source for verbatim quotes and open commitments ("I'll send you X"), and commitments are the highest-value NBA input. Mine it explicitly for promises made in both directions; cite it as caller-supplied.

**Degradation is expected, not exceptional.** Not every account has calls; some have only CRM activity, some only emails. Apply the evidence-lane matrix in [action-derivation.md](references/action-derivation.md) § Evidence lanes and state plainly which lanes were available.

**Observed / inferred / assumed is a hard distinction.** For non-trivial or consequential deals, follow [action-ledger-and-learning.md](references/action-ledger-and-learning.md) § Reasoning discipline. Name the inference chain, methodology assumptions, contraindications, counterfactual, and falsifier. Do not cite frameworks for decoration.

### Step 3: Prescribed state (the strategy layer, in parallel)

- `qualify_company({ companyDomain })` — segment/ICP classification if the account isn't already classified
- `list_motions()` → `list_motion_icps({ motionOId })` → `find_motion_icp({ motionIcpOId, includeLearnings: true })` — the persona × segment cell: `salesMethodology` stages (Buyer Mindset / Value Propositions / Talking Points), pains and consequences, benefits, references, Learning Loop learnings. This is the prescription's spine.
- `list_motion_playbooks({ motionOId })` + `get_motion_playbook` — pull the `COMPETITIVE` playbook when Step 2 surfaced a competitor; `ACCOUNT`/`MILESTONE`/`THEMATIC` when one clearly fits
- `search_knowledge_base` / `list_entities` — objection counters, proof points, references, buying triggers relevant to what the evidence surfaced

### Step 4: Change vectors (what's new since last look)

Delta sources make a *recurring* NBA worth running — they are why today's answer differs from last week's. Window: since `lastRunAt` for watched deals (from the state file), else 14 days.

- `list_revisions({ startDate })` — library changes: new positioning, updated competitor entity, new proof point that this deal has never heard
- `list_suggestions({ statuses: ["pending", "accepted"] })` — field intel accumulating in the inbox (e.g. a competitor suggestion with mounting evidence)
- `get_latest_gtm_report()` (+ `get_report_run` for sections) — segment/market intel and Beats digests: a compelling event in the account's segment is a reason to reach out *this week*
- `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"] } })` scoped to the same segment or competitor + `search_call_transcripts({ query, dealOutcome: "WON" | "LOST" })` — precedent: what worked in deals like this one, in the buyer's own words

### Step 5: Derive and rank the actions

Follow [action-derivation.md](references/action-derivation.md) exactly: walk the gap taxonomy — G1 unanswered strategy signal, G2 stage mismatch, G3 missing committee coverage, G4 uncountered competitor, G5 momentum decay, G6 fresh intel unexploited, G7 proof gap, G8 precedent divergence — score candidates on impact × confidence × perishability, cap at **3 actions** (1 is a fine answer; 0 is honest when nothing clears the bar — say "no strategy-grounded action; next trigger to watch for is X").

Before walking G1 to G8, run **G0: commitment integrity** (see that reference's § 0 and [action-ledger-and-learning.md](references/action-ledger-and-learning.md) § Commitment ledger). An open internal promise normally outranks a newly invented play. A mutual next step already booked retires redundant "schedule the next step" advice. An external commitment creates a monitor or a context-specific follow-up, not an immediate generic nudge.

Every action ships as four parts: **the move** (imperative, specific), **why now** (evidence citation — quote, timestamp, stage fact), **strategy source** (the prescription it comes from, in plain language), **execution hook** (the follow-through: `generate_email` draft, `/octave:meeting-prep`, `/octave:battlecard-doc`, a stakeholder to add via `find_person`).

**Groundedness is the same hard bar as every Octave skill.** Every quote, name, count, stage, and amount traces to a tool result from this run. Honest gaps beat inventions; seeded/demo CRM data (provider "generic", `seed-*` ids) is never rendered as real.

### Step 6: Deliver

**Terminal (always):** a compact digest — position in one sentence, the ranked actions with their four parts, evidence lanes used, what was NOT visible (no calls, no CRM, no motion cell). No HTML required for this path.

**Asset (`--asset` or watched-with-asset):** build/update the deal's hosted brief per [brief-spec.md](references/brief-spec.md), publish through the asset-manager route (upload scripts for files, `asset_update` for metadata — see that skill's One Decision Rule), and record the asset id in the state file. Review policy:
- **First brief in a workspace (template validation):** full review gate per the [review protocol](../shared/protocol.md) — lint + both reviewers + scorecard. This validates the template, not just the copy; a full gate runs 10-15 minutes of wall clock, so it cannot be the per-deal price.
- **Every other brief (new deals on the validated template, sweep updates):** mechanical lint (`bash <skill-dir>/../shared/scripts/lint.sh <file>`) + the render gate (`node <skill-dir>/../shared/scripts/render-gate.js <file> --chrome "nav,.toc,.sticky-nav"`) + the orchestrator's own groundedness check. Both scripts are deterministic and take seconds, so they run on every brief; it is the two-reviewer pass that is expensive and re-runs only when the template's structure changes or every 10th update of a given brief. A validated template still ships a defect when one deal's content is longer than the last: that is precisely what the render gate catches and a template validation cannot.
- **Stability rule:** if no new evidence arrived and prior actions are still open, do not re-word the brief — report "no change" in the digest and leave the asset alone.

**Sweep digest:** after all deals run, print the cross-deal ranking (which deal has the most perishable action first), per-deal one-liners, and any deals that returned "no strategy-grounded action." Format in [watchlist-and-sweep.md](references/watchlist-and-sweep.md) § Digest format.

### Step 7: Update the account ledger

For watched deals, follow [action-ledger-and-learning.md](references/action-ledger-and-learning.md):

- carry the same action by stable fingerprint; never mint a new action because wording changed
- retire only on positive closing evidence; a changed world marks it superseded; blind or stale coverage grades it unobservable and leaves it open
- keep acceptance (`executed`, `executed_modified`, `not_executed`, `superseded`, `unobservable`) separate from outcome (`progressed`, `stalled`, `regressed`, `unobservable`)
- record observed/inferred/assumed reasoning, strategy provenance, execution owner/channel/due date, consequence, and approval route for new actions
- apply acceptance/outcome labels only on a *later* run, from fresh cited evidence — never in the run that proposed the action; learned plays are promoted only by the user

One-off runs may show the lifecycle record in the response without persisting it. Recurring runs must maintain the account ledger.

## Scheduling (caller-owned, by design)

The sweep is a single idempotent entry point; *when* it runs belongs to the caller — Octave does not run a nightly agent on your CRM. Recipes (cron, Claude Code scheduled agents, event-triggered after a call lands) are in [watchlist-and-sweep.md](references/watchlist-and-sweep.md) § Scheduling recipes. Teams that want this available to MCP-only users (no plugin) can publish this skill into their workspace as an Octave managed skill via `create_skill` — same SKILL.md, invoked through `find_skill`/`get_skill`.

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `list_pipeline_overview` / `list_deal_health` | Resolve deals, eligibility filters, health signals for sweep |
| `get_deal_deep_dive` | Live deal position: stage history, velocity benchmarks, close-date pushes, stakeholder rollup, competitive mentions |
| `find_crm_records` / `find_crm_activities` / `generate_crm_context` | Live CRM reads; the no-calls evidence lane |
| `list_findings` / `list_events` / `get_event_detail` | Extracted conversation insights + interaction timeline |
| `search_call_transcripts` / `get_entity_evidence` | Verbatim buyer language with recording links + timestamps |
| `get_deal_strategy_evidence` | Deal-scoped receipts for whether relevant strategy entities appeared after a buyer signal |
| `qualify_company` / `enrich_person` / `find_person` | Segment classification, stakeholder verification and discovery |
| `list_motions` / `list_motion_icps` / `find_motion_icp` | The prescription: Motion ICP cell + `salesMethodology` stages |
| `list_motion_playbooks` / `get_motion_playbook` | Competitive / account / milestone / thematic prescriptions |
| `search_knowledge_base` / `list_entities` / `get_entity` | Objection counters, proof points, references, buying triggers |
| `list_revisions` / `list_suggestions` | Library change vector since last run |
| `list_gtm_reports` / `get_latest_gtm_report` / `get_report_run` | Segment/market intel change vector |
| `generate_email` / `generate_content` | Execution hooks for recommended actions |
| `asset_*` tools + asset-manager scripts | Publish/update the per-deal brief in place |
| `verify_connection` / `get_workspace_company` | Workspace identity for state scoping and brand |

## Error Handling

> **No CRM connection:** Run in account-level mode from conversation evidence; say the position is inferred, render deal-record fields as explicit gaps, and skip velocity/stakeholder gap types.

> **No conversation evidence (no calls, no emails):** CRM-only lane — actions can come from stage/velocity/stakeholder and change-vector gaps only. If the CRM is also absent, stop: "I can see your strategy for this cell but nothing about this deal. Connect a CRM or call recorder, or paste what you know."

> **No Motion ICP cell for this persona × segment:** Fall back to the nearest cell and the offering's playbooks; label every prescription citation with the fallback. Suggest creating the Motion cell — that is the durable fix.

> **Transcript search unavailable** (entitlement or no indexed calls): use `list_findings` + `get_event_detail`; quotes become paraphrases and are labeled as such.

> **Seeded/demo data detected** (`seed-*` ids, provider "generic"): never render as real numbers; coach from conversation evidence and say why.

> **MCP connection failed:** standard response in [octave-research-toolkit.md](../shared/octave-research-toolkit.md).

## Related Skills

- `/octave:pipeline` — interactive strategy session on one deal situation (stalled, competitive, executive)
- `/octave:signals` — workspace-wide morning briefing; this skill is per-deal and recurring
- `/octave:deal-coach` — methodology coaching microsite for a rep on one deal
- `/octave:meeting-prep` — the execution hook when the next action is a meeting
- `/octave:battlecard-doc` — the execution hook when the next action is competitive
- `/octave:asset-manager` — hosts and updates the per-deal briefs
