# Account Plan — HTML Scaffold

The proven, self-contained scaffold for the six-job account plan (locked from the Coinbase v2 build). Reproduce this structure and card vocabulary. Content specifics come from `account-plan-template.md`; brand tokens come from the workspace company's cached kit.

**Rules:** self-contained (inline CSS/JS, only Google Fonts external). No em-dashes or en-dashes. The `:root` brand block is inlined from `~/.octave/brands/<workspace-slug>/tokens.css` plus `get-brand-components/assets/kit_base.css`; the semantic + component CSS below is the reusable scaffold. Six sections in order, conclusion-carrying headers, sidebar nav dots, persona selector in section 5, print flattening.

## `<head>` + `<style>`

```html
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Account Plan: [Company]</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=[kit fonts]&display=swap" rel="stylesheet">
<style>
/* ===== Brand tokens inlined from the workspace kit (tokens.css + kit_base.css). Below is the Material Security set as reference. ===== */
:root{
  --brand-bg:#efefef; --brand-bg-alt:#ffffff; --brand-surface:#ffffff;
  --brand-ink:#333; --brand-muted:#666; --brand-on-dark:#efefef;
  --brand-primary:#4f87b8; --brand-accent:#6cafd9; --brand-band:#111;
  --brand-border:#d8d8d8; --brand-border-soft:#e6e6e6;
  --brand-positive:#a3b98a; --brand-negative:#e16464; --brand-yellow:#f2c861; --brand-purple:#816189; --brand-teal:#68adad;
  --brand-font-heading:"[kit heading]",Arial,sans-serif; --brand-font-body:"[kit body]",Arial,sans-serif; --brand-font-mono:"[kit mono]",ui-monospace,monospace;
  --brand-radius:10px; --brand-radius-pill:999px; --brand-radius-section:20px;
  --brand-glow:radial-gradient(60% 80% at 50% 0%,rgba(79,135,184,.20),transparent 70%);
  --brand-grid-line:rgba(255,255,255,.06);
  /* semantic mappings */
  --bg:var(--brand-bg); --text-primary:var(--brand-ink); --text-secondary:#4a4a4a; --text-muted:var(--brand-muted);
  --border:var(--brand-border); --border-strong:#c9c9c9; --bg-card:var(--brand-surface); --bg-elevated:#f4f6f8;
  --success:var(--brand-positive); --warning:var(--brand-yellow); --error:var(--brand-negative); --secondary:var(--brand-teal); --warning-soft:rgba(242,200,97,.22);
  /* darkened on-tint text for AA contrast on tints (derive per kit) */
  --on-positive:#5c7040; --on-primary-tint:#2f6491; --on-purple:#6a4f72; --on-teal:#0f3535;
  --on-positive-strong:#2f3e1f; --on-yellow:#5a4712; --on-yellow-strong:#8a6d18; --on-negative:#b64a4a;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--text-primary);font-family:var(--brand-font-body);line-height:1.6;-webkit-font-smoothing:antialiased;padding:26px 0;}
.doc{max-width:920px;margin:0 auto;background:var(--brand-bg-alt);border-radius:var(--brand-radius-section);overflow:hidden;box-shadow:0 30px 90px -28px rgba(12,18,32,.22),0 0 0 1px rgba(12,18,32,.04);}

/* masthead with dot-grid + glow */
.masthead{position:relative;background:var(--brand-band);color:#fff;padding:34px 48px 30px;overflow:hidden;}
.masthead::before{content:"";position:absolute;inset:0;background:var(--brand-glow);}
.masthead::after{content:"";position:absolute;inset:0;background-image:radial-gradient(var(--brand-grid-line) 1px,transparent 1px);background-size:22px 22px;opacity:.8;}
.masthead>*{position:relative;z-index:1;}
.masthead .topbar{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:30px;}
.masthead .ms-logo svg{display:block;height:26px;width:auto;}
.masthead .acct{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.94);padding:8px 14px;border-radius:var(--brand-radius);}
.eyebrow,.k{font-family:var(--brand-font-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--brand-primary);margin-bottom:8px;}
.masthead .eyebrow{color:var(--brand-accent);}
.masthead h1{font-family:var(--brand-font-heading);font-weight:500;font-size:clamp(2rem,4vw,2.7rem);letter-spacing:-.02em;line-height:1.04;margin-bottom:10px;text-wrap:balance;}
.masthead .descriptor{color:var(--brand-on-dark);font-size:1rem;max-width:60ch;text-wrap:pretty;}
.masthead .datestamp{font-family:var(--brand-font-mono);font-size:11px;letter-spacing:.06em;color:rgba(239,239,239,.7);margin-top:14px;}

/* sidebar nav dots */
.side-nav{position:fixed;top:50%;right:clamp(.5rem,2vw,1.6rem);transform:translateY(-50%);display:flex;flex-direction:column;gap:.55rem;z-index:100;}
.side-nav a{display:block;width:9px;height:9px;border-radius:50%;background:var(--border-strong);transition:all .3s ease;text-indent:-9999px;overflow:hidden;}
.side-nav a.active{background:var(--brand-primary);transform:scale(1.45);}

main{padding:40px 48px 12px;}
.section{margin-bottom:30px;padding-bottom:26px;border-bottom:1px solid var(--border);}
.section:last-of-type{border-bottom:0;}
.section h2{font-family:var(--brand-font-heading);font-weight:500;font-size:clamp(1.3rem,2.4vw,1.62rem);letter-spacing:-.01em;line-height:1.16;margin-bottom:14px;text-wrap:balance;}
.section h2 .hl,.masthead h1 .hl{background-image:linear-gradient(transparent 62%,rgba(108,175,217,.42) 62%);background-repeat:no-repeat;-webkit-box-decoration-break:clone;box-decoration-break:clone;}
.lead-verdict{font-size:1.03rem;line-height:1.62;color:var(--text-primary);max-width:74ch;text-wrap:pretty;}
.muted{color:var(--text-muted);} .small{font-size:.82rem;}

/* §2 stat strip */
.deal-intel-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:20px;}
.deal-intel-card{padding:16px 18px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--brand-radius);}
.deal-intel-card .label{font-family:var(--brand-font-mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--text-muted);margin-bottom:6px;}
.deal-intel-card .value{font-family:var(--brand-font-heading);font-size:1.18rem;font-weight:500;line-height:1.2;}
.deal-intel-card .value .u{font-family:var(--brand-font-mono);font-size:.8rem;color:var(--brand-primary);}
.deal-intel-card .sub{font-size:.78rem;color:var(--text-muted);margin-top:3px;}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px;}
.stack-title{font-family:var(--brand-font-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:9px;}
.line-list{list-style:none;} .line-list li{display:flex;gap:9px;align-items:flex-start;font-size:.92rem;line-height:1.5;margin-bottom:9px;}
.line-list li .dot{flex:0 0 auto;width:7px;height:7px;border-radius:50%;margin-top:.5em;}
.dot.pos{background:var(--success);} .dot.warn{background:var(--brand-yellow);} .dot.neu{background:var(--brand-primary);}

/* §3 driver cards */
.driver{border-left:3px solid var(--brand-primary);background:var(--bg-elevated);padding:13px 16px;border-radius:0 var(--brand-radius) var(--brand-radius) 0;margin-bottom:11px;}
.driver .top{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:3px;}
.driver .pain{font-weight:600;font-size:.95rem;} .driver .body{font-size:.9rem;line-height:1.5;color:var(--text-secondary);}
.tag{display:inline-block;font-family:var(--brand-font-mono);font-size:9.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border-radius:var(--brand-radius-pill);vertical-align:middle;}
.tag.known{background:rgba(163,185,138,.28);color:var(--on-positive);} .tag.likely{background:rgba(108,175,217,.24);color:var(--on-primary-tint);} .tag.explore{background:rgba(129,97,137,.20);color:var(--on-purple);}

/* §4 stakeholder cards */
.people{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:6px;}
.person{display:flex;gap:14px;align-items:flex-start;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--brand-radius);padding:16px;}
.avatar{width:46px;height:46px;border-radius:50%;background:var(--brand-primary);color:#fff;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-family:var(--brand-font-heading);font-weight:600;}
.person .nm{font-weight:600;font-size:.98rem;line-height:1.2;} .person .tt{font-size:.82rem;color:var(--text-muted);margin:2px 0 8px;}
.role-badge{display:inline-block;padding:.16rem .55rem;border-radius:var(--brand-radius-pill);font-family:var(--brand-font-mono);font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;}
.role-badge.champion{background:var(--success);color:var(--on-positive-strong);} .role-badge.budget-owner{background:var(--brand-primary);color:#fff;} .role-badge.evaluator{background:var(--brand-teal);color:var(--on-teal);} .role-badge.gatekeeper{background:var(--brand-yellow);color:var(--on-yellow);}
.person .disp{font-size:.86rem;line-height:1.5;color:var(--text-secondary);margin:8px 0;}
.person a.li{font-family:var(--brand-font-mono);font-size:11px;color:var(--brand-primary);text-decoration:none;}
.unconfirmed{display:inline-flex;font-family:var(--brand-font-mono);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;padding:.1rem .4rem;border-radius:var(--brand-radius-pill);background:var(--warning-soft);color:var(--on-yellow-strong);margin-left:6px;}
.gap-line{margin-top:16px;background:rgba(225,100,100,.09);border:1px solid rgba(225,100,100,.25);border-radius:var(--brand-radius);padding:12px 15px;font-size:.9rem;line-height:1.55;}

/* §5 persona selector */
.persona-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 18px;}
.persona-tabs button{font-family:var(--brand-font-body);font-size:.86rem;font-weight:500;cursor:pointer;padding:9px 16px;border-radius:var(--brand-radius-pill);border:1px solid var(--border-strong);background:var(--bg-card);color:var(--text-secondary);transition:all .2s ease;}
.persona-tabs button[aria-selected="true"]{background:var(--brand-primary);color:#fff;border-color:var(--brand-primary);}
.persona-panel{display:none;} .persona-panel.active{display:block;}
.pfield{margin-bottom:15px;} .pfield .fh{font-family:var(--brand-font-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--brand-primary);margin-bottom:6px;}
.pfield ul{list-style:none;} .pfield li{display:flex;gap:9px;align-items:flex-start;font-size:.92rem;line-height:1.5;margin-bottom:6px;}
.pfield li .dot{flex:0 0 auto;width:6px;height:6px;border-radius:50%;background:var(--brand-primary);margin-top:.5em;}
.pfield p{font-size:.92rem;line-height:1.55;color:var(--text-secondary);}
.lead-with{background:var(--bg-elevated);border-left:3px solid var(--brand-primary);border-radius:0 var(--brand-radius) var(--brand-radius) 0;padding:13px 16px;}
.proof-fit{font-size:.86rem;color:var(--text-secondary);line-height:1.5;} .proof-fit b{color:var(--text-primary);}

/* §6 engagement */
.entry-card{background:var(--brand-band);color:#fff;border-radius:var(--brand-radius-section);padding:22px 24px;position:relative;overflow:hidden;margin-bottom:20px;}
.entry-card::before{content:"";position:absolute;inset:0;background:var(--brand-glow);} .entry-card>*{position:relative;z-index:1;}
.entry-card .k{color:var(--brand-accent);} .entry-card h3{font-family:var(--brand-font-heading);font-weight:500;font-size:1.2rem;margin-bottom:8px;} .entry-card p{color:var(--brand-on-dark);font-size:.92rem;line-height:1.55;}
.talk-track{background:var(--bg-elevated);border-left:3px solid var(--brand-primary);border-radius:0 var(--brand-radius) var(--brand-radius) 0;padding:14px 16px;margin-bottom:12px;}
.talk-track .label{font-family:var(--brand-font-mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--brand-primary);margin-bottom:7px;}
.talk-track .subj{font-weight:600;font-size:.9rem;margin-bottom:6px;} .talk-track .body{font-size:.88rem;line-height:1.6;color:var(--text-secondary);white-space:pre-line;}
.seq{list-style:none;counter-reset:step;margin-top:6px;}
.seq li{display:grid;grid-template-columns:30px 1fr;gap:14px;padding:11px 0;border-bottom:1px solid var(--border);} .seq li:last-child{border-bottom:0;}
.seq li::before{counter-increment:step;content:counter(step);font-family:var(--brand-font-mono);font-weight:700;font-size:.82rem;color:var(--brand-primary);width:26px;height:26px;border-radius:50%;background:var(--bg-elevated);display:flex;align-items:center;justify-content:center;}
.seq .st{font-size:.92rem;line-height:1.5;}

/* §7 risk grid */
.risk-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:6px;}
.risk-pair{display:contents;}
.risk-item,.mit-item{border-radius:var(--brand-radius);padding:14px 16px;font-size:.9rem;line-height:1.5;}
.risk-item{background:rgba(225,100,100,.08);border-left:3px solid var(--error);} .mit-item{background:rgba(163,185,138,.14);border-left:3px solid var(--success);}
.risk-item .rh,.mit-item .rh{font-family:var(--brand-font-mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;}
.risk-item .rh{color:var(--on-negative);} .mit-item .rh{color:var(--on-positive);}

/* footer */
.footer{background:var(--brand-band);color:var(--brand-on-dark);margin:16px 48px 34px;border-radius:18px;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;}
.footer .src{font-size:.76rem;color:rgba(239,239,239,.72);line-height:1.6;max-width:68ch;}

@media (max-width:768px){.grid-2,.people,.risk-grid{grid-template-columns:1fr;}main{padding:32px 24px 8px;}.masthead{padding:28px 24px;}.footer{margin:16px 24px 28px;}.side-nav{display:none;}}
@media (prefers-reduced-motion:reduce){*{transition:none !important;animation:none !important;}}
@media print{
  body{background:#fff;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .doc{border-radius:0;box-shadow:none;max-width:100%;} .side-nav{display:none;}
  .section,.person,.driver,.risk-item,.mit-item,.entry-card,.talk-track{break-inside:avoid;}
  .persona-panel{display:block !important;border-top:1px solid var(--border);padding-top:14px;margin-top:14px;}
  .persona-panel::before{content:attr(data-tab-label);display:block;font-family:var(--brand-font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-primary);margin-bottom:10px;}
  .persona-tabs{display:none;}
}
</style></head>
```

## `<body>` skeleton

```html
<body>
<nav class="side-nav" aria-label="Section navigation">
  <a href="#fit" class="active">Fit and timing</a>
  <a href="#drivers">What is driving them</a>
  <a href="#committee">Buying committee</a>
  <a href="#positioning">Positioning</a>
  <a href="#engagement">Engagement plan</a>
  <a href="#risks">What could go wrong</a>
</nav>
<div class="doc">
  <!-- 1. Masthead: workspace logo (topbar left) + target account chip (topbar right), eyebrow, conclusion H1, descriptor, datestamp -->
  <header class="masthead">...</header>
  <main>
    <!-- 2. Fit & timing: .k label + conclusion h2 + .lead-verdict + .deal-intel-grid (4 cards) + .grid-2 (Why it fits / Watch-outs) -->
    <section class="section" id="fit">...</section>
    <!-- 3. Drivers: .driver cards, each .pain + .tag(known|likely|explore) + .body -->
    <section class="section" id="drivers">...</section>
    <!-- 4. Committee: .people grid of .person cards (avatar, nm, tt, role-badge, disp, li link, .unconfirmed as needed) + .gap-line -->
    <section class="section" id="committee">...</section>
    <!-- 5. Positioning: .persona-tabs (role=tablist) + .persona-panel[data-tab-label] each with .pfield blocks (concerns/status quo/.lead-with/proof-fit).
         The <key>/<Persona Name> below are PLACEHOLDERS — choose the ≤3 personas per account (see account-plan-template.md §5); do NOT default to a fixed eng/ciso/grc set. -->
    <section class="section" id="positioning">...</section>
    <!-- 6. Engagement: .entry-card + .talk-track sample emails + .seq numbered steps + seed/CRM note -->
    <section class="section" id="engagement">...</section>
    <!-- 7. Risks: .risk-grid of .risk-pair (.risk-item + .mit-item) -->
    <section class="section" id="risks">...</section>
  </main>
  <!-- 8. Footer: workspace logo + .src provenance line -->
  <footer class="footer">...</footer>
</div>
<script>
function selectPersona(id){
  document.querySelectorAll('.persona-panel').forEach(function(p){p.classList.toggle('active',p.id==='panel-'+id);});
  document.querySelectorAll('.persona-tabs button').forEach(function(t){t.setAttribute('aria-selected',t.id==='tab-'+id?'true':'false');});
}
document.querySelectorAll('.persona-tabs button').forEach(function(btn){
  btn.addEventListener('keydown',function(e){
    var tabs=[].slice.call(document.querySelectorAll('.persona-tabs button')),i=tabs.indexOf(e.target);
    if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();
      var n=e.key==='ArrowRight'?(i+1)%tabs.length:(i-1+tabs.length)%tabs.length;tabs[n].focus();tabs[n].click();}
  });
});
(function(){var links=document.querySelectorAll('.side-nav a'),map={};links.forEach(function(l){map[l.getAttribute('href').slice(1)]=l;});
  var obs=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){links.forEach(function(l){l.classList.remove('active');});if(map[en.target.id])map[en.target.id].classList.add('active');}});},{rootMargin:'-40% 0px -55% 0px'});
  document.querySelectorAll('main section[id]').forEach(function(s){obs.observe(s);});})();
</script>
</body></html>
```

**Persona panel wiring:** each tab is `<button role="tab" id="tab-<key>" aria-controls="panel-<key>" aria-selected=... onclick="selectPersona('<key>')">`; each panel is `<div class="persona-panel[ active]" id="panel-<key>" role="tabpanel" data-tab-label="<Persona Name>">`. First tab/panel starts `active` / `aria-selected="true"`. All panels print (the `data-tab-label` shows as the printed heading).
