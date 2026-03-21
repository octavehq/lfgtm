# Deal Coaching Messaging Narratives — Grounding Coaching in GTM Context

This reference defines how each coaching agent grounds its advice in the seller's Octave library data. Every coaching output produces three fields — **Buyer Mindset**, **Value Propositions**, and **Talking Points** — each grounded in specific Octave sources.

---

## Grounding Principle

The coaching model provides the **structure** (stages, principles, rubrics). The seller's Octave library provides the **substance** (messaging, data, proof). The coaching agent's job is to **weave structure and substance together** so the seller gets stage-specific coaching that sounds like their product, not a textbook.

### The Grounding Formula

```
Coaching Stage + Octave Library Data = Grounded Coaching Output
```

For every coaching output:
1. Identify which stage the coaching targets
2. Determine what each output field needs (Buyer Mindset, Value Props, Talking Points)
3. Find the most relevant Octave library data for each field
4. Synthesize into coaching that is both methodologically sound and deal-specific

---

## Resonate — Grounding Map

**Agent:** Resonance Coach
**Focus:** Discovery principles (wide, deep, high), building trust

### Buyer Mindset Grounding

Build the mindset assessment from:

| Data Source | What It Tells You | How to Use |
|------------|-------------------|------------|
| `enrich_company` → company description, industry, size | Buyer's world — context for empathy | Frame the mindset relative to their industry and scale |
| `find_crm_records` → deal stage, deal age | How far along they are | Calibrate whether buyer is truly exploratory or further than CRM suggests |
| `list_findings` → pain points | What problems they've already articulated | Assess awareness level — surface symptoms vs. root causes |
| `find_crm_activities` → recent interactions | Engagement pattern | Gauge openness — frequent engagement = open; sporadic = guarded |

**Example grounded output:**

> **Buyer Mindset:** Exploratory with underlying urgency. [Company] is a [size] [industry] company that recently [trigger from enrichment]. The champion, [Name], has articulated a surface-level problem around [pain from findings] but hasn't connected it to business impact yet. They've had [N] discovery conversations, suggesting genuine interest but uncertainty about scope. Key constraint: they've tried [prior approach from findings] and it failed, so they're cautious about committing again.

### Value Propositions Grounding

| Octave Source | Selection Logic |
|---------------|----------------|
| `get_playbook` → problem statements, discovery messaging | Select props that mirror the buyer's stated pain — validate, don't prescribe |
| `list_all_entities` → proof points (benchmarks) | Use industry benchmarks to show "we understand this problem at scale" |
| `search_knowledge_base` → relevant research | Pull research that expands the problem scope (supports going wide) |

**Selection filter:** At Resonate, only surface value props that validate pain or expand problem scope. Exclude solution-focused, ROI-focused, or competitive props.

### Talking Points Grounding

| Discovery Principle | Octave Source | Grounded Output Pattern |
|-------------------|---------------|------------------------|
| Go wide | `list_all_entities` → personas; `list_findings` → stakeholder mentions | "Who else is affected by [pain from findings]? How does this look from [persona's] perspective?" |
| Go deep | `get_playbook` → discovery questions; `list_findings` → pain points | "You mentioned [pain from findings]. In our experience with [industry from enrichment] companies, that usually traces back to [root cause from playbook]. Is that what you're seeing?" |
| Go high | `list_all_entities` → proof points (metrics); `get_playbook` → business impact messaging | "When [similar company from proof points] faced this, it was affecting [business metric]. How is that showing up at the leadership level for you?" |

**Example grounded talking point:**

> *Generic:* "Help me understand — how long has this been going on?"
>
> *Grounded:* "You mentioned your team spends significant time on [pain from findings]. In our experience with [industry from enrichment] companies using [current tool from findings], this usually starts as a tactical problem but ripples into [business metric from playbook]. How is that showing up for your team?"

---

## Elevate — Grounding Map

**Agent:** Elevation Coach
**Focus:** Case for Change, Value Framing, differentiated value, proof points

### Buyer Mindset Grounding

| Data Source | What It Tells You | How to Use |
|------------|-------------------|------------|
| `list_findings` → status quo signals, objections | How attached to current approach | Calibrate disruption intensity — gentle for open buyers, aggressive for entrenched |
| `list_findings` → competitor mentions | Whether they're actively comparing | If comparing → focus on differentiation; if not → focus on disrupting status quo |
| `find_crm_records` → stage, time in stage | Evaluation momentum | Long time in Evaluate = stuck in status quo comfort zone |
| `find_crm_activities` → multi-threading | Breadth of engagement | Single-threaded = vulnerable; multi-threaded = progressing |

### Value Propositions Grounding

| Octave Source | Selection Logic |
|---------------|----------------|
| `get_playbook` → differentiators, positioning | Core: what's unique in the playbook that matters to this buyer |
| `list_all_entities` → competitors | Filter: cross-reference to find differentiated value (unique + important + competitor can't match) |
| `list_all_entities` → proof points (results) | Proof points: specific customer results that make differentiation credible |
| `get_playbook` → value props (outcomes) | Future state vision: what the changed state looks like |

**Selection filter:** At Elevate, prioritize props that represent differentiated value. Deprioritize parity capabilities and irrelevant uniqueness.

### Talking Points Grounding

Build the Case for Change by chaining Octave data across three narrative beats. **Note:** These beat names (The Shift, The Stakes, The Possibility) are internal structure for grounding — do NOT use them as visible headers in the coaching output. Use practical, deal-specific language instead.

| Narrative Beat | Octave Source | Grounded Output Pattern |
|---------------|---------------|------------------------|
| **The Shift** | `enrich_company` → industry trends, news; `search_knowledge_base` → market research; `list_findings` → pain points; `get_playbook` → problem framing | "I've been talking to [industry from enrichment] leaders, and [specific trend from knowledge base] is creating pressure. Teams still doing [current approach from findings] built it for a world where [old assumption from playbook]. Under [trend], that approach breaks because [specific flaw]..." |
| **The Stakes** | `list_all_entities` → proof points (metrics); `get_playbook` → positioning, blind spots | "Companies that didn't adapt saw [quantified impact from proof points]. And here's what most people miss: this isn't about [surface problem from findings]. It's about [reframed need from playbook positioning]..." |
| **The Possibility** | `get_playbook` → value prop outcomes; `list_all_entities` → proof points (results) | "Customers who made this shift saw [specific outcome from proof points]..." |

For Value Framing:
```
Product voice:  [Feature from playbook — brief]
Buyer voice:    [Day-to-day change from value props — in this persona's language]
Executive voice: [P&L impact from proof points — ideally from their industry]
```

For perspective-shifting questions:
```
Source: [Competitor gap from competitor entities]
Question: "[Question that highlights the gap] — it matters because [connected to this buyer's requirements]"
```

---

## Compel — Grounding Map

**Agent:** Compel Coach
**Focus:** Business case building (Value Discovery + Value Proof), Why Now Case, champion enablement

### Buyer Mindset Grounding

| Data Source | What It Tells You | How to Use |
|------------|-------------------|------------|
| `find_crm_records` → deal amount, stage, close date | Deal position and financial scope | Frame the business case relative to deal size |
| `find_crm_activities` → exec engagement | Whether economic buyer is in play | If no exec engagement → champion enablement is priority |
| `generate_crm_context` → synthesized narrative | Full deal story | Understand decision dynamics, competing priorities |
| `list_all_entities` → personas (champion) | Champion's role and influence | Assess: can they sell internally, or do they need heavy coaching? |

### Value Propositions Grounding

| Octave Source | Selection Logic |
|---------------|----------------|
| `list_all_entities` → proof points (quantified) | Core: props with specific ROI metrics from similar customers |
| `enrich_company` → strategic initiatives | Alignment: props that map to the buyer's stated priorities |
| `get_playbook` → ROI data, outcomes | Financial: props with quantifiable outcomes for business case |
| `list_all_entities` → personas | Stakeholder mapping: tailor props per decision maker's priorities |

**Selection filter:** At Compel, only surface props with quantified outcomes or strategic alignment. Exclude discovery-stage props and generic positioning.

### Talking Points Grounding

#### Business Case Building

| Phase | Octave Source | Grounded Output Pattern |
|-------|---------------|------------------------|
| **Value Discovery** | `find_crm_records` → deal amount; `enrich_company` → revenue, headcount | "Based on [company size from enrichment], if [metric] improves by [benchmark from proof points]..." |
| **Value Proof — Before/After** | `list_findings` → pain points; `get_playbook` → use cases | "Today your team spends [current effort from findings] on [process]. In the new model, [future state from playbook]..." |
| **Value Proof — Quantify** | `list_all_entities` → proof points (quantified) | "Based on what [similar customer from proof points] achieved — [metric improvement] — that translates to [dollar impact]..." |
| **Value Chain** | `get_playbook` → value props (full chain) | "[Capability] → [workflow improvement] → [business outcome] → [$financial_result] — mapped through [buyer's org from personas]" |

#### Why Now Case

| Dimension | Octave Source | Grounded Output Pattern |
|-----------|---------------|------------------------|
| Business urgency | `enrich_company` → strategic initiatives; `generate_crm_context`; `find_crm_records` → timeline; `list_all_entities` → proof points | "Your company prioritized [initiative from enrichment]. This supports it. Every month of delay costs [monthly_burn from benchmarks]. Over [timeline from CRM], that's [total]..." |
| Personal urgency | `list_all_entities` → personas (champion); `find_crm_activities` → interactions | "As [champion's role from persona], delivering this initiative gives you visibility on [strategic priority]..." |

#### Champion Enablement (Executive Decision Kit)

| Material | Octave Source | Content |
|----------|---------------|---------|
| Executive Summary | CRM context + playbook positioning | One paragraph: problem → solution → impact → ask |
| Financial Impact | Proof points (model from similar customers) | Investment, returns, payback period |
| Risk Framing | Findings (risk of inaction) vs. proof points (risk of acting) | Asymmetric: NOT buying is riskier |
| Talk Track | Playbook executive messaging + personas | Specific words for the champion's executive conversation |
| Objection Prep | Findings (likely pushbacks) + proof points (counters) | Response for every likely internal objection |

---

## Cross-Stage Agents — Grounding Maps

### Negotiation Strategist

| Output Field | Octave Source | Mapping Logic |
|-------------|---------------|---------------|
| Value Anchor | Prior Compel business case + CRM deal amount | Reference quantified value already established |
| Concession Inventory | Playbook packaging/pricing data | Know what can be traded without destroying value |
| Buyer BATNA | Competitor entities | Understand the buyer's best alternative |
| Relationship Leverage | CRM activities + findings (sentiment) | Gauge relationship strength for negotiation approach |

### Objection Handler

| Output Field | Octave Source | Mapping Logic |
|-------------|---------------|---------------|
| Objection Context | Findings → objections | Match to stage gap (see objection mapping in coaching-agents.md) |
| Resolution Approach | frameworks.md → relevant stage | Pull Talking Points for the gap stage |
| Supporting Evidence | Proof points | Counter objections with quantified data |
| Playbook Response | Playbook → objection handling section | Combine stage coaching with product-specific responses |

---

## Quality Checklist for Grounded Coaching

Before delivering any coaching output, verify:

- [ ] **Buyer Mindset is specific** — References actual data (enrichment, CRM, findings), not generic psychology
- [ ] **Value Props match the stage** — Resonate = pain-resonant, Elevate = differentiation, Compel = ROI/strategic
- [ ] **Talking Points are grounded** — Every talk track references specific deal data or library content
- [ ] **Persona-appropriate** — Language and framing match the target persona's level and priorities
- [ ] **Evidence-backed** — Claims supported by proof points, enrichment data, or CRM signals
- [ ] **Actionable** — Every coaching point includes a specific next action or talk track
- [ ] **Stage-appropriate** — Advice matches the coaching stage, not a different stage's methodology
- [ ] **Playbook-consistent** — Talk tracks align with the seller's established messaging and positioning
- [ ] **No duplication** — Each piece of information appears in exactly one output field
