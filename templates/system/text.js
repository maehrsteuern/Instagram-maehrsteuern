// Shared helpers: *word* turns green, \n breaks the line
window.fmt = s => String(s ?? '')
  .replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/\*(.+?)\*/g,'<span class="a">$1</span>')
  .replace(/\n/g,'<br>');
window.$ = id => document.getElementById(id);
// Shrink headings until no word overflows the edge
window.fitAll = () => document.querySelectorAll('h1,h2').forEach(el => {
  let s = parseFloat(getComputedStyle(el).fontSize);
  while (el.scrollWidth > el.clientWidth + 1 && s > 40) el.style.fontSize = (s -= 4) + 'px';
});
