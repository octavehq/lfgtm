# Style Presets Reference

Full CSS variable definitions for the 12 style presets available in `/octave:deck`.

Each preset defines a complete visual system. Apply by copying the `:root` block into the generated HTML.

---

## Dark Themes

### 1. `midnight-pro`

Dark navy with clean white text and subtle blue accents. Executive, high-stakes feel.

```css
:root {
  /* Backgrounds */
  --bg: #0b1121;
  --bg-elevated: #111b2e;
  --bg-card: rgba(17, 27, 46, 0.7);
  --bg-card-hover: rgba(23, 37, 62, 0.8);

  /* Text */
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;

  /* Brand / Accent */
  --brand-primary: #3b82f6;
  --brand-500: #60a5fa;
  --brand-200: #bfdbfe;
  --brand-100: #dbeafe;
  --secondary: #818cf8;

  /* Status */
  --success: #34d399;
  --error: #f87171;
  --warning: #fbbf24;

  /* Borders & Shadows */
  --border: rgba(59, 130, 246, 0.15);
  --border-strong: rgba(59, 130, 246, 0.3);
  --shadow-brand: rgba(59, 130, 246, 0.08);
  --shadow-brand-md: rgba(59, 130, 246, 0.15);

  /* Radius */
  --radius: 6px;
  --radius-lg: 12px;
  --radius-pill: 9999px;

  /* Typography */
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;

  /* Animation */
  --ease: cubic-bezier(0.16, 1, 0.3, 1);

  /* Spacing */
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Inter:wght@200;300;400;500;600&display=swap`

---

### 2. `executive-dark`

Charcoal with warm gold accents. Premium boardroom aesthetic.

```css
:root {
  --bg: #1a1a1a;
  --bg-elevated: #242424;
  --bg-card: rgba(36, 36, 36, 0.7);
  --bg-card-hover: rgba(42, 42, 42, 0.8);

  --text-primary: #f5f0eb;
  --text-secondary: #a8a09a;
  --text-muted: #736e69;

  --brand-primary: #c9a84c;
  --brand-500: #d4b85a;
  --brand-200: #ede0b8;
  --brand-100: #f5ecd4;
  --secondary: #a89060;

  --success: #6b9e7a;
  --error: #c45c5c;
  --warning: #d4a84c;

  --border: rgba(201, 168, 76, 0.12);
  --border-strong: rgba(201, 168, 76, 0.25);
  --shadow-brand: rgba(201, 168, 76, 0.06);
  --shadow-brand-md: rgba(201, 168, 76, 0.12);

  --radius: 4px;
  --radius-lg: 8px;
  --radius-pill: 9999px;

  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Source Sans 3', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Playfair+Display:wght@400;500;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap`

---

### 3. `octave-brand`

Octave's purple palette on dark navy. Product-aligned, on-brand.

```css
:root {
  --bg: rgb(15, 23, 42);
  --bg-elevated: rgb(22, 33, 55);
  --bg-card: rgba(30, 41, 66, 0.6);
  --bg-card-hover: rgba(40, 51, 80, 0.7);

  --text-primary: rgb(255, 255, 255);
  --text-secondary: rgb(148, 163, 184);
  --text-muted: rgb(100, 116, 139);

  --brand-primary: rgb(47, 38, 178);
  --brand-500: rgb(100, 91, 237);
  --brand-200: rgb(217, 214, 255);
  --brand-100: rgb(236, 234, 255);
  --secondary: rgb(166, 116, 233);

  --success: rgb(99, 164, 127);
  --error: rgb(229, 100, 109);
  --warning: rgb(234, 151, 74);

  --border: rgba(100, 91, 237, 0.2);
  --border-strong: rgba(100, 91, 237, 0.4);
  --shadow-brand: rgba(47, 38, 178, 0.1);
  --shadow-brand-md: rgba(47, 38, 178, 0.2);

  --radius: 5px;
  --radius-lg: 10px;
  --radius-pill: 9999px;

  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Inter:wght@200;300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`

---

### 4. `electric-studio`

Pure black canvas with electric blue accent. Clean, tech-forward.

```css
:root {
  --bg: #0a0a0a;
  --bg-elevated: #141414;
  --bg-card: rgba(20, 20, 20, 0.8);
  --bg-card-hover: rgba(26, 26, 26, 0.9);

  --text-primary: #ffffff;
  --text-secondary: #a3a3a3;
  --text-muted: #737373;

  --brand-primary: #4361ee;
  --brand-500: #6380f5;
  --brand-200: #b8c5fb;
  --brand-100: #dce2fd;
  --secondary: #7c8cf5;

  --success: #34d399;
  --error: #f87171;
  --warning: #fbbf24;

  --border: rgba(67, 97, 238, 0.15);
  --border-strong: rgba(67, 97, 238, 0.3);
  --shadow-brand: rgba(67, 97, 238, 0.08);
  --shadow-brand-md: rgba(67, 97, 238, 0.15);

  --radius: 8px;
  --radius-lg: 16px;
  --radius-pill: 9999px;

  --font-display: 'Manrope', -apple-system, sans-serif;
  --font-body: 'Manrope', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Manrope:wght@200;300;400;500;600;700&display=swap`

---

### 5. `neon-pulse`

Dark background with neon green and cyan. Developer energy, hacker aesthetic.

```css
:root {
  --bg: #0d0d0d;
  --bg-elevated: #161616;
  --bg-card: rgba(22, 22, 22, 0.8);
  --bg-card-hover: rgba(28, 28, 28, 0.9);

  --text-primary: #e4e4e7;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;

  --brand-primary: #22d3ee;
  --brand-500: #06b6d4;
  --brand-200: #a5f3fc;
  --brand-100: #cffafe;
  --secondary: #4ade80;

  --success: #4ade80;
  --error: #f87171;
  --warning: #facc15;

  --border: rgba(34, 211, 238, 0.15);
  --border-strong: rgba(34, 211, 238, 0.3);
  --shadow-brand: rgba(34, 211, 238, 0.08);
  --shadow-brand-md: rgba(34, 211, 238, 0.15);

  --radius: 4px;
  --radius-lg: 8px;
  --radius-pill: 9999px;

  --font-display: 'Space Grotesk', -apple-system, sans-serif;
  --font-body: 'Space Grotesk', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap`

---

### 6. `dark-botanical`

Dark canvas with warm gold, pink, and rose accents. Elegant and premium.

```css
:root {
  --bg: #0f0f0f;
  --bg-elevated: #1a1a1a;
  --bg-card: rgba(26, 26, 26, 0.7);
  --bg-card-hover: rgba(32, 32, 32, 0.8);

  --text-primary: #e8e4df;
  --text-secondary: #9a9590;
  --text-muted: #6b6661;

  --brand-primary: #d4a574;
  --brand-500: #e0b88a;
  --brand-200: #f0dcc4;
  --brand-100: #f7ede0;
  --secondary: #e8b4b8;

  --success: #6b9e7a;
  --error: #c45c5c;
  --warning: #d4a574;

  --border: rgba(212, 165, 116, 0.12);
  --border-strong: rgba(212, 165, 116, 0.25);
  --shadow-brand: rgba(212, 165, 116, 0.06);
  --shadow-brand-md: rgba(212, 165, 116, 0.12);

  --radius: 4px;
  --radius-lg: 8px;
  --radius-pill: 9999px;

  --font-display: 'Cormorant', Georgia, serif;
  --font-body: 'IBM Plex Sans', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Cormorant:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`

---

## Light Themes

### 7. `swiss-modern`

White canvas with red accent. Bauhaus-inspired, grid-driven minimalism.

```css
:root {
  --bg: #fafafa;
  --bg-elevated: #ffffff;
  --bg-card: rgba(255, 255, 255, 0.9);
  --bg-card-hover: rgba(245, 245, 245, 1);

  --text-primary: #0a0a0a;
  --text-secondary: #525252;
  --text-muted: #a3a3a3;

  --brand-primary: #ff3300;
  --brand-500: #ff5533;
  --brand-200: #ffb8a8;
  --brand-100: #ffddd5;
  --secondary: #0a0a0a;

  --success: #16a34a;
  --error: #dc2626;
  --warning: #d97706;

  --border: rgba(0, 0, 0, 0.08);
  --border-strong: rgba(0, 0, 0, 0.15);
  --shadow-brand: rgba(255, 51, 0, 0.05);
  --shadow-brand-md: rgba(255, 51, 0, 0.1);

  /* Grid lines (unique to this preset) */
  --grid: rgba(0, 0, 0, 0.06);
  --grid-strong: rgba(0, 0, 0, 0.10);

  --radius: 0px;
  --radius-lg: 0px;
  --radius-pill: 9999px;

  --font-display: 'Archivo', -apple-system, sans-serif;
  --font-body: 'Nunito', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Archivo:wght@400;500;600;700;800;900&family=Nunito:wght@300;400;500;600;700&display=swap`

**Note:** This preset uses sharp corners (`--radius: 0px`) and optional grid lines via `--grid` variables. Add a `.bg-grid` layer using repeating linear gradients for the full Bauhaus grid effect.

---

### 8. `soft-light`

Warm white with sage green accents. Calm, approachable, friendly.

```css
:root {
  --bg: #faf9f7;
  --bg-elevated: #ffffff;
  --bg-card: rgba(255, 255, 255, 0.8);
  --bg-card-hover: rgba(245, 243, 240, 1);

  --text-primary: #1a1a1a;
  --text-secondary: #5c5c5c;
  --text-muted: #999999;

  --brand-primary: #5b8a72;
  --brand-500: #6f9e85;
  --brand-200: #c2dace;
  --brand-100: #e0ede6;
  --secondary: #8b7355;

  --success: #5b8a72;
  --error: #c45c5c;
  --warning: #c4943a;

  --border: rgba(91, 138, 114, 0.12);
  --border-strong: rgba(91, 138, 114, 0.2);
  --shadow-brand: rgba(91, 138, 114, 0.06);
  --shadow-brand-md: rgba(91, 138, 114, 0.12);

  --radius: 8px;
  --radius-lg: 16px;
  --radius-pill: 9999px;

  --font-display: 'DM Sans', -apple-system, sans-serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'DM Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap`

---

### 9. `paper-minimal`

Off-white with pure black type. Editorial simplicity. Content speaks for itself.

```css
:root {
  --bg: #f5f3ef;
  --bg-elevated: #faf8f5;
  --bg-card: rgba(250, 248, 245, 0.9);
  --bg-card-hover: rgba(240, 237, 232, 1);

  --text-primary: #111111;
  --text-secondary: #555555;
  --text-muted: #999999;

  --brand-primary: #111111;
  --brand-500: #333333;
  --brand-200: #cccccc;
  --brand-100: #e5e5e5;
  --secondary: #888888;

  --success: #2d6a4f;
  --error: #9b2c2c;
  --warning: #92400e;

  --border: rgba(0, 0, 0, 0.08);
  --border-strong: rgba(0, 0, 0, 0.15);
  --shadow-brand: rgba(0, 0, 0, 0.03);
  --shadow-brand-md: rgba(0, 0, 0, 0.06);

  --radius: 2px;
  --radius-lg: 4px;
  --radius-pill: 9999px;

  --font-display: 'Libre Baskerville', Georgia, serif;
  --font-body: 'Source Sans 3', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@300;400;500;600&display=swap`

---

## Vibrant Themes

### 10. `solar-flare`

Deep orange and amber gradients on dark. Bold, energetic, high-impact.

```css
:root {
  --bg: #1a0e05;
  --bg-elevated: #241508;
  --bg-card: rgba(36, 21, 8, 0.7);
  --bg-card-hover: rgba(48, 28, 10, 0.8);

  --text-primary: #fef3e2;
  --text-secondary: #c9a882;
  --text-muted: #8a7054;

  --brand-primary: #f97316;
  --brand-500: #fb923c;
  --brand-200: #fed7aa;
  --brand-100: #ffedd5;
  --secondary: #fbbf24;

  --success: #4ade80;
  --error: #f87171;
  --warning: #fbbf24;

  --border: rgba(249, 115, 22, 0.15);
  --border-strong: rgba(249, 115, 22, 0.3);
  --shadow-brand: rgba(249, 115, 22, 0.08);
  --shadow-brand-md: rgba(249, 115, 22, 0.15);

  --radius: 6px;
  --radius-lg: 12px;
  --radius-pill: 9999px;

  --font-display: 'Sora', -apple-system, sans-serif;
  --font-body: 'Sora', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Sora:wght@200;300;400;500;600;700&display=swap`

**Note:** Use radial gradient orbs with `--brand-primary` and `--secondary` for a warm glowing background effect. Gradient direction should be bottom-left to top-right.

---

### 11. `aurora-gradient`

Purple-to-teal gradients on deep dark. Visionary, modern, forward-looking.

```css
:root {
  --bg: #0a0a1a;
  --bg-elevated: #12122a;
  --bg-card: rgba(18, 18, 42, 0.7);
  --bg-card-hover: rgba(24, 24, 52, 0.8);

  --text-primary: #f0f0ff;
  --text-secondary: #a0a0c0;
  --text-muted: #6b6b8a;

  --brand-primary: #8b5cf6;
  --brand-500: #a78bfa;
  --brand-200: #ddd6fe;
  --brand-100: #ede9fe;
  --secondary: #06b6d4;

  --success: #34d399;
  --error: #f87171;
  --warning: #fbbf24;

  --border: rgba(139, 92, 246, 0.15);
  --border-strong: rgba(139, 92, 246, 0.3);
  --shadow-brand: rgba(139, 92, 246, 0.08);
  --shadow-brand-md: rgba(139, 92, 246, 0.15);

  --radius: 10px;
  --radius-lg: 20px;
  --radius-pill: 9999px;

  --font-display: 'Outfit', -apple-system, sans-serif;
  --font-body: 'Outfit', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Outfit:wght@200;300;400;500;600;700&display=swap`

**Note:** Use gradient orbs blending `--brand-primary` (purple) and `--secondary` (teal) for the aurora effect. Cards can use a subtle gradient border: `border-image: linear-gradient(135deg, var(--brand-primary), var(--secondary)) 1`.

---

### 12. `monochrome-bold`

High-contrast black and white. Statement typography. No color distractions.

```css
:root {
  --bg: #000000;
  --bg-elevated: #0d0d0d;
  --bg-card: rgba(13, 13, 13, 0.9);
  --bg-card-hover: rgba(20, 20, 20, 1);

  --text-primary: #ffffff;
  --text-secondary: #b0b0b0;
  --text-muted: #707070;

  --brand-primary: #ffffff;
  --brand-500: #e0e0e0;
  --brand-200: #a0a0a0;
  --brand-100: #c0c0c0;
  --secondary: #808080;

  --success: #ffffff;
  --error: #ffffff;
  --warning: #ffffff;

  --border: rgba(255, 255, 255, 0.1);
  --border-strong: rgba(255, 255, 255, 0.25);
  --shadow-brand: rgba(255, 255, 255, 0.03);
  --shadow-brand-md: rgba(255, 255, 255, 0.06);

  --radius: 0px;
  --radius-lg: 0px;
  --radius-pill: 9999px;

  --font-display: 'Bebas Neue', Impact, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Google Fonts:** `Bebas+Neue&family=Inter:wght@200;300;400;500;600&display=swap`

**Note:** This preset relies on typography scale and whitespace for visual impact. Use oversized `heading-1` with `clamp(3rem, 8vw, 7rem)` for statement slides. Avoid decorative elements — let the words do the work.

---

## Variable Reference

All presets share this consistent variable interface:

| Variable | Purpose | Used By |
|----------|---------|---------|
| `--bg` | Page/slide background | `.slide`, `body` |
| `--bg-elevated` | Raised surface background | Headers, navigation |
| `--bg-card` | Card background (usually semi-transparent) | `.card` |
| `--bg-card-hover` | Card hover state | `.card:hover` |
| `--text-primary` | Main text color | `body`, `.heading-*` |
| `--text-secondary` | Supporting text | `.text-secondary`, subtitles |
| `--text-muted` | De-emphasized text | `.text-muted`, captions |
| `--brand-primary` | Primary accent (darkest) | `.pill`, `.brand-line`, links |
| `--brand-500` | Medium accent | Hover states, active indicators |
| `--brand-200` | Light accent | Backgrounds, subtle highlights |
| `--brand-100` | Lightest accent | Background tints |
| `--secondary` | Secondary accent color | Complementary highlights |
| `--success` | Positive state | `.pill-success`, check marks |
| `--error` | Negative state | `.pill-error`, warnings |
| `--warning` | Caution state | `.pill-warning` |
| `--border` | Subtle borders | `.card`, `.divider` |
| `--border-strong` | Emphasized borders | Active states, focus rings |
| `--shadow-brand` | Subtle shadow | Card shadows |
| `--shadow-brand-md` | Medium shadow | Hover shadows, elevated cards |
| `--radius` | Default border radius | Cards, buttons, inputs |
| `--radius-lg` | Large border radius | Modals, featured cards |
| `--radius-pill` | Pill shape | `.pill`, tags, badges |
| `--font-display` | Heading font | `.heading-1`, `.heading-2`, `.heading-3` |
| `--font-body` | Body text font | `body`, `.body-text`, `.body-lg` |
| `--font-mono` | Monospace font | `.mono`, code blocks |
| `--ease` | Animation easing | All transitions |
| `--pad-x` | Horizontal padding | `.slide-inner` |
| `--pad-y` | Vertical padding | `.slide-inner` |

## Creating Custom Presets

To create a brand-specific preset from extracted brand colors:

```css
:root {
  /* Map brand colors to the variable system */
  --bg: [brand dark background or #0f172a for dark themes];
  --bg-elevated: [slightly lighter than --bg];
  --bg-card: [--bg-elevated with 0.6-0.8 alpha];
  --bg-card-hover: [--bg-elevated with 0.7-0.9 alpha];

  --text-primary: [brand text color, ensure 4.5:1 contrast ratio with --bg];
  --text-secondary: [60% opacity of --text-primary];
  --text-muted: [40% opacity of --text-primary];

  --brand-primary: [primary brand color];
  --brand-500: [lighter variant, +15% lightness];
  --brand-200: [very light variant, +40% lightness];
  --brand-100: [near-white tint, +50% lightness];
  --secondary: [secondary brand color or complementary hue];

  /* Keep status colors universal for accessibility */
  --success: #34d399;
  --error: #f87171;
  --warning: #fbbf24;

  --border: [brand-primary with 0.12-0.2 alpha];
  --border-strong: [brand-primary with 0.25-0.4 alpha];
  --shadow-brand: [brand-primary with 0.06-0.1 alpha];
  --shadow-brand-md: [brand-primary with 0.12-0.2 alpha];

  --radius: [4-8px for professional, 10-16px for friendly, 0px for bold];
  --radius-lg: [2x --radius];
  --radius-pill: 9999px;

  --font-display: [brand heading font], [system fallback];
  --font-body: [brand body font], [system fallback];
  --font-mono: 'IBM Plex Mono', monospace;

  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --pad-x: clamp(2rem, 5vw, 6rem);
  --pad-y: clamp(1.5rem, 3vh, 4rem);
}
```

**Contrast requirements:**
- `--text-primary` on `--bg`: minimum 7:1 (WCAG AAA)
- `--text-secondary` on `--bg`: minimum 4.5:1 (WCAG AA)
- `--brand-primary` on `--bg`: minimum 3:1 for large text
