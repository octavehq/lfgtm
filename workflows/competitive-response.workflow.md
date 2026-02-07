---
name: Competitive Response
description: Assess competitive changes, update positioning, generate displacement content, and equip the team
author: octave
tags: [competitive, battlecard, enablement, displacement]
inputs:
  - name: competitor_name
    type: string
    required: true
    description: Name of the competitor to respond to
  - name: trigger
    type: string
    required: false
    description: What triggered this response (e.g., "launched new AI feature", "won a deal we were in")
---

# Competitive Response

React to competitive changes with updated positioning, displacement campaigns, and team enablement.

### Step 1: Get Competitor Intelligence

Pull existing competitive intel from the library.

- tool: search_knowledge_base
- params:
  - query: "{{competitor_name}} competitive positioning differentiation"
  - entityTypes: ["competitor", "playbook", "proof_point"]
  - limit: 15
- save_as: competitor_intel
- description: Gather all existing competitive intelligence

### Step 2: Analyze Recent Competitive Encounters

Check conversation data for recent competitor mentions.

- tool: list_findings
- params:
  - query: "{{competitor_name}} competitive mention objection comparison"
  - startDate: "{{90_days_ago}}"
- save_as: competitive_findings
- description: Surface recent field encounters with this competitor

### Step 3: Review Win/Loss Data

Analyze deal outcomes against this competitor.

- tool: list_events
- params:
  - startDate: "{{180_days_ago}}"
  - filters:
    - eventTypes: ["DEAL_WON", "DEAL_LOST"]
- save_as: deal_outcomes
- description: Pull win/loss data to understand competitive performance

### Step 4: Assess Competitive Position

Review the data and decide on response strategy.

- type: decision
- description: Choose the response strategy based on the competitive landscape
- present: |
    COMPETITIVE ASSESSMENT: {{competitor_name}}

    Recent mentions: {{competitive_findings.count}}
    Deal wins against them: {{deal_outcomes.wins}}
    Deal losses to them: {{deal_outcomes.losses}}

    Trigger: {{trigger}}
- options:
  - label: Full competitive refresh (update everything)
    value: full
  - label: Targeted displacement campaign
    value: displacement
  - label: Enablement update only (equip the team)
    value: enablement
  - label: All of the above
    value: all

### Step 5: Update Competitor Entity

Update the competitor entity with new intel.

- tool: update_entity
- params:
  - entityType: "competitor"
  - oId: "{{competitor_intel.competitor_oId}}"
  - instructions: "Update with latest competitive intelligence. Trigger: {{trigger}}. Recent field data: {{competitive_findings}}. Win/loss patterns: {{deal_outcomes}}. Update strengths, weaknesses, and our differentiation."
- save_as: updated_competitor
- description: Refresh the competitor entity with current data

### Step 6: Generate Displacement Outreach

Create a displacement email sequence for prospects using this competitor.

- tool: generate_email
- params:
  - person:
    - firstName: "{{competitor_intel.target_persona}}"
    - jobTitle: "{{competitor_intel.persona_title}}"
  - numEmails: 4
  - sequenceType: "COLD_OUTBOUND"
  - allEmailsContext: "Target currently uses {{competitor_name}}. Their weaknesses: {{updated_competitor.weaknesses}}. Our advantages: {{updated_competitor.our_differentiation}}. Recent proof of switches: {{competitor_intel.proof_points}}."
  - allEmailsInstructions: "Displacement campaign. Don't name the competitor unless they do first. Lead with pain their current solution likely causes."
- save_as: displacement_sequence
- description: Generate displacement outreach emails

### Step 7: Generate Competitive Enablement

Create a competitive cheat sheet for the sales team.

- tool: generate_content
- params:
  - instructions: "Create a competitive cheat sheet for the sales team about {{competitor_name}}. Include: quick counter for each major claim, trap questions, top 3 proof points, objection responses. Format for quick reference — scannable, not long-form."
  - customContext: "Competitor data: {{updated_competitor}}. Field encounters: {{competitive_findings}}. Win/loss patterns: {{deal_outcomes}}."
- save_as: competitive_cheat_sheet
- description: Create a quick-reference competitive guide for reps

### Step 8: Results

Compile the competitive response package.

- type: output
- template: |
    COMPETITIVE RESPONSE: {{competitor_name}}
    ==========================================

    Trigger: {{trigger}}

    UPDATED POSITIONING
    -------------------
    {{updated_competitor.differentiation_summary}}

    DISPLACEMENT EMAIL SEQUENCE
    ----------------------------
    {{displacement_sequence}}

    COMPETITIVE CHEAT SHEET
    -----------------------
    {{competitive_cheat_sheet}}

    FIELD DATA SUMMARY
    ------------------
    Recent mentions: {{competitive_findings.count}}
    Win rate: {{deal_outcomes.win_rate}}
    Top win reasons: {{deal_outcomes.win_reasons}}
    Top loss reasons: {{deal_outcomes.loss_reasons}}

    NEXT STEPS
    ----------
    1. Share competitive cheat sheet with the team
    2. Run /octave:battlecard for the full battlecard refresh
    3. Use /octave:campaign for a broader competitive campaign
    4. Monitor with /octave:insights --competitor "{{competitor_name}}"
