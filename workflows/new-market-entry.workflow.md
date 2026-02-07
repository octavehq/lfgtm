---
name: New Market Entry
description: Research, define ICP, build personas and playbooks, create messaging, and launch outreach for a new market
author: octave
tags: [strategy, expansion, market, messaging]
inputs:
  - name: market_description
    type: string
    required: true
    description: Description of the new market (e.g., "Healthcare SaaS companies, 100-500 employees")
  - name: product_oId
    type: string
    required: false
    description: Product oId to position for this market (auto-detects if not provided)
---

# New Market Entry

End-to-end workflow for entering a new market segment — from research through messaging to first outreach.

### Step 1: Research the Market

Research the target market to understand the landscape.

- tool: search_knowledge_base
- params:
  - query: "{{market_description}}"
  - entityTypes: ["segment", "persona", "competitor"]
  - limit: 10
- save_as: existing_coverage
- description: Check what library coverage already exists for this market

### Step 2: Find Representative Companies

Identify companies in the target market for analysis.

- tool: find_company
- params:
  - keywords: ["{{market_description}}"]
  - limit: 10
- save_as: market_companies
- description: Find companies that match the new market profile

### Step 3: Enrich Top Companies

Deep research on 3 representative companies to understand the market.

- tool: enrich_company
- params:
  - companyDomain: "{{market_companies[0].domain}}"
- save_as: company_profiles
- description: Enrich top companies to understand industry patterns, pain points, and buying behaviors

### Step 4: Create Market Segment

Create a new segment entity based on research.

- tool: create_entity
- params:
  - entityType: "segment"
  - name: "{{market_description}} Segment"
  - instructions: "Create a segment for {{market_description}}. Use the company research to define firmographic criteria (industry, size, stage, geography), common characteristics, technology stack patterns, and buying behaviors. Base this on the enriched company data."
  - keyContext: "{{company_profiles}}"
- save_as: new_segment
- description: Define the ICP segment from research findings

### Step 5: Create Buyer Persona

Create the primary buyer persona for this market.

- tool: create_entity
- params:
  - entityType: "persona"
  - name: "{{market_description}} Buyer"
  - instructions: "Create a buyer persona for the primary decision maker in {{market_description}} companies. Include their typical title, responsibilities, pain points, goals, evaluation criteria, and objections. Ground in the market research."
  - keyContext: "{{company_profiles}}"
- save_as: new_persona
- description: Define the primary buyer persona for this market

### Step 6: Review New Entities

Review the segment and persona before proceeding.

- type: decision
- description: Review the new segment and persona definitions
- present: |
    New segment and persona created:

    SEGMENT: {{new_segment.name}}
    PERSONA: {{new_persona.name}}

    Review these entities in your library before continuing.
- options:
  - label: Continue to messaging
    value: continue
  - label: Refine entities first
    value: refine
  - label: Stop here
    value: stop

### Step 7: Build Messaging Framework

Generate a messaging framework for the new market.

- tool: generate_content
- params:
  - instructions: "Build a messaging framework for selling to {{market_description}}. Include: positioning statement, 3 messaging pillars with proof points, key messages by persona, competitive differentiation. Ground in the persona pain points and market context."
  - customContext: "Segment: {{new_segment}}. Persona: {{new_persona}}. Market companies: {{company_profiles}}"
- save_as: messaging_framework
- description: Create the messaging foundation for this market

### Step 8: Create Playbook

Generate a playbook for the new market.

- tool: create_playbook
- params:
  - name: "{{market_description}} Playbook"
  - description: "Playbook for selling into {{market_description}}"
  - instructions: "Create a sales playbook for {{market_description}}. Use the messaging framework, persona, and segment data to build comprehensive guidance including discovery questions, value propositions, objection handling, and competitive positioning."
  - personaOIds: ["{{new_persona.oId}}"]
  - segmentOId: "{{new_segment.oId}}"
- save_as: new_playbook
- description: Build the sales playbook for this market

### Step 9: Find Initial Prospects

Find initial prospects to target in the new market.

- tool: find_person
- params:
  - searchMode: "people"
  - fuzzyTitles: ["{{new_persona.commonTitles}}"]
  - keywords: ["{{market_description}}"]
  - limit: 10
- save_as: initial_prospects
- description: Identify initial prospects matching the new persona

### Step 10: Generate Campaign Brief

Create an initial outreach campaign brief.

- type: output
- template: |
    NEW MARKET ENTRY: {{market_description}}
    ==========================================

    CREATED ENTITIES
    ----------------
    ✓ Segment: {{new_segment.name}}
    ✓ Persona: {{new_persona.name}}
    ✓ Playbook: {{new_playbook.name}}

    MESSAGING FRAMEWORK
    -------------------
    {{messaging_framework}}

    INITIAL PROSPECTS
    -----------------
    {{initial_prospects}}

    NEXT STEPS
    ----------
    1. Review and refine the segment, persona, and playbook in your library
    2. Run /octave:campaign to generate multi-channel content
    3. Run /octave:enablement to create team training materials
    4. Run /octave:abm on top prospect companies for account plans
    5. Use /octave:generate to create personalized outreach for each prospect
