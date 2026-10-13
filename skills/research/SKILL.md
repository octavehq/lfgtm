---
name: research
description: Context-aware research and prep for calls, meetings, demos, outreach, and deal reviews. Outputs plain text (default) or a styled, scannable HTML document. Use when user says "research [company]", "prep for my call", "who is [person]", "meeting prep", "demo prep", "brief me on [company]", "account dossier", or asks to research a company or person. Do NOT use for bulk prospecting — use /octave:prospector instead. Do NOT use for customer-facing documents — use /octave:one-pager or /octave:proposal instead.
---

# /octave:research - Context-Aware Research & Prep

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Infer discovery, demo, follow-up, outreach, QBR, executive, deal-review, or general from the request. Text is the default; HTML adds visual checks. Use occasion-workflows for the selected occasion.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:research <target> [--for <occasion>] [--format text|html] [--style <preset>]
```

## References by task

- [brief html architecture](references/brief-html-architecture.md)
- [demo prep](references/demo-prep.md)
- [discovery call prep](references/discovery-call-prep.md)
- [occasion workflows](references/occasion-workflows.md)
- [outreach prep](references/outreach-prep.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
