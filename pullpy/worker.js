/* Pullpy · intermediario entre NotPull y Gemini (Cloudflare Worker)
 *
 * Configuración en Cloudflare (Worker → Settings → Variables and Secrets):
 *   GEMINI_KEY  (secreto, obligatorio)  API key de Google AI Studio
 *   MODEL       (opcional)              modelo de Gemini; por defecto DEF_MODEL
 *   LIMITE_DIA  (opcional)              consultas por usuario al día; por defecto 40
 * KV opcional (Bindings → KV namespace) con el nombre LIMITES: activa el límite diario.
 *
 * Para agregar una función de Pullpy: agregar una entrada en TASKS (abajo)
 * y su contraparte en PULLPY.fx dentro de index.html.
 */
const FB_PROJECT = 'entrenadorutec';            // proyecto de Firebase de NotPull (login)
const ORIGENES = ['https://gferruzo.github.io']; // páginas que pueden usar a Pullpy
const DEF_MODEL = 'gemini-2.5-flash';
const NECESITA_LOGIN = true;                     // solo usuarios con sesión iniciada
const MAX_DATA = 16000;                          // tamaño máximo de lo que manda la app

const PERSONA = `Eres Pullpy, el pulpito con birrete de NotPull, una app gratuita para que estudiantes de la UTEC (Lima, Perú) practiquen para sus exámenes.
Hablas en español peruano, casual y cercano, pero claro y preciso. Respuestas cortas, pensadas para leerse en el celular.
Te basas solo en el material del curso que te pasa la app (teoría, enunciado, solución). Si algo no está ahí, no lo inventes.
Escribe las fórmulas en LaTeX entre \\( y \\). Usa **negritas** con moderación. No uses tablas ni encabezados.`;

/* Cada tarea: prompt(d) arma el mensaje con los datos que manda la app.
 * Opcionales: sys (instrucciones extra), max (tokens de salida), temp (temperatura). */
const TASKS = {
  prueba: { max: 120, temp: 0.8, prompt: () => 'Saluda en una sola línea y di que ya estás conectado a NotPull.' },
  // Aquí van las funciones de Pullpy, por ejemplo:
  // explica: { max: 500, sys: '...', prompt: d => `...${JSON.stringify(d)}` },
};

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const okOrigin = ORIGENES.includes(origin) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
    const cors = {
      'Access-Control-Allow-Origin': okOrigin ? origin : ORIGENES[0],
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    const res = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8' } });

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (req.method === 'GET') return res({ ok: true, pullpy: 'listo', tareas: Object.keys(TASKS), modelo: env.MODEL || DEF_MODEL, clave: !!env.GEMINI_KEY, limites: !!env.LIMITES });
    if (req.method !== 'POST') return res({ ok: false, error: 'metodo' }, 405);
    if (!okOrigin) return res({ ok: false, error: 'origen' }, 403);
    if (!env.GEMINI_KEY) return res({ ok: false, error: 'config' }, 500);

    let body;
    try { body = await req.json(); } catch { return res({ ok: false, error: 'json' }, 400); }
    const task = TASKS[body && body.task];
    if (!task) return res({ ok: false, error: 'tarea' }, 400);
    const data = body.data || {};
    if (JSON.stringify(data).length > MAX_DATA) return res({ ok: false, error: 'grande' }, 413);

    // Usuario (token de Firebase)
    let uid = null;
    const auth = req.headers.get('Authorization') || '';
    if (auth.startsWith('Bearer ')) { try { uid = await verificarToken(auth.slice(7)); } catch { uid = null; } }
    if (NECESITA_LOGIN && !uid) return res({ ok: false, error: 'login' }, 401);

    // Límite diario por usuario (solo si hay KV LIMITES)
    let quedan = null;
    if (env.LIMITES && uid) {
      const lim = parseInt(env.LIMITE_DIA || '40', 10);
      const dia = new Date(Date.now() - 5 * 3600e3).toISOString().slice(0, 10); // día en Lima
      const k = uid + ':' + dia;
      const n = parseInt((await env.LIMITES.get(k)) || '0', 10);
      if (n >= lim) return res({ ok: false, error: 'limite', quedan: 0 }, 429);
      await env.LIMITES.put(k, String(n + 1), { expirationTtl: 172800 });
      quedan = lim - n - 1;
    }

    // Gemini
    const model = env.MODEL || DEF_MODEL;
    const gen = { maxOutputTokens: task.max || 600, temperature: task.temp ?? 0.4 };
    if (/^gemini-2\.5-flash/.test(model)) gen.thinkingConfig = { thinkingBudget: task.think ?? 0 };
    let r, j;
    try {
      r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.GEMINI_KEY },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: PERSONA + (task.sys ? '\n\n' + task.sys : '') }] },
          contents: [{ role: 'user', parts: [{ text: task.prompt(data) }] }],
          generationConfig: gen,
        }),
      });
      j = await r.json();
    } catch { return res({ ok: false, error: 'ia' }, 502); }
    if (!r.ok) {
      const det = ((j && j.error) || {});
      return res({ ok: false, error: r.status === 429 ? 'ocupado' : 'ia', detalle: { status: r.status, estado: det.status, mensaje: String(det.message || '').slice(0, 300) } }, 502);
    }
    const text = ((((j.candidates || [])[0] || {}).content || {}).parts || []).map(p => p.text || '').join('').trim();
    if (!text) return res({ ok: false, error: 'vacio' }, 502);
    return res({ ok: true, text, quedan });
  },
};

/* ---------- Verificación del token de Firebase (RS256) ---------- */
let JWKS = null, JWKS_T = 0;
async function llaves() {
  if (JWKS && Date.now() - JWKS_T < 3600e3) return JWKS;
  const r = await fetch('https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com');
  JWKS = (await r.json()).keys; JWKS_T = Date.now();
  return JWKS;
}
function b64u(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '=';
  return Uint8Array.from(atob(s), c => c.charCodeAt(0));
}
async function verificarToken(tok) {
  const [h, p, s] = tok.split('.');
  if (!s) throw new Error('token');
  const dec = x => JSON.parse(new TextDecoder().decode(b64u(x)));
  const H = dec(h), P = dec(p);
  if (H.alg !== 'RS256') throw new Error('alg');
  const jwk = (await llaves()).find(k => k.kid === H.kid);
  if (!jwk) throw new Error('kid');
  const key = await crypto.subtle.importKey('jwk', { kty: jwk.kty, n: jwk.n, e: jwk.e, alg: 'RS256', ext: true },
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64u(s), new TextEncoder().encode(h + '.' + p));
  const now = Date.now() / 1000;
  if (!ok || P.aud !== FB_PROJECT || P.iss !== 'https://securetoken.google.com/' + FB_PROJECT || P.exp < now || P.iat > now + 300 || !P.sub) throw new Error('token');
  return P.sub;
}
