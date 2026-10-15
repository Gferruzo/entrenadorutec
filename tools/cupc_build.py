#!/usr/bin/env python3
"""Cálculo I (UPC, 1AMA0758): construye cursos/cupc-rep.json y cursos/cupc-pr.json.
Cada respuesta se verifica con sympy antes de escribir (integrales derivando, valores exactos comparando).
Uso: python3 tools/cupc_build.py   (desde la raíz del repo o desde cualquier parte)"""
import json, os, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x, t, u = sp.symbols('x t u', real=True)
LOC = {'x': x, 't': t, 'u': u, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'sec': sp.sec, 'csc': sp.csc, 'cot': sp.cot,
       'asin': sp.asin, 'atan': sp.atan, 'log': sp.log, 'sqrt': sp.sqrt, 'exp': sp.exp, 'Abs': sp.Abs, 'pi': sp.pi, 'E': sp.E}

def S(a):
    """Convierte la sintaxis de la app (MX) a sympy."""
    s = a.replace('^', '**').replace('π', 'pi').replace('arcsen', 'asin').replace('arctan', 'atan')
    s = re.sub(r'\bsen\b', 'sin', s).replace('ln(', 'log(').replace('abs(', 'Abs(')
    s = re.sub(r'\be\b', 'E', s)
    return parse_expr(s, local_dict=LOC, transformations=standard_transformations)

def same(a, b, var=x, pts=(0.37, 0.71, 1.13, 1.41)):
    for p in pts:
        va, vb = complex(sp.N(a.subs(var, p))), complex(sp.N(b.subs(var, p)))
        if abs(va - vb) > 1e-7 * max(1, abs(vb)): return False
    return True

def chk_anti(ans, integrand, var=x, pts=(0.37, 0.71, 1.13, 1.41)):
    d = sp.diff(S(ans), var)
    assert same(d, integrand, var, pts), ('antiderivada mala', ans, sp.simplify(d - integrand))

def chk_val(ans, exact):
    v = sp.N(S(ans)); e = sp.N(exact)
    assert abs(complex(v) - complex(e)) < 1e-9, ('valor malo', ans, v, e)

# ---------- armado de ejercicios ----------
def ex(id, lvl, title, q, checks, steps, ans, hint, tags, chain=False):
    assert len(tags) == len(steps), (id, 'tags/steps')
    e = {"id": id, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans, "hint": hint,
         "fig": None, "draw": False, "open": False, "solfig": None, "tags": tags}
    if chain: e["chain"] = True
    return e

def mc(p, opts): return {"p": p, "o": opts}
def num(p, fs): return {"t": "num", "p": p, "f": fs}
def anti(label, a, var='x', dom=None, p='Escribe una antiderivada (puedes agregar + C).'):
    f = {"l": label, "a": a, "v": [var], "mode": "anti"}
    if dom: f["dom"] = {var: dom}
    return {"t": "expr", "p": p, "f": [f]}
def val(a, p='Escribe el valor exacto (puedes usar π, e, ln, sqrt).', label=None):
    f = {"a": a, "v": []}
    if label: f["l"] = label
    return {"t": "expr", "p": p, "f": [f]}
def eqx(label, a, var='x', dom=None, p='Escribe la expresión.'):
    f = {"l": label, "a": a, "v": [var], "mode": "eq"}
    if dom: f["dom"] = {var: dom}
    return {"t": "expr", "p": p, "f": [f]}
def graph(o): return "<div class=\"lw\" data-w=\"graph\" data-o='" + json.dumps(o, ensure_ascii=False) + "'></div>"

# =====================================================================
# BLOQUE REPASO
# =====================================================================
R = []
# --- rp1 derivadas y cadena
rp1 = []
assert same(S('15*x^4+2/x^2'), sp.diff(3*x**5 - 2/x, x))
rp1.append(ex("rp1e1", 1, "Potencias", "<p>Deriva \\(f(x)=3x^5-\\dfrac{2}{x}\\).</p>",
   [eqx("f′(x) =", "15*x^4+2/x^2", dom=[0.5, 3])],
   ["Escribe \\(\\frac2x=2x^{-1}\\).", "Regla de la potencia: \\((x^n)'=nx^{n-1}\\).", "\\(f'(x)=15x^4+2x^{-2}=15x^4+\\frac{2}{x^2}\\)."],
   "\\(15x^4+\\frac{2}{x^2}\\)", "Pasa 2/x a potencia negativa.", [["expo"], ["dpot"], ["dpot"]]))
assert same(S('3*cos(3*x)'), sp.diff(sp.sin(3*x), x))
rp1.append(ex("rp1e2", 1, "Regla de la cadena: seno", "<p>Deriva \\(y=\\operatorname{sen}(3x)\\).</p>",
   [eqx("y′ =", "3*cos(3*x)")],
   ["Afuera: seno → coseno. Adentro: \\(3x\\), su derivada es 3.", "\\(y'=\\cos(3x)\\cdot3\\)."],
   "\\(3\\cos(3x)\\)", "Deriva lo de afuera y multiplica por la derivada de lo de adentro.", [["cadena"], ["cadena"]]))
assert same(S('2*x*exp(x^2)'), sp.diff(sp.exp(x**2), x))
rp1.append(ex("rp1e3", 2, "Regla de la cadena: exponencial", "<p>Deriva \\(y=e^{x^2}\\).</p>",
   [eqx("y′ =", "2*x*exp(x^2)", p="Escribe la derivada (usa exp(…) o e^(…)).")],
   ["La derivada de \\(e^{u}\\) es \\(e^{u}\\cdot u'\\).", "Con \\(u=x^2\\): \\(y'=e^{x^2}\\cdot2x\\)."],
   "\\(2xe^{x^2}\\)", "Lo de adentro es x².", [["cadena"], ["cadena"]]))
assert same(S('1/x'), sp.diff(sp.log(5*x), x))
rp1.append(ex("rp1e4", 2, "Diferencial", "<p>Si \\(v=\\ln(5x)\\), entonces \\(dv=\\;?\\,dx\\).</p>",
   [eqx("dv/dx =", "1/x", dom=[0.5, 3])],
   ["\\((\\ln u)'=\\frac{u'}{u}\\): \\(\\frac{5}{5x}=\\frac1x\\).", "Por eso \\(dv=\\frac1x\\,dx\\). Las diferenciales son la base de la sustitución."],
   "\\(\\frac1x\\)", "El 5 se cancela.", [["cadena"], ["difer"]]))
rp1.append(ex("rp1e5", 1, "¿Qué dice la regla de la cadena?", "<p>Para \\(y=f(g(x))\\), ¿cuál es \\(y'\\)?</p>",
   [mc("Respuesta", ["\\(f'(g(x))\\cdot g'(x)\\)", "\\(f'(x)\\cdot g'(x)\\)", "\\(f'(g'(x))\\)", "\\(f(g'(x))\\cdot g(x)\\)", "\\(f'(g(x))+g'(x)\\)"])],
   ["Derivas la de afuera evaluada en la de adentro y multiplicas por la derivada de la de adentro.", "La regla de sustitución es esta regla al revés: por eso buscas «una función y su derivada»."],
   "\\(f'(g(x))\\cdot g'(x)\\)", "Afuera por adentro.", [["cadena"], ["cadena"]]))
R.append({"id": "rp1", "name": "Repaso · Derivadas y regla de la cadena",
  "teo": "<p>Integrar es derivar al revés, así que necesitas las derivadas a la mano:</p><ul><li>\\((x^n)'=nx^{n-1}\\) · \\((e^x)'=e^x\\) · \\((\\ln x)'=\\frac1x\\)</li><li>\\((\\operatorname{sen}x)'=\\cos x\\) · \\((\\cos x)'=-\\operatorname{sen}x\\) · \\((\\tan x)'=\\sec^2x\\) · \\((\\sec x)'=\\sec x\\tan x\\)</li></ul>"
         "<p><b>Regla de la cadena:</b> \\((f(g(x)))'=f'(g(x))\\cdot g'(x)\\). Ejemplo: \\((\\operatorname{sen}3x)'=3\\cos3x\\).</p>"
         "<p><b>Diferencial:</b> si \\(u=g(x)\\), entonces \\(du=g'(x)\\,dx\\). Ejemplo: \\(u=x^2+1\\Rightarrow du=2x\\,dx\\). Esto es lo que se usa en la regla de sustitución.</p>",
  "form": ["\\((x^n)'=nx^{n-1}\\)", "\\((e^u)'=e^u\\,u'\\) · \\((\\ln u)'=\\frac{u'}{u}\\)", "\\((\\operatorname{sen}u)'=\\cos u\\,u'\\) · \\((\\cos u)'=-\\operatorname{sen}u\\,u'\\)", "\\(u=g(x)\\Rightarrow du=g'(x)\\,dx\\)"],
  "lesson": "<h3>Idea central</h3><p>Si sabes derivar, puedes comprobar cualquier integral: derivas tu resultado y debe salir lo de adentro.</p><div class=\"ej\"><b>Ejemplo:</b> \\(\\int2x\\,e^{x^2}dx=e^{x^2}+C\\) porque \\((e^{x^2})'=2xe^{x^2}\\).</div><div class=\"err\"><b>Error común:</b> olvidar multiplicar por la derivada de lo de adentro.</div>",
  "ex": rp1})

# --- rp2 exponentes y raíces
rp2 = []
rp2.append(ex("rp2e1", 1, "Fracción a potencia", "<p>Escribe \\(\\dfrac{1}{x^3}=x^{n}\\). ¿Cuánto vale n?</p>", [val("-3", p="Escribe n.", label="n =")],
   ["\\(\\frac{1}{x^a}=x^{-a}\\).", "\\(n=-3\\)."], "\\(-3\\)", "El exponente sube con signo cambiado.", [["expo"], ["expo"]]))
rp2.append(ex("rp2e2", 1, "Raíz a potencia", "<p>Escribe \\(\\dfrac{1}{\\sqrt[3]{x^2}}=x^{n}\\). ¿Cuánto vale n?</p>", [val("-2/3", p="Escribe n (puede ser una fracción, como 1/2).", label="n =")],
   ["\\(\\sqrt[3]{x^2}=x^{2/3}\\).", "En el denominador cambia de signo: \\(x^{-2/3}\\)."], "\\(-\\frac23\\)", "Raíz n-ésima = exponente 1/n.", [["expo"], ["expo"]]))
rp2.append(ex("rp2e3", 1, "Producto de potencias", "<p>Escribe \\(x\\sqrt{x}=x^{n}\\). ¿Cuánto vale n?</p>", [val("3/2", p="Escribe n.", label="n =")],
   ["\\(\\sqrt x=x^{1/2}\\).", "\\(x^1\\cdot x^{1/2}=x^{3/2}\\): los exponentes se suman."], "\\(\\frac32\\)", "Se suman los exponentes.", [["expo"], ["expo"]]))
rp2.append(ex("rp2e4", 2, "Dividir término a término", "<p>¿Cómo queda \\(\\dfrac{x^5-2x+1}{x}\\) lista para integrar?</p>",
   [mc("Respuesta", ["\\(x^4-2+\\frac1x\\)", "\\(x^4-2x+1\\)", "\\(x^4-2+x\\)", "\\(x^5-2+\\frac1x\\)", "\\(x^4-\\frac2x+1\\)"])],
   ["Cada término del numerador se divide entre x: \\(\\frac{x^5}{x}-\\frac{2x}{x}+\\frac1x\\).", "Queda \\(x^4-2+\\frac1x\\), que se integra término a término."],
   "\\(x^4-2+\\frac1x\\)", "Divide cada término.", [["expo"], ["expo"]]))
R.append({"id": "rp2", "name": "Repaso · Exponentes y raíces",
  "teo": "<p>Antes de integrar casi siempre hay que <b>reescribir</b> la función como suma de potencias de x, porque \\(\\int x^n dx=\\frac{x^{n+1}}{n+1}+C\\) solo sirve con potencias.</p>"
         "<ul><li>\\(\\frac{1}{x^n}=x^{-n}\\)</li><li>\\(\\sqrt[n]{x^m}=x^{m/n}\\)</li><li>\\(x^a\\cdot x^b=x^{a+b}\\) · \\(\\frac{x^a}{x^b}=x^{a-b}\\)</li><li>Una fracción con un solo término abajo se reparte: \\(\\frac{a+b}{x}=\\frac ax+\\frac bx\\).</li></ul>",
  "form": ["\\(\\frac1{x^n}=x^{-n}\\)", "\\(\\sqrt[n]{x^m}=x^{m/n}\\)", "\\(x^ax^b=x^{a+b}\\) · \\(\\frac{x^a}{x^b}=x^{a-b}\\)"],
  "lesson": "<h3>Idea central</h3><p>Raíces y fracciones se convierten en exponentes para poder usar la regla de la potencia.</p><div class=\"err\"><b>Error común:</b> repartir una fracción con suma abajo: \\(\\frac{1}{x+1}\\neq\\frac1x+1\\).</div>",
  "ex": rp2})

# --- rp3 identidades
rp3 = []
rp3.append(ex("rp3e1", 1, "Bajar el cuadrado del seno", "<p>¿Cuál identidad convierte \\(\\operatorname{sen}^2x\\) en algo sin cuadrados?</p>",
   [mc("Respuesta", ["\\(\\operatorname{sen}^2x=\\frac{1-\\cos2x}{2}\\)", "\\(\\operatorname{sen}^2x=\\frac{1+\\cos2x}{2}\\)", "\\(\\operatorname{sen}^2x=2\\operatorname{sen}x\\cos x\\)", "\\(\\operatorname{sen}^2x=1+\\cos^2x\\)", "\\(\\operatorname{sen}^2x=\\operatorname{sen}(x^2)\\)"])],
   ["Es la identidad del ángulo mitad: con menos para el seno y más para el coseno.", "Se usa para integrar potencias pares de seno y coseno."],
   "\\(\\frac{1-\\cos2x}{2}\\)", "Seno lleva menos.", [["idtrig"], ["idtrig"]]))
rp3.append(ex("rp3e2", 1, "Tangente al cuadrado", "<p>Completa: \\(\\tan^2x=\\;?\\)</p>",
   [mc("Respuesta", ["\\(\\sec^2x-1\\)", "\\(1-\\sec^2x\\)", "\\(\\sec^2x+1\\)", "\\(\\csc^2x-1\\)", "\\(1-\\cos^2x\\)"])],
   ["De \\(1+\\tan^2x=\\sec^2x\\).", "Se usa con \\(\\int\\tan^m\\sec^n\\) y en la sustitución \\(x=a\\tan\\theta\\)."],
   "\\(\\sec^2x-1\\)", "Divide \\(\\operatorname{sen}^2+\\cos^2=1\\) entre \\(\\cos^2\\).", [["idtrig"], ["idtrig"]]))
rp3.append(ex("rp3e3", 1, "¿De quién es esta derivada?", "<p>Clasifica cada expresión según la función de la que es derivada.</p>",
   [{"t": "cls", "cats": ["sen x", "cos x", "tan x", "sec x"], "items": [
     {"x": "\\(\\cos x\\)", "c": 0}, {"x": "\\(-\\operatorname{sen}x\\)", "c": 1, "e": "La derivada del coseno lleva signo menos."},
     {"x": "\\(\\sec^2x\\)", "c": 2}, {"x": "\\(\\sec x\\tan x\\)", "c": 3}]}],
   ["Estas parejas son la tabla de integrales leída al revés.", "Por ejemplo \\(\\int\\sec^2x\\,dx=\\tan x+C\\)."],
   "sen → cos · cos → −sen · tan → sec² · sec → sec·tan", "", [["dtrig"], ["dtrig"]]))
rp3.append(ex("rp3e4", 2, "Ángulo doble", "<p>Si \\(\\operatorname{sen}\\theta=\\frac35\\) y θ es agudo, ¿cuánto vale \\(\\operatorname{sen}2\\theta\\)?</p>",
   [val("24/25", label="sen 2θ =")],
   ["\\(\\cos\\theta=\\sqrt{1-\\frac{9}{25}}=\\frac45\\).", "\\(\\operatorname{sen}2\\theta=2\\operatorname{sen}\\theta\\cos\\theta=2\\cdot\\frac35\\cdot\\frac45=\\frac{24}{25}\\)."],
   "\\(\\frac{24}{25}\\)", "Primero halla el coseno.", [["idtrig"], ["idtrig"]]))
R.append({"id": "rp3", "name": "Repaso · Identidades trigonométricas",
  "teo": "<p>Las integrales trigonométricas casi nunca se resuelven directo: primero se transforma con una identidad.</p>"
         "<ul><li>\\(\\operatorname{sen}^2x+\\cos^2x=1\\)</li><li>\\(1+\\tan^2x=\\sec^2x\\) · \\(1+\\cot^2x=\\csc^2x\\)</li>"
         "<li>\\(\\operatorname{sen}2x=2\\operatorname{sen}x\\cos x\\)</li><li>\\(\\operatorname{sen}^2x=\\frac{1-\\cos2x}{2}\\) · \\(\\cos^2x=\\frac{1+\\cos2x}{2}\\)</li></ul>",
  "form": ["\\(\\operatorname{sen}^2x+\\cos^2x=1\\)", "\\(1+\\tan^2x=\\sec^2x\\)", "\\(\\operatorname{sen}^2x=\\frac{1-\\cos2x}2\\) · \\(\\cos^2x=\\frac{1+\\cos2x}2\\)", "\\(\\operatorname{sen}2x=2\\operatorname{sen}x\\cos x\\)"],
  "lesson": "<h3>Idea central</h3><p>Pitagórica para cambiar seno por coseno (o tan por sec); ángulo mitad para bajar cuadrados.</p><div class=\"err\"><b>Error común:</b> confundir el signo de \\(\\frac{1\\pm\\cos2x}{2}\\): seno lleva menos.</div>",
  "ex": rp3})

# --- rp4 triángulo
rp4 = []
rp4.append(ex("rp4e1", 1, "Del triángulo a la secante", "<p>Si θ es agudo y \\(\\tan\\theta=\\frac43\\), ¿cuánto vale \\(\\sec\\theta\\)?</p>",
   [val("5/3", label="sec θ =")],
   ["Opuesto 4, adyacente 3 ⇒ hipotenusa \\(\\sqrt{16+9}=5\\).", "\\(\\sec\\theta=\\frac{\\text{hip}}{\\text{ady}}=\\frac53\\)."],
   "\\(\\frac53\\)", "Dibuja el triángulo y usa Pitágoras.", [["triang"], ["triang"]]))
assert same(S('sqrt(4-x^2)/2'), sp.sqrt(4 - x**2)/2)
rp4.append(ex("rp4e2", 2, "Con x en el triángulo", "<p>Si \\(\\operatorname{sen}\\theta=\\frac{x}{2}\\), escribe \\(\\cos\\theta\\) en términos de x.</p>",
   [eqx("cos θ =", "sqrt(4-x^2)/2", dom=[-1.5, 1.5])],
   ["Opuesto x, hipotenusa 2 ⇒ adyacente \\(\\sqrt{4-x^2}\\).", "\\(\\cos\\theta=\\frac{\\sqrt{4-x^2}}{2}\\)."],
   "\\(\\frac{\\sqrt{4-x^2}}2\\)", "Pitágoras: ady² = hip² − op².", [["triang"], ["triang"]]))
rp4.append(ex("rp4e3", 2, "Tangente con x", "<p>Si \\(\\tan\\theta=\\frac{x}{3}\\), escribe \\(\\sec\\theta\\) en términos de x.</p>",
   [eqx("sec θ =", "sqrt(9+x^2)/3", dom=[-3, 3])],
   ["Opuesto x, adyacente 3 ⇒ hipotenusa \\(\\sqrt{9+x^2}\\).", "\\(\\sec\\theta=\\frac{\\text{hip}}{\\text{ady}}=\\frac{\\sqrt{9+x^2}}{3}\\)."],
   "\\(\\frac{\\sqrt{9+x^2}}3\\)", "", [["triang"], ["triang"]]))
rp4.append(ex("rp4e4", 2, "Secante con x", "<p>Si \\(\\sec\\theta=\\frac{x}{2}\\) (θ agudo), ¿cuánto vale \\(\\tan\\theta\\)?</p>",
   [mc("Respuesta", ["\\(\\frac{\\sqrt{x^2-4}}{2}\\)", "\\(\\frac{2}{\\sqrt{x^2-4}}\\)", "\\(\\frac{\\sqrt{4-x^2}}{2}\\)", "\\(\\frac{x}{\\sqrt{x^2-4}}\\)", "\\(\\frac{\\sqrt{x^2+4}}{2}\\)"])],
   ["\\(\\sec\\theta=\\frac{\\text{hip}}{\\text{ady}}\\): hipotenusa x, adyacente 2.", "Opuesto \\(\\sqrt{x^2-4}\\) ⇒ \\(\\tan\\theta=\\frac{\\sqrt{x^2-4}}{2}\\)."],
   "\\(\\frac{\\sqrt{x^2-4}}2\\)", "", [["triang"], ["triang"]]))
R.append({"id": "rp4", "name": "Repaso · Triángulo rectángulo y razones trigonométricas",
  "teo": "<p>En un triángulo rectángulo con ángulo θ:</p><p>\\(\\operatorname{sen}\\theta=\\frac{\\text{op}}{\\text{hip}}\\) · \\(\\cos\\theta=\\frac{\\text{ady}}{\\text{hip}}\\) · \\(\\tan\\theta=\\frac{\\text{op}}{\\text{ady}}\\)</p>"
         "<p>\\(\\sec\\theta=\\frac{\\text{hip}}{\\text{ady}}\\) · \\(\\csc\\theta=\\frac{\\text{hip}}{\\text{op}}\\) · \\(\\cot\\theta=\\frac{\\text{ady}}{\\text{op}}\\)</p>"
         "<p>Si conoces una razón, dibujas el triángulo, hallas el lado que falta con Pitágoras y lees cualquier otra. Es exactamente el último paso de la <b>sustitución trigonométrica</b> (sem. 9).</p>",
  "form": ["sen = op/hip · cos = ady/hip · tan = op/ady", "sec = hip/ady · csc = hip/op · cot = ady/op", "Pitágoras: hip² = op² + ady²"],
  "lesson": "<h3>Idea central</h3><p>Una razón trigonométrica = dos lados del triángulo. Pitágoras te da el tercero.</p><div class=\"err\"><b>Error común:</b> poner la raíz en el lado equivocado: con \\(\\tan\\theta=\\frac x3\\) la raíz es la hipotenusa.</div>",
  "tools": [{"w": "tri", "t": "El triángulo de cada raíz", "p": "Toca cada tipo de raíz y mira qué lado es cada cosa.", "o": {"a": 3}}],
  "ex": rp4})

# =====================================================================
# BLOQUE PRÁCTICA
# =====================================================================
P = []
# --- s7a antiderivadas
s7a = []
s7a.append(ex("s7a1", 1, "¿Cuál no es antiderivada?", "<p>¿Cuál de estas funciones <b>no</b> es una antiderivada de \\(f(x)=3x^2\\)?</p>",
   [mc("Respuesta", ["\\(6x\\)", "\\(x^3\\)", "\\(x^3+5\\)", "\\(x^3-\\pi\\)", "\\(x^3+100\\)"])],
   ["F es antiderivada de f si \\(F'=f\\). Todas las \\(x^3+C\\) cumplen \\((x^3+C)'=3x^2\\).", "\\(6x\\) es la <b>derivada</b> de \\(3x^2\\), no su antiderivada."],
   "\\(6x\\)", "Deriva cada opción.", [["antider"], ["antider"]]))
I1 = 6*x - 3/x + 5*sp.cos(x); chk_anti("3*x^2-3*ln(abs(x))+5*sen(x)", I1)
s7a.append(ex("s7a2", 1, "Término a término", "<p>Calcula \\(\\int\\left(6x-\\frac3x+5\\cos x\\right)dx\\).</p>",
   [anti("∫ … dx =", "3*x^2-3*ln(abs(x))+5*sen(x)", dom=[0.4, 3])],
   ["Propiedades: la integral de una suma es la suma de integrales y las constantes salen.", "\\(6\\int x\\,dx-3\\int\\frac1x dx+5\\int\\cos x\\,dx\\).", "\\(=3x^2-3\\ln|x|+5\\operatorname{sen}x+C\\)."],
   "\\(3x^2-3\\ln|x|+5\\operatorname{sen}x+C\\)", "\\(\\int\\frac1x dx=\\ln|x|\\).", [["propind"], ["propind"], ["tabla"]]))
chk_anti("x^5/5-2*x+ln(abs(x))", (x**5 - 2*x + 1)/x)
s7a.append(ex("s7a3", 2, "Primero divide", "<p>Calcula \\(\\int\\dfrac{x^5-2x+1}{x}\\,dx\\).</p>",
   [anti("∫ … dx =", "x^5/5-2*x+ln(abs(x))", dom=[0.4, 3])],
   ["Divide cada término entre x: \\(x^4-2+\\frac1x\\).", "Integra: \\(\\frac{x^5}{5}-2x+\\ln|x|+C\\)."],
   "\\(\\frac{x^5}5-2x+\\ln|x|+C\\)", "No hay regla del cociente para integrar: simplifica antes.", [["expo"], ["tabla"]]))
chk_anti("5*x^(7/5)+40*x^(1/5)", 7*x**sp.Rational(2, 5) + 8*x**sp.Rational(-4, 5))
s7a.append(ex("s7a4", 2, "Exponentes fraccionarios", "<p>Halla la antiderivada general de \\(f(x)=7x^{2/5}+8x^{-4/5}\\).</p>",
   [anti("F(x) =", "5*x^(7/5)+40*x^(1/5)", dom=[0.4, 3])],
   ["\\(\\int x^n dx=\\frac{x^{n+1}}{n+1}\\): \\(7\\cdot\\frac{x^{7/5}}{7/5}=5x^{7/5}\\).", "\\(8\\cdot\\frac{x^{1/5}}{1/5}=40x^{1/5}\\). Resultado: \\(5x^{7/5}+40x^{1/5}+C\\)."],
   "\\(5x^{7/5}+40x^{1/5}+C\\)", "Dividir entre 7/5 es multiplicar por 5/7.", [["tabla"], ["tabla"]]))
chk_anti("-2*cos(t)-tan(t)", 2*sp.sin(t) - sp.sec(t)**2, var=t)
s7a.append(ex("s7a5", 1, "Trigonométricas", "<p>Calcula \\(\\int\\left(2\\operatorname{sen}t-\\sec^2t\\right)dt\\).</p>",
   [anti("∫ … dt =", "-2*cos(t)-tan(t)", var='t', dom=[0.2, 1.2])],
   ["\\(\\int\\operatorname{sen}t\\,dt=-\\cos t\\) y \\(\\int\\sec^2t\\,dt=\\tan t\\).", "\\(-2\\cos t-\\tan t+C\\)."],
   "\\(-2\\cos t-\\tan t+C\\)", "Ojo con el signo de la integral del seno.", [["tabla"], ["tabla"]]))
fx = x**5 - x**3 + 4*x + 6
assert sp.diff(fx, x) == 5*x**4 - 3*x**2 + 4 and fx.subs(x, -1) == 2
s7a.append(ex("s7a6", 2, "Con condición inicial", "<p>Encuentra f si \\(f'(x)=5x^4-3x^2+4\\) y \\(f(-1)=2\\).</p>",
   [eqx("f(x) =", "x^5-x^3+4*x+6", dom=[-2, 2])],
   ["Integra: \\(f(x)=x^5-x^3+4x+C\\).", "\\(f(-1)=-1+1-4+C=2\\Rightarrow C=6\\).", "\\(f(x)=x^5-x^3+4x+6\\)."],
   "\\(f(x)=x^5-x^3+4x+6\\)", "La condición sirve para hallar C.", [["antider"], ["cini"], ["cini"]]))
s7a.append(ex("s7a7", 2, "De la velocidad a la posición", "<p>Una partícula se mueve con velocidad \\(v(t)=2t\\) m/s y en \\(t=0\\) está en \\(s=3\\) m. ¿Dónde está?</p>",
   [eqx("s(t) =", "t^2+3", var='t', dom=[0, 4])],
   ["La posición es una antiderivada de la velocidad: \\(s(t)=t^2+C\\).", "\\(s(0)=C=3\\) ⇒ \\(s(t)=t^2+3\\). La antiderivada reconstruye el movimiento a partir de su tasa de cambio."],
   "\\(s(t)=t^2+3\\)", "", [["antider"], ["cini"]]))
P.append({"id": "s7a", "name": "Sem. 7 · Antiderivada e integral indefinida",
  "teo": "<p>F es una <b>antiderivada</b> de f si \\(F'(x)=f(x)\\). Si hay una, hay infinitas: todas difieren en una constante. La <b>integral indefinida</b> es esa familia:</p>"
         "<p style='text-align:center'>\\(\\int f(x)\\,dx=F(x)+C\\)</p>"
         "<p><b>Tabla básica:</b> \\(\\int x^n dx=\\frac{x^{n+1}}{n+1}+C\\) (\\(n\\neq-1\\)) · \\(\\int\\frac1x dx=\\ln|x|+C\\) · \\(\\int e^xdx=e^x+C\\) · \\(\\int\\cos x\\,dx=\\operatorname{sen}x+C\\) · \\(\\int\\operatorname{sen}x\\,dx=-\\cos x+C\\) · \\(\\int\\sec^2x\\,dx=\\tan x+C\\) · \\(\\int\\sec x\\tan x\\,dx=\\sec x+C\\) · \\(\\int\\frac{dx}{1+x^2}=\\arctan x+C\\) · \\(\\int\\frac{dx}{\\sqrt{1-x^2}}=\\operatorname{arcsen}x+C\\).</p>"
         "<p><b>Propiedades:</b> \\(\\int[f\\pm g]=\\int f\\pm\\int g\\) y \\(\\int kf=k\\int f\\). <b>No</b> hay regla para productos ni cocientes: hay que simplificar antes (o usar sustitución).</p>"
         "<p>Si te dan un dato como \\(f(-1)=2\\), lo usas al final para hallar C.</p>",
  "form": ["\\(F'=f\\Leftrightarrow\\int f\\,dx=F+C\\)", "\\(\\int x^ndx=\\frac{x^{n+1}}{n+1}+C\\ (n\\neq-1)\\)", "\\(\\int\\frac1xdx=\\ln|x|+C\\) · \\(\\int e^xdx=e^x+C\\)", "\\(\\int\\cos x=\\operatorname{sen}x\\) · \\(\\int\\operatorname{sen}x=-\\cos x\\)", "\\(\\int\\sec^2x=\\tan x\\) · \\(\\int\\frac{dx}{1+x^2}=\\arctan x\\)"],
  "lesson": "<h3>Idea central</h3><p>Integrar es preguntarse «¿qué función, al derivarla, da esto?». Siempre puedes comprobarlo derivando.</p><div class=\"ej\"><b>Ejemplo:</b> \\(\\int(4x^3)dx=x^4+C\\) porque \\((x^4)'=4x^3\\).</div><div class=\"err\"><b>Error común:</b> olvidar la + C o integrar un cociente «dividiendo integrales».</div>",
  "ex": s7a})

# --- s7b integral definida como área
s7b = []
g1 = {"f": "x-1", "xr": [-0.5, 3.5], "yr": [-1.5, 2.5], "fs": [{"f": "x-1", "cl": "f", "l": "y = x − 1"}], "id": "g71"}
assert sp.integrate(x - 1, (x, 0, 3)) == sp.Rational(3, 2)
s7b.append(ex("s7b1", 1, "Con triángulos", "<p>Evalúa \\(\\int_0^3(x-1)\\,dx\\) usando áreas.</p>" + graph(g1),
   [num("Valor", [{"l": "∫ =", "a": 1.5}])],
   ["De 0 a 1 la recta está bajo el eje: triángulo de área \\(\\frac{1\\cdot1}2=\\frac12\\) que <b>resta</b>.", "De 1 a 3 está sobre el eje: triángulo de área \\(\\frac{2\\cdot2}2=2\\) que <b>suma</b>.", "\\(2-\\frac12=\\frac32\\)."],
   "\\(\\frac32\\)", "Lo que está bajo el eje resta.", [["areasig"], ["areasig"], ["areasig"]]))
assert sp.integrate(sp.sqrt(4 - x**2), (x, -2, 2)) == 2*sp.pi
s7b.append(ex("s7b2", 2, "Semicírculo", "<p>Evalúa \\(\\int_{-2}^{2}\\sqrt{4-x^2}\\,dx\\) interpretándola como un área.</p>" +
   graph({"f": "sqrt(4-x^2)", "xr": [-2.5, 2.5], "yr": [-0.5, 2.5], "fs": [{"f": "sqrt(4-x^2)", "cl": "f"}], "id": "g72"}),
   [val("2*π")],
   ["\\(y=\\sqrt{4-x^2}\\) es la mitad de arriba de la circunferencia de radio 2.", "Área del semicírculo: \\(\\frac{\\pi\\cdot2^2}{2}=2\\pi\\)."],
   "\\(2\\pi\\)", "Eleva al cuadrado: \\(x^2+y^2=4\\).", [["areasig"], ["areasig"]]))
s7b.append(ex("s7b3", 2, "Mueve b hasta que se anule", "<p>Con \\(f(x)=x-1\\) y \\(a=0\\), mueve b hasta que \\(\\int_0^b(x-1)\\,dx=0\\).</p>",
   [{"t": "acum", "p": "Mueve b", "f": "x-1", "F": "x^2/2-x", "xr": [0, 4], "yr": [-1.5, 3], "a": 0, "b0": 3.5, "ans": 2, "tol": 0.051, "step": 0.05, "fl": "x − 1",
     "e": "Busca el punto donde lo verde (que suma) es igual a lo rojo (que resta)."}],
   ["Lo rojo de 0 a 1 mide \\(\\frac12\\).", "Lo verde de 1 a b mide \\(\\frac{(b-1)^2}{2}\\); se iguala a \\(\\frac12\\) cuando \\(b=2\\)."],
   "\\(b=2\\)", "La integral es área neta.", [["areasig"], ["areasig"]]))
s7b.append(ex("s7b4", 1, "¿Qué mide la integral?", "<p>Si f toma valores positivos y negativos en [a; b], \\(\\int_a^bf(x)\\,dx\\) es…</p>",
   [mc("Respuesta", ["el área sobre el eje menos el área bajo el eje", "la suma de todas las áreas, sin signo", "siempre un número positivo", "el área bajo el eje menos el área sobre el eje", "una función de x"])],
   ["La integral definida es un <b>área neta</b>: lo de arriba suma y lo de abajo resta.", "Es un número (no depende de x). Si quieres el área total sin signo, tienes que separar los tramos."],
   "Área sobre el eje − área bajo el eje", "", [["areasig"], ["defi"]]))
s7b.append(ex("s7b5", 2, "¿Positiva, negativa o cero?", "<p>Clasifica cada integral sin calcularla.</p>",
   [{"t": "cls", "cats": ["Positiva", "Negativa", "Cero"], "items": [
     {"x": "\\(\\int_0^{\\pi}\\operatorname{sen}x\\,dx\\)", "c": 0, "e": "El seno es positivo entre 0 y π."},
     {"x": "\\(\\int_{-1}^{1}x^2\\,dx\\)", "c": 0, "e": "x² nunca es negativa."},
     {"x": "\\(\\int_{\\pi}^{2\\pi}\\operatorname{sen}x\\,dx\\)", "c": 1, "e": "El seno es negativo entre π y 2π."},
     {"x": "\\(\\int_0^{2}(x-3)\\,dx\\)", "c": 1, "e": "x − 3 es negativa en [0; 2]."},
     {"x": "\\(\\int_0^{2\\pi}\\operatorname{sen}x\\,dx\\)", "c": 2, "e": "La parte de arriba y la de abajo son iguales."},
     {"x": "\\(\\int_{-1}^{1}x^3\\,dx\\)", "c": 2, "e": "x³ es impar: lo de la izquierda cancela lo de la derecha."}]}],
   ["Mira el signo de f en el intervalo.", "Si hay partes arriba y abajo iguales (funciones impares en intervalos simétricos), se cancelan."],
   "Clasificación correcta", "Dibuja la función mentalmente.", [["areasig"], ["areasig"]]))
assert sp.integrate(2 - x, (x, 0, 4)) == 0
s7b.append(ex("s7b6", 1, "Áreas que se cancelan", "<p>Evalúa \\(\\int_0^4(2-x)\\,dx\\) con áreas.</p>",
   [num("Valor", [{"l": "∫ =", "a": 0}])],
   ["De 0 a 2: triángulo sobre el eje de área 2.", "De 2 a 4: triángulo bajo el eje de área 2. Neto: \\(2-2=0\\)."],
   "\\(0\\)", "", [["areasig"], ["areasig"]]))
P.append({"id": "s7b", "name": "Sem. 7 · Integral definida como área",
  "teo": "<p>La <b>integral definida</b> \\(\\int_a^bf(x)\\,dx\\) es un <b>número</b>: si f es positiva, el área entre la curva, el eje x y las rectas x = a, x = b.</p>"
         "<p>Si f toma valores negativos, esa parte <b>resta</b>: la integral es el <b>área neta</b> \\(A_1-A_2+A_3\\dots\\)</p>"
         "<p>Existe siempre que f sea continua (o tenga un número finito de saltos). Cuando la figura es conocida (triángulos, trapecios, círculos), puedes calcularla sin fórmulas.</p>"
         "<p>Diferencia clave: la indefinida es una <b>familia de funciones</b> (\\(F(x)+C\\)); la definida es <b>un número</b>.</p>",
  "form": ["\\(\\int_a^bf\\,dx\\) = área sobre el eje − área bajo el eje", "Indefinida: funciones · definida: número", "Triángulo \\(\\frac{bh}2\\) · trapecio \\(\\frac{(B+b)h}2\\) · semicírculo \\(\\frac{\\pi r^2}2\\)"],
  "lesson": "<h3>Idea central</h3><p>Mira la gráfica: arriba suma, abajo resta.</p><div class=\"err\"><b>Error común:</b> sumar todas las áreas como positivas cuando la pregunta es la integral.</div>",
  "tools": [{"w": "acum", "t": "Acumulador: área con signo", "p": "Mueve a y b. Lo verde suma, lo rojo resta.", "o": {"f": "x-1", "F": "x^2/2-x", "xr": [-1, 4], "yr": [-2.5, 3.5], "a": 0, "b": 3, "fl": "x − 1"}},
            {"w": "acum", "t": "Con seno", "p": "Prueba de 0 a π, de π a 2π y de 0 a 2π.", "o": {"f": "sin(x)", "F": "-cos(x)", "xr": [0, 7], "yr": [-1.5, 1.5], "a": 0, "b": 3.14, "step": 0.01, "fl": "sen x"}}],
  "ex": s7b})

# --- s8a propiedades
s8a = []
s8a.append(ex("s8a1", 1, "Partir el intervalo", "<p>Si \\(\\int_0^7f(x)\\,dx=12\\) y \\(\\int_0^5f(x)\\,dx=9\\), halla \\(\\int_5^7f(x)\\,dx\\).</p>",
   [num("Valor", [{"l": "∫ =", "a": 3}])],
   ["Propiedad aditiva: \\(\\int_0^5f+\\int_5^7f=\\int_0^7f\\).", "\\(\\int_5^7f=12-9=3\\)."], "\\(3\\)", "", [["aditiva"], ["aditiva"]]))
s8a.append(ex("s8a2", 1, "Linealidad", "<p>Si \\(\\int_8^{12}f(x)\\,dx=32\\) y \\(\\int_8^{12}g(x)\\,dx=4\\), calcula \\(\\int_8^{12}[3f(x)+2g(x)]\\,dx\\).</p>",
   [num("Valor", [{"l": "∫ =", "a": 104}])],
   ["Se separa la suma y salen las constantes: \\(3\\int f+2\\int g\\).", "\\(3(32)+2(4)=104\\)."], "\\(104\\)", "", [["lineal"], ["lineal"]]))
s8a.append(ex("s8a3", 2, "Una sola integral", "<p>Escribe como una sola integral: \\(\\int_{-2}^{2}f\\,dx+\\int_{2}^{5}f\\,dx-\\int_{-2}^{-1}f\\,dx\\)</p>",
   [mc("Respuesta", ["\\(\\int_{-1}^{5}f\\,dx\\)", "\\(\\int_{-2}^{5}f\\,dx\\)", "\\(\\int_{-1}^{2}f\\,dx\\)", "\\(\\int_{-2}^{-1}f\\,dx\\)", "\\(\\int_{2}^{5}f\\,dx\\)"])],
   ["Las dos primeras se juntan: \\(\\int_{-2}^{5}f\\).", "Quitar \\(\\int_{-2}^{-1}f\\) deja \\(\\int_{-1}^{5}f\\)."], "\\(\\int_{-1}^{5}f\\,dx\\)", "Pega los intervalos.", [["aditiva"], ["aditiva"]]))
s8a.append(ex("s8a4", 1, "Constante", "<p>Calcula \\(\\int_2^7 4\\,dx\\).</p>", [num("Valor", [{"l": "∫ =", "a": 20}])],
   ["\\(\\int_a^bc\\,dx=c(b-a)\\): un rectángulo.", "\\(4(7-2)=20\\)."], "\\(20\\)", "", [["const"], ["const"]]))
s8a.append(ex("s8a5", 2, "¿Tiene razón?", "<p>Una estudiante afirma que \\(\\int_a^bf(x)\\,dx=\\int_b^af(x)\\,dx\\). ¿Es correcto?</p>",
   [mc("Respuesta", ["No: al invertir los límites cambia el signo, \\(\\int_a^bf=-\\int_b^af\\)", "Sí, el área es la misma", "Sí, siempre que f sea continua", "No: la segunda siempre vale 0", "Solo si a < b"])],
   ["Propiedad 1: \\(\\int_a^bf=-\\int_b^af\\).", "Solo serían iguales si la integral vale 0."], "Cambia el signo", "", [["invertir"], ["invertir"]]))
s8a.append(ex("s8a6", 1, "Mismo límite", "<p>Calcula \\(\\int_3^3(x^2+e^x)\\,dx\\).</p>", [num("Valor", [{"l": "∫ =", "a": 0}])],
   ["\\(\\int_a^af=0\\): no hay ancho.", "No hace falta integrar."], "\\(0\\)", "", [["invertir"], ["invertir"]]))
s8a.append(ex("s8a7", 2, "Invertir y multiplicar", "<p>Si \\(\\int_1^4f(x)\\,dx=5\\), ¿cuánto vale \\(\\int_4^1 2f(x)\\,dx\\)?</p>",
   [num("Valor", [{"l": "∫ =", "a": -10}])],
   ["Sale el 2: \\(2\\int_4^1f\\).", "Invertir límites cambia el signo: \\(2(-5)=-10\\)."], "\\(-10\\)", "", [["lineal"], ["invertir"]]))
P.append({"id": "s8a", "name": "Sem. 8 · Propiedades de la integral definida",
  "teo": "<ol><li>\\(\\int_a^bf=-\\int_b^af\\) (invertir límites cambia el signo)</li><li>\\(\\int_a^af=0\\)</li><li>\\(\\int_a^bc\\,dx=c(b-a)\\)</li>"
         "<li>\\(\\int_a^b[f\\pm g]=\\int_a^bf\\pm\\int_a^bg\\)</li><li>\\(\\int_a^bcf=c\\int_a^bf\\)</li><li>\\(\\int_a^cf+\\int_c^bf=\\int_a^bf\\) (aditividad)</li></ol>"
         "<p>La aditividad se ve en el dibujo: el área de a a c más la de c a b es la de a a b. Sirve en física: la distancia total es la suma de las distancias de cada tramo.</p>",
  "form": ["\\(\\int_a^b=-\\int_b^a\\) · \\(\\int_a^a=0\\)", "\\(\\int_a^bc\\,dx=c(b-a)\\)", "\\(\\int(f\\pm g)=\\int f\\pm\\int g\\) · \\(\\int cf=c\\int f\\)", "\\(\\int_a^c+\\int_c^b=\\int_a^b\\)"],
  "lesson": "<h3>Idea central</h3><p>Con las propiedades calculas integrales sin conocer f: solo combinas los datos.</p><div class=\"err\"><b>Error común:</b> olvidar el signo al invertir límites.</div>",
  "tools": [{"w": "acum", "t": "Aditividad en vivo", "p": "Pon a = 0 y b = 2, luego a = 2 y b = 4, y compáralo con a = 0, b = 4.", "o": {"f": "x^2-2*x", "F": "x^3/3-x^2", "xr": [-1, 4.5], "yr": [-2, 8], "a": 0, "b": 4, "fl": "x² − 2x"}}],
  "ex": s8a})

# --- s8b TFC
s8b = []
def tfc(id, lvl, title, q, ans, exact, steps, tags, hint=""):
    chk_val(ans, exact)
    return ex(id, lvl, title, q, [val(ans)], steps, "\\(" + sp.latex(exact).replace('\\log', '\\ln') + "\\)", hint, tags)
s8b.append(tfc("s8b1", 1, "Potencia", "<p>Calcula \\(\\int_{-1}^{5}x^2\\,dx\\).</p>", "42", sp.integrate(x**2, (x, -1, 5)),
   ["\\(F(x)=\\frac{x^3}{3}\\).", "\\(F(5)-F(-1)=\\frac{125}3-\\left(-\\frac13\\right)=\\frac{126}3=42\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b2", 1, "Logaritmo", "<p>Calcula \\(\\int_1^3\\frac1x\\,dx\\).</p>", "ln(3)", sp.log(3),
   ["\\(F(x)=\\ln|x|\\).", "\\(\\ln3-\\ln1=\\ln3\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b3", 1, "Arcotangente", "<p>Calcula \\(\\int_0^1\\frac{1}{1+x^2}\\,dx\\).</p>", "π/4", sp.pi/4,
   ["\\(F(x)=\\arctan x\\).", "\\(\\arctan1-\\arctan0=\\frac\\pi4\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b4", 1, "Potencia negativa", "<p>Calcula \\(\\int_1^2\\frac{1}{x^2}\\,dx\\).</p>", "1/2", sp.Rational(1, 2),
   ["\\(x^{-2}\\Rightarrow F(x)=-\\frac1x\\).", "\\(-\\frac12-(-1)=\\frac12\\)."], [["expo", "tfc"], ["tfc"]]))
s8b.append(tfc("s8b5", 1, "Exponencial", "<p>Calcula \\(\\int_0^6e^x\\,dx\\).</p>", "e^6-1", sp.exp(6) - 1,
   ["\\(F(x)=e^x\\).", "\\(e^6-e^0=e^6-1\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b6", 2, "Polinomio", "<p>Calcula \\(\\int_0^3(x^3-6x)\\,dx\\).</p>", "-27/4", sp.integrate(x**3 - 6*x, (x, 0, 3)),
   ["\\(F(x)=\\frac{x^4}4-3x^2\\).", "\\(F(3)-F(0)=\\frac{81}4-27=-\\frac{27}4\\). Sale negativo: hay más área bajo el eje."], [["tfc"], ["tfc", "areasig"]]))
s8b.append(ex("s8b7", 2, "Con la derivada", "<p>f(1) = 7, f′ es continua y \\(\\int_1^5f'(x)\\,dx=23\\). Halla f(5).</p>",
   [num("Valor", [{"l": "f(5) =", "a": 30}])],
   ["TFC: \\(\\int_1^5f'(x)\\,dx=f(5)-f(1)\\).", "\\(f(5)-7=23\\Rightarrow f(5)=30\\)."], "\\(30\\)", "Una antiderivada de f′ es f.", [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b8", 2, "Con t", "<p>Calcula \\(\\int_1^4(t^2-t-6)\\,dt\\).</p>", "-9/2", sp.integrate(t**2 - t - 6, (t, 1, 4)),
   ["\\(F(t)=\\frac{t^3}3-\\frac{t^2}2-6t\\).", "\\(F(4)-F(1)=-\\frac{32}{3}-\\left(-\\frac{37}{6}\\right)=-\\frac92\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b9", 1, "Un arco del seno", "<p>Calcula el área bajo un arco de \\(y=\\operatorname{sen}x\\) (de 0 a π).</p>", "2", sp.integrate(sp.sin(x), (x, 0, sp.pi)),
   ["\\(F(x)=-\\cos x\\).", "\\(-\\cos\\pi-(-\\cos0)=1+1=2\\)."], [["tfc"], ["tfc"]]))
s8b.append(tfc("s8b10", 2, "Seno más coseno", "<p>Calcula \\(\\int_0^{\\pi/3}(\\operatorname{sen}\\theta+\\cos\\theta)\\,d\\theta\\).</p>", "(1+sqrt(3))/2", (1 + sp.sqrt(3))/2,
   ["\\(F(\\theta)=-\\cos\\theta+\\operatorname{sen}\\theta\\).", "\\(F(\\frac\\pi3)-F(0)=\\left(-\\frac12+\\frac{\\sqrt3}2\\right)-(-1)=\\frac{1+\\sqrt3}{2}\\approx1{,}37\\)."], [["tfc"], ["tfc"]]))
P.append({"id": "s8b", "name": "Sem. 8 · Teorema fundamental del cálculo (parte 2)",
  "teo": "<p>Si f es continua en [a; b] y F es <b>cualquier</b> antiderivada de f:</p><p style='text-align:center'>\\(\\int_a^bf(x)\\,dx=F(x)\\Big|_a^b=F(b)-F(a)\\)</p>"
         "<p>Une las dos mitades del cálculo: el área (integral) se calcula con una antiderivada, sin sumas de Riemann. La C se cancela al restar, por eso no se pone.</p>"
         "<p>Otra forma: \\(\\int_a^bF'(x)\\,dx=F(b)-F(a)\\): integrar una tasa de cambio da el <b>cambio total</b>. Por ejemplo, integrar la velocidad da el desplazamiento.</p>",
  "form": ["\\(\\int_a^bf=F(b)-F(a)\\), con \\(F'=f\\)", "\\(\\int_a^bF'(x)dx=F(b)-F(a)\\)", "En definidas no va + C"],
  "lesson": "<h3>Idea central</h3><p>Halla una antiderivada, evalúa arriba, evalúa abajo y resta.</p><div class=\"ej\"><b>Ejemplo:</b> \\(\\int_0^2x\\,dx=\\frac{x^2}2\\Big|_0^2=2-0=2\\).</div><div class=\"err\"><b>Error común:</b> restar al revés \\(F(a)-F(b)\\) o evaluar mal los signos de F(a) cuando a es negativo.</div>",
  "tools": [{"w": "acum", "t": "Área = F(b) − F(a)", "p": "Mueve a y b: la suma de áreas siempre coincide con F(b) − F(a).", "o": {"f": "x^2", "F": "x^3/3", "xr": [-2, 4], "yr": [-1, 12], "a": -1, "b": 3, "fl": "x²"}}],
  "ex": s8b})

# --- s9a sustitución
s9a = []
s9a.append(ex("s9a1", 1, "¿Qué u elijo? (1)", "<p>Para calcular la integral, ¿qué conviene llamar u?</p>",
   [{"t": "usub", "p": "Elige u", "int": "\\int x^4(x^5+3)^6\\,dx", "opts": [
      {"u": "x^5+3", "du": "5x^4\\,dx", "new": "\\frac15\\int u^6\\,du", "ok": True, "e": "La derivada de lo de adentro (x⁴) ya está afuera."},
      {"u": "x^4", "du": "4x^3\\,dx", "new": "\\int u\\,(x^5+3)^6\\frac{du}{4x^3}", "ok": False, "e": "Siguen quedando x sueltas."},
      {"u": "(x^5+3)^6", "du": "30x^4(x^5+3)^5\\,dx", "new": "\\frac1{30}\\int\\frac{u\\,du}{(x^5+3)^5}", "ok": False, "e": "Es demasiado: deja una potencia de x⁵ + 3 sin resolver."}]}],
   ["Busca una función de adentro cuya derivada aparezca afuera.", "\\(u=x^5+3\\), \\(du=5x^4dx\\): queda \\(\\frac15\\int u^6du\\)."],
   "\\(u=x^5+3\\)", "Lo de adentro del paréntesis.", [["elegu"], ["sust"]]))
s9a.append(ex("s9a2", 2, "¿Qué u elijo? (2)", "<p>¿Qué conviene llamar u?</p>",
   [{"t": "usub", "p": "Elige u", "int": "\\int\\frac{\\ln x}{x}\\,dx", "opts": [
      {"u": "\\ln x", "du": "\\frac1x\\,dx", "new": "\\int u\\,du", "ok": True, "e": "1/x es justo la derivada de ln x."},
      {"u": "x", "du": "dx", "new": "\\int\\frac{\\ln u}{u}\\,du", "ok": False, "e": "No cambia nada: es la misma integral."},
      {"u": "\\frac1x", "du": "-\\frac1{x^2}\\,dx", "new": "-\\int\\ln x\\cdot x\\,du", "ok": False, "e": "Quedan x y ln x sin resolver."}]}],
   ["La derivada de ln x es 1/x, que está en la integral.", "\\(\\int u\\,du=\\frac{u^2}2=\\frac{(\\ln x)^2}2+C\\)."],
   "\\(u=\\ln x\\)", "", [["elegu"], ["sust"]]))
chk_anti("(2*x+1)^6/12", (2*x + 1)**5)
s9a.append(ex("s9a3", 1, "Lineal adentro", "<p>Calcula \\(\\int(2x+1)^5\\,dx\\).</p>", [anti("∫ … dx =", "(2*x+1)^6/12")],
   ["\\(u=2x+1\\), \\(du=2dx\\Rightarrow dx=\\frac{du}2\\).", "\\(\\frac12\\int u^5du=\\frac{u^6}{12}\\).", "\\(\\frac{(2x+1)^6}{12}+C\\)."],
   "\\(\\frac{(2x+1)^6}{12}+C\\)", "No olvides dividir entre 2.", [["sust"], ["sust"], ["sust"]]))
chk_anti("(x^5+3)^7/35", x**4*(x**5 + 3)**6)
s9a.append(ex("s9a4", 2, "La del ejemplo", "<p>Calcula \\(\\int x^4(x^5+3)^6\\,dx\\).</p>", [anti("∫ … dx =", "(x^5+3)^7/35")],
   ["\\(u=x^5+3\\), \\(du=5x^4dx\\).", "\\(\\frac15\\int u^6du=\\frac{u^7}{35}\\).", "\\(\\frac{(x^5+3)^7}{35}+C\\)."],
   "\\(\\frac{(x^5+3)^7}{35}+C\\)", "", [["elegu"], ["sust"], ["sust"]]))
chk_anti("-ln(abs(7-5*x))/5", 1/(7 - 5*x), pts=(0.1, 0.3, 0.5, 0.9))
s9a.append(ex("s9a5", 2, "Logaritmo", "<p>Calcula \\(\\int\\frac{1}{7-5x}\\,dx\\).</p>", [anti("∫ … dx =", "-ln(abs(7-5*x))/5", dom=[0, 1.2])],
   ["\\(u=7-5x\\), \\(du=-5dx\\Rightarrow dx=-\\frac{du}5\\).", "\\(-\\frac15\\int\\frac{du}u=-\\frac15\\ln|u|\\).", "\\(-\\frac15\\ln|7-5x|+C\\)."],
   "\\(-\\frac15\\ln|7-5x|+C\\)", "Ojo con el signo de du.", [["sust"], ["sust"], ["sust"]]))
chk_anti("ln(exp(2*x)+3)/2", sp.exp(2*x)/(sp.exp(2*x) + 3))
s9a.append(ex("s9a6", 2, "Exponencial", "<p>Calcula \\(\\int\\frac{e^{2x}}{e^{2x}+3}\\,dx\\).</p>", [anti("∫ … dx =", "ln(exp(2*x)+3)/2")],
   ["\\(u=e^{2x}+3\\), \\(du=2e^{2x}dx\\).", "\\(\\frac12\\int\\frac{du}{u}=\\frac12\\ln(e^{2x}+3)+C\\) (siempre positivo, no hace falta el valor absoluto)."],
   "\\(\\frac12\\ln(e^{2x}+3)+C\\)", "Abajo hay una función cuya derivada está arriba.", [["elegu"], ["sust"]]))
chk_anti("sqrt(x^2+1)", x/sp.sqrt(x**2 + 1))
s9a.append(ex("s9a7", 2, "Con raíz", "<p>Calcula \\(\\int\\frac{x}{\\sqrt{x^2+1}}\\,dx\\).</p>", [anti("∫ … dx =", "sqrt(x^2+1)")],
   ["\\(u=x^2+1\\), \\(du=2x\\,dx\\).", "\\(\\frac12\\int u^{-1/2}du=u^{1/2}=\\sqrt{x^2+1}+C\\)."], "\\(\\sqrt{x^2+1}+C\\)", "", [["sust"], ["sust"]]))
chk_anti("-exp(-x^3)/3", x**2*sp.exp(-x**3))
s9a.append(ex("s9a8", 2, "Exponente cúbico", "<p>Calcula \\(\\int x^2e^{-x^3}\\,dx\\).</p>", [anti("∫ … dx =", "-exp(-x^3)/3")],
   ["\\(u=-x^3\\), \\(du=-3x^2dx\\).", "\\(-\\frac13\\int e^udu=-\\frac13e^{-x^3}+C\\)."], "\\(-\\frac13e^{-x^3}+C\\)", "", [["sust"], ["sust"]]))
chk_val("ln(2)/3", sp.integrate(x**2/(1 + x**3), (x, 0, 1)))
s9a.append(ex("s9a9", 2, "Definida: cambia los límites", "<p>Calcula \\(\\int_0^1\\frac{x^2}{1+x^3}\\,dx\\).</p>", [val("ln(2)/3")],
   ["\\(u=1+x^3\\), \\(du=3x^2dx\\). Límites: x = 0 → u = 1; x = 1 → u = 2.", "\\(\\frac13\\int_1^2\\frac{du}u=\\frac13[\\ln u]_1^2=\\frac13\\ln2\\).",
    "<span class='note'>En la lectura, al final de este ejemplo aparece una línea copiada de otro ejercicio («reemplazando u = 7 − 5x»): ignórala, el resultado es \\(\\frac13\\ln2\\).</span>"],
   "\\(\\frac13\\ln2\\)", "Si cambias los límites, no regresas a x.", [["sustdef"], ["sustdef"], []]))
s9a.append(ex("s9a10", 1, "Los nuevos límites", "<p>En \\(\\int_0^1\\frac{x^2}{1+x^3}dx\\) con \\(u=1+x^3\\), ¿entre qué valores va u?</p>",
   [mc("Respuesta", ["De 1 a 2", "De 0 a 1", "De 0 a 2", "De 1 a 3", "Los límites no cambian"])],
   ["Se reemplaza cada límite en \\(u=1+x^3\\): \\(1+0=1\\) y \\(1+1=2\\).", "Así no hay que volver a x al final."], "De 1 a 2", "", [["sustdef"], ["sustdef"]]))
chk_val("ln(2)^2/2", sp.integrate(sp.log(x)/x, (x, 1, 2)))
s9a.append(ex("s9a11", 2, "Logaritmo sobre x", "<p>Calcula \\(\\int_1^2\\frac{\\ln x}{x}\\,dx\\).</p>", [val("ln(2)^2/2")],
   ["\\(u=\\ln x\\), \\(du=\\frac{dx}x\\). Límites: 1 → 0, 2 → ln 2.", "\\(\\int_0^{\\ln2}u\\,du=\\frac{(\\ln2)^2}2\\approx0{,}24\\)."], "\\(\\frac{(\\ln2)^2}{2}\\)", "", [["sustdef"], ["sustdef"]]))
chk_anti("arctan(t)+ln(1+t^2)/2", (1 + t)/(1 + t**2), var=t)
s9a.append(ex("s9a12", 3, "Separar y sustituir", "<p>Calcula \\(\\int\\frac{1+t}{1+t^2}\\,dt\\).</p>", [anti("∫ … dt =", "arctan(t)+ln(1+t^2)/2", var='t', dom=[-2, 2])],
   ["Separa: \\(\\int\\frac{dt}{1+t^2}+\\int\\frac{t\\,dt}{1+t^2}\\).", "La primera es \\(\\arctan t\\). En la segunda \\(u=1+t^2\\): \\(\\frac12\\ln(1+t^2)\\).", "\\(\\arctan t+\\frac12\\ln(1+t^2)+C\\)."],
   "\\(\\arctan t+\\frac12\\ln(1+t^2)+C\\)", "Una fracción con suma arriba se separa.", [["propind"], ["sust"], ["sust"]]))
P.append({"id": "s9a", "name": "Sem. 9 · Regla de sustitución",
  "teo": "<p>Es la <b>regla de la cadena al revés</b>. Si en la integral aparece una función \\(g(x)\\) y también su derivada \\(g'(x)\\):</p>"
         "<p style='text-align:center'>\\(\\int f(g(x))\\,g'(x)\\,dx=\\int f(u)\\,du\\), con \\(u=g(x)\\), \\(du=g'(x)\\,dx\\).</p>"
         "<p><b>Pasos:</b> 1) elige u (casi siempre «lo de adentro»), 2) calcula du y despeja dx, 3) reemplaza: no debe quedar ninguna x, 4) integra y 5) regresa a x.</p>"
         "<p><b>En definidas</b> también cambian los límites: si \\(u=g(x)\\), van de \\(g(a)\\) a \\(g(b)\\) y ya no se regresa a x.</p>"
         "<p>Útiles: \\(\\int\\frac{dx}{ax+b}=\\frac1a\\ln|ax+b|\\) · \\(\\int e^{kx}dx=\\frac{e^{kx}}k\\) · \\(\\int\\cos(kx)dx=\\frac{\\operatorname{sen}kx}k\\).</p>",
  "form": ["\\(u=g(x)\\Rightarrow du=g'(x)dx\\)", "\\(\\int f(g(x))g'(x)dx=\\int f(u)du\\)", "Definida: \\(\\int_{g(a)}^{g(b)}f(u)du\\)", "\\(\\int\\frac{dx}{ax+b}=\\frac1a\\ln|ax+b|\\)"],
  "lesson": "<h3>Idea central</h3><p>Buscas «una función y su derivada» dentro de la integral. Si eliges bien u, la integral se vuelve de tabla.</p><div class=\"ej\"><b>Ejemplo:</b> \\(\\int2x\\cos(x^2)dx\\): \\(u=x^2\\) ⇒ \\(\\int\\cos u\\,du=\\operatorname{sen}(x^2)+C\\).</div><div class=\"err\"><b>Error común:</b> dejar x mezcladas con u, o en definidas no cambiar los límites.</div>",
  "tools": [{"w": "usub", "t": "¿Qué u elijo?", "p": "Toca cada opción y mira cómo queda la integral.", "o": {"int": "\\int\\frac{x^2}{1+x^3}\\,dx", "opts": [
      {"u": "1+x^3", "du": "3x^2\\,dx", "new": "\\frac13\\int\\frac{du}{u}", "ok": True, "e": "Queda de tabla: \\(\\frac13\\ln|1+x^3|+C\\)."},
      {"u": "x^3", "du": "3x^2\\,dx", "new": "\\frac13\\int\\frac{du}{1+u}", "ok": True, "e": "También funciona, aunque deja un paso más."},
      {"u": "x^2", "du": "2x\\,dx", "new": "\\int\\frac{u}{1+x^3}\\cdot\\frac{du}{2x}", "ok": False, "e": "Quedan x mezcladas con u."},
      {"u": "\\frac{1}{1+x^3}", "du": "-\\frac{3x^2}{(1+x^3)^2}dx", "new": "-\\frac13\\int\\frac{du}{u}", "ok": True, "e": "Curiosamente también sale, pero es más difícil de ver."}]}}],
  "ex": s9a})

# --- s9b integrales trigonométricas
s9b = []
s9b.append(ex("s9b1", 2, "¿Qué caso es?", "<p>Clasifica cada integral según la estrategia que usarías.</p>",
   [{"t": "cls", "cats": ["sen o cos impar", "sen y cos pares", "tan impar (con sec)", "sec par (con tan)"], "items": [
     {"x": "\\(\\int\\operatorname{sen}^3x\\cos^4x\\,dx\\)", "c": 0, "e": "El seno tiene potencia impar: separas un sen x."},
     {"x": "\\(\\int\\cos^5x\\,dx\\)", "c": 0, "e": "Potencia impar de coseno: separas un cos x."},
     {"x": "\\(\\int\\operatorname{sen}^4x\\,dx\\)", "c": 1, "e": "Solo potencias pares: ángulo mitad."},
     {"x": "\\(\\int\\operatorname{sen}^2x\\cos^2x\\,dx\\)", "c": 1, "e": "Ambas pares: ángulo mitad."},
     {"x": "\\(\\int\\tan^5x\\sec x\\,dx\\)", "c": 2, "e": "tan impar: separas sec x tan x, u = sec x."},
     {"x": "\\(\\int\\sqrt{\\tan x}\\sec^4x\\,dx\\)", "c": 3, "e": "sec par: separas sec²x, u = tan x."}]}],
   ["Senos y cosenos: si alguna potencia es impar, separas un factor; si todas son pares, bajas el grado con el ángulo mitad.", "tan y sec: con tan impar, u = sec x; con sec par, u = tan x."],
   "Clasificación correcta", "Mira qué potencia es impar.", [["trigcasos"], ["trigcasos"]]))
s9b.append(ex("s9b2", 1, "El primer paso", "<p>Para \\(\\int\\operatorname{sen}^3x\\cos^4x\\,dx\\), ¿cuál es el primer paso?</p>",
   [mc("Respuesta", ["Separar un sen x y escribir \\(\\operatorname{sen}^2x=1-\\cos^2x\\), con \\(u=\\cos x\\)", "Usar \\(\\cos^2x=\\frac{1+\\cos2x}2\\) dos veces", "Hacer \\(u=\\operatorname{sen}x\\) directamente", "Integrar cada factor por separado", "Usar \\(x=\\operatorname{sen}\\theta\\)"])],
   ["El seno tiene potencia impar: separas uno, que formará el du.", "Lo demás queda en cosenos y \\(u=\\cos x\\), \\(du=-\\operatorname{sen}x\\,dx\\)."], "Separar un sen x", "", [["trigcasos"], ["trigcasos"]]))
def trig(id, lvl, title, integ, tex, ans, steps, tags, dom=None, hint=""):
    chk_anti(ans, integ, pts=(0.2, 0.5, 0.8, 1.1))
    return ex(id, lvl, title, "<p>Calcula \\(" + tex + "\\).</p>", [anti("∫ … dx =", ans, dom=dom or [0.15, 1.2])], steps, "", hint, tags)
sx, cx, tx, scx = sp.sin(x), sp.cos(x), sp.tan(x), sp.sec(x)
L = []
L.append(trig("s9b3", 2, "Seno impar", sx**3*cx**4, "\\int\\operatorname{sen}^3x\\cos^4x\\,dx", "-cos(x)^5/5+cos(x)^7/7",
   ["\\(\\operatorname{sen}^2x\\operatorname{sen}x=(1-\\cos^2x)\\operatorname{sen}x\\); \\(u=\\cos x\\).", "\\(-\\int(1-u^2)u^4du=-\\frac{u^5}5+\\frac{u^7}7\\).", "\\(-\\frac{\\cos^5x}5+\\frac{\\cos^7x}7+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
L.append(trig("s9b4", 2, "Coseno impar", cx**5, "\\int\\cos^5x\\,dx", "sen(x)-2*sen(x)^3/3+sen(x)^5/5",
   ["\\(\\cos^4x\\cos x=(1-\\operatorname{sen}^2x)^2\\cos x\\); \\(u=\\operatorname{sen}x\\).", "\\(\\int(1-2u^2+u^4)du=u-\\frac{2u^3}3+\\frac{u^5}5\\).", "\\(\\operatorname{sen}x-\\frac23\\operatorname{sen}^3x+\\frac15\\operatorname{sen}^5x+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
L.append(trig("s9b5", 3, "Seno a la quinta", sx**5*cx**2, "\\int\\operatorname{sen}^5x\\cos^2x\\,dx", "-cos(x)^3/3+2*cos(x)^5/5-cos(x)^7/7",
   ["\\(\\operatorname{sen}^4x=(1-\\cos^2x)^2\\); \\(u=\\cos x\\).", "\\(-\\int(1-u^2)^2u^2du=-\\int(u^2-2u^4+u^6)du\\).", "\\(-\\frac{\\cos^3x}3+\\frac{2\\cos^5x}5-\\frac{\\cos^7x}7+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
L.append(trig("s9b6", 3, "Potencia par", sx**4, "\\int\\operatorname{sen}^4x\\,dx", "3*x/8-sen(2*x)/4+sen(4*x)/32",
   ["\\(\\operatorname{sen}^4x=\\left(\\frac{1-\\cos2x}2\\right)^2=\\frac14(1-2\\cos2x+\\cos^22x)\\).", "Otra vez ángulo mitad: \\(\\cos^22x=\\frac{1+\\cos4x}2\\).", "\\(\\frac{3x}8-\\frac{\\operatorname{sen}2x}4+\\frac{\\operatorname{sen}4x}{32}+C\\)."], [["trigcasos", "idtrig"], ["idtrig"], ["tabla"]]))
L.append(trig("s9b7", 2, "Ambas pares", sx**2*cx**2, "\\int\\operatorname{sen}^2x\\cos^2x\\,dx", "x/8-sen(4*x)/32",
   ["\\(\\operatorname{sen}x\\cos x=\\frac12\\operatorname{sen}2x\\) ⇒ el integrando es \\(\\frac14\\operatorname{sen}^22x\\).", "\\(\\frac14\\cdot\\frac{1-\\cos4x}2=\\frac18-\\frac{\\cos4x}8\\).", "\\(\\frac x8-\\frac{\\operatorname{sen}4x}{32}+C\\)."], [["idtrig"], ["idtrig"], ["tabla"]]))
L.append(trig("s9b8", 2, "tan impar", tx**3*scx**5, "\\int\\tan^3x\\sec^5x\\,dx", "sec(x)^7/7-sec(x)^5/5",
   ["Separa \\(\\sec x\\tan x\\): \\(\\tan^2x\\sec^4x\\cdot\\sec x\\tan x\\), con \\(\\tan^2x=\\sec^2x-1\\).", "\\(u=\\sec x\\): \\(\\int(u^2-1)u^4du\\).", "\\(\\frac{\\sec^7x}7-\\frac{\\sec^5x}5+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
L.append(trig("s9b9", 3, "tan a la quinta", tx**5*scx, "\\int\\tan^5x\\sec x\\,dx", "sec(x)^5/5-2*sec(x)^3/3+sec(x)",
   ["\\(\\tan^4x\\cdot\\sec x\\tan x=(\\sec^2x-1)^2\\sec x\\tan x\\).", "\\(u=\\sec x\\): \\(\\int(u^4-2u^2+1)du\\).", "\\(\\frac{\\sec^5x}5-\\frac23\\sec^3x+\\sec x+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
L.append(trig("s9b10", 3, "sec par", sp.sqrt(tx)*scx**4, "\\int\\sqrt{\\tan x}\\,\\sec^4x\\,dx", "2*tan(x)^(3/2)/3+2*tan(x)^(7/2)/7",
   ["Separa \\(\\sec^2x\\): \\(\\sqrt{\\tan x}(\\tan^2x+1)\\sec^2x\\).", "\\(u=\\tan x\\): \\(\\int(u^{5/2}+u^{1/2})du\\).", "\\(\\frac27\\tan^{7/2}x+\\frac23\\tan^{3/2}x+C\\)."], [["trigcasos"], ["sust"], ["sust"]]))
for e in L:
    e["ans"] = None
s9b += L
P.append({"id": "s9b", "name": "Sem. 9 · Integrales trigonométricas",
  "teo": "<p><b>\\(\\int\\operatorname{sen}^mx\\cos^nx\\,dx\\)</b></p><ul><li><b>Caso I (alguna impar):</b> separas un factor de la impar (un sen x o un cos x) y lo demás lo pasas a la otra función con \\(\\operatorname{sen}^2=1-\\cos^2\\). Luego \\(u=\\cos x\\) o \\(u=\\operatorname{sen}x\\).</li>"
         "<li><b>Caso II (ambas pares):</b> bajas el grado con \\(\\operatorname{sen}^2x=\\frac{1-\\cos2x}2\\) y \\(\\cos^2x=\\frac{1+\\cos2x}2\\) (las veces que haga falta).</li></ul>"
         "<p><b>\\(\\int\\tan^mx\\sec^nx\\,dx\\)</b></p><ul><li><b>Caso III (tan impar):</b> separas \\(\\sec x\\tan x\\), usas \\(\\tan^2=\\sec^2-1\\) y \\(u=\\sec x\\).</li>"
         "<li><b>Caso IV (sec par):</b> separas \\(\\sec^2x\\), usas \\(\\sec^2=\\tan^2+1\\) y \\(u=\\tan x\\).</li></ul>"
         "<p>Tabla extra: \\(\\int\\tan x=\\ln|\\sec x|\\) · \\(\\int\\sec x=\\ln|\\sec x+\\tan x|\\) · \\(\\int\\csc^2x=-\\cot x\\).</p>",
  "form": ["Impar: separa un factor y \\(\\operatorname{sen}^2=1-\\cos^2\\)", "Pares: \\(\\operatorname{sen}^2=\\frac{1-\\cos2x}2\\), \\(\\cos^2=\\frac{1+\\cos2x}2\\)", "tan impar: separa \\(\\sec x\\tan x\\), \\(u=\\sec x\\)", "sec par: separa \\(\\sec^2x\\), \\(u=\\tan x\\)"],
  "lesson": "<h3>Idea central</h3><p>Siempre buscas dejar «una función y su derivada»: sen con cos, tan con sec². La identidad es solo para lograrlo.</p><div class=\"err\"><b>Error común:</b> usar ángulo mitad cuando hay una potencia impar (se complica muchísimo).</div>",
  "ex": s9b})
for e in s9b:
    if e["ans"] is None:
        e["ans"] = "Tu antiderivada coincide (ver solución)"

# --- s9c sustitución trigonométrica
s9c = []
s9c.append(ex("s9c1", 1, "¿Qué sustitución?", "<p>Clasifica cada raíz según la sustitución que conviene.</p>",
   [{"t": "cls", "cats": ["x = a sen θ", "x = a tan θ", "x = a sec θ"], "items": [
     {"x": "\\(\\sqrt{25-x^2}\\)", "c": 0}, {"x": "\\(\\sqrt{4-x^2}\\)", "c": 0},
     {"x": "\\(\\sqrt{9+x^2}\\)", "c": 1}, {"x": "\\(\\sqrt{x^2+1}\\)", "c": 1},
     {"x": "\\(\\sqrt{x^2-16}\\)", "c": 2, "e": "x² va primero: secante."}, {"x": "\\(\\sqrt{x^2-3}\\)", "c": 2}]}],
   ["\\(a^2-x^2\\) → seno; \\(a^2+x^2\\) → tangente; \\(x^2-a^2\\) → secante.", "Cada una usa la identidad que borra la raíz."], "Clasificación correcta", "", [["trigsust"], ["trigsust"]]))
s9c.append(ex("s9c2", 2, "Arma el triángulo: a² − x²", "<p>Para \\(\\int\\frac{dx}{\\sqrt{4-x^2}}\\), arma la sustitución y el triángulo.</p>",
   [{"t": "tri", "p": "Sustitución y triángulo", "a": 2, "k": "resta", "ask": ["sen"], "e": "Con x = 2 sen θ, la hipotenusa es 2 y el cateto opuesto es x."}],
   ["\\(x=2\\operatorname{sen}\\theta\\Rightarrow\\operatorname{sen}\\theta=\\frac x2\\): opuesto x, hipotenusa 2.", "Adyacente: \\(\\sqrt{4-x^2}\\)."], "x = 2 sen θ · hip 2 · op x · ady √(4 − x²)", "", [["trigsust"], ["triang"]]))
s9c.append(ex("s9c3", 2, "Arma el triángulo: a² + x²", "<p>Para \\(\\int\\frac{x\\,dx}{\\sqrt{9+x^2}}\\), arma la sustitución y el triángulo, y lee sec θ.</p>",
   [{"t": "tri", "p": "Sustitución y triángulo", "a": 3, "k": "suma", "ask": ["sec"], "e": "Con x = 3 tan θ: opuesto x, adyacente 3 y la raíz es la hipotenusa."}],
   ["\\(\\tan\\theta=\\frac x3\\): opuesto x, adyacente 3, hipotenusa \\(\\sqrt{9+x^2}\\).", "\\(\\sec\\theta=\\frac{\\sqrt{9+x^2}}{3}\\)."], "x = 3 tan θ · sec θ = √(9 + x²) / 3", "", [["trigsust"], ["triang"]]))
s9c.append(ex("s9c4", 2, "Arma el triángulo: x² − a²", "<p>Para \\(\\int\\frac{\\sqrt{x^2-4}}{x}dx\\), arma la sustitución y el triángulo, y lee tan θ.</p>",
   [{"t": "tri", "p": "Sustitución y triángulo", "a": 2, "k": "menos", "ask": ["tan"], "e": "Con x = 2 sec θ: hipotenusa x, adyacente 2 y la raíz es el opuesto."}],
   ["\\(\\sec\\theta=\\frac x2\\): hipotenusa x, adyacente 2, opuesto \\(\\sqrt{x^2-4}\\).", "\\(\\tan\\theta=\\frac{\\sqrt{x^2-4}}2\\)."], "x = 2 sec θ · tan θ = √(x² − 4) / 2", "", [["trigsust"], ["triang"]]))
chk_anti("arcsen(x/2)", 1/sp.sqrt(4 - x**2))
s9c.append(ex("s9c5", 2, "Caso seno", "<p>Calcula \\(\\int\\frac{dx}{\\sqrt{4-x^2}}\\).</p>", [anti("∫ … dx =", "arcsen(x/2)", dom=[-1.5, 1.5])],
   ["\\(x=2\\operatorname{sen}\\theta\\), \\(dx=2\\cos\\theta\\,d\\theta\\), \\(\\sqrt{4-x^2}=2\\cos\\theta\\).", "\\(\\int\\frac{2\\cos\\theta}{2\\cos\\theta}d\\theta=\\theta+C\\).", "\\(\\theta=\\operatorname{arcsen}\\frac x2\\): resultado \\(\\operatorname{arcsen}\\frac x2+C\\)."],
   "\\(\\operatorname{arcsen}\\frac x2+C\\)", "", [["trigsust"], ["trigsust"], ["triang"]]))
chk_anti("sqrt(9+x^2)", x/sp.sqrt(9 + x**2))
s9c.append(ex("s9c6", 2, "Caso tangente", "<p>Calcula \\(\\int\\frac{x\\,dx}{\\sqrt{9+x^2}}\\).</p>", [anti("∫ … dx =", "sqrt(9+x^2)", dom=[-2, 2])],
   ["\\(x=3\\tan\\theta\\), \\(dx=3\\sec^2\\theta\\,d\\theta\\), \\(\\sqrt{9+x^2}=3\\sec\\theta\\).", "\\(\\int3\\tan\\theta\\sec\\theta\\,d\\theta=3\\sec\\theta\\).", "Del triángulo \\(\\sec\\theta=\\frac{\\sqrt{9+x^2}}3\\): resultado \\(\\sqrt{9+x^2}+C\\). (También sale con \\(u=9+x^2\\).)"],
   "\\(\\sqrt{9+x^2}+C\\)", "", [["trigsust"], ["trigsust"], ["triang"]]))
chk_val("2-π/2", sp.integrate(sp.sqrt(x**2 - 4)/x, (x, 2, 2*sp.sqrt(2))))
s9c.append(ex("s9c7", 3, "Caso secante, definida", "<p>Calcula \\(\\int_2^{2\\sqrt2}\\frac{\\sqrt{x^2-4}}{x}\\,dx\\).</p>", [val("2-π/2")],
   ["\\(x=2\\sec\\theta\\), \\(dx=2\\sec\\theta\\tan\\theta\\,d\\theta\\), \\(\\sqrt{x^2-4}=2\\tan\\theta\\). Límites: x = 2 → θ = 0; x = 2√2 → θ = π/4.",
    "\\(\\int_0^{\\pi/4}2\\tan^2\\theta\\,d\\theta=2\\int_0^{\\pi/4}(\\sec^2\\theta-1)d\\theta\\).", "\\(2[\\tan\\theta-\\theta]_0^{\\pi/4}=2\\left(1-\\frac\\pi4\\right)=2-\\frac\\pi2\\approx0{,}43\\)."],
   "\\(2-\\frac\\pi2\\)", "Cambia los límites a θ.", [["trigsust"], ["idtrig"], ["tfc"]]))
chk_anti("sqrt(x^2-1)", x/sp.sqrt(x**2 - 1), pts=(1.3, 1.7, 2.2, 2.9))
s9c.append(ex("s9c8", 2, "x² − 1", "<p>Calcula \\(\\int\\frac{x\\,dx}{\\sqrt{x^2-1}}\\) (x &gt; 1).</p>", [anti("∫ … dx =", "sqrt(x^2-1)", dom=[1.2, 3])],
   ["Con \\(x=\\sec\\theta\\): \\(\\int\\frac{\\sec\\theta}{\\tan\\theta}\\sec\\theta\\tan\\theta\\,d\\theta=\\int\\sec^2\\theta\\,d\\theta=\\tan\\theta\\).", "Del triángulo \\(\\tan\\theta=\\sqrt{x^2-1}\\). (Con \\(u=x^2-1\\) sale más rápido: si ves la derivada afuera, usa sustitución simple.)"],
   "\\(\\sqrt{x^2-1}+C\\)", "", [["trigsust"], ["triang"]]))
chk_anti("x/(9*sqrt(x^2+9))", 1/(x**2 + 9)**sp.Rational(3, 2))
s9c.append(ex("s9c9", 3, "Potencia 3/2", "<p>Calcula \\(\\int\\frac{dx}{(x^2+9)^{3/2}}\\).</p>", [anti("∫ … dx =", "x/(9*sqrt(x^2+9))", dom=[-2, 2])],
   ["\\(x=3\\tan\\theta\\): \\((x^2+9)^{3/2}=27\\sec^3\\theta\\), \\(dx=3\\sec^2\\theta\\,d\\theta\\).", "\\(\\frac19\\int\\cos\\theta\\,d\\theta=\\frac19\\operatorname{sen}\\theta\\).", "Triángulo: \\(\\operatorname{sen}\\theta=\\frac{x}{\\sqrt{x^2+9}}\\) ⇒ \\(\\frac{x}{9\\sqrt{x^2+9}}+C\\)."],
   "\\(\\frac{x}{9\\sqrt{x^2+9}}+C\\)", "", [["trigsust"], ["trigsust"], ["triang"]]))
P.append({"id": "s9c", "name": "Sem. 9 · Sustitución trigonométrica",
  "teo": "<p>Sirve para integrales con raíces de la forma:</p><ul><li>\\(\\sqrt{a^2-x^2}\\): \\(x=a\\operatorname{sen}\\theta\\), \\(dx=a\\cos\\theta\\,d\\theta\\), la raíz queda \\(a\\cos\\theta\\).</li>"
         "<li>\\(\\sqrt{a^2+x^2}\\): \\(x=a\\tan\\theta\\), \\(dx=a\\sec^2\\theta\\,d\\theta\\), la raíz queda \\(a\\sec\\theta\\).</li>"
         "<li>\\(\\sqrt{x^2-a^2}\\): \\(x=a\\sec\\theta\\), \\(dx=a\\sec\\theta\\tan\\theta\\,d\\theta\\), la raíz queda \\(a\\tan\\theta\\).</li></ul>"
         "<p>Al final hay que <b>regresar a x</b>: dibujas el triángulo rectángulo que dice la sustitución (por ejemplo \\(\\operatorname{sen}\\theta=\\frac xa\\): opuesto x, hipotenusa a) y lees la razón que necesites. En definidas puedes cambiar los límites a θ y no regresar.</p>"
         "<p>Antes de usarla, mira si una sustitución simple basta: \\(\\int\\frac{x}{\\sqrt{9+x^2}}dx\\) sale con \\(u=9+x^2\\).</p>",
  "form": ["\\(\\sqrt{a^2-x^2}\\): \\(x=a\\operatorname{sen}\\theta\\) → \\(a\\cos\\theta\\)", "\\(\\sqrt{a^2+x^2}\\): \\(x=a\\tan\\theta\\) → \\(a\\sec\\theta\\)", "\\(\\sqrt{x^2-a^2}\\): \\(x=a\\sec\\theta\\) → \\(a\\tan\\theta\\)", "Regresa a x con el triángulo"],
  "lesson": "<h3>Idea central</h3><p>Cada raíz es un lado de un triángulo rectángulo. La sustitución elige qué lado es x.</p><div class=\"err\"><b>Error común:</b> elegir la sustitución por el signo equivocado: si x² va primero (\\(x^2-a^2\\)), es secante.</div>",
  "tools": [{"w": "tri", "t": "El triángulo de cada raíz", "p": "Toca cada tipo de raíz: mira dónde va x, a y la raíz, y cómo se lee cada razón.", "o": {"a": 3}}],
  "ex": s9c})

# --- s9d razonamiento cuantitativo
s9d = []
r = 500/(1 + sp.Rational(1, 5)*t)**2
N = sp.integrate(r, (t, 2, 7)); Nn = float(N)
assert abs(Nn - 744.05) < 0.01
s9d.append(ex("s9d1", 2, "Gaviotas en Paracas", "<p>La tasa de crecimiento de una población de gaviotas es \\(r(t)=\\frac{500}{(1+0{,}2t)^2}\\) gaviotas por año, con t en años desde 2025. ¿Cuántas gaviotas se suman entre 2027 y 2032?</p>",
   [mc("Interpretación: ¿qué representa \\(\\int r(t)\\,dt\\) en un intervalo?", ["La cantidad de gaviotas nuevas en ese intervalo", "La población total en 2032", "La tasa de crecimiento promedio", "Cuántas gaviotas nacen por año", "La población en 2027"]),
    num("Representación: límites de integración", [{"l": "t inicial =", "a": 2, "e": "2027 − 2025."}, {"l": "t final =", "a": 7, "e": "2032 − 2025."}]),
    num("Cálculo: \\(N=\\int_2^7r(t)\\,dt\\)", [{"l": "N ≈", "a": round(Nn, 2), "tol": 0.6}]),
    mc("Conclusión", ["Entre 2027 y 2032 la población aumenta en unas 744 gaviotas", "En 2032 habrá 744 gaviotas en total", "La población crece 744 gaviotas por año", "Entre 2027 y 2032 se pierden 744 gaviotas", "En 2027 había 744 gaviotas"])],
   ["Integrar una tasa da el cambio total en el intervalo.", "t = 2 es 2027 y t = 7 es 2032.", "\\(u=1+0{,}2t\\), \\(dt=5\\,du\\): \\(2500\\int_{1{,}4}^{2{,}4}u^{-2}du=2500\\left[\\frac1{1{,}4}-\\frac1{2{,}4}\\right]\\approx744{,}05\\).", "Es lo que se <b>suma</b> a la población, no la población total."],
   "≈ 744 gaviotas más", "", [["rcuant"], ["rcuant"], ["sustdef"], ["rcuant"]], chain=True))
Pm = 2*t + sp.Rational(1, 2)*sp.cos(sp.pi*t/4)
E = sp.integrate(Pm, (t, 2, 6)); assert sp.simplify(E - (32 - 4/sp.pi)) == 0 and abs(float(E) - 30.73) < 0.01
s9d.append(ex("s9d2", 2, "Energía de un motor", "<p>Un motor consume una potencia \\(P(t)=2t+\\frac12\\cos\\left(\\frac{\\pi t}{4}\\right)\\) kW (t en horas). La energía es la integral de la potencia. Halla la energía entre la hora 2 y la hora 6 y su costo a \\$0,15 por kWh.</p>",
   [val("32-4/π", p="Energía exacta en kWh.", label="E ="), num("Costo", [{"l": "Costo", "a": round(float(E)*0.15, 2), "u": "$", "tol": 0.011}])],
   ["\\(E=\\int_2^6\\left[2t+\\frac12\\cos\\frac{\\pi t}4\\right]dt=\\left[t^2+\\frac2\\pi\\operatorname{sen}\\frac{\\pi t}4\\right]_2^6\\).", "\\(=(36-4)+\\frac2\\pi(-1-1)=32-\\frac4\\pi\\approx30{,}73\\) kWh.", "Costo: \\(30{,}73\\times0{,}15\\approx\\$4{,}61\\)."],
   "\\(32-\\frac4\\pi\\approx30{,}73\\) kWh · \\$4,61", "kW × h = kWh.", [["rcuant"], ["sust"], ["rcuant"]], chain=True))
Pt = sp.Rational(3, 2)*t + sp.Rational(3, 4)*sp.cos(sp.pi*t/3)
E2 = sp.integrate(Pt, (t, 1, 4)); e2 = float(E2); assert 4 < e2*0.5 < 5.1
s9d.append(ex("s9d3", 3, "¿Tiene razón el jefe?", "<p>Un motor textil consume \\(P(t)=1{,}5t+\\frac34\\cos\\left(\\frac{\\pi t}{3}\\right)\\) kW. El jefe de mantenimiento dice que, entre la hora 1 y la hora 4, a \\$0,50 por kWh, el costo <b>no supera</b> los \\$4.</p>",
   [num("Energía entre t = 1 y t = 4", [{"l": "E ≈", "a": round(e2, 2), "u": "kWh", "tol": 0.03}]),
    num("Costo", [{"l": "Costo ≈", "a": round(e2*0.5, 2), "u": "$", "tol": 0.02}]),
    mc("¿El jefe tiene razón?", ["No: el costo es de unos \\$5,00, así que sí supera los \\$4", "Sí: el costo es menor que \\$4", "Sí: la energía es menor que 4 kWh", "No se puede saber sin la potencia máxima", "No: el costo es de unos \\$20"])],
   ["\\(E=\\left[0{,}75t^2+\\frac{9}{4\\pi}\\operatorname{sen}\\frac{\\pi t}3\\right]_1^4=11{,}25-\\frac{9\\sqrt3}{4\\pi}\\approx10{,}01\\) kWh.", "Costo: \\(10{,}01\\times0{,}50\\approx\\$5{,}00\\).",
    "Supera los \\$4: el jefe se equivoca. <span class='note'>Ojo: la respuesta de la lectura dice «no supera los 4 dólares» y a la vez que el jefe está equivocado; lo correcto es que el costo <b>sí supera</b> los \\$4.</span>"],
   "≈ 10,01 kWh · ≈ \\$5,00 · el jefe se equivoca", "", [["sust"], ["rcuant"], ["rcuant"]], chain=True))
s9d.append(ex("s9d4", 1, "Unidades", "<p>Si P(t) está en kilovatios y t en horas, ¿en qué unidades sale \\(\\int_a^bP(t)\\,dt\\)?</p>",
   [mc("Respuesta", ["kWh (kilovatios-hora)", "kW (kilovatios)", "kW/h", "horas", "kW²"])],
   ["Una integral multiplica la función por el diferencial: kW × h.", "Integrar una tasa (potencia = energía por tiempo) da la cantidad acumulada (energía)."], "kWh", "", [["rcuant"], ["rcuant"]]))
P.append({"id": "s9d", "name": "Sem. 9 · Razonamiento cuantitativo con integrales",
  "teo": "<p>Si \\(r(t)\\) es una <b>tasa de cambio</b> (gaviotas por año, kW = energía por hora, litros por minuto…), entonces</p><p style='text-align:center'>\\(\\int_a^br(t)\\,dt\\) = cantidad acumulada entre a y b.</p>"
         "<p>La UPC califica estos problemas con una rúbrica de cuatro partes:</p><ol><li><b>Interpretación:</b> qué te piden, qué datos tienes y qué concepto usarás.</li><li><b>Representación:</b> variables con unidades, restricciones y el modelo (la integral con sus límites).</li><li><b>Cálculo:</b> el procedimiento (TFC, sustitución) y el número.</li><li><b>Análisis y argumentación:</b> la respuesta en una oración con unidades, verificando que tenga sentido.</li></ol>",
  "form": ["Integral de una tasa = cambio total", "Potencia (kW) → energía (kWh)", "Rúbrica: interpretación · representación · cálculo · argumentación"],
  "lesson": "<h3>Idea central</h3><p>Antes de integrar, traduce el texto: ¿qué es una tasa?, ¿cuáles son los límites en la variable del problema?</p><div class=\"err\"><b>Error común:</b> poner los años (2027, 2032) como límites cuando t cuenta desde 2025.</div>",
  "ex": s9d})

# =====================================================================
# ARMADO
# =====================================================================
CONC = {
 "dpot": ("Regla de la potencia", "\\((x^n)'=nx^{n-1}\\)", "Baja el exponente y réstale 1.", "rp1"),
 "cadena": ("Regla de la cadena", "\\((f(g(x)))'=f'(g(x))g'(x)\\)", "Afuera por la derivada de adentro.", "rp1"),
 "difer": ("Diferencial", "\\(du=g'(x)\\,dx\\)", "Es lo que se reemplaza en la sustitución.", "rp1"),
 "expo": ("Leyes de exponentes", "\\(\\frac1{x^n}=x^{-n}\\) · \\(\\sqrt[n]{x^m}=x^{m/n}\\)", "Reescribe antes de integrar.", "rp2"),
 "idtrig": ("Identidades trigonométricas", "\\(\\operatorname{sen}^2x=\\frac{1-\\cos2x}2\\) · \\(\\tan^2=\\sec^2-1\\)", "Transforman la integral en una de tabla.", "rp3"),
 "dtrig": ("Derivadas trigonométricas", "\\((\\tan x)'=\\sec^2x\\) · \\((\\sec x)'=\\sec x\\tan x\\)", "La tabla de integrales al revés.", "rp3"),
 "triang": ("Triángulo rectángulo", "sen = op/hip · tan = op/ady · sec = hip/ady", "Pitágoras da el lado que falta.", "rp4"),
 "antider": ("Antiderivada", "\\(F'=f\\)", "Todas las antiderivadas difieren en una constante.", "s7a"),
 "tabla": ("Tabla de integrales", "\\(\\int x^n=\\frac{x^{n+1}}{n+1}\\) · \\(\\int\\frac1x=\\ln|x|\\)", "Las derivadas leídas al revés.", "s7a"),
 "propind": ("Propiedades de la indefinida", "\\(\\int(f\\pm g)=\\int f\\pm\\int g\\) · \\(\\int kf=k\\int f\\)", "No hay regla para productos ni cocientes.", "s7a"),
 "cini": ("Condición inicial", "\\(f(x_0)=y_0\\Rightarrow C\\)", "Un dato fija la constante.", "s7a"),
 "areasig": ("Área con signo", "\\(\\int_a^bf=A_{\\text{arriba}}-A_{\\text{abajo}}\\)", "La integral definida es área neta.", "s7b"),
 "defi": ("Integral definida", "\\(\\int_a^bf(x)dx\\in\\mathbb R\\)", "Es un número, no una función.", "s7b"),
 "aditiva": ("Aditividad", "\\(\\int_a^c+\\int_c^b=\\int_a^b\\)", "Se pegan intervalos.", "s8a"),
 "lineal": ("Linealidad", "\\(\\int(\\alpha f+\\beta g)=\\alpha\\int f+\\beta\\int g\\)", "Sumas y constantes salen.", "s8a"),
 "invertir": ("Invertir límites", "\\(\\int_a^b=-\\int_b^a\\) · \\(\\int_a^a=0\\)", "Cambia el signo.", "s8a"),
 "const": ("Integral de una constante", "\\(\\int_a^bc\\,dx=c(b-a)\\)", "Un rectángulo.", "s8a"),
 "tfc": ("TFC (parte 2)", "\\(\\int_a^bf=F(b)-F(a)\\)", "Con cualquier antiderivada; la C se cancela.", "s8b"),
 "elegu": ("Elegir u", "u = lo de adentro, su derivada afuera", "Si quedan x mezcladas, cambia de u.", "s9a"),
 "sust": ("Regla de sustitución", "\\(\\int f(g(x))g'(x)dx=\\int f(u)du\\)", "La cadena al revés.", "s9a"),
 "sustdef": ("Sustitución en definidas", "\\(\\int_{g(a)}^{g(b)}f(u)du\\)", "Cambian los límites.", "s9a"),
 "trigcasos": ("Casos de integrales trigonométricas", "impar: separa un factor · pares: ángulo mitad", "Busca una función y su derivada.", "s9b"),
 "trigsust": ("Sustitución trigonométrica", "\\(a^2-x^2\\): sen · \\(a^2+x^2\\): tan · \\(x^2-a^2\\): sec", "Cada raíz es un lado del triángulo.", "s9c"),
 "rcuant": ("Razonamiento cuantitativo", "\\(\\int_a^b\\text{tasa}\\,dt\\) = cambio total", "Interpretar, representar, calcular y argumentar.", "s9d")}

def concepts(topics):
    ids = {tt["id"] for tt in topics}
    return {k: {"n": v[0], "f": v[1], "x": v[2], "home": v[3]} for k, v in CONC.items() if v[3] in ids}

def check_tags(topics, cs):
    allids = set()
    for tt in topics:
        for e in tt["ex"]:
            assert e["id"] not in allids, e["id"]; allids.add(e["id"])
            for st in e["tags"]:
                for k in st: assert k in cs, (e["id"], k)
    return allids

def fgrid(note, topics):
    cards = ''.join('<div><b>' + tt["name"].split('·', 1)[-1].strip() + '</b><br>' + ' · '.join(tt["form"]) + '</div>\n' for tt in topics)
    return '<p class="note">' + note + '</p>\n<div class="fgrid">\n' + cards + '</div>'

BASE = {"code": "1AMA0758", "uni": "UPC", "name": "Cálculo I", "nbname": "Cálculo I", "guide": True, "free": True, "formSim": False, "figs": {}, "simEx": []}
TAPA = {"p": "lunares", "c": ["#FFF0EC", "#F08C78", "#A8382A", "#7A231A"]}

rep_c = concepts(R); ids_r = check_tags(R, rep_c)
rep = dict(BASE, id="cupc-rep", tapa=TAPA, exam="Repaso introductorio", short="Repaso", sub="Bases para integrar",
  intro="Lo mínimo que necesitas antes de integrar: derivadas y regla de la cadena, exponentes, identidades trigonométricas y el triángulo rectángulo. Es corto a propósito: si ya lo dominas, pasa directo a la <b>Práctica</b>.",
  form=fgrid("Hoja de repaso: lo que usa el cálculo integral.", R), topics=R, concepts=rep_c,
  sim={"minutes": 30, "intro": "Simulacro corto del repaso (20 puntos, 30 min): una pregunta de cada base.", "slots": [
    {"pts": 5, "name": "Derivadas y regla de la cadena", "pool": ["rp1e2", "rp1e3", "rp1e4"]},
    {"pts": 5, "name": "Exponentes y raíces", "pool": ["rp2e2", "rp2e3", "rp2e4"]},
    {"pts": 5, "name": "Identidades trigonométricas", "pool": ["rp3e1", "rp3e2", "rp3e4"]},
    {"pts": 5, "name": "Triángulo rectángulo", "pool": ["rp4e1", "rp4e2", "rp4e3", "rp4e4"]}]})
pr_c = concepts(P)
for k in ("expo", "idtrig", "triang"):  # conceptos del repaso usados en la práctica
    pr_c[k] = {"n": CONC[k][0], "f": CONC[k][1], "x": CONC[k][2], "home": "s7a" if k == "expo" else ("s9b" if k == "idtrig" else "s9c")}
ids_p = check_tags(P, pr_c)
pr = dict(BASE, id="cupc-pr", exam="Práctica (semanas 7 a 9)", short="Práctica", sub="Sem. 7 a 9",
  intro="Práctica de cálculo integral de la unidad 3, con las lecturas del curso: antiderivadas, integral definida como área, propiedades, teorema fundamental (parte 2), sustitución, integrales trigonométricas, sustitución trigonométrica y razonamiento cuantitativo. "
        "Todos los temas están abiertos; si te falta base, empieza por el bloque <b>Repaso</b>. Las integrales se corrigen solas: acepta cualquier antiderivada correcta. "
        "Interactivos: acumulador del área con signo, «¿qué u elijo?» y el triángulo de la sustitución trigonométrica. "
        "<b>Ojo con dos detalles de las lecturas</b>: el final del ejemplo 6 de sustitución y la respuesta de la práctica de razonamiento cuantitativo; aquí están corregidos. Se irá actualizando con las siguientes semanas.",
  form=fgrid("Hoja de repaso de la unidad 3.", P), topics=P, concepts=pr_c,
  sim={"minutes": 90, "intro": "Simulacro de la unidad 3 (20 puntos, 90 min), con una pregunta de cada tema.", "slots": [
    {"pts": 2, "name": "Sem. 7: antiderivadas", "pool": ["s7a3", "s7a4", "s7a6"]},
    {"pts": 2, "name": "Sem. 7: integral definida como área", "pool": ["s7b1", "s7b2", "s7b5"]},
    {"pts": 2, "name": "Sem. 8: propiedades", "pool": ["s8a2", "s8a3", "s8a7"]},
    {"pts": 3, "name": "Sem. 8: teorema fundamental", "pool": ["s8b6", "s8b8", "s8b10"]},
    {"pts": 3, "name": "Sem. 9: sustitución", "pool": ["s9a4", "s9a5", "s9a9", "s9a11"]},
    {"pts": 3, "name": "Sem. 9: integrales trigonométricas", "pool": ["s9b3", "s9b4", "s9b7", "s9b8"]},
    {"pts": 2, "name": "Sem. 9: sustitución trigonométrica", "pool": ["s9c5", "s9c7", "s9c9"]},
    {"pts": 3, "name": "Sem. 9: razonamiento cuantitativo", "pool": ["s9d1", "s9d2", "s9d3"]}]})
for blk, ids in ((rep, ids_r), (pr, ids_p)):
    assert sum(s["pts"] for s in blk["sim"]["slots"]) == 20
    for s in blk["sim"]["slots"]:
        for i in s["pool"]: assert i in ids, (blk["id"], i)

for blk in (rep, pr):
    p = os.path.join(RAIZ, 'cursos', blk["id"] + '.json')
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(blk, fh, indent=1, ensure_ascii=False); fh.write('\n')
idxp = os.path.join(RAIZ, 'cursos', 'indice.json')
idx = json.load(open(idxp, encoding='utf-8'))
for i in ("cupc-rep", "cupc-pr"):
    if i not in idx["cursos"]:
        k = idx["cursos"].index("alga-pr") + 1 if "alga-pr" in idx["cursos"] else len(idx["cursos"])
        idx["cursos"].insert(k + (1 if i == "cupc-pr" else 0), i)
with open(idxp, 'w', encoding='utf-8') as fh:
    json.dump(idx, fh, indent=1, ensure_ascii=False); fh.write('\n')
print('ok', sum(len(tt["ex"]) for tt in R), sum(len(tt["ex"]) for tt in P))
