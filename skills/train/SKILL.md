---
name: train
description: "Onboarding GTM primer generator. Produces a self-contained, interactive slide lesson a new rep works through to learn the whole go-to-market: what we sell, who we sell to, how to position to each buyer, who we compete with, and proof, with checkpoint questions they must clear to advance and a score at the end. Use when user says \"onboarding primer\", \"GTM primer\", \"onboard a new rep\", \"ramp doc\", \"train a new hire\", or \"GTM 101\"."
argument-hint: "[--personas <name,name,...>] [--style <preset>]"
---

# /octave:train - Onboarding GTM Primer

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Teach the rep’s agreed remit across relevant offerings and motions. Use zero to three approved examples as available; proof is not a guarantee. The lesson uses the slide-deck gate and the executable lesson controller. Per-deal coaching routes to deal-coach.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:train [--personas <name,name,...>] [--style <preset>]
```

## References by task

- [html scaffold](references/html-scaffold.md)
- [primer sections](references/primer-sections.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

Resolve these paths from the installed skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- [lesson.js](assets/lesson.js)
