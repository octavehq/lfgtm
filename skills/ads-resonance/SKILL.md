---
name: ads-resonance
description: Analyze ad performance and feed the learnings back into your Octave library — the resonance loop. Pulls performance data from Google Ads MCP, BigQuery Data Transfer, direct API, or manual paste; maps winners back to the source cards behind each ad variant; generates library update recommendations and a sales intelligence brief; writes falsifiable prediction cards and accumulates a calibration track record over time. Use when user says "analyze ad performance", "resonance loop", "score predictions", "evaluate my ads", or asks to turn ad performance into GTM intelligence. Do NOT use to build a new ad campaign — use /octave:ads instead.
argument-hint: "[--min-impressions N] [--min-clicks N] [--min-conversions N] [--mode smoke-test|ad-group|ad|full-resonance]"
---

# Octave Ads Resonance Loop — Performance → Library Intelligence

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Support connected API, CSV and BigQuery inputs. Scope every record to verified workspace/platform/customer IDs. Use exact creative membership or a unique complete fingerprint; never join on a headline alone. Use the deterministic prediction reducer. No automatic strategic writes, confidence promotion, CPC-based pausing, or budget transfers.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

Use /octave:ads-resonance with the requested task, target, and output.

## References by task

- [performance data sources](references/performance-data-sources.md)
- [prediction cards](references/prediction-cards.md)
- [prediction dashboard template](references/prediction-dashboard-template.md)
- [resonance report template](references/resonance-report-template.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

Resolve these paths from the installed skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- [predictions.py](scripts/predictions.py)
