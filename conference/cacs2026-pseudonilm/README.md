# Personal English Loop Shadowing Player

同一個手機播放器收錄 Automation 2026、CACS 2026、自我介紹與每日英語教材。

## 手機播放

[開啟 Shadowing 播放器](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/)

播放器功能：

- 可安裝為手機桌面 Web App
- 四類教材：Automation 2026、CACS 2026、自我介紹、每日練習
- Automation 2026 是預設分類，收錄第 1–13 頁正式講稿（含封面介紹與 Thank you／email 收尾）、第 14 頁計算方式備答與第 15 段完整 Q&A Response Pack
- CACS 2026 保留原分類，依序收錄 1–10 正式講稿、11 結尾與 Q&A 畫面、12 一份完整 Q&A Response Pack
- 兩套研討會講稿都同步顯示投影片、逐頁音檔與英文講稿
- 自我介紹與每日教材同步顯示音檔與英文逐字稿
- 點選投影片可開啟原尺寸圖片
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
- `slide-01...slide-11.*`：正式講稿與結尾逐頁音檔及英文講稿
- `slide-12-q-a-response-pack.*`：合併後的完整 Q&A 音檔與講稿
- `slides/slide-1...slide-10.png`：主講第 1–10 頁正式投影片圖片
- `slides/slide-15.png`：Thank you and Q&A 畫面，顯示於 Shadow 第 11 段
- `qa-script.json`：從核准版 Word 講稿整理出的結尾與 Q&A 可重生來源
- `pronunciation-guide.mp3`：專有名詞發音
- `pronunciation-guide.txt`：專有名詞文字稿
- `automation2026/automation2026-full-talk.mp3`：Automation 2026 完整講稿
- `automation2026/slide-01...slide-15.*`：Automation 2026 逐頁講稿、收尾、計算方式備答、合併 Q&A 與音檔
- `automation2026/slides/slide-1...slide-14.png`：Automation 2026 投影片圖片
- `practice-materials/automation2026/extension-v5.json`：封面／Future Work 覆寫、第 13 頁收尾與第 14 頁計算備答的可重生來源
- `automation2026/generation-manifest.json`：Automation 2026 音訊生成紀錄

新增音檔由地端 RTX 3090 的 Qwen3-TTS 複製聲音產生。音檔為 24 kHz、單聲道、96 kbps MP3，輸出響度目標為 -16 LUFS，沒有改變原始生成語速。

## Automation 2026 更新流程

1. `python3 scripts/generate_automation_audio.py --prepare --work-root <work-dir>` 從 12 頁基礎講稿與 `extension-v5.json` 套用封面、Future Work、收尾及附錄後，建立固定的 x-vector 工作清單。
2. 在 `ac-3090` 以 `scripts/remote_qwen_clone_worker.py` 和既有參考聲音執行工作清單，參數維持 `--max-new-tokens 512 --x-vector-only`。
3. `python3 scripts/generate_automation_audio.py --assemble --work-root <work-dir> --xvector-cache <wav-cache> --output-root <output-dir>` 合併、正規化並輸出 MP3。
4. 將生成檔與投影片圖片放進 `automation2026/`，更新 `library-manifest.json` 後執行 `scripts/build_shadowing_player.py`。
5. 跑完整測試、推送 GitHub Pages，並查回頁面與音檔 HTTP 200 後才視為上線。
