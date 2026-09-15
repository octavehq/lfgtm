---
name: asset-manager
description: "Publish and manage hosted websites and file bundles on the Octave assets service. Upload or update files, manage privacy and shares, inspect access requests and visits, configure vanity URLs, restore versions, download, list, or delete an identified asset. Use for hosting and asset management, including recipient-restricted microsites; use the content skills to author the material."
---

# /octave:asset-manager - Publish & Manage Hosted Assets

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Manage hosted website/storage artifacts with verified workspace and artifact identity. Use an explicit publish manifest for public bundles. Read back metadata, version and file manifest after writes. An indeterminate write requires reconciliation before retry. Preserve old local files on failed downloads; document the residual race when the service lacks compare-and-swap.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:asset-manager                       # Interactive - asks what to do
/octave:asset-manager publish <path>        # Publish a folder, file, or .zip
/octave:asset-manager update <identifier>   # Replace files or change metadata
/octave:asset-manager share <identifier>    # Create/manage share links
/octave:asset-manager versions <identifier> # Version history, rollback, pinned URLs
/octave:asset-manager requests              # Access-request inbox (grant / dismiss)
/octave:asset-manager stats <identifier>    # Visits, downloads, who opened it
/octave:asset-manager list                  # List published assets (from registry)
/octave:asset-manager download <identifier> # Download an asset's files locally
/octave:asset-manager delete <identifier>   # Delete an asset (confirms first)
```

## References by task

- [script usage](references/script-usage.md)

- [operations](references/operations.md)


Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

Resolve these paths from the installed skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- [artifact_io.py](scripts/artifact_io.py)
- [download-artifact.sh](scripts/download-artifact.sh)
- [update-artifact.sh](scripts/update-artifact.sh)
- [upload-artifact.sh](scripts/upload-artifact.sh)
- [zip-and-upload-artifact.sh](scripts/zip-and-upload-artifact.sh)
