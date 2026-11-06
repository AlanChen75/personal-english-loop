# Personal English Loop

一套以「敢講、敢用」為核心的個人化英語口說循環系統。

教材按真實使用場景排列。每日練習使用 OLMCP「PEL 100 段情境英文 v1.1」，
每段各做成一集、每集保留原本 4 句，使用既有複製聲音。

[開始每日練習 100 集](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/#daily-practice)
｜[完整教材與來源](lessons/pel-100/README.md)
｜[機器可讀教材索引](lessons/pel-100/corpus.json)

001–020 生活基礎、021–040 日常互動與問題處理、041–060 經驗與工作、
061–080 比較與觀點、081–100 專業溝通。A2–B1 是設計意圖，並非正式難度認證。
先聽一集，再以 0.8×／0.9× 跟讀；可重複本集或 Repeat All。
教材中的角色、工作與研究情境不代表使用者真實經歷，原文未自行改寫。

原第一階段主題安排保留供歷史教材參照：

> D Professional → E Academic → B About Me → C Work & Projects → F Discussion → A Daily Life

## 舊版 Day 01–02（保留，不列於每日播放器）

| Day | 主題 | 教材 | 完整通勤音訊 |
|---|---|---|---|
| 01 | What is Energy Management? | [文字教材](lessons/day-01-energy-management/lesson.md) | [播放 MP3](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/learning/daily-day-01-commute-pack.mp3) |
| 02 | How AI and IoT Help Energy Management | [文字教材](lessons/day-02-ai-iot-energy/lesson.md) | [播放 MP3](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/learning/daily-day-02-commute-pack.mp3) |

每一天另有四段練習音訊：slow、natural、listen-and-repeat、Q&A。完整連結見各課教材。

## 手機 Shadowing 播放器

| 分類 | 內容 | 手機播放器 |
|---|---|---|
| Automation 2026 講稿 | 第 1–13 頁（含封面介紹與 Thank you／email 收尾）、計算方式備用頁與合併 Q&A，預設優先顯示 | [開啟 Automation 2026](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/#automation-2026) |
| CACS 2026 講稿 | 第 1–10 頁、結尾與合併 Q&A | [開啟 CACS 2026](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/#conference) |
| 自我介紹 | 六個可組合單元：我是誰、工作、研究、原因、最近任務、下一步；各四句，附 T/L/E 與重組／換情境練習 | [開啟自我介紹](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/?v=24#about-me) |
| 每日練習 · 100 集 | OLMCP v1.1 的 001–100 原文、逐集音檔與逐句高亮 | [開啟每日練習](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/#daily-practice) |

播放器支援安裝到手機桌面、分類切換、0.8×、0.9×、1.0×、倒退 5 秒、重複本頁與分類內全部循環播放。開車時請勿閱讀或操作畫面。

## 舊版通勤包使用方式

### 去程：輸入（約 30–45 分鐘）

1. 播放 Commute pack（約 20–22 分鐘，內含三輪重複）。
2. 第一輪以聽懂為主。
3. 第二輪跟說，第三輪盡量不靠提示自己回答。
4. 若仍有通勤時間，單獨重播 Listen and Repeat 或 Natural。

### 回程：輸出（約 20–40 分鐘）

1. Q&A：聽問題，在停頓中自己回答。
2. 用 ChatGPT Voice 按 `coach/CHATGPT_COACH.md` 練習。
3. 結束時請 ChatGPT 產出一筆 progress JSON，並透過共用 SB MCP 追加到當週私人紀錄。

開車時不要閱讀或操作手機。請在出發前開始播放，行車中只用耳朵和口說。

## Repository 結構

```text
personal-english-loop/
├── README.md
├── curriculum/
│   └── phase-1.md
├── lessons/
│   ├── pel-100/
│   │   ├── source-v1.1.md
│   │   ├── corpus.json
│   │   └── units/pel100-001...pel100-100.md
│   ├── day-01-energy-management/
│   │   ├── lesson.md
│   │   └── audio-scripts/
│   ├── day-02-ai-iot-energy/
│   │   ├── lesson.md
│   │   └── audio-scripts/
│   └── about-me-introduction/
│       ├── lesson.md
│       └── audio-scripts/
├── audio/
│   ├── day-01/
│   └── day-02/
├── conference/
│   └── cacs2026-pseudonilm/
│       ├── index.html
│       ├── learning/pel100/  # 100 集音檔、字稿與時間戳
│       ├── cacs2026-full-talk.mp3
│       ├── slide-01...slide-12.*
│       └── automation2026/
│           ├── automation2026-full-talk.mp3
│           └── slide-01...slide-15.*
├── coach/
│   ├── CHATGPT_COACH.md
│   └── coach-index.json
└── progress/
    ├── README.md
    ├── progress.schema.json
    └── examples/
```

## 設計原則

- 短句、基礎字、一次只表達一個意思。
- 專業概念用生活化說法，不堆疊術語。
- 同一批核心句在不同音訊中反覆出現。
- 先求能回答，再求完整；先求清楚，再求流利。
- 每次練習留下可機器讀取的紀錄，下一輪內容依弱點調整。
- GitHub 是教材唯一來源；SB 是私人學習進度唯一來源。
- SB 每週一份紀錄，每次練習追加一個 Session；每週日產生總結並討論教材調整方向。

## Automation 2026 簡報來源

2026-11-07 修訂：簡報／講稿 v11，Shadow 快取 v25。核准簡化第 3、5、6、8、9、10、12 頁；第 10 頁改為 “We do this extra analysis after selection.”。保留原開場、權重、主要結果、研究限制與 Q&A，14 頁簡報畫面及其他教材不變。來源註記不放入講者備註。線上狀態以 GitHub Pages 成功部署為準。

- 講稿來源：`practice-materials/automation2026/extension-v11.json`；音訊產生器預設讀取此版。逐頁差異、保留的備答細節與驗收契約見 [v11 修訂說明](practice-materials/automation2026/revision-v11.md)。
- 簡報產生器：`scripts/build_automation_identity.mjs`，依固定雜湊的原始 v7 產生器製作，不改研究表格與圖表。
- 本機交付：`outputs/automation2026-v11/automation2026_13min_deck_v11.pptx`、同目錄 `automation2026_13min_script_v11.md` 與 `automation2026_13min_display_script_v11.md`。
- 講稿變更界線：只修改使用者指定並核准的句段；增加封面身分資訊不代表可以增加口播。新增或改寫其他句段前須取得同意。
- 校方識別素材：[台科大官方下載頁](https://secretariat-r.ntust.edu.tw/p/404-1063-74346.php?Lang=zh-tw)。
- 更新音訊後必須重新產生並驗證 `.timings.json` 的音訊與字稿雜湊，再重建播放器，不能沿用舊時間戳。

## 免費資源

播放器內的自我介紹、Day 01–02、Automation 2026 與 CACS 2026 講稿都使用地端 RTX 3090 上的 Qwen3-TTS 聲音複製模型產生，並統一做響度校正。MP3 儲存在本 repository，手機版入口由 GitHub Pages 免費提供。
