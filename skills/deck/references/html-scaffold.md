# Deck HTML Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Deck Title]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

    /* === Slide Container === */
    .slide {
      height: 100vh;
      height: 100dvh;
      width: 100%;
      scroll-snap-align: start;
      overflow: hidden;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(2rem, 5vw, 4rem); }
    .heading-2 { font-size: clamp(1.5rem, 3.5vw, 2.75rem); }
    .heading-3 { font-size: clamp(1rem, 2vw, 1.5rem); }
    .body-text { font-size: clamp(0.85rem, 1.4vw, 1.05rem); }

    /* === Layout Utilities === */
    .slide-inner { max-width: 1100px; width: 100%; padding: clamp(1.5rem, 4vh, 3rem) clamp(2rem, 5vw, 6rem); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(1rem, 2vw, 2rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1rem, 2vw, 2rem); }

    /* === Components (cards, pills, metrics, etc.) === */
    /* === Animations === */
    /* === Navigation (progress bar + nav dots) === */
    /* === Responsive (max-height media queries) === */
    /* === prefers-reduced-motion === */
  </style>
</head>
<body>

  <div id="progress-bar"></div>
  <nav id="nav-dots"></nav>

  <!-- Slides -->
  <section class="slide" data-slide="0">
    <div class="bg-mesh">...</div>
    <div class="slide-inner">
      <!-- Slide content -->
    </div>
  </section>

  <!-- Repeat for each slide -->

  <script>
    // Navigation: keyboard (ArrowDown/Up, Space, PageDown/Up), scroll snap, touch
    // Progress bar animation
    // Nav dots generation and active state
    // Intersection Observer for .animate-in elements
    // prefers-reduced-motion check
  </script>

</body>
</html>
```
