/* Inline this file after the lesson DOM. Navigation indexes come from the DOM. */
(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  if (!slides.length) throw new Error('Lesson has no slides');
  const questions = [...document.querySelectorAll('[data-checkpoint]')];
  const answers = new Map();
  let current = 0;
  const content = slides.filter(s => s.dataset.type === 'content');
  const done = s => [...s.querySelectorAll('[data-checkpoint]')].every(q => answers.has(q));
  const canReach = i => slides.slice(0, i).filter(s => s.dataset.type === 'content').every(done);
  const dots = document.getElementById('dots');
  if (dots) content.forEach((s, n) => {
    const button = document.createElement('button');
    button.className = 'dot'; button.setAttribute('aria-label', `Topic ${n + 1}`);
    button.addEventListener('click', () => go(slides.indexOf(s))); dots.append(button);
  });
  function update() {
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === current); s.setAttribute('aria-hidden', String(i !== current));
      s.querySelectorAll('[data-next]').forEach(b => b.disabled = !canReach(i + 1));
      const qs = [...s.querySelectorAll('[data-checkpoint]')];
      const hint = s.querySelector('[data-hint]');
      if (hint) hint.textContent = qs.length ? `${qs.filter(q => answers.has(q)).length} of ${qs.length} answered` : '';
    });
    if (dots) [...dots.children].forEach((d, n) => {
      const i = slides.indexOf(content[n]); d.disabled = !canReach(i);
      d.classList.toggle('current', i === current); d.classList.toggle('done', done(content[n]));
    });
    const label = document.querySelector('.step-label');
    if (label) label.textContent = `${current + 1} / ${slides.length}`;
    document.querySelectorAll('.score-big').forEach(e => {
      e.textContent = questions.length ? `${[...answers.values()].filter(Boolean).length} / ${questions.length}` : 'No scored checks';
    });
    const logo = document.querySelector('.topbar .brand');
    const dark = ['cover', 'done'].includes(slides[current].dataset.type);
    if (logo?.dataset[dark ? 'onDark' : 'onLight']) logo.src = logo.dataset[dark ? 'onDark' : 'onLight'];
  }
  function go(i) {
    if (!Number.isInteger(i) || i < 0 || i >= slides.length || !canReach(i)) return false;
    current = i; update(); slides[i].querySelector('.slide-body')?.scrollTo(0, 0); return true;
  }
  function restart() {
    answers.clear();
    questions.forEach(q => {
      q.querySelectorAll('.cp-opt').forEach(b => { b.disabled = false; b.classList.remove('correct', 'wrong'); });
      q.querySelector('.cp-explain')?.classList.remove('show');
    });
    current = 0; update();
  }
  questions.forEach(q => q.querySelectorAll('.cp-opt').forEach(b => b.addEventListener('click', () => {
    if (answers.has(q)) return;
    const correct = b.dataset.answer === 'true'; answers.set(q, correct);
    b.classList.add(correct ? 'correct' : 'wrong');
    q.querySelectorAll('.cp-opt').forEach(o => o.disabled = true);
    q.querySelector('.cp-explain')?.classList.add('show'); update();
  })));
  document.querySelectorAll('[data-tabset]').forEach((set, n) => {
    const tabs = [...set.querySelectorAll(':scope > .tabs > .tab')];
    const panels = [...set.querySelectorAll(':scope > .tpanel')];
    if (tabs.length !== panels.length) throw new Error('Tab and panel counts differ');
    set.querySelector(':scope > .tabs')?.setAttribute('role', 'tablist');
    function select(i, focus = false) {
      tabs.forEach((t, j) => { t.setAttribute('aria-selected', String(i === j)); t.tabIndex = i === j ? 0 : -1; });
      panels.forEach((p, j) => p.classList.toggle('active', i === j));
      if (focus) tabs[i].focus();
    }
    tabs.forEach((t, i) => {
      t.id = `lesson-tab-${n}-${i}`; t.setAttribute('role', 'tab');
      panels[i].id = `lesson-panel-${n}-${i}`; panels[i].setAttribute('role', 'tabpanel');
      panels[i].setAttribute('aria-labelledby', t.id); t.setAttribute('aria-controls', panels[i].id);
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
        e.preventDefault(); e.stopPropagation();
        select(e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length, true);
      });
    }); select(0);
  });
  document.querySelectorAll('[data-next],[data-prev],[data-start],[data-restart],[data-go]').forEach(b => {
    b.removeAttribute('onclick');
    b.addEventListener('click', () => {
      if (b.hasAttribute('data-restart')) restart();
      else if (b.hasAttribute('data-go')) { const s = document.getElementById(b.dataset.go); go(slides.indexOf(s)); }
      else go(b.hasAttribute('data-start') ? 1 : current + (b.hasAttribute('data-prev') ? -1 : 1));
    });
  });
  document.addEventListener('keydown', e => {
    if (e.target.closest('input,textarea,select,button,a,[contenteditable=true],[role=tab]')) return;
    if (['ArrowRight', 'ArrowLeft'].includes(e.key)) { e.preventDefault(); go(current + (e.key === 'ArrowRight' ? 1 : -1)); }
  });
  window.go = go; window.restart = restart; update();
})();
