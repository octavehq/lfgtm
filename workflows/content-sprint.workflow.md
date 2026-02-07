---
name: Content Sprint
description: Generate a batch of multi-format content assets around a theme — messaging, emails, social, blog, landing page, and enablement
author: octave
tags: [content, campaign, marketing, multi-channel]
inputs:
  - name: theme
    type: string
    required: true
    description: The content theme or topic (e.g., "AI-powered analytics", "cost reduction for CFOs")
  - name: persona_name
    type: string
    required: false
    description: Target persona (auto-detects if not provided)
  - name: channels
    type: string
    required: false
    default: "email,linkedin,blog,social"
    description: Comma-separated channels to generate content for
---

# Content Sprint

Rapid content generation across multiple formats and channels around a single theme — all grounded in consistent messaging from your library.

### Step 1: Establish Messaging Foundation

Build the messaging angle for this content sprint.

- tool: search_knowledge_base
- params:
  - query: "{{theme}}"
  - entityTypes: ["playbook", "persona", "use_case", "proof_point"]
  - limit: 15
- save_as: theme_context
- description: Find all relevant library context for the theme

### Step 2: Get Brand Voice

Ensure content consistency.

- tool: list_brand_voices
- params: {}
- save_as: brand_voices
- description: Get brand voice guidelines for content generation

### Step 3: Generate Core Messaging

Create the messaging backbone for the sprint.

- tool: generate_content
- params:
  - instructions: "Create a brief messaging framework for the theme '{{theme}}'. Include: Core message (1 sentence), 3 supporting points, key proof point, primary CTA. This will be the backbone for all content in this sprint. Target: {{persona_name}}."
  - customContext: "Library context: {{theme_context}}. Brand voice: {{brand_voices}}."
- save_as: core_messaging
- description: Establish consistent messaging for all content pieces

### Step 4: Generate Email Sequence

Create an email campaign.

- tool: generate_email
- params:
  - person:
    - firstName: "{{persona_name}}"
    - jobTitle: "{{theme_context.persona_title}}"
  - numEmails: 4
  - sequenceType: "COLD_OUTBOUND"
  - allEmailsContext: "Theme: {{theme}}. Core messaging: {{core_messaging}}. Proof points: {{theme_context.proof_points}}."
  - allEmailsInstructions: "Each email should explore a different facet of the theme. Progressive structure building on the core messaging."
- save_as: email_sequence
- description: Generate a 4-email sequence around the theme

### Step 5: Generate LinkedIn Content

Create LinkedIn outreach and posts.

- tool: generate_content
- params:
  - instructions: "For the theme '{{theme}}', generate: 1) LinkedIn connection request (300 chars), 2) LinkedIn follow-up DM, 3) LinkedIn post (thought leadership angle, 150-200 words), 4) 3 LinkedIn comment templates for engaging with posts about this topic. All aligned with core messaging."
  - customContext: "Core messaging: {{core_messaging}}. Brand voice: {{brand_voices}}."
- save_as: linkedin_content
- description: Generate LinkedIn outreach and thought leadership content

### Step 6: Generate Blog Post

Create a long-form content piece.

- tool: generate_content
- params:
  - instructions: "Write a blog post on the theme '{{theme}}'. Target reader: {{persona_name}}. Structure: Hook (why this matters now), The problem (2-3 paragraphs), Our perspective (2-3 paragraphs), How to approach it (actionable framework), Results/proof (case study or data), CTA. Length: 1200-1500 words. Tone: {{brand_voices.primary}}."
  - customContext: "Core messaging: {{core_messaging}}. Proof points: {{theme_context.proof_points}}. Use cases: {{theme_context.use_cases}}."
- save_as: blog_post
- description: Generate a blog post that serves as the content hub

### Step 7: Generate Social Posts

Create social media content.

- tool: generate_content
- params:
  - instructions: "Create 5 social media posts for '{{theme}}': 1) Key stat/insight, 2) Provocative question, 3) Mini case study, 4) Quick tip/framework, 5) Blog post promo (linking to the blog we created). Include hashtag suggestions. Platform: LinkedIn primary."
  - customContext: "Core messaging: {{core_messaging}}. Proof points: {{theme_context.proof_points}}."
- save_as: social_posts
- description: Generate social media posts to amplify the content

### Step 8: Review Sprint Output

Review all generated content.

- type: decision
- description: Review the content sprint output
- present: |
    CONTENT SPRINT COMPLETE: {{theme}}

    Generated:
    ✓ Core messaging framework
    ✓ 4-email sequence
    ✓ LinkedIn content (DMs + post + comments)
    ✓ Blog post (~1,300 words)
    ✓ 5 social media posts
- options:
  - label: Looks good — generate enablement piece too
    value: add_enablement
  - label: Revise a specific piece
    value: revise
  - label: Done — export everything
    value: done

### Step 9: Sprint Summary

Present the full content package.

- type: output
- template: |
    CONTENT SPRINT: {{theme}}
    ==========================

    TARGET: {{persona_name}}

    CORE MESSAGING
    --------------
    {{core_messaging}}

    EMAIL SEQUENCE
    --------------
    {{email_sequence}}

    LINKEDIN CONTENT
    ----------------
    {{linkedin_content}}

    BLOG POST
    ---------
    {{blog_post}}

    SOCIAL POSTS
    ------------
    {{social_posts}}

    ========================================

    CONTENT CALENDAR SUGGESTION
    ---------------------------
    Week 1: Publish blog post, social post #1, start email sequence
    Week 1: LinkedIn connection requests to target list
    Week 2: Social posts #2-3, LinkedIn post, email #2
    Week 3: Social posts #4-5, email #3, LinkedIn follow-ups
    Week 4: Email #4, LinkedIn engagement comments

    NEXT STEPS
    ----------
    1. Run /octave:repurpose to adapt for additional personas
    2. Run /octave:campaign --channels ads,landing-page for paid content
    3. Run /octave:pmm to create a supporting one-pager or case study
