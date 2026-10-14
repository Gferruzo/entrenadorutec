from bq_lib import *

def uf1():
    T = Topic("u1", "UF1 · Técnicas de bioquímica (I): luz y espectrofotometría", "lb")
    T.teo = ("<p>La <strong>luz</strong> es una onda electromagnética y a la vez un chorro de fotones. "
             "Su energía es <b>E = h·ν = h·c/λ</b>: a <b>menor λ, mayor frecuencia y mayor energía</b> (de los rayos gamma a las ondas de radio, la energía baja). "
             "El visible va de ~400 a 700 nm. Una disolución tiene el <b>color complementario</b> del que absorbe: si se ve roja, absorbe verde-azul (≈ 500 nm), así que se mide a esa λ.</p>"
             "<p><strong>Espectrofotómetro de haz simple</strong>: fuente (tungsteno: visible; deuterio/hidrógeno: UV) → rendija de entrada → <b>monocromador</b> (prisma o red de difracción) → rendija de salida → <b>cubeta</b> (1 cm; cuarzo para UV, vidrio o plástico para visible) → <b>detector</b> (fotomultiplicador, fotodiodo) → lector. "
             "El de <b>doble haz</b> mide blanco y muestra a la vez (en el espacio, con <i>beamsplitter</i>) o alternando (en el tiempo, con <i>chopper</i>): compensa las variaciones de la lámpara. "
             "El <b>fotocolorímetro</b> usa <b>filtros</b> en vez de monocromador: más simple y menos preciso, solo visible.</p>"
             "<p><strong>Ley de Lambert-Beer</strong>: <b>A = ε·c·l</b>. La absorbancia es lineal con la concentración; la transmitancia no (es exponencial). "
             "<b>T = I/I₀</b>, <b>A = −log T = 2 − log %T</b>. Solo se cumple con luz monocromática, sin interferentes ni fluorescencia, con cubeta limpia y dentro del <b>intervalo de linealidad</b>: si la concentración es muy alta, <b>se diluye</b> y se multiplica por el factor de dilución.</p>"
             "<p><strong>Espectroscopia atómica</strong>: la muestra se atomiza (desolvación → vaporización → atomización). En <b>absorción atómica</b> la lámpara de <b>cátodo hueco</b> es del mismo metal que se busca (llama: ppm; horno de grafito: ppb; metales como Cu, Fe, Pb, Li). En <b>emisión (fotometría de llama)</b> no hay lámpara: la llama excita los átomos y se mide la luz que emiten (hoy reemplazada por el electrodo selectivo).</p>"
             "<p><strong>Luminiscencia</strong>: en la <b>fluorimetría</b> la luz emitida tiene <b>mayor λ</b> (menos energía) que la de excitación, hay dos monocromadores y el detector está a <b>90°</b>; cubetas de cuarzo. En la <b>quimioluminiscencia</b> la luz sale de una reacción química (luminol): <b>no hace falta seleccionar λ</b>.</p>"
             "<p><strong>Curva de calibrado</strong>: blanco + 4 a 6 patrones de concentración conocida → recta A = m·C + b → se <b>interpola</b> la muestra. "
             "<strong>Técnicas</strong>: colorimétricas (cromógenos) o enzimáticas; <b>a punto final</b> (la reacción termina; C = A<sub>m</sub>·C<sub>p</sub>/A<sub>p</sub>) o <b>cinéticas</b> (se mide ΔA/min; C = C<sub>p</sub>·ΔA<sub>m</sub>/ΔA<sub>p</sub>).</p>")
    T.form = ["E = h·ν = h·c/λ", "A = ε·c·l (l = 1 cm)", "T = I/I₀ · A = −log T = 2 − log %T",
              "Punto final: Cm = Am · Cp / Ap", "Cinética: Cm = Cp · ΔAm / ΔAp", "Fuera de linealidad → diluir × factor"]
    T.lesson = ("<h3>Idea central</h3><p>Casi todo el laboratorio de bioquímica mide <b>cuánta luz absorbe</b> una muestra coloreada. En la práctica te van a pedir manejar el espectrofotómetro y calcular una concentración con un patrón.</p>"
                "<h3>Procedimiento en el equipo (haz simple)</h3><ul><li><b>1.</b> Enchufar y encender; <b>esperar ~20 min</b> a que la lámpara se estabilice.</li><li><b>2.</b> Elegir la <b>λ</b> del analito (máxima absorción) y la magnitud (normalmente absorbancia).</li><li><b>3.</b> Poner el <b>blanco</b> (agua destilada o reactivo) y ajustar a cero.</li><li><b>4.</b> Leer patrón y muestra.</li><li><b>5.</b> Apagar y desenchufar.</li></ul>"
                "<div class=\"ej\"><b>Ejemplo (caso de Irene):</b> patrón de glucosa 100 mg/dL con A = 0,47; muestra A = 0,52 → C = 0,52 × 100 / 0,47 = <b>110,6 mg/dL</b>.</div>"
                "<div class=\"err\"><b>Error común:</b> calcular con la transmitancia como si fuera lineal. Primero pasa %T a absorbancia (A = 2 − log %T).</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> la constante de Planck es 6,626·10<sup>−34</sup> J·s y c = 3·10<sup>8</sup> m/s (el PDF pierde los signos de los exponentes).</div>")
    T.tools = [{"w": "espec", "t": "Espectrofotómetro virtual", "p": "Practica el procedimiento completo antes de la práctica real.", "o": {}},
               {"w": "calib", "t": "Curva de calibrado", "o": {}}]
    T.add(1, "Energía y longitud de onda", "<p>Compara una radiación UV (250 nm) con una roja (650 nm).</p>",
          [cls("¿Qué pasa al <b>aumentar</b> la longitud de onda?", ["Aumenta", "Disminuye"],
               [("La frecuencia", 1), ("La energía del fotón", 1, "E = h·c/λ: λ está en el denominador."), ("El periodo de la onda", 0, "El periodo es 1/f: si f baja, el periodo sube.")]),
           opt("¿Cuál tiene más energía?", "La UV (250 nm)", "La roja (650 nm)", "Tienen la misma energía", "Depende de la amplitud", "Depende de la concentración")],
          ["E = h·c/λ: energía y λ son inversamente proporcionales; la frecuencia también baja al subir λ (ν = c/λ).", "El periodo es el inverso de la frecuencia, así que aumenta.", "250 nm < 650 nm → la UV tiene más energía."],
          "Frecuencia y energía bajan; el periodo sube. Más energía: UV.", "Mira dónde está λ en E = h·c/λ.")
    T.add(1, "Color y λ de medida", "<p>Un reactivo produce una disolución de color <b>anaranjado</b>. Según la tabla de colores complementarios, ¿a qué λ conviene medirla?</p>",
          [opt("Rango de λ a seleccionar", "440–470 nm (absorbe azul)", "580–620 nm (absorbe naranja)", "620–680 nm (absorbe rojo)", "380–420 nm (absorbe violeta)", "No importa la λ: la ley se cumple a cualquiera")],
          ["Vemos el color complementario del absorbido: anaranjado (580–620 nm) ↔ se absorbe azul (440–470 nm).", "Se mide donde la absorción es máxima: ahí la sensibilidad es mayor."],
          "440–470 nm", "Vemos lo que NO se absorbe.")
    T.add(1, "Partes del espectrofotómetro", "<p>Esquema de un espectrofotómetro de haz simple (sin rótulos).</p>",
          [tap("Toca el <b>monocromador</b> (selector de λ).", "espec1", "mono", e="Es el prisma o la red de difracción, entre las dos rendijas."),
           tap("Toca la <b>cubeta</b>.", "espec1", "cub"),
           tap("Toca el componente que convierte la luz en señal eléctrica.", "espec1", "det", e="El detector funciona por efecto fotoeléctrico.")],
          ["Orden: fuente → rendija de entrada → monocromador → rendija de salida → cubeta → detector → lector.", "La cubeta contiene la muestra (en la figura, con líquido).", "El detector (fotomultiplicador, fotodiodo) transforma la energía luminosa en corriente eléctrica."],
          "Monocromador, cubeta y detector", "La luz atraviesa los componentes de izquierda a derecha.", chain=True)
    T.add(1, "Transmitancia ↔ absorbancia", "<p>Usa A = 2 − log(%T).</p>",
          [num("Conversiones", ("%T si A = 0,184", 65.5, "%", 0.3), ("A si %T = 25 %", 0.602, None, 0.005), ("A si T = 1 (100 %)", 0, None, 0.001))],
          ["log %T = 2 − 0,184 = 1,816 → %T = 10^1,816 = 65,5 %.", "A = 2 − log 25 = 2 − 1,398 = 0,602.", "Si toda la luz pasa, no hay absorción: A = 0."],
          "65,5 %; 0,602; 0", "A = 2 − log %T")
    T.add(2, "Lambert-Beer con ε", "<p>El NADH absorbe a 340 nm con ε = 6 220 L·mol⁻¹·cm⁻¹. Una muestra en cubeta de 1 cm da A = 0,311.</p>",
          [num("Concentración de NADH", ("c", 50, "µmol/L", 0.5))],
          ["c = A/(ε·l) = 0,311 / (6 220 × 1) = 5,0·10⁻⁵ mol/L.", "En µmol/L: 5,0·10⁻⁵ × 10⁶ = 50 µmol/L."],
          "50 µmol/L", "Despeja c = A/(ε·l) y pasa a µmol/L.")
    T.add(1, "Glucosa con patrón (caso Irene)", "<p>Kit de glucosa a punto final: patrón 100 mg/dL con A = 0,47. La muestra de suero da A = 0,52.</p>",
          [num("Glucosa de la muestra", ("C", 110.6, "mg/dL", 0.3))],
          ["Punto final: C<sub>m</sub> = A<sub>m</sub> × C<sub>p</sub> / A<sub>p</sub>.", "C = 0,52 × 100 / 0,47 = 110,6 mg/dL."],
          "110,6 mg/dL", "Regla de tres con el patrón.")
    T.add(2, "Práctica: glucosa en el espectrofotómetro", "<p>Haz tú la medida. Reactivo GOD-POD (cromógeno rojo, λ máx ≈ 505 nm). Patrón: 100 mg/dL. Recuerda: encender, esperar, λ, blanco, patrón y muestra.</p>",
          [espec("Opera el equipo y escribe la glucosa de la muestra.", {"n": "Glucosa · GOD-POD (rojo)", "lmax": 505, "Cp": 100, "Ap": 0.47, "As": 0.52, "reag": 0.1, "u": "mg/dL"})],
          ["Encender y esperar los 20 min de calentamiento.", "λ ≈ 505 nm (el color rojo absorbe verde-azul).", "Blanco de reactivo → ajustar a cero (descuenta el color del reactivo).", "Leer patrón (0,470) y muestra (0,520): C = 0,520 × 100 / 0,470 = 110,6 mg/dL."],
          "110,6 mg/dL", "Sin blanco, la lectura incluye el color del reactivo.")
    T.add(1, "Pasos del espectrofotómetro (caso Daniel)", "<p>Primer día de Daniel en el laboratorio. Ordena los pasos.</p>",
          [order("Orden correcto", ["Enchufar y encender el equipo", "Esperar ~20 min a que la lámpara se caliente", "Seleccionar la λ del analito", "Seleccionar la magnitud (absorbancia)", "Hacer el blanco con agua destilada o el reactivo", "Medir la muestra problema", "Apagar y desenchufar"])],
          ["Sin calentar, la lámpara fluctúa y las lecturas no son estables.", "Primero λ y magnitud; luego el blanco a esa λ; después la muestra."],
          "Encender → esperar → λ → magnitud → blanco → muestra → apagar", "El blanco se hace a la λ que vas a usar.")
    T.add(2, "Dos glucosas con la misma absorbancia (caso Jimena)", "<p>Dos disoluciones de glucosa de distinta concentración dan absorbancias casi iguales.</p>",
          [opt("¿Qué ocurre y qué hace Jimena?", "Están fuera del intervalo de linealidad: diluir y multiplicar por el factor", "La lámpara está fría: esperar y repetir sin cambios", "Hay fluorescencia: cambiar a cubeta de plástico", "Es normal: la absorbancia nunca depende de la concentración", "Debe pasar a transmitancia, que sí es lineal")],
          ["Con concentraciones muy altas la recta se curva (desviación de Lambert-Beer).", "Se diluye la muestra hasta entrar en el tramo lineal y el resultado se multiplica por el factor de dilución."],
          "Fuera de linealidad → diluir", "Mira la figura de desviaciones positiva y negativa.")
    T.add(1, "Punto final o cinética", "<p>Clasifica cada afirmación.</p>",
          [cls("¿A qué técnica corresponde?", ["Punto final", "Cinética"],
               [("La reacción se deja terminar y se lee una vez", 0), ("Se mide la variación de absorbancia por minuto (ΔA/min)", 1), ("Se usa para medir actividades enzimáticas (ALT, AST)", 1),
                ("C = A<sub>m</sub> × C<sub>p</sub> / A<sub>p</sub>", 0), ("Es crítico controlar temperatura y tiempos de lectura", 1, "En la cinética la velocidad depende de la T: un grado cambia el resultado."), ("Glucosa por GOD-POD tras 10 min de incubación", 0)])],
          ["Punto final: se agota el analito y se lee el color formado.", "Cinética: se mide la velocidad (ΔA/min) antes de que termine la reacción."],
          "PF · C · C · PF · C · PF", "¿Esperas a que termine la reacción?")
    T.add(2, "Cálculo cinético", "<p>Método cinético con patrón de 200 mg/dL: ΔA/min del patrón = 0,060; ΔA/min de la muestra = 0,045.</p>",
          [num("Concentración", ("C", 150, "mg/dL", 0.5))],
          ["C<sub>m</sub> = C<sub>p</sub> × ΔA<sub>m</sub> / ΔA<sub>p</sub>.", "C = 200 × 0,045 / 0,060 = 150 mg/dL."],
          "150 mg/dL", "Es la misma regla de tres, pero con ΔA/min.")
    T.add(2, "¿Qué técnica es?", "<p>Clasifica cada característica.</p>",
          [cls("Técnica", ["Absorción atómica", "Fotometría de llama", "Fluorimetría", "Quimioluminiscencia"],
               [("Lámpara de cátodo hueco del mismo metal que se busca", 0), ("No tiene fuente de luz: la llama excita los átomos", 1), ("Detector a 90° de la luz de excitación", 2),
                ("La luz sale de una reacción química (luminol)", 3), ("No necesita seleccionar λ", 3), ("La luz emitida tiene mayor λ que la absorbida", 2), ("Horno de grafito para detectar ppb de plomo", 0)])],
          ["Absorción atómica: lámpara de cátodo hueco + atomización (llama: ppm; horno de grafito: ppb).", "Emisión/fotometría de llama: la llama es la fuente de energía; se mide la luz emitida.", "Fluorescencia: dos monocromadores, detector a 90°, emisión de menor energía (mayor λ).", "Quimioluminiscencia: la reacción genera la luz; no hace falta monocromador."],
          "AA · llama · fluor · quimio · quimio · fluor · AA", "¿De dónde sale la luz que se mide?")
    T.add(1, "Doble haz y fotocolorímetro (caso Germán)", "<p>Germán quiere saber las ventajas de los equipos.</p>",
          [opt("Ventaja del doble haz frente al haz simple", "Las variaciones de la fuente y del detector afectan por igual a blanco y muestra, y se compensan", "No necesita blanco", "Usa filtros en lugar de monocromador", "Permite medir sin cubeta", "Solo funciona en el infrarrojo"),
           opt("Diferencia del fotocolorímetro", "Usa filtros (no monocromador): más simple, solo visible y menos preciso", "Usa dos monocromadores y detector a 90°", "Mide la luz dispersada", "No usa cubeta", "Tiene lámpara de cátodo hueco")],
          ["El doble haz divide la luz: un haz por la muestra y otro por el blanco; la relación entre ambos no cambia si la lámpara fluctúa.", "El fotocolorímetro cambia el monocromador por filtros (vidrio o interferencia)."],
          "Compensa fluctuaciones; el fotocolorímetro usa filtros.", "¿Qué pasa si la lámpara pierde intensidad?")
    return T

def uf2():
    T = Topic("u2", "UF2 · Técnicas de bioquímica (II): dispersión, masas, cromatografía y automatización", "disp")
    T.teo = ("<p><strong>Dispersión</strong>: con partículas en suspensión, parte de la luz se desvía. "
             "<b>Turbidimetría</b>: mide la luz <b>transmitida</b> (detector en línea con la fuente; A = k·c·l); sirve para concentraciones <b>altas</b> y es poco sensible. "
             "<b>Nefelometría</b>: mide la luz <b>dispersada</b> en un ángulo (detector a 15–90°; láser); más sensible, para concentraciones <b>bajas</b>. Se usan para proteínas específicas con antígeno-anticuerpo.</p>"
             "<p><strong>Refractometría</strong>: η = c/v; el índice de refracción sube con los solutos (en suero, sobre todo la albúmina). "
             "<strong>Reflectancia y química seca</strong>: tiras reactivas y películas multicapa (capa difusora → reactiva → indicadora → soporte); se guardan <b>protegidas de la humedad</b>.</p>"
             "<p><strong>Espectrometría de masas</strong>: volatilizar → ionizar (ESI, MALDI) → acelerar → separar por <b>m/z</b> (TOF, cuadrupolo, sector magnético, trampa de iones) → detectar. Es destructiva y muy sensible. "
             "En el espectro: <b>pico molecular</b> (la molécula entera, da la masa) y <b>pico base</b> (el más alto, 100 %). Usos: cribado neonatal (tándem), toxicología, monitorización de fármacos.</p>"
             "<p><strong>Cromatografía</strong>: fase móvil (eluyente) + fase estacionaria. Lo que más interactúa con la estacionaria sale <b>más tarde</b>. Tipos: adsorción, <b>intercambio iónico</b> (carga), <b>exclusión molecular</b> (tamaño: las grandes salen primero), <b>afinidad</b> (Ag-Ac, test de embarazo), partición, gases (GLC). "
             "Cromatograma: tiempo muerto t<sub>M</sub>, tiempo de retención t<sub>R</sub>, t'<sub>R</sub> = t<sub>R</sub> − t<sub>M</sub>. En capa fina: <b>Rf = distancia del soluto / distancia del disolvente</b>. La <b>HPLC</b> usa bomba de alta presión y partículas pequeñas.</p>"
             "<p><strong>Osmometría</strong>: mide el número de partículas (osmolalidad, mOsm/kg). Crioscopia: al subir la osmolalidad <b>baja el punto de congelación</b>; presión de vapor: al subir la osmolalidad <b>baja la presión de vapor</b>. "
             "<strong>ISE</strong>: diferencia de potencial frente a un electrodo de referencia; rápido (&lt; 1 min), técnica de elección para Na⁺, K⁺, Cl⁻.</p>"
             "<p><strong>Automatización</strong>: parcial (preanalítica: clasificar, centrifugar, destaponar, alicuotar; analítica: autoanalizador; postanalítica: pruebas reflejas, seroteca) o total (robots). Los errores son 76 % preanalíticos, 7 % analíticos y 17 % postanalíticos.</p>")
    T.form = ["Turbidimetría: luz transmitida · conc. altas", "Nefelometría: luz dispersada · conc. bajas", "Rf = d soluto / d disolvente", "t'R = tR − tM", "η = c / v", "Pico base = 100 % · pico molecular = masa"]
    T.lesson = ("<h3>Idea central</h3><p>Esta unidad es «¿qué técnica uso?». Fíjate siempre en <b>qué se mide</b> (luz transmitida, dispersada, reflejada, iones…) y en <b>dónde está el detector</b>.</p>"
                "<div class=\"ej\"><b>Ejemplo:</b> para microorganismos en suspensión (muchas partículas) → turbidimetría; para una proteína a baja concentración con anticuerpos → nefelometría.</div>"
                "<div class=\"err\"><b>Error común:</b> pensar que el pico base es el de la molécula entera. El pico base es el <b>más alto</b>; el molecular es el de <b>mayor m/z</b> (sin fragmentar).</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> en el osmómetro de presión de vapor, al aumentar la osmolalidad la presión de vapor <b>disminuye</b> (el PDF dice que aumenta). Y el caso del espectro se llama «pentano» pero dibuja el 2-metilbutano: ambos tienen M = 72 y pico base 43.</div>")
    T.tools = [{"w": "calib", "t": "Curva de calibrado (turbidimetría)", "p": "En turbidimetría y en el ISE siempre se trabaja con curva de calibrado.", "o": {"pts": [[0, 0], [25, .09], [50, .18], [75, .27], [100, .355], [150, .45], [200, .5]], "lin": 100, "a": .22, "u": "mg/L"}}]
    T.add(1, "Turbidímetro o nefelómetro", "<p>Mira los dos equipos: en ambos la luz atraviesa una suspensión de partículas.</p>",
          [tap("Toca el detector del <b>nefelómetro</b>.", "turbnef", "d2", e="El nefelómetro mide la luz dispersada: su detector está en ángulo, no en línea."),
           opt("¿Qué técnica elegirías para cuantificar microorganismos en suspensión (concentración alta)?", "Turbidimetría", "Nefelometría", "Refractometría", "Fluorimetría", "Osmometría")],
          ["Turbidimetría: detector en línea, mide la luz transmitida (la que no se dispersó).", "Nefelometría: detector en ángulo, mide la luz dispersada; es mejor para concentraciones bajas.", "Con muchas partículas la transmitida baja claramente → turbidimetría."],
          "Equipo 2 · turbidimetría", "¿Qué luz recoge cada detector?")
    T.add(1, "Transmitancia en turbidimetría", "<p>Un espectrofotómetro UV-VIS da A = 0,30 en una suspensión.</p>",
          [num("Transmitancia", ("%T", 50.1, "%", 0.3))],
          ["A = 2 − log %T → log %T = 2 − 0,30 = 1,70.", "%T = 10^1,70 = 50,1 %."],
          "50,1 %", "Usa la fórmula de la UF1.")
    T.add(2, "Espectro de masas", "<p>Espectro de un hidrocarburo de fórmula C₅H₁₂ (masa molar 72).</p>",
          [tap("Toca el <b>pico base</b>.", "ms", "m43"), tap("Toca el <b>pico molecular</b>.", "ms", "m72", e="El pico molecular corresponde a la molécula entera ionizada: m/z = 72.")],
          ["Pico base: la señal más intensa (se le asigna el 100 %): m/z = 43.", "Pico molecular: la molécula sin fragmentar; su m/z da la masa molar: 72.", "Los demás (15, 27, 29, 41, 42, 57) son picos de fragmentación."],
          "Base 43; molecular 72", "El base es el más alto; el molecular no tiene por qué serlo.", chain=True)
    T.add(1, "Factor de retención", "<p>Capa fina: el frente del disolvente avanzó 10 cm. Tres manchas recorrieron 1,5 cm, 3 cm y 7 cm.</p>",
          [num("Rf de cada mancha", ("Mancha 1", 0.15, None, 0.005), ("Mancha 2", 0.3, None, 0.005), ("Mancha 3", 0.7, None, 0.005))],
          ["Rf = distancia del soluto / distancia del disolvente.", "1,5/10 = 0,15; 3/10 = 0,30; 7/10 = 0,70."],
          "0,15 · 0,30 · 0,70", "Divide entre la distancia del frente.")
    T.add(2, "Tipos de cromatografía", "<p>¿Qué cromatografía usarías?</p>",
          [cls("Fundamento", ["Intercambio iónico", "Exclusión molecular", "Afinidad", "Gases"],
               [("Separar proteínas por su carga neta (p. ej., HbA1c)", 0), ("Separar moléculas por tamaño con esferas de gel poroso", 1), ("Test de embarazo (antígeno-anticuerpo)", 2),
                ("Analizar compuestos volátiles con un gas inerte como fase móvil", 3), ("Resina con cargas fijas y contraiones", 0), ("Unión enzima-sustrato o ligando-receptor", 2)])],
          ["Intercambio iónico: atracción electrostática por grupos cargados de la resina.", "Exclusión: el gel retiene las moléculas pequeñas en sus poros.", "Afinidad: uniones específicas (Ag-Ac, enzima-sustrato).", "Gases: fase móvil gaseosa (He, Ar, N₂), para volátiles."],
          "II · EM · Af · Gas · II · Af", "¿Qué propiedad aprovecha cada una?")
    T.add(2, "Exclusión molecular", "<p>Pasas por una columna de exclusión molecular una mezcla de albúmina (66 kDa), IgM (900 kDa) y glucosa.</p>",
          [opt("¿Cuál sale primero?", "IgM: es tan grande que no entra en los poros", "Glucosa: es la más pequeña y corre más", "Albúmina: es la más abundante", "Salen todas a la vez", "Depende solo de la carga")],
          ["Las moléculas grandes no caben en los poros y pasan entre las esferas: recorren menos camino y salen antes.", "Las pequeñas entran en los poros y se retrasan."],
          "IgM", "En este caso, lo grande va «por fuera».")
    T.add(2, "Cromatograma", "<p>Cromatograma de una mezcla en columna.</p>",
          [tap("Toca el pico del compuesto <b>no retenido</b> (marca el tiempo muerto).", "cromat", "p1"),
           tap("Toca el compuesto que <b>más interactúa</b> con la fase estacionaria.", "cromat", "p3")],
          ["El compuesto no retenido sale con el frente de fase móvil: su tiempo es el tiempo muerto t<sub>M</sub>.", "Cuanto más interactúa con la fase estacionaria, más tarde eluye: el último pico."],
          "Primer pico · último pico", "Más retenido = más tiempo en salir.", chain=True)
    T.add(1, "Etapas de la espectrometría de masas", "<p>Ordena el funcionamiento del espectrómetro.</p>",
          [order("Orden", ["Volatilizar la muestra (moléculas en fase gaseosa)", "Ionizar las moléculas", "Acelerar los iones en un campo eléctrico", "Separar los iones según su m/z", "Detectar y procesar la señal (espectro)"])],
          ["Sin iones no hay separación: primero fase gaseosa, luego ionización (ESI/MALDI).", "El analizador separa por m/z y el detector amplifica la señal."],
          "Volatilizar → ionizar → acelerar → separar → detectar", "Piensa en qué necesita cada paso del anterior.")
    T.add(1, "Automatización: ¿en qué fase?", "<p>Clasifica cada unidad o tarea.</p>",
          [cls("Fase", ["Preanalítica", "Analítica", "Postanalítica"],
               [("Unidad destaponadora", 0), ("Unidad alicuotadora", 0), ("Pipetas de dispensación de reactivos", 1), ("Pruebas reflejas según el resultado", 2), ("Centrifugación de los tubos", 0), ("Sistema de medida espectrofotométrica", 1), ("Archivo de alícuotas (seroteca) para análisis futuros", 2)])],
          ["Preanalítica: preparar la muestra (clasificar, centrifugar, destaponar, alicuotar).", "Analítica: el autoanalizador mide.", "Postanalítica: validar, informar, pruebas reflejas y archivo de muestras."],
          "Pre · pre · ana · post · pre · ana · post", "¿Antes, durante o después de medir?")
    T.add(1, "Química seca (caso Mónica)", "<p>Mónica pasa a un laboratorio con autoanalizadores de química seca.</p>",
          [opt("¿Qué precaución es clave al almacenar esos reactivos?", "Protegerlos de la humedad", "Guardarlos siempre congelados", "Guardarlos en envases transparentes al sol", "Diluirlos antes de guardarlos", "Ninguna: la química seca no caduca")],
          ["En química seca es el agua de la muestra la que humedece y activa el reactivo.", "Si el reactivo absorbe humedad, se altera y los resultados dejan de ser fiables."],
          "Protegerlos de la humedad", "¿Qué activa el reactivo seco?")
    T.add(1, "Osmometría", "<p>Una muestra tiene más partículas disueltas que otra.</p>",
          [opt("En el osmómetro de punto de congelación, la muestra más concentrada…", "Congela a menor temperatura (mayor descenso crioscópico)", "Congela a mayor temperatura", "Congela igual: solo importa el tamaño de las partículas", "No congela", "Tiene mayor presión de vapor"),
           opt("Y en el de presión de vapor…", "Su presión de vapor es menor", "Su presión de vapor es mayor", "Su presión de vapor no cambia", "No se puede medir", "Se mide con un refractómetro")],
          ["Las propiedades coligativas dependen del número de partículas: más solutos → mayor descenso del punto de congelación.", "Más solutos → menor presión de vapor (el PDF lo pone al revés)."],
          "Menor punto de congelación y menor presión de vapor", "Piensa en la sal que se echa al hielo.")
    T.add(1, "Errores del laboratorio", "<p>Según la ISO, los errores se reparten entre las tres fases.</p>",
          [opt("¿Dónde se producen la mayoría?", "En la fase preanalítica (~76 %)", "En la fase analítica (~76 %)", "En la fase postanalítica (~76 %)", "Se reparten por igual", "Solo en el autoanalizador"),
           opt("¿Por qué han bajado los errores en los últimos años?", "Por la informatización, la automatización y la robotización", "Porque ya no se usan controles de calidad", "Porque los pacientes ya no ayunan", "Porque se eliminó la fase preanalítica", "Por usar más reactivos caducados")],
          ["La fase preanalítica depende de muchas personas (paciente, médico, enfermería, transporte): 76 % de los errores.", "Los sistemas informáticos, la automatización y la robótica han reducido los errores de todas las fases."],
          "Preanalítica; informatización y automatización", "¿Cuántas personas tocan la muestra antes de medirla?")
    return T

def uf3():
    T = Topic("u3", "UF3 · Metabolismo de los glúcidos y diabetes", "dm")
    T.teo = ("<p><strong>Metabolismo</strong> = catabolismo (degrada y libera energía: ATP, NADH, FADH₂) + anabolismo (sintetiza, consume energía). "
             "Rutas de la glucosa: <b>glucólisis</b> (glucosa → 2 piruvato, citosol), <b>glucogenogénesis</b> (síntesis de glucógeno, anabólica), <b>glucogenólisis</b> (degradación de glucógeno), "
             "<b>gluconeogénesis</b> (glucosa a partir de lactato, aminoácidos o glicerol; hígado y corteza renal), <b>pentosas fosfato</b> (NADPH y ribosa-5-P, sin ATP), <b>vía del sorbitol</b> (cataratas y neuropatía en diabéticos).</p>"
             "<p><strong>Hormonas</strong>: la <b>insulina</b> (células β) es la única hipoglucemiante; son hiperglucemiantes el <b>glucagón</b> (células α), la adrenalina, el cortisol, la GH y la tiroxina.</p>"
             "<p><strong>Glucosa en sangre</strong>: plasma, por la mañana tras <b>8 h de ayuno</b>; separar en &lt; 30 min o usar tubo con <b>fluoruro sódico</b> (inhibe la enolasa); sin separar baja un 5–7 %/h. "
             "Métodos enzimáticos: <b>glucosa oxidasa-peroxidasa (GOD-POD)</b> a punto final (cromógeno; interfieren reductores como el ascorbato) y <b>hexoquinasa</b> (método de referencia; mide NADH a 340 nm).</p>"
             "<p><strong>Otras pruebas</strong>: <b>HbA1c</b> (glucosa media de ~2–3 meses; cromatografía de intercambio iónico; EDTA, sin ayuno), <b>fructosamina</b> (1–3 semanas: gestación, anemia o hemoglobinopatías), "
             "<b>péptido C</b> (insulina propia; bajo con insulina alta = insulina inyectada), <b>microalbuminuria</b> (nefropatía diabética precoz), glucosuria (umbral renal ~180 mg/dL) y azúcares reductores (Benedict: Cu²⁺ azul → Cu₂O rojo-naranja).</p>"
             "<p><strong>Diabetes mellitus</strong>: tipo 1 (autoinmune, insulinopenia, cetoacidosis, jóvenes), tipo 2 (resistencia a la insulina, 80–90 %, obesidad), prediabetes y gestacional. "
             "Criterios: <b>HbA1c ≥ 6,5 %</b>, <b>glucemia en ayunas ≥ 126 mg/dL</b> (dos veces), <b>SOG a las 2 h ≥ 200 mg/dL</b> (75 g) o <b>glucemia al azar ≥ 200 mg/dL con síntomas</b>. "
             "Prediabetes: ayunas 100–125 (glucemia alterada) o SOG 140–199 (intolerancia). <strong>Hipoglucemia</strong>: &lt; 70 mg/dL (nivel 1), &lt; 54 (nivel 2), severa si necesita ayuda (nivel 3).</p>")
    T.form = ["Ayunas ≥ 126 mg/dL (×2) → DM", "SOG 2 h ≥ 200 → DM · 140–199 → intolerancia", "HbA1c ≥ 6,5 % → DM", "Al azar ≥ 200 + síntomas → DM", "Ayunas 100–125 → glucemia alterada (ADA)", "Hipoglucemia < 70 · < 54 · severa"]
    T.lesson = ("<h3>Idea central</h3><p>En los casos de esta unidad te dan glucemias, HbA1c o una curva y tienes que <b>clasificar al paciente</b> y decir <b>qué muestra y qué tubo</b> usar.</p>"
                "<h3>Algoritmo</h3><ul><li><b>1.</b> Glucemia basal &lt; 100 → normal.</li><li><b>2.</b> 100–125 → repetir y, si sigue alterada, SOG.</li><li><b>3.</b> SOG a las 2 h: &lt; 140 normal · 140–199 intolerancia · ≥ 200 diabetes.</li><li><b>4.</b> ≥ 126 en dos ocasiones → diabetes.</li></ul>"
                "<div class=\"ej\"><b>Test de O’Sullivan (embarazo):</b> 50 g de glucosa y glucemia a la hora; si sale entre 140 y 200 se hace la curva larga con 100 g.</div>"
                "<div class=\"err\"><b>Error común:</b> usar la HbA1c para ver el control de las últimas 2 semanas. Para periodos cortos (gestación, anemias) se usa la <b>fructosamina</b>.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> el criterio es glucemia ≥ 200 mg/<b>dL</b> (no mg/mL). Y la tabla de normalidad mezcla el límite de la OMS (110) con el de la ADA (100): en los ejercicios se indica cuál se usa.</div>")
    T.add(1, "Hormonas y glucemia", "<p>Clasifica las hormonas que regulan la glucemia.</p>",
          [cls("Efecto", ["Hipoglucemiante", "Hiperglucemiante"],
               [("Insulina", 0), ("Glucagón", 1), ("Adrenalina", 1), ("Cortisol", 1), ("Hormona del crecimiento (GH)", 1, "Altos niveles de GH dan resistencia a la insulina."), ("Tiroxina", 1)])],
          ["La insulina (células β) es la única que baja la glucemia: favorece la entrada de glucosa y la síntesis de glucógeno.", "Glucagón, adrenalina, cortisol, GH y tiroxina la suben."],
          "Solo la insulina es hipoglucemiante.", "Solo hay una que la baja.")
    T.add(1, "Rutas metabólicas", "<p>Clasifica cada ruta.</p>",
          [cls("Tipo de ruta", ["Catabólica", "Anabólica"],
               [("Glucólisis", 0), ("Glucogenogénesis", 1), ("Glucogenólisis", 0), ("Gluconeogénesis", 1, "Sintetiza glucosa (consume ATP): anabólica."), ("Ruta de las pentosas fosfato", 0), ("Lipogénesis", 1)])],
          ["Catabólicas: degradan (glucólisis, glucogenólisis, pentosas fosfato).", "Anabólicas: sintetizan con gasto de energía (glucogenogénesis, gluconeogénesis, lipogénesis)."],
          "C · A · C · A · C · A", "¿Construye o rompe?")
    T.add(2, "Algoritmo diagnóstico (ADA)", "<p>Mujer de 45 años, asintomática. Glucemia basal: <b>112 mg/dL</b>. Usa los criterios de la ADA.</p>",
          [tree("Recorre el algoritmo.", [
              ("¿Cómo clasificas la glucemia basal de 112 mg/dL?", ["Alterada (100–125): hay que repetirla", "Normal", "Diabetes directamente", "Hipoglucemia"], [None, "Normal según la ADA es < 100 mg/dL.", "Para diabetes hacen falta ≥ 126 mg/dL en dos ocasiones.", "Hipoglucemia es < 70 mg/dL."]),
              ("Se repite y sale 118 mg/dL. ¿Qué haces?", ["Prueba de sobrecarga oral (75 g) con glucemia a las 2 h", "Diagnosticar diabetes", "Alta: es normal", "Medir solo glucosuria"], [None, "Sigue sin llegar a 126.", "Sigue siendo ≥ 100.", "La glucosuria es solo complementaria (umbral 180)."], "Glucemia alterada en ayunas (prediabetes) → SOG."),
              ("La glucemia a las 2 h de la SOG es 165 mg/dL. ¿Resultado?", ["Intolerancia a la glucosa (140–199)", "Normal (< 200)", "Diabetes (≥ 140)", "Hipoglucemia reactiva"], [None, "Normal es < 140.", "Diabetes es ≥ 200 a las 2 h.", "No hay valores bajos."])],
              "Prediabetes: glucemia basal alterada + intolerancia a la glucosa. Control y cambios en el estilo de vida.")],
          ["112 está entre 100 y 124 (ADA) → repetir.", "Persistente → SOG con 75 g de glucosa anhidra.", "2 h: 140–199 → intolerancia a la glucosa (prediabetes)."],
          "Prediabetes (intolerancia a la glucosa)", "Sigue la Figura 8 del material.")
    T.add(2, "Lee la analítica: diabetes", "<p>Varón de 52 años con poliuria y polidipsia. Analítica en ayunas:</p>",
          [lab("Valora cada parámetro.", "Varón · 52 años · ayunas de 8 h", [
              ("Glucosa", "148", "mg/dL", "70–100", 1), ("HbA1c", "7,4", "%", "< 5,7", 1), ("Glucosa en orina", "Positiva", "", "Negativa", 1, "Si la glucemia supera el umbral renal (~180), aparece glucosuria."),
              ("Péptido C", "1,8", "ng/mL", "0,8–3,1", 0), ("Creatinina", "0,9", "mg/dL", "0,7–1,3", 0)]),
           opt("¿Qué concluyes?", "Diabetes: HbA1c ≥ 6,5 % y glucemia en ayunas ≥ 126", "Prediabetes", "Hipoglucemia", "Normal: falta la SOG", "Diabetes tipo 1 con cetoacidosis")],
          ["Glucosa 148 ≥ 126 y HbA1c 7,4 ≥ 6,5: cumple dos criterios.", "El péptido C normal indica que aún produce insulina (más propio de tipo 2).", "Con síntomas y dos criterios no hace falta SOG."],
          "Diabetes", "Compara con los criterios de la Tabla 7.")
    T.add(1, "HbA1c y glucemia media", "<p>Según la tabla de equivalencias (6 % → 135, 7 % → 170, 8 % → 205 mg/dL; +35 por cada punto).</p>",
          [num("Glucemia media estimada", ("HbA1c 9 %", 240, "mg/dL", 1), ("HbA1c 7,5 %", 187.5, "mg/dL", 2))],
          ["Cada 1 % de HbA1c suma 35 mg/dL.", "9 %: 205 + 35 = 240. 7,5 %: 170 + 17,5 = 187,5 mg/dL."],
          "240 y 187,5 mg/dL", "Interpola en la tabla.")
    T.add(1, "Método de la glucosa oxidasa", "<p>Ordena las reacciones del método GOD-POD.</p>",
          [order("Orden", ["La mutarrotasa pasa la α-D-glucosa a β-D-glucosa", "La GOD oxida la β-D-glucosa a ácido glucónico + H₂O₂", "La peroxidasa usa el H₂O₂ para oxidar el cromógeno", "Se mide la absorbancia del color formado (punto final)"])],
          ["La GOD actúa sobre la forma β; por eso algunos reactivos llevan mutarrotasa.", "El H₂O₂ se acopla con un cromógeno (reactivo de Trinder: color rojo) mediante la peroxidasa."],
          "Mutarrotasa → GOD → POD → leer A", "¿Quién produce el H₂O₂?")
    T.add(2, "Muestra para glucosa", "<p>Carolina prepara el protocolo de extracción. ¿Correcto o error?</p>",
          [cls("Clasifica", ["Correcto", "Error"],
               [("Medir en plasma, por la mañana, tras 8 h de ayuno", 0), ("Dejar el tubo sin separar toda la mañana en la mesa", 1, "La glucólisis ex vivo baja la glucosa un 5–7 % por hora."),
                ("Usar tubo con fluoruro sódico si no se separa enseguida", 0), ("El fluoruro actúa porque inhibe la enolasa", 0), ("Medir en sangre total porque da valores un 11 % más altos", 1, "Es al revés: el plasma da ~11 % más que la sangre total y no depende del hematocrito."),
                ("Separar células y plasma en menos de 30 minutos", 0)])],
          ["Plasma, ayuno de 8 h, separación < 30 min o tubo con inhibidor de la glucólisis.", "El fluoruro inhibe la enolasa (glucólisis); el plasma da un 11 % más que la sangre total."],
          "C · E · C · C · E · C", "La glucosa se sigue consumiendo dentro del tubo.")
    T.add(1, "Método de referencia", "<p>¿Cuál es el método de referencia para la glucosa y qué mide?</p>",
          [opt("Método", "Hexoquinasa / G6P-deshidrogenasa: mide el NADH formado a 340 nm", "Glucosa oxidasa: mide un cromógeno rojo a 505 nm", "Benedict: precipitado rojo de Cu₂O", "Refractometría", "Cromatografía de intercambio iónico")],
          ["Hexoquinasa: glucosa → glucosa-6-P; la G6PDH forma NADH, que absorbe a 340 nm.", "Es muy específico y sirve para sangre, orina, LCR y líquidos."],
          "Hexoquinasa (NADH a 340 nm)", "La coenzima reducida absorbe en el UV cercano.")
    T.add(2, "¿Qué prueba pides?", "<p>Elige la determinación más útil en cada caso.</p>",
          [cls("Prueba", ["HbA1c", "Fructosamina", "Péptido C", "Microalbuminuria"],
               [("Control del diabético en los últimos 2–3 meses", 0), ("Control de una embarazada diabética en las últimas semanas", 1), ("Diabético con anemia hemolítica (HbA1c no fiable)", 1),
                ("Sospecha de hipoglucemia por inyección de insulina a escondidas", 2, "Insulina alta con péptido C bajo = insulina exógena."), ("Detectar precozmente la nefropatía diabética", 3), ("Valorar si el páncreas aún secreta insulina", 2)])],
          ["HbA1c: glucemia media de meses. Fructosamina: 1–3 semanas y cuando la HbA1c falla.", "Péptido C: se libera junto a la insulina propia.", "Microalbuminuria: daño renal precoz."],
          "A1c · Fr · Fr · PC · MA · PC", "¿Qué periodo o qué órgano te interesa?")
    T.add(1, "Gravedad de la hipoglucemia", "<p>Clasifica según la ADA-EASD.</p>",
          [cls("Nivel", ["Nivel 1", "Nivel 2", "Nivel 3"],
               [("Glucemia 65 mg/dL, el paciente se trata solo", 0), ("Glucemia 50 mg/dL", 1), ("Confusión que requiere ayuda de otra persona", 2, "El nivel 3 no tiene punto de corte: se define por necesitar ayuda externa."), ("Glucemia 68 mg/dL con sudoración y temblor", 0)])],
          ["< 70 mg/dL: nivel 1 (alerta). < 54: nivel 2 (clínicamente significativa).", "Nivel 3: alteración cognitiva grave que necesita ayuda externa."],
          "1 · 2 · 3 · 1", "Fíjate en 70 y 54.")
    T.add(1, "Azúcares reductores", "<p>En una orina se sospecha galactosa (no la detecta la tira de glucosa oxidasa).</p>",
          [opt("¿Qué prueba usas y qué ves si es positiva?", "Benedict: el Cu²⁺ azul pasa a precipitado rojo-naranja de Cu₂O", "Biuret: color violeta", "Nitroprusiato: color púrpura", "Ehrlich: color rosado", "Jaffé: color rojizo")],
          ["Los azúcares reductores reducen el Cu²⁺ (azul) a Cu⁺ en medio alcalino → Cu₂O rojo-naranja.", "La tira (GOD) solo detecta glucosa."],
          "Benedict", "Reducen el cobre.")
    return T
