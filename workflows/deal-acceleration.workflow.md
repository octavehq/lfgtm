---
name: Deal Acceleration
description: Full account intelligence, deal coaching, stakeholder outreach, and meeting prep for high-value deals
author: octave
tags: [deal, pipeline, account, coaching]
inputs:
  - name: company_domain
    type: string
    required: true
    description: Target company domain
  - name: contact_email
    type: string
    required: false
    description: Primary contact email (if known)
  - name: deal_context
    type: string
    required: false
    description: Context about the deal (stage, challenges, history)
---

# Deal Acceleration

Accelerate a high-value deal with account intelligence, stakeholder mapping, deal coaching, and tailored outreach.

### Step 1: Account Research

Deep research on the target account.

- tool: enrich_company
- params:
  - companyDomain: "{{company_domain}}"
- save_as: company_profile
- description: Full company intelligence including financials, tech stack, news, and initiatives

### Step 2: Account Qualification

Score the account against ICP.

- tool: qualify_company
- params:
  - companyDomain: "{{company_domain}}"
  - additionalContext: "Deal context: {{deal_context}}"
- save_as: company_qualification
- description: Evaluate ICP fit and identify relevant segments

### Step 3: Research Primary Contact

Enrich and qualify the primary contact.

- tool: enrich_person
- params:
  - person:
    - email: "{{contact_email}}"
    - companyDomain: "{{company_domain}}"
- save_as: primary_contact
- description: Full background on the primary stakeholder

### Step 4: Map Additional Stakeholders

Find other decision makers and influencers.

- tool: find_person
- params:
  - searchMode: "people"
  - companyDomain: "{{company_domain}}"
  - fuzzyTitles: ["VP", "Director", "Head of", "Chief"]
  - limit: 8
- save_as: stakeholders
- description: Discover additional stakeholders for multi-threading

### Step 5: Check Conversation History

Pull any existing interaction data.

- tool: list_events
- params:
  - startDate: "{{365_days_ago}}"
  - filters:
    - companyDomains: ["{{company_domain}}"]
- save_as: conversation_history
- description: Review all previous interactions with this account

### Step 6: Extract Deal Insights

Get findings from past conversations.

- tool: list_findings
- params:
  - query: "objections pain points next steps champion stakeholders"
  - startDate: "{{365_days_ago}}"
  - eventFilters:
    - companyDomains: ["{{company_domain}}"]
- save_as: deal_insights
- description: Extract objections, pain points, and signals from past interactions

### Step 7: Match Playbook

Find the best playbook for this deal.

- tool: search_knowledge_base
- params:
  - query: "{{company_profile.industry}} {{primary_contact.jobTitle}} {{deal_context}}"
  - entityTypes: ["playbook"]
- save_as: matched_playbook
- description: Identify the most relevant playbook for this deal

### Step 8: Deal Health Review

Assess the deal and decide on strategy.

- type: decision
- description: Review deal health and choose acceleration strategy
- present: |
    DEAL HEALTH ASSESSMENT: {{company_profile.name}}

    ICP Score: {{company_qualification.score}}/100
    Primary Contact: {{primary_contact.name}} ({{primary_contact.title}})
    Stakeholders Found: {{stakeholders.count}}
    Past Interactions: {{conversation_history.count}}
    Key Insights: {{deal_insights.summary}}

    Playbook: {{matched_playbook.name}}
- options:
  - label: Multi-thread (engage more stakeholders)
    value: multi_thread
  - label: Re-engage (deal has stalled)
    value: re_engage
  - label: Competitive push (counter competitor)
    value: competitive
  - label: Executive engagement (elevate the deal)
    value: executive

### Step 9: Generate Stakeholder Outreach

Create tailored outreach for additional stakeholders.

- tool: generate_email
- params:
  - person:
    - firstName: "{{stakeholders[0].firstName}}"
    - lastName: "{{stakeholders[0].lastName}}"
    - companyDomain: "{{company_domain}}"
    - jobTitle: "{{stakeholders[0].title}}"
  - numEmails: 3
  - sequenceType: "WARM_OUTBOUND"
  - allEmailsContext: "Existing deal at {{company_profile.name}}. Already engaged with {{primary_contact.name}}. Key insights from conversations: {{deal_insights}}. Use {{matched_playbook.name}} messaging."
- save_as: stakeholder_outreach
- description: Generate personalized outreach for new stakeholders

### Step 10: Generate Meeting Prep

Prep for the next critical conversation.

- tool: generate_call_prep
- params:
  - person:
    - email: "{{contact_email}}"
    - companyDomain: "{{company_domain}}"
  - meetingContext: "{{deal_context}}. Previous insights: {{deal_insights}}. Strategy: {{chosen_strategy}}."
- save_as: meeting_prep
- description: Full call prep for the next critical meeting

### Step 11: Acceleration Plan

Compile the deal acceleration package.

- type: output
- template: |
    DEAL ACCELERATION PLAN: {{company_profile.name}}
    =================================================

    ACCOUNT OVERVIEW
    ----------------
    Company: {{company_profile.name}} ({{company_domain}})
    ICP Score: {{company_qualification.score}}/100
    Segment: {{company_qualification.segment}}

    BUYING COMMITTEE
    ----------------
    Primary: {{primary_contact.name}} - {{primary_contact.title}}
    Additional Stakeholders:
    {{stakeholders}}

    DEAL INTELLIGENCE
    -----------------
    Past Interactions: {{conversation_history.count}}
    Key Findings: {{deal_insights}}

    STRATEGY: {{chosen_strategy}}

    STAKEHOLDER OUTREACH
    --------------------
    {{stakeholder_outreach}}

    MEETING PREP
    ------------
    {{meeting_prep}}

    NEXT STEPS
    ----------
    1. Send stakeholder outreach this week
    2. Use the meeting prep for your next call
    3. Run /octave:pipeline for ongoing deal coaching
    4. Run /octave:analyzer after each conversation to track progress
    5. Use /octave:battlecard if a competitor surfaces
