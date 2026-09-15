/* Inline after the DOM; content is visible unless enhancement starts successfully. */
(() => {
  const nodes=[...document.querySelectorAll('.animate-in')];
  const revealAll=()=>nodes.forEach(n=>n.classList.remove('reveal-pending'));
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  let observer;
  try {
    observer=new IntersectionObserver(entries=>{
      try { entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('reveal-pending');observer.unobserve(e.target);}}); }
      catch (_) { revealAll(); observer.disconnect(); }
    });
    nodes.forEach(n=>{if(n.getBoundingClientRect().top>innerHeight){observer.observe(n);n.classList.add('reveal-pending');}});
    addEventListener('beforeprint', revealAll);
    // A missed callback may delay decoration, never conceal content indefinitely.
    setTimeout(revealAll, 4000);
  } catch (_) { revealAll(); observer?.disconnect(); }
})();
