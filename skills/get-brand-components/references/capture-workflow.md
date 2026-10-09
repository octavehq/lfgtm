# Capture workflow and kit contract

Use the [task method](task-method.md) for validation and source fidelity. Build in a unique staging directory. Canonical cache identity is verified workspace ID plus full normalized hostname/TLD; legacy names are aliases only after manifest identity matches. After mechanical and visual checks, use [brand_cache.py](../scripts/brand_cache.py) to promote the capture through an atomic pointer. A failed refresh preserves the prior capture. Consumers resolve `current.json` before reading manifest/assets. Source URLs, capture time, checksums and allowed-use decisions are required for promotion.

Read this reference for capture; it retains the visual extraction and token/component contract. No voice, messaging or proof library belongs in a kit.

## Who runs which step

The skill dispatches the agents in `<plugin-root>/agents/brand-kit/`; a host without delegation runs the same steps in one session, in this order.

| Step | Agent |
|---|---|
| 1 and 2 | `brand-crawler` |
| 2.5 (fonts, palette, emphasis, components, composition) and 3 | `brand-design-analyst` |
| 2.5 (logo, hero imagery, icons) | `brand-logo-verifier` |
| 4, 5, 6, 7 and the checksums | `brand-kit-author`; the skill promotes and marks ready |
| [fidelity gate](fidelity-gate.md) | `brand-kit-judge`, two or three per round; the skill decides the pass and the repair loop |

The analyst, the author and the judge also read [design judgement](design-judgement.md): the source brand is the brief, and a device the site does not use is never added.
## Capture the visual system

#### Step 1: Resolve the target and plan the crawl

1. Identity comes from one place: `python3 <plugin-root>/skills/get-brand-components/scripts/brand_cache.py canonical <domain-or-url> --workspace <id>` prints the canonical domain (lowercase, no `www.`) and the cache root. The seed URL keeps the host as the site serves it (`https://www.<domain>/` is fine); the cache and the manifest never carry `www.`.
2. Derive the `<slug>` from the canonical domain.
3. **Cache check (do this first).** The cache lives at `<brand-cache>/<workspace>/<domain>/` (default `~/.octave/brands/`) behind a `current.json` pointer; run `python3 <plugin-root>/skills/get-brand-components/scripts/brand_cache.py status <brand-cache>/<workspace>/<domain>` to read it. Status `ready` means a kit that passed the fidelity gate: **reuse it by default**, print a one-line summary from its `manifest.json`, `open` the gallery, and **stop — do not re-walk or spend scrape credits.** Status `draft` means a kit that never passed the gate: the capture proceeds to Step 2 for fresh source frames and findings, and the author re-renders the draft as the first candidate instead of building from scratch. Only proceed to Step 2 when the pointer is `missing`, the user passed `refresh` (or explicitly asked to rebuild/re-scrape), or the kit is partial/stale. Mention they can pass `refresh` to rebuild.
4. **Asset-store fallback (on local miss only).** No local kit? Before spending scrape credits, check whether this kit was already published as a hosted asset — **by you or a workspace teammate** (workspace-shared assets appear in the list with their `owner`). If the Octave MCP asset tools aren't available, skip this silently and continue to Step 2. If the tool exists but the call itself fails (connection refused, timeout, auth error), say so in one line ("asset-store check failed: <error>; continuing without it") and continue to Step 2; do not retry in a loop and do not treat the failure as "no match".
   - Run the `assets_list` MCP tool — an **actual tool call**, never a bash/python simulation, and never "assume" its result. If the `assets_list` result is not in your transcript, this check did not happen and you may not proceed to Step 2. Look for identifier `<slug>-brand-kit` — exact first, then fuzzy (identifier or description containing the slug/company name plus "brand").
   - **Match found** → tell the user: *"A brand kit for <domain> is already published (owner: <me | teammate name>): <link>"* and ask (AskUserQuestion): **Use it (Recommended)** — download it as the local cache — or **Rebuild fresh** — walk the site anyway.
     - *Use it*: follow the asset-manager download workflow in [`../../asset-manager/SKILL.md`](../../asset-manager/SKILL.md) — mint the token, then `download-artifact.sh --uuid <uuid> --out "${TMPDIR:-/tmp}"` (files land in `${TMPDIR:-/tmp}/<identifier>/`, where `<identifier>` is the matched asset's actual identifier — for a fuzzy match it may not be exactly `<slug>-brand-kit`). **Only if the download exits 0 and `${TMPDIR:-/tmp}/<identifier>/manifest.json` exists**, promote it: `mkdir -p ~/.octave/brands && rm -rf <brand-cache>/<slug> && mv "${TMPDIR:-/tmp}/<identifier>" <brand-cache>/<slug>` (the `mkdir -p` is required on a fresh machine — `mv` will not create the parent). If the download failed or `manifest.json` is missing, leave `<brand-cache>/` untouched and continue to Step 2. Then treat it exactly like a local cache hit: summarize, open the gallery, **stop** — no scrape credits spent. Update the asset-manager registry per its rules.
     - *Rebuild fresh*: continue to Step 2, but remember the asset's uuid and owner — the closing question (SKILL.md, *Hosting via `/octave:asset-manager`*) then **updates** the hosted kit if it is yours; a teammate-owned kit can't be modified, so you'd publish your own copy instead.
   - **No match** → continue to Step 2 without extra chatter.

#### Step 2: Fetch the pages and build the evidence pack

Pages come from the Octave `scrape_website` tool in full-document mode; `skills/get-brand-components/scripts/prefetch.py` turns them into the evidence pack. Nothing in this step reads page HTML into the conversation: the tool returns a small JSON with hosted URLs, `ingest` downloads them to disk, and `mine` does the extraction.

1. **Fetch the homepage:** `scrape_website({ url: "https://<domain>/", includeScreenshot: true, fullDocument: true })`. The result carries `finalUrl`, `statusCode`, `title`, `links`, `contentUrl` (the full HTML document, hosted) and `screenshotUrl`; the inline `content` is markdown you do not need.
2. **Save it in the same turn** (the `contentUrl` is a signed link that expires after about an hour), passing the tool's JSON result verbatim:
   ```bash
   python3 <plugin-root>/skills/get-brand-components/scripts/prefetch.py ingest --pages-dir evidence/firecrawl - <<'EOF'
   <the JSON result exactly as the tool returned it>
   EOF
   ```
   It downloads the HTML and the screenshot, writes `<slug>.html`, `<slug>.png` and a row in `evidence/firecrawl/firecrawl.json`, and prints the row. Every download the miner makes (pages, stylesheets, fonts, logos, icons, images, video prefixes) goes to public hosts only; loopback, private and link-local addresses are refused, redirects included. A `found: false` result or an error status is recorded as a failed row and reported; carry on with the other pages.
3. **Ask which pages to fetch next:** `python3 <plugin-root>/skills/get-brand-components/scripts/prefetch.py pick-pages --pages-dir evidence/firecrawl` prints up to five same-site URLs, one per line, chosen from the homepage's links in the order a design system is most fully expressed: product / platform / features (cards, grids, icon tiles, stats), pricing (plan cards, badges, comparison rows), a blog / learn / docs article (body type scale, inline links, callouts; a deep slug is preferred over the index), customers / case studies (quotes, logo treatment, stat blocks), about / company (secondary section patterns). Login, legal, careers and file links are skipped.
4. **Fetch every printed URL the same way.** The skill deals them to up to three crawler agents that run in parallel; each page lands as its own row file under `evidence/firecrawl/rows/`, so parallel ingests never lose a row, and `firecrawl.json` is rebuilt from them as a view (hand-written rows there still count). Pages that fail stay failed; the capture continues with the rest. Pages that fail are recorded and skipped by `mine`; do not substitute others by hand. When `pick-pages` prints nothing (a single-page site), continue with the homepage alone: body type then comes from `computed.<home>.p` and `computed.<home>.body`, and the fidelity gate judges the homepage only.
   Assets the site itself declares (a font weight the stylesheet lists, an icon file, a video poster) are fetched with `python3 <plugin-root>/skills/get-brand-components/scripts/prefetch.py fetch-asset --out <dir> <url>...` (same scheme check and size caps as the miner). That is the only extra download the capture makes; there is no page walk with curl.
5. **Build the evidence pack:** `python3 <plugin-root>/skills/get-brand-components/scripts/prefetch.py mine --pages-dir evidence/firecrawl --out evidence/`. It mines the stylesheet bundles for `@font-face` files (resolved against each sheet's URL, hashed next/font family names decoded, one latin face per weight), custom properties, colors by property, gradients, radii, shadows, container widths, button rules and section padding; lifts logo candidates from header, nav, footer and the home link with provenance and a `suspectWall` flag; dedupes inline icons; crops each screenshot (full page, a top frame, 1600 px strips of the homepage plus a dedicated bottom strip so the footer is always judgeable) and samples the hero's dominant pixel colors plus a color band every 300 px. When Playwright and Chromium are installed it also reads computed styles off the rendered homepage and article page: body, h1/h2/h3/p, nav, footer, the real button groups with hover state, the section list, every styled word inside large display text (color, chip, gradient text, weight, face, underline, inline icon), a second homepage frame 4 s later for animated devices, a dark-theme frame when the CSS declares one, and a screenshot for any page the tool returned without one. Without a browser that pass is skipped, `capabilities.playwright` is `false` and `capabilities.playwrightError` says why; `playwrightDisabled: true` means the `--no-playwright` flag was passed, which a capture never does (it exists for tests). Stylesheets served by embedded widgets (chat, meetings, consent) are skipped and their custom properties dropped, so `customProperties` is the brand's own set. If a page arrived without `<head>` the miner recovers it with one plain GET and lists the page in `capabilities.headRecovered`. The result is `evidence/evidence.json` plus `pages/`, `css/`, `fonts/`, `logos/`, `icons.json`, `screenshots/`.

Report progress as the pages land:

```
Walking <domain>…
  ✓ /              (hero, nav, primary CTA)
  ✓ /product       (feature cards, icon tiles)
  ✓ /pricing       (plan cards, comparison table)
  ✓ /learn/post/x  (article typography, callouts)
  ✓ /customers     (testimonials, stat blocks)
Captured 5 pages. Deriving the design system…
```

With the evidence pack, the capture session reads `evidence.json`, views the homepage strips and the pricing and article page tops, verifies two logo files by eye, and writes `manifest.json`, `tokens.css` and `brand-kit.md` (Steps 3, 4, 6, 7). It does not re-walk the site and does not write `components.html`: `skills/get-brand-components/scripts/render_gallery.py <kit-dir>` composes the gallery from `manifest.render` through the shared renderer (always renderable, honors the optional `render.gallery` composition block: per-block `surfaces`, `headingAlign`, `cardStyle`, `navStyle`, `sectionFrame`, and an optional bespoke `hero.html`). Then run the [fidelity gate](fidelity-gate.md).

**Without the tool (manual fallback).** When `scrape_website` is not available on the host, produce the same pages dir with the host browser: for the homepage and the pages you would have picked, save the rendered document (`document.documentElement.outerHTML`) as `evidence/firecrawl/<slug>.html` and a full-page screenshot as `<slug>.png`, write the `firecrawl.json` rows by hand (`url`, `ok`, `status`, `finalUrl`, `title`, `htmlFile`, `screenshotFile`, `links`), then run `mine`. Do not walk the site with curl and do not use web archives. With neither the tool nor a browser, stop and say the capture cannot run.

#### Step 2.5: Read the evidence (the fidelity step — do not skip)

The **exact values live in the stylesheet bundles and the rendered page**, and the miner has already pulled them. Work from `evidence/evidence.json` and the files next to it; do not transcribe a vibe from the screenshots alone, and do not walk the site again (missing declared assets go through `fetch-asset`, Step 2).

**Utility-class sites (Tailwind and friends).** When `capabilities.cssSignal` is `low`, the stylesheet is mostly resets and utilities and says little about the brand: `buttonRules`, `sectionPadding` and `transitions` come back empty or near-empty. The truth is then in `computed.<slug>` (real button anatomy, heading and body weights, section rhythm, emphasis) and in the screenshot strips; read those first and treat the CSS keys below as secondary.

- **Fonts** — `fontFaces` (family, weight, style, the downloaded file under `evidence/fonts/`), `fontFamiliesRanked` and `fontFamilyByContext` (heading / body / button / label). Capture the true family **and weight** for headings vs body (many brands use a **medium-weight** display face for headings — defaulting to bold-700/800 would be wrong; the real weight is in `computed.<home>.h1.fontWeight`). **Then EMBED the real webfont** so output renders pixel-exact instead of in a fallback (a wrong heading face is the #1 "AI slop" tell): copy the downloaded files into `<staging-kit>/fonts/` and list them in `manifest.render.fonts` (`{family, weight, style, file, format}`); the renderer base64-embeds them.
  - **Licensing caveat:** embedding a licensed face is fine for an internal stab / a doc going to the brand owner; for anything redistributed, fall back to the closest free face and say so. Either way keep the real family **first** in the stack so a machine with it installed renders it, with a close free fallback behind. State which path you took in `brand-kit.md`.
- **Component rules** — `buttonRules` (the real button selectors with their declarations), `radii`, `shadows`, `transitions`, `maxWidths`, `sectionPadding`, and `computed.<slug>.buttons` (each button group's measured height, padding, radius, fill, font and hover state). Copy exact `border-radius`, `padding`, `box-shadow`, `background`, inset rings, transitions.
- **Button size scale — capture it, don't ship one guessed size.** Brands define buttons at multiple sizes (sm/md/lg), and the proportions are a strong brand tell. For each size record **height, x/y padding, font-size, corner radius, and icon size** (e.g. sm 32px·r8, md 40px·r12, lg 48px·pill — note that corner radius often grows with size). Note the default size used for primary CTAs and whether CTAs are pill vs the standard rounded-rect. Emit `--brand-btn-{sm,md,lg}-{height,pad,font,radius}` tokens and show all sizes in the gallery.
- **Palette** — `colorsRanked` (usage-ranked hexes), `colorsByProperty` (background / color / border / fill), `gradients`, `customProperties` and `customPropertiesDark`, plus the pixel truth in `pages[].screenshotPalette` (hero, whole page, and a band every 300 px) for surfaces the CSS hides (canvas, video and image heroes). Map the top hits to roles; confirm against the screenshot strips.
- **Emphasis & accent mechanism — figure out *how* the brand emphasizes, don't assume.** `computed.<home>.emphasis` lists every styled word inside large display text with exactly what differs from its heading (color, chip background, gradient text, weight, face, underline, inline icon), and `emphasisLater` catches treatments that cycle in after load. Confirm against the hero strips and identify the actual device(s):
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
  - **Depth treatments** — what stops it being a flat rectangle: radial-gradient **glows** on dark sections, **glow box-shadows** on icon tiles (`box-shadow:0 0 100px #01f846`-style), **gradient borders** (`border-image:linear-gradient(...)` or a mask ring), layered surfaces, and any hero **graphic / floating product chips**. Capture the treatments the source actually uses and reproduce those; a flat dark band is correct when the site is flat, and an invented glow or graphic is a fidelity miss, not a fix.
  - **Texture / pattern** — capture any background *tooth* the brand uses on its bands: dot grids, line/blueprint grids, film grain, mesh-gradient blobs. These read as "premium" and are easy to miss. Set `--brand-texture` (layered above the glow on dark bands; `--brand-hero-texture` for light heroes). Reusable CSS recipes — tint the rgba to the brand:
    - **dot grid:** `radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.4px) 0 0/22px 22px`
    - **line/blueprint grid:** `linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px) 0 0/30px 30px, linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px) 0 0/30px 30px`
    - **film grain:** an inline SVG `feTurbulence` data-URI (`<rect filter=fractalNoise opacity='0.12'>`) — premium tooth on dark/gradient bands
    Tune intensity per type: line/dot grids read at ≈5% alpha, but **grain needs ≈10–14%** (at 6% it's invisible at normal size). Keep it subtle enough not to hurt contrast, and confirm against the source — don't add texture a brand doesn't use.
  - **Edges & containers** — match how the brand *frames* sections. Capture the **section corner radius** (many brands round everything — `~1.5–2.5rem`), whether sections **float on a soft canvas** (rounded sheet/cards) vs full-bleed, and any **curved/wavy dividers** between bands. **Never emit a sharp full-bleed rectangle when the brand rounds its sections** — round the hero/band/footer corners to the section radius (e.g. wrap the doc in a rounded sheet with `overflow:hidden` so even the top hero corners are rounded). Hard right-angle edges against the page are an instant "not from them" tell.
  - **Real type scale at real sizes** — headings are large and confident (often `2.5–4rem`). Scaling them down to ~17px kills the brand feel; keep them big.

**Lift the real assets (download + inline, never hotlink):**

- **Logo** — `logoCandidates` lists every `<img>` and inline `<svg>` candidate from the header, nav, footer and the home link with its `region`, `src` or `viewBox`, the `suspectWall` flag, the saved file under `evidence/logos/`, and `inkLuminance` / `inkSaturation` / `suggestedSurface` (the color of the marks themselves, measured from the rendered SVG when a browser ran: light ink suggests `dark`, dark ink suggests `light`; saturated or gradient marks, mid-tones and `currentColor` marks are `null` because they read on either surface or cannot be measured); `meta` adds the favicon and `og:image`. Copy the chosen files into `<staging-kit>/`. **Capture BOTH lockups:** the dark-text version for light backgrounds AND the white/light version for dark bands (look for `logoFullWhite`, `logo-white`, the nav logo on a dark hero, etc.). Use the right one per surface.
  - **Surface rule: pick by the logo's own ink, use the page region only as a hint.** `suggestedSurface: "light"` (dark marks) is the onLight candidate; `"dark"` (white or pale marks) is the onDark candidate. Regions are not reliable: a site with a photo or video hero carries its white logo in the **header** and its dark logo in a **white footer**, the reverse of the usual pattern. When ink is `null` (a `currentColor` SVG), render it on both surfaces and look. **NEVER take a logo from a "trusted by" / customers / partners / clients / logo-wall container** (`suspectWall: true`) — those are white *customer* logos and are the #1 source of a wrong-company mark. The onDark variant is the one that gets contaminated, because the customer wall is dark and full of white logos.
  - **Wordmark gate — inspect the pixels, not the metadata.** After downloading EACH variant, **Read the image file (the Read tool renders it) and confirm the wordmark reads THIS brand's name.** Manifest metadata is not enough: a kit can record `lockup.wordmark: "Octave"` while the actual file is a WorkSpan logo scraped from the customer wall. A white logo is invisible on a light preview, so the onDark variant must be checked specifically — render it on a dark background. Reject any asset that shows a different company.
  - **Run the verifier before caching:** `bash <plugin-root>/skills/get-brand-components/scripts/verify-logos.sh <staging-kit> --out <staging-kit>/.logo-verify.png` checks the files and aspect ratios, writes a swatch page with onLight on white and onDark on dark, and renders it to the PNG when Playwright is installed (without Playwright pass an `.html` path and open it). Eyeball both cells; each must read the brand's name.
  - **Record provenance.** Store the source URL of each variant in the manifest (`logo.onLightSource`, `logo.onDarkSource`). If a source path or its container class/id contains `customers|partners|trusted|clients|logos`, or points at a different domain than the brand's, treat the asset as suspect and re-source.
  - **Fallback ladder for onDark:** verified footer/nav white lockup → `favicon` / `og:image` (authoritative brand marks) → **controlled recolor of the VERIFIED onLight** as a last resort. A recolor (`filter:brightness(0) invert(1)`) flattens a colored mark, so avoid it when a real inverse lockup exists — but a recolor of the *correct* logo always beats shipping the *wrong* company's logo. Never fill the onDark slot from the logo wall.
- **Hero imagery** — `heroImages` lists the video poster (or, for a poster-less video, a frame grabbed with ffmpeg as `kind: video-frame`), the opening section's large image and `og:image`, saved under `evidence/images/` (the video file itself is recorded by URL only). A brand whose hero is a photo or a video cannot be expressed with tokens: copy the poster or hero frame into `<staging-kit>/images/`, set `manifest.render.heroVisual: "image"` and `heroImage: "images/<file>"`, and give `--brand-hero-scrim` the gradient or tint the site lays over it for legibility. The renderer inlines the file behind the hero copy. Reach for a bespoke `hero.html` only when the *composition* (not the imagery) cannot be expressed.
- **Icons** — `evidence/icons.json` holds the page's own icons, inline `<svg>` elements and `<img src="*.svg">` files alike (name, viewBox, inner markup, `source`, deduped); copy it to `<staging-kit>/icons.json` and reuse them verbatim in cards/tiles. Do **not** substitute generic icons. If the site exposes too few icons to lift, pick ONE line-icon set whose stroke weight matches the brand's (`--brand-icon-stroke`) and **flag the substitution** in `brand-kit.md` (*"icons: <set name> — substitution, swap when the brand's own set is available"*). A flagged single-set substitution is fine; a silent mix of lifted + lookalike icons is not.

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
- **Weights come from evidence, never from defaults.** `--brand-weight-heading` is `computed.<home>.h1.fontWeight` (or the article page's `h2`), `--brand-weight-body` is `computed.<home>.body.fontWeight`; without computed styles, read the weight off the screenshot strips against the downloaded faces. Do not write 600 or 700 because it looks like a heading: a medium display face set bold is the most common fidelity miss.
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
  --brand-weight-h1: <hero heading weight when it differs from section headings, e.g. 300>;
  --brand-weight-h2: <section heading weight when it differs>;
  --brand-weight-body: <e.g. 400>;
  /* the resting primary button has its own tokens; an outline brand sets btn-bg transparent, btn-ink and btn-border to ink */
  --brand-btn-bg: <fill | transparent>; --brand-btn-ink: <text>; --brand-btn-border: <ring color | transparent>;
  --brand-btn-hover-bg: <fill on hover>; --brand-btn-hover-ink: <text on hover>; --brand-btn-weight: <e.g. 500>;
  --brand-btn-bg-dark: <fill on dark bands>; --brand-btn-ink-dark: <text on dark bands>; --brand-btn-border-dark: <ring on dark bands>; /* only when the button inverts on dark surfaces */
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

  /* shape — every component radius chains to --brand-radius, so a square brand sets it to 0 and is done;
     override per role only where the site differs */
  --brand-radius-sm: <px>; --brand-radius: <px>; --brand-radius-pill: 999px;
  --brand-radius-card: <cards, tables, quote, dark footer>; --brand-radius-tile: <icon tiles>; --brand-radius-badge: <pill | 0>;
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

**Light/dark theme pairing.** If the brand ships *both* a light and dark theme (common — Grafana, many dev tools), capture both. Put the default mode in `tokens` and the opposite-mode overrides in `manifest.render.tokensDark` (or `tokensLight`) — only the tokens that differ. The renderer's `--theme light|dark` merges them, so one kit renders either mode. (A brand that is inherently single-mode — e.g. all-dark — just uses `tokens`.) Pick the default from evidence, not taste: `computed.<home>.darkMode` is non-null only when the site honours both schemes. Then `tokens` holds the scheme the homepage served at first paint (the `computed.<home>.body` block: dark if its background is dark, otherwise light), the opposite scheme goes into `tokensDark` or `tokensLight` from the `darkMode` block, and `defaultTheme` is written explicitly. When `darkMode` is null the site is single-mode and `tokens` alone is correct.

`kit_base.css` consumes the new scales where they change output: elevation (`shadow-sm/md/xl`), motion (button/card transitions + `prefers-reduced-motion`), icon stroke, and **responsive breakpoints** (grids stack and gutters shrink ≤720px). The ramp / spacing / semantic / gradient tokens are captured as kit metadata and used by components/exports that need them. All are additive with fallbacks, so kits missing them still render.

#### Step 5: Produce `components.html` (the gallery)

Do not hand-write the gallery. After Step 6 has written `manifest.json` with its `render` block, run `skills/get-brand-components/scripts/render_gallery.py <kit-dir>`: it composes `components.html` from `manifest.render` through the shared renderer (`render_kit.py` + `skills/get-brand-components/assets/kit_base.css`), so the gallery is self-contained, always renderable and identical in structure across brands. Everything the brand looks like must therefore be expressed in the tokens, fonts, logo files and the optional `render.gallery` composition block, which is also what every other consumer of the kit reads.

The gallery contains, in order: hero (top bar with logo and nav, eyebrow, heading with one emphasized word, lead, primary button), stat strip, section header with kicker, three feature cards with icon tiles, comparison table, quote, checklist, pricing cards, CTA band, footer, and a kit reference strip at the end (color swatches, heading and body faces at real size, embedded fonts, rules). Per-block surfaces (`dark`/`light`), heading alignment, card style, nav style and section framing come from `render.gallery` (see the renderer contract). Icons come from `icons.json`; a card without an icon collapses its tile.

The bar the tokens must clear is unchanged: the real logo files on both surfaces (downloaded in Step 2.5, never a wordmark typed as text), the real icons, the real font weights (many brands use a medium display face; defaulting to bold is wrong), the real button anatomy, and the brand's own emphasis device. A kit whose gallery looks generic has thin tokens, not a thin gallery; fix the tokens.

Optional bespoke hero: when the fixed hero cannot express the brand's hero composition, write `hero.html`, one `<section class="hero-bespoke">` using only `--brand-*` tokens, plain layout and text elements, and `<img src="<kit-relative file>">` for imagery. `render_gallery.py` sanitizes it (allowlisted elements and attributes, kit-relative images only, no scripts, styles, inline SVG or external resources) and swaps it in for the mechanical hero; a fragment that fails the allowlist is refused with the reason printed and the mechanical hero stays.

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
