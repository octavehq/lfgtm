# Octave Tool Reference

#### Company & Contact Research

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always — gives industry, size, tech stack, signals |
| Champion profile | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When champion is known — tailor language to their role |
| Key stakeholders | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you need to understand the buying committee |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to quantify "why us" for this account |
| Person qualification | `qualify_person({ person: { ... } })` | When champion fit matters for framing |

---

#### Motions & Messaging

| What you need | Tool | When to use |
|---------------|------|-------------|
| All Motions | `list_motions()` | Quick scan to find the right Motion(s) for this offering |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` | Default + Custom Motion Playbooks under the Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full Motion Playbook content — drives the proposal narrative |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | Find the persona × segment cell that matches the account |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full per-cell narrative (Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) + Learning Loop learnings |

---

#### Proof Points & Social Proof

This is critical for proposals. Buyers share these documents internally — social proof is what gets budget approved.

| What you need | Tool | When to use |
|---------------|------|-------------|
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Proof by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | Proof points relevant to their industry or use case |
| Uploaded case studies | `search_resources({ query: "case study" })` | Existing case study documents or PDFs |

---

#### Competitive Context

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor profiles | `search_knowledge_base({ query: "<competitor>", entityTypes: ["competitor"] })` | When a competitor is in the deal |
| Competitor deep dive | `get_entity({ oId })` | Full competitor strengths, weaknesses, positioning |
| Competitive Motion Playbook | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` on any `COMPETITIVE` narrative-type playbook | Pull a dedicated competitive Custom Motion Playbook if one exists |
| Products for comparison | `list_entities({ entityType: "product" })` | When you need feature-level differentiation |
| Competitive resources | `search_resources({ query: "<competitor>" })` | Uploaded battlecards, analyst reports |

---

#### Conversation History & Deal Intel

| What you need | Tool | When to use |
|---------------|------|-------------|
| Recent findings | `list_findings({ query: "<company>", startDate: "<relevant period>" })` | What was said in calls — objections, priorities, feature requests |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Timeline of the relationship |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific call or meeting |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Comprehensive brief to work from |

---

#### Existing Resources

| What you need | Tool | When to use |
|---------------|------|-------------|
| All resources | `list_resources()` | Browse uploaded docs, URLs, Drive files |
| Search resources | `search_resources({ query: "<topic>" })` | Find existing proposals, pricing docs, case studies |
