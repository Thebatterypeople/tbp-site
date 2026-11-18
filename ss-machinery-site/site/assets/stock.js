/* S&S Machinery: live stock list, read from the MDMS stock feed copy at window.SS_STOCK.raw */
(function () {
  var C = window.SS_STOCK, grid = document.getElementById('stock-grid'), note = document.getElementById('stock-note');
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-AU'); }
  function key(model) { return String(model || '').replace(/[^a-z0-9]/gi, '').toUpperCase(); }
  function fail() {
    note.innerHTML = 'The live stock list is not available right now. Call <a href="tel:' + C.tel + '">' + esc(C.phone) +
      '</a> or see <a href="machines.html">the full range</a>.';
  }

  var lbx = document.getElementById('lbx'), lImg = lbx.querySelector('img'), lCap = lbx.querySelector('.c'), set = [], at = 0;
  function show(i) { at = (i + set.length) % set.length; lImg.src = set[at]; lCap.textContent = (at + 1) + ' / ' + set.length; }
  function open(list, i) { set = list; show(i); lbx.classList.add('on'); }
  function close() { lbx.classList.remove('on'); lImg.removeAttribute('src'); }
  lbx.querySelector('.x').onclick = close;
  lbx.querySelector('.pv').onclick = function () { show(at - 1); };
  lbx.querySelector('.nx').onclick = function () { show(at + 1); };
  lbx.addEventListener('click', function (e) { if (e.target === lbx) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lbx.classList.contains('on')) return;
    if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(at - 1); else if (e.key === 'ArrowRight') show(at + 1);
  });

  fetch(C.raw + 'stock.json', {cache: 'no-cache'}).then(function (r) {
    if (!r.ok) throw new Error(r.status); return r.json();
  }).then(function (data) {
    var units = (data.units || []).slice();
    if (!units.length) { note.innerHTML = 'Our stock list is being updated. Call <a href="tel:' + C.tel + '">' + esc(C.phone) + '</a> for what is in the yard today.'; return; }
    note.textContent = units.length + (units.length === 1 ? ' machine' : ' machines') + ' listed, in our yard at Hallam.';
    grid.innerHTML = units.map(function (u, idx) {
      var name = [u.make === 'S&S Machinery' ? '' : u.make, u.model].join(' ').trim();
      var m = C.models[key(u.model)];
      var thumbs = (u.photos || []).map(function (p) { return C.raw + 'thumbs/' + p; });
      var img = thumbs[0] || (m ? m.cut : '');
      var meta = [];
      meta.push(u.status === 'reserved' ? '<span class="res">Reserved</span>' : '<span class="ok">Available</span>');
      if (u.condition) meta.push('<span>' + esc(u.condition.charAt(0).toUpperCase() + u.condition.slice(1)) + '</span>');
      if (u.year) meta.push('<span>' + esc(u.year) + '</span>');
      if (u.meter_type === 'hours' && u.hours) meta.push('<span>' + esc(u.hours) + ' hrs</span>');
      if (u.location_suburb) meta.push('<span>' + esc(u.location_suburb) + '</span>');
      meta.push('<span>Stock ' + esc(u.stock_number) + '</span>');
      var enq = 'contact.html?m=' + encodeURIComponent(name + ' (' + u.stock_number + ')');
      return '<div class="scard"><div class="img" data-i="' + idx + '">' +
        (img ? '<img src="' + esc(img) + '" alt="' + esc(name) + '" loading="lazy">' : '') +
        (thumbs.length > 1 ? '<span class="n">' + thumbs.length + ' photos</span>' : '') + '</div>' +
        '<div class="body"><div class="t">' + esc(u.category || '') + '</div><h3>' + esc(name) + '</h3>' +
        '<div class="p">' + (u.price ? money(u.price) + '<small>inc GST</small>' : 'Call for price') + '</div>' +
        '<div class="meta">' + meta.join('') + '</div>' +
        (u.description ? '<div class="d">' + esc(u.description) + '</div>' : '') +
        '<div class="btns"><a class="btn red" href="' + enq + '">Enquire</a><a class="btn dark" href="tel:' + C.tel + '">Call</a>' +
        (m ? '<a class="btn ghost-dark" href="machines/' + m.slug + '.html">360° &amp; specs</a>' : '') + '</div></div></div>';
    }).join('');
    grid.querySelectorAll('.img[data-i]').forEach(function (el) {
      var u = units[+el.getAttribute('data-i')], full = (u.photos || []).map(function (p) { return C.raw + 'photos/' + p; });
      if (full.length) el.onclick = function () { open(full, 0); }; else el.style.cursor = 'default';
    });
  }).catch(fail);
})();
