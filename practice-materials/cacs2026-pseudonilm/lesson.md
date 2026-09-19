---
id: D03
day: 3
category: D
title: Explain My PseudoNILM Research
level: A2-B1
status: ready
version: 1.0.0
source_material_id: PEL-MAT-CACS2026-PSEUDONILM-001
source_version: CACS2026-R1-script-v1
---

# 用短句介紹 PseudoNILM 研究

先能說出研究在做什麼，再練方法、結果與限制。句型以 A2–B1 為主；必要研究名詞屬專業加字，不代表整份原講稿是 A2–B1。此課分六次練，每次約 10–15 分鐘，不必一次背完。

這是使用者授權改寫的教材，研究敘述與數字來自私人 CACS 2026 R1 講稿 v1，未在此課重新驗證實驗。完整原稿、個人資料、原句對照與來源路徑只留在私人素材庫。公開以 Material ID 追溯；本課不是原講稿逐字稿。

## 開始練習

1. 只讀今天一個場景，確認意思。
2. 關閉本頁與答案頁，只開 [題目頁](practice.md)。先回憶再說或打字。
3. 卡住時先說一個短句。教練最多等八秒，再給一個 chunk 提示。
4. 回答後才開 [核對頁](answer-key.md)。意思正確即可，不必逐字一樣。
5. 教練先回應你的意思，再修一個最重要的問題。科學意思錯誤優先於小文法錯誤。
6. 關閉答案、立刻重答，再換一個問法。跟讀不等於獨立回憶成功。
7. 隔日、第三天、第七天再抽問；這是本課起始安排，依實際表現調整。

沒有本課音檔。可由教練逐題口頭提問，問題後留八秒，核對後再留八秒讓你重答；目前不把文字稿標成已生成的音訊。

## 六次短練習

| 次序 | 場景 | 先練 chunks | 閉卷題目 | 完成行為 |
|---|---|---|---|---|
| 1 | 自我研究介紹 | C01–C03 | R01、R02；T01；S01 | 說出約十秒介紹 |
| 2 | 研究問題 | C04–C06 | R03、R04；T02；S02 | 說出一個問題與原因 |
| 3 | 方法 | C07–C10 | R05–R08；T03、T04；S03 | 說明輸入、選路、何時用標籤 |
| 4 | 結果 | C11–C13 | R09–R11；T05；S04 | 結果與限制一起說 |
| 5 | 限制 | C14–C17 | R12–R14；T06、T07；S05 | 回答新工廠與標籤問題 |
| 6 | 會議 Q&A | C18–C20 | R15、R16；T08；S06 | 先回答，再補一句理由 |

R17–R24 是進階備用題，熟悉核心後再加入。每天專業新字最多選五個。只記錄實際練過的項目，不預填熟練度。

## 場景一 自我研究介紹

**先敢講**

I study power use in factories. I work on PseudoNILM. We study when to give a result and when to stop.

**再加一句**

We use total power data to estimate how much energy each machine uses. If the required support is missing, the system gives no score.

**約三十秒版**

I study power use in factories. My research is about PseudoNILM. We use total power data to estimate energy use for each machine. Different sites provide different evidence. We use fixed rules to choose a method. Sometimes the system gives no score. This is a pilot study. We still need to test new plants.

這裡的 stop 是停止產生歸屬分數，不是關閉工廠或設備。

## 場景二 研究問題

When should the system give a result? When should it stop? Different factories provide different evidence. Some machines change speed. Some loads are not monitored. One method may not fit every dataset.

進一步說：Some machines have similar roles, but their power patterns differ. Production schedules also affect the patterns.

口語可用 **fixed rules choose a method** 說明 frozen dispatch，不把它說成能自動判斷所有新場域的安全控制器。

## 場景三 方法

We use total power data, device information, and pseudo traces. Pseudo traces give timing information. They do not contain target labels. We fix the rules before the final run. The rules choose a route for each dataset.

### 四條路線

| Dataset | 口語先說 | 需要時保留的術語 |
|---|---|---|
| IMDELD | We share out the power and adjust device pairs. | modulated allocation with pair calibration |
| WELTRON | We apply a repair step with checks. | guarded repair |
| Case1 | We use rectangles to represent events. | event rectangles |
| HIPE | The system gives no score in this setup. | no-score boundary |

前三個有 attribution scores；HIPE 在本次設定下缺少必要 pseudo-trace support，不是第四個 scored dataset。不要把 routes 說成「到新工廠就會自動選對」。

### 標籤何時出現

We used validation labels to set a few constants. Then we fixed the rules. The final run uses no equipment labels for route selection or trace construction. After reconstruction, we use labels to calculate TECA and other diagnostics.

簡短版：We used labels earlier to set some values. We use them again later to check results. We do not claim a fully label-free system.

## 場景四 結果

Three datasets scored above 0.7 on TECA. Here, 0.7 is our fixed study reference. It is not a rule for the whole industry. The results support energy attribution. They do not show precise event timing.

| 完整時間分區的 TECA | 講稿數值 | 需要時的讀法 |
|---|---|---|
| IMDELD | 0.7619 | zero point seven six one nine |
| WELTRON | 0.8021 | zero point eight zero two one |
| Case1 | 0.7136 | zero point seven one three six |
| 三組平均 | 0.7592 | zero point seven five nine two |
| 最低一組 | 0.7136 | zero point seven one three six |

不用每天背四位小數。先能說「Three datasets scored above our study reference」，再核對數字。不要把 0.7619 TECA 說成 76.19% accuracy。

### 進階結果卡

- Segment F1 is between 0.15 and 0.32. Event timing is still weak.
- Without pair calibration, IMDELD drops from 0.7619 to 0.7210.
- Without guarded repair, WELTRON drops from 0.8021 to 0.7223.
- Without the Case1 route, Case1 drops from 0.7136 to 0.5900.
- These changes support the components on these datasets. They do not prove transfer to new plants.
- The worst bootstrap lower endpoint is 0.7061. It only applies to the eligible activity-bearing chunks used in that analysis. It is not a confidence interval for the full time partition.

Bootstrap 那三句要一起說。原講稿沒有提供本課可用的信賴水準，不自行加上「95%」。

## 場景五 限制

This is a pilot study. All four datasets helped shape the design. Earlier checks also affected development. We have not shown that it works at a new plant. We need a new study planned in advance.

We cannot claim precise event timing. We also cannot claim a fully label-free system or a validated safety controller.

### HIPE 為什麼重要

A later audit based on equipment data gave a selector score of 0.1602. It supported giving no score. A proxy using only nameplate ratings gave 0.9220 and changed the decision to score. These are selector/audit scores, not HIPE TECA results.

The monitored devices supplied only 3.83% of the aggregate energy. A nameplate tells us a device's rated capacity. It does not tell us its actual energy contribution. That proxy was not safe for this boundary. A reliable proxy for deployment is still unresolved.

先練短版：Rated power is not actual energy use. We still need a reliable proxy.

## 場景六 會議 Q&A

回答結構：**直接回答 → 一句原因 → 必要時補限制**。長問句聽不懂，先要求重述。

- Is it fully label-free? → No. We used validation labels to set some values.
- Does it work at a new plant? → We have not shown that yet. We need a new study.
- Why no score for HIPE? → This setup lacks the required pseudo-trace support.
- Is 0.7 a universal threshold? → No. It is the reference for this study.
- Can the private dataset be shared? → It can be requested from the corresponding author. Identifying information will be removed before sharing. The public artifact does not include revealing raw traces.
- What does the cost table cover? → It covers CPU analysis after the rules were fixed. It excludes pseudo-trace generation and validation searches. It does not show hardware-independent complexity.

先看懂這些示範，練習時改開只有題目的頁面。

## 核心 chunks

| ID | Chunk | 用途與替換 |
|---|---|---|
| C01 | I study ___. | 我研究⋯；power use in factories |
| C02 | My research is about ___. | 我的研究主題；PseudoNILM |
| C03 | We use ___ to estimate ___. | 用什麼估計什麼；total power data / machine energy use |
| C04 | When should the system ___? | 提出問題；give a result / stop |
| C05 | Different sites provide ___. | 說明差異；different evidence |
| C06 | One method may not fit ___. | 保留條件；every dataset |
| C07 | First, we ___. Then, we ___. | 說順序；set values / fix the rules |
| C08 | The rules choose ___. | 說選路；a route |
| C09 | If ___ is missing, ___. | 說邊界；required support / we give no score |
| C10 | We use labels to ___. | 交代標籤用途；set values / check results |
| C11 | The results support ___. | 說有支持的主張；energy attribution |
| C12 | The score drops from ___ to ___. | 說消融變化；0.7619 / 0.7210 |
| C13 | This does not show ___. | 說結果界線；precise event timing |
| C14 | This is a pilot study. | 界定研究階段 |
| C15 | We have not shown ___ yet. | 說未證實的事；transfer to new plants |
| C16 | We still need ___. | 說下一步；a new study / a reliable proxy |
| C17 | It applies only to ___. | 限定範圍；the selected chunks |
| C18 | Could you say that again? | 請對方重述 |
| C19 | Do you mean ___? | 確認問題；a new plant |
| C20 | Let me put it simply. | 用短句重新解釋 |

C18–C20 是教材新增的溝通工具，不是原講稿中的研究發現。

## 必要專業詞彙

前五個先會認、會用；其餘遇到對應場景再學。不擴寫講稿沒有定義的 TECA 公式。

| Term | 簡單意思 | 可直接說的英文 |
|---|---|---|
| aggregate power | 合計功率 | total power from the site |
| energy attribution | 估計能量歸屬到哪些設備 | estimate how much energy each machine uses |
| pseudo traces | 此研究中含時間資訊、不含目標標籤的序列 | timing information without target labels |
| no-score output | 明確不提供歸屬分數 | the system gives no score |
| pilot study | 初步研究 | an early study with limited evidence |
| device priors | 預先宣告的設備資訊 | device information given in advance |
| frozen protocol | 執行前固定的規則 | rules fixed before the final run |
| dispatch / route | 選擇處理路徑／路徑 | choose a method / a path |
| validation labels | 用來校準常數的驗證標籤 | labels used to set some values |
| reconstruction | 重建估計的設備序列 | build estimated device traces |
| TECA | 本研究的能量歸屬評估指標 | a measure of energy attribution |
| segment F1 | 區段重建表現的指標 | a measure of segment reconstruction |
| nameplate rating | 銘牌額定值 | rated capacity, not actual use |
| proxy | 間接指標 | an indirect measure |
| abstention | 選擇不給結果 | choose not to give a result |
| generalization | 在未見場域也適用 | work at a new site |

發音沿用講稿提示：TECA → T-E-C-A；IMDELD → I-M-D-E-L-D；HIPE → hype；WELTRON → well-tron；NILM → N-I-L-M；VFD → V-F-D。字根只在卡字時輔助記憶，不另背一份字根表。

## 正式句與口語句的使用規則

私人原句對照表逐項標記了「保留」或「拆短」。公開教材採以下規則：

- **正式發表保留**：方法名稱、資料集名稱、TECA 與 segment F1 的分別、full-partition 與 chunk-conditional 的範圍、pilot、no-score、label-free 的限制。
- **日常口說拆短**：長研究問題拆成兩問；多重原因一次說一個；五階段流程分成數句；數值列表先講趨勢再按需報數字。
- **可縮短但不可加強**：未證實新工廠轉移，不說 works everywhere；不把 no-score 說成系統故障；不把 private field dataset 說成公開原始資料。

## 給 PEL 教練

讀完本課與核對頁後，一次只顯示一道題。首次嘗試不顯示 model answer、關鍵數字、答案關鍵詞或變形題解析。先讓學員回答；需要提示時才給一個 chunk，並記為 with_hint。看過示範後的回答記為 after_model，不能當 independent。

Typing 是過渡：先閉卷打一句，修一點，再遮住文字說出同一意思。說得出來後換問法或改成向非研究者解釋。不要要求完美逐字背稿。

本課使用既有 progress schema 2.0：lesson_id `D03`、day `3`。來源 URL 使用本課公開網址，course_git_ref 使用當次實際 commit。材料 ID 可用 `D03-SCENES`、`D03-CHUNKS`、`D03-VOCAB`、`D03-TYPING`、`D03-SPEAKING`、`D03-RETRIEVAL`；題號放在 prompt_or_task。

沿用 activity `qa`、`role_play` 或 `review`，不新增 schema 不接受的 `typing` enum；打字練習可在 prompt_or_task 標記「typing」。說明是否有音訊，缺乏證據的分數填 null。

私人紀錄追蹤：看懂、提示後取回、獨立取回、能換情境使用。現有 chunk status 仍用 new / practicing / comfortable；以 practice_events 的 result 與回答片段保存更細的提取證據，不擅自擴增 enum。間隔複習日期寫入 next_plan.goal。

實際練習結束才建立 Session，append 到 SB 當週 `PEL 進度 YYYY-Www` 並讀回。本次教材建立不算學員練習，不產生虛構分數、練習分鐘或完成紀錄。
