# Brand kits: whose brand, kit lookup, and brand extraction

Shared reference for every skill that renders styled HTML output. Covers (1) whose brand an asset should wear by default, (2) how to find and apply a cached brand kit, and (3) how to extract brand styling from a website when no kit exists.

## 1. Whose brand: the workspace company, always

The document's design system (fonts, colors, header, footer, chrome) always wears the **workspace company's brand**: the Octave customer whose instance is running the skill. Resolve it with `get_workspace_company`, derive its `<slug>`, and run the kit lookup below. This holds for every asset type, whether it stays internal (battlecard, meeting-prep, brief, wins-losses, positioning) or goes out to a prospect (one-pager, proposal, microsite, deck). A company brands its own output, the same way it puts its own letterhead on a document it sends. Use the workspace company's kit by default, without asking.

The **target company's logo** (the prospect, account, or competitor) appears only in content, a masthead accent, a "prepared for" line, or a deal-context card, to personalize the asset. It never controls the design system. Fetch it with `get_external_brand_logo` / `get_external_brand_assets` and place it in content, not the chrome.

- Branding a document in the target's colors is the wrong default; a target-company kit for the design system is used only if the user explicitly asks (e.g. a co-branded piece).
- Respect an explicit `--style <preset>` or brand override.

> **POC / demo runs are not a special case.** When Octave produces showcase assets inside a *prospect's* workspace to demonstrate the platform, `get_workspace_company` resolves to that prospect, so the same rule renders the demo in the prospect's brand automatically. "Workspace company" is always whoever's instance is running the skill.

## 2. Brand kit lookup (cache first)

1. Resolve the chosen company to a `<slug>` and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`.
2. **If a kit exists →** use it by default (it's the workspace company's own brand, no need to ask). Style the output with the kit instead of a generic preset:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** [`../get-brand-components/assets/kit_base.css`](../get-brand-components/assets/kit_base.css) into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`;
   - for doc-shaped output you can compose directly with the renderer at `../get-brand-components/scripts/render_kit.py` (hero / split / logos / pricing / cta / footer blocks, see the `get-brand-components` skill for the token contract).
3. **If no kit exists →** offer to build one first: *"No brand kit for <Company> yet, want me to capture it (~1 min) so this is on-brand?"* → run `/octave:get-brand-components <domain>`, then proceed.
4. **If the user declines →** generate with the default style preset (see [style-presets.md](style-presets.md)).

> The brand kit is the strongest styling signal: when one is available, prefer it over generic `--style` presets. See the `get-brand-components` skill for the kit format, token contract, and renderer.

### Logo integrity: verify the pixels before you ship

A cached kit can carry a **stray or mislabeled logo** (a real case: a cached Octave kit's `*-logo-white.png` was actually a WorkSpan logo scraped from a "trusted by" wall). This is nearly invisible in normal review, because a white/onDark logo does not show on a light preview and the manifest metadata can claim the right company while the file is wrong. So, before delivering any HTML that uses a kit logo:

- **Render both variants on their intended surfaces and confirm each reads the workspace company's name.** Read the `onLight` file (it sits on a light surface) and the `onDark` file (put it on a dark swatch), or run `../get-brand-components/scripts/verify-logos.sh <slug>`. Do not trust `lockup.wordmark`; inspect the image.
- **The `onDark` variant is the usual culprit** and the one you cannot see on a white page. Always check it on a dark background specifically.
- If a variant is the wrong company or clearly wrong, do not ship it: use the other cached kit for the same company, re-source from the footer/nav, or recolor the *verified* `onLight` mark. Never ship a logo you have not eyeballed on its real surface.
- Customers/partners appear only as content proof, never as the document's brand mark. If the logo on the chrome is a customer, it is contaminated.

## 3. Brand extraction without a kit (tiered)

When the user wants brand styling but no kit exists (and doesn't want to build one), work down these tiers: start at Tier 1 and only fall through when a tier is unavailable. Tiers 1–2 are the fast, high-quality path; combine both when you can (colors+logo from Tier 1, fonts+components from Tier 2). Run the extraction against the workspace company's domain (the brand the design system will wear); the target company's logo is a separate one-off fetch for content, per Section 1.

**Tier 1: Octave brand-assets tool (first-party, fast, try first)**
```
get_external_brand_assets({ url: "https://<domain>" })
  → colors (primary / secondary / accent), logo variants, backdrop images, brand name
get_external_brand_logo({ domain: "<domain>" })   # if you only need the single best logo
```
This is one call for the visual identity and the right default. **Sanity-check the result: the scraper reads the DOM and can misattribute a homepage logo wall.**
- If `brandName` doesn't match the target company, ignore it (it likely grabbed a customer name).
- A strip of many logos with varied aspect ratios is usually a **"trusted by" customer wall**, not the brand's own logo. Don't use those as the asset's logo. Prefer the `favicon` / `apple-touch-icon` entries or the nav wordmark.
- The `colors` are usually reliable; still confirm with the user.

**Tier 2: `scrape_website`, components & typography (the "looks like their site" leap)**
```
scrape_website({ url: "https://<domain>",        format: "markdown", includeScreenshot: true })
scrape_website({ url: "https://<representative-page>", format: "markdown", includeScreenshot: true })
```
Pull the homepage **and one representative page** (case study, blog post, pricing, or product page). Then:
- **From the screenshot(s):** read the component vocabulary the DOM hides (button shapes, card styles, corner radii, spacing rhythm, type scale, section patterns, use of gradients/imagery) and the typeface's visual character. The screenshot is the primary typography source: identify the face (or the closest widely-available stand-in) visually and record the substitution in the brand config. Emulate the *component and layout system*, not just the colors.
- **`format: "html"` caveats:** the tool returns body-only HTML (no `<head>`, so font `<link>`s and most CSS are unrecoverable from it), and asset-heavy pages can exceed the response cap and truncate. Reach for html only to inspect specific inline markup (e.g. CSS custom properties like `--brand-*`); markdown + screenshot is the workable default.
- **Logos and images from any tier are download sources, not link targets:** embed them in the final asset as data URIs (or recreate the wordmark as a styled type treatment), never hotlink a remote URL in a delivered document.

> If `scrape_website` isn't available in the connected workspace, skip to Tier 3.

**Tier 3: browser-use (fallback if `scrape_website` unavailable)**
```
1. browser-use open <website-url>
2. browser-use screenshot brand-capture.png
3. browser-use eval "(() => {
     const body = getComputedStyle(document.body);
     return {
       bgColor: body.backgroundColor, textColor: body.color, fontFamily: body.fontFamily,
       links: getComputedStyle(document.querySelector('a') || document.body).color,
       headings: getComputedStyle(document.querySelector('h1,h2,h3') || document.body).fontFamily,
       logos: [...document.querySelectorAll('header img, img[src*=logo], svg[class*=logo]')].map(e => e.src || 'inline-svg').slice(0, 3)
     };
   })()"
4. browser-use extract "List the primary brand colors (hex), fonts, and logo URLs visible on this page"
```

**Tier 4: WebFetch (fallback if browser-use unavailable)**
```
1. WebFetch the homepage URL
2. Parse HTML/CSS for CSS custom properties (--brand-*, --color-*), font-family on body/h1-h3,
   logo URLs from <img>/<svg>/og:image, and meta theme-color
```

**Tier 5: Manual (if nothing automated works)**
```
I couldn't automatically extract your brand. You can:
1. Share your brand guidelines (PDF or link)
2. Provide hex colors: primary, secondary, background, text
3. Name your fonts (heading + body)   4. Share logo files
```

**Always confirm the brand config with the user before proceeding:**

```
BRAND CONFIG EXTRACTED
======================

Colors:
  Primary:    #XXXXXX ██   Secondary: #XXXXXX ██   Accent: #XXXXXX ██
  Background: #XXXXXX ██   Text:      #XXXXXX ██

Fonts:    Headings: [Font name]    Body: [Font name]

Logo:     [URL or file path]   (verified as the brand's own, not a customer logo)

Components observed (from screenshots, if Tier 2 ran):
  • [e.g. pill buttons, 12px card radius, generous section spacing, gradient accents]

Does this look right? (y/n/adjust)
```

## 4. Applying an extracted brand (no kit)

Auto-generate CSS variables from the extracted brand config:

```
- --bg: [brand background or dark variant]
- --bg-elevated: [slightly lighter than bg]
- --bg-card: [semi-transparent card bg]
- --text-primary: [brand text color]
- --text-secondary: [muted variant]
- --brand-primary: [primary brand color]
- --brand-500: [lighter accent]
- --font-display: [brand heading font]
- --font-body: [brand body font]
```

Show the generated style to the user for confirmation. Prefer the brand's own fonts; if none are available, fall back to the heading/body pairing of the closest preset.
