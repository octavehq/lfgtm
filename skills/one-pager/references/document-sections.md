# Document Sections

**Header:**
```html
<header class="section header">
  <!-- Logo if available (from brand extraction or Octave workspace) -->
  <img src="[logo-url]" alt="[Company]" class="logo" />
  <h1 class="heading-1">[Document Title]</h1>
  <p class="body-text text-secondary">Prepared for [Target Company] | [Date]</p>
</header>
```

**The Problem Today:**
```html
<section class="section">
  <h2 class="heading-2 section-title">The Problem Today</h2>
  <p class="lede">
    [ONE sentence lede — the sharpest framing of their situation, ~20 words max.
    Drawn from enrichment data, findings, or persona pain points. Specific to this account.]
  </p>
  <div class="grid-2">
    <div class="card">
      <h3 class="heading-3">[Short subheader, 3-5 words, e.g. "Signals go undetected"]</h3>
      <p class="body-sm text-secondary">[One sentence. Write it, then cut it by a third.]</p>
    </div>
    <!-- 2 cards. The subheader carries the point; the body is supporting detail only. -->
  </div>
</section>
```

Rules for this section:
- **No prose paragraphs beyond the lede.** Pain points go in cards with short subheaders (the "Signals go undetected" pattern) or bullets — never 2-3 sentence paragraphs.
- **The lede must sit a visual tier above the card body text.** Larger size and/or heavier weight (`.lede`, not `.body-text`). If the intro renders at the same size as the card copy below it, the hierarchy is broken.
- **Draft long, deliver short.** Write the pain framing, then cut each block by a third to half. Density comes from specificity, not word count.

**How [Product] Helps:**
```html
<section class="section">
  <h2 class="heading-2 section-title">How [Product] Helps</h2>
  <div class="value-props">
    <div class="value-prop">
      <h3 class="heading-3">[Value Prop Headline]</h3>
      <p class="body-text text-secondary">[1-2 sentences tailored to their situation]</p>
    </div>
    <!-- Repeat for 3-4 value props -->
  </div>
</section>
```

**Key Differentiators:**
```html
<section class="section">
  <h2 class="heading-2 section-title">Why [Your Company]</h2>
  <div class="grid-3">
    <div class="card">
      <h3 class="heading-3">[Differentiator]</h3>
      <p class="body-sm text-secondary">[1-2 sentences]</p>
    </div>
    <!-- 3 cards max -->
  </div>
</section>
```

**Proof Points:**

This section's format is validated — big transformation numbers ("$14M → $3M", "3×", "11 → 22") with a one-line context label and named customer attribution. Keep it.

```html
<section class="section">
  <h2 class="heading-2 section-title">What Teams Are Seeing</h2>
  <div class="proof-points">
    <div class="metric-card">
      <span class="big-number">[Metric Value — prefer before → after transformations]</span>
      <span class="body-sm text-secondary">[Metric context, one line]</span>
      <span class="body-sm customer-name">
        <!-- Optional: customer logo/favicon before the name -->
        <img src="https://www.google.com/s2/favicons?domain=[customer-domain]&sz=64" alt="" class="customer-favicon" />
        [Customer Name]
      </span>
    </div>
    <!-- 2-3 metrics or quotes -->
  </div>
  <!-- Optional quote -->
  <blockquote class="proof-quote">
    "[Customer quote]"
    <cite>-- [Name, Title, Company]</cite>
  </blockquote>
</section>
```

Customer logos (nice-to-have, not required): if the reference customer entity has a logo or known domain, show a small mark next to the attribution. Resolution order: (1) logo stored on the Octave reference/proof-point entity, (2) `get_external_brand_logo` for the customer's domain, (3) Google favicon lookup (`https://www.google.com/s2/favicons?domain=<domain>&sz=64`). Only include it if the resolved image is a real, recognizable mark — a generic globe/blank favicon is worse than no logo. Omit silently on failure.

**Next Steps:**
```html
<section class="section cta-block">
  <h2 class="heading-2 section-title">Next Step</h2>
  <ul class="cta-list">
    <li>[What happens next — one line, concrete action with their data/context in it]</li>
    <li>[What they get out of it — one line]</li>
  </ul>
  <div class="contact-info">
    <p class="body-sm">[Name] | [Email] | [Phone]</p>
    <p class="body-sm">[Meeting link if available]</p>
  </div>
</section>
```

Rules for this section:
- **Two bullets, not a paragraph.** This is a CTA, not a description. If it reads like an explanation of what the product does, it's wrong.
- **Cut by a third.** Draft the CTA, then remove a third of the words. Every line should be an action or an outcome.
