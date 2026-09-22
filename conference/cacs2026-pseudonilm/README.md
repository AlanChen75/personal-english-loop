# Personal English Loop Shadowing Player

同一個手機播放器收錄研討會講稿、自我介紹與每日英語教材。

## 手機播放

[開啟 Shadowing 播放器](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/)

播放器功能：

- 可安裝為手機桌面 Web App
- 三類教材：研討會講稿、自我介紹、每日練習
- 每段音檔與英文逐字稿同步顯示
- 0.8×、0.9×、1.0× 播放速度
- 倒退 5 秒
- 重複本頁
- Repeat All：自動播放同一分類的下一段，最後一段後回到第一段

## 檔案

- `index.html`：手機及桌面 Shadowing 播放器
- `manifest.webmanifest`：手機安裝資訊
- `service-worker.js`：Web App 啟動與快取
- `library-manifest.json`：播放器分類與教材索引
- `icon-180.png`、`icon-192.png`、`icon-512.png`：桌面圖示
- `cacs2026-full-talk.mp3`：完整研討會講稿
- `slide-01...slide-10.mp3`：逐頁音檔
- `slide-01...slide-10.txt`：逐頁英文講稿
- `pronunciation-guide.mp3`：專有名詞發音
- `pronunciation-guide.txt`：專有名詞文字稿

新增音檔由地端 RTX 3090 的 Qwen3-TTS 複製聲音產生。音檔為 24 kHz、單聲道、96 kbps MP3，輸出響度目標為 -16 LUFS，沒有改變原始生成語速。
