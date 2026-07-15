# Champion Deal-Room HTML Scaffold

Implements [../../shared/formats/html-document.md](../../shared/formats/html-document.md) (scroll-based reading flow, sticky nav, card-based containers, print flattening) and [../../shared/presentation-principles.md](../../shared/presentation-principles.md) (universal visual rules) for this skill's specific case: a dense, self-contained working document in the meeting-prep battle-plan style: sticky sidebar nav dots, collapsible `details` sections (open by default, forced open on print), and a real card vocabulary. Styled with the workspace company's brand kit (inline `tokens.css` `:root` + the brand's Google Fonts). No external requests beyond Google Fonts.

This is NOT a full-viewport scrolling landing page. It is a max-900px document column with information density. Reproduce this structure and vocabulary.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deal Room: [Company] — [Workspace Company]</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
<style>
  :root { /* inline the workspace brand tokens.css :root here */ }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
  html{scroll-behavior:smooth;}
  body{font-family:var(--brand-font-body);background:var(--brand-bg);color:var(--brand-ink);line-height:1.55;-webkit-font-smoothing:antialiased;}

  /* layout */
  .room{max-width:900px;margin:0 auto;padding:2rem clamp(1rem,4vw,3rem);}
  .hl{background-image:linear-gradient(var(--brand-accent),var(--brand-accent));background-repeat:no-repeat;background-size:100% 34%;background-position:0 88%;-webkit-box-decoration-break:clone;box-decoration-break:clone;}

  /* sidebar nav dots */
  .nav{position:fixed;top:50%;right:clamp(.5rem,2vw,2rem);transform:translateY(-50%);display:flex;flex-direction:column;gap:.5rem;z-index:100;}
  .nav a{width:9px;height:9px;border-radius:50%;background:var(--brand-border);transition:all .3s ease;}
  .nav a.active{background:var(--brand-primary);transform:scale(1.4);}

  /* masthead + verdict */
  .masthead{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;padding-bottom:1rem;border-bottom:1px solid var(--brand-border);}
  .masthead .ms-logo svg{height:26px;width:auto;display:block;}
  .masthead .prepared{font-family:var(--brand-font-mono);font-size:.7rem;letter-spacing:.02em;color:var(--brand-muted);text-transform:uppercase;}
  .masthead .prepared b{color:var(--brand-ink);}
  .verdict{background:var(--brand-band);color:#fff;border-radius:var(--brand-radius-section);padding:1.5rem 1.75rem;margin:1.5rem 0;}
  .verdict h1{font-family:var(--brand-font-heading);font-weight:500;font-size:clamp(1.4rem,3vw,1.9rem);line-height:1.2;margin-bottom:.6rem;text-wrap:balance;}
  .verdict p{color:var(--brand-on-dark);font-size:.98rem;text-wrap:pretty;}

  /* deal-intel stat strip */
  .intel{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.75rem;margin-bottom:1.5rem;}
  .intel .card{background:var(--brand-surface);border:1px solid var(--brand-border);border-radius:var(--brand-radius);padding:1rem;text-align:center;}
  .intel .label{font-family:var(--brand-font-mono);font-size:.62rem;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-muted);margin-bottom:.3rem;}
  .intel .value{font-family:var(--brand-font-heading);font-weight:500;font-size:1.05rem;}

  /* collapsible sections */
  details.section{border-top:1px solid var(--brand-border);padding:.5rem 0 1.25rem;}
  details.section summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:.6rem;padding:1rem 0;font-family:var(--brand-font-heading);font-weight:500;font-size:clamp(1.15rem,2.2vw,1.45rem);}
  details.section summary::-webkit-details-marker{display:none;}
  details.section summary::before{content:"\25B6";font-size:.6em;color:var(--brand-primary);transition:transform .2s ease;}
  details.section[open] summary::before{transform:rotate(90deg);}
  .eyebrow{font-family:var(--brand-font-mono);font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--brand-primary);}

  /* generic card + grids */
  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;}
  .card{background:var(--brand-surface);border:1px solid var(--brand-border);border-radius:var(--brand-radius);padding:1.1rem 1.25rem;}

  /* business case: cost table + stat cards */
  .case-table{width:100%;border-collapse:collapse;font-size:.9rem;margin-bottom:1rem;}
  .case-table td{padding:.6rem .5rem;border-bottom:1px solid var(--brand-border);}
  .case-table td.n{font-family:var(--brand-font-heading);font-weight:500;text-align:right;white-space:nowrap;}
  .case-table .basis{display:block;font-family:var(--brand-font-mono);font-size:.62rem;color:var(--brand-muted);text-transform:uppercase;letter-spacing:.03em;}
  .est{font-family:var(--brand-font-mono);font-size:.58rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:.08rem .35rem;border-radius:var(--brand-radius-pill);background:var(--brand-border-soft);color:var(--brand-muted);vertical-align:middle;}
  .case-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.75rem;}
  .case-stats .big{font-family:var(--brand-font-heading);font-weight:500;font-size:1.7rem;color:var(--brand-primary);}
  .case-stats .lab{font-size:.8rem;color:var(--brand-muted);}

  /* committee stakeholder cards */
  .committee{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.9rem;}
  .stake{background:var(--brand-surface);border:1px solid var(--brand-border);border-radius:var(--brand-radius);padding:1.1rem 1.25rem;}
  .stake.champion{border:2px solid var(--brand-primary);}
  .role-badge{display:inline-block;font-family:var(--brand-font-mono);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#fff;background:var(--brand-primary);padding:.2rem .55rem;border-radius:var(--brand-radius-pill);}
  .pos{display:inline-flex;align-items:center;gap:.35rem;font-size:.7rem;color:var(--brand-muted);margin-left:.4rem;}
  .pos .dot{width:9px;height:9px;border-radius:50%;}
  .dot.supporter{background:var(--brand-positive);} .dot.neutral{background:var(--brand-yellow);} .dot.skeptic{background:var(--brand-negative);} .dot.champion{background:var(--brand-primary);}
  .stake .who{font-weight:600;font-size:.95rem;margin:.5rem 0 .4rem;}
  .stake .need{border-left:3px solid var(--brand-accent);padding-left:.7rem;font-size:.88rem;text-wrap:pretty;}
  .stake .gap{font-size:.75rem;color:var(--brand-muted);margin-top:.5rem;}
  .tier-label{font-family:var(--brand-font-mono);font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-muted);margin:1rem 0 .6rem;}
  .stake.role{border-style:dashed;background:transparent;}
  .stake .fillname{color:var(--brand-muted);font-style:italic;font-weight:400;}
  .suggested{font-family:var(--brand-font-mono);font-size:.55rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:.08rem .35rem;border-radius:var(--brand-radius-pill);background:var(--brand-border-soft);color:var(--brand-muted);vertical-align:middle;}

  /* pushback Q&A */
  .qa{border:1px solid var(--brand-border);border-radius:var(--brand-radius);padding:1.1rem 1.25rem;margin-bottom:.75rem;background:var(--brand-surface);}
  .qa .q{font-family:var(--brand-font-heading);font-weight:500;font-size:.98rem;margin-bottom:.4rem;}
  .qa .q::before,.qa .q::after{content:"\201C";color:var(--brand-primary);} .qa .q::after{content:"\201D";}
  .qa .a{font-size:.88rem;color:var(--brand-muted);text-wrap:pretty;}

  /* proof cards */
  .proof{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.9rem;}
  .proof .co{font-family:var(--brand-font-mono);font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-primary);margin-bottom:.5rem;}
  .proof .outcome{font-family:var(--brand-font-heading);font-weight:500;font-size:.98rem;text-wrap:pretty;}
  .proof .quote{font-size:.82rem;color:var(--brand-muted);font-style:italic;margin-top:.6rem;}
  .proof .attr{font-family:var(--brand-font-mono);font-size:.62rem;color:var(--brand-muted);margin-top:.4rem;}

  /* path timeline + cost of waiting */
  .step{display:grid;grid-template-columns:110px 1fr;gap:1rem;padding:.8rem 0;border-bottom:1px solid var(--brand-border);}
  .step .when{font-family:var(--brand-font-mono);font-size:.78rem;color:var(--brand-primary);font-weight:700;}
  .cost-wait{margin-top:1rem;border-left:3px solid var(--brand-negative);padding:.75rem 1rem;background:var(--brand-surface);font-size:.9rem;}

  @media (max-width:768px){.grid-2,.committee,.proof,.case-stats,.intel{grid-template-columns:1fr;}.step{grid-template-columns:1fr;gap:.25rem;}.nav{display:none;}}
  @media print{.nav{display:none;}details.section{border-color:#ccc;}details.section[open] summary::before,details.section summary::before{content:"";}.verdict,.role-badge{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}*{transition:none!important;}}
</style>
</head>
<body>
<div class="room">

  <header class="masthead">
    <span class="ms-logo">[workspace logo SVG inline]</span>
    <span class="prepared">Prepared for <b>[Company]</b> &middot; for [Champion first name], to take to the committee</span>
  </header>

  <!-- Verdict -->
  <section class="verdict">
    <h1>[State of play in one line, e.g. "A workspace-security consolidation Acme can prove in its own tenant before committing."]</h1>
    <p>[2 sentences: what is being evaluated, why now, why it's worth committee time.]</p>
  </section>

  <!-- Deal-intel strip -->
  <div class="intel">
    <div class="card"><div class="label">Compelling event</div><div class="value">[trigger]</div></div>
    <div class="card"><div class="label">Champion</div><div class="value">[name]</div></div>
    <div class="card"><div class="label">Committee</div><div class="value">[N seats]</div></div>
    <div class="card"><div class="label">The case</div><div class="value">[headline number]</div></div>
  </div>

  <!-- Job 1 -->
  <details class="section" open id="case-for-change">
    <summary>The case for change</summary>
    <!-- the problem in their words (2-3 bullets), why now, the open question -->
  </details>

  <!-- Job 2 -->
  <details class="section" open id="positioning-value">
    <summary>Positioning and value</summary>
    <p class="eyebrow">How to position it</p>
    <!-- the one-line value frame + what it replaces/offsets -->
    <p class="eyebrow">The value case</p>
    <table class="case-table"><!-- cost of status quo; real numbers or labeled estimates only --></table>
    <div class="case-stats"><!-- big number + label cards; reference outcomes labeled "your expected direction", ≤3 --></div>
  </details>

  <!-- Job 3: DATA-GATED. The champion is the READER, never a card here. Map everyone else. -->
  <details class="section" open id="committee">
    <summary>Who else to bring in</summary>
    <!-- Tier 1, OMIT ENTIRELY if the only confirmed person is the champion (common early): -->
    <p class="tier-label">Confirmed, from your deal</p>
    <div class="committee">
      <div class="stake"><span class="role-badge">[seat]</span><span class="pos"><span class="dot supporter"></span>[position]</span><div class="who">[name, title]</div><div class="need">[what they need + how to frame it]</div></div>
      <!-- only real deal-signal people OTHER than the champion (call/CRM/email) -->
    </div>
    <p class="tier-label">Roles to loop in</p>
    <div class="committee">
      <div class="stake role"><span class="role-badge">[seat]</span><div class="who"><span class="fillname">Name: ____</span></div><div class="need">[what they'll care about + the line that lands]</div><div class="gap">Possible: [find_person suggestion] <span class="suggested">you confirm</span></div></div>
    </div>
  </details>

  <!-- Job 4 -->
  <details class="section" open id="objections">
    <summary>Objection handling</summary>
    <div class="qa"><div class="q">[objection]</div><div class="a">[answer + proof anchor]</div></div>
  </details>

  <!-- Job 5 -->
  <details class="section" open id="proof">
    <summary>Proof and references</summary>
    <div class="proof"><div class="card"><div class="co">[Reference]</div><div class="outcome">[result]</div><p class="quote">"[quote]"</p><p class="attr">[attribution]</p></div></div>
  </details>

  <!-- Job 6 -->
  <details class="section" open id="path">
    <summary>The path forward</summary>
    <div class="step"><div class="when">[step 1, low-risk]</div><div>[who does what]</div></div>
    <div class="cost-wait">[Cost of waiting, tied to the compelling event.]</div>
  </details>

</div>
<script>
  // Build nav dots from .section + verdict; IntersectionObserver sets .active; smooth-scroll on click.
  // Force all <details> open on window.onbeforeprint. No other JS.
</script>
</body>
</html>
```

**Section order is fixed:** masthead → verdict → intel strip → case-for-change → positioning-value → committee → objections → proof → path. Do not add sections or a top nav bar.
