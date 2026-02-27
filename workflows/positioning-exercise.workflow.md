---
name: Positioning Exercise
description: Full messaging & positioning exercise — gather library data, validate completeness, generate the 8-framework visual positioning system, and save key outputs back to the library
author: octave
tags: [positioning, messaging, strategy, pmm, frameworks]
inputs:
  - name: product_name
    type: string
    required: false
    description: Product to build positioning for (auto-detects if only one product exists)
  - name: style
    type: string
    required: false
    description: Style preset for the HTML output (default "midnight-pro")
---

# Positioning Exercise

End-to-end workflow for building a complete Messaging & Positioning system — from library audit through framework generation to saving key outputs back.

### Step 1: Audit Library Completeness

Check that all required entity types exist before generating frameworks.

- tool: list_all_entities
- params:
  - entityType: "product"
- save_as: products
- description: Verify products exist — the positioning system needs at least one product

- tool: list_all_entities
- params:
  - entityType: "persona"
- save_as: personas
- description: Check personas — needed for Message Framework, Persona Messaging, Homepage Messaging

- tool: list_all_entities
- params:
  - entityType: "use_case"
- save_as: use_cases
- description: Check use cases — needed for Use Case Canvas and Lifecycle

- tool: list_all_entities
- params:
  - entityType: "competitor"
- save_as: competitors
- description: Check competitors — enriches Positioning Strategy and Use Case Canvas

- tool: list_all_entities
- params:
  - entityType: "playbook"
- save_as: playbooks
- description: Check playbooks — source of value propositions for Message Framework and Anchors

### Step 2: Review Library Gaps

- type: decision
- condition: "products.length === 0"
- prompt: |
  LIBRARY AUDIT RESULTS
  =====================

  Products:   {{products.length}} {{products.length === 0 ? '⚠ REQUIRED — cannot proceed without a product' : '✓'}}
  Personas:   {{personas.length}} {{personas.length === 0 ? '⚠ Sections 1,4,8 will be limited' : '✓'}}
  Use Cases:  {{use_cases.length}} {{use_cases.length === 0 ? '⚠ Sections 6,7 will be skipped' : '✓'}}
  Competitors: {{competitors.length}} {{competitors.length === 0 ? '— Sections 3,6 won't have competitive context' : '✓'}}
  Playbooks:  {{playbooks.length}} {{playbooks.length === 0 ? '⚠ Value props will be limited' : '✓'}}

  Options:
  1. Proceed with what we have (skip sections with insufficient data)
  2. Fill gaps first — I'll help create missing entities
  3. Stop and populate the library manually first

### Step 3: Gather Full Intelligence

Deep data pull for the selected product. All data gathered here feeds into all 8 frameworks.

- tool: get_entity
- params:
  - oId: "{{selected_product_oId}}"
- save_as: product_detail
- description: Full product details — category, capabilities, features, positioning

- tool: list_entities
- params:
  - entityType: "persona"
- save_as: persona_details
- description: Full persona data — roles, pain points, priorities, workflows

- tool: list_entities
- params:
  - entityType: "segment"
- save_as: segment_details
- description: Full segment data — firmographics, criteria, sizing

- tool: list_entities
- params:
  - entityType: "use_case"
- save_as: use_case_details
- description: Full use case data — descriptions, workflows, outcomes

- tool: get_playbook
- params:
  - oId: "{{primary_playbook_oId}}"
  - includeValueProps: true
- save_as: playbook_with_vps
- description: Primary playbook with all value propositions — feeds Message Framework and Anchors

- tool: list_entities
- params:
  - entityType: "proof_point"
- save_as: proof_points
- description: Proof points for evidence in Strategy table and Anchors

- tool: list_findings
- params:
  - query: "value propositions positive reactions"
  - startDate: "{{90_days_ago}}"
  - eventFilters:
    - sentiments: ["POSITIVE"]
- save_as: positive_findings
- description: What resonates in real conversations — grounds Anchors and Awareness Funnel

- tool: list_brand_voices
- save_as: brand_voices
- description: Brand voice for Homepage Messaging tone consistency

### Step 4: Generate Positioning System

Run the positioning skill to generate the complete 8-framework HTML document.

- tool: /octave:positioning
- params:
  - product: "{{product_detail.name}}"
  - style: "{{style || 'midnight-pro'}}"
  - context: "{{all gathered data}}"
- save_as: positioning_html
- description: Generate the full positioning system as a visual HTML document

### Step 5: Review and Approve

- type: decision
- prompt: |
  POSITIONING SYSTEM GENERATED
  =============================

  File: {{positioning_html.path}}

  Review the document in your browser. All 8 frameworks are populated
  from your library data.

  Options:
  1. Looks great — save key outputs to library
  2. Adjust specific sections
  3. Regenerate with different style
  4. Done — no library updates needed

### Step 6: Save Back to Library

Save key positioning outputs back to the Octave library for reuse across other skills.

- tool: update_entity
- params:
  - entityType: "product"
  - oId: "{{selected_product_oId}}"
  - instructions: "Update positioning to reflect the positioning system: Primary anchor: {{primary_anchor}}. Category: {{product_category}}. Key differentiator: {{key_differentiator}}."
- save_as: updated_product
- description: Save positioning statements to the product entity

- tool: add_value_props
- params:
  - playbookOId: "{{primary_playbook_oId}}"
  - instructions: "Add or update value propositions from the positioning exercise: {{persona_value_props_summary}}"
  - numValuesPerPersona: 3
- save_as: updated_vps
- description: Save persona-specific value propositions to the playbook

### Step 7: Results

- type: output
- template: |
  POSITIONING EXERCISE COMPLETE
  ==============================

  Product: {{product_detail.name}}
  Document: {{positioning_html.path}}

  Frameworks Generated:
  1. Message Framework — {{value_prop_count}} value props across {{persona_count}} personas
  2. Positioning Anchors — {{anchor_count}} positioning statements
  3. Positioning Strategy — {{competitive_alt_count}} competitive alternatives analyzed
  4. Persona Messaging — {{persona_count}} buying committee roles mapped
  5. Awareness Funnel — 4 awareness stages with messaging guidance
  6. Use Case Canvas — {{use_case_count}} use cases: Current Way vs New Way
  7. Use Case Lifecycle — {{use_case_count}} customer journeys mapped
  8. Homepage Messaging — Primary + secondary messaging templates

  Library Updates:
  - Product positioning: {{updated_product ? 'Updated ✓' : 'Skipped'}}
  - Playbook value props: {{updated_vps ? 'Updated ✓' : 'Skipped'}}

  ---

  Next steps:
  - /octave:deck — Turn this positioning into a presentation
  - /octave:campaign — Generate campaign content grounded in this positioning
  - /octave:launch — Build a launch plan using this messaging foundation
  - /octave:enablement — Create sales enablement materials from this positioning
