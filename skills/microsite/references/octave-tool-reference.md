# Octave Tool Reference

#### For All Microsites (Always Run)

Start with enrichment and qualification — this drives the personalization that makes microsites work:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — industry, size, tech stack, signals power the entire page |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — matched segment determines which Motion ICP cell to pull |
| Motions for offering | `list_motions()` | Always — find the Motion(s) covering this offering / motion type |
| Persona × segment matrix | `list_motion_icps({ motionOId })` | Always — pick the Motion ICP cell that matches their persona × segment |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | After identifying the cell — drives the solution section (Strategic narrative, Benefits and impacts, Pains and consequences) |
| Custom Motion Playbooks | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` | Pull any Thematic / Milestone / Account / Competitive angles layered on the Motion |
| Brand voice | `list_all_entities(entityType: "brand_voice")` | Always — consistent tone across the microsite |

---

#### For Person-Specific Microsites

When the target is an email address or named contact:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target — role, background, priorities |
| Person qualification | `qualify_person({ person: { ... } })` | When you need persona match for messaging precision |
| Find related contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to identify other stakeholders who might see the page |

---

#### For Social Proof & Credibility

The proof section is what turns a microsite from marketing fluff into a compelling story:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Customer references in their industry |
| Proof by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points about a specific topic or industry |
| Uploaded case studies | `search_resources({ query: "<industry> case study" })` | When the workspace has uploaded case study docs or assets |

---

#### For Competitive Angle

When the angle is competitive displacement:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on the specific competitor they likely use |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["competitor"] })` | Messaging angles for competitive deals |
| Competitive Motion Playbook | `list_motion_playbooks({ motionOId })` then `get_motion_playbook` on any `COMPETITIVE` narrative-type playbook | Pull a dedicated competitive Custom Motion Playbook if one exists for the relevant competitor |
| Competitive wins | `list_findings({ query: "<competitor>" })` | Real conversation intel about competitive situations |

---

#### For Trigger-Based Angle

When the angle is tied to a recent event or news:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation-based insights and signals |
| Events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Deal events, meetings, interactions |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific trigger event |

---

#### Additional Context

| What you need | Tool | When to use |
|---------------|------|-------------|
| Products | `list_all_entities({ entityType: "product" })` | When you need product capabilities for the solution section |
| Use cases | `list_all_entities({ entityType: "use_case" })` | When you want to show relevant use cases |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a comprehensive brief to work from |
