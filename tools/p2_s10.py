#!/usr/bin/env python3
"""Semana 10 de Programación II (CS1112): construye los temas, verifica con g++ y escribe p2-ef.json."""
import json, subprocess, tempfile, os, re, sys, html

REPO = sys.argv[1]
F = os.path.join(REPO, 'cursos', 'p2-ef.json')
d = json.load(open(F, encoding='utf-8'))

def esc(s): return html.escape(s, quote=False)
def pre(code): return '<pre class="cpp"><code>' + esc(code) + '</code></pre>'
def out(s): return '<code class="out">' + esc(s) + '</code>'
def c(s): return '<code>' + esc(s) + '</code>'

# ---------- compilación ----------
def run_cpp(src):
    with tempfile.TemporaryDirectory() as t:
        p = os.path.join(t, 'a.cpp'); open(p, 'w').write(src)
        r = subprocess.run(['g++', '-std=gnu++17', '-O0', '-o', os.path.join(t, 'a'), p], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        r = subprocess.run([os.path.join(t, 'a')], capture_output=True, text=True, timeout=10)
        assert r.returncode == 0, ('exit', r.returncode, r.stderr)
        return r.stdout

def norm(s): return '\n'.join(l.rstrip() for l in s.strip('\n').split('\n'))

def check_code(start, sol, tests):
    for t in tests:
        src = sol + '\n#include <iostream>\nint main(){\n{ using namespace std;\n' + t['main'] + '\n}\nreturn 0;}\n'
        got = run_cpp(src)
        assert norm(got) == norm(t['out']), ('test', t['n'], repr(got), repr(t['out']))
    # el código inicial debe compilar con al menos la clase (aunque las pruebas fallen): solo comprobamos sintaxis de la clase
    with tempfile.TemporaryDirectory() as tdir:
        p = os.path.join(tdir, 's.cpp'); open(p, 'w').write(start + '\nint main(){return 0;}\n')
        r = subprocess.run(['g++', '-std=gnu++17', '-fsyntax-only', p], capture_output=True, text=True)
        assert r.returncode == 0, ('start no compila', r.stderr)

def check_out(prog, expected):
    got = run_cpp(prog)
    assert norm(got) == norm(expected), (repr(got), repr(expected))

def ex(id, lvl, title, q, checks, steps, ans, hint, tags, play=None):
    e = {"id": id, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans, "hint": hint,
         "fig": None, "draw": False, "open": False, "solfig": None, "tags": tags, "lang": "cpp"}
    if play: e["play"] = play
    assert len(tags) == len(steps), (id, 'tags/steps')
    return e

def mcx(id, lvl, title, q, checks, steps, hint, tags):
    ch = checks[0]
    if 'o' in ch: ans = ch['o'][0]
    elif ch.get('t') == 'num': ans = ' · '.join(f"{f['l']}: {f['a']} {f.get('u','')}".strip() for f in ch['f'])
    else: ans = 'Clasificación correcta'
    return ex(id, lvl, title, q, checks, steps, ans, hint, tags)

def mc(p, opts): return {"p": p, "o": opts}

def code_ex(id, lvl, title, q, start, sol, tests, steps_pre, hint, tags):
    check_code(start, sol, tests)
    steps = steps_pre + ['Una solución posible:' + pre(sol)]
    return ex(id, lvl, title, q, [{"t": "code", "lang": "cpp", "p": "Escribe tu código y compruébalo con las pruebas", "start": start, "tests": tests}],
              steps, "Tu código pasa todas las pruebas", hint, tags)

def output_ex(id, lvl, title, prog, outs, steps, hint, tags):
    check_out(prog, outs[0])
    return ex(id, lvl, title, pre(prog) + '<p>¿Qué imprime este programa?</p>', [mc('Salida', [out(o) for o in outs])],
              steps, out(outs[0]), hint, tags, play=prog)

PUNTO = '''class CPunto2D {
    int x, y;
public:
    CPunto2D() { x = y = 0; }
    CPunto2D(int x, int y) { this->x = x; this->y = y; }
    int getX() { return x; }
    int getY() { return y; }
};'''

# =====================================================================
# TEMA A · Arreglos de objetos y punteros dobles
# =====================================================================
L = lambda c, *op: {"c": c, "op": list(op)}
H = lambda ind, *opts: {"ind": ind, "h": [dict(c=o[0], op=o[1], **({"e": o[2]} if len(o) > 2 else {})) for o in opts]}

tool_simple = {"cls": "CPunto2D", "lines": [
    L("int main() {"),
    L("    CPunto2D p1(5, 2);", ["sobj", "p1", 5, 2]),
    L("    CPunto2D* ptrP1 = &p1;", ["ref", "ptrP1", "p1"]),
    L("    CPunto2D* p2 = new CPunto2D(5, 2);", ["new", "p2", 5, 2]),
    L("    cout << p2->getX() << (*p2).getY();", ["use", "p2"]),
    L("    delete p2;", ["del", "p2"]),
    L("    p2 = nullptr;", ["null", "p2"]),
    L("    return 0;"),
    L("}", ["end"])]}
tool_arr = {"cls": "CPunto2D", "lines": [
    L("int main() {"),
    L("    CPunto2D* puntos = new CPunto2D[5];", ["newa", "puntos", 5]),
    L("    puntos[0] = CPunto2D(5, 4);", ["asg", "puntos", 0, 5, 4]),
    L("    puntos[1] = CPunto2D(6, 2);", ["asg", "puntos", 1, 6, 2]),
    L("    puntos[2] = CPunto2D(1, 1);", ["asg", "puntos", 2, 1, 1]),
    L("    cout << (*(puntos + 1)).getX();", ["use", "puntos"]),
    L("    delete[] puntos;", ["dela", "puntos"]),
    L("    puntos = nullptr;", ["null", "puntos"]),
    L("    return 0;"),
    L("}", ["end"])]}
tool_dbl = {"cls": "CPunto2D", "lines": [
    L("int main() {"),
    L("    CPunto2D** puntos = new CPunto2D*[5];", ["newp", "puntos", 5]),
    L("    puntos[0] = new CPunto2D(5, 4);", ["seti", "puntos", 0, 5, 4]),
    L("    puntos[1] = new CPunto2D(6, 2);", ["seti", "puntos", 1, 6, 2]),
    L("    puntos[2] = new CPunto2D(1, 1);", ["seti", "puntos", 2, 1, 1]),
    L("    puntos[3] = new CPunto2D(3, 1);", ["seti", "puntos", 3, 3, 1]),
    L("    puntos[4] = new CPunto2D(2, 2);", ["seti", "puntos", 4, 2, 2]),
    L("    for (int i = 0; i < 5; ++i)"),
    L("        delete puntos[i];", ["delall", "puntos"]),
    L("    delete[] puntos;", ["dela", "puntos"]),
    L("    puntos = nullptr;", ["null", "puntos"]),
    L("    return 0;"),
    L("}", ["end"])]}
tool_vec = {"cls": "CPunto2D", "lines": [
    L("int main() {"),
    L("    vector<CPunto2D> a = {CPunto2D(5,4), CPunto2D(6,2)};", ["vec", "a", [[5, 4], [6, 2]]]),
    L("    vector<CPunto2D*> b = {new CPunto2D(1,1),"),
    L("                           new CPunto2D(3,1)};", ["vecp", "b", [[1, 1], [3, 1]]]),
    L("    vector<shared_ptr<CPunto2D>> c = {"),
    L("        make_shared<CPunto2D>(2,2),"),
    L("        make_shared<CPunto2D>(7,7)};", ["sptr", "c", [[2, 2], [7, 7]]]),
    L("    for (auto p : b) delete p;", ["delall", "b"]),
    L("    return 0;"),
    L("}", ["end"])]}

DELAI = "cada v[i] es UN objeto creado con new (sin corchetes): se libera con delete v[i], sin corchetes."
mem1 = {"t": "mem", "p": "Completa las líneas que faltan", "cls": "CPunto2D", "lines": [
    L("int main() {"),
    H(4, ("CPunto2D** v = new CPunto2D*[3];", [["newp", "v", 3]]),
         ("CPunto2D** v = new CPunto2D[3];", [["fail", "No compila: new CPunto2D[3] devuelve CPunto2D*, no CPunto2D**. Para guardar punteros se crea new CPunto2D*[3]."]], "new CPunto2D[3] crea 3 objetos (devuelve CPunto2D*); para un arreglo de punteros es new CPunto2D*[3]."),
         ("CPunto2D** v = nullptr;", [["ptr", "v"]], "v queda en nullptr: v[i] = new … escribiría en ninguna parte.")),
    L("    for (int i = 0; i < 3; ++i)"),
    L("        v[i] = new CPunto2D(i, 2 * i);", ["seti", "v", 0, 0, 0], ["seti", "v", 1, 1, 2], ["seti", "v", 2, 2, 4]),
    L("    cout << v[2]->getY() << endl;", ["usei", "v", 2]),
    L("    for (int i = 0; i < 3; ++i)"),
    H(8, ("delete v[i];", [["delall", "v"]]),
         ("delete[] v[i];", [["fail", "delete[] v[0]: ese objeto se creó con new, sin corchetes; debe ser delete v[i]."]], DELAI),
         ("v[i] = nullptr;", [["nulli", "v", 0], ["nulli", "v", 1], ["nulli", "v", 2]], "poner nullptr no libera nada: los 3 objetos se quedan en el heap sin nadie que los apunte (fuga).")),
    H(4, ("delete[] v;", [["dela", "v"]]),
         ("delete v;", [["del", "v"]], "v se creó con new CPunto2D*[3] (con corchetes): se libera con delete[] v."),
         ("// no hace falta liberar v", [], "el arreglo de 3 punteros también está en el heap: si no haces delete[] v, queda una fuga.")),
    L("    v = nullptr;", ["null", "v"]),
    L("    return 0;"),
    L("}", ["end"])],
    "e": "Regla: lo que se crea con <code>new</code> se libera con <code>delete</code>; lo que se crea con <code>new[]</code>, con <code>delete[]</code>. Primero los objetos, después el arreglo de punteros."}

mem2 = {"t": "mem", "p": "Completa las líneas que faltan", "cls": "CPunto2D", "lines": [
    L("int main() {"),
    H(4, ("CPunto2D* p = new CPunto2D[3];", [["newa", "p", 3]]),
         ("CPunto2D* p = new CPunto2D(3);", [["fail", "No compila: CPunto2D no tiene un constructor con un solo parámetro. Para 3 puntos es new CPunto2D[3]."]], "con paréntesis llamas a un constructor (crearías UN objeto); para un arreglo van corchetes."),
         ("CPunto2D* p = new CPunto2D*[3];", [["fail", "No compila: new CPunto2D*[3] devuelve CPunto2D**, no CPunto2D*."]], "eso crea 3 punteros, no 3 puntos; además no coincide con el tipo CPunto2D*.")),
    L("    p[0] = CPunto2D(5, 4);", ["asg", "p", 0, 5, 4]),
    L("    p[1] = CPunto2D(6, 2);", ["asg", "p", 1, 6, 2]),
    L("    cout << p[1].getX() << endl;", ["use", "p"]),
    H(4, ("delete[] p;", [["dela", "p"]]),
         ("delete p;", [["del", "p"]], "p se creó con new CPunto2D[3]: se libera con delete[] p."),
         ("for (int i = 0; i < 3; ++i) delete p[i];", [["fail", "No compila: p[i] es un CPunto2D (un objeto), no un puntero; no se le puede hacer delete."]], "aquí los objetos están uno al lado del otro en un solo bloque: no hay punteros que liberar uno por uno.")),
    L("    p = nullptr;", ["null", "p"]),
    L("    return 0;"),
    L("}", ["end"])],
    "e": "Un arreglo de objetos (<code>CPunto2D*</code>) es un solo bloque: se crea con un <code>new[]</code> y se libera con un <code>delete[]</code>."}

mem3 = {"t": "mem", "p": "Completa la línea que falta", "cls": "CPunto2D", "lines": [
    L("int main() {"),
    L("    vector<CPunto2D*> a = {new CPunto2D(1,1),"),
    L("                           new CPunto2D(2,2)};", ["vecp", "a", [[1, 1], [2, 2]]]),
    L("    vector<shared_ptr<CPunto2D>> b = {"),
    L("        make_shared<CPunto2D>(3,3),"),
    L("        make_shared<CPunto2D>(4,4)};", ["sptr", "b", [[3, 3], [4, 4]]]),
    H(4, ("for (auto p : a) delete p;", [["delall", "a"]]),
         ("for (auto p : b) delete p;", [["fail", "No compila: un shared_ptr no se borra con delete; se libera solo cuando nadie lo usa."]], "los shared_ptr se liberan solos; delete no se usa con ellos."),
         ("// nada: los vectores se limpian solos", [], "el vector a libera su arreglo de punteros, pero NO los objetos a los que apuntan: fuga.")),
    L("    return 0;"),
    L("}", ["end"])],
    "e": "<code>vector&lt;T*&gt;</code> es «semi-automático»: el vector se libera solo, los objetos no. Con <code>shared_ptr</code> todo es automático."}

# op 'fail' (no compila) — se implementa en index.html
STEPS_MEM = lambda *s: list(s)

A_teo = ('<p>Un <b>objeto estático</b> vive en el stack: <code>CPunto2D p1(5, 2);</code>. Un puntero puede apuntarlo: <code>CPunto2D* ptr = &amp;p1;</code> y entonces <code>ptr-&gt;getX()</code> es lo mismo que <code>(*ptr).getX()</code>. '
 'Un <b>objeto dinámico</b> vive en el heap: <code>CPunto2D* p2 = new CPunto2D(5, 2);</code>; se libera con <code>delete p2;</code> y conviene dejar <code>p2 = nullptr;</code>.</p>'
 '<p><b>Arreglo de objetos</b>: <code>CPunto2D* puntos = new CPunto2D[5];</code> crea 5 objetos seguidos en un solo bloque y ejecuta el <b>constructor sin parámetros</b> una vez por elemento (por eso la clase lo necesita). '
 'Se usan con punto: <code>puntos[i].getX()</code> o <code>(*(puntos + i)).getY()</code>. También se pueden inicializar: <code>new CPunto2D[5]{CPunto2D(5,4), …}</code>. Se libera con <b>un</b> <code>delete[] puntos;</code>.</p>'
 '<p><b>Arreglo de punteros (puntero doble)</b>: <code>CPunto2D** puntos = new CPunto2D*[5];</code> crea 5 <i>punteros</i> (8 bytes cada uno en 64 bits); cada objeto se crea aparte: <code>puntos[i] = new CPunto2D(5, 4);</code> y se usa con flecha: <code>puntos[i]-&gt;getX()</code>. '
 'Para liberar, de adentro hacia afuera: <code>for (…) delete puntos[i];</code> → <code>delete[] puntos;</code> → <code>puntos = nullptr;</code>. Si borras primero el arreglo, pierdes las direcciones de los objetos (fuga).</p>'
 '<p><b>Simple vs. doble.</b> El doble usa más memoria (los punteros) y es más trabajo liberarlo, pero permite agregar objetos sin mover los demás y <b>mover o compartir</b> un objeto entre arreglos copiando solo su dirección.</p>'
 '<p><b>Con vectores</b>: <code>vector&lt;CPunto2D&gt;</code> libera todo solo; <code>vector&lt;CPunto2D*&gt;</code> es semi-automático (el vector se libera solo, pero cada objeto creado con <code>new</code> necesita su <code>delete</code>); <code>vector&lt;shared_ptr&lt;CPunto2D&gt;&gt;</code> con <code>make_shared&lt;CPunto2D&gt;(5,4)</code> libera todo solo.</p>'
 '<p class="note">En las láminas aparece «int = 8 bytes»: en las PC actuales un <code>int</code> ocupa 4 bytes (por eso su propio dibujo avanza de 4 en 4); el que ocupa 8 es el puntero.</p>')

A_lesson = ('<h3>Idea central</h3><p>Todo lo que se crea con <code>new</code> hay que liberarlo una vez, con el <code>delete</code> que le corresponde. Con punteros dobles hay dos niveles: los objetos y el arreglo de punteros.</p>'
 '<h3>Conceptos clave</h3><ul><li><code>new X[n]</code> ↔ <code>delete[]</code>; <code>new X(…)</code> ↔ <code>delete</code>.</li><li><code>X* v</code>: objetos seguidos (se usa <code>v[i].m()</code>). <code>X** v</code>: punteros a objetos (se usa <code>v[i]-&gt;m()</code>).</li><li>Fuga: memoria del heap que ya nadie apunta. Colgante: puntero a memoria ya liberada.</li><li>vector y shared_ptr liberan solos.</li></ul>'
 '<div class="ej"><b>Ejemplo:</b> <code>CPunto2D** v = new CPunto2D*[3];</code> → <code>v[i] = new CPunto2D(i, i);</code> → <code>delete v[i];</code> (cada uno) → <code>delete[] v;</code>.</div>'
 '<div class="err"><b>Error común:</b> hacer <code>delete[] v;</code> antes de borrar cada <code>v[i]</code>: los objetos quedan en el heap sin nadie que los apunte.</div>')

A_form = ['<code>X* p = new X(…);</code> · <code>p-&gt;m()</code> ≡ <code>(*p).m()</code> · <code>delete p;</code>',
          '<code>X* v = new X[n];</code> (constructor sin parámetros ×n) · <code>v[i].m()</code> · <code>delete[] v;</code>',
          '<code>X** v = new X*[n];</code> · <code>v[i] = new X(…);</code> · <code>v[i]-&gt;m()</code>',
          'Liberar doble: <code>delete v[i]</code> (cada uno) → <code>delete[] v</code> → <code>v = nullptr</code>',
          '<code>vector&lt;X&gt;</code> solo · <code>vector&lt;X*&gt;</code> delete a cada uno · <code>vector&lt;shared_ptr&lt;X&gt;&gt;</code> solo',
          'Puntero: 8 bytes (64 bits) · int: 4 bytes']

A_ex = []
A_ex.append(ex("p10m1", 2, "Mapa de memoria: punteros dobles", "<p>Completa las líneas que faltan para crear 3 puntos con un arreglo de punteros y dejar la memoria limpia. Usa ▶ para ver qué pasa en el stack y el heap con tu versión.</p>",
   [mem1], ["<code>new CPunto2D*[3]</code> crea el arreglo de 3 punteros; cada <code>v[i] = new CPunto2D(…)</code> crea un objeto aparte.",
            "Cada objeto se creó con <code>new</code> sin corchetes: se libera con <code>delete v[i]</code>.",
            "Al final se libera el arreglo de punteros con <code>delete[] v</code> (se creó con corchetes) y se deja <code>v = nullptr</code>."],
   "Tienes que ver «✅ Memoria limpia» al ejecutar todo.", "Tu versión deja la memoria limpia", [["pptr"], ["delarr", "pptr"], ["delarr"]]))
A_ex[-1]["ans"] = "<code>new CPunto2D*[3]</code> · <code>delete v[i]</code> · <code>delete[] v</code>"
A_ex.append(ex("p10m2", 2, "Mapa de memoria: arreglo de objetos", "<p>Completa las líneas que faltan. Esta vez los puntos están <b>dentro</b> del arreglo (no hay punteros a cada uno).</p>",
   [mem2], ["<code>new CPunto2D[3]</code> crea un solo bloque con 3 objetos (llama 3 veces al constructor sin parámetros).",
            "Como es un solo bloque creado con <code>new[]</code>, se libera con un único <code>delete[] p</code>."],
   "Corchetes al crear ⇒ corchetes al liberar.", "", [["arrobj"], ["delarr"]]))
A_ex[-1]["ans"] = "<code>new CPunto2D[3]</code> · <code>delete[] p</code>"
A_ex.append(ex("p10m3", 2, "Mapa de memoria: vector y shared_ptr", "<p>¿Qué línea falta para que el programa no tenga fugas?</p>",
   [mem3], ["El vector <code>a</code> guarda punteros: al terminar se libera el vector, pero no los objetos creados con <code>new</code>.",
            "Los <code>shared_ptr</code> de <code>b</code> se liberan solos: no se les hace <code>delete</code>."],
   "¿Quién creó los objetos de a? ¿Y los de b?", "", [["smart"], ["smart"]]))
A_ex[-1]["ans"] = "<code>for (auto p : a) delete p;</code>"

A_ex.append(mcx("p10t1", 1, "Flecha o punto", "<p>Con <code>CPunto2D* p = new CPunto2D(5, 2);</code>, ¿cuál de estas expresiones <b>NO</b> sirve para leer x (suponiendo que x es público)?</p>",
   [mc("Respuesta", [c("*p.x"), c("p->x"), c("(*p).x"), c("p[0].x"), c("(&(*p))->x")])],
   ["El punto tiene más prioridad que el asterisco: <code>*p.x</code> se lee como <code>*(p.x)</code>, y p es un puntero, no tiene .x.",
    "<code>p-&gt;x</code> es la forma corta de <code>(*p).x</code>; <code>p[0]</code> es lo mismo que <code>*p</code>."],
   "Fíjate en la prioridad de * y del punto.", [["objdin"], ["objdin"]]))
A_ex.append(mcx("p10t2", 1, "¿Qué constructor se ejecuta?", "<p>La clase <code>CPunto2D</code> tiene <code>CPunto2D()</code> y <code>CPunto2D(int x, int y)</code>. ¿Qué pasa con <code>CPunto2D* v = new CPunto2D[5];</code>?</p>",
   [mc("Respuesta", ["Se ejecuta <code>CPunto2D()</code> 5 veces, una por elemento",
                     "Se ejecuta <code>CPunto2D(int, int)</code> 5 veces con basura",
                     "No se ejecuta ningún constructor hasta asignar cada elemento",
                     "Se ejecuta <code>CPunto2D()</code> una sola vez para todo el arreglo",
                     "Da error: un arreglo dinámico de objetos necesita <code>CPunto2D**</code>"])],
   ["<code>new X[n]</code> construye n objetos seguidos y usa el constructor sin parámetros en cada uno.",
    "Si la clase no tuviera constructor sin parámetros, habría que inicializar con llaves: <code>new CPunto2D[2]{CPunto2D(1,1), CPunto2D(2,2)}</code>."],
   "Cada elemento es un objeto completo.", [["arrobj"], ["arrobj", "ctor"]]))
A_ex.append(mcx("p10t3", 2, "Bytes en el heap", "<p>Una clase tiene dos atributos <code>double</code> (8 bytes cada uno). En una PC de 64 bits, ¿cuántos bytes reserva cada instrucción (solo ese bloque)?</p>",
   [{"t": "num", "p": "Bytes", "f": [{"l": "new P[5]", "a": 80, "u": "bytes", "e": "5 objetos × (8 + 8) bytes."},
                                      {"l": "new P*[5]", "a": 40, "u": "bytes", "e": "5 punteros × 8 bytes: los objetos todavía no existen."}]}],
   ["<code>new P[5]</code>: 5 objetos completos de 16 bytes = 80 bytes.",
    "<code>new P*[5]</code>: solo 5 punteros de 8 bytes = 40 bytes; cada objeto se reserva después con su propio new."],
   "Un puntero ocupa 8 bytes, apunte a lo que apunte.", [["arrobj"], ["pptr"]]))
A_ex.append(mcx("p10t4", 2, "¿Cómo se libera?", "<p>Clasifica cada cosa según cómo se libera su memoria.</p>",
   [{"t": "cls", "cats": ["Se libera sola", "delete", "delete[]"], "items": [
       {"x": c("CPunto2D p(1, 2);"), "c": 0, "e": "Está en el stack: muere al terminar su bloque."},
       {"x": c("vector<CPunto2D> v(5);"), "c": 0, "e": "El vector libera sus objetos solo."},
       {"x": c("make_shared<CPunto2D>(1, 2)"), "c": 0, "e": "El shared_ptr lo libera cuando ya nadie lo usa."},
       {"x": c("new CPunto2D(1, 2)"), "c": 1, "e": "Un objeto creado con new, sin corchetes."},
       {"x": "cada " + c("v[i] = new CPunto2D(…)") + " de un " + c("CPunto2D**"), "c": 1, "e": "Cada elemento es un objeto creado con new."},
       {"x": c("new CPunto2D[5]"), "c": 2, "e": "Creado con corchetes ⇒ delete[]."},
       {"x": c("new CPunto2D*[5]"), "c": 2, "e": "El arreglo de punteros se creó con corchetes ⇒ delete[]."}]}],
   ["Stack, vector de objetos y shared_ptr: automático.", "new sin corchetes ⇒ delete; new con corchetes ⇒ delete[]."],
   "Mira si hay new y si lleva corchetes.", [["smart"], ["delarr"]]))
A_ex.append(mcx("p10t5", 2, "Simple vs. doble", "<p>¿Cuál es una <b>ventaja</b> de <code>CPunto2D** v = new CPunto2D*[n]</code> frente a <code>CPunto2D* v = new CPunto2D[n]</code>?</p>",
   [mc("Respuesta", ["Se puede mover o compartir un objeto entre arreglos copiando solo su dirección",
                     "Ocupa menos memoria en total",
                     "Se libera con un solo <code>delete[]</code>",
                     "No hace falta un <code>new</code> por cada objeto",
                     "Los objetos quedan uno al lado del otro en memoria"])],
   ["Con punteros, reordenar, mover o compartir un objeto es copiar 8 bytes, sin copiar ni reconstruir el objeto.",
    "Desventajas: usa memoria extra para los punteros, necesita un new por objeto y liberar es más trabajo (cada objeto y luego el arreglo)."],
   "Piensa en qué se copia cuando mueves un elemento.", [["pptr"], ["pptr", "delarr"]]))
A_ex.append(output_ex("p10o1", 2, "Arreglo de punteros: ¿qué imprime?",
 '#include <iostream>\nusing namespace std;\n\nclass CPunto2D {\n    int x, y;\npublic:\n    CPunto2D(int x, int y) { this->x = x; this->y = y; }\n    int getX() { return x; }\n    int getY() { return y; }\n};\n\nint main() {\n    CPunto2D** v = new CPunto2D*[3];\n    for (int i = 0; i < 3; ++i)\n        v[i] = new CPunto2D(i + 1, 10 * (i + 1));\n    CPunto2D* t = v[0];\n    v[0] = v[2];\n    v[2] = t;\n    for (int i = 0; i < 3; ++i)\n        cout << v[i]->getX() << "," << v[i]->getY() << " ";\n    cout << endl;\n    for (int i = 0; i < 3; ++i)\n        delete v[i];\n    delete[] v;\n    return 0;\n}',
 ["3,30 2,20 1,10 ", "1,10 2,20 3,30 ", "3,10 2,20 1,30 ", "3,30 2,20 3,30 ", "No compila: no se pueden intercambiar punteros"],
 ["Se intercambian las <b>direcciones</b> guardadas en v[0] y v[2]; los objetos no se mueven ni se copian.",
  "Por eso el recorrido muestra primero el objeto (3,30) y al final el (1,10). Cada objeto se sigue liberando una sola vez."],
 "Solo se cambian los punteros.", [["pptr"], ["pptr", "delarr"]]))

START_M8 = '''#include <iostream>
using namespace std;

class CPunto2D {
    int x, y;
public:
    inline static int vivos = 0;   // cuántos puntos existen ahora (para comprobar que liberas todo)
    CPunto2D(int x, int y) { this->x = x; this->y = y; vivos++; }
    ~CPunto2D() { vivos--; }
    int getX() { return x; }
    int getY() { return y; }
};

CPunto2D** crearPuntos(int n) {
}

void liberar(CPunto2D**& v, int n) {
}
'''
SOL_M8 = '''#include <iostream>
using namespace std;

class CPunto2D {
    int x, y;
public:
    inline static int vivos = 0;   // cuántos puntos existen ahora (para comprobar que liberas todo)
    CPunto2D(int x, int y) { this->x = x; this->y = y; vivos++; }
    ~CPunto2D() { vivos--; }
    int getX() { return x; }
    int getY() { return y; }
};

CPunto2D** crearPuntos(int n) {
    CPunto2D** v = new CPunto2D*[n];
    for (int i = 0; i < n; ++i)
        v[i] = new CPunto2D(i, 2 * i);
    return v;
}

void liberar(CPunto2D**& v, int n) {
    for (int i = 0; i < n; ++i)
        delete v[i];
    delete[] v;
    v = nullptr;
}
'''
T_M8 = [{"n": "Crea los puntos (i, 2i)", "main": 'CPunto2D** v = crearPuntos(4);\nfor (int i = 0; i < 4; ++i) {\n    if (i) cout << " ";\n    cout << v[i]->getX() << "," << v[i]->getY();\n}\ncout << endl;\ncout << CPunto2D::vivos << endl;\nliberar(v, 4);', "out": "0,0 1,2 2,4 3,6\n4"},
        {"n": "Libera todo y deja nullptr", "main": 'CPunto2D** v = crearPuntos(3);\nliberar(v, 3);\ncout << CPunto2D::vivos << " " << (v == nullptr) << endl;', "out": "0 1"}]
A_ex.append(code_ex("p10c1", 3, "Crear y liberar un arreglo de punteros",
  "<p>Completa dos funciones:</p><ul><li><code>CPunto2D** crearPuntos(int n)</code>: crea un arreglo dinámico de <code>n</code> punteros y en cada posición <code>i</code> un punto nuevo <code>(i, 2*i)</code>.</li>"
  "<li><code>void liberar(CPunto2D**&amp; v, int n)</code>: libera todos los puntos, después el arreglo, y deja <code>v</code> en <code>nullptr</code>.</li></ul>"
  "<p class=\"note\"><code>CPunto2D::vivos</code> cuenta cuántos puntos existen: si al final no es 0, te faltó un <code>delete</code>.</p>",
  START_M8, SOL_M8, T_M8,
  ["<code>new CPunto2D*[n]</code> crea los n punteros; cada <code>v[i] = new CPunto2D(i, 2*i)</code> crea un punto.",
   "Para liberar: primero cada <code>delete v[i]</code>, luego <code>delete[] v</code>. El parámetro es <code>CPunto2D**&amp;</code> (por referencia) para poder dejar la variable del main en nullptr."],
  "Libera de adentro hacia afuera.", [["pptr"], ["delarr", "pptr"], ["pptr"]]))

# =====================================================================
# TEMA B · Relaciones entre clases
# =====================================================================
B_teo = ('<p>Una <b>relación</b> es un vínculo entre objetos de clases distintas que se necesitan para hacer algo (un alumno <i>aprueba</i> un curso, un chofer <i>conduce</i> un taxi). Hay tres tipos, y cada uno se valida con una frase:</p>'
 '<p><b>Asociación — «usa un».</b> Dos objetos independientes trabajan juntos: el taxi usa un chofer, el cliente usa una tarjeta. Si se quita la tarjeta, el cliente sigue existiendo. '
 'En UML es una línea con <b>flecha</b> hacia la clase asociada. En C++: un atributo <b>puntero</b> (<code>Chofer* m_Chofer;</code>) y un método que la asocia (<code>void setChofer(Chofer* c)</code>); luego se accede a través de él: <code>m_Chofer-&gt;getNombres()</code>.</p>'
 '<p><b>Composición — «es parte de».</b> Un objeto grande está formado por partes que <b>nacen y mueren con él</b>: el motor es parte del auto, el muro es parte del usuario, la fecha y la hora son parte del evento. '
 'En UML: línea con <b>rombo lleno</b> junto a la clase «todo». En C++: atributos que son <b>objetos</b> (no punteros): <code>CTime m_Time; CDate m_Day;</code>, y un constructor que los construye con la <b>lista de inicialización</b>: '
 '<code>CEvent(…) : m_Time(h, m), m_Day(mes, d, a) { … }</code>. Las partes se construyen <i>antes</i> que el todo y se destruyen <i>después</i>.</p>'
 '<p><b>Agregación — «tiene un(os)».</b> El todo agrupa objetos que pueden existir sin él: la universidad tiene estudiantes, el estudiante tiene cursos. '
 'En UML: línea con <b>rombo vacío</b> junto al «todo». En C++: un atributo con la colección de partes, normalmente <code>vector&lt;Estudiante*&gt;</code>, y un método que agrega (<code>void agregar(Estudiante* e)</code>). '
 'Se usan <b>punteros</b> porque el todo no es dueño de las partes: si se destruye la universidad, los estudiantes siguen existiendo.</p>'
 '<p class="note">En las láminas hay detalles por corregir: con un puntero (<code>CEvent* pEvent = new CEvent()</code>) se llama <code>pEvent-&gt;setEventData(…)</code>, no <code>pEvent .setEventData</code>; los nombres de clase y constructor deben coincidir (<code>CDate::CDate()</code>, <code>CEvent</code>) y en <code>printEventData</code> el atributo es <code>m_Name</code>.</p>')
B_lesson = ('<h3>Idea central</h3><p>Lo que cambia entre las tres relaciones es <b>quién vive cuánto</b>: en la composición las partes mueren con el todo; en la asociación y la agregación cada objeto tiene vida propia.</p>'
 '<h3>Conceptos clave</h3><ul><li>Asociación: «usa un» · flecha · atributo puntero + set.</li><li>Composición: «es parte de» · rombo lleno · atributos objeto + lista de inicialización.</li><li>Agregación: «tiene un(os)» · rombo vacío · vector de punteros + agregar.</li></ul>'
 '<div class="ej"><b>Ejemplo:</b> <code>CEvent e(6, 0, 12, 25, 2019, "Navidad");</code> construye primero <code>m_Time</code> y <code>m_Day</code>, y luego el cuerpo del constructor de CEvent.</div>'
 '<div class="err"><b>Error común:</b> en una composición asignar las partes dentro de las llaves del constructor cuando no tienen constructor sin parámetros: no compila. Van en la lista de inicialización, después de los dos puntos.</div>')
B_form = ['Asociación: «usa un» · flecha → · <code>Chofer* m_Chofer;</code> + <code>setChofer(Chofer*)</code>',
          'Composición: «es parte de» · rombo lleno ◆ en el todo · <code>CTime m_Time;</code> · nacen y mueren juntos',
          'Lista de inicialización: <code>CEvent(…) : m_Time(h, m), m_Day(d, mes, a) { }</code>',
          'Agregación: «tiene un(os)» · rombo vacío ◇ en el todo · <code>vector&lt;Est*&gt;</code> + <code>agregar(Est*)</code>',
          'Orden: partes antes que el todo al construir; al revés al destruir']

B_ex = []
B_ex.append(mcx("p10r1", 1, "¿Qué relación es?", "<p>Clasifica cada pareja según su relación (usa las frases «usa un», «es parte de», «tiene un»).</p>",
   [{"t": "cls", "cats": ["Asociación", "Composición", "Agregación"], "items": [
       {"x": "Taxi – Chofer", "c": 0, "e": "El taxi usa un chofer; ambos existen por separado."},
       {"x": "Cliente – Tarjeta de crédito", "c": 0, "e": "Se puede quitar la tarjeta y el cliente sigue existiendo."},
       {"x": "Ingeniero – Computadora", "c": 0, "e": "El ingeniero usa una computadora."},
       {"x": "Auto – Motor", "c": 1, "e": "El motor es parte del auto."},
       {"x": "Usuario de Facebook – Muro", "c": 1, "e": "El muro se crea con la cuenta y muere con ella."},
       {"x": "Evento – Fecha y hora", "c": 1, "e": "La fecha y la hora son parte del evento."},
       {"x": "Universidad – Estudiantes", "c": 2, "e": "La universidad tiene (agrupa) estudiantes que existen sin ella."},
       {"x": "Estudiante – Cursos", "c": 2, "e": "Un estudiante tiene varios cursos."}]}],
   ["«Usa un» ⇒ asociación; «es parte de» y nacen/mueren juntos ⇒ composición.", "«Tiene un(os)», un conjunto de objetos con vida propia ⇒ agregación."],
   "Prueba cada frase con la pareja.", [["asoc", "compo"], ["agreg"]]))
B_ex.append(mcx("p10r2", 1, "Notación UML", "<p>En un diagrama de clases, ¿qué representa una línea con un <b>rombo lleno</b> junto a la clase <code>Auto</code> y la otra punta en <code>Motor</code>?</p>",
   [mc("Respuesta", ["Composición: el motor es parte del auto y muere con él",
                     "Agregación: el auto tiene motores que existen por separado",
                     "Asociación: el auto usa un motor",
                     "Herencia: el motor es un tipo de auto",
                     "Composición: el auto es parte del motor"])],
   ["Rombo lleno ⇒ composición; rombo vacío ⇒ agregación; flecha simple ⇒ asociación.", "El rombo va pegado a la clase «todo» (Auto); la otra punta es la parte (Motor)."],
   "El rombo marca al «todo».", [["uml", "compo"], ["uml"]]))
B_ex.append(mcx("p10r3", 2, "¿Por qué punteros en la agregación?", "<p>En <code>class Universidad { vector&lt;Estudiante*&gt; estudiantes; … };</code>, ¿por qué se guardan punteros y no objetos <code>Estudiante</code>?</p>",
   [mc("Respuesta", ["Porque los estudiantes existen por su cuenta: la universidad solo los referencia y no debe destruirlos ni copiarlos",
                     "Porque un vector no puede guardar objetos de una clase",
                     "Porque los punteros ocupan siempre menos memoria y son más rápidos",
                     "Porque así la universidad destruye a sus estudiantes en su destructor",
                     "Porque la agregación exige usar new dentro de la clase"])],
   ["En la agregación el todo no es dueño de las partes: guardar punteros permite apuntar a estudiantes que ya existen (y que pueden estar en otras universidades).",
    "Si guardara objetos, tendría copias que nacerían y morirían con la universidad: eso sería composición."],
   "¿Quién es dueño de los estudiantes?", [["agreg"], ["agreg", "compo"]]))
B_ex.append(mcx("p10r4", 2, "Asociación: ¿dónde va cada cosa?", "<p>Para que <code>Taxi</code> «use un» <code>Chofer</code>, ¿qué necesita la clase Taxi?</p>",
   [mc("Respuesta", ["Un atributo <code>Chofer*</code> y un método <code>setChofer(Chofer*)</code> que lo asigne",
                     "Un atributo <code>Chofer</code> construido en la lista de inicialización",
                     "Que Chofer tenga un atributo <code>Taxi*</code> y nada más",
                     "Un <code>vector&lt;Chofer&gt;</code> con todos los choferes",
                     "Heredar de Chofer: <code>class Taxi : public Chofer</code>"])],
   ["La asociación se arma con un atributo del tipo de la clase asociada (puntero, porque el chofer existe aparte) y un método que hace la asociación.",
    "Luego el taxi accede a los datos de su chofer a través de él: <code>m_Chofer-&gt;getNombres()</code>."],
   "El chofer ya existe; el taxi solo lo apunta.", [["asoc"], ["asoc"]]))
B_ex.append(mcx("p10r5", 1, "Encuentra el error", pre('CEvent* pEvent = new CEvent();\npEvent.setEventData(6, 0, 12, 25, 2019, "Navidad");\npEvent.printEventData(cout);') + "<p>¿Por qué no compila?</p>",
   [mc("Respuesta", ["pEvent es un puntero: se debe usar <code>pEvent-&gt;setEventData(…)</code>",
                     "Falta <code>delete pEvent;</code> antes de llamar a los métodos",
                     "<code>new CEvent()</code> no se puede usar si la clase tiene atributos de otras clases",
                     "printEventData no puede recibir <code>cout</code>",
                     "Los métodos de una composición solo se llaman desde el constructor"])],
   ["Con un objeto se usa el punto; con un puntero, la flecha (o <code>(*pEvent).setEventData(…)</code>).",
    "Además falta liberar al final con <code>delete pEvent;</code>, aunque eso no impide compilar."],
   "¿pEvent es un objeto o un puntero?", [["objdin"], ["objdin"]]))
B_ex.append(output_ex("p10r6", 2, "Composición: orden de construcción",
 '#include <iostream>\nusing namespace std;\n\nclass Motor {\npublic:\n    Motor() { cout << "M+ "; }\n    ~Motor() { cout << "M- "; }\n};\n\nclass Llanta {\npublic:\n    Llanta() { cout << "L+ "; }\n    ~Llanta() { cout << "L- "; }\n};\n\nclass Auto {\n    Motor motor;\n    Llanta llanta;\npublic:\n    Auto() { cout << "A+ "; }\n    ~Auto() { cout << "A- "; }\n};\n\nint main() {\n    Auto a;\n    cout << "| ";\n    return 0;\n}',
 ["M+ L+ A+ | A- L- M- ", "A+ M+ L+ | A- L- M- ", "M+ L+ A+ | M- L- A- ", "A+ M+ L+ | M- L- A- ", "M+ L+ A+ | A- "],
 ["Las partes (atributos objeto) se construyen <b>antes</b> que el cuerpo del constructor del todo, en el orden en que están declaradas: Motor, Llanta y luego Auto.",
  "Al destruir es al revés: primero el destructor de Auto y después sus partes en orden inverso (Llanta, Motor). Las partes mueren con el todo."],
 "Primero las piezas, luego el auto.", [["compo"], ["compo", "dtor"]]))
B_ex.append(output_ex("p10r7", 2, "Agregación: ¿quién sobrevive?",
 '#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n\nclass Estudiante {\n    string nombre;\npublic:\n    Estudiante(string n) { nombre = n; }\n    ~Estudiante() { cout << "~" << nombre << " "; }\n};\n\nclass Universidad {\n    vector<Estudiante*> estudiantes;\npublic:\n    void agregar(Estudiante* e) { estudiantes.push_back(e); }\n    ~Universidad() { cout << "~Uni "; }\n};\n\nint main() {\n    Estudiante ana("Ana"), beto("Beto");\n    {\n        Universidad u;\n        u.agregar(&ana);\n        u.agregar(&beto);\n    }\n    cout << "| ";\n    return 0;\n}',
 ["~Uni | ~Beto ~Ana ", "~Ana ~Beto ~Uni | ", "~Uni ~Ana ~Beto | ", "~Beto ~Ana ~Uni | ", "| ~Uni ~Beto ~Ana "],
 ["La universidad muere al cerrar su bloque, pero solo guardaba <b>punteros</b>: destruirla no destruye a los estudiantes.",
  "Ana y Beto mueren al terminar main, en orden inverso a su creación (Beto, Ana). Así se ve la diferencia con la composición."],
 "¿La universidad es dueña de sus estudiantes?", [["agreg"], ["agreg", "dtor"]]))

START_R1 = '''#include <iostream>
#include <string>
using namespace std;

class Chofer {
    string nombre;
public:
    Chofer(string n) { nombre = n; }
    string getNombre() { return nombre; }
};

class Taxi {
    string placa;
    Chofer* chofer;
public:
    Taxi(string p) {
        placa = p;
        chofer = nullptr;
    }
    // completa: void setChofer(Chofer* c) y string getNombreChofer()
};
'''
SOL_R1 = '''#include <iostream>
#include <string>
using namespace std;

class Chofer {
    string nombre;
public:
    Chofer(string n) { nombre = n; }
    string getNombre() { return nombre; }
};

class Taxi {
    string placa;
    Chofer* chofer;
public:
    Taxi(string p) {
        placa = p;
        chofer = nullptr;
    }
    void setChofer(Chofer* c) { chofer = c; }
    string getNombreChofer() {
        if (chofer == nullptr) return "Sin chofer";
        return chofer->getNombre();
    }
};
'''
T_R1 = [{"n": "Sin chofer", "main": 'Taxi t("A1Z521");\ncout << t.getNombreChofer() << endl;', "out": "Sin chofer"},
        {"n": "Asociar un chofer", "main": 'Chofer juan("Juan Perez");\nTaxi t("A1Z521");\nt.setChofer(&juan);\ncout << t.getNombreChofer() << endl;', "out": "Juan Perez"},
        {"n": "Cambiar de chofer", "main": 'Chofer a("Ana"), b("Beto");\nTaxi t("B2X100");\nt.setChofer(&a);\nt.setChofer(&b);\ncout << t.getNombreChofer() << endl;', "out": "Beto"},
        {"n": "El chofer sigue existiendo sin el taxi", "main": 'Chofer ana("Ana");\n{\n    Taxi t("C3Y200");\n    t.setChofer(&ana);\n}\ncout << ana.getNombre() << endl;', "out": "Ana"}]
B_ex.append(code_ex("p10c2", 2, "Asociación: Taxi usa un Chofer",
  "<p>Completa la clase <code>Taxi</code> para que «use un» <code>Chofer</code>:</p><ul><li><code>void setChofer(Chofer* c)</code>: asocia el chofer.</li>"
  "<li><code>string getNombreChofer()</code>: devuelve el nombre del chofer, o <code>\"Sin chofer\"</code> si todavía no tiene.</li></ul>",
  START_R1, SOL_R1, T_R1,
  ["La asociación necesita un atributo puntero (ya está: <code>Chofer* chofer</code>) y un método que lo asigne.",
   "Antes de usar <code>chofer-&gt;</code> hay que comprobar que no sea <code>nullptr</code>. El taxi no hace <code>delete</code> del chofer: no es su dueño."],
  "Comprueba nullptr antes de usar la flecha.", [["asoc"], ["asoc"], ["asoc"]]))

START_R2 = '''#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

class CFecha {
    int dia, mes, anio;
public:
    CFecha(int d, int m, int a) { dia = d; mes = m; anio = a; }
    void imprimir() {
        cout << setfill('0') << setw(2) << dia << "/" << setw(2) << mes << "/" << anio;
    }
};

class CHora {
    int hora, minuto;
public:
    CHora(int h, int m) {
        hora = (h >= 0 && h < 24) ? h : 0;
        minuto = (m >= 0 && m < 60) ? m : 0;
    }
    void imprimir() {
        cout << setfill('0') << setw(2) << hora << ":" << setw(2) << minuto;
    }
};

class CEvento {
    string nombre;
    CFecha fecha;
    CHora hora;
public:
    // completa: CEvento(string n, int d, int m, int a, int h, int mi)
    //           void imprimir()  ->  Navidad: 25/12/2019 06:00
};
'''
SOL_R2 = START_R2.replace('''    // completa: CEvento(string n, int d, int m, int a, int h, int mi)
    //           void imprimir()  ->  Navidad: 25/12/2019 06:00
''', '''    CEvento(string n, int d, int m, int a, int h, int mi) : fecha(d, m, a), hora(h, mi) {
        nombre = n;
    }
    void imprimir() {
        cout << nombre << ": ";
        fecha.imprimir();
        cout << " ";
        hora.imprimir();
        cout << endl;
    }
''')
T_R2 = [{"n": "Navidad", "main": 'CEvento e("Navidad", 25, 12, 2019, 6, 0);\ne.imprimir();', "out": "Navidad: 25/12/2019 06:00"},
        {"n": "Hora inválida", "main": 'CEvento e("Open Day", 9, 3, 2026, 25, 15);\ne.imprimir();', "out": "Open Day: 09/03/2026 00:15"},
        {"n": "Dos eventos", "main": 'CEvento a("Parcial", 6, 10, 2026, 8, 30), b("Final", 1, 12, 2026, 14, 5);\na.imprimir();\nb.imprimir();', "out": "Parcial: 06/10/2026 08:30\nFinal: 01/12/2026 14:05"}]
B_ex.append(code_ex("p10c3", 3, "Composición: un evento con fecha y hora",
  "<p><code>CEvento</code> está <b>compuesto</b> por una <code>CFecha</code> y una <code>CHora</code>. Completa:</p><ul>"
  "<li>El constructor <code>CEvento(string n, int d, int m, int a, int h, int mi)</code>, que construye la fecha y la hora.</li>"
  "<li><code>void imprimir()</code>, que muestra <code>Navidad: 25/12/2019 06:00</code> y salta de línea (usa los <code>imprimir()</code> de cada parte).</li></ul>"
  "<p class=\"note\">Ojo: CFecha y CHora no tienen constructor sin parámetros.</p>",
  START_R2, SOL_R2, T_R2,
  ["Como las partes no tienen constructor sin parámetros, se construyen en la <b>lista de inicialización</b>: <code>: fecha(d, m, a), hora(h, mi)</code>.",
   "imprimir delega en las partes: el evento no sabe cómo se imprime una fecha, se lo pide a su CFecha."],
  "Después de los dos puntos del constructor.", [["compo"], ["compo"], ["compo"]]))

START_R3 = '''#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Curso {
    string nombre;
public:
    Curso(string n) { nombre = n; }
    string getNombre() { return nombre; }
};

class Estudiante {
    string nombre;
    vector<Curso*> cursos;
public:
    Estudiante(string n) { nombre = n; }
    // completa: void agregar(Curso* c), int cantidad(), void listar()
};
'''
SOL_R3 = START_R3.replace('''    // completa: void agregar(Curso* c), int cantidad(), void listar()
''', '''    void agregar(Curso* c) {
        if (c == nullptr) return;
        for (Curso* x : cursos)
            if (x == c) return;
        cursos.push_back(c);
    }
    int cantidad() { return cursos.size(); }
    void listar() {
        cout << nombre << ": ";
        if (cursos.empty()) cout << "sin cursos";
        for (int i = 0; i < (int)cursos.size(); ++i) {
            if (i) cout << ", ";
            cout << cursos[i]->getNombre();
        }
        cout << endl;
    }
''')
T_R3 = [{"n": "Agregar y listar", "main": 'Curso p("Prog2"), c("Calculo");\nEstudiante e("Ana");\ne.agregar(&p);\ne.agregar(&c);\ne.listar();\ncout << e.cantidad() << endl;', "out": "Ana: Prog2, Calculo\n2"},
        {"n": "Sin cursos", "main": 'Estudiante e("Luis");\ne.listar();', "out": "Luis: sin cursos"},
        {"n": "No repite ni acepta nullptr", "main": 'Curso p("Prog2");\nEstudiante e("Rosa");\ne.agregar(&p);\ne.agregar(&p);\ne.agregar(nullptr);\ncout << e.cantidad() << endl;', "out": "1"},
        {"n": "El curso existe sin el estudiante", "main": 'Curso p("Prog2");\n{\n    Estudiante e("Beto");\n    e.agregar(&p);\n}\ncout << p.getNombre() << endl;', "out": "Prog2"}]
B_ex.append(code_ex("p10c4", 3, "Agregación: un estudiante tiene cursos",
  "<p>Un <code>Estudiante</code> <b>tiene</b> varios <code>Curso</code>. Completa:</p><ul>"
  "<li><code>void agregar(Curso* c)</code>: lo agrega si no es <code>nullptr</code> y si no estaba ya.</li>"
  "<li><code>int cantidad()</code>: cuántos cursos tiene.</li>"
  "<li><code>void listar()</code>: imprime <code>Ana: Prog2, Calculo</code> (o <code>Ana: sin cursos</code>) y salta de línea.</li></ul>",
  START_R3, SOL_R3, T_R3,
  ["La agregación guarda punteros a objetos que existen aparte (<code>vector&lt;Curso*&gt;</code>) y tiene un método para agregarlos.",
   "Para no repetir, se compara la dirección: el mismo curso es el mismo puntero.",
   "El estudiante no hace <code>delete</code> de los cursos: no es su dueño."],
  "Recorre el vector antes de hacer push_back.", [["agreg"], ["agreg"], ["agreg"], ["agreg"]]))

# =====================================================================
# Ensamblar
# =====================================================================
topA = {"id": "w10mem", "name": "Sem. 10 · Arreglos de objetos y punteros dobles", "teo": A_teo, "form": A_form, "ex": A_ex, "lesson": A_lesson,
        "tools": [{"w": "mem", "t": "Objeto en el stack vs. objeto dinámico", "p": "Toca ▶ para avanzar línea por línea y mira dónde vive cada cosa.", "o": tool_simple},
                  {"w": "mem", "t": "Arreglo de objetos: new CPunto2D[5]", "p": "Un solo bloque con los 5 objetos seguidos.", "o": tool_arr},
                  {"w": "mem", "t": "Arreglo de punteros: new CPunto2D*[5]", "p": "Fíjate en el orden de liberación: primero cada objeto, después el arreglo.", "o": tool_dbl},
                  {"w": "mem", "t": "vector, vector de punteros y shared_ptr", "p": "Al llegar al final, ¿qué se liberó solo y qué no?", "o": tool_vec}]}
topB = {"id": "w10rel", "name": "Sem. 10 · Relaciones entre clases: asociación, composición y agregación", "teo": B_teo, "form": B_form, "ex": B_ex, "lesson": B_lesson}

ids = {t['id'] for t in d['topics']}
d['topics'] = [t for t in d['topics'] if t['id'] not in ('w10mem', 'w10rel')] + [topA, topB]
d['concepts'].update({
 "pptr": {"n": "Arreglo de punteros a objetos", "f": "<code>X** v = new X*[n]; v[i] = new X(…);</code>", "x": "Cada objeto se crea y se libera aparte; se usa con flecha.", "home": "w10mem"},
 "delarr": {"n": "delete vs. delete[]", "f": "<code>new</code> ↔ <code>delete</code> · <code>new[]</code> ↔ <code>delete[]</code>", "x": "Liberar de adentro hacia afuera y dejar nullptr.", "home": "w10mem"},
 "smart": {"n": "vector y shared_ptr", "f": "<code>vector&lt;X*&gt;</code> · <code>make_shared&lt;X&gt;(…)</code>", "x": "vector&lt;X*&gt; no libera los objetos; shared_ptr sí.", "home": "w10mem"},
 "asoc": {"n": "Asociación", "f": "«usa un» · <code>X* m_x;</code> + <code>setX(X*)</code>", "x": "Objetos independientes que trabajan juntos.", "home": "w10rel"},
 "compo": {"n": "Composición", "f": "«es parte de» · <code>: parte(…)</code>", "x": "Las partes nacen y mueren con el todo.", "home": "w10rel"},
 "agreg": {"n": "Agregación", "f": "«tiene un(os)» · <code>vector&lt;X*&gt;</code>", "x": "El todo agrupa objetos que existen sin él.", "home": "w10rel"},
 "uml": {"n": "Notación UML de relaciones", "f": "→ asociación · ◆ composición · ◇ agregación", "x": "El rombo va junto a la clase «todo».", "home": "w10rel"}})
allc = set(d['concepts'])
for t in (topA, topB):
    for e in t['ex']:
        for s in e['tags']:
            for k in s: assert k in allc, (e['id'], k)

# hoja de repaso
card = ('<div><b>Punteros dobles</b><br><code>X** v = new X*[n];</code> · <code>v[i] = new X(…);</code> · liberar <code>delete v[i]</code> → <code>delete[] v</code> → <code>v = nullptr</code></div>\n'
        '<div><b>vector y shared_ptr</b><br><code>vector&lt;X&gt;</code> solo · <code>vector&lt;X*&gt;</code> delete a cada uno · <code>make_shared&lt;X&gt;(…)</code> solo</div>\n'
        '<div><b>Relaciones</b><br>Asociación «usa un» <code>X*</code> + set · Composición «es parte de» <code>: parte(…)</code> · Agregación «tiene un» <code>vector&lt;X*&gt;</code></div>\n')
if 'Punteros dobles</b>' not in d['form']:
    k = d['form'].rindex('</div>')
    d['form'] = d['form'][:k] + card + d['form'][k:]

d['intro'] = ('Repaso acumulado con los temas ordenados por semana y todos abiertos desde el inicio. El examen final pone el énfasis en las semanas 9 en adelante (POO en C++): '
              'ya están la semana 9 (clases, constructores y destructores) y la 10 (arreglos de objetos, punteros dobles y relaciones entre clases, con un mapa de memoria para ver el stack y el heap). '
              'El simulacro tiene la mayoría de preguntas de esas semanas y una parte de repaso. Se actualiza cada vez que se agrega una semana nueva. Igual que en el parcial, elige si practicar en computadora o escrito.')

comp = {"name": "💻 En computadora", "desc": "Cuatro programas en 100 minutos, con compilador.", "minutes": 100, "slots": [
    {"pts": 4, "name": "Clases: atributos, constructores y métodos (sem. 9)", "pool": ["oo10", "oo11"]},
    {"pts": 5, "name": "Objetos dinámicos, arreglos de objetos y punteros dobles (sem. 9–10)", "pool": ["oo12", "oo13", "p10c1"]},
    {"pts": 7, "name": "Relaciones entre clases (sem. 10)", "pool": ["p10c2", "p10c3", "p10c4"]},
    {"pts": 4, "name": "Repaso: arreglos dinámicos y punteros", "pool": ["fpc_temps", "fpc_consumo", "far8"]}],
    "intro": "Simulacro acumulativo del examen final: la mayor parte es de las semanas 9 y 10 y una pregunta de repaso. Se actualiza cada semana."}
writ = {"name": "✍️ Escrito", "desc": "Opción múltiple (lectura de código y teoría) y dos programas sin compilar.", "minutes": 100, "slots": [
    {"pts": 1, "name": "Constructores sobrecargados y orden de destrucción", "pool": ["oo2", "oo3"]},
    {"pts": 1, "name": "Objetos dinámicos y this", "pool": ["oo4", "oo6", "p10t1"]},
    {"pts": 1, "name": "Encapsulamiento y lectura de clases", "pool": ["oo1", "oo5", "oo7", "oo8", "oo9"]},
    {"pts": 1, "name": "Memoria: new, delete y delete[] (sem. 10)", "pool": ["p10m1", "p10m2", "p10m3", "p10t4"]},
    {"pts": 1, "name": "Arreglos de objetos y punteros dobles (sem. 10)", "pool": ["p10t2", "p10t3", "p10t5", "p10o1"]},
    {"pts": 1, "name": "Tipos de relación y UML (sem. 10)", "pool": ["p10r1", "p10r2", "p10r3", "p10r4"]},
    {"pts": 1, "name": "Composición y agregación en código (sem. 10)", "pool": ["p10r5", "p10r6", "p10r7"]},
    {"pts": 1, "name": "Repaso: funciones, punteros, arreglos y vectores", "pool": ["ffu1", "fpu2", "fpu5", "fpu6", "far4", "fma3", "fve3", "fve4"]},
    {"pts": 6, "name": "Escribe una clase o un arreglo de objetos (a mano)", "pool": ["oo10", "oo11", "oo12", "oo13", "p10c1"]},
    {"pts": 6, "name": "Relaciones entre clases (a mano)", "pool": ["p10c2", "p10c3", "p10c4"]}],
    "intro": "Modalidad en papel: no puedes compilar. Al entregar se compila y se prueba tu código.", "noRun": True}
for v in (comp, writ): assert sum(s['pts'] for s in v['slots']) == 20
d['sim']['slots'] = comp['slots']; d['sim']['intro'] = comp['intro']; d['sim']['versions'] = [comp, writ]
allex = {e['id'] for t in d['topics'] for e in t['ex']} | {e['id'] for e in (d.get('simEx') or [])}
for v in d['sim']['versions']:
    for s in v['slots']:
        for i in s['pool']: assert i in allex, ('pool', i)

json.dump(d, open(F, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(F, 'a').write('\n')
json.dump({"mems": [mem1, mem2, mem3], "tools": [tool_simple, tool_arr, tool_dbl, tool_vec]}, open(os.path.join(tempfile.gettempdir(), 'p2_mems.json'), 'w'))
print('ok', len(A_ex), len(B_ex))
