# tokens.css Template

The reusable core of a brand kit (SKILL.md Step 4). A single `:root` block plus a web-font `@import`/comment. Use neutral, brand-agnostic token NAMES (so consuming skills reference the same names across brands) with this brand's VALUES:

```css
/* Brand tokens — <Company> (<domain>) — generated <date> */
/* Font: <web-font name + link or @font-face, or note the fallback> */
:root {
  /* color */
  --brand-bg: <hex>;
  --brand-bg-alt: <hex>;
  --brand-surface: <hex>;
  --brand-surface-dark: <hex>;
  --brand-ink: <hex>;
  --brand-muted: <hex>;
  --brand-on-dark: <hex>;
  --brand-primary: <hex>;
  --brand-primary-ink: <hex>;
  --brand-accent: <hex>;
  --brand-border: <hex>;
  --brand-border-soft: <hex>;
  --brand-positive: <hex>;
  --brand-negative: <hex>;
  --brand-band: <full gradient or solid for dark hero/footer>;

  /* type */
  --brand-font-heading: <stack>;
  --brand-font-body: <stack>;
  --brand-h1: <size>; --brand-h2: <size>; --brand-h3: <size>;
  --brand-body: <size>; --brand-eyebrow: <size>;
  --brand-tracking-heading: <em>;
  /* exact weights per role (capture the real values — many brands use medium display, not bold) */
  --brand-weight-heading: <e.g. 500>;
  --brand-weight-body: <e.g. 400>;
  --brand-weight-label: <eyebrow/label weight, e.g. 600>;
  --brand-weight-emphasis: <weight of emphasized words; equal to body if emphasis is color-only>;
  /* emphasis mechanism — how key words stand out (color / weight / size / decoration / none) */
  --brand-emphasis-ink-on-light: <hex or `inherit` if not color-based>;
  --brand-emphasis-ink-on-dark: <hex or `inherit`>;
  --brand-emphasis-decoration: <underline-bar | wash | gradient-text | none>;

  /* shape */
  --brand-radius-sm: <px>; --brand-radius: <px>; --brand-radius-pill: 999px;
  --brand-radius-section: <big radius for section containers, e.g. 28px>;
  --brand-shadow: <box-shadow>;
  /* button size scale (height / padding / font / radius per size) */
  --brand-btn-sm-height: <px>; --brand-btn-sm-pad: <y x>; --brand-btn-sm-font: <px>; --brand-btn-sm-radius: <px>;
  --brand-btn-md-height: <px>; --brand-btn-md-pad: <y x>; --brand-btn-md-font: <px>; --brand-btn-md-radius: <px>;
  --brand-btn-lg-height: <px>; --brand-btn-lg-pad: <y x>; --brand-btn-lg-font: <px>; --brand-btn-lg-radius: <px>;

  /* layout & rhythm (the composition layer — keep it airy) */
  --brand-container: <max-width, e.g. 1440px>;
  --brand-pad-section: <generous section vertical padding, e.g. 56-96px>;
  --brand-pad-card: <px>; --brand-gap: <px>;

  /* depth (what stops it looking flat) */
  --brand-glow: <radial-gradient glow layer(s) for dark bands>;
  --brand-tile-glow: <icon-tile box-shadow glow, e.g. 0 8px 30px -6px rgba(...)>;
  --brand-grad-border: <linear-gradient used for gradient borders>;
  /* texture — a subtle pattern layered above the glow on dark bands (--brand-hero-texture for light heroes). Recipes in SKILL.md Step 2.5. */
  --brand-texture: <dot grid | line grid | grain | none>;

  /* ---- foundations (capture the brand's scales, not just one value each) ---- */
  /* full neutral ramp — brands define 50→950; collapsing to 3 greys loses fidelity */
  --brand-gray-50: <hex>; --brand-gray-100: <hex>; --brand-gray-200: <hex>;
  --brand-gray-300: <hex>; --brand-gray-400: <hex>; --brand-gray-500: <hex>;
  --brand-gray-600: <hex>; --brand-gray-700: <hex>; --brand-gray-800: <hex>;
  --brand-gray-900: <hex>; --brand-gray-950: <hex>;
  /* semantic states (not just positive/negative) — each with a weak/bg tint */
  --brand-success: <hex>; --brand-success-weak: <hex>;
  --brand-warning: <hex>; --brand-warning-weak: <hex>;
  --brand-error:   <hex>; --brand-error-weak: <hex>;
  --brand-info:    <hex>; --brand-info-weak: <hex>;
  /* spacing scale (4px base or the brand's own step) */
  --brand-space-1: 4px; --brand-space-2: 8px; --brand-space-3: 12px; --brand-space-4: 16px;
  --brand-space-5: 24px; --brand-space-6: 32px; --brand-space-7: 48px; --brand-space-8: 64px;
  /* elevation scale (the renderer uses sm on cards, md on hover, xl on the sheet) */
  --brand-shadow-sm: <subtle>; --brand-shadow-md: <card hover>; --brand-shadow-lg: <raised>; --brand-shadow-xl: <sheet>;
  /* motion — read from the brand's CSS transitions */
  --brand-ease: <e.g. cubic-bezier(.2,0,0,1)>; --brand-duration: <e.g. .18s>;
  /* iconography — the brand's icon stroke weight (renderer applies it to icon tiles) */
  --brand-icon-stroke: <e.g. 1.5>;
  /* signature gradients captured as named tokens */
  --brand-gradient-1: <linear/radial gradient>; --brand-gradient-2: <…>;
}
```

**Light/dark theme pairing.** If the brand ships *both* a light and dark theme (common — many dev tools do), capture both. Put the default mode in `tokens` and the opposite-mode overrides in `manifest.render.tokensDark` (or `tokensLight`) — only the tokens that differ. The renderer's `--theme light|dark` merges them, so one kit renders either mode. (A brand that is inherently single-mode — e.g. all-dark — just uses `tokens`.)

`kit_base.css` consumes the new scales where they change output: elevation (`shadow-sm/md/xl`), motion (button/card transitions + `prefers-reduced-motion`), icon stroke, and **responsive breakpoints** (grids stack and gutters shrink ≤720px). The ramp / spacing / semantic / gradient tokens are captured as kit metadata and used by components/exports that need them. All are additive with fallbacks, so kits missing them still render.
