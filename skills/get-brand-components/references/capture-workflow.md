# Capture workflow and kit contract

Use the [task method](task-method.md) for validation and source fidelity. Build in a unique staging directory. Canonical cache identity is verified workspace ID plus full normalized hostname/TLD; legacy names are aliases only after manifest identity matches. After mechanical and visual checks, use [brand_cache.py](../scripts/brand_cache.py) to promote the capture through an atomic pointer. A failed refresh preserves the prior capture. Consumers resolve `current.json` before reading manifest/assets. Source URLs, capture time, checksums and allowed-use decisions are required for promotion.

Read this reference for capture; it retains the visual extraction and token/component contract. No voice, messaging or proof library belongs in a kit.
## Capture the visual system

#### Step 1: Resolve the target and plan the crawl

1. Normalize the input to a base URL (`https://www.<domain>` if only a bare domain is given; keep an explicit URL as the seed).
2. Derive the `<slug>` from the registrable domain.
3. **Cache check (do this first).** If a kit already exists at `<staging-kit>/` (has `manifest.json`), **reuse it by default**: print a one-line summary from `manifest.json`, `open` the gallery, and **stop — do not re-walk or spend scrape credits.** Only proceed to Step 2 when the user passed `refresh` (or explicitly asked to rebuild/re-scrape), or the kit is missing/partial/stale. Mention they can pass `refresh` to rebuild.
4. **Asset-store fallback (on local miss only).** No local kit? Before spending scrape credits, check whether this kit was already published as a hosted asset — **by you or a workspace teammate** (workspace-shared assets appear in the list with their `owner`). If the Octave MCP asset tools aren't available, skip this silently and continue to Step 2.
   - Run the `assets_list` MCP tool — an **actual tool call**, never a bash/python simulation, and never "assume" its result. If the `assets_list` result is not in your transcript, this check did not happen and you may not proceed to Step 2. Look for identifier `<slug>-brand-kit` — exact first, then fuzzy (identifier or description containing the slug/company name plus "brand").
   - **Match found** → tell the user: *"A brand kit for <domain> is already published (owner: <me | teammate name>): <link>"* and ask (AskUserQuestion): **Use it (Recommended)** — download it as the local cache — or **Rebuild fresh** — walk the site anyway.
     - *Use it*: follow the asset-manager download workflow in [`../../asset-manager/SKILL.md`](../../asset-manager/SKILL.md) — mint the token, then `download-artifact.sh --uuid <uuid> --out "${TMPDIR:-/tmp}"` (files land in `${TMPDIR:-/tmp}/<identifier>/`, where `<identifier>` is the matched asset's actual identifier — for a fuzzy match it may not be exactly `<slug>-brand-kit`). **Only if the download exits 0 and `${TMPDIR:-/tmp}/<identifier>/manifest.json` exists**, promote it: `mkdir -p ~/.octave/brands && rm -rf <brand-cache>/<slug> && mv "${TMPDIR:-/tmp}/<identifier>" <brand-cache>/<slug>` (the `mkdir -p` is required on a fresh machine — `mv` will not create the parent). If the download failed or `manifest.json` is missing, leave `<brand-cache>/` untouched and continue to Step 2. Then treat it exactly like a local cache hit: summarize, open the gallery, **stop** — no scrape credits spent. Update the asset-manager registry per its rules.
     - *Rebuild fresh*: continue to Step 2, but remember the asset's uuid and owner — Step 8.5 will offer to **update** the hosted kit if it is yours; a teammate-owned kit can't be modified, so you'd publish your own copy instead.
   - **No match** → continue to Step 2 without extra chatter.

#### Step 2: Walk the key pages

Scrape the homepage first (`format: html`, `includeScreenshot: true`). Then choose up to **5 more** high-signal pages — these are where a brand's design system is most fully expressed. Discover them from the homepage's nav/footer links and prefer, in order:

1. **Homepage** (`/`) — hero pattern, primary CTA, nav, color story (always)
2. **Product / Platform / Features** — cards, feature grids, icon tiles, stats
3. **Pricing** — tables, plan cards, badges, toggles, comparison rows
4. **A blog / "learn" / docs article** — long-form typography, body type scale, inline links, callouts
5. **Customers / Case studies** — quotes/testimonials, logo treatment, metric/stat blocks
6. **About / Company or a solutions page** — secondary section patterns

Skip pages that 404 or duplicate a pattern you already have. Aim for coverage of distinct component types, not page count. **Fan the non-home pages out to parallel page analysts** (see *Run the heavy steps as subagents*) so the raw HTML never lands in the main context — each returns compact visual observations plus the page's section order. Report progress:

```
Walking <domain>…
  ✓ /              (hero, nav, primary CTA)
  ✓ /product       (feature cards, icon tiles)
  ✓ /pricing       (plan cards, comparison table)
  ✓ /learn/post/x  (article typography, callouts)
  ✓ /customers     (testimonials, stat blocks)
Captured 5 pages. Deriving the design system…
```

For each scraped page, if `screenshotUrl` is present, save it:

```bash
mkdir -p <staging-kit>/screenshots
curl -s "<screenshotUrl>" -o <staging-kit>/screenshots/<page-slug>.png
```

#### Step 2.5: Pull the real CSS & assets (the fidelity step — do not skip)

The scrape gives you rendered HTML + a picture; the **exact values live in the stylesheet bundle**. Fetch and mine it directly. Use a browser User-Agent so you get the real markup.

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
curl -s -A "$UA" https://www.<domain>/ -o /tmp/<slug>_home.html
# Next.js sites: CSS at /_next/static/css/*.css . Other stacks: grep the <link rel=stylesheet> hrefs.
for f in $(grep -oE '/_next/static/css/[^"]+\.css' /tmp/<slug>_home.html | sort -u); do
  curl -s -A "$UA" "https://www.<domain>$f" >> /tmp/<slug>_all.css; echo >> /tmp/<slug>_all.css
done
```

Then extract the **real** values (don't transcribe a vibe):

- **Fonts** — `grep -oE 'font-family:[^;}]+'` and the `@font-face`/`--font-*` vars. Capture the true family **and weight** for headings vs body (many brands use a **medium-weight** display face for headings — defaulting to bold-700/800 would be wrong). **Then EMBED the real webfont** so output renders pixel-exact instead of in a fallback (a wrong heading face is the #1 "AI slop" tell):
  - Pull each `@font-face` `src:url(...)` for the heading family from the CSS (`grep -oE "@font-face\{[^}]*}" all.css | grep -i <family>`), `curl` the `.woff2`/`.woff` into `<staging-kit>/fonts/`, then **base64-embed it** as an `@font-face` with a `data:` URL in `tokens.css` / the output `<style>`. Example:
    ```bash
    curl -s -A "$UA" "https://www.<domain>/_next/static/media/<hash>.woff" -o <staging-kit>/fonts/<family>-<wght>.woff
    B64=$(base64 -i <staging-kit>/fonts/<family>-<wght>.woff)   # embed as: @font-face{font-family:'<Family>';src:url(data:font/woff;base64,$B64) format('woff');font-weight:...;font-display:swap}
    ```
  - **Licensing caveat:** embedding a licensed face is fine for an internal stab / a doc going to the brand owner; for anything redistributed, fall back to the closest free face and say so. Either way keep the real family **first** in the stack so a machine with it installed renders it, with a close free fallback behind. State which path you took in `brand-kit.md`.
- **Component rules** — grep the real class rules: buttons (`button-primary/secondary/tertiary`), the type scale (`Heading*`, `Text*`, `Label*`), cards. Copy exact `border-radius`, `padding`, `box-shadow`, `background`, inset rings, transitions.
- **Button size scale — capture it, don't ship one guessed size.** Brands define buttons at multiple sizes (sm/md/lg), and the proportions are a strong brand tell. For each size record **height, x/y padding, font-size, corner radius, and icon size** (e.g. sm 32px·r8, md 40px·r12, lg 48px·pill — note that corner radius often grows with size). Note the default size used for primary CTAs and whether CTAs are pill vs the standard rounded-rect. Emit `--brand-btn-{sm,md,lg}-{height,pad,font,radius}` tokens and show all sizes in the gallery.
- **Palette** — rank actual usage: `grep -oE '#[0-9a-fA-F]{6}' all.css | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -30`. Map the top hits to roles; confirm against the screenshot.
- **Emphasis & accent mechanism — figure out *how* the brand emphasizes, don't assume.** Look at the hero/section headings and inline copy and identify the actual device(s):
  - **Color** — is the emphasized word a different color (accent/lavender/blue)? On light vs dark?
  - **Weight** — heavier (or lighter) than surrounding text? (Capture the exact weights — e.g. body 400, emphasis 600; or a *light* display heading with regular-weight emphasis.)
  - **Size** — larger? a different type ramp step?
  - **Decoration** — underline bar, highlighter wash, boxed/pill, gradient-text (`background-clip:text`), letter-spacing, italics, all-caps?
  - **None of the above** — many brands emphasize *only* by color or *only* by weight; do **not** bolt on an underline/wash the brand doesn't use. Borrowing another brand's emphasis device is an instant tell.
  Record the mechanism as a rule (e.g. `--brand-emphasis: color #582ecc on light / #a384f6 on dark, same weight, no underline`) and apply *that*, with the light/dark contrast variants below.
- **Signature treatments** — pull the literal `background-image`/gradient for things like highlighted-word underlines and icon-tile fills (these are what make it unmistakable). **Capture light AND dark variants of each treatment** — brands swap accent colors per background. (A brand's highlighted text might be a saturated accent on light but flip to **white on dark**, keeping the same underline in both — its CSS will carry both color rules.)
- **Contrast rules (legibility — non-negotiable).** Record, per token, which background it's legible on, and store on-light / on-dark variants. Then enforce in every component:
  - A mid-tone accent (a link blue, a saturated brand color) used as **text** must meet contrast on its background — **never place it as text on a dark band**; use the brand's on-dark variant (usually white or a pale tint). Highlighted words flip to the on-dark color.
  - Decorative wash/gradient *behind* text is fine on light but goes muddy on dark — drop or invert it on dark surfaces; keep only the high-contrast part (e.g. the underline bar).
  - Aim for WCAG AA (≈4.5:1 for body, 3:1 for large headings). When unsure, use the foreground the brand itself uses on that surface.
- **Composition & depth (do not skip — this is what separates "designer-grade" from "AI slop").** Tokens alone produce a correctly-colored but flat, cramped doc. You must also lift the brand's *layout system*:
  - **Rhythm & whitespace** — container `max-width` + responsive gutters, and the **section vertical padding** (grep the hero/section wrapper rules; section padding is often `4–6rem` top/bottom). Brands look professional because they're *airy* — generous section padding, large headings, comfortable line-height. Reproduce that scale; do not pack content edge-to-edge.
  - **Section header pattern** — how a section opens (e.g. a **centered** `eyebrow label → balanced heading (one highlighted word) → muted subhead`). Mirror the brand's actual pattern on every section.
  - **Depth treatments** — what stops it being a flat rectangle: radial-gradient **glows** on dark sections, **glow box-shadows** on icon tiles (`box-shadow:0 0 100px #01f846`-style), **gradient borders** (`border-image:linear-gradient(...)` or a mask ring), layered surfaces, and any hero **graphic / floating product chips**. Capture these and use them — a dark hero must have glow + a graphic element, not be a plain block.
  - **Texture / pattern** — capture any background *tooth* the brand uses on its bands: dot grids, line/blueprint grids, film grain, mesh-gradient blobs. These read as "premium" and are easy to miss. Set `--brand-texture` (layered above the glow on dark bands; `--brand-hero-texture` for light heroes). Reusable CSS recipes — tint the rgba to the brand:
    - **dot grid:** `radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.4px) 0 0/22px 22px`
    - **line/blueprint grid:** `linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px) 0 0/30px 30px, linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px) 0 0/30px 30px`
    - **film grain:** an inline SVG `feTurbulence` data-URI (`<rect filter=fractalNoise opacity='0.12'>`) — premium tooth on dark/gradient bands
    Tune intensity per type: line/dot grids read at ≈5% alpha, but **grain needs ≈10–14%** (at 6% it's invisible at normal size). Keep it subtle enough not to hurt contrast, and confirm against the source — don't add texture a brand doesn't use.
  - **Edges & containers** — match how the brand *frames* sections. Capture the **section corner radius** (many brands round everything — `~1.5–2.5rem`), whether sections **float on a soft canvas** (rounded sheet/cards) vs full-bleed, and any **curved/wavy dividers** between bands. **Never emit a sharp full-bleed rectangle when the brand rounds its sections** — round the hero/band/footer corners to the section radius (e.g. wrap the doc in a rounded sheet with `overflow:hidden` so even the top hero corners are rounded). Hard right-angle edges against the page are an instant "not from them" tell.
  - **Real type scale at real sizes** — headings are large and confident (often `2.5–4rem`). Scaling them down to ~17px kills the brand feel; keep them big.

**Lift the real assets (download + inline, never hotlink):**

- **Logo** — find `<img alt="…Logo">` or the nav logo `<svg>`; `curl` it to `<staging-kit>/` and inline it. **Capture BOTH lockups:** the dark-text version for light backgrounds AND the white/light version for dark bands (look for `logoFullWhite`, `logo-white`, the nav logo on a dark hero, etc.). Use the right one per surface.
  - **Source rule (this is where contamination starts).** Take the **onLight** logo from the **nav brand lockup** (top-left, linked to `/`). Take the **onDark** logo from the **footer** (footers are usually dark and carry the brand's real white lockup) or the nav rendered over a dark hero. **NEVER take a logo from a "trusted by" / customers / partners / clients / logo-wall container** — those are white *customer* logos and are the #1 source of a wrong-company mark. The onDark variant is the one that gets contaminated, because the customer wall is dark and full of white logos.
  - **Wordmark gate — inspect the pixels, not the metadata.** After downloading EACH variant, **Read the image file (the Read tool renders it) and confirm the wordmark reads THIS brand's name.** Manifest metadata is not enough: a kit can record `lockup.wordmark: "Octave"` while the actual file is a WorkSpan logo scraped from the customer wall. A white logo is invisible on a light preview, so the onDark variant must be checked specifically — render it on a dark background. Reject any asset that shows a different company.
  - **Run the verifier before caching:** `bash scripts/verify-logos.sh <slug>` renders onLight on white and onDark on dark side by side and flags file/aspect issues. Eyeball both cells; each must read the brand's name.
  - **Record provenance.** Store the source URL of each variant in the manifest (`logo.onLightSource`, `logo.onDarkSource`). If a source path or its container class/id contains `customers|partners|trusted|clients|logos`, or points at a different domain than the brand's, treat the asset as suspect and re-source.
  - **Fallback ladder for onDark:** verified footer/nav white lockup → `favicon` / `og:image` (authoritative brand marks) → **controlled recolor of the VERIFIED onLight** as a last resort. A recolor (`filter:brightness(0) invert(1)`) flattens a colored mark, so avoid it when a real inverse lockup exists — but a recolor of the *correct* logo always beats shipping the *wrong* company's logo. Never fill the onDark slot from the logo wall.
- **Icons** — extract the page's own `<svg>` icons (match by `<title>`), save to `<staging-kit>/icons.json`, and reuse them verbatim in cards/tiles. Do **not** substitute generic icons. If the site exposes too few icons to lift, pick ONE line-icon set whose stroke weight matches the brand's (`--brand-icon-stroke`) and **flag the substitution** in `brand-kit.md` (*"icons: <set name> — substitution, swap when the brand's own set is available"*). A flagged single-set substitution is fine; a silent mix of lifted + lookalike icons is not.

#### Step 3: Derive the design system

**Scope: visual design only.** Capture colors, typography, layout, spacing, shapes, imagery, icons, motion, and visual usage rules. Copy, messaging, tone of voice, and proof points come from the producing skill and its sources; they are not captured or stored in the brand kit.

Work primarily from the **real CSS (Step 2.5)** — the screenshots only confirm layout and visual truth. Extract:

**3a. Color tokens.** Find the real values, don't guess:
- Inspect the HTML for CSS custom properties (`--color-*`, `:root` blocks), inline `style` colors, `background`, `color`, `border`, `fill`/`stroke`, gradient stops, and `box-shadow` colors.
- Pull button/link/highlight colors from their actual rules; confirm against the screenshot.
- Resolve into named roles. Capture the hex (and rgba where opacity matters):
  - `bg` / `bg-alt` (page + alternating section backgrounds)
  - `surface` (card background), `surface-dark` (dark-section card)
  - `ink` (primary text), `muted` (secondary text), on-dark text color
  - `primary` (main brand/CTA color) + `primary-ink` (text on primary)
  - `accent` / `highlight` (used to emphasize words, links, underlines)
  - `border`, `border-soft`
  - semantic: `positive` / `negative` (for ✓/✕ comparisons) if present, else derive tasteful defaults from the palette
  - any signature gradient(s) — record the full `background:` value
- Note whether the brand has a **dark hero/footer** treatment (very common) and capture that as a `band` token set.

**3b. Typography.**
- Font families (heading vs body) from `font-family`. Note the web-font source if linkable (Google Fonts name, or a CDN/`@font-face` URL) so other skills can `<link>` it; otherwise pick the closest common fallback and say so.
- Type scale: H1/H2/H3/body/eyebrow sizes, weights, letter-spacing, line-height (read from the article page especially).
- Heading style signals: tight tracking? highlighted words in an accent color? all-caps eyebrows?

**3c. Shape & depth.**
- Border radius scale (buttons, cards, pills) — read actual `border-radius`.
- Shadow style (soft/elevated/none) — read `box-shadow`.
- Spacing rhythm (section padding, card padding, gap) — approximate a 4/8px scale.
- Button anatomy: pill vs rounded-rect, has-arrow-icon, fill vs outline vs ghost, size.

**3d. Component inventory.** Identify which of these the brand uses and how it styles each: buttons (primary/secondary/tertiary), badge/pill/eyebrow, card (plain + icon-tile), icon tile, section header (eyebrow + title + highlight + subtitle), hero/banner band, stat/metric block, comparison/feature table, quote/testimonial, checklist, CTA block, footer/brand bar, logo/wordmark treatment.

Quote a concrete observation for each major token (e.g. *"primary CTA is a pill in the brand's accent color, radius 999px, with a trailing arrow"*) so the kit is grounded, not invented.

#### Step 4: Write `tokens.css`

The reusable core. A single `:root` block plus a web-font `@import`/comment. Use neutral, brand-agnostic token NAMES (so consuming skills reference the same names across brands) with this brand's VALUES. Template:

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
  /* emphasis mechanism — how key words stand out (color / weight / size / decoration / none).
     NOTE: these short names are what kit_base.css and the render contract consume — do not
     write long-form variants (emphasis-ink-on-light); they will silently not render. */
  --brand-emph-ink-light: <hex or `inherit` if not color-based>;
  --brand-emph-ink-dark: <hex or `inherit`>;
  --brand-emph-underline: <linear-gradient(...) underline bar | none>;
  --brand-emph-underline-dark: <dark-surface underline or none>;
  --brand-emph-weight: <weight of emphasized words | inherit if emphasis is color-only>;

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
  /* texture — a subtle pattern layered above the glow on dark bands (--brand-hero-texture for light heroes). Recipes below. */
  --brand-texture: <dot grid | line grid | grain | none>;

  /* ---- foundations (capture the brand's scales, not just one value each) ---- */
  /* full neutral ramp — brands define 50→950; collapsing to 3 greys loses fidelity */
  --brand-gray-50: <hex>; --brand-gray-100: <hex>; --brand-gray-200: <hex>;
  --brand-gray-300: <hex>; --brand-gray-400: <hex>; --brand-gray-500: <hex>;
  --brand-gray-600: <hex>; --brand-gray-700: <hex>; --brand-gray-800: <hex>;
  --brand-gray-900: <hex>; --brand-gray-950: <hex>;
  /* brand-hue tint ramp — brands ship their primary at several tint stops for
     soft fills, borders, and washes; collapsing to one hex loses the system */
  --brand-primary-90: <hex>; --brand-primary-60: <hex>;
  --brand-primary-30: <hex>; --brand-primary-10: <hex>;
  /* accent AS TEXT — if the accent fails contrast as text (common for neon/pastel
     accents), capture the brand's readable stand-in; else repeat the accent */
  --brand-accent-text: <hex legible at 4.5:1 on --brand-bg>;
  /* focus ring — for interactive output (microsites); read the brand's :focus rule
     or derive a 3px ring from the accent at ~45% alpha */
  --brand-focus-ring: <e.g. 0 0 0 3px rgba(...,.45)>;
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

**Light/dark theme pairing.** If the brand ships *both* a light and dark theme (common — Grafana, many dev tools), capture both. Put the default mode in `tokens` and the opposite-mode overrides in `manifest.render.tokensDark` (or `tokensLight`) — only the tokens that differ. The renderer's `--theme light|dark` merges them, so one kit renders either mode. (A brand that is inherently single-mode — e.g. all-dark — just uses `tokens`.)

`kit_base.css` consumes the new scales where they change output: elevation (`shadow-sm/md/xl`), motion (button/card transitions + `prefers-reduced-motion`), icon stroke, and **responsive breakpoints** (grids stack and gutters shrink ≤720px). The ramp / spacing / semantic / gradient tokens are captured as kit metadata and used by components/exports that need them. All are additive with fallbacks, so kits missing them still render.

#### Step 5: Write `components.html` (the template reference library)

A **self-contained** HTML file (inlines the tokens from Step 4 — no external CSS dependency, web fonts via `<link>` allowed) that renders the **minimal component kit**. This is both a visual reference AND a copy-paste source for other skills. For each component show a **live preview** and, directly beneath it, the **HTML snippet** in a `<pre><code>` block.

Build these components, styled with the brand's tokens, **composition, and depth**. Atoms aren't enough — a kit of correctly-colored buttons on a cramped flat page still reads as "AI slop." Include the layout primitives:

*Composition primitives (the part that makes it look designed):*
1. **Section shell** — the reusable section wrapper with the brand's **generous vertical padding** and **centered header** (eyebrow → balanced heading w/ one highlighted word → muted subhead). Everything else sits inside this rhythm.
2. **Hero** — reproduce the source’s actual surface, spacing and motif. Include glow/graphics only where observed; a minimal flat hero is valid. Big confident heading + primary CTA.
3. **Section band** — use the source’s surface/radius treatment, including a plain band when that is the observed design.

*Atoms & blocks:*
4. **Buttons** — primary, secondary, tertiary/ghost (real anatomy: pill/rect, arrow, size).
5. **Badge / Pill / Eyebrow** — the small label treatment (match case — many brands are sentence-case, not all-caps).
6. **Card** — plain + a card with an **icon tile** (real size, gradient/tint, and any **glow** shadow the brand uses).
7. **Gradient-border element** — if the brand uses gradient borders / glowing chips, include one.
8. **Stat / metric block**, **Comparison ✕-vs-✓**, **Quote**, **Checklist**, **CTA band**, **Footer / brand bar** — each in the brand's treatment.
9. **Color + type swatches** — token reference at the top, headings rendered at their **real large sizes**.

Faithful over minimal — it's a kit, not a clone of the whole site, but it must capture the brand's *spacing, hierarchy, and depth*, not only its colors. **Inline the real logo SVG** saved in Step 2.5 (downloaded, not hotlinked) and the brand's **real icons** from `icons.json` — do not recreate the wordmark as plain text or swap in lookalike icons. Match the real font weight, button anatomy, and signature treatments (highlight underline, gradient tiles). Add `print-color-adjust: exact` on dark bands so the components survive PDF export when reused in print collateral.

#### Step 6: Write `manifest.json`

Machine-readable summary so other skills can discover and load the kit programmatically:

```json
{
  "schemaVersion": 1,
  "canonicalDomain": "<full-normalized-hostname>",
  "workspaceOId": "<verified-workspace-id>",
  "sourceUrls": ["<source-url>"],
  "capturedAt": "<ISO-timestamp>",
  "allowedUse": {"logos": "<verified-use>", "fonts": "<embedding-license-or-fallback>"},
  "assetChecksums": {"<relative-file>": "<sha256>"},
  "slug": "<display-alias>",
  "company": "<Company Name>",
  "domain": "<domain>",
  "generated": "<YYYY-MM-DD>",
  "pages": ["/", "/product", "/pricing", "..."],
  "fonts": { "heading": "<name>", "body": "<name>", "link": "<webfont url or null>",
             "status": { "heading": "embedded|webfont|fallback", "body": "..." } },
  "tokens": { "primary": "<hex>", "accent": "<hex>", "bg": "<hex>", "ink": "<hex>", "band": "<value>" },
  "hasDarkBand": true,
  "buttonStyle": "pill-with-arrow",
  "sectionOrder": ["hero", "logos", "features", "quote", "stats", "cta", "footer"],
  "rules": ["<hard guardrail 1 — see Step 7 Guardrails>", "<hard guardrail 2>"],
  "files": { "tokens": "tokens.css", "components": "components.html", "spec": "brand-kit.md" },
  "render": { "...": "the machine token contract the renderer consumes — see 'Generating collateral from a kit'" }
}
```

- **`fonts.status`** flags substitutions honestly: `embedded` (real files base64'd), `webfont` (real face via `<link>`), `fallback` (closest free face — name it). A consumer can then decide whether a fallback face is acceptable for a given asset.
- **`sectionOrder`** is the homepage's actual section grammar (what follows what). Consuming skills mirror it when composing multi-section assets — the *order* of a brand's page is as recognizable as its palette.
- **`rules`** carries the kit's 2–3 hard guardrails in machine-readable form (mirrors `brand-kit.md` → Guardrails).

**Always include the `render` block** (the renderer's contract): `hasDarkBand`, `docWidth`, `heroVisual`, `webfonts`, `fonts[]`, `logo{onDark,onLight,lockup}`, and the full `--brand-*` `tokens` map. Without it the kit is viewable but not renderable into collateral. See *Generating collateral from a kit* for the field list.

#### Step 7: Write `brand-kit.md`

Human-readable spec + usage guide. Sections:

```markdown
# Brand Kit: <Company> (<domain>)

**Source pages:** <list>
**Generated:** <date>

## Brand at a glance
<2–3 sentences: the visual personality — e.g. "Dark, technical, modern. Mint-on-navy with electric-blue highlights. Tight, confident headings; clean white content sections.">

## Color tokens
<table: token name | hex | role / where used>

## Typography
<heading + body fonts, scale, AND the **emphasis mechanism** — exactly how key words are emphasized (color? weight? size? underline/wash/gradient-text? none?), with light/dark variants. Be explicit so consumers don't bolt on a device the brand doesn't use.>

## Shape & depth
<radius, shadow, spacing rhythm, button anatomy>

## Components
<one line per component on what's distinctive about the brand's version. Where a component has a
non-obvious usage rule, say it here in one clause — e.g. "accent button: at most one per view">

## Page anatomy
<the homepage's section order (matches manifest.sectionOrder) + one line on rhythm —
e.g. "dark hero → logo strip → 3 alternating feature splits → quote → CTA band">

## Signature moves
<2–4 things that make output unmistakably this brand — e.g. "highlight one key word per heading in --brand-accent", "dark hero + dark footer bands", "icon tiles in a tinted rounded square">

## Guardrails (rules to never break)
<distill the 2–3 visual design rules a generator is MOST likely to violate for this brand — the accent-vs-flood
rule, a headline-face-only rule, a "this brand never uses gradients/underlines/glows" rule.
State each as a prohibition with the correct alternative. Mirror them into manifest.rules.
If `corrections.md` exists, its entries are guardrails too — read both.>

## Using this kit in other skills
<the consumption guide — see the section below>
```

**`corrections.md` — the learned-constraints file.** When a user corrects the visual design of branded output ("stop using glow circles", "never put the logo on the accent color"), append the rule there (one bullet: the prohibition + the correct alternative + date) instead of only fixing the one asset. Every consumer reads it alongside the guardrails, so a correction sticks across future runs instead of being re-discovered per asset. Keep it to visual design rules learned *in use*; observed-at-capture rules belong in Guardrails.
