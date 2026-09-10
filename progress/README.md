# Progress Records

本資料夾保存 session schema、weekly review schema 與匿名範例。真實個人學習紀錄的唯一來源是共用 SB MCP，不寫入公開 GitHub repository。

## 儲存粒度

- Category：`learning/personal-english-loop/progress`
- Weekly title：`PEL 進度 YYYY-Www`
- Session ID：`YYYY-MM-DD-[lesson_id]-HHmm`
- Timezone：`Asia/Taipei`

每個 ISO week 建立一份 SB 週誌。每次練習結束立即追加一個 Session；同週所有 Session 寫在同一份週誌。每週日再追加一個 Weekly Review，並在原 Codex 任務回報、討論調整方向。

週誌採 append-only。禁止覆蓋或修改舊 Session。

## Session 必記內容

### 來源與版本

- Session ID、記錄時間、時區。
- 對話來源、Coach 版本。
- lesson ID、教材標題、來源 URL 與 Git ref。
- 練習情境與實際分鐘數。

### 材料清單

- 實際使用的 transcript、audio、chunks、vocabulary、Q&A 或 role-play。
- 每項材料的 ID、網址、是否完成與重複次數。
- 未使用的材料不得寫成已完成。

### 練習證據

- 只保存具有代表性或發生問題的練習事件，不保存完整對話逐字稿。
- 每個事件保存任務、必要的回答片段、是否獨立完成、提示程度及開始回答秒數。
- 問題以 issue ID 連結到結構化問題紀錄。

### 問題與能力追蹤

- 問題類型：理解、發音、文法、字彙、流利度、回答速度、信心、內容難度。
- 每個問題保存觀察片段、修正版、原因、提示程度與目前狀態。
- 相同問題跨 Session 使用穩定的 `recurrence_key`，讓每週分析能正確計數。
- 追蹤 chunks 的嘗試次數、成功次數與 `new / practicing / comfortable`。
- 追蹤最多五個新字、學員自評、Coach 判斷限制與下一次練習計畫。

## 寫入程序

1. 讀取 GitHub 的 `progress.schema.json`。
2. 根據當次對話建立 Session；沒有證據的分數填 `null`。
3. 計算當週 ISO week，搜尋 `PEL 進度 YYYY-Www`。
4. 讀取完整週誌並確認 Session ID 沒有重複。
5. 追加完整 Session 區塊。
6. 再次讀取並確認 Session ID 存在。
7. 只有查回成功才能回報已保存。

## 每週分析

每週分析必須符合 `weekly-summary.schema.json`，至少包含：

- Session 與練習時間覆蓋率。
- 使用過的教材與練習模式。
- 各項分數趨勢及有效觀察筆數。
- 跨 Session 重複出現的問題。
- chunks 熟練狀態變化。
- 哪些材料有幫助、過難或證據不足。
- 證據缺口、教材調整建議與需要和學員討論的問題。

不因單一 Session 直接修改教材。相同問題至少跨兩個 Session，或同一低分指標至少有三次有效觀察，才可列為高優先調整依據。教材變更必須先與學員討論，確認後才提交 GitHub。

## 分數定義

所有分數均為 1–5，必須根據當次對話觀察，不能猜測。

| Score | Meaning |
|---|---|
| 1 | 幾乎無法開始，需要完整提示 |
| 2 | 能說少量字詞，需要多次提示 |
| 3 | 能用短句表達主要意思 |
| 4 | 大多流暢，偶爾需要修正或停頓 |
| 5 | 能自然、清楚地完成此課任務 |

若當次沒有足夠證據評分，使用 `null`。

## 滾動調整規則

- 同一 chunk 連續兩次標記 `comfortable`：下一課降低出現頻率。
- 回答開始時間連續兩次超過五秒：加入下一次 listen-and-repeat。
- 同一 `recurrence_key` 跨兩個 Session 出現：列入週報優先問題。
- 同一問題跨三個 Session 仍為 `open`：提出教材微型練習調整。
- 每次最多新增五個字，避免教材快速變難。
- 流利度優先於文法完整度；若意思清楚，只修最影響理解的一處。
