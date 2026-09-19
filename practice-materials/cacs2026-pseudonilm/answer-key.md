# D03 回答後核對

先完成 [題目頁](practice.md) 的一次閉卷回答，再讀對應題號。以下是示範，不是唯一正解。先檢查意思，再修一個最重要的問題；關閉本頁後立即重答。教練不能在學員第一次嘗試前顯示此頁內容。

## 核心題

| ID | 短答案 | 核對重點 |
|---|---|---|
| R01 | I study power use in factories. My research is about PseudoNILM. | 主題清楚即可；不要求背姓名或完整機構名稱。 |
| R02 | We ask when the system should give a result and when it should stop. | 包含出結果與不出結果兩種情況。 |
| R03 | Different sites provide different evidence. Some machines change speed. | 可改答未監測負載、製程依賴、機器角色相似但訊號不同。 |
| R04 | It means giving no attribution score. It does not mean stopping a machine. | 是報告邊界，不是實體控制。 |
| R05 | It uses total power data, device priors, and pseudo traces. | 三種輸入；不能把目標標籤說成最終執行的輸入。 |
| R06 | They give timing information. They do not contain target labels. | 同時保留時間資訊與無目標標籤。 |
| R07 | Fixed rules choose a route for each dataset. | 指本次凍結規則，不宣稱已驗證新工廠選路能力。 |
| R08 | We used validation labels to set some constants. After reconstruction, we use labels to check the results. | 最終 dispatch 與 trace construction 不讀設備標籤；不能說整個流程從未用過標籤。 |
| R09 | Three datasets scored above 0.7 on TECA. This supports energy attribution. | 是三組 scored datasets；HIPE 不算第四組 TECA 結果。 |
| R10 | It is a fixed reference for this study. It is not an industry-wide rule. | 不把研究參考值當普遍驗收門檻。 |
| R11 | Event timing is still weak. We cannot claim precise event reconstruction. | 可補 segment F1 為 0.15–0.32；TECA 高不等於事件時間精準。 |
| R12 | All four datasets helped shape the design. Earlier checks also affected development. | final execution 的隔離不會抹去先前開發影響。 |
| R13 | We have not shown that it works at a new plant. We need a new study. | 尚未證實，不要改說一定失敗或一定成功。 |
| R14 | No. We used validation labels to set some values. | attribution mapping 非監督式，也不能推成整個系統 fully label-free。 |
| R15 | HIPE tests the no-score boundary. This setup lacks the required pseudo-trace support. | no-score 是設計中的輸出，不是遺漏結果或第四個 scored test。 |
| R16 | The nameplate-only proxy changed the decision in the wrong direction. We still need a reliable proxy. | 這是負面結果；不能稱已解決部署選路。 |

## 進階備用題

### R17 各資料集數字

IMDELD scores 0.7619. WELTRON scores 0.8021. Case1 scores 0.7136.

三組平均 0.7592，最低 0.7136。這些是 full-partition TECA，不是 accuracy 百分比。初學階段只要先講出三組超過研究參考值，不必被小數卡住。

### R18 元件證據

Without pair calibration, IMDELD drops from 0.7619 to 0.7210. Without guarded repair, WELTRON drops from 0.8021 to 0.7223. Without the Case1 route, Case1 drops from 0.7136 to 0.5900.

短版：Each tested component helps its own dataset. This does not prove transfer to new plants.

### R19 Bootstrap 範圍

The worst lower endpoint is 0.7061. It applies only to eligible activity-bearing chunks. It is not a confidence interval for the full time partition.

不能只答「最低界超過 0.7，因此所有時間都通過」。不要自行補信賴水準。

### R20 額定值與實際貢獻

A nameplate shows rated capacity. It does not show actual energy use in the measured total.

HIPE 受監測設備只占 aggregate energy 的 3.83%。不把這個能量比例說成設備數量比例。

### R21 HIPE 分數的意思

The equipment-based audit gives 0.1602 and supports no score. The nameplate-only proxy gives 0.9220 and changes the decision to score.

這兩個是 retrospective audit／selector proxy 的分數，不是 HIPE TECA。設備資料的回顧稽核，也不能冒充為已可部署的無標籤 selector。

### R22 WELTRON 分享

You can request it from the corresponding author. Identifying information will be removed before sharing. Revealing raw traces are not in the public artifact.

這是講稿的資料提供條件，本次沒有分享資料，也沒有代替作者承諾批准申請。

### R23 成本表

It reports CPU analysis after the protocol was fixed. It excludes pseudo-trace generation and validation searches. It does not show hardware-independent complexity.

不要說成 end-to-end cost，或對硬體無關的速度保證。

### R24 文獻定位

Other studies use process constraints or active learning. Our study focuses on fixed routes and the option to give no score. We do not claim to beat those methods.

較完整的中文核對：講稿提到 process/equipment constraints、仍保留監督階段的 active learning，以及資料集、指標、實作不同造成的比較困難。這是定位，不是同條件 benchmark 排名；本教材未另行查核那些文獻。

## Typing 核對示範

| ID | 可以這樣寫 |
|---|---|
| T01 | I study power use in factories. We estimate energy use for each machine. |
| T02 | Different sites provide different evidence. One method may not fit every dataset. |
| T03 | We use total power data and device information. We also use pseudo traces. Fixed rules choose a route. |
| T04 | We used validation labels to set a few constants. We use equipment labels after reconstruction to check results. |
| T05 | Three datasets scored above 0.7 on TECA. This does not show precise event timing. |
| T06 | We have not shown transfer to a new plant. We need a new study. |
| T07 | Nameplate ratings do not show actual energy contribution. We still need a reliable proxy. |
| T08 | Could you say that again? Do you mean a new plant? |

打字答對後遮住答案再說。若只能照讀，先記為 after_model，再用下一輪問題確認是否能獨立取回。

## Speaking 核對

- S01：研究主題與目的清楚即可。可使用 R01，再加一句 R02。
- S02：先說場域證據不同，再舉一種原因。參考 R03。
- S03：輸入、固定規則、路線、no-score；被追問再補標籤階段。參考 R05–R08、R15。
- S04：先說三組 TECA 結果，再說事件時間的限制。參考 R09、R11。
- S05：不能承諾直接適用。說未證實新工廠轉移，以及需要新研究。參考 R13。
- S06：先確認問題，再直接回答與補理由。請教練從 R10、R14、R15、R22、R23 中一次挑一題。

## 重答後的變形題

教練只讀 Question，不把後面的核對點一起說出。學員回答後再看核對點。

| Question | 回答後核對 |
|---|---|
| Explain your work to someone who does not know NILM. | 用 total power、machine energy use，不強迫對方懂術語。 |
| A manager asks you to always give a number. How do you respond? | 缺少必要 support 時應 no-score，不捏造可用分數。 |
| Someone says a high TECA score means perfect event timing. What would you say? | 區分 energy attribution 與 event timing。 |
| A colleague calls the final run fully label-free. What would you explain? | 交代 validation labels 的早期角色與之後的評估角色。 |
| A new factory asks for a guarantee. What evidence is still needed? | 需要 prospective unseen-site study，不給保證。 |

## 一次只修一點

若學員說「We use no labels」，先修研究意思：「We used labels to set some values.」再請他重答；不一次加上多個文法規則。若意思已正確，再修一個最妨礙理解的語言問題。

回憶成功看意思與必要限制，不看是否與示範逐字相同。學員實際回答、提示、錯誤與熟練度只存 SB 私人週誌。
