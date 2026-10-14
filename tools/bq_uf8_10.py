from bq_lib import *

def uf8():
    T = Topic("u8", "UF8 · Análisis de orina: tira, sedimento y cálculos", "ori")
    T.teo = ("<p>La <strong>orina</strong> normal es amarillo-ámbar (urobilina), transparente, con densidad 1,010–1,030 y pH 6–6,5 (rango 4,5–8). Diuresis 800–2 000 mL/24 h: <b>oliguria</b> &lt; 450 (adulto), <b>anuria</b> &lt; 200, <b>poliuria</b> &gt; 2 500–3 000 mL/24 h. "
             "Orden del estudio: examen físico → microbiológico (si se pide) → bioquímico y densidad → sedimento.</p>"
             "<p><strong>Tira reactiva</strong> (química seca, reflectancia): sumergir 10 s, escurrir y leer cada almohadilla a su tiempo con la carta de colores o con lector automático. "
             "<b>Glucosa</b> (GOD-POD, 30 s; umbral renal 160–180 mg/dL), <b>bilirrubina</b> (diazo, 30 s; solo la conjugada), <b>cetonas</b> (nitroprusiato, 40 s; acetoacetato y acetona), <b>densidad</b> (45 s), "
             "<b>sangre</b> (pseudoperoxidasa: punteado = hematíes intactos; uniforme = hemoglobina o mioglobina; 60 s), <b>pH</b> (60 s), <b>proteínas</b> (error de proteínas del indicador; sobre todo albúmina; no detecta Bence-Jones; 60 s), "
             "<b>urobilinógeno</b> (60 s), <b>nitritos</b> (Griess; bacterias gramnegativas; 60 s) y <b>leucocitos</b> (esterasa; 2 min).</p>"
             "<p><strong>Sedimento</strong>: 10 mL, centrifugar a 1 500–2 000 rpm durante 5–10 min, decantar dejando 0,5–1 mL, resuspender, montar sin burbujas y mirar a <b>10x</b> (cilindros, cristales) y a <b>40x</b> (hematíes, leucocitos, bacterias). Antes de 3–4 h. "
             "Hematíes &gt; 3/campo = hematuria (dismórficos = glomerulares). Leucocitos &gt; 2–3/campo = leucocituria. Células escamosas (sin valor), de transición y <b>tubulares</b> (daño renal). "
             "<b>Cilindros</b> (proteína de Tamm-Horsfall): hialinos (sin valor), granulosos, hemáticos (glomerulonefritis), leucocitarios (pielonefritis), céreos (ERC avanzada), grasos. "
             "<b>Cristales</b> de orina ácida: oxalato cálcico (dihidrato en sobre; monohidrato en pesa), ácido úrico (amarillo, romboidal), uratos amorfos. De orina alcalina: <b>estruvita</b> (tapa de ataúd; infección por gérmenes ureolíticos), fosfatos amorfos, urato amónico, carbonato. Patológicos: <b>cistina</b>, tirosina, leucina, colesterol.</p>"
             "<p><strong>Orina de 24 h</strong>: proteinuria (&gt; 150 mg/día; significativa &gt; 300), Bence-Jones, <b>microalbuminuria 30–300 mg/día</b> (macro &gt; 300), mucopolisacáridos (test de Berry), porfirinas (envase opaco: <b>ALA con ácido acético</b>; <b>porfobilinógeno con carbonato sódico</b>), cortisol (Cushing) y marcadores óseos. "
             "<strong>Cálculos</strong>: estudio macroscópico (lavar, medir, describir, fracturar) + composición (la técnica más usada es la <b>espectroscopia IR</b>). Los más frecuentes son de oxalato cálcico.</p>")
    T.form = ["Oliguria < 450 · anuria < 200 · poliuria > 2 500 mL/día", "Densidad 1,010–1,030 · pH 4,5–8", "Microalbuminuria 30–300 mg/día", "Proteinuria > 150 (significativa > 300) mg/día", "Sedimento: 10x cilindros/cristales · 40x células", "ALA → ácido acético · PBG → carbonato sódico"]
    T.lesson = ("<h3>Idea central</h3><p>Es la unidad más práctica: <b>leer una tira</b> respetando los tiempos e <b>identificar al microscopio</b> células, cilindros y cristales. Usa las dos herramientas 🧪 de abajo para entrenar el ojo.</p>"
                "<div class=\"ej\"><b>Infección urinaria típica:</b> leucocitos +++, nitritos positivos, algo de sangre; en el sedimento, leucocitos y bacterias; confirmar con urocultivo.</div>"
                "<div class=\"err\"><b>Error común:</b> leer todas las almohadillas a la vez al final. Cada parámetro tiene su tiempo (glucosa 30 s… leucocitos 2 min).</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> la glucosuria no es «siempre patológica»: hay glucosuria renal y en el embarazo sin enfermedad. Y la proteinuria normal es &lt; 150 mg/<b>día</b> (en un punto dice «2 a 10 mg/dL»).</div>")
    T.tools = [{"w": "tira", "t": "Carta de colores de la tira", "o": {}}, {"w": "micro", "t": "Atlas del sedimento urinario", "o": {"g": ["Células", "Cilindros", "Cristales", "Microorganismos"]}}]
    T.add(2, "Lee la tira 1", "<p>Varón de 24 años con sed intensa, poliuria y aliento afrutado. Lee la tira.</p>",
          [tira("Toca, para cada almohadilla, el color de la carta que coincide.", {"leu": 0, "nit": 0, "uro": 0, "pro": 1, "ph": 0, "san": 0, "den": 5, "cet": 4, "bil": 0, "glu": 4}, ["glu", "cet", "ph", "den", "pro"]),
           opt("¿Qué sugiere?", "Diabetes descompensada con cetosis (glucosuria y cetonuria intensas)", "Infección urinaria", "Ictericia obstructiva", "Hematuria por cálculo", "Orina normal")],
          ["Glucosa ≥ 1 000 y cetonas 80 mg/dL, pH 5 y densidad alta.", "Glucosuria + cetonuria + aliento afrutado = cetoacidosis diabética probable."],
          "Glucosuria y cetonuria → DM descompensada", "Compara color por color, no de memoria.")
    T.add(2, "Lee la tira 2", "<p>Mujer de 30 años con disuria y polaquiuria. Lee estas almohadillas.</p>",
          [tira("Toca el color correcto.", {"leu": 3, "nit": 1, "uro": 0, "pro": 1, "ph": 5, "san": 2, "den": 2, "cet": 0, "bil": 0, "glu": 0}, ["leu", "nit", "san", "ph"]),
           opt("¿Qué sugiere y qué haces?", "Infección urinaria: confirmar con urocultivo", "Diabetes: pedir HbA1c", "Ictericia: pedir bilirrubina", "Normal: no hace falta nada", "Rabdomiólisis: pedir CK")],
          ["Leucocitos ++ y nitritos positivos: bacterias gramnegativas que reducen nitratos.", "pH alcalino (8) es frecuente con gérmenes ureolíticos.", "La tira orienta; el diagnóstico se confirma con urocultivo."],
          "ITU → urocultivo", "Los nitritos solo tienen dos colores.")
    T.add(1, "Tiempos de lectura", "<p>¿A qué tiempo se lee cada almohadilla?</p>",
          [cls("Tiempo", ["30 s", "40–45 s", "60 s", "2 min"],
               [("Glucosa", 0), ("Bilirrubina", 0), ("Cetonas", 1), ("Densidad", 1), ("Nitritos", 2), ("Sangre", 2), ("Leucocitos", 3, "La esterasa leucocitaria es la reacción más lenta.")])],
          ["Glucosa y bilirrubina: 30 s. Cetonas: 40 s. Densidad: 45 s.", "pH, proteínas, sangre, urobilinógeno y nitritos: 60 s. Leucocitos: 2 min."],
          "30 · 30 · 40 · 45 · 60 · 60 · 2 min", "Los leucocitos son los últimos.")
    T.add(2, "Microscopio: cristales", "<p>Sedimento de una orina ácida.</p>",
          [micro("Toca el cristal de <b>ácido úrico</b>.", [("oxd", -.45, -.3), ("uric", .35, -.35, 20), ("hem", -.1, .3), ("leu", .4, .35), ("esc", -.5, .45, 10), ("hem", .05, -.05)], ["1"], e="El ácido úrico es amarillo-ámbar y romboidal (en «limón»)."),
           micro("Ahora toca el <b>oxalato cálcico dihidratado</b>.", [("oxd", -.45, -.3), ("uric", .35, -.35, 20), ("hem", -.1, .3), ("leu", .4, .35), ("esc", -.5, .45, 10), ("hem", .05, -.05)], ["0"], e="Es el que parece un sobre: un cuadrado con una X.")],
          ["Ácido úrico: amarillo, rombos o rosetas; orina ácida; gota y cálculos.", "Oxalato dihidratado: bipirámide en «sobre»; sin interés clínico si es aislado."],
          "El amarillo romboidal y el «sobre»", "Fíjate en el color y la forma.", chain=True)
    T.add(2, "Microscopio: cilindros", "<p>Paciente con edemas, hipertensión y orina color «coca-cola».</p>",
          [micro("Toca el cilindro que indica <b>sangrado glomerular</b>.", [("chia", -.35, -.35, 15), ("chem", .25, .05, -10), ("cgra", -.3, .45, 5), ("hem", .5, -.45), ("hem", .45, .55)], ["1"], obj=10, e="Busca el cilindro con hematíes dentro."),
           opt("¿Qué patología sugiere?", "Glomerulonefritis", "Cistitis bacteriana", "Deshidratación leve", "Contaminación vaginal", "Ejercicio intenso")],
          ["Cilindro hemático: hematíes atrapados en la proteína de Tamm-Horsfall dentro del túbulo → el sangrado es renal.", "Con edemas, HTA y orina oscura → glomerulonefritis."],
          "Cilindro hemático → glomerulonefritis", "El hialino es casi invisible y no tiene valor.", chain=True)
    T.add(2, "Microscopio: orina alcalina", "<p>Orina alcalina (pH 8) en un paciente con infección por <i>Proteus</i>.</p>",
          [micro("Toca el cristal típico de la infección por gérmenes ureolíticos.", [("oxd", -.4, -.35), ("estr", .3, .1, 10), ("amor", -.35, .4), ("bac", .45, -.45), ("bac", -.05, -.05)], ["1"], e="Tiene forma de «tapa de ataúd»."),
           opt("¿Qué tipo de cálculo puede formar?", "De estruvita (fosfato amónico-magnésico), a veces coraliforme", "De ácido úrico", "De cistina", "De oxalato dihidratado", "De colesterol")],
          ["La ureasa del <i>Proteus</i> produce amoniaco: alcaliniza la orina y precipita fosfato amónico-magnésico (estruvita).", "Puede formar cálculos coraliformes."],
          "Estruvita", "Pensar en la ureasa.", chain=True)
    T.add(1, "Obtener el sedimento (caso Inma)", "<p>Ordena el procedimiento.</p>",
          [order("Orden", ["Homogeneizar bien la muestra", "Poner unos 10 mL en un tubo de centrífuga", "Centrifugar a 1 500–2 000 rpm durante 5–10 min", "Decantar el sobrenadante dejando 0,5–1 mL", "Resuspender el sedimento", "Montar una gota con cubreobjetos, sin burbujas", "Observar a 10x y luego a 40x"])],
          ["Centrifugar concentra los elementos; se deja un volumen residual para resuspender.", "10x para cilindros y cristales (los cilindros se van a los bordes); 40x para células y microorganismos."],
          "Homogeneizar → 10 mL → centrifugar → decantar → resuspender → montar → 10x/40x", "Primero el aumento menor.")
    T.add(1, "Color de la orina", "<p>Relaciona cada color con su causa más probable.</p>",
          [cls("Causa", ["Pigmentos biliares", "Sangre", "Infección o quilomicrones", "Alcaptonuria"],
               [("Marrón oscuro, «como coca-cola», con espuma amarilla", 0), ("Rojiza con sedimento rojo", 1), ("Blanquecina, lechosa", 2), ("Se vuelve negra al exponerse al aire", 3, "El ácido homogentísico se oxida con el aire."), ("Verdosa-amarilla con ictericia", 0)])],
          ["Bilirrubina/urobilinógeno: amarillo verdoso a marrón.", "Sangre: rojiza. Lechosa: pus (piuria) o quilomicrones. Negra al aire: alcaptonuria."],
          "Bil · Sangre · Inf · Alcap · Bil", "La alcaptonuria cambia con el aire.")
    T.add(1, "Volumen de 24 h (caso Mónica)", "<p>La orina de 24 h recogida mide 3 200 mL.</p>",
          [opt("¿Cómo se llama?", "Poliuria", "Oliguria", "Anuria", "Normal", "Polaquiuria"),
           opt("¿Qué puede causarla?", "Diabetes (mellitus o insípida), mucha ingesta de líquidos o diuréticos", "Deshidratación grave", "Obstrucción completa del tracto urinario", "Glomerulonefritis aguda", "Hemorragia")],
          ["Poliuria > 2 500–3 000 mL/24 h.", "Causas: diabetes, ingesta elevada, ERC, diuréticos, acromegalia…"],
          "Poliuria", "Normal es 800–2 000 mL.")
    T.add(1, "Cristales según el pH", "<p>¿En qué orina aparecen típicamente?</p>",
          [cls("pH", ["Orina ácida", "Orina alcalina"],
               [("Ácido úrico", 0), ("Estruvita (fosfato triple)", 1), ("Uratos amorfos (polvo rosado)", 0), ("Fosfatos amorfos (polvo blanco)", 1), ("Urato amónico", 1), ("Oxalato cálcico", 0), ("Carbonato cálcico", 1)])],
          ["Ácidas: ácido úrico, uratos amorfos, oxalato cálcico (y cistina, tirosina, leucina).", "Alcalinas: estruvita, fosfatos amorfos, fosfato cálcico, carbonato, urato amónico."],
          "Á · Al · Á · Al · Al · Á · Al", "Los uratos son ácidos (salvo el amónico).")
    T.add(2, "Porfiria (orina de 24 h)", "<p>Se sospecha una porfiria aguda y se piden los precursores en orina de 24 h.</p>",
          [cls("Conservante", ["Ácido acético glacial (pH < 5,5)", "Carbonato sódico (pH 8–9)"],
               [("Ácido δ-aminolevulínico (ALA)", 0), ("Porfobilinógeno (PBG)", 1), ("Porfirinas", 1)]),
           opt("¿Qué recipiente usas?", "Opaco o de color topacio, protegido de la luz", "Transparente, para ver el color", "Con fluoruro sódico", "Con EDTA", "Cualquiera, refrigerado")],
          ["El ALA es estable en medio ácido; el PBG y las porfirinas, en medio alcalino.", "Las porfirinas se degradan con la luz: envase opaco. El PBG se detecta con el reactivo de Ehrlich (color rosado)."],
          "ALA ácido · PBG y porfirinas alcalino · envase opaco", "Cada precursor tiene su pH.")
    T.add(1, "Albuminuria", "<p>Diabético con albúmina en orina de 24 h = 120 mg/día.</p>",
          [opt("¿Cómo se clasifica?", "Microalbuminuria (30–300 mg/día)", "Normal (< 300)", "Macroalbuminuria (> 30)", "Proteinuria de Bence-Jones", "Proteinuria ortostática")],
          ["30–300 mg/día = microalbuminuria; > 300 = macroalbuminuria.", "Es el marcador precoz de nefropatía diabética; se expresa también como cociente albúmina/creatinina."],
          "Microalbuminuria", "Entre 30 y 300.")
    return T

def uf9():
    T = Topic("u9", "UF9 · Heces, LCR, líquidos biológicos y semen", "liq")
    T.teo = ("<p><strong>Función digestiva</strong>: déficit de factor intrínseco (B12, fólico, ácido metilmalónico, homocisteína, gastrina); <i>H. pylori</i> (<b>test del aliento</b> con urea marcada con ¹³C o antígeno en heces); "
             "EII (<b>calprotectina</b> fecal); celiaquía (<b>anti-transglutaminasa IgA</b> y biopsia; tratamiento: dieta sin gluten); intolerancia a la lactosa (test de <b>hidrógeno espirado</b>); insuficiencia pancreática (grasa fecal, <b>elastasa</b> y quimotripsina bajas).</p>"
             "<p><strong>Heces</strong>: color (negras = melena, sangrado alto; blancas = acolia), escala de <b>Bristol</b> (3–4 normales), pH 6,8–7,2. <b>Sangre oculta</b>: el método <b>inmunoquímico</b> detecta globina humana (no da falsos positivos por la dieta; es el del cribado del cáncer de colon); el químico (guayaco) detecta el hemo y requiere dieta. "
             "Microscopio: fibras musculares mal digeridas (<b>creatorrea</b>), almidón azul-negro con lugol (<b>amilorrea</b>), grasas neutras con Sudán III (<b>esteatorrea</b>), cristales de Charcot-Leyden (parásitos).</p>"
             "<p><strong>LCR</strong>: transparente; glucosa 40–80 mg/dL (≈ 2/3 de la plasmática). Rojizo: si la sangre <b>disminuye del tubo 1 al 3</b> y el sobrenadante es claro → <b>punción traumática</b>; si es uniforme y el sobrenadante es <b>xantocrómico</b> → hemorragia subaracnoidea. "
             "Meningitis bacteriana: turbio, <b>glucosa ↓</b>, proteínas ↑, <b>lactato ↑</b>, neutrófilos; ADA &gt; 10 U/L → tuberculosa. Leucocitos normales 0–5/µL.</p>"
             "<p><strong>Líquido sinovial</strong>: viscoso (filancia de 2,5–5 cm), &lt; 200 leucocitos/µL. Para la bioquímica se trata con hialuronidasa. Cristales con luz polarizada: <b>urato monosódico</b> (agujas; gota) y <b>pirofosfato cálcico</b> (romboides; pseudogota). Glucosa ~10 mg/dL menor que la plasmática (más baja en la artritis séptica).</p>"
             "<p><strong>Líquidos serosos</strong> (pleural, pericárdico, peritoneal): <b>criterios de Light</b>: es exudado si proteína líquido/suero &gt; 0,5, o LDH líquido/suero &gt; 0,6, o LDH del líquido &gt; 2/3 del límite superior sérico. "
             "Glucosa &lt; 60 mg/dL en el exudado (&lt; 15 en la artritis reumatoide); ADA (tuberculosis); amilasa (pancreatitis). Ascitis: proteínas &lt; 3 g/dL trasudado; gradiente de albúmina &gt; 1,1 g/dL (11 g/L) → hipertensión portal.</p>"
             "<p><strong>Seminograma</strong> (OMS): volumen ≥ 1,5 mL, pH ≥ 7,2, licuefacción &lt; 30 min, concentración ≥ 15 millones/mL (total ≥ 39 M), progresivos ≥ 32 %, vivos ≥ 58 %, formas normales ≥ 4 %, leucocitos &lt; 1 M/mL. "
             "Marcadores: citrato, zinc, fosfatasa ácida → <b>próstata</b>; fructosa → <b>vesículas seminales</b>; carnitina y α-glucosidasa neutra → <b>epidídimo</b>. Mujer: FSH (día 2–3), AMH (reserva ovárica), progesterona (día 21).</p>")
    T.form = ["Light: prot L/S > 0,5 · LDH L/S > 0,6 · LDH L > 2/3 LSN", "LCR: glucosa 40–80 · leucocitos 0–5/µL", "Semen: ≥ 15 M/mL · ≥ 32 % prog. · ≥ 4 % normales", "Total = concentración × volumen", "Gradiente de albúmina > 1,1 g/dL → HT portal", "Sinovial < 200 leucocitos/µL"]
    T.lesson = ("<h3>Idea central</h3><p>Cada líquido tiene su <b>pregunta clave</b>: LCR → ¿punción traumática o hemorragia? ¿meningitis? · Pleural → ¿exudado o trasudado? (Light) · Sinovial → ¿qué cristal? · Semen → ¿qué nomenclatura?</p>"
                "<div class=\"ej\"><b>Light:</b> proteína líquido 3,8 / suero 6,2 = 0,61 &gt; 0,5 → exudado (basta un criterio).</div>"
                "<div class=\"err\"><b>Error común:</b> pedir sangre oculta química sin dieta previa: la carne roja da falsos positivos. Con el método inmunoquímico no hace falta.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> (1) los leucocitos normales del líquido sinovial son <b>&lt; 200/µL</b> (el PDF dice 100 000, que sería un líquido séptico). (2) En el LCR los recuentos son por <b>µL</b>, no por mL. (3) El gradiente de albúmina para la hipertensión portal es &gt; 1,1 g/dL (= 11 g/L). (4) Según la ESHRE, «infertilidad» no se limita a la mujer: el material lo simplifica.</div>")
    T.tools = [{"w": "micro", "t": "Atlas: sinovial y heces", "o": {"g": ["Líquido sinovial", "Heces"]}}]
    T.add(2, "Criterios de Light (caso Lucy)", "<p>Líquido pleural: proteínas 3,8 g/dL; LDH 320 U/L. Suero: proteínas 6,2 g/dL; LDH 210 U/L (límite superior normal 250).</p>",
          [num("Cocientes", ("Proteína líquido/suero", 0.61, None, 0.01), ("LDH líquido/suero", 1.52, None, 0.02)),
           opt("Conclusión", "Exudado (cumple los criterios de Light)", "Trasudado", "No se puede saber sin la glucosa", "Quilotórax", "Hemotórax")],
          ["3,8/6,2 = 0,61 > 0,5.", "320/210 = 1,52 > 0,6; además 320 > 2/3 × 250 = 167.", "Basta un criterio para que sea exudado: hay que buscar la causa (infección, cáncer, tuberculosis)."],
          "0,61 · 1,52 → exudado", "Basta con un criterio.")
    T.add(2, "LCR rojizo (caso Francisca)", "<p>Llegan tres tubos de LCR rojizo.</p>",
          [tree("Decide paso a paso.", [
              ("¿Qué miras primero en los tres tubos?", ["Si la sangre disminuye del tubo 1 al 3 o es uniforme", "Solo el tubo 3", "El volumen total", "El pH"], [None, "Necesitas comparar los tres.", "No orienta.", "No orienta."]),
              ("La sangre disminuye del 1 al 3. ¿Qué haces?", ["Centrifugar antes de 1 hora y mirar el sobrenadante", "Congelar la muestra", "Descartar el tubo 1 y no hacer nada más", "Añadir EDTA"], [None, "No sirve para decidir.", "Hay que confirmar.", "No aporta."]),
              ("El sobrenadante es transparente. ¿Conclusión?", ["Punción traumática", "Hemorragia subaracnoidea", "Meningitis bacteriana", "Xantocromía verdadera"], [None, "En la hemorragia la sangre es uniforme y el sobrenadante, xantocrómico.", "No hay datos de infección.", "Xantocromía = sobrenadante amarillo, rosa o naranja."])],
              "Punción traumática: la sangre se introdujo al pinchar.")],
          ["Si la sangre va disminuyendo del 1.<sup>er</sup> al 3.<sup>er</sup> tubo, se contaminó al pinchar.", "Centrifugar pronto evita que la lisis cree una falsa xantocromía.", "Sobrenadante claro + gradiente → traumática."],
          "Punción traumática", "Compara los tres tubos.")
    T.add(2, "Lee la analítica: LCR", "<p>Niño de 6 años con fiebre, rigidez de nuca y LCR turbio. Glucemia simultánea: 100 mg/dL.</p>",
          [lab("Valora cada parámetro.", "Niño · 6 años · LCR", [
              ("Aspecto", "Turbio", "", "Transparente", 1, "La turbidez aparece con ≥ 200 leucocitos/µL."), ("Glucosa", "18", "mg/dL", "40–80", -1), ("Proteínas", "220", "mg/dL", "15–45", 1),
              ("Lactato", "8,5", "mmol/L", "< 2,8", 1), ("Leucocitos", "1 800", "/µL", "0–5", 1), ("ADA", "4", "U/L", "< 10", 0)]),
           opt("¿Qué sugiere?", "Meningitis bacteriana (purulenta)", "Meningitis tuberculosa", "Punción traumática", "LCR normal", "Hemorragia subaracnoidea")],
          ["Glucosa muy baja (las bacterias la consumen), proteínas y lactato altos, muchos leucocitos.", "ADA normal: no orienta a tuberculosis."],
          "Meningitis bacteriana", "Glucosa baja + lactato alto.")
    T.add(2, "Cristales en el líquido sinovial", "<p>Varón de 55 años con dolor agudo en el dedo gordo del pie. Líquido sinovial con luz polarizada:</p>",
          [micro("Toca el cristal que confirma la sospecha clínica (gota).", [("cppd", -.35, -.3), ("msu", .3, -.2, 15), ("leu", -.3, .35), ("leu", .35, .4), ("cppd", .05, .45, 30)], ["1"], e="Son agujas finas."),
           opt("¿Y si fueran romboides cortos?", "Pirofosfato cálcico: pseudogota", "Urato monosódico: gota", "Colesterol", "Corticoides inyectados", "Apatita")],
          ["Urato monosódico: agujas, a menudo dentro de los neutrófilos durante el ataque → gota.", "Pirofosfato cálcico dihidratado: romboides o rectángulos cortos → pseudogota."],
          "Agujas = urato; romboides = pirofosfato", "Agujas o romboides.", chain=True)
    T.add(1, "Seminograma: nomenclatura", "<p>Nombra cada alteración (criterios de la OMS del material).</p>",
          [cls("Nomenclatura", ["Oligozoospermia", "Astenozoospermia", "Teratozoospermia", "Necrozoospermia", "Azoospermia", "Hipospermia"],
               [("Concentración de 8 millones/mL", 0), ("22 % de espermatozoides progresivos", 1), ("2 % de formas normales", 2), ("45 % de espermatozoides vivos", 3), ("Ausencia de espermatozoides en el eyaculado", 4), ("Volumen de 0,9 mL", 5)])],
          ["< 15 M/mL: oligo. < 32 % progresivos: asteno. < 4 % normales: terato.", "< 58 % vivos: necro. Sin espermatozoides: azoo. Volumen < 1,5 mL: hipospermia."],
          "Oligo · asteno · terato · necro · azoo · hipo", "Cada prefijo indica qué falla.")
    T.add(1, "Recuento total", "<p>Seminograma: volumen 3,2 mL; concentración 25 millones/mL.</p>",
          [num("Recuento total", ("Total", 80, "millones", 0.5)),
           opt("¿Es normal?", "Sí: ≥ 39 millones por eyaculado", "No: oligozoospermia", "No: hipospermia", "No: azoospermia", "No se puede saber")],
          ["Total = concentración × volumen = 25 × 3,2 = 80 millones.", "El mínimo de referencia es 39 millones por eyaculado."],
          "80 millones (normal)", "Concentración por volumen.")
    T.add(1, "Marcadores seminales", "<p>¿Qué glándula refleja cada marcador?</p>",
          [cls("Origen", ["Próstata", "Vesículas seminales", "Epidídimo"],
               [("Citrato", 0), ("Zinc", 0), ("Fosfatasa ácida", 0), ("Fructosa", 1, "La glucosa se transforma en fructosa en las vesículas (depende de la testosterona)."), ("L-carnitina", 2), ("α-1,4-glucosidasa neutra", 2)])],
          ["Próstata: citrato, zinc, fosfatasa ácida.", "Vesículas seminales: fructosa. Epidídimo: carnitina y α-glucosidasa neutra."],
          "P · P · P · VS · E · E", "La fructosa es el «combustible» de las vesículas.")
    T.add(1, "Hallazgos en las heces", "<p>¿Qué indica cada hallazgo microscópico?</p>",
          [cls("Indica", ["Insuficiencia pancreática", "Insuficiencia gástrica", "Malabsorción o insuficiencia biliar", "Parasitosis"],
               [("Muchas grasas neutras (rojas con Sudán III)", 0), ("Tejido conjuntivo sin digerir", 1), ("Ácidos grasos (agujas, no se tiñen)", 2), ("Cristales de Charcot-Leyden", 3), ("Células con almidón sin digerir", 0)])],
          ["Grasas neutras: falta lipasa pancreática. Tejido conjuntivo: falta digestión gástrica.", "Ácidos grasos: la grasa se digirió pero no se absorbió (biliar o malabsorción). Charcot-Leyden: parásitos."],
          "Panc · Gás · Bil · Par · Panc", "¿Qué enzima faltó?")
    T.add(2, "Microscopio: heces", "<p>Estudio microscópico de heces de un paciente con diarrea y eosinofilia.</p>",
          [micro("Toca el elemento que orienta a una parasitosis.", [("gras", -.35, -.3), ("fibm", .3, .3, 10), ("charc", .25, -.35, 25), ("gras", -.3, .4)], ["2"], e="Busca la «aguja de brújula»."),
           opt("¿Y las gotas rojo-naranja con Sudán III, si son muchas?", "Esteatorrea", "Creatorrea", "Amilorrea", "Melena", "Acolia")],
          ["Cristales de Charcot-Leyden: bipiramidales, como agujas de brújula → parásitos.", "Grasas neutras abundantes (> 60 gotas por campo a 40x) = esteatorrea."],
          "Charcot-Leyden; esteatorrea", "Bipiramidal y alargado.", chain=True)
    T.add(1, "Sangre oculta en heces", "<p>Cribado de cáncer colorrectal.</p>",
          [opt("¿Qué método se recomienda y por qué?", "Inmunoquímico: detecta globina humana (sin interferencia de la dieta)", "Guayaco: detecta el hemo de cualquier sangre", "Bencidina con dieta libre", "Test de ureasa", "Calprotectina fecal")],
          ["El inmunoquímico detecta globina humana: la carne de la dieta no da positivos.", "Además, la globina del tracto alto se degrada antes del colon: es más específico para el colon."],
          "Inmunoquímico", "¿Qué parte de la Hb detecta cada uno?")
    T.add(1, "¿Qué prueba pido?", "<p>Elige la prueba más adecuada.</p>",
          [cls("Prueba", ["Anti-transglutaminasa IgA", "Test del aliento con urea ¹³C", "Hidrógeno espirado", "Calprotectina fecal", "Elastasa fecal"],
               [("Sospecha de celiaquía (caso Álvaro)", 0), ("Úlcera y sospecha de <i>Helicobacter pylori</i>", 1), ("Diarrea con los lácteos", 2), ("Sospecha de enfermedad de Crohn", 3), ("Fibrosis quística con esteatorrea", 4)])],
          ["Celiaquía: tTGA-IgA (primera elección) y biopsia. <i>H. pylori</i>: su ureasa libera CO₂ marcado.", "Lactosa: las bacterias del colon la fermentan y producen H₂. EII: calprotectina. Páncreas exocrino: elastasa."],
          "tTGA · urea ¹³C · H₂ · calprotectina · elastasa", "¿Qué produce o consume cada proceso?")
    return T

def uf10():
    T = Topic("u10", "UF10 · Hormonas, marcadores tumorales, fármacos y embarazo", "horm")
    T.teo = ("<p><strong>Hormonas</strong>: se miden por inmunoanálisis (IRMA, ELISA, quimioluminiscencia); la HPLC es de elección para las catecolaminas y los esteroides. Su secreción es pulsátil y circadiana (cortisol y ACTH altos por la mañana): a veces hacen falta varias extracciones. "
             "La adenohipófisis secreta GH, ACTH, TSH, prolactina, FSH y LH; la neurohipófisis almacena ADH y oxitocina. El hipotálamo estimula (TRH, GnRH, CRH, GHRH) o inhibe (somatostatina, dopamina).</p>"
             "<p><strong>Tiroides</strong>: TSH 0,5–4 µU/mL; la TSH es la prueba más sensible. <b>TSH ↑ + T4L ↓ = hipotiroidismo primario</b> (Hashimoto, déficit de yodo); <b>TSH ↓ + T4L ↑ = hipertiroidismo primario</b> (Graves); TSH ↓ o normal + T4L ↓ = hipotiroidismo <b>central</b> (hipófisis o hipotálamo). "
             "Anticuerpos: anti-TPO y antitiroglobulina (Hashimoto), anti-receptor de TSH (Graves). Tiroglobulina y calcitonina como marcadores tumorales.</p>"
             "<p><strong>Otras</strong>: GH (IGF-1; test de supresión con 75 g de glucosa: GH &lt; 1 ng/mL descarta acromegalia), prolactina (curva de 3 extracciones; prolactinoma), <b>ACTH</b> (EDTA en hielo, centrífuga refrigerada), ADH (diabetes insípida central o nefrogénica; SIADH → hiponatremia), PTH (calcio). "
             "<b>Cortisol</b> (Cushing): cortisol salival nocturno a las 23:00, cortisol libre en orina de 24 h y <b>supresión con 1 mg de dexametasona</b> (23:00 → cortisol a las 8:00). Catecolaminas: metanefrinas (feocromocitoma). Hipogonadismo primario: LH/FSH ↑ y testosterona ↓ (Klinefelter); secundario: todo ↓.</p>"
             "<p><strong>Marcadores tumorales</strong>: <b>sensibilidad</b> = enfermos con resultado positivo (lo opuesto son los falsos negativos); <b>especificidad</b> = sanos con resultado negativo (lo opuesto son los falsos positivos). Sirven sobre todo para el <b>seguimiento</b> y las recidivas, no para el diagnóstico aislado. "
             "PSA (próstata), CEA (colorrectal), CA-125 (ovario), CA 15-3 (mama), CA 19-9 (páncreas), AFP (hígado, testículo), β-hCG (testículo, coriocarcinoma), calcitonina (carcinoma medular de tiroides), tiroglobulina, cromogranina A (neuroendocrinos).</p>"
             "<p><strong>Monitorización de fármacos</strong> (margen estrecho): fenitoína 5–15 µg/mL, carbamazepina 8–12, fenobarbital 20–40, valproico 50–100, <b>litio 0,6–1,5 mEq/L</b> (12 h tras la dosis), <b>digoxina 0,8–2 ng/mL</b>, ciclosporina 100–200 ng/mL, metotrexato a 24, 48 y 72 h. "
             "<strong>Drogas</strong>: cribado inmunoquímico en orina y <b>confirmación</b> por GC-MS o HPLC-MS; cadena de custodia en los casos forenses. Tóxicos: etanol (GC-FID), metanol (gap aniónico y osmolal), metales (absorción atómica), CO (cooximetría; COHb &gt; 3 % en no fumadores o &gt; 10 % en fumadores).</p>"
             "<p><strong>Embarazo</strong>: β-hCG en orina (≈ 20 mU/mL, ~10 días tras la fecundación); en seriado: sube menos de lo esperado → ectópico; más → gemelar o mola. Cribado del 1.<sup>er</sup> trimestre: <b>translucencia nucal + PAPP-A + β-hCG + edad</b>; 2.º trimestre: AFP, hCG, estriol e inhibina A. "
             "Cribado neonatal: sangre del talón en papel (hipotiroidismo congénito, fenilcetonuria, fibrosis quística, MCADD…).</p>")
    T.form = ["TSH ↑ T4L ↓ → hipo primario", "TSH ↓ T4L ↑ → hiper primario", "Sens = VP/(VP+FN) · Esp = VN/(VN+FP)", "Litio 0,6–1,5 mEq/L · digoxina 0,8–2 ng/mL", "COHb > 3 % (no fumador) confirma exposición", "Cribado 1T: TN + PAPP-A + β-hCG + edad"]
    T.lesson = ("<h3>Idea central</h3><p>Casos de <b>patrón hormonal</b> (¿primario o central?), de <b>niveles de fármacos</b> (¿en rango?) y de <b>cribado vs confirmación</b> (marcadores, drogas, Down).</p>"
                "<div class=\"ej\"><b>Regla del eje:</b> si falla la glándula periférica, la hormona hipofisaria <b>sube</b> (intenta estimularla). Si falla la hipófisis, <b>las dos bajan</b>.</div>"
                "<div class=\"err\"><b>Error común:</b> confundir una prueba de cribado con una diagnóstica. Un cribado positivo (marcadores, drogas, Down) siempre se confirma con otra técnica.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> (1) En el caso de Julia, TSH alta con T4 baja indica <b>hipotiroidismo primario</b>; en el hipopituitarismo la TSH estaría <b>baja</b>. Las demás hormonas bajas no encajan con esa TSH. (2) La digoxina es 0,8–2 <b>ng/mL</b> (no mg/mL). (3) La GnRH regula la <b>adenohipófisis</b> (no la neurohipófisis). (4) La TSH se expresa en µU/mL o mU/L.</div>")
    T.add(1, "Patrones tiroideos", "<p>Interpreta cada resultado.</p>",
          [cls("Diagnóstico", ["Hipotiroidismo primario", "Hipertiroidismo primario", "Hipotiroidismo central", "Hipotiroidismo subclínico"],
               [("TSH 12 µU/mL · T4L baja", 0), ("TSH 0,01 µU/mL · T4L alta", 1), ("TSH 0,3 µU/mL · T4L baja", 2, "Si la T4L es baja, la TSH debería subir: si no sube, falla la hipófisis o el hipotálamo."), ("TSH 7 µU/mL · T4L normal", 3), ("TSH alta · anticuerpos anti-TPO positivos · T4L baja", 0)])],
          ["Glándula tiroidea que falla → la TSH sube (primario).", "Tiroides hiperactiva → la TSH se suprime.", "TSH baja o inadecuadamente normal con T4L baja → central. TSH alta con T4L normal → subclínico."],
          "1.º · Hiper · Central · Subclínico · 1.º", "La TSH va en sentido contrario a la T4L si el eje funciona.")
    T.add(2, "Caso Julia (corregido)", "<p>Mujer de 35 años con aumento de peso, cansancio, intolerancia al frío y piel seca. <b>TSH alta, T3 y T4 bajas</b>.</p>",
          [tree("Razona el eje.", [
              ("T4 baja. ¿Qué hace la TSH si la hipófisis funciona?", ["Sube, para estimular el tiroides", "Baja", "No cambia"], [None, "Bajaría solo si la hipófisis fallara.", "La retroalimentación negativa la haría subir."]),
              ("La TSH está alta. ¿Dónde está el fallo?", ["En la glándula tiroides (primario)", "En la hipófisis (secundario)", "En el hipotálamo (terciario)"], [None, "Con fallo hipofisario, la TSH sería baja.", "Con fallo hipotalámico, la TRH y la TSH serían bajas."]),
              ("¿Qué prueba orienta a la causa más frecuente en zonas con yodo suficiente?", ["Anticuerpos anti-TPO (tiroiditis de Hashimoto)", "Anti-receptor de TSH", "Calcitonina", "IGF-1"], [None, "Son típicos de Graves (hipertiroidismo).", "Es un marcador del carcinoma medular.", "Es para la GH."])],
              "Hipotiroidismo primario (el solucionario del material dice hipopituitarismo, pero con TSH alta no encaja).")],
          ["Retroalimentación: la T4 baja estimula la secreción de TSH.", "TSH alta + T4 baja = el tiroides no responde: primario.", "En el mundo, la causa más frecuente es el déficit de yodo; si hay yodo suficiente, Hashimoto (anti-TPO)."],
          "Hipotiroidismo primario", "¿Qué haría la hipófisis si estuviera sana?")
    T.add(2, "Sensibilidad y especificidad", "<p>Un marcador se prueba en 100 pacientes con cáncer y 200 sin cáncer: 90 enfermos dan positivo; 30 sanos dan positivo.</p>",
          [num("Calcula", ("Sensibilidad", 90, "%", 0.2), ("Especificidad", 85, "%", 0.2), ("Falsos negativos", 10, None, 0.1))],
          ["Sensibilidad = VP/(VP + FN) = 90/100 = 90 %.", "Especificidad = VN/(VN + FP) = 170/200 = 85 %.", "FN = enfermos con resultado negativo = 100 − 90 = 10."],
          "90 % · 85 % · 10", "Sensibilidad: entre los enfermos; especificidad: entre los sanos.")
    T.add(1, "Marcadores tumorales", "<p>Relaciona cada marcador con su neoplasia principal.</p>",
          [cls("Neoplasia", ["Próstata", "Ovario", "Mama", "Páncreas", "Hígado / testículo", "Tiroides medular"],
               [("PSA", 0), ("CA-125", 1), ("CA 15-3", 2), ("CA 19-9", 3), ("Alfa-fetoproteína", 4), ("Calcitonina", 5)])],
          ["PSA próstata; CA-125 ovario; CA 15-3 mama; CA 19-9 páncreas y vías biliares.", "AFP: hepatocarcinoma y tumores germinales; calcitonina: carcinoma medular de tiroides (células C)."],
          "Pr · Ov · Ma · Pa · Hí/Te · TM", "Memoriza los seis más usados.")
    T.add(1, "Niveles de fármacos", "<p>¿El nivel está en rango terapéutico?</p>",
          [cls("Nivel", ["Por debajo", "En rango", "Por encima"],
               [("Litio 0,9 mEq/L", 1), ("Fenitoína 22 µg/mL", 2), ("Digoxina 0,5 ng/mL", 0), ("Ácido valproico 75 µg/mL", 1), ("Carbamazepina 6 µg/mL", 0), ("Ciclosporina 260 ng/mL", 2), ("Litio 2,3 mEq/L", 2, "Más de 2 mEq/L es una intoxicación grave (convulsiones, coma).")])],
          ["Litio 0,6–1,5; fenitoína 5–15; digoxina 0,8–2 ng/mL; valproico 50–100.", "Carbamazepina 8–12 (según el material); ciclosporina 100–200 ng/mL."],
          "R · ↑ · ↓ · R · ↓ · ↑ · ↑", "Repasa los rangos de la tabla.")
    T.add(1, "Cribado o confirmación", "<p>¿Qué papel tiene cada prueba?</p>",
          [cls("Papel", ["Cribado", "Confirmación / diagnóstico"],
               [("Test rápido inmunocromatográfico de drogas en orina", 0), ("Cromatografía de gases con espectrometría de masas (GC-MS)", 1), ("Cribado combinado del 1.<sup>er</sup> trimestre (TN + PAPP-A + β-hCG)", 0),
                ("Amniocentesis con cariotipo", 1), ("ADN fetal libre en sangre materna", 0, "Es un cribado no invasivo de alta sensibilidad; si sale positivo, se confirma con una prueba invasiva."), ("Prueba de embarazo en orina (POCT)", 0)])],
          ["Cribado: rápido, sensible, barato; un positivo no confirma (reacciones cruzadas).", "Confirmación: técnica distinta y específica (GC-MS, HPLC-MS, cariotipo)."],
          "Cr · Conf · Cr · Conf · Cr · Cr", "¿Da certeza o solo riesgo?")
    T.add(1, "hCG seriada", "<p>Embarazo de 5 semanas: la β-hCG sube, pero bastante menos de lo esperado en 48 h.</p>",
          [opt("¿Qué sospechas?", "Embarazo ectópico (o mala evolución)", "Embarazo gemelar", "Mola hidatiforme", "Embarazo normal", "Restos tras un aborto completo")],
          ["Aborto: no sube o baja. Ectópico: sube menos de lo esperado.", "Gemelar o enfermedad trofoblástica: sube más de lo esperado."],
          "Ectópico", "Compara con lo esperado.")
    T.add(1, "Hipogonadismo masculino", "<p>Varón de 20 años con testículos pequeños: testosterona baja, LH y FSH muy altas; cariotipo 47,XXY.</p>",
          [opt("Tipo", "Hipogonadismo primario (hipergonadotropo): síndrome de Klinefelter", "Hipogonadismo secundario (hipogonadotropo)", "Síndrome de Kallmann", "Hiperprolactinemia", "Hipertiroidismo")],
          ["El testículo falla → baja la testosterona → la hipófisis sube LH y FSH (primario, hipergonadotropo).", "En el secundario (Kallmann) LH, FSH y testosterona están bajas."],
          "Primario (Klinefelter)", "LH y FSH altas = el fallo es periférico.")
    T.add(1, "Estudio del cortisol", "<p>Sospecha de síndrome de Cushing.</p>",
          [opt("¿Cómo se hace la supresión rápida con dexametasona?", "1 mg de dexametasona a las 23:00 y cortisol sérico a las 8:00", "1 mg a las 8:00 y cortisol a las 23:00", "Cortisol a cualquier hora sin preparación", "75 g de glucosa y GH a las 2 h", "TRH intravenosa y TSH a los 30 min"),
           opt("¿Y la muestra de cortisol salival?", "Saliva a las 23:00, dos días seguidos, sin comer ni fumar 2 h antes", "Saliva en ayunas a las 8:00", "Orina de primera hora", "Sangre con EDTA en hielo", "Saliva tras cepillarse con pasta")],
          ["En una persona sana la dexametasona suprime la ACTH y el cortisol de la mañana baja; en el Cushing no se suprime.", "El cortisol nocturno debería ser mínimo; en el Cushing se pierde ese descenso."],
          "Dexametasona 23:00 → cortisol 8:00; saliva a las 23:00", "El cortisol normal baja por la noche.")
    T.add(1, "Intoxicación por monóxido de carbono", "<p>Familia con cefalea en una casa con calentador de gas. Una persona no fumadora tiene COHb del 18 %.</p>",
          [opt("¿Qué significa y cómo se midió?", "Confirma la exposición (> 3 % en no fumadores); se mide por cooximetría", "Es normal en invierno", "Solo es significativo por encima del 50 %", "Se mide con un pulsioxímetro convencional", "Indica metahemoglobinemia")],
          ["COHb > 3 % en no fumadores (> 10 % en fumadores) confirma la exposición.", "El CO tiene ~240 veces más afinidad por la Hb que el O₂; la cooximetría mide las fracciones con varias λ (un pulsioxímetro normal confunde COHb con O₂Hb)."],
          "Exposición confirmada · cooximetría", "El pulsioxímetro normal no distingue la COHb.")
    return T
