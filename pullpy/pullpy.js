/* ================= PULLPY · la mascota de NotPull =================
 * El dibujo original (pullpy.webp) no se modifica: las expresiones se logran con
 * "parches" encima (párpados, boca) y las animaciones mueven el dibujo completo.
 *
 * Uso desde la app:  pullpyPet.ev('good'|'bad'|'topic'|'half'|'course'|'sim'|'think'|'idle'|'quedan'|'limite', dato)
 *                    pullpyPet.say('texto')   pullpyPet.set('happy'|'sad'|'thinking'|'sleeping'|'idle')
 * Lee el estado de la app a través de window.PPB (lo expone index.html).
 * Frases: sin emojis (solo el fuego en la racha). Edítalas en FR.
 */
(function () {
  'use strict';
  const IMG = 'pullpy/pullpy.webp';
  const VB = '0 0 466 520';           // tamaño del dibujo
  const EYE_L = [154, 223], EYE_R = [272, 210], MOUTH = [218.5, 267];

  /* ---------- Frases (sin emojis) ---------- */
  const FR = {
    intro: 'Hola, soy Pullpy y todavía estoy en progreso. Muy pronto podré ayudarte con más cosas.',
    manana: ['Buenos días. ¿Qué estudiamos hoy?', 'Buen día. Un ratito y avanzamos.', 'Buenos días. Empecemos con algo cortito.'],
    tarde: ['Buenas tardes. ¿Seguimos?', 'Buenas tardes. ¿Repasamos un tema?', 'Un rato de estudio y listo.'],
    noche: ['Buenas noches. Un último repaso y a descansar.', 'Buenas noches. Algo cortito y a dormir.'],
    madrugada: ['Estudiando de madrugada. No te olvides de dormir.', 'Ya es tarde. Un poco más y a descansar, ¿ya?'],
    acierto: ['Tres seguidas. Vas muy bien.', 'Bien ahí, sigue así.', 'Eso, ya lo tienes claro.', 'Así se hace.'],
    error: ['Tranqui, de los errores se aprende.', 'Revisa la teoría del tema, ahí está la clave.', 'Casi. Mira la pista si la necesitas.', 'Respira y vuelve a intentarlo.'],
    toque: ['Aquí estoy.', '¿Seguimos?', 'Tú puedes.', 'Un tema a la vez.'],
    consejos: [
      'Consejo: intenta el ejercicio antes de ver la solución.',
      'Consejo: si fallas, vuelve a hacerlo mañana. Así se queda.',
      'Consejo: estudia en bloques cortos y descansa entre ellos.',
      'Consejo: explica el tema en voz alta, como si enseñaras.',
      'Consejo: deja el celular lejos mientras estudias.',
      'Consejo: repasa primero los temas donde más fallas.',
      'Consejo: duerme bien antes del examen, también es estudiar.',
      'Consejo: anota tus errores y revísalos antes del examen.'
    ],
    extrane: 'Te extrañé. ¿Retomamos?',
    racha: n => 'Llevas ' + n + ' días seguidos 🔥',
    novedades: n => n === 1 ? 'Hay una novedad en la campanita.' : 'Hay ' + n + ' novedades en la campanita.',
    pomoAviso: 'Falta un minuto para tu descanso.',
    pomoDescanso: ['Descansa, te lo ganaste.', 'Toma agua y estira un poco.'],
    pomoVuelta: 'Se acabó el descanso. A seguir.',
    flowAviso: 'Llevas 45 minutos. ¿Descansamos?',
    tema: 'Tema completado. Bien hecho.',
    mitad: 'Ya vas por la mitad del curso. Sigue así.',
    curso: 'Terminaste todo el curso. Increíble.',
    sim: 'Simulacro terminado. Revisa tus errores con calma.',
    quedan: n => n === 1 ? 'Me queda 1 explicación por hoy.' : 'Me quedan ' + n + ' explicaciones por hoy.',
    sinEnergia: 'Me quedé sin energía por hoy. Vuelvo mañana a ayudarte.'
  };

  /* ---------- utilidades ---------- */
  const LS = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  const SS = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  const B = () => window.PPB || null;
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dayStr = d => { d = d || new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
  const today = () => dayStr();
  const dayDiff = (a, b) => Math.round((new Date(b + 'T12:00:00') - new Date(a + 'T12:00:00')) / 864e5);
  const last = {};
  const pick = (k) => { const l = FR[k]; const c = l.filter(x => x !== last[k]); const p = c[Math.floor(Math.random() * c.length)] || l[0]; last[k] = p; return p; };
  const modalOpen = () => { const o = document.getElementById('ovl'); return !!(o && o.children.length); };

  /* ---------- estilos ---------- */
  const css = `
#ppet{position:absolute;z-index:3;width:104px;aspect-ratio:466/560;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none;touch-action:manipulation}
#ppet[hidden]{display:none}
#ppet .pp-hit{position:absolute;inset:0 0 7% 0;cursor:pointer;border:0;padding:0;background:none;border-radius:40%}
#ppet .pp-hit:focus-visible{outline:2px solid var(--ink,#2B2B2B);outline-offset:2px}
#ppet .pp-body{position:absolute;left:0;top:0;width:100%;aspect-ratio:466/520;transform-origin:50% 90%;animation:pp-float 3s ease-in-out infinite;pointer-events:none}
#ppet .pp-body img,#ppet .pp-body svg{position:absolute;inset:0;width:100%;height:100%;display:block}
#ppet .pp-body img{filter:drop-shadow(1.2px 0 0 #3D1214) drop-shadow(-1.2px 0 0 #3D1214) drop-shadow(0 1.2px 0 #3D1214) drop-shadow(0 -1.2px 0 #3D1214) drop-shadow(0 2px 3px rgba(61,18,20,.2))}
#ppet .pp-floor{position:absolute;left:50%;bottom:0;width:56%;height:9%;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse at center,rgba(20,30,50,.2) 0%,transparent 70%);animation:pp-floorA 3s ease-in-out infinite;pointer-events:none}
#ppet .lid{opacity:0}#ppet .lid ellipse,#ppet .lid .cv,#ppet .pp-mt .cv{fill:#FFB794;stroke:none}
#ppet .lid path{fill:none;stroke:#3D1214;stroke-width:4;stroke-linecap:round}
#ppet .pp-blink{animation:pp-blink 4.5s infinite}
#ppet .pp-mt{opacity:0}#ppet .pp-mt .op{fill:#3D1214;transform-box:fill-box;transform-origin:center}
#ppet .pp-sw{opacity:0}
#ppet .pp-fx{position:absolute;pointer-events:none}
#ppet .pp-sp{inset:-6% -10%}
#ppet .pp-sp i{position:absolute;width:16%;aspect-ratio:1;opacity:0;background:currentColor;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
#ppet .pp-sp i:nth-child(1){left:0;top:22%;color:#F6C445}#ppet .pp-sp i:nth-child(2){right:0;top:10%;color:#F2796B;width:19%}
#ppet .pp-sp i:nth-child(3){right:6%;top:44%;color:#FFD166;width:12%}#ppet .pp-sp i:nth-child(4){left:12%;top:2%;color:#F58D7E;width:11%}
#ppet .pp-z{right:-4%;top:2%;width:44%;height:36%;color:var(--ink,#2B2B2B);font-family:Figtree,system-ui,sans-serif}
#ppet .pp-z b{position:absolute;opacity:0;font-weight:800;line-height:1}
#ppet .pp-z b:nth-child(1){left:0;bottom:0;font-size:12px}#ppet .pp-z b:nth-child(2){left:30%;bottom:30%;font-size:16px}#ppet .pp-z b:nth-child(3){left:62%;bottom:62%;font-size:21px}
#ppet .pp-th{right:-14%;top:-6%;width:56%;opacity:0;transition:opacity .2s}
#ppet .pp-th .cl{position:relative;margin-left:auto;width:100%;aspect-ratio:1.7;border-radius:999px;background:var(--card,#fff);border:2px solid var(--ink,#2B2B2B);display:flex;align-items:center;justify-content:center;gap:9%}
#ppet .pp-th .cl span{width:12%;aspect-ratio:1;border-radius:50%;background:var(--ink,#2B2B2B);opacity:.25}
#ppet .pp-th .d{position:absolute;border-radius:50%;background:var(--card,#fff);border:2px solid var(--ink,#2B2B2B)}
#ppet .pp-th .d1{width:20%;aspect-ratio:1;left:4%;top:92%}#ppet .pp-th .d2{width:12%;aspect-ratio:1;left:-8%;top:118%}
#ppet .pp-bub{position:absolute;bottom:72%;right:78%;width:max-content;max-width:min(220px,62vw);padding:8px 12px;border-radius:14px;background:var(--card,#fff);color:var(--ink,#2B2B2B);border:2px solid var(--ink,#2B2B2B);font:600 13.5px/1.35 Figtree,system-ui,sans-serif;box-shadow:0 6px 16px rgba(0,0,0,.12);opacity:0;transform:scale(.8);transform-origin:bottom right;transition:opacity .2s,transform .25s cubic-bezier(.34,1.56,.64,1);pointer-events:none;text-align:left}
#ppet .pp-bub.on{opacity:1;transform:scale(1);pointer-events:auto;cursor:pointer}
#ppet .pp-bub::after{content:"";position:absolute;right:14px;bottom:-8px;width:12px;height:12px;background:inherit;border-right:2px solid;border-bottom:2px solid;border-color:inherit;transform:rotate(45deg)}
#ppet.dock{position:fixed;left:8px;right:auto;top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + 8px);width:76px;z-index:44}
#ppet.dock .pp-bub{right:auto;left:84%;bottom:70%;transform-origin:bottom left}
#ppet.dock .pp-bub::after{right:auto;left:14px}
#ppet.brk{width:118px}
#ppet.mini{width:46px}
#ppet.mini .pp-body{border-radius:50%;overflow:hidden;background:var(--card,#fff);border:2px solid var(--ink,#2B2B2B);animation:none;aspect-ratio:1}
#ppet.mini .pp-body img{inset:auto;top:-8%;left:-14%;width:128%;height:auto;filter:none}
#ppet.mini .pp-body svg,#ppet.mini .pp-floor,#ppet.mini .pp-fx,#ppet.mini .pp-bub{display:none}
.hero.pp-on h1{padding-right:112px}
@media (min-width:700px){#ppet:not(.dock){width:128px}.hero.pp-on h1{padding-right:140px}}
/* estados */
#ppet.happy .pp-body{animation:pp-jump .9s cubic-bezier(.3,.8,.4,1) both}
#ppet.happy .pp-floor{animation:pp-floorJ .9s ease both}
#ppet.party .pp-body{animation:pp-jump .9s cubic-bezier(.3,.8,.4,1) 2 both}
#ppet.party .pp-floor{animation:pp-floorJ .9s ease 2 both}
#ppet.happy .pp-hap,#ppet.party .pp-hap{opacity:1}
#ppet.happy .pp-blink,#ppet.party .pp-blink,#ppet.sleeping .pp-blink{animation:none}
#ppet.happy .pp-sp i,#ppet.party .pp-sp i{animation:pp-spark .9s ease-out both}
#ppet.party .pp-sp i{animation-iteration-count:2}
#ppet .pp-sp i:nth-child(2){animation-delay:.08s}#ppet .pp-sp i:nth-child(3){animation-delay:.16s}#ppet .pp-sp i:nth-child(4){animation-delay:.12s}
#ppet.sad .pp-body{animation:pp-sad 1.1s ease-in-out both}
#ppet.sad .pp-sw{animation:pp-sweat 1.1s ease-out both}
#ppet.sad .pp-tri,#ppet.blue .pp-tri{opacity:1}#ppet.sad .pp-blink,#ppet.blue .pp-blink{animation:none}
#ppet.blue.talk:not(.done) .pp-mt{opacity:0}
#ppet.blue .pp-body{animation:pp-blue .7s ease-out forwards}
#ppet.blue .pp-sw{animation:pp-sweat 1.4s ease-out .3s both}
#ppet.talk:not(.done):not(.blue) .pp-body{animation:pp-talk .45s ease-in-out infinite}
#ppet.talk:not(.done) .pp-mt{opacity:1}
#ppet.talk:not(.done) .pp-mt .op{animation:pp-chat .22s ease-in-out infinite}
#ppet.sleeping .pp-body{animation:pp-breathe 5s ease-in-out infinite}
#ppet.sleeping .pp-floor{animation:pp-floorA 5s ease-in-out infinite}
#ppet.sleeping .pp-slp{opacity:1}
#ppet.sleeping .pp-z b{animation:pp-z 3s ease-in-out infinite}
#ppet.sleeping .pp-z b:nth-child(2){animation-delay:1s}#ppet.sleeping .pp-z b:nth-child(3){animation-delay:2s}
#ppet.thinking .pp-body{animation:pp-ponder 4s ease-in-out infinite}
#ppet.thinking .pp-th{opacity:1}
#ppet.thinking .pp-th .cl span{animation:pp-dot 1.2s infinite}
#ppet.thinking .pp-th .cl span:nth-child(2){animation-delay:.2s}#ppet.thinking .pp-th .cl span:nth-child(3){animation-delay:.4s}
@keyframes pp-float{0%,100%{transform:translateY(5%) scale(1.01,.99)}50%{transform:translateY(-6%) scale(.995,1.01)}}
@keyframes pp-floorA{0%,100%{transform:translateX(-50%) scale(1);opacity:1}50%{transform:translateX(-50%) scale(.82);opacity:.7}}
@keyframes pp-floorJ{0%,100%{transform:translateX(-50%) scale(1)}18%{transform:translateX(-50%) scale(1.08)}50%{transform:translateX(-50%) scale(.6);opacity:.5}}
@keyframes pp-jump{0%{transform:none}18%{transform:translateY(5%) scale(1.06,.92)}50%{transform:translateY(-26%) scale(.95,1.06) rotate(-3deg)}78%{transform:translateY(3%) scale(1.04,.95)}90%{transform:translateY(-4%)}100%{transform:none}}
@keyframes pp-sad{0%{transform:none}15%{transform:translateY(6%) scale(1.02,.95)}25%{transform:translate(-3%,6%) scale(1.02,.95) rotate(-2deg)}35%{transform:translate(3%,6%) scale(1.02,.95) rotate(2deg)}45%{transform:translate(-2%,6%) scale(1.02,.95)}55%,85%{transform:translateY(6%) scale(1.02,.95)}100%{transform:none}}
@keyframes pp-blue{0%{transform:none}100%{transform:translateY(7%) scale(1.03,.93) rotate(-4deg)}}
@keyframes pp-talk{0%,100%{transform:translateY(2%) scale(1.01,.99)}50%{transform:translateY(-3%) scale(.995,1.01)}}
@keyframes pp-breathe{0%,100%{transform:translateY(6%) rotate(-3deg) scale(1)}50%{transform:translateY(3%) rotate(-3deg) scale(1.025)}}
@keyframes pp-ponder{0%,100%{transform:translateY(3%) rotate(4deg)}50%{transform:translateY(-4%) rotate(4deg)}}
@keyframes pp-blink{0%,94%,100%{opacity:0}96%,98%{opacity:1}}
@keyframes pp-chat{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}
@keyframes pp-spark{0%{opacity:0;transform:scale(.2) rotate(-30deg)}35%{opacity:1;transform:scale(1.15) rotate(0)}100%{opacity:0;transform:translateY(-60%) scale(.5) rotate(25deg)}}
@keyframes pp-sweat{0%,12%{opacity:0;transform:translateY(-3%)}30%{opacity:1;transform:none}80%{opacity:1;transform:translateY(5%)}100%{opacity:0;transform:translateY(7%)}}
@keyframes pp-z{0%{opacity:0;transform:translate(-20%,30%) scale(.7)}30%{opacity:1}100%{opacity:0;transform:translate(40%,-60%) scale(1.1)}}
@keyframes pp-dot{0%,100%{opacity:.25}40%{opacity:1}}
:root[data-theme="dark"] #ppet .pp-body img{filter:none}
:root[data-theme="dark"] #ppet .pp-floor{background:radial-gradient(ellipse at center,rgba(0,0,0,.45) 0%,transparent 70%)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #ppet .pp-body img{filter:none}:root:not([data-theme="light"]) #ppet .pp-floor{background:radial-gradient(ellipse at center,rgba(0,0,0,.45) 0%,transparent 70%)}}
@media (prefers-reduced-motion:reduce){#ppet .pp-body,#ppet .pp-floor,#ppet .pp-fx *{animation-duration:0s!important;animation-iteration-count:1!important}}
`;

  /* ---------- DOM ---------- */
  const lids = (cls, dl, dr) =>
    '<g class="lid ' + cls + '"><ellipse cx="' + EYE_L[0] + '" cy="' + EYE_L[1] + '" rx="17" ry="17"/><ellipse cx="' + EYE_R[0] + '" cy="' + EYE_R[1] + '" rx="17" ry="17"/><path d="' + dl + '"/><path d="' + dr + '"/></g>';
  function build() {
    const st = document.createElement('style'); st.id = 'ppet-css'; st.textContent = css; document.head.appendChild(st);
    const w = document.createElement('div'); w.id = 'ppet'; w.hidden = true;
    w.innerHTML =
      '<div class="pp-floor"></div>' +
      '<div class="pp-body"><img src="' + IMG + '" alt="" draggable="false">' +
      '<svg viewBox="' + VB + '" aria-hidden="true">' +
      lids('pp-blink', 'M140 225 Q154 231 168 225', 'M258 212 Q272 218 286 212') +
      lids('pp-hap', 'M141 228 Q154 210 167 228', 'M259 215 Q272 197 285 215') +
      lids('pp-slp', 'M141 222 Q154 233 167 222', 'M259 209 Q272 220 285 209') +
      '<g class="lid pp-tri"><path class="cv" d="M134 203 L174 203 L174 216 L134 228 Z"/><path class="cv" d="M252 190 L292 190 L292 215 L252 203 Z"/>' +
      '<path d="M136 227 L172 216"/><path d="M254 203 L290 214"/>' +
      '<ellipse class="cv" cx="' + MOUTH[0] + '" cy="' + MOUTH[1] + '" rx="15" ry="8"/><path d="M209 272 Q218.5 262 228 272"/></g>' +
      '<g class="pp-mt"><ellipse class="cv" cx="' + MOUTH[0] + '" cy="' + MOUTH[1] + '" rx="15" ry="8"/><ellipse class="op" cx="' + MOUTH[0] + '" cy="' + (MOUTH[1] + 1) + '" rx="7" ry="6"/></g>' +
      '<path class="pp-sw" d="M330 150 C330 150 339 164 339 170 A9 9 0 0 1 321 170 C321 164 330 150 330 150Z" fill="#7CC6FE" stroke="#fff" stroke-width="3"/>' +
      '</svg></div>' +
      '<div class="pp-fx pp-sp"><i></i><i></i><i></i><i></i></div>' +
      '<div class="pp-fx pp-z"><b>z</b><b>z</b><b>Z</b></div>' +
      '<div class="pp-fx pp-th"><div class="cl"><span></span><span></span><span></span></div><div class="d d1"></div><div class="d d2"></div></div>' +
      '<button class="pp-hit" type="button" aria-label="Pullpy"></button>' +
      '<div class="pp-bub" role="status" aria-live="polite"></div>';
    return w;
  }

  /* ---------- estado ---------- */
  const W = build();
  const bub = W.querySelector('.pp-bub'), hit = W.querySelector('.pp-hit');
  const STATES = ['happy', 'party', 'sad', 'blue', 'sleeping', 'thinking'];
  const SHORT = { happy: 900, party: 1800, sad: 1100 };
  let cur = 'idle', mood = null, back = null, typing = null, hideT = null, queue = [], speaking = false;
  let mode = '', mini = SS.get('pp-mini') === '1';
  let streakGood = 0, streakBad = 0, thinking = false;
  const tired = () => LS.get('pp-zzz', '') === today();
  const base = () => (pomoBreak || tired()) ? 'sleeping' : thinking ? 'thinking' : 'idle';

  function paint(s) {
    W.classList.remove(...STATES);
    if (s !== 'idle') W.classList.add(s);
    void W.offsetWidth;
  }
  function set(s) {
    clearTimeout(back); cur = s;
    if (s === 'idle') s = base();
    paint(s);
    if (SHORT[s]) back = setTimeout(() => { cur = 'idle'; paint(speaking && mood ? mood : base()); }, SHORT[s]);
  }

  /* globo: escribe letra por letra; si hay un modal abierto, espera */
  function say(text, opts) {
    opts = opts || {};
    if (!text) return;
    queue.push({ text, opts });
    if (!speaking) next();
  }
  function next() {
    if (!queue.length) { speaking = false; return; }
    if (modalOpen() || W.hidden || mini) { setTimeout(next, 700); return; }
    speaking = true;
    const { text, opts } = queue.shift();
    clearInterval(typing); clearTimeout(hideT);
    mood = opts.mood || null;
    if (mood) paint(mood);
    W.classList.add('talk'); W.classList.remove('done');
    bub.textContent = ''; bub.classList.add('on');
    const hold = opts.hold || 3500;
    const done = () => {
      W.classList.add('done');
      hideT = setTimeout(close, hold);
    };
    const start = () => {
      if (RM) { bub.textContent = text; return done(); }
      const ch = Array.from(text); let i = 0;
      typing = setInterval(() => { if (i < ch.length) bub.textContent += ch[i++]; else { clearInterval(typing); typing = null; done(); } }, 32);
    };
    if (opts.mood) setTimeout(start, opts.moodMs || 1000); else start();
  }
  function close() {
    clearInterval(typing); clearTimeout(hideT); typing = null;
    bub.classList.remove('on'); W.classList.remove('talk', 'done');
    speaking = false; mood = null; paint(base());
    if (queue.length) setTimeout(next, 400);
  }
  bub.addEventListener('click', close);

  /* ---------- toque: feliz (+ frase o consejo) · mantener presionado: esconder ---------- */
  let pressT = null, longPress = false;
  hit.addEventListener('pointerdown', () => { longPress = false; pressT = setTimeout(() => { longPress = true; toggleMini(true); }, 650); });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(e => hit.addEventListener(e, () => clearTimeout(pressT)));
  hit.addEventListener('contextmenu', e => e.preventDefault());
  hit.addEventListener('click', () => {
    if (longPress) return;
    if (mini) return toggleMini(false);
    if (speaking) close();
    set('happy');
    if (tired()) { setTimeout(() => say(FR.sinEnergia), 900); return; }
    if (Math.random() < .55) setTimeout(() => say(Math.random() < .6 ? pick('consejos') : pick('toque'), { hold: 4500 }), 900);
  });
  function toggleMini(on) {
    mini = on; SS.set('pp-mini', on ? '1' : '0');
    W.classList.toggle('mini', on);
    hit.setAttribute('aria-label', on ? 'Mostrar a Pullpy' : 'Pullpy');
    if (on) { close(); }
    place(true);
  }

  /* ---------- racha de días de estudio ---------- */
  function days() { return LS.get('pp-dias', []); }
  function streakTo(d) {
    const s = new Set(days()); let n = 0, t = new Date(d + 'T12:00:00');
    while (s.has(dayStr(t))) { n++; t.setDate(t.getDate() - 1); }
    return n;
  }
  function studied() {
    const d = days(), t = today();
    if (d.includes(t)) return;
    d.push(t); LS.set('pp-dias', d.slice(-60));
    const n = streakTo(t);
    if (n >= 2 && LS.get('pp-racha-dia', '') !== t) { LS.set('pp-racha-dia', t); set('happy'); setTimeout(() => say(FR.racha(n), { hold: 4500 }), 900); }
  }

  /* ---------- eventos desde la app ---------- */
  function ev(k, d) {
    switch (k) {
      case 'good':
        studied(); streakBad = 0; streakGood++;
        set('happy');
        if (streakGood >= 3 && streakGood % 3 === 0 && !speaking) setTimeout(() => say(pick('acierto')), 900);
        break;
      case 'bad':
        studied(); streakGood = 0; streakBad++;
        set('sad');
        if (streakBad === 2 && !speaking) setTimeout(() => say(pick('error')), 1000);
        break;
      case 'topic': set('party'); say(FR.tema); break;
      case 'half': set('party'); try { B() && B().confetti(); } catch (e) {} say(FR.mitad, { hold: 4500 }); break;
      case 'course': set('party'); say(FR.curso, { hold: 4500 }); break;
      case 'sim': say(FR.sim, { hold: 4500 }); break;
      case 'think': thinking = true; if (!speaking) set('thinking'); break;
      case 'idle': thinking = false; if (!speaking) set('idle'); break;
      case 'quedan': if (d === 2 || d === 1) say(FR.quedan(d)); if (d === 0) { LS.set('pp-zzz', today()); } break;
      case 'limite': thinking = false; LS.set('pp-zzz', today()); say(FR.sinEnergia, { mood: 'blue', moodMs: 900, hold: 5000 }); break;
    }
  }

  /* ---------- dónde se muestra ---------- */
  let typingInput = false;
  document.addEventListener('focusin', e => { const t = e.target; typingInput = !!(t && (t.matches('input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=button]),textarea,select,[contenteditable=""],[contenteditable="true"],math-field'))); place(); });
  document.addEventListener('focusout', () => { typingInput = false; setTimeout(place, 50); });

  function place(force) {
    const b = B(); if (!b) return;
    const v = b.view;
    let want;
    if (b.examNow && b.examNow()) want = 'off';
    else if (v === 'menu') want = 'hero';
    else want = 'dock';
    if (want === 'dock' && typingInput && innerWidth < 760) want = 'off';
    const hero = document.querySelector('#vMenu .hero');
    if (want !== mode || force) {
      if (want === 'hero' && hero) {
        hero.classList.add('pp-on'); hero.style.position = 'relative';
        if (W.parentNode !== hero) hero.appendChild(W);
        W.classList.remove('dock');
      } else if (want === 'dock') {
        if (hero) hero.classList.remove('pp-on');
        if (W.parentNode !== document.body) document.body.appendChild(W);
        W.classList.add('dock');
      }
      W.hidden = want === 'off';
      if (want === 'off') close();
      mode = want;
    }
    W.classList.toggle('mini', mini && want === 'dock');
    W.classList.toggle('brk', pomoBreak && want === 'dock' && !mini);
    if (want === 'hero' && hero) {
      const h1 = hero.querySelector('h1');
      if (h1) W.style.top = Math.max(0, h1.offsetTop + h1.offsetHeight / 2 - W.offsetHeight * .55) + 'px';
      W.style.right = '0'; W.style.bottom = '';
    } else if (want === 'dock') {
      W.style.top = ''; W.style.right = '';
      const ab = document.getElementById('aubar');
      let bot = 8;
      if (ab && !ab.hidden && ab.offsetParent !== null) { const r = ab.getBoundingClientRect(); if (r.left < 120) bot = Math.max(8, innerHeight - r.top + 8); }
      W.style.bottom = 'calc(env(safe-area-inset-bottom,0px) + ' + bot + 'px)';
    }
  }

  /* ---------- Pomodoro ---------- */
  let pomoBreak = false, pomoWarned = null, lastPhase = null;
  function pomo() {
    const b = B(); const tm = b && b.TM;
    const ph = tm ? tm.phase : null;
    if (tm && ph === 'work' && tm.cfg && tm.cfg.kind === 'pomo' && tm.t0) {
      const left = tm.t0 + tm.len - (tm.acc || 0) - Date.now();
      const key = tm.blk + ':' + tm.len;
      if (left > 0 && left <= 60000 && pomoWarned !== key) { pomoWarned = key; say(FR.pomoAviso); }
    }
    if (tm && ph === 'work' && tm.cfg && tm.cfg.kind === 'flow' && tm.ask && pomoWarned !== 'flow' + tm.blk) { pomoWarned = 'flow' + tm.blk; say(FR.flowAviso); }
    if (ph !== lastPhase) {
      if (ph === 'break') { pomoBreak = true; say(pick('pomoDescanso')); }
      else if (lastPhase === 'break') { pomoBreak = false; set('happy'); say(FR.pomoVuelta); }
      else pomoBreak = false;
      lastPhase = ph;
      if (!speaking) paint(base());
      place(true);
    }
  }

  /* ---------- mensajes al entrar al menú ---------- */
  let greeted = false;
  function greet() {
    if (greeted) return; const b = B(); if (!b || b.view !== 'menu') return;
    greeted = true;
    const t = today();
    if (!LS.get('pp-intro', 0)) { LS.set('pp-intro', 1); say(FR.intro, { hold: 6000 }); return; }
    const d = days().filter(x => x < t).sort(); const lastDay = d[d.length - 1];
    if (lastDay && dayDiff(lastDay, t) >= 2 && LS.get('pp-extrane', '') !== t) {
      LS.set('pp-extrane', t); say(FR.extrane, { mood: 'blue', moodMs: 1400, hold: 4500 }); return;
    }
    try {
      const k = b.NOTI ? b.nvList().filter(b.nvCounts).length : 0;
      const sig = k ? b.nvList().filter(b.nvCounts).map(n => n.id).join(',') : '';
      if (k && LS.get('pp-nov', '') !== sig) { LS.set('pp-nov', sig); say(FR.novedades(k), { hold: 4000 }); return; }
    } catch (e) {}
    if (tired()) return;
    if (SS.get('pp-hola')) return; SS.set('pp-hola', '1');
    const h = new Date().getHours();
    say(pick(h < 5 ? 'madrugada' : h < 12 ? 'manana' : h < 19 ? 'tarde' : 'noche'));
  }

  /* ---------- arranque ---------- */
  function tick() { place(); pomo(); greet(); }
  function boot() {
    if (!B()) return setTimeout(boot, 300);
    paint(base()); place(true);
    setTimeout(() => { greet(); }, 1200);
    setInterval(tick, 1000);
    addEventListener('resize', () => place(true));
  }
  window.pullpyPet = { ev, say, set, close, FR };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
