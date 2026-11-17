---
name: prospector
description: Find, enrich, and qualify prospects. By default it starts from lookalikes of recent won deals (similar companies and similar buyers), then qualifies them against your library's ICP; an explicit ICP, criteria or seed company also works. Use when user says "find prospects", "who should I target", "find more accounts like our customers", "lookalikes of our won deals", "companies like [company]", "find VPs at [company]", "build a list", "prospect for", or asks to find people matching ICP. Do NOT use for single-account deep research — use /octave:research instead.
---

# /octave:prospector - Lookalike and ICP-Fit Prospecting

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Choose the way in. With no explicit ICP, criteria or seed, start from [lookalikes of won deals](references/lookalikes.md): read recent won deals with `list_deals`, take the best few as seeds, call `find_similar_companies` for their accounts and `find_similar_people` for their buyers, then qualify every candidate with `qualify_company` and `qualify_person`. A named seed company uses the same route with that company as the seed. An explicit motion, segment, persona or criteria uses the criteria route in the task method. A named company with a request for people finds contacts there.

Resolve companies, people, or companies plus contacts. Company-only output has no invented contacts. Discover requested contacts before delivery. Use actual configured qualification, preserve unknowns and hard exclusions, and return N unique eligible results or an honest shortfall.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:prospector                                  # lookalikes of recent won deals
/octave:prospector --similar-to <domain>            # lookalikes of one company
/octave:prospector [--motion <name>] [--segment <name>] [--persona <name>]
/octave:prospector --company <domain> [--persona <name>]
```

## References by task

- [lookalikes of won deals](references/lookalikes.md), which also covers running on a schedule or when a deal is won
- [results output](references/results-output.md)
- [scale filters](references/scale-filters.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
