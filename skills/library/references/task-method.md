# library: task method

Before creating, verify the workspace and resolve the requested entity type. Search for exact/near duplicates and inspect plausible matches. Read the adjacent offering, buyer/segment, relevant Motion and linked context. Decide whether this is a new distinct entity or an authorized refinement of an existing one. Do not create duplicate context solely because the user used a different label.

Draft against the entity's task schema:
- Persona: actual responsibility/workflow, desired outcome, pain mechanism, buying role, evaluation criteria, objections, relevant offerings and segment differences.
- Offering/core feature: what is delivered, workflow change, capability boundaries, supported use cases, buyer value, dependencies and commercial relationship to other offerings.
- Segment: observable inclusion/exclusion, business context, distinctive needs, evidence and linked offerings/personas.
- Competitor/alternative: category and relevance, strengths, weaknesses/tradeoffs, comparison criteria, current dated sources and linked motions.
- Proof/reference: exact claim, measured/reported status, unit/period/denominator, customer/applicability, source and external-use constraints.
- Trigger/objection: observable event or buyer concern, relevant stage/persona, why it matters, evidence and appropriate response.

Use CRM/calls and library evidence first. Ask only for missing strategic intent or material facts. Retain unsupported propositions as draft hypotheses, not approved claims. Specify intentional links and preserve source provenance. Show the concise proposed entity when review is needed; respect existing authorization to create/update. Then write using the supported schema and read back the complete saved object and links before confirming completion.

Resolve exact IDs through reads, snapshot the target/revision and linked objects that could be affected, and record allowed changes plus protected fields. Use supported structured mutation when available; otherwise pass precise natural-language instructions preserving those boundaries. For a Motion/Playbook/ICP edit, use its dedicated supported API and verify the relevant narratives, cells and links afterward. Compare saved state with the preimage. Report only changes verified by readback; expose no-op, partial success or unintended change. Reconcile before retrying. Keep recovery revision IDs and a reversible plan; do not overwrite unrelated later edits during recovery.

For “all,” exhaust pagination and deduplicate by ID; report returned/total coverage and any failed page. Hydrate details only where required by the request, and never present missing slim fields as absent data. Show timestamps only when returned. Separate authentication/permission, missing object, unsupported schema/type, conflict, transient failure and partial completion. Preserve the user's intended scope when retrying; do not replace a failed instruction with a weaker “simpler” request. Resume from verified progress and keep an accurate pending list.
