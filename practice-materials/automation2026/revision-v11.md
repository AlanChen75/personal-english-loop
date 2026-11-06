# Automation 2026 v11 口播簡化

核准日期：2026-11-07（Asia/Taipei）。依本對話核准的七頁範圍，以及第 10 頁明確選定的句子修改。來源為 v10；SB 試講分析僅用來定位卡點，不將 ASR 誤聽視為確定的發音錯誤。

## 範圍與保留項目

- 改第 3、5、6、8、9、10、12 頁。第 1、2、4、7、11、13 頁與 Q&A 不變。
- 簡報視覺、封面照片、台科大標頭、數據圖表不變；更新講者備註、顯示稿、TTS、音訊及高亮。
- 第 4 頁四項權重、第 7 頁 baseline 與結果、第 8 頁 5／1／20 的 test/validation 證據差別保留。
- 第 9 頁口播保留 2.22% 與 6%，不改成 2.2%；原計數 5/225 與 54/900 仍在簡報表格及 v10。
- 第 10 頁使用 “We do this extra analysis after selection.”；保留 oracle 使用 validation labels 與不能作為 label-free selector 的限制，以及兩種加權結果。
- 第 12 頁保留正確、靠近邊界、錯誤 bounds 三種情境及分開檢驗候選限制／重建上限。
- 其他研究內容、CACS、自我介紹、每日 100 集、播放器互動與預設主題不變。

## 文字量與計時界線

正式 13 段顯示稿以空白分詞：v10 1,143 words → v11 1,051 words，減少 92 words。此計法把小數及縮寫算一個單位，不能當成實際口播字數。

沒有新的使用者試講錄音，不能宣稱已壓到 13 分鐘；TTS 長度也不是使用者現場報告時間。本次優先降低卡句，不為湊時間刪研究限制。

本機產物實測：完整 TTS MP3 635.92 秒（10 分 35.92 秒），v10 為 694.67 秒，減少 58.75 秒。格式為 24 kHz、單聲道、96 kbps；17 份輸出 MP3 皆完整解碼。108 個 TTS 片段中，96 個核對輸入與 SHA-256 後重用，12 個由 3090 新生成。CTC 對齊與自動辨識僅是機械品質檢查，不等於逐字人耳審聽或專有名詞發音認證。

簡報驗證：14 頁渲染與 v10 逐像素相同；只有七頁講者備註不同，內容對應 v11 JSON；未在原生 PowerPoint 現場播放。

## 逐頁新稿與差異

### 第 3 頁

原稿：

> We used 3 industrial corpora: IMDELD, Case 1, and WELTRON, with 9 devices in total. Each trace was aligned to 1 power sample per second. We split the data in time order. The first 50% is for calibration. The next 20% is for validation. The last 30% is for testing. The table shows four conditions: LLM wide, LLM bounded, LHS wide, and LHS bounded. LHS means Latin hypercube sampling. Each pool contained 15 joint configurations for each dataset, source, bounds condition, and seed. For the LLM, device proposals were joined by index, rather than by every possible combination. Both sources received the same candidate-count and calibration-sample budgets.

v11：

> We used 3 industrial corpora: IMDELD, Case 1, and WELTRON, with 9 devices in total. Each trace was aligned to 1 power sample per second. We split the data in time order. The first 50% is for calibration. The next 20% is for validation. The last 30% is for testing. The table shows two candidate sources. Each uses wide or bounded ranges. LHS means Latin hypercube sampling. Each pool contained 15 joint configurations for each dataset, source, bounds condition, and seed. Both sources received the same candidate-count and calibration-sample budgets.

### 第 5 頁

原稿：

> Here, bounds are declared engineering ranges. Examples include power factor and on-ratio. The table shows two places where bounds act. First, they restrict candidate parameters. Bounded LHS samples directly within the ranges, without clipping or rejecting wide samples. Second, bounds restrict accepted events and cap reconstructed device power. The wide procedure keeps wider candidate ranges and wider reconstruction rules. So enabling bounds changes both candidate generation and reconstruction. If performance changes, this experiment cannot tell us how much comes from each part. Also, these declared ranges are engineering assumptions. We have not measured the true feasible region.

v11：

> Here, bounds are declared engineering ranges. The table shows two places where bounds act. First, they restrict candidate parameters. Second, bounds restrict accepted events and cap reconstructed device power. The wide procedure keeps wider candidate ranges and wider reconstruction rules. So enabling bounds changes both candidate generation and reconstruction. If performance changes, this experiment cannot tell us how much comes from each part. Also, these declared ranges are engineering assumptions. We have not measured the true feasible region.

### 第 6 頁

原稿：

> Our primary outcome is load-state detection. MCC stands for Matthews correlation coefficient. For each device, we compare predicted on and off states with test labels. We count true positives, true negatives, false positives, and false negatives, then calculate one MCC for that device. To calculate macro MCC, we add the 9 MCC scores and divide by 9. Each device receives equal weight, regardless of its duration or power rating. We average device scores rather than combine all devices into one confusion matrix. This test metric is separate from the aggregate-only selection score. We use test labels only after selection is locked. Event F-one is secondary.

v11：

> Our primary outcome is load-state detection. MCC stands for Matthews correlation coefficient. For each device, we compare its predicted on and off states with the test labels. We calculate one MCC score for each device. For macro MCC, we add the 9 scores and divide by 9. Each device has equal weight. This test metric is separate from the aggregate-only selection score. We use test labels only after selection is locked. Event F-one is secondary.

### 第 8 頁

原稿：

> Across 5 LLM test seeds, mean MCC was 0.6262 without bounds, with a sample standard deviation of 0.1131. With bounds, the mean was 0.5951, with a smaller standard deviation of 0.0413. So bounds reduced variation, but the mean was also lower. The table below shows the evidence available: 5 LLM test seeds, 1 LHS test seed, and 20 LHS validation seeds. The 20 LHS seeds add no repeated test result. We therefore cannot treat this as a matched repeated-test comparison between LLM and LHS.

v11：

> Across 5 LLM test seeds, mean MCC was 0.6262 without bounds, with a sample standard deviation of 0.1131. With bounds, the mean was 0.5951, with a smaller standard deviation of 0.0413. So bounds reduced variation, but the mean was also lower. The table shows only 1 LHS test seed. There are also 20 LHS validation seeds. These add no repeated test result. We therefore cannot treat this as a matched repeated-test comparison between LLM and LHS.

### 第 9 頁

原稿：

> Here, we use only validation data for an extra check. We check how many candidates meet all the engineering limits. Only 5 out of 225 LLM configurations did so, or 2.22%. For LHS, 54 out of 900 did so, or 6%. The LLM proposals were closer to the ranges on average, but fewer met all the limits at once. Also, none of the selected unbounded configurations from either source were fully compliant. Being close to a range does not mean meeting every limit. These numbers show whether candidates meet the engineering limits. This check adds no new test results.

v11：

> Here, we use only validation data for an extra check. We check how many candidates meet all the engineering limits. Only 2.22% of LLM configurations met all the limits. For LHS, the figure was 6%. The LLM proposals were closer to the ranges on average, but fewer met all the limits at once. Also, none of the selected unbounded configurations from either source were fully compliant. This check adds no new test results.

### 第 10 頁

原稿：

> This page uses unbounded validation pools only. Every delta means LLM minus LHS. A pool ceiling is the best validation MCC available inside that fixed pool. Selection regret is the gap between this ceiling and the score of the chosen candidate. Selected MCC therefore equals ceiling minus regret. In the first row, with equal device weights, the selected difference is 0.3150. A higher pool ceiling and lower selection regret both contribute. In the second row, with equal dataset weights, the selected difference is 0.2786. The ceiling difference is close to zero, so lower regret explains most of the difference. These are post-hoc diagnostics. The oracle uses validation labels to find the ceiling. We cannot use it as a label-free selector.

v11：

> This page uses unbounded validation pools only. Every delta means LLM minus LHS. A pool ceiling is the best validation MCC available inside that fixed pool. Selection regret is the gap between this ceiling and the score of the chosen candidate. Selected MCC therefore equals ceiling minus regret. In the first row, with equal device weights, the selected difference is 0.3150. A higher pool ceiling and lower selection regret both contribute. In the second row, with equal dataset weights, the selected difference is 0.2786. The ceiling difference is close to zero, so lower regret explains most of the difference. We do this extra analysis after selection. The oracle uses validation labels to find the ceiling. We cannot use it as a label-free selector.

### 第 12 頁

原稿：

> The next step is independent controlled validation. We would specify device states, physical behavior, and a feasible region independently of the generators. Then we would test correct, boundary-adjacent, and misspecified bounds while separating candidate restrictions from reconstruction caps. That would show when bounds help, when generation adds value, and when the procedure fails. For now, assess bounds, the selector, and a simple baseline together.

v11：

> The next step is independent controlled validation. We would specify device states, physical behavior, and a feasible region independently of the generators. We would test correct bounds, bounds near the boundary, and incorrect bounds. We would test candidate limits and reconstruction caps separately. That would show when bounds help, when generation adds value, and when the procedure fails. For now, assess bounds, the selector, and a simple baseline together.

## 保留作為備答的原細節

第 3 頁：For the LLM, device proposals were joined by index, rather than by every possible combination.

第 5 頁：Examples include power factor and on-ratio. Bounded LHS samples directly within the ranges, without clipping or rejecting wide samples.

第 6 頁：各設備各自計算 TP、TN、FP、FN 後得到 MCC；macro MCC 等權重平均，並非先把所有設備合成一個 confusion matrix。

這些細節保留於此供備答查閱；不另增 Q&A 音軌或改寫既有 Q&A。

## 維護與驗收契約

資料流：extension-v11.json → 原 v7 簡報產生器及 v11 講稿 → 140 字元 TTS 分段 → 3090 複製聲音 WAV → loudnorm MP3 → 原 WAV CTC 對齊 → 綁定音檔與字稿 SHA-256 → 內嵌 Shadow → GitHub Pages。

音訊參數不變：Qwen3-TTS-12Hz-1.7B-Base，x-vector-only，max_new_tokens=512，單片段超過或等於 20.8 秒拒絕；既有聲音參考檔 SHA-256 f191156890b60d505173f5ef33e0a72736297728f938f5884f244e86efbee8ba。MP3 loudnorm -16 LUFS、TP -1.5 dB、LRA 11，不調整生成速度。NILM／LLM／LHS 沿用逐字母，MCC 沿用逗號分隔字母；小數保留 zero。

僅對本次新輸入生成音訊；既有快取先核對輸入文字及原 WAV hash。先跑第 6／10 頁三個新片段，再擴大到其餘工作。缺 WAV、token 對齊不符、音檔或字稿 hash 改變、超時、部署失敗均不得宣稱完成；失敗訊息回報於本次對話，不啟用背景排程。

驗收：七頁範圍／數字／證據限制／未改頁一致；14 頁簡報視覺一致、備註只有七頁差異；音檔可完整解碼；timings 連續、有界且對應完整字稿；瀏覽器實際播放、高亮、倍速、Repeat All，375／768／1280px；Pages built 且 commit 一致；正式資產 GET/hash 與畫面讀回。這些檢查不等於人耳逐字審聽或使用者已達成 13 分鐘。

回復方式：v10 JSON 與既有 Git 歷史保留，可按舊版重建整套講稿／音檔／時間戳並用新提交發布，不能單獨回復音檔造成高亮錯位。不得刪除其他教材或強推歷史。
