// Gemeinsame Helfer: *Wort* wird grün, Zeilenumbruch mit \n
window.fmt = s => String(s ?? '')
  .replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/\*(.+?)\*/g,'<span class="a">$1</span>')
  .replace(/\n/g,'<br>');
window.$ = id => document.getElementById(id);
// Überschriften verkleinern, bis kein Wort mehr über den Rand ragt
window.fitAll = () => document.querySelectorAll('h1,h2').forEach(el => {
  let s = parseFloat(getComputedStyle(el).fontSize);
  while (el.scrollWidth > el.clientWidth + 1 && s > 40) el.style.fontSize = (s -= 4) + 'px';
});
