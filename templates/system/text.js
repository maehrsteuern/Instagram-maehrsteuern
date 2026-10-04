// Shared helpers for all templates.
// fmt(s): *word* turns accent green, \n breaks the line, & and < are escaped.
window.fmt = s => String(s ?? '')
  .replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/\*(.+?)\*/g,'<span class="a">$1</span>')
  .replace(/\n/g,'<br>');
window.$ = id => document.getElementById(id);
// fitAll(): shrink headings until no word overflows the edge.
// Then shrink any element marked .fit (via CSS zoom) until its content fits its height.
window.fitAll = () => {
  document.querySelectorAll('h1,h2').forEach(el => {
    let s = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > el.clientWidth + 1 && s > 40) el.style.fontSize = (s -= 4) + 'px';
  });
  document.querySelectorAll('.fit').forEach(box => {
    const inner = box.firstElementChild; if (!inner) return;
    let z = 1;
    while (inner.getBoundingClientRect().height > box.clientHeight + 1 && z > 0.72) inner.style.zoom = (z -= 0.02);
    if (z < 1) console.warn('fit: content zoomed to', z.toFixed(2));
  });
};
