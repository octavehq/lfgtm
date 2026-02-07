---
name: prospector
description: Find, enrich, and qualify prospects against your library's ICP criteria
---

# /octave:prospector - ICP-Fit Prospecting

Find companies and people that match your Ideal Customer Profile. Uses your library's segments, personas, and playbooks to search for and score prospects. Returns qualified prospect lists with fit reasoning, recommended approaches, and filter suggestions for scaling in Apollo, Clay, or LinkedIn Sales Navigator.

## Usage

```
/octave:prospector [options]
```

## Options

- `--playbook <name>` - Scope to a specific playbook's ICP criteria
- `--segment <name>` - Filter by market segment
- `--persona <name>` - Target specific persona type
- `--company <domain>` - Find people at a specific company
- `--similar-to <domain>` - Find companies similar to this one
- `--count <n>` - Number of results (default: 10)

## Examples

```
/octave:prospector                                    # Interactive mode
/octave:prospector --playbook "Enterprise Sales"     # Use playbook ICP
/octave:prospector --segment "Healthcare"            # Healthcare companies
/octave:prospector --persona "CTO" --segment "SaaS"  # CTOs at SaaS companies
/octave:prospector --similar-to stripe.com           # Companies like Stripe
/octave:prospector --company acme.com                # Decision makers at Acme
```

## Instructions

When the user runs `/octave:prospector`:

### Step 1: Determine Search Mode

If no options provided, ask:

```
What kind of prospects are you looking for?

1. Companies that fit a playbook's ICP
2. People at a specific company
3. Companies similar to a reference account
4. Open search (I'll help you define criteria)

Your choice:
```

### Step 2: Gather ICP Criteria

Use MCP tools to gather ICP criteria from your library:

**From Playbook:**
```
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })
```

Extract:
- Target segment characteristics
- Buyer persona titles and seniority
- Product fit criteria
- Qualifying questions (invert to search criteria)

**From Segment:**
```
get_entity({ oId: "<segment_oId>" })
```

Extract:
- Firmographic criteria (size, industry, location)
- Common characteristics
- Segment-specific signals

**From Persona:**
```
get_entity({ oId: "<persona_oId>" })
```

Extract:
- Common job titles
- Seniority level
- Department/function

### Step 3: Build Search Criteria

Translate library criteria to search parameters:

```
Building Search Criteria
========================

From your library, I'll search for:

Company Criteria:
- Industry: SaaS, Technology
- Size: 100-1000 employees
- Stage: Series A+
- Location: US, UK, Canada

Person Criteria:
- Titles: CTO, VP Engineering, Head of Engineering
- Seniority: VP+
- Department: Engineering, Technology

Derived from:
- Segment: "Scaling SaaS Companies"
- Persona: "CTO - Enterprise Tech"
- Playbook: "Enterprise DevOps Sale"

Proceed with this search? (or adjust criteria)
```

### Step 4: Execute Search

**For Company Search:**
```
find_company({
  industry: "<industry>",
  employeeCount: { min: X, max: Y },
  keywords: ["<relevant keywords>"],
  limit: 10
})
```

**For Person Search:**
```
find_person({
  searchMode: "people",
  fuzzyTitles: ["CTO", "VP Engineering"],
  companyDomain: "<domain>",  // if specified
  employeeCount: { min: X, max: Y },
  industry: "<industry>",
  limit: 10
})
```

**For Similar Companies:**
```
find_similar_companies({
  referenceCompany: { domain: "<domain>" },
  numResults: 10,
  similarityTraits: ["industry", "size", "business_model"]
})
```

**For People at Company:**
```
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from persona>"],
  limit: 10
})
```

### Step 5: Score and Present Results

For each result, calculate ICP fit:

**Company Scoring:**
```
qualify_company({
  companyDomain: "<domain>",
  additionalContext: "Evaluating fit for [playbook/segment]"
})
```

**Person Scoring:**
```
qualify_person({
  person: { linkedInProfile: "<url>" },
  additionalContext: "Evaluating fit for [persona] in [playbook]"
})
```

Present results:

```
Prospect Results: [Criteria Summary]
====================================

Found 10 companies matching your ICP:

---

1. TechCorp (techcorp.com)
   ========================
   Fit Score: 92/100 - EXCELLENT FIT

   Company Profile:
   - Industry: B2B SaaS
   - Employees: 450
   - Stage: Series C
   - Location: San Francisco, CA
   - Description: "Developer tools for cloud infrastructure..."

   Why They Fit:
   ✓ Matches segment: "Scaling SaaS Companies"
   ✓ Right size for your product (100-500 sweet spot)
   ✓ Growth signals: 50% headcount growth YoY
   ✓ Tech stack alignment: Uses [relevant technologies]

   Potential Concerns:
   ⚠ May have existing solution (competitor X mentioned on site)

   Key Contacts to Target:
   - Sarah Chen, CTO (Primary decision maker)
   - Mike Johnson, VP Engineering (Technical evaluator)
   - Lisa Park, Head of DevOps (User buyer)

   Recommended Playbook: "Enterprise DevOps Sale"
   Recommended Approach: Lead with scalability story

---

2. DataFlow Inc (dataflow.io)
   ==========================
   Fit Score: 85/100 - GOOD FIT

   [Similar format...]

---

[Continue for all results]

---

Summary
=======
- Excellent Fit (90+): 3 companies
- Good Fit (70-89): 5 companies
- Moderate Fit (50-69): 2 companies

Top Recommendation: TechCorp - strong signals, right stage, clear pain point
```

### Step 6: Generate Filter Recommendations

After presenting results, provide filters for scale:

```
Scale This Search
=================

To find more companies like these, use these filters in your prospecting tools:

APOLLO FILTERS
--------------
Industry: Software Development, SaaS
Employee Count: 100-1000
Funding: Series A, Series B, Series C
Technologies: Kubernetes, AWS, Docker
Location: United States, United Kingdom, Canada
Keywords: "developer tools" OR "infrastructure" OR "DevOps"

Copy-paste for Apollo:
[Generate Apollo-compatible filter string]

---

CLAY FILTERS
------------
Enrichment columns to add:
- Company growth rate (Harmonic)
- Tech stack (BuiltWith)
- Funding history (Crunchbase)

Filter criteria:
- growth_rate > 20%
- tech_stack CONTAINS "kubernetes"
- last_funding_date > 2024-01-01

Scoring formula suggestion:
= IF(employees > 100, 20, 0) + IF(growth_rate > 30, 30, 0) + ...

---

LINKEDIN SALES NAVIGATOR
------------------------
Company filters:
- Industry: Computer Software, Internet
- Company headcount: 51-200, 201-500, 501-1000
- Headquarters: United States

Lead filters:
- Seniority: VP, CXO, Director
- Function: Engineering, Information Technology
- Title keywords: CTO, "VP Engineering", "Head of"

Boolean search string:
(CTO OR "VP Engineering" OR "Head of Engineering") AND (SaaS OR "developer tools")

---

IDEAL SIGNALS TO LOOK FOR
-------------------------
Based on your successful deals, prioritize companies showing:
1. Recent funding (within 18 months)
2. Hiring for engineering roles (10+ open positions)
3. Job posts mentioning [pain point keywords]
4. Using [complementary technologies]
5. Expanding to new markets

Would you like me to:
1. Research any of these companies in depth
2. Find contacts at specific companies
3. Generate outreach for top prospects
4. Save these criteria to a playbook
```

### Step 7: Deep Dive Options

Offer to go deeper on specific prospects:

**Research Company:**
```
enrich_company({ companyDomain: "techcorp.com" })
```

Present enriched data with:
- Full company profile
- Recent news and events
- Key people and org structure
- Technology stack
- Funding history
- Growth signals

**Find Contacts:**
```
find_person({
  searchMode: "people",
  companyDomain: "techcorp.com",
  fuzzyTitles: ["<persona titles>"],
  limit: 5
})
```

Then for each:
```
enrich_person({
  person: { linkedInProfile: "<url>" }
})
```

**Generate Outreach:**
Suggest running `/octave:generate email` or `/octave:research` for selected prospects.

## ICP Criteria Translation

| Library Concept | Search Parameter |
|-----------------|------------------|
| Segment firmographics | Industry, employee count, location |
| Segment characteristics | Keywords, technologies |
| Persona job titles | fuzzyTitles, exactTitles |
| Persona seniority | Seniority filter |
| Playbook qualifying questions | Inverse as search signals |
| Product fit criteria | Technology stack, business model |

## MCP Tools Used

### Search Operations
- `find_company` - Company search with filters
- `find_person` - People search with filters
- `find_similar_companies` - Lookalike company search
- `find_similar_people` - Lookalike people search

### Enrichment Operations
- `enrich_company` - Full company intelligence
- `enrich_person` - Full person intelligence
- `qualify_company` - ICP scoring for company
- `qualify_person` - ICP scoring for person

### Library Context
- `get_playbook` - Get playbook ICP criteria
- `get_entity` - Get segment/persona details
- `search_knowledge_base` - Find relevant messaging

## Output Modes

### Default: Interactive
Shows results with scoring, asks for next steps.

### List Mode: `--format list`
Compact list format for quick scanning:

```
Companies (10 results)
=====================
1. TechCorp (techcorp.com) - 92/100 - SaaS, 450 emp
2. DataFlow (dataflow.io) - 85/100 - SaaS, 230 emp
3. CloudBase (cloudbase.com) - 78/100 - Infra, 180 emp
...
```

### Export Mode: `--format csv`
Outputs CSV-compatible format:

```
Company,Domain,Score,Industry,Employees,Location,Recommended Playbook
TechCorp,techcorp.com,92,SaaS,450,San Francisco,Enterprise DevOps
DataFlow,dataflow.io,85,SaaS,230,New York,Growth SaaS
...
```

## Error Handling

**No Results:**
> No companies found matching your criteria.
>
> Try:
> 1. Broadening the search (larger employee range, more industries)
> 2. Removing specific filters
> 3. Using similar-to search with a known good-fit company
>
> Current filters: [show active filters]

**Missing Library Context:**
> Playbook "[name]" not found in your library.
>
> Available playbooks:
> - Enterprise Sales
> - SMB Quick Close
> - Healthcare Vertical
>
> Or run /octave:audit to see your library coverage.

**API Limits:**
> Search returned maximum results. Narrow your criteria for more targeted results.
>
> Suggestions:
> - Add industry filter
> - Specify location
> - Use tighter employee range

## Related Skills

- `/octave:research` - Deep dive on specific prospects
- `/octave:generate` - Create outreach for prospects
- `/octave:brainstorm` - Generate campaign ideas for prospect lists
- `/octave:audit` - Ensure library has good ICP definitions
- `/octave:abm` - Full account plan for top prospects
- `/octave:icp-refine` - Refine ICP definitions from deal data
