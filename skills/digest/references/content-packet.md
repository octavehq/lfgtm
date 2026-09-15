# Digest content packet

Reuse approved scope in recurring/render-only runs; ask only unresolved content decisions. Actions and timelines remain conditional on the task and evidence.

### 1. Discover the available reports

1. Call `verify_connection`.
2. Call `list_gtm_reports`. If there is one obvious group, use it. If several are plausible, ask which group.
3. Call `get_latest_gtm_report` for the selected group.
4. Show a compact inventory with report title, period, and one-sentence delta. Do not dump the report prose.



### 2. Choose insight scope

For an interactive run, ask:

> Which insights should this digest include?
>
> 1. All reports in this period
> 2. A subset I choose
> 3. Pick the strongest connected story for me

For a subset, let the user select by displayed report title. For an editorial pick, choose reports that form one non-redundant narrative and briefly state the selection logic.

Fetch every selected report with `get_report_run` and set `includeEvidence: { perSectionLimit: 3 }`. Use this evidence preview for every section so the initial digest has inspectable support without requiring full hydration. Never build a multi-report digest from summary-only data.

When the user selects all reports, include every completed report returned for the period. Do not infer missing reports from the group's configured report count. If the configured and completed counts differ, state the completed count in the artifact and note the discrepancy during delivery.



### 4. Choose evidence depth

The default is the evidence preview returned by `get_report_run({ includeEvidence: { perSectionLimit: 3 } })`.

For an interactive run, ask whether the user wants to go beyond that preview:

> The digest will include a short evidence preview by default. Do you want detailed evidence too?
>
> 1. Preview only: evidence counts and a few supporting examples
> 2. Selected details: verified quotes and source context for the most important claims
> 3. Full receipts: quotes, companies, people, deal context, and source links where available

Explain that options 2 to 3 call `get_report_section_evidence` and may require additional event hydration, so they take longer and consume more tokens. Never fabricate precision to compensate for missing evidence.

Follow [evidence-and-links.md](evidence-and-links.md). Keep private deal or person details out of externally shared output unless the user explicitly confirms the audience and inclusion.

### 5. Choose content density

For an interactive run, ask:

> How should this digest read?
>
> 1. Executive: compressed conclusions, key evidence, and actions
> 2. Detailed: more of the reports' reasoning, examples, caveats, and section-level prose

Content density is separate from evidence depth. Detailed mode may use report prose without exposing named people, companies, deals, or verbatim quotes. Evidence privacy choices still apply.

In detailed mode:

- Start from the full `get_report_run` summary, comparison, and section details
- Preserve meaningful reasoning and concrete examples that explain why each conclusion holds
- Edit for coherence and remove repetition across overlapping reports
- Attribute each analytical section to its source report
- Add pages or slides instead of shrinking type, overfilling layouts, or turning prose into tiny cards
- Do not paste report text wholesale; shape it into a readable combined narrative



### 7. Build the content brief

Present for approval:

- Audience and decision the digest should support
- Digest name and stable slug
- Included reports and period
- Display date range. Show a timezone only when an exact timestamp boundary materially affects which evidence is included.
- Main conclusion
- Narrative arc
- Section or slide outline
- Content density
- Evidence mode and privacy assumptions
- Planned links back to Octave
- Whether to include a source appendix and “Chat with this insight” prompt

Wait for approval before generating visual output.

### 7b. Build each section from a table before writing it

Do not synthesize prose directly from the report summaries. For each included report, in order:

1. **Gather.** Put what the report observed into a structured table: the category (persona, competitor, use case, objection, call purpose), a count or frequency where the report supplies one, material counterexamples or rival explanations, and one or two named examples with verbatim language where the claim is about what people said. Use the workspace library's own entity names for personas, segments, use cases, and competitors; never coin a label ("technical owner," "the platform team") that does not exist in the library. If the report gives frequency only qualitatively ("most common"), carry it as qualitative and say that a count was not available.
2. **Derive.** Write the one-sentence takeaway the table supports, at the level of inference the evidence supports. If the table does not support a takeaway, the section says so and stays short.
3. **Decide.** When the evidence supports a specific action, write what a reader would change: a message, a material, a qualification rule, an enablement asset. Mark any item that is a change to the workspace library, so it can be filed as a suggestion rather than left as advice. If no change is warranted, say so briefly or omit the action panel.

Only then compose the spread. The table is its evidence layer, the takeaway is its title, an earned decision can be its closing panel. A section that skips the gather step is the one that ends up as a wall of text with no "so what."
