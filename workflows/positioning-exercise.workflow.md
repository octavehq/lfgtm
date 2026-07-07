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

## Steps

### Step 1: Audit Library Completeness

Check that all required entity types exist before generating frameworks.

tool: list_all_entities
params:
  entityType: "product"
save_as: products
description: Verify products exist — the positioning system needs at least one product. If multiple products exist and no product_name input was given, ask the user which one to position; save the chosen product's oId as selected_product_oId.

tool: list_all_entities
params:
  entityType: "persona"
save_as: personas
description: Check personas — needed for Message Framework, Persona Messaging, Homepage Messaging.

tool: list_all_entities
params:
  entityType: "use_case"
save_as: use_cases
description: Check use cases — needed for Use Case Canvas and Lifecycle.

tool: list_all_entities
params:
  entityType: "competitor"
save_as: competitors
description: Check competitors — enriches Positioning Strategy and Use Case Canvas.

tool: list_motions
save_as: motions
description: Check Motions — the Default Motion Playbook covers persona × segment as Motion ICP cells, and any Custom Motion Playbooks layer thematic/account/competitive narratives on top. Motion ICPs are the source of positioning narrative for the Message Framework and Anchors. Identify the Motion for the selected product and save its oId as primary_motion_oId.

### Step 2: Review Library Gaps

type: decision
condition: "products.length === 0"
prompt: |
  LIBRARY AUDIT RESULTS
  =====================

  Products:   {{products.length}} {{products.length === 0 ? '⚠ REQUIRED — cannot proceed without a product' : '✓'}}
  Personas:   {{personas.length}} {{personas.length === 0 ? '⚠ Sections 1,4,8 will be limited' : '✓'}}
  Use Cases:  {{use_cases.length}} {{use_cases.length === 0 ? '⚠ Sections 6,7 will be skipped' : '✓'}}
  Competitors: {{competitors.length}} {{competitors.length === 0 ? '— Sections 3,6 won't have competitive context' : '✓'}}
  Motions:    {{motions.length}} {{motions.length === 0 ? '⚠ Positioning narrative will be limited (no Motion ICP cells to anchor messaging)' : '✓'}}

  Options:
  1. Proceed with what we have (skip sections with insufficient data)
  2. Fill gaps first — I'll help create missing entities
  3. Stop and populate the library manually first
save_as: gap_decision

### Step 3: Gather Full Intelligence

Deep data pull for the selected product. All data gathered here feeds into all 8 frameworks.

tool: get_entity
params:
  oId: "{{selected_product_oId}}"
save_as: product_detail
description: Full product details — category, capabilities, features, positioning.

tool: list_entities
params:
  entityType: "persona"
save_as: persona_details
description: Full persona data — roles, pain points, priorities, workflows.

tool: list_entities
params:
  entityType: "segment"
save_as: segment_details
description: Full segment data — firmographics, criteria, sizing.

tool: list_entities
params:
  entityType: "use_case"
save_as: use_case_details
description: Full use case data — descriptions, workflows, outcomes.

tool: list_motion_icps
params:
  motionOId: "{{primary_motion_oId}}"
save_as: motion_icps
description: List Motion ICP cells (persona × segment intersections) under the primary Motion. Pick the cell that best represents the core persona × segment for this product and save its oId as primary_motion_icp_oId.

tool: find_motion_icp
params:
  motionIcpOId: "{{primary_motion_icp_oId}}"
  includeLearnings: true
save_as: primary_motion_icp_narrative
description: Primary Motion ICP narrative — Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, plus Learning Loop learnings. Feeds Message Framework and Anchors.

tool: list_motion_playbooks
params:
  motionOId: "{{primary_motion_oId}}"
save_as: motion_playbooks
description: List Motion Playbooks (Default + any Custom). Fetch each Custom Motion Playbook via `get_motion_playbook` for thematic/account/competitive narrative content that overlays the persona × segment matrix. Note the Default Motion Playbook's oId as primary_motion_playbook_oId (used when saving back in Step 6).

tool: list_entities
params:
  entityType: "proof_point"
save_as: proof_points
description: Proof points for evidence in Strategy table and Anchors.

tool: list_findings
params:
  query: "value propositions positive reactions"
  startDate: "{{90_days_ago}}"
  eventFilters:
    sentiments: ["POSITIVE"]
save_as: positive_findings
description: What resonates in real conversations — grounds Anchors and Awareness Funnel.

tool: list_all_entities
params:
  entityType: "brand_voice"
save_as: brand_voices
description: Brand voice for Homepage Messaging tone consistency.

### Step 4: Generate Positioning System

Run the positioning skill to generate the complete 8-framework HTML document.

type: skill
skill: /octave:positioning
inputs:
  product: "{{product_detail.name}}"
  style: "{{style || 'midnight-pro'}}"
  context: "All data gathered in Steps 1-3"
save_as: positioning_html
description: Generate the full positioning system as a visual HTML document. Save the output file path in positioning_html.

### Step 5: Review and Approve

type: decision
prompt: |
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
save_as: review_decision

### Step 6: Save Back to Library

Save key positioning outputs back to the Octave library for reuse across other skills. Derive the values below (primary anchor, product category, key differentiator, per-persona value prop summary) from the generated positioning document.

tool: update_entity
params:
  entityType: "product"
  oId: "{{selected_product_oId}}"
  instructions: "Update positioning to reflect the positioning system: Primary anchor: [primary anchor from positioning_html]. Category: [product category from positioning_html]. Key differentiator: [key differentiator from positioning_html]."
save_as: updated_product
description: Save positioning statements to the product entity.

tool: update_motion_playbook
params:
  motionPlaybookOId: "{{primary_motion_playbook_oId}}"
  instructions: "Update the Motion Playbook narrative sections (Strategic narrative, Benefits and impacts, Methodology) for each Motion ICP cell to reflect the positioning exercise outputs: [per-persona value prop summary from positioning_html]. Keep the persona × segment matrix intact — edit narrative content per ICP cell, not the cell structure itself."
save_as: updated_motion_playbook
description: Save positioning back to the primary Motion Playbook by editing narrative sections across its Motion ICP cells.

### Step 7: Results

type: output
template: |
  POSITIONING EXERCISE COMPLETE
  ==============================

  Product: {{product_detail.name}}
  Document: {{positioning_html.path}}

  Frameworks Generated:
  1. Message Framework — value props across {{personas.length}} personas
  2. Positioning Anchors — positioning statements
  3. Positioning Strategy — {{competitors.length}} competitive alternatives analyzed
  4. Persona Messaging — buying committee roles mapped
  5. Awareness Funnel — 4 awareness stages with messaging guidance
  6. Use Case Canvas — {{use_cases.length}} use cases: Current Way vs New Way
  7. Use Case Lifecycle — {{use_cases.length}} customer journeys mapped
  8. Homepage Messaging — Primary + secondary messaging templates

  Library Updates:
  - Product positioning: {{updated_product ? 'Updated ✓' : 'Skipped'}}
  - Motion Playbook narrative sections: {{updated_motion_playbook ? 'Updated ✓' : 'Skipped'}}

  ---

  Next steps:
  - /octave:deck — Turn this positioning into a presentation
  - /octave:campaign — Generate campaign content grounded in this positioning
  - /octave:launch — Build a launch plan using this messaging foundation
  - /octave:enablement — Create sales enablement materials from this positioning
