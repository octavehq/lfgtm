# Library Analysis Report — Output Template

Use this structure when presenting the analysis in Step 4. Keep all three sections even when a section is empty — an explicit "None found." is a finding.

```
## Library Analysis — [Document Title]

### Library Gaps ([N] items)

**ADD — [EntityType]: [Proposed Name]**
[What to add, concretely.]
Why it matters: [GTM rationale — how a PMM or AE would use this]
Source: "[verbatim excerpt, max 100 words]"

**REFINE — [EntityType]: [Existing Name]** (`[oId]`)
[What to change on the existing entity, concretely.]
Why it matters: [GTM rationale]
Source: "[verbatim excerpt, max 100 words]"

**ADD — [EntityType]: [Proposed Name]** — ⏳ already queued (`[suggestion oId]`)
[What the pending suggestion proposes, and anything this document adds to it.]
Source: "[verbatim excerpt, max 100 words]"

---

### Contradictions ([N] items)

| Entity | Library says | Document says |
|---|---|---|
| [EntityType]: [Name] (`[oId]`) | [current library claim] | [conflicting document claim] |

---

### Aligned ([N] items)

**[EntityType]: [Name]** (`[oId]`) — [what the document affirms]

---

### Next step

**Apply now** — write the [N] gaps to the library in one pass (`create_entity` / `update_entity`). Best when this source is trusted and you've reviewed the report.

**Queue for review** — park as PENDING suggestions in Octave. Use when another stakeholder should accept in the inbox, or the source is contested/external — not as a second review of work you already signed off on here.

**Selective** — e.g. "apply the reference + proof points; queue the rest."
```

## Vocabulary

Use Octave's own change vocabulary throughout — **add** and **refine**, never "update". These map 1:1 to `changeType` on write tools, so the report reads the same as the calls it produces.

## Section rules

**Library Gaps** are the only actionable section — the only one that produces writes in Step 5.

**Already-queued gaps stay in the report.** A gap that matches a pending suggestion (from the Step 2 `list_suggestions()` snapshot) is annotated with ⏳ and its suggestion oId, never dropped. On a re-run of the same document, the report looks the same as the first run — except gaps carry their queue status, and the Step 5 offer becomes "review/accept the queued suggestions" instead of "queue them". Zero-output re-runs are a bug, not politeness.

**Contradictions** are informational. Only list one when the document asserts a specific claim that conflicts with a specific library entity. A document that merely omits something, or emphasizes it differently, is not a contradiction. Contradictions are a prompt for the user to decide who is right; never auto-resolve one into a refine.

**Aligned** is informational and earns its place by building trust — it shows the analysis read the library, not just the document. Only list an entity when the document makes a substantive claim that matches it. Mentioning an entity's name is not alignment.

## Excerpts

Every gap carries a verbatim `Source:` excerpt. It grounds the write (apply or queue) and lets a reviewer judge the change without reopening the document. Quote, never paraphrase, and keep it under 100 words.
