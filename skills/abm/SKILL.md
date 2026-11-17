---
name: abm
description: Account-based planning for one company or for a cohort. For a named company it maps stakeholders, matches personas and plans coordinated outreach. For a segment, a cohort or a list of accounts it writes a cohort plan with who is in it, the one angle they share (from won deals that look like them), tiers, and the plays per tier. Use when user says "plan for [company]", "account plan", "stakeholder map", "ABM strategy", "campaign for this segment", "ABM campaign", "plan these accounts", "tier this list", or mentions targeting a specific named company or a named segment. Do NOT use to find new accounts; use /octave:prospector instead.
---

# /octave:abm - Account and Cohort Planner

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

A request that names one company gets an account plan. A request that names a segment, a cohort or a list of accounts gets a cohort plan from [cohort plan](references/cohort-plan.md): who is in it and why they belong together, the one angle they share, tiers, and the plays per tier, ending on how the per-account plans are run. A cohort plan names no committee for an individual account.

For an account plan, Quick covers the strongest entry route, up to three primary roles, one sample email, and next actions. Full covers the requested committee count or reports the discovery shortfall. Assemble outreach before rendering and review.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:abm <company> [--stakeholders <N>] [--motion <name>] [--depth quick|full]
/octave:abm --segment <name> [--motion <name>]
/octave:abm --accounts <domains or file> [--motion <name>]
```

## References by task

- [cohort plan](references/cohort-plan.md)
- [account plan template](references/account-plan-template.md)
- [html scaffold](references/html-scaffold.md)
- [regression checklist](references/regression-checklist.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
