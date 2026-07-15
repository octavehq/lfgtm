# Section Templates Reference

HTML templates for all 8 sections of the Positioning System document. Each template shows the structure, CSS classes, and placeholder content. Populate with real Octave library data.

All templates use the CSS classes defined in the main SKILL.md and extended in [section-layouts.md](section-layouts.md).

---

## Section 1: Message Framework

The foundational framework. Three stacked layers — Market context at the top, Minimum Viable Positioning in the middle, and Value Propositions by persona at the bottom.

```html
<details class="section" open id="section-message-framework">
  <summary>
    <div>
      <p class="section-number">Section 01</p>
      <h2 class="section-title">Message Framework</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">The foundational messaging architecture — from market context through product positioning to persona-specific value propositions.</p>

    <!-- Layer 1: Market -->
    <div class="house-layer house-market">
      <div class="house-layer-label">Market</div>
      <div class="grid-4">
        <div class="house-cell">
          <span class="house-cell-label">Champion</span>
          <p>[Primary champion persona — e.g., "Head of Growth"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Company Type</span>
          <p>[Target segment — e.g., "Series A-C B2B SaaS, $10M+ ARR"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Use Case</span>
          <p>[Primary use case — e.g., "Hyper-personalized outbound at scale"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Problem</span>
          <p>[Core problem — e.g., "Personalization is manual, expensive, and impossible at scale"]</p>
        </div>
      </div>
    </div>

    <!-- Layer 2: Minimum Viable Positioning -->
    <div class="house-layer house-mvp">
      <div class="house-layer-label">Minimum Viable Positioning</div>
      <div class="grid-4">
        <div class="house-cell">
          <span class="house-cell-label">Product Category</span>
          <p>[Category — e.g., "AI Messaging Hub"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Most Compelling Capability</span>
          <p>[Top capability — e.g., "Library-grounded personalization"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Most Compelling Feature</span>
          <p>[Top feature — e.g., "Specialized AI Agents"]</p>
        </div>
        <div class="house-cell">
          <span class="house-cell-label">Main Benefit</span>
          <p>[Primary benefit — e.g., "Close more pipeline while spending less time on personalization"]</p>
        </div>
      </div>
    </div>

    <!-- Layer 3: Value Propositions -->
    <div class="house-layer house-vps">
      <div class="house-layer-label">Value Propositions</div>

      <!-- Column Headers -->
      <div class="vp-grid vp-header">
        <div class="vp-col-label">Champion</div>
        <div class="vp-col-label">What They're Trying To Do</div>
        <div class="vp-col-label">How They Do It Today</div>
        <div class="vp-col-label">Limitation</div>
        <div class="vp-col-label">Moment of Progress</div>
        <div class="vp-col-label">Capability</div>
        <div class="vp-col-label">Product Feature</div>
        <div class="vp-col-label">Benefit</div>
      </div>

      <!-- One row per persona-use-case value prop -->
      <!-- Color-code each row with the persona class -->

      <div class="vp-grid vp-row persona-champion">
        <div class="vp-cell"><span class="persona-dot"></span>[Persona title]</div>
        <div class="vp-cell">[Job to be done]</div>
        <div class="vp-cell">[Current workflow / sub-process]</div>
        <div class="vp-cell">[Why current way falls short]</div>
        <div class="vp-cell">[Trigger / problem moment]</div>
        <div class="vp-cell">[Product capability]</div>
        <div class="vp-cell">[Specific feature]</div>
        <div class="vp-cell">[Promised value / outcome]</div>
      </div>

      <div class="vp-grid vp-row persona-user">
        <div class="vp-cell"><span class="persona-dot"></span>[Persona title]</div>
        <div class="vp-cell">[Job to be done]</div>
        <div class="vp-cell">[Current workflow]</div>
        <div class="vp-cell">[Limitation]</div>
        <div class="vp-cell">[Trigger moment]</div>
        <div class="vp-cell">[Capability]</div>
        <div class="vp-cell">[Feature]</div>
        <div class="vp-cell">[Benefit]</div>
      </div>

      <!-- Repeat for each value prop row (up to 8 rows) -->
      <!-- Use persona-decision, persona-financial, persona-technical as needed -->

    </div>

    <!-- Optional: Opposites / Tension Pairs -->
    <div class="house-opposites" style="margin-top: 1.5rem;">
      <p class="text-secondary" style="font-size: 0.85rem; margin-bottom: 0.75rem;">Tension Pairs — value props that reinforce each other from opposite angles:</p>
      <div class="grid-2">
        <div class="card" style="text-align: center;">
          <p style="font-size: 0.85rem; color: var(--text-secondary);">[VP A]</p>
          <p style="font-size: 0.75rem; color: var(--text-muted);">↔</p>
          <p style="font-size: 0.85rem; color: var(--text-secondary);">[VP B]</p>
        </div>
        <!-- More tension pairs if applicable -->
      </div>
    </div>

  </div>
</details>
```

---

## Section 2: Positioning Anchors

Positioning statements with highlighted keywords. Primary anchor (the core "We are X for Y" statement), secondary anchors (supporting claims), and examples of combining them.

```html
<details class="section" open id="section-positioning-anchors">
  <summary>
    <div>
      <p class="section-number">Section 02</p>
      <h2 class="section-title">Positioning Anchors</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Modular positioning statements you can combine for different audiences, channels, and contexts.</p>

    <!-- Primary Anchor Statements -->
    <div style="margin-bottom: 2rem;">
      <h3 style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Anchor Statements</h3>

      <div class="anchor-statements">
        <!-- Each statement is a styled line with highlighted key terms -->
        <div class="anchor-line">
          <p>[Product] is a <span class="highlight highlight-category">[Category]</span> for <span class="highlight highlight-usecase">[use case]</span></p>
        </div>
        <div class="anchor-line">
          <p>[Product] replaces <span class="highlight highlight-problem">[current alternatives]</span> for <span class="highlight highlight-usecase">[use case]</span></p>
        </div>
        <div class="anchor-line">
          <p>[Product] is for <span class="highlight highlight-persona">[Persona 1]</span> and <span class="highlight highlight-persona">[Persona 2]</span> at <span class="highlight highlight-category">[company type]</span></p>
        </div>
        <div class="anchor-line">
          <p>[Product] grounds your <span class="highlight highlight-usecase">[use case]</span> in <span class="highlight highlight-feature">[key differentiator]</span></p>
        </div>
        <div class="anchor-line">
          <p>[Product] makes <span class="highlight highlight-feature">[key capability]</span> <span class="highlight highlight-usecase">[desirable outcome]</span></p>
        </div>
      </div>
    </div>

    <!-- Primary vs Secondary Anchors -->
    <div class="grid-2" style="margin-bottom: 2rem;">
      <div>
        <h3 style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Primary Anchors</h3>
        <p class="text-secondary" style="font-size: 0.85rem; margin-bottom: 1rem;">These define what you are. Use at least one in every message.</p>
        <div class="card" style="margin-bottom: 0.75rem; border-left: 3px solid var(--brand-primary);">
          <span class="badge badge-primary">Product Category</span>
          <p style="margin-top: 0.5rem;">[Category anchor — defines the mental shelf]</p>
        </div>
        <div class="card" style="margin-bottom: 0.75rem; border-left: 3px solid var(--success);">
          <span class="badge badge-success">Use Case</span>
          <p style="margin-top: 0.5rem;">[Use case anchor — defines the job to be done]</p>
        </div>
        <div class="card" style="border-left: 3px solid var(--warning);">
          <span class="badge badge-warning">Competitive Alternative</span>
          <p style="margin-top: 0.5rem;">[Alternative anchor — defines what you replace]</p>
        </div>
      </div>

      <div>
        <h3 style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Secondary Anchors</h3>
        <p class="text-secondary" style="font-size: 0.85rem; margin-bottom: 1rem;">These add specificity. Stack them to narrow your positioning for a segment.</p>
        <div class="card" style="margin-bottom: 0.75rem;">
          <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #a78bfa;">Company Type</span>
          <p style="margin-top: 0.5rem;">[Firmographic qualifier — e.g., "Series A-C B2B SaaS"]</p>
        </div>
        <div class="card" style="margin-bottom: 0.75rem;">
          <span class="badge" style="background: rgba(236, 72, 153, 0.15); color: #f472b6;">Departmental Buyer</span>
          <p style="margin-top: 0.5rem;">[Persona qualifier — e.g., "Head of Growth"]</p>
        </div>
        <div class="card">
          <span class="badge" style="background: rgba(34, 211, 238, 0.15); color: #22d3ee;">Differentiator</span>
          <p style="margin-top: 0.5rem;">[Proof qualifier — e.g., "grounded in your specific ICP knowledge"]</p>
        </div>
      </div>
    </div>

    <!-- Combining Anchors -->
    <div>
      <h3 style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Combined Positioning Examples</h3>
      <p class="text-secondary" style="font-size: 0.85rem; margin-bottom: 1rem;">Layer primary + secondary anchors to create positioning tailored to different contexts.</p>

      <div class="callout" style="margin-bottom: 1rem;">
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">For broad awareness</p>
        <p style="font-weight: 600;">[Product] is a <span class="highlight highlight-category">[Category]</span> that helps <span class="highlight highlight-persona">[Persona]</span> in <span class="highlight highlight-category">[Company Type]</span> <span class="highlight highlight-usecase">[achieve outcome]</span></p>
      </div>
      <div class="callout" style="margin-bottom: 1rem;">
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">For targeted outreach</p>
        <p style="font-weight: 600;">[Product] is a <span class="highlight highlight-category">[Category]</span> that helps <span class="highlight highlight-persona">[Persona]</span> in <span class="highlight highlight-category">[Company Type]</span> who are trying to <span class="highlight highlight-usecase">[use case]</span> and <span class="highlight highlight-problem">[spending too much time on X]</span></p>
      </div>
      <div class="callout">
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">For competitive displacement</p>
        <p style="font-weight: 600;">[Product] is a <span class="highlight highlight-category">[Category]</span> that helps <span class="highlight highlight-persona">[Persona]</span> in <span class="highlight highlight-category">[Company Type]</span> making <span class="highlight highlight-usecase">[outcome]</span> <span class="highlight highlight-feature">[streamlined/instant/etc.]</span> with <span class="highlight highlight-feature">[key differentiator]</span></p>
      </div>
    </div>

    <!-- Tips -->
    <div class="card" style="margin-top: 1.5rem; border-left: 4px solid var(--warning);">
      <p style="font-weight: 600; margin-bottom: 0.5rem;">Anchor Layering Rules</p>
      <ul style="font-size: 0.85rem; color: var(--text-secondary); padding-left: 1.25rem;">
        <li>Choose the right level of clarity for each context — not every message needs all anchors</li>
        <li>Choosing an anchor is also choosing a market segment</li>
        <li>You can strategically layer anchors to create a more specific ICP</li>
      </ul>
    </div>

  </div>
</details>
```

---

## Section 3: Positioning Strategy

Tactical strategy table — the grid that maps target company, buyer, use case, competitive alternatives, problems, capabilities, and differentiation.

```html
<details class="section" open id="section-positioning-strategy">
  <summary>
    <div>
      <p class="section-number">Section 03</p>
      <h2 class="section-title">Positioning Strategy</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Tactical positioning mapped against competitive alternatives — problems they create, capabilities we unlock, and why that's better.</p>

    <!-- Strategy Summary Row -->
    <div class="callout" style="margin-bottom: 2rem;">
      <p style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Positioning Strategy Summary</p>
      <p class="text-secondary" style="font-size: 0.85rem; margin-bottom: 1rem;">[Product] should anchor its positioning to a <strong>[use case / product category]</strong> because [strategic rationale — e.g., "the category is nascent and not established, making it harder to frame for our ICP"].</p>
      <div class="grid-4" style="gap: 1rem;">
        <div>
          <span class="badge badge-primary">Target Company</span>
          <p style="margin-top: 0.5rem; font-size: 0.85rem;">[e.g., "Series A-C B2B SaaS, $10M+ ARR"]</p>
        </div>
        <div>
          <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #a78bfa;">Target Department</span>
          <p style="margin-top: 0.5rem; font-size: 0.85rem;">[e.g., "Primary: Head of Growth / Secondary: RevOps Lead"]</p>
        </div>
        <div>
          <span class="badge badge-warning">Product Category</span>
          <p style="margin-top: 0.5rem; font-size: 0.85rem;">[e.g., "AI ICP Engine"]</p>
        </div>
        <div>
          <span class="badge badge-success">Primary Use Case</span>
          <p style="margin-top: 0.5rem; font-size: 0.85rem;">[e.g., "Hyper-personalized outbound with specific ICP and product knowledge"]</p>
        </div>
      </div>
    </div>

    <!-- Competitive Comparison Table -->
    <div style="overflow-x: auto;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Competitive Alternative</th>
            <th>Why That Sucks</th>
            <th>Capabilities</th>
            <th>Features</th>
            <th>How We Do It Differently</th>
            <th>Why That's Better</th>
          </tr>
        </thead>
        <tbody>
          <!-- Row per competitive alternative -->
          <tr>
            <td>
              <strong>[Alternative 1 — e.g., "DIY: prompting LLMs"]</strong>
              <p class="text-muted" style="font-size: 0.8rem;">[Brief description]</p>
            </td>
            <td style="color: var(--error); font-size: 0.85rem;">[Why this approach fails — e.g., "Manual, no ICP context, generic output"]</td>
            <td style="font-size: 0.85rem;">[Capability we unlock]</td>
            <td><span class="badge badge-primary">[Feature name]</span></td>
            <td style="font-size: 0.85rem;">[Our differentiated approach]</td>
            <td style="color: var(--success); font-size: 0.85rem;">[Outcome improvement]</td>
          </tr>
          <tr>
            <td>
              <strong>[Alternative 2]</strong>
              <p class="text-muted" style="font-size: 0.8rem;">[Description]</p>
            </td>
            <td style="color: var(--error); font-size: 0.85rem;">[Pain]</td>
            <td style="font-size: 0.85rem;">[Capability]</td>
            <td><span class="badge badge-primary">[Feature]</span></td>
            <td style="font-size: 0.85rem;">[Differentiation]</td>
            <td style="color: var(--success); font-size: 0.85rem;">[Better outcome]</td>
          </tr>
          <!-- Repeat for up to 6 competitive alternatives -->
        </tbody>
      </table>
    </div>

  </div>
</details>
```

---

## Section 4: Persona-Based Messaging

Core product message translated per buying committee member. Two zones: "Focus messaging here" (User + Champion) and "Help your champion translate" (Decision Maker, Financial Buyer, Technical Influencer).

```html
<details class="section" open id="section-persona-messaging">
  <summary>
    <div>
      <p class="section-number">Section 04</p>
      <h2 class="section-title">Persona-Based Messaging</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">How the core product message translates for each member of the buying committee.</p>

    <!-- Messaging Focus Zones -->
    <div class="grid-2" style="margin-bottom: 2rem;">
      <div class="callout" style="border-left-color: var(--success);">
        <p style="font-weight: 700; color: var(--success); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Focus messaging here</p>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">(what the product actually does)</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">User + Champion are closest to the problem. Lead with product truth.</p>
      </div>
      <div class="callout" style="border-left-color: var(--warning);">
        <p style="font-weight: 700; color: var(--warning); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Help your champion translate</p>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">(for the rest of the buying committee)</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">Decision Maker, Financial Buyer, and Technical Influencer need translated value.</p>
      </div>
    </div>

    <!-- Persona Grid -->
    <div class="persona-messaging-grid">
      <!-- Column Headers -->
      <div class="pm-header-row">
        <div class="pm-label"></div>
        <div class="pm-col-header">What They Care About</div>
        <div class="pm-col-header">Relevant Challenge</div>
        <div class="pm-col-header">New Thing They Can Do</div>
        <div class="pm-col-header">Promised Value</div>
      </div>

      <!-- Persona Row: User -->
      <div class="pm-row persona-user" style="border-left: 3px solid #34d399;">
        <div class="pm-label">
          <span class="persona-dot"></span>
          <div>
            <p style="font-weight: 600;">User</p>
            <p class="text-muted" style="font-size: 0.8rem;">[Title — e.g., "RevOps Lead"]</p>
          </div>
        </div>
        <div class="pm-cell card">[Workflow they care about — e.g., "Trying to personalize email at scale"]</div>
        <div class="pm-cell card" style="border-color: var(--error);">[Their specific problem — e.g., "Personalization is generic and lacks context"]</div>
        <div class="pm-cell card" style="border-color: var(--brand-primary);">[New capability — e.g., "Auto-personalize with specific ICP knowledge"]</div>
        <div class="pm-cell card" style="border-color: var(--success);">[Benefit — e.g., "Close more pipeline with less manual work"]</div>
      </div>

      <!-- Persona Row: Champion -->
      <div class="pm-row persona-champion" style="border-left: 3px solid #60a5fa;">
        <div class="pm-label">
          <span class="persona-dot"></span>
          <div>
            <p style="font-weight: 600;">Champion</p>
            <p class="text-muted" style="font-size: 0.8rem;">[Title — e.g., "Head of Growth"]</p>
          </div>
        </div>
        <div class="pm-cell card">[Care about]</div>
        <div class="pm-cell card" style="border-color: var(--error);">[Challenge]</div>
        <div class="pm-cell card" style="border-color: var(--brand-primary);">[New capability]</div>
        <div class="pm-cell card" style="border-color: var(--success);">[Promised value]</div>
      </div>

      <!-- Divider between focus zones -->
      <div class="pm-divider">
        <span class="text-muted" style="font-size: 0.75rem;">↓ Champion translates for these roles ↓</span>
      </div>

      <!-- Persona Row: Decision Maker -->
      <div class="pm-row persona-decision" style="border-left: 3px solid #f59e0b;">
        <div class="pm-label">
          <span class="persona-dot"></span>
          <div>
            <p style="font-weight: 600;">Decision Maker</p>
            <p class="text-muted" style="font-size: 0.8rem;">[Title — e.g., "CMO/CRO"]</p>
          </div>
        </div>
        <div class="pm-cell card">[Care about]</div>
        <div class="pm-cell card" style="border-color: var(--error);">[Challenge]</div>
        <div class="pm-cell card" style="border-color: var(--brand-primary);">[New capability]</div>
        <div class="pm-cell card" style="border-color: var(--success);">[Promised value]</div>
      </div>

      <!-- Persona Row: Financial Buyer -->
      <div class="pm-row persona-financial" style="border-left: 3px solid #f87171;">
        <div class="pm-label">
          <span class="persona-dot"></span>
          <div>
            <p style="font-weight: 600;">Financial Buyer</p>
            <p class="text-muted" style="font-size: 0.8rem;">[Title — e.g., "CFO"]</p>
          </div>
        </div>
        <div class="pm-cell card">[Care about]</div>
        <div class="pm-cell card" style="border-color: var(--error);">[Challenge]</div>
        <div class="pm-cell card" style="border-color: var(--brand-primary);">[New capability]</div>
        <div class="pm-cell card" style="border-color: var(--success);">[Promised value]</div>
      </div>

      <!-- Persona Row: Technical Influencer -->
      <div class="pm-row persona-technical" style="border-left: 3px solid #a78bfa;">
        <div class="pm-label">
          <span class="persona-dot"></span>
          <div>
            <p style="font-weight: 600;">Technical Influencer</p>
            <p class="text-muted" style="font-size: 0.8rem;">[Title — e.g., "RevOps Lead"]</p>
          </div>
        </div>
        <div class="pm-cell card">[Care about]</div>
        <div class="pm-cell card" style="border-color: var(--error);">[Challenge]</div>
        <div class="pm-cell card" style="border-color: var(--brand-primary);">[New capability]</div>
        <div class="pm-cell card" style="border-color: var(--success);">[Promised value]</div>
      </div>
    </div>

  </div>
</details>
```

---

## Section 5: Value Prop by Awareness Stage

Four-column funnel showing how messaging shifts as buyer awareness increases. Split into "Creating Demand" (left) and "Capturing Demand" (right).

```html
<details class="section" open id="section-awareness-funnel">
  <summary>
    <div>
      <p class="section-number">Section 05</p>
      <h2 class="section-title">Value Prop by Awareness Stage</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">How your messaging shifts as prospects move from unaware to product-aware — what to lead with, how to earn trust, and how to convince.</p>

    <!-- Demand Type Labels -->
    <div class="grid-2" style="margin-bottom: 0.5rem;">
      <div style="text-align: center;">
        <span class="badge" style="background: rgba(248, 113, 113, 0.15); color: var(--error); font-size: 0.75rem;">Creating Demand</span>
      </div>
      <div style="text-align: center;">
        <span class="badge" style="background: rgba(52, 211, 153, 0.15); color: var(--success); font-size: 0.75rem;">Capturing Demand</span>
      </div>
    </div>

    <!-- 4-Column Funnel Grid -->
    <div class="funnel-grid">
      <!-- Column Headers -->
      <div class="funnel-header funnel-stage-1">
        <p class="funnel-stage-label">Problem Unaware</p>
      </div>
      <div class="funnel-header funnel-stage-2">
        <p class="funnel-stage-label">Problem Aware</p>
      </div>
      <div class="funnel-header funnel-stage-3">
        <p class="funnel-stage-label">Solution Aware</p>
      </div>
      <div class="funnel-header funnel-stage-4">
        <p class="funnel-stage-label">Product Aware</p>
      </div>

      <!-- Row: Lead With... -->
      <div class="funnel-row-label">Lead with...</div>
      <div class="funnel-cell card funnel-stage-1">
        <span class="badge badge-warning">Alternative</span>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">[Lead with the familiar alternative they're already using — e.g., "Stitching together docs, LLM prompts, Clay, and SEPs"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-2">
        <span class="badge badge-error">Problem</span>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">[Lead with the problem they recognize — e.g., "Personalization is cumbersome and doesn't scale"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-3">
        <span class="badge badge-primary">Capability</span>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">[Lead with the capability they want — e.g., "Create hyper-personalized outbound sequences and turn them into Clay"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-4">
        <span class="badge badge-success">Feature</span>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">[Lead with the product feature — e.g., "Octave Messaging Library and Sequence Agents"]</p>
      </div>

      <!-- Row: Earn Trust By... -->
      <div class="funnel-row-label">Earn trust by...</div>
      <div class="funnel-cell card funnel-stage-1">
        <p style="font-size: 0.85rem;">[e.g., "Showing you understand their situation"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-2">
        <p style="font-size: 0.85rem;">[e.g., "Showing you understand their problem"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-3">
        <p style="font-size: 0.85rem;">[e.g., "Showing you understand their desired capability"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-4">
        <p style="font-size: 0.85rem;">[e.g., "Connecting their desired features to an outcome"]</p>
      </div>

      <!-- Row: To Convince Them... -->
      <div class="funnel-row-label">To convince them...</div>
      <div class="funnel-cell card funnel-stage-1" style="border-color: var(--warning);">
        <p style="font-size: 0.85rem; font-weight: 600;">[e.g., "They have a problem"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-2" style="border-color: var(--error);">
        <p style="font-size: 0.85rem; font-weight: 600;">[e.g., "They are missing a key capability"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-3" style="border-color: var(--brand-primary);">
        <p style="font-size: 0.85rem; font-weight: 600;">[e.g., "Your feature unlocks the capability"]</p>
      </div>
      <div class="funnel-cell card funnel-stage-4" style="border-color: var(--success);">
        <p style="font-size: 0.85rem; font-weight: 600;">[e.g., "Your solution delivers on its benefit"]</p>
      </div>
    </div>

  </div>
</details>
```

---

## Section 6: Use Case Messaging Canvas

"The Current Way" vs "The New Way" — a split-view comparison for each use case. Shows the overarching problem, moment of progress, limitations, and how the product creates a better path.

```html
<details class="section" open id="section-use-case-canvas">
  <summary>
    <div>
      <p class="section-number">Section 06</p>
      <h2 class="section-title">Use Case Messaging Canvas</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">For each use case: the current way prospects solve the problem vs. the new way your product enables — with the overarching problem, moment of progress, and desired outcome.</p>

    <!-- Repeat this block for each use case -->
    <div class="use-case-block" style="margin-bottom: 2.5rem;">
      <div class="callout" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
          <div>
            <span class="badge badge-primary">Use Case</span>
            <p style="font-weight: 600; font-size: 1.1rem; margin-top: 0.25rem;">[Use case name — e.g., "Hyper-personalized outbound sales"]</p>
          </div>
          <div>
            <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #a78bfa;">Target Customer</span>
            <p style="font-size: 0.85rem; margin-top: 0.25rem;">[Primary persona for this use case]</p>
          </div>
        </div>
      </div>

      <!-- Split Canvas -->
      <div class="canvas-split">
        <!-- The Current Way -->
        <div class="canvas-current">
          <div class="canvas-label canvas-label-current">The Current Way</div>

          <div class="canvas-flow">
            <div class="canvas-cell canvas-problem">
              <span class="canvas-cell-label">Overarching Problem</span>
              <p>[Big picture struggle — e.g., "Missing opportunities and spending too much time on manual personalization"]</p>
            </div>
            <div class="canvas-arrow">→</div>
            <div class="canvas-cell">
              <span class="canvas-cell-label">Moment of Progress</span>
              <p>[Trigger — e.g., "Team realizes outbound response rates are dropping"]</p>
            </div>
            <div class="canvas-arrow">→</div>
            <div class="canvas-cell">
              <span class="canvas-cell-label">Current Approach</span>
              <p>[What they do today — e.g., "Manually research, prompt LLMs, stitch tools together"]</p>
            </div>
            <div class="canvas-arrow">→</div>
            <div class="canvas-cell canvas-limitation">
              <span class="canvas-cell-label">Limitation</span>
              <p>[Why it falls short — e.g., "Generic output, no ICP context, time-consuming"]</p>
            </div>
          </div>
        </div>

        <!-- The New Way -->
        <div class="canvas-new">
          <div class="canvas-label canvas-label-new">The New Way</div>

          <div class="canvas-flow">
            <div class="canvas-cell canvas-capability">
              <span class="canvas-cell-label">New Capability</span>
              <p>[What becomes possible — e.g., "Auto-generate hyper-personalized sequences grounded in your ICP"]</p>
            </div>
            <div class="canvas-arrow">→</div>
            <div class="canvas-cell">
              <span class="canvas-cell-label">Product Feature</span>
              <span class="badge badge-primary" style="margin-bottom: 0.25rem;">[Feature name]</span>
              <p>[Brief description]</p>
            </div>
            <div class="canvas-arrow">→</div>
            <div class="canvas-cell canvas-outcome">
              <span class="canvas-cell-label">Desired Outcome</span>
              <p>[End state — e.g., "Close more pipeline while spending less time on personalization workflows"]</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Repeat for additional use cases -->

  </div>
</details>
```

---

## Section 7: Use Case Lifecycle

Horizontal customer journey showing phases, activities, stakeholders, and touchpoints for each use case.

```html
<details class="section" open id="section-lifecycle">
  <summary>
    <div>
      <p class="section-number">Section 07</p>
      <h2 class="section-title">Use Case Lifecycle</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">The full customer journey for each use case — from documentation through prospecting, outreach, and closing — with the tools, stakeholders, and messaging at each phase.</p>

    <!-- Repeat for each use case -->
    <div class="lifecycle-block" style="margin-bottom: 2.5rem;">
      <div class="callout" style="margin-bottom: 1.5rem;">
        <span class="badge badge-primary">Use Case</span>
        <p style="font-weight: 600; margin-top: 0.25rem;">[Use case name]</p>
      </div>

      <!-- Horizontal Phase Timeline -->
      <div class="timeline-phases">
        <!-- Each phase is a column -->
        <div class="phase">
          <div class="phase-header">
            <span class="phase-number">1</span>
            <p class="phase-title">[Phase name — e.g., "Document ICP"]</p>
          </div>
          <div class="phase-body">
            <p class="phase-activity">[What happens — e.g., "Build messaging & positioning library"]</p>
            <div class="phase-tools">
              <span class="badge badge-primary" style="font-size: 0.65rem;">[Tool/Feature]</span>
            </div>
            <div class="phase-stakeholders">
              <span class="persona-dot" style="background: #60a5fa;" title="Champion"></span>
              <span class="persona-dot" style="background: #34d399;" title="User"></span>
            </div>
          </div>
        </div>

        <div class="phase">
          <div class="phase-header">
            <span class="phase-number">2</span>
            <p class="phase-title">[Phase 2 — e.g., "Build prospect lists"]</p>
          </div>
          <div class="phase-body">
            <p class="phase-activity">[Activity]</p>
            <div class="phase-tools">
              <span class="badge badge-primary" style="font-size: 0.65rem;">[Tool]</span>
            </div>
            <div class="phase-stakeholders">
              <span class="persona-dot" style="background: #34d399;"></span>
            </div>
          </div>
        </div>

        <!-- Continue for 6-8 phases -->
        <!-- Phase 3: Enrich & qualify -->
        <!-- Phase 4: Build campaigns -->
        <!-- Phase 5: Execute outreach -->
        <!-- Phase 6: Meet & close -->
        <!-- Phase 7: Track outcomes -->

      </div>
    </div>

    <!-- Repeat for additional use cases -->

  </div>
</details>
```

---

## Section 8: Homepage Messaging

Website implementation guide — what goes on the homepage (primary) vs. what goes on secondary pages (expanded). Uses the "We are a..." / "That helps..." / "Dealing with..." / "Solved by..." template.

```html
<details class="section" open id="section-homepage">
  <summary>
    <div>
      <p class="section-number">Section 08</p>
      <h2 class="section-title">Homepage Messaging</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Be specific with your most compelling use case & target customer. What belongs on the homepage vs. other pages.</p>

    <div class="grid-2" style="gap: 2rem;">

      <!-- Primary: Homepage Focus -->
      <div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
          <span class="badge badge-success">Homepage</span>
          <span class="text-muted" style="font-size: 0.8rem;">This should be the ONLY focus on the homepage</span>
        </div>

        <div class="homepage-template">
          <div class="homepage-row">
            <span class="homepage-label">We are a...</span>
            <div class="card">
              <span class="badge highlight-category" style="margin-bottom: 0.25rem;">Product Category</span>
              <p style="font-weight: 600;">[Category — e.g., "AI Messaging Hub"]</p>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">That helps...</span>
            <div class="card">
              <span class="badge highlight-persona" style="margin-bottom: 0.25rem;">Target Customer</span>
              <p style="font-weight: 600;">[Primary persona — e.g., "Heads of Growth"]</p>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">Dealing with...</span>
            <div class="card">
              <span class="badge highlight-problem" style="margin-bottom: 0.25rem;">Problem</span>
              <p style="font-weight: 600;">[Core problem — e.g., "Generic, undifferentiated messaging at scale"]</p>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">Solved by...</span>
            <div class="card">
              <span class="badge highlight-feature" style="margin-bottom: 0.25rem;">Capability & Feature</span>
              <p style="font-weight: 600;">[Solution — e.g., "Your ICP and messaging library powering specialized AI agents"]</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Secondary: Expanded Messaging -->
      <div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
          <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #a78bfa;">Other Pages</span>
          <span class="text-muted" style="font-size: 0.8rem;">Save extras for additional pages & in-app messaging</span>
        </div>

        <div class="homepage-template">
          <div class="homepage-row">
            <span class="homepage-label">We are...</span>
            <div class="card">
              <span class="badge highlight-category" style="margin-bottom: 0.25rem;">Product Category</span>
              <p style="font-weight: 600;">[Broader category — e.g., "More than just an account research and personalization tool"]</p>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">We also help...</span>
            <div class="card">
              <!-- Multiple target customer badges -->
              <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span class="badge highlight-persona">[Persona 2]</span>
                <span class="badge highlight-persona">[Persona 3]</span>
                <span class="badge highlight-persona">[Persona 4]</span>
                <span class="badge highlight-persona">[Persona 5]</span>
              </div>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">Dealing with...</span>
            <div class="card">
              <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span class="badge highlight-problem">[Problem 2]</span>
                <span class="badge highlight-problem">[Problem 3]</span>
                <span class="badge highlight-problem">[Problem 4]</span>
              </div>
            </div>
          </div>
          <div class="homepage-row">
            <span class="homepage-label">Solved by...</span>
            <div class="card">
              <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span class="badge highlight-feature">[Capability 2]</span>
                <span class="badge highlight-feature">[Capability 3]</span>
                <span class="badge highlight-feature">[Capability 4]</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</details>
```
