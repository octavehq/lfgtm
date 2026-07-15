---
name: positioning
description: Generate positioning systems and messaging frameworks — full visual HTML positioning documents, messaging frameworks, matrices, elevator pitches, positioning statements, narrative arcs, and value prop hierarchies. Use when user says "positioning system", "positioning exercise", "message framework", "messaging framework", "positioning anchors", "positioning document", "visual messaging framework", "elevator pitch", "messaging matrix", "narrative arc", "positioning statement", "value prop hierarchy", "build messaging", or asks for a comprehensive positioning or messaging deliverable.
---

# /octave:positioning - Positioning & Messaging System

Generate positioning systems and messaging frameworks — from a complete 8-section visual HTML positioning document to standalone text-based messaging artifacts like frameworks, matrices, elevator pitches, positioning statements, narrative arcs, and value prop hierarchies. Everything is pulled from your Octave library and grounded in real conversation evidence.

**Key differentiators:**
- vs `/octave:deck` -- deck is a presentation for an audience; positioning is a reference document
- vs `/octave:research` -- research is account-specific; positioning is about YOUR product/company

## Modes

The skill has two categories of output: the **full positioning system** (visual HTML) and **standalone messaging artifacts** (text-based).

```
POSITIONING SYSTEM (HTML output)
/octave:positioning                           # Full 8-section positioning system (default)
/octave:positioning full                      # Same as above
/octave:positioning system                    # Same as above
/octave:positioning message-framework         # Section 1: Message Framework pyramid
/octave:positioning anchors                   # Section 2: Positioning Anchors
/octave:positioning strategy                  # Section 3: Positioning Strategy table
/octave:positioning personas                  # Section 4: Persona-Based Messaging
/octave:positioning awareness                 # Section 5: Value Prop by Awareness Stage
/octave:positioning use-cases                 # Section 6: Use Case Messaging Canvas
/octave:positioning lifecycle                 # Section 7: Use Case Lifecycle
/octave:positioning homepage                  # Section 8: Homepage Messaging

MESSAGING ARTIFACTS (text output)
/octave:positioning framework                 # Messaging framework: pillars, proof points, key messages by audience
/octave:positioning matrix                    # Persona x use case messaging matrix
/octave:positioning elevator-pitch            # Elevator pitches (15s/30s/60s/2min)
/octave:positioning narrative                 # Company/product narrative arc
/octave:positioning value-props               # Value proposition hierarchy
/octave:positioning statement                 # Positioning statement with variations
```

## Usage

```
/octave:positioning [mode] [--product <name>] [--persona <name>] [--competitor <name>] [--style <preset>]
```

## Examples

```
/octave:positioning                                           # Full 8-section HTML positioning system
/octave:positioning full --product "Enterprise Platform"      # Full system for a specific product
/octave:positioning message-framework                         # Just the HTML message framework section
/octave:positioning personas --product "Analytics"            # HTML persona messaging for specific product
/octave:positioning homepage                                  # HTML homepage messaging template
/octave:positioning awareness --style paper-minimal           # HTML awareness funnel with light style
/octave:positioning framework                                 # Text-based messaging framework
/octave:positioning matrix                                    # Text-based persona x use case matrix
/octave:positioning elevator-pitch                            # Text-based elevator pitches at multiple lengths
/octave:positioning narrative                                 # Text-based narrative arc
/octave:positioning value-props                               # Text-based value prop hierarchy
/octave:positioning statement                                 # Text-based positioning statement
/octave:positioning framework --product "Platform"            # Messaging framework for a specific product
/octave:positioning elevator-pitch --persona "CTO"            # Persona-focused elevator pitches
```

## On-brand styling -- brand kit first, then generate (HTML modes only)

**Resolve the brand before generating (do not skip this step).** The positioning document wears the **workspace company's brand** (the Octave customer whose workspace you are operating in): it is their internal reference document. A target company's logo, if one is relevant to the scope (e.g., a competitive section naming a specific account), can appear in content but does not control the document's design system. See [brand kit usage](../shared/brand-kit-usage.md) for the full whose-brand, lookup, and extraction flow.

1. Call `get_workspace_company` to identify the workspace company, resolve it to a `<slug>`, and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`.
2. **If a kit exists -->** use it by default (it is their own brand, no need to ask). Style the output with the kit instead of a generic preset:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` --> **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`;
   - for doc-shaped output you can compose directly with `get-brand-components/scripts/render_kit.py` (hero / split / logos / pricing / cta / footer blocks).
3. **If no kit exists -->** offer to build one first: *"No brand kit for <Company> yet -- want me to capture it (~1 min) so this is on-brand?"* --> run `/octave:get-brand-components <domain>`, then proceed.
4. **If the user declines -->** generate with the default style/preset.

> The brand kit is the strongest styling signal -- when one is available, prefer it over generic `--style` presets. See the `get-brand-components` skill for the kit format, token contract, and renderer.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable document specifics

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

**Review gate (mandatory for HTML output):** After generating, run the review per the [review protocol](../shared/protocol.md). Don't ask permission, announce it at intake. For HTML output the protocol is a mandatory gate: the file is not opened or delivered until the combined scorecard has printed. For text output, run the protocol's mechanical preflight (em dashes, broken images/logos, unsafe links, leaked internals) plus the editorial reviewer's checks.

## Instructions

When the user runs `/octave:positioning`:

### Step 1: Determine Mode and Focus

**If no mode specified,** present the full menu:

```
What positioning or messaging artifact do you need?

POSITIONING SYSTEM (visual HTML document)
  1. Full Positioning System    - All 8 frameworks in one scrollable HTML document [DEFAULT]
  2. Single Section             - Just one section from the 8-framework system

MESSAGING ARTIFACTS (text-based)
  STRATEGIC
  3. Messaging Framework        - Complete: pillars, proof points, key messages by audience
  4. Positioning Statement      - Problem -> solution -> differentiation -> proof
  5. Narrative Arc              - Situation -> complication -> resolution story

  TACTICAL
  6. Messaging Matrix           - Persona x use case grid with tailored messages
  7. Value Prop Hierarchy       - Primary -> secondary -> supporting value props
  8. Elevator Pitches           - 15-second through 2-minute versions

Your choice:
```

Then ask for focus:
```
What's the focus?

1. [Product 1 from library]
2. [Product 2 from library]
3. Entire company / all products
4. Specific use case or segment

Your choice:
```

**If a specific mode was provided** (e.g., `framework`, `matrix`, `elevator-pitch`, `statement`, `narrative`, `value-props`), confirm and proceed directly to Step 2.

**If a positioning system mode was provided** (e.g., `full`, `system`, or a section name like `anchors`, `personas`), confirm the scope:

```
I'll generate a complete Messaging & Positioning system -- all 8 frameworks
in one visual HTML document.

THE 8 FRAMEWORKS
1. Message Framework     - 3-layer pyramid: market -> product -> value props by persona
2. Positioning Anchors   - Primary & secondary positioning statements
3. Positioning Strategy  - Tactical table: buyer, use case, problems, differentiators
4. Persona Messaging     - Core message translated per buying committee role
5. Awareness Funnel      - Value props adapted by buyer awareness stage
6. Use Case Canvas       - Current Way vs New Way per use case
7. Use Case Lifecycle    - Customer journey phases with touchpoints & messaging
8. Homepage Messaging    - Website implementation: primary vs secondary messaging

PRODUCT FOCUS
Which product should this positioning system cover?

1. [Product 1 from library]
2. [Product 2 from library]
3. Entire company / all products
4. Specific use case or segment

Your choice:
```

If a specific section was requested, confirm and proceed directly.

### Step 2: Octave Context Gathering

Gather all library intelligence in a single pass. **Tell the user what you're researching and why.** All modes share the same data pool -- gather once, then render into the chosen mode.

**Call as many tools as needed to build a complete picture.** The best positioning systems come from layering multiple sources -- product details + persona definitions + Motion ICP cell narratives + competitive context + proof points + conversation evidence all combine to create frameworks grounded in real data.

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all personas" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content -- "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept -- "how do we position for enterprise?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### Data Gathering Matrix

Every mode needs data from the library. Gather it all up front:

| What you need | Tool | Modes that use it |
|---------------|------|-------------------|
| All products | `list_entities({ entityType: "product" })` | All |
| Product deep dive | `get_entity({ oId: "<product_oId>" })` | All |
| All personas | `list_entities({ entityType: "persona" })` | All |
| All segments | `list_entities({ entityType: "segment" })` | system, framework, matrix, statement |
| All use cases | `list_entities({ entityType: "use_case" })` | system, framework, matrix, narrative, statement |
| All competitors | `list_entities({ entityType: "competitor" })` | system, framework, statement |
| Competitor details | `get_entity({ oId })` | system, framework |
| All Motions | `list_motions()` | All |
| Motion Playbooks under a Motion | `list_motion_playbooks({ motionOId })` | system, framework, matrix, value-props |
| Full Motion Playbook | `get_motion_playbook({ motionPlaybookOId })` | system, framework, matrix, value-props |
| Persona x segment matrix | `list_motion_icps({ motionOId })` | system, framework, matrix, value-props |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | system, framework, matrix, value-props, elevator-pitch |
| Proof points | `list_entities({ entityType: "proof_point" })` | All |
| References | `list_entities({ entityType: "reference" })` | system, framework, statement |
| Brand voice | `list_entities(entityType: "brand_voice")` | system (homepage tone), framework, elevator-pitch |
| Competitive positioning | `search_knowledge_base({ query: "<product> differentiation competitive advantage", entityTypes: ["competitor"] })` | system, framework, statement |
| What resonates | `list_findings({ query: "value propositions positive reactions resonated", startDate: "<90 days ago>", eventFilters: { sentiments: ["POSITIVE"] } })` | All |
| What falls flat | `list_findings({ query: "objections pushback concerns", startDate: "<90 days ago>", eventFilters: { sentiments: ["NEGATIVE"] } })` | system, framework, value-props |

---

**Output of this step:** Present a data summary and content outline:

```
POSITIONING DATA SUMMARY: [Product/Company]
=============================================

Product: [Name]
Product Category: [Category from entity]
Target Segments: [List]
Target Personas: [List with roles]
Use Cases: [List]
Competitors: [List]
Motions: [N] with [N] Motion ICP cells across Default + Custom Motion Playbooks
Proof Points: [N] available
Conversation Evidence: [N] positive findings, [N] negative findings

---

MODE: [Full Positioning System / Messaging Framework / etc.]

[Mode-specific outline -- see below]

Octave Sources Used:
- Products: [list]
- Personas: [list]
- Segments: [list]
- Use Cases: [list]
- Competitors: [list]
- Motions: [list] with [N] Motion ICP cells
- Proof Points: [N]
- Conversation Findings: [N]

---

Does this look right? I can:
1. Proceed to generation
2. Add or remove scope
3. Go deeper on any data area
4. Change the product focus
```

**Wait for user approval before proceeding.**

### Step 3: Generate Output (Branching by Mode)

---

#### Positioning System Modes (HTML Output): `full` / `system` / section names

##### Style Selection

The positioning system uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the shared [style-presets.md](../shared/style-presets.md).

Positioning documents default to strategic, executive-friendly presets. If `--style` was not provided, ask:

```
Pick a style for your positioning system:

DARK (recommended for strategy documents)
  1. midnight-pro      - Dark navy + blue accents. Executive feel. [DEFAULT]
  2. executive-dark    - Charcoal + gold. Premium boardroom.
  3. octave-brand      - Purple on navy. Product-aligned.

LIGHT
  4. paper-minimal     - Off-white + black type. Editorial.
  5. swiss-modern      - White + red accent. Clean minimal.
  6. soft-light        - Warm white + sage green. Calm.

VIBRANT
  7. solar-flare       - Deep orange gradients. Bold.
  8. aurora-gradient   - Purple-to-teal. Visionary.

OTHER
  9. Use my brand      - Extract from website or provide colors
  10. Match an existing doc - Reuse style from a previous /octave: document

Your choice (number or name, or press Enter for midnight-pro):
```

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback). If they select "Match an existing doc," ask for the file path and extract its CSS variables.

##### Generate HTML

Build a single self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

###### Output Directory

```
.octave-positioning/
|-- <product-kebab>-<YYYY-MM-DD>/
    |-- positioning-system.html
```

Example: `/octave:positioning --product "Octave"` produces `.octave-positioning/octave-2026-02-24/positioning-system.html`

For single sections: `.octave-positioning/octave-message-framework-2026-02-24/message-framework.html`

The `.octave-positioning/` directory should be in `.gitignore`.

###### HTML Architecture

The positioning system is a scrollable reference document -- not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

The full HTML structure, section templates, and CSS component patterns are defined in the references:
- [section-templates.md](references/section-templates.md) -- HTML templates for all 8 section types
- [section-layouts.md](references/section-layouts.md) -- Section-specific CSS patterns (grids, funnels, timelines, canvases)

See [html-scaffold.md](references/html-scaffold.md) for the full HTML + CSS scaffold of the positioning system document, including persona color system, highlight classes, and key differences from other doc skills.

###### Content Population

Populate each section using the templates in [section-templates.md](references/section-templates.md). Each section has:
- A **section number** and **title** in the summary
- A **subtitle** explaining what this framework answers
- The **visual layout** appropriate to that framework type
- **Real data** from the Octave context gathered in Step 2

For each section, use `generate_content` to synthesize the gathered library data into the framework structure:

```
generate_content({
  instructions: "Generate content for the [Section Name] framework.
    Structure: [specific structure for this section -- see section-templates.md]
    Ground everything in the library data provided. Do not invent data.",
  customContext: "<relevant subset of gathered library intelligence>"
})
```

Then render the generated content into the HTML template for that section.

###### Content Density Guidelines

Each section has specific content limits to keep the document scannable:

| Section | Content Limit |
|---------|--------------|
| Message Framework | 3 layers, up to 8 value prop rows (one per persona-use case combination) |
| Positioning Anchors | 1 primary anchor + 3-5 secondary anchors + 2-3 combination examples |
| Positioning Strategy | 1 summary row + up to 6 comparison rows (competitive alternatives) |
| Persona Messaging | Up to 5 persona columns (User, Champion, Decision Maker, Financial Buyer, Technical Influencer) |
| Awareness Funnel | 4 fixed columns x 3 rows (Lead with, Earn trust by, To convince them) |
| Use Case Canvas | 1 canvas per use case, up to 3 use cases |
| Use Case Lifecycle | 6-8 journey phases per use case |
| Homepage Messaging | 1 primary column + 1 secondary column with up to 5 expansion rows |

---

#### Messaging Artifact Modes (Text Output)

For text-based messaging modes, skip style selection. Generate using `generate_content` and present as formatted text.

##### Mode: `framework` -- Messaging Framework

See [messaging-framework.md](references/messaging-framework.md) for the messaging framework template.

```
generate_content({
  instructions: "Generate a comprehensive messaging framework for [product/company].
    Structure:
    - Core positioning statement
    - 3-4 messaging pillars with supporting points
    - Key messages by audience (for each persona)
    - Proof points mapped to each pillar
    - Competitive differentiators
    All grounded in the library data provided.",
  customContext: "<all gathered library intelligence>"
})
```

##### Mode: `matrix` -- Messaging Matrix

See [messaging-matrix.md](references/messaging-matrix.md) for the messaging matrix template.

##### Mode: `elevator-pitch` -- Elevator Pitches

See [elevator-pitches.md](references/elevator-pitches.md) for the elevator pitches template.

##### Mode: `narrative` -- Narrative Arc

See [narrative-arc.md](references/narrative-arc.md) for the narrative arc template.

##### Mode: `value-props` -- Value Prop Hierarchy

See [value-prop-hierarchy.md](references/value-prop-hierarchy.md) for the value prop hierarchy template.

##### Mode: `statement` -- Positioning Statement

See [positioning-statement.md](references/positioning-statement.md) for the positioning statement template.

### Step 3b: Review Pipeline — MANDATORY GATE for HTML output

After generating, run the review per the [review protocol](../shared/protocol.md) before delivering. Do not ask the user whether to review, announce that it's happening.

For HTML Positioning System modes, the protocol is a mandatory gate: run the full pipeline (preflight, then the dedicated `octave-editorial-reviewer` and `octave-presentation-reviewer` pair in parallel) against the generated HTML file, and do not open or deliver it until the combined scorecard has printed. For text-based Messaging Artifact modes, run the preflight and the editorial reviewer's checks against the generated text (presentation checks don't apply to plain text output).

### Step 4: Delivery

#### For HTML Positioning System Modes

After the review pipeline scorecard has been output:

1. **Open the document** in the default browser
2. **Present a summary:**

```
POSITIONING SYSTEM READY
=========================

Folder: .octave-positioning/<product>-<date>/
File:   .octave-positioning/<product>-<date>/positioning-system.html
Style:  [Preset name]

Product: [Product name]
Sections: [N] frameworks generated
Data sources: [N] personas, [N] use cases, [N] value props, [N] proof points

Navigation:
- Scroll through all 8 frameworks
- Sidebar dots on the right track your position
- Click section headers to collapse/expand
- PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-positioning/<product>-<date>/positioning-system.html  -- or Cmd+P / Ctrl+P -> Save as PDF

---

Want me to:
1. Adjust or expand a section
2. Go deeper on a specific framework
3. Generate a messaging artifact from this positioning (framework, matrix, elevator pitch, etc.)
4. Create a sales deck from this (/octave:deck)
5. Save positioning statements back to library
6. Change the style
7. Export as PDF (print dialog)
8. Done
```

#### For Text-Based Messaging Modes

After generating any messaging artifact:

```
What would you like to do next?

1. Generate another messaging artifact
2. Create a persona-specific version
3. Generate the full visual positioning system from this foundation
4. Save key messages back into Motion ICP narratives (Strategic narrative, Benefits and impacts, etc.)
5. Generate content from this messaging (/octave:generate)
6. Export this framework
7. Done
```

**If the user wants to save back to library:**

```
# Save positioning statements to product entity
update_entity({
  entityType: "product",
  oId: "<product_oId>",
  instructions: "Update positioning to: [primary positioning anchor]. Category: [category]. Primary value prop: [primary VP]."
})

# Fold the positioning system into Motion Playbook narrative sections (Strategic narrative,
# Benefits and impacts, Pains and consequences) for the Motion ICP cells in scope.
# A positioning exercise typically updates the Default Motion Playbook of the offering's Motion,
# touching every persona x segment cell to reflect the new anchors and persona messaging.
update_motion_playbook({
  motionPlaybookOId: "<motion_playbook_oId>",
  instructions: "Update Strategic narrative and Benefits and impacts across all Motion ICP cells to reflect: primary anchor = [...], persona-specific messages = [...]."
})
```

## MCP Tools Used

### Library -- Fetching Entities
- `list_entities` -- Quick scan of all entities of a type (products, personas, segments, use cases, competitors)
- `list_entities` -- Fetch entities with full data and pagination (personas, proof points, references, use cases)
- `get_entity` -- Deep dive on one specific entity (product, competitor)

### Motions
- `list_motions` -- Motions for the offering
- `list_motion_playbooks` -- Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` -- Full Motion Playbook details
- `list_motion_icps` -- Persona x segment matrix
- `find_motion_icp` -- Per-cell narrative + Learning Loop learnings

### Library -- Searching
- `search_knowledge_base` -- Semantic search across library entities and resources (competitive positioning, differentiation)
- `search_resources` -- Search uploaded docs and reference material

### Intelligence & Signals
- `list_findings` -- Conversation findings: what resonates (positive) and what falls flat (negative)
- `list_entities` (entityType: "brand_voice") -- Brand voice for tone consistency

### Content Generation
- `generate_content` -- Synthesize library data into framework structures and messaging artifacts

### Library Updates (Post-Generation)
- `update_entity` -- Save positioning statements back to product entity
- `update_motion_playbook` -- Fold positioning into Motion Playbook narrative sections (Strategic narrative, Benefits and impacts, Pains and consequences) across the Motion's ICP cells

## Error Handling

**No Products Found:**
> No products in your library.
>
> Positioning and messaging frameworks need at least one product to build around.
> Run `/octave:library create product` first, or describe your product and I'll work from that.

**No Personas Found:**
> No personas defined yet.
>
> I can generate a basic positioning system, but persona-specific sections (Message Framework value props, Persona Messaging, Homepage expansion, Messaging Matrix) will be limited.
> Run `/octave:library create persona` to add personas.

**No Use Cases Found:**
> No use cases defined.
>
> Sections 6 (Use Case Canvas) and 7 (Use Case Lifecycle) require use cases. I'll skip them and generate the other 6 sections. Text-based modes like matrix and narrative will also be limited.
> Run `/octave:library create use_case` to add use cases.

**No Motions or Motion ICP Cells:**
> No Motions or Motion ICP cells found.
>
> The Message Framework and Persona Messaging sections will use product-level information only. For richer output, create a Motion in the Motion builder (which auto-generates a Default Motion Playbook covering the persona x segment matrix), then re-run this skill.

**No Competitors Found:**
> No competitors in your library.
>
> Sections 3 (Positioning Strategy) and 6 (Use Case Canvas) will omit competitive comparisons. Messaging framework competitive differentiation will also be limited.
> Run `/octave:library create competitor` to add competitors.

**No Proof Points:**
> No proof points found to support the messaging.
>
> I'll generate the framework with placeholder evidence.
> Mark items tagged [NEEDS EVIDENCE] and add proof points as they become available.

**No Conversation Evidence:**
> No conversation findings available.
>
> The positioning system will be built entirely from library data. As your team logs calls, re-running this skill will surface what resonates and what doesn't -- making each iteration sharper.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The positioning system builder needs Octave data to generate useful frameworks. Without it, most sections would be empty.
> To reconnect: check your Octave MCP configuration and reconnect

## Related Skills

- `/octave:deck` -- Build a presentation from your positioning
- `/octave:product-launch` -- Launch plan using this positioning as the messaging foundation
- `/octave:research` -- Account-specific prep document (positioning is product-level)
- `/octave:battlecard-doc` -- Competitive intelligence (feeds into Section 3: Strategy)
- `/octave:train` -- Team training grounded in your positioning
- `/octave:one-pager` -- Customer-facing document built from positioning
- `/octave:pipeline` -- Pipeline strategy informed by your positioning
- `/octave:one-pager` -- Collateral that uses this messaging
- `/octave:library` -- Update library entities with finalized positioning
