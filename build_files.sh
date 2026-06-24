#!/bin/bash
# Vercel ejecuta este script en el build (@vercel/static-build).
# Instala dependencias y recolecta los archivos estaticos en /staticfiles.
set -e

echo "==> Instalando dependencias de Python"
pip install -r requirements.txt

echo "==> Recolectando archivos estaticos"
python3 manage.py collectstatic --noinput --clear

echo "==> Build completado"
