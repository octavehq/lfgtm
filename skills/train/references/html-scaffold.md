# Onboarding GTM Primer — HTML Scaffold (gated slide lesson)

A single self-contained HTML file. Inline all CSS and JS; the only external dependency is Google Fonts (or the brand kit's `@font-face`). The head carries the social share block (og:title + og:description always, relative og:image when published; canonical block in [../../shared/social-meta.md](../../shared/social-meta.md)). The primer is a **gated slide lesson**: fixed-viewport slides, a progress-dot rail, per-slide checkpoints that unlock the Next button, interactive tab selectors (personas, competitors, proof lenses), and a scored completion slide.

**Styling comes from the workspace company's brand kit.** Inline the kit's `tokens.css` (`:root` + `@font-face`) and `../../get-brand-components/assets/kit_base.css`, then map the component classes below onto the kit's `--brand-*` variables. The classes here are structural; the brand kit supplies color, type, radius, and signature moves. (When authoring a cleaned `:root`, do not paste comment lines from the kit that contain em/en-dashes; the lint rejects them.)

## Layout model

- `body { overflow: hidden }`. A fixed `.topbar` (logo, step label, progress dots). A `.deck` holding absolutely-positioned `.slide`s; only `.slide.active` is shown.
- Each content slide: `.slide-inner` (flex column, full height) > `.slide-body` (flex:1, `overflow-y:auto`, holds content + `.checkpoints`) + `.slide-nav` (pinned, Back / hint / Next).
- Cover and completion are `.slide.gradient` (brand dark/gradient band, centered).

## Core CSS components

```css
/* progress rail */
.topbar { position: fixed; top:0; left:0; right:0; height:56px; display:flex; align-items:center; gap:1.25rem; z-index:10; background:var(--brand-bg); }
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
.rec-strip { display:grid; grid-template-columns:repeat(3,1fr); gap:.65rem; }         /* three talk-track stages, named by the workspace's methodology */
.rec-stage { border-top:3px solid var(--brand-accent); border-radius:10px; }
.pending-note { background: var(--brand-warning-weak); border:1px dashed; }            /* persona with no ready ICP version */

/* Slide 4 competitor deep-dive */
.comp-verdict { border-radius: var(--brand-radius-pill); font-size:.62rem; }           /* Direct / Adjacent / Build */
.cap-table { width:100%; border-collapse:collapse; }                                   /* Capability | alternative | selected offering */
.cap-table-wrap { overflow-x:auto; }
/* below 520px each capability row becomes a card, and every cell names its column (data-label = the header text),
   so the selected offering's column is never the one pushed off-screen (presentation principle 9k) */
@media (max-width:520px) {
  .cap-table thead { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
  .cap-table, .cap-table tbody, .cap-table tr, .cap-table td, .cap-table th[scope=row] { display:block; }
  .cap-table tr { border:1px solid var(--brand-border); border-radius:10px; padding:.6rem .8rem; margin-bottom:.6rem; }
  .cap-table td[data-label]::before { content:attr(data-label); display:block; font-size:.7rem; text-transform:uppercase; letter-spacing:.05em; color:var(--brand-muted); }
}
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

/* completion: the score and each topic's result; beside them, once published, a note to the lesson's owner */
.score-big { font-family: var(--brand-font-heading); font-size: clamp(3.5rem,9vw,6rem); line-height:1; margin:0; font-variant-numeric: tabular-nums; }
/* centered with auto margins, not justify-content: when the slide is taller than a phone the top stays reachable */
.slide.gradient .slide-inner:has(.done-grid) { justify-content:flex-start; overflow-y:auto; }
.done-grid { width:100%; max-width:1040px; margin-block:auto; padding:1.5rem 0; display:grid; grid-template-columns:minmax(0,1fr); justify-items:center; gap:1.75rem; text-align:center; }
.done-score { display:flex; flex-direction:column; align-items:center; gap:1rem; width:100%; max-width:520px; min-width:0; }
.done-k { margin:0; text-transform:uppercase; letter-spacing:.06em; font-size:.8rem; font-weight:600; color: var(--brand-on-dark); }
.score-msg { margin:0; font-size:1.15rem; text-wrap:pretty; }
/* review links are rows that carry the topic's result; lesson.js fills .rv-score and lists topics with a miss first */
.review-menu { display:grid; grid-template-columns:minmax(0,1fr); justify-content:stretch; gap:8px; width:100%; max-width:460px; }
.review-menu button { display:flex; align-items:center; justify-content:space-between; gap:1rem; width:100%; min-height:44px; padding:.6rem .95rem; text-align:left; cursor:pointer;
  font-family: var(--brand-font-body); font-size:.95rem; line-height:1.3; color: var(--brand-faint, rgba(255,255,255,.7));
  border:1px solid var(--brand-border-dark, rgba(255,255,255,.16)); border-radius: var(--brand-radius-tile, 10px); background: color-mix(in srgb, #fff 4%, transparent); }
.review-menu button:hover { background: color-mix(in srgb, #fff 9%, transparent); border-color: rgba(255,255,255,.34); }
.review-menu button[data-result=missed] { color:#fff; border-color: rgba(255,255,255,.34); }
.rv-score { flex:0 0 auto; font-size:.85rem; font-variant-numeric: tabular-nums; white-space:nowrap; }
.review-menu button[data-result=missed] .rv-score { font-weight:600; }
.btn-quiet { min-height:44px; padding:.4rem 0; border:0; background:none; cursor:pointer; font-family: var(--brand-font-body); font-size:.9rem;
  color: var(--brand-faint, rgba(255,255,255,.7)); text-decoration:underline; text-underline-offset:3px; text-decoration-color: rgba(255,255,255,.35); }
.btn-quiet:hover { color:#fff; text-decoration-color: currentColor; }
.done-grid .meta-line { grid-column:1/-1; }
/* shown only when the lesson is published: Octave's recorder marks <html data-octave-recording> */
.done-form, .record-note { display:none; }
.record-note { margin:0; font-size:.8rem; line-height:1.45; color: var(--brand-faint, rgba(255,255,255,.7)); }
html[data-octave-recording] .record-note { display:block; }
html[data-octave-recording] .done-form { display:flex; justify-content:center; width:100%; min-width:0; }
@media (min-width:861px) {
  html[data-octave-recording] .done-grid { grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr); gap:1.75rem clamp(2rem,5vw,4.5rem); align-items:center; justify-items:stretch; text-align:left; }
  html[data-octave-recording] .done-score { align-items:flex-start; max-width:none; }
  html[data-octave-recording] .done-form { justify-content:flex-end; }
}

@media print {
 html,body,.deck{height:auto!important;overflow:visible!important}
 .slide,.slide.active{display:block!important;position:static!important;height:auto!important;padding-top:0!important;break-after:page}
 .slide:last-child{break-after:auto}
 .slide-inner,.slide-body{height:auto!important;overflow:visible!important}
 .tpanel,.persona-panel,.checkpoint,.cp-explain{display:block!important}
 .topbar,.slide-nav,.tabs,.review-menu,[data-next-question]{display:none!important}
}
:focus-visible{outline:3px solid var(--brand-primary);outline-offset:3px}
@media (max-width:760px) { .how-steps, .rec-strip, .hearsay, .proof-grid, .seg-grid, .grid-2, .grid-3 { grid-template-columns:1fr; } }
@media (max-width:520px) { .topbar { gap:.75rem; padding:0 16px; } .step-label { display:none; } .progress-dots { min-width:0; flex-wrap:wrap; } .slide-inner { padding-left:16px; padding-right:16px; } .tab, .cp-opt, .slide-nav .btn { min-height:44px; } }
.slide-body > *, .archetype-card, .seg-card, .proof-card { min-width:0; }
@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } }
```

## Body skeleton

```html
<div class="topbar"><img class="brand" ...><span class="step-label"></span><div class="progress-dots" id="dots"></div></div>
<div class="deck">
  <section class="slide gradient active" data-type="cover"><button data-start>Start</button></section>
  <section class="slide" data-type="content"><!-- Slide 1: What we sell -->
    <div class="slide-inner">
      <div class="slide-body">
        ...lead, callout, archetype cards, why-now, how-steps, product card...
        <div class="checkpoints">
          <div class="checkpoint" data-checkpoint="sell-1"> <div class="q-text">...</div>
            <div class="cp-opts"><button class="cp-opt" data-answer="true|false">...</button>...</div>
            <div class="cp-explain">...</div>
          </div>
          <!-- more checkpoints -->
        </div>
      </div>
      <div class="slide-nav"><button class="btn" data-prev>Back</button><div class="spacer"></div>
        <span class="nav-hint" data-hint>Clear the checkpoints to continue</span>
        <button class="btn btn-primary" data-next disabled>Next</button></div>
    </div>
  </section>
  <!-- Slide 2 (committee + segments), Slide 3 (persona .tabset), Slide 4 (competitor .tabset), Slide 5 (proof .tabset) -->
  <section class="slide gradient" data-type="done" id="done">
    <div class="slide-inner">
      <div class="done-grid">
        <div class="done-score">
          <p class="done-k">Your score</p>
          <p class="score-big"></p>
          <p class="score-msg" data-score-msg></p>
          <div class="review-menu"><button data-go="slide-id">Topic title</button><!-- one per content slide --></div>
          <p class="record-note">Your answers are shared with the person who sent you this lesson.</p>
          <button class="btn-quiet" data-restart>Restart the lesson</button>
        </div>
        <div class="done-form">
          <form class="rf" data-octave-form="lesson-feedback">
            <div class="rf-head"><h3 class="rf-title">What should this lesson explain better?</h3>
              <p class="rf-lede">One line is enough. It goes to whoever keeps this primer current.</p></div>
            <div class="rf-fields"><div class="rf-field"><label for="fb-notes">Your note</label>
              <textarea id="fb-notes" name="notes" required maxlength="2000"></textarea></div></div>
            <div class="rf-actions"><button class="btn btn-primary" type="submit">Send note</button>
              <p data-octave-notice>Shared with the owner of this lesson.</p></div>
          </form>
          <div class="rf-done" data-octave-done="lesson-feedback" role="status" hidden>
            <span class="rf-check" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M3.5 8.5l3 3 6-6.5"/></svg></span>
            <div><h3 class="rf-title">Note sent</h3><p>Thanks. It will shape the next version of this lesson.</p></div>
          </div>
        </div>
        <p class="meta-line"><!-- generation date, covered remit, "a learning aid, not a certification" --></p>
      </div>
    </div>
  </section>
</div>
```

Slides 3, 4, 5 each hold a `<div class="tabset" data-tabset>` with a `.tabs` row of `.tab` buttons and index-matched `.tpanel`s (first `.active`).

## The script (behavior)

Inline, no framework. Four responsibilities:

Inline [lesson.js](../assets/lesson.js) after the lesson DOM.

## Results: what the owner sees

A published lesson reports what each learner did to its owner, through the recorder Octave adds to every hosted page ([asset responses](../../shared/asset-responses.md)). lesson.js makes the calls; the lesson HTML only has to be well formed:

- **Give every checkpoint a stable id**: `data-checkpoint="sell-1"`, unique in the lesson and kept when the lesson is edited, so one question's answers line up across versions. An empty `data-checkpoint` still works and is numbered by position.
- **`.q-text` holds the question and nothing else.** Its text and the chosen option's text are what the owner reads, so neither carries numbering, icons or hidden helper text.
- **What is recorded:** `answer` per checkpoint (question, choice, correct), `slide` as each topic is first reached, `score` on the completion slide, `restart`, and the feedback form (`form`, key `lesson-feedback`). Each lesson event carries an `attempt` number that goes up on every restart, because the owner sees the latest answer per question. Nothing is recorded when the file is opened from disk.
- **The completion slide tells the learner.** `.record-note` and the feedback form appear only when the page is really being recorded (`html[data-octave-recording]`), so a local copy never shows a form that goes nowhere. Keep the note's meaning when rewording it: answers are shared with whoever sent the lesson.
- **Named results need named viewers.** Publish at workspace tier or share to named recipients when the owner wants to know who answered what. A public or open link gives anonymous results; say so before publishing that way, and only then add optional name and email fields to the form (the [response form](../../shared/formats/response-form.css) has the `.rf-row` for them).
- **The form is the shared component.** Inline [response-form.css](../../shared/formats/response-form.css) after the kit's tokens and `kit_base.css`; do not restyle its fields per lesson.



Use `:scope >` selectors when wiring tabsets so the three independent selectors (personas, competitors, proof) do not cross-fire. Gating is independent of tabsets: a slide with a tab selector still gates on its checkpoints.

## Notes

- **The gate is the point.** Next must be disabled until all checkpoints on the slide are answered. Must-answer, not must-be-correct, so no dead ends.
- Show each checkpoint with its explanation immediately below it; wrong answers unlock after the explanation. Every earlier content slide must be answered before jumping ahead. Review links use `data-go="slide-id"`; restart uses `data-restart`.
- **The revealed explanation stacks vertically**: `.cp-explain.show { display: flex; flex-direction: column; align-items: flex-start; }` so the "Next question" button drops onto its own line **below** the explanation text, left-aligned. Do NOT leave the advance button as an inline element after the text, or it floats to the right and the text wraps under it (a known "wonky" layout bug).
- **One checkpoint per persona on Slide 3**, so the score reflects knowing every buyer.
- **Capability tables and hear/say** must trace to the competitor entity descriptions; never invent a row or a checkmark. Each `td` carries `data-label` with its column header (the alternative's name, the selected offering's name) so the table stacks into labelled cards at 375px; check at 375 that the selected offering's column is visible in every row.
- **Pending panels** (persona with no ICP version, competitor deal mentions with no findings) use the dashed `.pending-note`, never fabricated content.
- **Logo is dynamic and inlined.** Never hardcode a logo. Resolve it from the workspace company's brand kit (`manifest.json` `logo` block) so it is the correct company's mark, and inline it as a base64 **data URI** so the file is self-contained. Use the onLight variant on the light topbar and the onDark/white variant on the dark cover, completion, and the topbar while those show. Swap the topbar logo `src` between the two in `updateChrome()` based on the current slide's `data-type`. Recolor-to-white via `filter` only as a fallback when the kit ships a single logo.
- **Self-contained:** inline CSS + JS and the logo (data URI); only Google Fonts (or kit `@font-face`) external. No frameworks, and no network calls of its own: the only requests a published lesson makes are the recorder's, which Octave adds when it serves the page.
