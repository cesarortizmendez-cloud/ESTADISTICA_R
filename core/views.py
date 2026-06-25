# -*- coding: utf-8 -*-
"""Vistas del nucleo: portada, consola libre y hoja de referencia R."""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from .curriculum import nav_list, DATAFRAMES


def home(request):
    return render(request, "core/home.html", {
        "chapters": nav_list(),
        "active": "home",
    })


CONSOLE_SEED = """# Consola R libre — escribe y presiona Ctrl+Enter
# Datasets de R ya disponibles: iris, mtcars, airquality, ...

x <- c(12, 7, 9, 15, 22, 8, 14, 19, 11, 6)
cat("media   :", mean(x), "\\n")
cat("mediana :", median(x), "\\n")
cat("sd      :", sd(x), "\\n")

summary(mtcars[, c("mpg","hp","wt")])

hist(x, col = "#00ff9c", border = "#0b0f14",
     main = "Mi primer histograma", xlab = "valores")
"""


def console(request):
    """Consola R libre, sin contenido de capitulo."""
    return render(request, "core/console.html", {
        "chapters": nav_list(),
        "active": "console",
        "seed": CONSOLE_SEED,
    })


CHEATSHEET = [
    {"titulo": "Crear y manipular datos", "filas": [
        ("c()", "Combina valores en un vector", 'x <- c(4, 8, 15, 16, 23)'),
        ("seq()", "Secuencia de números", 'seq(1, 10, by=2)'),
        ("rep()", "Repite valores", 'rep("a", 3)'),
        ("data.frame()", "Crea una tabla (data frame)", 'data.frame(a=1:3, b=c("x","y","z"))'),
        ("factor()", "Variable categórica", 'factor(c("bajo","alto","bajo"))'),
        ("cut()", "Agrupa numérico en intervalos", 'cut(x, breaks=3)'),
    ]},
    {"titulo": "Estadígrafos de posición", "filas": [
        ("mean()", "Media aritmética", 'mean(x)'),
        ("median()", "Mediana", 'median(x)'),
        ("quantile()", "Cuartiles y percentiles", 'quantile(x, 0.25)'),
        ("table()", "Frecuencias / moda", 'table(x)'),
        ("summary()", "Resumen de 6 números", 'summary(x)'),
    ]},
    {"titulo": "Dispersión y forma", "filas": [
        ("var()", "Varianza", 'var(x)'),
        ("sd()", "Desviación estándar", 'sd(x)'),
        ("range()", "Mínimo y máximo", 'range(x)'),
        ("IQR()", "Rango intercuartílico", 'IQR(x)'),
        ("scale()", "Estandariza (z-score)", 'scale(x)'),
    ]},
    {"titulo": "Bivariado y modelos", "filas": [
        ("cov()", "Covarianza", 'cov(x, y)'),
        ("cor()", "Correlación de Pearson", 'cor(x, y)'),
        ("lm()", "Regresión lineal", 'lm(y ~ x)'),
        ("predict()", "Predice con un modelo", 'predict(modelo)'),
        ("aggregate()", "Resumen por grupos", 'aggregate(y ~ g, data, mean)'),
    ]},
    {"titulo": "Probabilidad y distribuciones", "filas": [
        ("dbinom()", "Probabilidad binomial", 'dbinom(2, 10, 0.3)'),
        ("dpois()", "Probabilidad de Poisson", 'dpois(3, lambda=2)'),
        ("pnorm()", "Acumulada normal", 'pnorm(1.96)'),
        ("qnorm()", "Cuantil normal (z)", 'qnorm(0.975)'),
        ("dexp()", "Densidad exponencial", 'dexp(1, rate=0.5)'),
        ("t.test()", "Prueba t / intervalo confianza", 't.test(x)'),
    ]},
    {"titulo": "Gráficos base", "filas": [
        ("hist()", "Histograma", 'hist(x, col="#00ff9c")'),
        ("barplot()", "Gráfico de barras", 'barplot(table(x))'),
        ("boxplot()", "Diagrama de caja", 'boxplot(x)'),
        ("pie()", "Gráfico de torta", 'pie(table(g))'),
        ("plot()", "Dispersión / general", 'plot(x, y)'),
        ("abline()", "Agrega una recta", 'abline(lm(y~x))'),
    ]},
    {"titulo": "Inspeccionar y limpiar", "filas": [
        ("str()", "Estructura de un objeto", 'str(datos)'),
        ("head()", "Primeras filas", 'head(datos, 5)'),
        ("dim()", "Filas x columnas", 'dim(datos)'),
        ("is.na()", "Detecta faltantes", 'colSums(is.na(datos))'),
        ("na.omit()", "Elimina filas con NA", 'na.omit(datos)'),
        ("read.csv()", "Lee un CSV", 'read.csv("archivo.csv")'),
    ]},
]


def cheatsheet(request):
    return render(request, "core/cheatsheet.html", {
        "chapters": nav_list(),
        "active": "cheatsheet",
        "grupos": CHEATSHEET,
    })


def manifest(request):
    """Manifest PWA para instalar EstadísticaR en Android, Windows e iPhone."""
    data = {
        "id": "/",
        "name": "EstadísticaR · Terminal Estadístico",
        "short_name": "EstadísticaR",
        "description": "Aplicación educativa para aprender estadística ejecutando R real en el navegador.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#070b11",
        "theme_color": "#00ff9c",
        "orientation": "portrait-primary",
        "lang": "es-CL",
        "categories": ["education", "productivity"],
        "icons": [
            {"src": "/static/core/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/static/core/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/static/core/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
        ],
        "shortcuts": [
            {"name": "Consola R libre", "short_name": "Consola", "description": "Abrir la consola libre para practicar código R.", "url": "/consola/", "icons": [{"src": "/static/core/icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Referencia R", "short_name": "Ayuda R", "description": "Abrir la hoja de referencia rápida de R.", "url": "/ayuda-r/", "icons": [{"src": "/static/core/icons/icon-192.png", "sizes": "192x192"}]}
        ]
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})


@never_cache
def service_worker(request):
    """Service worker en la raíz del sitio para habilitar instalación PWA."""
    content = r'''
const CACHE_NAME = 'estadistica-r-pwa-v1';
const APP_SHELL = [
  '/',
  '/manifest.json',
  '/static/core/css/app.css',
  '/static/core/js/rengine.js',
  '/static/core/js/pwa-install.js',
  '/static/core/icons/icon-192.png',
  '/static/core/icons/icon-512.png',
  '/static/core/icons/icon-maskable-512.png',
  '/static/core/icons/apple-touch-icon.png',
  '/static/core/icons/favicon-32.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => Promise.all(APP_SHELL.map((url) => {
        return fetch(url).then((response) => {
          if (response.ok) return cache.put(url, response);
          return null;
        }).catch(() => null);
      })))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((key) => key === CACHE_NAME ? null : caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      fetch(request).then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        return response;
      }).catch(() => caches.match(request))
    );
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => caches.match('/')));
  }
});
'''.strip()
    response = HttpResponse(content, content_type="application/javascript; charset=utf-8")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Service-Worker-Allowed"] = "/"
    return response

