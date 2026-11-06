# PEL 100 集情境英文

## 來源與範圍

資料聲明：教材來自 SB「PEL 100段情境英文教材庫 v1.1」原創教學情境，
不是使用者真實經歷、論文結果或學習評分。原文保存在 `source-v1.1.md`；
來源為 `raw/2026-11/20261106074615-mcp-note.md`，擷取自 knowledge-base
commit `3af9420a6e4876e71b202cbc1b763f5209b8310b`。
不改寫 400 句原文、不把 Sam 改成使用者姓名、不增加口播或另做簡化稿。
A2–B1 是來源的教學設計意圖，尚未經專業 CEFR 校準。

## 資料契約與驗收

- 一集一份音檔，共 001–100 集；每集四句，保留中英文題名、T/L/E 與原版編號。
- `unit_id=pel100-origin-NNN` 固定綁定原始情境；`lesson_id=pel100-NNN` 與
  `canonical_order` 對應 v1.1 排序，未來改排序不可改寫歷史學習紀錄。
- 僅替換播放器 `daily-practice` 清單；其他分類及預設 Automation 不變。
- 舊 Day 01–02 原檔不刪除；未全部生成、驗證前不發布部分清單。
- 私人回答、錄音與 T/L/E 能力證據不寫入公開教材；不把聽完視為能力通過。
- Session schema 2.0 與 Weekly Review schema 1.0 只做向後相容的 ID 擴充，
  接受 `pel100-origin-001` 到 `pel100-origin-100`，仍接受 D01 等舊 ID。
  `lesson.lesson_id` 使用固定的 `unit_id`；`lesson.day` 使用此次的集數。
  Coach 索引的 D01／D02 移到 archived_lessons，歷史音檔與紀錄不變；
  D03 的原 day 3 改為 legacy_day，避免和新第 3 集混淆。

邊界檢查：缺集、重複排序、重複原版 ID、非法 ID、缺標題、缺 T/L/E、
非四句、空句、無句末標點、缺 WAV、截斷生成、錯版字稿、過期時間戳、
錯誤音訊格式與非目標分類改動。任一失敗中止，不補造教材或靜默忽略。

## 實作與資料流

`source-v1.1.md` → `scripts/build_pel100.py` 驗證／匯入 →
`corpus.json`（來源 hash、版本、100 筆 metadata）＋TTS 計畫 →
既有 `remote_qwen_clone_worker.py` → WAV 快取 →
`generate_library_audio.py` 合併與 loudnorm → MP3／顯示稿 →
CTC forced alignment → hash 綁定的句子時間戳 → Shadow 索引與 HTML。

沿用 RTX 3090、Qwen3-TTS x-vector-only、既有本人參考聲音、512 token 上限；
一次一個生成工作，以內容 hash 快取，可從未完成片段續跑，不做無限重試。
生成與對齊的終端紀錄是完成／失敗依據；非背景排程，錯誤直接回報本對話。
先完成 001／022／091 三集全流程再跑全量。不修改現有服務或安裝新環境。
MP3：24 kHz／mono／96 kbps，響度目標 -16 LUFS／-1.5 dBTP；
維持原速，0.8／0.9／1.0 倍速由播放器提供。

## 重建

```sh
python3 scripts/build_pel100.py --work-root work/pel100-v1.1
# 在既有 3090 環境執行生成清單，下載生成 WAV 後：
python3 scripts/build_pel100.py --work-root work/pel100-v1.1 --assemble --cache work/pel100-v1.1/cache --output-root outputs/pel100-v1.1
# 對齊使用 remote_align_tts_chunks.py，再執行：
python3 scripts/build_automation_timings.py --plan work/pel100-v1.1/xvector-plan.json --alignment work/pel100-v1.1/alignment.json --cache work/pel100-v1.1/cache --audio-root outputs/pel100-v1.1
python3 -m unittest discover -s tests
```

## 可用性界線

本批生成驗證：199 個 WAV 片段逐檔比對遠端 SHA-256，合併成 100 份
24 kHz mono MP3；全部經 ffmpeg 完整解碼，合計 1,487.77 秒（約 24 分 48 秒）。
400 句顯示文字與原文一致，時間戳綁定對應 MP3 hash。
58 項單元／契約測試通過；`build_pel100.py` 的標準庫 trace 行覆蓋為 100%，
不代表分支覆蓋或整個系統的覆蓋率。
375／768／1280px 實際瀏覽器檢查包含播放、倍速、四句隨音訊高亮、
100 集選單、上下集、Repeat All 換回第 1 集與關鍵元素溢出。
全量音訊解碼不等於全量人工聽審；語音辨識只用於輔助抽查，
不能保證每個字的發音完美。來源、生成參數與每集技術資料見
`conference/cacs2026-pseudonilm/learning/pel100/learning-manifest.json`。

單元測試驗證匯入與映射，不能代表音檔已生成；WAV／MP3 格式、長度、
字稿及時間戳需另驗。發布時需確認 100 集檔案齊全、其他分類未變、
手機版畫面與播放可用；未得到部署授權不自行 push。
還原方式是將 daily-practice 索引指回保留的 Day 01–02 檔案並重建播放器，
不清除教材及私人進度。
