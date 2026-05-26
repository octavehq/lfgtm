---
name: Persona-Targeted Outreach
description: Find people matching a persona across companies, qualify, and generate outreach
author: octave
tags: [persona, prospecting, outreach]
inputs:
  - name: persona_name
    type: string
    required: true
    description: Target persona name from library (e.g., "CTO", "VP of Engineering")
  - name: industry
    type: string
    required: false
    description: Industry to focus on (e.g., "SaaS", "Healthcare")
    default: any
  - name: min_company_size
    type: number
    required: false
    description: Minimum company employee count
    default: 50
  - name: max_company_size
    type: number
    required: false
    description: Maximum company employee count
    default: 1000
  - name: num_results
    type: number
    required: false
    description: Number of people to find
    default: 10
---

# Persona-Targeted Outreach

Start from a persona definition in your library, find matching people across companies, qualify them, and generate personalized outreach. Ideal for building targeted prospect lists from your ICP.

## Steps

### Step 1: Get Persona Details
tool: get_entity
params:
  oId: "{{persona_oId}}"
save_as: persona
description: Fetch the full persona definition from your library including common job titles, pain points, key objectives, and qualification criteria.

If the user provided a persona name rather than an oId, first use `list_all_entities({ entityType: "persona" })` to find the matching persona and get its oId.

Present the persona overview to confirm this is the right target.

### Step 2: Find Matching Motion ICP
tool: list_motions
save_as: motions
description: List Motions in the workspace.

tool: list_motion_icps
params:
  motionOId: "{{motions[0].oId}}"
save_as: motion_icps
description: List Motion ICP cells (persona × segment intersections) under the relevant Motion.

tool: find_motion_icp
params:
  motionIcpOId: "{{motion_icp_for_persona.oId}}"
  includeLearnings: true
save_as: matched_motion_icp
description: Identify the Motion ICP cell whose persona aligns with {{persona.name}} and fetch its narrative (Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) + Learning Loop learnings.

Present the matched Motion ICP cell. If no matching cell is found, note that outreach will use persona-level messaging only and recommend adding the missing persona × segment cell to the Motion.

### Step 3: Find Matching People
tool: find_person
params:
  searchMode: "people"
  fuzzyTitles: "{{persona.commonJobTitles}}"
  industry: "{{industry}}"
  employeeCount:
    min: "{{min_company_size}}"
    max: "{{max_company_size}}"
  limit: "{{num_results}}"
save_as: prospects
description: Search for people whose titles match the persona's common job titles, filtered by industry and company size criteria.

Present the prospect list with names, titles, companies, and LinkedIn profiles.

### Step 4: Select Prospects
type: decision
prompt: |
  Found {{prospects.length}} people matching "{{persona.name}}":

  {{#each prospects}}
  {{@index + 1}}. {{name}} - {{title}}
     Company: {{companyName}} ({{companyDomain}})
     {{linkedInProfile}}
  {{/each}}

  Which prospects should I qualify and generate outreach for?
  (Enter numbers separated by commas, or "all")

Save the selected prospects for subsequent steps.

### Step 5: Enrich Selected Prospects
tool: enrich_person
params:
  person:
    linkedInProfile: "{{prospect.linkedInProfile}}"
save_as: enriched_prospects
description: Get detailed intelligence on each selected prospect including background, interests, recent activity, and company context.

Run this for each selected prospect. Present a brief summary of each.

### Step 6: Qualify Selected Prospects
tool: qualify_person
params:
  person:
    linkedInProfile: "{{prospect.linkedInProfile}}"
  additionalContext: "Evaluate fit for {{persona.name}} persona. Key criteria: {{persona.qualificationCriteria}}"
save_as: prospect_qualifications
description: Score each selected prospect against the persona's qualification criteria.

Run this for each enriched prospect. Present qualification scores ranked from highest to lowest.

### Step 7: Review Qualified Prospects
type: decision
prompt: |
  Qualified Prospects (ranked by fit):

  {{#each prospect_qualifications sorted by score desc}}
  {{@index + 1}}. {{name}} - {{title}} at {{companyName}}
     Persona Fit: {{score}}/100
     Key Match: {{matchReason}}
  {{/each}}

  Generate outreach for:
  1. Top prospect only
  2. Top 3 prospects
  3. All qualified prospects (score > 50)
  4. Specific prospects (enter numbers)

Save the final selection.

### Step 8: Generate Outreach
tool: generate_email
params:
  person:
    firstName: "{{prospect.firstName}}"
    lastName: "{{prospect.lastName}}"
    email: "{{prospect.email}}"
    linkedInProfile: "{{prospect.linkedInProfile}}"
    companyName: "{{prospect.companyName}}"
    title: "{{prospect.title}}"
  allEmailsContext: "Targeting {{persona.name}} persona. Pain points: {{persona.painPoints}}. Motion ICP narrative (strategic narrative + benefits + methodology): {{matched_motion_icp}}. Person background: {{prospect.enrichment.summary}}"
  numEmails: 4
save_as: email_sequences
description: Generate personalized email sequences for each selected prospect, using persona messaging and individual enrichment data.

Run this for each prospect selected in Step 7.

### Step 9: Results
type: output
template: |
  PERSONA-TARGETED OUTREACH COMPLETE
  ====================================

  Persona: {{persona.name}}
  Motion ICP: {{matched_motion_icp.name}}
  Prospects Targeted: {{selected_prospects.length}}

  ---

  {{#each selected_prospects}}
  PROSPECT: {{name}} ({{title}} at {{companyName}})
  Persona Fit: {{qualification.score}}/100
  ─────────────────────────────────────────

  {{email_sequence}}

  ---
  {{/each}}

  FILTER RECOMMENDATIONS
  ----------------------
  To find more {{persona.name}} prospects at scale:

  Titles: {{persona.commonJobTitles}}
  Industries: {{industry}}
  Company Size: {{min_company_size}}-{{max_company_size}} employees
  Keywords: {{persona.keywords}}

  ---

  Next steps:
  1. Copy emails to outreach tool
  2. Find more prospects with broader criteria
  3. Run for a different persona
  4. Create a prospect list in Apollo/Clay/LinkedIn
