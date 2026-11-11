import json, os, shutil, html
from machines_data import MACHINES, BUSINESS as B, price_str

MEDIA = json.load(open('/home/claude/work/wix_media.json'))
MAN = json.load(open('/home/claude/work/web_assets/manifest.json'))
OUT = '/home/claude/work/site'
SITE = B['site']
LOGO_W = MEDIA['brand/logo-white.png']
LOGO_B = MEDIA['brand/logo-black.png']


def thumb(url, w, h=None, q=80):
    h = h or w
    name = url.rsplit('/', 1)[-1].split('~')[0] + '.jpg'
    return f'{url}/v1/fill/w_{w},h_{h},al_c,q_{q},enc_auto/{name}'


def e(s):
    return html.escape(s, quote=True)


CSS = r"""
:root{--red:#E31E24;--ink:#111;--ink2:#2a2a2a;--line:#e6e6e6;--bg:#f6f6f6;--muted:#666}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Barlow,system-ui,Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.5}
h1,h2,h3,.cond{font-family:"Barlow Condensed",Barlow,Arial,sans-serif;text-transform:uppercase;letter-spacing:.01em;line-height:1}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.nav{background:#0d0d0d;color:#fff;position:sticky;top:0;z-index:50;border-bottom:1px solid #222}
.nav .wrap{display:flex;align-items:center;gap:28px;height:64px}
.nav img{height:34px;width:auto;display:block}
.nav .links{margin-left:auto;display:flex;gap:22px;font-family:"Barlow Condensed";font-weight:600;font-size:17px;text-transform:uppercase;letter-spacing:.04em}
.nav .links a{text-decoration:none;color:#ddd}.nav .links a:hover,.nav .links a.on{color:#fff;border-bottom:2px solid var(--red)}
.nav .call{background:var(--red);color:#fff;padding:9px 14px;border-radius:3px;text-decoration:none;font-weight:700;white-space:nowrap}
@media(max-width:760px){.nav .links{display:none}}
.hero{background:radial-gradient(ellipse at 50% 35%,#2b2b2b 0%,#141414 70%);color:#fff;padding:36px 0 44px}
.hero .grid{display:grid;grid-template-columns:1.05fr .95fr;gap:36px;align-items:center}
@media(max-width:900px){.hero .grid{grid-template-columns:1fr}}
.crumb{font-size:13px;color:#aaa;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px}
.crumb a{color:#aaa;text-decoration:none}
.hero h1{font-size:clamp(56px,8vw,104px);font-weight:800;color:var(--red);margin:0 0 6px}
.hero .type{font-family:"Barlow Condensed";font-size:clamp(20px,2.4vw,28px);font-weight:600;text-transform:uppercase;color:#fff;letter-spacing:.03em}
.hero p.tag{font-size:18px;color:#cfcfcf;margin:14px 0 22px;max-width:52ch}
.pricebox{display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap;margin:6px 0 22px}
.pricebox .from{font-family:"Barlow Condensed";font-size:14px;letter-spacing:.14em;color:#bbb;text-transform:uppercase}
.pricebox .amt{font-family:"Barlow Condensed";font-weight:800;font-size:clamp(44px,5vw,64px);line-height:.9}
.pricebox .inc{font-size:14px;color:#bbb;max-width:28ch;padding-bottom:6px}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;padding:14px 22px;border-radius:3px;text-decoration:none;font-weight:700;font-size:16px;border:2px solid transparent}
.btn.red{background:var(--red);color:#fff}.btn.ghost{border-color:#fff;color:#fff}.btn.dark{background:var(--ink);color:#fff}
.btn:hover{filter:brightness(1.08)}
.assure{display:flex;gap:22px;flex-wrap:wrap;margin-top:22px;font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:14px;color:#ddd}
.assure span::before{content:"";display:inline-block;width:8px;height:8px;background:var(--red);margin-right:8px;transform:rotate(45deg)}
/* spin */
.spin{position:relative;aspect-ratio:1/1;max-width:620px;margin:0 auto;user-select:none;touch-action:pan-y;cursor:grab}
.spin:active{cursor:grabbing}
.spin img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .08s linear;pointer-events:none;filter:drop-shadow(0 18px 22px rgba(0,0,0,.55))}
.spin img.on{opacity:1}
.spin .floor{position:absolute;left:12%;right:12%;bottom:4%;height:10%;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.6),rgba(0,0,0,0) 70%)}
.spin .hint{position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);font-family:"Barlow Condensed";font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#aaa;white-space:nowrap}
.spin .hint b{color:#fff}
.spin .arr{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:1px solid #555;background:rgba(0,0,0,.4);color:#fff;font-size:20px;line-height:38px;text-align:center;cursor:pointer}
.spin .arr.l{left:-4px}.spin .arr.r{right:-4px}
.spin .badge{position:absolute;top:8px;left:8px;background:var(--red);color:#fff;font-family:"Barlow Condensed";font-weight:700;font-size:13px;letter-spacing:.14em;padding:5px 9px;text-transform:uppercase}
/* body */
section{padding:56px 0}
section.alt{background:var(--bg)}
h2{font-size:clamp(34px,4vw,48px);font-weight:800;margin:0 0 22px}
h2 i{color:var(--red);font-style:normal}
.two{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:start}
@media(max-width:860px){.two{grid-template-columns:1fr}}
.lead{font-size:19px;color:var(--ink2);max-width:62ch}
ul.ticks{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:9px}
ul.ticks li{padding-left:26px;position:relative;font-size:17px}
ul.ticks li::before{content:"";position:absolute;left:0;top:7px;width:11px;height:11px;background:var(--red);transform:rotate(45deg)}
.card{background:#fff;border:1px solid var(--line);border-radius:6px;padding:22px}
.card.dark{background:#111;color:#fff;border-color:#111}
table.specs{width:100%;border-collapse:collapse;font-size:17px}
table.specs td{padding:12px 0;border-bottom:1px solid var(--line);vertical-align:top}
table.specs td:first-child{color:var(--muted);width:46%;font-family:"Barlow Condensed";text-transform:uppercase;letter-spacing:.06em;font-size:15px;padding-top:14px}
table.specs td:last-child{font-weight:600}
.pr{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.pr .k{font-family:"Barlow Condensed";font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#bbb}
.pr .v{font-family:"Barlow Condensed";font-weight:800;font-size:40px;line-height:1;margin:6px 0 4px}
.pr .s{font-size:14px;color:#bbb}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
.chips span{border:1px solid #444;color:#ddd;padding:7px 11px;border-radius:3px;font-size:14px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.gal a{display:block;aspect-ratio:1/1;background:#fff;border:1px solid var(--line);border-radius:4px;overflow:hidden}
.gal img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .25s}.gal a:hover img{transform:scale(1.04)}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:100;cursor:zoom-out}
.lb.on{display:flex}.lb img{max-width:94vw;max-height:92vh;background:#fff}
.cta{background:var(--red);color:#fff;text-align:center;padding:60px 0}
.cta h2{color:#fff;margin-bottom:10px}.cta p{font-size:18px;margin:0 0 22px;color:#ffe9ea}
.cta .btn.ghost{border-color:#fff}
.cta .btn.white{background:#fff;color:var(--red)}
footer{background:#0d0d0d;color:#bbb;padding:40px 0;font-size:14px}
footer .wrap{display:flex;gap:30px;flex-wrap:wrap;align-items:center;justify-content:space-between}
footer img{height:30px}footer a{color:#fff;text-decoration:none}
.fine{font-size:13px;color:var(--muted);margin-top:14px}
/* index */
.mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:22px}
.mcard{background:#141414;color:#fff;border-radius:8px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;border:1px solid #222;transition:transform .2s,border-color .2s}
.mcard:hover{transform:translateY(-3px);border-color:var(--red)}
.mcard .img{aspect-ratio:1/1;background:radial-gradient(ellipse at 50% 40%,#2c2c2c,#121212 70%);display:flex;align-items:flex-end;justify-content:center;padding:18px}
.mcard .img img{width:88%;height:auto;filter:drop-shadow(0 16px 18px rgba(0,0,0,.6))}
.mcard .body{padding:18px 20px 22px}
.mcard .t{font-family:"Barlow Condensed";font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#aaa}
.mcard h3{font-size:40px;font-weight:800;margin:2px 0 4px;color:#fff}
.mcard .p{font-family:"Barlow Condensed";font-weight:800;font-size:28px;color:var(--red)}
.mcard .p small{font-family:Barlow;font-weight:400;font-size:13px;color:#aaa;margin-left:6px}
.mcard .d{color:#cfcfcf;font-size:15px;margin:8px 0 14px;min-height:44px}
.mcard .go{font-family:"Barlow Condensed";font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#fff}
.mcard .go::after{content:" →"}
.band{background:#111;color:#fff;padding:56px 0}
.band h1{font-size:clamp(48px,7vw,92px);color:var(--red);margin:0 0 8px}
.band p{font-size:19px;color:#cfcfcf;max-width:70ch;margin:0}
"""

JS = r"""
(function(){
  var sp=document.querySelector('.spin');if(!sp)return;
  var imgs=[].slice.call(sp.querySelectorAll('img')),n=imgs.length,i=0,auto=true,t;
  function show(k){i=((k%n)+n)%n;imgs.forEach(function(im,j){im.classList.toggle('on',j===i)});}
  function startAuto(){clearInterval(t);t=setInterval(function(){if(auto)show(i+1)},1400);}
  startAuto();
  var down=false,sx=0,acc=0,step=Math.max(28,Math.round(sp.clientWidth/ n /1.4));
  function px(ev){return (ev.touches?ev.touches[0].clientX:ev.clientX);}
  sp.addEventListener('pointerdown',function(ev){down=true;sx=px(ev);acc=0;auto=false;sp.setPointerCapture&&sp.setPointerCapture(ev.pointerId);});
  window.addEventListener('pointerup',function(){down=false;});
  sp.addEventListener('pointermove',function(ev){if(!down)return;var dx=px(ev)-sx;acc+=dx;sx=px(ev);while(acc>step){show(i-1);acc-=step}while(acc<-step){show(i+1);acc+=step}});
  sp.querySelector('.arr.l').addEventListener('click',function(ev){ev.stopPropagation();auto=false;show(i-1)});
  sp.querySelector('.arr.r').addEventListener('click',function(ev){ev.stopPropagation();auto=false;show(i+1)});
  var lb=document.querySelector('.lb');
  if(lb){document.querySelectorAll('.gal a').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();lb.querySelector('img').src=a.href;lb.classList.add('on');});});lb.addEventListener('click',function(){lb.classList.remove('on')});}
})();
"""

HEAD = """<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}"><meta property="og:type" content="product">
<link rel="icon" href="{shield}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
</head><body>"""


def nav(root, on=''):
    L = [('Home', SITE + '/', ''), ('Machines', root + 'index.html', 'machines'), ('Hire', SITE + '/hire', ''),
         ('Attachments', SITE + '/attachments', ''), ('Service', SITE + '/service', ''), ('Contact', SITE + '/contact', '')]
    links = ''.join(f'<a href="{h}" class="{"on" if k == on and k else ""}">{t}</a>' for t, h, k in L)
    return (f'<div class="nav"><div class="wrap"><a href="{SITE}/"><img src="{LOGO_W}" alt="S&amp;S Machinery"></a>'
            f'<div class="links">{links}</div><a class="call" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a></div></div>')


def footer():
    return (f'<footer><div class="wrap"><img src="{LOGO_W}" alt="S&amp;S Machinery">'
            f'<div>{e(B["legal"])} · {e(B["address"])}</div>'
            f'<div><a href="tel:{B["phone_tel"]}">{B["phone"]}</a> · <a href="mailto:{B["email"]}">{B["email"]}</a> · <a href="{SITE}">{B["web"]}</a></div>'
            f'</div></footer><script src="{{root}}assets/site.js"></script></body></html>')


def machine_page(m):
    k = m['key']; root = '../'
    spin = [MEDIA[f'{k}/{f}'] for f in MAN[k]['spin']]
    angles = [MEDIA[f'{k}/{f}'] for f in MAN[k]['angles']]
    hero_tile = MEDIA[f'{k}/hero_tile.jpg']
    title = f'{m["name"]} {m["type"]} — {price_str(m["price"])} inc GST | S&S Machinery Hallam'
    desc = f'{m["name"]} {m["type"].lower()}: {m["engine"]}, {dict(m["specs"]).get("Operating weight")} operating weight. {price_str(m["price"])} inc GST, 5 year / 200 hour warranty, first 3 services free. Hire or buy from S&S Machinery, Hallam VIC.'
    h = HEAD.format(title=e(title), desc=e(desc), og=hero_tile, shield=MEDIA['brand/shield-white.png'], root=root)
    h += nav(root, 'machines')
    spin_imgs = ''.join(f'<img src="{u}" alt="{e(m["name"])} view {j+1}" class="{"on" if j == 0 else ""}" loading="eager">' for j, u in enumerate(spin))
    h += f'''<div class="hero"><div class="wrap"><div class="grid">
<div><div class="crumb"><a href="{root}index.html">Machines</a> / {e(m["cls"])}</div>
<h1>{e(m["name"])}</h1><div class="type">{e(m["type"])}</div>
<p class="tag">{e(m["tagline"])}</p>
<div class="pricebox"><div><div class="from">Buy from</div><div class="amt">{price_str(m["price"])}</div></div><div class="inc">{e(m["price_note"])}</div></div>
<div class="btns"><a class="btn red" href="{SITE}/contact">Enquire to buy</a><a class="btn ghost" href="{SITE}/hire">Book a hire</a><a class="btn ghost" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a></div>
<div class="assure"><span>{e(B["warranty"])}</span><span>{e(B["services"])}</span><span>In stock at Hallam</span></div>
</div>
<div><div class="spin"><div class="badge">360° view</div><div class="floor"></div>{spin_imgs}<div class="arr l">&#8249;</div><div class="arr r">&#8250;</div><div class="hint"><b>Drag</b> to rotate</div></div></div>
</div></div></div>'''
    bl = ''.join(f'<li>{e(b)}</li>' for b in m['bullets'])
    specs = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in m['specs'])
    uses = ''.join(f'<li>{e(u)}</li>' for u in m['uses'])
    h += f'''<section><div class="wrap"><div class="two">
<div><h2>Built for <i>the job</i></h2><p class="lead">{e(m["blurb"])}</p><ul class="ticks">{bl}</ul>
<h3 style="font-size:26px;margin:30px 0 8px">Typical work</h3><ul class="ticks">{uses}</ul></div>
<div class="card"><h2 style="font-size:30px">Specifications</h2><table class="specs">{specs}</table>
<p class="fine">Specifications from the manufacturer's compliance plate. Confirm final configuration with us before purchase.</p></div>
</div></div></section>'''
    deliv = ''.join(f'<div><div class="k">{e(a)}</div><div class="v" style="font-size:30px">{e(b)}</div></div>' for a, b in B['delivery'])
    chips = ''.join(f'<span>{e(a)}</span>' for a in B['attachments'])
    h += f'''<section class="alt"><div class="wrap"><h2>Price, <i>warranty</i> &amp; delivery</h2>
<div class="card dark"><div class="pr">
<div><div class="k">Purchase price</div><div class="v">{price_str(m["price"])}</div><div class="s">{e(m["price_note"])}</div></div>
<div><div class="k">Warranty</div><div class="v" style="font-size:30px">5 yr / 200 hr</div><div class="s">Standard on every machine we sell</div></div>
<div><div class="k">Servicing</div><div class="v" style="font-size:30px">First 3 free</div><div class="s">Booked through our Hallam workshop</div></div>
<div><div class="k">Hire</div><div class="v" style="font-size:30px">Day / week</div><div class="s">{e(B["hire_line"])}</div></div>
</div>
<hr style="border:0;border-top:1px solid #333;margin:22px 0">
<div class="pr">{deliv}</div><div class="s" style="color:#bbb;font-size:14px;margin-top:8px">{e(B["delivery_note"])}</div>
<hr style="border:0;border-top:1px solid #333;margin:22px 0">
<div class="k">Attachments</div><div class="chips">{chips}</div>
</div></div></section>'''
    gal = ''.join(f'<a href="{u}"><img src="{thumb(u, 520)}" alt="{e(m["name"])} angle {j+1}" loading="lazy"></a>' for j, u in enumerate(angles))
    h += f'''<section><div class="wrap"><h2>Every <i>angle</i></h2><div class="gal">{gal}</div></div></section>
<div class="lb"><img alt=""></div>
<div class="cta"><div class="wrap"><h2>Hire it. Own it.</h2><p>Come and see the {e(m["name"])} at our Hallam yard, or call and we'll talk you through the options.</p>
<div class="btns" style="justify-content:center"><a class="btn white" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a><a class="btn ghost" href="{SITE}/contact">Send an enquiry</a><a class="btn ghost" href="mailto:{B["email"]}?subject={e(m["name"])} enquiry">Email us</a></div></div></div>'''
    h += footer().replace('{root}', root)
    return h


def index_page():
    root = ''
    title = 'Machines for sale & hire — mini loaders, skid steer, excavator | S&S Machinery Hallam'
    desc = 'S&S Machinery range: HM 370T, HM 380T, HM 750T and HM 1000T stand-on mini loaders, HM 1500S skid steer and HME 30T excavator. Buy or hire from Hallam, Victoria. 5 year / 200 hour warranty, first 3 services free.'
    h = HEAD.format(title=e(title), desc=e(desc), og=MEDIA['HM1500S/hero_tile.jpg'], shield=MEDIA['brand/shield-white.png'], root=root)
    h += nav(root, 'machines')
    h += f'''<div class="band"><div class="wrap"><h1>The range</h1><p>Six machines, every one in stock at Hallam and available to hire by the day or week or to own outright. Every machine sold comes with a {B["warranty"]} and the first three services free.</p></div></div>'''
    cards = ''
    for m in MACHINES:
        cut = MEDIA[f'{m["key"]}/hero_cutout.webp']
        cards += f'''<a class="mcard" href="machines/{m["slug"]}.html"><div class="img"><img src="{cut}" alt="{e(m["name"])}" loading="lazy"></div>
<div class="body"><div class="t">{e(m["type"])}</div><h3>{e(m["name"])}</h3><div class="p">{price_str(m["price"])}<small>inc GST</small></div>
<div class="d">{e(m["tagline"])}</div><div class="go">View machine &amp; 360°</div></div></a>'''
    h += f'<section class="alt"><div class="wrap"><div class="mgrid">{cards}</div></div></section>'
    h += f'''<div class="cta"><div class="wrap"><h2>Not sure which one?</h2><p>Tell us the job and we'll match the machine. Call {B["phone"]} or send an enquiry.</p>
<div class="btns" style="justify-content:center"><a class="btn white" href="tel:{B["phone_tel"]}">Call {B["phone"]}</a><a class="btn ghost" href="{SITE}/contact">Send an enquiry</a></div></div></div>'''
    h += footer().replace('{root}', root)
    return h


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(f'{OUT}/assets'); os.makedirs(f'{OUT}/machines')
    open(f'{OUT}/assets/site.css', 'w').write(CSS)
    open(f'{OUT}/assets/site.js', 'w').write(JS)
    open(f'{OUT}/index.html', 'w').write(index_page())
    for m in MACHINES:
        open(f'{OUT}/machines/{m["slug"]}.html', 'w').write(machine_page(m))
    os.system(f'du -sh {OUT}; find {OUT} -type f | xargs wc -c | tail -1')


main()
