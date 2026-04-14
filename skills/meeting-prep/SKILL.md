---
name: meeting-prep
description: "Strategic meeting battle plan with coaching frameworks, scripted talk tracks, and a phase-by-phase game plan — rendered as self-contained HTML. Use when user says 'meeting prep', 'battle plan', 'prep me for my meeting', 'prep for my call', or wants a coached game plan for an upcoming meeting. Do NOT use for account reference documents — use /octave:brief instead."
---

# /octave:meeting-prep - Strategic Meeting Battle Plan

Build a coached, strategic meeting battle plan rendered as a self-contained HTML document. Unlike `/octave:brief` (a reference dossier), this skill produces a battle plan — combining Octave intelligence with coaching frameworks to generate belief stacks, scripted talk tracks, discovery questions, a stakeholder map, landmine warnings, and a phase-by-phase game plan timed to your meeting duration.

Reads two coaching reference files at runtime: `references/strategic-coach.md` (belief stacking, ecosystem positioning, Socratic discovery) and `references/positioning-coach.md` (April Dunford's positioned sales pitch, competitive alternatives, feature-value-emotion ladder). If a user replaces these with their own coaching frameworks, the skill adapts automatically.

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>]
```

**Meeting types:** `discovery` (questions + beliefs + qualification), `demo` (positioned pitch + demo landmines), `follow-up` (updated pain + deal advancement), `executive` (TL;DR + board-level framing), `qbr` (value delivered + expansion), `general` (balanced, default).

## Instructions

When the user runs `/octave:meeting-prep`:

### Step 1: Understand the Context

**1.1 Identify the target:**
- Email address -> Person-targeted prep (enrich person + company)
- Domain -> Company-targeted prep (enrich company + find key contacts)
- LinkedIn URL -> Person-targeted prep
- Meeting description -> Extract company/people from context

**1.2** If `--type` not specified, ask: meeting type (discovery/demo/follow-up/executive/qbr/general), duration (30/45/60/90 min), prior context (transcript/notes/none), and attendees (names+roles or "unknown"). If attendees unknown, build a general stakeholder map from Octave contacts. If user provides a transcript or notes, synthesize alongside Octave data.

**1.3 Read coaching reference files** from the skill directory:
- `references/strategic-coach.md` — belief stacking, ecosystem positioning, enhancement framing, guardrail reframe, Socratic discovery
- `references/positioning-coach.md` — positioned sales pitch (5 steps), feature→value→emotion, competitive alternatives, category framing, language mining

Fall back to general sales coaching best practices if files not found.

### Step 2: Octave Context Gathering

Layer multiple intelligence sources to build a thorough battle plan. **Tell the user what you're researching and why.**

**Person-targeted prep** (email/LinkedIn):
```
enrich_person({ email: "jane@acme.com" })          # Role, seniority, social profiles
enrich_company({ domain: "acme.com" })              # Company context, size, industry
list_findings({ personOId: "<oId>", days: 90 })     # Recent conversation signals
```

**Company-targeted prep** (domain):
```
enrich_company({ domain: "acme.com" })              # Company intelligence
list_all_entities({ entityType: "persona" })         # Match attendees to personas
search_knowledge_base({ query: "acme challenges" })  # Relevant library intelligence
```

**Always attempt** (gracefully skip if empty):
```
get_playbook({ oId: "<playbook_oId>" })              # Messaging, value props, talk tracks
list_value_props({ playbookOId: "<oId>" })           # Persona-specific value props
list_findings({ companyOId: "<oId>", days: 90 })     # Conversation evidence
list_events({ companyOId: "<oId>", days: 90 })       # Recent activity signals
search_knowledge_base({ query: "<competitor>" })     # Competitive context
```

See `references/mcp-tool-reference.md` for the full tool catalog.

---

**Output of this step:** Present a content outline listing: target, meeting type, duration, attendees, the 12 sections to include (Header, TL;DR, Stakeholder Map, Their Pain, What They Need to Believe, Positioned Sales Pitch, Discovery Questions, Landmines & Watch-Outs, Coach's Corner, Meeting Game Plan, Deal Intelligence, The Line), and Octave sources used. Ask user to approve, add/remove sections, or go deeper before proceeding.

### Step 3: Style Selection

Uses the same CSS variable / style preset system as `/octave:deck`. Full presets in [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md). If `--style` not provided, offer: `midnight-pro` (default), `paper-minimal`, `executive-dark`, `soft-light`, `swiss-modern`, "Use my brand", or "Match my deck".

Default by meeting type: Executive and QBR use `executive-dark`; all others use `midnight-pro`. For "Use my brand," follow the deck skill's brand discovery flow. For "Match my deck," extract CSS variables from the existing deck file.

### Step 4: Generate HTML

Build a single self-contained HTML file. The battle plan is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

See `references/battle-plan-template.html` for the full HTML scaffold, CSS architecture, and component patterns (sidebar nav, collapsible sections, cards, badges, grids, print/responsive styles).

#### Meeting Type -> Section Emphasis

Not all sections are equally weighted in every meeting type:

| Meeting Type | Emphasized Sections | De-emphasized / Condensed |
|--------------|-------------------|---------------------------|
| Discovery | Their Pain, What They Need to Believe, Discovery Questions, Coach's Corner | Positioned Sales Pitch (lighter), Deal Intelligence |
| Demo | Positioned Sales Pitch, Stakeholder Map, Landmines & Watch-Outs | Discovery Questions (lighter), Deal Intelligence |
| Follow-up | Their Pain (updated), Deal Intelligence, Meeting Game Plan, Landmines | Stakeholder Map (condensed) |
| Executive | TL;DR, Positioned Sales Pitch (concise), Coach's Corner, The Line | Discovery Questions (fewer, strategic), Landmines (condensed) |
| QBR | Deal Intelligence, Coach's Corner, Meeting Game Plan | What They Need to Believe (condensed), Discovery Questions (expansion-focused) |
| General | All sections at equal weight | None |

#### Document Sections (12 total)

**1. Header** — Meeting title, date, type badge, duration badge, attendee list with roles.

**2. TL;DR** — 2-3 sentence opportunity summary. What's the situation, what's at stake, what's the play.

**3. Stakeholder Map** — Cards for each attendee tagged with buying role (Budget Owner, Champion, Evaluator, Gatekeeper). Each card: name, title, LinkedIn URL, inferred priorities, communication style, what they care about.

**4. Their Pain** — Pain points by stakeholder or theme, drawn from user context, Octave enrichment, findings, and playbook personas. Each: the pain (their words when possible), business impact, your response.

**5. What They Need to Believe** — Belief stacking from `strategic-coach.md`: 5-6 sequential beliefs, each rated Proven/Mostly Proven/Needs Proof with evidence. Color-coded status (green/yellow/red). Highlight weakest links as meeting priorities.

**6. Positioned Sales Pitch** — 5-step pitch from `positioning-coach.md` scripted for this meeting: (1) Set status quo, (2) Name the problem, (3) Introduce the category, (4) Position in category, (5) Proof. Each step has a talk track plus coaching note. Apply feature->value->emotion ladder for every product mention.

**7. Discovery Questions** — 8-12 questions max, segmented by stakeholder or category. Meeting-type-aware: Discovery=full battery, Demo=landmine/confirmation, Follow-up=progress/blockers, Executive=strategic/vision, QBR=value/expansion. Each with coaching note on what the answer reveals.

**8. Landmines & Watch-Outs** — 4-6 risk/mitigation pairs: competitive traps, likely objections with coached responses, topics to avoid, signals to watch for. Two-column layout.

**9. Coach's Corner** — Two perspectives from coaching frameworks. Strategic Coach: ecosystem positioning, enhancement framing, ideal customer fit, guardrail reframe. Positioning Coach: category framing, competitive alternatives, language mining, heads on pillows test. 3-4 bullets each.

**10. Meeting Game Plan** — Phase-by-phase timeline matched to meeting duration. See `references/game-plan-timing.md` for the full time allocation tables (30/45/60/90 min). Each phase: what to say, what to listen for, transition line.

**11. Deal Intelligence** — Budget, Champion, Decision Maker, Compelling Event, Competition, Stage, Next Milestone. If no deal data exists (new prospect), flag what to uncover in this meeting.

**12. The Line** — One memorable sentence capturing the strategic essence. The sticky-note insight for your monitor before the call. Examples: "They believe the problem exists but don't believe anyone's solved it — that's your opening." / "The VP is bought in; the Director needs proof it won't break their workflow."

#### Content Limits

Keep the battle plan thorough but scannable: TL;DR 2-3 sentences, Stakeholder Map 4-6 cards, Pain 4-6 points, Beliefs 5-6 max, Pitch 5 steps with 2-3 sentence tracks, Questions 8-12 max, Landmines 4-6 pairs, Coach's Corner 3-4 bullets per perspective, Game Plan 5-7 phases, Deal Intel 6-8 fields, The Line 1 sentence. Prioritize by meeting type relevance when trimming.

### Step 5: Delivery

Open the battle plan in the default browser. Present: file path, style, duration, sections included, and navigation tips (scroll, sidebar dots, collapsible sections, Cmd+P for PDF).

Offer follow-up actions: adjust/expand a section, add/remove stakeholders, go deeper on any topic, change style, regenerate for different duration, export PDF, generate a brief (`/octave:brief`), or build a presentation (`/octave:deck`).

## Error Handling

| Scenario | Response |
|----------|----------|
| No user context | Build from Octave intel + coaching frameworks; suggest re-running with notes after meeting |
| Coaching files not found | Fall back to general sales coaching; suggest adding custom files to `references/` |
| Octave connection failed | Build from user context + coaching frameworks; suggest checking MCP config |
| Company not found | Offer: check domain, try different domain, provide details manually |
| No findings data | Skip Prior Intelligence section; build from enrichment + coaching + user context |
| Attendees unknown | Build general stakeholder map from Octave contacts |
| No matching playbook | Use general value props from knowledge base + coaching frameworks |
