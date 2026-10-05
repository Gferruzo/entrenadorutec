// Service worker del Entrenador: siempre intenta traer lo más nuevo de internet
// y solo usa la copia guardada cuando no hay conexión.
const CACHE = 'entrenador-v1';
const CDN = ['cdn.jsdelivr.net', 'fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);

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
