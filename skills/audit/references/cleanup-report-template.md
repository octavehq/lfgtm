# Cleanup Report Template

```
Library Audit Report
====================
Generated: <timestamp>
MCP Server: <mcpServerName>

Summary
-------
Total Entities: <count>
  - Personas: X
  - Products: X
  - Playbooks: X
  - Segments: X
  - Use Cases: X
  - Competitors: X
  - Alternatives: X
  - Buying Triggers: X
  - Proof Points: X
  - References: X

Health Score: X/100

Issues Found: X total
  - Critical: X
  - Warning: X
  - Info: X
  - Design observations: X

---

CRITICAL ISSUES (X)
===================

1. [ORPHAN] Playbook "Enterprise Sales" has no linked personas
   oId: pb_abc123
   Impact: Cannot generate persona-specific messaging
   Fix: Link buyer personas to this playbook

2. [MISSING] No proof points defined
   Impact: Cannot support claims with evidence
   Action: Do you have customer results to encode? If yes, add them.
   If not, skip this tier — don't fabricate.

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

5. [PRODUCT-NAME] Product name appears in use case
   "Deploy Strategy-Aware Agents" summary references "Acme" directly
   Impact: Agent output sounds like a brochure
   Fix: Describe the outcome without naming the product

6. [STALE] Competitor "Acme Corp" not updated in 120 days
   oId: cp_xyz789
   Last updated: 2025-10-01
   Fix: Review and refresh competitive intelligence

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

  Product (1 entity, 8 questions):
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
5. CONSIDER: Design review observations above
6. LOW: Refresh stale content

Run /octave:audit --fix to address issues interactively.
Run /octave:qual-doctor to tune qualification scoring.
```
