
(function(){
  var slug=document.body.getAttribute('data-machine'),m=window.SS_MACHINES[slug],B=window.SS_BIZ;if(!m)return;
  var GLB={"HM370T":"e98477_f4b6968ced7b4573bc7e8ab773dbdff4","HM380T":"e98477_3452a9f3ba9f4bfeb938cdb164134566","HM750T":"e98477_882a220774c34b80a96096a6880dd4e1","HM1000T":"e98477_c01c7a6781e44fd4bb360d4dec47439b","HM1500S":"e98477_895967eb2e2f49959ce882a48e0aae91","HME30T":"e98477_a48548fc3e454be3b4e6402653512489"};
  var M='https://static.wixstatic.com/media/';function full(id){return M+id}function th(id){return M+id+'/v1/fill/w_520,h_520,al_c,q_80,enc_auto/'+id.split('~')[0]+'.jpg'}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  var h='';
  h+='<div class="hero"><div class="wrap"><div class="grid"><div><div class="crumb"><a href="../index.html">Machines</a> / '+esc(m.cls)+'</div>'
    +'<h1>'+esc(m.name)+'</h1><div class="type">'+esc(m.type)+'</div><p class="tag">'+esc(m.tagline)+'</p>'
    +'<div class="pricebox"><div><div class="from">Buy from</div><div class="amt">'+esc(m.price)+'</div></div><div class="inc">'+esc(m.price_note)+'</div></div>'
    +'<div class="btns"><a class="btn red" href="../contact.html?m='+encodeURIComponent(m.name)+'">Enquire to buy</a><a class="btn ghost" href="../hire.html?m='+encodeURIComponent(m.name)+'#book">Book a hire</a><a class="btn ghost" href="tel:'+B.tel+'">Call '+B.phone+'</a></div>'
    +'<div class="assure"><span>'+esc(B.warranty)+'</span><span>'+esc(B.services)+'</span><span>In stock at Hallam</span></div></div>'
    +'<div class="viewer"><div class="vtabs"><button class="on" data-v="spin">360° photos</button><button data-v="3d">3D model</button></div><div class="spin"><div class="badge">360° view</div><div class="floor"></div>'
    +m.spin.map(function(u,j){return '<img src="'+full(u)+'" alt="'+esc(m.name)+' view '+(j+1)+'"'+(j?'':' class="on"')+'>'}).join('')
    +'<div class="arr l">&#8249;</div><div class="arr r">&#8250;</div><div class="hint"><b>Drag</b> to rotate</div></div><div class="mv3d" hidden><div class="badge">3D model</div><div class="hint"><b>Drag</b> to orbit · pinch or scroll to zoom</div></div></div></div></div></div>';
  h+='<section><div class="wrap"><div class="two"><div><h2>Built for <i>the job</i></h2><p class="lead">'+esc(m.blurb)+'</p><ul class="ticks">'
    +m.bullets.map(function(b){return '<li>'+esc(b)+'</li>'}).join('')+'</ul><h3 style="font-size:26px;margin:30px 0 8px">Typical work</h3><ul class="ticks">'
    +m.uses.map(function(b){return '<li>'+esc(b)+'</li>'}).join('')+'</ul></div>'
    +'<div class="card"><h2 style="font-size:30px">Specifications</h2><table class="specs">'
    +m.specs.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td>'+esc(r[1])+'</td></tr>'}).join('')
    +'</table><p class="fine">Specifications from the manufacturer\'s compliance plate. Confirm final configuration with us before purchase.</p></div></div></div></section>';
  h+='<section class="alt"><div class="wrap"><h2>Price, <i>warranty</i> &amp; delivery</h2><div class="card dark"><div class="pr">'
    +'<div><div class="k">Purchase price</div><div class="v">'+esc(m.price)+'</div><div class="s">'+esc(m.price_note)+'</div></div>'
    +'<div><div class="k">Warranty</div><div class="v" style="font-size:30px">5 yr / 200 hr</div><div class="s">Standard on every machine we sell</div></div>'
    +'<div><div class="k">Servicing</div><div class="v" style="font-size:30px">First 3 free</div><div class="s">Booked through our Hallam workshop</div></div>'
    +'<div><div class="k">Hire</div><div class="v" style="font-size:30px">Day / week</div><div class="s">'+esc(B.hire_line)+'</div></div></div>'
    +'<hr style="border:0;border-top:1px solid #333;margin:22px 0"><div class="pr">'
    +B.delivery.map(function(d){return '<div><div class="k">'+esc(d[0])+'</div><div class="v" style="font-size:30px">'+esc(d[1])+'</div></div>'}).join('')
    +'</div><div class="s" style="color:#bbb;font-size:14px;margin-top:8px">'+esc(B.delivery_note)+'</div>'
    +'<hr style="border:0;border-top:1px solid #333;margin:22px 0"><div class="k">Attachments</div><div class="chips">'
    +B.attachments.map(function(a){return '<span>'+esc(a)+'</span>'}).join('')+'</div></div></div></section>';
  h+='<section><div class="wrap"><h2>Every <i>angle</i></h2><div class="gal">'
    +m.angles.map(function(a,j){return '<a href="'+full(a)+'"><img src="'+th(a)+'" alt="'+esc(m.name)+' angle '+(j+1)+'" loading="lazy"></a>'}).join('')
    +'</div></div></section><div class="lb"><img alt=""></div>';
  h+='<div class="cta"><div class="wrap"><h2>Hire it. Own it.</h2><p>Come and see the '+esc(m.name)+' at our Hallam yard, or call and we\'ll talk you through the options.</p>'
    +'<div class="btns" style="justify-content:center"><a class="btn white" href="tel:'+B.tel+'">Call '+B.phone+'</a><a class="btn ghost" href="../contact.html?m='+encodeURIComponent(m.name)+'">Send an enquiry</a><a class="btn ghost" href="mailto:'+B.email+'?subject='+encodeURIComponent(m.name+' enquiry')+'">Email us</a></div></div></div>';
  document.getElementById('app').innerHTML=h;
  var s=document.createElement('script');s.src='../assets/site.js';document.body.appendChild(s);
  var tabs=document.querySelectorAll('.vtabs button'),spinEl=document.querySelector('.spin'),box=document.querySelector('.mv3d'),loaded=false;
  tabs.forEach(function(b){b.addEventListener('click',function(){tabs.forEach(function(x){x.classList.toggle('on',x===b)});var is3d=b.getAttribute('data-v')==='3d';spinEl.hidden=is3d;box.hidden=!is3d;
    if(is3d&&!loaded){loaded=true;var sc=document.createElement('script');sc.type='module';sc.src='https://unpkg.com/@google/model-viewer@4/dist/model-viewer.min.js';document.head.appendChild(sc);
      var mv=document.createElement('model-viewer');mv.setAttribute('src','https://static.wixstatic.com/3d/'+GLB[m.key]+'.glb');mv.setAttribute('alt',m.name+' 3D model');mv.setAttribute('camera-controls','');mv.setAttribute('auto-rotate','');mv.setAttribute('shadow-intensity','0.9');mv.setAttribute('exposure','1.05');mv.setAttribute('environment-image','neutral');mv.setAttribute('camera-orbit','35deg 78deg auto');box.insertBefore(mv,box.querySelector('.hint'));}});});
})();
