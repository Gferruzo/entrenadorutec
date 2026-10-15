#!/usr/bin/env python3
"""Corre la solución modelo (último <pre> de los pasos) de cada ejercicio de código contra sus
pruebas, igual que la app: Python con el mismo arnés de py-worker.js y C++ con g++ -std=c++17
(como godbolt). También avisa si la plantilla `start` ya pasa las pruebas.
Uso: python3 tools/auditar_codigo.py   (sale con 1 si algo falla)
"""
import json,glob,re,html,subprocess,os,sys,tempfile
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H=json.loads(re.search(r'const HARNESS = (".*?");\n',open(REPO+'/py-worker.js').read(),re.S).group(1))
def norm(s):return '\n'.join(l.rstrip() for l in str(s).replace('\r','').split('\n')).rstrip('\n')
def ncmp(s):
  import unicodedata;s=unicodedata.normalize('NFD',str(s));s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+','',s.lower())
def hasall(out,has):
  o=ncmp(out);p=0
  for h in has:
    k=o.find(ncmp(h),p)
    if k<0:return False
    p=k+len(ncmp(h))
  return True
def model(e):
  pres=re.findall(r'<pre class="(py|cpp)"><code>(.*?)</code></pre>',' '.join(e['steps']),re.S)
  return html.unescape(pres[-1][1]) if pres else None
def runpy(code,tests,files):
  src=H+'\nimport json,sys\nprint("@@R@@"+run_all(sys.argv[1],sys.argv[2],sys.argv[3]))'
  with tempfile.TemporaryDirectory() as d:
    f=os.path.join(d,'h.py');open(f,'w').write(src)
    r=subprocess.run([sys.executable,f,code,json.dumps(tests or [{}]),json.dumps(files or {})],capture_output=True,text=True,timeout=30,cwd=d)
  return json.loads(r.stdout.split('@@R@@')[-1])
MARK=lambda i:'@@PRUEBA_'+str(i)+'@@'
def cpp(src,stdin=''):
  with tempfile.TemporaryDirectory() as d:
    f=os.path.join(d,'a.cpp');open(f,'w').write(src)
    c=subprocess.run(['g++','-std=c++17','-O1','-o',d+'/a',f],capture_output=True,text=True)
    if c.returncode:return {'ce':c.stderr[:400]}
    try:r=subprocess.run([d+'/a'],input=stdin,capture_output=True,text=True,timeout=10)
    except subprocess.TimeoutExpired:return {'out':'','err':'timeout'}
    return {'out':r.stdout,'err':None if r.returncode==0 else 'code %d'%r.returncode}
def runcpp(code,tests):
  tests=tests or [{}]
  if any(t.get('main') for t in tests):
    h=code+'\n\n#include <iostream>\nint main(){\n'+''.join('    std::cout<<"\\n'+MARK(i)+'"<<std::endl;\n    { using namespace std;\n'+t['main']+'\n    }\n    std::cout<<std::flush;\n' for i,t in enumerate(tests))+'    std::cout<<"\\n'+MARK('FIN')+'"<<std::endl;\n    return 0;\n}\n'
    m=cpp(h)
    if 'ce' in m:return [{'ok':False,'err':'CE '+m['ce']}]*len(tests)
    res=[];out=m['out']
    for i,t in enumerate(tests):
      a=out.find(MARK(i))
      if a<0:res.append({'ok':False,'err':'no llegó'});continue
      s=a+len(MARK(i));nx=[x for x in (out.find(MARK(i+1),s),out.find(MARK('FIN'),s)) if x>=0]
      seg=out[s:min(nx) if nx else len(out)]
      if seg.startswith('\n'):seg=seg[1:]
      if seg.endswith('\n'):seg=seg[:-1]
      ok=bool(nx) and (t.get('out') is None or norm(seg)==norm(t['out']))
      res.append({'ok':ok,'out':seg,'err':m['err']})
    return res
  res=[]
  for t in tests:
    m=cpp(code,t.get('in',''))
    if 'ce' in m:res.append({'ok':False,'err':'CE '+m['ce']});continue
    ok=not m['err']
    if ok and t.get('has'):ok=hasall(m['out'],t['has'])
    if ok and t.get('out') is not None:ok=norm(m['out'])==norm(t['out'])
    if ok and t.get('tail'):ok=norm(m['out']).split('\n')[-len(t['tail']):]==[l.rstrip() for l in t['tail']]
    res.append({'ok':ok,'out':m['out'],'err':m['err']})
  return res
seen=set();bad=0;n=0;nomodel=[];trivial=[]
for f in sorted(glob.glob(REPO+'/cursos/*.json')):
  if 'indice' in f or 'novedades' in f:continue
  d=json.load(open(f))
  allex=[e for t in d['topics'] for e in t['ex']]+d.get('simEx',[])
  for e in allex:
    for ch in e['checks']:
      if ch.get('t')!='code':continue
      key=json.dumps([ch,e['steps']],sort_keys=True)
      if key in seen:continue
      seen.add(key);n+=1
      code=model(e)
      if not code:nomodel.append(os.path.basename(f)+':'+e['id']);continue
      lang=ch.get('lang','py')
      try:
        r=runcpp(code,ch.get('tests')) if lang=='cpp' else runpy(code,ch.get('tests'),ch.get('files'))
        if lang!='cpp':
          for t,x in zip(ch.get('tests') or [{}],r):
            if x['ok'] and t.get('has'):x['ok']=hasall(x['out'],t['has'])
            if x['ok'] and t.get('tail'):x['ok']=norm(x['out']).split('\n')[-len(t['tail']):]==[l.rstrip() for l in t['tail']]
      except Exception as ex:r=[{'ok':False,'err':'EXC '+str(ex)[:200]}]
      fails=[(i,x) for i,x in enumerate(r) if not x['ok']]
      st=ch.get('start') or ''
      if st.strip():
        try:
          r2=runcpp(st,ch.get('tests')) if lang=='cpp' else runpy(st,ch.get('tests'),ch.get('files'))
          if all(x['ok'] for x in r2):trivial.append(os.path.basename(f)+':'+e['id'])
        except Exception:pass
      if fails:
        bad+=1;print('✗',os.path.basename(f),e['id'],lang,'fallan',len(fails),'de',len(r))
        for i,x in fails[:2]:
          t=(ch.get('tests') or [{}])[i];print('   prueba',t.get('n',i),'| err:',str(x.get('err'))[:200],'| salida:',repr(str(x.get('out',''))[:150]),'| esperada:',repr(str(t.get('out',t.get('has',t.get('tail',''))))[:150]))
print('ejercicios de código',n,'· con fallas',bad,'· sin solución modelo',nomodel,'· plantilla que ya pasa',trivial)
sys.exit(1 if bad or nomodel or trivial else 0)
