# Ad Set Output Template

The full output template for each ad set generated in Step 3. Produce one of these per persona/ICP/segment (based on the structure chosen in Step 1).

```markdown
## Ad Set: {Persona Name} {— Segment Name if ICP mode}

### Theme & Positioning
- **Primary Use Case**: {top use case for this persona from library}
- **Secondary Use Case**: {second use case}
- **Core Pain Point**: {from knowledge base search}
- **Competitive Angle**: {if campaign is competitive displacement, or if competitor is frequently mentioned for this persona}

### Ad Creative Variants

{4-8 variants, each derived from its source card — see variant-methodologies.md for the eight variant types, their methodologies, and skip conditions. For each variant, generate creative that respects the platform constraints from Step 1.}

### Prospect Language Sources
{For each variant, cite WHERE the language came from:}
- "getting burned on audits" — extracted from call with VP Eng at Acme Corp (2 weeks ago)
- "board breathing down our necks" — extracted from email reply by CTO at FinCo

{If no prospect language is available for this persona, note: "No field intelligence available yet — creative is based on library entity descriptions. Connect call/email integrations to generate prospect-voice creative."}

### Audience Targeting Recommendations

**Positive targeting:**
- Job titles: {derived from persona definition — e.g., "VP Engineering", "Director of Engineering", "Head of Engineering"}
- Industries: {derived from segment — e.g., "Financial Services", "Banking", "Insurance"}
- Company size: {derived from segment — e.g., "500-5000 employees"}
- Interests/keywords: {derived from use cases + competitor names}
- Platform-specific:
  - Google Search keywords: {5-10 recommended keywords derived from use case language}
  - Meta interests: {interest categories matching persona}
  - LinkedIn: {job functions, seniority levels, company sizes}

**Negative targeting / exclusions:**
- Job titles to exclude: {personas NOT in the target set — e.g., if targeting VPs, exclude individual contributors, interns, students}
- Industries to exclude: {segments NOT in the target set}
- Negative keywords (Google): {keywords that would attract wrong audience — e.g., "free", "tutorial", "certification", "jobs", competitor product names if NOT doing competitive campaign}

### Landing Page Recommendation
- **Suggested URL**: {from resources search, or user-provided}
- **Why**: {which resource matches this persona/use case best}
- If no resource found: "No matching resource found. Consider creating a landing page focused on {primary use case} for {persona}."

### Estimated Keyword Competitiveness (Google only)
Based on the use case language and competitor landscape in your library, categorize keywords as:
- **High competition** (likely expensive): {generic industry terms, competitor names}
- **Medium competition**: {specific use case terms}
- **Low competition / long-tail** (best value): {prospect-specific language, niche terms from calls}
```

## Per-platform creative examples

**Google Search example** (per variant):
```
Headline 1 (30 chars): "Stop Compliance Audit Panic"
Headline 2 (30 chars): "Automated Risk Monitoring"
Headline 3 (30 chars): "Trusted by 200+ FinServs"
Description 1 (90 chars): "Your security team shouldn't chase every new regulation. Get continuous compliance monitoring."
Description 2 (90 chars): "Join 200+ financial services firms who eliminated audit fire drills. Book a demo today."
```

**Meta example** (per variant):
```
Primary Text (125 chars): "Your security team is drowning in compliance audits. There's a better way."
Headline (40 chars): "End Compliance Fire Drills"
```
