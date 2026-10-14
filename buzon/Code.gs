/**
 * NotPull · Buzón de aportes (Google Apps Script, cuenta gferruzo2007@gmail.com)
 *
 * Recibe los envíos de «📤 Aportar material» y:
 *  - crea una subcarpeta en «NotPull · Buzón» con nombre
 *      <Curso> · Sem N · <Tipo> · AAAA-MM-DD HH:mm   (curso nuevo: «🆕 <Nombre> · …»)
 *  - guarda los archivos y un info.txt
 *  - manda un correo con el mismo título
 *
 * Envíos grandes (zip) llegan en varias partes con el mismo `lote`:
 * todas van a la misma carpeta y el correo sale una sola vez, con la última parte.
 *
 * Después de pegar este código: Implementar → Gestionar implementaciones →
 * ✏️ editar la implementación actual → Versión: «Nueva versión» → Implementar.
 * (Así la URL /exec no cambia.) Si pide permisos nuevos, aceptarlos.
 */

const RAIZ = 'NotPull · Buzón';
const TZ = 'America/Lima';

function doPost(e) {
  try {
    const b = JSON.parse(e.postData.contents);
    const files = b.files || [];
    if (!files.length) return out_({ ok: false, error: 'sin archivos' });

    const props = PropertiesService.getScriptProperties();
    const lock = LockService.getScriptLock();
    lock.waitLock(30000);
    let carpeta, titulo, nuevo = false;
    try {
      const key = b.lote ? 'lote_' + b.lote : '';
      const id = key && props.getProperty(key);
      if (id) {
        carpeta = DriveApp.getFolderById(id);
        titulo = carpeta.getName();
      } else {
        titulo = titulo_(b);
        carpeta = raiz_().createFolder(titulo);
        nuevo = true;
        if (key) props.setProperty(key, carpeta.getId());
      }
    } finally {
      lock.releaseLock();
    }

    const nombres = [];
    files.forEach(f => {
      const nombre = limpio_(f.name || 'archivo');
      const blob = Utilities.newBlob(Utilities.base64Decode(f.data), f.mime || 'application/octet-stream', nombre);
      carpeta.createFile(blob);
      nombres.push(nombre);
    });

    if (nuevo) carpeta.createFile('info.txt', info_(b), MimeType.PLAIN_TEXT);

    // Cuántos archivos van en total en este lote
    const nk = b.lote ? 'n_' + b.lote : '';
    const total = (nk ? Number(props.getProperty(nk) || 0) : 0) + nombres.length;
    const ultima = !b.lote || !b.partes || Number(b.parte) >= Number(b.partes);

    if (ultima) {
      aviso_(b, titulo, carpeta, total);
      if (b.lote) { props.deleteProperty('lote_' + b.lote); props.deleteProperty(nk); }
    } else if (nk) {
      props.setProperty(nk, String(total));
    }

    return out_({ ok: true, n: nombres.length });
  } catch (err) {
    console.error(err);
    return out_({ ok: false, error: String(err && err.message || err) });
  }
}

function doGet() {
  return out_({ ok: true, buzon: RAIZ });
}

// «Cálculo de una Variable (CC6103) · Sem 10 · Guía o práctica · 2026-10-14 01:40»
function titulo_(b) {
  const c = String(b.curso || 'Sin curso').trim();
  const esNuevo = /^NUEVO:\s*/i.test(c);
  const partes = [(esNuevo ? '🆕 ' : '') + c.replace(/^NUEVO:\s*/i, '')];
  if (b.semana) partes.push('Sem ' + b.semana);
  if (b.tipo) partes.push(b.tipo);
  partes.push(Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'));
  return limpio_(partes.join(' · ')).slice(0, 200);
}

function info_(b) {
  return [
    'Universidad: ' + (b.universidad || 'UTEC'),
    'Curso: ' + (b.curso || ''),
    'Semana: ' + (b.semana || '—'),
    'Tipo: ' + (b.tipo || ''),
    'Nota: ' + (b.nota || ''),
    'Usuario: ' + (b.usuario || ''),
    'Correo: ' + (b.email || ''),
    'UID: ' + (b.uid || ''),
    'Fecha: ' + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm:ss'),
  ].join('\n');
}

function aviso_(b, titulo, carpeta, total) {
  const cuerpo = [
    'Nuevo aporte en NotPull',
    '',
    'Universidad: ' + (b.universidad || 'UTEC'),
    'Curso: ' + (b.curso || ''),
    'Semana: ' + (b.semana || '—'),
    'Tipo: ' + (b.tipo || ''),
    'Archivos: ' + total,
    'De: ' + (b.usuario || '') + (b.email ? ' <' + b.email + '>' : ''),
    b.nota ? 'Nota: ' + b.nota : '',
    '',
    'Carpeta: ' + carpeta.getUrl(),
  ].filter(x => x !== '').join('\n');
  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    subject: '📤 NotPull · ' + titulo,
    body: cuerpo,
  });
}

function raiz_() {
  const it = DriveApp.getFoldersByName(RAIZ);
  return it.hasNext() ? it.next() : DriveApp.createFolder(RAIZ);
}

function limpio_(s) {
  return String(s).replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
