# Helpers para construir cursos/bq-pr.json (Análisis Bioquímico · XTART)
import math

def opt(p, ok, *wrong, **kw):
    d = {"p": p, "o": [ok, *wrong]}
    d.update(kw)
    return d

def num(p, *fields, **kw):
    f = []
    for x in fields:
        if isinstance(x, dict):
            f.append(x)
        else:
            l, a, *rest = x
            d = {"l": l, "a": a}
            if rest:
                if rest[0] is not None: d["u"] = rest[0]
                if len(rest) > 1 and rest[1] is not None: d["tol"] = rest[1]
                if len(rest) > 2 and rest[2] is not None: d["e"] = rest[2]
            f.append(d)
    d = {"t": "num", "p": p, "f": f}
    d.update(kw)
    return d

def cls(p, cats, items, **kw):
    it = []
    for x in items:
        d = {"x": x[0], "c": x[1]}
        if len(x) > 2: d["e"] = x[2]
        it.append(d)
    d = {"t": "cls", "p": p, "cats": cats, "items": it}
    d.update(kw)
    return d

def order(p, items, **kw):
    d = {"t": "order", "p": p, "items": items}
    d.update(kw)
    return d

def tap(p, fig, a, multi=False, e=None):
    d = {"t": "tap", "p": p, "fig": fig, "a": a if isinstance(a, list) else [a]}
    if multi: d["multi"] = True
    if e: d["e"] = e
    return d

def lab(p, pac, rows, **kw):
    R = []
    for r in rows:
        n, v, u, ref, a, *e = r
        d = {"n": n, "v": v, "u": u, "r": ref, "a": a}
        if e: d["e"] = e[0]
        R.append(d)
    d = {"t": "lab", "p": p, "pac": pac, "rows": R}
    d.update(kw)
    return d

def tree(p, steps, end, **kw):
    S = []
    for s in steps:
        q, o, *rest = s
        d = {"q": q, "o": o}
        if rest and rest[0]: d["e"] = rest[0]
        if len(rest) > 1 and rest[1]: d["ok"] = rest[1]
        S.append(d)
    d = {"t": "tree", "p": p, "steps": S, "end": end}
    d.update(kw)
    return d

def mkt(p, s, a, e=None):
    d = {"t": "mkt", "p": p, "set": s, "a": a}
    if e: d["e"] = e
    return d

def tira(p, res, ask=None, e=None):
    d = {"t": "tira", "p": p, "res": res}
    if ask: d["ask"] = ask
    if e: d["e"] = e
    return d

def micro(p, items, a, multi=False, obj=40, e=None):
    d = {"t": "micro", "p": p, "items": [dict(k=i[0], x=i[1], y=i[2], r=(i[3] if len(i) > 3 else 0)) for i in items], "a": a, "obj": obj}
    if multi: d["multi"] = True
    if e: d["e"] = e
    return d

def espec(p, s):
    return {"t": "espec", "p": p, "s": s}

class Topic:
    def __init__(self, tid, name, main):
        self.id, self.name, self.main = tid, name, main
        self.ex = []
        self.k = 0

    def add(self, lvl, title, q, checks, steps, ans, hint, tags=None, chain=False):
        self.k += 1
        eid = f"{self.id}e{self.k}"
        if tags is None:
            tags = [[self.main] if isinstance(self.main, str) else self.main for _ in steps]
        d = {"id": eid, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans,
             "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}
        if chain: d["chain"] = True
        self.ex.append(d)
        return eid

# ---------------------- Figuras ----------------------
def svg(w, h, body, label):
    return f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" style="max-width:360px">{body}</svg>'

def fig_espec():
    b = '<line class="gl" x1="40" y1="60" x2="300" y2="60" stroke-dasharray="5 3"/>'
    b += '<circle class="bx" cx="28" cy="60" r="13"/><path class="gl" d="M22 54l12 12M34 54l-12 12"/>'
    b += '<rect class="bx" x="66" y="40" width="6" height="40"/><rect x="66" y="56" width="6" height="8" fill="var(--card)"/>'
    b += '<polygon class="bx" points="98,80 128,80 113,44"/>'
    b += '<rect class="bx" x="146" y="40" width="6" height="40"/><rect x="146" y="56" width="6" height="8" fill="var(--card)"/>'
    b += '<rect class="bx" x="180" y="38" width="26" height="44" rx="2"/><rect x="183" y="56" width="20" height="23" fill="#E8735A" opacity=".55"/>'
    b += '<path class="bx" d="M238 44h14a16 16 0 0 1 0 32h-14z"/>'
    b += '<rect class="bx" x="282" y="42" width="48" height="36" rx="4"/><text class="dl" x="306" y="65" text-anchor="middle">0,52</text>'
    z = [("fuente", 12, 44, 32, 32), ("rend1", 60, 36, 18, 48), ("mono", 92, 40, 42, 44), ("rend2", 140, 36, 18, 48), ("cub", 174, 34, 38, 52), ("det", 232, 38, 40, 44), ("lect", 278, 38, 56, 44)]
    for k, x, y, w, h in z:
        b += f'<rect data-z="{k}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>'
    return svg(340, 110, b, "Esquema de un espectrofotómetro de haz simple")

def fig_turbnef():
    b = '<text class="dm" x="6" y="16">Equipo 1</text><text class="dm" x="6" y="96">Equipo 2</text>'
    # equipo 1: detector en línea
    b += '<circle class="bx" cx="30" cy="45" r="11"/><line class="gl" x1="42" y1="45" x2="246" y2="45" stroke-dasharray="5 3"/>'
    b += '<rect class="bx" x="120" y="28" width="26" height="34"/>' + ''.join(f'<circle cx="{126+i*4}" cy="{36+(i*7)%20}" r="1.6" class="dot"/>' for i in range(5))
    b += '<path class="bx" d="M246 33h12a12 12 0 0 1 0 24h-12z"/>'
    # equipo 2: detector en ángulo
    b += '<circle class="bx" cx="30" cy="130" r="11"/><line class="gl" x1="42" y1="130" x2="200" y2="130" stroke-dasharray="5 3"/>'
    b += '<rect class="bx" x="120" y="113" width="26" height="34"/>' + ''.join(f'<circle cx="{126+i*4}" cy="{121+(i*7)%20}" r="1.6" class="dot"/>' for i in range(5))
    b += '<line class="gl" x1="146" y1="122" x2="214" y2="94" stroke-dasharray="3 3"/><path class="bx" d="M214 80l12 -2l6 22l-12 4z"/>'
    b += '<rect data-z="d1" x="240" y="26" width="34" height="38" rx="4"/><rect data-z="d2" x="206" y="72" width="34" height="38" rx="4"/>'
    return svg(300, 160, b, "Dos equipos de dispersión de la luz")

def fig_ms():
    peaks = [(15, 6), (27, 32), (29, 42), (39, 16), (41, 46), (42, 58), (43, 100), (57, 14), (72, 11)]
    X = lambda m: 34 + (m - 10) * 4.1
    Y = lambda v: 150 - v * 1.25
    b = '<path class="gl" d="M34 20V150H310"/>'
    for v in (0, 50, 100):
        b += f'<text class="dm" x="30" y="{Y(v)+4}" text-anchor="end">{v}</text>'
    b += '<text class="dm" x="38" y="16">Abundancia relativa (%)</text><text class="dm" x="306" y="168" text-anchor="end">m/z</text>'
    for m, v in peaks:
        b += f'<line x1="{X(m)}" y1="150" x2="{X(m)}" y2="{Y(v)}" stroke="var(--curve)" stroke-width="3"/><text class="dm" x="{X(m)}" y="{Y(v)-5}" text-anchor="middle">{m}</text>'
    for m, v in peaks:
        b += f'<circle data-z="m{m}" cx="{X(m)}" cy="{Y(v)}" r="7"/>'
    return svg(320, 176, b, "Espectro de masas")

def fig_cromat():
    def g(t, h, s):
        return [(t + (i - 30) / 30 * 3 * s, h * math.exp(-((i - 30) / 30 * 3) ** 2 / 2)) for i in range(61)]
    X = lambda t: 30 + t * 45
    Y = lambda v: 140 - v
    pts = []
    for i in range(0, 301):
        t = i / 50
        v = 18 * math.exp(-((t - 1.0) / 0.08) ** 2 / 2) + 95 * math.exp(-((t - 3.0) / 0.16) ** 2 / 2) + 70 * math.exp(-((t - 5.0) / 0.22) ** 2 / 2)
        pts.append(f"{X(t):.1f},{Y(v):.1f}")
    b = '<path class="gl" d="M30 20V140H310"/><text class="dm" x="306" y="156" text-anchor="end">tiempo (min)</text><text class="dm" x="34" y="16">Señal del detector</text>'
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--curve)" stroke-width="2"/>'
    b += '<line class="dsh" x1="30" y1="140" x2="30" y2="140"/>'
    for k, t, h in (("p1", 1.0, 18), ("p2", 3.0, 95), ("p3", 5.0, 70)):
        b += f'<circle data-z="{k}" cx="{X(t):.1f}" cy="{Y(h):.1f}" r="8"/>'
    b += '<text class="dm" x="30" y="152" text-anchor="middle">0</text><text class="dm" x="300" y="152" text-anchor="middle">6</text>'
    return svg(320, 160, b, "Cromatograma con tres picos")

def fig_prot(spike=False, low_alb=False):
    X = lambda x: 20 + x
    pk = [(40, 120 if not low_alb else 70, 9), (95, 14, 6), (130, 30, 7), (170, 26, 8), (240, 34, 22)]
    if spike:
        pk[4] = (240, 18, 22)
    pts = []
    for x in range(0, 291):
        v = sum(h * math.exp(-((x - c) / s) ** 2 / 2) for c, h, s in pk)
        if spike: v += 105 * math.exp(-((x - 236) / 3.2) ** 2 / 2)
        pts.append(f"{X(x):.0f},{150 - v:.1f}")
    b = '<path class="gl" d="M20 150H312"/><text class="dm" x="22" y="168">(+) ánodo</text><text class="dm" x="312" y="168" text-anchor="end">cátodo (−)</text>'
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--curve)" stroke-width="2"/>'
    zz = [("alb", 40), ("a1", 95), ("a2", 130), ("b", 170), ("g", 240 if not spike else 236)]
    for k, c in zz:
        v = sum(h * math.exp(-((c - cc) / s) ** 2 / 2) for cc, h, s in pk) + (105 if spike and k == "g" else 0)
        b += f'<circle data-z="{k}" cx="{X(c)}" cy="{150 - v:.1f}" r="8"/>'
    return svg(320, 176, b, "Proteinograma")

def fig_lipid():
    b = '<rect class="bx" x="14" y="40" width="300" height="34" rx="4"/><text class="dm" x="16" y="30">(+) ánodo</text><text class="dm" x="312" y="30" text-anchor="end">cátodo (−)</text>'
    b += '<line class="gl" x1="268" y1="36" x2="268" y2="78"/><text class="dm" x="268" y="92" text-anchor="middle">punto de aplicación</text>'
    for k, x, w in (("hdl", 54, 20), ("vldl", 142, 14), ("ldl", 196, 22), ("qm", 262, 10)):
        b += f'<rect x="{x}" y="44" width="{w}" height="26" rx="3" fill="var(--curve)" opacity=".7"/>'
        b += f'<rect data-z="{k}" x="{x-6}" y="40" width="{w+12}" height="34" rx="4"/>'
    return svg(330, 100, b, "Lipidograma en gel de agarosa")

def fig_hb():
    X = lambda p: 34 + p * 2.6
    Y = lambda s: 140 - s * 1.2
    def curve(p50, col):
        pts = []
        for p in range(0, 101, 2):
            s = 100 * p ** 2.7 / (p ** 2.7 + p50 ** 2.7) if p else 0
            pts.append(f"{X(p):.1f},{Y(s):.1f}")
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.2"/>'
    b = '<path class="gl" d="M34 14V140H300"/><text class="dm" x="38" y="12">Saturación de Hb (%)</text><text class="dm" x="300" y="156" text-anchor="end">pO₂ (mmHg)</text>'
    b += f'<line class="dsh" x1="34" y1="{Y(50)}" x2="300" y2="{Y(50)}"/><text class="dm" x="30" y="{Y(50)+4}" text-anchor="end">50</text>'
    b += curve(17, '#4C78A8') + curve(27, 'var(--muted)') + curve(38, '#E45756')
    for k, p50 in (("izq", 17), ("norm", 27), ("der", 38)):
        b += f'<circle data-z="{k}" cx="{X(p50):.1f}" cy="{Y(50):.1f}" r="8"/>'
    return svg(310, 160, b, "Curvas de disociación de la hemoglobina")

def fig_lb(kind):
    # Lineweaver-Burk: sin inhibidor (gris) y con inhibidor (rojo)
    X = lambda x: 160 + x * 60
    Y = lambda y: 120 - y * 40
    b = '<path class="gl" d="M20 120H310M160 10V140"/><text class="dm" x="306" y="134" text-anchor="end">1/[S]</text><text class="dm" x="164" y="16">1/v</text>'
    def ln(m, q, col):
        x0 = -q / m
        x0 = max(x0, -2.2)
        return f'<line x1="{X(x0):.1f}" y1="{Y(m*x0+q):.1f}" x2="{X(2.3):.1f}" y2="{Y(m*2.3+q):.1f}" stroke="{col}" stroke-width="2.2"/>'
    b += ln(0.5, 0.5, 'var(--muted)')
    if kind == 'comp': b += ln(1.1, 0.5, '#E45756')
    if kind == 'nocomp': b += ln(1.0, 1.0, '#E45756')
    if kind == 'acomp': b += ln(0.5, 1.0, '#E45756')
    b += '<text class="dm" x="300" y="22" text-anchor="end" fill="#E45756" style="fill:#E45756">con inhibidor</text><text class="dm" x="300" y="36" text-anchor="end">sin inhibidor</text>'
    return svg(320, 150, b, "Gráfica de Lineweaver-Burk")
