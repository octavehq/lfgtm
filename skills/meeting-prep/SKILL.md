---
name: meeting-prep
description: Strategic meeting battle plan with coaching frameworks, scripted talk tracks, and a phase-by-phase game plan — rendered as self-contained HTML. Use when user says "meeting prep", "battle plan", "prep me for my meeting", "prep for my call", or wants a coached game plan for an upcoming meeting. Do NOT use for account reference documents — use /octave:brief instead.
---

# /octave:meeting-prep - Strategic Meeting Battle Plan

Build a coached, strategic meeting battle plan rendered as a self-contained HTML document. Unlike `/octave:brief` (a reference dossier), this skill produces a battle plan — combining Octave intelligence with coaching frameworks to generate belief stacks, scripted talk tracks, discovery questions, a stakeholder map, landmine warnings, and a phase-by-phase game plan timed to your meeting duration.

The skill reads two coaching reference files at runtime:
- `references/strategic-coach.md` — Enterprise strategic sales coaching (belief stacking, ecosystem positioning, Socratic discovery)
- `references/positioning-coach.md` — Product positioning coaching based on April Dunford's methodology (positioned sales pitch, competitive alternatives, feature-value-emotion ladder)

If a user replaces these files with their own coaching frameworks, the skill adapts automatically.

**Key differentiators:**
- vs `/octave:brief` — brief is a reference dossier; meeting-prep is a coached battle plan with talk tracks and a timed game plan
- vs `/octave:research` — research outputs plain text; meeting-prep renders a styled HTML document with coaching intelligence
- vs `/octave:deck` — deck is a slide presentation for the audience; meeting-prep is internal prep for the seller

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>]
```

## Examples

```
/octave:meeting-prep acme.com                                    # General meeting prep
/octave:meeting-prep jane@acme.com --type discovery              # Discovery call battle plan
/octave:meeting-prep acme.com --type demo                        # Demo prep with talk tracks
/octave:meeting-prep acme.com --type executive                   # Executive meeting with board framing
/octave:meeting-prep jane@acme.com --type follow-up              # Follow-up with prior call context
/octave:meeting-prep acme.com --type qbr --style executive-dark  # QBR prep with specific style
/octave:meeting-prep "meeting with VP Sales at Acme"             # Context-based prep
```

## Meeting Types

| Type | Primary Focus |
|------|--------------|
| `discovery` | Discovery questions primary, belief framework, qualification |
| `demo` | Positioned pitch tailored to demo flow, demo landmines |
| `follow-up` | Updated pain from prior calls, deal advancement |
| `executive` | Concise TL;DR, executive talk tracks, board-level framing |
| `qbr` | Value delivered, renewal/expansion angles |
| `general` | Balanced all sections (default) |

## Instructions

When the user runs `/octave:meeting-prep`:

### Step 1: Understand the Context

**1.1 Identify the target:**
- Email address -> Person-targeted prep (enrich person + company)
- Domain -> Company-targeted prep (enrich company + find key contacts)
- LinkedIn URL -> Person-targeted prep
- Meeting description -> Extract company/people from context

**1.2 Detect or ask meeting type:**

If `--type` not specified, infer from context or ask:

```
What type of meeting are you prepping for?

1. Discovery — First conversation, qualifying the opportunity
2. Demo — Showing the product, proving value
3. Follow-up — Continuing a conversation, advancing the deal
4. Executive — High-level strategic conversation
5. QBR — Quarterly business review with existing customer
6. General — Balanced battle plan (default)

Your choice:
```

**1.3 Ask meeting duration:**

The duration drives the game plan timeline — phases get proportional time allocations.

```
How long is this meeting?

1. 30 minutes
2. 45 minutes
3. 60 minutes
4. 90 minutes

Your choice:
```

**1.4 Collect user context:**

Ask if the user has any prior context to incorporate:

```
Do you have any prior context to fold in?

1. Call transcript or recording notes
2. Email thread or meeting notes
3. My own notes / talking points
4. No prior context — use Octave intel + coaching frameworks

Paste or describe (or press Enter to skip):
```

If the user provides a transcript, notes, or email thread, synthesize that context alongside Octave data. If they skip, proceed with Octave intel and coaching frameworks only.

**1.5 Identify attendees:**

```
Who's attending? (names, titles, emails — or "I don't know yet")
```

If attendees are unknown, build a general stakeholder map from Octave contacts.

**1.6 Read coaching reference files:**

Read the two coaching reference files from the skill directory:
- `references/strategic-coach.md` — Extract: belief stacking, ecosystem positioning, enhancement framing, ideal customer fit, guardrail reframe, Socratic discovery
- `references/positioning-coach.md` — Extract: positioned sales pitch (5 steps), feature→value→emotion, competitive alternatives, category framing, language mining, heads on pillows test

If the files are not found, fall back to general sales coaching best practices.

### Step 2: Octave Context Gathering

Based on the target and meeting type, use Octave MCP tools to build a complete intelligence picture. **Tell the user what you're researching and why.**

**Call as many tools as needed to build a thorough battle plan.** The best meeting preps layer multiple sources — company enrichment + person enrichment + playbook messaging + proof points + conversation intel + coaching frameworks all combine to create a document grounded in real data. Don't stop at one tool when several would give you a stronger prep.

Not every tool applies to every meeting. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest context for the meeting type and target.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Findings and events — always attempt, gracefully skip:**

ALWAYS try to pull findings and events if you have a company domain or contact emails. Use a 90-day window. If data exists, it populates the "Prior Intelligence" section. If not, silently omit — no error message.

- `list_findings({ query: "<company or contact>", startDate: "<90 days ago>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent
- `get_event_detail({ eventOId })` — deep dive on specific past interactions

---

#### For Person-Targeted Preps

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted preps — gives background, role, priorities |
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, signals |
| ICP fit (person) | `qualify_person({ person: { ... } })` | When you need persona match and fit assessment |
| ICP fit (company) | `qualify_company({ companyDomain })` | When you need segment match and ICP scoring |
| Additional contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to map the broader buying committee |
| Matching playbook | `get_playbook({ oId, includeValueProps: true })` | After identifying relevant playbook — full strategy + value props |
| Playbook search | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | When you need the best-fit playbook by concept |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | Conversation-based insights from past interactions |
| Deal history | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Timeline of deal events |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Quick comprehensive brief to use as a starting point |

---

#### For Company-Targeted Preps

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate the Stakeholder Map |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan to find the right strategic approach |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | Full content + value props for the matching playbook |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for the recommended playbook |
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |

---

**Output of this step:** Present a content outline to the user for approval before generating:

```
BATTLE PLAN OUTLINE: [Company/Person] — [Meeting Type]
========================================================

Target: [Company name / Person name at Company]
Meeting Type: [Discovery / Demo / Follow-up / Executive / QBR / General]
Duration: [30 / 45 / 60 / 90] minutes
Attendees: [Names and roles, or "General stakeholder map"]
Style: [Will be selected in Step 3]

---

SECTIONS TO INCLUDE
-------------------

1. Header — Meeting details, date, duration, attendees
2. TL;DR — 2-3 sentence opportunity summary
3. Stakeholder Map — Buying roles: budget owner, champion, evaluator, gatekeeper
4. Their Pain — By stakeholder/theme, from context + enrichment
5. What They Need to Believe — Belief stack with proof status
6. Positioned Sales Pitch — 5-step scripted talk track
7. Discovery Questions — Segmented by stakeholder, meeting-type-aware
8. Landmines & Watch-Outs — Risk/mitigation pairs, competitive traps
9. Coach's Corner — Strategic + positioning coach perspectives
10. Meeting Game Plan — Timeline phased to [duration] minutes
11. Deal Intelligence — Budget, champion, decision maker, compelling event
12. The Line — One memorable sentence

Octave Sources Used:
- Company enrichment: [Company] — [key insights]
- Person enrichment: [Person] — [persona match]
- Playbook: [Playbook name] — [strategic angle]
- Proof points: [N] references pulled
- Findings: [N] recent signals (or "none found — skipped")
- Competitive: [If applicable]
- User context: [Transcript / notes / none]

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Go deeper on any area
4. Change the meeting type or emphasis
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

The battle plan uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

Battle plans default to readability-optimized presets. If `--style` was not provided, ask:

```
Pick a style for your battle plan:

1. midnight-pro     — Dark navy, white text, blue accents (default)
2. paper-minimal    — Off-white, black type, editorial simplicity
3. executive-dark   — Charcoal + gold, premium boardroom aesthetic
4. soft-light       — Warm white + sage green, calm and approachable
5. swiss-modern     — White + red accent, Bauhaus minimal
6. Use my brand     — Extract from website or provide colors
7. Match my deck    — Use the same style as an existing /octave:deck

Your choice (or press Enter for default):
```

| Meeting Type | Recommended Default |
|--------------|-------------------|
| Discovery | `midnight-pro` |
| Demo | `midnight-pro` |
| Follow-up | `midnight-pro` |
| Executive | `executive-dark` |
| QBR | `executive-dark` |
| General | `midnight-pro` |

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback). If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. The battle plan is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-meeting-prep/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:meeting-prep acme.com --type discovery` -> `.octave-meeting-prep/acme-discovery-2026-02-27/acme-discovery.html`

The `.octave-meeting-prep/` directory should be in `.gitignore`.

#### Meeting Type → Section Emphasis

Not all sections are equally weighted in every meeting type. The type determines emphasis:

| Meeting Type | Emphasized Sections | De-emphasized / Condensed |
|--------------|-------------------|---------------------------|
| Discovery | Their Pain, What They Need to Believe, Discovery Questions, Coach's Corner | Positioned Sales Pitch (lighter), Deal Intelligence |
| Demo | Positioned Sales Pitch, Stakeholder Map, Landmines & Watch-Outs | Discovery Questions (lighter), Deal Intelligence |
| Follow-up | Their Pain (updated), Deal Intelligence, Meeting Game Plan, Landmines | Stakeholder Map (condensed) |
| Executive | TL;DR, Positioned Sales Pitch (concise), Coach's Corner, The Line | Discovery Questions (fewer, strategic), Landmines (condensed) |
| QBR | Deal Intelligence, Coach's Corner, Meeting Game Plan | What They Need to Believe (condensed), Discovery Questions (expansion-focused) |
| General | All sections at equal weight | None |

#### Document Sections (12 total)

**1. Header**
Meeting title, generation date, meeting type badge (pill label like "Discovery Battle Plan" or "Executive Prep"), duration badge, attendee list with roles.

**2. TL;DR**
2-3 sentence opportunity summary. What's the situation, what's at stake, what's the play. Scannable in 10 seconds.

**3. Stakeholder Map**
Cards for each attendee or known contact, tagged with buying role:
- **Budget Owner** — Controls the money
- **Champion** — Internal advocate, wants you to win
- **Evaluator** — Technical or functional gatekeeper
- **Gatekeeper** — Controls access to decision makers

Each card: name, title, LinkedIn URL (if known), inferred priorities, communication style notes, what they care about.

**4. Their Pain**
Pain points organized by stakeholder or by theme, drawn from:
- User-provided context (transcript, notes, email thread)
- Octave enrichment data
- Findings from prior conversations
- Persona pain points from matching playbook

Each pain point: the pain (their words when possible), the business impact, your response.

**5. What They Need to Believe**
Apply the belief stacking framework from `strategic-coach.md`:
- 5-6 sequential beliefs, each building on the previous
- Each rated: Proven / Mostly Proven / Needs Proof
- Evidence or proof point for each
- Highlight the weakest links — these are the meeting priorities

Visual: color-coded status (green = Proven, yellow = Mostly Proven, red = Needs Proof).

**6. Positioned Sales Pitch**
Apply the 5-step positioned sales pitch from `positioning-coach.md`, scripted for this specific meeting:
1. Set the status quo — "Here's what we see in your world..."
2. Name the problem — "But as [trigger], [what breaks]..."
3. Introduce the category — "That's why [category] exists..."
4. Position in the category — "[Product] is the [differentiator] [category]..."
5. Proof — "[Similar customer] saw [result]..."

Each step includes a scripted talk track (actual words to say) plus a coaching note on delivery. Apply the feature→value→emotion ladder from the positioning framework for every product mention.

**7. Discovery Questions**
Segmented by stakeholder (if attendees are known) or by category. Meeting-type-aware:
- Discovery: full question battery (diagnostic, forcing-function, accountability from `strategic-coach.md`)
- Demo: landmine questions, confirmation questions, "what would make this real?" questions
- Follow-up: progress questions, blocker questions, expansion questions
- Executive: strategic questions, vision questions, decision criteria
- QBR: value realization, adoption, expansion opportunity

8-12 questions max. Each with a brief coaching note on what the answer reveals.

**8. Landmines & Watch-Outs**
Risk/mitigation pairs:
- Competitive traps (things the competitor wants them to ask about)
- Objections likely to surface (with coached responses)
- Topics to avoid or defer
- Signals to watch for (body language, tone shifts, questions they ask)

Visual: two-column layout — Risk | Mitigation.

**9. Coach's Corner**
Two perspectives synthesized from the coaching frameworks:

**Strategic Coach** (from `strategic-coach.md`):
- Ecosystem positioning angle for this account
- Enhancement framing recommendation
- Ideal customer fit assessment
- Guardrail reframe if applicable

**Positioning Coach** (from `positioning-coach.md`):
- Category framing recommendation
- Competitive alternative analysis (what they'd do without you)
- Language to mine from prior context
- Heads on pillows test for this audience

**10. Meeting Game Plan**
Phase-by-phase timeline matched to the meeting duration. Time allocations are proportional:

**30-minute meeting:**
| Phase | Time | Focus |
|-------|------|-------|
| Open & Rapport | 0-3 min | Set the frame, confirm agenda |
| Discovery / Pitch | 3-18 min | Core content (meeting-type-dependent) |
| Proof & Stories | 18-23 min | Evidence that lands |
| Next Steps | 23-28 min | Clear commitments |
| Buffer | 28-30 min | Questions, soft close |

**45-minute meeting:**
| Phase | Time | Focus |
|-------|------|-------|
| Open & Rapport | 0-5 min | Set the frame, confirm agenda |
| Discovery / Pitch | 5-25 min | Core content |
| Proof & Stories | 25-33 min | Evidence that lands |
| Discussion | 33-40 min | Questions, objection handling |
| Next Steps | 40-45 min | Clear commitments |

**60-minute meeting:**
| Phase | Time | Focus |
|-------|------|-------|
| Open & Rapport | 0-5 min | Set the frame, confirm agenda |
| Context Setting | 5-12 min | Status quo, their world |
| Discovery / Pitch | 12-35 min | Core content |
| Proof & Stories | 35-45 min | Evidence that lands |
| Discussion | 45-53 min | Questions, objection handling |
| Next Steps | 53-58 min | Clear commitments |
| Buffer | 58-60 min | Soft close |

**90-minute meeting:**
| Phase | Time | Focus |
|-------|------|-------|
| Open & Rapport | 0-7 min | Set the frame, confirm agenda |
| Context Setting | 7-18 min | Status quo, mutual discovery |
| Discovery / Pitch | 18-50 min | Core content (deeper, more interactive) |
| Proof & Stories | 50-62 min | Evidence + customer stories |
| Deep Discussion | 62-75 min | Objections, technical deep-dives |
| Action Planning | 75-85 min | Concrete next steps, timeline |
| Close | 85-90 min | Summary, commitments |

Each phase includes: what to say, what to listen for, and a transition line to the next phase.

**11. Deal Intelligence**
Key deal context at a glance:
- **Budget**: Known budget or budget signals
- **Champion**: Who is championing internally (or "not yet identified")
- **Decision Maker**: Who ultimately signs
- **Compelling Event**: Timeline driver, if any (quarter end, contract renewal, initiative launch)
- **Competition**: Who else is in the deal
- **Stage**: Current deal stage and how long they've been there
- **Next Milestone**: What needs to happen next

If no deal data exists (new prospect), present what's known and flag what to uncover in this meeting.

**12. The Line**
One memorable sentence that captures the strategic essence of this meeting. This is the thing you'd write on a sticky note and put on your monitor before the call. It should distill the entire battle plan into a single actionable insight.

Examples:
- "They believe the problem exists but don't believe anyone's solved it — that's your opening."
- "The VP is bought in; the Director needs proof it won't break their workflow."
- "This is a displacement deal — lead with what they lose by staying, not what they gain by switching."

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Battle Plan: [Company] — [Meeting Type]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.6;
    }

    /* === Layout === */
    .battle-plan-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .bp-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .bp-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
    }
    .bp-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.4);
    }

    /* === Section Styles === */
    .bp-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    /* === Collapsible Sections (details/summary) === */
    details.bp-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.bp-section summary {
      cursor: pointer;
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.75rem 0;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    details.bp-section summary::before {
      content: "\25B6";
      font-size: 0.7em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.bp-section[open] summary::before {
      transform: rotate(90deg);
    }

    /* === Cards === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
    }
    .card:hover {
      background: var(--bg-card-hover);
    }

    /* === Stakeholder Cards === */
    .stakeholder-card {
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }
    .stakeholder-avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--brand-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      flex-shrink: 0;
    }

    /* === Buying Role Badge === */
    .role-badge {
      display: inline-block;
      padding: 0.2rem 0.6rem;
      border-radius: var(--radius-pill);
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .role-badge.champion { background: var(--success); color: white; }
    .role-badge.budget-owner { background: var(--brand-primary); color: white; }
    .role-badge.evaluator { background: var(--secondary); color: white; }
    .role-badge.gatekeeper { background: var(--warning); color: #1a1a1a; }

    /* === Belief Stack === */
    .belief-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      border-radius: var(--radius);
      margin-bottom: 0.5rem;
    }
    .belief-status {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .belief-status.proven { background: var(--success); }
    .belief-status.mostly-proven { background: var(--warning); }
    .belief-status.needs-proof { background: var(--error); }

    /* === Talk Track Cards === */
    .talk-track {
      background: var(--bg-elevated);
      border-left: 3px solid var(--brand-primary);
      padding: 1rem 1.25rem;
      border-radius: 0 var(--radius) var(--radius) 0;
      margin-bottom: 1rem;
    }
    .talk-track .label {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      margin-bottom: 0.25rem;
    }
    .coaching-note {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-style: italic;
      margin-top: 0.5rem;
    }

    /* === Risk/Mitigation Grid === */
    .risk-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(0.75rem, 1.5vw, 1.25rem);
    }
    .risk-item { border-left: 3px solid var(--error); }
    .mitigation-item { border-left: 3px solid var(--success); }

    /* === Game Plan Timeline === */
    .game-plan-phase {
      display: grid;
      grid-template-columns: 100px 1fr;
      gap: 1rem;
      padding: 1rem 0;
      border-bottom: 1px solid var(--border);
    }
    .phase-time {
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: var(--brand-primary);
      font-weight: 600;
    }

    /* === The Line (featured) === */
    .the-line {
      text-align: center;
      padding: 2rem;
      border: 2px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      margin-top: 2rem;
    }
    .the-line blockquote {
      font-family: var(--font-display);
      font-size: clamp(1.2rem, 2.5vw, 1.6rem);
      font-weight: 500;
      font-style: italic;
      color: var(--text-primary);
    }

    /* === Meeting Type Badge === */
    .meeting-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--brand-primary);
      color: white;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .duration-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      font-size: 0.75rem;
      font-weight: 600;
    }

    /* === Grid Utilities === */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }

    /* === Typography === */
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .body-text { font-size: clamp(0.85rem, 1.2vw, 1rem); }
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); }

    /* === Deal Intel Cards === */
    .deal-intel-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: clamp(0.75rem, 1.5vw, 1.25rem);
    }
    .deal-intel-card {
      text-align: center;
      padding: 1rem;
    }
    .deal-intel-card .label {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.25rem;
    }
    .deal-intel-card .value {
      font-family: var(--font-display);
      font-size: 1.1rem;
      font-weight: 600;
    }

    /* === Print Styles === */
    @media print {
      .bp-nav { display: none; }
      .battle-plan-container { max-width: 100%; padding: 1rem; }
      details.bp-section { open; }
      details.bp-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .meeting-badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .risk-grid { grid-template-columns: 1fr; }
      .game-plan-phase { grid-template-columns: 80px 1fr; }
      .bp-nav { display: none; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="bp-nav" id="bp-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <!-- Main Battle Plan -->
  <main class="battle-plan-container">

    <!-- 1. Header -->
    <header class="bp-section">
      <span class="meeting-badge">[Meeting Type] Battle Plan</span>
      <span class="duration-badge">[Duration] min</span>
      <h1>[Company Name] — Meeting Prep</h1>
      <p class="text-secondary">[Date] · [Attendees summary]</p>
    </header>

    <!-- 2. TL;DR -->
    <section class="bp-section" id="tldr">
      <h2 class="section-title">TL;DR</h2>
      <p class="body-text">[2-3 sentence opportunity summary]</p>
    </section>

    <!-- 3. Stakeholder Map -->
    <details class="bp-section" open id="stakeholder-map">
      <summary>Stakeholder Map</summary>
      <div class="grid-2">
        <!-- Stakeholder cards with role badges -->
      </div>
    </details>

    <!-- 4. Their Pain -->
    <details class="bp-section" open id="their-pain">
      <summary>Their Pain</summary>
      <!-- Pain points by stakeholder or theme -->
    </details>

    <!-- 5. What They Need to Believe -->
    <details class="bp-section" open id="belief-stack">
      <summary>What They Need to Believe</summary>
      <!-- Belief items with status indicators -->
    </details>

    <!-- 6. Positioned Sales Pitch -->
    <details class="bp-section" open id="sales-pitch">
      <summary>Positioned Sales Pitch</summary>
      <!-- 5-step talk track cards -->
    </details>

    <!-- 7. Discovery Questions -->
    <details class="bp-section" open id="discovery-questions">
      <summary>Discovery Questions</summary>
      <!-- Questions segmented by stakeholder or category -->
    </details>

    <!-- 8. Landmines & Watch-Outs -->
    <details class="bp-section" open id="landmines">
      <summary>Landmines & Watch-Outs</summary>
      <div class="risk-grid">
        <!-- Risk/mitigation pairs -->
      </div>
    </details>

    <!-- 9. Coach's Corner -->
    <details class="bp-section" open id="coachs-corner">
      <summary>Coach's Corner</summary>
      <div class="grid-2">
        <!-- Strategic coach card + Positioning coach card -->
      </div>
    </details>

    <!-- 10. Meeting Game Plan -->
    <details class="bp-section" open id="game-plan">
      <summary>Meeting Game Plan</summary>
      <!-- Phase timeline matched to duration -->
    </details>

    <!-- 11. Deal Intelligence -->
    <details class="bp-section" open id="deal-intel">
      <summary>Deal Intelligence</summary>
      <div class="deal-intel-grid">
        <!-- Budget, Champion, Decision Maker, Compelling Event cards -->
      </div>
    </details>

    <!-- 12. The Line -->
    <section class="bp-section" id="the-line">
      <div class="the-line">
        <blockquote>"[One memorable sentence]"</blockquote>
      </div>
    </section>

  </main>

  <script>
    // Generate nav dots from sections
    // Intersection Observer for active section tracking
    // Smooth scroll on nav dot click
    // Open all details on print (window.onbeforeprint)
  </script>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts). No JavaScript frameworks.

#### Content Density Guidelines

Battle plans are reference documents — they should be thorough but scannable:

| Section | Content Limit |
|---------|--------------|
| TL;DR | 2-3 sentences max |
| Stakeholder Map | 4-6 stakeholder cards max |
| Their Pain | 4-6 pain points max |
| What They Need to Believe | 5-6 beliefs max |
| Positioned Sales Pitch | 5 steps, each with 2-3 sentence talk track |
| Discovery Questions | 8-12 questions max |
| Landmines & Watch-Outs | 4-6 risk/mitigation pairs |
| Coach's Corner | 2 perspectives, 3-4 bullets each |
| Meeting Game Plan | 5-7 phases matching duration |
| Deal Intelligence | 6-8 data fields |
| The Line | 1 sentence |

If a section would exceed its limit, prioritize by relevance to the meeting type and trim the rest.

### Step 5: Delivery

After generating the HTML file:

1. **Open the battle plan** in the default browser
2. **Present a summary:**

```
BATTLE PLAN READY
==================

Folder: .octave-meeting-prep/<name>-<date>/
File:   .octave-meeting-prep/<name>-<date>/<name>.html
Style:  [Preset name or "Custom Brand"]
Duration: [30 / 45 / 60 / 90] min game plan
Sections: [List of included sections]

Navigation:
- Scroll naturally to read through sections
- Click nav dots on the right edge to jump to sections
- Click section headers to collapse/expand
- Print-friendly: Cmd+P / Ctrl+P for clean PDF output

---

Want me to:
1. Adjust or expand a section
2. Add/remove stakeholders
3. Go deeper on any topic (beliefs, talk tracks, questions)
4. Change the style
5. Regenerate for a different meeting duration
6. Export as PDF (print dialog)
7. Generate a brief for this account (/octave:brief)
8. Build a presentation from this (/octave:deck)
9. Done
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `find_company` — Find companies matching criteria
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` — Fetch entities with full data and pagination (proof points, references, etc.)
- `get_entity` — Deep dive on one specific entity
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (stage changes, meetings, outcomes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief (useful as a starting point)
- `generate_content` — Generate positioning or messaging content

## Error Handling

**No user context provided:**
> No prior context provided. I'll build the battle plan from Octave intelligence and coaching frameworks.
>
> The prep will be strong on strategy and positioning. After the meeting, run this again with your notes for a grounded follow-up prep.

**Coaching reference files not found:**
> Coaching reference files not found in `references/`. Using general sales coaching best practices.
>
> To customize coaching frameworks, add `strategic-coach.md` and `positioning-coach.md` to the `skills/meeting-prep/references/` directory.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> I'll build the battle plan from your provided context and coaching frameworks. The result will focus on talk tracks, discovery questions, and game plan without enrichment data.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Check the domain spelling and try again
> 2. Try a different domain or company name
> 3. Provide company details manually and I'll build the battle plan

**No Findings Data:**
> No conversation signals found for [company/person] in the last 90 days.
>
> Skipping the Prior Intelligence section. The battle plan will focus on enrichment data, coaching frameworks, and your provided context.

**Attendees Not Specified:**
> No specific attendees provided. I'll build a general stakeholder map from Octave contacts and apply coaching frameworks broadly.
>
> Tip: Adding attendee names and roles before the meeting makes the belief stack and talk tracks much sharper.

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use general value props and positioning from the knowledge base, combined with coaching frameworks. Consider creating a playbook for this segment: `/octave:library create playbook`

## Related Skills

- `/octave:brief` — Internal account dossier (reference doc without coaching frameworks)
- `/octave:research` — Deep-dive research on a company or person
- `/octave:deck` — Full slide presentation for the audience
- `/octave:one-pager` — Customer-facing leave-behind document
- `/octave:battlecard` — Competitive intelligence and displacement strategy
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:abm` — Account-based planning with stakeholder mapping
