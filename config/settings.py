# -*- coding: utf-8 -*-
"""
Configuracion del proyecto EstadisticaR.
Sin base de datos, sin usuarios. Pensado para Vercel + WhiteNoise.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad / entorno ------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-cambiala-en-produccion-14256-estadistica-r"
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Vercel sirve bajo *.vercel.app; permitimos todo porque no hay datos sensibles.
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# --- Apps ---------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.staticfiles",   # unica contrib necesaria (no hay DB/users)
    "core",
    "apps.cap01",
    "apps.cap02",
    "apps.cap03",
    "apps.cap04",
    "apps.cap05",
    "apps.cap06",
    "apps.cap07",
    "apps.cap08",
    "apps.cap09",
    "apps.cap10",
    "apps.cap11",
    "apps.dataframes",
    "apps.transformador",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # sirve estaticos en Vercel
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.app"

# --- Sin base de datos --------------------------------------------------
DATABASES = {}   # el proyecto no persiste nada

# --- Internacionalizacion ----------------------------------------------
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# --- Archivos estaticos (WhiteNoise) -----------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

STORAGES = {
    "staticfiles": {
        # Comprime pero NO usa manifest con hashes: evita que el manifest
        # falle en el filesystem de solo lectura de Vercel y que la funcion
        # Python tenga que leer staticfiles.json en tiempo de request.
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
