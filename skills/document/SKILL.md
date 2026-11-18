---
name: document
description: Turn a subject or supplied content into an interactive doc, a designed page that scrolls top to bottom with charts, timelines and quotes where the evidence calls for them, as self-contained HTML or Markdown. Use when user says "write this up", "make a report on", "turn these notes into a document", "long-form document about", or asks for a readable write-up with no more specific deliverable in mind. Do NOT use when a job skill fits the request (meeting prep, battlecard, account plan, win/loss report, proposal); use that skill.
---

# /octave:document - Long-Form Document

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill.

This is an output skill: it says how a long-form document is shaped and written, for any subject. It holds no opinion about which evidence a subject needs. When a job skill fits the request (meeting prep, a battlecard, an account plan, a win/loss review), run that skill and let it use this one for the shape.

Resolve whether content is supplied or only a subject is given, then the purpose: a decision to make, findings to absorb, a plan to follow, or a review of what happened. The purpose picks the narrative pattern in the task method. Default to HTML where the host can render it and Markdown in chat.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A render-only handoff of finished content does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:document <subject or content> [--for <purpose>] [--style <preset>]
```

## References by task

- [task method](references/task-method.md): the two ways in, the narrative patterns by purpose, what to cut
- [HTML document format](../shared/formats/html-document.md): structure, layout and the review checklist
- [information principles](../shared/information-principles.md): what leads, how evidence is shown
- [editorial rules](../shared/editorial-rules.md): how it is written

Read the task method first, then the format reference when rendering.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.
