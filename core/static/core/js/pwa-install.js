/* ============================================================
   pwa-install.js — Botón de instalación PWA para EstadísticaR
   Android/Windows: dispara la ventana nativa cuando está disponible.
   iPhone/iPad: muestra instrucciones para agregar a pantalla de inicio.
   ============================================================ */
(function () {
  const card = document.getElementById('install-card');
  const button = document.getElementById('pwa-install-btn');
  const close = document.getElementById('pwa-install-close');
  const text = document.getElementById('pwa-install-text');
  const iosHelp = document.getElementById('pwa-ios-help');
  if (!card || !button) return;
  let deferredPrompt = null;
  const DISMISS_KEY = 'estadisticaR_install_dismissed_until';
  const isIOS = /iphone|ipad|ipod/i.test(window.navigator.userAgent);
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
  function isDismissed() {
    const dismissedUntil = Number(localStorage.getItem(DISMISS_KEY) || 0);
    return dismissedUntil && dismissedUntil > Date.now();
  }
  function showCard(mode) {
    if (isStandalone || isDismissed()) return;
    card.hidden = false;
    if (mode === 'ios') {
      button.hidden = true;
      if (iosHelp) iosHelp.hidden = false;
      if (text) text.textContent = 'En iPhone la instalación se realiza desde Safari con “Agregar a pantalla de inicio”.';
      return;
    }
    button.hidden = false;
    if (iosHelp) iosHelp.hidden = true;
    if (text) text.textContent = 'Presiona el botón y confirma la instalación para dejarla como app en tu equipo.';
  }
  function hideCard(days) {
    card.hidden = true;
    if (days) {
      localStorage.setItem(DISMISS_KEY, String(Date.now() + days * 24 * 60 * 60 * 1000));
    }
  }
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/service-worker.js', { scope: '/' }).catch(function () {});
    });
  }
  window.addEventListener('beforeinstallprompt', function (event) {
    event.preventDefault();
    deferredPrompt = event;
    showCard('prompt');
  });
  button.addEventListener('click', async function () {
    if (!deferredPrompt) {
      showCard(isIOS ? 'ios' : 'prompt');
      return;
    }
    deferredPrompt.prompt();
    try {
      const choice = await deferredPrompt.userChoice;
      hideCard(choice && choice.outcome === 'accepted' ? 365 : 7);
    } finally {
      deferredPrompt = null;
    }
  });
  if (close) close.addEventListener('click', function () { hideCard(14); });
  window.addEventListener('appinstalled', function () { hideCard(365); });
  window.addEventListener('load', function () {
    if (isIOS && !isStandalone && !isDismissed()) {
      setTimeout(function () { showCard('ios'); }, 900);
    }
  });
})();
