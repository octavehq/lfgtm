/* Inline after the deck DOM. Use data-editable on text-only leaves. */
(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const stage = document.getElementById('deckStage');
  if (!slides.length || !stage) throw new Error('Deck requires slides and deckStage');
  let current = 0, editing = false, touch = null;
  const mobile = () => matchMedia('(max-width: 720px)').matches;
  const controls = document.getElementById('deckControls');
  if (!controls) throw new Error('Deck requires deckControls');
  controls.replaceChildren();
  const prev = document.createElement('button'), next = document.createElement('button'), count = document.createElement('span');
  prev.textContent = 'Previous'; next.textContent = 'Next'; count.setAttribute('aria-live', 'polite');
  controls.append(prev, count, next);
  function show(i) {
    current = Math.max(0, Math.min(i, slides.length - 1));
    slides.forEach((s, j) => {
      s.classList.toggle('active', j === current); s.classList.toggle('visible', j === current || mobile());
      s.setAttribute('aria-hidden', String(j !== current && !mobile()));
      s.inert = !mobile() && j !== current;
    });
    count.textContent = `${current + 1} / ${slides.length}`;
    prev.disabled = current === 0; next.disabled = current === slides.length - 1;
  }
  function fit() {
    if (mobile()) stage.style.transform = 'none';
    else {
      const w = Number(stage.dataset.width || 1920), h = Number(stage.dataset.height || 1080);
      const scale = Math.min(innerWidth / w, innerHeight / h);
      stage.style.transformOrigin = '0 0';
      stage.style.transform = `translate(${(innerWidth-w*scale)/2}px,${(innerHeight-h*scale)/2}px) scale(${scale})`;
    }
    show(current);
  }
  prev.addEventListener('click', () => show(current - 1)); next.addEventListener('click', () => show(current + 1));
  addEventListener('resize', fit);
  const leaves = [...document.querySelectorAll('[data-editable]')];
  const version = document.documentElement.dataset.contentVersion;
  const key = version ? `octave-deck:${location.pathname}:${version}` : null;
  try {
    const saved = key && JSON.parse(localStorage.getItem(key));
    if (saved?.length === leaves.length) leaves.forEach((e, i) => { if (!e.children.length && typeof saved[i] === 'string') e.textContent = saved[i]; });
  } catch (_) { /* editing remains usable when storage is unavailable */ }
  leaves.forEach(e => e.addEventListener('input', () => {
    try { if (key) localStorage.setItem(key, JSON.stringify(leaves.map(x => x.textContent))); } catch (_) {}
  }));
  const edit = document.getElementById('editToggle');
  function toggleEdit() {
    if (!edit) return;
    editing = !editing;
    leaves.filter(e => !e.children.length).forEach(e => e.contentEditable = String(editing));
    edit?.setAttribute('aria-pressed', String(editing));
  }
  edit?.addEventListener('click', toggleEdit);
  edit?.classList.add('show');
  document.addEventListener('keydown', e => {
    if (e.target.closest('input,textarea,select,button,a,[contenteditable=true]')) return;
    if (e.key.toLowerCase() === 'e') { toggleEdit(); return; }
    if (mobile()) return;
    const routes = {ArrowRight: current+1, ' ':current+1, PageDown:current+1, ArrowLeft:current-1, PageUp:current-1, Home:0, End:slides.length-1};
    if (e.key in routes) { e.preventDefault(); show(routes[e.key]); }
  });
  stage.addEventListener('touchstart', e => { touch = e.touches.length === 1 ? [e.touches[0].clientX,e.touches[0].clientY] : null; }, {passive:true});
  stage.addEventListener('touchend', e => {
    if (!touch || editing || mobile() || e.target.closest('a,button,input,textarea')) return;
    const dx=e.changedTouches[0].clientX-touch[0], dy=e.changedTouches[0].clientY-touch[1]; touch=null;
    if (Math.abs(dx)>60 && Math.abs(dx)>Math.abs(dy)*1.5) show(current+(dx<0?1:-1));
  }, {passive:true});
  document.querySelector('[data-export-html]')?.addEventListener('click', () => {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('[contenteditable]').forEach(e => e.removeAttribute('contenteditable'));
    clone.querySelectorAll('.edit-hotzone,#editToggle,[data-export-html]').forEach(e => e.remove());
    const blob = new Blob(['<!DOCTYPE html>\n'+clone.outerHTML],{type:'text/html'});
    const url=URL.createObjectURL(blob), a=document.createElement('a'); a.href=url; a.download='presentation.html'; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  fit();
})();
