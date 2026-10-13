---
name: qual-doctor
description: Diagnose and tune qualification agents by testing against known-fit prospects, analyzing per-question scoring patterns, and recommending specific changes to questions, weights, and entity descriptions. Use when user says "tune my qualification", "qual doctor", "fix qualification scores", "qualification isn't working", "scores are off", "tune scoring", or asks to improve how qualification agents score prospects.
argument-hint: "[no args — the skill is fully interactive and walks through agent selection, section picking, test case collection, and diagnosis]"
---

# /qual-doctor - Qualification Agent Tuner

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Verify workspace and actual saved-agent configuration. Preserve raw answers alongside evidence states; absence is not verified No. Use diagnostic and held-out cases and inspect shared-agent impact. Apply only the authorized tested change and read it back. Pricing/usage estimates come from available current metadata; otherwise state unavailable.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

Use /octave:qual-doctor with the requested task, target, and output.

## References by task

- [per mismatch deep dive templates](references/per-mismatch-deep-dive-templates.md)
- [wrap up summary templates](references/wrap-up-summary-templates.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.
