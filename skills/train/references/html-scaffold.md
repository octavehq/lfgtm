# Onboarding GTM Primer — HTML Scaffold (gated slide lesson)

A single self-contained HTML file. Inline all CSS and JS; the only external dependency is Google Fonts (or the brand kit's `@font-face`). The primer is a **gated slide lesson**: fixed-viewport slides, a progress-dot rail, per-slide checkpoints that unlock the Next button, interactive tab selectors (personas, competitors, proof lenses), and a scored completion slide.

**Styling comes from the workspace company's brand kit.** Inline the kit's `tokens.css` (`:root` + `@font-face`) and `../get-brand-components/assets/kit_base.css`, then map the component classes below onto the kit's `--brand-*` variables. The classes here are structural; the brand kit supplies color, type, radius, and signature moves. (When authoring a cleaned `:root`, do not paste comment lines from the kit that contain em/en-dashes; the lint rejects them.)

## Layout model

- `body { overflow: hidden }`. A fixed `.topbar` (logo, step label, progress dots). A `.deck` holding absolutely-positioned `.slide`s; only `.slide.active` is shown.
- Each content slide: `.slide-inner` (flex column, full height) > `.slide-body` (flex:1, `overflow-y:auto`, holds content + `.checkpoints`) + `.slide-nav` (pinned, Back / hint / Next).
- Cover and completion are `.slide.gradient` (brand dark/gradient band, centered).

## Core CSS components

```css
/* progress rail */
.topbar { position: fixed; top:0; left:0; right:0; height:56px; display:flex; align-items:center; gap:1.25rem; ... }
.progress-dots .dot { width:9px; height:9px; border-radius:50%; background: var(--brand-border); cursor:pointer; }
.progress-dots .dot.done { background: var(--brand-accent-light); }
.progress-dots .dot.current { background: var(--brand-primary); transform: scale(1.35); }

/* deck + slides */
.deck { position: relative; height: 100vh; }
.slide { position:absolute; inset:0; padding-top:56px; display:none; flex-direction:column; }
.slide.active { display:flex; animation: slidein .32s; }
.slide-inner { max-width: 980px; margin:0 auto; padding:1.6rem clamp(1rem,4vw,2.5rem) 0; display:flex; flex-direction:column; height:100%; }
.slide-body { flex:1; overflow-y:auto; padding-bottom:1rem; }
.slide-nav { display:flex; align-items:center; gap:1rem; padding:.8rem 0 1.05rem; }
.slide.gradient { background: var(--brand-band); color: var(--brand-on-dark); }
.slide.gradient .slide-inner { justify-content:center; text-align:center; align-items:center; }

/* teaching components */
.callout { border-left:3px solid var(--brand-primary); background: var(--brand-surface); padding:.85rem 1.1rem; font-style:italic; }
.sub-label { font-family: var(--brand-font-mono); text-transform:uppercase; letter-spacing:.06em; font-size:.7rem; color: var(--brand-muted); }   /* with a trailing hairline rule */
.how-steps { display:grid; grid-template-columns:repeat(3,1fr); gap:.85rem; }     /* Structure / Ingest / Propagate */
.stakes-item { border-left:3px solid var(--brand-negative); }                     /* "without us" */
.theme-item .k { font-family: var(--brand-font-heading); color: var(--brand-accent); font-size:1.35rem; }  /* outcome metric */

/* Slide 1: customer archetype cards */
.archetype-card { display:flex; flex-direction:column; gap:.55rem; background: var(--brand-surface); border-radius: var(--brand-radius); padding:1rem 1.1rem; }
.archetype-card .a-prob { color: var(--brand-muted); }              /* their problem, red eyebrow */
.archetype-card .a-why { border-left:3px solid var(--brand-positive); padding-left:.65rem; }  /* why us */
.archetype-card .a-cust { font-family: var(--brand-font-mono); color: var(--brand-primary); }  /* Real story: <customer> */

/* Slide 2: committee + segments */
.persona-card .role-tag { border-radius: var(--brand-radius-pill); font-size:.6rem; }   /* Champion / Econ buyer */
.seg-card { background: var(--brand-surface); border-radius: var(--brand-radius); padding:.85rem 1rem; }  /* uniform, no "Primary" tag or ranking */
.segment-chip { border:1px solid var(--brand-border); border-radius: var(--brand-radius-pill); }   /* the "also a fit" row */

/* generic tabset — used by Slide 3 (personas), Slide 4 (competitors), Slide 5 (proof) */
.tabset { }
.tabs { display:flex; flex-wrap:wrap; gap:.45rem; margin-bottom:1.1rem; }
.tab { font-family: var(--brand-font-mono); border:1px solid var(--brand-border); border-radius: var(--brand-radius-pill); padding:.45rem .9rem; cursor:pointer; }
.tab[aria-selected="true"] { background: var(--brand-primary); color:#fff; border-color: var(--brand-primary); }
.tpanel { display:none; } .tpanel.active { display:block; }

/* Slide 3 persona panel */
.block-label { font-family: var(--brand-font-mono); color: var(--brand-primary); text-transform:uppercase; }
.leadwith { background: var(--brand-surface); border-radius: var(--brand-radius); }
.rec-strip { display:grid; grid-template-columns:repeat(3,1fr); gap:.65rem; }         /* Resonate / Elevate / Compel */
.rec-stage { border-top:3px solid var(--brand-accent); border-radius:10px; }
.pending-note { background: var(--brand-warning-weak); border:1px dashed; }            /* persona with no ready ICP version */

/* Slide 4 competitor deep-dive */
.comp-verdict { border-radius: var(--brand-radius-pill); font-size:.62rem; }           /* Direct / Adjacent / Build */
.cap-table { width:100%; border-collapse:collapse; }                                   /* Capability | them | Octave */
.cap-table .us { background: color-mix(in srgb, var(--brand-primary) 6%, transparent); }
.hearsay { display:grid; grid-template-columns:1fr 1fr; gap:.7rem; }                    /* You'll hear | What to say */
.hs-say { background: var(--brand-positive-weak); }
.watchlist { background: var(--brand-surface); border-radius: var(--brand-radius); }    /* lesser + honest-gap competitors */

/* Slide 5 proof (lenses via .tabset); .proof-card uses subgrid to align bands */
.proof-card { display:grid; grid-template-rows:subgrid; grid-row:span 3; }

/* checkpoints */
.checkpoints { border-top:2px solid var(--brand-border); padding-top:1.1rem; }
.checkpoint { margin-bottom:1.15rem; }
.cp-opt { display:block; width:100%; text-align:left; border:1px solid var(--brand-border); border-radius:10px; cursor:pointer; }
.cp-opt.correct { border-color: var(--brand-positive); background: var(--brand-positive-weak); }
.cp-opt.wrong { border-color: var(--brand-negative); background: var(--brand-negative-weak); }
.cp-explain { display:none; border-left:2px solid var(--brand-border); } .cp-explain.show { display:block; }
.btn-primary:disabled { opacity:.4; cursor:not-allowed; }

/* completion */
.score-big { font-family: var(--brand-font-heading); font-size: clamp(3.5rem,9vw,6rem); }
.review-menu button { border-radius: var(--brand-radius-pill); }

@media print { .persona-panel, .tpanel { display:block !important; } .tabs { display:none; } .cp-explain { display:block !important; } .cp-opt[data-answer="true"] { border-color: var(--brand-positive); } }
@media (max-width:760px) { .how-steps, .rec-strip, .hearsay, .proof-grid, .seg-grid, .grid-2, .grid-3 { grid-template-columns:1fr; } }
@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } }
```

## Body skeleton

```html
<div class="topbar"><img class="brand" ...><span class="step-label"></span><div class="progress-dots" id="dots"></div></div>
<div class="deck">
  <section class="slide gradient active" data-type="cover">...Start button calls go(1)...</section>
  <section class="slide" data-type="content"><!-- Slide 1: What we sell -->
    <div class="slide-inner">
      <div class="slide-body">
        ...lead, callout, archetype cards, why-now, how-steps, product card...
        <div class="checkpoints">
          <div class="checkpoint" data-checkpoint> <div class="q-text">...</div>
            <div class="cp-opts"><button class="cp-opt" data-answer="true|false">...</button>...</div>
            <div class="cp-explain">...</div>
          </div>
          <!-- more checkpoints -->
        </div>
      </div>
      <div class="slide-nav"><button class="btn" onclick="go(0)">Back</button><div class="spacer"></div>
        <span class="nav-hint" data-hint>Clear the checkpoints to continue</span>
        <button class="btn btn-primary" data-next disabled onclick="go(2)">Next</button></div>
    </div>
  </section>
  <!-- Slide 2 (committee + segments), Slide 3 (persona .tabset), Slide 4 (competitor .tabset), Slide 5 (proof .tabset) -->
  <section class="slide gradient" data-type="done"><!-- score-big, score-msg, review-menu, restart --></section>
</div>
```

Slides 3, 4, 5 each hold a `<div class="tabset" data-tabset>` with a `.tabs` row of `.tab` buttons and index-matched `.tpanel`s (first `.active`).

## The script (behavior)

Inline, no framework. Four responsibilities:

```js
// 1) Navigation + gating
const slides = [...document.querySelectorAll('.slide')];
const contentIdx = slides.map((s,i)=> s.dataset.type==='content'?i:-1).filter(i=>i>=0);
const slideDone = {};                 // content slide index -> all checkpoints answered
function canReach(idx){ return idx<=current || contentIdx.filter(i=>i<idx).every(i=>slideDone[i]); }
function go(idx){ /* swap .active, updateChrome(), scroll body to top, showScore() on done */ }

// 2) Progress dots: one per content slide, click to reach (guarded by canReach), classes current/done/locked

// 3) Checkpoints: per content slide, on option click -> lock that checkpoint, mark correct/wrong,
//    reveal .cp-explain, record first-attempt correctness. When EVERY .checkpoint on the slide is
//    answered -> slideDone[sIdx]=true and enable [data-next]; hint shows "N of M correct".

// 4) Generic tabsets: for each [data-tabset], wire its ':scope > .tabs > .tab' buttons to its
//    ':scope > .tpanel' children by index (aria-selected + .active). Independent per tabset.

// Completion: score = count of checkpoints with first-attempt correct / total checkpoints.
// restart(): clear slideDone + checkpoint state, re-disable Next, go(0).
// keydown: ArrowRight advances only when [data-next] is enabled (or from cover); ArrowLeft goes back.
```

Use `:scope >` selectors when wiring tabsets so the three independent selectors (personas, competitors, proof) do not cross-fire. Gating is independent of tabsets: a slide with a tab selector still gates on its checkpoints.

## Notes

- **The gate is the point.** Next must be disabled until all checkpoints on the slide are answered. Must-answer, not must-be-correct, so no dead ends.
- **Checkpoints run one question at a time.** Only `.checkpoint.current` is shown, with a "Question X of N" counter and a small progress bar. On answer: lock it, reveal the explanation, and reveal a "Next question" button (except on the last) that advances `.current` to the next checkpoint. On answering, smooth-scroll the explanation and Next-question button into view so the reveal never leaves them below the fold (a known funky-scroll fix). The last checkpoint answered unlocks the slide's Next button in the always-visible nav.
- **The revealed explanation stacks vertically**: `.cp-explain.show { display: flex; flex-direction: column; align-items: flex-start; }` so the "Next question" button drops onto its own line **below** the explanation text, left-aligned. Do NOT leave the advance button as an inline element after the text, or it floats to the right and the text wraps under it (a known "wonky" layout bug).
- **One checkpoint per persona on Slide 3**, so the score reflects knowing every buyer.
- **Capability tables and hear/say** must trace to the competitor entity descriptions; never invent a row or a checkmark.
- **Pending panels** (persona with no ICP version, competitor deal mentions with no findings) use the dashed `.pending-note`, never fabricated content.
- **Logo is dynamic and inlined.** Never hardcode a logo. Resolve it from the workspace company's brand kit (`manifest.json` `logo` block) so it is the correct company's mark, and inline it as a base64 **data URI** so the file is self-contained. Use the onLight variant on the light topbar and the onDark/white variant on the dark cover, completion, and the topbar while those show. Swap the topbar logo `src` between the two in `updateChrome()` based on the current slide's `data-type`. Recolor-to-white via `filter` only as a fallback when the kit ships a single logo.
- **Self-contained:** inline CSS + JS and the logo (data URI); only Google Fonts (or kit `@font-face`) external. No frameworks, no network calls.
