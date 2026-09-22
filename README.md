# Personal English Loop

一套以「敢講、敢用」為核心的個人化英語口說循環系統。

教材不是按文法章節排列，而是按真實使用場景排列。第一階段依指定順序進行：

> D Professional → E Academic → B About Me → C Work & Projects → F Discussion → A Daily Life

## 前兩天直接開始

| Day | 主題 | 教材 | 完整通勤音訊 |
|---|---|---|---|
| 01 | What is Energy Management? | [文字教材](lessons/day-01-energy-management/lesson.md) | [播放 MP3](https://cdn.jsdelivr.net/gh/AlanChen75/personal-english-loop@main/audio/day-01/day-01-commute-pack.mp3) |
| 02 | How AI and IoT Help Energy Management | [文字教材](lessons/day-02-ai-iot-energy/lesson.md) | [播放 MP3](https://cdn.jsdelivr.net/gh/AlanChen75/personal-english-loop@main/audio/day-02/day-02-commute-pack.mp3) |

每一天另有四段練習音訊：slow、natural、listen-and-repeat、Q&A。完整連結見各課教材。

## 研討會講稿

| 主題 | 練習方式 | 手機播放器 |
|---|---|---|
| CACS 2026 — PseudoNILM | 逐頁講稿、逐頁音檔、調速 Shadowing、Repeat All | [開啟練習頁](https://alanchen75.github.io/personal-english-loop/conference/cacs2026-pseudonilm/) |

播放器支援安裝到手機桌面、0.8×、0.9×、1.0×、倒退 5 秒、重複本頁與全部循環播放。開車時請勿閱讀或操作畫面。

## 每日使用方式

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
│   ├── day-01-energy-management/
│   │   ├── lesson.md
│   │   └── audio-scripts/
│   └── day-02-ai-iot-energy/
│       ├── lesson.md
│       └── audio-scripts/
├── audio/
│   ├── day-01/
│   └── day-02/
├── conference/
│   └── cacs2026-pseudonilm/
│       ├── index.html
│       ├── cacs2026-full-talk.mp3
│       ├── slide-01...slide-10.mp3
│       └── slide-01...slide-10.txt
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

## 免費資源

Day 01–02 音訊使用 macOS 內建英文語音合成，不需要付費 API。研討會講稿使用地端 Qwen3-TTS 聲音複製模型產生，並統一做響度校正。MP3 儲存在本 repository；一般教材透過免費 jsDelivr GitHub CDN 播放，研討會 Shadowing 介面則透過 GitHub Pages 提供手機版入口。
