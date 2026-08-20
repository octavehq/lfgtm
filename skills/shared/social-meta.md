# Social share metadata: making artifacts unfurl

Shared reference for every skill that emits HTML. When a link to a published artifact is pasted into Slack, LinkedIn, X, Facebook, or WhatsApp, the platform's crawler fetches the page and builds a preview card from its Open Graph tags. Without them the card degrades to a bare `<title>` at best. The tags cost four lines; author them in every deliverable.

## What the asset service does (and cannot do)

The artifact service meets unfurlers halfway, on **published + `public` website assets only**:

- Named social crawlers are allowed on the site-serving surfaces. Share links stay crawler-blocked by design, and nothing is search-indexable.
- A **relative** `og:image` path is absolutized at serve time against the real origin. A wrong authoring-time origin (e.g. `http://localhost:3015/...`) is swapped for the real one, but only the origin, never the path, and only for URLs pointing at that artifact.
- `twitter:card: summary_large_image` is injected automatically when an `og:image` exists and no card is declared.
- Unfurl fetches are not counted as visits, so pasting a link into a channel doesn't inflate stats.

What it cannot do: invent a missing tag, write your description, or conjure a missing image file. That is authoring-time work, which is why the canonical block below is part of every scaffold head and the mechanical lint checks for it.

## The canonical block

Immediately after `<title>` in the `<head>`:

```html
<meta property="og:title" content="[What this is and who it is for, in plain language]">
<meta property="og:description" content="[1-2 sentence summary a stranger understands]">
<meta property="og:image" content="assets/og.png">
<meta name="twitter:card" content="summary_large_image">
```

## Rules

1. **`og:title` and `og:description` go on every HTML deliverable.** They cost nothing and survive a later privacy flip to `public` without a re-edit. This copy renders on the social card, so it is reader-facing: hold it to [editorial-rules.md](editorial-rules.md) even though the mechanical lint cannot see attribute text (its text extraction strips tags). No unfilled placeholders, no internal framing, no em dashes.

2. **`og:image` is always a RELATIVE path** (`assets/og.png`), never anything else:
   - Never a `data:` URI. Every unfurler ignores it, and the service skips non-http schemes when rewriting.
   - Never an absolute URL. A hardcoded origin bakes the authoring machine's address into the artifact; a baked-in `http://localhost:3015` is exactly the bug that broke a real share card. The service absolutizes the relative path against the real origin at serve time, so relative is both safer and sufficient. It also survives the asset moving to a vanity URL or a different host.
   - Never root-absolute (`/assets/og.png`). Artifacts serve under `/sites/<identifier>-<uuid>/`, so a leading-slash path 404s.

3. **`twitter:card` only alongside `og:image`.** The service injects it if forgotten; writing it is better form.

4. **Omit `og:url` and `rel="canonical"`.** Authoring time cannot know the final URL, the service can only repair a wrong origin (never a wrong path), and unfurlers fall back to the fetched URL when `og:url` is absent. Emitting them is pure downside.

5. **Internal-only deliverables** (meeting prep, deal coaching, briefs, internal dashboards) may drop the `og:image` + `twitter:card` pair; keep title and description always. Anything published `public` carries all four; the asset-manager publish flow checks this before uploading a public website.

## Rendering the share image

The brand-kit renderer already has a 1200×630 OG canvas; the image is a two-command chain (no new tooling):

```bash
mkdir -p <deliverable-dir>/assets
python3 <skill-dir>/../get-brand-components/scripts/render_kit.py --kit <slug> \
  --spec og-spec.json --format og --out og-frame.html
python3 <skill-dir>/../get-brand-components/scripts/render.py \
  --file og-frame.html --out <deliverable-dir>/assets/og.png --width 1200 --height 630 --scale 1
```

`og-spec.json` is a single `hero` block carrying the deliverable's headline and a one-line subhead, written fresh from the deliverable (not pasted from internal notes) and held to editorial rules:

```json
{"title": "<headline>", "blocks": [{"type": "hero", "title": "<headline>", "lead": "<one-line subhead>"}]}
```

Delete `og-frame.html` afterwards; only `assets/og.png` ships. The `get-brand-components` skill renders this automatically when a deliverable is headed for publishing (see its Output formats section); other variants (square, story, email) stay ask-first.

## The one sanctioned sibling file

A relative `og:image` is not an external dependency: the page itself never fetches it, only crawlers do, so it does not violate a format's self-containment rule. It does turn a single-file deliverable into a two-file folder (`index.html` + `assets/og.png`). That is the one sanctioned sibling file, and the asset-manager upload scripts already handle folders.

## Where cards actually render

Only **published + `public`** website assets unfurl. `workspace` and `only_me` sit behind email verification, and share links are crawler-blocked, so perfect tags on those tiers produce no card. Author the tags everywhere anyway: flipping an asset public later then needs no re-edit, and the asset-manager flow fills the image gap at publish time.
