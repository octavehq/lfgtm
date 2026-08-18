---
name: digest
description: Turn one or more Octave GTM Explorer / Beats reports into a branded, shareable digest with selectable insight scope, evidence depth, and output format. Use when the user asks for a report digest, weekly or monthly insight recap, executive intelligence brief, magazine-style insight story, report deck, or a recurring published summary of Octave insights.
---

# /octave:digest - GTM Insight Digest

Turn completed Octave reports into one coherent editorial asset. On an interactive first run, ask the user what to include, what to call the digest, how much evidence to hydrate, how it should render, whether to publish it, and whether to repeat the workflow. On a scheduled run, reuse the approved named configuration without asking the same questions again.

## Principles

Read before generating:

- [Editorial rules](../shared/editorial-rules.md)
- [Information principles](../shared/information-principles.md)
- [Presentation principles](../shared/presentation-principles.md) for visual output
- [Brand kit usage](../shared/brand-kit-usage.md) for branded output
- [Evidence and links](references/evidence-and-links.md) when quotes, citations, companies, people, deals, or source links are requested
- [Format routing](references/format-routing.md) after the user selects an output format

The editorial rules apply to **titles and headings**, not just body copy. Every chapter, section, and spread title must state its finding as an intelligible sentence, or, if it is a short label, be clearly decipherable on its own. A vague evocative fragment that could sit on any report ("The Pressure," "The New Owner," "The Wall") does not pass: lead with the claim it stands in for. State the finding **plainly**. A dramatic reversal or clever turn ("we won X and inherited Y," "we won the argument and lost the war") fails on the opposite end, reading as performative even when the underlying finding is real. The editorial review must audit titles the same way it audits prose.

**Write like a dispatch, not an inside joke.** Frame every finding for a reader who was not on the calls and does not yet share the context. State plainly what happened, to whom, and why it matters before layering in the clever turn. An elliptical, knowing line that assumes shared context ("Buyers stopped asking why and started handing our own framing back to us," "the conversation moved") is a failure even when it is literally true: the reader has to reverse-engineer what it means. A real magazine sets the scene, then delivers the point. Prefer the sentence a smart colleague who missed the week would understand on first read over the one that sounds knowing to someone who was there.

## Workflow

### 1. Discover the available reports

1. Call `verify_connection`.
2. Call `list_gtm_reports`. If there is one obvious group, use it. If several are plausible, ask which group.
3. Call `get_latest_gtm_report` for the selected group.
4. Show a compact inventory with report title, period, and one-sentence delta. Do not dump the report prose.

### Interactive and recurring modes

Determine the run mode before intake:

- **Interactive setup or ad hoc run:** explicitly ask the scope, evidence depth, output format, hosting, URL behavior, and scheduling questions below. Do not silently choose for the user unless they already answered or said to use your judgment.
- **Scheduled run with a saved digest specification:** load it by digest name or slug and reuse the saved selection rule, evidence depth, format, audience, brand, hosting, timezone, URL behavior, and delivery destination. Do not ask the setup questions again.
- **Scheduled run with missing or invalid configuration:** pause only for the missing decision. Save the answer back to the digest specification for future runs.

Treat an explicit instruction in the current request as an answer. Do not ask the user to repeat information they already supplied.

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

### 3. Name the digest

For an interactive first run, ask:

> What should this digest be called?

Offer a concise default derived from the report group, audience, or theme, such as `Weekly Competitive Intelligence` or `Executive Buyer Signals`. Let the user accept or replace it.

Treat the name as the identity of this digest configuration, not as a global workspace setting. Derive a stable slug from the approved name and use it to scope saved configuration, recurring schedules, hosted assets, and update-in-place URLs. A workspace may have multiple named digests with different report scope, format, audience, privacy, and cadence.

If the derived slug already belongs to a different digest specification, ask whether to update that digest or choose another name. Never silently overwrite another digest.

### 4. Choose evidence depth

The default is the evidence preview returned by `get_report_run({ includeEvidence: { perSectionLimit: 3 } })`.

For an interactive run, ask whether the user wants to go beyond that preview:

> The digest will include a short evidence preview by default. Do you want detailed evidence too?
>
> 1. Preview only: evidence counts and a few supporting examples
> 2. Selected details: verified quotes and source context for the most important claims
> 3. Full receipts: quotes, companies, people, deal context, and source links where available

Explain that options 2 to 3 call `get_report_section_evidence` and may require additional event hydration, so they take longer and consume more tokens. Never fabricate precision to compensate for missing evidence.

Follow [evidence-and-links.md](references/evidence-and-links.md). Keep private deal or person details out of externally shared output unless the user explicitly confirms the audience and inclusion.

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

### 6. Choose the output

For an interactive run, ask:

> What should I generate?
>
> 1. Magazine style
> 2. Slide deck
> 3. Interactive microsite
> 4. One pager
> 5. Executive brief
> 6. Markdown digest

Supported formats, in display order: magazine style, slide deck, interactive microsite, one pager, executive brief, or Markdown.

Use [format-routing.md](references/format-routing.md). Reuse the selected reports, narrative, evidence packet, and workspace brand kit across formats. If the user asks for multiple formats, establish one approved content brief before rendering any of them.

If the user requests both Executive and Detailed variants, treat them as adaptations of one shared source packet:

- Keep the reporting window, report scope, claim provenance, evidence counts, privacy decisions, and core conclusion consistent
- Executive versions compress to decisions, major evidence, and actions
- Detailed versions preserve report-level reasoning, caveats, concrete examples, and additional source context
- Do not independently research each variant or allow their factual claims to drift

Magazine length is narrative-driven. Never force a fixed spread count.

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

### 8. Generate and review

1. Load or capture the workspace brand kit **first**, and set the digest in **its** typefaces (read them from the kit's `tokens.css` / manifest), not a generic editorial pairing. Then make sure those brand fonts are actually loaded and, for any hosted or shared digest, self-contained (`@font-face` with base64 `src`, not a remote `@import`/CDN link) so the render never falls back to a system font. Using generic type when a kit exists, or leaving a font unloaded, is a defect. See the font rules in [the shared magazine spec](../shared/formats/magazine.md).
2. Generate through the selected format skill or reference. For editorial swipe magazines, follow the shared [magazine format spec](../shared/formats/magazine.md) with its [magazine-base.css](../shared/formats/magazine-base.css) scaffold, plus the digest-specific rules in [format-routing.md](references/format-routing.md); do not route magazines through `/octave:deck`.
3. Include source notes only where they help verification.
4. For internal output, include Octave report links as described in [evidence-and-links.md](references/evidence-and-links.md).
5. Every displayed number must tell the reader what it counts. Put the unit next to the value, state the reporting period and scope nearby, and explain deduplication or overlap when categories are not mutually exclusive. Translate internal evidence mechanics into reader language: use “calls,” “companies,” “deals,” or “buyer quotes,” never an unexplained label such as “receipt set.”
6. When defensible totals are available, put a compact sample-size line on the title or opening spread (for example: calls, companies, evidence excerpts, and completed reports). Keep the reporting window separately visible so readers can judge coverage before interpreting the story.
7. **Run the review gate. This is a mandatory step, not an option.** Do not open the artifact, present a delivery summary, or tell the user it is ready until the gate has run and produced a scorecard. Load the [review protocol](../shared/protocol.md); the wiring below is digest-specific.

   **Which gate runs where.** For digest-native HTML this skill renders directly (editorial swipe magazine and executive brief), run the full gate here. For formats handed to another skill (`/octave:deck`, `/octave:microsite`, `/octave:one-pager`), that skill owns its own mandatory gate; do not duplicate it. For Markdown, run the editorial half only, since there is no visual layer. In every case the digest orchestrator stays responsible for groundedness: no claim, quote, number, or attribution ships that the source reports and evidence do not support.

   **7a. Preflight (deterministic, always first).** Run the protocol preflight, then the lint, and fix every violation before going further:

   ```bash
   bash <skill-dir>/../shared/scripts/lint.sh <path-to-output.html>
   ```

   **7a2. Render gate (visual formats).** For the magazine and the executive brief, run the shared render gate next and fix everything it reports. It decides fonts-actually-loaded, contrast, content-box overflow, and collisions with fixed chrome, so the reviewers' screenshot budget goes to judgment instead of defect hunting:

   ```bash
   node <skill-dir>/../shared/scripts/render-gate.js <path-to-output.html> \
     --panes ".spread" --chrome "#nav,.folio" \
     --viewports 1600x900,1680x1050,2560x1080,1180x820
   ```

   Do not replace this with a `scrollHeight` check of your own: a spread sets `overflow: hidden`, so that difference reads 0 while content is visibly clipped.

   **7b. Spawn the two dedicated reviewers in parallel** (both Task calls in one message):

   **Editorial reviewer:**
   ```
   Task tool:
     subagent_type: "octave-editorial-reviewer"
     prompt: "Review the file at [FILE PATH].
              Read and run the checklist in each of:
              1. [skill-dir]/../shared/editorial-rules.md
              2. [skill-dir]/../shared/information-principles.md
              3. [skill-dir]/../shared/formats/magazine.md (magazine output)
                 Audit titles AND body copy: every chapter, section, and
                 spread title must state its finding as an intelligible
                 sentence (not a vague evocative fragment, not a dramatic
                 clever turn); body copy must frame each finding for a reader
                 who was not on the calls, never dropping cryptic or elliptical
                 lines that assume shared context.
              Fix violations inline. Return scorecard."
   ```

   **Presentation reviewer:**
   ```
   Task tool:
     subagent_type: "octave-presentation-reviewer"
     prompt: "Review the file at [FILE PATH].
              Read and run the checklist in each of:
              1. [skill-dir]/../shared/presentation-principles.md
              2. [skill-dir]/../shared/formats/magazine.md (magazine output)
                 or [skill-dir]/references/format-routing.md for other formats
              For magazine output, run the full responsive review gate in that
              file at 16:9, 16:10, ultrawide, and a narrow viewport: the
              multi-aspect check, the nested-surface and per-spread contrast
              check (including fixed navigation chrome that must stay visible
              on both light and dark spreads), the title-states-its-finding
              check, and the typefaces-actually-rendered check. A brand font
              that is declared but not loaded and falls back to a system face
              is a hard failure. A single desktop screenshot is insufficient.
              Fix violations inline. Return scorecard."
   ```

   **7c. Loop and scorecard.** Follow the protocol's loop decision (max 3 cycles, re-run both reviewers each loop) and output the combined scorecard. Delivery cannot start without it.

For internal visual output, offer a compact source appendix after the main narrative and before the closing. The appendix may include:

- Included report titles, reporting windows, and links back to the full reports in Octave
- A brief scope or evidence note
- A copyable **Chat with this insight** starter prompt that tells the reader to use the Octave MCP, identifies the reports by stable title or identifier, and asks a useful follow-up question

Keep the starter prompt portable: do not assume a specific AI client or expose private evidence. Ask the MCP to fetch the current report rather than embedding the entire report in the prompt. When a stable report identifier is available, include it alongside the human-readable title.

For every output, state the reporting window prominently. Do not display a timezone for ordinary day- or week-based windows; include one only when an exact timestamp boundary materially affects scope. When the digest combines multiple reports or insight threads, visual formats must include:

- A cover or opening view with the digest title, reporting window, and scope
- A contents or agenda view naming each included report or insight thread
- Clear section dividers or navigation that preserve report provenance while supporting one combined narrative

Do not make readers infer which period or source report a claim belongs to.

### 9. Offer hosting

After the artifact passes review on an interactive run, ask:

> Host this with Octave Asset Manager?
>
> 1. Workspace access
> 2. Public link
> 3. Only me
> 4. Not now

If yes, also ask:

> What kind of URL should this use?
>
> 1. Stable or vanity URL that updates in place
> 2. New versioned URL for every digest

Recommend a stable URL for recurring digests and a versioned URL for immutable reports or campaign-specific deliverables. If the user chooses a stable URL, ask for the preferred readable slug or offer one derived from the digest name.

Then hand off to `/octave:asset-manager`. Pass the chosen access level and URL behavior with the approved artifact. That skill owns identifier choice, slug availability, privacy confirmation, token handling, upload or update-in-place behavior, and final links. Do not duplicate its publish workflow here.

### 10. Offer scheduling

After delivery on an interactive run, ask:

> Run this digest on a schedule?
>
> 1. Weekly
> 2. Monthly
> 3. Custom cadence
> 4. No

Clarify what should recur:

- **Report schedule:** Octave produces the underlying GTM reports.
- **Digest schedule:** the approved selection, evidence mode, format, hosting privacy, and audience are applied to each new period.

Use the runtime's recurring-task or monitoring capability when available. Save a named digest specification containing the digest name and slug, report group, selection rule, content density, evidence depth, format, audience, brand, hosting privacy, URL behavior and stable slug when applicable, timezone, and delivery destination. Key saved state by digest identity rather than a single global digest setting. Instruct the recurring run to load this specification and skip interactive intake unless a required value is missing or the report source becomes invalid. If no scheduler is available, say so plainly and provide the complete schedule specification for later activation. Never claim a schedule was created without a confirmed scheduler result.

## Defaults

When the user says “use your judgment”:

- Scope: strongest connected story, not every report
- Name: offer a concise derived name and ask the user to accept or replace it
- Content density: executive
- Evidence: the `get_report_run` evidence preview, with no private deal details
- Format: executive brief for internal reading
- Links: include report links for internal readers
- Hosting: ask after review, including stable/vanity versus versioned URL
- Scheduling: ask after delivery

## Error handling

**No completed reports:** offer `/octave:insights` for an event-and-finding digest or ask the user to widen the report group or period.

**Selected report has no sections:** use its comparison and summary, label the evidence as limited, and do not inflate the output.

**Evidence cannot be hydrated:** generate from report sections and counts, state that quotes and entity-level citations were unavailable, and offer to continue without them.

**External audience with private evidence selected:** pause and confirm exactly which companies, people, quotes, and deal details may be disclosed.

## Related skills

- `/octave:insights` for ad hoc findings that are not based on completed reports
- `/octave:deck` for presentation rendering
- `/octave:microsite` for interactive web output
- `/octave:one-pager` for a compact leave-behind
- `/octave:asset-manager` for hosting and sharing
