# Generating collateral from a kit (the renderer)

**The primary way to turn a kit into an on-brand asset is the bundled renderer — do NOT hand-write per-asset CSS.** One engine composes any asset from any kit; the same content spec rendered through a different kit comes out fully on-brand for that brand (designed for dark, gradient, and light visual systems; verify the current output).

```bash
python3 <skill-dir>/scripts/render_kit.py --kit <slug|path> --spec <asset-spec.json> --out <out.html> \
        [--kit-dir <path>] [--theme light|dark] [--format doc|og|social-square|social-story|email|slide]
```

- `--kit-dir` renders a kit stored anywhere (kits don't have to live in `~/.octave/brands/`).
- `--theme` picks the light or dark palette when the kit carries both (`tokensDark`/`tokensLight`).

### Output formats

The same kit + spec can render to **multiple formats** — the brand kit is format-agnostic, so don't rebuild styling per format. `--format` sets the canvas: `doc` (default page), `og` (1200×630 share image), `social-square` (1080²), `social-story` (1080×1920), `email` (600px width), `slide` (1280×720 single-slide canvas — one hero-or-stats-sized spec per slide; for full decks use the deck skill). The *spec* controls content (a short hero/CTA spec makes a clean OG/social image).

**The OG share image is automatic at publish; every other variant is ask-first.** When an HTML deliverable is headed somewhere anyone with the link can open it — the asset-manager `public` tier, the microsite deploy, or the user saying at intake they'll publish, post, or share the link — render its share image without asking and place it beside the HTML:

```bash
python3 <skill-dir>/scripts/render_kit.py --kit <slug> --spec og-spec.json --format og --out og-frame.html
python3 <skill-dir>/scripts/render.py --file og-frame.html --out <deliverable-dir>/assets/og.png --width 1200 --height 630 --scale 1
```

The spec is one `hero` block carrying the deliverable's headline and a one-line subhead — write both fresh from the deliverable and hold them to editorial-rules.md; this copy renders on the social card. Delete `og-frame.html` after. Then confirm the deliverable's head references the image relatively (`assets/og.png`) with the block from [social-meta.md](../../shared/social-meta.md) — never an absolute URL, never a data URI. Square, story, and email variants stay opt-in: after producing the main asset, ask whether the user wants them, and only then render.

- **`scripts/render_kit.py`** — loads the kit, emits a self-contained HTML doc: `<style>` = `:root{}` from `manifest.render.tokens` + base64 `@font-face` from `manifest.render.fonts` + `assets/kit_base.css`; body = composed blocks; logo/icons inlined.
- **`assets/kit_base.css`** — brand-AGNOSTIC component stylesheet (every rule references a `--brand-*` token). This is the single source of truth for component CSS — fix a component once here and every asset for every brand inherits it.
- **Content spec** (JSON) — `{ title, blocks: [...] }`. Block types: `hero`, `stats`, `about`, `quote`, `section`, `features`, `comparison`, `checklist`, `cta`, `footer`, plus the imagery/marketing blocks:
  - **`split`** — image-paired feature row: `{kicker, heading, paras[], bullets[], image, imageSide: left|right, cta}`. The `image` is a kit-relative path (inlined) or URL; it's framed (rounded + shadow).
  - **`logos`** — logo wall: `{label, mono: bool, items:[{img}|{text}]}`. `mono` greyscales color logos for a uniform wall.
  - **`pricing`** — plan cards: `{plans:[{name, price, period, blurb, cta, features[], featured, badge}]}`; the `featured` plan gets the primary border + badge.
  - Any content block can take `surface: "dark"` to render as a full-bleed dark band (e.g. a logo wall with white logos).
  - Emphasis: wrap a word in `**double asterisks**`. `hero.featured.logoKit` pulls *another* kit's logo (customer logo in a vendor case study).
- **Real imagery** — store the brand's actual product screenshots / customer logos in the kit's **`images/`** dir (downloaded during the walk) and reference them by relative path; the renderer inlines them as data-URIs (self-contained). Don't fake imagery with gradient placeholders when the real assets exist on the site — extract logo walls and a hero/product shot. (Apply the same logo-verification care: confirm a "customer logo" is real, not a stray asset.) Optional `--brand-texture` token layers a subtle pattern (dot/grid) onto dark bands.
- **Visual constraints** — respect `manifest.rules` and `corrections.md` when styling the asset.
- **After rendering** — run `scripts/check_adherence.py` on the output, then the fidelity gate (Step 7.5) if the asset is shippable.

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
- `logo`: `{onDark, onLight, onDarkSource, onLightSource, lockup}` — per-surface logos. **The renderer picks `onDark` on dark surfaces and `onLight` on light ones** (this is what prevents white-logo-on-white-footer). `onDarkSource` / `onLightSource` record the URL each variant was downloaded from (provenance, so a wrong asset can be audited); a source in a `customers|partners|trusted|clients|logos` container or a foreign domain is suspect. `lockup` = `{mark, wordmark, wordmarkWeight}` for brands whose logo is a mark + wordmark. **Both variants must be pixel-verified (see the logo source rule + wordmark gate in Step 2.5) before the kit is considered complete.**
- `tokens`: the `--brand-*` contract — colors (`bg`, `canvas`, `surface`, `surface-dark`, `ink`, `muted`, `faint`, `on-dark`, `primary`/`-ink`, `link`, `border`, `negative`, `band`, `glow`, `tile-bg`/`-ink`/`-glow`, `grad-border`), emphasis (`emph-ink-light`/`-dark`, `emph-underline`, `emph-weight`), type (`font-heading`/`-body`, `weight-*`, `tracking-heading`, `h1`/`h2`), shape (`radius-section`/`-pill`, `shadow`, `btn-shadow`), and the **foundations** (`shadow-sm`/`-md`/`-xl` elevation, `ease`/`duration` motion, `icon-stroke`, gray ramp, semantic states, spacing scale, gradients — see Step 4). `hero-bg`/`cta-bg` add a light-surface wash; `heading-transform` forces all-caps.
- `tokensDark` / `tokensLight` (optional): override maps for the opposite theme, merged when `--theme` is passed.
- `defaultTheme` (optional): `light` | `dark`.

Add `render` when building a kit (Step 6). The verbose `tokens.css` + `components.html` remain the human-readable reference; `render` is the machine contract the engine consumes.

### Fallback (manual compose)
If a one-off needs a layout the block types don't cover, you can still inline `tokens.css` + `assets/kit_base.css` and write markup using the `kit_base` classes — but prefer adding a block type to the renderer over hand-CSS, so the fix compounds.

Reference token names are brand-agnostic, so the same spec restyles to any captured brand just by swapping `--kit`.


Read the structured-link contract in [task-method.md](task-method.md). Use explicit text items or {label,href,target?}; all interactive blocks preserve destinations. Missing href is an authoring error. Capture OG at --width 1200 --height 630 --scale 1 --no-full-page.

Lockup marks preserve the complete verified SVG. Store approved surface variants for recoloring; the renderer does not reduce a logo to its first path or invent a new color treatment.
