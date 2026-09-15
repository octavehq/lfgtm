# Signals brief

Scope strip: workspace, active CRM roster/as-of, event window and history, per-detector coverage, configured heuristics and missing sources.

For each supported signal show: exact opportunity/account ID in the internal working record; observed change and dates; prior baseline; why it matters to this offering/motion; confidence/limits; evidence and alternative explanation. Keep account context separate from opportunity-specific events.

Distinguish new, continuing, resolved and baseline-only states. Store schemaVersion 1, workspaceOId, asOf, detector configuration, source coverage, opportunity IDs, prior observations and last emitted signal keys at `.octave/signals/<workspaceOId>/state.json` using [workspace_state.py](../../shared/scripts/workspace_state.py). No previous state means no novelty claim. An unknown read does not resolve an old alert.

Prioritize at most three grounded actions: owner, exact next step, timing/condition and success criterion. Respect buyer-agreed pauses. Competitor mentions require relevant buyer context; message usage is not effectiveness. No active roster or missing historical coverage produces a clear detector limitation, not false inactivity.

Use [the task method](task-method.md) for detector definitions and prerequisites.
