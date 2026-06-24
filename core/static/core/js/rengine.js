/* ============================================================
   rengine.js — Motor R real en el navegador (WebR / WebAssembly)
   + consolas educativas + carga/descarga Excel (SheetJS)
   Sin servidor R: todo corre en la máquina del alumno.
   Autor: César Ortiz Méndez · https://cv-cesarortiz.vercel.app
   ============================================================ */
import { WebR } from 'https://webr.r-wasm.org/latest/webr.mjs';

const STATUS = document.getElementById('engine-status');
const DOT = document.getElementById('engine-dot');

function setStatus(txt, state) {
  if (STATUS) STATUS.textContent = txt;
  if (DOT) { DOT.className = 'dot' + (state ? ' ' + state : ''); }
}

/* --- Singleton de WebR: una sola instancia para toda la página --- */
let webR = null;
let bootPromise = null;

async function boot() {
  if (bootPromise) return bootPromise;
  setStatus('R · descargando WASM…', '');
  bootPromise = (async () => {
    const r = new WebR({ interactive: false });
    await r.init();
    // semilla por defecto para reproducibilidad del curso
    await r.evalRVoid('set.seed(14256); options(warn=1)');
    webR = r;
    setStatus('R 4.6 · WASM · LISTO', 'ready');
    return r;
  })();
  return bootPromise;
}

/* Ejecuta código R y devuelve {text, images, error} */
async function runR(code) {
  const r = await boot();
  const shelter = await new r.Shelter();
  try {
    const res = await shelter.captureR(code, {
      withAutoprint: true,
      captureStreams: true,
      captureConditions: false,
      captureGraphics: { width: 460, height: 460, bg: 'white' },
    });
    const text = res.output
      .map(o => ({ stream: o.type, line: o.data }));
    const images = res.images || [];
    return { text, images, error: null };
  } catch (e) {
    return { text: [], images: [], error: (e && e.message) ? e.message : String(e) };
  } finally {
    shelter.purge();
  }
}

/* --- Pintar salida en un panel --- */
function renderOutput(panel, result) {
  panel.innerHTML = '';
  if (result.error) {
    const span = document.createElement('span');
    span.className = 'err';
    span.textContent = 'Error: ' + result.error + '\n';
    panel.appendChild(span);
  }
  for (const item of result.text) {
    const span = document.createElement('span');
    span.className = (item.stream === 'stderr') ? 'err' : '';
    span.textContent = item.line + '\n';
    panel.appendChild(span);
  }
  if (!result.error && result.text.length === 0 && result.images.length === 0) {
    panel.innerHTML = '<span class="m" style="color:#5d7186">[sin salida de texto]</span>';
  }
}

function renderPlots(box, images) {
  if (!box) return;
  if (!images.length) {
    box.innerHTML = '<div class="empty">Sin gráfico. Usa plot(), hist(), barplot()…</div>';
    return;
  }
  box.innerHTML = '';
  for (const img of images) {
    const canvas = document.createElement('canvas');
    canvas.width = img.width; canvas.height = img.height;
    canvas.getContext('2d').drawImage(img, 0, 0);
    box.appendChild(canvas);
  }
}

/* ============================================================
   Enlaza cada bloque .rconsole de la página
   ============================================================ */
function bindConsole(el) {
  const ta   = el.querySelector('textarea');
  const out  = el.querySelector('.output');
  const plot = el.querySelector('.plotbox');
  const runBtn   = el.querySelector('[data-act=run]');
  const clearBtn = el.querySelector('[data-act=clear]');
  const resetBtn = el.querySelector('[data-act=reset]');
  const xlsxIn   = el.querySelector('[data-act=loadxlsx]');
  const xlsxOut  = el.querySelector('[data-act=savexlsx]');
  const chip     = el.querySelector('.filechip');
  const original = ta ? ta.value : '';

  async function execute() {
    if (!ta) return;
    runBtn.disabled = true;
    const prev = runBtn.textContent;
    runBtn.textContent = '⟳ ejecutando…';
    if (out) out.innerHTML = '<span class="m" style="color:#5d7186">Corriendo R…</span>';
    const result = await runR(ta.value);
    renderOutput(out, result);
    renderPlots(plot, result.images);
    runBtn.disabled = false;
    runBtn.textContent = prev;
  }

  if (runBtn) runBtn.addEventListener('click', execute);
  if (clearBtn) clearBtn.addEventListener('click', () => {
    if (out) out.innerHTML = '';
    if (plot) plot.innerHTML = '<div class="empty">Sin gráfico.</div>';
  });
  if (resetBtn) resetBtn.addEventListener('click', () => { ta.value = original; });

  // Ctrl/Cmd + Enter para ejecutar
  if (ta) ta.addEventListener('keydown', (ev) => {
    if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); execute(); }
    // Tab inserta dos espacios
    if (ev.key === 'Tab') {
      ev.preventDefault();
      const s = ta.selectionStart, e = ta.selectionEnd;
      ta.value = ta.value.slice(0, s) + '  ' + ta.value.slice(e);
      ta.selectionStart = ta.selectionEnd = s + 2;
    }
  });

  /* --- Cargar Excel/CSV -> data.frame `datos` en R --- */
  if (xlsxIn) {
    const fileEl = el.querySelector('input[type=file]');
    xlsxIn.addEventListener('click', () => fileEl && fileEl.click());
    if (fileEl) fileEl.addEventListener('change', async (ev) => {
      const file = ev.target.files[0];
      if (!file) return;
      if (chip) chip.textContent = '⟳ cargando ' + file.name + '…';
      try {
        const buf = await file.arrayBuffer();
        const wb = XLSX.read(buf, { type: 'array' });
        const ws = wb.Sheets[wb.SheetNames[0]];
        const csv = XLSX.utils.sheet_to_csv(ws);
        const r = await boot();
        await r.FS.writeFile('/tmp/datos.csv', new TextEncoder().encode(csv));
        await r.evalRVoid('datos <- read.csv("/tmp/datos.csv", stringsAsFactors=TRUE, check.names=FALSE)');
        if (chip) chip.textContent = '✓ ' + file.name + ' → data.frame `datos`';
        if (out) {
          const result = await runR('cat("Datos cargados en el data.frame `datos`:\\n"); str(datos); head(datos)');
          renderOutput(out, result);
        }
      } catch (e) {
        if (chip) chip.textContent = '✗ error: ' + (e.message || e);
      }
    });
  }

  /* --- Exportar un data.frame de R a Excel --- */
  if (xlsxOut) {
    xlsxOut.addEventListener('click', async () => {
      const name = (prompt('¿Qué objeto R exportar a Excel? (data.frame o tabla)', 'datos') || '').trim();
      if (!name) return;
      try {
        const r = await boot();
        const exists = await r.evalRBoolean(`exists("${name}") && (is.data.frame(${name}) || is.matrix(${name}) || is.table(${name}))`);
        if (!exists) { alert(`'${name}' no existe o no es una tabla/data.frame.\nEjecuta primero el código que lo crea.`); return; }
        await r.evalRVoid(`.out <- as.data.frame(${name}); write.csv(.out, "/tmp/out.csv", row.names = !is.null(rownames(.out)) && is.matrix(${name}))`);
        const bytes = await r.FS.readFile('/tmp/out.csv');
        const csv = new TextDecoder().decode(bytes);
        const wb = XLSX.read(csv, { type: 'string' });
        XLSX.writeFile(wb, name + '_estadisticaR.xlsx');
      } catch (e) {
        alert('No se pudo exportar: ' + (e.message || e));
      }
    });
  }
}

/* --- Init global --- */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.rconsole').forEach(bindConsole);
  // Pre-calienta el motor para que el primer Run sea rápido
  boot().catch(() => setStatus('R · error de carga', 'err'));
});

window.__runR = runR;   // expuesto para el transformador CSV
window.__bootR = boot;
