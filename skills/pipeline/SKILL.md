---
name: pipeline
description: Deal-level strategy for live deals — diagnosis, stakeholder strategy, and next-step recommendations. Use when user says "help with this deal", "deal is stalled", "how do I close this", "competitive deal", "multi-thread", or mentions a specific stuck deal. Do NOT use for methodology practice or coaching assets (role-play, coaching decks, quizzes) — use /octave:deal-coach instead.
argument-hint: "[stalled|multi-thread|competitive|executive|close|expand] <account> [--contact <email>] [--competitor <name>]"
---

# /octave:pipeline - Deal Strategist

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Own live opportunity strategy. Select stalled, competitive, multi-thread, executive, close, or expand; read only that mode reference. Deal-coach handles structured deal rehearsal; train handles onboarding. Generic practice stays conversational.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:pipeline [mode] <account> [--contact <email>] [--competitor <name>]
```

## References by task

- [mode close output](references/mode-close-output.md)
- [mode competitive output](references/mode-competitive-output.md)
- [mode executive output](references/mode-executive-output.md)
- [mode expand output](references/mode-expand-output.md)
- [mode multi thread output](references/mode-multi-thread-output.md)
- [mode stalled output](references/mode-stalled-output.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
