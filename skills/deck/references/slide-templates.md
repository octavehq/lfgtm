# Slide Type Templates

Use these templates for each slide type in the outline. Mix types for visual variety.

> **Fixed-canvas authoring.** Every `<section class="slide">` lives inside `.deck-stage` and is authored at **1920×1080** (see [html-scaffold.md](html-scaffold.md)). Size content in **px against that canvas**, never `clamp()`/`vw`/`vh`. The semantic classes below (`heading-1`, `body-text`, `slide-inner`, etc.) are defined in the scaffold at authored px sizes. The **first slide** must carry `class="slide slide-title active visible"` so it shows and animates on load; all other slides are just `class="slide"` and become visible as the controller navigates.

> **Emphasis slides need a distinct surface.** Title, section divider, and CTA/closing slides should look visually different from content slides — they signal chapter breaks and anchor points in the narrative. Use gradient orbs (`.glow-orb` from the scaffold), subtle background color shifts, or accent lines to separate them from the flat content slide surface. If every slide in the deck has the same background treatment, the presentation feels monotone regardless of the content. Example glow technique for a title slide:
> ```css
> /* Add as a child of the slide, positioned with inline styles */
> <div class="glow-orb" style="width:800px; height:800px; top:-200px; right:-200px;"></div>
> <div class="glow-orb" style="width:500px; height:500px; bottom:-150px; left:-100px; background:var(--secondary);"></div>
> ```
>
> **Cards must have depth.** Every `.card` and `.metric-card` uses `box-shadow` from the scaffold to lift off the slide background. A card with only a faint border on the same-colored background doesn't register as a distinct container. Shadows create the physical separation.

**Title Slide (first slide — note `active visible`):**

> **Pill tags are optional.** Only include the `<span class="pill">` if the category or context genuinely helps orient the viewer (e.g., a product name or audience the viewer doesn't already know). Don't pill information the audience already has (the event name, the date, "Q2 Update"). If the context matters, make it the subtitle. If it doesn't, cut it.

> **Subtitles describe the content directly.** State what the deck covers: "Patterns from 12 paying accounts and where the opportunity is." Don't use dramatic rhetorical framing: "What separates the winners from the losers" or "The one thing every team gets wrong." The audience wants to know what they're about to see, not to be teased.

```html
<section class="slide slide-title active visible" data-slide="0">
  <div class="slide-inner flex-center flex-col">
    <!-- pill is optional — only when the tag genuinely orients -->
    <h1 class="heading-1 animate-in">[Main Title]</h1>
    <p class="body-lg text-secondary animate-in">[Subtitle — describes what the deck covers]</p>
  </div>
</section>
```

**Content Slide (bullets):**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Section Title]</h2>
    <div class="feature-list mt-md">
      <div class="animate-in">[Point 1]</div>
      <div class="animate-in">[Point 2]</div>
      <div class="animate-in">[Point 3]</div>
    </div>
  </div>
</section>
```

**Grid/Card Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Section Title]</h2>
    <div class="grid-3 mt-md">
      <div class="card animate-in">[Card 1]</div>
      <div class="card animate-in">[Card 2]</div>
      <div class="card animate-in">[Card 3]</div>
    </div>
  </div>
</section>
```

**Metric Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Section Title]</h2>
    <div class="grid-3 mt-md">
      <div class="metric-card animate-in">
        <span class="big-number">[Value]</span>
        <span class="body-text text-secondary">[Label]</span>
      </div>
      <!-- Repeat -->
    </div>
  </div>
</section>
```

**Quote Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner flex-center flex-col">
    <blockquote class="heading-2 animate-in" style="font-style: italic; max-width: 800px;">
      "[Quote text — 3 lines max]"
    </blockquote>
    <cite class="body-text text-secondary animate-in mt-sm">— [Attribution]</cite>
  </div>
</section>
```

**Comparison Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Comparison Title]</h2>
    <div class="grid-2 mt-md">
      <div class="card animate-in">
        <h3 class="heading-3">[Option A]</h3>
        <!-- Points -->
      </div>
      <div class="card card-brand animate-in">
        <h3 class="heading-3">[Option B — highlighted]</h3>
        <!-- Points -->
      </div>
    </div>
  </div>
</section>
```

**Section Divider Slide:**
```html
<section class="slide slide-divider" data-slide="N">
  <div class="slide-inner flex-center flex-col">
    <span class="pill animate-in">[Section Number / Label]</span>
    <h1 class="heading-1 animate-in">[Section Title]</h1>
    <p class="body-lg text-secondary animate-in">[Brief context — one line]</p>
  </div>
</section>
```

**Section Navigation (on every slide within a section):**

> **Section nav signals where the viewer is.** When a deck has numbered or color-coded sections, every slide within a section should display a consistent section nav element: the section number and label in the section's color. The nav should be large enough to scan at projection distance (number at heading scale, label in uppercase with generous letter-spacing) but visually subordinate to the slide's headline.

```html
<!-- Place at the top of every slide's inner content -->
<div class="section-nav animate-in">
  <span class="section-num" style="color: var(--section-color);">[01]</span>
  <span class="section-label" style="color: var(--section-color);">[Section Name]</span>
</div>
```

**Deck-Level Section Nav (persistent top bar):**

> **Top nav shows deck-level position.** When a deck has two or more major sections (e.g., "Customer Stories" + "Opportunity"), a thin persistent bar at the top of every slide shows all section labels with the current section highlighted. This gives the viewer a map of the full presentation and their position in it.

```html
<!-- Place at absolute top of every slide (except title/closing) -->
<div style="position:absolute; top:0; left:0; right:0; height:52px; display:flex; align-items:center; padding:0 120px; gap:48px; border-bottom:1px solid var(--border);">
  <div class="active">[A] [Section Name]</div>
  <div>[B] [Section Name]</div>
</div>
```

**Deep Dive Slide (entity-level detail — bullet format):**

> **Entity name as focal heading, claim as subtitle.** When a deep-dive slide focuses on a specific entity (company, product, account), the entity name IS the visual focal point — large, bold, the first thing the eye lands on. The action-title claim lives as a colored subtitle directly below. This makes entity identification immediate while still delivering the insight.

> **Bullet format over prose.** Deep-dive slides use scannable bullet lists, not prose paragraphs or two-column sidebar layouts. Bullets can be processed in 5 seconds at projection speed. Use the `.bullet-list` / `.bullet-item` components from the scaffold with colored dots matching the section color.

> **Fixed-position nav and consistent template.** The section nav (number + label) appears at the same absolute position on every slide within a section. Every deep-dive slide in a section uses the same layout template — same `.slide-body`, same content structure. The viewer recognizes the pattern and focuses on content differences, not layout changes.

> **Three font sizes only.** Entity name, subtitle, and bullet text. That's it. No sidebar headings, no stat callouts, no caption text competing for attention.

```html
<section class="slide" data-slide="N">
  <!-- Section identity bar -->
  <div class="section-bar" style="background:var(--section-color);"></div>
  <!-- Deck-level nav (if deck has 2+ sections) -->
  <div class="deck-nav">
    <div class="active">[A] [Current Section]</div>
    <div>[B] [Other Section]</div>
  </div>
  <!-- Section nav -->
  <div class="section-nav">
    <span class="section-num" style="color:var(--section-color);">[01]</span>
    <span class="section-label" style="color:var(--section-color);">[Section Name]</span>
  </div>
  <!-- Content -->
  <div class="slide-body">
    <div>
      <h2 class="entity-name">[Entity Name]</h2>
      <p class="entity-subtitle" style="color:var(--section-color);">[Why they're X]</p>
    </div>
    <div class="bullet-list">
      <div class="bullet-item" style="--dot:var(--section-color);">[Key point 1]</div>
      <div class="bullet-item" style="--dot:var(--section-color);">[Key point 2]</div>
      <div class="bullet-item" style="--dot:var(--section-color);">[Key point 3]</div>
      <div class="bullet-item" style="--dot:var(--section-color);">[Key point 4]</div>
    </div>
  </div>
</section>
```

> **Dot color override.** Bullet dots default to `var(--brand-primary)` via the scaffold CSS. Override per-section by setting `style="--dot:var(--section-color);"` on each `.bullet-item`, or redefine `.bullet-item::before { background: var(--section-color); }` in the deck's custom CSS.

**Overview Cards Slide (section summary):**

> **Overview cards introduce a section's entities.** When a section contains multiple deep-dive slides (e.g., 3 customer archetypes, 4 product lines), an overview slide presents all entities as a grid of summary cards. Each card has a name and 1-2 sentence description. This orients the viewer before the deep dives begin.

> **Cards fill the canvas.** Use `.slide-body` with `justify-content:center` and generous card padding (48px) so the grid occupies the visual center. No empty voids below the cards.

```html
<section class="slide" data-slide="N">
  <div class="section-bar" style="background:var(--section-color);"></div>
  <div class="deck-nav">
    <div class="active">[A] [Current Section]</div>
    <div>[B] [Other Section]</div>
  </div>
  <div class="section-nav">
    <span class="section-num" style="color:var(--section-color);">[01]</span>
    <span class="section-label" style="color:var(--section-color);">[Section Name]</span>
  </div>
  <div class="slide-body">
    <h2 class="heading-2">[Section overview headline]</h2>
    <div class="grid-3 gap-lg">
      <div class="card" style="border-top:4px solid [entity-color];">
        <h3 class="heading-3" style="color:[entity-color];">[Entity Name]</h3>
        <p class="body-text text-secondary mt-sm">[1-2 sentence summary]</p>
      </div>
      <div class="card" style="border-top:4px solid [entity-color];">
        <h3 class="heading-3" style="color:[entity-color];">[Entity Name]</h3>
        <p class="body-text text-secondary mt-sm">[1-2 sentence summary]</p>
      </div>
      <div class="card" style="border-top:4px solid [entity-color];">
        <h3 class="heading-3" style="color:[entity-color];">[Entity Name]</h3>
        <p class="body-text text-secondary mt-sm">[1-2 sentence summary]</p>
      </div>
    </div>
  </div>
</section>
```

**Staircase / Maturity Model Slide:**

> **Visual hierarchy IS the argument.** A staircase or maturity model uses progressively taller bars to show tiers (bad → good, basic → advanced). The visual shape communicates the ranking before the viewer reads any text. Keep each tier to one name — no subtitle + description + count stacked inside.

> **Ghost numbers for sequence.** Large, semi-transparent numbers (01, 02, 03) anchor each tier. The tier name sits next to the number in bold. Everything else (descriptions, account lists) belongs on the overview or deep-dive slides that follow.

```html
<section class="slide" data-slide="N">
  <div class="slide-body" style="justify-content:flex-end;">
    <h2 class="heading-2">[Staircase Title]</h2>
    <div style="display:flex; align-items:flex-end; gap:24px; flex:1; padding-bottom:40px;">
      <!-- Shortest tier (worst/lowest) -->
      <div style="flex:1; height:35%; border-radius:16px 16px 0 0; background:linear-gradient(180deg, [color-a] 0%, transparent 100%); padding:36px 28px; display:flex; flex-direction:column; justify-content:flex-end;">
        <span style="font-size:72px; font-weight:200; opacity:0.3; color:[color-a];">01</span>
        <span style="font-size:36px; font-weight:700;">[Tier Name]</span>
      </div>
      <!-- Middle tier -->
      <div style="flex:1; height:55%; border-radius:16px 16px 0 0; background:linear-gradient(180deg, [color-b] 0%, transparent 100%); padding:36px 28px; display:flex; flex-direction:column; justify-content:flex-end;">
        <span style="font-size:72px; font-weight:200; opacity:0.3; color:[color-b];">02</span>
        <span style="font-size:36px; font-weight:700;">[Tier Name]</span>
      </div>
      <!-- Tallest tier (best/highest) -->
      <div style="flex:1; height:80%; border-radius:16px 16px 0 0; background:linear-gradient(180deg, [color-c] 0%, transparent 100%); padding:36px 28px; display:flex; flex-direction:column; justify-content:flex-end;">
        <span style="font-size:72px; font-weight:200; opacity:0.3; color:[color-c];">03</span>
        <span style="font-size:36px; font-weight:700;">[Tier Name]</span>
      </div>
    </div>
  </div>
</section>
```

**Timeline / Process Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Process Title]</h2>
    <div class="timeline mt-md">
      <div class="timeline-step animate-in">
        <span class="step-number">1</span>
        <div>
          <h3 class="heading-3">[Step Name]</h3>
          <p class="body-text text-secondary">[Brief description]</p>
        </div>
      </div>
      <div class="timeline-step animate-in">
        <span class="step-number">2</span>
        <div>
          <h3 class="heading-3">[Step Name]</h3>
          <p class="body-text text-secondary">[Brief description]</p>
        </div>
      </div>
      <!-- Up to 4-6 steps -->
    </div>
  </div>
</section>
```

**Logo Wall Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner flex-center flex-col">
    <h2 class="heading-2 animate-in">[e.g., Trusted by Industry Leaders]</h2>
    <div class="logo-grid mt-md animate-in">
      <!-- 8-12 logos, using img tags or styled text fallbacks -->
      <div class="logo-item"><img src="[logo-url]" alt="[Company]" /></div>
      <div class="logo-item"><img src="[logo-url]" alt="[Company]" /></div>
      <!-- Repeat -->
    </div>
    <p class="body-text text-secondary animate-in mt-sm">[Optional supporting stat, e.g., "500+ companies worldwide"]</p>
  </div>
</section>
```

**Image Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">[Image Title]</h2>
    <div class="image-container mt-md animate-in">
      <img src="[image-url-or-path]" alt="[Description]" style="max-width: 100%; max-height: 720px; object-fit: contain;" />
    </div>
    <p class="body-text text-secondary animate-in mt-sm">[Caption or context]</p>
  </div>
</section>
```

**Agenda / TOC Slide:**
```html
<section class="slide" data-slide="N">
  <div class="slide-inner">
    <h2 class="heading-2 animate-in">Agenda</h2>
    <div class="agenda-list mt-md">
      <div class="agenda-item animate-in">
        <span class="agenda-number">01</span>
        <span class="body-text">[Topic Name]</span>
      </div>
      <div class="agenda-item animate-in">
        <span class="agenda-number">02</span>
        <span class="body-text">[Topic Name]</span>
      </div>
      <!-- Up to 5-8 items -->
    </div>
  </div>
</section>
```

**CTA / Closing Slide:**
```html
<section class="slide slide-cta" data-slide="N">
  <div class="slide-inner flex-center flex-col">
    <h1 class="heading-1 animate-in">[Call to Action Headline]</h1>
    <p class="body-lg text-secondary animate-in">[Supporting line — one sentence]</p>
    <div class="cta-button animate-in mt-md">
      <a href="[link]" class="btn-primary">[Button Text]</a>
    </div>
    <p class="body-text text-secondary animate-in mt-sm">[Contact info or next step details]</p>
  </div>
</section>
```
