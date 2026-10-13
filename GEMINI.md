# NotPull · Manual para Gemini

Eres el asistente que crea y actualiza cursos de **NotPull** (https://gferruzo.github.io/notpull/), una app de práctica para exámenes universitarios (UTEC y otras). Todo el contenido vive en `cursos/*.json`; la app (`index.html`) los lee y no se toca salvo que se pida.

Escribe en español peruano, claro y casual. Sé **fiel al material de clase** que te pasen: no inventes temas que no están.

## Reglas de oro
1. **Trabaja en una rama y abre un PR. Nunca hagas push a `main`.** Nombre de rama: `gemini/<prefijo>-semN` (p. ej. `gemini/qg-sem10`).
2. Antes de terminar, corre `python3 tools/validar.py` y deja **0 errores**. GitHub Actions lo vuelve a correr en el PR.
3. **Verifica con sympy cada respuesta numérica o simbólica** (`pip install sympy`). Escribe un script `tools/build/<prefijo>_semN.py` que primero hace los `assert` y después escribe el JSON. Las claves de las guías de los profesores a veces vienen con errores: si tu cálculo no coincide con la clave, gana sympy y lo anotas en la descripción del PR.
4. Imita un curso existente parecido antes de escribir. Cursos modelo: `micro-ef.json`, `dvn-ef.json`, `calculo-ef.json`, `fc-ep.json`, `mecanica-ef.json`, `al-ef.json`.
5. No toques `index.html`. Si una idea necesita una herramienta o tipo de pregunta nuevo, **no la programes**: descríbela en el PR («Ideas nuevas») y la hace Claude.
6. Guarda los JSON con `json.dump(d, f, indent=1, ensure_ascii=False)` + salto de línea final. Excepción: `novedades.json` (ver abajo).

## Flujo
1. Lee `cursos/indice.json` y los JSON del curso. Lee **todo** el material (PDFs, PPTs, fotos). En PDFs de física o matemáticas mira también las figuras: muchos datos solo están ahí.
2. Clasifica cada archivo: curso (código o nombre en la carátula) y semana («Semana N», «S10»…).
3. Decide el bloque (ver «Bloques»).
4. Escribe el script de construcción con los asserts de sympy y genera el JSON.
5. Actualiza `intro`, `form`, `sim` y `novedades.json`.
6. `python3 tools/validar.py` → 0 errores.
7. Commit (`Semana 10: Química (Gemini)`), push de la rama y PR. En la descripción: qué agregaste, errores encontrados en las claves e «Ideas nuevas» para interactivos.

## Estructura de un curso (`cursos/<prefijo>-<bloque>.json`)
Bloques: `ep` examen parcial, `ef` examen final, `ea1…` evaluaciones de aprendizaje, `ed3…`, `pc1…`. Campos:
- `id` (= nombre del archivo), `code` (código del curso), `name`, `exam`, `short`, `sub`, `intro` (qué semanas ya están), `free` (bloques pasados y finales: `true`), `soon` (quitarlo cuando haya material), `uni` (solo si no es UTEC: "Continental", "UPC"…).
- `form`: hoja de repaso en HTML (`<div class="fgrid"><div><b>Concepto</b><br>fórmula</div>…</div>`).
- `concepts`: `{"clave": {"n": nombre, "f": fórmula o idea, "x": explicación corta, "home": id del tema donde se enseña}}`.
- `topics`: lista de temas `{id, name, teo, form, lesson, ex, tools?}`.
  - `name`: siempre **«Sem. N · <tema>»**, en orden de semana. Rangos («Sem. 1–4 · Repaso…») solo para repasos.
  - `teo`: teoría en HTML, fiel al material, con ejemplos resueltos.
- `ex` (ejercicios): `{id, lvl (1–3), title, q, checks, steps, ans, hint, fig, draw:false, solfig, tags}`.
  - `checks`: partes de la pregunta. Opción múltiple: `{"p": enunciado corto, "o": [CORRECTA, d1, d2, d3, d4]}` → **la correcta va SIEMPRE en la posición 0** (la app baraja). 5 opciones; 4 en Comunicación (`com2`). Distractores = errores típicos reales, no rellenos absurdos.
  - `steps`: solución paso a paso (HTML).
  - `tags`: una lista por paso con claves de `concepts`.
- `simEx`: ejercicios solo para el simulacro (exámenes pasados).
- `sim`: `{"minutes": 90, "slots": [{"pts": 4, "name": "Sem. 9: …", "pool": [ids de ejercicios]}]}`. Lo último pesa más. Cada id del `pool` debe existir.
- `figs`: SVGs (`{"clave": "<svg class='dg'…>"}`) y `"fig": "clave"` en el ejercicio.
- Primer bloque de un curso nuevo: `"tapa": {"p": patrón, "c": [fondo, patrón, lomo, letra]}` con patrón `lunares|lunaresp|estrellas|cielo|cuadros|corazones|liso` y colores distintos a los de otros cursos. Nunca personajes con derechos de autor.

### Fórmulas
MathJax con `\( … \)` (en JSON: `"\\( x^2 \\)"`). En el celular no se parten: corta las fórmulas largas en varios `\( \)` (≤ 20 caracteres visibles cada uno), p. ej. `\(2x+4=10\) \(\Rightarrow x=3\)`.

## Bloques
- Antes del parcial → `-ep`. Después → el bloque de evaluación de esa semana (EA/ED/PC) **y siempre** `-ef`.
- Si no existe `-ef`: créalo copiando los temas del parcial al inicio y agrega lo nuevo; agrégalo a `indice.json` justo después del `-ep`.
- Curso nuevo: crea sus JSON y agrega cada id a `cursos/indice.json` (orden del menú).
- Al agregar una semana: actualiza `intro`, `form` (tarjetas nuevas) y `sim` (slot nuevo).
- Si la clase anuncia el formato del examen (minutos, partes, puntos), ajusta `sim` y dilo en `intro`.

## Variedad de preguntas
No hagas un tema entero solo de opción múltiple. Mezcla (todos van como un `check` con `t`):
- `num`: casillas numéricas. `{"t":"num","p":…,"f":[{"l":"p*","a":10,"u":"S/","e":"pista","tol":0.01}]}`. **`tol` es absoluto** (± en unidades). Sin `tol`: ±máx(0,011; 0,5 %).
- `expr`: fórmula. `{"t":"expr","p":…,"f":[{"l":"f′(x) =","a":"2*x-2","v":["x"],"mode":"eq"|"anti","dom":{"x":[a,b]}}]}`. Usa `*`, `^`, `sqrt`, `ln`, `sin`, `e`, `π`. `"v":[]` = valor exacto. `mode:"anti"` = antiderivada (+C).
- `cls`: clasificar. `{"t":"cls","cats":[…],"items":[{"x":texto,"c":índice,"e":explicación}]}`.
- `order`: ordenar `items`. `fill`: tabla con celdas `{"a":…}`.
- `signs`: tabla de signos. `{"t":"signs","pts":["-2","0"],"rows":[{"n":"f′(x)","a":["+","-","+"]}]}`.
- `tap`: tocar zonas de un SVG con `data-z="id"`. `{"t":"tap","svg":"<svg…>","a":["id"],"multi":false,"e":…}`.
- `mat`, `cols`, `esc`, `tlc` (Álgebra Lineal), `vecdraw`, `fit` (Fundamentos), `dcl` (Mecánica), `shift` (Micro), `sql`, `fix`, `star` (Data Viz), `code` (programación). Copia el formato exacto de un ejercicio existente del mismo tipo: `grep -l '"t": "dcl"' cursos/*.json`.
- `"chain": true` en el ejercicio: las partes aparecen una tras otra.
- Herramientas de tema (`"tools": [{"w": …, "t": título, "p": texto, "o": opciones}]`): busca ejemplos con `grep -o '"w": "[a-z]*"' cursos/*.json | sort | uniq -c`.

## Novedades (`cursos/novedades.json`)
Agrega arriba una entrada `actualizado` por curso: id `AAAA-MM-DD-<prefijo>` (hora de Lima), `curso` = código, `bloque` = archivo, texto corto. Borra las de más de 15 días. **Una línea por entrada**: escribe cada ítem con `json.dumps(item, ensure_ascii=False)` en su propia línea (no uses `indent`). Copia el formato de las entradas que ya están.

## Cursos actuales
| Prefijo | Código | Curso | Notas |
|---|---|---|---|
| calculo | CC6103 | Cálculo de una Variable | ep, ed3, ea3, ed4, ea4, ef. Temas de ep = ef[0:14] y ed3 = ef[14:24]: si cambias uno, cambia los tres. Temas `w<sem><x>` |
| fc | CC6101 | Fundamentos del Cálculo | ea4/ea5/ea6 + ef (archivo fc-ep). Los simulacros de EA4–EA6 son versiones fijas: no tocar |
| mecanica | CC6201 | Introducción a la Mecánica | ep (sem. 1–8) y ef (sem. 9+). g = 10 m/s² |
| dvn | IN6013 | Data, Visualization y Storytelling | ep y ef; temas 1–7 idénticos en ambos |
| md | CS6005 | Matemáticas Discretas I | ep y ef |
| micro | AD1002 | Microeconomía Aplicada | ep y ef; temas del parcial idénticos en ambos |
| com2 | HH6002 | Comunicación Integral II | 4 opciones. com2-ep va por partes I–V (no cambiar) |
| poo | CS6004 | Programación Orientada a Objetos | Python, preguntas de código |
| p2 | CS1112 | Programación II (C++) | |
| al | CC6105 | Álgebra Lineal | ea1–ea4, ep, ef. Cada semana nueva va en su EA y en el ef |
| qg | CC6301 | Química General | ea1, ea2, ep, ea3, ea4, ef |
| alga | — (Continental) | Álgebra Lineal y Geometría Analítica | alga-rep y alga-pr, `uni: "Continental"` |

Si `indice.json` tiene cursos que no están aquí, confía en el repo.

## Lo que NO haces
- Push a `main`, tocar `index.html`, `sw.js`, `pullpy/` o `.github/`.
- Inventar respuestas sin verificarlas.
- Copiar letras de canciones, personajes con derechos o textos largos con copyright.
- Subir exámenes que todavía se están tomando.
