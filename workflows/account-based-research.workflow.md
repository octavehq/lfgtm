---
name: Account-Based Research
description: Deep research dossier on a target account with contact mapping and playbook matching
author: octave
tags: [research, abm, account]
inputs:
  - name: company_domain
    type: string
    required: true
    description: Target company domain (e.g., acme.com)
  - name: num_contacts
    type: number
    required: false
    description: Number of key contacts to research
    default: 3
---

# Account-Based Research

Build a comprehensive research dossier on a target account. Includes company intelligence, ICP scoring, key contact mapping with enrichment, and matched playbook recommendations. Produces a full account brief without generating outreach.

## Steps

### Step 1: Research Company
tool: enrich_company
params:
  companyDomain: "{{company_domain}}"
save_as: company_profile
description: Get full company intelligence including firmographics, tech stack, recent news, funding history, growth signals, and competitive landscape.

Present a detailed company overview.

### Step 2: Qualify Company
tool: qualify_company
params:
  companyDomain: "{{company_domain}}"
  additionalContext: "Provide detailed segment matching and fit reasoning"
save_as: company_qualification
description: Score the company against all ICP criteria from your library. Identify which segments they match and why.

Present the full qualification breakdown.

### Step 3: Find Key Contacts
tool: find_person
params:
  searchMode: "people"
  companyDomain: "{{company_domain}}"
  limit: "{{num_contacts}}"
save_as: contacts
description: Find key decision-makers and influencers at the company. Search broadly across senior titles to map the buying committee.

Present the list of contacts found.

### Step 4: Enrich Top Contacts
tool: enrich_person
params:
  person:
    linkedInProfile: "{{contact.linkedInProfile}}"
save_as: enriched_contacts
description: Get detailed intelligence on each contact including background, interests, recent activity, and communication preferences.

Run this for each contact found in Step 3 (up to num_contacts). Present enrichment results for each person.

### Step 5: Qualify Contacts
tool: qualify_person
params:
  person:
    linkedInProfile: "{{contact.linkedInProfile}}"
  additionalContext: "Identify which persona from our library this person best matches"
save_as: contact_qualifications
description: Score each contact against persona fit criteria. Identify which library persona they map to and their role in the buying process.

Run this for each enriched contact. Present qualification scores and persona mappings.

### Step 6: Match Playbooks
tool: search_knowledge_base
params:
  query: "playbook for {{company_profile.industry}} {{company_profile.description}} targeting {{matched_personas}}"
save_as: matched_playbooks
description: Search the library for playbooks that best match this account based on their industry, use cases, and the personas identified.

Present the top matching playbooks with reasoning.

### Step 7: Account Brief
type: output
template: |
  ACCOUNT RESEARCH BRIEF
  =======================
  Company: {{company_profile.name}}
  Domain: {{company_domain}}
  Generated: {{current_date}}

  COMPANY OVERVIEW
  ----------------
  Industry: {{company_profile.industry}}
  Employees: {{company_profile.employees}}
  Revenue: {{company_profile.revenue}}
  Stage: {{company_profile.stage}}
  Location: {{company_profile.location}}

  {{company_profile.description}}

  ICP FIT
  -------
  Score: {{company_qualification.score}}/100
  Matched Segments: {{company_qualification.segments}}
  Fit Summary: {{company_qualification.summary}}

  KEY SIGNALS
  -----------
  {{company_profile.signals}}

  BUYING COMMITTEE
  ----------------
  {{#each enriched_contacts}}
  {{@index + 1}}. {{name}} - {{title}}
     Persona Match: {{qualification.persona}} ({{qualification.score}}/100)
     Background: {{background}}
     Key Interests: {{interests}}
     Buying Role: {{qualification.buyingRole}}
  {{/each}}

  RECOMMENDED PLAYBOOKS
  ---------------------
  {{#each matched_playbooks}}
  - {{name}}: {{description}}
    Approach: {{approachAngle}}
  {{/each}}

  RECOMMENDED NEXT STEPS
  ----------------------
  1. Use a matched playbook to generate outreach
  2. Run /octave:workflow run "Full Outbound Pipeline" --company {{company_domain}}
  3. Generate call prep for an upcoming meeting
  4. Research similar companies for account expansion
