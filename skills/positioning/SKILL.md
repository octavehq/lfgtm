---
name: positioning
description: Generate a complete Messaging & Positioning system as a stunning visual HTML document — message framework, positioning anchors, strategy table, persona-based messaging, awareness funnel, use case canvases, lifecycle mapping, and homepage messaging. Use when user says "positioning system", "positioning exercise", "message framework", "positioning anchors", "positioning document", "visual messaging framework", or asks for a comprehensive positioning deliverable.
---

# /octave:positioning - Visual Messaging & Positioning System

Generate a complete, visual Messaging & Positioning system rendered as a single stunning HTML document. Eight interconnected frameworks — from the foundational Message Framework through Positioning Anchors, Strategy Table, Persona Messaging, Awareness Funnel, Use Case Canvas, Lifecycle Mapping, and Homepage Messaging — all pulled from your Octave library and grounded in real conversation evidence.

Unlike `/octave:messaging` which outputs text-based frameworks, this skill renders the full positioning system as a polished, scrollable HTML document with visual grids, color-coded persona columns, funnel diagrams, timelines, and split-view canvases. Designed to be the single source of truth for your product's positioning — bookmarkable, printable, and shareable.

**Key differentiators:**
- vs `/octave:messaging` — messaging outputs text; positioning renders it as a visual HTML system
- vs `/octave:deck` — deck is a presentation for an audience; positioning is a reference document
- vs `/octave:brief` — brief is account-specific; positioning is about YOUR product/company

## Usage

```
/octave:positioning [section] [--product <name>] [--style <preset>]
```

## Modes

```
/octave:positioning                           # Full 8-section exercise (default)
/octave:positioning message-framework         # Section 1: Message Framework pyramid
/octave:positioning anchors                   # Section 2: Positioning Anchors
/octave:positioning strategy                  # Section 3: Positioning Strategy table
/octave:positioning personas                  # Section 4: Persona-Based Messaging
/octave:positioning awareness                 # Section 5: Value Prop by Awareness Stage
/octave:positioning use-cases                 # Section 6: Use Case Messaging Canvas
/octave:positioning lifecycle                 # Section 7: Use Case Lifecycle
/octave:positioning homepage                  # Section 8: Homepage Messaging
/octave:positioning --product "Platform"      # Focus on specific product
/octave:positioning --style executive-dark    # Choose style preset
```

## Examples

```
/octave:positioning                                           # Full exercise for primary product
/octave:positioning --product "Enterprise Platform"           # Full exercise for a specific product
/octave:positioning message-framework                         # Just the message framework
/octave:positioning personas --product "Analytics"            # Persona messaging for specific product
/octave:positioning homepage                                  # Homepage messaging template
/octave:positioning awareness --style paper-minimal           # Awareness funnel with light style
```

## Instructions

When the user runs `/octave:positioning`:

### Step 1: Understand the Context

**Determine scope:**

If no section specified, confirm full exercise:

```
I'll generate a complete Messaging & Positioning system — all 8 frameworks
in one visual HTML document.

THE 8 FRAMEWORKS
1. Message Framework     — 3-layer pyramid: market → product → value props by persona
2. Positioning Anchors   — Primary & secondary positioning statements
3. Positioning Strategy  — Tactical table: buyer, use case, problems, differentiators
4. Persona Messaging     — Core message translated per buying committee role
5. Awareness Funnel      — Value props adapted by buyer awareness stage
6. Use Case Canvas       — Current Way vs New Way per use case
7. Use Case Lifecycle    — Customer journey phases with touchpoints & messaging
8. Homepage Messaging    — Website implementation: primary vs secondary messaging

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

Gather all library intelligence in a single pass. **Tell the user what you're researching and why.** All 8 sections share the same data pool — gather once, render many.

**Call as many tools as needed to build a complete picture.** The best positioning systems come from layering multiple sources — product details + persona definitions + playbook messaging + competitive context + proof points + conversation evidence all combine to create frameworks grounded in real data.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all personas" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept — "how do we position for enterprise?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### Data Gathering Matrix

Every section needs data from the library. Gather it all up front:

| What you need | Tool | Sections that use it |
|---------------|------|---------------------|
| All products | `list_all_entities({ entityType: "product" })` | All 8 |
| Product deep dive | `get_entity({ oId: "<product_oId>" })` | All 8 |
| All personas | `list_entities({ entityType: "persona" })` | 1, 3, 4, 5, 7, 8 |
| All segments | `list_entities({ entityType: "segment" })` | 1, 3 |
| All use cases | `list_entities({ entityType: "use_case" })` | 1, 3, 6, 7 |
| All competitors | `list_all_entities({ entityType: "competitor" })` | 2, 3, 6 |
| Competitor details | `get_entity({ oId })` | 3, 6 |
| All playbooks | `list_all_entities({ entityType: "playbook" })` | 1, 2, 4, 5, 8 |
| Playbook + value props | `get_playbook({ oId, includeValueProps: true })` | 1, 2, 4, 5, 8 |
| Proof points | `list_entities({ entityType: "proof_point" })` | 2, 3, 5 |
| References | `list_entities({ entityType: "reference" })` | 2, 3 |
| Brand voice | `list_brand_voices()` | 8 (homepage tone) |
| Competitive positioning | `search_knowledge_base({ query: "<product> differentiation competitive advantage", entityTypes: ["competitor", "playbook"] })` | 2, 3, 6 |
| What resonates | `list_findings({ query: "value propositions positive reactions resonated", startDate: "<90 days ago>", eventFilters: { sentiments: ["POSITIVE"] } })` | 2, 5 |
| What falls flat | `list_findings({ query: "objections pushback concerns", startDate: "<90 days ago>", eventFilters: { sentiments: ["NEGATIVE"] } })` | 3, 5 |

---

**Output of this step:** Present a data summary and content outline:

```
POSITIONING SYSTEM OUTLINE: [Product/Company]
===============================================

Product: [Name]
Product Category: [Category from entity]
Target Segments: [List]
Target Personas: [List with roles]
Use Cases: [List]
Competitors: [List]
Playbooks: [N] with [N] value props
Proof Points: [N] available
Conversation Evidence: [N] positive findings, [N] negative findings

---

SECTIONS TO GENERATE
---------------------

1. Message Framework
   Market: [Champion] + [Company Type] + [Use Case] + [Problem]
   MVP: [Category] + [Most Compelling Capability] + [Feature] + [Main Benefit]
   Value Props: [N] value props across [N] personas

2. Positioning Anchors
   Primary: "[Product] is a [category] for [persona] doing [use case]"
   Secondary: [N] supporting anchors

3. Positioning Strategy
   [N] rows: competitive alternatives, problems, differentiators, proof by role

4. Persona-Based Messaging
   [N] personas: User, Champion, Decision Maker, Financial Buyer, Technical Influencer

5. Value Prop by Awareness Stage
   4 stages: Problem Unaware → Problem Aware → Solution Aware → Product Aware

6. Use Case Messaging Canvas
   [N] use cases: Current Way vs New Way

7. Use Case Lifecycle
   [N] use cases with customer journey phases

8. Homepage Messaging
   Primary (homepage): core product + persona + problem + solution
   Secondary (other pages): additional personas, problems, capabilities

Octave Sources Used:
- Products: [list]
- Personas: [list]
- Segments: [list]
- Use Cases: [list]
- Competitors: [list]
- Playbooks: [list] with [N] value props
- Proof Points: [N]
- Conversation Findings: [N]

---

Does this look right? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Go deeper on any data area
4. Change the product focus
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

The positioning system uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [style-presets.md](../deck/references/style-presets.md).

Positioning documents default to strategic, executive-friendly presets. If `--style` was not provided, ask:

```
Pick a style for your positioning system:

DARK (recommended for strategy documents)
  1. midnight-pro      — Dark navy + blue accents. Executive feel. [DEFAULT]
  2. executive-dark    — Charcoal + gold. Premium boardroom.
  3. octave-brand      — Purple on navy. Product-aligned.

LIGHT
  4. paper-minimal     — Off-white + black type. Editorial.
  5. swiss-modern      — White + red accent. Clean minimal.
  6. soft-light        — Warm white + sage green. Calm.

VIBRANT
  7. solar-flare       — Deep orange gradients. Bold.
  8. aurora-gradient   — Purple-to-teal. Visionary.

OTHER
  9. Use my brand      — Extract from website or provide colors
  10. Match an existing doc — Reuse style from a previous /octave: document

Your choice (number or name, or press Enter for midnight-pro):
```

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback). If they select "Match an existing doc," ask for the file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

#### Output Directory

```
.octave-positioning/
└── <product-kebab>-<YYYY-MM-DD>/
    └── positioning-system.html
```

Example: `/octave:positioning --product "Octave"` produces `.octave-positioning/octave-2026-02-24/positioning-system.html`

For single sections: `.octave-positioning/octave-message-framework-2026-02-24/message-framework.html`

The `.octave-positioning/` directory should be in `.gitignore`.

#### HTML Architecture

The positioning system is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

The full HTML structure, section templates, and CSS component patterns are defined in the references:
- [section-templates.md](references/section-templates.md) — HTML templates for all 8 section types
- [section-layouts.md](references/section-layouts.md) — Section-specific CSS patterns (grids, funnels, timelines, canvases)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Positioning System: [Product/Company]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset — see style-presets.md) === */
    :root { /* ... paste chosen preset variables here ... */ }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-primary); font-family: var(--font-body); line-height: 1.6; }

    /* === Document Layout (wider than brief — positioning is grid-heavy) === */
    .doc-container { max-width: 1100px; margin: 0 auto; padding: 2rem clamp(1rem, 4vw, 3rem); }

    /* === Sticky Sidebar Navigation === */
    .sidebar { position: fixed; top: 50%; transform: translateY(-50%); right: clamp(0.5rem, 2vw, 2rem); display: flex; flex-direction: column; gap: 0.35rem; z-index: 100; }
    .sidebar a { display: block; width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); transition: all 0.2s var(--ease); text-decoration: none; }
    .sidebar a.active { background: var(--brand-primary); transform: scale(1.5); }
    .sidebar a:hover { background: var(--brand-500); transform: scale(1.3); }

    /* === Section Base === */
    .section { margin-bottom: clamp(3rem, 6vh, 5rem); padding-top: 1rem; }
    .section-number { font-family: var(--font-mono); font-size: 0.75rem; color: var(--brand-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.25rem; }
    .section-title { font-family: var(--font-display); font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 700; margin-bottom: 0.5rem; }
    .section-subtitle { font-size: clamp(0.85rem, 1.2vw, 1rem); color: var(--text-secondary); margin-bottom: 1.5rem; }

    /* === Collapsible Sections (details/summary) === */
    details.section { border-bottom: 1px solid var(--border); padding-bottom: 2rem; }
    details.section summary { cursor: pointer; list-style: none; display: flex; align-items: center; gap: 0.75rem; }
    details.section summary::before { content: "\25B6"; font-size: 0.6em; color: var(--brand-primary); transition: transform 0.2s ease; }
    details.section[open] summary::before { transform: rotate(90deg); }
    details.section .section-body { margin-top: 1.5rem; }

    /* === Header Banner === */
    .header-banner { padding: clamp(2rem, 5vh, 4rem) 0; border-bottom: 1px solid var(--border); margin-bottom: clamp(2rem, 4vh, 3rem); }
    .header-banner h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 700; margin-bottom: 0.5rem; }
    .header-banner .subtitle { font-size: clamp(1rem, 1.5vw, 1.25rem); color: var(--text-secondary); }
    .meta-badges { display: flex; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap; }
    .meta-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); background: var(--bg-card); border: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); }

    /* === Cards & Grids === */
    .card { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
    .card:hover { border-color: var(--border-strong); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: clamp(0.75rem, 1.5vw, 1rem); }

    /* === Callout Box === */
    .callout { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border-left: 4px solid var(--brand-primary); }

    /* === Tables === */
    .data-table { width: 100%; border-collapse: collapse; font-size: clamp(0.8rem, 1vw, 0.9rem); }
    .data-table th { text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-strong); color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .data-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); vertical-align: top; }

    /* === Persona Colors === */
    .persona-user { border-color: #34d399; }
    .persona-user .persona-dot { background: #34d399; }
    .persona-champion { border-color: #60a5fa; }
    .persona-champion .persona-dot { background: #60a5fa; }
    .persona-decision { border-color: #f59e0b; }
    .persona-decision .persona-dot { background: #f59e0b; }
    .persona-financial { border-color: #f87171; }
    .persona-financial .persona-dot { background: #f87171; }
    .persona-technical { border-color: #a78bfa; }
    .persona-technical .persona-dot { background: #a78bfa; }
    .persona-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.4rem; }

    /* === Badges === */
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: var(--radius-pill); font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }
    .badge-primary { background: rgba(59, 130, 246, 0.15); color: var(--brand-primary); }
    .badge-success { background: rgba(52, 211, 153, 0.15); color: var(--success); }
    .badge-warning { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
    .badge-error { background: rgba(248, 113, 113, 0.15); color: var(--error); }

    /* === Highlighted Text (for positioning anchors) === */
    .highlight { padding: 0.1rem 0.4rem; border-radius: 3px; font-weight: 600; }
    .highlight-category { background: rgba(168, 85, 247, 0.2); color: #c084fc; }
    .highlight-persona { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
    .highlight-usecase { background: rgba(52, 211, 153, 0.2); color: #6ee7b7; }
    .highlight-problem { background: rgba(248, 113, 113, 0.2); color: #fca5a5; }
    .highlight-feature { background: rgba(251, 191, 36, 0.2); color: #fcd34d; }

    /* === Section-specific layouts — see references/section-layouts.md === */
    /* Included inline: message framework bands, funnel columns, timeline, canvas split */

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3, .grid-4, .grid-5 { grid-template-columns: 1fr; }
      .sidebar { display: none; }
      .funnel-grid { grid-template-columns: 1fr; }
      .canvas-split { grid-template-columns: 1fr; }
      .timeline-phases { overflow-x: auto; }
    }

    /* === Print === */
    @media print {
      .sidebar { display: none; }
      details.section { break-inside: avoid; }
      details.section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .meta-badge { border: 1px solid #ccc; background: transparent; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="sidebar" id="sidebar-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <div class="doc-container">

    <!-- Header Banner -->
    <header class="header-banner" id="section-header">
      <p style="color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem; margin-bottom: 0.5rem;">Messaging & Positioning System</p>
      <h1>[Product / Company Name]</h1>
      <p class="subtitle">[Product category] for [primary persona] in [target segment]</p>
      <div class="meta-badges">
        <span class="meta-badge">Generated [Date]</span>
        <span class="meta-badge">[N] Personas</span>
        <span class="meta-badge">[N] Use Cases</span>
        <span class="meta-badge">[N] Value Props</span>
        <span class="meta-badge">[N] Proof Points</span>
      </div>
    </header>

    <!-- Section 1: Message Framework -->
    <!-- Section 2: Positioning Anchors -->
    <!-- Section 3: Positioning Strategy -->
    <!-- Section 4: Persona-Based Messaging -->
    <!-- Section 5: Value Prop by Awareness Stage -->
    <!-- Section 6: Use Case Messaging Canvas -->
    <!-- Section 7: Use Case Lifecycle -->
    <!-- Section 8: Homepage Messaging -->
    <!-- See references/section-templates.md for full HTML per section -->

  </div>

  <script>
    // Sidebar: generate dots from .section elements
    // Intersection Observer highlights active section dot
    // Smooth scroll on dot click
    // Open all details on print
    (function() {
      const sections = document.querySelectorAll('.section');
      const sidebar = document.getElementById('sidebar-nav');
      sections.forEach((section, i) => {
        const dot = document.createElement('a');
        dot.href = '#' + section.id;
        dot.title = section.querySelector('.section-title')?.textContent || '';
        if (i === 0) dot.classList.add('active');
        sidebar.appendChild(dot);
      });
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            sidebar.querySelectorAll('a').forEach(d => d.classList.remove('active'));
            const active = sidebar.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { threshold: 0.2 });
      sections.forEach(s => observer.observe(s));
      window.onbeforeprint = () => {
        document.querySelectorAll('details.section').forEach(d => d.open = true);
      };
    })();
  </script>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts). No JavaScript frameworks.

**Key differences from brief/battlecard-doc HTML:**
- **Max-width 1100px** (wider — positioning frameworks need horizontal space for grids)
- **Persona color system** — consistent color coding across all 8 sections (User=green, Champion=blue, Decision Maker=amber, Financial Buyer=red, Technical Influencer=purple)
- **Highlight classes** — for styling positioning anchor keywords (category, persona, use case, problem, feature)
- **Grid-4 and Grid-5** — for persona columns and awareness stage columns
- **Section numbering** — "Section 01" labels for clear progression through the exercise

#### Content Population

Populate each section using the templates in [section-templates.md](references/section-templates.md). Each section has:
- A **section number** and **title** in the summary
- A **subtitle** explaining what this framework answers
- The **visual layout** appropriate to that framework type
- **Real data** from the Octave context gathered in Step 2

For each section, use `generate_content` to synthesize the gathered library data into the framework structure:

```
generate_content({
  instructions: "Generate content for the [Section Name] framework.
    Structure: [specific structure for this section — see section-templates.md]
    Ground everything in the library data provided. Do not invent data.",
  customContext: "<relevant subset of gathered library intelligence>"
})
```

Then render the generated content into the HTML template for that section.

#### Content Density Guidelines

Each section has specific content limits to keep the document scannable:

| Section | Content Limit |
|---------|--------------|
| Message Framework | 3 layers, up to 8 value prop rows (one per persona-use case combination) |
| Positioning Anchors | 1 primary anchor + 3-5 secondary anchors + 2-3 combination examples |
| Positioning Strategy | 1 summary row + up to 6 comparison rows (competitive alternatives) |
| Persona Messaging | Up to 5 persona columns (User, Champion, Decision Maker, Financial Buyer, Technical Influencer) |
| Awareness Funnel | 4 fixed columns × 3 rows (Lead with, Earn trust by, To convince them) |
| Use Case Canvas | 1 canvas per use case, up to 3 use cases |
| Use Case Lifecycle | 6-8 journey phases per use case |
| Homepage Messaging | 1 primary column + 1 secondary column with up to 5 expansion rows |

### Step 5: Delivery

After generating the HTML file:

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
- Print-friendly: Cmd+P / Ctrl+P for clean PDF

---

Want me to:
1. Adjust or expand a section
2. Go deeper on a specific framework
3. Generate campaign content from this positioning (/octave:campaign)
4. Create a sales deck from this (/octave:deck)
5. Save positioning statements back to library
6. Change the style
7. Export as PDF (print dialog)
8. Done
```

**If the user wants to save back to library:**

```
# Save positioning statements to product entity
update_entity({
  entityType: "product",
  oId: "<product_oId>",
  instructions: "Update positioning to: [primary positioning anchor]. Category: [category]. Primary value prop: [primary VP]."
})

# Add or update value props in playbook
add_value_props({
  playbookOId: "<playbook_oId>",
  instructions: "<persona-specific value props from the message framework>",
  numValuesPerPersona: 3
})
```

## MCP Tools Used

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (products, personas, segments, use cases, competitors, playbooks)
- `list_entities` — Fetch entities with full data and pagination (personas, proof points, references, use cases)
- `get_entity` — Deep dive on one specific entity (product, competitor)
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources (competitive positioning, differentiation)
- `search_resources` — Search uploaded docs and reference material

### Intelligence & Signals
- `list_findings` — Conversation findings: what resonates (positive) and what falls flat (negative)
- `list_brand_voices` — Brand voice for homepage messaging tone

### Content Generation
- `generate_content` — Synthesize library data into framework structures

### Library Updates (Post-Generation)
- `update_entity` — Save positioning statements back to product entity
- `add_value_props` — Save value props to playbooks

## Error Handling

**No Products Found:**
> No products in your library.
>
> The positioning system needs at least one product to build frameworks around.
> Run `/octave:library create product` first, or describe your product and I'll work from that.

**No Personas Found:**
> No personas defined yet.
>
> I can generate a basic positioning system, but persona-specific sections (Message Framework value props, Persona Messaging, Homepage expansion) will be limited.
> Run `/octave:library create persona` to add personas.

**No Use Cases Found:**
> No use cases defined.
>
> Sections 6 (Use Case Canvas) and 7 (Use Case Lifecycle) require use cases. I'll skip them and generate the other 6 sections.
> Run `/octave:library create use_case` to add use cases.

**No Playbooks or Value Props:**
> No playbooks or value propositions found.
>
> The Message Framework and Persona Messaging sections will use product-level information only. For richer output, create a playbook with value propositions.

**No Competitors Found:**
> No competitors in your library.
>
> Sections 3 (Positioning Strategy) and 6 (Use Case Canvas) will omit competitive comparisons. The other sections will generate from product and persona data.
> Run `/octave:library create competitor` to add competitors.

**No Conversation Evidence:**
> No conversation findings available.
>
> The positioning system will be built entirely from library data. As your team logs calls, re-running this skill will surface what resonates and what doesn't — making each iteration sharper.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The positioning system builder needs Octave data to generate useful frameworks. Without it, most sections would be empty.
> To reconnect: check your MCP configuration or run `/octave:workspace status`

## Related Skills

- `/octave:messaging` — Text-based messaging frameworks (this is the visual counterpart)
- `/octave:deck` — Build a presentation from your positioning
- `/octave:campaign` — Generate campaign content grounded in your positioning
- `/octave:launch` — Launch plan using this positioning as the messaging foundation
- `/octave:brief` — Account-specific prep document (positioning is product-level)
- `/octave:battlecard` — Competitive intelligence (feeds into Section 3: Strategy)
- `/octave:enablement` — Sales enablement materials using your positioning
- `/octave:one-pager` — Customer-facing document built from positioning
- `/octave:library` — Update library entities with finalized positioning
