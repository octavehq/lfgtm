# digest: task method

## Choose the job and gather evidence

For a **completed-report recap**, use [content-packet.md](content-packet.md) to select and hydrate the requested runs. For an **investigation**, use [investigation-method.md](investigation-method.md) and [research-tools.md](research-tools.md); completed reports are optional inputs. Keep the user's questions as the spine. Confirm the workspace, reuse supplied scope and preferences, and raise only ambiguities that materially affect a population, claim, or recommendation. Continue independent work while those questions are pending.

Build the [evidence packet](evidence-packet.md) before the conclusion and outline. Gather observed counts and correctly attributed examples, derive the strongest supported takeaway, then recommend action only when earned. Useful directionality does not require statistical significance; associations do not establish cause. Apply [editorial-guidance.md](editorial-guidance.md) during writing and review.

Use [content-packet.md](content-packet.md) for the shared brief and [format-routing.md](format-routing.md) for rendering. Reuse supplied decisions; seek brief approval only when requested or a material decision remains unresolved. Evidence-display depth does not reduce the verification standard.

## Durable state and recurring execution

Store a workspace-scoped digest specification at .octave/digests/<workspaceOId>/<digestId>/spec.json. Use a stable opaque digestId; the display name is editable and not identity. Schema fields: schemaVersion, workspaceOId, companyOId, name, job mode, questions and business definitions, source/report IDs, selection rules, timezone, window boundaries, evidence depth, density, format, brand identity, approved audience/privacy/recipient scope, hosting artifact ID, and authorized recurrence settings. Store no credentials or short-lived preview links.

Record each execution in runs/<runId>.json: selected completed report-run IDs, source cutoff/window, hydration coverage, content checksum, status, output paths, artifact/version IDs, publication result, and unresolved inputs. Deduplicate execution with a key derived from workspace, spec version, report-run IDs and output format. Acquire an exclusive per-digest run lock; a concurrent invocation reports the active run rather than publishing again. An expired lock requires reconciliation of the previous run before retry.

For report recaps, select completed reports only. Commit the consumed-report checkpoint after the intended output is verified; preserve partial-run state on failure. If the same report set has already been published, return the existing verified artifact. For a recurring report recap, if no new completed material exists, record “no new material” and do not publish a recycled digest. After a timeout, inspect the recorded artifact/version and checksum before retrying a write.

For investigations, record query scope, source cutoff, and evidence version/checksum in the run identity instead of relying on an empty report ID list. The report checkpoint helper applies to report-backed runs; do not invent support for an investigation checkpoint.

Initial setup resolves missing scope/format/privacy and scheduling authorization. Interactive one-off runs can request content decisions that remain open. Authorized recurring runs reuse their saved configuration and perform the same evidence/content/render checks without asking routine intake again. A broadened audience, new recipient, changed privacy, missing required input, or unresolved sensitive-content decision pauses only the dependent publication and records the question. Continue independent drafting. Do not interpret elapsed time as approval.

Pass downstream renderOnly=true, the approved content packet, allowed transformations, brand, requested format, CTA/navigation needs, and authorized distribution. A renderer must not rerun strategy intake or silently change the findings. Apply its format-specific validator: a magazine's spread/nav checks are not automatically appropriate to an executive brief.

For each finding, retain report/run/source IDs, inspected evidence, date/window, entity affected, evidence strength, and known limits. Preserve separate counts for reports, findings, calls/events, companies and deals; deduplicate by stable IDs within the declared unit. A snippet preview is an inspected sample, not the population denominator. State overlap and coverage; do not infer market prevalence from a few visible quotes.

When actions are requested, compare the finding with the current offering and relevant Motion/Playbook/persona × segment. Produce: recommended owner role, exact change/test, affected audience/channel, supporting evidence, expected mechanism, and validation measure. Label this recommendation separately from the source report. Do not amplify a stale product claim. For example, a recurring pricing objection should yield a specific discovery/message test and success criterion, not “improve messaging.”
