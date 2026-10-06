// Service worker del Entrenador: siempre intenta traer lo más nuevo de internet
// y solo usa la copia guardada cuando no hay conexión.
const CACHE = 'entrenador-v1';
// Los audios guardados por el usuario van aparte para no borrarse al actualizar
const AUDIOS = 'entrenador-audios';
const CDN = ['cdn.jsdelivr.net', 'fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== AUDIOS).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);

  // Audios: si el usuario lo guardó, sale de la copia (con soporte para adelantar);
  // si no, se reproduce directo de internet sin guardar nada
  if (u.origin === location.origin && u.pathname.includes('/audios/')) {
    e.respondWith(audio(r));
    return;
  }

  // Archivos propios (index, cursos, imágenes): primero internet, si falla, la copia
  if (u.origin === location.origin) {
    e.respondWith(
      fetch(r).then(res => {
        if (res.ok) { const c = res.clone(); caches.open(CACHE).then(ca => ca.put(r, c)); }
        return res;
      }).catch(() =>
        caches.match(r, { ignoreSearch: true })
          .then(m => m || (r.mode === 'navigate' ? caches.match('./') : null))
          .then(m => m || Response.error())
      )
    );
    return;
  }

  // Fórmulas (MathJax) y fuentes: no cambian, se guardan la primera vez
  if (CDN.includes(u.hostname)) {
    e.respondWith(
      caches.match(r).then(m => m || fetch(r).then(res => {
        if (res.ok || res.type === 'opaque') { const c = res.clone(); caches.open(CACHE).then(ca => ca.put(r, c)); }
        return res;
      }))
    );
  }
  // Todo lo demás (login de Google, Firebase) pasa directo, sin tocarlo
});

async function audio(r) {
  const hit = await caches.match(r.url.split('#')[0], { ignoreSearch: true, cacheName: AUDIOS });
  if (!hit) return fetch(r);
  const range = r.headers.get('range');
  if (!range) return hit;
  const buf = await hit.arrayBuffer(), total = buf.byteLength;
  const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
  let a = m[1] ? +m[1] : 0, b = m[2] ? +m[2] : total - 1;
  if (!m[1] && m[2]) { a = Math.max(0, total - +m[2]); b = total - 1; }
  b = Math.min(b, total - 1);
  if (a > b || a >= total) return new Response(null, { status: 416, headers: { 'Content-Range': 'bytes */' + total } });
  return new Response(buf.slice(a, b + 1), { status: 206, headers: {
    'Content-Type': hit.headers.get('Content-Type') || 'audio/mpeg',
    'Content-Range': 'bytes ' + a + '-' + b + '/' + total,
    'Content-Length': String(b - a + 1), 'Accept-Ranges': 'bytes' } });
}
