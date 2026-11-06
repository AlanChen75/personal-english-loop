# Personal English Loop Shadowing Player

同一個手機播放器收錄 Automation 2026、CACS 2026、自我介紹與每日英語教材。

## 手機播放

[開啟 Shadowing 播放器](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/)

播放器功能：

- 可安裝為手機桌面 Web App
- 四類教材：Automation 2026、CACS 2026、自我介紹、每日練習
- Automation 2026 是預設分類，收錄第 1–13 頁正式講稿（含封面介紹與 Thank you／email 收尾）、第 14 頁計算方式備答、第 15 段完整 Q&A Response Pack，以及第 16 段重點發音練習
- CACS 2026 保留原分類，依序收錄 1–10 正式講稿、11 結尾與 Q&A 畫面、12 一份完整 Q&A Response Pack
- 兩套研討會講稿都同步顯示投影片、逐頁音檔與英文講稿
- 自我介紹與每日教材同步顯示音檔與英文逐字稿
- 播放、拖曳或倒退音訊時，逐字稿會同步標示目前句子
- Automation 第 1–15 段使用原始語音片段的 CTC 對齊時間戳，包含實際停頓；0.8×／0.9×／1.0× 都依音訊 currentTime 切換。發音重點清單不是完整逐字稿，不啟用逐句高亮。其他教材暫保留估算模式。
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
- `automation2026/pronunciation-guide.*`：NILM、MCC 與較少使用術語的重點發音練習
- `automation2026/slides/slide-1...slide-14.png`：Automation 2026 投影片圖片
- `practice-materials/automation2026/extension-v7.json`：對齊簡報 v7／講稿 v6 的第 1–12 頁覆寫、第 13 頁收尾與第 14 頁計算備答；第 3–6、8–11 頁補上研究條件、公式、指標定義與證據範圍
- `automation2026/generation-manifest.json`：Automation 2026 音訊生成紀錄
- `automation2026/*.timings.json`：逐句起訖秒數及音檔／字稿 SHA-256；重建播放器時若音檔或字稿變更卻未更新時間戳，會拒絕產出

新增音檔由地端 RTX 3090 的 Qwen3-TTS 複製聲音產生。音檔為 24 kHz、單聲道、96 kbps MP3，輸出響度目標為 -16 LUFS，沒有改變原始生成語速。

## Automation 2026 更新流程

1. `python3 scripts/generate_automation_audio.py --prepare --work-root <work-dir>` 從 12 頁基礎講稿與 `extension-v10.json` 套用逐頁講稿、收尾及附錄後，建立固定的 x-vector 工作清單。顯示稿用數字；TTS 保留小數前的 zero 與 MCC 逐字母停頓。2026-11-06 僅恢復第 1 頁 v7 原稿，保留第 3、6、9 頁核准簡化；不得因封面資訊變更自行增加口播。
2. 在 `ac-3090` 以 `scripts/remote_qwen_clone_worker.py` 和既有參考聲音執行工作清單，參數維持 `--max-new-tokens 512 --x-vector-only`。
3. `python3 scripts/generate_automation_audio.py --assemble --work-root <work-dir> --xvector-cache <wav-cache> --output-root <output-dir>` 合併、正規化並輸出 MP3。
4. 將生成檔與投影片圖片放進 `automation2026/`。用 `scripts/remote_align_tts_chunks.py --jobs <jobs.json> --cache <wav-cache> --output <alignment.json>` 在 3090 對齊原始片段，再以 `scripts/build_automation_timings.py --plan <plan.json> --alignment <alignment.json> --cache <wav-cache> --audio-root conference/cacs2026-pseudonilm/automation2026` 產生時間戳。對齊流程不修改聲音或語速。
5. 更新 `library-manifest.json` 的 `timings` 路徑後，執行 `scripts/build_shadowing_player.py`。時間戳必須與音檔、字稿版本一致，播放器會以音檔雜湊建立快取網址。
6. 跑完整測試、推送 GitHub Pages，並查回頁面與音檔 HTTP 200 後才視為上線。
