# Slide Type Templates

Use these templates for each slide type in the outline. Mix types for visual variety.

**Title Slide:**
```html
<section class="slide slide-title" data-slide="0">
  <div class="slide-inner flex-center flex-col">
    <span class="pill animate-in">[Category/Tag]</span>
    <h1 class="heading-1 animate-in">[Main Title]</h1>
    <p class="body-lg text-secondary animate-in">[Subtitle]</p>
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
      <img src="[image-url-or-path]" alt="[Description]" style="max-width: 100%; max-height: 55vh; object-fit: contain;" />
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
