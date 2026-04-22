# List Output Template

```
AVAILABLE WORKFLOWS
===================

TEMPLATES (4)
-------------

1. Full Outbound Pipeline
   Company research → qualify → find contacts → qualify → email outreach
   Inputs: company_domain (required), persona, num_contacts
   Run: /octave:workflow run "Full Outbound Pipeline" --company <domain>

2. Account-Based Research
   Deep research dossier on a target account with contact mapping
   Inputs: company_domain (required), num_contacts
   Run: /octave:workflow run "Account-Based Research" --company <domain>

3. Competitive Deal Prep
   Research + competitive positioning + tailored displacement outreach
   Inputs: company_domain (required), contact_email (required), competitor_name (required)
   Run: /octave:workflow run "Competitive Deal Prep" --company <domain> --contact <email> --competitor <name>

4. Persona-Targeted Outreach
   Find people matching a persona across companies and generate outreach
   Inputs: persona_name (required), industry, min_company_size
   Run: /octave:workflow run "Persona-Targeted Outreach" --persona "CTO"

---

MY WORKFLOWS (2)
-----------------

1. Security Team Outreach
   Find and reach security decision-makers at target companies
   Inputs: company_domain (required), num_contacts
   Run: /octave:workflow run "Security Team Outreach" --company <domain>

2. Partner Channel Mapping
   Research potential partners and their GTM teams
   Inputs: company_domain (required)
   Run: /octave:workflow run "Partner Channel Mapping" --company <domain>

---

Use /octave:workflow show <name> for details.
Use /octave:workflow create to build a new workflow.
```
