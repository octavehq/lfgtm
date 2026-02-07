---
name: Full Outbound Pipeline
description: Research, qualify, and generate personalized outreach for a target company
author: octave
tags: [outbound, prospecting, email]
inputs:
  - name: company_domain
    type: string
    required: true
    description: Target company domain (e.g., acme.com)
  - name: persona
    type: string
    required: false
    description: Target persona name from library (e.g., "CTO")
    default: auto-detect
  - name: playbook
    type: string
    required: false
    description: Playbook name or oId to use for messaging context
    default: auto-detect
  - name: num_contacts
    type: number
    required: false
    description: Number of contacts to find at the company
    default: 5
---

# Full Outbound Pipeline

Research a target company, qualify it against your ICP, find decision-makers, qualify them against your personas, and generate personalized outreach sequences.

## Steps

### Step 1: Research Company
tool: enrich_company
params:
  companyDomain: "{{company_domain}}"
save_as: company_profile
description: Get detailed intelligence on the target company including firmographics, tech stack, recent news, funding history, and growth signals.

Present the company overview and key signals to the user.

### Step 2: Qualify Company
tool: qualify_company
params:
  companyDomain: "{{company_domain}}"
  additionalContext: "Evaluate fit against our segments and playbooks"
save_as: company_qualification
description: Score the company against ICP criteria from your library segments. Identifies which segments they match and overall fit.

Present the qualification score and fit reasoning.

### Step 3: Review Company Fit
type: decision
condition: "company_qualification.score < 50"
prompt: |
  Company qualification score: {{company_qualification.score}}/100

  Fit summary:
  {{company_qualification.summary}}

  This score is below the recommended threshold of 50.

  Options:
  1. Continue anyway - proceed with outreach despite low score
  2. Stop here - end the workflow
  3. Find similar companies - search for better-fit alternatives

If score >= 50, auto-continue and note the fit level (Excellent 90+, Good 70-89, Moderate 50-69).

### Step 3b: Find Similar Companies (if user chose option 3)
tool: find_similar_companies
params:
  referenceCompany:
    domain: "{{company_domain}}"
  numResults: 5
save_as: similar_companies
description: Find companies similar to the target that may be a better ICP fit.

Present the list and ask the user if they want to restart the workflow with one of these companies, or end here.

### Step 4: Find Decision Makers
tool: find_person
params:
  searchMode: "people"
  companyDomain: "{{company_domain}}"
  fuzzyTitles: "{{persona_titles}}"
  limit: "{{num_contacts}}"
save_as: contacts
description: Find people at the company matching the target persona titles and seniority level.

If a persona was specified (or auto-detected from library), use its common job titles for the search. Otherwise, search for senior decision-makers.

Present the contact list with names, titles, and LinkedIn profiles.

### Step 5: Select Contacts
type: decision
prompt: |
  Found {{contacts.length}} contacts at {{company_profile.name}}:

  {{#each contacts}}
  {{@index + 1}}. {{name}} - {{title}}
     {{linkedInProfile}}
  {{/each}}

  Which contact(s) should I target?
  (Enter a number, multiple numbers separated by commas, or "all")

Save the selected contact(s) for subsequent steps.

### Step 6: Qualify Top Contact
tool: qualify_person
params:
  person:
    linkedInProfile: "{{selected_contact.linkedInProfile}}"
  additionalContext: "Evaluate fit for {{persona}} persona in context of {{playbook}} playbook"
save_as: person_qualification
description: Score the selected contact against persona fit criteria including seniority, responsibilities, and decision-making authority.

If multiple contacts were selected, qualify each one. Present qualification scores.

### Step 7: Generate Email Sequence
tool: generate_email
params:
  person:
    firstName: "{{selected_contact.firstName}}"
    lastName: "{{selected_contact.lastName}}"
    email: "{{selected_contact.email}}"
    linkedInProfile: "{{selected_contact.linkedInProfile}}"
    companyName: "{{company_profile.name}}"
    title: "{{selected_contact.title}}"
  allEmailsContext: "Company intelligence: {{company_profile.summary}}. Company qualification: {{company_qualification.summary}}. Person qualification: {{person_qualification.summary}}"
  numEmails: 4
save_as: email_sequence
description: Generate a personalized email sequence using all gathered intelligence about the company and contact.

If multiple contacts were selected, generate sequences for each one.

### Step 8: Results
type: output
template: |
  OUTBOUND PIPELINE COMPLETE
  ===========================

  Company: {{company_profile.name}} ({{company_domain}})
  ICP Score: {{company_qualification.score}}/100
  Contact: {{selected_contact.name}} ({{selected_contact.title}})
  Persona Fit: {{person_qualification.score}}/100

  ---

  {{email_sequence}}

  ---

  Personalization used:
  - Company: {{company_profile.name}} ({{company_profile.employees}} employees)
  - Matched persona: {{persona}}
  - Playbook: {{playbook}}

  ---

  Next steps:
  1. Copy emails to your outreach tool
  2. Research additional contacts (/octave:research)
  3. Run this workflow for similar companies
  4. Adjust and re-run for a different contact
