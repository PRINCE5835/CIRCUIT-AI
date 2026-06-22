/// <reference lib="webworker" />

const CACHE_NAME = 'breadboard-cache-v1';

const CRITICAL_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.png',
  '/icons/Icon-192.png',
  '/icons/Icon-512.png',
  '/icons/Icon-maskable-192.png',
  '/icons/Icon-maskable-512.png',
];

const API_CACHE = 'breadboard-api-v1';
const API_PREFIXES = [
  '/v1/components',
  '/v1/health',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CRITICAL_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME && key !== API_CACHE)
          .map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  if (event.request.method !== 'GET') return;
  if (url.pathname.startsWith('/v1/')) {
    return event.respondWith(networkFirst(event.request));
  }

  if (
    url.origin === self.location.origin &&
    (url.pathname === '/' || url.pathname.startsWith('/icons/') || url.pathname === '/manifest.json' || url.pathname === '/favicon.png')
  ) {
    return event.respondWith(cacheFirst(event.request));
  }

  event.respondWith(networkFirst(event.request));
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  return cached || fetchAndCache(request);
}

async function networkFirst(request) {
  try {
    const response = await fetchAndCache(request);
    return response;
  } catch (e) {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response('Offline', { status: 503 });
  }
}

async function fetchAndCache(request) {
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(
      request.url.includes('/v1/') ? API_CACHE : CACHE_NAME
    );
    cache.put(request, response.clone());
  }
  return response;
}
