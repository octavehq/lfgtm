/* Visual kit runtime (shared/formats/visual-kit.md). Inline at the end of <body>.
   Everything here is enhancement: the page reads the same with this script
   removed. It adds html.vk-js (which arms motion), marks the screen in view
   with .is-in, keeps the chapter progress current, steps screens from the
   keyboard, counts stat numerals up to the value already in the DOM, and
   finishes the loader line once fonts settle. */
(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const screens = [...document.querySelectorAll('.vk-screen')];
  const printing = matchMedia('print').matches;
  if (printing) return;
  root.classList.add('vk-js');

  // loader: a sweep that ends when fonts are ready or 1.6 s pass, whichever first
  const loader = document.querySelector('.vk-loader');
  if (loader) {
    const done = () => loader.classList.add('is-done');
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(done, done);
    setTimeout(done, 1600);
  }

  // in-view marking: a screen is "in" once its top crosses 85% of the viewport.
  // Screens already in view at load are marked before the observer runs, so the
  // first screen never flashes.
  const markIn = (el) => el.classList.add('is-in');
  const inView = (el) => el.getBoundingClientRect().top < innerHeight * 0.85;
  const targets = screens.length ? screens : [...document.querySelectorAll('.vk-section, .vk-doc-hero')];
  targets.filter(inView).forEach(markIn);
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { markIn(e.target); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -15% 0px', threshold: 0.01 });
    targets.forEach((t) => { if (!t.classList.contains('is-in')) io.observe(t); });
  } else {
    targets.forEach(markIn);
  }
  // a missed callback delays decoration, never hides content
  setTimeout(() => targets.forEach(markIn), 5000);
  addEventListener('beforeprint', () => targets.forEach(markIn));

  // stat count-up: the DOM already holds the final text; animate towards it and
  // put the exact original string back at the end
  if (!reduced) {
    document.querySelectorAll('[data-vk-count]').forEach((el) => {
      const final = el.textContent;
      const target = parseFloat(el.dataset.vkCount);
      if (!isFinite(target)) return;
      const decimals = (String(el.dataset.vkCount).split('.')[1] || '').length;
      const prefix = final.match(/^[^\d-]*/)[0];
      const suffix = final.match(/[^\d.,]*$/)[0];
      const run = () => {
        const t0 = performance.now(), dur = 1100;
        const tick = (now) => {
          const p = Math.min(1, (now - t0) / dur), ease = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + (target * ease).toFixed(decimals) + suffix;
          if (p < 1) requestAnimationFrame(tick); else el.textContent = final;
        };
        requestAnimationFrame(tick);
      };
      const host = el.closest('.vk-screen, .vk-section, .vk-doc-hero');
      if (!host || host.classList.contains('is-in')) run();
      else new MutationObserver((m, o) => { if (host.classList.contains('is-in')) { o.disconnect(); run(); } })
        .observe(host, { attributes: true, attributeFilter: ['class'] });
    });
  }

  if (!screens.length) return;

  // chapter progress
  const pips = document.querySelector('.vk-pips');
  const current = document.querySelector('[data-vk-current]');
  const total = document.querySelector('[data-vk-total]');
  if (total) total.textContent = String(screens.length);
  if (pips && !pips.children.length) {
    screens.forEach((s, i) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + (s.id || (s.id = 'screen-' + (i + 1)));
      a.setAttribute('aria-label', 'Go to screen ' + (i + 1));
      li.appendChild(a); pips.appendChild(li);
    });
  }
  const pipItems = pips ? [...pips.children] : [];
  let active = -1;
  const indexInView = () => {
    const mid = innerHeight * 0.5;
    let best = 0, bestD = Infinity;
    screens.forEach((s, i) => {
      const r = s.getBoundingClientRect();
      const d = r.top <= mid && r.bottom > mid ? 0 : Math.min(Math.abs(r.top - mid), Math.abs(r.bottom - mid));
      if (d < bestD) { bestD = d; best = i; }
    });
    return best;
  };
  const setActive = (i) => {
    if (i === active) return;
    active = i;
    pipItems.forEach((p, k) => p.classList.toggle('is-on', k <= i));
    if (current) current.textContent = String(i + 1);
    const dark = screens[i].classList.contains('is-dark');
    document.body.classList.toggle('vk-on-dark', dark);
  };
  const moved = () => document.body.classList.add('vk-moved');
  setTimeout(moved, 9000);
  let raf = 0;
  const onScroll = () => { if (scrollY > 40) moved(); if (!raf) raf = requestAnimationFrame(() => { raf = 0; setActive(indexInView()); }); };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  setActive(indexInView());

  // keyboard stepping; scrolling and the pips still work on their own
  const go = (i) => {
    i = Math.max(0, Math.min(screens.length - 1, i));
    screens[i].scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
  };
  addEventListener('keydown', (e) => {
    moved();
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(input|textarea|select|button|summary|a)$/i.test(t.tagName))) return;
    const i = indexInView();
    const k = e.key;
    const down = k === 'ArrowDown' || k === 'PageDown' || (k === ' ' && !e.shiftKey);
    const up = k === 'ArrowUp' || k === 'PageUp' || (k === ' ' && e.shiftKey);
    // A screen taller than the viewport (zoom, short or narrow windows) scrolls
    // natively until its edge is in view, so no content is skipped.
    const r = screens[i].getBoundingClientRect();
    if (down && r.bottom > innerHeight + 2) return;
    if (up && r.top < -2) return;
    if (down || k === 'ArrowRight') go(i + 1);
    else if (up || k === 'ArrowLeft') go(i - 1);
    else if (k === 'Home') go(0);
    else if (k === 'End') go(screens.length - 1);
    else if (/^[1-9]$/.test(k)) go(Number(k) - 1);
    else return;
    e.preventDefault();
  });
})();
