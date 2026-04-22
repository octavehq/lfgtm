# Per-Mismatch Deep Dive Templates

**Score mismatch example** (score-only mode or right entity, wrong score):
```
WHY Acme Corp scored 8 (you expected 4-6):
==========================================

GOOD fit questions pushing the score UP:
  #1 [HIGH]   "500+ employees?"           → YES (HIGH confidence)
  #5 [HIGH]   "Dedicated security team?"   → YES (MEDIUM confidence)

BAD fit questions that SHOULD have pulled it down but didn't:
  #12 [MEDIUM] "Fewer than 500 employees?" → NO — correct, they're large

WHAT'S MISSING: You said Acme Corp should be lower because "they use a competitor."
  → No existing question checks for competitor tool usage.
  → RECOMMENDATION: Add BAD fit question [HIGH weight]:
    "Does the company currently use a direct competitor product in the same category?"
  → Expected impact: drops competitor-using companies by ~1.5-2 points

ENTITY DESCRIPTION CHECK: The description says nothing about competitive landscape.
  → Adding competitive context to the description would help edge case interpretation.
```

**Routing mismatch example** (wrong entity selected):
```
WHY Bob Smith matched "VP of Sales" instead of "RevOps Leader":
================================================================

The agent scored Bob against BOTH personas and picked the higher score:
  VP of Sales:    7  ← selected (higher)
  RevOps Leader:  5  ← expected match

VP of Sales scored higher because:
  #1 [HIGH] "Manages quota-carrying reps?"  → YES (MEDIUM) — Bob manages 2 SDRs
  #3 [HIGH] "Owns pipeline number?"         → YES (MEDIUM) — Bob reports on pipeline

RevOps Leader scored lower because:
  #2 [HIGH] "Owns tech stack decisions?"    → NO (LOW) — couldn't verify
  #4 [HIGH] "Builds/manages dashboards?"    → NO (LOW) — no evidence found

ROOT CAUSE: Bob has a hybrid role (RevOps + some SDR management). The VP of Sales
persona's questions are too broad — managing 2 SDRs shouldn't qualify as "manages
quota-carrying reps" the way a VP with 50 reps does.

RECOMMENDATIONS:
  1. Sharpen VP of Sales Q1: "Manages a team of 5+ quota-carrying sales reps?"
     → Stops hybrid ops roles from matching VP of Sales
  2. Add RevOps Q: "Is the person's primary function building/maintaining revenue
     systems and processes rather than directly managing sellers?"
     → Gives RevOps a stronger signal to win the routing contest
  3. Update RevOps description to mention: "RevOps leaders may manage small teams
     of SDRs or analysts alongside their systems responsibilities"
     → Gives the agent context for hybrid roles
```
