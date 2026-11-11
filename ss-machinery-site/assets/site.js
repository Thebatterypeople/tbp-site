
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
