---
name: magazine
description: Turn a subject or supplied content into an editorial magazine with a cover, contents and a few full-screen spreads to swipe through, as self-contained HTML. Use when user says "make a magazine", "magazine about", "turn this into a magazine", "editorial recap", or wants a period, a theme or a body of findings told as a story people will want to read. Do NOT use for a recurring digest of Octave reports; use /octave:digest.
---

# /octave:magazine - Editorial Magazine

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill.

This is an output skill: it says how a magazine is shaped and written, for any subject. It holds no opinion about which evidence a subject needs. When a job skill fits the request (meeting prep, a battlecard, an account plan, a win/loss review), run that skill and let it use this one for the shape.

Resolve whether content is supplied or only a subject is given, then the story: a period recapped, a theme explored across accounts, or one account or deal told from start to now. A magazine is for material with a story and voices in it. If the content is a list of facts with no arc, a document serves it better; say so and offer one.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A render-only handoff of finished content does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:magazine <subject or content> [--for <purpose>] [--style <preset>]
```

## References by task

- [task method](references/task-method.md): the two ways in, the narrative patterns by purpose, what to cut
- [magazine format](../shared/formats/magazine.md): structure, layout and the review checklist
- [magazine base styles](../shared/formats/magazine-base.css): the spread scaffold
- [information principles](../shared/information-principles.md): what leads, how evidence is shown
- [editorial rules](../shared/editorial-rules.md): how it is written

Read the task method first, then the format reference when rendering.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.
