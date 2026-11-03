/* Enkel offline-støtte: alt lagres første gang appen åpnes med nett. */
const CACHE = 'jorda-rundt-v35';   // øk tallet (v36, v37 …) når du oppdaterer spillet
const FILES = [
  './', './index.html', './manifest.webmanifest',
  './icons/apple-touch-icon.png', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png',
  './fonts/lilita-one-latin-400-normal.woff2', './fonts/nunito-latin-600-normal.woff2',
  './fonts/nunito-latin-700-normal.woff2', './fonts/nunito-latin-800-normal.woff2'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  /* listene over bilder og ikoner hentes først fra nettet, så nye ikoner dukker opp uten at versjonen må økes */
  const path = new URL(e.request.url).pathname;
  if (/\/(emoji|photos)\.json$/.test(path)) {
    e.respondWith(fetch(e.request).then(res => {
      if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(hit => hit || new Response('{}', { status: 404 }))));
    return;
  }
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request).then(res => {
      if (res && res.ok && new URL(e.request.url).origin === location.origin) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy));
      }
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
