# Analytical scope and conclusions

Use for aggregate findings, trends, win/loss, ICP refinement, performance feedback, and calibrated qualification evaluations. Apply a compact relevant subset to a single-call or single-deal analysis; do not create a population study for a narrow request.

Before calculating or ranking, establish the population, inclusion/exclusion rules, period/timezone, unit of analysis, stable identity, outcome definition, denominator, pagination/coverage, deduplication method, and missing data. Preserve those choices with the normalized rows or working evidence. Account, opportunity, event, speaker excerpt, ad, and ad group are different units.

Retrieve the relevant CRM and call evidence first. For supplementary usage, value, conversion, or POC inputs that the requested conclusion requires, follow evidence-and-inputs.md. Operator-supplied data is valid when attributed and scoped. If necessary measurements do not exist, make the appropriate descriptive or qualitative conclusion and identify a practical next measurement.

Counts must state what was counted. A recurring quote from one deal is not several customers. Trend claims require comparable baseline periods and disclosure of changes in source coverage. Inactivity requires an eligible active roster and an adequate observation window; no retrieved event is not proof that nothing happened.

Distinguish seller usage, buyer acknowledgment, resolved concern, engagement, and commercial outcome. State association as association unless the evidence supports a causal design; a buyer-attributed explanation remains an attributed explanation. Account-level totals cannot establish a headline-level winner or a persona-specific effect.

Show numerator, denominator, scope, confidence limits, and alternative explanations when they change a decision. Do not use arbitrary scores or volume thresholds as proof of certainty. Unknown, zero, and not-applicable require separate calculation behavior. Do not calculate a ratio when its denominator is undefined; report the reason.

For tuning or learning, keep diagnostic/training cases separate from evaluation cases; include relevant good, bad, borderline, unknown, and adjacent cases. Record the original hypothesis, comparison, outcome, and decision rule before evaluating. Preserve inconclusive results; do not change the population after seeing results to rescue a prediction. When changes affect shared library objects, evaluate impacted consumers and use workspace-mutations.md.

Every recommendation should name the exact action, affected offering/motion/audience, supporting evidence, confidence or unresolved assumption, and a practical success measure. Recommend a bounded test when evidence supports a hypothesis but not a durable strategic change.
## Deterministic normalized rows

Use [analysis_rows.py](scripts/analysis_rows.py) when normalizing closed opportunity
snapshots or reconciling raw/joined ad metrics. Its input fields are a local
normalized schema, not invented backend arguments. Preserve source IDs, coverage
and the chosen outcome definition. Render text, rates and bars from the same
returned metric object; for example 9 wins and 5 losses is 9/14, about 64.3%.
Readback/coverage gaps remain separate from zero observed events.
