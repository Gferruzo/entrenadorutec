#!/usr/bin/env python3
"""Matemáticas Discretas I · Semana 10 (Conjuntos II y Relaciones I) → cursos/md-ef.json.

Interactivos: tocar los pares de una relación en la cuadrícula A×B (tap) y ordenar demostraciones (order).
Uso: python3 tools/md_s10.py   (reejecutable: reemplaza los temas c10*). Las respuestas se calculan aquí mismo.
"""
import json, os
from itertools import combinations

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "cursos", "md-ef.json")
d = json.load(open(F, encoding="utf-8"))


def E(i, lvl, title, q, checks, steps, ans, hint, tags, chain=False):
    e = {"id": i, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans,
         "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}
    if chain:
        e["chain"] = True
    return e


def O(o, p="Respuesta"):
    assert len(o) == 5 and len(set(o)) == 5
    return {"p": p, "o": o}


def zid(x, y):
    return f"p{x}_{y}".replace("-", "m")


def grid(X, Y, xl="A", yl="B"):
    """Cuadrícula X×Y: columnas = primera componente, filas = segunda. Zonas = puntos (x, y)."""
    s = 34 if max(len(X), len(Y)) <= 6 else 28
    L, T = 46, 14
    W = L + s * len(X) + 18
    H = T + s * len(Y) + 46
    o = [f'<svg class="dg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for j, y in enumerate(Y):
        cy = T + s * (len(Y) - 1 - j) + s / 2
        o.append(f'<line class="dsh" x1="{L}" y1="{cy:.0f}" x2="{L + s * len(X)}" y2="{cy:.0f}"/>')
        o.append(f'<text class="dl" x="{L - 8}" y="{cy + 4:.0f}" text-anchor="end">{y}</text>')
    for i, x in enumerate(X):
        cx = L + s * i + s / 2
        o.append(f'<line class="dsh" x1="{cx:.0f}" y1="{T}" x2="{cx:.0f}" y2="{T + s * len(Y)}"/>')
        o.append(f'<text class="dl" x="{cx:.0f}" y="{T + s * len(Y) + 18}" text-anchor="middle">{x}</text>')
    o.append(f'<text class="dm" x="{L + s * len(X) / 2:.0f}" y="{H - 6}" text-anchor="middle">1.ª componente ({xl})</text>')
    o.append(f'<text class="dm" x="12" y="{T + s * len(Y) / 2:.0f}" text-anchor="middle" transform="rotate(-90 12 {T + s * len(Y) / 2:.0f})">2.ª ({yl})</text>')
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            cx = L + s * i + s / 2
            cy = T + s * (len(Y) - 1 - j) + s / 2
            o.append(f'<circle data-z="{zid(x, y)}" cx="{cx:.0f}" cy="{cy:.0f}" r="{s * 0.34:.0f}"/>')
    o.append("</svg>")
    return "".join(o)


def tap(X, Y, R, p, e, xl="A", yl="B"):
    return {"t": "tap", "p": p, "svg": grid(X, Y, xl, yl), "a": [zid(x, y) for x, y in R], "multi": True, "e": e}


def pares(R):
    return "\\(\\{" + ",".join(f"({x},{y})" for x, y in R) + "\\}\\)"


# ---------------------------------------------------------------- cálculos
A1, B1 = [1, 2, 3], [2, 3, 4]
R1 = [(x, y) for x in A1 for y in B1 if x + y == 5]
assert R1 == [(1, 4), (2, 3), (3, 2)]
A2, B2 = [2, 3, 4], [2, 6, 8]
R2 = [(x, y) for x in A2 for y in B2 if y % x == 0]
R2i = sorted((y, x) for x, y in R2)
assert R2 == [(2, 2), (2, 6), (2, 8), (3, 6), (4, 8)]
A3, B3 = [3, 4, 5], [4, 5, 6]
R3 = [(x, y) for x in A3 for y in B3 if x < y]
assert len(R3) == 6
A4 = [3, 4, 5, 6, 7]
R4 = [(x, y) for x in A4 for y in A4 if (x - y) % 2 == 0 and x > y]
assert sorted(R4) == [(5, 3), (6, 4), (7, 3), (7, 5)]
A5 = list(range(9))
R5 = [(x, y) for x in A5 for y in A5 if (x * x - y * y) % 5 == 0]
assert len(R5) == 29
edades = {"A": 15, "B": 18, "C": 15, "D": 16, "E": 15, "F": 17, "G": 18, "H": 18}
n_imp = sum(1 for m in edades for n in edades if (edades[m] + edades[n]) % 2 == 1)
assert n_imp == 32
assert 2 ** 6 == 64 and 2 ** 6 * 1 == 64 and 2 ** 3 * 2 ** 4 == 128
An = lambda n: {-i for i in range(1, n + 1)}
assert len(An(4) | An(3)) * len(An(5) - An(3)) == 8
ok28 = [(n, b) for n in range(8) for b in range(8) if 2 ** n * b == 20]
assert ok28 == [(2, 5)]
Aset = {(k * k - 1) // 2 for k in range(0, 200) if (k * k - 1) % 2 == 0 and k * k >= 1}
Bset = {x for x in range(0, 100) if x * x == 8 * x}
Cset = {x for x in range(0, 100) if x * x - 32 * x + 192 == 0}
assert (Bset - Aset) & Cset == {8} and ({8} - Aset) & Cset == {8}
PA = {frozenset(c) for r in range(4) for c in combinations({3, 4, 7}, r)}
PB = {frozenset(c) for r in range(4) for c in combinations({4, 6, 7}, r)}
assert PA & PB == {frozenset(), frozenset({4}), frozenset({7}), frozenset({4, 7})}

# ---------------------------------------------------------------- Tema 1
T1 = {
 "id": "c10prod",
 "name": "Sem. 10 · Producto cartesiano, conjunto potencia y cardinalidad",
 "teo": (
  "<p><strong>Producto cartesiano:</strong> \\(A\\times B=\\{(a,b): a\\in A\\wedge b\\in B\\}\\). En un par ordenado importa el orden: \\((a,b)\\ne(b,a)\\) si \\(a\\ne b\\), así que en general \\(A\\times B\\ne B\\times A\\).</p>"
  "<p class=\"ej\"><b>Ejemplo:</b> \\(A=\\{0,1,2,3\\}\\), \\(B=\\{0,5\\}\\): \\(A\\times B=\\{(0,0),(0,5),\\) \\((1,0),(1,5),\\) \\((2,0),(2,5),\\) \\((3,0),(3,5)\\}\\).</p>"
  "<p><strong>Conjunto potencia:</strong> \\(\\mathcal P(A)=\\{X: X\\subseteq A\\}\\). Decir \\(X\\in\\mathcal P(A)\\) es lo mismo que \\(X\\subseteq A\\). Siempre \\(\\varnothing\\in\\mathcal P(A)\\) y \\(A\\in\\mathcal P(A)\\).</p>"
  "<p class=\"ej\">\\(\\mathcal P(\\{a,b,c\\})=\\{\\varnothing,\\) \\(\\{a\\},\\{b\\},\\{c\\},\\) \\(\\{a,b\\},\\{a,c\\},\\{b,c\\},\\) \\(\\{a,b,c\\}\\}\\)</p>"
  "<p><strong>Propiedades del cardinal</strong> (A y B finitos):</p><ol><li>\\(|A\\cup B|=|A|+|B|-|A\\cap B|\\)</li><li>Si \\(|A|=n\\), entonces \\(|\\mathcal P(A)|=2^n\\)</li><li>Si \\(A\\subseteq B\\), entonces \\(|A|\\le|B|\\)</li><li>\\(|A\\times B|=|A|\\cdot|B|\\)</li></ol>"
  "<div class=\"err\"><b>Trampas:</b> los elementos de \\(\\mathcal P(A)\\) son <em>conjuntos</em>: \\(\\{a\\}\\in\\mathcal P(A)\\) pero \\(a\\notin\\mathcal P(A)\\). Y \\(|\\mathcal P(\\varnothing)|=2^0=1\\), porque \\(\\mathcal P(\\varnothing)=\\{\\varnothing\\}\\).</div>"
 ),
 "form": [
  "\\(A\\times B=\\{(a,b):a\\in A,\\ b\\in B\\}\\) · \\((a,b)\\ne(b,a)\\)",
  "\\(|A\\times B|=|A|\\cdot|B|\\)",
  "\\(X\\in\\mathcal P(A)\\iff X\\subseteq A\\)",
  "\\(|\\mathcal P(A)|=2^{|A|}\\) · \\(\\mathcal P(\\varnothing)=\\{\\varnothing\\}\\)",
  "\\(|A\\cup B|=|A|+|B|-|A\\cap B|\\)",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Esta semana se construyen conjuntos nuevos a partir de otros: los <strong>pares</strong> de \\(A\\times B\\) y los <strong>subconjuntos</strong> de \\(\\mathcal P(A)\\). Contarlos es multiplicar: cada elemento de A se combina con cada uno de B, y cada elemento de A puede estar o no en un subconjunto (2 opciones, \\(2^n\\) en total).</p>"
  "<h3>Cómo calcular sin listar</h3><ul><li>\\(|A\\times B|\\): multiplica los cardinales.</li><li>\\(|\\mathcal P(A)\\times\\mathcal P(B)|=2^{|A|}\\cdot2^{|B|}\\).</li><li>\\(\\mathcal P(A)\\cap\\mathcal P(B)=\\mathcal P(A\\cap B)\\): un conjunto es subconjunto de ambos si y solo si es subconjunto de la intersección.</li></ul>"
  "<div class=\"err\"><b>Ojo:</b> \\(\\mathcal P(A\\cup B)\\) <em>no</em> es \\(\\mathcal P(A)\\cup\\mathcal P(B)\\) en general: \\(\\{1,2\\}\\subseteq\\{1\\}\\cup\\{2\\}\\), pero no está en \\(\\mathcal P(\\{1\\})\\) ni en \\(\\mathcal P(\\{2\\})\\).</div>"
 ),
 "ex": [
  E("cp1", 1, "¿Qué par está en A × B?",
    "<p>\\(A=\\{0,1,2,3\\}\\), \\(B=\\{0,5\\}\\). ¿Cuál par pertenece a \\(A\\times B\\)?</p>",
    [O(["\\((3,5)\\)", "\\((5,3)\\)", "\\((5,0)\\)", "\\((0,1)\\)", "\\((2,2)\\)"])],
    ["En \\(A\\times B\\) la primera componente viene de A y la segunda de B.",
     "\\((3,5)\\): \\(3\\in A\\), \\(5\\in B\\) ✓. \\((5,3)\\) y \\((5,0)\\) tienen \\(5\\notin A\\) primero; \\((0,1)\\) y \\((2,2)\\) tienen segunda componente fuera de B."],
    "\\((3,5)\\)", "1.ª de A, 2.ª de B.", [["prodc"], ["prodc"]]),
  E("cp2", 1, "Contar sin listar",
    "<p>\\(A=\\{1,2,3\\}\\) y \\(B=\\{3,4,5,6\\}\\). Calcula:</p>",
    [{"t": "num", "p": "Cardinales", "f": [
      {"l": "\\(|A\\times B|=\\)", "a": 12, "e": "Multiplica los cardinales: 3 · 4."},
      {"l": "\\(|\\mathcal P(A\\cup B)|=\\)", "a": 64, "e": "\\(A\\cup B=\\{1,\\dots,6\\}\\) tiene 6 elementos (el 3 se cuenta una vez)."},
      {"l": "\\(|\\mathcal P(A)\\times\\mathcal P(B)|=\\)", "a": 128, "e": "\\(2^3\\cdot2^4\\)."}]}],
    ["\\(|A\\times B|=3\\cdot4=12\\).",
     "\\(A\\cup B=\\{1,2,3,4,5,6\\}\\): \\(|\\mathcal P(A\\cup B)|=2^6=64\\).",
     "\\(|\\mathcal P(A)\\times\\mathcal P(B)|=2^3\\cdot2^4=8\\cdot16=128\\)."],
    "12 · 64 · 128", "\\(|\\mathcal P(X)|=2^{|X|}\\)", [["cardp", "prodc"], ["cardp", "cardn"], ["cardp", "pot"]]),
  E("cp3", 1, "¿Elemento o no?",
    "<p>\\(A=\\{a,b,c\\}\\). ¿Cuál <strong>no</strong> es elemento de \\(\\mathcal P(A)\\)?</p>",
    [O(["\\(a\\)", "\\(\\varnothing\\)", "\\(\\{a\\}\\)", "\\(\\{a,b,c\\}\\)", "\\(\\{b,c\\}\\)"])],
    ["Los elementos de \\(\\mathcal P(A)\\) son los <em>subconjuntos</em> de A.",
     "\\(\\varnothing\\), \\(\\{a\\}\\), \\(\\{b,c\\}\\) y \\(A\\) son subconjuntos. \\(a\\) es un elemento de A, no un subconjunto: \\(a\\in A\\), pero \\(a\\notin\\mathcal P(A)\\)."],
    "\\(a\\)", "¿Es un conjunto contenido en A?", [["pot"], ["pot", "pert"]]),
  E("cp4", 2, "Intersección de potencias",
    "<p>\\(A=\\{3,4,7\\}\\), \\(B=\\{4,6,7\\}\\). Halla \\(\\mathcal P(A)\\cap\\mathcal P(B)\\).</p>",
    [O(["\\(\\{\\varnothing,\\{4\\},\\{7\\},\\{4,7\\}\\}\\)", "\\(\\{4,7\\}\\)", "\\(\\{\\{4\\},\\{7\\},\\{4,7\\}\\}\\)", "\\(\\{\\varnothing,\\{4,7\\}\\}\\)", "\\(\\varnothing\\)"])],
    ["\\(X\\in\\mathcal P(A)\\cap\\mathcal P(B)\\) \\(\\iff X\\subseteq A\\wedge X\\subseteq B\\) \\(\\iff X\\subseteq A\\cap B\\).",
     "\\(A\\cap B=\\{4,7\\}\\), así que la respuesta es \\(\\mathcal P(\\{4,7\\})=\\) \\(\\{\\varnothing,\\{4\\},\\{7\\},\\{4,7\\}\\}\\). No olvides \\(\\varnothing\\)."],
    "\\(\\mathcal P(\\{4,7\\})\\)", "Subconjunto de ambos = subconjunto de \\(A\\cap B\\).", [["pot", "opsc"], ["pot"]]),
  E("cp5", 2, "Familias \\(A_n\\)",
    "<p>Sea \\(A_n=\\{-i: i\\in\\mathbb N,\\ 1\\le i\\le n\\}\\). Calcula \\(|(A_4\\cup A_3)\\times(A_5-A_3)|\\).</p>",
    [{"t": "num", "p": "Por partes", "f": [
      {"l": "\\(|A_4\\cup A_3|=\\)", "a": 4, "e": "\\(A_3\\subseteq A_4\\), así que la unión es \\(A_4\\)."},
      {"l": "\\(|A_5-A_3|=\\)", "a": 2, "e": "Quedan \\(-4\\) y \\(-5\\)."},
      {"l": "\\(|(A_4\\cup A_3)\\times(A_5-A_3)|=\\)", "a": 8}]}],
    ["\\(A_3=\\{-1,-2,-3\\}\\) \\(\\subseteq A_4=\\{-1,-2,-3,-4\\}\\): \\(A_4\\cup A_3=A_4\\), con 4 elementos.",
     "\\(A_5-A_3=\\{-4,-5\\}\\), con 2 elementos.", "\\(|A\\times B|=|A|\\cdot|B|=4\\cdot2=8\\)."],
    "8", "Primero cada conjunto, luego multiplica.", [["opsc"], ["opsc"], ["cardp"]]),
  E("cp6", 3, "Despejar un cardinal",
    "<p>\\(A\\) y \\(B\\) están incluidos en \\(U=\\{1,2,3,4,5,6,7\\}\\) y \\(|\\mathcal P(A)\\times B|=20\\). ¿Cuánto vale \\(|B|\\)?</p>",
    [{"t": "num", "p": "Respuesta", "f": [{"l": "\\(|B|=\\)", "a": 5, "e": "Escribe \\(2^{|A|}\\cdot|B|=20\\) y prueba \\(|A|=0,1,2,\\dots\\) con \\(|B|\\le7\\)."}]}],
    ["\\(|\\mathcal P(A)\\times B|=2^{|A|}\\cdot|B|=20\\), con \\(0\\le|B|\\le7\\).",
     "\\(|A|=0\\Rightarrow|B|=20\\) ✗; \\(|A|=1\\Rightarrow|B|=10\\) ✗; \\(|A|=2\\Rightarrow|B|=5\\) ✓; \\(|A|\\ge3\\): \\(2^{|A|}\\) no divide a 20.",
     "Por tanto \\(|B|=5\\)."],
    "5", "\\(2^{|A|}\\cdot|B|=20\\)", [["cardp"], ["cardp", "pot"], []]),
  E("cp7", 2, "Verdadero o falso",
    "<p>¿Cuál afirmación es <strong>verdadera</strong>?</p>",
    [O(["Si \\(A=\\varnothing\\), entonces \\(|\\mathcal P(A)|=1\\)",
        "Si \\(A=\\varnothing\\), entonces \\(|\\mathcal P(A)|=0\\)",
        "Existe un conjunto finito \\(A\\) con \\(|\\mathcal P(A)|=30\\)",
        "Si \\((x,y)\\in A\\times A\\), entonces \\(x=y\\)",
        "\\(A\\times B=B\\times A\\) para cualesquiera A y B"])],
    ["\\(\\mathcal P(\\varnothing)=\\{\\varnothing\\}\\) tiene un elemento: \\(2^0=1\\).",
     "\\(|\\mathcal P(A)|\\) siempre es potencia de 2, y 30 no lo es. En \\(A\\times A\\) hay pares como \\((1,2)\\). Y \\(\\{1\\}\\times\\{2\\}=\\{(1,2)\\}\\ne\\{(2,1)\\}\\)."],
    "\\(|\\mathcal P(\\varnothing)|=1\\)", "\\(2^0\\)", [["pot", "cardp"], ["cardp", "prodc"]]),
 ],
}

# ---------------------------------------------------------------- Tema 2
T2 = {
 "id": "c10alg",
 "name": "Sem. 10 · Álgebra de conjuntos y demostraciones",
 "teo": (
  "<p><strong>Relaciones de subconjuntos</strong> (para todos A, B, C):</p><ul><li>\\(A\\cap B\\subseteq A\\) y \\(A\\cap B\\subseteq B\\) (inclusión de la intersección)</li><li>\\(A\\subseteq A\\cup B\\) y \\(B\\subseteq A\\cup B\\) (inclusión en la unión)</li><li>Si \\(A\\subseteq B\\) y \\(B\\subseteq C\\), entonces \\(A\\subseteq C\\) (transitividad)</li></ul>"
  "<div class=\"tbl\"><table><tr><th>Ley</th><th>Unión</th><th>Intersección</th></tr>"
  "<tr><td>Conmutativa</td><td>\\(A\\cup B=B\\cup A\\)</td><td>\\(A\\cap B=B\\cap A\\)</td></tr>"
  "<tr><td>Distributiva</td><td>\\(A\\cup(B\\cap C)=(A\\cup B)\\cap(A\\cup C)\\)</td><td>\\(A\\cap(B\\cup C)=(A\\cap B)\\cup(A\\cap C)\\)</td></tr>"
  "<tr><td>De Morgan</td><td>\\(\\overline{A\\cup B}=\\overline A\\cap\\overline B\\)</td><td>\\(\\overline{A\\cap B}=\\overline A\\cup\\overline B\\)</td></tr>"
  "<tr><td>Idempotente</td><td>\\(A\\cup A=A\\)</td><td>\\(A\\cap A=A\\)</td></tr>"
  "<tr><td>Identidad</td><td>\\(A\\cup\\varnothing=A\\)</td><td>\\(A\\cap U=A\\)</td></tr>"
  "<tr><td>Inversa</td><td>\\(A\\cup\\overline A=U\\)</td><td>\\(A\\cap\\overline A=\\varnothing\\)</td></tr>"
  "<tr><td>Dominación</td><td>\\(A\\cup U=U\\)</td><td>\\(A\\cap\\varnothing=\\varnothing\\)</td></tr>"
  "<tr><td>Absorción</td><td>\\(A\\cup(A\\cap B)=A\\)</td><td>\\(A\\cap(A\\cup B)=A\\)</td></tr></table></div>"
  "<p>Doble complemento: \\(\\overline{\\overline A}=A\\). Diferencia: \\(A-B=A\\cap\\overline B\\).</p>"
  "<p><strong>Cómo demostrar:</strong> se traduce cada operación a lógica (\\(\\cup\\to\\vee\\), \\(\\cap\\to\\wedge\\), complemento \\(\\to\\neg\\)) y se aplica la ley lógica que corresponde, justificando cada paso.</p>"
 ),
 "form": [
  "\\(A\\cap B\\subseteq A\\) · \\(A\\subseteq A\\cup B\\) · transitividad de \\(\\subseteq\\)",
  "Absorción: \\(A\\cup(A\\cap B)=A\\), \\(A\\cap(A\\cup B)=A\\)",
  "De Morgan: \\(\\overline{A\\cup B}=\\overline A\\cap\\overline B\\)",
  "\\(A-B=A\\cap\\overline B\\)",
  "Demostrar: \\(x\\in\\dots\\iff\\) lógica \\(\\iff\\dots\\), con la ley de cada paso",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Cada ley de conjuntos es una ley lógica disfrazada: \\(x\\in A\\cup B\\) significa \\(x\\in A\\vee x\\in B\\). Por eso las demostraciones de esta semana son <strong>cadenas de equivalencias</strong> que empiezan en \\(x\\in\\) (lado izquierdo) y terminan en \\(x\\in\\) (lado derecho).</p>"
  "<h3>Plantilla</h3><div class=\"ej\"><p>\\(x\\in A\\cup A\\iff x\\in A\\vee x\\in A\\) <em>(definición de \\(\\cup\\))</em></p><p>\\(\\iff x\\in A\\) <em>(idempotencia \\(p\\vee p\\equiv p\\))</em></p><p>Por tanto \\(A\\cup A=A\\).</p></div>"
  "<p>Para una contención (\\(\\subseteq\\)) basta una implicación: tomar \\(x\\) arbitrario del lado izquierdo y llegar a que está en el derecho.</p>"
  "<div class=\"err\"><b>Errores frecuentes:</b> saltarse la justificación de un paso, usar «=» entre proposiciones en vez de \\(\\iff\\), y olvidar que \\(\\neg(x\\in A\\wedge x\\in B)\\) se abre con De Morgan.</div>"
 ),
 "ex": [
  E("ca1", 1, "Ordena: \\(A\\cap B\\subseteq A\\)",
    "<p>Ordena la demostración de que \\(A\\cap B\\subseteq A\\).</p>",
    [{"t": "order", "p": "Toca los pasos en orden.", "items": [
      "Sea \\(x\\in A\\cap B\\) arbitrario.",
      "Por definición de \\(\\cap\\): \\(x\\in A\\wedge x\\in B\\).",
      "Por especificación (\\(p\\wedge q\\Rightarrow p\\)): \\(x\\in A\\).",
      "Como \\(x\\) era arbitrario, \\(A\\cap B\\subseteq A\\)."]}],
    ["Para probar una contención se toma un elemento arbitrario del lado izquierdo.",
     "Se traduce \\(\\cap\\) a \\(\\wedge\\) y se usa la ley de especificación (simplificación) para quedarse con \\(x\\in A\\).",
     "Al ser \\(x\\) arbitrario, vale para todos: \\(A\\cap B\\subseteq A\\). De forma similar, \\(A\\cap B\\subseteq B\\)."],
    "Tomar x → definición → especificación → conclusión", "Empieza con «Sea x…».", [["subc"], ["algc"], ["subc"]]),
  E("ca2", 2, "Ordena: \\(A-B=A-(A\\cap B)\\)",
    "<p>Ordena la cadena de equivalencias que demuestra \\(A-(A\\cap B)=A-B\\).</p>",
    [{"t": "order", "p": "Toca los pasos en orden.", "items": [
      "\\(x\\in A-(A\\cap B)\\iff x\\in A\\wedge\\neg(x\\in A\\wedge x\\in B)\\) — definición de \\(-\\) y de \\(\\cap\\)",
      "\\(\\iff x\\in A\\wedge(x\\notin A\\vee x\\notin B)\\) — De Morgan",
      "\\(\\iff(x\\in A\\wedge x\\notin A)\\vee(x\\in A\\wedge x\\notin B)\\) — distributiva",
      "\\(\\iff F\\vee(x\\in A\\wedge x\\notin B)\\) — contradicción \\(p\\wedge\\neg p\\equiv F\\)",
      "\\(\\iff x\\in A\\wedge x\\notin B\\) — identidad \\(F\\vee p\\equiv p\\)",
      "\\(\\iff x\\in A-B\\) — definición de \\(-\\)"]}],
    ["Se parte del lado más complicado y se traduce a lógica: \\(x\\in A\\wedge\\neg(x\\in A\\wedge x\\in B)\\).",
     "De Morgan abre la negación; la distributiva separa en dos casos; el primero es una contradicción.",
     "Por identidad queda \\(x\\in A\\wedge x\\notin B\\), que es la definición de \\(x\\in A-B\\). Como todo fue \\(\\iff\\), los conjuntos son iguales."],
    "Definición → De Morgan → distributiva → contradicción → identidad → definición", "Abre la negación primero.",
    [["algc", "opsc"], ["algc"], ["igconj"]]),
  E("ca3", 2, "Ordena: si A y B son disjuntos, \\(A-B=A\\)",
    "<p>Ordena la demostración por doble contención.</p>",
    [{"t": "order", "p": "Toca los pasos en orden.", "items": [
      "\\(A-B\\subseteq A\\) por definición: todo \\(x\\in A-B\\) cumple \\(x\\in A\\).",
      "Para la otra contención, sea \\(x\\in A\\) arbitrario.",
      "Si fuera \\(x\\in B\\), tendríamos \\(x\\in A\\cap B=\\varnothing\\), absurdo; luego \\(x\\notin B\\).",
      "Entonces \\(x\\in A\\wedge x\\notin B\\), es decir, \\(x\\in A-B\\); así \\(A\\subseteq A-B\\).",
      "Por doble contención, \\(A-B=A\\)."]}],
    ["Igualdad = doble contención. \\(A-B\\subseteq A\\) es inmediata.",
     "Para \\(A\\subseteq A-B\\) se toma \\(x\\in A\\) y se usa la hipótesis \\(A\\cap B=\\varnothing\\) por contradicción para obtener \\(x\\notin B\\).",
     "Con las dos contenciones, \\(A-B=A\\)."],
    "Fácil → tomar x → absurdo → x ∈ A − B → doble contención", "Doble contención.", [["igconj"], ["subc"], ["igconj"]]),
  E("ca4", 1, "Simplifica",
    "<p>Simplifica \\((A\\cap B)\\cup A\\).</p>",
    [O(["\\(A\\)", "\\(B\\)", "\\(A\\cap B\\)", "\\(A\\cup B\\)", "\\(\\varnothing\\)"])],
    ["Por conmutativa, \\((A\\cap B)\\cup A=A\\cup(A\\cap B)\\).", "Por absorción, \\(A\\cup(A\\cap B)=A\\)."],
    "\\(A\\)", "Absorción.", [["algc"], ["algc"]]),
  E("ca5", 2, "Simplifica una diferencia",
    "<p>Simplifica \\((A-B)\\cup(A\\cap B)\\).</p>",
    [O(["\\(A\\)", "\\(B\\)", "\\(A\\cup B\\)", "\\(A\\cap B\\)", "\\(A-B\\)"])],
    ["\\((A\\cap\\overline B)\\cup(A\\cap B)=A\\cap(\\overline B\\cup B)\\) (distributiva).",
     "\\(=A\\cap U\\) (inversa) \\(=A\\) (identidad). Idea: lo de A que no está en B, más lo de A que sí está en B, es todo A."],
    "\\(A\\)", "Escribe \\(A-B=A\\cap\\overline B\\).", [["algc", "opsc"], ["algc"]]),
  E("ca6", 1, "Nombre de la ley",
    "<p>¿Qué ley es \\(\\overline{A\\cap B}=\\overline A\\cup\\overline B\\)?</p>",
    [O(["De Morgan", "Distributiva", "Absorción", "Doble complemento", "Inversa"])],
    ["El complemento de una intersección es la unión de los complementos: <b>De Morgan</b>.",
     "Es la versión de conjuntos de \\(\\neg(p\\wedge q)\\equiv\\neg p\\vee\\neg q\\)."],
    "De Morgan", "Niega e invierte la operación.", [["algc"], ["algc"]]),
  E("ca7", 2, "Ejercicio de clase: \\((B-A)\\cap C\\)",
    "<p>\\(A=\\left\\{x\\in\\mathbb N: x=\\tfrac{k^2-1}{2},\\ k\\in\\mathbb N\\right\\}\\), \\(B=\\{x\\in\\mathbb N: x^2=8x\\}\\), \\(C=\\{x\\in\\mathbb N: x^2-32x+192=0\\}\\). Halla \\((B-A)\\cap C\\).</p>",
    [O(["\\(\\{8\\}\\)", "\\(\\{8,24\\}\\)", "\\(\\{0,8\\}\\)", "\\(\\{24\\}\\)", "\\(\\varnothing\\)"])],
    ["\\(A\\): solo los \\(k\\) impares dan natural: \\(k=1,3,5,7,\\dots\\) \\(\\Rightarrow x=0,4,12,24,40,\\dots\\)",
     "\\(B\\): \\(x(x-8)=0\\Rightarrow B=\\{0,8\\}\\) (o \\(\\{8\\}\\) si \\(0\\notin\\mathbb N\\)). \\(C\\): \\((x-8)(x-24)=0\\Rightarrow C=\\{8,24\\}\\).",
     "\\(B-A=\\{8\\}\\) (el 0 está en A) y \\(\\{8\\}\\cap\\{8,24\\}=\\{8\\}\\). Ojo: 24 está en C pero no en B."],
    "\\(\\{8\\}\\)", "Lista cada conjunto primero.", [["defconj"], ["opsc"], ["opsc"]]),
 ],
}

# ---------------------------------------------------------------- Tema 3
T3 = {
 "id": "c10rel",
 "name": "Sem. 10 · Relaciones: pares, inversa y digrafo",
 "teo": (
  "<p><strong>Relación de A en B:</strong> cualquier subconjunto \\(R\\subseteq A\\times B\\). Se escribe \\(xRy\\iff(x,y)\\in R\\).</p>"
  "<p class=\"ej\">\\(A=\\{1,2,3\\}\\), \\(B=\\{3,5\\}\\): \\(\\{(3,3)\\}\\), \\(\\{(1,3),(3,5)\\}\\) y \\(\\varnothing\\) son relaciones de A en B; \\(\\{(1,2),(2,5)\\}\\) no, porque \\(2\\notin B\\). Hay \\(2^{|A\\times B|}=2^6=64\\) relaciones posibles.</p>"
  "<p><strong>Relación inversa:</strong> \\(R^{-1}=\\{(y,x)\\in B\\times A:(x,y)\\in R\\}\\). Se invierte cada par: \\((y,x)\\in R^{-1}\\iff(x,y)\\in R\\).</p>"
  "<p><strong>Relación sobre A:</strong> una relación de A en A. Se dibuja como <strong>grafo dirigido</strong> (digrafo): una flecha de x a y si \\(xRy\\), y un <em>bucle</em> en x si \\(xRx\\).</p>"
  "<p>En la cuadrícula de \\(A\\times B\\), cada punto es un par: las columnas son la primera componente y las filas, la segunda. Una relación es una selección de puntos, y su inversa es la misma selección reflejada (se intercambian los ejes).</p>"
 ),
 "form": [
  "Relación de A en B: \\(R\\subseteq A\\times B\\) · \\(xRy\\iff(x,y)\\in R\\)",
  "Número de relaciones: \\(2^{|A|\\cdot|B|}\\)",
  "\\(R^{-1}=\\{(y,x):(x,y)\\in R\\}\\)",
  "Digrafo: flecha x → y si xRy · bucle si xRx",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Una relación es simplemente <strong>una lista de pares</strong> elegidos de \\(A\\times B\\) según una regla. Para hallarla, recorre todos los pares y quédate con los que cumplen la regla.</p>"
  "<h3>Método</h3><ol><li>Arma la cuadrícula de \\(A\\times B\\) (o lista todos los pares).</li><li>Prueba la regla en cada par.</li><li>Para la inversa, voltea cada par: \\((x,y)\\to(y,x)\\).</li></ol>"
  "<div class=\"ej\"><b>Ejemplo:</b> \\(A=\\{2,3,4\\}\\), \\(B=\\{2,6,8\\}\\), \\(xRy\\iff x\\mid y\\). \\(R=\\{(2,2),(2,6),(2,8),(3,6),(4,8)\\}\\) y \\(R^{-1}=\\{(2,2),(6,2),(8,2),(6,3),(8,4)\\}\\).</div>"
  "<div class=\"err\"><b>Errores frecuentes:</b> invertir el orden del par (en \\(A\\times B\\) la primera componente es de A), olvidar pares como \\((2,2)\\) cuando el número está en ambos conjuntos, y en un digrafo olvidar los bucles.</div>"
 ),
 "ex": [
  E("cr1", 1, "Toca los pares: \\(x+y=5\\)",
    "<p>\\(A=\\{1,2,3\\}\\), \\(B=\\{2,3,4\\}\\) y \\(xRy\\iff x+y=5\\). Toca en la cuadrícula los pares de R.</p>",
    [tap(A1, B1, R1, "Toca todos los pares de R", "Suma la columna (x) y la fila (y): deben dar 5.")],
    ["Recorre cada x de A y busca el y de B con \\(y=5-x\\).",
     "\\(x=1\\to y=4\\) ✓; \\(x=2\\to y=3\\) ✓; \\(x=3\\to y=2\\) ✓. " + "\\(R=\\{(1,4),(2,3),(3,2)\\}\\)."],
    "\\(R=\\{(1,4),(2,3),(3,2)\\}\\)", "\\(y=5-x\\)", [["rel"], ["rel"]]),
  E("cr2", 2, "Divide a: R y su inversa",
    "<p>\\(A=\\{2,3,4\\}\\), \\(B=\\{2,6,8\\}\\) y \\(xRy\\iff x\\mid y\\).</p>",
    [tap(A2, B2, R2, "Parte 1: toca los pares de R ⊆ A × B", "x divide a y: y es múltiplo de x. No olvides (2, 2)."),
     tap(B2, A2, R2i, "Parte 2: ahora toca los pares de R⁻¹ ⊆ B × A", "Voltea cada par de R: (x, y) → (y, x).", "B", "A")],
    ["\\(2\\mid2\\), \\(2\\mid6\\), \\(2\\mid8\\), \\(3\\mid6\\), \\(4\\mid8\\): " + pares(R2) + ".",
     "\\(R^{-1}\\) se obtiene volteando cada par: " + pares(R2i) + ". En la cuadrícula se ve como la misma figura con los ejes intercambiados."],
    "R = {(2,2),(2,6),(2,8),(3,6),(4,8)} · R⁻¹ = pares volteados", "y es múltiplo de x.",
    [["rel"], ["relinv"]], chain=True),
  E("cr3", 1, "Toca los pares: \\(x<y\\)",
    "<p>\\(A=\\{3,4,5\\}\\), \\(B=\\{4,5,6\\}\\) y \\(xRy\\iff x<y\\). Toca los pares de R.</p>",
    [tap(A3, B3, R3, "Toca todos los pares de R", "En cada columna x, marca las filas con y mayor que x.")],
    ["Para \\(x=3\\): \\(y=4,5,6\\). Para \\(x=4\\): \\(y=5,6\\). Para \\(x=5\\): \\(y=6\\).",
     "\\(R=\\{(3,4),(3,5),(3,6),\\) \\((4,5),(4,6),(5,6)\\}\\), con 6 pares; \\(R^{-1}\\) son los mismos volteados."],
    "6 pares", "Fila mayor que columna.", [["rel"], ["rel", "relinv"]]),
  E("cr4", 2, "Relación sobre A: paridad y orden",
    "<p>\\(A=\\{3,4,5,6,7\\}\\) y \\(xRy\\iff 2\\mid(x-y)\\ \\wedge\\ x>y\\). Toca los pares de R (cuadrícula \\(A\\times A\\)).</p>",
    [tap(A4, A4, R4, "Toca todos los pares de R", "x e y deben tener la misma paridad y x > y (no hay bucles).", "A", "A")],
    ["\\(2\\mid(x-y)\\) significa que x e y tienen la <b>misma paridad</b>; además \\(x>y\\).",
     "Impares: \\((5,3),(7,3),(7,5)\\). Pares: \\((6,4)\\). Ningún \\((x,x)\\), porque \\(x>x\\) es falso: en el digrafo no hay bucles."],
    "\\(\\{(5,3),(7,3),(7,5),(6,4)\\}\\)", "Misma paridad y x mayor.", [["rel"], ["digr"]]),
  E("cr5", 3, "Relación grande: \\(5\\mid(x^2-y^2)\\)",
    "<p>\\(A=\\{0,1,\\dots,8\\}\\) y \\(xSy\\iff 5\\mid(x^2-y^2)\\). Toca los pares de S.</p>",
    [tap(A5, A5, R5, "Toca todos los pares de S", "Agrupa por el resto de \\(x^2\\) entre 5: los del mismo grupo se relacionan entre sí (incluido consigo mismo).", "A", "A")],
    ["\\(5\\mid(x^2-y^2)\\iff x^2\\) y \\(y^2\\) dejan el mismo resto entre 5.",
     "Restos de \\(x^2\\): 0 → 0, 1 → 1, 2 → 4, 3 → 4, 4 → 1, 5 → 0, 6 → 1, 7 → 4, 8 → 4. Grupos: \\(\\{0,5\\}\\), \\(\\{1,4,6\\}\\), \\(\\{2,3,7,8\\}\\).",
     "Todo par dentro de un mismo grupo está en S: \\(2^2+3^2+4^2=29\\) pares. En el digrafo, cada número tiene bucle."],
    "29 pares (tres bloques: {0,5}, {1,4,6}, {2,3,7,8})", "Mira el resto de x² entre 5.", [["rel"], ["defdiv"], ["digr"]]),
  E("cr6", 1, "¿Es relación de A en B?",
    "<p>\\(A=\\{1,2,3\\}\\), \\(B=\\{3,5\\}\\). ¿Cuál es una relación de A en B?</p>",
    [O(["\\(\\{(1,3),(3,5)\\}\\)", "\\(\\{(1,2),(2,5)\\}\\)", "\\(\\{(3,1)\\}\\)", "\\(\\{(5,3)\\}\\)", "\\(\\{(1,3),(4,5)\\}\\)"])],
    ["Una relación de A en B es un subconjunto de \\(A\\times B\\): cada par tiene la primera componente en A y la segunda en B.",
     "\\((1,2)\\): \\(2\\notin B\\). \\((3,1)\\) y \\((5,3)\\) tienen la segunda componente fuera de B (y en el segundo, la primera fuera de A). \\((4,5)\\): \\(4\\notin A\\)."],
    "\\(\\{(1,3),(3,5)\\}\\)", "Revisa cada componente.", [["rel"], ["prodc"]]),
  E("cr7", 1, "¿Cuántas relaciones hay?",
    "<p>\\(A=\\{1,2,3\\}\\), \\(B=\\{3,5\\}\\). ¿Cuántas relaciones de A en B existen (contando \\(\\varnothing\\))?</p>",
    [{"t": "num", "p": "Respuesta", "f": [{"l": "Número de relaciones", "a": 64, "e": "Una relación es un subconjunto de \\(A\\times B\\): cuenta los elementos de \\(\\mathcal P(A\\times B)\\)."}]}],
    ["\\(|A\\times B|=3\\cdot2=6\\).", "Cada relación es un subconjunto de \\(A\\times B\\): hay \\(|\\mathcal P(A\\times B)|=2^6=64\\)."],
    "64", "Relaciones = subconjuntos de A × B.", [["cardp"], ["rel", "pot"]]),
  E("cr8", 2, "Relación entre subconjuntos",
    "<p>En \\(\\mathcal P(\\{a,b,c\\})\\) se define \\(ARB\\) si A tiene al menos tantos elementos como B. ¿Qué par <strong>no</strong> está en R?</p>",
    [O(["\\((\\{b,c\\},\\{a,b,c\\})\\)", "\\((\\{a,b\\},\\{b,c\\})\\)", "\\((\\{a\\},\\varnothing)\\)", "\\((\\{a,b,c\\},\\{a\\})\\)", "\\((\\varnothing,\\varnothing)\\)"])],
    ["Se compara \\(|A|\\ge|B|\\).", "\\(|\\{b,c\\}|=2<3=|\\{a,b,c\\}|\\): no se cumple. Los demás: \\(2\\ge2\\), \\(1\\ge0\\), \\(3\\ge1\\), \\(0\\ge0\\)."],
    "\\((\\{b,c\\},\\{a,b,c\\})\\)", "Compara cardinales.", [["rel", "cardn"], ["rel"]]),
  E("cr9", 2, "Edades con suma impar",
    "<p>Alumnos y edades: A 15, B 18, C 15, D 16, E 15, F 17, G 18, H 18. En \\(X=\\{A,\\dots,H\\}\\) se define \\(R=\\{(m,n): \\text{la suma de las edades es impar}\\}\\). ¿Cuántos pares tiene R?</p>",
    [{"t": "num", "p": "Respuesta", "f": [{"l": "\\(|R|=\\)", "a": 32, "e": "Una suma es impar si una edad es par y la otra impar. Cuenta los pares ordenados en ambos sentidos."}]}],
    ["Edad impar: A, C, E, F (4 alumnos). Edad par: B, D, G, H (4 alumnos).",
     "Suma impar ⇔ uno impar y otro par. Pares ordenados: \\(4\\cdot4\\) con el impar primero y \\(4\\cdot4\\) con el par primero: \\(32\\).",
     "No hay bucles: \\((m,m)\\) suma el doble, que es par."],
    "32", "Impar + par.", [["rel"], ["paridad"], ["rel"]]),
 ],
}

NUEVOS = [T1, T2, T3]

CONC = {
 "prodc": {"n": "Producto cartesiano", "f": "\\(A\\times B=\\{(a,b):a\\in A\\wedge b\\in B\\}\\)", "x": "Pares ordenados: \\((a,b)\\ne(b,a)\\), así que \\(A\\times B\\ne B\\times A\\) en general.", "home": "c10prod"},
 "pot": {"n": "Conjunto potencia", "f": "\\(\\mathcal P(A)=\\{X:X\\subseteq A\\}\\)", "x": "Sus elementos son conjuntos; siempre contiene a \\(\\varnothing\\) y a A.", "home": "c10prod"},
 "cardp": {"n": "Cardinales de construcciones", "f": "\\(|A\\times B|=|A||B|\\), \\(|\\mathcal P(A)|=2^{|A|}\\)", "x": "Además \\(|A\\cup B|=|A|+|B|-|A\\cap B|\\) y \\(A\\subseteq B\\Rightarrow|A|\\le|B|\\).", "home": "c10prod"},
 "algc": {"n": "Álgebra de conjuntos", "f": "De Morgan, distributiva, absorción, identidad, inversa…", "x": "Cada ley de conjuntos es una ley lógica: \\(\\cup\\to\\vee\\), \\(\\cap\\to\\wedge\\), complemento \\(\\to\\neg\\).", "home": "c10alg"},
 "rel": {"n": "Relación", "f": "\\(R\\subseteq A\\times B\\), \\(xRy\\iff(x,y)\\in R\\)", "x": "Hay \\(2^{|A||B|}\\) relaciones de A en B.", "home": "c10rel"},
 "relinv": {"n": "Relación inversa", "f": "\\(R^{-1}=\\{(y,x):(x,y)\\in R\\}\\)", "x": "Se voltea cada par; es una relación de B en A.", "home": "c10rel"},
 "digr": {"n": "Digrafo", "f": "Flecha x → y si xRy; bucle si xRx", "x": "Representa una relación sobre un conjunto A.", "home": "c10rel"},
}

# ---------------------------------------------------------------- ensamblar
d["concepts"].update(CONC)
for t in NUEVOS:
    for e in t["ex"]:
        assert len(e["tags"]) == len(e["steps"]), e["id"]
        for l in e["tags"]:
            for k in l:
                assert k in d["concepts"], (e["id"], k)

top = [t for t in d["topics"] if not t["id"].startswith("c10")]
pos = next(i for i, t in enumerate(top) if t["id"] == "c9op") + 1
d["topics"] = top[:pos] + NUEVOS + top[pos:]

d["intro"] = ("Repaso acumulado con todos los temas abiertos: primero los temas del parcial, luego <b>la semana 9: conjuntos I</b> "
  "(definición y notación, cardinal, subconjuntos e igualdad con demostraciones, diagramas de Venn y operaciones) y <b>la semana 10: conjuntos II y relaciones</b> "
  "(producto cartesiano, conjunto potencia, cardinalidad, álgebra de conjuntos con demostraciones, relaciones, inversa y digrafo), que pesa más en el simulacro. "
  "En el examen real debes justificar todo: aquí marcas y luego revisas la justificación en «Ver solución». Se actualiza cada semana.")

CARDS = ('<div><b>Producto cartesiano</b><br>\\(|A\\times B|=|A|\\cdot|B|\\) · \\((a,b)\\ne(b,a)\\)</div>'
  '<div><b>Potencia</b><br>\\(X\\in\\mathcal P(A)\\iff X\\subseteq A\\) · \\(|\\mathcal P(A)|=2^n\\)</div>'
  '<div><b>Leyes</b><br>De Morgan · distributiva · absorción · \\(A-B=A\\cap\\overline B\\)</div>'
  '<div><b>Relación</b><br>\\(R\\subseteq A\\times B\\) · \\(2^{|A||B|}\\) relaciones</div>'
  '<div><b>Inversa y digrafo</b><br>\\(R^{-1}\\): voltear pares · bucle si \\(xRx\\)</div>')
f = d["form"]
if "Producto cartesiano</b>" not in f:
    assert f.endswith("</div></div>")
    d["form"] = f[:-len("</div>")] + CARDS + "</div>"

d["sim"]["slots"] = [
 {"pts": 1, "name": "Repaso parcial: lógica y cuantificadores", "pool": ["q9", "q10", "q11", "i9", "i10"]},
 {"pts": 1, "name": "Repaso parcial: demostraciones", "pool": ["t8", "t9", "t10", "dv6", "dv7"]},
 {"pts": 2, "name": "Sem. 9: definición y cardinal", "pool": ["cj3", "cj5", "cj7", "cx2"]},
 {"pts": 3, "name": "Sem. 9: subconjuntos e igualdad", "pool": ["cs3", "cs4", "cs5", "cs7", "cx1"]},
 {"pts": 2, "name": "Sem. 9: operaciones y Venn", "pool": ["co3", "co5", "co6", "co7", "cx3", "co8", "co9", "co10"]},
 {"pts": 3, "name": "Sem. 10: producto cartesiano y potencia", "pool": ["cp2", "cp4", "cp5", "cp6", "cp7"]},
 {"pts": 4, "name": "Sem. 10: álgebra de conjuntos", "pool": ["ca2", "ca3", "ca5", "ca7"]},
 {"pts": 4, "name": "Sem. 10: relaciones", "pool": ["cr2", "cr4", "cr5", "cr8", "cr9"]},
]
todos = {e["id"] for t in d["topics"] for e in t["ex"]} | {e["id"] for e in d.get("simEx", [])}
for s in d["sim"]["slots"]:
    for i in s["pool"]:
        assert i in todos, i
assert sum(s["pts"] for s in d["sim"]["slots"]) == 20
assert len(todos) == sum(len(t["ex"]) for t in d["topics"]) + len(d.get("simEx", [])), "ids repetidos"

with open(F, "w", encoding="utf-8") as o:
    json.dump(d, o, indent=1, ensure_ascii=False)
    o.write("\n")
print("ok:", [t["id"] for t in d["topics"]])
