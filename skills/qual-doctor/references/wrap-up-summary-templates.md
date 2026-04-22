# Wrap Up Summary Templates

**Score-only mode:**
```
QUAL DOCTOR — COMPLETE
======================
Entity:    "Your Product" (product)
Section:   Offering qualification
Mode:      Score-only (single entity)
Changes:   3 applied (1 archived, 1 added, 1 description update)
Rounds:    2 (initial diagnosis + verification)

Score Improvement:
  Good fits:     9 → 9  (stable)
  Borderlines:   8 → 5  (moved into 4-6 band — fixed)
  Bad fits:      2 → 1  (stable)

Questions: 19 → 19 (1 archived, 1 added)
  GOOD fit: 11 → 11
  BAD fit:  8 → 9
```

**Routing + Scoring mode:**
```
QUAL DOCTOR — COMPLETE
======================
Section:   Persona qualification
Mode:      Routing + Scoring (3 personas)
Entities:  VP of Sales, RevOps Leader, SDR Manager
Changes:   5 applied across 2 entities
Rounds:    2 (initial diagnosis + verification)

Routing Improvement:
  Correct matches:   2/4 → 4/4  (2 routing fixes)

Score Improvement:
  In-band scores:    2/4 → 4/4  (2 score fixes)

Entity Changes:
  VP of Sales:     1 question sharpened
  RevOps Leader:   2 questions added, 1 description update
  SDR Manager:     1 question reweighted
```

If the analysis surfaced non-tuning insights, call them out separately:
```
ADDITIONAL INSIGHTS
===================
- LIBRARY GAP: The agent picked "RevOps Leader" for a marketing person.
  You may need a more distinct persona for marketing ops roles.

- SECTION INCONSISTENCY: Product scores a company at 9 but Playbook scores it
  at 2 (too large for playbook ICP). Intentional or misaligned?

- DEEP RESEARCH: 3/5 test cases had LOW confidence on tool-usage questions.
  Enabling deep research on the agent would improve answer quality.
```
