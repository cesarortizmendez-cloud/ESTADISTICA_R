# EstadísticaR · Terminal Estadístico

> **Software abierto de aprendizaje de estadística con R**, creado por el **Dr. César Ortiz Méndez** — [cv-cesarortiz.vercel.app](https://cv-cesarortiz.vercel.app)

Webapp educativa en **Django** para aprender **estadística con R**, directamente en el navegador.
Cada una de las **11 lecciones**
es una app Django con su propia **consola de R real, funcional**, capaz de **cargar Excel** y
**exportar a Excel**. Incluye dos módulos extra: **Data Frames & Minería de datos** y un
**Transformador automático de CSV → tablas de frecuencia**.

- **R de verdad en el navegador** vía [WebR](https://webr.r-wasm.org/) (R 4.x compilado a WebAssembly). No hay servidor de R.
- **Sin base de datos, sin usuarios, libre acceso.** Nada se almacena.
- **Excel I/O** con [SheetJS](https://sheetjs.com/).
- **Estética hacker / terminal** (fósforo verde, cian, magenta, ámbar).
- **Despliegue en Vercel** desde GitHub.

---

## Contenido

| Ruta | Módulo |
|------|--------|
| `/` | Inicio |
| `/cap/01/` … `/cap/11/` | Las 11 lecciones |
| `/dataframes/` | Data Frames & Minería de datos (extra) |
| `/transformador/` | Transformador CSV → tablas (extra) |
| `/consola/` | Consola R libre |
| `/ayuda-r/` | Hoja de referencia R |

Lecciones: 1) Conceptos · 2) Tablas de frecuencia (Sturges) · 3) Gráficos · 4) Posición ·
5) Dispersión/asimetría/curtosis · 6) Bivariado y regresión · 7) Probabilidades ·
8) Condicional y Bayes · 9) V.A. discretas · 10) V.A. continuas · 11) Intervalos de confianza.



## Instalación como app en Android, Windows e iPhone

El proyecto está preparado como **PWA**. Al abrir `https://estadistica-r.vercel.app/`, la aplicación puede instalarse como ícono en el celular, tablet o computador.

- **Android / Windows / Chrome / Edge:** aparece el botón **“Instalar en mi equipo”** dentro de la aplicación. Al presionarlo, el navegador pide confirmación y crea el ícono.
- **iPhone / iPad:** iOS no permite abrir automáticamente la ventana de instalación. La aplicación muestra una guía: abrir en Safari, tocar **Compartir** y seleccionar **Agregar a pantalla de inicio**.

Archivos incorporados:

```text
core/static/core/icons/icon-192.png
core/static/core/icons/icon-512.png
core/static/core/icons/icon-maskable-512.png
core/static/core/icons/apple-touch-icon.png
core/static/core/icons/favicon-32.png
core/static/core/js/pwa-install.js
/manifest.json
/service-worker.js
```

---

## Desarrollo local (Windows · command prompt)

Necesitas **Python 3.10+** instalado.

```cmd
:: 1. Clonar el repositorio
git clone https://github.com/cesarortizmendez-cloud/ESTADISTICA_R.git
cd ESTADISTICA_R

:: 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate

:: 3. Instalar dependencias
pip install -r requirements.txt

:: 4. Recolectar estáticos (opcional en local) y levantar el servidor
python manage.py collectstatic --noinput
python manage.py runserver
```

Abre **http://127.0.0.1:8000/** en el navegador.

> La **primera** vez que ejecutes código R, el navegador descarga el motor WebR (unos MB de
> WebAssembly). Tarda unos segundos; luego queda en caché y es instantáneo. La barra de estado
> superior muestra `R 4.x · WASM · LISTO` cuando el motor está disponible.

Para editar: abre la carpeta en **VS Code** (`code .`).

---

## Despliegue en Vercel (desde GitHub)

1. Sube el proyecto a un repositorio de GitHub:

   ```cmd
   git init
   git add .
   git commit -m "EstadísticaR inicial"
   git branch -M main
   git remote add origin https://github.com/cesarortizmendez-cloud/ESTADISTICA_R.git
   git push -u origin main
   ```

2. En [vercel.com](https://vercel.com): **Add New → Project → Import** tu repo.
3. Vercel detecta `vercel.json` automáticamente. No necesitas configurar nada más.
   (Opcional: en *Settings → Environment Variables* define `DJANGO_DEBUG=False`.)
4. **Deploy.** Cada `git push` vuelve a desplegar.

### ¿Cómo está configurado el deploy?

- `vercel.json` define dos builds: uno **estático** (`build_files.sh`, que instala dependencias y
  ejecuta `collectstatic` dejando todo en `staticfiles/`) y una **función Python** (`config/wsgi.py`,
  que expone la variable `app` que Vercel necesita).
- Las rutas `/static/*` se sirven desde el CDN; el resto va a la función Django.
- Se usa `CompressedStaticFilesStorage` (sin manifest con hashes) para no depender de un manifest
  en el filesystem de solo lectura de Vercel.

---

## Cómo se usan las consolas

- Escribe R en el editor y presiona **Ctrl + Enter** (o el botón **ejecutar**).
- **cargar excel**: importa un `.xlsx`/`.csv` como el data frame **`datos`**.
- **exportar excel**: descarga cualquier data frame o tabla de R como `.xlsx`.
- Los datasets clásicos de R (`iris`, `mtcars`, `airquality`, …) ya están disponibles.

### Transformador CSV → tablas

Sube un archivo, elige una columna y pulsa **generar tabla**:
- columna **numérica** → tabla de frecuencias por intervalos (regla de **Sturges**) + histograma;
- columna **categórica** → conteo por categoría + gráfico de barras.
La tabla resultante (`frecuencias`) se exporta a Excel con un clic.

---

## Estructura del proyecto

```
estadistica_r/
├─ config/            # settings, urls, wsgi (sin BD)
├─ core/              # núcleo: vistas base, currículo, estáticos y plantillas
│  ├─ curriculum*.py  # contenido de los 11 capítulos + data frames
│  ├─ static/core/    # app.css (diseño) y rengine.js (motor WebR + Excel)
│  └─ templates/core/ # base de plantillas reutilizables
├─ apps/
│  ├─ cap01 … cap11/  # una app Django por capítulo
│  ├─ dataframes/     # módulo extra
│  └─ transformador/  # módulo extra
├─ templates/base.html
├─ requirements.txt
├─ vercel.json · build_files.sh
└─ manage.py
```

---

## Notas técnicas

- **WebR** corre por el canal automático (no requiere cabeceras COOP/COEP). Si quieres acelerar el
  arranque usando `SharedArrayBuffer`, puedes servir con las cabeceras
  `Cross-Origin-Opener-Policy: same-origin` y `Cross-Origin-Embedder-Policy: require-corp`,
  pero no es necesario y puede complicar la carga de CDNs.
- No se persiste ningún dato del alumno: los archivos cargados viven solo en memoria del navegador.

## Autor y licencia de uso

Creado por el **Dr. César Ortiz Méndez**
Portafolio: [cv-cesarortiz.vercel.app](https://cv-cesarortiz.vercel.app)

**EstadísticaR** es un software abierto de aprendizaje de estadística con R: libre para
estudiar, usar y compartir con fines educativos. El código, el diseño y el contenido
pedagógico son obra del Dr. César Ortiz Méndez. Si lo reutilizas o adaptas, por favor
mantén la atribución a su autor.
