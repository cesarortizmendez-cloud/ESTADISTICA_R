#!/bin/bash
# Vercel ejecuta este script durante el build.
# Se crea un entorno virtual para evitar el error:
# externally-managed-environment / PEP 668.

set -e

echo "==> Creando entorno virtual de Python"
python3 -m venv .venv

echo "==> Activando entorno virtual"
source .venv/bin/activate

echo "==> Actualizando pip dentro del entorno virtual"
python -m pip install --upgrade pip

echo "==> Instalando dependencias de Python"
python -m pip install -r requirements.txt

echo "==> Recolectando archivos estaticos"
python manage.py collectstatic --noinput --clear

echo "==> Build completado"