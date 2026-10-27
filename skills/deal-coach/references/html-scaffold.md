# Coaching Microsite — HTML Scaffold

Self-contained, single HTML file. The only external dependency is the kit's Google Fonts link, when it has one; the kit's own font files and the workspace-company logo are embedded as data URIs. This scaffold reproduces the approved format. Every colour comes from the resolved brand kit ([brand-kit-usage.md](../../shared/brand-kit-usage.md)): inline the kit's `tokens.css` `:root` and its `@font-face` rules, and the scaffold's own roles below derive from those tokens with `var()` and `color-mix()`, so the CSS carries no colour literal of its own and `check_adherence.py` runs clean against the kit.

## Head + fonts

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deal Coaching: [Company]</title>
<meta property="og:title" content="Deal Coaching: [Company]">
<meta property="og:description" content="[1-2 sentence summary a stranger understands]">
<meta property="og:image" content="assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- The kit's render.webfonts URL; drop this link and both preconnects when the kit has none. -->
<link href="https://fonts.googleapis.com/css2?family=[kit fonts]&display=swap" rel="stylesheet">
<style>
  /* The kit's font files from manifest.render.fonts, base64-embedded, one rule per weight. */
  @font-face { font-family: '[Kit Heading Face]'; src: url(data:font/woff2;base64,<FILE>) format('woff2'); font-weight: 400; font-style: normal; font-display: swap; }
  /* ...kit tokens, scaffold roles and component CSS below... */
</style>
</head>
```

## CSS (component system)

Paste this whole block into `<style>` after the `@font-face` rules. The first `:root` is the resolved kit's `tokens.css`, pasted as is. The second maps the scaffold's roles onto kit tokens; leave it unchanged.

```css
:root { /* inline the workspace brand tokens.css :root here */ }
:root {
  /* Scaffold roles, derived only from kit tokens. Text roles stay at full kit ink so contrast holds. */
  --dc-ink-2: var(--brand-body-ink, var(--brand-ink));
  --dc-on-dark-2: color-mix(in srgb, var(--brand-on-dark) 80%, transparent);
  --dc-border-soft: var(--brand-border-soft, var(--brand-border));
  --dc-border-dark: var(--brand-border-dark, color-mix(in srgb, var(--brand-on-dark) 22%, transparent));
  --dc-primary-weak: color-mix(in srgb, var(--brand-primary) 10%, var(--brand-bg));
  --dc-accent: var(--brand-accent, var(--brand-primary));
  --dc-positive: var(--brand-positive, var(--brand-primary));
  --dc-positive-weak: color-mix(in srgb, var(--dc-positive) 8%, var(--brand-bg));
  --dc-warning: var(--brand-warning, var(--dc-accent));
  --dc-negative: var(--brand-negative, var(--brand-ink));
  --dc-negative-weak: color-mix(in srgb, var(--dc-negative) 8%, var(--brand-bg));
  --emph: var(--brand-emph-ink-light, var(--brand-primary)); --emph-dark: var(--brand-emph-ink-dark, var(--brand-on-dark));
  --font-display: var(--brand-font-heading); --font-body: var(--brand-font-body);
  --font-mono: var(--brand-font-mono), ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --radius-sm: var(--brand-radius-sm, 8px); --radius: var(--brand-radius, 12px); --radius-md: var(--brand-radius-card, 16px); --radius-pill: var(--brand-radius-pill, 999px);
  --shadow-sm: var(--brand-shadow-sm, none);
  --gap: 1rem; --gap-lg: 2rem;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--brand-bg); color: var(--brand-ink); font-family: var(--font-body); font-size: 1rem; line-height: 1.6; letter-spacing: -0.2px; -webkit-font-smoothing: antialiased; }
em, .emph { color: var(--emph); font-style: normal; }
.wrap { max-width: 880px; margin: 0 auto; padding: 0 clamp(1rem, 4vw, 2.5rem); }

/* sidebar nav dots */
.dots { position: fixed; top: 50%; right: clamp(0.5rem, 2vw, 1.75rem); transform: translateY(-50%); display: flex; flex-direction: column; gap: 0.6rem; z-index: 100; }
.dots a { position: relative; width: 9px; height: 9px; border-radius: 50%; background: var(--brand-border); transition: all 0.25s ease; }
.dots a.active { background: var(--brand-primary); transform: scale(1.45); }
.dots a span { position: absolute; right: 18px; top: 50%; transform: translateY(-50%); white-space: nowrap; font-size: 0.68rem; color: var(--brand-muted); background: var(--brand-bg); padding: 2px 8px; border-radius: var(--radius-pill); box-shadow: var(--shadow-sm); opacity: 0; pointer-events: none; transition: opacity 0.2s ease; }
.dots a:hover span, .dots a:focus-visible span { opacity: 1; }

/* keyboard focus */
a:focus-visible, button:focus-visible, summary:focus-visible, details.path > summary:focus-visible { outline: 2px solid var(--brand-primary); outline-offset: 2px; border-radius: var(--radius-sm); }
.dots a:focus-visible { outline-offset: 3px; }

/* hero band */
.hero { background: var(--brand-band); color: var(--brand-on-dark); padding: clamp(2.25rem, 5vw, 3.5rem) 0 clamp(2.5rem, 5vw, 3.75rem); }
.hero .wrap { display: flex; flex-direction: column; gap: 1.5rem; }
.hero-top { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.brand-mark { font-family: var(--font-display); font-weight: 300; font-size: 1.35rem; letter-spacing: 0.5px; color: var(--brand-on-dark); }
.brand-logo { height: 32px; width: auto; display: block; }
.method-badge { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.04em; color: var(--dc-on-dark-2); border: 1px solid var(--dc-border-dark); border-radius: var(--radius-pill); padding: 0.35rem 0.85rem; }
.eyebrow { font-size: 0.78rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.12em; color: var(--dc-on-dark-2); }
.hero h1 { font-family: var(--font-display); font-weight: 300; font-size: clamp(2.4rem, 6vw, 4rem); line-height: 1.02; letter-spacing: -1.24px; text-wrap: balance; }
.hero h1 em { color: var(--emph-dark); }
.hero-meta { display: flex; flex-wrap: wrap; gap: 0.5rem 0.75rem; }
.chip { font-size: 0.8rem; color: var(--brand-on-dark); background: rgba(255,255,255,0.08); border: 1px solid var(--dc-border-dark); border-radius: var(--radius-pill); padding: 0.3rem 0.8rem; }
.chip b { font-weight: 500; color: var(--emph-dark); }

/* stage rail */
.rail { display: flex; align-items: stretch; margin-top: 0.25rem; border: 1px solid var(--dc-border-dark); border-radius: var(--radius); overflow: hidden; }
.rail-step { flex: 1; min-width: 0; padding: 0.7rem 0.9rem; display: flex; flex-direction: column; gap: 0.15rem; border-right: 1px solid var(--dc-border-dark); }
.rail-step:last-child { border-right: 0; }
.rail-step .s-name { font-family: var(--font-display); font-weight: 400; font-size: 1rem; }
.rail-step .s-obj { font-size: 0.72rem; color: var(--dc-on-dark-2); }
.rail-step.current { background: color-mix(in srgb, var(--brand-on-dark) 14%, transparent); box-shadow: inset 0 3px 0 var(--emph-dark); }
/* the current stage reads at full on-dark ink; colour alone never marks it, so a pale emphasis hue cannot dim it */
.rail-step.current .s-name { color: var(--brand-on-dark); font-weight: 500; }
.rail-step.current .s-obj { color: var(--brand-on-dark); }
.rail-step.done .s-name::after { content: " \2713"; color: var(--emph-dark); font-size: 0.8em; }

/* sections */
main { padding: clamp(2rem, 4vw, 3rem) 0 4rem; }
section, .sec { scroll-margin-top: 1.5rem; }
.sec { padding: clamp(1.5rem, 3vw, 2.25rem) 0; border-bottom: 1px solid var(--brand-border); }
.sec:last-of-type { border-bottom: 0; }
.sec-head { margin-bottom: 1.25rem; }
.sec-num { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.08em; color: var(--brand-primary); font-weight: 500; }
.sec h2 { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.5rem, 3vw, 2.1rem); line-height: 1.12; letter-spacing: -0.5px; margin-top: 0.15rem; text-wrap: balance; }
.sec h2 em { color: var(--emph); }
.lead { color: var(--dc-ink-2); font-size: 1.02rem; margin-top: 0.4rem; max-width: 62ch; text-wrap: pretty; }

/* verdict */
.verdict { background: var(--brand-surface); border: 1px solid var(--dc-border-soft); border-radius: var(--radius-md); padding: clamp(1.25rem, 2.5vw, 1.75rem); display: flex; flex-direction: column; gap: 0.9rem; }
.verdict .headline { font-family: var(--font-display); font-weight: 400; font-size: clamp(1.15rem, 2.2vw, 1.45rem); line-height: 1.28; text-wrap: pretty; }
.verdict .headline em { color: var(--emph); }
.verdict-move { display: flex; gap: 0.7rem; align-items: flex-start; font-size: 0.95rem; color: var(--dc-ink-2); }
.verdict-move .tag { flex-shrink: 0; font-size: 0.66rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--brand-primary); background: var(--dc-primary-weak); border-radius: var(--radius-pill); padding: 0.22rem 0.6rem; margin-top: 0.1rem; }

/* cards + utilities */
.card { background: var(--brand-surface); border: 1px solid var(--dc-border-soft); border-radius: var(--radius); padding: clamp(1rem, 2vw, 1.35rem); }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--gap); }
.label { font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--brand-muted); }

/* Job 1 stage read + no-CRM note */
.stand { display: grid; grid-template-columns: 1fr; gap: var(--gap); align-items: stretch; }
.stand.has-deal { grid-template-columns: 1.1fr 1fr; } /* second column: the CRM opportunity card */
.stand > * { min-width: 0; }
.stand .read { display: flex; flex-direction: column; gap: 0.75rem; }
.conf { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: var(--dc-ink-2); }
.conf .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--dc-warning); }
.evi { list-style: none; display: flex; flex-direction: column; gap: 0.55rem; }
.evi li { display: grid; grid-template-columns: 92px 1fr; gap: 0.6rem; font-size: 0.88rem; align-items: baseline; }
.evi .w { font-family: var(--font-mono); font-size: 0.72rem; color: var(--brand-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.no-crm { grid-column: 1 / -1; font-size: 0.85rem; color: var(--dc-ink-2); }

/* stage gloss */
.stage-gloss { border: 1px solid var(--dc-border-soft); border-left: 3px solid var(--emph-dark); border-radius: 0 var(--radius) var(--radius) 0; padding: 0.9rem 1.15rem; margin-bottom: 1rem; }
.stage-gloss .label { display: block; margin-bottom: 0.3rem; }
.stage-gloss p { font-size: 0.92rem; color: var(--dc-ink-2); text-wrap: pretty; }
.stage-gloss p em { color: var(--emph); }

/* Job 2 buyer mindset */
.mindset { border-left: 3px solid var(--dc-accent); background: var(--brand-surface); border-radius: 0 var(--radius) var(--radius) 0; padding: 1.1rem 1.35rem; }
.mindset p { font-size: 0.98rem; color: var(--brand-ink); }
.mindset p + p { margin-top: 0.6rem; }
.heard { margin-top: 1.1rem; }
.heard-list { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.6rem; }
.heard-list li { display: flex; gap: 0.65rem; align-items: flex-start; font-size: 0.9rem; }
.heard-list li::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--brand-primary); margin-top: 0.5rem; flex-shrink: 0; }
.heard-list .who { color: var(--brand-muted); font-size: 0.8rem; }

/* Job 3 goals + value props + talk tracks */
.goals { list-style: none; counter-reset: g; display: flex; flex-direction: column; gap: 0.6rem; margin: 0.6rem 0 1.3rem; }
.goals li { counter-increment: g; display: grid; grid-template-columns: 26px 1fr; gap: 0.7rem; align-items: start; font-size: 0.94rem; }
.goals li::before { content: counter(g); display: flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; background: var(--brand-primary); color: var(--brand-primary-ink); font-family: var(--font-mono); font-size: 0.72rem; font-weight: 500; margin-top: 0.05rem; }
.goals li em { color: var(--emph); }
.vp-list { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; margin: 0.6rem 0 1.3rem; }
.vp-list li { display: grid; grid-template-columns: 16px 1fr; gap: 0.55rem; font-size: 0.94rem; align-items: start; }
.vp-list li::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--dc-accent); margin-top: 0.55rem; }
.vp-list li em { color: var(--emph); }
.tt { background: var(--brand-bg); border: 1px solid var(--dc-border-soft); border-left: 3px solid var(--brand-primary); border-radius: 0 var(--radius) var(--radius) 0; padding: 1rem 1.25rem; }
.tt + .tt { margin-top: 0.85rem; }
.tt .tt-label { font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; color: var(--brand-primary); margin-bottom: 0.35rem; }
.tt .tt-say { font-size: 0.98rem; line-height: 1.5; }
.tt .tt-say em { color: var(--emph); }
.tt .tt-note { font-size: 0.82rem; color: var(--brand-muted); margin-top: 0.5rem; }

/* Job 4 readiness + forward-stage collapsibles */
.ready { border: 1px solid var(--dc-border-soft); border-left: 3px solid var(--dc-positive); background: var(--dc-positive-weak); border-radius: 0 var(--radius) var(--radius) 0; padding: 1rem 1.25rem; margin-bottom: 1.1rem; }
.ready .label { color: var(--dc-positive); display: block; margin-bottom: 0.55rem; }
.ready ul { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
.ready ul li { display: grid; grid-template-columns: 18px 1fr; gap: 0.55rem; font-size: 0.92rem; align-items: start; }
.ready ul li::before { content: "\2713"; color: var(--dc-positive); font-weight: 600; }
.ready ul li em { color: var(--emph); }
details.path { border: 1px solid var(--dc-border-soft); border-radius: var(--radius); margin-top: 0.85rem; overflow: hidden; background: var(--brand-bg); }
details.path > summary { cursor: pointer; list-style: none; padding: 0.95rem 1.15rem; display: flex; align-items: center; gap: 0.75rem; }
details.path > summary::-webkit-details-marker { display: none; }
details.path > summary::before { content: "\25B6"; font-size: 0.62em; color: var(--brand-primary); transition: transform 0.2s ease; }
details.path[open] > summary::before { transform: rotate(90deg); }
details.path .p-stage { font-family: var(--font-display); font-weight: 400; font-size: 1.1rem; }
details.path .p-obj { font-size: 0.8rem; color: var(--brand-muted); }
details.path .p-body { padding: 0 1.15rem 1.15rem; display: flex; flex-direction: column; gap: 0.75rem; }
.prove { font-size: 0.9rem; }
.prove .label { display: block; margin-bottom: 0.45rem; }
.prove ul { list-style: none; display: flex; flex-direction: column; gap: 0.4rem; }
.prove ul li { display: flex; gap: 0.6rem; font-size: 0.9rem; }
.prove ul li::before { content: "\2192"; color: var(--brand-primary); flex-shrink: 0; }

/* Job 5 risk list (scales to any number of risks) */
.risk-list { display: flex; flex-direction: column; gap: var(--gap); }
.risk-pair { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--dc-border-soft); border-radius: var(--radius); overflow: hidden; }
.risk-pair > * { min-width: 0; }
.risk-pair .r-risk { padding: 0.9rem 1.15rem; border-left: 3px solid var(--dc-negative); background: var(--dc-negative-weak); }
.risk-pair .r-counter { padding: 0.9rem 1.15rem; border-left: 3px solid var(--dc-positive); background: var(--dc-positive-weak); }
.risk-pair .label { margin-bottom: 0.3rem; }
.risk-pair .r-risk .label { color: var(--dc-negative); }
.risk-pair .r-counter .label { color: var(--dc-positive); }
.risk-pair p { font-size: 0.9rem; }
.risk-pair p em { color: var(--emph); }

/* Job 6 quiz + rubric */
.quiz { display: flex; flex-direction: column; gap: 1.1rem; margin-top: 0.5rem; }
.q { background: var(--brand-surface); border: 1px solid var(--dc-border-soft); border-radius: var(--radius); padding: 1.1rem 1.25rem; }
.q .q-text { font-weight: 500; font-size: 0.98rem; margin-bottom: 0.75rem; }
.q .opt { display: block; width: 100%; text-align: left; font: inherit; font-size: 0.9rem; color: var(--brand-ink); background: var(--brand-bg); border: 1px solid var(--dc-border-soft); border-radius: var(--radius-sm); padding: 0.6rem 0.85rem; margin-bottom: 0.5rem; cursor: pointer; transition: border-color 0.15s ease, background 0.15s ease; }
.q .opt:hover { border-color: var(--brand-primary); }
.q .opt.correct { border-color: var(--dc-positive); background: var(--dc-positive-weak); }
.q .opt.wrong { border-color: var(--dc-negative); background: var(--dc-negative-weak); }
.q .opt:disabled { cursor: default; }
.q .q-answer { font-size: 0.85rem; color: var(--dc-ink-2); margin-top: 0.4rem;  }
.q .q-answer.show { display: block; }
.q .q-answer em { color: var(--emph); }
.rubric { display: flex; flex-direction: column; gap: 0.5rem; }
.rubric-row { display: grid; grid-template-columns: 150px 1fr; gap: 1rem; padding: 0.7rem 0; border-bottom: 1px solid var(--brand-border); align-items: baseline; }
.rubric-row:last-child { border-bottom: 0; }
.rubric-row .crit { font-weight: 500; font-size: 0.9rem; }
.rubric-row .good { font-size: 0.9rem; color: var(--dc-ink-2); }
.rubric-row .good em { color: var(--emph); }

footer { border-top: 1px solid var(--brand-border); padding: 1.75rem 0 2.5rem; color: var(--brand-muted); font-size: 0.8rem; display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; justify-content: space-between; }
footer .src { max-width: 60ch; }

@media (max-width: 720px) {
  .dots { display: none; }
  .grid-2, .stand, .risk-pair { grid-template-columns: 1fr; }
  .rail { flex-direction: column; }
  .rail-step { border-right: 0; border-bottom: 1px solid var(--dc-border-dark); }
  .rail-step:last-child { border-bottom: 0; }
  .evi li { grid-template-columns: 78px 1fr; }
  .rubric-row { grid-template-columns: 1fr; gap: 0.2rem; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; scroll-behavior: auto !important; } }
@media print {
  .dots { display: none; }
  .hero { background: var(--brand-surface-dark) !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .card, .risk-pair, .tt, .q, details.path, .verdict, .rubric-row { break-inside: avoid; }
  details.path .p-body { display: flex !important; }
  body { color: #111; }
}
```

## Body skeleton

```html
<body>
<nav class="dots" aria-label="Section navigation">
  <a href="#stands"><span>Where it stands</span></a>
  <a href="#head"><span>Buyer's head</span></a>
  <a href="#say"><span>What to do now</span></a>
  <a href="#path"><span>Path to close</span></a>
  <a href="#exposed"><span>Top risks</span></a>
  <a href="#practice"><span>Practice</span></a>
</nav>

<header class="hero"><div class="wrap">
  <div class="hero-top">
    <img class="brand-logo" src="data:image/png;base64,<LOGO>" alt="[Workspace Company]" width="133" height="32">
    <!-- Only when the workspace has a methodology on file or the user asked for one: its own stage names. Otherwise omit the badge. -->
    <span class="method-badge">[Stage 1] → [Stage 2] → [Stage 3]</span>
  </div>
  <div>
    <p class="eyebrow">Deal coaching plan</p>
    <h1>[Company]: [claim about this deal, with <em>pivotal words</em>]</h1>
  </div>
  <div class="hero-meta">
    <span class="chip">Buyer: <b>[Real Name]</b>, [Title]</span>
    <span class="chip">Persona: <b>[Persona]</b></span>
    <span class="chip">Segment: <b>[Segment]</b></span>
  </div>
  <!-- Same condition as the badge: the workspace's own stages and objectives, or no rail. -->
  <div class="rail" role="list" aria-label="Methodology stages">
    <div class="rail-step current" role="listitem" aria-current="step"><span class="s-name">[Stage 1]</span><span class="s-obj">[Objective]</span></div>
    <div class="rail-step" role="listitem"><span class="s-name">[Stage 2]</span><span class="s-obj">[Objective]</span></div>
    <div class="rail-step" role="listitem"><span class="s-name">[Stage 3]</span><span class="s-obj">[Objective]</span></div>
  </div>
</div></header>

<main class="wrap">
  <section class="sec" id="stands">   <!-- Job 1: gloss + verdict + div.stand(read). With a CRM opportunity: div.stand.has-deal(read + deal card). Without: p.no-crm, one line, and no deal-record card --></section>
  <section class="sec" id="head">     <!-- Job 2: mindset + heard-list --></section>
  <section class="sec" id="say">      <!-- Job 3: goals + vp-list + 3 tt --></section>
  <section class="sec" id="path">     <!-- Job 4: ready + details.path (one per stage ahead) --></section>
  <section class="sec" id="exposed">  <!-- Job 5: risk-list of N risk-pair --></section>
  <section class="sec" id="practice"> <!-- Job 6: quiz + rubric --></section>
</main>

<footer class="wrap">
  <span class="src">[provenance: which calls, buyer, Motion ICP cell; where deal fields were blank]</span>
  <span>[Workspace Company] · Deal Coach</span>
</footer>
```

**Grid + inline-em gotcha:** `.goals li`, `.vp-list li`, and `.ready ul li` are CSS grid. Any inline `<em>` inside them MUST be wrapped with the item's text in a `<span>` (grid column 2), or the `<em>` becomes its own grid cell and drops to a new line. Pattern: `<li><span>text with <em>emphasis</em> inline.</span></li>`.

## JS (nav dots + quiz + print)

```html
<script>
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dots a'));
  var secs = dots.map(function (d) { return document.querySelector(d.getAttribute('href')); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { var i = secs.indexOf(e.target); dots.forEach(function (d, j) { d.classList.toggle('active', j === i); }); } });
    }, { rootMargin: '-40% 0px -55% 0px' });
    secs.forEach(function (s) { if (s) io.observe(s); });
  }
  document.querySelectorAll('.q').forEach(function (q) {
    var answer = parseInt(q.getAttribute('data-answer'), 10);
    var opts = Array.prototype.slice.call(q.querySelectorAll('.opt'));
    var explain = q.querySelector('.q-answer');
    opts.forEach(function (opt, i) {
      opt.addEventListener('click', function () {
        opts.forEach(function (o, j) { o.disabled = true; if (j === answer) o.classList.add('correct'); else if (j === i) o.classList.add('wrong'); });
        if (explain) explain.open = true;
      });
    });
  });
  window.addEventListener('beforeprint', function () { document.querySelectorAll('details.path, details.q-answer').forEach(function (d) { d.open = true; }); });
</script>
```

Print CSS must expose `.q-answer > *` and print every path. Native answer details remain available without JavaScript.
