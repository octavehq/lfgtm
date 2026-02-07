---
name: Competitive Deal Prep
description: Research, competitive positioning, and tailored displacement outreach
author: octave
tags: [competitive, deal, outreach]
inputs:
  - name: company_domain
    type: string
    required: true
    description: Target company domain (e.g., acme.com)
  - name: contact_email
    type: string
    required: true
    description: Email of the primary contact at the company
  - name: competitor_name
    type: string
    required: true
    description: Name of the competitor in the deal (e.g., "Salesforce")
---

# Competitive Deal Prep

Prepare for a competitive deal by researching the target account, pulling competitive intelligence, and generating positioning-aware outreach. Produces a competitive brief and tailored email sequence.

## Steps

### Step 1: Research Company
tool: enrich_company
params:
  companyDomain: "{{company_domain}}"
save_as: company_profile
description: Get full intelligence on the target company to understand their business, challenges, and tech stack.

Present the company overview, noting any signals related to the competitor (current usage, mentions on their site, job posts, etc.).

### Step 2: Get Competitor Intelligence
tool: search_knowledge_base
params:
  query: "{{competitor_name}} competitor competitive intelligence"
  entityTypes: ["competitor"]
save_as: competitor_intel
description: Pull competitive intelligence from your library for the named competitor. This includes their strengths, weaknesses, differentiators, and reasons you win.

If no competitor entity is found in the library, note this and use general knowledge. Suggest creating one with /octave:library create competitor.

Present the competitive positioning summary.

### Step 3: Get Competitive Positioning
tool: search_knowledge_base
params:
  query: "competitive positioning against {{competitor_name}} reasons we win differentiators"
save_as: positioning
description: Search for relevant proof points, case studies, and messaging that specifically addresses competitive situations with this competitor.

Pull from proof points, references, and playbooks that mention the competitor. Present the most relevant competitive positioning angles.

### Step 4: Research Contact
tool: enrich_person
params:
  person:
    email: "{{contact_email}}"
save_as: contact_profile
description: Get detailed intelligence on the primary contact including their background, role, interests, and communication preferences.

Present the contact profile with focus on what matters in a competitive context (their evaluation criteria, priorities, etc.).

### Step 5: Qualify Contact
tool: qualify_person
params:
  person:
    email: "{{contact_email}}"
  additionalContext: "Evaluating in context of competitive deal against {{competitor_name}}"
save_as: contact_qualification
description: Score the contact against persona fit criteria. Understand their role in the buying process and what they care about.

Present the qualification with competitive context.

### Step 6: Review Competitive Position
type: decision
prompt: |
  Competitive Summary:
  - Competitor: {{competitor_name}}
  - Their Strengths: {{competitor_intel.strengths}}
  - Their Weaknesses: {{competitor_intel.weaknesses}}
  - Our Advantages: {{competitor_intel.reasons_we_win}}

  Contact: {{contact_profile.name}} ({{contact_profile.title}})
  - Persona Fit: {{contact_qualification.score}}/100
  - Likely Priorities: {{contact_profile.priorities}}

  How should we approach this deal?
  1. Lead with differentiation - emphasize where we're stronger
  2. Lead with proof points - show customer wins against this competitor
  3. Lead with value - focus on outcomes, not comparison
  4. Adjust strategy - let me describe a different angle

Save the chosen strategy for email generation.

### Step 7: Generate Competitive Outreach
tool: generate_email
params:
  person:
    firstName: "{{contact_profile.firstName}}"
    lastName: "{{contact_profile.lastName}}"
    email: "{{contact_email}}"
    linkedInProfile: "{{contact_profile.linkedInProfile}}"
    companyName: "{{company_profile.name}}"
    title: "{{contact_profile.title}}"
  allEmailsContext: "Competitive deal against {{competitor_name}}. Strategy: {{chosen_strategy}}. Competitor weaknesses: {{competitor_intel.weaknesses}}. Our advantages: {{competitor_intel.reasons_we_win}}. Proof points: {{positioning.proof_points}}. Company context: {{company_profile.summary}}"
  allEmailsInstructions: "Write a competitive displacement sequence. Do not mention the competitor by name unless the contact brought them up. Focus on our unique value and proof points that specifically counter {{competitor_name}}'s positioning."
  numEmails: 4
save_as: email_sequence
description: Generate a competitive-aware email sequence that positions against the competitor without being directly combative.

### Step 8: Results
type: output
template: |
  COMPETITIVE DEAL PREP COMPLETE
  ================================

  Company: {{company_profile.name}} ({{company_domain}})
  Contact: {{contact_profile.name}} ({{contact_profile.title}})
  Competitor: {{competitor_name}}
  Strategy: {{chosen_strategy}}

  COMPETITIVE BRIEF
  -----------------
  Their Strengths: {{competitor_intel.strengths}}
  Their Weaknesses: {{competitor_intel.weaknesses}}
  Why We Win: {{competitor_intel.reasons_we_win}}
  Key Proof Points: {{positioning.proof_points}}

  ---

  {{email_sequence}}

  ---

  Talk Tracks:
  - If they mention {{competitor_name}}'s strength: {{counter_messaging}}
  - Key differentiator to emphasize: {{top_differentiator}}
  - Proof point to reference: {{strongest_proof_point}}

  ---

  Next steps:
  1. Copy emails to outreach tool
  2. Generate call prep (/octave:generate call-prep)
  3. Create a competitive playbook (/octave:library create playbook)
  4. Research the deal further (/octave:research)
