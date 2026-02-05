---
name: brainstorm
description: Brainstorm campaigns, playbook ideas, lead magnets, CTAs, and growth experiments using your GTM library
---

# /octave:brainstorm - GTM Ideation Engine

Interactive brainstorming for campaigns, playbook concepts, lead magnets, CTAs, offers, and growth experiments—all grounded in your Octave library context.

## Usage

```
/octave:brainstorm [topic]
```

## Examples

```
/octave:brainstorm                           # Open-ended, asks what to brainstorm
/octave:brainstorm campaigns for enterprise  # Campaign ideas for enterprise segment
/octave:brainstorm lead magnets              # Content offer ideas
/octave:brainstorm playbook pack             # Generate playbook concepts for TAM
/octave:brainstorm CTAs for CFOs             # Call-to-action ideas for persona
```

## Instructions

When the user runs `/octave:brainstorm`:

### Step 1: Determine Brainstorm Type

If no topic provided, ask:

```
What would you like to brainstorm?

1. Campaign Ideas - Outreach campaigns for specific segments/personas
2. Playbook Concepts - New playbook ideas to cover your TAM
3. Lead Magnets - Content offers to attract prospects
4. CTAs & Offers - Calls-to-action and promotional offers
5. Growth Experiments - Test ideas to improve conversion
6. Messaging Angles - New positioning approaches
7. Something else - Tell me what you're thinking

Your choice (or describe freely):
```

If topic is provided, infer the type and confirm:

```
I'll brainstorm lead magnet ideas for you. Sound good?
(Or tell me more about what you're looking for)
```

### Step 2: Gather Context

Use MCP tools based on brainstorm type:

**For Campaigns:**
```
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "playbook" })
- list_all_entities({ entityType: "use_case" })
```

**For Playbook Concepts:**
```
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "product" })
- list_all_entities({ entityType: "use_case" })
- list_all_entities({ entityType: "playbook" })  # To see existing coverage
```

**For Lead Magnets:**
```
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "use_case" })
- list_all_entities({ entityType: "proof_point" })
- search_knowledge_base({ query: "pain points challenges problems" })
```

**For CTAs & Offers:**
```
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "product" })
- list_all_entities({ entityType: "proof_point" })
```

**For Growth Experiments:**
```
- list_all_entities({ entityType: "playbook" })
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
```

### Step 3: Ask Scoping Questions (Optional)

If the request is broad, narrow the focus:

**For Campaigns:**
```
Let me tailor these campaign ideas. Quick questions:

1. Target segment? (e.g., Enterprise SaaS, Healthcare, All)
2. Target persona? (e.g., CTOs, VP Sales, Multiple)
3. Campaign goal? (e.g., awareness, demos, pipeline)
4. Channel preference? (e.g., email, LinkedIn, multi-channel)

(Answer any/all, or say "surprise me")
```

**For Playbook Pack:**
```
To generate playbook concepts for your TAM:

1. What verticals/industries should we cover?
2. Company size focus? (SMB, Mid-market, Enterprise, All)
3. Any specific use cases to emphasize?
4. Gaps you've noticed in current playbook coverage?

(Share what you know, or I'll analyze your library for gaps)
```

### Step 4: Generate Ideas

Present ideas in a structured, actionable format:

---

#### Campaign Ideas Output

```
Campaign Ideas: [Segment/Persona]
=================================

Based on your library, here are campaign concepts:

---

CAMPAIGN 1: "The Hidden Cost of Manual Processes"
Target: VP of Operations at Mid-Market Manufacturing
Channel: Email sequence + LinkedIn

Hook:
"Most operations leaders lose 20+ hours/week to manual data entry.
Here's how three companies eliminated it."

Why This Works:
- Addresses pain point: "Manual processes consuming team time" (from your VP Ops persona)
- Supported by proof point: "Acme Corp reduced manual work by 85%"
- Aligns with playbook: "Operational Efficiency"

Sequence Outline:
1. Pain agitation (the hidden cost)
2. Social proof (customer story)
3. Solution tease (how they did it)
4. CTA (15-min assessment call)

---

CAMPAIGN 2: "Security Leaders Share Their Automation Playbook"
Target: CISO at Enterprise Financial Services
Channel: Webinar + nurture sequence

Hook:
"Join 3 security leaders from Fortune 500 companies as they share
how they automated compliance without adding headcount."

Why This Works:
- Addresses pain point: "Compliance burden with limited resources"
- Leverages reference: "Major Bank case study"
- Positions against competitor weakness: "Legacy tools require large teams"

---

[3-5 total campaign ideas]

---

Next Steps:
1. Pick a campaign to develop further
2. Generate the full email sequence (/octave:generate)
3. Save as a new playbook (/octave:library create playbook)

Which campaign interests you most?
```

---

#### Playbook Pack Output

```
Playbook Pack: Covering Your TAM
================================

Current Coverage Analysis:
- You have 4 playbooks covering 3 segments
- Gap identified: No playbook for [Healthcare] segment
- Gap identified: No playbook targeting [CFO] persona
- Opportunity: [Compliance use case] appears in 0 playbooks

Proposed Playbook Pack (5 new playbooks):

---

PLAYBOOK 1: "Healthcare Digital Transformation"
Segment: Healthcare & Life Sciences
Primary Persona: CTO / VP of IT
Secondary Persona: Chief Medical Information Officer

Strategic Angle:
Position as the secure, compliant foundation for healthcare innovation.
Lead with HIPAA compliance, follow with interoperability and patient outcomes.

Key Use Cases:
- Patient data integration
- Clinical workflow automation
- Compliance audit automation

Differentiators to Emphasize:
- HIPAA-compliant by design
- Healthcare-specific integrations
- Proven with 3 health systems

Estimated Fit: HIGH (your product has healthcare references)

---

PLAYBOOK 2: "CFO's Guide to Operational ROI"
Segment: Cross-vertical (Enterprise)
Primary Persona: CFO / VP Finance
Secondary Persona: VP Operations

Strategic Angle:
Financial lens on operational efficiency. Lead with ROI metrics,
payback period, and cost avoidance. Avoid technical depth.

Key Use Cases:
- Cost reduction through automation
- Budget optimization
- Financial close acceleration

Differentiators to Emphasize:
- Fastest time-to-value (proof point: 6-week average)
- Measurable ROI guarantee
- No additional headcount required

Estimated Fit: HIGH (strong proof points for ROI)

---

[Continue for all 5 playbooks]

---

Coverage After Implementation:
- Segments covered: 3 → 6
- Personas with dedicated playbooks: 4 → 7
- Use case coverage: 60% → 90%

Next Steps:
1. Pick playbooks to create
2. I'll generate full playbook content
3. Create in Octave (/octave:library create playbook)

Which playbooks should we build first?
```

---

#### Lead Magnet Ideas Output

```
Lead Magnet Ideas
=================

Based on your personas and their pain points:

---

LEAD MAGNET 1: "The [Industry] Automation Maturity Assessment"
Type: Interactive assessment / Quiz
Target Persona: VP of Operations, CTO

Concept:
10-question self-assessment that scores their automation maturity
across 5 dimensions. Personalized report with recommendations.

Why It Works:
- Addresses pain point: "Don't know where to start"
- Generates qualified leads (assessment answers = qualification data)
- Natural CTA: "Get expert review of your results"

Gated Content Includes:
- Maturity score (1-100)
- Comparison to industry benchmarks
- Top 3 quick wins
- Custom roadmap based on answers

---

LEAD MAGNET 2: "ROI Calculator: What's Manual Work Costing You?"
Type: Interactive calculator
Target Persona: CFO, VP Finance, VP Operations

Concept:
Simple calculator: Input team size, hours on manual tasks, average salary.
Output: Annual cost of manual work + potential savings.

Why It Works:
- CFO pain point: "Need to justify investments with hard numbers"
- Creates urgency with personalized data
- Natural CTA: "See how [Company] achieved these savings"

---

LEAD MAGNET 3: "[Persona]'s Playbook: 5 Strategies for [Outcome]"
Type: PDF guide / Ebook
Target Persona: [Specific persona from library]

Concept:
Tactical guide with 5 actionable strategies. Include customer quotes,
metrics, and implementation tips. Brand as peer-to-peer advice.

Why It Works:
- Positions you as thought leader
- Includes proof points naturally
- Evergreen content for nurture sequences

---

[3-5 total ideas]

---

For each lead magnet, I can help you:
1. Create the content outline
2. Draft the copy
3. Design the promotion campaign

Which one should we develop?
```

---

#### CTA & Offer Ideas Output

```
CTA & Offer Ideas for [Persona]
===============================

Based on [Persona] pain points and buying behavior:

---

LOW COMMITMENT CTAs (Top of Funnel)
-----------------------------------

1. "Get the [Industry] Benchmark Report"
   Why: Educational, non-salesy, establishes expertise
   Best for: Cold outreach, ads

2. "See How [Reference Customer] Did It"
   Why: Social proof, curiosity-driven
   Best for: Email sequences, LinkedIn

3. "Take the 2-Minute Assessment"
   Why: Interactive, personalized, low effort
   Best for: Website, ads

---

MEDIUM COMMITMENT CTAs (Middle of Funnel)
-----------------------------------------

4. "Join Our [Persona] Roundtable"
   Why: Peer learning, community, non-salesy
   Best for: Nurture sequences, LinkedIn

5. "Get Your Custom ROI Analysis"
   Why: Personalized value, requires brief call
   Best for: Warm leads, follow-ups

6. "Watch the 15-Min Demo"
   Why: Self-serve, shows product value
   Best for: Website, email

---

HIGH COMMITMENT CTAs (Bottom of Funnel)
---------------------------------------

7. "Start Your Free Pilot"
   Why: Risk-free trial, proves value
   Best for: Qualified leads

8. "Book Your Strategy Session"
   Why: Consultative, high-touch
   Best for: Enterprise prospects

9. "Get Pricing for Your Team"
   Why: Direct, buyer-ready
   Best for: Hot leads, website

---

PROMOTIONAL OFFERS
------------------

10. "First 90 Days Free" (limited time)
    Why: Urgency + risk reversal
    Best for: End of quarter push

11. "Implementation Included" (value add)
    Why: Removes adoption friction
    Best for: Enterprise deals

12. "Bring a Peer, Both Get [Benefit]"
    Why: Referral + social proof
    Best for: Customer base expansion

---

Recommended CTA Sequence for [Persona]:
1. Cold: "Get the Benchmark Report"
2. Engaged: "See How [Customer] Did It"
3. Interested: "Get Your Custom ROI Analysis"
4. Ready: "Start Your Free Pilot"

Want me to draft copy for any of these CTAs?
```

### Step 5: Refine and Save

After presenting ideas, offer next steps:

```
What would you like to do next?

1. Develop one of these ideas further
2. Generate more ideas (different angle)
3. Save an idea to your library
4. Create content for an idea (/octave:generate or /octave:pmm)
5. Done for now

Your choice:
```

**If "Save to library":**
- Campaign → Create as playbook with campaign details in notes
- Lead Magnet → Create as collateral or resource reference
- Playbook concept → Use `create_playbook` to generate full playbook

**For Playbook Creation:**

1. **First, get available offerings:**
   ```
   list_all_entities({ entityType: "product" })
   ```

2. **Ask user which product/service this playbook is for:**
   ```
   Which product or service is this playbook for?

   1. [Product A] (px_abc123)
   2. [Product B] (px_def456)

   Your choice:
   ```

3. **Create the playbook:**
   ```
   create_playbook({
     name: "Healthcare Digital Transformation",
     description: "Sales playbook for healthcare digital transformation targeting CTO/VP IT personas",
     instructions: "Create a sales playbook for healthcare digital transformation. Target CTO/VP IT personas in healthcare organizations. Focus on HIPAA compliance, interoperability, and patient outcomes. Use the strategic angle of 'secure, compliant foundation for healthcare innovation'.",
     productOId: "<selected product oId>",
     keyContext: "<relevant context from the brainstorm>"
   })
   ```

## MCP Tools Used

### Read Operations
- `list_all_entities` - Get entities for context
- `get_entity` - Deep dive on specific entities
- `get_playbook` - Understand existing playbook coverage
- `search_knowledge_base` - Find relevant messaging and proof points

### Write Operations
- `create_entity` - Create new entities (except playbooks) from ideas
- `create_playbook` - Create new playbooks with offering association
- `add_value_props` - Add value props to new playbooks

## Brainstorm Modes Summary

| Mode | Output | Key Inputs |
|------|--------|------------|
| Campaigns | 3-5 campaign concepts with hooks, sequences, rationale | Segment, persona, channel |
| Playbook Pack | 3-7 playbook concepts covering TAM gaps | Current coverage, target markets |
| Lead Magnets | 3-5 content offer ideas with mechanics | Persona pain points, buying stage |
| CTAs & Offers | Tiered CTA options + promotional offers | Persona, funnel stage |
| Growth Experiments | Test hypotheses with success metrics | Current playbooks, conversion goals |
| Messaging Angles | Alternative positioning approaches | Product, competitors, personas |

## Error Handling

**Empty Library:**
> Your library needs some content for effective brainstorming.
>
> I can still generate ideas, but they'll be more generic.
> For better results, add at least:
> - 1 product
> - 2-3 personas
> - Key pain points
>
> Run /octave:library create to add content, or continue anyway?

**No Relevant Context:**
> I couldn't find [segment/persona] in your library.
>
> Options:
> 1. Brainstorm anyway (I'll use general knowledge)
> 2. Create [segment/persona] first (/octave:library create)
> 3. Choose a different focus

## Related Skills

- `/octave:generate` - Generate content for brainstormed ideas
- `/octave:pmm` - Develop lead magnets and collateral
- `/octave:library` - Create entities from brainstormed concepts
- `/octave:prospector` - Find prospects for brainstormed campaigns
- `/octave:audit` - Identify gaps to brainstorm around
