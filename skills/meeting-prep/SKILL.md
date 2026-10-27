---
name: meeting-prep
description: Strategic meeting prep grounded in lookalike deals. Opens with the closest won and lost deals and what happened on their calls, charts what each attendee is likely to raise, names the approved content to bring, structures the pitch around the company's own framework when one exists, and ends on the next best action (the move, why now, the strategy behind it, and the follow-through). Rendered as self-contained HTML, or as Markdown in chat and agent hosts, with copy-ready prompts to continue. Use when user says "meeting prep", "battle plan", "prep me for my meeting", "prep for my call", "what should I expect from this meeting", "deals like this one", or wants a coached game plan for an upcoming meeting. Do NOT use for account reference documents; use /octave:research instead.
---

# /octave:meeting-prep - Strategic Meeting Prep

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Infer meeting type and duration. Use one content schema: lookalikes, context, goals, competitive, expect, content, say-ask, next-action, in that order, then the keep-going prompts. The outline, HTML IDs, review, and delivery summary use meeting-sections.md. The scaffold supplies layout, not a second content schema.

Resolve the account and deal first, then lead the analysis with seeded `ask_octave` calls about the account and its lookalike deals, and verify what they cite with the narrow tools. The two sections that set this prep apart, lookalike deals and the next best action, are built by [lookalikes and expectations](references/lookalikes-and-expectations.md) and [strategy gap](references/strategy-gap.md). Never invent quotes, numbers, customers, roles or content; counts carry their base; other customers stay internal.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>]
```

## References by task

- [lookalikes and expectations](references/lookalikes-and-expectations.md)
- [strategy gap](references/strategy-gap.md)
- [html scaffold](references/html-scaffold.md)
- [meeting sections](references/meeting-sections.md)
- [output rules](references/output-rules.md)
- [positioning coach](references/positioning-coach.md)
- [strategic coach](references/strategic-coach.md)

Read the lookalike and strategy-gap references for every full prep run, the positioning references only when choosing an approach, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Deliver the asset id or URL when the prep was published and the copy-ready "keep going" prompts described in meeting-sections.md, so a user or agent can fetch the prep through the Octave MCP and continue. In a host that cannot render HTML (ChatGPT, Claude chat, an internal agent), deliver the same sections as Markdown.

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
