# Full Briefing Output Template

```
MORNING BRIEFING — [Date]
===========================

DEALS THAT NEED YOU TODAY ([N])
-------------------------------

[For each deal with a critical or high-priority signal:]

[Priority icon] [N]. [Company Name] — [Signal headline]
   Signal: [What happened and why it matters]
   Context: [Relevant history — avg response time, deal stage, last interaction]
   Suggested: [Specific skill command to run next]

Priority icons:
  🔴 = Critical (act today)
  🟡 = High (act this week)

Examples:
  🔴 1. Acme Corp — Champion went silent
     Signal: No response in 12 days (avg response time was 2 days)
     Context: Deal in Evaluation stage, $180K, 3 stakeholders engaged
     Suggested: /octave:pipeline stalled acme.com

  🔴 2. TechFlow — Competitor mentioned for first time
     Signal: "Gong" mentioned in yesterday's call — not previously in play
     Context: Deal in Demo stage, $95K, single-threaded with VP Sales
     Suggested: /octave:battlecard --competitor "Gong"

  🟡 3. DataCorp — Advanced to Negotiation
     Signal: Deal moved from Evaluation → Negotiation yesterday
     Context: $220K, strong champion, 45 days in pipeline
     Suggested: /octave:pipeline close datacorp.com

---

EMERGING PATTERNS ([N])
-----------------------

[Compare current period findings to previous period. Surface:]

Objections Trending Up:
  ↑ "[Objection theme]" — [N] instances this period (up from [M] last period)
    Affected personas: [Persona list]
    In playbook: [Yes/No — if No, flag as gap]
    Suggested: /octave:enablement objections --topic "[topic]"

Objections Trending Down:
  ↓ "[Objection theme]" — [N] this period (down from [M])
    Interpretation: [Likely reason — e.g., new messaging landed, market shifted]

New Competitors Appearing:
  🆕 "[Competitor]" mentioned [N] times — not previously tracked
    Deals affected: [Company list]
    Suggested: /octave:battlecard --competitor "[name]"

Hot Proof Points:
  🔥 "[Proof point]" cited in [N] conversations this period
    Context: [Which deals, which personas responded well]
    This is your strongest weapon right now.

Cold Proof Points:
  ❄️  "[Proof point]" — 0 citations in [period]
    Last used: [date]
    Consider: Refresh or retire?

---

PIPELINE HEALTH
---------------

| Metric | This Period | Last Period | Trend |
|--------|------------|-------------|-------|
| New deals | [N] ($[X]K) | [M] ($[Y]K) | [↑/↓/→] |
| Advanced | [N] deals moved forward | [M] | [↑/↓/→] |
| At risk | [N] (see Deals above) | [M] | [↑/↓/→] |
| Closed won | [N] ($[X]K) | [M] ($[Y]K) | [↑/↓/→] |
| Closed lost | [N] ($[X]K) | [M] ($[Y]K) | [↑/↓/→] |

Activity Pulse:
- Calls this period: [N] (vs [M] last period)
- Emails sent: [N] (vs [M])
- Replies received: [N] (vs [M])
- Reply rate: [X]% (vs [Y]%)

Engagement Gaps:
- [N] active deals with no activity in [X]+ days
  [List top 3 by deal value]

---

CONTENT PERFORMANCE
-------------------

Most-Used Proof Points (this period):
1. "[Proof point]" — [N] citations
2. "[Proof point]" — [N] citations

Most-Referenced Value Props:
1. "[Value prop]" — appeared in [N] conversations
2. "[Value prop]" — appeared in [N] conversations

Stale Content:
- "[Playbook/entity]" — 0 activations in [period] — stale?
- "[Proof point]" — last cited [N] days ago

Library Gaps Detected:
- Objection "[X]" raised [N] times but no playbook response exists
- Competitor "[Y]" mentioned [N] times but no battlecard exists
- Persona "[Z]" appeared in [N] deals but isn't in library

---

YOUR TOP 3 ACTIONS TODAY
=========================

1. [Most urgent action] → [Command to run]
2. [Second priority] → [Command to run]
3. [Third priority] → [Command to run]

---

Dive deeper:
1. Show me deal details for [deal]
2. Drill into a pattern
3. Update library with detected gaps
4. Run a different period
```
