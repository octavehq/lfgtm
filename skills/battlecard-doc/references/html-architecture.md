# HTML Architecture -- Deal Card (v3)

Self-contained HTML with a dark "sheet" container on a black body. Design modeled after high-quality Octave skill outputs (editorial feel, tight CSS, visual depth).

## Design System

- **Black body** with a contained `.sheet` element (max-width, border, radius, deep shadow)
- **Topbar** with brand logos
- **Hero** with radial glow gradient overlay
- **Alternating sections** using `.canvas` class for background rhythm
- **Tabbed interface** for per-competitor panels (ARIA-compliant)
- **Comparison grids** for side-by-side competitive content
- **Eyebrow labels** for section categorization
- **No emoji** -- use CSS-based indicators (colored borders, markers)

## CSS Variable System

Define a custom palette per output. Use the seller's brand colors as accent (e.g., Descope's teal). Fall back to a generic dark palette if no brand kit exists.

```css
:root{
  --bg:#07090f; --canvas:#0c0f18; --surface:#12161f; --surface-dk:#0c0f18;
  --ink:#f0f2f5; --muted:#8e95a3; --faint:#5c6270; --on-dark:#f0f2f5;
  --primary:#00b8d4; --primary-ink:#fff; --link:#00e5c8;
  --accent:#6FEF2D; --neg:#ff5c5c; --warn:#f5a623;
  --border:#1c2030;
  --glow:radial-gradient(60% 80% at 50% 0%,rgba(0,184,212,.14) 0%,rgba(0,184,212,0) 70%);
  --emph:#00e5c8; --emph-w:600;
  --font:Inter,system-ui,sans-serif; --tracking:-.02em;
  --radius:14px; --radius-sec:20px; --pill:999px;
}
```

Adapt `--primary`, `--link`, `--glow` to the seller's brand colors when a brand kit is available.

## Core Layout Components

### Sheet Container
```css
body{font-family:var(--font);background:#000;color:var(--ink);font-size:15px;line-height:1.6;
  -webkit-font-smoothing:antialiased;padding:30px 16px}
.sheet{max-width:1080px;margin:0 auto;background:var(--bg);border-radius:var(--radius-sec);
  overflow:hidden;border:1px solid var(--border);box-shadow:0 40px 100px -40px rgba(0,0,0,.9)}
```

### Topbar
```css
.topbar{display:flex;align-items:center;justify-content:space-between;padding:18px 48px;
  border-bottom:1px solid var(--border)}
```
Left side: seller logo (base64 `<img>`) + separator + "Battle Card" label.
Right side: "prepared for [Account]" + account logo (base64 `<img>`).

### Hero
```css
.hero{position:relative;padding:44px 48px 48px;overflow:hidden;background:var(--bg)}
.hero::after{content:"";position:absolute;inset:0;background:var(--glow);pointer-events:none}
.hero>*{position:relative;z-index:1}
```
Eyebrow + h1 + subtitle + metadata chips.

### Sections & Canvas Alternation
```css
section{padding:40px 0}
.canvas{background:var(--canvas)}
.wrap{padding:0 48px}
.eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--link)}
```
Wrap alternating sections in `.canvas` divs for visual rhythm: Deal Situation (canvas) → Competitors (default bg) → Our Pitch (canvas).

### Deal Situation Grid
```css
.deal-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.deal-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.deal-card .eyebrow{margin-bottom:8px}
.deal-card p{font-size:.9rem;color:var(--muted);margin-bottom:6px}
.deal-card p:last-child{margin-bottom:0}
.deal-card ul{font-size:.9rem;color:var(--muted);padding-left:18px;margin:0}
.deal-card li{margin-bottom:4px}
.deal-card strong{color:var(--ink);font-weight:600}
.deal-card .hl{color:var(--link);font-style:italic}
```

### Tabs (Competitor Panels)
```css
.tab-bar{display:flex;gap:2px;background:var(--surface-dk);border:1px solid var(--border);
  border-bottom:none;border-radius:var(--radius) var(--radius) 0 0;padding:8px 8px 0}
.tab-bar button{font-family:var(--font);font-size:.85rem;font-weight:600;padding:.6rem 1.2rem;
  border:none;border-radius:8px 8px 0 0;cursor:pointer;background:transparent;color:var(--faint);
  transition:color .15s,background .15s}
.tab-bar button[aria-selected="true"]{color:var(--link);background:var(--surface)}
.tab-panel{display:none;background:var(--surface);border:1px solid var(--border);
  border-top:none;border-radius:0 0 var(--radius) var(--radius);padding:32px 28px}
.tab-panel[aria-hidden="false"]{display:block}
```

### Comparison Grid (side-by-side competitive content)
```css
.sub-lbl{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.14em;
  color:var(--faint);margin:28px 0 10px}
.sub-lbl:first-child{margin-top:0}
.cmp-hdr{display:grid;grid-template-columns:1fr 1fr;padding:0 0 8px}
.cmp-hdr span{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--faint)}
.cmp-hdr span:last-child{padding-left:20px}
.cmp-grid{display:flex;flex-direction:column;gap:8px}
.cmp-row{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--border);border-radius:8px;overflow:hidden}
.cmp-them{padding:14px 18px;background:var(--surface-dk);font-size:.88rem;color:var(--muted);
  line-height:1.55;border-right:1px solid var(--border)}
.cmp-us{padding:14px 18px;font-size:.88rem;line-height:1.55;color:var(--muted);
  border-left:2px solid var(--link)}
.cmp-them strong,.cmp-us strong{color:var(--ink);font-weight:600}
.cmp-us .qt{color:var(--link);font-style:italic}
```

HTML pattern:
```html
<div class="sub-lbl">Their Strengths &rarr; Our Counter</div>
<div class="cmp-hdr"><span>What they'll say</span><span>What you say back</span></div>
<div class="cmp-grid">
  <div class="cmp-row">
    <div class="cmp-them"><strong>[Strength]</strong> -- [1 sentence context on why it lands]</div>
    <div class="cmp-us"><strong>[Counter-point as declarative statement, no quotes.]</strong> [1 sentence tying to this account's needs.]</div>
  </div>
  <!-- more rows -->
</div>
```

### Single Competitor Variant (no tabs)

When there is only one competitor, skip the `.tab-bar` and render the panel directly:
```html
<div class="tab-panel" style="border-radius:var(--radius);border-top:1px solid var(--border)" aria-hidden="false">
  <!-- panel content identical to tabbed version -->
</div>
```
No tab switching JS needed. The panel gets full top border-radius since there's no tab bar above it.

### Proof List (green accent)
```css
.pf-list{display:flex;flex-direction:column}
.pf{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid var(--border);
  font-size:.92rem;line-height:1.6;color:var(--muted)}
.pf:last-child{border-bottom:none}
.pf-m{flex:0 0 3px;border-radius:2px;background:var(--accent);margin-top:6px;align-self:stretch}
.pf strong{color:var(--accent);font-weight:600}
```

### Watch-out (amber accent)
```css
.wo{background:rgba(245,166,35,.06);border-left:3px solid var(--warn);padding:14px 20px;
  border-radius:0 8px 8px 0;font-size:.92rem;line-height:1.6}
.wo strong{color:var(--warn);font-weight:600}
.wo .cm{color:var(--faint);margin-top:8px;font-size:.85rem}
```
The `<strong>` lead-in is a named risk pattern (e.g. "They anchor on price"), never a quoted prospect line. Follow it with labeled lines for "You'll hear," "Response," and "Proof" using `.wo .cm` (or additional `<p>` tags with the same muted styling) -- keep each to one line so the callout stays scannable.

```html
<div class="wo">
  <strong>They anchor on price.</strong> [1 sentence on why this deal is exposed to it.]
  <p class="cm"><strong>You'll hear:</strong> [the signal, paraphrased, not a quote]</p>
  <p class="cm"><strong>Response:</strong> [the counter-move for this account]</p>
  <p class="cm"><strong>Proof:</strong> [metric, reference, or switch story]</p>
</div>
```

### Trap Questions (optional card)
```css
.tq-list{display:flex;flex-direction:column;gap:10px}
.tq{background:var(--surface-dk);border:1px solid var(--border);border-radius:8px;padding:14px 18px}
.tq .q{font-size:.92rem;color:var(--ink);font-weight:600;margin-bottom:6px}
.tq p{font-size:.85rem;color:var(--muted);margin:4px 0 0}
.tq p strong{color:var(--faint);font-weight:600}
```
Compact card, one `.tq` block per question. Bold the question itself since it's meant to be read and asked near-verbatim; the "why this works" and follow-up lines stay muted.

```html
<div class="sub-lbl">Trap Questions</div>
<div class="tq-list">
  <div class="tq">
    <div class="q">"[Discovery question, asked near-verbatim, no competitor name]"</div>
    <p><strong>Why this works:</strong> [what it exposes]</p>
    <p><strong>If they say X:</strong> [follow-up that presses the gap]</p>
  </div>
  <!-- 2-4 total -->
</div>
```

### Landmines to Plant (optional, in Our Pitch)
```css
.lm-list{display:flex;flex-direction:column;gap:6px}
.lm{display:flex;gap:10px;padding:6px 0;font-size:.9rem;line-height:1.55;color:var(--muted)}
.lm-m{flex:0 0 3px;border-radius:2px;background:var(--link);margin-top:6px;align-self:stretch}
.lm strong{color:var(--ink);font-weight:600}
```
Reuses the proof-list visual language (marker + text) with the link color instead of the accent green, so it reads as "plant this" rather than "proof of this."

```html
<div class="p-sub">Landmines to Plant</div>
<div class="lm-list">
  <div class="lm"><div class="lm-m"></div><div><strong>[Criterion to raise early]</strong> -- [why it tilts the eval toward us]</div></div>
  <!-- 3-5 total -->
</div>
```

### Win Rate Bar
```css
.wr-bar{display:flex;height:1.6rem;border-radius:8px;overflow:hidden;background:var(--surface-dk);margin-top:8px}
.wr-w{background:var(--accent);display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:.7rem;color:var(--bg)}
.wr-l{background:var(--neg);display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:.7rem;color:var(--bg)}
```

### Pitch Cards (Our Pitch section)
```css
.p-sub{font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:28px 0 10px}
.p-sub:first-child{margin-top:0}
.p-sub .vs{color:var(--link);font-weight:700}
.p-grid{display:flex;flex-direction:column;gap:12px}
.p-card{padding:22px;border-radius:var(--radius);background:var(--surface);border:1px solid var(--border)}
.p-card h3{font-size:1rem;margin-bottom:6px}
.p-card p{font-size:.92rem;color:var(--muted);margin:0}
```

Our Pitch uses three sub-sections with `.p-sub` labels:
```html
<div class="p-sub">Unified -- works against any competitor</div>
<div class="p-grid"><!-- 3-4 unified pitch cards --></div>

<div class="p-sub">Sharpen <span class="vs">vs [Competitor 1]</span></div>
<div class="p-grid"><!-- 1-2 targeted cards --></div>

<div class="p-sub">Sharpen <span class="vs">vs [Competitor 2]</span></div>
<div class="p-grid"><!-- 1-2 targeted cards --></div>
```

### Footer
```css
.foot{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;
  padding:22px 48px;border-top:1px solid var(--border);color:var(--faint);font-size:.78rem}
```

## Responsive & Print

```css
@media(max-width:760px){
  .wrap,.topbar,.hero,.foot{padding-left:24px;padding-right:24px}
  .tab-panel{padding:24px 18px}
  .deal-grid,.cmp-row,.cmp-hdr{grid-template-columns:1fr}
  .cmp-us{border-left:none;border-top:1px solid var(--border)}
  .hero h1{font-size:1.9rem}
}
@media print{
  body{background:#fff;padding:0}
  .sheet{box-shadow:none;border-radius:0;border:none}
  .tab-panel{display:block!important;border:1px solid #ddd;border-radius:8px;margin-bottom:16px;break-inside:avoid}
  .tab-panel::before{content:attr(data-tab-label);display:block;font-size:1.1rem;font-weight:700;
    padding-bottom:6px;margin-bottom:12px;border-bottom:2px solid var(--primary)}
  .tab-bar{display:none}
}
```

## JavaScript (minimal)

Tab switching + keyboard navigation only. No sidebar dots (the sheet container makes them unnecessary).

```javascript
(function(){
  const tabs=document.querySelectorAll('[role="tab"]');
  const panels=document.querySelectorAll('[role="tabpanel"]');
  tabs.forEach(tab=>{
    tab.addEventListener('click',()=>{
      tabs.forEach(t=>t.setAttribute('aria-selected','false'));
      panels.forEach(p=>p.setAttribute('aria-hidden','true'));
      tab.setAttribute('aria-selected','true');
      const p=document.getElementById(tab.getAttribute('aria-controls'));
      if(p) p.setAttribute('aria-hidden','false');
    });
    tab.addEventListener('keydown',e=>{
      const a=Array.from(tabs),i=a.indexOf(tab);let t;
      if(e.key==='ArrowRight') t=a[(i+1)%a.length];
      if(e.key==='ArrowLeft') t=a[(i-1+a.length)%a.length];
      if(t){e.preventDefault();t.click();t.focus();}
    });
  });
})();
```

## Key Principles

1. **Sheet container, not full-bleed** -- the document lives inside a bordered, rounded container on a black background
2. **No emoji** -- use CSS-based indicators (colored borders, markers, accents)
3. **Tight CSS** -- aim for ~130 lines of styles, not 400. Compact variable names, purposeful rules only
4. **Alternating backgrounds** -- use `.canvas` wrapper for visual section rhythm
5. **Side-by-side is king** -- competitive content always shows their point alongside our response
6. **Logos as base64** -- self-contained, no external image dependencies
7. **Google Fonts only** -- the single external dependency (Inter)
8. **Tab panels need `class="tab-panel"`** -- the CSS show/hide targets this class
