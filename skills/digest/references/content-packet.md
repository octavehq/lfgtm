# Digest content packet

### 1. Establish scope and discover sources

1. Call `verify_connection` and confirm the intended workspace. Recheck identity after a reconnect before continuing retrieval.
2. Establish audience, decision, exact period, job mode, and relevant business definitions from the request and existing context. Distinguish questions from hypotheses. Ask early when unresolved meaning would materially change a population, claim, or recommendation; explain why and recommend a resolution. Continue independent work while the affected claim waits.
3. For a recap, use `get_latest_gtm_report` only if its period matches the request. For any other period, call `list_report_runs`: with no arguments it lists the Weekly Beats group's runs across every config, newest window first; pass `groupOId` for another group or `configOId` for one report, and page with `limit` and `offset` until the requested window is covered. Select the runs whose windows fall inside the period and keep skipped or failed runs in the inventory as explained gaps; do not substitute the latest period. Call `list_gtm_reports` when the group or its reports must be named first: each group lists its `configs[]`. Show a compact inventory of titles, periods, statuses, and supported deltas.
4. For an investigation, inspect available tool schemas and source coverage using the research guide, then gather the evidence needed for the user's questions. Do not require an existing completed report.

### Interactive and recurring modes

Determine the run mode before intake:

- **Interactive setup or ad hoc run:** use the questions below only for unresolved preferences that affect the result. Bundle them where helpful; reuse supplied answers and judgment authorization. A request for a local artifact does not require hosting or scheduling intake.
- **Scheduled run with a saved digest specification:** resolve its stable digestId within the workspace and load it and reuse the saved selection rule, evidence depth, format, audience, brand, hosting, timezone, URL behavior, and delivery destination. Do not ask the setup questions again.
- **Scheduled run with missing or invalid configuration:** pause only for the missing decision. Save the answer back to the digest specification for future runs.

Treat an explicit instruction in the current request as an answer. Do not ask the user to repeat information they already supplied.

### 2. Choose insight scope

For a recap with unresolved scope, ask:

> Which insights should this digest include?
>
> 1. All reports in this period
> 2. A subset I choose
> 3. Pick the strongest connected story for me

For a subset, let the user select by displayed report title. For an editorial pick, choose reports that form one non-redundant narrative and briefly state the selection logic.

Fetch every selected report with `get_report_run` and set `includeEvidence: { perSectionLimit: 3 }`; when the connected schema accepts `reportRunOIds`, pass up to 20 run oIds per call and read `notFound` before assuming a run exists. Use this evidence preview for every section so the initial digest has inspectable support without requiring full hydration. Never build a multi-report digest from summary-only data.

When the user selects all reports, include every completed report returned for the period. Do not infer missing reports from the group's configured report count. If the configured and completed counts differ, state the completed count in the artifact and note the discrepancy during delivery.

For an investigative digest, select the primary questions and eligible population under the investigation method instead of requiring report selection. Reports used as supporting sources still retain their run IDs and evidence links.

### 3. Name the digest

Reuse the supplied name or choose a concise one when authorized. Use the stable opaque digestId and workspace-scoped state in [task-method.md](task-method.md); changing the display name must not overwrite another digest.

### 4. Choose evidence depth

For a recap, default to the evidence preview returned by `get_report_run({ includeEvidence: { perSectionLimit: 3 } })`. For an investigation, retrieve enough source context to verify material claims regardless of how much evidence the reader wants displayed. Evidence depth controls presentation detail, not the standard of verification.

If evidence-display preferences remain unresolved, ask whether to go beyond that preview:

> The digest will include a short evidence preview by default. Do you want detailed evidence too?
>
> 1. Preview only: evidence counts and a few supporting examples
> 2. Selected details: verified quotes and source context for the most important claims
> 3. Full receipts: quotes, companies, people, deal context, and source links where available

Explain that options 2 to 3 call `get_report_section_evidence` and may require additional event hydration, so they take longer and consume more tokens. Never fabricate precision to compensate for missing evidence.

Follow [evidence-and-links.md](evidence-and-links.md). Keep private deal or person details out of externally shared output unless the user explicitly confirms the audience and inclusion.

### 5. Choose content density

If density remains unresolved and the user has not delegated the choice, ask:

> How should this digest read?
>
> 1. Executive: compressed conclusions, key evidence, and actions
> 2. Detailed: more of the reports' reasoning, examples, caveats, and section-level prose

Content density is separate from evidence depth. Detailed mode may use report prose without exposing named people, companies, deals, or verbatim quotes. Evidence privacy choices still apply.

In detailed mode:

- Start from full report sections for a recap, or the verified claim packet for an investigation
- Preserve meaningful reasoning and concrete examples that explain why each conclusion holds
- Edit for coherence and remove repetition across overlapping reports
- Retain the source reports or underlying evidence for each analytical section
- Add pages or slides instead of shrinking type, overfilling layouts, or turning prose into tiny cards
- Do not paste report text wholesale; shape it into a readable combined narrative

### 6. Choose the output

If format remains unresolved and the user has not delegated the choice, ask:

> What should I generate?
>
> 1. Magazine style
> 2. Slide deck
> 3. Interactive microsite
> 4. One pager
> 5. Executive brief
> 6. Markdown digest

Supported formats, in display order: magazine style, slide deck, interactive microsite, one pager, executive brief, or Markdown.

Use [format-routing.md](format-routing.md). Reuse the selected reports, narrative, evidence packet, and workspace brand kit across formats. If the user asks for multiple formats, establish one settled content brief before rendering any of them; seek approval only when requested or a material decision remains unresolved.

If the user requests both Executive and Detailed variants, treat them as adaptations of one shared source packet:

- Keep the reporting window, report scope, claim provenance, evidence counts, privacy decisions, and core conclusion consistent
- Executive versions compress to decisions, major evidence, and actions
- Detailed versions preserve report-level reasoning, caveats, concrete examples, and additional source context
- Do not independently research each variant or allow their factual claims to drift

Magazine length is narrative-driven. Never force a fixed spread count.

### 7. Gather evidence, then build the content brief

Build the compact [evidence packet](evidence-packet.md) before selecting the main conclusion. For investigations, complete the relevant coverage and comparison checks in [investigation-method.md](investigation-method.md). Do not propose a headline and then search only for support.

For each candidate section:

1. **Gather.** Record the category, measured unit and counts where available, source scope, correctly attributed examples, and material counterevidence. Use verified workspace entity names. Plain-language grouping is allowed if clearly editorial; never invent a library entity or silently replace the customer's taxonomy. Preserve qualitative frequency as qualitative when counts are unavailable.
2. **Derive.** Write the strongest takeaway the evidence supports. Valid directionality is useful without statistical significance. If support is limited, narrow the claim; omit a section only when it adds no supported understanding.
3. **Decide.** Explain why the finding matters to the requested business decision. Recommend a message, material, targeting test, or other change only when earned. Keep library changes as suggestions unless authorized to apply them.

Then form the brief: audience and decision; digest identity; questions and source inventory; reporting period; main conclusion; narrative and outline; density; evidence/privacy choices; format, brand, and useful links. Show it for review when the user requested staged approval or a material decision remains unresolved. Existing approval or authorization to proceed is sufficient; do not add a mandatory approval round to every digest.

Keep net-new acquisition, expansion, retention, and other requested motions distinct from industry or persona segmentation. Use verified product/capability relationships. Write from the team's standpoint for an internal executive audience; do not turn normal customer operating patterns into dramatic failures. Prefer a few well-explained findings over thin coverage of every category.
