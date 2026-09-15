---
name: battlecard-doc
description: Create competitive battlecards in HTML or text for a specific deal, a reusable competitor reference, or a full landscape. Use for battlecards, competitor comparisons, competitive reference documents, and evidence-based objection preparation. Reusable and landscape comparisons do not require an account.
---

# /octave:battlecard-doc - Visual Competitive Battlecard

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Select deal-specific, reusable competitor, or landscape; --competitor all implies landscape. Reusable and landscape modes require no account. HTML and text use the same comparison record; text does not route back to this skill.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:battlecard-doc [--competitor <name(s)>]
```

## References by task

- [html architecture](references/html-architecture.md)
- [landscape sections](references/landscape-sections.md)
- [single competitor sections](references/single-competitor-sections.md)
- [tool reference](references/tool-reference.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
