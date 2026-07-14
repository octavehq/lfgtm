---
name: get-brand-components
description: Capture a brand's visual design system from its website and build a reusable component kit. Walks key pages on a domain (screenshots + HTML via the Octave scrape tool), derives design tokens (colors, type, spacing, radius, shadow), and produces a minimal component library (buttons, cards, headers, stats, tables, badges, hero, footer) as a self-contained HTML reference plus CSS tokens. Use when the user says "get brand components", "capture the brand", "build a component kit for [domain]", "make outputs look like [company]", wants other skills to generate on-brand HTML for a target company, or wants to reuse an already-published brand kit from the asset store or host/share a kit as a live link (via asset-manager).
argument-hint: <domain-or-url> [refresh] | list | show <slug> | export <slug> | delete <slug>
---

# Get Brand Components — Brand-to-Component-Kit Builder

Walks the key pages of a target website, captures screenshots and HTML, derives the brand's design system (colors, typography, spacing, components), and produces a **reusable component kit**: design tokens (`tokens.css`), a self-contained component gallery (`components.html`), a machine-readable manifest (`manifest.json`), and a human-readable spec (`brand-kit.md`). Other skills (one-pagers, microsites, battlecards, decks, two-pagers) load this kit to generate outputs that look and feel like the target brand.

## When to Use

- User wants to make generated HTML (one-pagers, microsites, decks, battlecards) look like a specific company's brand
- User provides a domain and asks to "capture the brand", "get the components", or "build a design kit"
- User wants a reusable, on-brand component library before producing a batch of branded collateral
- Another skill needs brand tokens/components for a target company and none are saved yet

## Usage

```
/octave:get-brand-components <domain-or-url>     # Walk the site and build a brand component kit
/octave:get-brand-components <domain> refresh    # Force a fresh re-walk, overwriting the cached kit
/octave:get-brand-components list                # List saved brand kits
/octave:get-brand-components show <slug>         # Display a saved kit (and open the gallery)
/octave:get-brand-components export <slug>       # Zip the cached kit to ~/Desktop/<slug>-brand-kit.zip
/octave:get-brand-components delete <slug>       # Remove a saved kit
```

`<domain-or-url>` accepts `acme.com`, `https://www.acme.com`, or `https://www.acme.com/product` (a specific seed URL).

### Cache-first (reuse by default)

Kits are **cached** at `~/.octave/brands/<slug>/` and **reused by default** — building a kit costs scrape credits + time, so don't rebuild what you already have. When a kit for the domain already exists, the default action is to **load and reuse it** (summarize + open the gallery), NOT re-walk the site. Re-walk only when the user explicitly asks (`refresh`, "rebuild", "re-scrape") or the kit is clearly stale. This applies whether the skill is called directly or by another skill needing the brand: **check the cache first, reuse on hit, only build on miss.**

## Storage

Brand kits are stored under `~/.octave/brands/<slug>/`:

```
~/.octave/brands/<slug>/
  brand-kit.md        # Human-readable design system spec + usage guide
  tokens.css          # :root design tokens (the reusable core)
  components.html     # Self-contained component gallery (live previews + snippets)
  manifest.json       # Machine-readable: slug, domain, pages, tokens summary, date
  <slug>-logo.svg     # Real logo, downloaded + inlined (not hotlinked)
  icons.json          # Real page icons lifted verbatim {name: {viewBox, inner}}
  fonts/              # Real webfont files (.woff2/.woff) for base64 @font-face embedding
  images/             # Real product screenshots + customer logos (for split/logos blocks)
  screenshots/        # Reference PNGs of the walked pages
```

`<slug>` is the registrable domain, lowercased and hyphenated (e.g. `acme.com` → `acme`, `acme-corp.io` → `acme-corp`).

## Tooling

**Primary capture tool — the Octave `scrape_website` MCP tool:**
- Returns page content as `html` or `markdown`, and optionally a full-page screenshot.
- For brand work always call with `format: "html"` and `includeScreenshot: true` — you need both the DOM (for colors, fonts, structure, real class names) and the rendered visual (for layout, gradients, button shape, spacing rhythm the DOM hides).
- Charges 1 credit per successful scrape. Returns `found: false` (no charge) when a page is unreachable — keep the page count tight (≤ 6 pages).
- The result may include a `screenshotUrl` (a signed URL). When present, persist it to `screenshots/` with `curl` so the kit has reference images.

**Fallback when the Octave MCP scrape tool is unavailable:** use `WebFetch` for text/HTML only and tell the user *"No screenshot capture available — the kit is derived from HTML only, so visual fidelity (gradients, spacing, button shape) is lower. Connect the Octave MCP server for screenshot-backed analysis."* Still produce the kit.

### ⚠️ The fidelity bar — mirror, don't approximate

The whole value of this skill is that output looks like it came **off the page**, not "close-ish." A designer at the target company will instantly reject tasteful recreations as "AI slop." So the rule is: **lift the brand's REAL atomic elements, never eyeball them.**

- Get the **real CSS** (exact button fill / radius / shadow, real font family, real type scale) by fetching the stylesheet bundle — see Step 2.5. Do not infer colors from a screenshot when the CSS has the exact hex.
- Use the brand's **own SVG icons and logo**, lifted verbatim from the page (Step 2.5) — not lookalike icons or a re-typed wordmark.
- Mirror **real component anatomy** (their actual card/button/heading structure and the real font *weight* — many brands use medium-weight display type, not bold).
- Only fall back to a guess when something is genuinely unextractable, and say so explicitly in `brand-kit.md`.

---

## Instructions

### Subcommand: (default — build a kit)

#### Step 1: Resolve the target and plan the crawl

1. Normalize the input to a base URL (`https://www.<domain>` if only a bare domain is given; keep an explicit URL as the seed).
2. Derive the `<slug>` from the registrable domain.
3. **Cache check (do this first).** If a kit already exists at `~/.octave/brands/<slug>/` (has `manifest.json`), **reuse it by default**: print a one-line summary from `manifest.json`, `open` the gallery, and **stop — do not re-walk or spend scrape credits.** Only proceed to Step 2 when the user passed `refresh` (or explicitly asked to rebuild/re-scrape), or the kit is missing/partial/stale. Mention they can pass `refresh` to rebuild.
4. **Asset-store fallback (on local miss only).** No local kit? Before spending scrape credits, check whether this kit was already published as a hosted asset — **by you or a workspace teammate** (workspace-shared assets appear in the list with their `owner`). If the Octave MCP asset tools aren't available, skip this silently and continue to Step 2.
   - Run the `assets_list` MCP tool — an **actual tool call**, never a bash/python simulation, and never "assume" its result. If the `assets_list` result is not in your transcript, this check did not happen and you may not proceed to Step 2. Look for identifier `<slug>-brand-kit` — exact first, then fuzzy (identifier or description containing the slug/company name plus "brand").
   - **Match found** → tell the user: *"A brand kit for <domain> is already published (owner: <me | teammate name>): <link>"* and ask (AskUserQuestion): **Use it (Recommended)** — download it as the local cache — or **Rebuild fresh** — walk the site anyway.
     - *Use it*: follow the asset-manager download workflow in [`../asset-manager/SKILL.md`](../asset-manager/SKILL.md) — mint the token, then `download-artifact.sh --uuid <uuid> --out "${TMPDIR:-/tmp}"` (files land in `${TMPDIR:-/tmp}/<identifier>/`, where `<identifier>` is the matched asset's actual identifier — for a fuzzy match it may not be exactly `<slug>-brand-kit`). **Only if the download exits 0 and `${TMPDIR:-/tmp}/<identifier>/manifest.json` exists**, promote it: `mkdir -p ~/.octave/brands && rm -rf ~/.octave/brands/<slug> && mv "${TMPDIR:-/tmp}/<identifier>" ~/.octave/brands/<slug>` (the `mkdir -p` is required on a fresh machine — `mv` will not create the parent). If the download failed or `manifest.json` is missing, leave `~/.octave/brands/` untouched and continue to Step 2. Then treat it exactly like a local cache hit: summarize, open the gallery, **stop** — no scrape credits spent. Update the asset-manager registry per its rules.
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

Skip pages that 404 or duplicate a pattern you already have. Aim for coverage of distinct component types, not page count. Report progress:

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
mkdir -p ~/.octave/brands/<slug>/screenshots
curl -s "<screenshotUrl>" -o ~/.octave/brands/<slug>/screenshots/<page-slug>.png
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
  - Pull each `@font-face` `src:url(...)` for the heading family from the CSS (`grep -oE "@font-face\{[^}]*}" all.css | grep -i <family>`), `curl` the `.woff2`/`.woff` into `~/.octave/brands/<slug>/fonts/`, then **base64-embed it** as an `@font-face` with a `data:` URL in `tokens.css` / the output `<style>`. Example:
    ```bash
    curl -s -A "$UA" "https://www.<domain>/_next/static/media/<hash>.woff" -o ~/.octave/brands/<slug>/fonts/<family>-<wght>.woff
    B64=$(base64 -i ~/.octave/brands/<slug>/fonts/<family>-<wght>.woff)   # embed as: @font-face{font-family:'<Family>';src:url(data:font/woff;base64,$B64) format('woff');font-weight:...;font-display:swap}
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

- **Logo** — find `<img alt="…Logo">` or the nav logo `<svg>`; `curl` it to `~/.octave/brands/<slug>/` and inline it. **Capture BOTH lockups:** the dark-text version for light backgrounds AND the white/light version for dark bands (look for `logoFullWhite`, `logo-white`, the nav logo on a dark hero, etc.). Use the right one per surface.
  - **Never recolor a raster logo with `filter:brightness(0) invert(1)`** — it flattens a detailed/colored mark into a featureless white blob. Fetch the brand's actual inverse lockup instead.
  - **VERIFY the asset is actually this brand.** CDN buckets (Webflow, Framer, etc.) routinely contain *stale or wrong* assets — a predecessor brand's mark, a customer/client logo, a placeholder. Render the downloaded logo and eyeball it before using it. (This bites in practice: a bucket may host a file named like the white logo that is actually a *previous brand's* mark; Framer sites often reuse `alt="logo"` for many *client* logos in social-proof rows — none of which are the brand.) When the nav logo is ambiguous or you keep pulling client logos, the **favicon / `og:image`** is usually the reliable brand mark — and `og:image` often shows the full lockup. Prefer the asset actually rendered in the live nav, confirmed by eye.
- **Icons** — extract the page's own `<svg>` icons (match by `<title>`), save to `~/.octave/brands/<slug>/icons.json`, and reuse them verbatim in cards/tiles. Do **not** substitute generic icons.

#### Step 3: Derive the design system

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

The reusable core. A single `:root` block plus a web-font `@import`/comment. Use neutral, brand-agnostic token NAMES (so consuming skills reference the same names across brands) with this brand's VALUES. Use the full token template in [references/tokens-template.md](references/tokens-template.md) — it covers color roles, type (families, sizes, exact weights, the emphasis mechanism), shape (radii, shadows, the button size scale), layout & rhythm, depth (glow, gradient borders, texture), and the foundations (neutral ramp, semantic states, spacing/elevation scales, motion, icon stroke, signature gradients).

**Light/dark theme pairing.** If the brand ships *both* a light and dark theme, capture both: default mode in `tokens`, opposite-mode overrides in `manifest.render.tokensDark` (or `tokensLight`) — only the tokens that differ. The renderer's `--theme light|dark` merges them, so one kit renders either mode.

#### Step 5: Write `components.html` (the template reference library)

A **self-contained** HTML file (inlines the tokens from Step 4 — no external CSS dependency, web fonts via `<link>` allowed) that renders the **minimal component kit**. This is both a visual reference AND a copy-paste source for other skills. For each component show a **live preview** and, directly beneath it, the **HTML snippet** in a `<pre><code>` block.

Build these components, styled with the brand's tokens, **composition, and depth**. Atoms aren't enough — a kit of correctly-colored buttons on a cramped flat page still reads as "AI slop." Include the layout primitives:

*Composition primitives (the part that makes it look designed):*
1. **Section shell** — the reusable section wrapper with the brand's **generous vertical padding** and **centered header** (eyebrow → balanced heading w/ one highlighted word → muted subhead). Everything else sits inside this rhythm.
2. **Hero with depth** — the dark/signature band built with the real **glow** layers AND a graphic element (floating product chips, a gradient-bordered mini-graphic, or the brand's hero motif) — never a plain flat rectangle. Big confident heading + primary CTA.
3. **Dark rounded band** — a `--brand-radius-section` container with glow, used to break up white sections and add rhythm.

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
  "slug": "<slug>",
  "company": "<Company Name>",
  "domain": "<domain>",
  "generated": "<YYYY-MM-DD>",
  "pages": ["/", "/product", "/pricing", "..."],
  "fonts": { "heading": "<name>", "body": "<name>", "link": "<webfont url or null>" },
  "tokens": { "primary": "<hex>", "accent": "<hex>", "bg": "<hex>", "ink": "<hex>", "band": "<value>" },
  "hasDarkBand": true,
  "buttonStyle": "pill-with-arrow",
  "files": { "tokens": "tokens.css", "components": "components.html", "spec": "brand-kit.md" },
  "render": { "...": "the machine token contract the renderer consumes — see 'Generating collateral from a kit'" }
}
```

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
<one line per component on what's distinctive about the brand's version>

## Signature moves
<2–4 things that make output unmistakably this brand — e.g. "highlight one key word per heading in --brand-accent", "dark hero + dark footer bands", "icon tiles in a tinted rounded square">

## Using this kit in other skills
<the consumption guide — see the section below>
```

#### Step 7.5: Fidelity gate — score the output against the source (the "indistinguishable" bar)

Don't ship blind. Render the output and **score it against a source screenshot on a fixed rubric** — this turns "looks close-ish" into a measurable gate. Applies to BOTH the kit's `components.html` AND any collateral generated from the kit (two-pagers, case studies, etc.).

**1. Render.** Use the bundled helper (don't rewrite a screenshot script each time — paths relative to this skill's directory):
```bash
python3 scripts/render.py --file <output.html> --out /tmp/out.png
# need a source frame too?  python3 scripts/render.py --url https://<domain>/ --out /tmp/src.png
```

**2. Score.** View the rendered PNG next to a source screenshot (Step 2) and grade each dimension **0–5** (5 = indistinguishable from the brand). Be a harsh critic — this is the step that catches "AI slop" before the user does.

| # | Dimension | 5 = | Common miss (0–2) |
|---|---|---|---|
| 1 | **Typography** | real face + right weight + tracking | fallback font / bold where brand is medium |
| 2 | **Color/palette** | exact hexes in the right roles | approximated or off-role colors |
| 3 | **Emphasis** | brand's actual mechanism (color/weight/size) | a borrowed underline/wash the brand never uses |
| 4 | **Contrast/legibility** | every line ≥ AA on its bg | accent text on a dark band, muddy wash |
| 5 | **Spacing & padding** | airy rhythm; **symmetric gutters**; floating bands clear of edges on ALL sides | cramped; flush-to-edge band (e.g. footer jammed into the sheet's bottom corner); uneven L/R/top/bottom padding |
| 6 | **Depth** | brand's real treatment (glow/shadow/imagery) | flat rectangles |
| 7 | **Edges/containers** | rounded to the brand's radii | hard full-bleed corners |
| 8 | **Logo/assets** | correct lockup, right brand, right surface | wrong/stale asset, filter-recolored blob, missing |

Report a compact scorecard + an **overall /40** (≈ /100), and for every dimension < 4 give a **specific fix** ("heading rendered in a fallback face — embed the real woff2"; "comparison ✓ uses a mid-tone accent on a dark band — flip to the on-dark variant"). **Pass: ≥ 85% (≈ 34/40) AND no dimension below 3.** A wrong/missing logo (dim 8 = 0) is an automatic fail regardless of total.

**3. Present the scorecard, then ASK the user how to proceed** (default behavior — do not silently auto-fix or silently skip). Show the compact scorecard + per-dimension fixes, then offer:
- **Auto-fix loop** — apply the fixes, re-render, re-score; repeat until it passes (≥85%, no dim <3) or hits the max-iteration cap (default 3); then surface the final scorecard. If still failing at the cap, stop and report what's blocking.
- **I'll fix specific ones** — user picks which deltas to apply.
- **Ship as-is** — accept the current output.

The user can also set a standing preference per run ("always auto-fix", "skip the critique entirely") — honor it for that session. But absent that, **ask**.

#### Step 8: Present and confirm

1. Open the gallery so the user can see it (macOS): `open ~/.octave/brands/<slug>/components.html`
2. Summarize: the palette (with hex), fonts, the signature moves, and the files written.
3. Confirm: **"Brand kit saved to `~/.octave/brands/<slug>/`. Other skills can now generate on-brand output for <Company> — or run `/octave:get-brand-components show <slug>` to view it."**

#### Step 8.5: Offer to host / share the kit (asset-manager)

The kit is built and reviewed — offer to publish it so it's reachable by link and reusable as a cache by future runs (Step 1.4). If the Octave MCP asset tools aren't available, skip the offer and mention `export <slug>` as the offline alternative.

1. Ask (AskUserQuestion): **"Host this brand kit as a shareable asset?"** — options: `Host for the workspace (Recommended)` ("teammates can find, open, and reuse it") / `Host it (public link)` / `Not now`.
2. On host, hand off to the asset-manager publish workflow in [`../asset-manager/SKILL.md`](../asset-manager/SKILL.md) — it owns the token lifecycle and the registry — with these prefills (still user-confirmable per that skill's flow):
   - Identifier suggestion: **`<slug>-brand-kit`**. Description: *"Brand component kit for <Company> (<domain>) — design tokens, component gallery, fonts, and logo"*.
   - `--type website --entry-point components.html --status published`; `--privacy` from the choice above (**recommend `workspace`** — that is what lets teammates find and reuse the kit instead of rebuilding it; `public` only when the user wants an open link).
   - Source: a staged copy WITHOUT the heavy `screenshots/` rebuild artifacts (keeps the upload well under the size cap):
     ```bash
     STAGE="${TMPDIR:-/tmp}/<slug>-brand-kit" && rm -rf "$STAGE" && \
       cp -R ~/.octave/brands/<slug> "$STAGE" && rm -rf "$STAGE/screenshots"
     ```
     then upload the staged folder with `zip-and-upload-artifact.sh`.
3. If Step 1.4 found this kit already hosted (or the upload returns 409): offer to **update the existing hosted kit** instead — `update-artifact.sh --uuid <uuid> --src "$STAGE"` (full replace) — never create a duplicate. Only possible when the hosted kit is YOURS (`owner: "me"`); a teammate-owned kit is read-only — publish your own copy.
   The entire hosting step is **2 MCP tool calls + the one-line staging + one upload command** (see the asset-manager skill's "Exact Publish Sequence"). More shell than that means you're doing it wrong.
4. If someone OUTSIDE the workspace needs the kit → asset-manager's share flow (emails and/or allowed domains; the one-time share URL goes into its registry).
5. Report the final link: the live site URL (public — anyone; workspace — teammates verify their work email once), plus the `preview:` link for a zero-friction internal open, plus any share URL for people outside the workspace.

---

### Subcommand: list

1. List directories under `~/.octave/brands/`.
2. For each, read `manifest.json` and show a table: Company | Domain | Pages | Primary color | Generated.
3. If none: "No brand kits saved yet. Run `/octave:get-brand-components <domain>` to build one."

### Subcommand: show <slug>

1. Resolve `<slug>` (exact then fuzzy match against directory names).
2. Print the `brand-kit.md` spec and the token summary from `manifest.json`.
3. `open ~/.octave/brands/<slug>/components.html` (macOS) so the user sees the gallery.
4. Offer: **"Want to refresh this kit from the live site, or use it to generate something on-brand?"**

### Subcommand: export <slug> [dest]

Zip a cached kit so it can be shared / handed to a designer. Self-contained (fonts, logo, components all inline).

1. Resolve `<slug>` (exact then fuzzy match against `~/.octave/brands/`). If missing, offer to build it first.
2. Optionally drop a fresh rendered preview into the kit: screenshot `components.html` headless to `screenshots/components-preview.png` (skip if Playwright isn't available).
3. Zip the kit directory to the destination (default `~/Desktop`):
   ```bash
   cd ~/.octave/brands && rm -f "<dest>/<slug>-brand-kit.zip" && \
   zip -r -X "<dest>/<slug>-brand-kit.zip" "<slug>" -x '*.DS_Store'
   ```
4. Confirm with the path and a one-line `unzip -l` summary of what's inside (tokens.css, components.html, brand-kit.md, manifest.json, logo, fonts/, screenshots/).
5. Mention: to share as a **live link** instead of a zip, use the hosting offer (Step 8.5) or `/octave:asset-manager`.

### Subcommand: delete <slug>

1. Resolve `<slug>`; show the company name from `manifest.json`.
2. Confirm: **"Delete the brand kit for '<Company>' at `~/.octave/brands/<slug>/`? Type 'yes' to confirm."**
3. Remove the directory and confirm.

---

## Generating collateral from a kit (the renderer)

**The primary way to turn a kit into an on-brand asset is the bundled renderer — do NOT hand-write per-asset CSS.** One engine composes any asset from any kit; the same content spec rendered through a different kit comes out fully on-brand for that brand (validated across multiple brands spanning dark, gradient, and light visual systems).

```bash
# scripts/ is relative to this skill's directory
python3 scripts/render_kit.py --kit <slug|path> --spec <content.json> --out <out.html> \
        [--kit-dir <path>] [--theme light|dark] [--format doc|og|social-square|social-story|email]
```

- `--kit-dir` renders a kit stored anywhere (kits don't have to live in `~/.octave/brands/`).
- `--theme` picks the light or dark palette when the kit carries both (`tokensDark`/`tokensLight`).

### Output formats (optional — ask the user)

The same kit + spec can render to **multiple formats** — the brand kit is format-agnostic, so don't rebuild styling per format. `--format` sets the canvas: `doc` (default page), `og` (1200×630 share image), `social-square` (1080²), `social-story` (1080×1920), `email` (600px width). The *spec* controls content (a short hero/CTA spec makes a clean OG/social image).

**Don't generate format variants by default** — they cost extra renders and the user usually wants just the doc. After producing the main asset, **ask** whether they also want any format variants (e.g. an OG image, a square social tile), and only then render them.

- **`scripts/render_kit.py`** — loads the kit, emits a self-contained HTML doc: `<style>` = `:root{}` from `manifest.render.tokens` + base64 `@font-face` from `manifest.render.fonts` + `assets/kit_base.css`; body = composed blocks; logo/icons inlined.
- **`assets/kit_base.css`** — brand-AGNOSTIC component stylesheet (every rule references a `--brand-*` token). This is the single source of truth for component CSS — fix a component once here and every asset for every brand inherits it.
- **Content spec** (JSON) — `{ title, blocks: [...] }`. Block types: `hero`, `stats`, `about`, `quote`, `section`, `features`, `comparison`, `checklist`, `cta`, `footer`, plus the imagery/marketing blocks:
  - **`split`** — image-paired feature row: `{kicker, heading, paras[], bullets[], image, imageSide: left|right, cta}`. The `image` is a kit-relative path (inlined) or URL; it's framed (rounded + shadow).
  - **`logos`** — logo wall: `{label, mono: bool, items:[{img}|{text}]}`. `mono` greyscales color logos for a uniform wall.
  - **`pricing`** — plan cards: `{plans:[{name, price, period, blurb, cta, features[], featured, badge}]}`; the `featured` plan gets the primary border + badge.
  - Any content block can take `surface: "dark"` to render as a full-bleed dark band (e.g. a logo wall with white logos).
  - Emphasis: wrap a word in `**double asterisks**`. `hero.featured.logoKit` pulls *another* kit's logo (customer logo in a vendor case study).
- **Real imagery** — store the brand's actual product screenshots / customer logos in the kit's **`images/`** dir (downloaded during the walk) and reference them by relative path; the renderer inlines them as data-URIs (self-contained). Don't fake imagery with gradient placeholders when the real assets exist on the site — extract logo walls and a hero/product shot. (Apply the same logo-verification care: confirm a "customer logo" is real, not a stray asset.) Optional `--brand-texture` token layers a subtle pattern (dot/grid) onto dark bands.

### Imagery is earned, not defaulted

Place a kit's screenshots and logos only where they **truthfully illustrate the specific point** — never because the kit happens to have them. A product shot dropped into a `split` whose copy describes something the screenshot doesn't show, or a logo wall stamped onto every doc (including internal ones like battlecards), reads as filler and undercuts the asset.

- **Screenshots:** use one only when the section is genuinely *about* what it shows, and caption it for what it actually is (e.g. "The Octave platform"), not for the narrative you wish it depicted. If no apt image exists, carry the point with type + icon tiles — don't shoehorn.
- **Proof:** prefer a **specific, true** callout (a named reference customer matching the audience, with the real result) over a generic logo grid. One earned proof beats a wall of logos.
- **Don't destroy brand:** `mono` greyscale / hard inversion can erase a logo's identity — only use it when a uniform wall genuinely serves the layout.
- **Never** use gradient/masonry placeholder tiles as stand-in "content."

The test for every image: *does it make this exact point clearer, or is it decoration the kit made available?* If the latter, cut it. (The earlier "Real imagery" note means *don't fake* imagery with placeholders — it does **not** mean force every real asset into every doc.)

### The `manifest.render` token contract

For a kit to be renderable it needs a `render` block in `manifest.json`:
- `hasDarkBand` (bool — dark hero/footer/CTA vs light), `docWidth`, `heroVisual` (`chips`|`masonry`|`none`), `webfonts` (optional `<link>` URL for fallback faces)
- `fonts`: `[{family, weight, style?, file, format}]` — base64-embedded so output renders the real face
- `logo`: `{onDark, onLight, lockup}` — per-surface logos. **The renderer picks `onDark` on dark surfaces and `onLight` on light ones** (this is what prevents white-logo-on-white-footer). `lockup` = `{mark, markFill, wordmark, wordmarkWeight}` for brands whose logo is a mark + wordmark.
- `tokens`: the `--brand-*` contract — colors (`bg`, `canvas`, `surface`, `surface-dark`, `ink`, `muted`, `faint`, `on-dark`, `primary`/`-ink`, `link`, `border`, `negative`, `band`, `glow`, `tile-bg`/`-ink`/`-glow`, `grad-border`), emphasis (`emph-ink-light`/`-dark`, `emph-underline`, `emph-weight`), type (`font-heading`/`-body`, `weight-*`, `tracking-heading`, `h1`/`h2`), shape (`radius-section`/`-pill`, `shadow`, `btn-shadow`), and the **foundations** (`shadow-sm`/`-md`/`-xl` elevation, `ease`/`duration` motion, `icon-stroke`, gray ramp, semantic states, spacing scale, gradients — see Step 4). `hero-bg`/`cta-bg` add a light-surface wash; `heading-transform` forces all-caps.
- `tokensDark` / `tokensLight` (optional): override maps for the opposite theme, merged when `--theme` is passed.
- `defaultTheme` (optional): `light` | `dark`.

Add `render` when building a kit (Step 6). The verbose `tokens.css` + `components.html` remain the human-readable reference; `render` is the machine contract the engine consumes.

### Fallback (manual compose)
If a one-off needs a layout the block types don't cover, you can still inline `tokens.css` + `assets/kit_base.css` and write markup using the `kit_base` classes — but prefer adding a block type to the renderer over hand-CSS, so the fix compounds.

Reference token names are brand-agnostic, so the same spec restyles to any captured brand just by swapping `--kit`.

## Reviewing an asset (optional)

After producing an asset from a kit, you can run an optional QA pass before delivery — layout, brand adherence, narrative coherence, groundedness, and AI-slop. Offer it; don't force it. The rubric and the slop standard ("write like a human") live in the shared [`../shared/asset-review.md`](../shared/asset-review.md), with its generation-time companion [`../shared/presentation-principles.md`](../shared/presentation-principles.md). The key discipline: **render the output and inspect the pixels** — overflow, misalignment, and white-on-white only show in the render, not the source. (The document skills that consume this kit run this pass automatically.)

## Error Handling

- Create `~/.octave/brands/<slug>/` automatically if missing.
- If the homepage scrape returns `found: false`, retry once with the bare apex domain (`https://<domain>` without `www`), then ask the user to confirm the URL.
- If only some pages are reachable, proceed with what you have and note reduced coverage in `brand-kit.md`.
- If no screenshot capability is available, derive from HTML only and flag the lower visual fidelity (see Tooling).
- Never hotlink remote logo/image assets into the kit — download the real asset and inline it (Step 2.5) so outputs stay self-contained and don't break when the source rotates assets. Only if a real logo genuinely can't be sourced, fall back to the company name as clean text and say so in `brand-kit.md`.

## Notes

- Keep the crawl to ≤ 6 pages — each scrape costs 1 credit, and 5–6 well-chosen pages capture a brand's system. Breadth of *component types* beats page count.
- Ground every token in an observed value; if you must infer (e.g. a missing semantic color), pick from the existing palette and say so in `brand-kit.md`.
- The kit is intentionally **minimal** — a faithful component set, not a full site clone. Other skills compose these primitives.
- Refresh by re-running with the same domain; the directory is overwritten.
