# Evidence packet and comparison ledger

Keep a compact, local record supporting the artifact. A Markdown table or JSON file is sufficient; do not build a new persistence service. Scale the record to the task: a recap needs exact runs and load-bearing claim references, while an investigation needs population and comparison definitions. Private source material belongs in the authorized task output location, never in a public skill/repository or a generic example.

## Run record

Record:

- User question, audience, decision, mode, reporting period/timezone, and privacy scope.
- Workspace identity, source cutoff/freshness, exact report run IDs if used, and loaded skill location/version or content hash.
- Relevant connected tool/schema/build identities where exposed; mark unverified identity honestly. Record a local source revision separately from the responding server build.
- Business definitions and human decisions reused or resolved, with their scope; relevant capability and coverage limitations.
- Paths to bounded raw responses or stable source references sufficient to reproduce material claims. Do not store credentials or unnecessary private content.

## Claim record

A useful shape (omit inapplicable fields rather than filling them with invented values):

```yaml
claim_id: C1
question: Which buyer problem warrants a messaging test?
statement: Pending evidence
status: candidate # supported, directional, qualified, withheld, superseded
inference: observed # compared, associated, hypothesized
sources: [] # tool calls, exact selectors, run/section/event/finding IDs, quote locations
window: null
outcome_as_of: null
unit: null # events, companies, people, opportunities; never interchangeable
population: null # eligibility, exclusions, link rule, history/ordering basis
measurement: null # numerator, denominator, rate, amount basis, or qualitative observation
coverage: null # known reach, missingness, processing state, unknowns
support: [] # correctly attributed evidence and representative examples
counterevidence: []
alternative_explanations: []
limitations: []
recommendation: null # proportional action, or no action warranted
artifact_locations: [] # headings/charts/variants to revise when this claim changes
```

Never treat this example as measured data. For quotes preserve verbatim text, speaker-side confidence, event/date, and source location; label paraphrases. Keep derived graph relations and authored library context separate from observed customer evidence. A quote outside an aggregate's population can add context, but cannot serve as proof of that cell's membership or frequency.

## Comparison ledger

Before comparing, identify the primary questions and prospective comparison family where practical. Record each comparison when it is run, including uninteresting results and sensitivity variants:

| Field | What to preserve |
|---|---|
| Identity and intent | Comparison ID, question, primary vs exploratory, hypothesis or decision |
| Definition | Each arm's membership, unit, window, outcome, linkage, exclusions, and supported controls |
| Inputs | Exact call parameters and source cutoff/build; paths to results |
| Results | Both numerators/denominators, observed direction and gap, uncertainty/verdict, missingness, and counterevidence |
| Family | Family ID, comparisons explored, declared correction method/count where used; when the family was chosen |
| Materiality | Margin, units (absolute percentage points vs relative change), baseline, reason, and when selected, if relevant |
| Disposition | Included, contradicted, inconclusive, unsupported, or withheld; reason and follow-up |

A descriptive directional finding does not need an equivalence margin. If testing practical equivalence, choose the margin before examining that gap; a software default is not a business-endorsed threshold. Do not reinterpret a failed significance test as equivalence.

The agent owns cross-call bookkeeping. A stateless tool cannot know how many comparisons were explored elsewhere. When a displayed adjusted result depends on a final family count, recompute with the final declared family using the supported tool contract. Recording a comparison count does not turn adaptive exploration into independent confirmation. Do not invent inferential statistics when the tool does not provide or support them.

## Reader-facing use

Keep essential counts, denominators, period, attribution, and material limits beside the claim. Put detailed method and source references in an appropriate appendix or local companion packet. Keep IDs, tool names, and implementation bookkeeping out of executive prose. The packet supports review; it is not a template to dump into every digest.

Analytical completeness belongs in this packet, not in every summary panel. Select the numbers that explain the finding; do not reproduce every interval, sensitivity result, comparison adjustment, and sample-size target in the main narrative. Explain material limitations in plain language where they change the takeaway. Keep useful observed directionality visible even when it does not establish a reliable general difference. A reader should understand what happened and why it matters before opening supporting detail.
