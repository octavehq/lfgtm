---
name: Quarterly GTM Review
description: End-of-quarter analysis of wins, losses, field intelligence, ICP accuracy, and competitive landscape
author: octave
tags: [strategy, review, quarterly, analysis]
inputs:
  - name: period_days
    type: number
    required: false
    default: 90
    description: Number of days to analyze (default 90 for quarterly)
---

# Quarterly GTM Review

Comprehensive end-of-quarter analysis covering deal outcomes, field intelligence, ICP accuracy, competitive landscape, and library health.

### Step 1: Win/Loss Analysis

Analyze deal outcomes for the period.

- tool: list_events
- params:
  - startDate: "{{period_start}}"
  - filters:
    - eventTypes: ["DEAL_WON", "DEAL_LOST"]
- save_as: deal_outcomes
- description: Pull all won and lost deals for the quarter

### Step 2: Win Factor Analysis

Understand why we won.

- tool: list_findings
- params:
  - query: "why we won decision factors champion value resonated"
  - startDate: "{{period_start}}"
  - eventFilters:
    - outcomeFilters: ["WON"]
- save_as: win_factors
- description: Extract success factors from won deals

### Step 3: Loss Factor Analysis

Understand why we lost.

- tool: list_findings
- params:
  - query: "why we lost objections competitor chosen budget timing"
  - startDate: "{{period_start}}"
  - eventFilters:
    - outcomeFilters: ["LOST"]
- save_as: loss_factors
- description: Extract failure factors from lost deals

### Step 4: Field Intelligence

Surface trends from all conversations.

- tool: list_findings
- params:
  - query: "objections pain points competitor mentions trends"
  - startDate: "{{period_start}}"
- save_as: field_intel
- description: Identify conversation trends, common objections, and emerging patterns

### Step 5: Positive Signals

Find what's resonating.

- tool: list_findings
- params:
  - query: "positive excited interested value proposition resonated"
  - startDate: "{{period_start}}"
  - eventFilters:
    - sentiments: ["POSITIVE"]
- save_as: positive_signals
- description: Identify messaging and value props that are landing well

### Step 6: Get Current ICP

Pull current library definitions for comparison.

- tool: list_all_entities
- params:
  - entityType: "segment"
- save_as: current_segments
- description: Get current ICP segment definitions to compare against deal data

### Step 7: Get Current Personas

Pull persona definitions.

- tool: list_all_entities
- params:
  - entityType: "persona"
- save_as: current_personas
- description: Get current persona definitions for effectiveness analysis

### Step 8: Competitive Landscape

Check competitive activity.

- tool: list_all_entities
- params:
  - entityType: "competitor"
- save_as: competitors
- description: Get all competitors for landscape analysis

### Step 9: Library Health Check

Assess library coverage and freshness.

- tool: list_all_entities
- params:
  - entityType: "playbook"
- save_as: playbooks
- description: Check playbook coverage and identify gaps

### Step 10: Review and Prioritize

Review findings and decide on priorities.

- type: decision
- description: Based on the quarterly data, which areas need the most attention?
- present: |
    QUARTERLY DATA SUMMARY

    Deals: {{deal_outcomes.won}} won, {{deal_outcomes.lost}} lost
    Win Rate: {{deal_outcomes.win_rate}}
    Top Win Factor: {{win_factors[0]}}
    Top Loss Factor: {{loss_factors[0]}}
    Trending Objection: {{field_intel.top_objection}}
    Best Performing Value Prop: {{positive_signals[0]}}
- options:
  - label: ICP needs refinement (targeting issues)
    value: icp
  - label: Messaging needs update (not resonating)
    value: messaging
  - label: Competitive positioning needs work
    value: competitive
  - label: All areas need attention
    value: all

### Step 11: Quarterly Report

Generate the comprehensive review.

- tool: generate_content
- params:
  - instructions: "Generate a comprehensive quarterly GTM review report. Include: Executive summary, Win/loss analysis with patterns, Field intelligence trends, ICP accuracy assessment, Competitive landscape changes, Messaging effectiveness, Recommended actions for next quarter. Be data-driven — cite specific numbers and patterns."
  - customContext: "Deal outcomes: {{deal_outcomes}}. Win factors: {{win_factors}}. Loss factors: {{loss_factors}}. Field intel: {{field_intel}}. Positive signals: {{positive_signals}}. Current segments: {{current_segments}}. Personas: {{current_personas}}. Competitors: {{competitors}}. Playbooks: {{playbooks}}."
- save_as: quarterly_report
- description: Generate the full quarterly GTM review

### Step 12: Quarterly Review Output

Present the complete quarterly review.

- type: output
- template: |
    QUARTERLY GTM REVIEW
    ====================

    Period: Last {{period_days}} days

    {{quarterly_report}}

    ========================================

    RECOMMENDED NEXT STEPS
    ----------------------
    Based on the priority area: {{chosen_priority}}

    1. Run /octave:icp-refine to update ICP definitions
    2. Run /octave:messaging to refresh messaging frameworks
    3. Run /octave:battlecard landscape for competitive refresh
    4. Run /octave:audit to clean up library health
    5. Run /octave:enablement onboarding to update training materials
    6. Run /octave:brainstorm for next quarter's campaign ideas
