# Deal Stage Mapping & Inference

This reference defines how to map CRM deal stages to the Resonate → Elevate → Compel coaching model, how to infer the correct stage from available signals, and how to diagnose root causes for stalled deals.

---

## Buyer's Journey → Coaching Stage Mapping

| Journey Phase | Buyer Activity | Coaching Stage | Focus |
|--------------|---------------|----------------|-------|
| **Explore** | Exploring whether a problem exists and is worth solving | **Resonate** | Diagnose the real problem; build shared understanding |
| **Evaluate** | Evaluating options; building a case for change internally | **Elevate** | Disrupt status quo; differentiate from alternatives |
| **Justify** | Building the business case; seeking budget and approval | **Compel** | Quantify value; build executive-ready justification |
| **Decide** | Making the final decision; negotiating terms | **Compel** | Create urgency; arm the champion; enable the decision |
| **Close** | Contract execution; procurement; legal review | **Compel** + Negotiation Strategist | Maintain urgency; protect value through negotiation |

---

## CRM Stage → Coaching Stage Mapping

### Standard Mappings

| CRM Stage | Journey Phase | Primary Coaching Stage | Notes |
|-----------|--------------|----------------------|-------|
| Prospecting | Explore | **Resonate** | Early: focus on problem diagnosis |
| Discovery | Explore | **Resonate** | Deep diagnosis phase |
| Qualification | Explore → Evaluate | **Resonate** → **Elevate** | Transitioning: problem confirmed, begin case for change |
| Demo | Evaluate | **Elevate** | Show change is needed AND you're the right choice |
| Evaluation | Evaluate | **Elevate** | Buyer comparing; lead with differentiation |
| Proposal | Justify | **Compel** | Lead with value quantification |
| Negotiation | Decide | **Compel** + Negotiation Strategist | Decision justification + deal protection |
| Closing | Decide | **Compel** | Final commitment; urgency critical |
| Contract | Close | **Compel** + Negotiation Strategist | Procurement and legal; protect scope and value |
| Pending | Close | **Compel** | Administrative close; maintain momentum |
| Closed Won | — | — | Post-sale; not in scope |
| Closed Lost | — | Root Cause Analysis | Diagnose which coaching stage failed |

### Custom Stage Name Matching

CRM systems use varied naming. Use fuzzy matching:

| Keywords in Stage Name | Map To |
|----------------------|--------|
| prospect, lead, inbound, new, initial | Explore → **Resonate** |
| discover, diagnose, explore, assess, intake | Explore → **Resonate** |
| qualify, qualified, fit, scoping | Explore/Evaluate → **Resonate** / **Elevate** |
| demo, demonstration, show, present, pitch | Evaluate → **Elevate** |
| evaluate, evaluation, compare, trial, poc, pilot | Evaluate → **Elevate** |
| propose, proposal, quote, pricing, business case | Justify → **Compel** |
| negotiate, negotiation, terms, contract review | Decide → **Compel** |
| close, closing, commit, decision, final | Decide → **Compel** |
| contract, legal, procurement, order, signing | Close → **Compel** |

---

## Stage Inference Algorithm

### Signal Weights

| Signal | Weight | Source | What It Tells Us |
|--------|--------|--------|-----------------|
| CRM deal stage | 40% | `find_crm_records` → stage field | Direct intent signal — where CRM says the deal is |
| Conversation findings | 30% | `list_findings` → pain points, competitor mentions, ROI keywords | What the buyer is talking about reveals their mindset |
| Deal activity patterns | 20% | `list_events` → demos, proposals, exec meetings | Actions taken indicate progression |
| Time in stage | 10% | `find_crm_records` → days in stage | Stall detection — long time suggests a gap |

### Signal-to-Stage Scoring

#### CRM Deal Stage (40% weight)
Map the CRM stage using the table above. Assign 100% confidence to the mapped coaching stage.

#### Conversation Findings (30% weight)

| Finding Signal | Points Toward | Confidence |
|---------------|---------------|------------|
| Pain points mentioned but not quantified | **Resonate** | High |
| "Happy with current vendor" / status quo defense | **Elevate** (gap — status quo not disrupted) | High |
| Pain points quantified with business impact | **Elevate** | High |
| Competitor names mentioned | **Elevate** | High |
| "What makes you different?" | **Elevate** | High |
| ROI / pricing / budget discussed | **Compel** | High |
| Executive stakeholder engaged | **Compel** | Medium |
| Timeline / urgency language | **Compel** | Medium |
| "Can you justify the cost?" | **Compel** | High |
| "I need to get approval" / boss sign-off | **Compel** | High |

#### Deal Activity Patterns (20% weight)

| Activity Signal | Points Toward | Confidence |
|----------------|---------------|------------|
| Initial meeting / intro call | **Resonate** | High |
| Discovery call completed | **Resonate** → **Elevate** | High |
| Demo / presentation delivered | **Elevate** | High |
| Technical evaluation / POC underway | **Elevate** | High |
| Proposal / quote sent | **Compel** | High |
| Executive meeting scheduled or completed | **Compel** | High |
| Contract sent / redlines in progress | **Compel** | High |
| No activity in 14+ days | Stall — see diagnosis | High |

#### Time in Stage (10% weight)

| Time Signal | Interpretation | Action |
|-------------|---------------|--------|
| < median time | On track | Continue with inferred stage |
| 1-2x median time | Slowing | Flag potential stall |
| > 2x median time | Stalled | Route to root cause diagnosis |
| > 3x median time | At risk | Escalate; consider stage regression |

### Combining Signals

1. Score each signal against all three stages (Resonate, Elevate, Compel)
2. Apply weights (40/30/20/10)
3. Normalize to 100%
4. Highest-scoring stage is the inference
5. Confidence:
   - **High**: Top stage is 15+ points ahead
   - **Medium**: Top stage is 5-15 points ahead
   - **Low**: Top stage is < 5 points ahead (multiple stages plausible)

### CRM Absence Handling

CRM absence is a data hygiene issue, not a deal health signal. If CRM data is missing but activity signals are strong and consistent, do NOT downgrade confidence. Redistribute the CRM weight (40%) across other signals proportionally: Findings ~45%, Activities ~40%, Time ~15%.

### Inference Output Format

```
STAGE INFERENCE
===============
Stage: [Resonate / Elevate / Compel]
Confidence: [High / Medium / Low]
Buyer's Journey Phase: [Phase Name]

EVIDENCE
--------
CRM Stage (40%): "[Stage Name]" → maps to [Stage]  [or "No CRM record — data gap, not deal gap"]
Findings (30%): [Key signals and what they indicate]
Activities (20%): [Key activities and what stage they suggest]
Time (10%): [Days in stage vs. median; stall assessment]

RECOMMENDATION
--------------
[1-2 sentences on why this stage and what to focus on]
```

---

## Stage Transition Indicators

### Resonate → Elevate

The deal is ready to advance when:
- [ ] A clear, agreed problem statement exists
- [ ] The problem is understood from multiple perspectives across the organization
- [ ] Key stakeholders have been identified
- [ ] The buyer agrees the problem is worth solving
- [ ] Discovery is deep enough to support a case for change

### Elevate → Compel

The deal is ready to advance when:
- [ ] The buyer acknowledges the status quo is untenable
- [ ] Your differentiation is understood and valued
- [ ] Decision criteria favor your strengths
- [ ] The buyer is asking "how much?" and "what's the ROI?"
- [ ] A preferred vendor has emerged (ideally you)
- [ ] A champion is forming internally

### Compel → Won

The deal is ready to close when:
- [ ] A quantified business case exists (co-created with buyer's numbers)
- [ ] The champion can articulate ROI in executive language
- [ ] Budget is identified or a path to budget is clear
- [ ] The economic buyer has approved or is about to
- [ ] A compelling event drives urgency
- [ ] All detractors have been addressed

---

## MEDDPICC Integration (Optional)

Each coaching stage aligns with MEDDPICC elements. Use this for additional deal gap analysis when requested:

| MEDDPICC Element | Primary Stage | What Good Looks Like |
|-----------------|--------------|---------------------|
| **M**etrics | Compel | Quantified business impact co-created with buyer |
| **E**conomic Buyer | Compel | Identified, engaged, and aligned on strategic value |
| **D**ecision Criteria | Elevate | Shaped by seller to favor differentiated capabilities |
| **D**ecision Process | Compel | Mapped with timeline, stakeholders, and approval steps |
| **P**aper Process | Compel | Legal, procurement, and contract process understood |
| **I**mplicated Pain | Resonate / Elevate | Pain diagnosed (Resonate) and connected to urgency (Elevate) |
| **C**hampion | Compel | Armed with business case and executive talk track |
| **C**ompetition | Elevate | Mapped, differentiated against, perspective-shifting questions deployed |

### MEDDPICC Gap → Coaching Action

| Gap | Coaching Action |
|-----|----------------|
| No Metrics defined | Compel — Value Discovery + Value Proof to co-create business case |
| Economic Buyer not engaged | Compel — Why Now Case to create executive urgency |
| Decision Criteria not shaped | Elevate — Differentiated value to shape criteria |
| Decision Process unclear | Compel — Map process and identify blockers |
| Pain not quantified | Resonate → Elevate — Diagnose then build Case for Change |
| No Champion identified | Compel — Find and arm an internal advocate |
| Competition unknown | Elevate — Competitive mapping and perspective-shifting questions |

---

## Root Cause Diagnosis for Stalled Deals

When a deal is stalled (time in stage > 2x median), diagnose which coaching stage gap is the root cause:

### Stalled at Explore (Resonate gap)

**Symptoms:**
- Buyer keeps scheduling "more discovery" calls
- Can't articulate the problem in their own words
- Multiple stakeholders have different views of the problem
- No urgency despite expressed interest

**Resolution:**
- Return to discovery principles — especially go deep and go high
- Get the problem statement in writing and validated by multiple stakeholders
- Make sure the problem is understood from the perspective of operators, leaders, and executives

### Stalled at Evaluate (Elevate gap)

**Symptoms:**
- "We're still evaluating whether to do anything"
- "We have other priorities right now"
- Champion loses internal momentum
- No executive engagement

**Resolution:**
- Introduce blind spots — new information the buyer doesn't have
- Quantify the cost of inaction for this specific company
- Use proof points from similar companies that delayed and suffered
- Re-engage with a fresh look at The Shift — what's changing in their market
- If differentiation is the issue: refocus on differentiated value, deploy proof points

### Stalled at Justify/Decide (Compel gap)

**Symptoms:**
- "We need to build the business case" (value gap)
- "My boss hasn't signed off yet" (champion gap)
- "Can you do anything on pricing?" (value gap masquerading as price)
- Deal pushed from one close date to the next (urgency gap)

**Resolution (value gap):**
- Co-create (not deliver) a business case using buyer's own metrics
- Build before/after model with their numbers
- Map the value chain to connect capability to financial outcome

**Resolution (urgency gap):**
- Build the Why Now Case — both business and personal urgency
- Create or strengthen the compelling event
- Arm the champion with an executive decision kit

**Resolution (champion gap):**
- Build executive-ready materials the champion can present
- Co-create the talk track for the executive conversation
- Facilitate exec-to-exec alignment

### Stalled at Close (Execution gap)

**Symptoms:**
- Contract in legal review for weeks
- Procurement requesting additional documentation
- Key stakeholder goes silent
- New competing priority emerges

**Resolution:**
- Re-establish the compelling event with cost-of-delay data
- Offer to participate in legal/procurement calls
- Engage executive sponsor to prioritize
- Activate Negotiation Strategist to protect terms while unblocking
