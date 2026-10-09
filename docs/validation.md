# Plugin validation and release readiness

## Local and CI checks

From the source checkout:

```bash
python3 -m pip install -r requirements-validation.txt
python3 -m playwright install chromium
npm ci --ignore-scripts
bash scripts/validate.sh
```

Core helpers require Python 3.10+; builds also need bash and jq. Asset scripts
need curl. The browser suite uses pinned Playwright/Chromium and Pillow. Source
and both generated packages must pass resource-closure checks. Tests use
synthetic data, mocked HTTP, and offline pages; no customer writes occur.
Temporary output lives outside the repository and is removed after tests.

CI runs these checks on pull requests. Downstream mirroring and the rolling
Claude ZIP release depend on the same validation workflow. Release ZIPs use a
tracked runtime allowlist instead of recursively uploading the checkout.

## What the checks establish

- Artifact wrappers work without jq, with dotted output ancestors, quoted JSON
  and null previews. Manifest/readback, traversal, symlink, indeterminate-write
  and per-file atomic-download behavior have deterministic coverage.
- Brand links preserve destinations and escaping. Unsafe SVG/URLs, missing
  assets and mismatched identity fail validation. The generic block fixture is
  checked at 375/768/1440 px; viewport-only OG capture is 1200×630 px.
- Lesson navigation, checkpoint gating, wrong-answer progression, reset,
  independent tabs and print visibility run in Chromium. Deck navigation,
  editing and downloaded HTML run in Chromium. Microsite reveal failures keep
  content visible.
- Workspace state, interrupted locks, repeated digest runs, prediction
  boundaries, attribution isolation, CSV quoting and normalized metrics have
  synthetic regressions.

These checks do not establish live service access, customer-specific source
fidelity, model judgment quality, platform import acceptance or conversion
fidelity for an arbitrary PDF/PPTX. Record those as NOT RUN until actually tested.

## Behavioral evaluation matrix

Run the relevant skill using only its current instructions, the user request,
and raw fixture evidence. Include a normal case, a sparse/degraded case, and
the highest-risk case below. Do not provide the expected answer to an evaluating
agent. Preserve the generated artifact, input turns, observed outcome and rubric
outside the public repository; source fixtures here must be synthetic or cleared
for publication. An unexecuted scenario is a pending check, not a pass.

Use materially different customer contexts: a single-offering software firm;
a suite with separately contracted modules and shared buyers; a services firm;
a displacement motion; a sparse early-stage library; a multi-region enterprise.
Provide source dates, stable synthetic IDs, actual versus hypothetical claims,
and explicit external-use status. Include a second input turn with missing
commercials, POC or usage data where it matters.

| Skill | Normal / sparse case | Highest-risk case |
|---|---|---|
| research | Discovery or demo / absent proof | QBR receives missing results on turn two; no reference result becomes realized value |
| abm | Known account / candidates only | A library trigger with no occurrence cannot become a congratulatory email; full count is honored |
| pipeline | Opportunity coaching / incomplete history | Two opportunities at one domain retain different blockers and buyer-agreed pauses |
| meeting-prep | Discovery meeting / unknown workflow | Replacement and service offers do not inherit a context-layer pitch; six sections agree |
| deal-coach | Committee rehearsal / absent CRM | Real cash cap or better-fit rival permits defer/no-fit; no invented stage probability |
| champion-deal-room | Committee case / qualitative value | Restricted seller notes stay private; freed hours are not automatically cash savings |
| generate | One follow-up / no saved agent | All engines preserve the same claims, scope and requested count |
| prospector | Account or contact list / limited discovery | Hard disqualifier survives a high score; unknown evidence stays unknown; CSV round-trips |
| train | Rep remit / zero approved examples | Multiple offerings/motions remain distinct; omitted slides and wrong answers do not break navigation |
| positioning | Full system / missing proof | Narrow persona edit preserves other cells; customer operations are not a prospecting lifecycle |
| product-launch | Launch kit / unknown date or price | Corrected eligibility/pricing propagates to every requested asset before delivery |
| ads | Campaign creative / qualitative proof | No-persist performs no file I/O; quotes retain provenance; preview assets remain within one RSA |
| ads-resonance | API or CSV analysis / small units | Duplicate headlines across workspaces cannot cross-match; new units cannot rescue frozen predictions |
| battlecard-doc | Reusable or deal card / unknown rival feature | Legitimate competitor advantage is conceded; landscape needs no invented account |
| insights | Scoped question / sampled retrieval | Seller usage is not buyer resolution; a failed detail read is not a library gap |
| signals | Active roster / missing history | No baseline means no novelty claim; agreed pause does not become escalation |
| win-loss-report | Closed cohort / missing outcomes | Reopened deals deduplicate; 9/14 is 64.3%; loss association is not preventability |
| icp-refine | Pursued/closed cohorts / small samples | Missing champion/budget is not anti-ICP; holdouts expose tuning overfit |
| call-analyzer | Complete transcript / partial speakers | Skepticism may be engagement; no fabricated ICP score or buyer commitment |
| deck | Pitch/QBR / missing usage | Operator answers update dependent figures; exported file is opened and inspected |
| one-pager | Web leave-behind / one qualitative proof | Physical Letter/A4 output is exactly one readable page; sender brand persists |
| proposal | Completed proposal / requested scaffold | Missing seller inputs are collected; intentional future POC measurements may remain open |
| microsite | Named account or industry / no JS | Restricted proof uses the right host; renderOnly preserves the approved digest hierarchy |
| digest | One-off / no new reports | Concurrent or uncertain runs reconcile; changed recipients cannot inherit old distribution approval |
| brand kit | Light/dark visual kit / missing font | Wrong-domain, unsafe SVG and interrupted refresh cannot replace a valid cache |
| asset-manager | Create/update/download / null preview | Public bundle excludes notes; interrupted download preserves old file; readback detects wrong target |
| library | List/create/update / missing page | Scoped Motion edit preserves protected cells; no-op/partial write is not called complete; approved copy written with `verbatim: true` reads back character-for-character and an ambiguous field mapping is asked, not guessed |
| audit | Structural and semantic review / failed read | Separate commercial offerings survive shared-buyer heuristics; no archive before verified migration |
| qual-doctor | Diagnostic plus holdout / no score trace | Absence does not become exclusion; shared agents are checked and raw answers retained |

Evaluate task correctness, source fidelity, offering/buyer relevance, handling of
uncertainty and operator replies, audience suitability, usable final output,
scoped mutation/readback and routing. Test cases and human judgment complement
the deterministic suite; they cannot be replaced by a keyword-presence test.

## Integration checks before claiming production verification

- Asset access matrix: owner, workspace member, explicit share recipient and
  anonymous × only_me/workspace/public × published/unpublished. Verify effective
  routes and existing share grants. Do not infer access from a preview label.
- Asset concurrency: verify the supported API's version/idempotency semantics.
  The client snapshot/reread detects observed changes but has a residual race;
  it does not implement server-side compare-and-swap.
- Workspace tools: test current read/write schemas, pagination, protected-field
  readback, no-op/partial writes and shared-agent effects in a controlled workspace.
- Platform exports/analytics: import into a verified child account in paused
  state; dry-run actual BigQuery schemas and reconcile full key sets and metrics.
  Local CSV validation does not establish platform acceptance.
- Installed hosts: check Claude, Codex and Cursor installation/discovery and
  optional runtimes. Packaged reviewer instructions do not imply native host
  subagent registration; sequential review is the documented fallback.

Maintainers own deterministic/package gates; reviewers of a release own the
applicable behavioral and integration acceptance record. Do not label an entire
plugin production-verified solely because its source and browser fixtures pass.

## Compatibility notes

- Brand CTA/nav/footer inputs use `{label, href, target?}`; text items explicitly
  use `{type: "text", label}`. `url` is accepted only as a nonconflicting href
  alias. Inert strings/buttons now fail rather than silently losing destinations.
- New brand captures bind full hostname/TLD and verified workspace, store
  provenance/checksums/allowed use, and promote immutable versions through an
  atomic `current.json` pointer. Existing aliases need verified identity.
- Source cards and prediction registries use schema 0.3 and workspace/account
  identity. Legacy files remain unbound until explicitly reconciled; no fuzzy
  name/headline migration or automatic strategy promotion occurs.
- Public uploads require an explicit approved file manifest, including updates
  to an already-public asset and ZIP uploads. Asset helpers use environment
  configuration and do not source a local `.env` file.
- Download overwrite is explicit. Historical non-ZIP downloads use `.bin` until
  their actual format is identified. No extension or export fidelity is invented.
