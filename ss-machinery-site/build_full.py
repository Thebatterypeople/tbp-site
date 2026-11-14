"""Full S&S Machinery site in the new design (static, Wix-hosted). Root pages + machines/."""
import json, os, html
from machines_data import MACHINES, BUSINESS as B, price_str
from build_site import MEDIA, MAN, OUT, SITE, LOGO_W, e, CSS as BASE_CSS, JS
import build_site2  # regenerates data.js/render.js/machine shells (nav fixed below)

FORMS = {'hire': '9dc6077e-bd62-41d0-be82-8f3778b31238', 'contact': '20a665aa-7608-438e-ada9-5013825945a5'}
HIRE_RATES = {  # ex GST, from the current site
    'HM380T': ('$220', '$600', '$950'), 'HM1500S': ('$320', '$850', '$1,350'),
    'HM370T': ('POA', 'POA', 'POA'), 'HM750T': ('POA', 'POA', 'POA'), 'HM1000T': ('POA', 'POA', 'POA'), 'HME30T': ('POA', 'POA', 'POA'),
}
HOURS = [('Monday to Friday', '7:00 am – 5:00 pm'), ('Saturday', '8:00 am – 12:00 pm'), ('Sunday', 'Closed')]
NAV = [('Home', 'index.html'), ('Machines', 'machines.html'), ('Hire', 'hire.html'), ('Attachments', 'attachments.html'),
       ('Service', 'service.html'), ('About', 'about.html'), ('Contact', 'contact.html'), ('Hire terms', 'hire-terms.html')]

EXTRA_CSS = r"""
/* home */
.home-hero{background:radial-gradient(ellipse at 70% 60%,#2c2c2c 0%,#131313 65%);color:#fff;padding:56px 0 0;overflow:hidden}
.home-hero .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:end}
@media(max-width:900px){.home-hero .grid{grid-template-columns:1fr}}
.home-hero h1{font-size:clamp(44px,6.2vw,86px);font-weight:800;color:var(--red);margin:0 0 18px;line-height:.95}
.home-hero p{font-size:19px;color:#d6d6d6;max-width:56ch;margin:0 0 26px}
.home-hero .pic img{width:100%;max-width:640px;display:block;margin:0 auto;filter:drop-shadow(0 24px 28px rgba(0,0,0,.6))}
.home-hero .pad{padding-bottom:56px}
.stats{background:var(--red);color:#fff}
.stats .wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0}
.stats div{padding:22px 20px;border-left:1px solid rgba(255,255,255,.25)}
.stats div:first-child{border-left:0}
.stats b{display:block;font-family:"Barlow Condensed";font-size:30px;font-weight:800;line-height:1}
.stats span{font-size:14px;color:#ffe3e4;text-transform:uppercase;letter-spacing:.08em;font-family:"Barlow Condensed";font-weight:600}
.split{display:grid;grid-template-columns:1fr 1fr;gap:22px}
@media(max-width:860px){.split{grid-template-columns:1fr}}
.panel{border-radius:8px;padding:34px;color:#fff;background:#141414;border:1px solid #242424;display:flex;flex-direction:column;gap:12px}
.panel h3{font-size:40px;font-weight:800;margin:0;color:#fff}
.panel p{color:#cfcfcf;margin:0;font-size:17px}
.panel .btn{align-self:flex-start;margin-top:8px}
.panel.light{background:#fff;color:var(--ink);border-color:var(--line)}.panel.light h3{color:var(--ink)}.panel.light p{color:#444}
/* generic page band */
.pband{background:#111;color:#fff;padding:48px 0 44px}
.pband h1{font-size:clamp(44px,6.5vw,88px);color:var(--red);margin:0 0 8px}
.pband p{font-size:19px;color:#cfcfcf;max-width:70ch;margin:0}
/* rate table */
table.rates{width:100%;border-collapse:collapse;font-size:17px;background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden}
table.rates th{font-family:"Barlow Condensed";text-transform:uppercase;letter-spacing:.08em;font-size:14px;color:#fff;background:#111;padding:14px 16px;text-align:left}
table.rates td{padding:14px 16px;border-top:1px solid var(--line);vertical-align:middle}
table.rates td.m{font-family:"Barlow Condensed";font-weight:800;font-size:24px}
table.rates td.m small{display:block;font-family:Barlow;font-weight:400;font-size:13px;color:var(--muted);letter-spacing:0}
table.rates td.r{font-family:"Barlow Condensed";font-weight:700;font-size:22px;white-space:nowrap}
table.rates td.r.poa{color:var(--muted);font-weight:600;font-size:16px}
table.rates a.l{font-size:14px;color:var(--red);font-weight:600}
@media(max-width:700px){table.rates thead{display:none}table.rates td{display:block;border-top:0;padding:6px 16px}table.rates tr{display:block;border-top:1px solid var(--line);padding:10px 0}table.rates td.r::before{content:attr(data-l) " ";font-family:Barlow;font-weight:400;font-size:13px;color:var(--muted)}}
/* attachments */
.agrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
.acard{background:#fff;border:1px solid var(--line);border-radius:6px;padding:22px}
.acard h3{font-size:30px;margin:0 0 6px}
.acard .p{font-family:"Barlow Condensed";font-weight:800;font-size:24px;color:var(--red)}
.acard .p small{font-family:Barlow;font-weight:400;font-size:13px;color:var(--muted);margin-left:6px}
.acard p{color:#444;font-size:15px;margin:8px 0 0}
/* terms */
.terms h3{font-size:26px;margin:26px 0 8px}
.terms p{max-width:78ch;font-size:17px;color:#333}
/* forms */
.formcard{background:#fff;border:1px solid var(--line);border-radius:8px;padding:28px}
.formcard.dark{background:#141414;border-color:#2a2a2a;color:#fff}
.f-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 18px}
@media(max-width:700px){.f-grid{grid-template-columns:1fr}}
.f-field.wide{grid-column:1/-1}
.f-field label{display:block;font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.08em;font-size:13px;color:#555;margin-bottom:6px}
.formcard.dark .f-field label{color:#bbb}
.f-field input,.f-field select,.f-field textarea{width:100%;font:inherit;font-size:16px;padding:12px 12px;border:1px solid #cfcfcf;border-radius:4px;background:#fff;color:#111}
.formcard.dark .f-field input,.formcard.dark .f-field select,.formcard.dark .f-field textarea{background:#1e1e1e;border-color:#3a3a3a;color:#fff}
.f-field textarea{min-height:110px;resize:vertical}
.f-field input:focus,.f-field select:focus,.f-field textarea:focus{outline:2px solid var(--red);outline-offset:1px;border-color:var(--red)}
.f-field [aria-invalid="true"]{border-color:var(--red)}
.f-err{color:var(--red);font-size:13px;margin:6px 0 0}
.f-actions{grid-column:1/-1;display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:6px}
.f-actions .btn[disabled]{opacity:.6;cursor:progress}
.f-note{font-size:13px;color:var(--muted)}
.formcard.dark .f-note{color:#aaa}
.f-done{font-size:18px;padding:18px 0}
.f-done b{display:block;font-family:"Barlow Condensed";font-size:30px;color:var(--red);margin-bottom:6px}
.contact-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:34px;align-items:start}
@media(max-width:900px){.contact-grid{grid-template-columns:1fr}}
.kv{display:grid;gap:14px}
.kv .k{font-family:"Barlow Condensed";font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#888}
.kv .v{font-size:18px;font-weight:600}
.kv .v a{text-decoration:none}
.btn.dark{background:#111;color:#fff;border-color:#111}
.card:not(.dark) .pr .k{color:#777}.card:not(.dark) .pr .s{color:#777}
.card.dark .kv .k{color:#999}
"""

FORM_JS = r"""
import { createFormStore, FORM_ERROR } from "/js/wix/form-store.js";
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function inputType(c){return ({email:'email',url:'url',phone:'tel',password:'password',number:'number',date:'date',time:'time',datetime:'datetime-local'})[c]||'text'}
export function mountForm(root, formId, opts){
  opts=opts||{};
  var store=createFormStore({formId:formId}), built=false, formEl=null;
  function control(f, v){
    var id='f_'+f.target, req=f.required?' required':'', ro=f.readOnly?' disabled':'';
    if(f.control==='textarea') return '<textarea id="'+id+'" name="'+f.target+'" placeholder="'+esc(f.placeholder)+'"'+ro+'>'+esc(v||'')+'</textarea>';
    if(f.control==='select'){var o='<option value="">Select…</option>';(f.choices||[]).forEach(function(c){o+='<option value="'+esc(c.value)+'"'+(v===c.value?' selected':'')+'>'+esc(c.label)+'</option>'});return '<select id="'+id+'" name="'+f.target+'"'+ro+'>'+o+'</select>'}
    if(f.control==='checkbox') return '<input id="'+id+'" name="'+f.target+'" type="checkbox"'+(v===true?' checked':'')+'>';
    var extra='';if(f.control==='date'&&f.validation&&f.validation.minDate)extra+=' min="'+esc(f.validation.minDate)+'"';
    return '<input id="'+id+'" name="'+f.target+'" type="'+inputType(f.control)+'" value="'+esc(v||'')+'" placeholder="'+esc(f.placeholder)+'"'+extra+ro+'>';
  }
  function build(s){
    var h='<form class="f-grid" novalidate>';
    s.form.fields.forEach(function(f){
      if(f.hidden)return;
      var wide=f.control==='textarea'?' wide':'';
      if(opts.wide&&opts.wide.test(f.label))wide=' wide';
      h+='<div class="f-field'+wide+'" data-f="'+f.target+'"><label for="f_'+f.target+'">'+esc(f.label)+(f.required?' *':'')+'</label>'+control(f,s.values[f.target])+'<p class="f-err" data-err hidden></p></div>';
    });
    h+='<div class="f-actions"><button class="btn red" type="submit">'+esc(s.form.submitText||opts.submitText||'Send')+'</button><span class="f-note">'+esc(opts.note||'We reply within one business day. Urgent? Call 0466 892 400.')+'</span></div>';
    h+='<p class="f-err" data-formerr hidden style="grid-column:1/-1"></p></form>';
    root.innerHTML=h; formEl=root.querySelector('form'); built=true;
    if(opts.preselect){var sel=formEl.querySelector('select');if(sel){for(var i=0;i<sel.options.length;i++){if(sel.options[i].value.indexOf(opts.preselect)===0){sel.value=sel.options[i].value;store.setValue(sel.name,sel.value);break}}}}
    formEl.addEventListener('input',function(ev){var t=ev.target;if(!t.name)return;store.setValue(t.name,t.type==='checkbox'?t.checked:t.value)});
    formEl.addEventListener('change',function(ev){var t=ev.target;if(!t.name)return;store.setValue(t.name,t.type==='checkbox'?t.checked:t.value)});
    formEl.addEventListener('focusout',function(ev){if(ev.target.name)store.validate(ev.target.name)});
    formEl.addEventListener('submit',function(ev){var st=store.getState();if(st.form&&st.step<st.form.steps.length-1)store.next(ev);else store.submit(ev)});
  }
  function render(s){
    if(!s.form){root.innerHTML=s.errors[FORM_ERROR]?'<p class="f-err">'+esc(s.errors[FORM_ERROR])+'</p>':'<p class="f-note">Loading form…</p>';built=false;return}
    if(s.closed){root.innerHTML='<p class="f-done">'+esc(s.form.disabledMessage||'This form is not taking enquiries right now. Call 0466 892 400.')+'</p>';built=false;return}
    if(s.outcome){if(s.outcome.url){if(s.outcome.newTab)window.open(s.outcome.url);else location.href=s.outcome.url;return}
      root.innerHTML='<div class="f-done"><b>Thanks — enquiry sent</b>'+(s.outcome.message||'We will be in touch within one business day.').split('\n').map(function(l){return '<p>'+esc(l)+'</p>'}).join('')+'</div>';built=false;return}
    if(!built)build(s);
    s.form.fields.forEach(function(f){var w=formEl.querySelector('[data-f="'+f.target+'"]');if(!w)return;var err=s.errors[f.target],p=w.querySelector('[data-err]'),c=w.querySelector('[name]');p.hidden=!err;p.textContent=err||'';if(c)c.setAttribute('aria-invalid',err?'true':'false')});
    var fe=formEl.querySelector('[data-formerr]');fe.hidden=!s.errors[FORM_ERROR];fe.textContent=s.errors[FORM_ERROR]||'';
    var b=formEl.querySelector('button[type=submit]');b.disabled=!!s.loading;b.textContent=s.loading?'Sending…':(s.form.submitText||opts.submitText||'Send');
  }
  store.subscribe(render);render(store.getState());store.start();
  return store;
}
"""

HEAD = """<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}"><meta property="og:type" content="website">
<link rel="icon" href="{shield}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
</head><body{battr}>"""


def nav(root, on):
    links = ''.join(f'<a href="{root}{h}"{" class=on" if h == on else ""}>{t}</a>' for t, h in NAV)
    return (f'<div class="nav"><div class="wrap"><a href="{root}index.html"><img src="{LOGO_W}" alt="S&amp;S Machinery"></a>'
            f'<div class="links">{links}</div><a class="call" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a></div></div>')


def footer(root):
    return (f'<footer><div class="wrap"><img src="{LOGO_W}" alt="S&amp;S Machinery"><div>{e(B["legal"])} · {e(B["address"])}<br>'
            f'<span style="color:#888">Mon–Fri 7:00 am – 5:00 pm · Sat 8:00 am – 12:00 pm</span></div>'
            f'<div><a href="tel:{B["phone_tel"]}">{B["phone"]}</a> · <a href="mailto:{B["email"]}">{B["email"]}</a> · <a href="{root}hire-terms.html">Hire terms</a></div>'
            f'</div></footer>')


def page(fname, title, desc, body, on, og=None, battr='', scripts=''):
    h = HEAD.format(title=e(title), desc=e(desc), og=og or MEDIA['HM1500S/hero_tile.jpg'], shield=MEDIA['brand/shield-white.png'], root='', battr=battr)
    h += nav('', on) + body + footer('') + scripts + '</body></html>'
    open(f'{OUT}/{fname}', 'w').write(h)


def cta(text, sub):
    return (f'<div class="cta"><div class="wrap"><h2>{text}</h2><p>{e(sub)}</p><div class="btns" style="justify-content:center">'
            f'<a class="btn white" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a><a class="btn ghost" href="hire.html">Book a hire</a><a class="btn ghost" href="contact.html">Send an enquiry</a></div></div></div>')


def machine_cards():
    cards = ''
    for m in MACHINES:
        cut = MEDIA[f'{m["key"]}/hero_cutout.webp']
        cards += (f'<a class="mcard" href="machines/{m["slug"]}.html"><div class="img"><img src="{cut}" alt="{e(m["name"])}" loading="lazy"></div>'
                  f'<div class="body"><div class="t">{e(m["type"])}</div><h3>{e(m["name"])}</h3><div class="p">{price_str(m["price"])}<small>inc GST</small></div>'
                  f'<div class="d">{e(m["tagline"])}</div><div class="go">View machine, 360° &amp; 3D</div></div></a>')
    return f'<div class="mgrid">{cards}</div>'


def home():
    hero_cut = MEDIA['HM1500S/hero_cutout.webp']
    body = f'''<div class="home-hero"><div class="wrap"><div class="grid"><div class="pad">
<h1>Designed for Australian conditions. Built with parts you can trust.</h1>
<p>Mini loaders, a skid steer and a 2.8 tonne excavator to hire by the day or week, or to own outright. Delivered from Hallam and backed by our own workshop, a 5 year / 200 hour warranty and three free services on every machine sold.</p>
<div class="btns"><a class="btn red" href="machines.html">See the machines</a><a class="btn ghost" href="hire.html">Book a hire</a></div></div>
<div class="pic"><img src="{hero_cut}" alt="HM 1500S skid steer"></div></div></div>
<div class="stats"><div class="wrap"><div><b>6</b><span>machines in stock at Hallam</span></div><div><b>5 yr / 200 hr</b><span>warranty on every sale</span></div><div><b>3 free</b><span>services in our workshop</span></div><div><b>From $120</b><span>delivery across the south-east</span></div></div></div></div>
<section class="alt"><div class="wrap"><h2>The <i>range</i></h2>{machine_cards()}</div></section>
<section><div class="wrap"><h2>Hire it. <i>Own it.</i></h2><div class="split">
<div class="panel"><h3>Hire</h3><p>Day, weekend and weekly rates. Fuel full on pick-up, induction included, delivered to site or collect from Hallam. Attachments available on the same hire.</p><a class="btn red" href="hire.html">Hire rates &amp; booking</a></div>
<div class="panel light"><h3>Buy</h3><p>Brand new machines from $14,999 inc GST with the standard bucket, a 5 year / 200 hour warranty and the first three services free. Finance and trade pricing on request.</p><a class="btn dark" href="machines.html">Machines for sale</a></div>
</div></div></section>
<section class="alt"><div class="wrap"><div class="two"><div><h2>Family owned, <i>Hallam VIC</i></h2><p class="lead">Sayed and Sons Machinery is a family business at Factory 5, 65-67 Hallam South Road. We design our machines for Australian soil, heat and site conditions and build them with quality international components, so parts and servicing are handled locally rather than shipped from overseas.</p><ul class="ticks"><li>Briggs &amp; Stratton, Honda, Kubota and Yanmar power</li><li>Parts stocked and fitted in our Hallam workshop</li><li>Operator handover and induction with every machine</li><li>Open Monday to Friday 7–5, Saturday 8–12</li></ul></div>
<div class="card dark"><h2 style="font-size:30px;color:#fff">Talk to us</h2><div class="kv"><div><div class="k">Phone</div><div class="v"><a href="tel:{B["phone_tel"]}">{B["phone"]}</a></div></div><div><div class="k">Email</div><div class="v"><a href="mailto:{B["email"]}">{B["email"]}</a></div></div><div><div class="k">Yard</div><div class="v">{e(B["address"])}</div></div></div><div class="btns" style="margin-top:18px"><a class="btn red" href="contact.html">Send an enquiry</a></div></div></div></div></section>
{cta("Ready when you are", "Call us, book a hire online, or come and see the machines at Hallam.")}'''
    page('index.html', 'S&S Machinery — mini loaders, skid steers & excavators for hire and sale, Hallam VIC',
         'S&S Machinery, Hallam: HM mini loaders, the HM 1500S skid steer and HME 30T excavator for hire by the day or week, or to buy with a 5 year / 200 hour warranty and three free services. Delivery across Melbourne\'s south-east.', body, 'index.html')


def machines():
    body = f'''<div class="pband"><div class="wrap"><h1>The range</h1><p>Six machines, every one in stock at Hallam and available to hire by the day or week or to own outright. Every machine sold comes with a 5 year / 200 hour warranty and the first three services free. Open each machine for the 360° spin, the 3D model and full specifications.</p></div></div>
<section class="alt"><div class="wrap">{machine_cards()}</div></section>
{cta("Not sure which one?", "Tell us the job and we will match the machine.")}'''
    page('machines.html', 'Machines for sale & hire — mini loaders, skid steer, excavator | S&S Machinery Hallam',
         'S&S Machinery range: HM 370T, HM 380T, HM 750T and HM 1000T stand-on mini loaders, HM 1500S skid steer and HME 30T excavator. Buy or hire from Hallam, Victoria. 5 year / 200 hour warranty, first 3 services free.', body, 'machines.html')


def hire():
    rows = ''
    for m in MACHINES:
        d, w, wk = HIRE_RATES[m['key']]
        def cell(v, l):
            return f'<td class="r{" poa" if v == "POA" else ""}" data-l="{l}">{"On application" if v == "POA" else v}</td>'
        rows += f'<tr><td class="m">{e(m["name"])}<small>{e(m["type"])} · <a class="l" href="machines/{m["slug"]}.html">Specs &amp; 360°</a></small></td>{cell(d, "Day")}{cell(w, "Weekend")}{cell(wk, "Week")}</tr>'
    body = f'''<div class="pband"><div class="wrap"><h1>Hire fleet</h1><p>Industrial-grade machinery hire across Melbourne's south-east. Rates are ex GST and include the standard bucket, a full tank and an operator induction at handover. Weekend is Saturday pick-up to Monday morning return.</p></div></div>
<section class="alt"><div class="wrap"><table class="rates"><thead><tr><th>Machine</th><th>Day</th><th>Weekend</th><th>Week</th></tr></thead><tbody>{rows}</tbody></table>
<p class="fine">Attachments on hire: 4-in-1 bucket included; trencher $80 per day; post hole auger $60 per day. Longer hires, multi-machine jobs and trade accounts: call {B["phone"]}. A $500 bond (mini loaders) or $1,000 bond (skid steer and excavator) is pre-authorised at pick-up and a 12% damage waiver applies to every hire — see the <a href="hire-terms.html">hire terms</a>.</p>
<div class="pr" style="margin-top:22px"><div class="card"><div class="k" style="color:#888">Delivery within 25 km</div><div class="v" style="font-size:30px">$120 each way</div></div><div class="card"><div class="k" style="color:#888">25–50 km of Hallam</div><div class="v" style="font-size:30px">$180 each way</div></div><div class="card"><div class="k" style="color:#888">Pick up from Hallam</div><div class="v" style="font-size:30px">Free</div></div></div></div></section>
<section id="book"><div class="wrap"><h2>Book a <i>hire</i></h2><p class="lead">Tell us the machine, where it is going and the dates. We confirm availability and the rate within one business day; same-day hires by phone.</p>
<div class="formcard" style="margin-top:18px"><div id="hireform"></div></div></div></section>
{cta("Prefer to talk?", "Call the yard and we will sort it on the phone.")}'''
    scripts = f'<script type="module">import {{mountForm}} from "/assets/form-page.js";var p=new URLSearchParams(location.search).get("m");mountForm(document.getElementById("hireform"),"hire",{{preselect:p}});</script>'
    page('hire.html', 'Machinery hire rates — mini loaders, skid steer, excavator | S&S Machinery Hallam',
         'Hire the HM 380T mini loader from $220 a day or the HM 1500S skid steer from $320 a day (ex GST). Delivery across Melbourne\'s south-east from Hallam. Book online or call 0466 892 400.', body, 'hire.html', scripts=scripts)


def attachments():
    items = [('4-in-1 multi bucket', 'Included on hire', '+$1,500 to buy', 'Dig, doze, grab and level with one attachment. Fits every HM loader.'),
             ('Trencher', '$80 per day', 'Price on request', 'Clean narrow trenches for irrigation, cable and drainage. Fits the HM loaders.'),
             ('Post hole auger', '$60 per day', 'Price on request', 'Auger drive with bits for fencing and footings. Pictured on the HM 380T.'),
             ('Stump grinder', 'On application', 'Price on request', 'Grind stumps flush without bringing in a dedicated machine.'),
             ('General purpose bucket', 'Included', 'Included with every loader', 'The standard bucket supplied with each machine.'),
             ('Excavator buckets', 'On application', 'Price on request', 'Digging and trenching buckets for the HME 30T.')]
    cards = ''.join(f'<div class="acard"><h3>{e(n)}</h3><div class="p">{e(h)}<small>hire</small></div><div class="p" style="font-size:18px;color:#111">{e(b)}</div><p>{e(d)}</p></div>' for n, h, b, d in items)
    body = f'''<div class="pband"><div class="wrap"><h1>Attachments</h1><p>Quick-hitch attachments for the HM loaders and buckets for the HME 30T. Hire rates ex GST per day; purchase prices inc GST. Fitment and pricing for any attachment not listed on request.</p></div></div>
<section class="alt"><div class="wrap"><div class="agrid">{cards}</div></div></section>
{cta("Need a specific attachment?", "Tell us the job and the machine and we will quote it.")}'''
    page('attachments.html', 'Attachments — multi bucket, trencher, auger, stump grinder | S&S Machinery',
         'Attachments for S&S Machinery loaders and excavator: 4-in-1 multi bucket, trencher, post hole auger, stump grinder. Hire rates and purchase prices, Hallam VIC.', body, 'attachments.html')


def service():
    body = f'''<div class="pband"><div class="wrap"><h1>Workshop &amp; service</h1><p>Every machine we hire or sell is backed by our own workshop at Hallam, with parts on the shelf rather than on a ship.</p></div></div>
<section class="alt"><div class="wrap"><div class="two"><div><h2>What we <i>do</i></h2><ul class="ticks"><li>Scheduled servicing and maintenance for all S&amp;S machinery</li><li>Stocked parts and components for fast turnaround and on-site repairs</li><li>Warranty claims and technical support</li><li>Pre-start inspections and operator handover</li><li>Attachment fitment and hydraulic set-up</li></ul></div>
<div class="card dark"><h2 style="font-size:30px;color:#fff">Included with <i>every sale</i></h2><div class="pr"><div><div class="k">Warranty</div><div class="v" style="font-size:30px">5 yr / 200 hr</div><div class="s">Whichever comes first</div></div><div><div class="k">Servicing</div><div class="v" style="font-size:30px">First 3 free</div><div class="s">Booked through the Hallam workshop</div></div></div><div class="btns" style="margin-top:18px"><a class="btn red" href="contact.html">Book a service</a></div></div></div></div></section>
{cta("Book a service", "Call the workshop or send the machine and hours through the enquiry form.")}'''
    page('service.html', 'Workshop & servicing — warranty, parts, repairs | S&S Machinery Hallam',
         'S&S Machinery workshop at Hallam: servicing, stocked parts, warranty claims and operator handover. 5 year / 200 hour warranty and first 3 services free on every machine sold.', body, 'service.html')


def about():
    body = f'''<div class="pband"><div class="wrap"><h1>Our story</h1><p>Family owned, Hallam VIC.</p></div></div>
<section class="alt"><div class="wrap"><div class="two"><div><p class="lead">Sayed and Sons Machinery is a family business based at Factory 5, 65-67 Hallam South Road, Hallam. We design our machines for Australian soil, heat and site conditions and build them with quality international components, so parts and servicing are handled locally rather than shipped from overseas.</p><p class="lead" style="margin-top:14px">Every machine we hire or sell is backed by our Hallam workshop, a 5 year / 200 hour warranty and three free services. We import our own machines, run our own transport and keep the parts on the shelf, which is how we keep the prices where they are.</p></div>
<div class="card"><h2 style="font-size:30px">Find us</h2><div class="kv"><div><div class="k">Yard &amp; workshop</div><div class="v">{e(B["address"])}</div></div><div><div class="k">Hours</div><div class="v">Mon–Fri 7:00 am – 5:00 pm<br>Sat 8:00 am – 12:00 pm</div></div><div><div class="k">Phone</div><div class="v"><a href="tel:{B["phone_tel"]}">{B["phone"]}</a></div></div></div></div></div></div></section>
{cta("Come and see the machines", "The full range is on the floor at Hallam.")}'''
    page('about.html', 'About S&S Machinery — family owned machinery sales and hire, Hallam VIC',
         'Sayed and Sons Machinery is a family business at Hallam, Victoria, designing machines for Australian conditions and backing them with a local workshop.', body, 'about.html')


def contact():
    hours = ''.join(f'<div><div class="k">{e(a)}</div><div class="v">{e(b)}</div></div>' for a, b in HOURS)
    body = f'''<div class="pband"><div class="wrap"><h1>Get in touch</h1><p>Ready to get a machine on site? Tell us the job and we will find the right fit — to hire or to own.</p></div></div>
<section class="alt"><div class="wrap"><div class="contact-grid"><div class="card"><div class="kv"><div><div class="k">Phone</div><div class="v"><a href="tel:{B["phone_tel"]}">{B["phone"]}</a></div></div><div><div class="k">Email</div><div class="v"><a href="mailto:{B["email"]}">{B["email"]}</a></div></div><div><div class="k">Yard &amp; workshop</div><div class="v">Factory 5, 65-67 Hallam South Road<br>Hallam VIC 3803</div></div>{hours}</div><div class="btns" style="margin-top:20px"><a class="btn dark" href="https://maps.google.com/?q=65-67+Hallam+South+Road+Hallam+VIC+3803" target="_blank" rel="noopener">Open in Maps</a></div></div>
<div class="formcard"><h2 style="font-size:30px;margin-bottom:14px">Send an <i>enquiry</i></h2><div id="contactform"></div></div></div></div></section>'''
    scripts = f'<script type="module">import {{mountForm}} from "/assets/form-page.js";var p=new URLSearchParams(location.search).get("m");mountForm(document.getElementById("contactform"),"contact",{{preselect:p}});</script>'
    page('contact.html', 'Contact S&S Machinery — Hallam VIC | 0466 892 400',
         'Contact S&S Machinery at Factory 5, 65-67 Hallam South Road, Hallam VIC 3803. Phone 0466 892 400, sales@sandsmachinery.com.au. Open Mon–Fri 7–5, Sat 8–12.', body, 'contact.html', scripts=scripts)


def terms():
    body = f'''<div class="pband"><div class="wrap"><h1>Hire agreement</h1><p>The terms that apply to every machine hired from S&amp;S Machinery.</p></div></div>
<section class="alt"><div class="wrap terms">
<h3>1. General terms</h3><p>By booking a machine from S&amp;S Machinery you agree to the following terms. All hire charges are exclusive of GST and are subject to change without notice. Fuel is provided at the start of the hire period and the machine must be returned full, or fuel is charged at cost at the end of the hire.</p>
<h3>2. Payment and deposits</h3><p>Hire charges are payable in advance unless a trade account has been approved. A security bond of $500 (mini loaders) or $1,000 (skid steer and excavator) is pre-authorised on a credit card at pick-up or delivery and released within 5 business days of the machine being returned in the condition it left.</p>
<h3>3. Damage and maintenance</h3><p>The hirer is responsible for the machine from delivery or pick-up until it is returned, including loss, theft and damage. A 12% damage waiver applies to every hire and limits the hirer's liability for accidental damage to the bond amount, subject to the waiver exclusions. The hirer must not repair, modify or service the machine; report any fault to S&amp;S Machinery immediately and stop using the machine if it is unsafe. Only operators who have completed the S&amp;S handover induction may operate the machine.</p>
<h3>4. Delivery and return</h3><p>Delivery is provided from our Factory 5 yard in Hallam. Delivery within 25 km is $120 each way; between 25 km and 50 km it is $180 each way; pick-up from the yard is free. All machines must be returned to the yard in Hallam, or be ready for collection, at the end of the hire period.</p>
<h3>5. Cancellations</h3><p>Free cancellation up to 24 hours before the start of the hire; later cancellations are charged one day's hire.</p>
</div></section>'''
    page('hire-terms.html', 'Hire terms | S&S Machinery', 'S&S Machinery hire agreement: payment, bond, damage waiver, delivery and cancellation terms.', body, 'hire-terms.html')


def rewrite_machine_shells():
    """Machine shells: nav to new root pages, buttons to hire.html?m= / contact.html?m="""
    for m in MACHINES:
        p = f'{OUT}/machines/{m["slug"]}.html'
        s = open(p).read()
        start = s.index('<div class="nav">'); end = s.index('</div></div>', start) + len('</div></div>')
        s = s[:start] + nav('../', 'machines.html') + s[end:]
        fs = s.index('<footer>'); fe = s.index('</footer>') + len('</footer>')
        s = s[:fs] + footer('../') + s[fe:]
        open(p, 'w').write(s)


def main():
    open(f'{OUT}/assets/site.css', 'w').write(BASE_CSS + EXTRA_CSS)
    pass  # form-page.js is maintained directly in site/assets (Web3Forms relay)
    home(); machines(); hire(); attachments(); service(); about(); contact(); terms()
    rewrite_machine_shells()
    # render.js: point CTAs at new pages with machine preselect
    r = open(f'{OUT}/assets/render.js').read()
    r = r.replace('href="\'+B.site+\'/contact">Enquire to buy', 'href="../contact.html?m=\'+encodeURIComponent(m.name)+\'">Enquire to buy')
    r = r.replace('href="\'+B.site+\'/hire">Book a hire', 'href="../hire.html?m=\'+encodeURIComponent(m.name)+\'#book">Book a hire')
    r = r.replace('href="\'+B.site+\'/contact">Send an enquiry', 'href="../contact.html?m=\'+encodeURIComponent(m.name)+\'">Send an enquiry')
    r = r.replace("B.site+'/contact'", "'../contact.html?m='+encodeURIComponent(m.name)").replace("B.site+'/hire'", "'../hire.html?m='+encodeURIComponent(m.name)+'#book'")
    open(f'{OUT}/assets/render.js', 'w').write(r)
    os.system(f'ls -la {OUT} {OUT}/assets && wc -c {OUT}/*.html {OUT}/assets/*.js {OUT}/assets/site.css')


main()
