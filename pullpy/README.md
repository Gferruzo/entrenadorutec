# Pullpy · la IA de NotPull

La base ya está en la app, **apagada** mientras `PULLPY.url` (en `index.html`) esté vacía.

## Piezas
- `pullpy/worker.js`: Cloudflare Worker que guarda la API key de Gemini y recibe los pedidos de la app. Verifica el login de Firebase (proyecto `entrenadorutec`), solo acepta pedidos desde gferruzo.github.io y, si tiene un KV `LIMITES`, pone un límite diario por usuario.
- `index.html` → bloque «PULLPY (IA de NotPull)»: configuración (`PULLPY`), llamadas al Worker (`pullpy.ask`), contexto del ejercicio (`pullpy.data`), burbuja (`pullpy.box`) y botón (`pullpy.btn`).
- Enganches ya puestos en la app: `error` (falló una alternativa), `ex` (cada tarjeta de ejercicio), `topic` (al abrir un tema) y `simq` (cada pregunta del simulacro ya corregida).

## Prender a Pullpy (una sola vez)
1. Google AI Studio → «Get API key» → crear key (gratis, sin tarjeta).
2. Cloudflare (cuenta gratis) → Workers & Pages → Create → Worker «pullpy» → Edit code → pegar `pullpy/worker.js` → Deploy.
3. Worker → Settings → Variables and Secrets → agregar el secreto `GEMINI_KEY` con la key.
4. (Opcional, para el límite diario) Storage → KV → crear «pullpy-limites» y en el Worker → Bindings → KV namespace con el nombre `LIMITES`.
5. Abrir la URL del Worker en el navegador: debe decir `"pullpy":"listo"` y `"clave":true`.
6. Probar solo en tu navegador: en NotPull, consola → `localStorage.setItem('pullpy-url','"https://pullpy.<tu-usuario>.workers.dev"')`, recargar, iniciar sesión y correr `pullpy.test()`.
7. Para todos: poner esa URL en `PULLPY.url` dentro de `index.html`.

## Agregar una función
1. En `worker.js`, agregar la tarea en `TASKS` (`prompt(d)` con los datos que manda la app; opcionales `sys`, `max`, `temp`).
2. En `index.html`, registrarla en `PULLPY.fx`:
```js
PULLPY.fx.explica={at:'error',run({e,qi,oi,box}){if(box.querySelector('.ppbtn,.pullpy'))return;
  box.append(pullpy.btn('Explícame mi error',async function(){this.remove();
    const b=pullpy.box(box).load();
    try{b.say(await pullpy.ask('explica',pullpy.data(e,{pregunta:qi,elegida:pullpy.txt(e.checks[qi].o[oi])})))}catch(x){b.err(x)}}))}};
```
Para apagar una función sin borrarla: `off:true`.
