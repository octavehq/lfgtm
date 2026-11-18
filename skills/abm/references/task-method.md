# abm: task method

### One company or a cohort
A request that names one company follows the account plan contract below. A request that names a segment, a cohort or a list of accounts follows [cohort-plan.md](cohort-plan.md) instead and does not build a committee for any single account. When a request could be read either way (one parent company with many divisions, a list of one), ask once and continue with the reading the wording supports.

### Account plan contract
Read [gtm-context.md](../../shared/gtm-context.md) for the selected account's offering, motion, segment, and persona cells. Read [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for claims and operator inputs; use [output-readiness.md](../../shared/output-readiness.md) for the final plan. Load HTML/brand references only when rendering the plan. Do not load mutation guidance unless the user requests a separate library change.

Retrieve CRM relationship, open opportunities, owners, activities, and relevant calls first. Distinguish acquisition, expansion, and displacement. Use account-wide evidence for account planning while identifying the opportunity behind any deal-specific assertion. Ask a grouped clarification for materially ambiguous offering, division, account objective, or unrecorded engagement; continue supported research and incorporate the response with provenance.

Use [Ask Octave first](../../shared/octave-research-toolkit.md#ask-octave-first-for-questions-that-span-records) for the first pass on the account: ask `ask_octave` which people at the account have appeared in calls and deals, what the account has raised, and which comparable accounts and proof points sit behind won deals for the same personas. Use that to find candidates and routes, then verify identity, participation, and role with the narrow CRM, call, and person tools. Graph links do not establish a buying role, and an answer can be wrong about this account, so drop any statement that cites another account. If the tool is unavailable, continue with the narrow tools and note it.

On an Octave host, find people at the account with `find_person`, take firmographics from `enrich_company`, and read account fit from `qualify_company`. A fit result is a score out of 10 with its reasons: 7 or more is a fit unless a disqualifier was triggered.


Select the committee from this customer's relevant persona cells. For each person, record identity source, participation evidence, and buying-role evidence independently. A verified title without engagement supports a candidate, not a confirmed champion. A seller-reported role is usable with that provenance. Preserve role gaps instead of manufacturing names. Count a role as missing only when it should be engaged at this account's stage, size and motion, list later roles as needed later, and write the committee as people, never seats ([information principles](../../shared/information-principles.md#reading-calls-and-deals) rules 23 and 24; [editorial rule 14b](../../shared/editorial-rules.md)).

For every buying trigger, separate the library definition from the account occurrence. Mark occurrence Known only when dated account evidence or attributed operator confirmation establishes it. Otherwise show Trigger to validate, its relevance, and a confirming question. Apply the same separation to persona pains: strategic relevance is not confirmed account pain.

Build the engagement plan before rendering: entry person or role, why this entry point, supported hook, one or two complete sample emails unless the user specifies otherwise, and the sequence for involving the other people on the committee. Base each touch on prior CRM/call context, the recipient's cell, relevant proof, and the next desired commitment. State the condition for the next step rather than assuming each touch succeeds. Fit the plan to the account's setting per [Reading Calls and Deals](../../shared/information-principles.md#reading-calls-and-deals) rules 16 to 21. Personal facts stay out of the plan, the emails and the risks, and a relationship that changes how the account is run appears once in the internal plan's risks and never in the emails. Pair each material risk with its mitigation.

Keep the committee, per-persona positioning, outreach, and sequence aligned. For every selected persona provide concerns, current approach, lead argument, relevant proof or an honest proof gap, and desired next action. Review the complete plan including outreach; deliver only that reviewed version. A later content change requires checking the changed claims and final artifact again.

### Depth and scope
Quick: a compact account decision, the strongest available entry route, up to three primary people/roles, relevant persona framing, one sample email, and the next three actions. Retrieve enough evidence for those claims; put unresolved research into a short next-check list.

Full: cover the requested stakeholder count and relevant buying roles, all material persona framing, engagement sequence, and risks. Show a compact primary committee with additional verified people in an appendix when needed. The user's explicit count overrides default display caps. Return an honest discovery shortfall rather than weak matches or invented people. Do not treat a fixed security persona triad as the default committee.

## Data beside the document

When the run is asked for data beside its document (the skill's `output.schema.json`), return the account's name and domain, each mapped person as a row of `stakeholders` (name, title, matched persona, their part in a decision, profile link, and one sentence on the angle) and each recommended play as a row of `plays` in the order to run them. Copy names, titles and links exactly as a tool returned them, write null for what no tool returned, and use `unknown` for a part in a decision the evidence does not show.
