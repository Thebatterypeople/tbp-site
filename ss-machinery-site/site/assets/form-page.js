
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
