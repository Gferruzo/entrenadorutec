import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bq_lib import *
from bq_uf1_3 import uf1, uf2, uf3
from bq_uf4_7 import uf4, uf5, uf6, uf7
from bq_uf8_10 import uf8, uf9, uf10

topics = [f() for f in (uf1, uf2, uf3, uf4, uf5, uf6, uf7, uf8, uf9, uf10)]

concepts = {
 "lb": {"n": "Espectrofotometría y Lambert-Beer", "f": "A = ε·c·l · A = 2 − log %T · Cm = Am·Cp/Ap", "x": "La absorbancia es lineal con la concentración dentro del intervalo de linealidad; fuera de él se diluye. Blanco, λ de máxima absorción y lámpara estable.", "home": "u1"},
 "disp": {"n": "Técnicas de separación y dispersión", "f": "Turbidimetría (transmitida) · nefelometría (dispersada) · Rf · m/z", "x": "Elige la técnica según qué se mide; en cromatografía, lo más retenido sale al final; en EM, pico base = el más alto y pico molecular = M.", "home": "u2"},
 "dm": {"n": "Glucosa y diabetes", "f": "Ayunas ≥ 126 · SOG ≥ 200 · HbA1c ≥ 6,5 %", "x": "Plasma en ayunas de 8 h, separar < 30 min o fluoruro. HbA1c (meses), fructosamina (semanas), péptido C (insulina propia).", "home": "u3"},
 "lip": {"n": "Proteínas y lípidos", "f": "LDL = CT − (TG/5 + HDL) si TG < 400", "x": "Proteinograma: Alb > α1 > α2 > β > γ; pico estrecho en γ = monoclonal. Fredrickson según el aspecto del suero.", "home": "u4"},
 "renal": {"n": "Productos finales: función renal y bilirrubina", "f": "Cl = U·V/(P·1440) · urea = BUN × 2,14", "x": "Ictericia indirecta (prehepática/conjugación) vs directa (obstructiva, con coluria). Amonio y lactato: en frío y rápido.", "home": "u5"},
 "enz": {"n": "Enzimas", "f": "Km bajo = más afinidad · 1 U = 16,67 nkat", "x": "Competitiva (Km↑), no competitiva (Vmáx↓), acompetitiva (ambas↓). Patrones hepático, pancreático y del IAM en el tiempo.", "home": "u6"},
 "ab": {"n": "Ácido-base y electrolitos", "f": "pH = 6,1 + log HCO₃⁻/(0,03·pCO₂)", "x": "pH → pCO₂ (respiratoria) → HCO₃⁻ (metabólica) → compensación. Heparina de litio para Na/K; la hemólisis sube el K.", "home": "u7"},
 "ori": {"n": "Análisis de orina", "f": "Tira: cada almohadilla a su tiempo · sedimento 10x/40x", "x": "Cilindros hemáticos = glomerular; leucocitarios = pielonefritis; estruvita = infección ureolítica.", "home": "u8"},
 "liq": {"n": "Heces y líquidos biológicos", "f": "Light: 0,5 · 0,6 · 2/3", "x": "LCR traumático vs hemorragia; meningitis bacteriana: glucosa ↓ y lactato ↑. Sinovial: urato (agujas) vs pirofosfato (romboides).", "home": "u9"},
 "horm": {"n": "Hormonas, marcadores y fármacos", "f": "TSH ↑ T4L ↓ = primario", "x": "Si falla la glándula periférica, la hipofisaria sube. Cribado ≠ confirmación. Rangos de los fármacos con margen estrecho.", "home": "u10"},
}

figs = {"espec1": fig_espec(), "turbnef": fig_turbnef(), "ms": fig_ms(), "cromat": fig_cromat(), "prot": fig_prot(), "protm": fig_prot(spike=True),
        "lipid": fig_lipid(), "hb": fig_hb()}

def ids(t, ks):
    return [f"{t}e{k}" for k in ks]

sim = {"minutes": 90, "slots": [
    {"pts": 2, "name": "UF1 · Cálculo con patrón / Lambert-Beer", "pool": ids("u1", [4, 5, 6, 11])},
    {"pts": 2, "name": "UF1 · Manejo del espectrofotómetro", "pool": ids("u1", [7, 8, 3])},
    {"pts": 1, "name": "UF2 · Técnicas de separación", "pool": ids("u2", [3, 4, 5, 7, 1])},
    {"pts": 2, "name": "UF3 · Diagnóstico de diabetes", "pool": ids("u3", [3, 4, 7, 9])},
    {"pts": 2, "name": "UF4 · Proteinograma y perfil lipídico", "pool": ids("u4", [2, 5, 7, 8])},
    {"pts": 2, "name": "UF5 · Función renal e ictericias", "pool": ids("u5", [1, 4, 5, 7])},
    {"pts": 2, "name": "UF6 · Enzimas y marcadores en el tiempo", "pool": ids("u6", [3, 5, 6, 7, 9])},
    {"pts": 2, "name": "UF7 · Gasometría y electrolitos", "pool": ids("u7", [1, 3, 4, 5, 8])},
    {"pts": 2, "name": "UF8 · Orina: tira y sedimento", "pool": ids("u8", [1, 2, 4, 5, 6])},
    {"pts": 2, "name": "UF9 · Líquidos biológicos y semen", "pool": ids("u9", [1, 2, 3, 4, 5])},
    {"pts": 1, "name": "UF10 · Hormonas, marcadores y fármacos", "pool": ids("u10", [1, 2, 3, 5, 6])}]}

course = {
 "id": "bq-pr", "code": "BQ-XTART", "uni": "XTART", "tapa": {"p": "lunaresp", "c": ["#F2FAF9", "#9ED9D2", "#1F8A84", "#17605C"]},
 "name": "Análisis Bioquímico", "nbname": "Análisis Bioquímico", "exam": "Práctica (UF1 a UF10)", "short": "Práctica", "sub": "UF1 a UF10",
 "guide": True, "free": True,
 "intro": ("Práctica del módulo <b>Análisis Bioquímico</b> (Laboratorio Clínico y Biomédico, XTART FP): las 10 unidades formativas con casos tipo examen. "
           "El enfoque es práctico: <b>decidir qué técnica, muestra o equipo usar</b>, <b>calcular</b> e <b>interpretar analíticas</b>. "
           "Incluye un espectrofotómetro virtual, la lectura de tiras de orina, un microscopio con sedimento y cristales, la curva de marcadores del infarto y de la pancreatitis, y árboles diagnósticos. "
           "Los errores que trae el material están corregidos y marcados con ⚠️ en cada unidad. El simulacro (90 min) mezcla casos de todas las UF."),
 "form": ("<p class=\"note\">Hoja de repaso de Análisis Bioquímico.</p>\n<div class=\"fgrid\">\n"
          "<div><b>Espectrofotometría</b><br>A = ε·c·l · A = 2 − log %T<br>Cm = Am·Cp/Ap · Cm = Cp·ΔAm/ΔAp</div>\n"
          "<div><b>Separación</b><br>Rf = d soluto/d disolvente · t'R = tR − tM<br>Turbidimetría: alta conc. · nefelometría: baja conc.</div>\n"
          "<div><b>Diabetes</b><br>Ayunas ≥ 126 (×2) · SOG 2 h ≥ 200 · HbA1c ≥ 6,5 %<br>Prediabetes: 100–125 · 140–199</div>\n"
          "<div><b>Lípidos</b><br>LDL = CT − (TG/5 + HDL) (TG < 400)<br>CT < 200 · TG < 150</div>\n"
          "<div><b>Renal</b><br>Cl = U·V/(P·1440) · urea = BUN × 2,14<br>ERC: 90 · 60 · 30 · 15</div>\n"
          "<div><b>Enzimas</b><br>Km↓ = afinidad↑ · 1 U = 16,67 nkat<br>ALT/AST > 1 aguda · IAM: CK-MB/Tn → AST → LDH</div>\n"
          "<div><b>Ácido-base</b><br>pH = 6,1 + log HCO₃⁻/(0,03·pCO₂)<br>Osm = 2Na + Glu/18 + Urea/6 · Ca corr = Ca + 0,8(4 − Alb)</div>\n"
          "<div><b>Orina</b><br>Oliguria < 450 · anuria < 200 · poliuria > 2 500<br>Microalbuminuria 30–300 mg/día</div>\n"
          "<div><b>Líquidos</b><br>Light: prot 0,5 · LDH 0,6 · 2/3 LSN<br>Semen ≥ 15 M/mL · ≥ 32 % prog. · ≥ 4 % normales</div>\n"
          "<div><b>Hormonas y fármacos</b><br>TSH ↑ T4L ↓ primario · TSH ↓ T4L ↓ central<br>Litio 0,6–1,5 · digoxina 0,8–2 ng/mL</div>\n</div>"),
 "formSim": False,
 "topics": [], "figs": figs, "concepts": concepts, "simEx": [], "sim": sim}

for t in topics:
    d = {"id": t.id, "name": t.name, "teo": t.teo, "form": t.form, "lesson": t.lesson, "ex": t.ex}
    if getattr(t, "tools", None): d["tools"] = t.tools
    course["topics"].append(d)

# validaciones
allids = {e["id"] for t in course["topics"] for e in t["ex"]}
for s in sim["slots"]:
    for p in s["pool"]:
        assert p in allids, p
for t in course["topics"]:
    for e in t["ex"]:
        for ch in e["checks"]:
            if ch.get("t") == "tap": assert ch["fig"] in figs, ch["fig"]
            if "o" in ch and not ch.get("t"): assert len(ch["o"]) >= 3, e["id"]
        for tg in e["tags"]:
            for k in tg: assert k in concepts
print(len(course["topics"]), "temas,", len(allids), "ejercicios")
out = os.path.join(os.path.dirname(__file__), "..", "cursos", "bq-pr.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(course, f, indent=1, ensure_ascii=False)
    f.write("\n")
