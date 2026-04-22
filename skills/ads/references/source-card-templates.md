# Source Card Templates

The seven source card templates for variant generation in Step 2F.

#### 1. Pain Language Audit (drives Pain-Focused variant)

Analyze all findings fetched via `list_findings` for this persona/segment. If no findings exist, analyze the persona entity description and matched use case descriptions instead.

```markdown
### Pain Language Audit: {Persona} × {Segment}

**Raw prospect language** (ranked by vividness — most visceral first):
1. "{exact quote or finding snippet}" — {company}, {event type}, {date}
2. "{exact quote or finding snippet}" — {company}, {event type}, {date}
3. ...

**Emotional core**: {1 sentence — the underlying feeling behind the pain. Not the business problem, the human experience. e.g., "The fear of looking incompetent in front of the board because your AI generates generic output that anyone could have written."}

**Specific dysfunction named**: {The precise, named problem — not abstract. e.g., "AI-generated content sounds like it was written by someone who's never met the buyer." NOT "poor content quality."}

**Headline derivation**: {Show how the raw language transforms into a headline. e.g., "Prospect said 'our AI just spits out generic stuff' → emotional core is frustration with wasted AI investment → dysfunction is 'AI without GTM context' → headline candidate: 'Your AI Writes Generic Copy'"}

**Data tier**: {FIELD (from real calls/emails) | LIBRARY (from entity descriptions/hypotheses) | INFERRED (synthesized from multiple signals)}
```

If the data tier is LIBRARY or INFERRED, note: "No prospect-voice data for this persona yet. Creative will be sharper once call/email integrations surface real buyer language."

---

#### 2. Proof Chain Card (drives Outcome-Focused and Data-Driven variants)

For each proof point that matches this persona/segment, build a defensibility chain.

```markdown
### Proof Chain Card: {Persona} × {Segment}

| Claim | Source Proof Point | Exact Metric | Confidence Tier | Caveats | Headline Candidate |
|-------|-------------------|-------------|-----------------|---------|-------------------|
| "3.2x pipeline growth" | Series B SaaS Pipeline Velocity (pp_xxx) | 3.2x qualified pipeline increase in one quarter | Named-anonymized (company unnamed but specific) | Single company, single quarter | "3.2x Pipeline in 1 Quarter" |
| "Sales cycles cut 38%" | Same proof point | 47 days → 29 days | Named-anonymized | Same company | "47-Day Cycles Now Take 29" |
| ... | ... | ... | ... | ... | ... |

**Confidence tiers** (strongest to weakest):
- **Named + metric**: "Acme Corp grew pipeline 3x with [product]" — named customer, specific number. Strongest possible claim.
- **Named-anonymized + metric**: "A Series B SaaS company cut cycles from 47 to 29 days" — specific number, unnamed company. Strong.
- **Aggregate**: "200+ B2B companies use [product]" — no specific metric. Weakest.

**Best available claim for this persona**: {Which proof point is the strongest match for this specific persona/segment, considering both metric impressiveness AND audience relevance?}

**Claims we CANNOT make**: {Any metrics from use case names that aren't backed by proof points. e.g., "The 90-Day Onboarding Accelerator" is a use case name — we cannot claim "90 days" unless a proof point confirms it.}
```

---

#### 3. Self-Selection Matrix (drives Question-Based variant)

For each candidate question, score its ability to make the RIGHT person stop and the WRONG person scroll past.

```markdown
### Self-Selection Matrix: {Persona} × {Segment}

| Candidate Question | Target says YES | Non-target says NO | Specificity Score | Source |
|-------------------|----------------|-------------------|-------------------|--------|
| "Still prepping audits by hand?" | VP Eng who spends weeks on manual compliance prep before every audit cycle | Product managers, marketers, sales reps — they don't own audit prep | 8/10 | Persona pain: "accountable for compliance but drowning in manual process" |
| "How many hours did your last audit take?" | Engineering leader who personally felt the pain of a recent audit cycle | Anyone not responsible for compliance workflows | 9/10 | Campaign angle: the audit prep process is broken, automation fixes it |
| "Want better compliance?" | EVERYONE | NO ONE | 1/10 — fails completely | Generic, do not use |
| ... | ... | ... | ... | ... |

**Best question for this persona**: {The question with the highest specificity score — this one becomes the headline}

**Why it works**: {Explain the self-selection mechanism in one sentence. e.g., "Only a VP Eng who has personally sat through a multi-week manual audit prep cycle would recognize this question as describing their exact situation."}
```

---

#### 4. Compounding Cost Model (drives Status Quo / Cost of Inaction variant)

Identify what decays, compounds, or breaks over time WITHOUT the solution.

```markdown
### Compounding Cost Model: {Persona} × {Segment}

**What decays without action**: {The specific thing that gets worse over time. Not "things get worse" — name it. e.g., "Every new hire rebuilds the founder's GTM knowledge from scratch because it's not in a system."}

**Rate of decay**: {How fast? Per week, per month, per hire, per campaign? e.g., "Each new rep adds 8-10 weeks of ramp time. With 4 hires per quarter, that's 32-40 person-weeks of low productivity per quarter."}

**The math of inaction**: {Quantify the cumulative cost. Use proof points inverted. e.g., "If context-aware AI cuts ramp from 10 weeks to 3, the status quo costs 7 weeks × $X per rep × N reps per quarter. That compounds every quarter you wait."}

**The tipping point**: {What breaks if they wait too long? e.g., "The first VP of Sales hire gets no context, builds their own playbook from scratch, and the founder's strategy never reaches the field. By the time you realize it, the team is selling a different product than the one you built."}

**Headline derivation**: {Show how the compounding model becomes a headline. e.g., "7 weeks of wasted ramp per rep → 'Every Hire Starts From Zero' or 'Founder-Led Selling Breaks'"}

**Key word**: {The word that makes status quo headlines work is "every" or "each" — it implies repetition and compounding. Identify the repeating unit for this persona.}
```

---

#### 5. Contrarian Thesis Card (drives Authority / Thought Leadership variant)

Identify an assumption the market holds that your data shows is wrong.

```markdown
### Contrarian Thesis Card: {Persona} × {Segment}

**What the market believes**: {The conventional wisdom. e.g., "VPs of Engineering think they need more compliance tools to manage regulatory risk."}

**What's actually true**: {The contrarian insight, backed by data. e.g., "The problem isn't the number of compliance tools — it's that audit prep is still a manual process even with modern tooling. More tools without workflow automation = more dashboards to check."}

**Source of the insight**: {Which library entity, hypothesis, or finding supports this? e.g., Hypothesis "Tool Sprawl Masks Process Debt" — "teams add monitoring tools but never automate the preparation workflow itself."}

**The reframe**: {One sentence that shifts the buyer's mental model. e.g., "You don't have a tooling problem. You have a workflow problem."}

**Why this is credible from your brand**: {Why can YOU say this and be believed? e.g., "Your product was built around automating the workflow, not just monitoring the outcome. The architecture proves the thesis."}

**Headline derivation**: {Show how the reframe becomes a headline. e.g., "Reframe: 'workflow problem, not tooling problem' → 'Compliance Has a Workflow Problem' or 'Your Audit Stack Needs Automation'"}
```

---

#### 6. Social Proof Hierarchy (drives Social Proof variant)

Rank all available proof assets by strength for this specific persona/segment.

```markdown
### Social Proof Hierarchy: {Persona} × {Segment}

**Tier 1 — Named customer + metric** (strongest):
- {Reference name}: "{specific metric}" — Relevance to this persona: {high/medium/low}. e.g., "Acme Corp: 'Cut audit prep from 3 weeks to 2 days' — high relevance for mid-market FinServ engineering leaders"

**Tier 2 — Anonymized + specific metric**:
- "{A Series B SaaS company cut sales cycles from 47 to 29 days}" — Source: pp_xxx. Relevance: {high/medium/low}

**Tier 3 — Aggregate** (weakest):
- "X companies use [product]" — if available

**Best proof for this persona**: {Which tier and which specific proof point? Why?}

**Segment match quality**: {Does the best proof point actually match this persona's segment? A FinServ proof point in a SaaS ad set is a mismatch — note it.}

**Headline derivation**: {e.g., "Acme Corp is a named reference in mid-market FinServ → 'Acme Corp Cut Audit Prep 90%' (Tier 1, high relevance)"}
```

---

#### 7. Metric Defensibility Card (drives Data-Driven variant)

For the single most dramatic metric available, stress-test its defensibility.

```markdown
### Metric Defensibility Card: {Persona} × {Segment}

**The number**: {e.g., "3.2x pipeline growth"}
**Source**: {Exact proof point oId and name}
**Context needed to interpret it**: {e.g., "This was a Series B SaaS company expanding into mid-market. One quarter. No SDR headcount added."}
**What could be challenged**: {e.g., "Single company, single quarter — could be an outlier. No industry-specific context."}
**How to defend it**: {e.g., "The proof point is specific about the conditions. If challenged, the description copy provides the context: 'A Series B team...'"}
**Should we use it?**: {YES with caveats / YES confidently / NO — not defensible for this audience}

**If NO**: {What's the next best metric? Or should we skip Data-Driven entirely and generate an extra variant of a different type?}
```
