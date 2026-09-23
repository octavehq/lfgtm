# Evidence hydration and Octave links

Use this reference when the digest includes quotes, companies, people, deals, citations, or links back to Octave.

## Evidence modes

### Evidence preview

Call `get_report_run` with `includeEvidence: { perSectionLimit: 3 }`, one run per call or up to 20 as `reportRunOIds` when the connected schema offers it. Use its per-section preview and evidence counts as the default for a completed-report recap. Keep claims at the level supported by the report. Do not turn a count of linked findings into a count of unique companies or deals.

### Selected quotes

For each important section:

1. Call `get_report_section_evidence` for the exact report section.
2. Hydrate promising events with `get_event_detail` when the returned preview lacks required context.
3. Use `search_call_transcripts` when verbatim, speaker-attributed language is required.
4. Keep only quotes whose wording and attribution can be verified.

If `get_report_section_evidence` is unavailable, search `list_findings` using the section topic, report window, and relevant filters. State that this fallback may not reproduce the report section's exact evidence set because semantic search is not the same as traversing the section-to-finding links.

## Investigative evidence

For an investigative digest, use the [research tool guide](research-tools.md) to measure the population and retrieve supporting events, findings, and transcript moments. Keep the [claim packet](evidence-packet.md) alongside the artifact. A completed report is optional.

- Match aggregate and drill-down selectors, windows, linkage, and eligible units. If a supporting quote comes from a different population, label it contextual rather than evidence for that cell.
- Verify who said the relevant words, not merely whether an external person attended the event. Inspect same-finding semantics and actual speaker metadata; unknown side stays unknown.
- Inspect `get_entity_evidence` linkage versus semantic fallback. Preserve source context and timestamps where available; a retrieval score is not an outcome effect or prevalence measure.
- Use `get_event_detail` or transcript retrieval for exact language. An extracted summary is not automatically a verbatim quote. Verify original wording and attribution before using quotation marks.
- Keep library positioning, graph-inferred relationships, seller statements, buyer observations, and external research separately attributed.
- Hydration failure narrows the affected claim. It does not authorize fabricating evidence or discarding independently verified findings.

## Evidence-worthiness gate

Evidence is optional, even when it is available. Include an item only when it:

- Supports, qualifies, or provides a material counterexample to the spread's main claim
- Adds specificity, tension, language, or context that the report summary does not already provide
- Is understandable without reconstructing the full conversation
- Has enough source context to avoid a misleading interpretation
- Is appropriate for the confirmed audience and privacy level

Prefer one strong receipt over several weak snippets. Cut generic labels, fragments, routine feature questions, seller monologues, repeated examples from the same event, and quotes chosen only because they sound colorful. Do not use a quote as decoration.

For each candidate, ask:

1. What claim does this support, qualify, or challenge?
2. What does the reader learn from it that they did not already know?
3. Would removing it weaken the argument?

If those answers are unclear, omit it. Paraphrase when the idea matters but the verbatim language is noisy. Label paraphrases as conversation summaries, never as quotes.

### Full receipts

Hydrate:

- Verbatim quote or exact quoted phrase
- Speaker and title when confirmed
- Company
- Event date and type
- Deal name, stage, amount, and outcome when available and relevant
- Recording or event link when the tool returns one

Deduplicate companies and events before reporting frequencies. Separate the number of findings, calls, companies, and deals. They are not interchangeable.

## Links back to Octave

Call `verify_connection` to resolve `organizationSlug` and `workspaceOId`.

For each report run, build:

```text
https://app.octavehq.com/o/{organizationSlug}/{workspaceOId}/insights?view=beats&reportRun={reportRunOId}
```

Use links only for internal readers who can access the workspace. Label them clearly, for example `View the full report in Octave`.

For public or customer-facing assets:

- Omit workspace links by default because recipients cannot open them.
- Include them only when the user confirms the audience has Octave access.
- Never expose raw oIds as reader-facing copy.

## Privacy gate

Before rendering named companies, people, quotes, or deal information, establish whether the artifact is:

- Internal
- Workspace-shared
- Restricted external
- Public

Internal does not mean unrestricted. Include only details that serve the argument. For external or public output, require explicit confirmation for private CRM and conversation details.
