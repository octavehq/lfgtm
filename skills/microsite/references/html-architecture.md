# HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Built for [Company] | [Your Company]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset — same system as deck) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.6;
    }

    /* === Layout === */
    .section {
      width: 100%;
      padding: clamp(3rem, 8vh, 6rem) clamp(1.5rem, 5vw, 3rem);
    }
    .section-inner {
      max-width: 800px;
      margin: 0 auto;
    }
    .hero {
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(2.2rem, 5.5vw, 4rem); font-family: var(--font-display); }
    .heading-2 { font-size: clamp(1.6rem, 3.5vw, 2.5rem); font-family: var(--font-display); }
    .heading-3 { font-size: clamp(1.1rem, 2vw, 1.4rem); font-family: var(--font-display); }
    .body-text { font-size: clamp(0.95rem, 1.4vw, 1.1rem); }
    .body-lg { font-size: clamp(1.05rem, 1.8vw, 1.3rem); }

    /* === Components (cards, metrics, proof blocks) === */
    /* === Scroll-triggered animations === */
    /* === Mobile responsive === */
    /* === prefers-reduced-motion === */
  </style>
</head>
<body>

  <!-- Hero: full viewport, gradient background, "Built for [Company]" -->
  <section class="section hero" id="hero">
    <div class="bg-gradient"></div>
    <div class="section-inner">
      <span class="built-for animate-in">Built for [Company]</span>
      <h1 class="heading-1 animate-in">[Headline based on angle]</h1>
      <p class="body-lg text-secondary animate-in">[Subhead]</p>
    </div>
  </section>

  <!-- Section 2-4: Content sections based on angle -->
  <section class="section" id="[section-id]">
    <div class="section-inner">
      <!-- Section content -->
    </div>
  </section>

  <!-- CTA: final section with clear action -->
  <section class="section hero" id="cta">
    <div class="section-inner">
      <h2 class="heading-1 animate-in">[CTA headline]</h2>
      <p class="body-lg text-secondary animate-in">[Supporting line]</p>
      <a href="[cta-link]" class="cta-button animate-in">[Button text]</a>
    </div>
  </section>

  <script>
    // Intersection Observer for scroll-triggered .animate-in elements
    // Smooth scroll for anchor links
    // Counter animation for metric numbers (if present)
    // prefers-reduced-motion check
  </script>

</body>
</html>
```
