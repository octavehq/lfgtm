---
name: deck
description: Octave-powered presentation builder that researches, structures, and generates self-contained HTML slide decks. Use when user says "build a deck", "create a presentation", "pitch deck", "QBR slides", "sales deck", or asks for slides on any topic.
---

# /octave:deck - Octave-Powered Deck Builder

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Select the actual decision narrative. QBR/renewal/value reviews use goals versus results and an auditable claim ledger; a pitch may use problem/solution/proof/ask. Use the complete presentation controller; check the actual requested HTML/PDF/PPTX export before reporting it ready.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:deck [topic or file] [--for <purpose>] [--audience <target>] [--style <preset>]
```

## References by task

- [pptx conversion](references/pptx-conversion.md)

- [animation patterns](references/animation-patterns.md)
- [export guide](references/export-guide.md)
- [html scaffold](references/html-scaffold.md)
- [slide templates](references/slide-templates.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

Resolve these paths from the installed skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- [presentation.js](assets/presentation.js)
