#!/usr/bin/env python3
"""Auditoría completa de NotPull en el navegador.

Uso:
  python3 tools/auditar.py                   # solo lo que cambió respecto de origin/main (segundos)
  python3 tools/auditar.py --todo            # todos los bloques (~6 min)
  python3 tools/auditar.py calculo-ep p2-ef  # solo esos bloques
  python3 tools/auditar.py --webkit …        # motor de Safari (instalar: python3 -m playwright install webkit)

Sin argumentos: revisa completos los bloques cuyo JSON cambió y, si cambió index.html, una
muestra de pocos temas que juntos cubren cada tipo de pregunta y herramienta, y las pruebas
de arrastre.

Qué hace, por cada tema de cada bloque publicado:
  · abre el tema, construye todas las preguntas y soluciones y las pasa por MathJax
    (errores de fórmulas, fórmulas de más de 340 px, scroll horizontal, errores de JS);
  · resuelve cada pregunta interactiva desde su JSON (expr, tap, cols, sql, espec con
    clics o texto reales; el resto con reveal()) y comprueba que quede correcta (f = 1);
  · revisa opciones repetidas o vacías y que cada id de los simulacros exista;
  · arranca cada simulacro y comprueba que sume 20 pts;
  · arrastra de verdad las manijas de vecdraw, tlc y las herramientas de vectores.
Sale con código 1 si hay errores. Las soluciones que solo se desplazan (> 340 px dentro de
la solución) son avisos.

Necesita Playwright con Chromium (en la sesión ya está en /opt/pw-browsers). Las librerías de
jsDelivr se bajan una vez a ~/.cache/notpull-cdn y se sirven desde ahí; el resto de la red se corta.
"""
import asyncio,json,os,sys,subprocess,collections
from playwright.async_api import async_playwright
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDN=os.path.expanduser('~/.cache/notpull-cdn')
URLS=['npm/jszip@3.10.1/dist/jszip.min.js','npm/mathjax@3.2.2/es5/tex-svg.js','npm/sortablejs@1.15.6/Sortable.min.js','npm/sql.js@1.10.3/dist/sql-wasm.js','npm/sql.js@1.10.3/dist/sql-wasm.wasm']
def bajar():
    os.makedirs(CDN,exist_ok=True)
    for u in URLS:
        f=os.path.join(CDN,os.path.basename(u))
        if not os.path.exists(f):subprocess.run(['curl','-sSfL','-o',f,'https://cdn.jsdelivr.net/'+u],check=True)
def patched():
    s=open(os.path.join(REPO,'index.html'),encoding='utf-8').read()
    reps=[('NOVS=await novP;','NOVS=await novP;window.__X={get COURSES(){return COURSES},openCourse,goTopic,startSim,get T(){return T},get C(){return C},get IW(){return IW},get st(){return st}};'),
          ('function iwPractice(ch,box,fb,qi,pre,cb,e,key){const w=IW[ch.t](ch,{key,pre});','function iwPractice(ch,box,fb,qi,pre,cb,e,key){const w=IW[ch.t](ch,{key,pre});box.__w=w;box.__ch=ch;'),
          ('const lockSol=()=>!e.draw&&hasChk','const lockSol=()=>false&&!e.draw&&hasChk')]
    for a,b in reps:
        assert s.count(a)==1,a
        s=s.replace(a,b)
    return s
LIBS={'tex-svg.js':'application/javascript','Sortable.min.js':'application/javascript','jszip.min.js':'application/javascript','sql-wasm.js':'application/javascript','sql-wasm.wasm':'application/wasm'}
async def setup(page,base):
    html=patched()
    async def h(route):
        u=route.request.url
        if 'cdn.jsdelivr.net' in u:
            n=u.split('?')[0].rsplit('/',1)[-1]
            if n in LIBS: return await route.fulfill(path=os.path.join(CDN,n),content_type=LIBS[n])
            return await route.abort()
        if u.startswith(base):
            p=u[len(base):].split('?')[0].split('#')[0] or 'index.html'
            if p=='sw.js': return await route.fulfill(status=404,body='')
            if p=='index.html': return await route.fulfill(body=html,content_type='text/html; charset=utf-8')
            f=os.path.join(REPO,p)
            if os.path.isfile(f): return await route.fulfill(path=f)
            return await route.fulfill(status=404,body='')
        await route.abort()
    await page.route('**/*',h)

TOPIC_JS=r"""async (i)=>{
  const X=window.__X, R={i, merr:[], wide:[], iw:[], ex:0, opt:[], err:[]};
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  X.goTopic(i);const main=document.getElementById('main')||document.querySelector('main');
  await sleep(50);
  const t=X.T[i];R.name=t.name;R.id=t.id;
  for(const c of main.querySelectorAll('article.ex')){R.ex++;
    try{const bv=c.querySelector(':scope > .acts .bv');const vv=c.querySelector(':scope > .ver');if(bv&&vv&&vv.hidden)bv.click();
        const bs=c.querySelector(':scope > .acts .bs');const ss=c.querySelector(':scope > .sol');if(bs&&ss&&ss.hidden)bs.click();}catch(e){R.err.push(c.id+': click '+e)}}
  main.querySelectorAll('details').forEach(d=>d.open=true);
  main.querySelectorAll('[hidden]').forEach(n=>{if(n.closest('article.ex'))n.hidden=false});
  try{await MathJax.typesetPromise([main])}catch(e){R.err.push('mj '+e)}
  await sleep(150);
  main.querySelectorAll('mjx-merror').forEach(m=>{const a=m.closest('article.ex');R.merr.push((a?a.id:'teo')+': '+(m.getAttribute('data-mjx-error')||m.textContent).slice(0,120))});
  main.querySelectorAll('mjx-container:not([display="true"])').forEach(m=>{const w=m.getBoundingClientRect().width;if(w>340&&!m.closest('.lw,svg,table,.tbl,pre')){const a=m.closest('article.ex');const pc=m.closest('.opt')?'opción':m.closest('.sol')?'solución':m.closest('.enun')?'enunciado':m.closest('.chk')?'pregunta':m.closest('.hint')?'pista':'otro';R.wide.push((a?a.id:'teo')+' '+pc+': '+Math.round(w)+'px')}});
  R.sw=document.documentElement.scrollWidth;
  for(const box of main.querySelectorAll('.ver > .chk')){const w=box.__w,ch=box.__ch;if(!w)continue;const ex=box.closest('article.ex').id;
    try{box.hidden=false;
      if(ch.t==='expr'){const fs=ch.f||[{a:ch.a,mode:ch.mode,c:ch.c}];box.querySelectorAll('.mxin').forEach((inp,k)=>{const f=fs[k]||{};inp.value=String(f.a)+((f.mode==='anti'||f.c)?'+C':'');inp.dispatchEvent(new Event('input',{bubbles:true}))})}
      else if(ch.t==='tap'){for(const id of ch.a){const z=w.el.querySelector('[data-z="'+id+'"]');if(!z)throw new Error('zona '+id+' no existe');z.dispatchEvent(new MouseEvent('click',{bubbles:true}))}}
      else if(ch.t==='cols'){const bs=w.el.querySelectorAll('.alcol');for(const k of ch.a){if(!bs[k])throw new Error('columna '+k+' no existe');bs[k].click()}}
      else if(ch.t==='sql'){const ta=w.el.querySelector('textarea');ta.value=ch.a;ta.dispatchEvent(new Event('input',{bubbles:true}))}
      else if(ch.t==='espec'){const S=ch.s;const B=t=>{const b=[...w.el.querySelectorAll('button')].find(x=>x.textContent.includes(t)&&!x.disabled);if(!b)throw new Error('botón '+t);b.click()};
        B('Encender');B('Esperar');B('Esperar');const r=w.el.querySelector('input[type=range]');r.value=Math.round(S.lmax/5)*5;r.dispatchEvent(new Event('input'));r.dispatchEvent(new Event('change'));
        B('Blanco');B('Ajustar blanco');B('Patrón');B('Leer');B('Muestra');B('Leer');let dil=1;
        while(/OVER/.test(w.el.querySelector('.bqdisp').textContent)&&dil<64){B('Diluir');dil*=2;B('Leer')}
        const fin=w.el.querySelector('input.fin');fin.value=String(S.Cp*S.As/S.Ap).replace('.',',');fin.dispatchEvent(new Event('input'))}
      else w.reveal();let g=w.agrade?await w.agrade():w.grade();
      if(!g||!(g.f>=0.999))R.iw.push(ex+' ['+ch.t+'] f='+(g&&g.f)+' '+String(g&&g.msg||'').replace(/<[^>]+>/g,'').slice(0,140))}
    catch(e){R.iw.push(ex+' ['+(ch&&ch.t)+'] EXC '+String(e).slice(0,160))}}
  // opciones: correctas duplicadas o vacías
  for(const e of t.ex)for(const ch of e.checks){if(ch.t)continue;const o=ch.o||[];
    if(o.length<2)R.opt.push(e.id+': menos de 2 opciones');
    const norm=o.map(s=>String(s).replace(/\s+/g,' ').trim());if(new Set(norm).size!==norm.length)R.opt.push(e.id+': opciones repetidas');
    if(norm.some(s=>!s))R.opt.push(e.id+': opción vacía')}
  return R}
"""

DRAG=[("tlc","check"),("vecdraw","check"),("tl","tool"),("det","tool"),("vec","tool"),("recta","tool"),("pdef","tool"),("rcirc","tool")]
BASE='http://notpull.test/'
async def main(engine,only,drag=True):
  res=[];probs=collections.defaultdict(list)
  async with async_playwright() as p:
    b=await getattr(p,engine).launch()
    pg=await b.new_page(viewport={'width':390,'height':844})
    perr=[];pg.on('pageerror',lambda e:perr.append(str(e)[:200]))
    pg.on('console',lambda m:perr.append('console: '+m.text[:200]) if m.type=='error' and 'ERR_FAILED' not in m.text and 'Failed to load resource' not in m.text and 'NaN' not in m.text else None)
    await setup(pg,BASE);await pg.goto(BASE+'index.html')
    await pg.wait_for_function('window.__X&&window.__X.COURSES&&window.MathJax&&MathJax.typesetPromise',timeout=60000)
    await pg.wait_for_timeout(2500);await pg.evaluate("document.getElementById('ovl')&&(document.getElementById('ovl').innerHTML='')")
    ids=await pg.evaluate('__X.COURSES.filter(c=>!c.soon&&c.topics.length).map(c=>c.id)')
    for cid in ids:
      if only is not None and cid not in only:continue
      n=await pg.evaluate('id=>{__X.openCourse(id);return __X.T.length}',cid)
      sel=only.get(cid) if only is not None else None
      for i in range(n):
        if sel is not None and i not in sel:continue
        perr.clear()
        try:r=await asyncio.wait_for(pg.evaluate(TOPIC_JS,i),120)
        except Exception as ex:r={'i':i,'err':['TIMEOUT/EXC '+str(ex)[:200]]}
        r['course']=cid;r['perr']=list(perr);res.append(r)
        print('·',cid,i,r.get('name','')[:60],flush=True)
      perr.clear()
      s=await pg.evaluate("""async id=>{const C=__X.C;const pool=new Set();C.topics.forEach(t=>t.ex.forEach(e=>pool.add(e.id)));(C.simEx||[]).forEach(e=>pool.add(e.id));
          const miss=[];(C.sim&&C.sim.slots||[]).forEach(s=>(s.pool||[]).forEach(id=>{if(!pool.has(id))miss.push(id)}));if(miss.length)return 'ids que no existen: '+miss.join(',');
          if(!C.sim||!C.sim.slots||!C.sim.slots.length)return 'ok';__X.startSim(true);await new Promise(r=>setTimeout(r,400));
          const qs=document.querySelectorAll('#simmain .q').length,sum=C.sim.slots.reduce((a,s)=>a+s.pts,0);
          const r=qs!==C.sim.slots.length?'el simulacro dibujó '+qs+' de '+C.sim.slots.length+' preguntas':Math.abs(sum-20)>0.01?'el simulacro suma '+sum+' pts':document.querySelector('#simmain mjx-merror')?'error de MathJax en el simulacro':'ok';
          __X.openCourse(id);return r}""",cid)
      if s!='ok':probs['simulacro'].append(cid+': '+s)
      for x in perr:probs['errores JS'].append(cid+' simulacro: '+x)
    # arrastres
    await pg.evaluate("document.getElementById('ovl').innerHTML=''")
    for t,kind in (DRAG if drag else []):
      loc=await pg.evaluate("""([t,kind])=>{for(const c of __X.COURSES){if(c.soon)continue;for(const [i,tp] of c.topics.entries()){
         if(kind==='tool'&&(tp.tools||[]).some(w=>w.w===t))return{c:c.id,i};
         if(kind==='check')for(const e of tp.ex)for(const [q,ch] of e.checks.entries())if(ch.t===t)return{c:c.id,i,e:e.id,q}}}return null}""",[t,kind])
      if not loc:continue
      await pg.evaluate("x=>{__X.openCourse(x.c);__X.goTopic(x.i);document.querySelectorAll('#main details').forEach(d=>d.open=true);if(x.e)document.getElementById(x.e).querySelector('.bv').click()}",loc)
      await pg.wait_for_timeout(900)
      root=('#'+loc['e']+' .ver') if kind=='check' else ('.lw[data-w="'+t+'"]')
      sel=root+' [data-h], '+root+' .lwh'
      h=pg.locator(sel).first
      if await h.count()==0:probs['arrastre'].append(t+': sin manija');continue
      await h.evaluate("n=>n.scrollIntoView({block:'center'})");await pg.wait_for_timeout(200);bb=await h.bounding_box()
      sx,sy=bb['x']+bb['width']/2,bb['y']+bb['height']/2
      await pg.mouse.move(sx,sy);await pg.mouse.down()
      for k in range(1,16):await pg.mouse.move(sx-4*k,sy+5*k)
      await pg.mouse.up();await pg.wait_for_timeout(200)
      bb2=await pg.locator(sel).first.bounding_box()
      d=((bb2['x']-bb['x'])**2+(bb2['y']-bb['y'])**2)**.5 if bb2 else 0
      if d<40:probs['arrastre'].append(t+' ('+loc['c']+'): la manija se movió '+str(round(d))+' px en un arrastre de 96 px')
    await b.close()
  for r in res:
    k=r['course']+' '+str(r.get('i'))
    for x in r.get('merr',[]):probs['MathJax'].append(r['course']+' '+x)
    for x in r.get('iw',[]):probs['pregunta interactiva no queda resuelta'].append(r['course']+' '+x)
    for x in r.get('opt',[]):probs['opciones'].append(r['course']+' '+x)
    for x in r.get('err',[]):probs['errores al construir'].append(k+' '+x)
    for x in r.get('perr',[]):probs['errores JS'].append(k+' '+x)
    if r.get('sw',0)>390:probs['scroll horizontal'].append(k+' ancho '+str(r['sw']))
    for x in r.get('wide',[]):
      (probs['fórmula ancha en pregunta u opción'] if ('opción' in x or 'enunciado' in x or 'pregunta' in x) else probs['aviso: fórmula ancha en solución (se desplaza)']).append(r['course']+' '+x)
  print('\n'+engine+':',len(res),'temas ·',sum(r.get('ex',0) for r in res),'ejercicios')
  nerr=0
  for k,v in probs.items():
    print('\n==',k,len(v))
    for x in v[:40]:print('  ',x)
    if not k.startswith('aviso'):nerr+=len(v)
  print('\n'+('✅ Sin errores' if not nerr else '❌ '+str(nerr)+' errores'))
  return nerr
def cambios():
  """Archivos cambiados respecto de origin/main (commits sin subir + cambios sin commit)."""
  def g(*a):
    r=subprocess.run(['git','-C',REPO]+list(a),capture_output=True,text=True);return r.stdout.split()
  subprocess.run(['git','-C',REPO,'fetch','-q','origin','main'],capture_output=True)
  return set(g('diff','--name-only','origin/main')+g('ls-files','--others','--exclude-standard'))
def muestra():
  """Pocos temas que juntos cubren cada tipo de pregunta y herramienta ."""
  idx=json.load(open(os.path.join(REPO,'cursos','indice.json')))['cursos']
  temas=[];sel=collections.defaultdict(set)
  for cid in idx:
    d=json.load(open(os.path.join(REPO,'cursos',cid+'.json')))
    if d.get('soon') or not d['topics']:continue
    for i,t in enumerate(d['topics']):
      k={'c:'+(ch.get('t') or 'opt') for e in t['ex'] for ch in e['checks']}|{'w:'+w.get('w','') for w in t.get('tools',[])}
      temas.append((cid,i,k))
  falta=set().union(*(k for _,_,k in temas))
  while falta:
    cid,i,k=max(temas,key=lambda x:len(x[2]&falta));sel[cid].add(i);falta-=k
  return dict(sel)
if __name__=='__main__':
  a=sys.argv[1:];eng='webkit' if '--webkit' in a else 'chromium';ids=[x for x in a if not x.startswith('--')]
  bajar();drag=True
  if ids:only={c:None for c in ids}
  elif '--todo' in a:only=None
  else:
    ch=cambios();only={}
    bl={os.path.basename(f)[:-5] for f in ch if f.startswith('cursos/') and f.endswith('.json') and not f.endswith(('indice.json','novedades.json'))}
    app='index.html' in ch
    if app:only.update(muestra())
    for c in bl:only[c]=None
    drag=app
    if not only:print('No hay cambios respecto de origin/main. Para revisar todo: --todo');sys.exit(0)
    print('Revisando',('la app (muestra de cada tipo de pregunta) y ' if app else '')+(', '.join(sorted(bl)) or 'ningún bloque'),flush=True)
  sys.exit(1 if asyncio.run(main(eng,only,drag)) else 0)
