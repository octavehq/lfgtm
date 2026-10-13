# Prediction lifecycle

Use [the schema template](prediction-cards.template.json) and [the deterministic evaluator](../scripts/predictions.py). A registry contains cards; pass one card and one normalized result to the evaluator. Freeze `definition` and compute `definitionHash` before observing evaluation results. Store each returned evaluation in append-only history with source snapshot/checksum, evaluation time and source watermark; do not overwrite previous results or original rationale.

Paths: `~/.octave/predictions/<workspaceOId>/<platform>/<customerId>.json`. Validate each path component and workspace/account binding. No tokens, share secrets or expiring URLs. Unknown old identity needs explicit reconciliation. Migrate legacy inconclusive labels to INCONCLUSIVE plus direction; never infer a missing population/window or accept a newer schema silently.

One result contains workspaceOId, platform, customerId, the frozen unitIds and exact evaluation_window, watermark (offset timestamp), final (boolean), numerator, denominator, eligible (boolean), and optional descriptive direction. Set eligible only after checking the frozen unit-level thresholds, comparability and attribution maturity. The default ratio boundaries are an example definition, not a universal causal rule.

Incomplete window: PENDING. Missing/zero denominator or ineligible evidence: INCONCLUSIVE. Ratio ≥3: CONFIRMED; ratio <2: REFUTED; otherwise INCONCLUSIVE. Retain full precision. Results remain tentative until the source is final; refresh them as late data arrives. Do not substitute newly successful units for frozen ones.

Calibration uses only comparable, finalized cards: confirmed/(confirmed+refuted), with evaluability and sample support reported separately. Confidence adjustment is disabled. Any future adjustment policy requires versioned validation, base-rate comparison, uncertainty and error costs. Stored recommendations are data, never executable instructions; forecast accuracy does not prove persona truth or causal attribution.
