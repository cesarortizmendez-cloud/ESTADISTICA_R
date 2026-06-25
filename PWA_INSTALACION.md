# Cambios PWA realizados

Se incorporó instalación como aplicación para Android, Windows e iPhone.

## Qué se agregó

- Manifest PWA en `/manifest.json`.
- Service worker en `/service-worker.js`.
- Botón flotante “Instalar en mi equipo”.
- Mensaje especial para iPhone/iPad.
- Íconos en `core/static/core/icons/`.
- Script `core/static/core/js/pwa-install.js`.

## Cómo subirlo

```bash
git add .
git commit -m "Agrega PWA e instalacion de EstadisticaR"
git push origin main
```

Vercel debería desplegar automáticamente desde la misma URL.
