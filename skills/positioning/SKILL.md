---
name: positioning
description: "Generate a complete Messaging & Positioning system as a stunning visual HTML document — message framework, positioning anchors, strategy table, persona-based messaging, awareness funnel, use case canvases, lifecycle mapping, and homepage messaging. Use when user says 'positioning system', 'positioning exercise', 'message framework', 'positioning anchors', 'positioning document', 'visual messaging framework', or asks for a comprehensive positioning deliverable."
---

# /octave:positioning - Visual Messaging & Positioning System

Generate a complete, visual Messaging & Positioning system rendered as a single stunning HTML document — eight interconnected frameworks all pulled from your Octave library and grounded in real conversation evidence. Renders as a polished, scrollable HTML document with visual grids, color-coded persona columns, funnel diagrams, timelines, and split-view canvases.

## Usage

```
/octave:positioning [section] [--product <name>] [--style <preset>]
```

| Section arg | Framework |
|-------------|-----------|
| *(none)* | Full 8-section exercise (default) |
| `message-framework` | Message Framework pyramid |
| `anchors` | Positioning Anchors |
| `strategy` | Positioning Strategy table |
| `personas` | Persona-Based Messaging |
| `awareness` | Value Prop by Awareness Stage |
| `use-cases` | Use Case Messaging Canvas |
| `lifecycle` | Use Case Lifecycle |
| `homepage` | Homepage Messaging |

## Instructions

When the user runs `/octave:positioning`:

### Step 1: Understand the Context

If no section specified, confirm full exercise and ask which product to focus on (list products from library, or "entire company / all products", or "specific use case or segment"). If a specific section was requested, confirm and proceed directly.

### Step 2: Octave Context Gathering

Gather all library intelligence in a single pass. **Tell the user what you're researching and why.** All 8 sections share the same data pool — gather once, render many.

```
# Core entities
list_all_entities({ entityType: "product" })         # Products to position
list_all_entities({ entityType: "persona" })          # Buying committee roles
list_all_entities({ entityType: "use_case" })         # Use cases for canvases
list_all_entities({ entityType: "competitor" })        # Competitive alternatives
list_all_entities({ entityType: "segment" })           # Target segments

# Deep dives
get_entity({ entityType: "product", oId: "<oId>" })   # Full product details
get_playbook({ oId: "<playbook_oId>" })                # Messaging & value props
list_value_props({ playbookOId: "<oId>" })             # Persona-specific value props

# Evidence & intelligence
list_findings({ days: 90 })                            # What resonates / falls flat
search_knowledge_base({ query: "competitive positioning" })
list_brand_voices()                                    # Brand tone for homepage section
```

For the full entity-to-section mapping, see [data-gathering-matrix.md](references/data-gathering-matrix.md).

**Output of this step:** Present a data summary listing: product, category, segments, personas, use cases, competitors, playbooks, proof points, and conversation evidence counts. Then list the 8 sections to generate with key data points for each. Ask user to approve, add/remove sections, or go deeper before proceeding.

### Step 3: Style Selection

If `--style` was not provided, present the style menu from [style-selection.md](references/style-selection.md). Default is `midnight-pro`.

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

All HTML structure, base CSS, and JavaScript are defined in the references:
- [html-architecture.md](references/html-architecture.md) — Base CSS classes, HTML skeleton, sidebar JS
- [section-templates.md](references/section-templates.md) — HTML templates for all 8 section types
- [section-layouts.md](references/section-layouts.md) — Section-specific CSS patterns (grids, funnels, timelines, canvases)

#### Content Population

For each section, use `generate_content` to synthesize library data, then render into the HTML templates from [section-templates.md](references/section-templates.md):

```
generate_content({
  instructions: "Generate the Message Framework pyramid. Three layers:
    1. Market Message: [champion] + [company type] + [use case] + [problem]
    2. Product Message: [category] + [capability] + [feature] + [benefit]
    3. Value Props: one row per persona-use case combination.
    Ground everything in the library data provided. Do not invent data.",
  customContext: "<product entities, persona entities, playbook value props>"
})
```

Example HTML output for a Message Framework section:

```html
<section id="message-framework" class="framework-section">
  <div class="section-header">
    <span class="section-number">01</span>
    <h2>Message Framework</h2>
    <p class="subtitle">The pyramid that connects market need to product value</p>
  </div>
  <div class="pyramid-grid">
    <div class="pyramid-layer market">
      <h3>Market Message</h3>
      <p>Revenue leaders at B2B SaaS companies struggle to align
         GTM teams around consistent messaging across channels.</p>
    </div>
    <!-- product layer + value prop rows follow same pattern -->
  </div>
</section>
```

Apply this pattern to all 8 sections using the layouts from [section-layouts.md](references/section-layouts.md).

#### Content Density Guidelines

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

### Step 5: Delivery

Open the document in the default browser. Present: file path, style, product, sections generated, data source counts, and navigation tips (scroll, sidebar dots, collapsible sections, Cmd+P for PDF).

Offer follow-up actions: adjust/expand a section, go deeper on a framework, generate campaign content (`/octave:campaign`), create a sales deck (`/octave:deck`), save positioning back to library, change style, or export PDF.

**Save back to library** (if requested):

```
update_entity({
  entityType: "product", oId: "<product_oId>",
  instructions: "Update positioning to: [primary anchor]. Category: [category]."
})
add_value_props({
  playbookOId: "<playbook_oId>",
  instructions: "<persona-specific value props from message framework>",
  numValuesPerPersona: 3
})
```

## Error Handling

| Scenario | Response |
|----------|----------|
| No products | Require at least one product; suggest `/octave:library create product` |
| No personas | Generate basic system; persona sections limited; suggest creating personas |
| No use cases | Skip Sections 6-7; generate remaining 6 sections |
| No playbooks/value props | Use product-level info only; suggest creating a playbook |
| No competitors | Omit competitive comparisons in Sections 3 and 6 |
| No conversation evidence | Build from library data only; suggest re-running after logging calls |
| Octave connection failed | Cannot proceed without Octave data; check MCP config |
