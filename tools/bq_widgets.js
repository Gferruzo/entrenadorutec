/* ================= ANÁLISIS BIOQUÍMICO (XTART): interactivos =================
   IW.lab:   «Lee la analítica». ch.pac (texto del paciente), ch.rows=[{n,v,u,r,a:-1|0|1,e}] → marcar ↓ / = / ↑ en cada parámetro (puntaje parcial).
   IW.tree:  árbol diagnóstico paso a paso. ch.steps=[{q,o:[correcta,…],e:[,expl. de cada errada],ok:'nota al acertar'}], ch.end (conclusión).
   IW.mkt:   línea de tiempo de marcadores. ch.set='iam'|'panc', ch.a=[desde,hasta] (horas) → mover el deslizador hasta un momento que cumpla el enunciado.
   IW.tira:  tira reactiva de orina. ch.res={glu:i,pro:i,…} (índice del color real), ch.ask=['glu',…] (almohadillas a leer; por defecto todas).
   IW.micro: microscopio. ch.items=[{k,x,y,r}] (k = clave de BQ_MIC, x,y en −1..1), ch.a=[índices a tocar], ch.obj=10|40.
   IW.espec: espectrofotómetro virtual. ch.s={n,col,lmax,Cp,Ap,As,reag,dil} → hacer el procedimiento y escribir la concentración.
   Herramientas (🧪): LW.mk (marcadores), LW.tira (carta de colores), LW.micro (atlas del sedimento), LW.espec (espectrofotómetro libre), LW.calib (curva de calibrado). */
const bqLock=w=>w.classList.add('lk');
/* ---------- Lee la analítica ---------- */
IW.lab=(ch,o)=>{const w=el('div','bqlab');let lk=false;
  const hd=el('div','bqlabh','<b>🧪 Informe de laboratorio</b>'+(ch.pac?'<span>'+ch.pac+'</span>':''));w.append(hd);
  const t=el('div','bqlabt');t.append(el('div','bqlabr bqlabhd','<span>Parámetro</span><span>Resultado</span><span>Referencia</span><span>Valoración</span>'));
  const L=['↓','=','↑'],TT=['Bajo','Normal','Alto'];
  const rows=ch.rows.map(r=>{const R={r,v:null};const d=el('div','bqlabr');d.append(el('span','bqn',r.n),el('span','bqv','<b>'+r.v+'</b> '+(r.u||'')),el('span','bqr',r.r||''));
    const seg=el('span','bqseg');R.bs=[-1,0,1].map((v,k)=>{const b=el('button','bqb',L[k]);b.type='button';b.title=TT[k];b.setAttribute('aria-label',r.n+': '+TT[k]);
      b.onclick=()=>{if(lk)return;R.v=v;R.bs.forEach(x=>x.classList.toggle('on',x===b));d.classList.remove('good','bad');o.on&&o.on()};seg.append(b);return b});
    d.append(seg);t.append(d);R.d=d;return R});
  w.append(t);typeset(w);
  return{el:w,note:'Marca cada parámetro: ↓ bajo, = normal, ↑ alto (compara con la referencia).',need:'Valora todos los parámetros antes de comprobar.',okMsg:'¡Analítica bien leída!',
   filled:()=>rows.every(R=>R.v!=null),
   grade(){const bad=rows.filter(R=>R.v!==R.r.a);const ex=bad.filter(R=>R.r.e).slice(0,3).map(R=>'<br>• <b>'+R.r.n+'</b>: '+R.r.e).join('');
    return{f:(rows.length-bad.length)/rows.length,msg:bad.length?(bad.length===1?'Un parámetro está mal valorado (en rojo).':bad.length+' parámetros están mal valorados (en rojo).')+ex:''}},
   mark(){rows.forEach(R=>{const k=R.v===R.r.a;R.d.classList.toggle('good',k);R.d.classList.toggle('bad',!k)})},
   reveal(){rows.forEach(R=>{R.v=R.r.a;R.bs.forEach((b,k)=>b.classList.toggle('on',k-1===R.r.a));R.d.classList.remove('bad');R.d.classList.add('good')})},
   lock(){lk=true;bqLock(w);rows.forEach(R=>R.bs.forEach(b=>b.disabled=true))}}};
/* ---------- Árbol diagnóstico ---------- */
IW.tree=(ch,o)=>{const w=el('div','bqtree');const n=ch.steps.length;let cur=0,lk=false;const miss=new Array(n).fill(0);
  const path=el('div','bqpath');const q=el('div','bqtq');const fb=el('p','bqtfb');w.append(path,q,fb);
  const node=(i,txt,cls)=>{const d=el('div','bqnode'+(cls?' '+cls:''),'<small>'+(i+1)+'</small><span>'+txt+'</span>');return d};
  const draw=()=>{path.innerHTML='';for(let i=0;i<cur;i++){path.append(node(i,ch.steps[i].o[0],miss[i]?'miss':'ok'));if(ch.steps[i].ok)path.append(el('p','bqnote',ch.steps[i].ok))}
    q.innerHTML='';if(cur>=n){if(ch.end)path.append(el('div','bqend','🏁 '+ch.end));typeset(w);return}
    const s=ch.steps[cur];q.append(el('p','bqtqq','<b>Paso '+(cur+1)+' de '+n+'.</b> '+s.q));const g=el('div','bqopts');
    perm(o.key+'#t'+cur,s.o.length).forEach(oi=>{const b=el('button','opt','<span>'+s.o[oi]+'</span>');b.type='button';
      b.onclick=()=>{if(lk)return;if(oi===0){fb.textContent='';fb.className='bqtfb';cur++;draw();o.on&&o.on()}else{b.classList.add('bad');b.disabled=true;miss[cur]=1;fb.className='bqtfb bad';fb.innerHTML='✗ '+((s.e&&s.e[oi])||'Ese camino no corresponde. Mira otra vez el dato clave.');typeset(fb);o.on&&o.on()}};g.append(b)});
    q.append(g);typeset(w)};
  draw();
  return{el:w,note:'Avanza por el algoritmo: en cada paso elige la rama correcta.',need:'Termina todo el recorrido antes de comprobar.',okMsg:'¡Recorrido sin errores!',
   filled:()=>cur>=n,
   grade(){const m=miss.reduce((a,b)=>a+b,0);return{f:(n-m)/n,msg:m?'Llegaste, pero te equivocaste en '+(m===1?'un paso':m+' pasos')+' (en naranja).':''}},
   mark(){},reveal(){cur=n;draw()},lock(){lk=true;bqLock(w);q.innerHTML=''},
   reset(){cur=0;miss.fill(0);fb.textContent='';draw();o.on&&o.on()}}};
/* ---------- Marcadores en el tiempo ---------- */
const BQ_MK={
 iam:{t:'Infarto agudo de miocardio',u:'h',max:288,ticks:[0,24,48,72,96,120,168,240,288],mk:[
  {n:'CK-MB',c:'#E45756',on:4,pk:18,h:6,off:60},{n:'CK total',c:'#F58518',on:5,pk:24,h:5,off:84},
  {n:'Troponina I',c:'#4C78A8',on:4,pk:24,h:9,off:216},{n:'Troponina T',c:'#72B7B2',on:4,pk:24,h:8,off:288},
  {n:'AST (GOT)',c:'#B279A2',on:8,pk:48,h:4,off:120},{n:'LDH',c:'#9D755D',on:18,pk:72,h:3.5,off:240}]},
 panc:{t:'Pancreatitis aguda',u:'h',max:336,ticks:[0,24,48,72,120,168,240,336],mk:[
  {n:'Amilasa (sangre)',c:'#E45756',on:6,pk:24,h:6,off:96},{n:'Lipasa (sangre)',c:'#4C78A8',on:6,pk:24,h:7,off:240},
  {n:'Amilasa (orina)',c:'#54A24B',on:12,pk:36,h:5,off:168}]}};
const bqMkV=(m,t)=>{if(t<=m.on||t>=m.off)return t>=m.off?0.6:0.6;if(t<=m.pk)return 1+(m.h-1)*Math.pow((t-m.on)/(m.pk-m.on),1.3);return 1+(m.h-1)*Math.pow((m.off-t)/(m.off-m.pk),1.6)};
const bqMkUp=(m,t)=>t>m.on&&t<m.off;
const bqHrs=t=>t<48?Math.round(t)+' h':(Math.round(t/24*10)/10+' días').replace('.',',')+' ('+Math.round(t)+' h)';
function bqMkUI(root,set,onCh,ro){const S=BQ_MK[set];const W=320,H=190,L=34,R=8,T=10,B=24;let t=ro&&ro.t0!=null?ro.t0:0;
  const X=v=>L+(W-L-R)*v/S.max,Y=v=>T+(H-T-B)*(1-v/10);
  const fig=el('div','chfig');const sl=el('input','bqsl');sl.type='range';sl.min=0;sl.max=S.max;sl.step=1;sl.value=t;sl.setAttribute('aria-label','Tiempo desde el inicio');
  const lab=el('p','bqtime');const chips=el('div','bqchips');root.append(fig,lab,sl,chips);
  const draw=()=>{let s='<svg class="pls" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="'+S.t+'">';
    s+='<rect x="'+L+'" y="'+Y(1)+'" width="'+(W-L-R)+'" height="'+(Y(0)-Y(1))+'" fill="var(--ok-bg)"/><text class="chk" x="'+(L+3)+'" y="'+(Y(1)+11)+'" style="font-size:9px">rango normal</text>';
    [0,2,4,6,8,10].forEach(v=>{s+='<line class="chg" x1="'+L+'" x2="'+(W-R)+'" y1="'+Y(v)+'" y2="'+Y(v)+'"/><text class="chk" x="'+(L-4)+'" y="'+(Y(v)+4)+'" text-anchor="end">'+(v?v+'×':'')+'</text>'});
    S.ticks.forEach(v=>s+='<text class="chk" x="'+X(v)+'" y="'+(H-8)+'" text-anchor="middle" style="font-size:9px">'+(v<48?v+'h':Math.round(v/24)+'d')+'</text>');
    S.mk.forEach(m=>{let p='';for(let k=0;k<=160;k++){const tt=S.max*k/160;p+=(k?'L':'M')+X(tt).toFixed(1)+' '+Y(Math.min(10,bqMkV(m,tt))).toFixed(1)}s+='<path d="'+p+'" fill="none" stroke="'+m.c+'" stroke-width="2"/>'});
    s+='<line x1="'+X(t)+'" x2="'+X(t)+'" y1="'+T+'" y2="'+(H-B)+'" stroke="var(--ink)" stroke-width="1.6" stroke-dasharray="4 3"/>';
    s+='<path class="chax" fill="none" d="M'+L+' '+T+'V'+(H-B)+'H'+(W-R)+'"/><text class="chk" x="'+(L+2)+'" y="'+(T+8)+'" style="font-size:9px">× límite normal</text></svg>';fig.innerHTML=s;
    lab.innerHTML='⏱ <b>'+bqHrs(t)+'</b> desde el inicio';chips.innerHTML='';
    S.mk.forEach(m=>{const up=bqMkUp(m,t);chips.append(el('span','bqchip'+(up?' up':''),'<i style="background:'+m.c+'"></i>'+m.n+': <b>'+(up?'↑ elevada':'normal')+'</b>'))})};
  sl.oninput=()=>{t=+sl.value;draw();onCh&&onCh(t)};draw();
  return{get t(){return t},set(v){t=v;sl.value=v;draw()},lock(){sl.disabled=true}}}
LW.mk=(b,o)=>{b.append(el('h4',null,BQ_MK[o.set||'iam'].t));bqMkUI(b,o.set||'iam',null,{t0:o.t0||0})};
IW.mkt=(ch,o)=>{const w=el('div','bqmk');let moved=false,lk=false;const ui=bqMkUI(w,ch.set||'iam',()=>{moved=true;w.classList.remove('good','bad');o.on&&o.on()},{t0:ch.t0||0});
  const inR=()=>ui.t>=ch.a[0]&&ui.t<=ch.a[1];
  return{el:w,note:'Mueve el deslizador del tiempo hasta un momento que cumpla lo que dice el enunciado.',need:'Mueve el deslizador antes de comprobar.',okMsg:'¡Momento correcto!',
   filled:()=>moved,grade(){return{f:inR()?1:0,msg:inR()?'':'En ese momento los marcadores no coinciden con el enunciado. '+(ch.e||'')}},
   mark(g){w.classList.toggle('good',g.f>=1);w.classList.toggle('bad',g.f<1)},reveal(){ui.set(Math.round((ch.a[0]+ch.a[1])/2));w.classList.add('good')},lock(){lk=true;ui.lock()}}};
/* ---------- Tira reactiva de orina ---------- */
const BQ_TIRA=[
 {k:'leu',n:'Leucocitos',s:120,l:['Neg','Trazas','+','++','+++'],c:['#F2EEE3','#E2D9DC','#C9B6CB','#A88DB3','#866C9C']},
 {k:'nit',n:'Nitritos',s:60,l:['Neg','Pos'],c:['#FBF4E6','#F0AFC2']},
 {k:'uro',n:'Urobilinógeno',s:60,l:['0,2','1','2','4','8 mg/dL'],c:['#F7DCC5','#F2C1A8','#ECA690','#E2897C','#D46C6C']},
 {k:'pro',n:'Proteínas',s:60,l:['Neg','Trazas','30','100','300','≥2000 mg/dL'],c:['#E6E05A','#C8D85E','#A7CC6A','#7DB97A','#55A38C','#3C8C8E']},
 {k:'ph',n:'pH',s:60,l:['5','6','6,5','7','7,5','8','8,5'],c:['#F08A3E','#E9A43A','#D7B43C','#AFB83F','#7FAE4A','#3E8E6A','#2D6E85']},
 {k:'san',n:'Sangre',s:60,l:['Neg','Trazas','+','++','+++'],c:['#F2C94C','#C9C24F','#9CB55A','#5E9A63','#2F6E5E']},
 {k:'den',n:'Densidad',s:45,l:['1,000','1,005','1,010','1,015','1,020','1,025','1,030'],c:['#2E5E5A','#45705A','#5E7D4F','#7A8A45','#94933C','#A99B38','#B9A234']},
 {k:'cet',n:'Cetonas',s:40,l:['Neg','Trazas','15','40','80','160 mg/dL'],c:['#F2D9C4','#EBBFB3','#DFA0A3','#C67891','#A55479','#7F3A63']},
 {k:'bil',n:'Bilirrubina',s:30,l:['Neg','+','++','+++'],c:['#F3EBD3','#E9D3B5','#DDB9A0','#C99C8E']},
 {k:'glu',n:'Glucosa',s:30,l:['Neg','100','250','500','≥1000 mg/dL'],c:['#86CBD8','#8FC9A0','#9BB86A','#A6914A','#8B6236']}];
function bqStrip(res,on){const h=BQ_TIRA.length*26+30;let s='<svg class="bqstrip" viewBox="0 0 60 '+h+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tira reactiva"><rect x="18" y="2" width="24" height="'+(h-4)+'" rx="3" fill="#F7F7F2" stroke="#BBB"/><text x="30" y="'+(h-8)+'" text-anchor="middle" font-size="7" fill="#888">mango</text>';
  BQ_TIRA.forEach((p,i)=>{const v=res[p.k]!=null?res[p.k]:0;s+='<rect x="21" y="'+(6+i*26)+'" width="18" height="18" rx="2" fill="'+p.c[v]+'" stroke="'+(on===p.k?'#15233B':'#999')+'" stroke-width="'+(on===p.k?2.5:.8)+'"/>'});return s+'</svg>'}
IW.tira=(ch,o)=>{const ask=ch.ask||BQ_TIRA.map(p=>p.k);const w=el('div','bqtira');let lk=false,cur=ask[0];const sel={};
  const left=el('div','bqtl');const right=el('div','bqtr');w.append(left,right);
  const draw=()=>{left.innerHTML=bqStrip(ch.res,cur);right.innerHTML='';
    BQ_TIRA.forEach(p=>{if(!ask.includes(p.k))return;const row=el('div','bqtrow'+(p.k===cur?' cur':'')+(sel[p.k]!=null?' done':''));row.dataset.k=p.k;
      row.append(el('div','bqtn','<b>'+p.n+'</b> <small>lee a los '+(p.s>=60?(p.s/60)+' min':p.s+' s')+'</small>'));const sw=el('div','bqsw');
      p.c.forEach((c,ci)=>{const b=el('button','bqswb'+(sel[p.k]===ci?' on':''),'<i style="background:'+c+'"></i><small>'+p.l[ci]+'</small>');b.type='button';b.setAttribute('aria-label',p.n+' '+p.l[ci]);
        b.onclick=()=>{if(lk)return;sel[p.k]=ci;cur=p.k;row.classList.remove('bad','good');draw();o.on&&o.on()};sw.append(b)});
      row.onclick=ev=>{if(ev.target.closest('.bqswb'))return;cur=p.k;draw()};row.append(sw);right.append(row)})};
  draw();
  const rowsBad=()=>ask.filter(k=>sel[k]!==ch.res[k]);
  return{el:w,note:'Compara cada almohadilla de la tira (la marcada) con su fila de la carta de colores y toca el color que coincide.',need:'Lee todas las almohadillas antes de comprobar.',okMsg:'¡Tira bien leída!',
   filled:()=>ask.every(k=>sel[k]!=null),
   grade(){const b=rowsBad();return{f:(ask.length-b.length)/ask.length,msg:b.length?'No coincide: '+b.map(k=>BQ_TIRA.find(p=>p.k===k).n).join(', ')+'.'+(ch.e?'<br>'+ch.e:''):''}},
   mark(){right.querySelectorAll('.bqtrow').forEach(r=>{const k=r.dataset.k;r.classList.toggle('good',sel[k]===ch.res[k]);r.classList.toggle('bad',sel[k]!==ch.res[k])})},
   reveal(){ask.forEach(k=>sel[k]=ch.res[k]);draw();right.querySelectorAll('.bqtrow').forEach(r=>r.classList.add('good'))},lock(){lk=true;bqLock(w)}}};
LW.tira=(b,o)=>{const res={};BQ_TIRA.forEach(p=>res[p.k]=0);const box=el('div');b.append(box);const draw=()=>{box.innerHTML='';const w=el('div','bqtira');const L=el('div','bqtl',bqStrip(res));const R=el('div','bqtr');
  BQ_TIRA.forEach(p=>{const row=el('div','bqtrow');row.append(el('div','bqtn','<b>'+p.n+'</b> <small>'+(p.s>=60?(p.s/60)+' min':p.s+' s')+'</small>'));const sw=el('div','bqsw');
    p.c.forEach((c,ci)=>{const x=el('button','bqswb'+(res[p.k]===ci?' on':''),'<i style="background:'+c+'"></i><small>'+p.l[ci]+'</small>');x.type='button';x.onclick=()=>{res[p.k]=ci;draw()};sw.append(x)});row.append(sw);R.append(row)});
  w.append(L,R);box.append(w)};draw();b.append(el('p','note','Toca un color de la carta para «pintar» esa almohadilla y ver cómo se vería la tira.'))};
/* ---------- Microscopio (sedimento, líquido sinovial, heces) ---------- */
const bqE=(rx,ry,f,st,x,y,a)=>'<ellipse cx="'+(x||0)+'" cy="'+(y||0)+'" rx="'+rx+'" ry="'+ry+'" fill="'+f+'" stroke="'+st+'"'+(a?' transform="rotate('+a+' '+(x||0)+' '+(y||0)+')"':'')+'/>';
const BQ_MIC={
 hem:{n:'Hematíe',g:'Células',d:'Disco pequeño y pálido, sin núcleo, con el centro más claro. Si es dismórfico, viene del riñón (glomerular).',s:()=>bqE(6,6,'#F1B3A8','#C9786B')+bqE(2.6,2.6,'#F8D6CF','none')},
 leu:{n:'Leucocito',g:'Células',d:'Algo mayor que el hematíe, granuloso y con núcleo lobulado. Muchos = leucocituria/piuria (infección).',s:()=>bqE(8,8,'#E7E2DA','#8E8A82')+'<path d="M-4 -1q2 -4 4 0q2 4 4 0" fill="none" stroke="#6B6A9A" stroke-width="2"/><circle cx="-2" cy="4" r="1.6" fill="#6B6A9A"/>'},
 esc:{n:'Célula epitelial escamosa',g:'Células',d:'Muy grande y aplanada, bordes irregulares o plegados, núcleo pequeño central. Viene de uretra/vagina: poca importancia.',s:()=>'<path d="M-22 -10L-6 -20L18 -15L24 4L10 20L-14 17L-24 4Z" fill="#F1EEE6" stroke="#9A968C"/><circle r="3" fill="#7F7B70"/>'},
 trans:{n:'Célula de transición',g:'Células',d:'Piriforme o con «cola», núcleo bien visible. Pelvis renal, vejiga, uretra; muchas = inflamación.',s:()=>'<path d="M-10 -6Q-12 8 0 10Q12 8 10 -4Q8 -12 0 -12Q-4 -12 -10 -6Z M8 -6L18 -16" fill="#EEE8DD" stroke="#8C877C"/><circle cx="0" cy="0" r="3.6" fill="#7F7B70"/>'},
 tub:{n:'Célula tubular renal',g:'Células',d:'Cúbica/rectangular, algo mayor que un leucocito, núcleo grande y excéntrico. Indica daño de la nefrona.',s:()=>'<rect x="-9" y="-7" width="18" height="14" rx="3" fill="#E9E3D6" stroke="#8C877C"/><circle cx="3" cy="-1" r="4" fill="#706B60"/>'},
 lev:{n:'Levaduras',g:'Microorganismos',d:'Ovoides pequeñas, a veces con gemación. Se tiñen violeta con Gram. Pueden confundirse con hematíes.',s:()=>bqE(3.5,4.6,'#E6EEE0','#7B8C70',-5,0)+bqE(2.4,3,'#E6EEE0','#7B8C70',-0.5,-5)+bqE(3.5,4.6,'#E6EEE0','#7B8C70',6,3,30)},
 bac:{n:'Bacterias',g:'Microorganismos',d:'Bastoncillos o cocos diminutos y abundantes. Con leucocitos = infección urinaria (confirmar con cultivo).',s:()=>{let s='';[[-8,-6,20],[-3,2,-40],[4,-8,70],[7,5,10],[-7,7,-10],[1,-1,45],[10,-2,-60],[-1,9,80]].forEach(p=>s+='<rect x="'+(p[0]-2.4)+'" y="'+(p[1]-.9)+'" width="4.8" height="1.8" rx=".9" fill="#5E6E7E" transform="rotate('+p[2]+' '+p[0]+' '+p[1]+')"/>');return s}},
 trich:{n:'Trichomonas vaginalis',g:'Microorganismos',d:'Piriforme, con flagelos y muy móvil. Suele acompañarse de piuria.',s:()=>'<path d="M-6 -8Q0 -12 6 -8Q8 2 0 10Q-8 2 -6 -8Z" fill="#E4EBE6" stroke="#6E8577"/><path d="M-2 -11Q-6 -18 -2 -22M1 -11Q2 -19 6 -21M3 -10Q8 -15 11 -14M0 10Q2 16 -1 20" fill="none" stroke="#6E8577"/><circle cx="0" cy="-4" r="2.2" fill="#6E8577"/>'},
 esp:{n:'Espermatozoide',g:'Células',d:'Cabeza ovalada y cola larga. Hallazgo casual (en varones se informa).',s:()=>bqE(3.2,4.4,'#ECE7DD','#7E786C',0,-10)+'<path d="M0 -5Q4 2 -2 8Q-6 14 0 20" fill="none" stroke="#7E786C" stroke-width="1.2"/>'},
 chia:{n:'Cilindro hialino',g:'Cilindros',d:'Homogéneo, incoloro, poco refringente, extremos romos. Difícil de ver; deshidratación o ejercicio, sin gran valor clínico.',s:()=>'<rect x="-26" y="-6" width="52" height="12" rx="6" fill="#F4F7F8" fill-opacity=".6" stroke="#B4C0C5" stroke-dasharray="3 2"/>'},
 cgra:{n:'Cilindro granuloso',g:'Cilindros',d:'Matriz llena de gránulos (restos de células tubulares). Suele indicar nefropatía (glomerulonefritis).',s:()=>{let s='<rect x="-26" y="-6" width="52" height="12" rx="6" fill="#ECE6D8" stroke="#8F8878"/>';for(let i=0;i<18;i++)s+='<circle cx="'+(-22+i*2.6)+'" cy="'+((i*37%9)-4)+'" r="1" fill="#6F6858"/>';return s}},
 chem:{n:'Cilindro hemático',g:'Cilindros',d:'Contiene hematíes. Sangrado en el túbulo: típico de glomerulonefritis.',s:()=>{let s='<rect x="-26" y="-7" width="52" height="14" rx="7" fill="#F3E1DC" stroke="#A36B60"/>';for(let i=0;i<6;i++)s+=bqE(3.4,3.4,'#E79C8F','#B5665A',-19+i*7.6,(i%2?2:-2));return s}},
 cleu:{n:'Cilindro leucocitario',g:'Cilindros',d:'Contiene leucocitos. Inflamación de origen renal: pielonefritis.',s:()=>{let s='<rect x="-26" y="-7" width="52" height="14" rx="7" fill="#ECEAE6" stroke="#85817A"/>';for(let i=0;i<5;i++)s+=bqE(4.2,4.2,'#DCD7CE','#85817A',-18+i*9,(i%2?1.5:-1.5))+'<circle cx="'+(-18+i*9)+'" cy="'+(i%2?1.5:-1.5)+'" r="1.4" fill="#6B6A9A"/>';return s}},
 ccer:{n:'Cilindro céreo',g:'Cilindros',d:'Muy refringente, rígido, con muescas en los bordes y extremos en ángulo. Enfermedad renal crónica avanzada.',s:()=>'<path d="M-26 -6L22 -6L26 -1L24 0L26 6L-26 6L-24 2L-26 0Z M-8 -6L-6 -3L-4 -6 M10 6L12 3L14 6" fill="#F3EBC9" stroke="#9C8C46" stroke-width="1.4"/>'},
 oxd:{n:'Oxalato cálcico dihidratado',g:'Cristales · orina ácida',d:'Bipirámide en forma de «sobre» (cuadrado con una X). Sin interés clínico.',s:()=>'<rect x="-8" y="-8" width="16" height="16" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.3"/><path d="M-8 -8L8 8M8 -8L-8 8" stroke="#5C6B75" stroke-width="1.1"/>'},
 oxm:{n:'Oxalato cálcico monohidratado',g:'Cristales · orina ácida',d:'Ovalado o en «pesa/reloj de arena», incoloro. Hiperoxaluria, riesgo de litiasis.',s:()=>'<path d="M-9 -4Q-9 -9 -4 -8Q0 -6 4 -8Q9 -9 9 -4L9 4Q9 9 4 8Q0 6 -4 8Q-9 9 -9 4Z" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.3"/>'},
 uric:{n:'Ácido úrico',g:'Cristales · orina ácida',d:'Romboides, rosetas o «limones», de color amarillo-ámbar. Gota y cálculos.',s:()=>'<path d="M-12 0Q0 -10 12 0Q0 10 -12 0Z" fill="#F2C75A" stroke="#B0832A" stroke-width="1.2"/><path d="M-6 -6Q4 -12 14 -2" fill="none" stroke="#B0832A" opacity=".6"/>'},
 amor:{n:'Uratos / fosfatos amorfos',g:'Cristales',d:'Granulado fino sin forma. Uratos amorfos (pardos, orina ácida) o fosfatos amorfos (orina alcalina).',s:()=>{let s='';for(let i=0;i<26;i++)s+='<circle cx="'+((i*53%26)-13)+'" cy="'+((i*29%20)-10)+'" r="'+(0.8+i%3*.4)+'" fill="#8C735E"/>';return s}},
 estr:{n:'Fosfato amónico-magnésico (estruvita)',g:'Cristales · orina alcalina',d:'Prisma incoloro en «tapa de ataúd». Infección por gérmenes ureolíticos.',s:()=>'<path d="M-16 -5L-11 -9L11 -9L16 -5L16 5L11 9L-11 9L-16 5Z M-16 -5L16 -5 M-11 -9L-8 -5 M11 -9L8 -5" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.3"/>'},
 uram:{n:'Urato amónico',g:'Cristales · orina alcalina',d:'Esferas pardo-verdosas, a veces con espículas («manzana espinosa»).',s:()=>{let s=bqE(7,7,'#A88A5A','#6D5630');for(let i=0;i<8;i++){const a=i*Math.PI/4;s+='<path d="M'+(7*Math.cos(a)).toFixed(1)+' '+(7*Math.sin(a)).toFixed(1)+'L'+(12*Math.cos(a+.2)).toFixed(1)+' '+(12*Math.sin(a+.2)).toFixed(1)+'" stroke="#6D5630" stroke-width="1.3"/>'}return s}},
 cist:{n:'Cistina',g:'Cristales relevantes',d:'Placas hexagonales transparentes. Cistinuria: alto riesgo de litiasis.',s:()=>'<path d="M-12 0L-6 -10L6 -10L12 0L6 10L-6 10Z" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.3"/><path d="M-6 0L-3 -5L3 -5L6 0L3 5L-3 5Z" fill="none" stroke="#9AA6AD"/>'},
 col:{n:'Colesterol',g:'Cristales relevantes',d:'Placas rectangulares transparentes con una esquina recortada. Patología linfática.',s:()=>'<path d="M-16 -10L14 -10L14 4L8 10L-16 10Z" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.3"/><path d="M-10 -18L10 -18L10 -12" fill="none" stroke="#9AA6AD"/>'},
 tir:{n:'Tirosina',g:'Cristales relevantes',d:'Agujas finas en haces o rosetas. Daño hepático grave.',s:()=>{let s='';for(let i=0;i<10;i++){const a=i*Math.PI/10;s+='<path d="M'+(-14*Math.cos(a)).toFixed(1)+' '+(-14*Math.sin(a)).toFixed(1)+'L'+(14*Math.cos(a)).toFixed(1)+' '+(14*Math.sin(a)).toFixed(1)+'" stroke="#8C7A3A" stroke-width="1"/>'}return s}},
 leuc:{n:'Leucina',g:'Cristales relevantes',d:'Esferas amarillentas con anillos concéntricos y estrías radiales. Hepatopatía grave.',s:()=>bqE(9,9,'#EED79A','#9C7F2C')+bqE(5.5,5.5,'none','#9C7F2C')+bqE(2.4,2.4,'none','#9C7F2C')},
 msu:{n:'Urato monosódico (sinovial)',g:'Líquido sinovial',d:'Agujas finas, a menudo dentro de neutrófilos durante el ataque. Gota.',s:()=>'<path d="M-14 -3L14 3M-12 4L12 -4M-6 -9L8 9" stroke="#5C6B75" stroke-width="1.4"/>'},
 cppd:{n:'Pirofosfato cálcico (sinovial)',g:'Líquido sinovial',d:'Cristales cortos romboidales o rectangulares. Pseudogota.',s:()=>'<path d="M-10 -3L-4 -6L2 -3L-4 0Z M2 3L8 0L12 3L6 6Z M-6 5L-2 3L0 7L-4 9Z" fill="#F7FAFB" stroke="#5C6B75" stroke-width="1.2"/>'},
 charc:{n:'Charcot-Leyden (heces)',g:'Heces',d:'Cristales bipiramidales alargados como «aguja de brújula». Parasitosis intestinal.',s:()=>'<path d="M-16 0L0 -4L16 0L0 4Z" fill="#F4F0E2" stroke="#7E7556" stroke-width="1.2"/><path d="M-4 9L0 8L4 9L0 10Z" fill="none" stroke="#7E7556"/>'},
 fibm:{n:'Fibra muscular mal digerida (heces)',g:'Heces',d:'Fragmento rectangular amarillento con estrías transversales y bordes rectos: creatorrea.',s:()=>{let s='<rect x="-16" y="-8" width="32" height="16" fill="#F2DFA4" stroke="#9C8236"/>';for(let i=-12;i<=12;i+=4)s+='<path d="M'+i+' -8V8" stroke="#9C8236" stroke-width=".8"/>';return s}},
 gras:{n:'Grasa neutra (Sudán III)',g:'Heces',d:'Gotitas rojo-naranja al teñir con Sudán III. Muchas por campo = esteatorrea.',s:()=>bqE(5,5,'#F08A4B','#B5562A',-6,-3)+bqE(3.4,3.4,'#F08A4B','#B5562A',6,2)+bqE(2.4,2.4,'#F08A4B','#B5562A',-1,7)}};
const BQ_MICS=40;
function bqField(items,obj,zones){const sc=obj===10?.42:1;let s='<svg class="bqfield" viewBox="-160 -160 320 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Campo de microscopio"><defs><clipPath id="bqclp"><circle r="150"/></clipPath><radialGradient id="bqfg"><stop offset="0" stop-color="#FFFDF5"/><stop offset="1" stop-color="#E9E4D4"/></radialGradient></defs><circle r="152" fill="#222"/><g clip-path="url(#bqclp)"><circle r="150" fill="url(#bqfg)"/>';
  items.forEach((it,i)=>{const m=BQ_MIC[it.k];if(!m)return;const x=it.x*120,y=it.y*120,r=it.r||0,k=(it.s||1)*sc*2.2;s+='<g transform="translate('+x.toFixed(1)+' '+y.toFixed(1)+') rotate('+r+') scale('+k.toFixed(2)+')">'+m.s()+'</g>';
    if(zones)s+='<circle data-z="'+i+'" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+Math.max(16,30*sc*(it.s||1)*1.2).toFixed(1)+'"/>'});
  return s+'</g><text x="140" y="148" text-anchor="end" font-size="11" fill="#eee" font-weight="700">'+obj+'x</text></svg>'}
IW.micro=(ch,o)=>{const w=el('div','bqmic tapw');let obj=ch.obj||40;const A=new Set(ch.a.map(String));const sel=new Set();let lk=false;
  const fig=el('div','bqmf');const tg=el('div','bqobj');w.append(tg,fig);
  const draw=()=>{fig.innerHTML=bqField(ch.items,obj,true);tg.innerHTML='';[10,40].forEach(v=>{const b=el('button','tbtn'+(obj===v?' on':''),'Objetivo '+v+'x');b.type='button';b.onclick=()=>{obj=v;draw()};tg.append(b)});
    fig.querySelectorAll('[data-z]').forEach(z=>{z.classList.add('tz');z.classList.toggle('on',sel.has(z.dataset.z));z.onclick=()=>{if(lk)return;const id=z.dataset.z;if(ch.multi){sel.has(id)?sel.delete(id):sel.add(id)}else{const h=sel.has(id);sel.clear();if(!h)sel.add(id)}draw();o.on&&o.on()}})};
  draw();
  return{el:w,note:(ch.multi?'Toca todos los elementos que correspondan (otra vez para quitar).':'Toca el elemento correcto.')+' Puedes cambiar de objetivo.',need:'Toca un elemento del campo.',okMsg:'¡Bien identificado!',
   filled:()=>sel.size>0,grade(){const ok=sel.size===A.size&&[...sel].every(z=>A.has(z));return{f:ok?1:0,msg:ok?'':'No es eso. '+(ch.e||'Fíjate en la forma y el tamaño.')}},
   mark(){fig.querySelectorAll('[data-z]').forEach(z=>{const id=z.dataset.z;z.classList.toggle('good',sel.has(id)&&A.has(id));z.classList.toggle('bad',sel.has(id)&&!A.has(id))})},
   reveal(){sel.clear();A.forEach(x=>sel.add(x));draw();fig.querySelectorAll('[data-z]').forEach(z=>z.classList.toggle('good',A.has(z.dataset.z)))},lock(){lk=true;w.classList.add('lk')}}};
LW.micro=(b,o)=>{const gs=[...new Set(Object.values(BQ_MIC).map(m=>m.g))].filter(g=>!o.g||o.g.some(x=>g.indexOf(x)===0));let g=gs[0],k=null;
  const tabs=el('div','bqobj');const grid=el('div','bqatl');const det=el('div','bqatd');b.append(tabs,grid,det);
  const draw=()=>{tabs.innerHTML='';gs.forEach(x=>{const t=el('button','tbtn'+(x===g?' on':''),x);t.type='button';t.onclick=()=>{g=x;k=null;draw()};tabs.append(t)});
    grid.innerHTML='';Object.keys(BQ_MIC).filter(x=>BQ_MIC[x].g===g).forEach(x=>{const m=BQ_MIC[x];const c=el('button','bqatc'+(x===k?' on':''),'<svg viewBox="-30 -30 60 60" xmlns="http://www.w3.org/2000/svg"><circle r="29" fill="#FFFDF5" stroke="#ccc"/><g transform="scale(1.1)">'+m.s()+'</g></svg><small>'+m.n+'</small>');c.type='button';c.onclick=()=>{k=x;draw()};grid.append(c)});
    det.innerHTML=k?'<b>'+BQ_MIC[k].n+'.</b> '+BQ_MIC[k].d:'<span class="note">Toca una imagen para ver cómo se reconoce.</span>'};draw()};
/* ---------- Espectrofotómetro virtual ---------- */
const bqWl=l=>{const c=[[380,'#7A3CA8'],[440,'#3048D8'],[490,'#2AA6C9'],[520,'#33B24A'],[570,'#D6CF2A'],[590,'#F0A12A'],[620,'#E8532A'],[700,'#B5221E']];if(l<380)return'#8A5CC0';for(let i=1;i<c.length;i++)if(l<=c[i][0])return c[i][1];return'#B5221E'};
function bqSpec(root,S,task){const st={on:false,warm:0,l:340,mode:'A',cub:null,zero:null,log:[],reads:{},dil:1};
  const scr=el('div','bqscr');const ctl=el('div','bqctl');const lg=el('ol','bqlog');root.append(scr,ctl,lg);
  const absOf=c=>{if(c==='blanco')return S.reag;const base=c==='patron'?S.Ap:S.As/st.dil;const band=Math.exp(-Math.pow((st.l-S.lmax)/45,2));return S.reag+base*band};
  const L=t=>{st.log.push(t);lg.innerHTML=st.log.slice(-6).map(x=>'<li>'+x+'</li>').join('')};
  const read=()=>{if(!st.on)return'— — —';if(!st.cub)return'Sin cubeta';let a=absOf(st.cub);if(st.zero!=null)a-=st.zero;if(st.warm<20)a+=0.06*Math.sin(Date.now()/300)+0.07;
    if(st.mode==='T'){const t=100*Math.pow(10,-a);return(Math.max(0,Math.min(999,t))).toFixed(1).replace('.',',')+' %T'}
    if(a>2.5)return'OVER (A > 2,5)';return a.toFixed(3).replace('.',',')+' A'};
  const draw=()=>{scr.innerHTML='<div class="bqdisp'+(st.on?'':' off')+'">'+read()+'</div><div class="bqinfo">'+(st.on?(st.warm<20?'🔥 Lámpara calentando: '+st.warm+'/20 min':'✅ Lámpara estable')+' · λ = <b style="color:'+bqWl(st.l)+'">'+st.l+' nm</b> · modo '+(st.mode==='A'?'absorbancia':'transmitancia')+' · '+(st.zero!=null?'blanco hecho':'<span class="bad">sin blanco</span>'):'Apagado')+'</div><div class="bqcuv">Cubeta en el equipo: <b>'+(st.cub?({blanco:'Blanco',patron:'Patrón',muestra:'Muestra'+(st.dil>1?' (diluida 1:'+st.dil+')':'')}[st.cub]):'ninguna')+'</b></div>';
    ctl.innerHTML='';const B=(t,f,dis)=>{const b=el('button','tbtn',t);b.type='button';b.disabled=!!dis;b.onclick=()=>{f();draw()};ctl.append(b);return b};
    B(st.on?'⏻ Apagar':'⏻ Encender',()=>{st.on=!st.on;if(st.on){st.warm=0;L('Encendido. La lámpara necesita ~20 min.')}else{st.zero=null;L('Apagado.')}});
    B('⏩ Esperar 10 min',()=>{st.warm=Math.min(20,st.warm+10);L('Esperas 10 min ('+st.warm+'/20).')},!st.on||st.warm>=20);
    const lw=el('label','bqlam','λ <input type="range" min="340" max="700" step="5" value="'+st.l+'">');const r=lw.querySelector('input');r.oninput=()=>{st.l=+r.value;st.zero=null;draw()};r.onchange=()=>L('Longitud de onda: '+st.l+' nm (hay que repetir el blanco).');r.disabled=!st.on;ctl.append(lw);
    B('Modo: '+(st.mode==='A'?'A → %T':'%T → A'),()=>{st.mode=st.mode==='A'?'T':'A';L('Modo '+(st.mode==='A'?'absorbancia':'transmitancia')+'.')},!st.on);
    ['blanco','patron','muestra'].forEach(c=>B('🧪 '+({blanco:'Blanco',patron:'Patrón',muestra:'Muestra'}[c]),()=>{st.cub=c;L('Colocas la cubeta: '+({blanco:'blanco',patron:'patrón',muestra:'muestra'}[c])+'.')},!st.on));
    B('0️⃣ Ajustar blanco',()=>{if(st.cub!=='blanco'){L('⚠️ Para ajustar el cero debe estar el blanco en la cubeta.');return}st.zero=absOf('blanco');L('Blanco ajustado a A = 0 en '+st.l+' nm.')},!st.on);
    B('📖 Leer',()=>{if(!st.cub)return;const t=read();st.reads[st.cub]={t,l:st.l,z:st.zero!=null,w:st.warm>=20,dil:st.dil};L('Lectura '+({blanco:'blanco',patron:'patrón',muestra:'muestra'}[st.cub])+': '+t+(st.warm<20?' (¡inestable!)':''))},!st.on);
    if(S.dil)B('💧 Diluir muestra 1:2',()=>{st.dil*=2;L('Muestra diluida 1:'+st.dil+' (recuerda multiplicar por '+st.dil+').')},!st.on)};
  draw();const tk=setInterval(()=>{if(!document.body.contains(root)){clearInterval(tk);return}if(st.on&&st.warm<20&&st.cub)draw()},700);
  L('Equipo listo. Muestra: '+S.n+'.');return st}
LW.espec=(b,o)=>{const S=Object.assign({n:'Disolución roja (absorbe verde-azul)',lmax:505,Cp:100,Ap:.47,As:.52,reag:.1},o);b.append(el('p','note','Muestra: <b>'+S.n+'</b>. Patrón: '+String(S.Cp).replace('.',',')+' '+(S.u||'mg/dL')+'. Prueba qué pasa si no esperas, si no haces el blanco o si eliges mal la λ.'));bqSpec(b,S)};
IW.espec=(ch,o)=>{const S=ch.s;const w=el('div','bqesp');let lk=false;const st=bqSpec(w,S,true);
  const r=el('label','nrow');r.append(el('span','nl','Concentración de la muestra'));const i=el('input','fin');i.inputMode='decimal';i.placeholder='?';i.oninput=()=>{i.classList.remove('bad','good');o.on&&o.on()};r.append(i,el('span','nu',S.u||'mg/dL'));w.append(r);
  const ans=S.Cp*S.As/S.Ap;
  return{el:w,note:'Haz el procedimiento completo en el equipo (encender, esperar, λ, blanco, patrón, muestra) y escribe la concentración.',need:'Escribe la concentración.',okMsg:'¡Procedimiento y resultado correctos!',
   filled:()=>i.value.trim()!=='',
   grade(){const p=[],m=st.reads.muestra,q=st.reads.patron;if(!q)p.push('no leíste el patrón');if(!m)p.push('no leíste la muestra');
     [m,q].forEach(x=>{if(!x)return;if(!x.w)p.push('leíste con la lámpara sin calentar');if(!x.z)p.push('leíste sin hacer el blanco');if(Math.abs(x.l-S.lmax)>20)p.push('la λ no era la de máxima absorción ('+S.lmax+' nm)')});
     const ok=numOk(numV(i.value),ans,Math.max(0.6,ans*0.02));if(!ok)p.push('la concentración no es correcta (C = A<sub>muestra</sub> × C<sub>patrón</sub> / A<sub>patrón</sub>'+(S.dil?' × factor de dilución':'')+')');
     const u=[...new Set(p)];return{f:u.length?0:1,msg:u.length?'Revisa: '+u.join('; ')+'.':''}},
   mark(g){i.classList.toggle('good',g.f>=1);i.classList.toggle('bad',g.f<1)},
   reveal(){i.value=fmtC(Math.round(ans*10)/10);i.classList.add('rev')},lock(){lk=true;i.disabled=true;w.classList.add('lk')}}};
/* ---------- Curva de calibrado ---------- */
LW.calib=(b,o)=>{const P=o.pts||[[0,0],[50,.115],[100,.232],[150,.348],[200,.461],[300,.62],[400,.71]],lin=o.lin||200,u=o.u||'mg/dL';
  const lp=P.filter(p=>p[0]<=lin);const n=lp.length,sx=lp.reduce((a,p)=>a+p[0],0),sy=lp.reduce((a,p)=>a+p[1],0),sxx=lp.reduce((a,p)=>a+p[0]*p[0],0),sxy=lp.reduce((a,p)=>a+p[0]*p[1],0);
  const m=(n*sxy-sx*sy)/(n*sxx-sx*sx),q=(sy-m*sx)/n;let A=o.a||.3;
  const fig=el('div','chfig');const ro=el('p','bqtime');const sl=el('input','bqsl');sl.type='range';sl.min=0;sl.max=.8;sl.step=.005;sl.value=A;b.append(fig,ro,sl,el('p','note','Mueve la absorbancia de la muestra problema. Recta = ajuste por mínimos cuadrados del tramo lineal; la zona gris está fuera de linealidad.'));
  const xm=P[P.length-1][0]*1.05,W=320,H=210,L=40,R=10,T=10,B=28,X=v=>L+(W-L-R)*v/xm,Y=v=>T+(H-T-B)*(1-v/.8);
  const draw=()=>{const c=(A-q)/m,out=c>lin;let s='<svg class="pls" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg"><rect x="'+X(lin)+'" y="'+T+'" width="'+(X(xm)-X(lin))+'" height="'+(H-T-B)+'" fill="var(--grid)"/>';
    [0,.2,.4,.6,.8].forEach(v=>s+='<line class="chg" x1="'+L+'" x2="'+(W-R)+'" y1="'+Y(v)+'" y2="'+Y(v)+'"/><text class="chk" x="'+(L-4)+'" y="'+(Y(v)+4)+'" text-anchor="end">'+String(v).replace('.',',')+'</text>');
    P.forEach(p=>s+='<text class="chk" x="'+X(p[0])+'" y="'+(H-12)+'" text-anchor="middle" style="font-size:9px">'+p[0]+'</text>');
    s+='<line x1="'+X(0)+'" y1="'+Y(q)+'" x2="'+X(lin)+'" y2="'+Y(q+m*lin)+'" stroke="var(--curve)" stroke-width="2"/>';
    P.forEach(p=>s+='<circle cx="'+X(p[0])+'" cy="'+Y(p[1])+'" r="3.6" fill="'+(p[0]>lin?'var(--bad)':'var(--curve)')+'"/>');
    const cx=Math.min(c,xm);s+='<line x1="'+L+'" x2="'+X(Math.max(0,cx))+'" y1="'+Y(A)+'" y2="'+Y(A)+'" stroke="var(--exe)" stroke-dasharray="4 3"/><line x1="'+X(Math.max(0,cx))+'" x2="'+X(Math.max(0,cx))+'" y1="'+Y(A)+'" y2="'+(H-B)+'" stroke="var(--exe)" stroke-dasharray="4 3"/><circle cx="'+X(Math.max(0,cx))+'" cy="'+Y(A)+'" r="4.5" fill="var(--exe)"/>';
    s+='<path class="chax" fill="none" d="M'+L+' '+T+'V'+(H-B)+'H'+(W-R)+'"/><text class="chk" x="'+(W-R)+'" y="'+(H-1)+'" text-anchor="end">Concentración ('+u+')</text><text class="chk" x="'+(L+3)+'" y="'+(T+9)+'">A</text></svg>';
    fig.innerHTML=s;ro.innerHTML='A<sub>muestra</sub> = <b>'+A.toFixed(3).replace('.',',')+'</b> → C = (A − b)/m = <b>'+(c<0?'—':c.toFixed(1).replace('.',','))+' '+u+'</b>'+(out?' <span class="bad">⚠ fuera del intervalo lineal: diluye la muestra y multiplica por el factor.</span>':'')+'<br><small>Recta: A = '+m.toFixed(5).replace('.',',')+'·C + '+q.toFixed(4).replace('.',',')+'</small>'};
  sl.oninput=()=>{A=+sl.value;draw()};draw()};
