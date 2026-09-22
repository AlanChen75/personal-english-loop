#!/usr/bin/env python3
"""Build a self-contained transcript-and-audio shadowing workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIO_ROOT = ROOT / "outputs/cacs2026-conference-audio"
APP_MANIFEST = {
    "id": "./",
    "name": "Personal English Loop",
    "short_name": "Shadow",
    "description": "播放研討會、自我介紹與每日英語教材，同步閱讀逐字稿並練習 Shadowing。",
    "lang": "zh-Hant",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#f4efe4",
    "theme_color": "#173a42",
    "prefer_related_applications": False,
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}
SERVICE_WORKER = r'''const CACHE_NAME = 'personal-english-loop-v3';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest?v=3',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  if (event.request.headers.has('range')) return;
  const requestUrl = new URL(event.request.url);
  if (requestUrl.origin !== self.location.origin) return;

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      if (response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      }
      return response;
    }))
  );
});
'''


def _safe_relative_name(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"{field} must stay inside the player directory")
    return path.as_posix()


def _load_items(manifest_path: Path, items: object) -> list[dict]:
    if not isinstance(items, list) or not items:
        raise ValueError("Every collection must contain at least one item")
    result = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Every item must be an object")
        number = item.get("number")
        title = item.get("title")
        if not isinstance(number, int) or number < 1:
            raise ValueError("Every item needs a positive integer number")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Every item needs a title")
        audio_name = _safe_relative_name(item.get("audio"), "audio")
        transcript_name = _safe_relative_name(item.get("spoken_transcript"), "spoken_transcript")
        audio_path = manifest_path.parent / audio_name
        transcript_path = manifest_path.parent / transcript_name
        if not audio_path.is_file():
            raise FileNotFoundError(audio_path)
        if not transcript_path.is_file():
            raise FileNotFoundError(transcript_path)
        transcript = transcript_path.read_text(encoding="utf-8").strip()
        if not transcript:
            raise ValueError(f"Transcript is empty: {transcript_path}")
        result.append(
            {
                "number": number,
                "title": title.strip(),
                "audio": audio_name,
                "transcript": transcript,
            }
        )
    return result


def load_collections(manifest_path: Path) -> list[dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    collections = manifest.get("collections")
    if collections is None:
        slides = manifest.get("slides")
        return [
            {
                "id": "conference",
                "title": "研討會講稿",
                "items": _load_items(manifest_path, slides),
            }
        ]
    if not isinstance(collections, list) or not collections:
        raise ValueError("Manifest must contain at least one collection")
    result = []
    for collection in collections:
        if not isinstance(collection, dict):
            raise ValueError("Every collection must be an object")
        collection_id = collection.get("id")
        title = collection.get("title")
        if not isinstance(collection_id, str) or not collection_id.strip():
            raise ValueError("Every collection needs an id")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Every collection needs a title")
        result.append(
            {
                "id": collection_id.strip(),
                "title": title.strip(),
                "items": _load_items(manifest_path, collection.get("items")),
            }
        )
    return result


def load_slides(manifest_path: Path) -> list[dict]:
    """Compatibility helper for callers that still expect one flat list."""
    return load_collections(manifest_path)[0]["items"]


def build_player(manifest_path: Path, output_path: Path) -> None:
    collections = load_collections(manifest_path)
    data = json.dumps(collections, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__COLLECTION_DATA__", data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    build_pwa_assets(output_path.parent)


def write_app_icon(path: Path, size: int) -> None:
    """Draw a safe-area PWA icon without depending on external assets."""
    image = Image.new("RGB", (size, size), "#f4efe4")
    draw = ImageDraw.Draw(image)
    margin = round(size * 0.16)
    radius = round(size * 0.09)
    draw.rounded_rectangle(
        (margin, margin, size - margin, size - margin),
        radius=radius,
        fill="#173a42",
    )
    play_left = round(size * 0.33)
    play_top = round(size * 0.31)
    play_bottom = round(size * 0.69)
    play_right = round(size * 0.61)
    draw.polygon(
        [(play_left, play_top), (play_left, play_bottom), (play_right, size // 2)],
        fill="#e58a3a",
    )
    line_left = round(size * 0.64)
    line_right = round(size * 0.72)
    line_width = max(2, round(size * 0.025))
    for y_ratio in (0.38, 0.5, 0.62):
        y = round(size * y_ratio)
        draw.line((line_left, y, line_right, y), fill="#f4efe4", width=line_width)
    image.save(path, format="PNG", optimize=True)


def build_pwa_assets(output_dir: Path) -> None:
    (output_dir / "manifest.webmanifest").write_text(
        json.dumps(APP_MANIFEST, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "service-worker.js").write_text(SERVICE_WORKER, encoding="utf-8")
    for size in (180, 192, 512):
        write_app_icon(output_dir / f"icon-{size}.png", size)


TEMPLATE = r'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#173a42">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="Shadow">
  <link rel="manifest" href="manifest.webmanifest?v=3">
  <link rel="apple-touch-icon" href="icon-180.png">
  <title>Personal English Loop</title>
  <style>
    :root {
      color-scheme: light;
      --ink: oklch(25% 0.035 215);
      --muted: oklch(48% 0.035 215);
      --paper: oklch(96% 0.018 78);
      --paper-deep: oklch(91% 0.025 78);
      --teal: oklch(37% 0.075 205);
      --orange: oklch(68% 0.15 48);
      --line: oklch(82% 0.035 78);
      --focus: oklch(55% 0.13 205);
      --display: "Avenir Next", Avenir, "Trebuchet MS", sans-serif;
      --reading: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    }

    * { box-sizing: border-box; }
    html { background: var(--paper-deep); scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      background:
        linear-gradient(90deg, var(--teal) 0 0.72rem, transparent 0.72rem),
        repeating-linear-gradient(0deg, transparent 0 2.95rem, color-mix(in oklch, var(--line), transparent 65%) 2.95rem 3rem),
        var(--paper);
      font-family: var(--display);
      padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(2rem, env(safe-area-inset-bottom)) max(1.75rem, env(safe-area-inset-left));
    }

    button, select, audio { font: inherit; }
    button:focus-visible, select:focus-visible, audio:focus-visible {
      outline: 3px solid var(--focus);
      outline-offset: 3px;
    }

    .shell { width: min(76rem, 100%); margin: 0 auto; }
    header {
      display: grid;
      gap: 0.4rem;
      padding: clamp(1rem, 3vw, 2.5rem) 0 clamp(1.5rem, 4vw, 3rem);
      border-bottom: 2px solid var(--ink);
    }
    .eyebrow {
      color: var(--teal);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }
    h1 {
      margin: 0;
      max-width: 18ch;
      font-size: clamp(2rem, 7vw, 5.2rem);
      font-weight: 650;
      letter-spacing: -0.055em;
      line-height: 0.98;
    }
    .lede { margin: 0.7rem 0 0; color: var(--muted); font-size: 1rem; }
    :is(h1, h2, p, .page-button) { text-wrap: pretty; overflow-wrap: break-word; }
    .install-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; margin-top: 0.8rem; }
    .install-button {
      min-height: 2.75rem;
      padding: 0.62rem 1rem;
      border: 1px solid var(--teal);
      border-radius: 999px;
      color: var(--paper);
      background: var(--teal);
      font-weight: 700;
      cursor: pointer;
    }
    .install-button:active { transform: translateY(1px); }
    .install-status { margin: 0; max-width: 48ch; color: var(--muted); font-size: 0.88rem; line-height: 1.55; }

    .workspace { display: grid; gap: 2rem; padding-top: clamp(1.5rem, 4vw, 3rem); }
    nav { min-width: 0; }
    .select-label { display: grid; gap: 0.35rem; margin-bottom: 0.85rem; color: var(--muted); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.06em; }
    .collection-select, .mobile-select { width: 100%; min-height: 3rem; padding: 0.65rem 0.8rem; border: 1px solid var(--ink); background: var(--paper); color: var(--ink); }
    .page-list { display: none; list-style: none; margin: 0; padding: 0; }
    .page-button {
      width: 100%;
      display: grid;
      grid-template-columns: 2.2rem 1fr;
      gap: 0.6rem;
      min-height: 3.2rem;
      padding: 0.7rem 0;
      color: var(--muted);
      background: transparent;
      border: 0;
      border-bottom: 1px solid var(--line);
      text-align: left;
      cursor: pointer;
    }
    .page-button[aria-current="true"] { color: var(--ink); font-weight: 650; }
    .page-button[aria-current="true"] .number { color: var(--orange); }
    .number { font-variant-numeric: tabular-nums; font-weight: 750; }

    main { min-width: 0; }
    .page-meta { display: flex; align-items: baseline; gap: 0.7rem; color: var(--teal); }
    .page-meta span { font-weight: 750; font-variant-numeric: tabular-nums; }
    h2 { margin: 0.4rem 0 1.5rem; font-size: clamp(1.55rem, 4vw, 2.8rem); line-height: 1.12; letter-spacing: -0.035em; }

    .player-desk {
      position: sticky;
      top: 0.75rem;
      z-index: 2;
      display: grid;
      gap: 0.8rem;
      padding: 1rem;
      color: var(--paper);
      background: var(--ink);
      border-radius: 0.2rem;
      box-shadow: 0 0.8rem 2.5rem color-mix(in oklch, var(--ink), transparent 78%);
    }
    audio { width: 100%; min-height: 3.2rem; }
    .controls { display: flex; flex-wrap: wrap; gap: 0.55rem; align-items: center; }
    .controls button, .loop-label {
      min-height: 2.75rem;
      padding: 0.55rem 0.8rem;
      border: 1px solid color-mix(in oklch, var(--paper), transparent 56%);
      border-radius: 999px;
      color: inherit;
      background: transparent;
    }
    .controls button { cursor: pointer; }
    .controls button[aria-pressed="true"] { color: var(--ink); background: var(--orange); border-color: var(--orange); }
    .loop-label { display: inline-flex; align-items: center; gap: 0.45rem; margin-left: auto; }
    .status { grid-column: 1 / -1; margin: 0; color: color-mix(in oklch, var(--paper), transparent 25%); font-size: 0.82rem; line-height: 1.4; }

    .transcript {
      margin-top: clamp(2rem, 5vw, 4rem);
      max-width: 67ch;
      font-family: var(--reading);
      font-size: clamp(1.22rem, 2.2vw, 1.58rem);
      line-height: 1.78;
      letter-spacing: 0.006em;
    }
    .sentence { display: inline; transition: background-color 180ms ease-out; }
    .sentence:hover { background: color-mix(in oklch, var(--orange), transparent 70%); }
    .sentence::after { content: " "; }
    .practice-note { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--line); color: var(--muted); font-size: 0.9rem; line-height: 1.6; }

    @media (min-width: 48rem) {
      body { padding-left: max(2.5rem, env(safe-area-inset-left)); }
      .workspace { grid-template-columns: minmax(13rem, 0.68fr) minmax(0, 2fr); align-items: start; gap: clamp(2rem, 6vw, 6rem); }
      nav { position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow: auto; }
      .mobile-select { display: none; }
      .page-list { display: block; }
      .player-desk { grid-template-columns: minmax(16rem, 1fr) auto; align-items: center; }
      .controls { justify-content: flex-end; }
    }

    @media (hover: hover) {
      .page-button:hover { color: var(--ink); transform: translateX(0.18rem); }
      .controls button:hover { border-color: var(--orange); }
    }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } * { transition: none !important; } }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="eyebrow">Personal English Loop · practice desk</div>
      <h1>Listen. Read. Shadow.</h1>
      <p class="lede">選擇分類與教材，讓音檔與英文逐字稿保持在同一個畫面。</p>
      <div class="install-row">
        <button id="install-app" class="install-button" type="button" aria-describedby="install-status">安裝到手機</button>
        <p id="install-status" class="install-status" aria-live="polite">安裝後可從手機桌面直接開啟。</p>
      </div>
    </header>

    <div class="workspace">
      <nav aria-label="教材清單">
        <label class="select-label">練習分類
          <select id="collection-select" class="collection-select" aria-label="選擇練習分類"></select>
        </label>
        <select id="page-select" class="mobile-select" aria-label="選擇教材"></select>
        <ol id="page-list" class="page-list"></ol>
      </nav>

      <main id="main-content">
        <div class="page-meta"><span id="page-number">01</span><small id="collection-title">教材</small></div>
        <h2 id="page-title"></h2>

        <section class="player-desk" aria-label="Shadowing 播放控制">
          <audio id="practice-audio" controls preload="metadata"></audio>
          <div class="controls">
            <button id="rewind" type="button" title="倒退五秒">↶ 5 秒</button>
            <button class="speed" type="button" data-speed="0.8">0.8×</button>
            <button class="speed" type="button" data-speed="0.9">0.9×</button>
            <button class="speed" type="button" data-speed="1" aria-pressed="true">1×</button>
            <button id="repeat-all" type="button" aria-pressed="false">Repeat All</button>
            <label class="loop-label"><input id="loop" type="checkbox"> 重複本頁</label>
          </div>
          <p id="player-status" class="status" aria-live="polite"></p>
        </section>

        <article id="transcript" class="transcript" aria-live="polite"></article>
        <p class="practice-note">快捷鍵：空白鍵播放／暫停，← → 倒退或前進五秒。點選左側可切換下一頁。</p>
      </main>
    </div>
  </div>

  <script>
    const collections = __COLLECTION_DATA__;
    const audio = document.querySelector('#practice-audio');
    const title = document.querySelector('#page-title');
    const number = document.querySelector('#page-number');
    const collectionTitle = document.querySelector('#collection-title');
    const transcript = document.querySelector('#transcript');
    const list = document.querySelector('#page-list');
    const select = document.querySelector('#page-select');
    const collectionSelect = document.querySelector('#collection-select');
    const speedButtons = [...document.querySelectorAll('.speed')];
    const repeatAll = document.querySelector('#repeat-all');
    const repeatPage = document.querySelector('#loop');
    const playerStatus = document.querySelector('#player-status');
    const installButton = document.querySelector('#install-app');
    const installStatus = document.querySelector('#install-status');
    const requestedCollection = decodeURIComponent(window.location.hash.slice(1));
    const requestedCollectionIndex = collections.findIndex(collection => collection.id === requestedCollection);
    let activeCollectionIndex = requestedCollectionIndex >= 0 ? requestedCollectionIndex : 0;
    let activeIndex = 0;
    let speed = 1;
    let installPrompt = null;

    const sentenceParts = text => text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [text];

    function renderTranscript(text) {
      transcript.replaceChildren(...sentenceParts(text).map(sentence => {
        const span = document.createElement('span');
        span.className = 'sentence';
        span.textContent = sentence.trim();
        return span;
      }));
    }

    function activeItems() {
      return collections[activeCollectionIndex].items;
    }

    function loadItem(index, shouldFocus = false) {
      activeIndex = index;
      const item = activeItems()[index];
      audio.pause();
      audio.src = item.audio;
      audio.playbackRate = speed;
      playerStatus.textContent = '';
      number.textContent = String(item.number).padStart(2, '0');
      collectionTitle.textContent = collections[activeCollectionIndex].title;
      title.textContent = item.title;
      renderTranscript(item.transcript);
      select.value = String(index);
      document.querySelectorAll('.page-button').forEach((button, buttonIndex) => {
        button.setAttribute('aria-current', buttonIndex === index ? 'true' : 'false');
      });
      if (shouldFocus) title.scrollIntoView({behavior: 'smooth', block: 'start'});
    }

    function renderItemList() {
      select.replaceChildren();
      list.replaceChildren();
      activeItems().forEach((item, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `${String(item.number).padStart(2, '0')} · ${item.title}`;
        select.append(option);

        const listItem = document.createElement('li');
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'page-button';
        button.innerHTML = `<span class="number">${String(item.number).padStart(2, '0')}</span><span></span>`;
        button.lastElementChild.textContent = item.title;
        button.addEventListener('click', () => loadItem(index, true));
        listItem.append(button);
        list.append(listItem);
      });
    }

    collections.forEach((collection, index) => {
      const option = document.createElement('option');
      option.value = index;
      option.textContent = `${collection.title} · ${collection.items.length}`;
      collectionSelect.append(option);
    });

    collectionSelect.addEventListener('change', event => {
      activeCollectionIndex = Number(event.target.value);
      window.history.replaceState(null, '', `#${collections[activeCollectionIndex].id}`);
      renderItemList();
      loadItem(0);
    });
    select.addEventListener('change', event => loadItem(Number(event.target.value)));
    document.querySelector('#rewind').addEventListener('click', () => { audio.currentTime = Math.max(0, audio.currentTime - 5); });
    repeatPage.addEventListener('change', event => {
      audio.loop = event.target.checked;
      if (event.target.checked) repeatAll.setAttribute('aria-pressed', 'false');
    });
    repeatAll.addEventListener('click', () => {
      const enabled = repeatAll.getAttribute('aria-pressed') !== 'true';
      repeatAll.setAttribute('aria-pressed', enabled ? 'true' : 'false');
      if (enabled) {
        repeatPage.checked = false;
        audio.loop = false;
      }
    });
    audio.addEventListener('ended', () => {
      if (repeatAll.getAttribute('aria-pressed') !== 'true') return;
      loadItem((activeIndex + 1) % activeItems().length);
      audio.play().catch(error => {
        console.error('Repeat All playback was interrupted', error);
        playerStatus.textContent = '瀏覽器暫停了連續播放，請按播放繼續。';
      });
    });
    speedButtons.forEach(button => button.addEventListener('click', () => {
      speed = Number(button.dataset.speed);
      audio.playbackRate = speed;
      speedButtons.forEach(item => item.setAttribute('aria-pressed', item === button ? 'true' : 'false'));
    }));
    window.addEventListener('beforeinstallprompt', event => {
      event.preventDefault();
      installPrompt = event;
      installStatus.textContent = '已可安裝，點擊按鈕後確認即可。';
    });
    installButton.addEventListener('click', async () => {
      if (window.matchMedia('(display-mode: standalone)').matches) {
        installStatus.textContent = '這個練習頁已經安裝在裝置上。';
        return;
      }
      if (!installPrompt) {
        installStatus.textContent = '若未出現安裝視窗，請重新整理一次，或從 Chrome 選單選擇「安裝應用程式」。';
        return;
      }
      installPrompt.prompt();
      const choice = await installPrompt.userChoice;
      installStatus.textContent = choice.outcome === 'accepted' ? '安裝完成，可從手機桌面開啟。' : '尚未安裝，你可以稍後再試。';
      installPrompt = null;
    });
    window.addEventListener('appinstalled', () => {
      installButton.hidden = true;
      installStatus.textContent = '安裝完成，可從手機桌面開啟。';
    });
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js').catch(error => {
          console.error('Service worker registration failed', error);
          installStatus.textContent = '安裝元件載入失敗，請重新整理後再試。';
        });
      });
    }
    document.addEventListener('keydown', event => {
      if (['INPUT', 'SELECT', 'BUTTON'].includes(document.activeElement.tagName)) return;
      if (event.code === 'Space') { event.preventDefault(); audio.paused ? audio.play() : audio.pause(); }
      if (event.key === 'ArrowLeft') audio.currentTime = Math.max(0, audio.currentTime - 5);
      if (event.key === 'ArrowRight') audio.currentTime = Math.min(audio.duration || Infinity, audio.currentTime + 5);
    });

    collectionSelect.value = String(activeCollectionIndex);
    renderItemList();
    loadItem(0);
  </script>
</body>
</html>
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_AUDIO_ROOT / "generation-manifest.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_AUDIO_ROOT / "shadowing-player.html",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_player(args.manifest, args.output)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
