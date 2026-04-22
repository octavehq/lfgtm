---
name: abm
description: Account-based planning with stakeholder mapping, persona matching, and coordinated outreach strategy. Use when user says "plan for [company]", "account plan", "stakeholder map", "ABM strategy", or mentions targeting a specific named company.
---

# /octave:abm - Account Planner

Create comprehensive account plans for target accounts by combining deep research, stakeholder mapping, persona matching, and coordinated outreach — all grounded in your library's playbooks and proof points.

## Usage

```
/octave:abm <company> [--stakeholders <N>] [--playbook <name>] [--depth quick|full]
```

## Examples

```
/octave:abm acme.com                                      # Full account plan
/octave:abm acme.com --stakeholders 5                     # Map top 5 stakeholders
/octave:abm acme.com --playbook "Enterprise"              # Use specific playbook
/octave:abm acme.com --depth quick                        # Quick assessment only
/octave:abm "Acme Corp"                                   # Search by company name
```

## Instructions

When the user runs `/octave:abm`:

### Step 1: Identify Target Account

Parse input:
- Domain (e.g., `acme.com`) → Use directly
- Company name → Search for domain
- LinkedIn URL → Extract domain

If company name provided without domain:
```
find_company({ name: "<company_name>" })
```

### Step 2: Deep Account Research

```
# Full company enrichment
enrich_company({ companyDomain: "<domain>" })

# Qualify against ICP
qualify_company({
  companyDomain: "<domain>",
  additionalContext: "Evaluate fit against all segments. Identify which segment, use cases, and playbooks are most relevant."
})
```

### Step 3: Stakeholder Mapping

```
# Find decision makers and influencers
# Use persona titles from library to guide search
list_all_entities({ entityType: "persona" })

# Search for stakeholders matching each persona
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from persona 1>"],
  limit: <stakeholders_param or 3>
})

# Repeat for other relevant personas if needed
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from persona 2>"],
  limit: 3
})
```

For each key stakeholder found:
```
# Enrich top stakeholders
enrich_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>"
  }
})

# Qualify against personas
qualify_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  additionalContext: "Match to our buyer personas. Identify their likely role in a buying decision (champion, evaluator, economic buyer, blocker)."
})
```

### Step 4: Match Playbooks and Gather Intelligence

```
# Find best-fit playbook
search_knowledge_base({
  query: "<company industry> <company size> <identified personas>",
  entityTypes: ["playbook"]
})

# Get playbook with value props
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Find relevant proof points (industry, size match)
search_knowledge_base({
  query: "<company industry> <company size> results case study",
  entityTypes: ["proof_point", "reference"]
})

# Check for competitive context
search_knowledge_base({
  query: "<company name> <any tech stack signals>",
  entityTypes: ["competitor"]
})

# Check for any existing conversation history
list_events({
  startDate: "<365 days ago>",
  filters: {
    companyDomains: ["<domain>"]
  }
})
```

### Step 5: Generate Account Plan

See [account-plan-template.md](references/account-plan-template.md) for the full account plan output template.

### Step 6: Generate Initial Outreach (if requested)

For the recommended entry point stakeholder:
```
generate_email({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",
  allEmailsContext: "Account plan context: [company signals, persona match, value props, proof points]",
  allEmailsInstructions: "Personalized to [company] specifically. Reference [relevant signals]. Use [proof points] progressively."
})
```

## MCP Tools Used

### Research
- `enrich_company` - Deep company intelligence
- `enrich_person` - Stakeholder background
- `qualify_company` - ICP fit scoring
- `qualify_person` - Persona matching
- `find_person` - Stakeholder discovery
- `find_company` - Company lookup by name

### Library Context
- `list_all_entities` (persona) - Get persona definitions for stakeholder matching
- `get_playbook` - Get recommended playbook
- `list_value_props` - Persona-specific value props
- `search_knowledge_base` - Proof points, references, competitive intel
- `list_events` - Existing conversation history with account

### Content Generation
- `generate_email` - Outreach sequences
- `generate_content` - Account-specific content
- `generate_call_prep` - Meeting preparation

## Error Handling

**Company Not Found:**
> Couldn't find "[input]".
>
> Try:
> 1. Provide the company's website domain (e.g., acme.com)
> 2. Check spelling
> 3. Search by name: I'll look it up

**No Stakeholders Found:**
> No contacts found at [Company] matching your personas.
>
> Options:
> 1. Broaden the search (search all titles, not just persona matches)
> 2. Search for specific titles you know
> 3. Proceed with company-level plan only

**Low ICP Score:**
> [Company] scored [X/100] against your ICP.
>
> This is below typical qualification thresholds.
> Continue anyway? Or:
> 1. Find similar companies with better fit
> 2. See why the score is low and if any signals are missing
> 3. Proceed with adjusted expectations

## Related Skills

- `/octave:research` - Deep-dive on a specific stakeholder
- `/octave:campaign` - Generate multi-channel campaign for this account
- `/octave:battlecard` - Competitive intel if competitor detected
- `/octave:pipeline` - Coach on deal progression after engagement starts
- `/octave:prospector` - Find more accounts like this one
