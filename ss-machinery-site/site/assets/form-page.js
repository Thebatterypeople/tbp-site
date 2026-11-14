/* S&S Machinery enquiry forms — Web3Forms relay straight to the sales inbox. */
var ACCESS_KEY = "c2f3b5dd-6dbf-4193-a489-e740ec898212";
var MACHINES = ['HM 370T mini loader','HM 380T mini loader','HM 750T mini loader','HM 1000T mini loader','HM 1500S skid steer','HME 30T excavator','Not sure - help me choose'];
var FORMS = {
  hire: { subject: 'Hire enquiry', submit: 'Send hire enquiry', fields: [
    { n: 'name', l: 'Full name', t: 'text', req: 1 },
    { n: 'email', l: 'Email', t: 'email', req: 1 },
    { n: 'phone', l: 'Phone', t: 'tel', req: 1 },
    { n: 'machine', l: 'Machine', t: 'select', req: 1 },
    { n: 'delivery_suburb', l: 'Delivery suburb', t: 'text', req: 1, ph: 'Or "pick up from Hallam"', wide: 1 },
    { n: 'start_date', l: 'Start date', t: 'date', req: 1 },
    { n: 'end_date', l: 'End date', t: 'date' },
    { n: 'notes', l: 'Attachments or notes', t: 'textarea', ph: 'Attachments needed, site access, anything we should know', wide: 1 }
  ]},
  contact: { subject: 'Website enquiry', submit: 'Send enquiry', fields: [
    { n: 'name', l: 'Full name', t: 'text', req: 1 },
    { n: 'email', l: 'Email', t: 'email', req: 1 },
    { n: 'phone', l: 'Phone', t: 'tel', req: 1 },
    { n: 'machine', l: 'Machine interest', t: 'select' },
    { n: 'message', l: 'Message', t: 'textarea', req: 1, wide: 1 }
  ]}
};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
export function mountForm(root, kind, opts){
  opts = opts || {}; var def = FORMS[kind]; if (!def) return;
  var today = new Date().toISOString().slice(0,10);
  var h = '<form class="f-grid" novalidate>';
  def.fields.forEach(function(f){
    var id = 'f_' + f.n, ctl;
    if (f.t === 'textarea') ctl = '<textarea id="'+id+'" name="'+f.n+'" placeholder="'+esc(f.ph)+'"></textarea>';
    else if (f.t === 'select') ctl = '<select id="'+id+'" name="'+f.n+'"><option value="">Select…</option>' + MACHINES.map(function(m){return '<option'+(opts.preselect && m.indexOf(opts.preselect)===0 ? ' selected' : '')+'>'+esc(m)+'</option>'}).join('') + '</select>';
    else ctl = '<input id="'+id+'" name="'+f.n+'" type="'+f.t+'" placeholder="'+esc(f.ph)+'"'+(f.t==='date'?' min="'+today+'"':'')+(f.t==='tel'?' autocomplete="tel"':'')+(f.t==='email'?' autocomplete="email"':'')+(f.n==='name'?' autocomplete="name"':'')+'>';
    h += '<div class="f-field'+(f.wide?' wide':'')+'" data-f="'+f.n+'"><label for="'+id+'">'+esc(f.l)+(f.req?' *':'')+'</label>'+ctl+'<p class="f-err" data-err hidden></p></div>';
  });
  h += '<input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none">';
  h += '<div class="f-actions"><button class="btn red" type="submit">'+esc(def.submit)+'</button><span class="f-note">'+esc(opts.note||'We reply within one business day. Urgent? Call 0466 892 400.')+'</span></div>';
  h += '<p class="f-err" data-formerr hidden style="grid-column:1/-1"></p></form>';
  root.innerHTML = h;
  var formEl = root.querySelector('form'), btn = formEl.querySelector('button[type=submit]'), ferr = formEl.querySelector('[data-formerr]');
  function setErr(n, msg){ var w = formEl.querySelector('[data-f="'+n+'"]'); if(!w) return; var p = w.querySelector('[data-err]'), c = w.querySelector('[name]'); p.hidden = !msg; p.textContent = msg||''; c.setAttribute('aria-invalid', msg?'true':'false'); }
  function validate(){
    var ok = true, first = null;
    def.fields.forEach(function(f){
      var c = formEl.elements[f.n], v = (c.value||'').trim(), msg = '';
      if (f.req && !v) msg = 'Required';
      else if (v && f.t === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'Enter a valid email address';
      else if (v && f.t === 'tel' && v.replace(/\D/g,'').length < 8) msg = 'Enter a valid phone number';
      setErr(f.n, msg); if (msg) { ok = false; first = first || c; }
    });
    if (kind === 'hire') { var s = formEl.elements.start_date.value, e = formEl.elements.end_date.value; if (s && e && e < s) { setErr('end_date','End date is before the start date'); ok = false; } }
    if (first) first.focus();
    return ok;
  }
  formEl.addEventListener('focusout', function(ev){ if (ev.target.name) validate(); });
  formEl.addEventListener('submit', async function(ev){
    ev.preventDefault(); ferr.hidden = true;
    if (!validate()) return;
    var fd = new FormData(formEl);
    var machine = fd.get('machine') || '';
    var payload = {
      access_key: ACCESS_KEY,
      subject: 'S&S ' + def.subject + (machine ? ' — ' + machine : '') + ' from ' + fd.get('name'),
      from_name: 'S&S Machinery website',
      replyto: fd.get('email'),
      botcheck: fd.get('botcheck') ? 'x' : '',
      'Enquiry type': def.subject,
      'Page': location.href
    };
    def.fields.forEach(function(f){ payload[f.l] = fd.get(f.n) || ''; });
    btn.disabled = true; btn.textContent = 'Sending…';
    try {
      var r = await fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) });
      var j = await r.json();
      if (!r.ok || !j.success) throw new Error(j.message || 'Could not send');
      root.innerHTML = '<div class="f-done"><b>Thanks — enquiry sent</b><p>We will be in touch within one business day. Need it sooner? Call <a href="tel:+61466892400">0466 892 400</a>.</p></div>';
    } catch (e) {
      ferr.hidden = false; ferr.textContent = 'Sorry, that did not send. Please call 0466 892 400 or email sales@sandsmachinery.com.au.';
      btn.disabled = false; btn.textContent = def.submit;
    }
  });
}
