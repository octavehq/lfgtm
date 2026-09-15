---
name: get-brand-components
description: Capture a brand's visual design system from its website and build a reusable component kit. Walks key pages on a domain (screenshots + HTML via the Octave scrape tool), derives design tokens (colors, type, spacing, radius, shadow), and produces a minimal component library (buttons, cards, headers, stats, tables, badges, hero, footer) as a self-contained HTML reference plus CSS tokens. Use when the user says "get brand components", "capture the brand", "build a component kit for [domain]", "make outputs look like [company]", wants other skills to generate on-brand HTML for a target company, or wants to reuse an already-published brand kit from the asset store or host/share a kit as a live link (via asset-manager).
argument-hint: <domain-or-url> [refresh] | list | show <slug> | export <slug> | delete <slug>
---

# Get Brand Components — Brand-to-Component-Kit Builder

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Capture only the visual system: logos, colors, typography, layout, assets, components and visual usage rules. Keep voice, proof and messaging outside the kit. Preserve source fidelity; dark surfaces do not imply glow. Validate a staged kit before promoting its canonical domain/workspace identity.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:get-brand-components <domain-or-url>     # Walk the site and build a brand component kit
/octave:get-brand-components <domain> refresh    # Force a fresh re-walk, overwriting the cached kit
/octave:get-brand-components list                # List saved brand kits
/octave:get-brand-components show <slug>         # Display a saved kit (and open the gallery)
/octave:get-brand-components export <slug>       # Zip the cached kit to ~/Desktop/<slug>-brand-kit.zip
/octave:get-brand-components delete <slug>       # Remove a saved kit
```

## References by task

- [cache operations](references/cache-operations.md)

- [renderer contract](references/renderer-contract.md)

- [capture workflow](references/capture-workflow.md)

- [asset review](references/asset-review.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

Resolve these paths from the installed skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- [check_adherence.py](scripts/check_adherence.py)
- [kit_validation.py](scripts/kit_validation.py)
- [render.py](scripts/render.py)
- [render_kit.py](scripts/render_kit.py)
- [verify-logos.sh](scripts/verify-logos.sh)
- [verify_logos.py](scripts/verify_logos.py)
- [kit_base.css](assets/kit_base.css)

- [brand_cache.py](scripts/brand_cache.py)
