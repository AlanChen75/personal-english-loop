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

## 每日使用方式

### 去程：輸入（約 30–45 分鐘）

1. 播放 Commute pack（約 20–22 分鐘，內含三輪重複）。
2. 第一輪以聽懂為主。
3. 第二輪跟說，第三輪盡量不靠提示自己回答。
4. 若仍有通勤時間，單獨重播 Listen and Repeat 或 Natural。

### 回程：輸出（約 20–40 分鐘）

1. Q&A：聽問題，在停頓中自己回答。
2. 用 ChatGPT Voice 按 `coach/CHATGPT_COACH.md` 練習。
3. 結束時請 ChatGPT 產出一筆 progress JSON。

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

## 免費資源

目前音訊使用 macOS 內建英文語音合成，不需要付費 API。MP3 儲存在本 repository，並透過免費 jsDelivr GitHub CDN 提供標準 `audio/mpeg` 播放連結。Commute pack 把同一組約 7 分鐘的素材安排成三輪，利用重複加深記憶；未來若要更自然的多角色聲音，可在不改教材結構的情況下替換音訊。
