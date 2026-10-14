from bq_lib import *

def uf4():
    T = Topic("u4", "UF4 · Proteínas, lípidos y dislipemias", "lip")
    T.teo = ("<p><strong>Proteínas plasmáticas</strong> (6–8 g/dL): tampón, presión oncótica, transporte, defensa, coagulación. <b>Hipoproteinemia</b> (&lt; 6 g/dL): síndrome nefrótico, hemorragias, quemaduras, desnutrición, hepatopatía. <b>Hiperproteinemia</b>: deshidratación o paraproteinemia. "
             "Proteínas totales en <b>suero</b>: <b>Biuret</b> (Cu²⁺ + enlaces peptídicos en medio alcalino → violeta, 540 nm; 6,4–8,3 g/dL; la hemólisis interfiere), refractometría (sueros claros) y <b>Lowry</b> (Biuret + Folin, más sensible).</p>"
             "<p><strong>Proteinograma</strong> (electroforesis, de más a menos movilidad hacia el ánodo): <b>albúmina</b> (~55 %, 3,5–5,2 g/dL), <b>α1</b> (α1-antitripsina, orosomucoide, HDL), <b>α2</b> (α2-macroglobulina, haptoglobina, ceruloplasmina), "
             "<b>β</b> (transferrina, LDL, C3, hemopexina) y <b>γ</b> (inmunoglobulinas). Un pico estrecho en γ = <b>componente monoclonal</b> (mieloma, Waldenström); en orina, <b>Bence-Jones</b> (cadenas ligeras; precipitan a 45–60 °C y se redisuelven). "
             "Crioglobulinas: precipitan en frío (incubar a 37 °C y luego a 4 °C).</p>"
             "<p><strong>Lípidos</strong>: saponificables (triglicéridos, fosfolípidos) e insaponificables (colesterol, esteroides). Se transportan en <b>lipoproteínas</b>: quilomicrones (TG de la dieta; capa cremosa; quedan en el origen), "
             "<b>VLDL</b> (TG endógenos; pre-β; suero turbio), <b>LDL</b> (colesterol a los tejidos; β; aterogénica), <b>HDL</b> (colesterol de vuelta al hígado; α; protectora). Apo AI → HDL; apo B → LDL; apo CII activa la lipoproteinlipasa.</p>"
             "<p><strong>Metabolismo</strong>: lipogénesis (acetil-CoA → TG, la favorece la insulina), lipólisis (TG → glicerol + ácidos grasos), β-oxidación (ácidos grasos → acetil-CoA → Krebs). Si el Krebs se satura (ayuno, diabetes sin insulina) → <b>cuerpos cetónicos</b>.</p>"
             "<p><strong>Perfil lipídico</strong>: colesterol total (<b>CHOD-POD</b>, &lt; 200 mg/dL), TG (<b>GPO</b>, &lt; 150 mg/dL), HDL (precipitar las lipoproteínas con apo B y medir el sobrenadante, o método directo; &gt; 40 mg/dL en mujeres, &gt; 35 en hombres según el material) y LDL calculado con <b>Friedewald</b>: <b>LDL = CT − (TG/5 + HDL)</b>, solo si TG &lt; 400 mg/dL. "
             "También: VLDL = TG/5; no-HDL = CT − HDL; índice CT/HDL. <strong>Dislipemias</strong>: primarias (clasificación de Fredrickson por el aspecto del suero refrigerado) y secundarias (diabetes, nefrótico, hipotiroidismo, alcohol).</p>")
    T.form = ["LDL = CT − (TG/5 + HDL) (TG < 400)", "VLDL = TG/5 · no-HDL = CT − HDL", "CT < 200 · TG < 150 mg/dL", "Proteínas totales 6–8 g/dL · albúmina 3,5–5,2", "Electroforesis: Alb > α1 > α2 > β > γ", "Lipidograma: HDL (α) > VLDL (pre-β) > LDL (β) > QM (origen)"]
    T.lesson = ("<h3>Idea central</h3><p>Dos cosas que siempre caen: <b>leer un proteinograma o un perfil lipídico</b> y <b>calcular el LDL</b> con Friedewald (comprobando antes que los TG son &lt; 400).</p>"
                "<div class=\"ej\"><b>Caso Elisa:</b> CT 170, TG 130, HDL 70 → LDL = 170 − (26 + 70) = <b>74 mg/dL</b>.</div>"
                "<div class=\"err\"><b>Error común:</b> aplicar Friedewald con TG = 450 mg/dL. Por encima de 400 se mide el LDL directo.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> en el texto sobre el HDL dice «cálculo del colesterol HDL» donde debería decir LDL. Y en el lipidograma, el orden de migración hacia el ánodo es HDL > VLDL > LDL.</div>")
    T.add(1, "Proteinograma normal", "<p>Proteinograma por electroforesis capilar.</p>",
          [tap("Toca la banda de la <b>albúmina</b>.", "prot", "alb"), tap("Toca la fracción de las <b>inmunoglobulinas</b>.", "prot", "g")],
          ["La albúmina es la más abundante (~55 %) y la que más migra hacia el ánodo.", "Las inmunoglobulinas están en la fracción γ, la más lenta (cerca del cátodo)."],
          "Albúmina: primer pico; Ig: fracción γ", "Ánodo a la izquierda.", chain=True)
    T.add(2, "Componente monoclonal", "<p>Paciente de 68 años con dolores óseos y proteínas totales de 9,6 g/dL.</p>",
          [tap("Toca la alteración.", "protm", "g", e="Fíjate en el pico estrecho y alto."),
           opt("¿Qué sugiere?", "Gammapatía monoclonal (p. ej., mieloma múltiple)", "Síndrome nefrótico", "Inflamación aguda (α1 y α2 altas)", "Hipogammaglobulinemia", "Deshidratación simple")],
          ["Un pico estrecho y homogéneo en γ = proliferación de un solo clon de linfocitos B.", "Con hiperproteinemia y dolor óseo → mieloma; buscar Bence-Jones en orina."],
          "Pico monoclonal en γ → mieloma", "Policlonal = ancho; monoclonal = estrecho.", chain=True)
    T.add(1, "Proteínas en cada fracción", "<p>Ubica cada proteína en su fracción.</p>",
          [cls("Fracción", ["α1", "α2", "β", "γ"],
               [("α1-antitripsina", 0), ("Haptoglobina", 1), ("Ceruloplasmina", 1), ("Transferrina", 2), ("Inmunoglobulina G", 3), ("α2-macroglobulina", 1), ("C3 del complemento", 2), ("HDL (α1-lipoproteína)", 0)])],
          ["α1: α1-antitripsina, orosomucoide, HDL. α2: α2-macroglobulina, haptoglobina, ceruloplasmina.", "β: transferrina, LDL, C3, hemopexina. γ: inmunoglobulinas."],
          "α1 · α2 · α2 · β · γ · α2 · β · α1", "La haptoglobina y la ceruloplasmina van juntas.")
    T.add(1, "Friedewald (caso Elisa)", "<p>Perfil lipídico: CT = 170, TG = 130, HDL = 70 mg/dL.</p>",
          [num("LDL calculado", ("LDL", 74, "mg/dL", 0.5))],
          ["TG = 130 < 400 → se puede aplicar Friedewald.", "LDL = 170 − (130/5 + 70) = 170 − 96 = 74 mg/dL."],
          "74 mg/dL", "Primero divide los TG entre 5.")
    T.add(2, "Perfil lipídico completo", "<p>Varón: CT = 240, TG = 200, HDL = 45 mg/dL.</p>",
          [num("Calcula", ("VLDL (colesterol)", 40, "mg/dL", 0.5), ("LDL", 155, "mg/dL", 0.5), ("No-HDL", 195, "mg/dL", 0.5), ("Índice CT/HDL", 5.33, None, 0.02))],
          ["VLDL = TG/5 = 40.", "LDL = 240 − (40 + 45) = 155.", "No-HDL = 240 − 45 = 195. CT/HDL = 240/45 = 5,33."],
          "40 · 155 · 195 · 5,33", "Todo sale de CT, TG y HDL.")
    T.add(1, "¿Se puede usar Friedewald?", "<p>Perfil: CT = 280, TG = 520, HDL = 38 mg/dL.</p>",
          [opt("¿Qué haces?", "No aplicar Friedewald (TG > 400): medir el LDL directo", "LDL = 280 − (104 + 38) = 138", "Repetir sin ayuno", "Calcular LDL = CT − HDL", "Dividir los TG entre 2,2")],
          ["Friedewald asume una relación fija TG/colesterol en las VLDL; con TG > 400 el error es grande.", "Se usa el reactivo de LDL directo (sin pretratamiento ni centrifugación)."],
          "LDL directo", "Mira el límite de los TG.")
    T.add(2, "Lee la analítica: perfil lipídico", "<p>Mujer de 50 años, revisión anual, en ayunas.</p>",
          [lab("Valora cada parámetro.", "Mujer · 50 años · ayunas", [
              ("Colesterol total", "262", "mg/dL", "< 200", 1), ("Triglicéridos", "140", "mg/dL", "< 150", 0), ("Colesterol HDL", "38", "mg/dL", "> 40 (mujer)", -1, "En la mujer se considera bajo por debajo de 40 mg/dL."),
              ("Colesterol LDL (Friedewald)", "196", "mg/dL", "< 130", 1, "LDL = 262 − (28 + 38) = 196."), ("Glucosa", "92", "mg/dL", "70–100", 0)]),
           opt("¿Qué tipo de Fredrickson encaja (suero claro)?", "IIa: colesterol y LDL altos, TG normales", "I: exceso de quilomicrones", "IV: VLDL alta, suero turbio", "V: quilomicrones y VLDL", "IIb: colesterol y TG altos")],
          ["CT y LDL altos con TG normales y HDL bajo: mayor riesgo aterógeno.", "Colesterol alto con TG normales y suero claro → tipo IIa (LDL)."],
          "Hipercolesterolemia tipo IIa", "Compara con la Tabla 5 de Fredrickson.")
    T.add(1, "Aspecto del suero (Fredrickson)", "<p>Sueros en ayunas tras 12 h en nevera a 4 °C.</p>",
          [cls("Tipo", ["I", "IIa", "IV", "V"],
               [("Capa cremosa arriba y el resto claro", 0), ("Suero claro con colesterol alto", 1), ("Suero turbio sin capa cremosa (VLDL alta)", 2), ("Capa cremosa arriba y el resto turbio", 3, "Quilomicrones (capa) + VLDL (turbidez)."), ("Exceso de quilomicrones con colesterol normal", 0)])],
          ["Capa cremosa = quilomicrones (flotan). Turbidez = VLDL.", "I: solo QM. IV: solo VLDL. V: ambos. IIa: LDL, suero claro."],
          "I · IIa · IV · V · I", "Capa = quilomicrones; turbio = VLDL.")
    T.add(1, "Lipidograma", "<p>Electroforesis de lipoproteínas en agarosa (pH 8,6).</p>",
          [tap("Toca la banda de las <b>LDL</b>.", "lipid", "ldl", e="Las LDL migran con las β-globulinas."), tap("Toca dónde quedan los <b>quilomicrones</b>.", "lipid", "qm")],
          ["Hacia el ánodo migran HDL (α) > VLDL (pre-β) > LDL (β).", "Los quilomicrones no migran: se quedan en el punto de aplicación."],
          "LDL: banda β; QM: origen", "Las HDL son las que más corren.", chain=True)
    T.add(1, "Colesterol total (CHOD-POD)", "<p>Ordena las reacciones.</p>",
          [order("Orden", ["La colesterol esterasa hidroliza los ésteres de colesterol", "La colesterol oxidasa oxida el colesterol libre y forma H₂O₂", "La peroxidasa usa el H₂O₂ con 4-aminofenazona y forma una quinona coloreada", "Se lee la absorbancia a ~546 nm"])],
          ["Primero hay que liberar el colesterol esterificado.", "El H₂O₂ se acopla a un cromógeno: igual idea que en la glucosa (GOD-POD)."],
          "Esterasa → oxidasa → peroxidasa → 546 nm", "Se parece al método de la glucosa.")
    T.add(1, "Proteínas totales (caso de nefropatía)", "<p>Paciente con insuficiencia renal crónica y edemas: proteínas totales y albúmina bajas.</p>",
          [opt("¿Qué método y qué muestra?", "Biuret en suero (violeta, 540 nm)", "Biuret en plasma con EDTA a 340 nm", "Benedict en orina", "Jaffé en suero", "Nitroprusiato en sangre total"),
           opt("¿Qué prueba confirma la pérdida renal de proteínas?", "Proteinuria de orina de 24 horas", "Proteinograma en LCR", "Glucemia en ayunas", "HbA1c", "Lipidograma")],
          ["Biuret: los enlaces peptídicos forman un complejo violeta con el Cu²⁺ en medio alcalino.", "La pérdida se confirma cuantificando la proteína en orina de 24 h."],
          "Biuret en suero; proteinuria de 24 h", "¿Qué reacciona con el cobre?")
    return T

def uf5():
    T = Topic("u5", "UF5 · Productos finales del metabolismo", "renal")
    T.teo = ("<p><strong>Urea</strong>: se forma en el hígado (ciclo de la urea) con el NH₃ de los aminoácidos. Junto con la creatinina evalúa la función renal. Aumento prerrenal (deshidratación, insuficiencia cardiaca, hemorragia), renal (glomerulonefritis, necrosis tubular) o posrenal (obstrucción: cálculos, tumores). "
             "Método de la <b>ureasa</b> (urea → 2 NH₄⁺ + HCO₃⁻) acoplado a la <b>GLDH</b> (desaparición de NADH a 340 nm). <b>Urea = BUN × 2,14</b> (60/28).</p>"
             "<p><strong>Creatinina</strong>: viene de la creatina muscular; depende de la masa muscular, no de la dieta. Método de <b>Jaffé</b> (picrato alcalino, color rojizo; el modificado lee entre 20 y 80 s) o enzimático. "
             "<b>Aclaramiento</b>: <b>Cl = U<sub>cr</sub> × V / (P<sub>cr</sub> × 1 440)</b> (mL/min, con V en mL de orina de 24 h). La creatinina sérica solo sube cuando el filtrado ya bajó un 50 %. Estadios de la ERC: ≥ 90 · 60–89 · 30–59 · 15–29 · &lt; 15 mL/min.</p>"
             "<p><strong>Amonio</strong>: tóxico cerebral. Muestra de plasma con EDTA, <b>en hielo</b>, sin hemólisis, con torniquete mínimo, sin fumar ni hacer ejercicio. Método GLDH (NADPH a 340 nm).</p>"
             "<p><strong>Ácido úrico</strong>: fin del catabolismo de las purinas (xantina oxidasa). Hiperuricemia &gt; 6,8 mg/dL (H) o &gt; 6 mg/dL (M); gota (cristales de urato en las articulaciones, tofos), cálculos en orina ácida. Método de la <b>uricasa</b>. El <b>alopurinol</b> inhibe la xantina oxidasa.</p>"
             "<p><strong>Lactato</strong>: hipoxia tisular (fermentación láctica). Acidosis láctica tipo A (hipoxia: shock, IAM) o B (metabólica: diabetes, tóxicos, sepsis). &gt; 5 mmol/L = mal pronóstico. Muestra en reposo, sin torniquete, en frío y separada en &lt; 15 min. "
             "Cociente lactato/piruvato normal ≈ <b>10:1</b>.</p>"
             "<p><strong>Bilirrubina</strong>: hemo → biliverdina → bilirrubina <b>no conjugada (indirecta)</b>, unida a la albúmina → el hígado la <b>conjuga</b> (directa, hidrosoluble) → intestino → urobilinógeno → estercobilina (heces) y urobilina (orina). "
             "Ictericia si &gt; 2 mg/dL. Predomina la <b>indirecta</b>: hemólisis, Gilbert, ictericia neonatal (fototerapia). Predomina la <b>directa</b> (&gt; 20 %): colestasis/obstrucción → <b>coluria</b> y heces claras. Método de Jendrassik-Grof: directa sin acelerador; total con cafeína; indirecta = total − directa.</p>"
             "<p><strong>Cuerpos cetónicos</strong> (acetoacetato, β-hidroxibutirato, acetona): ayuno o diabetes sin insulina. La tira de <b>nitroprusiato</b> detecta acetoacetato y acetona, no el β-hidroxibutirato.</p>")
    T.form = ["Cl creat = Ucr·V / (Pcr·1440) [mL/min]", "Urea = BUN × 2,14", "B. indirecta = total − directa", "Lactato/piruvato ≈ 10:1", "Ácido úrico > 6,8 (H) · > 6 (M) mg/dL", "ERC: ≥90 · 60–89 · 30–59 · 15–29 · <15"]
    T.lesson = ("<h3>Idea central</h3><p>Casos de <b>función renal</b> (urea, creatinina, aclaramiento) y de <b>ictericia</b> (qué fracción de la bilirrubina sube). Además, en la práctica importan mucho las <b>condiciones de la muestra</b> (amonio y lactato en frío).</p>"
                "<div class=\"ej\"><b>Ictericia:</b> sube la indirecta → el problema está antes del hígado o en la conjugación (hemólisis, Gilbert, neonatos). Sube la directa → el problema está en la excreción (obstrucción) y aparece coluria.</div>"
                "<div class=\"err\"><b>Error común:</b> pensar que una creatinina normal descarta la insuficiencia renal. Hace falta perder ~50 % del filtrado para que suba: por eso se calcula el aclaramiento.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> (1) urea = BUN × <b>2,14</b> (60/28), no × 2,4. (2) El cociente lactato/piruvato normal es ≈ <b>10:1</b> (lactato 10 veces mayor), no 0,1, y en la acidosis láctica por hipoxia el cociente <b>sube</b>. (3) El lactato no forma «cristales» ni causa las agujetas. (4) El cerebro <b>sí</b> usa cuerpos cetónicos en el ayuno prolongado (los recibe del hígado; no los fabrica él).</div>")
    T.add(2, "Aclaramiento de creatinina", "<p>Orina de 24 h: volumen 1 500 mL; creatinina en orina 120 mg/dL; creatinina sérica 1,2 mg/dL.</p>",
          [num("Aclaramiento", ("Cl", 104.2, "mL/min", 0.6)),
           opt("¿En qué estadio de ERC lo situarías si hubiera lesión renal?", "Estadio 1 (≥ 90 mL/min)", "Estadio 2 (60–89)", "Estadio 3 (30–59)", "Estadio 4 (15–29)", "Estadio 5 (< 15)")],
          ["Cl = U × V / (P × 1 440) = 120 × 1 500 / (1,2 × 1 440).", "= 180 000 / 1 728 = 104,2 mL/min.", "≥ 90 mL/min: filtrado normal (estadio 1 si hay lesión renal)."],
          "104,2 mL/min · estadio 1", "1 440 son los minutos de un día.")
    T.add(1, "Causas de urea alta", "<p>Clasifica cada causa de aumento de la urea.</p>",
          [cls("Tipo", ["Prerrenal", "Renal", "Posrenal"],
               [("Deshidratación por vómitos", 0), ("Glomerulonefritis crónica", 1), ("Cálculo que obstruye el uréter", 2), ("Insuficiencia cardiaca", 0), ("Necrosis tubular", 1), ("Tumor de próstata que obstruye la uretra", 2), ("Hemorragia importante", 0)])],
          ["Prerrenal: llega poca sangre al riñón. Renal: el riñón no filtra bien.", "Posrenal: filtra bien, pero la orina no puede salir."],
          "Pre · R · Post · Pre · R · Post · Pre", "¿Antes, dentro o después del riñón?")
    T.add(1, "Del BUN a la urea", "<p>El informe trae BUN = 20 mg/dL.</p>",
          [num("Urea", ("Urea", 42.8, "mg/dL", 0.3))],
          ["La urea (PM 60) tiene 2 N (28): urea = BUN × 60/28 = BUN × 2,14.", "20 × 2,14 = 42,8 mg/dL (el material dice 2,4: es un error)."],
          "42,8 mg/dL", "60/28.")
    T.add(2, "Ictericia: ¿dónde está el problema?", "<p>Varón de 25 años con ictericia leve. Bilirrubina total 4,5 mg/dL; directa 0,4 mg/dL. Orina de color normal.</p>",
          [tree("Recorre el razonamiento.", [
              ("¿Qué fracción predomina?", ["La no conjugada (indirecta): 4,1 de 4,5", "La conjugada (directa)", "Las dos por igual", "No se puede saber"], [None, "La directa es solo 0,4 (< 20 % del total).", "La directa es apenas un 9 %.", "Indirecta = total − directa."]),
              ("¿Por qué no hay coluria?", ["La bilirrubina no conjugada no es hidrosoluble y no pasa a la orina", "Porque el riñón está dañado", "Porque es muy alta", "Por error del laboratorio"], [None, "No hay datos de daño renal.", "Aun alta, sin conjugar no se filtra.", "Es lo esperable."]),
              ("¿Qué causas encajan?", ["Hemólisis o déficit de conjugación (p. ej., Gilbert)", "Cálculo en el colédoco", "Cáncer de cabeza de páncreas", "Colestasis intrahepática"], [None, "La obstrucción eleva la directa y da coluria.", "Es obstructiva: sube la directa.", "La colestasis eleva la directa."])],
              "Hiperbilirrubinemia no conjugada (prehepática o de conjugación).")],
          ["Indirecta = 4,5 − 0,4 = 4,1 mg/dL: predomina claramente.", "La no conjugada viaja unida a la albúmina y no se filtra: no hay coluria.", "Causas: hemólisis, Gilbert, Crigler-Najjar, ictericia neonatal."],
          "Ictericia no conjugada", "Calcula la indirecta primero.")
    T.add(2, "Lee la analítica: ictericia obstructiva", "<p>Mujer de 58 años con ictericia, orina oscura y heces claras.</p>",
          [lab("Valora cada parámetro.", "Mujer · 58 años", [
              ("Bilirrubina total", "8,2", "mg/dL", "0,2–1,2", 1), ("Bilirrubina directa", "6,9", "mg/dL", "< 0,3", 1), ("Fosfatasa alcalina", "540", "U/L", "40–130", 1),
              ("γ-GT", "410", "U/L", "7–35", 1), ("ALT (GPT)", "28", "U/L", "≤ 34", 0), ("Urobilinógeno en orina", "Negativo", "", "Trazas (≤ 1 mg/dL)", -1, "Si la bilis no llega al intestino, no se forma urobilinógeno.")]),
           opt("¿Qué tipo de ictericia es?", "Obstructiva/colestásica: predomina la directa, con ALP y GGT altas", "Hemolítica", "Hepatitis aguda", "Síndrome de Gilbert", "Ictericia neonatal fisiológica")],
          ["La directa es el 84 % del total → hiperbilirrubinemia conjugada (colestasis).", "ALP y GGT altas = patrón colestásico; ALT normal = sin gran lisis de hepatocitos.", "Sin bilis en el intestino no hay urobilinógeno; heces claras (acolia) y coluria."],
          "Ictericia obstructiva", "¿Llega la bilis al intestino?")
    T.add(1, "Metabolismo de la bilirrubina", "<p>Ordena el recorrido.</p>",
          [order("Orden", ["Hemoglobina de hematíes viejos (bazo, SRE)", "Grupo hemo → biliverdina", "Bilirrubina no conjugada unida a la albúmina", "Conjugación con ácido glucurónico en el hepatocito", "Bilirrubina conjugada a la bilis y al intestino", "Urobilinógeno → estercobilina (heces) y urobilina (orina)"])],
          ["La biliverdina reductasa forma la bilirrubina no conjugada (apolar: necesita la albúmina).", "El hígado la conjuga (hidrosoluble) y la excreta; la microbiota forma el urobilinógeno."],
          "Hb → biliverdina → BNC-albúmina → conjugación → bilis → urobilinógeno", "Sigue el camino del glóbulo rojo al intestino.")
    T.add(1, "Muestra para amonio", "<p>¿Qué debes hacer al extraer y procesar una muestra de amonio?</p>",
          [cls("Clasifica", ["Hacer", "Evitar"],
               [("Meter el tubo en hielo enseguida", 0), ("Usar plasma con EDTA", 0), ("Torniquete largo y abrir y cerrar el puño", 1, "Falsea al alza el amonio."), ("Muestra hemolizada", 1, "Los hematíes tienen unas 3 veces más amonio que el plasma."),
                ("Que el paciente fume antes de la extracción", 1), ("Centrifugar (mejor refrigerada) y mantener el tubo tapado", 0), ("Extraer justo después de hacer ejercicio", 1)])],
          ["El amonio aumenta in vitro (~0,017 µg/mL/min a 25 °C): hielo y procesado rápido.", "Hemólisis, tabaco, ejercicio y torniquete prolongado lo suben falsamente."],
          "H · H · E · E · E · H · E", "Todo lo que lo suba falsamente se evita.")
    T.add(2, "Alopurinol y cálculos de xantina", "<p>Solubilidad en orina: ácido úrico 0,15 g/L; xantina 0,05 g/L; hipoxantina 1,4 g/L.</p>",
          [opt("¿Por qué el alopurinol puede dar cálculos de xantina, pero menos daño renal que la gota sin tratar?", "Inhibe la xantina oxidasa: se acumulan hipoxantina (muy soluble, se elimina) y algo de xantina (poco soluble)", "Aumenta la síntesis de ácido úrico", "Inhibe la uricasa humana", "Acidifica la orina", "Bloquea la reabsorción de calcio")],
          ["La xantina oxidasa convierte hipoxantina → xantina → ácido úrico.", "Al inhibirla, sube sobre todo la hipoxantina (muy soluble) y en menor medida la xantina (menos soluble que el úrico): pueden formarse cálculos de xantina, pero el daño global es menor."],
          "Inhibe la xantina oxidasa", "Mira las tres solubilidades.")
    T.add(1, "Acidosis láctica", "<p>Clasifica cada causa.</p>",
          [cls("Tipo", ["Tipo A (hipoxia)", "Tipo B (metabólica)"],
               [("Shock hemorrágico", 0), ("Infarto de miocardio", 0), ("Intoxicación por metanol", 1), ("Diabetes mellitus descompensada", 1), ("Edema pulmonar grave", 0), ("Leucemia", 1)])],
          ["Tipo A: falta de oxígeno en los tejidos (shock, IAM, insuficiencia cardiaca, edema pulmonar).", "Tipo B: origen metabólico (diabetes, sepsis, leucemia, hepatopatía, tóxicos)."],
          "A · A · B · B · A · B", "¿Falta oxígeno?")
    T.add(1, "Cociente lactato/piruvato", "<p>En condiciones normales, el lactato es ~1 mmol/L y el piruvato, ~0,1 mmol/L.</p>",
          [num("Cociente lactato/piruvato normal", ("L/P", 10, None, 0.5)),
           opt("En una acidosis láctica por hipoxia, el cociente…", "Aumenta (sobra NADH y el piruvato pasa a lactato)", "Baja a menos de 0,1", "No cambia nunca", "Se hace cero", "Solo cambia en la diabetes")],
          ["1/0,1 = 10: el lactato es unas 10 veces el piruvato (el material escribe 0,1, que sería piruvato/lactato).", "Con hipoxia se acumula NADH y el piruvato se reduce a lactato: el cociente sube."],
          "≈ 10; aumenta", "Divide lactato entre piruvato.")
    T.add(1, "Cuerpos cetónicos en tira", "<p>Paciente en cetoacidosis: la tira de cetonas sale solo «trazas», aunque el β-hidroxibutirato en sangre es muy alto.</p>",
          [opt("¿Por qué?", "El nitroprusiato detecta acetoacetato y acetona, no β-hidroxibutirato", "La tira detecta solo glucosa", "Los cuerpos cetónicos no pasan nunca a la orina", "El nitroprusiato solo reacciona a pH ácido", "Por exceso de ácido ascórbico")],
          ["La reacción de Legal (nitroprusiato) es específica de acetoacetato y acetona.", "En la cetoacidosis predomina el β-hidroxibutirato: se mide en sangre con medidores específicos o con la β-HBD."],
          "El nitroprusiato no detecta el β-HB", "¿Qué cetona falta?")
    T.add(1, "Bilirrubina indirecta", "<p>Jendrassik-Grof: bilirrubina total 3,2 mg/dL; directa 0,5 mg/dL.</p>",
          [num("Indirecta", ("B. indirecta", 2.7, "mg/dL", 0.05)),
           opt("¿Para qué se añade cafeína?", "Para solubilizar la no conjugada y medir la total", "Para medir solo la directa", "Para inhibir la reacción", "Para conservar la muestra", "Para eliminar la hemoglobina")],
          ["Indirecta = 3,2 − 0,5 = 2,7 mg/dL.", "Sin acelerador reacciona solo la directa; con cafeína reaccionan ambas (total)."],
          "2,7 mg/dL; la cafeína mide la total", "Total − directa.")
    return T

def uf6():
    T = Topic("u6", "UF6 · Enzimas: cinética, isoenzimas y patrones de alteración", "enz")
    T.teo = ("<p>Las <strong>enzimas</strong> son proteínas que catalizan reacciones bajando la energía de activación, sin consumirse. Centro activo (sustrato) y centro alostérico (reguladores); modelos de llave-cerradura y ajuste inducido. "
             "Clases EC: <b>1</b> oxidorreductasas (LDH, GOD), <b>2</b> transferasas (AST, ALT, CK, GGT), <b>3</b> hidrolasas (ALP, ACP, amilasa, lipasa, ChE), <b>4</b> liasas (aldolasa), <b>5</b> isomerasas, <b>6</b> ligasas.</p>"
             "<p><strong>Michaelis-Menten</strong>: v = V<sub>máx</sub>·[S]/(K<sub>m</sub> + [S]). <b>K<sub>m</sub></b> = [S] con la que v = V<sub>máx</sub>/2; <b>menor K<sub>m</sub> = mayor afinidad</b>. Con [S] baja: primer orden; con [S] saturante: orden cero (v solo depende de la enzima) → en el laboratorio se trabaja con <b>sustrato en exceso</b>. Influyen pH, T, cofactores e inhibidores.</p>"
             "<p><strong>Lineweaver-Burk</strong> (1/v frente a 1/[S]): corte en Y = 1/V<sub>máx</sub>; corte en X = −1/K<sub>m</sub>. "
             "Inhibición <b>competitiva</b>: K<sub>m</sub> ↑, V<sub>máx</sub> igual (las rectas se cortan en el eje Y; se revierte con más sustrato). <b>No competitiva</b>: V<sub>máx</sub> ↓, K<sub>m</sub> igual (se cortan en el eje X). <b>Acompetitiva</b>: bajan las dos (rectas paralelas).</p>"
             "<p><strong>Actividad</strong>: 1 U = 1 µmol/min; 1 katal = 1 mol/s; <b>1 U = 16,67 nkat</b>. Métodos a punto final o cinéticos (ΔA/min × factor). NAD(P)H absorbe a <b>340 nm</b> (NAD⁺ no).</p>"
             "<p><strong>Isoenzimas</strong>: CK-MM (músculo esquelético), <b>CK-MB (corazón)</b>, CK-BB (cerebro). LDH1-2 (corazón, hematíes), LDH4-5 (hígado, músculo). ALP: ósea (termolábil), hepática, placentaria (termorresistente). Amilasa P (páncreas) y S (saliva). Fosfatasa ácida prostática (inhibición con tartrato).</p>"
             "<p><strong>Patrones</strong>: hepatitis aguda → ALT ≫ (ALT/AST &gt; 1); crónica, cirrosis o alcohol → AST &gt; ALT; colestasis → GGT y ALP; alcoholismo → GGT; insuficiencia hepática → baja la colinesterasa. "
             "Pancreatitis → <b>lipasa</b> (más específica) y amilasa. IAM → CK-MB y troponinas precoces (3–6 h), AST (pico 48 h), LDH tardía (pico al 3.<sup>er</sup> día, normal a los 10–14 días). La <b>hemólisis</b> da falsos positivos (CK por adenilato quinasa, LDH, ACP, ALP).</p>")
    T.form = ["v = Vmáx·[S] / (Km + [S])", "1/v = (Km/Vmáx)·1/[S] + 1/Vmáx", "1 U = 1 µmol/min = 16,67 nkat", "U/L = ΔA/min × factor", "ALT/AST > 1 aguda · < 1 crónica", "NAD(P)H absorbe a 340 nm"]
    T.lesson = ("<h3>Idea central</h3><p>Dos tipos de caso: <b>¿qué inhibición es?</b> (mirando cómo cambian K<sub>m</sub> y V<sub>máx</sub>) y <b>¿qué órgano está dañado y cuándo pasó?</b> (patrón de enzimas y tiempos del IAM o de la pancreatitis).</p>"
                "<div class=\"ej\"><b>Triaje (caso Jorge):</b> dolor torácico → CK, CK-MB, troponinas, AST y LDH, y se repiten a las pocas horas para ver la curva: la CK-MB se normaliza al 2.º–3.<sup>er</sup> día y la LDH sigue alta más de una semana.</div>"
                "<div class=\"err\"><b>Error común:</b> creer que la LDH total sirve para localizar el órgano. Sin las isoenzimas da poca información.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> (1) el <b>alopurinol</b> es un inhibidor <b>competitivo</b> de la xantina oxidasa (análogo de la hipoxantina), no «no competitivo». (2) En el solucionario, a 340 nm absorbe el <b>NADH</b> (forma reducida), no el NAD⁺. (3) LDH4 = 1H/3M (no «3H/1H»).</div>")
    T.tools = [{"w": "mk", "t": "Marcadores del infarto en el tiempo", "o": {"set": "iam"}}, {"w": "mk", "t": "Marcadores de pancreatitis en el tiempo", "o": {"set": "panc"}}]
    T.add(1, "Clases de enzimas", "<p>Clasifica cada enzima según la EC.</p>",
          [cls("Clase", ["Oxidorreductasa", "Transferasa", "Hidrolasa", "Liasa"],
               [("Lactato deshidrogenasa (LDH)", 0), ("Aspartato aminotransferasa (AST)", 1), ("Creatina quinasa (CK)", 1), ("Fosfatasa alcalina", 2), ("Amilasa", 2), ("Aldolasa", 3), ("Glucosa oxidasa", 0), ("γ-glutamil transferasa", 1)])],
          ["Deshidrogenasas y oxidasas: oxidorreductasas (EC 1).", "Aminotransferasas, quinasas y GGT transfieren grupos (EC 2).", "Fosfatasas, amilasa, lipasa: hidrolizan (EC 3). Aldolasa: liasa (EC 4)."],
          "O · T · T · H · H · L · O · T", "El nombre suele decir la clase.")
    T.add(1, "Km y afinidad", "<p>La enzima A tiene K<sub>m</sub> = 0,2 mM y la enzima B, K<sub>m</sub> = 5 mM para el mismo sustrato.</p>",
          [opt("¿Cuál tiene más afinidad y actuará preferentemente?", "A: menor Km = mayor afinidad", "B: mayor Km = mayor afinidad", "Igual: Km no tiene que ver con la afinidad", "Depende solo de Vmáx", "Ninguna actúa")],
          ["K<sub>m</sub> es la [S] para alcanzar la mitad de V<sub>máx</sub>.", "Si necesita menos sustrato para ir a media velocidad, tiene más afinidad."],
          "A", "Km bajo = poco sustrato para ir a media marcha.")
    T.add(2, "¿Qué inhibición es?", "<p>Gráficas de Lineweaver-Burk sin inhibidor (gris) y con inhibidor (rojo).</p>",
          [opt("Gráfica 1: " + fig_lb('comp'), "Competitiva: Km ↑, Vmáx igual (mismo corte en Y)", "No competitiva", "Acompetitiva", "Alostérica positiva", "No hay inhibición"),
           opt("Gráfica 2: " + fig_lb('nocomp'), "No competitiva: Vmáx ↓, Km igual (mismo corte en X)", "Competitiva", "Acompetitiva", "Activación", "No hay inhibición"),
           opt("Gráfica 3: " + fig_lb('acomp'), "Acompetitiva: bajan Km y Vmáx (rectas paralelas)", "Competitiva", "No competitiva", "Irreversible", "No hay inhibición")],
          ["Corte en Y = 1/V<sub>máx</sub>; corte en X = −1/K<sub>m</sub>.", "Mismo corte en Y → V<sub>máx</sub> igual → competitiva (se supera con más sustrato).", "Mismo corte en X → K<sub>m</sub> igual → no competitiva.", "Paralelas → acompetitiva (el inhibidor se une al complejo ES)."],
          "Competitiva · no competitiva · acompetitiva", "Mira qué corte se mantiene.", chain=True)
    T.add(2, "ALT por método cinético", "<p>Lecturas de A (340 nm) cada minuto: 1,320 · 1,278 · 1,236 · 1,194. Factor del método: 1 750.</p>",
          [num("Cálculo", ("ΔA/min (en valor absoluto)", 0.042, None, 0.001), ("Actividad ALT", 73.5, "U/L", 0.6), ("En el SI", 1225, "nkat/L", 6))],
          ["Diferencias: 0,042 cada minuto → ΔA/min = 0,042 (baja porque se consume NADH).", "U/L = 0,042 × 1 750 = 73,5 U/L.", "× 16,67 = 1 225 nkat/L."],
          "0,042 · 73,5 U/L · 1 225 nkat/L", "Promedia las diferencias.")
    T.add(2, "Triaje: ¿cuándo empezó el dolor?", "<p>Paciente con dolor torácico. Resultados: <b>CK-MB y troponinas ya elevadas; AST todavía normal</b>.</p>",
          [mkt("Mueve el tiempo hasta un momento compatible.", "iam", [5, 8], "La CK-MB y las troponinas suben a las 3–6 h; la AST, más tarde.")],
          ["CK-MB y troponinas empiezan a subir a las ~4 h.", "La AST se eleva más tarde (~8 h) y hace pico a las 48 h.", "Ventana compatible: entre ~5 y 8 h."],
          "≈ 5–8 h", "¿Quién sube antes?")
    T.add(2, "Triaje: infarto de días", "<p>Llega un paciente con un infarto «de hace días»: <b>CK-MB y AST ya normales; troponina I y LDH aún elevadas</b>.</p>",
          [mkt("Mueve el tiempo hasta un momento compatible.", "iam", [121, 215])],
          ["La CK-MB se normaliza a las 48–72 h y la AST, hacia el 5.º día (120 h).", "La troponina I persiste 7–10 días y la LDH, más de 10 días.", "Ventana: entre el 5.º y el ~9.º día."],
          "Entre el día 5 y el 9", "Busca dónde ya bajaron las rápidas.")
    T.add(2, "Pancreatitis aguda", "<p>Resultados: <b>lipasa elevada, amilasa en sangre ya normal y amilasa en orina todavía elevada</b>.</p>",
          [mkt("Mueve el tiempo.", "panc", [97, 167])],
          ["La amilasa en sangre se normaliza entre el 2.º y el 8.º día (aquí, ~4 días).", "La amilasa en orina se normaliza después que en sangre, y la lipasa sigue alta 7–14 días."],
          "≈ días 4–7", "La amilasa en orina va con retraso.")
    T.add(1, "Patrones hepáticos", "<p>¿Qué patrón corresponde?</p>",
          [cls("Patología", ["Hepatitis aguda", "Colestasis", "Cirrosis / hepatopatía crónica", "Insuficiencia hepática"],
               [("ALT muy alta, ALT/AST > 1", 0), ("GGT y fosfatasa alcalina muy altas", 1), ("AST > ALT (cociente ALT/AST < 1)", 2), ("Colinesterasa disminuida", 3, "La ChE es una enzima plasma-específica que fabrica el hígado: baja si el hígado falla."),
                ("Transaminasas de 1 000 U/L que caen bruscamente (fulminante)", 0), ("5'-nucleotidasa alta con ALP alta y hueso normal", 1)])],
          ["Lisis aguda de hepatocitos: sobre todo ALT (citoplasma).", "Obstrucción biliar: GGT, ALP y 5'NT.", "Crónicas y alcohol: AST > ALT. Fallo de síntesis: bajan las enzimas plasma-específicas (ChE)."],
          "HA · Col · Cr · IH · HA · Col", "ALT = aguda; GGT/ALP = bilis.")
    T.add(2, "Lee la analítica: hepático", "<p>Varón de 30 años con astenia, náuseas e ictericia leve.</p>",
          [lab("Valora cada parámetro.", "Varón · 30 años", [
              ("ALT (GPT)", "820", "U/L", "≤ 45", 1), ("AST (GOT)", "560", "U/L", "≤ 37", 1), ("γ-GT", "62", "U/L", "11–50", 1), ("Fosfatasa alcalina", "110", "U/L", "40–130", 0),
              ("Bilirrubina total", "2,6", "mg/dL", "0,2–1,2", 1), ("Albúmina", "4,1", "g/dL", "3,5–5,2", 0)]),
           opt("¿Qué patrón es?", "Hepatitis aguda (ALT ≫, ALT/AST > 1)", "Colestasis extrahepática", "Cirrosis alcohólica", "Infarto de miocardio", "Pancreatitis aguda")],
          ["ALT/AST = 820/560 = 1,46 > 1 → daño agudo.", "ALP normal y GGT poco elevada: no es colestasis; albúmina normal: la síntesis se conserva."],
          "Hepatitis aguda", "Calcula ALT/AST.")
    T.add(1, "Isoenzimas y tejido", "<p>¿Qué tejido indica cada isoenzima?</p>",
          [cls("Tejido", ["Corazón", "Músculo esquelético", "Cerebro", "Hígado"],
               [("CK-MB", 0), ("CK-MM", 1), ("CK-BB", 2), ("LDH1 y LDH2", 0), ("LDH5", 3, "LDH4-5 predominan en hígado y músculo; aquí, hígado."), ("ALT (GPT)", 3)])],
          ["CK: MM músculo, MB corazón, BB cerebro.", "LDH1-2 corazón; LDH4-5 hígado y músculo. ALT: citoplasma del hepatocito."],
          "Co · Mu · Ce · Co · Hí · Hí", "M = muscle, B = brain, H = heart.")
    T.add(1, "Falsos positivos y negativos", "<p>Clasifica cada situación.</p>",
          [cls("Efecto", ["Falso positivo (↑)", "Falso negativo (↓)"],
               [("Hemólisis en una CK (libera adenilato quinasa)", 0), ("CK oxidada sin N-acetilcisteína en el reactivo", 1), ("Fosfatasa alcalina en plasma con EDTA", 1, "El EDTA quela el Mg²⁺, cofactor de la ALP."),
                ("LDH en una muestra hemolizada", 0), ("CK tras inyecciones intramusculares", 0), ("Fosfatasa ácida en tubo con fluoruro", 1)])],
          ["La hemólisis libera enzimas de los hematíes (AK, LDH, ACP): valores falsamente altos.", "Anticoagulantes inadecuados (EDTA, fluoruro, oxalato) inhiben enzimas: valores falsamente bajos."],
          "FP · FN · FN · FP · FP · FN", "¿Aporta enzima o la inhibe?")
    T.add(1, "¿Por qué 340 nm? (caso Jorge)", "<p>Para medir la AST se sigue la coenzima a 340 nm y no a 250 nm.</p>",
          [opt("¿Por qué?", "A 340 nm solo absorbe la forma reducida (NADH/NADPH), así que se ve cómo cambia", "A 340 nm solo absorbe el NAD⁺", "A 250 nm no absorbe ninguna", "Porque 340 nm es luz visible", "Porque a 340 nm absorbe la AST")],
          ["A 260 nm absorben NAD⁺ y NADH (el anillo de adenina): no se distinguen.", "A 340 nm solo absorbe la forma reducida: su aparición o desaparición mide la reacción (el solucionario lo dice al revés)."],
          "Solo el NADH absorbe a 340 nm", "¿Cuál de las dos formas tiene el pico extra?")
    return T

def uf7():
    T = Topic("u7", "UF7 · Electrolitos, equilibrio ácido-base y gasometría", "ab")
    T.teo = ("<p><strong>Agua corporal</strong> ≈ 60 % del peso (H) / 55 % (M): intracelular 40 %, extracelular 20 % (intersticial 15 % + plasma 4–5 %). Catión extracelular: <b>Na⁺</b>; intracelular: <b>K⁺</b> (~150 mmol/L). La regulan la ADH, la aldosterona, el sistema renina-angiotensina y el péptido natriurético.</p>"
             "<p><strong>Osmolalidad</strong> (osmómetro; normal 280–295 mOsm/kg): calculada = <b>2·Na + glucosa/18 + urea/6</b> (mg/dL). <b>Gap osmolal</b> = medida − calculada; &gt; 10 sugiere tóxicos (etanol, metanol) o cetoacidosis. Osmolaridad = osmolalidad × 0,93.</p>"
             "<p><strong>Electrolitos</strong>: Na⁺ 136–145; K⁺ 3,5–5; Cl⁻ 95–105 mEq/L; Ca 8,5–10,5 mg/dL; Mg 1,8–2,9 mg/dL. Na/K por <b>ISE</b> o fotometría de llama, con <b>heparina de litio</b> (nunca sódica); separar en &lt; 3 h; la <b>hemólisis sube el K⁺</b>. "
             "Cl⁻ con tiocianato de mercurio (525 nm); fosfato con molibdato (Fiske-Subbarow); Ca con cloranilato, calceína o ISE. Calcio corregido = <b>Ca + 0,8·(4 − albúmina)</b>.</p>"
             "<p><strong>pH</strong> 7,35–7,45. <b>Henderson-Hasselbalch</b>: <b>pH = 6,1 + log [HCO₃⁻]/(0,03·pCO₂)</b>; cociente normal HCO₃⁻/H₂CO₃ = 20/1. Tampones: bicarbonato (el principal), fosfato, proteínas, hemoglobina. Compensación respiratoria (rápida) y renal (lenta, 24 h o más).</p>"
             "<p><strong>Trastornos</strong>: acidosis metabólica (pH ↓, HCO₃⁻ ↓; compensa bajando la pCO₂: cetoacidosis, láctica, insuficiencia renal, diarrea), alcalosis metabólica (HCO₃⁻ ↑; vómitos, diuréticos, hipopotasemia), "
             "acidosis respiratoria (pCO₂ ↑; EPOC, opiáceos, neuromusculares), alcalosis respiratoria (pCO₂ ↓; ansiedad, fiebre, embarazo, ventilación mecánica). Regla: <b>el pH dice ácida o alcalina; la pCO₂, si es respiratoria; el HCO₃⁻, si es metabólica</b>.</p>"
             "<p><strong>Oxigenación</strong>: PaO₂ 80–100 mmHg (insuficiencia respiratoria &lt; 60); PaCO₂ 35–45; SaO₂ = O₂Hb/(O₂Hb + HHb) &gt; 94 %; COHb &lt; 1 % (fumadores 6–8 %); MetHb 0,2–0,6 %. "
             "<b>p50</b> (24–28 mmHg): <b>alta = curva a la derecha</b> (menor afinidad, libera más O₂: acidosis, ↑CO₂, ↑T, ↑2,3-DPG); baja = izquierda (COHb, MetHb, HbF).</p>"
             "<p><strong>Gasometría</strong>: sangre arterial en jeringa heparinizada, sin aire y tapada; transportar en mano (no por tubo neumático); hasta 30 min a temperatura ambiente y, si no, en agua con hielo; descartar 100–200 µL. Electrodos: pH (vidrio), <b>pCO₂ (Severinghaus)</b>, <b>pO₂ (Clark, amperometría)</b>.</p>")
    T.form = ["pH = 6,1 + log [HCO₃⁻]/(0,03·pCO₂)", "Osm calc = 2·Na + Glu/18 + Urea/6", "Gap osmolal = medida − calculada (> 10)", "Ca corregido = Ca + 0,8·(4 − Alb)", "pH 7,35–7,45 · pCO₂ 35–45 · HCO₃⁻ 22–26", "SaO₂ = O₂Hb/(O₂Hb + HHb)"]
    T.lesson = ("<h3>Idea central</h3><p>La gasometría se lee siempre en el mismo orden: <b>pH → pCO₂ → HCO₃⁻ → ¿compensa?</b></p>"
                "<ul><li><b>1.</b> pH &lt; 7,35 acidemia; &gt; 7,45 alcalemia.</li><li><b>2.</b> ¿Qué valor va en el sentido del pH? pCO₂ alta con acidemia → respiratoria; HCO₃⁻ bajo con acidemia → metabólica.</li><li><b>3.</b> El otro valor se mueve en el mismo sentido que el primario si hay compensación (acidosis metabólica: la pCO₂ baja ~1,2 mmHg por cada mEq que baja el HCO₃⁻).</li></ul>"
                "<div class=\"err\"><b>Error común:</b> en la gasometría con burbujas de aire, la pCO₂ baja y la pO₂ sube falsamente.</div>"
                "<div class=\"bqwarn\">⚠️ <b>Ojo con el material:</b> (1) Henderson-Hasselbalch va con el <b>bicarbonato arriba</b>: pH = 6,1 + log [HCO₃⁻]/(0,03·pCO₂); el cociente normal es HCO₃⁻/H₂CO₃ = 20/1. (2) El K⁺ intracelular es ≈ <b>150</b> mmol/L, no 15. (3) Calcio corregido = Ca + <b>0,8 × (4 − albúmina)</b>. (4) En la alcalosis respiratoria el pH <b>sube</b> (el texto dice «disminución del pH» en una frase). (5) En la tabla de compensaciones, en la alcalosis metabólica la pCO₂ <b>sube</b> ~0,7 mmHg por mEq.</div>")
    T.add(2, "Osmolalidad calculada y gap", "<p>Paciente confuso: Na⁺ 140 mEq/L, glucosa 90 mg/dL, urea 30 mg/dL. Osmolalidad medida: 312 mOsm/kg.</p>",
          [num("Cálculo", ("Osmolalidad calculada", 290, "mOsm/kg", 0.6), ("Gap osmolal", 22, "mOsm/kg", 0.6)),
           opt("¿Qué sugiere?", "Gap > 10: hay otra sustancia osmótica (p. ej., etanol o metanol)", "Es normal", "Hiponatremia por agua", "Error del osmómetro, siempre", "Hipoglucemia")],
          ["2 × 140 + 90/18 + 30/6 = 280 + 5 + 5 = 290 mOsm/kg.", "Gap = 312 − 290 = 22 > 10.", "Un gap alto indica solutos no medidos: alcoholes (intoxicación) o cetoacidosis."],
          "290; gap 22 → tóxico osmótico", "Multiplica el sodio por 2.")
    T.add(1, "Calcio corregido", "<p>Ca total = 7,6 mg/dL; albúmina = 2,5 g/dL. No hay síntomas de hipocalcemia.</p>",
          [num("Calcio corregido", ("Ca corregido", 8.8, "mg/dL", 0.05)),
           opt("Interpretación", "Normal: el calcio total es bajo por la hipoalbuminemia", "Hipocalcemia verdadera", "Hipercalcemia", "Hay que repetir con EDTA", "No se puede corregir")],
          ["Ca corregido = 7,6 + 0,8 × (4 − 2,5) = 7,6 + 1,2 = 8,8 mg/dL (normal).", "Con poca albúmina baja el calcio unido, pero el iónico puede ser normal (el material trae mal la fórmula)."],
          "8,8 mg/dL (normal)", "Cada g de albúmina que falta suma 0,8.")
    T.add(2, "Gasometría 1", "<p>Diabético con respiración rápida y profunda: <b>pH 7,28 · pCO₂ 30 mmHg · HCO₃⁻ 14 mEq/L</b>.</p>",
          [tree("Interpreta paso a paso.", [
              ("pH 7,28: ¿acidemia o alcalemia?", ["Acidemia (< 7,35)", "Alcalemia", "Normal"], [None, "Alcalemia es > 7,45.", "El rango normal es 7,35–7,45."]),
              ("¿Qué valor explica la acidemia?", ["HCO₃⁻ bajo (14): origen metabólico", "pCO₂ baja (30): origen respiratorio", "Ninguno"], [None, "Una pCO₂ baja alcaliniza: no puede causar acidemia.", "El HCO₃⁻ está claramente bajo."]),
              ("¿Hay compensación?", ["Sí: la pCO₂ bajó (hiperventilación); lo esperado es ~40 − 1,2 × 10 = 28", "No: la pCO₂ debería subir", "Es un trastorno mixto seguro"], [None, "En la acidosis metabólica el pulmón elimina CO₂: la pCO₂ baja.", "30 está cerca de lo esperado (28 ± 2)."])],
              "Acidosis metabólica con compensación respiratoria (probable cetoacidosis diabética).")],
          ["pH < 7,35 → acidemia.", "HCO₃⁻ 14 (bajo) va con la acidemia → metabólica.", "La pCO₂ baja por hiperventilación (Kussmaul): ΔHCO₃⁻ = 10 → pCO₂ esperada ≈ 28."],
          "Acidosis metabólica compensada parcialmente", "pH → pCO₂ → HCO₃⁻.")
    T.add(2, "Gasometría 2", "<p>Mujer con un ataque de ansiedad: <b>pH 7,52 · pCO₂ 28 mmHg · HCO₃⁻ 22 mEq/L</b>.</p>",
          [tree("Interpreta.", [
              ("pH 7,52:", ["Alcalemia", "Acidemia", "Normal"], [None, "Acidemia es < 7,35.", "Pasa de 7,45."]),
              ("¿Qué la explica?", ["pCO₂ baja (28): respiratoria", "HCO₃⁻ alto: metabólica", "El HCO₃⁻ bajo"], [None, "El HCO₃⁻ es 22: normal.", "Un HCO₃⁻ bajo acidificaría."]),
              ("¿Aguda o crónica?", ["Aguda: el HCO₃⁻ apenas bajó (~2 por cada 10 mmHg)", "Crónica: el riñón ya compensó del todo", "No hay forma de saberlo"], [None, "En la crónica bajaría ~5 mEq por cada 10 mmHg (quedaría en ~18).", "Compara con la Tabla 5."])],
              "Alcalosis respiratoria aguda por hiperventilación.")],
          ["pH > 7,45 → alcalemia.", "pCO₂ baja = elimina demasiado CO₂ (hiperventilación).", "HCO₃⁻ 22: compensación renal mínima → aguda."],
          "Alcalosis respiratoria aguda", "¿Quién se mueve en el sentido del pH?")
    T.add(1, "Cuatro gasometrías", "<p>Identifica el trastorno primario.</p>",
          [cls("Trastorno", ["Acidosis metabólica", "Alcalosis metabólica", "Acidosis respiratoria", "Alcalosis respiratoria"],
               [("pH 7,30 · pCO₂ 60 · HCO₃⁻ 29", 2), ("pH 7,50 · pCO₂ 48 · HCO₃⁻ 36", 1), ("pH 7,25 · pCO₂ 28 · HCO₃⁻ 12", 0), ("pH 7,49 · pCO₂ 30 · HCO₃⁻ 22", 3), ("pH 7,32 · pCO₂ 52 · HCO₃⁻ 27 (EPOC)", 2)])],
          ["Acidemia + pCO₂ alta → respiratoria; acidemia + HCO₃⁻ bajo → metabólica.", "Alcalemia + HCO₃⁻ alto → metabólica; alcalemia + pCO₂ baja → respiratoria."],
          "AR · AlM · AM · AlR · AR", "Primero el pH.")
    T.add(1, "Causas", "<p>¿Qué trastorno produce cada situación?</p>",
          [cls("Trastorno", ["Acidosis metabólica", "Alcalosis metabólica", "Acidosis respiratoria", "Alcalosis respiratoria"],
               [("Vómitos prolongados (pérdida de HCl)", 1), ("Sobredosis de opiáceos", 2), ("Cetoacidosis diabética", 0), ("Crisis de ansiedad", 3), ("Diarrea abundante (pierde bicarbonato)", 0), ("EPOC", 2), ("Hiperaldosteronismo con hipopotasemia", 1), ("Fiebre y sepsis por gramnegativos", 3)])],
          ["Pérdida de ácido o ganancia de bases → alcalosis metabólica; ganancia de ácidos o pérdida de HCO₃⁻ → acidosis metabólica.", "Hipoventilación → acidosis respiratoria; hiperventilación → alcalosis respiratoria."],
          "AlM · AR · AM · AlR · AM · AR · AlM · AlR", "¿Sobra o falta CO₂ o bicarbonato?")
    T.add(2, "Henderson-Hasselbalch", "<p>Usa pH = 6,1 + log [HCO₃⁻]/(0,03·pCO₂).</p>",
          [num("pH", ("HCO₃⁻ 24, pCO₂ 40", 7.40, None, 0.01), ("HCO₃⁻ 12, pCO₂ 25", 7.30, None, 0.01))],
          ["24/(0,03 × 40) = 24/1,2 = 20 → log 20 = 1,30 → pH = 7,40.", "12/(0,03 × 25) = 12/0,75 = 16 → log 16 = 1,20 → pH = 7,30."],
          "7,40 y 7,30", "0,03 × pCO₂ = ácido carbónico.")
    T.add(1, "Muestra para gasometría", "<p>Recomendaciones para el técnico en prácticas: ¿correcto o error?</p>",
          [cls("Clasifica", ["Correcto", "Error"],
               [("Transportar la jeringa en mano", 0), ("Enviarla por tubo neumático para ganar tiempo", 1, "La agitación mezcla burbujas (sube la pO₂) y hemoliza (sube el K⁺)."), ("Si tarda más de 30 min, conservarla en agua con hielo", 0),
                ("Dejar una burbuja de aire «para que respire»", 1, "El aire baja la pCO₂ (sube el pH) y sube la pO₂."), ("Descartar 100–200 µL antes de introducirla", 0), ("Usar heparina líquida en exceso", 1, "Diluye la muestra y baja la pCO₂.")])],
          ["Jeringa heparinizada, sin aire, tapada, en mano y medida pronto (o en agua con hielo si pasa de 30 min).", "Homogeneizar y descartar las primeras gotas evita coágulos y burbujas en el equipo."],
          "C · E · C · E · C · E", "El aire cambia los gases.")
    T.add(1, "Anticoagulante para Na⁺ y K⁺", "<p>Vas a medir sodio y potasio en plasma.</p>",
          [opt("¿Qué tubo usas?", "Heparina de litio", "Heparina sódica", "EDTA potásico", "Citrato sódico", "Fluoruro sódico"),
           opt("La muestra llega hemolizada. ¿Qué pasa con el potasio?", "Sale falsamente alto: se invalida la muestra", "Sale falsamente bajo", "No cambia", "Sube el sodio, no el potasio", "Se corrige multiplicando por 0,93")],
          ["La heparina sódica aporta sodio y el EDTA-K aporta potasio: falsean el resultado.", "Los hematíes tienen mucho K⁺: la hemólisis lo libera."],
          "Heparina de litio; K⁺ falsamente alto", "No uses un anticoagulante con el ion que mides.")
    T.add(2, "Curva de disociación de la Hb", "<p>Tres curvas de disociación de la hemoglobina.</p>",
          [tap("Toca el punto p50 de la curva desplazada a la <b>derecha</b> (p50 alta).", "hb", "der"),
           opt("¿Qué produce ese desplazamiento a la derecha?", "Acidosis, aumento de CO₂, de temperatura o de 2,3-DPG", "Carboxihemoglobina y metahemoglobina", "Hemoglobina fetal", "Alcalosis e hipotermia", "Hipocapnia")],
          ["p50 = pO₂ que satura la Hb al 50 %: si es alta, la Hb tiene menos afinidad y cede más O₂ a los tejidos.", "Derecha: ↑H⁺ (acidosis), ↑CO₂, ↑T, ↑2,3-DPG. Izquierda: COHb, MetHb, HbF, alcalosis."],
          "La curva roja; acidosis, CO₂, T, 2,3-DPG", "Más a la derecha = hace falta más pO₂ para saturar.", chain=True)
    T.add(1, "Saturación de oxígeno", "<p>Cooximetría: O₂Hb = 14,1 g/dL; HHb = 0,9 g/dL.</p>",
          [num("SaO₂", ("SaO₂", 94, "%", 0.2))],
          ["SaO₂ = O₂Hb/(O₂Hb + HHb) × 100 = 14,1/15,0 × 100 = 94 %.", "Por debajo de 92 % en el pulsioxímetro conviene hacer una gasometría arterial."],
          "94 %", "Solo cuentan las hemoglobinas funcionales.")
    return T
