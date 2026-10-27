# call-analyzer: task method

Parse supplied content before asking intake questions. Establish requested
outcome (rep coaching, message QA, or deal next step), conversation stage,
and whether the source is a complete transcript, excerpt, email thread, or
notes. Use existing context and ask grouped questions only for material
unresolved facts. Maintain the analysis and open questions across turns.

Resolve account and opportunity from accessible CRM/call context; record
source/date and avoid assuming one opportunity per domain. Distinguish
verified speaker/role from inferred or anonymized labels. Identify each
buyer's role and persona separately. Load [gtm-context.md](../../shared/gtm-context.md) to select
offering, Motion, segment, and the relevant cells; hydrate full offering,
proof, and competitive context only for dimensions actually being assessed.

A partial source limits conclusions. Do not infer total speaking time,
unseen objections, missing follow-through, names, or company qualification
scores from an excerpt. A person-to-persona match is not an account ICP
score. Show qualitative fit with supporting/unknown criteria unless an
actual configured qualification result exists; identify its scope/source.

Before scoring, write down the setting and apply the
[Reading Calls and Deals](../../shared/information-principles.md#reading-calls-and-deals)
rules (16 to 21): size of the sale, which meeting it was, stage on that date,
earlier calls, who was in the room and what was shown. Every score, risk and
next step is judged against what a meeting in that setting can achieve.

First mark each dimension applicable or N/A for this stage/objective and
source completeness. For scored dimensions, cite evidence, counterevidence,
confidence, and the reason for the selected score; do not mechanically
average incomparable dimensions or imply precision unsupported by the source.

Engagement/resonance:
1–2: explicit disengagement/refusal or repeated nonresponse where observable;
3–4: limited relevant exchange with weak follow-through;
5–6: mixed/unclear engagement;
7–8: substantive questions, shared operating details, or serious evaluation;
9–10: substantial engagement plus the strongest commitment the setting allows
(a dated next step in a late-stage call; after a first enterprise meeting, a
champion who says who they will take it to next).
Under rule 16 a first enterprise meeting without a dated next step does not
score 5–6, and reactions to named capabilities are tallied with timestamps
before engagement is called unclear.
Skepticism and detailed objections can be engaged evaluation. Email delay
needs context; absence of a later reply in an excerpt is unknown.

Narrative execution:
Select the few narrative/discovery elements relevant to this meeting goal.
1–2: material unsupported/misleading claims or ignored essential discovery;
3–4: major eligible gaps;
5–6: mixed execution;
7–8: accurate relevant framing and useful discovery, with minor gaps;
9–10: goal-appropriate, evidence-backed framing that helps the buyer evaluate.
Do not reward reciting every Motion field or penalize omitted irrelevant ones.

Differentiation:
N/A when alternatives are outside the conversation objective.
1–2: unsupported comparison or material misunderstood requirement;
3–4: important buyer criterion unaddressed;
5–6: accurate but generic comparison;
7–8: relevant criterion tied to capability/proof and tradeoff;
9–10: buyer-acknowledged differentiated fit with a useful evaluation step.
A legitimate conceded competitor advantage need not lower the score.

For each coaching recommendation show: observed moment, buyer implication,
a better specific response/question, supporting Motion/proof, and next use.
Rules 17, 19 and 21 apply to the recommendations: an unanswered buyer pain
ranks at least second, an unsupported seller claim becomes a recommendation
with the recorded figure to use instead, and personal facts stay out of the
analysis and any draft. A delivery habit (pacing, filler words, slide count)
is a recommendation only when the buyer's reaction shows it cost something.
Talk time is one of these: a seller share above about 60% of a complete
transcript becomes a recommendation when the buyer remarked on the pace or got
little room (short turns, questions cut off), with the share and that moment
as evidence.
Separate explicit commitments (who/what/when, with source) from suggestions,
unanswered product questions, and assumptions. Preserve the buyer's agreed
sequence. Do not add every omitted message to the follow-up.

If follow-up drafting serves the user's objective, use relevant approved
capability/proof facts, never a seller claim from the call that the record
doesn't support (rule 21). A capability, security, data-handling or results
line the draft adds on its own needs a record too; without one it leaves the
draft and becomes a question for the operator (rule 21). Load [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for material
unanswered integration, pricing, POC, or implementation questions. Ask the
operator, incorporate/source answers, and update the draft. Unknown answers
become an agreed working placeholder or a task to obtain the answer, never
an invented capability or promise. Distinguish sender commitments from
buyer commitments. Load [output-readiness.md](../../shared/output-readiness.md) at delivery; complete
the requested analysis/draft through corrections, with open tasks explicit.

Resolve and verify the workspace before using customer-specific context. When the task requires GTM conclusions, read the relevant Octave library entities, CRM opportunity/account data, and call recordings first. Hydrate selected entities and source material; an inventory row is not the full evidence. Use the current offering and Motion/Playbook/persona × segment to decide which facts matter to this task. Ask the operator only for material inputs still missing, such as value-assessment figures, feature usage, POC measurements, approved commercials, or delivery constraints. Preserve useful draft work and unanswered inputs across turns. Incorporate each answer, update dependent claims/calculations, and rerun the relevant checks. Attribute operator-provided facts as operator input; they need not already exist in a tool result. Do not expand a narrow list/get or structural check into unrelated commercial research.

Match completion to the requested deliverable. Instructions, intake forms, and working drafts may contain placeholders. Continue collecting, incorporating, and checking missing inputs when the user wants the completed artifact; completion may span turns. A buyer-facing POC or success-plan worksheet may intentionally leave future measurements or acceptance fields open when their definition, owner, and timing are stated. Distinguish those planning fields from accidental missing seller inputs. Before external delivery, check each load-bearing claim's evidence status and audience suitability, the working CTA/links, the requested format, and rendered readability. Do not infer an account's actual pain, incumbent, result, or agreement solely from a persona, segment, or category pattern.

When the call belongs to an account or opportunity in the workspace, optionally use [Ask Octave first](../../shared/octave-research-toolkit.md#ask-octave-first-for-questions-that-span-records) to calibrate the analysis: ask `ask_octave` what has resonated, and which objections and competitors recurred, on comparable calls and won deals for the same persona. Present these as workspace context beside, never in place of, evidence from the supplied transcript. Anchor the question on the account or opportunity ids and verify any claim with a narrow read before it shapes a visible line. If the tool is unavailable, analyze the supplied source alone.
