---
name: win-loss-report
description: Generate visual win/loss analysis reports as self-contained HTML with CSS-based charts and data visualizations. Use when user says "win/loss report", "deal report", "visual analysis", or wants a formatted HTML version of deal outcome analysis. Do NOT use for text-based deal analysis — use /octave:win-loss-report instead.
---

# /octave:win-loss-report - Visual Win/Loss Report Builder

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Use a normalized close-date cohort and one metric model for text, cards and charts. Use four sections: cohort/outcome summary, drivers and counterevidence, segment/competitor comparisons, interventions to test. Observed loss associations do not establish preventable losses.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:win-loss-report [--period <timeframe>] [--segment <filter>] [--competitor <name>] [--style <preset>]
```

## References by task

- [html architecture](references/html-architecture.md)
- [outline template](references/outline-template.md)
- [sections](references/sections.md)
- [tool reference](references/tool-reference.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
