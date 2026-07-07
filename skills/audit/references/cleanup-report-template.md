# CLEANUP MODE — Report Template (Step 4-C)

Present findings organized by severity. Language & Voice issues go with WARNINGS. Qualifying Questions issues get a dedicated section. Strategic Design Review findings get their own section with a conversational, thought-partner tone.

```
Library Audit Report
====================
Generated: <timestamp>
MCP Server: <mcpServerName>

Summary
-------
Total Entities: <count>
  - Personas: X
  - Offerings: X (Products / Services / Solutions)
  - Segments: X
  - Use Cases: X
  - Competitors: X
  - Alternatives: X
  - Buying Triggers: X
  - Objections: X
  - Proof Points: X
  - References: X

Health Score: X/100

Issues Found: X total
  - Critical: X
  - Warning: X
  - Info: X
  - Design observations: X

---

MOTIONS
=======
Motions: X total
  - [Motion name] (NET_NEW) — [offering]
  - [Motion name] (UPSELL) — [offering]

Motion Playbooks: X custom (+ X defaults)
  Types: THEMATIC: X, MILESTONE: X, ACCOUNT: X, COMPETITIVE: X

Legacy Playbooks: X still in workspace (deprecated)
  [If agents still wired to them, note which ones]

Learning Loop: [enabled/not configured] on X Motions

---

CRITICAL ISSUES (X)
===================

1. [ORPHAN] Motion "[name]" has no Default Motion Playbook
   Impact: No base narrative coverage for this offering
   Fix: Re-create the Motion or contact support

2. [MISSING] No Motions when offering exists
   Impact: Agents can't access the ICP matrix for this offering
   Fix: Create a Motion for [offering]

...

---

WARNINGS (X)
============

1. [INCOMPLETE] Persona "CTO" missing pain points
   oId: pe_def456
   Fields missing: painPoints, keyObjectives
   Fix: Add pain points and objectives

2. [DUPLICATE] Similar personas detected
   - "VP of Sales" (pe_111)
   - "Vice President of Sales" (pe_222)
   Similarity: 92%
   Fix: Consider merging these personas

3. [VOICE] Mixed perspectives in use cases
   - 8 use cases use third-person
   - 1 use case ("Build Your Pipeline") uses second-person "you/your"
   Impact: Agents produce inconsistent output
   Fix: Align to a consistent voice

4. [LANGUAGE] Capitalized coined term in "Data Integration Tools"
   Field: whereItBreaks #2 — "Rebuild Debt"
   Impact: Agents parrot this as a branded term prospects won't recognize
   Fix: Replace with descriptive language that carries equal specificity

5. [OFFERING-NAME] Offering name appears in use case
   "[Use case name]" summary references the offering directly
   Impact: Agent output sounds like a brochure
   Fix: Describe the outcome without naming the offering

6. [STALE] Competitor "[name]" not updated in 120 days
   oId: cp_xyz789
   Last updated: 2025-10-01
   Fix: Review and refresh competitive intelligence

7. [ORPHAN] Persona "Growth Marketer" not linked to any offering
   Impact: Won't appear in any Motion matrix
   Fix: Link to the relevant offering(s) via link_entities_to_offering, or archive

...

---

QUALIFYING QUESTIONS
====================
[Dedicated section for qual question analysis]

Weight Distribution:
  Personas (4 entities, 24 total questions):
    HIGH: 0 | MEDIUM: 24 | LOW: 0 | INSTANT_DISQUALIFIER: 0
    ISSUE: All MEDIUM — no weight differentiation

  Segments (4 entities, 16 total questions):
    HIGH: 0 | MEDIUM: 16 | LOW: 0 | INSTANT_DISQUALIFIER: 0
    ISSUE: All MEDIUM — no weight differentiation

  Offering (1 entity, 8 questions):
    HIGH: 3 | MEDIUM: 4 | LOW: 1 | INSTANT_DISQUALIFIER: 0
    OK — varied weights

FitType Balance:
  3 personas have NO BAD fit questions — can only score up, never down

Cross-Entity Differentiation:
  Persona questions are very similar across all 4 personas —
  agents may struggle to route to the right one

RECOMMENDATION: Run /octave:qual-doctor to tune weights with real
test cases. The audit can identify the pattern; qual-doctor can fix it.

---

DESIGN REVIEW
=============
These are observations, not errors. You know your business —
consider whether these reflect intentional choices or gaps worth addressing.

Library Shape:
  [Contextual observation about proportions]

Segment Design:
  [Challenge about whether the segment axis actually drives differentiation]

Use Case Lifecycle:
  [Observation about lifecycle coverage — execution only vs full span]

Persona Roles:
  [Question about whether personas represent deal drivers]

Evidence:
  [Challenge about proof points and references — push for real data]

Content Tone:
  [Flags for pitch copy vs operating context]

---

Recommendations
===============

1. IMMEDIATE: [Most critical fix]
2. HIGH: Tune qualifying question weights (/octave:qual-doctor)
3. HIGH: Address language/voice inconsistencies
4. MEDIUM: Review and merge duplicate entities
5. MEDIUM: Link orphaned entities to the right offerings
6. CONSIDER: Design review observations above
7. LOW: Refresh stale content

Run /octave:audit --fix to address issues interactively.
Run /octave:audit --migrate to translate legacy playbooks to Motions.
Run /octave:qual-doctor to tune qualification scoring.
```
