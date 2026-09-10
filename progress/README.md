# Progress Records

本資料夾只保存 progress schema 與匿名範例。真實個人學習紀錄的唯一來源是共用 SB MCP，不寫入公開 GitHub repository。

## SB 儲存位置

```text
category: learning/personal-english-loop/progress
monthly title: PEL 學習進度 YYYY-MM
session id: YYYY-MM-DD-[lesson_id]-HHmm
```

每次練習在當月月誌追加一個 Session 區塊，區塊內放置符合 `progress.schema.json` 的 JSON。禁止覆蓋或修改舊 Session。

## 寫入程序

1. 讀取 GitHub 的 progress schema。
2. 根據當次對話產生紀錄，沒有證據的分數填 `null`。
3. 從 SB 搜尋並讀取當月月誌。
4. 確認 Session ID 沒有重複。
5. 追加完整 Session 區塊。
6. 再次讀取並確認 Session ID 存在。
7. 只有查回成功才能回報已保存。

## 分數定義

所有分數均為 1–5，必須根據當次對話觀察，不能猜測。

| Score | Meaning |
|---|---|
| 1 | 幾乎無法開始，需要完整提示 |
| 2 | 能說少量字詞，需要多次提示 |
| 3 | 能用短句表達主要意思 |
| 4 | 大多流暢，偶爾需要修正或停頓 |
| 5 | 能自然、清楚地完成此課任務 |

若當次沒有足夠證據評分，使用 `null`，不要虛構。

## 滾動調整規則

- 同一個 chunk 連續兩次標記 `comfortable`：下一課降低出現頻率。
- 問題連續兩次超過五秒才開始回答：加入下一次 listen-and-repeat。
- 同一錯誤出現三次：下一課只安排一個針對該錯誤的微型練習。
- 每次最多新增五個字，避免教材快速變難。
- 流利度優先於文法完整度；若意思清楚，只修最影響理解的一處。

Codex Work 分析時，同時讀取 GitHub 當前教材與 SB 最近一至三個月的月誌；不得把私人 Session 複製回公開 repository。
