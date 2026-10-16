#!/usr/bin/env python3
"""Comunicación Integral II · Semana 11 (debate con Toulmin y selección de mociones) → cursos/com2-ef.json.

Uso: python3 tools/com2_s11.py   (desde la raíz del repo; se puede reejecutar: reemplaza los temas s11*)
"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "cursos", "com2-ef.json")
d = json.load(open(F, encoding="utf-8"))


def ex(i, lvl, title, q, o, steps, ans, hint, tags):
    return {"id": i, "lvl": lvl, "title": title, "q": q, "checks": [{"p": "Respuesta", "o": o}],
            "steps": steps, "ans": ans, "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}


def exc(i, lvl, title, q, check, steps, ans, hint, tags):
    return {"id": i, "lvl": lvl, "title": title, "q": q, "checks": [check],
            "steps": steps, "ans": ans, "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}


ELEM = ["Tesis", "Datos", "Garantía", "Respaldo", "Cualificador", "Refutación"]

# ---------------------------------------------------------------- Tema 1
T1 = {
 "id": "s11tou",
 "name": "Sem. 11 · Toulmin en el debate: los seis elementos",
 "teo": (
  "<h4>En una frase</h4><p>En un debate no ganas diciendo que tienes razón: ganas mostrando <strong>por qué tus datos autorizan tu conclusión</strong>, y por qué los del contrario no autorizan la suya.</p>"
  "<h4>Por qué Toulmin y no la lógica formal</h4><div class=\"tbl\"><table><tr><th></th><th>Lógica formal</th><th>Toulmin (1958)</th></tr>"
  "<tr><td>Pregunta</td><td>¿La forma es válida?</td><td>¿Qué autoriza pasar de estos datos a esta conclusión?</td></tr>"
  "<tr><td>Resultado</td><td>Todo o nada</td><td>Admite grados: fuerte, matizado o vulnerable</td></tr></table></div>"
  "<h4>Los seis elementos</h4><div class=\"tbl\"><table><tr><th>Elemento</th><th>Qué es</th><th>Pregunta que responde</th></tr>"
  "<tr><td><b>Tesis</b></td><td>Afirmación discutible que el equipo sostiene</td><td>¿Qué defiendes?</td></tr>"
  "<tr><td><b>Datos</b></td><td>Hechos, cifras, casos o testimonios aceptables de entrada</td><td>¿En qué te basas?</td></tr>"
  "<tr><td><b>Garantía</b></td><td>Regla general (casi siempre implícita) que autoriza el paso dato → tesis</td><td>¿Qué tendría que ser verdad en general para que el dato sostenga la tesis?</td></tr>"
  "<tr><td><b>Respaldo</b></td><td>Lo que sostiene la garantía: teoría, estudios, normas, especialistas</td><td>¿Por qué aceptar esa regla?</td></tr>"
  "<tr><td><b>Cualificador</b></td><td>El grado: «probablemente», «en la mayoría de los casos»</td><td>¿Con cuánta fuerza?</td></tr>"
  "<tr><td><b>Refutación</b></td><td>La condición de excepción: «salvo que…»</td><td>¿Cuándo dejaría de valer?</td></tr></table></div>"
  "<h4>Tesis: tres exigencias de la rúbrica</h4><ul><li><b>Precisión:</b> cada término clave queda definido.</li><li><b>Delimitación:</b> el alcance va <em>dentro</em> del enunciado (ámbito, periodo).</li><li><b>Posición:</b> se nota si defiendes o cuestionas.</li></ul>"
  "<div class=\"err\"><b>Error frecuente:</b> convertir la tesis en un tema («el sesgo en la IA») y perder la posición.</div>"
  "<h4>Datos: tres criterios</h4><ul><li><b>Pertinencia:</b> habla de lo que la tesis afirma, no de un asunto vecino.</li><li><b>Suficiencia:</b> un caso aislado no sostiene una afirmación general.</li><li><b>Confiabilidad:</b> fuente identificable, método conocido, fecha verificable.</li></ul>"
  "<h4>Respaldo: cuatro tipos</h4><p>Teórico, empírico, institucional y de autoridad. Un respaldo no vale por el prestigio del nombre, sino por su <strong>pertinencia</strong> respecto del punto discutido.</p>"
  "<div class=\"ej\"><b>Regla de oro:</b> quien deja su garantía implícita entrega el control del argumento. Enúnciala en voz alta, defiéndela y exige al contrario que explicite la suya. La garantía vale <b>4 puntos</b> en la rúbrica.</div>"
 ),
 "form": [
  "Tesis: afirmación discutible, precisa, delimitada y con posición",
  "Datos: pertinentes, suficientes y confiables (cita autor y obra)",
  "Garantía: regla general que autoriza dato → tesis (4 pts)",
  "Respaldo: sostiene la garantía; vale por pertinencia, no por prestigio",
  "Cualificador: el grado · Refutación: «salvo que…»",
  "Toulmin admite grados; la lógica formal es todo o nada",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>La semana 11 lleva el modelo de Toulmin al <strong>debate</strong>. Ya no basta con reconocer los elementos en un texto: hay que <strong>construir</strong> argumentos completos y exponerlos en voz alta.</p>"
  "<h3>Un argumento con los seis elementos</h3><div class=\"ej\"><p><b>Datos:</b> los sistemas auditados erran sistemáticamente contra un mismo grupo (Buolamwini y Gebru, 2018: hasta 34 % de error con mujeres de piel oscura, menos de 1 % con hombres de piel clara).</p>"
  "<p><b>Garantía:</b> si un sistema reproduce de forma sistemática la desventaja de un grupo, opera con un sesgo, no con un error aleatorio.</p>"
  "<p><b>Respaldo:</b> las auditorías independientes de la última década.</p><p><b>Cualificador:</b> «es altamente probable».</p>"
  "<p><b>Tesis:</b> la IA amplifica el sesgo humano y lo reviste de objetividad.</p>"
  "<p><b>Refutación:</b> salvo que el sistema incorpore auditoría externa y corrección continua de sus datos.</p></div>"
  "<h3>Cómo encontrar la garantía</h3><p>Pregúntate: <em>¿qué tendría que ser verdad en general para que este dato sostenga esta conclusión?</em> La respuesta, escrita como «si…, entonces…», es la garantía.</p>"
  "<h3>Dato vs. respaldo</h3><p>El <b>dato</b> apoya la tesis (habla del caso). El <b>respaldo</b> apoya la garantía (habla de la regla). Si el contrario pregunta «¿y por qué aceptar esa regla?», respondes con el respaldo. En el debate, ese es el trabajo del Reforzador.</p>"
  "<h3>Cualificador y refutación</h3><p>Un cualificador honesto <strong>no debilita</strong>: hace la tesis más difícil de derribar, porque ya reconoce sus límites. Anticipar la refutación («salvo que…») le quita al contrario el efecto sorpresa.</p>"
  "<div class=\"err\"><b>Trampas:</b> tesis convertida en tema o en pregunta; un solo caso como dato de una afirmación general; citar a alguien famoso pero de otro campo como respaldo.</div>"
 ),
 "ex": [
  exc("s11e1", 1, "Desarma el argumento: IA y sesgo",
      "<p>Este argumento completo viene de la clase. Ubica cada parte en su elemento de Toulmin.</p>",
      {"t": "cls", "p": "Toca el elemento de cada frase.", "cats": ELEM, "items": [
        {"x": "«La IA no replica el sesgo humano: lo amplifica y lo reviste de objetividad».", "c": 0},
        {"x": "«Los sistemas de reconocimiento facial evaluados erraban hasta en 34 % con mujeres de piel oscura, frente a menos de 1 % con hombres de piel clara».", "c": 1},
        {"x": "«Si un sistema reproduce de forma sistemática la desventaja de un grupo, opera con un sesgo, no con un error aleatorio».", "c": 2, "e": "Es una regla <b>general</b> que conecta el dato con la tesis: «si…, entonces…»."},
        {"x": "«Así lo muestran las auditorías independientes de sistemas de crédito de la última década».", "c": 3, "e": "No habla del caso concreto: sostiene la <b>regla</b> (la garantía)."},
        {"x": "«Es altamente probable que…».", "c": 4},
        {"x": "«…salvo que el sistema incorpore auditoría externa y corrección continua de sus datos».", "c": 5},
      ]},
      ["La tesis es la conclusión discutible; el dato, la cifra concreta (34 % frente a menos de 1 %).",
       "La garantía es la regla «si un sistema reproduce de forma sistemática la desventaja de un grupo, opera con sesgo»; las auditorías la <strong>respaldan</strong>.",
       "«Altamente probable» mide la fuerza (cualificador) y «salvo que…» marca la excepción (refutación)."],
      "Tesis · dato (34 %) · garantía (si reproduce sistemáticamente…) · respaldo (auditorías) · cualificador · refutación",
      "¿Habla del caso o de la regla?",
      [["tesis", "datos"], ["garantia", "respaldo"], ["cualificador", "refutacion"]]),
  exc("s11e2", 2, "Desarma el argumento: Pinker y la violencia",
      "<p>Tesis asignada en clase (base: Pinker, <em>Los ángeles que llevamos dentro</em>). Ubica cada frase en su elemento.</p>",
      {"t": "cls", "p": "Toca el elemento de cada frase.", "cats": ELEM, "items": [
        {"x": "«La violencia humana no es principalmente consecuencia de nuestra naturaleza biológica, sino del entorno social que permite o limita sus expresiones».", "c": 0},
        {"x": "«Las tasas de homicidio en Europa bajan desde la Edad Media junto con la consolidación del Estado, el comercio y la alfabetización».", "c": 1},
        {"x": "«Si una conducta varía drásticamente mientras la dotación biológica permanece constante, el factor explicativo principal debe buscarse en el entorno».", "c": 2},
        {"x": "«La evolución genética opera en escalas de tiempo muy superiores a las de estos cambios históricos».", "c": 3, "e": "Sostiene la regla: explica <b>por qué</b> la biología no pudo cambiar en esos siglos."},
        {"x": "«En sociedades con instituciones estables y respecto de la violencia interpersonal».", "c": 4, "e": "Limita el <b>alcance</b> y el grado de la afirmación: es el cualificador."},
        {"x": "«Salvo que el entorno se desorganice: en colapsos institucionales la violencia reaparece con rapidez».", "c": 5},
      ]},
      ["El dato es histórico y concreto: caída de homicidios en Europa junto con Estado, comercio y alfabetización.",
       "La garantía generaliza: si la conducta cambia y la biología no, la causa está en el entorno. El respaldo la sostiene con la escala temporal de la evolución.",
       "El cualificador acota (instituciones estables, violencia interpersonal) y la refutación nombra el caso en que falla (colapso institucional)."],
      "Tesis · dato (homicidios) · garantía (si la conducta varía y la biología no…) · respaldo (escala evolutiva) · cualificador · refutación",
      "El cualificador acota; la refutación dice cuándo falla.",
      [["tesis", "datos"], ["garantia", "respaldo"], ["cualificador", "refutacion"]]),
  ex("s11e3", 1, "Tesis, no tema",
     "<p>¿Cuál enunciado cumple las tres exigencias de la rúbrica para una tesis (precisión, delimitación y posición)?</p>",
     ["«En la selección de personal y el crédito automatizados, 2015-2025, la IA amplifica el sesgo humano y lo reviste de objetividad»",
      "«El sesgo en la inteligencia artificial»",
      "«¿Amplifica la inteligencia artificial el sesgo humano?»",
      "«La inteligencia artificial es injusta en todo lo que hace»"],
     ["Una tesis es una <strong>afirmación discutible</strong> con posición. «El sesgo en la IA» es un tema y la versión con signos de interrogación es una pregunta: ninguna toma posición.",
      "«Injusta en todo» toma posición pero no está delimitada. La primera lleva el alcance dentro del enunciado: ámbito (selección de personal y crédito) y periodo (2015-2025)."],
     "La tesis delimitada (ámbito y periodo)", "Tema, pregunta y afirmación sin límites no sirven.",
     [["tesis"], ["tesis"]]),
  ex("s11e4", 1, "¿Qué falla en el dato?",
     "<p class=\"lect\">«La IA discrimina en el crédito: a un amigo mío le negaron un préstamo en una app y él siempre paga a tiempo».</p><p>¿Qué criterio de los datos incumple principalmente?</p>",
     ["Suficiencia: un caso aislado no sostiene una afirmación general",
      "Pertinencia: el dato habla de otro tema",
      "Precisión: la tesis no define «crédito»",
      "Cualificador: falta decir «probablemente»"],
     ["El dato sí trata del crédito (es pertinente), pero es <strong>un solo caso</strong> y además anecdótico.",
      "La tesis es general («la IA discrimina en el crédito»), así que necesita datos variados y suficientes: auditorías, series, varios casos."],
     "Suficiencia", "¿Cuántos casos hay?", [["datos"], ["datos"]]),
  ex("s11e5", 2, "Encuentra la garantía",
     "<p>Dato: en los colegios que restringieron los celulares, los profesores reportaron más participación en clase. Tesis: la universidad debería restringir las pantallas en clase.</p><p>¿Cuál es la garantía que conecta el dato con la tesis?</p>",
     ["Si restringir pantallas mejora la participación en el colegio, también la mejorará en la universidad",
      "Si la universidad restringe las pantallas, los profesores reportarán más participación",
      "Los profesores de colegio reportaron más participación al quitar los celulares",
      "Dehaene identifica la atención como uno de los cuatro pilares del aprendizaje"],
     ["Pregunta clave: ¿qué tiene que ser verdad <em>en general</em> para que el dato del colegio autorice la tesis sobre la universidad? Que lo que funciona en el colegio también funcione en la universidad.",
      "La segunda es una predicción, la tercera repite el dato y la cuarta es un posible <strong>respaldo</strong> (sostendría la regla), no la regla misma.",
      "Al hacerla explícita se ve el punto débil: ¿colegio y universidad son comparables? Por eso la garantía es el centro del debate."],
     "Lo que funciona en el colegio funcionará en la universidad", "Une el tipo de dato con el tipo de tesis.",
     [["garantia"], ["garantia", "respaldo"], ["garantia"]]),
  ex("s11e6", 2, "Respaldo con nombre famoso",
     "<p>Para sostener la garantía «la instrucción explícita enseña más que el descubrimiento», un equipo cita a un premio Nobel de Física que opinó en una entrevista sobre educación. ¿Cómo se evalúa ese respaldo?</p>",
     ["Es débil: un respaldo vale por la pertinencia del nombre respecto del punto, no por su prestigio",
      "Es fuerte: un premio Nobel es la máxima autoridad disponible",
      "Es un dato, no un respaldo, porque es una persona",
      "Es un cualificador, porque matiza la garantía"],
     ["El respaldo de autoridad exige especialistas <strong>cuya competencia sea pertinente</strong> al punto discutido.",
      "Un físico no es especialista en aprendizaje; un estudio empírico o un marco de la neuroeducación (por ejemplo, Dehaene) sería pertinente."],
     "Débil: falta pertinencia", "¿Su campo cubre el punto discutido?", [["respaldo"], ["respaldo"]]),
  ex("s11e7", 1, "Para qué sirve el cualificador",
     "<p>Un equipo cambia «la IA siempre amplifica el sesgo» por «en la mayoría de los sistemas auditados, la IA amplifica el sesgo». ¿Qué logra?</p>",
     ["Hace la tesis más difícil de derribar, porque ya reconoce sus límites",
      "Debilita la tesis y le resta puntos en la rúbrica",
      "Convierte la tesis en un dato",
      "Elimina la necesidad de una garantía"],
     ["El cualificador marca cuánta fuerza reclama la conclusión. Un «siempre» cae con un solo contraejemplo.",
      "Un cualificador honesto no debilita: protege la tesis, porque el contrario ya no puede ganar mostrando una excepción."],
     "La hace más difícil de derribar", "«Siempre» cae con un contraejemplo.", [["cualificador"], ["cualificador", "refutacion"]]),
  ex("s11e8", 1, "Toulmin frente a la lógica formal",
     "<p>Según la clase, ¿en qué se diferencia el modelo de Toulmin de la lógica formal?</p>",
     ["Pregunta qué autoriza a pasar de los datos a la conclusión y admite grados de fuerza",
      "Solo evalúa si la forma del argumento es válida",
      "Evalúa los argumentos como todo o nada",
      "Prescinde de la evidencia y se centra en la retórica"],
     ["La lógica formal evalúa la <strong>validez de la forma</strong>: el argumento vale o no vale.",
      "Toulmin analiza los argumentos como funcionan en la vida real (derecho, ciencia, discusión pública), hace visible el puente implícito y admite grados: fuerte, matizado o vulnerable."],
     "Qué autoriza el paso y admite grados", "¿Todo o nada, o grados?", [["garantia"], ["garantia", "cualificador"]]),
 ],
}

# ---------------------------------------------------------------- Tema 2
T2 = {
 "id": "s11ref",
 "name": "Sem. 11 · Refutar y reconstruir: roles y rúbrica del debate",
 "teo": (
  "<h4>En una frase</h4><p>No se refuta contradiciendo: se refuta señalando <strong>en qué punto del esquema ajeno se rompe la cadena</strong>. Elige la vía y nómbrala.</p>"
  "<h4>Las tres vías de refutación</h4><div class=\"tbl\"><table><tr><th>Vía</th><th>Qué cuestionas</th><th>Ejemplo</th></tr>"
  "<tr><td><b>1. Atacar los datos</b></td><td>La base empírica</td><td>«Esa cifra viene de una muestra no representativa y de otro periodo».</td></tr>"
  "<tr><td><b>2. Desgarantizar</b></td><td>La regla que conecta dato y tesis</td><td>«Aun aceptando sus datos, su garantía supone que correlación implica causa».</td></tr>"
  "<tr><td><b>3. Atacar el respaldo</b></td><td>Lo que sostiene la garantía</td><td>«El autor que invocan trabaja sobre otro objeto».</td></tr></table></div>"
  "<p><b>Reconstrucción:</b> si atacaron tu argumento, el siguiente integrante lo recupera mostrando que el contrario <em>interpretó mal la garantía</em>, no repitiendo el discurso anterior.</p>"
  "<h4>Los cuatro roles (clase de debate)</h4><div class=\"tbl\"><table><tr><th>Rol</th><th>Tarea</th></tr>"
  "<tr><td>1 · Presentador y primer argumento</td><td>Interpreta la tesis y da el primer argumento con datos y garantía</td></tr>"
  "<tr><td>2 · Segundo argumento</td><td>Una razón <b>distinta</b> para la misma tesis, sin repetir la primera</td></tr>"
  "<tr><td>3 · Refutador</td><td>Examina la garantía contraria, identifica el paso débil y explica su efecto</td></tr>"
  "<tr><td>4 · Contraargumentador</td><td>Resume con fidelidad la postura contraria y desarrolla contraargumentos con razones, datos y garantía</td></tr></table></div>"
  "<p class=\"note\">Los tiempos cambian entre las dos presentaciones (3-2-2-3 min con pausa de 2 min en la clase de debate; 3 min por persona y turnos alternados en el laboratorio). Confirma con tu profe el formato del día.</p>"
  "<h4>Rúbrica: 18 grupales + 2 individuales = 20</h4><div class=\"tbl\"><table><tr><th>Criterio</th><th>Pts</th></tr>"
  "<tr><td>Razonamiento y uso de la garantía</td><td>4</td></tr><tr><td>Uso o análisis de datos y respaldos</td><td>4</td></tr>"
  "<tr><td>Organización y articulación de las intervenciones</td><td>3</td></tr><tr><td>Claridad de la comunicación oral</td><td>3</td></tr>"
  "<tr><td>Respeto de turnos y tiempos</td><td>2</td></tr><tr><td>Resumen de postura para el grupo contrario (1 entrega puntual + 1 síntesis fiel)</td><td>2</td></tr>"
  "<tr><td><b>Individual:</b> cumplimiento del rol</td><td>2</td></tr></table></div>"
 ),
 "form": [
  "3 vías: atacar datos · desgarantizar · atacar respaldo",
  "Refutar = señalar dónde se rompe la cadena, no contradecir",
  "Reconstruir: mostrar que el otro leyó mal tu garantía",
  "Roles: 1 tesis + arg. 1 · 2 arg. distinto · 3 refutador · 4 contraargumentador",
  "Rúbrica: garantía 4 · datos/respaldos 4 · organización 3 · claridad 3 · turnos 2 · resumen 2 + rol 2",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Cada argumento de Toulmin tiene eslabones: datos, garantía y respaldo. Refutar es elegir <strong>cuál eslabón</strong> se rompe y decirlo con nombre.</p>"
  "<h3>Cómo elegir la vía</h3><ul><li>¿La objeción discute la cifra, la muestra o la fuente del dato? → <b>atacar los datos</b>.</li>"
  "<li>¿Acepta los datos pero niega que lleven a la tesis (correlación ≠ causa, casos no comparables)? → <b>desgarantizar</b>.</li>"
  "<li>¿Discute al autor, la teoría o la norma que sostiene la regla? → <b>atacar el respaldo</b>.</li></ul>"
  "<div class=\"ej\"><b>Pista:</b> «Aun aceptando sus datos…» casi siempre anuncia una desgarantización.</div>"
  "<h3>El rol del refutador</h3><p>Su blanco principal es la <strong>garantía</strong> del otro grupo: ¿los datos justifican esa conclusión? Puede cuestionar datos o respaldos si es pertinente, pero debe explicar <em>cómo afecta</em> el fallo al argumento.</p>"
  "<h3>El resumen para el contrario</h3><p>Cada grupo entrega un resumen de su propia postura (tesis, argumentos, datos, garantías, respaldos, fuentes y límites). Vale 2 pts: 1 por entregarlo a tiempo con lo pedido y 1 por una síntesis clara y fiel. Ahí no se vuelve a puntuar la solidez de las pruebas.</p>"
  "<div class=\"err\"><b>Errores frecuentes:</b> refutar con «eso es falso» sin nombrar la vía; que el segundo argumento repita el primero; resumir mal al contrario (hombre de paja); pasarse del tiempo.</div>"
 ),
 "ex": [
  ex("s11r1", 1, "Vía de refutación (1)",
     "<p class=\"lect\">«La cifra que citan sale de una encuesta a 40 estudiantes de una sola universidad y de un año en que no existía la IA generativa».</p><p>¿Qué vía de refutación usa?</p>",
     ["Atacar los datos", "Desgarantizar", "Atacar el respaldo", "Reconstrucción"],
     ["Cuestiona la <strong>base empírica</strong>: muestra pequeña y no representativa, y un periodo que no cubre el fenómeno.",
      "No discute la regla que conecta dato y tesis ni al autor que la sostiene."],
     "Atacar los datos", "¿Cuestiona la cifra o la regla?", [["vias", "datos"], ["vias"]]),
  ex("s11r2", 1, "Vía de refutación (2)",
     "<p class=\"lect\">«Aun aceptando que los países con más ajedrez escolar tienen mejores notas en matemáticas, eso no prueba que el ajedrez las cause: también son países con más inversión educativa».</p><p>¿Qué vía de refutación usa?</p>",
     ["Desgarantizar", "Atacar los datos", "Atacar el respaldo", "Cualificar la tesis"],
     ["«Aun aceptando sus datos…» acepta la base y ataca el <strong>puente</strong>: la garantía supone que correlación implica causa.",
      "Desgarantizar es la vía más fuerte cuando los datos son sólidos: muestra que no autorizan la conclusión."],
     "Desgarantizar", "«Aun aceptando sus datos…»", [["vias", "garantia"], ["vias"]]),
  ex("s11r3", 1, "Vía de refutación (3)",
     "<p class=\"lect\">«Citan a De Waal para sostener que los humanos reconocemos emociones universales en el rostro, pero De Waal estudia el consuelo y la equidad en primates, no el reconocimiento facial».</p><p>¿Qué vía de refutación usa?</p>",
     ["Atacar el respaldo", "Atacar los datos", "Desgarantizar", "Hombre de paja"],
     ["Cuestiona lo que <strong>sostiene la garantía</strong>: la autoridad invocada trabaja sobre otro objeto, así que su competencia no cubre el punto.",
      "Es justo el ejemplo de la clase: «el autor que invocan trabaja sobre otro objeto»."],
     "Atacar el respaldo", "¿Discute al autor o la regla?", [["vias", "respaldo"], ["vias"]]),
  ex("s11r4", 2, "Refutar no es contradecir",
     "<p>Ante el primer argumento contrario, un refutador dice: «Eso es falso; nosotros pensamos exactamente lo contrario y lo vamos a demostrar». ¿Por qué es una refutación débil?</p>",
     ["No señala en qué eslabón (datos, garantía o respaldo) se rompe el argumento contrario",
      "Porque el refutador no debe hablar del argumento contrario",
      "Porque solo se puede refutar atacando el respaldo",
      "Porque le faltó el cualificador «probablemente»"],
     ["La clase lo dice así: no se refuta contradiciendo, se refuta señalando en qué punto del esquema ajeno se rompe la cadena.",
      "Además, el rol 3 debe explicar <strong>cómo afecta</strong> ese fallo al argumento; contradecir no explica nada."],
     "No nombra el eslabón que falla", "¿Dónde se rompe la cadena?", [["vias"], ["roles"]]),
  ex("s11r5", 2, "Reconstruir un argumento atacado",
     "<p>El grupo contrario desgarantizó tu primer argumento. ¿Qué debe hacer el siguiente integrante de tu equipo para reconstruirlo?</p>",
     ["Mostrar que el contrario interpretó mal la garantía y volver a enunciarla con precisión",
      "Repetir el primer discurso con más énfasis",
      "Cambiar de tesis para evitar el ataque",
      "Atacar a la persona que hizo la objeción"],
     ["La reconstrucción recupera el argumento mostrando que el ataque se basó en una mala lectura de la garantía, no repitiendo lo mismo.",
      "Cambiar de tesis es abandonar la posición y atacar a la persona es un ad hóminem."],
     "Mostrar la mala lectura de la garantía", "No repetir: precisar.", [["reconst", "garantia"], ["reconst", "adhom"]]),
  exc("s11r6", 1, "Orden del debate",
      "<p>Ordena las intervenciones según la organización de la clase de debate (grupo 1 presenta, grupo 2 refuta).</p>",
      {"t": "order", "p": "Arrastra para ordenar de la primera a la última.", "items": [
        "Rol 1 · Presentador: interpreta la tesis y da el primer argumento",
        "Rol 2 · Segundo argumento, distinto del primero",
        "Pausa de 2 minutos",
        "Rol 3 · Refutador: examina la garantía del grupo 1",
        "Rol 4 · Contraargumentador: resume al grupo 1 y desarrolla contraargumentos"]},
      ["El grupo 1 abre con la tesis y su primer argumento (rol 1) y añade una razón distinta (rol 2).",
       "Tras la pausa, el grupo 2 primero refuta (rol 3) y después resume al grupo 1 y contraargumenta (rol 4)."],
      "Rol 1 → Rol 2 → pausa → Rol 3 → Rol 4", "Primero se presenta, luego se refuta.",
      [["roles"], ["roles"]]),
  ex("s11r7", 1, "Qué hace el refutador",
     "<p>¿Cuál es la tarea principal del rol 3 (refutador)?</p>",
     ["Examinar la garantía del otro grupo, identificar el paso que no se sostiene y explicar cómo afecta al argumento",
      "Presentar un segundo argumento a favor de su propia tesis",
      "Resumir la postura contraria y cerrar con los puntos más sólidos",
      "Controlar los tiempos de todas las intervenciones"],
     ["El refutador se concentra en la <strong>garantía</strong> contraria: ¿los datos justifican esa conclusión? Puede cuestionar datos o respaldos si es pertinente.",
      "Resumir al contrario y desarrollar contraargumentos es el rol 4; el segundo argumento es el rol 2."],
     "Examinar la garantía contraria y explicar el efecto", "Rol 3 → garantía.", [["roles", "garantia"], ["roles"]]),
  ex("s11r8", 1, "La nota individual",
     "<p>En la rúbrica del debate, ¿qué parte de la nota es individual?</p>",
     ["Solo el cumplimiento del rol: hasta 2 puntos; los otros 18 son grupales",
      "La claridad oral: 3 puntos por persona",
      "El razonamiento y la garantía: 4 puntos por persona",
      "Toda la nota es individual"],
     ["La rúbrica tiene 18 puntos grupales (4 + 4 + 3 + 3 + 2 + 2) que reciben todos los integrantes.",
      "El único ítem individual es el <strong>cumplimiento del rol</strong> (2 pts): que cada persona haga la tarea de su turno. La complementariedad entre turnos se califica en organización, no aquí."],
     "Cumplimiento del rol, 2 pts", "18 + 2 = 20", [["rubdeb"], ["rubdeb", "roles"]]),
  ex("s11r9", 2, "El resumen para el grupo contrario",
     "<p>Un grupo entrega a tiempo su resumen de postura, pero omite una de sus dos razones centrales. ¿Cuántos puntos obtiene en ese criterio?</p>",
     ["1 de 2: gana el punto de la entrega puntual, pero pierde el de la síntesis fiel",
      "2 de 2: lo entregó a tiempo",
      "0 de 2: un resumen incompleto no vale nada",
      "Se descuenta en «razonamiento y garantía», no en el resumen"],
     ["El criterio da 1 punto por entregarlo en el momento acordado con lo solicitado y 1 por una síntesis clara y fiel, <strong>sin omitir sus razones centrales</strong>.",
      "Omitir una razón central rompe la fidelidad. La solidez de las pruebas no se vuelve a puntuar aquí."],
     "1 de 2", "Puntual ≠ fiel.", [["rubdeb"], ["rubdeb"]]),
 ],
}

# ---------------------------------------------------------------- Tema 3
T3 = {
 "id": "s11moc",
 "name": "Sem. 11 · Elegir mociones de debate",
 "teo": (
  "<h4>En una frase</h4><p>Una buena moción es una <strong>controversia</strong>: desacuerdo razonable, evidencia pertinente para ambos lados y un alcance que se pueda investigar y defender en el tiempo del debate.</p>"
  "<h4>¿Es controversia?</h4><div class=\"tbl\"><table><tr><th>Sí</th><th>No</th></tr>"
  "<tr><td>Desacuerdo razonable con razones contrastables</td><td>Un dato aislado que una consulta resuelve</td></tr>"
  "<tr><td>Cada postura necesita evidencia pertinente</td><td>Un gusto sin razones discutibles</td></tr>"
  "<tr><td>Puede ser normativa, explicativa o conceptual</td><td>Un falso dilema que excluye alternativas</td></tr>"
  "<tr><td>El alcance permite investigar antes del debate</td><td>Una pregunta demasiado amplia</td></tr>"
  "<tr><td>Importa a la audiencia y respeta a las personas</td><td>Una formulación que cuestiona la dignidad de personas</td></tr></table></div>"
  "<h4>Filtros obligatorios (antes de puntuar)</h4><ol><li>¿Se resuelve con un dato? → es consulta, no debate.</li><li>¿Puedo defender el otro lado? → si no, reformula o descarta.</li><li>¿Cabe en el tiempo del debate? → acota.</li></ol>"
  "<h4>Banderas rojas</h4><ul><li><b>Tema resuelto:</b> no fabriques dos lados frente a hechos establecidos.</li><li><b>Daño identitario:</b> la dignidad es condición de admisión; un puntaje alto no la compensa.</li>"
  "<li><b>Moción tramposa:</b> esconde una premisa no probada («¿Por qué la IA destruye la mente?»).</li><li><b>Tema agotado:</b> necesita pregunta delimitada y evidencia nueva.</li></ul>"
  "<h4>Rúbrica de selección (1 a 5)</h4><div class=\"tbl\"><table><tr><th>Criterio</th><th>Peso</th></tr><tr><td>Disputabilidad</td><td>25 %</td></tr><tr><td>Evidencia disponible</td><td>20 %</td></tr>"
  "<tr><td>Relevancia</td><td>15 %</td></tr><tr><td>Acotamiento</td><td>15 %</td></tr><tr><td>Equilibrio</td><td>15 %</td></tr><tr><td>Respeto</td><td>10 %</td></tr></table></div>"
  "<p>Nota = suma de (puntaje × peso). <b>Mínimo: 3/5.</b> Los filtros van primero.</p>"
  "<h4>Tres tipos de moción</h4><ul><li><b>Normativa:</b> «X debe hacer Y» (la universidad debe prohibir…).</li><li><b>Explicativa:</b> «En [ámbito y periodo], X explica Y mejor que Z».</li><li><b>Conceptual:</b> «En [ámbito], X debe entenderse como Y según [criterio]».</li></ul>"
 ),
 "form": [
  "Controversia: desacuerdo razonable + evidencia para ambos lados + alcance acotado",
  "Filtros: ¿dato? · ¿otro lado defendible? · ¿cabe en el tiempo?",
  "Banderas rojas: resuelto · daño identitario · tramposa · agotado",
  "Rúbrica: disputabilidad 25 · evidencia 20 · relevancia, acotamiento, equilibrio 15 · respeto 10 · mín. 3/5",
  "Mociones: normativa · explicativa · conceptual",
  "Fuente: distingue lo que sostiene de lo que no permite concluir",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Antes de debatir hay que elegir bien el tema. Una pregunta amplia («¿Debe prohibirse la IA en la universidad?») se convierte en moción al <strong>acotarla</strong>: «La universidad debe prohibir la IA generativa en exámenes escritos presenciales individuales».</p>"
  "<h3>Ejemplo guiado de la clase</h3><div class=\"ej\"><p>Puntajes: disputabilidad 4, evidencia 2, relevancia 5, acotamiento 5, equilibrio 4, respeto 5.</p>"
  "<p>Ponderado: 4×0,25 + 2×0,20 + 5×0,15 + 5×0,15 + 4×0,15 + 5×0,10 = <b>4,00</b>. Pasa a investigación, aunque falta verificar fuentes.</p></div>"
  "<div class=\"err\"><b>Ojo:</b> el ponderado no es el promedio simple. Multiplica cada puntaje por su peso.</div>"
  "<h3>Alcance de las fuentes</h3><p>Citar bien es decir lo que la fuente <strong>sostiene</strong> sin estirarla a lo que no permite concluir.</p>"
  "<div class=\"tbl\"><table><tr><th>Fuente</th><th>Sostiene</th><th>No permite concluir</th></tr>"
  "<tr><td>Mollick</td><td>Mantener a una persona en las decisiones finales con IA</td><td>Que quien escribe el prompt es autor de la obra</td></tr>"
  "<tr><td>Feldman Barrett et al. (2019)</td><td>Una misma configuración facial puede expresar distintas emociones; varía según cultura, situación y persona</td><td>Que el rostro no informa nada</td></tr>"
  "<tr><td>Brosnan y de Waal (2003)</td><td>Capuchinos rechazaron participar al ver a otro recibir más por igual esfuerzo</td><td>Que la moral humana depende solo de la biología</td></tr>"
  "<tr><td>Pinker (2011)</td><td>La violencia disminuyó en largos periodos, con retrocesos y sin garantía de continuidad</td><td>Que desapareció o que cada año es más pacífico</td></tr>"
  "<tr><td>Arsuaga et al. (2014)</td><td>Evolución en mosaico en Sima de los Huesos: rasgos a ritmos distintos</td><td>Que toda evolución tiene una dirección o meta</td></tr>"
  "<tr><td>Dehaene</td><td>Cuatro pilares: atención, compromiso activo, retorno de información, consolidación</td><td>Todas las afirmaciones de neuroeducación (p. ej., estilos de aprendizaje)</td></tr>"
  "<tr><td>Mitchell (2021)</td><td>Supuestos erróneos sobre la inteligencia llevan a predicciones demasiado optimistas</td><td>Que una máquina nunca podrá comprender</td></tr>"
  "<tr><td>Messeri y Crockett (2024)</td><td>La IA en investigación puede crear ilusiones de comprensión</td><td>Una regla de autoría o propiedad intelectual</td></tr></table></div>"
  "<p class=\"note\">Si no hallas apoyo pertinente para una afirmación, descártala o reformúlala: «no hay evidencia suficiente» es una respuesta válida.</p>"
 ),
 "ex": [
  ex("s11m1", 1, "¿Cuál es debatible?",
     "<p>¿Cuál de estas propuestas es una controversia adecuada para el debate?</p>",
     ["«La universidad debe prohibir la IA generativa en exámenes escritos presenciales individuales»",
      "«¿Cuál fue el PBI del Perú en 2025?»",
      "«El ceviche es más rico que el lomo saltado»",
      "«¿La IA es buena o mala para la humanidad?»"],
     ["El PBI se resuelve con un dato (consulta, no debate) y el ceviche es un gusto sin razones discutibles.",
      "«¿Buena o mala?» es un falso dilema y demasiado amplio. La primera es normativa, acotada y con razones para ambos lados."],
     "La moción sobre exámenes presenciales", "Aplica los tres filtros.", [["mocion", "filtros"], ["filtros", "fdilema"]]),
  ex("s11m2", 1, "Moción tramposa",
     "<p>¿Por qué «¿Por qué la IA destruye la mente de los estudiantes?» se descarta o reformula?</p>",
     ["Esconde una premisa no probada: da por sentado que la IA destruye la mente",
      "Porque se resuelve con un dato",
      "Porque ataca la dignidad de los estudiantes",
      "Porque es demasiado corta"],
     ["Es una <strong>moción tramposa</strong>: el lado contrario no puede responder, porque la pregunta ya asume el daño.",
      "Una versión admisible sería, por ejemplo, «En la universidad, el uso de IA para redactar ensayos atrofia más destrezas de las que amplifica»."],
     "Premisa no probada", "¿Qué da por sentado?", [["filtros"], ["mocion"]]),
  ex("s11m3", 2, "Calcula el ponderado",
     "<p>Una moción recibe: disputabilidad 3, evidencia 4, relevancia 5, acotamiento 2, equilibrio 4 y respeto 5. Con los pesos de la rúbrica (25, 20, 15, 15, 15 y 10 %), ¿cuál es su nota y qué se decide?</p>",
     ["3,70: pasa el mínimo de 3", "3,83: pasa el mínimo de 3", "3,70: no pasa, porque acotamiento tiene 2", "2,30: no pasa el mínimo"],
     ["3×0,25 + 4×0,20 + 5×0,15 + 2×0,15 + 4×0,15 + 5×0,10 = 0,75 + 0,80 + 0,75 + 0,30 + 0,60 + 0,50 = <b>3,70</b>.",
      "3,83 es el promedio simple (23 ÷ 6), que ignora los pesos. El mínimo se aplica a la nota ponderada; un 2 en un criterio no la descarta, aunque conviene mejorar el acotamiento."],
     "3,70, pasa", "Multiplica por los pesos.", [["rubsel"], ["rubsel"]]),
  ex("s11m4", 2, "Puntaje alto, pero…",
     "<p>Una moción obtiene 4,6 en la rúbrica, pero su formulación cuestiona la dignidad de un grupo de personas. ¿Qué corresponde?</p>",
     ["Descartarla o reformularla: el respeto es condición de admisión y un puntaje alto no lo compensa",
      "Aceptarla, porque supera ampliamente el mínimo de 3",
      "Aceptarla, pero bajando a 1 el criterio de respeto",
      "Debatirla solo si ambos equipos están de acuerdo"],
     ["El <strong>daño identitario</strong> es una bandera roja: la dignidad de las personas es condición de admisión.",
      "Por eso los filtros van antes de puntuar: un puntaje alto no compensa su incumplimiento."],
     "Descartar o reformular", "Filtros antes que puntaje.", [["filtros"], ["filtros", "rubsel"]]),
  ex("s11m5", 2, "Tipo de moción",
     "<p class=\"lect\">«En Europa, desde la Edad Media hasta el siglo XX, la consolidación del Estado explica la caída de los homicidios mejor que cualquier cambio biológico».</p><p>¿Qué tipo de moción es?</p>",
     ["Explicativa", "Normativa", "Conceptual", "No es moción: se resuelve con un dato"],
     ["Sigue la fórmula explicativa: «En [ámbito y periodo], X explica Y mejor que Z».",
      "No dice qué se <em>debe</em> hacer (normativa) ni cómo debe <em>entenderse</em> un concepto (conceptual)."],
     "Explicativa", "¿Debe, explica o se entiende como?", [["mocion"], ["mocion"]]),
  ex("s11m6", 1, "Qué permite afirmar De Waal",
     "<p>¿Qué permite afirmar el experimento de Brosnan y de Waal (2003) con monos capuchinos?</p>",
     ["Que, en esa tarea, los capuchinos rechazaron participar al ver a otro recibir una recompensa mejor por igual esfuerzo",
      "Que la moral humana depende solo de la biología",
      "Que los humanos reconocemos emociones universales en el rostro",
      "Que la cultura no influye en la moral"],
     ["El hallazgo se limita a <strong>esa tarea experimental</strong>.",
      "Usarlo para decir que la moral humana es solo biológica estira la fuente más allá de su alcance; y no trata del reconocimiento facial."],
     "El rechazo en esa tarea", "No estires la fuente.", [["alcance"], ["alcance", "respaldo"]]),
  ex("s11m7", 1, "Qué sostiene Pinker",
     "<p>Según el prefacio de 2011, ¿qué sostiene Pinker sobre la violencia?</p>",
     ["Que disminuyó en largos periodos, con retrocesos y sin garantía de que continúe",
      "Que cada año es más pacífico que el anterior",
      "Que la violencia ya desapareció en las sociedades modernas",
      "Que un caso de violencia antigua refuta la tendencia"],
     ["Pinker defiende una <strong>tendencia de largo plazo</strong>, no uniforme y sin garantía.",
      "Un caso antiguo aislado no refuta por sí solo una tendencia: hay que comparar periodos y medidas equivalentes."],
     "Declive de largo plazo, con retrocesos", "Tendencia ≠ cada año.", [["alcance"], ["alcance", "genap"]]),
  ex("s11m8", 2, "Sin apoyo en la lectura",
     "<p>Un equipo quiere defender «cada persona aprende mejor según su estilo: visual, auditivo o kinestésico». En el pasaje de Dehaene solo encuentran los cuatro pilares del aprendizaje. ¿Qué corresponde?</p>",
     ["Descartar o reformular la afirmación: no hay apoyo pertinente en la lectura",
      "Citar a Dehaene como respaldo de los estilos de aprendizaje",
      "Inventar el lado a favor para que el debate esté equilibrado",
      "Defenderla igual, porque es una creencia muy extendida"],
     ["Los cuatro pilares (atención, compromiso activo, retorno de información, consolidación) no respaldan los estilos de aprendizaje.",
      "La clase lo indica: si no hay apoyo pertinente, se descarta o reformula; registrar que no hay evidencia suficiente es una respuesta válida. Inventar un lado sin sustento rompe el equilibrio real."],
     "Descartar o reformular", "No inventes un lado sin sustento.", [["alcance", "filtros"], ["alcance"]]),
  ex("s11m9", 2, "Acota la pregunta",
     "<p>¿Cuál es la mejor reformulación de «¿Debe usarse la IA en la universidad?» para un debate?</p>",
     ["«En los cursos de redacción de primer año, debe permitirse la IA generativa para revisar borradores, con declaración obligatoria de su uso»",
      "«¿Es la IA el futuro de la educación?»",
      "«La IA es peligrosa»",
      "«¿Por qué la IA arruina la universidad?»"],
     ["La primera precisa ámbito (redacción de primer año), uso (revisar borradores) y condición (declaración obligatoria): se puede investigar y ambos lados tienen razones.",
      "«¿Es el futuro?» sigue siendo demasiado amplia, «La IA es peligrosa» no delimita nada y la última es una moción tramposa."],
     "La versión con ámbito, uso y condición", "Ámbito + uso + condición.", [["mocion", "rubsel"], ["filtros"]]),
 ],
}

NUEVOS = [T1, T2, T3]

CONC = {
 "vias": {"n": "Tres vías de refutación", "f": "Atacar datos · desgarantizar · atacar respaldo", "x": "Refutar es señalar qué eslabón del esquema ajeno se rompe.", "home": "s11ref"},
 "reconst": {"n": "Reconstrucción", "f": "Mostrar que el contrario leyó mal la garantía", "x": "Recuperar un argumento atacado sin repetir el discurso.", "home": "s11ref"},
 "roles": {"n": "Roles del debate", "f": "1 tesis + arg. · 2 arg. distinto · 3 refutador · 4 contraargumentador", "x": "Cada integrante tiene una tarea; cumplirla vale 2 pts individuales.", "home": "s11ref"},
 "rubdeb": {"n": "Rúbrica del debate", "f": "18 grupales (4+4+3+3+2+2) + 2 por rol", "x": "Garantía 4, datos y respaldos 4, organización 3, claridad 3, tiempos 2, resumen 2.", "home": "s11ref"},
 "mocion": {"n": "Moción", "f": "Normativa · explicativa · conceptual", "x": "Afirmación delimitada que admite dos tesis opuestas con evidencia.", "home": "s11moc"},
 "filtros": {"n": "Filtros de selección", "f": "¿Dato? · ¿otro lado? · ¿cabe en el tiempo?", "x": "Van antes de puntuar; banderas rojas: resuelto, daño identitario, tramposa, agotado.", "home": "s11moc"},
 "rubsel": {"n": "Rúbrica de selección", "f": "Σ puntaje × peso (25, 20, 15, 15, 15, 10) ≥ 3", "x": "No es el promedio simple.", "home": "s11moc"},
 "alcance": {"n": "Alcance de la fuente", "f": "Lo que sostiene ≠ lo que no permite concluir", "x": "No estirar una fuente más allá de su objeto y método.", "home": "s11moc"},
}

# ---------------------------------------------------------------- comprobaciones
pesos = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]
assert abs(sum(pesos) - 1) < 1e-9
assert abs(sum(p * w for p, w in zip([4, 2, 5, 5, 4, 5], pesos)) - 4.00) < 1e-9   # ejemplo de la clase
assert abs(sum(p * w for p, w in zip([3, 4, 5, 2, 4, 5], pesos)) - 3.70) < 1e-9   # s11m3
assert round(23 / 6, 2) == 3.83
assert 4 + 4 + 3 + 3 + 2 + 2 == 18

# ---------------------------------------------------------------- ensamblar
d["concepts"].update(CONC)
ids_c = set(d["concepts"])
for t in NUEVOS:
    for e in t["ex"]:
        assert len(e["checks"][0].get("o", ["", "", "", ""])) == 4 or e["checks"][0].get("t"), e["id"]
        for l in e["tags"]:
            for k in l:
                assert k in ids_c, (e["id"], k)

top = [t for t in d["topics"] if not t["id"].startswith("s11")]
pos = next(i for i, t in enumerate(top) if t["id"] == "s9diag") + 1
d["topics"] = top[:pos] + NUEVOS + top[pos:]

d["intro"] = ("Bloque del examen final, organizado por semanas y con más peso en lo último. "
  "<b>Semana 9:</b> calidad de la información y falacias en el argumento científico (inferencias, ciencia, cuatro defectos de información, las cinco falacias de la EC2 y los casos Wakefield, LaCour, Mehra y Pojman). "
  "<b>Semana 11</b> (no hubo semana 10): el modelo de Toulmin aplicado al debate (los seis elementos, las tres vías de refutación, roles y rúbrica) y cómo elegir mociones. "
  "Al final hay un repaso de Toulmin, que sigue siendo la base del análisis. Todos los temas están abiertos y el simulacro (20 preguntas de 4 alternativas) está siempre disponible; se amplía cada semana.")

CARDS = ('<div><b>Toulmin completo (sem. 11)</b><br>Tesis · datos · garantía · respaldo · cualificador · refutación</div>'
  '<div><b>Tesis</b><br>Precisa · delimitada · con posición (no tema ni pregunta)</div>'
  '<div><b>Refutar</b><br>Atacar datos · desgarantizar · atacar respaldo · nómbrala</div>'
  '<div><b>Roles</b><br>1 tesis + arg. · 2 arg. distinto · 3 refutador · 4 contraargumentador</div>'
  '<div><b>Rúbrica del debate</b><br>4 garantía · 4 datos · 3 organización · 3 claridad · 2 tiempos · 2 resumen + 2 rol</div>'
  '<div><b>Mociones</b><br>Filtros: ¿dato? ¿otro lado? ¿cabe? · ponderado ≥ 3 (25/20/15/15/15/10)</div>')
f = d["form"]
if "Toulmin completo (sem. 11)" not in f:
    assert f.endswith("</div></div>")
    d["form"] = f[:-len("</div>")] + CARDS + "</div>"

d["sim"]["slots"] = [
 {"pts": 1, "name": "Repaso Toulmin", "pool": ["t1a", "t1b", "t1c", "t1d", "t1e", "t1f", "t2a", "t2b", "t2c", "t2d", "t2e", "t2f", "t3a", "t3b", "t3c", "t3d", "t3e", "t3f"]},
 {"pts": 1, "name": "Tipos de inferencia", "pool": ["i1", "i2", "i5", "i6"]},
 {"pts": 1, "name": "Tipos de inferencia", "pool": ["i3", "i4", "i7", "i8"]},
 {"pts": 1, "name": "Ciencia e hipótesis", "pool": ["h1", "h4", "h6"]},
 {"pts": 1, "name": "Ciencia e hipótesis", "pool": ["h2", "h3", "h5", "s9s1"]},
 {"pts": 1, "name": "Calidad de la información", "pool": ["q1", "q2", "q3", "q4"]},
 {"pts": 1, "name": "Calidad de la información", "pool": ["q5", "q6", "q7", "s9s3"]},
 {"pts": 1, "name": "Falacias", "pool": ["f1", "f2", "f3", "s9s2"]},
 {"pts": 1, "name": "Falacias", "pool": ["f4", "f5", "f7", "s9s6", "s9s4"]},
 {"pts": 1, "name": "Falacias", "pool": ["f6", "f8", "f9"]},
 {"pts": 1, "name": "Casos de clase", "pool": ["c1", "c3", "c6", "c2"]},
 {"pts": 1, "name": "Casos de clase", "pool": ["c4", "c5", "c7", "c8", "s9s5"]},
 {"pts": 1, "name": "Diagnóstico", "pool": ["d1", "d2", "d3"]},
 {"pts": 1, "name": "Diagnóstico", "pool": ["d4", "d5", "d6"]},
 {"pts": 1, "name": "Sem. 11 · Toulmin en el debate", "pool": ["s11e1", "s11e2"]},
 {"pts": 1, "name": "Sem. 11 · Toulmin en el debate", "pool": ["s11e3", "s11e4", "s11e5", "s11e6", "s11e7"]},
 {"pts": 1, "name": "Sem. 11 · Refutación y roles", "pool": ["s11r1", "s11r2", "s11r3", "s11r4"]},
 {"pts": 1, "name": "Sem. 11 · Refutación y roles", "pool": ["s11r5", "s11r7", "s11r8", "s11r9", "s11r6"]},
 {"pts": 1, "name": "Sem. 11 · Mociones", "pool": ["s11m1", "s11m2", "s11m4", "s11m5", "s11m9"]},
 {"pts": 1, "name": "Sem. 11 · Mociones", "pool": ["s11m3", "s11m6", "s11m7", "s11m8"]},
]
todos = {e["id"] for t in d["topics"] for e in t["ex"]} | {e["id"] for e in d.get("simEx", [])}
for s in d["sim"]["slots"]:
    for i in s["pool"]:
        assert i in todos, i
assert sum(s["pts"] for s in d["sim"]["slots"]) == 20 and len(d["sim"]["slots"]) == d["sim"].get("nq", 20)

with open(F, "w", encoding="utf-8") as o:
    json.dump(d, o, indent=1, ensure_ascii=False)
    o.write("\n")
print("ok:", [t["id"] for t in d["topics"]])
