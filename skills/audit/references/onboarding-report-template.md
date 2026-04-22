# Onboarding Report Template

```
Library Onboarding Report
=========================
Generated: <timestamp>
MCP Server: <mcpServerName>

Current State
-------------
Total Active Entities: <count>
  - Products: X
  - Personas: X
  - Segments: X
  - Playbooks: X
  - Use Cases: X
  - Competitors: X
  - Alternatives: X
  - Buying Triggers: X
  - Proof Points: X
  - References: X

Readiness: <tier label>
  Tier 1 (Foundation): <complete / partial / not started>
  Tier 2 (Execution):  <complete / partial / not started>
  Tier 3 (Depth):      <complete / partial / not started>
  Tier 4 (Evidence):   <complete / partial / not started>

---

BUILD NEXT
==========

Your agents need [specific thing] to [specific capability].

Priority 1: [what to build]
  Why: [what agents can't do without it]

Priority 2: [what to build]
  Why: [what agents can't do without it]

Priority 3: [what to build]
  ...

---

DESIGN CHALLENGES
=================
[Challenge questions from Step 5-O, tailored to what the user is about to build.
These are questions for the user to answer, NOT prescriptive templates.]

Segments:
  Your [current segments] suggest [observation].
  CHALLENGE: [Specific question about their business that would
  sharpen their segment design]

Personas:
  CHALLENGE: [Question that pushes them to justify their persona choices]

...

---

QUALIFYING QUESTIONS
====================
[Weight distribution analysis from the qual questions audit check]
[If all-MEDIUM, flag it and recommend running /octave:qual-doctor]

---

EARLY ISSUES (X)
=================
[Light cleanup findings from Step 6-O on existing content]

1. [INCOMPLETE] Persona "CTO" is a stub — only has name and one-line description
   Fix: Flesh out pain points, objectives, and responsibilities

2. [VOICE] Product description uses "you/your" while personas use "they/their"
   Fix: Align to one voice before building more entities

---

Recommendations
===============

1. NEXT SESSION: Build [Tier X items] — but think through the design
   challenges above first
2. BEFORE BUILDING MORE: Fix [early issues] so new entities match
3. DESIGN DECISION: [Most important challenge question from above]

Run /octave:audit --fix to address early issues interactively.
Run /octave:qual-doctor to tune qualifying question weights and scoring.
```
