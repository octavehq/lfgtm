# generate: task method

### Choose the generation route
Honor an explicit engine or named saved-agent request. If the named agent resolves uniquely and fits the task, use it. Otherwise use Octave's native generation route by default. Ask only when an unresolved route or agent choice materially changes scope or behavior. Direct generation means the current assistant, regardless of host. If a question UI is unavailable, ask a plain conversational question; do not depend on a named host tool.

Read [content-contracts.md](content-contracts.md) for the applicable mode.


# Content contracts
- Email: singular requests produce one email with subject and body. A requested sequence has the requested number of touches and an explicit progression: initial reason, a distinct relevant angle/proof, and an appropriate next decision. Avoid repeating the same claim or implying prior engagement that did not occur. Respect any saved-agent sequence contract only when it matches the request.
- LinkedIn: distinguish connection note, InMail, and existing-thread follow-up; return only the fields needed for that type. Validate the current applicable channel limit or use the user's supplied limit; do not invent a universal platform character count. Keep one suitable CTA and no fabricated connection or reciprocity.
- Call prep: return objective, known context, argument/proof, questions, and next-decision ask. Route an explicitly requested strategic meeting game plan to meeting-prep with the assembled context; avoid starting a second intake.
- General content: derive the format, reader, desired decision, and completion criteria from the request. Preserve explicit scope rather than generating unsolicited variants.

On refinement, change the requested element while preserving validated facts and constraints. Recheck affected claims and the final payload after operator corrections.
