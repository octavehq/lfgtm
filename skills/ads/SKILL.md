---
name: ads
description: "Build ad campaign plans grounded in your Octave library. Generates ad sets with platform-ready creative, audience targeting, negative keywords, and landing page recommendations, every variant derived from an auditable source card built from real prospect language and proof points. Use when user says \"build an ad campaign\", \"create ads\", \"ad campaign for\", \"generate ad sets\", or asks for paid advertising creative. Do NOT use to analyze ad performance: use /octave:ads-resonance (the resonance loop) instead."
argument-hint: "[describe the campaign target and angle]"
---

# Octave Ads — Campaign Generation

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Resolve platform, objective, child advertising account, offer and CTA. Preserve paused defaults for exports. Google RSA exports require 3–15 headlines, 2–4 descriptions and final URL; five headlines is a recommendation. Meta/LinkedIn are copy-and-creative handoffs until their import schemas and media packages are verified. No-persist means no source-card file reads or writes.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

Use /octave:ads with the requested task, target, and output.

## References by task

- [google ads csv format](references/google-ads-csv-format.md)
- [google ads editor format](references/google-ads-editor-format.md)
- [html deck template](references/html-deck-template.md)
- [source card templates](references/source-card-templates.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.


- [creative.py](scripts/creative.py)
