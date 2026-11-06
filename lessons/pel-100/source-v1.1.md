---
received: 2026-11-06T07:46:15.113Z
type: mcp-note
source: claude-chat
---

---
title: "PEL 100段情境英文教材庫 v1.1"
date: 2026-11-06
category: personal/learning
tags: [PEL, OLMCP, Open Learning MCP, English, A2, B1, 教材庫, 情境英文, 原創]
type: note
source: "原創思考：2026-11-06 使用者與 ChatGPT 對話所設計之100段原創英文情境；非竹岡廣信《Dragon English》原文"
---

# PEL 100段情境英文教材庫 v1.1

## 目的與來源
此筆記是 **Personal English Loop（PEL）／Open Learning MCP（OLMCP）** 的原創 English Domain Pack 基礎 Corpus。2026-11-06 從對話中的100段英文情境 v1.0 重新編排順序，每段保留**原始中文／英文標題、完整4句英文、三項能力 T/L/E、原版編號**。**非**竹岡廣信《Dragon English 基本英文100》的100句摘錄、改寫或授權翻譯；僅借鑑「少量高遷移價值句型」理念。

收錄時間：2026-11-06（Asia/Taipei）。狀態：**教材初稿 v1.1／規格與內容已建檔；尚未完成 CEFR 專業校準、母語者審稿、實際學習成效驗證或程式部署。**

## 使用方法（給 Agent 與教材設計者）
1. **推薦順序**：canonical_order 001–100 是標準難度／通用實用度排序。實際學員的 adaptive_order 可依情境偏好（生活、旅遊、工作、研究）及能力調整，但必須評估當前句子難度，而非只依主題分類。
2. **T（Tense）** 檢查時態和時間觀念；**L（Logic）** 檢查四句之間的事件／因果／比較邏輯；**E（Expression）** 檢查自然英文 chunks 的重新組句能力。
3. **一次一題**：先理解→跟讀 Shadowing→替換詞與句型→Agent 提問（一次一題）→學員不看原文自主回答→一次只修正一個主要問題→跨情境遷移驗證。
4. **能力證據**：逐項記錄 T/L/E 達成與否、提示程度、原創回答、錯誤類型、重試時間；**背誦正確≠能力通過**。
5. **螺旋複現**：相同句型在不同場景重複出現，從短句增加 because／but／if／完成式／假設；若高實用教材的語法高於學員能力，應先由 Agent 生成**明確標成衍生教材**的簡化版，後續再使用本庫原版。
6. **版控**：lesson_id 為新排序（新001…新100），origin_id 為對話 v1.0 原編號；不要用排序變動破壞學員歷史紀錄。後續升版應使用穩定不變的內部教材 ID。此處僅為筆記，不代表已設計完成正式 DB schema。
7. **隱私**：本庫是教學素材，不含真實學員學習回應；個人表現只能寫入個別 OAuth 限定的 Learning State，不可回填共用教材庫。

相關規格： [OLMCP 教學協定核心規格 v0.1](https://github.com/AlanChen75/knowledge-base/blob/main/tech/agent/2026-11-04-OLMCP-教學協定核心規格-v0.1.md)；2026-11-06 已追加100段教材排序與使用規則。

## 五階段配置
| 新編號 | 難度設計（初步估計） | 能力焦點 |
|---|---|---|
| 001–020 | A2 | 自介、習慣、生活基本請求、簡短敘述 |
| 021–040 | A2→A2+ | 問路、服務、問題說明、協助、事件回顧 |
| 041–060 | A2+→B1 | 工作進度、已完成事件、因果、處理與追蹤 |
| 061–080 | B1 | 經驗、比較、觀點、理由、決策 |
| 081–100 | B1 | 提案、商業溝通、研究說明、證據與風險 |

**注意：** 此處 A2/B1 為教學設計意圖而非正式 CEFR 逐句驗證；如某些前段文本出現超前語法，教學應支援簡化版並且不能把它錯誤評為純 A2。

## 新舊編號映射表

| 新編號 | 原版編號 | 情境 | 階段 |
|---|---|---|---|
| 001 | 001 | 自我介紹 | 1 |
| 002 | 003 | 早晨習慣 | 1 |
| 003 | 002 | 我的家庭 | 1 |
| 004 | 012 | 住家附近 | 1 |
| 005 | 006 | 飲食習慣 | 1 |
| 006 | 041 | 介紹自己的工作 | 1 |
| 007 | 021 | 在咖啡店點餐 | 1 |
| 008 | 024 | 結帳付款 | 1 |
| 009 | 033 | 買衣服 | 1 |
| 010 | 015 | 購買日用品 | 1 |
| 011 | 025 | 問路 | 1 |
| 012 | 026 | 搭火車 | 1 |
| 013 | 022 | 預訂餐廳 | 1 |
| 014 | 031 | 飯店入住 | 1 |
| 015 | 018 | 慶祝生日 | 1 |
| 016 | 016 | 在家煮飯 | 1 |
| 017 | 010 | 我的興趣 | 1 |
| 018 | 004 | 忙碌的一天 | 1 |
| 019 | 005 | 週末計畫 | 1 |
| 020 | 042 | 認識新同事 | 1 |
| 021 | 028 | 搭計程車 | 2 |
| 022 | 029 | 機場報到 | 2 |
| 023 | 023 | 特殊飲食需求 | 2 |
| 024 | 037 | 寄送包裹 | 2 |
| 025 | 038 | 銀行開戶 | 2 |
| 026 | 039 | 網路故障 | 2 |
| 027 | 032 | 飯店房間問題 | 2 |
| 028 | 034 | 商品退貨 | 2 |
| 029 | 040 | 化解誤會 | 2 |
| 030 | 044 | 安排會議 | 2 |
| 031 | 045 | 說明議程 | 2 |
| 032 | 048 | 工作優先順序 | 2 |
| 033 | 050 | 確認任務 | 2 |
| 034 | 049 | 尋求協助 | 2 |
| 035 | 017 | 和朋友見面 | 2 |
| 036 | 008 | 睡眠與健康 | 2 |
| 037 | 007 | 運動習慣 | 2 |
| 038 | 011 | 我的家鄉 | 2 |
| 039 | 019 | 面對壓力 | 2 |
| 040 | 027 | 錯過公車 | 2 |
| 041 | 043 | 每日工作會議 | 3 |
| 042 | 046 | 進度報告 | 3 |
| 043 | 047 | 期限延後 | 3 |
| 044 | 051 | 回報問題 | 3 |
| 045 | 052 | 提出解決方案 | 3 |
| 046 | 053 | 給予建設性回饋 | 3 |
| 047 | 054 | 接受批評 | 3 |
| 048 | 055 | 說明數據 | 3 |
| 049 | 056 | 遠端協作 | 3 |
| 050 | 057 | 了解客戶需求 | 3 |
| 051 | 058 | 產品展示 | 3 |
| 052 | 059 | 處理團隊意見分歧 | 3 |
| 053 | 060 | 專案檢討 | 3 |
| 054 | 009 | 學英文的原因 | 3 |
| 055 | 020 | 今年的目標 | 3 |
| 056 | 030 | 班機延誤 | 3 |
| 057 | 035 | 在藥局詢問 | 3 |
| 058 | 036 | 醫生看診 | 3 |
| 059 | 014 | 照顧寵物 | 3 |
| 060 | 013 | 天氣影響計畫 | 3 |
| 061 | 061 | 第一份工作 | 4 |
| 062 | 062 | 從錯誤中學習 | 4 |
| 063 | 063 | 面對失敗 | 4 |
| 064 | 064 | 計畫突然改變 | 4 |
| 065 | 065 | 最有成就感的事情 | 4 |
| 066 | 066 | 困難的選擇 | 4 |
| 067 | 067 | 兩種工作方式 | 4 |
| 068 | 068 | 選擇工具 | 4 |
| 069 | 069 | 別人的建議 | 4 |
| 070 | 070 | 遠端工作好不好 | 4 |
| 071 | 071 | AI與學習 | 4 |
| 072 | 072 | 再生能源 | 4 |
| 073 | 073 | 永續生活 | 4 |
| 074 | 074 | 城市與鄉村 | 4 |
| 075 | 075 | 公共運輸 | 4 |
| 076 | 076 | 消費與儲蓄 | 4 |
| 077 | 077 | 閱讀與思考 | 4 |
| 078 | 078 | 難忘的旅行 | 4 |
| 079 | 079 | 文化差異 | 4 |
| 080 | 080 | 改變自己的想法 | 4 |
| 081 | 081 | 一分鐘自我介紹 | 5 |
| 082 | 082 | 說明市場問題 | 5 |
| 083 | 083 | 訪談客戶 | 5 |
| 084 | 084 | 最小可行產品 | 5 |
| 085 | 085 | 競爭優勢 | 5 |
| 086 | 086 | 市場驗證 | 5 |
| 087 | 087 | 商業模式 | 5 |
| 088 | 088 | 評估風險 | 5 |
| 089 | 089 | 長期願景 | 5 |
| 090 | 090 | 資料隱私 | 5 |
| 091 | 091 | 介紹研究主題 | 5 |
| 092 | 092 | 提出研究假設 | 5 |
| 093 | 093 | 說明研究方法 | 5 |
| 094 | 094 | 解釋意外的結果 | 5 |
| 095 | 095 | 研究限制 | 5 |
| 096 | 096 | 回答聽眾問題 | 5 |
| 097 | 097 | 商業協商 | 5 |
| 098 | 098 | 回應反對意見 | 5 |
| 099 | 099 | 情境推演 | 5 |
| 100 | 100 | 總結與下一步 | 5 |

## 正式情境內容

## 第 1 階段｜立即能用／A2：先能說、會請求（新 001–020）

### 001｜自我介紹（Introducing Myself）

- **origin_id**：001
- **English（4句）**：Hi, I'm Sam. I work with technology and business. I enjoy learning new things. I want to improve my English so I can talk to more people.
- **T 時態**：現在式／目標表達
- **L 邏輯**：身分→工作→興趣→目標
- **E 表達**：work with；want to

### 002｜早晨習慣（My Morning Routine）

- **origin_id**：003
- **English（4句）**：I usually wake up at seven. After breakfast, I check my messages. Then I make a plan for the day. This helps me stay organized.
- **T 時態**：現在簡單式
- **L 邏輯**：時間順序→效果
- **E 表達**：after；then；help me

### 003｜我的家庭（My Family）

- **origin_id**：002
- **English（4句）**：I live with my family. We usually have dinner together. Everyone is busy during the day. That's why we enjoy talking at night.
- **T 時態**：現在簡單式
- **L 邏輯**：日常習慣→原因→結果
- **E 表達**：usually；that's why

### 004｜住家附近（My Neighborhood）

- **origin_id**：012
- **English（4句）**：There is a small park near my home. Many people go there in the evening. I sometimes walk there after dinner. It's a nice place to relax.
- **T 時態**：現在簡單式
- **L 邏輯**：地點→活動→個人體驗
- **E 表達**：there is；a nice place to

### 005｜飲食習慣（Eating Habits）

- **origin_id**：006
- **English（4句）**：I try to eat healthy food every day. I usually have vegetables and rice for lunch. Sometimes I eat too much when I'm busy. I'm trying to change that habit.
- **T 時態**：現在式／現在進行式
- **L 邏輯**：習慣→例外→改善
- **E 表達**：try to；too much

### 006｜介紹自己的工作（Describing My Job）

- **origin_id**：041
- **English（4句）**：I work as a project manager. My job is to help different teams work together. I spend a lot of time solving problems. What I enjoy most is seeing a project succeed.
- **T 時態**：現在簡單式
- **L 邏輯**：職位→職責→日常→成就感
- **E 表達**：work as；what I enjoy most

### 007｜在咖啡店點餐（Ordering Coffee）

- **origin_id**：021
- **English（4句）**：I'd like a medium coffee, please. Could you make it without sugar? I'll have it to go because I'm in a hurry. How much is it altogether?
- **T 時態**：現在式／禮貌請求
- **L 邏輯**：需求→條件→原因→詢價
- **E 表達**：I'd like；could you

### 008｜結帳付款（Paying the Bill）

- **origin_id**：024
- **English（4句）**：Excuse me, could we have the bill, please? We'd like to split it into two payments. I'll pay my part by card. Thank you for your help.
- **T 時態**：現在式／禮貌請求
- **L 邏輯**：結帳→分帳→付款
- **E 表達**：split the bill；pay by card

### 009｜買衣服（Buying Clothes）

- **origin_id**：033
- **English（4句）**：I'm looking for a jacket for work. This one looks nice, but it's a little too small. Do you have it in a larger size? I'd like to try it on before deciding.
- **T 時態**：現在進行式
- **L 邏輯**：需求→評估→詢問→決策
- **E 表達**：looking for；try it on

### 010｜購買日用品（Grocery Shopping）

- **origin_id**：015
- **English（4句）**：I went to the supermarket after work. I needed some milk, eggs, and vegetables. The store was crowded, so I finished shopping quickly. Luckily, I found everything on my list.
- **T 時態**：過去式
- **L 邏輯**：目的→障礙→結果
- **E 表達**：needed some；luckily

### 011｜問路（Asking for Directions）

- **origin_id**：025
- **English（4句）**：Excuse me, how can I get to the train station? Is it within walking distance? I'm not familiar with this area. Could you show me the way on a map?
- **T 時態**：現在式
- **L 邏輯**：目的地→距離→原因→請求
- **E 表達**：get to；within walking distance

### 012｜搭火車（Taking a Train）

- **origin_id**：026
- **English（4句）**：I need a ticket to the city center. Is there a direct train, or do I need to transfer? I'd prefer the fastest route. Could you tell me which platform to use?
- **T 時態**：現在式
- **L 邏輯**：目的→路線比較→選擇
- **E 表達**：direct train；need to transfer

### 013｜預訂餐廳（Booking a Restaurant）

- **origin_id**：022
- **English（4句）**：I'd like to book a table for four people. Do you have anything available around seven tonight? We prefer a quiet area if possible. Could you confirm the reservation by text?
- **T 時態**：現在式
- **L 邏輯**：需求→時間→偏好→確認
- **E 表達**：book a table；if possible

### 014｜飯店入住（Checking Into a Hotel）

- **origin_id**：031
- **English（4句）**：Hello, I have a reservation under the name Chen. I booked a room for two nights. Is breakfast included in the price? Also, what time do I need to check out?
- **T 時態**：現在式／過去式
- **L 邏輯**：訂房確認→服務→退房
- **E 表達**：under the name；included

### 015｜慶祝生日（Celebrating a Birthday）

- **origin_id**：018
- **English（4句）**：Today is my mother's birthday. We're having dinner at her favorite restaurant. I bought her a small gift yesterday. I hope she enjoys the surprise.
- **T 時態**：現在式／過去式
- **L 邏輯**：特別日子→安排→心意
- **E 表達**：favorite；hope

### 016｜在家煮飯（Cooking at Home）

- **origin_id**：016
- **English（4句）**：I'm learning to cook simple meals. Yesterday, I made dinner for my family. The food wasn't perfect, but everyone enjoyed it. I'll try a different recipe next time.
- **T 時態**：現在進行式／過去式／未來式
- **L 邏輯**：嘗試→結果→改善
- **E 表達**：learn to；next time

### 017｜我的興趣（My Hobbies）

- **origin_id**：010
- **English（4句）**：I enjoy reading about new technology. Last week, I watched a video about robots. It gave me some interesting ideas. I'd like to learn more about this topic.
- **T 時態**：現在式／過去式
- **L 邏輯**：興趣→事件→收穫→延伸
- **E 表達**：enjoy -ing；would like to

### 018｜忙碌的一天（A Busy Day）

- **origin_id**：004
- **English（4句）**：I had a busy day yesterday. I attended two meetings and finished a report. I felt tired when I got home. However, I was happy with my progress.
- **T 時態**：過去式
- **L 邏輯**：事件→感受→轉折
- **E 表達**：felt tired；however

### 019｜週末計畫（Weekend Plans）

- **origin_id**：005
- **English（4句）**：I'm going to visit my friends this weekend. We plan to have lunch together. If the weather is nice, we'll go for a walk. I hope we can spend more time together.
- **T 時態**：未來式／第一類條件句
- **L 邏輯**：計畫→條件→期待
- **E 表達**：be going to；if

### 020｜認識新同事（Meeting a New Colleague）

- **origin_id**：042
- **English（4句）**：Welcome to the team. I joined this company three years ago. I mainly work on product development. If you need any help, feel free to ask me.
- **T 時態**：過去式／現在式
- **L 邏輯**：歡迎→背景→角色→協助
- **E 表達**：mainly；feel free to

## 第 2 階段｜日常互動與問題處理／A2→A2+（新 021–040）

### 021｜搭計程車（Taking a Taxi）

- **origin_id**：028
- **English（4句）**：Could you take me to this address? I'm running a little late for a meeting. If possible, please use the fastest route. Let me know when we're close to the building.
- **T 時態**：現在進行式／祈使句
- **L 邏輯**：目的→原因→要求
- **E 表達**：running late；let me know

### 022｜機場報到（Airport Check-In）

- **origin_id**：029
- **English（4句）**：I'm checking in for my flight to Singapore. I have one suitcase to check and one carry-on bag. Could I have an aisle seat if one is available? Please let me know if the flight is on time.
- **T 時態**：現在進行式／條件句
- **L 邏輯**：報到→行李→座位→確認
- **E 表達**：check in；carry-on；aisle seat

### 023｜特殊飲食需求（Food Preferences）

- **origin_id**：023
- **English（4句）**：I'm looking for something without dairy. Do you have any dishes that would work for me? I can eat vegetables, rice, and seafood. If you're not sure, could you check with the kitchen?
- **T 時態**：現在式／條件句
- **L 邏輯**：限制→詢問→可接受範圍
- **E 表達**：looking for；check with

### 024｜寄送包裹（Sending a Package）

- **origin_id**：037
- **English（4句）**：I'd like to send this package overseas. It contains some books and small gifts. How long will delivery usually take? I'd also like a tracking number if possible.
- **T 時態**：現在式／未來式
- **L 邏輯**：目的→內容→時間→追蹤
- **E 表達**：send overseas；tracking number

### 025｜銀行開戶（Opening a Bank Account）

- **origin_id**：038
- **English（4句）**：I'd like to open a savings account. I already have my passport and identification documents. Could you explain the monthly fees? I'd also like to know whether I can manage the account online.
- **T 時態**：現在式／情態動詞
- **L 邏輯**：需求→準備→費用→功能
- **E 表達**：open an account；whether

### 026｜網路故障（An Internet Problem）

- **origin_id**：039
- **English（4句）**：My internet connection stopped working this morning. I've already restarted the router twice. The problem is still there. Could you help me check whether there's a service outage?
- **T 時態**：過去式／現在完成式
- **L 邏輯**：問題→已嘗試→現況→請求
- **E 表達**：restart；service outage

### 027｜飯店房間問題（A Problem With the Room）

- **origin_id**：032
- **English（4句）**：I'm having trouble with the air conditioner. It doesn't seem to be working properly. Could someone come and take a look? If it can't be fixed, I'd like to change rooms.
- **T 時態**：現在進行式／被動式
- **L 邏輯**：問題→請求→替代方案
- **E 表達**：having trouble with；take a look

### 028｜商品退貨（Returning an Item）

- **origin_id**：034
- **English（4句）**：I bought these headphones last week. Unfortunately, the left side doesn't work. I still have the receipt and the original box. Could I get a replacement or a refund?
- **T 時態**：過去式／現在式
- **L 邏輯**：購買→問題→證明→要求
- **E 表達**：replacement；refund

### 029｜化解誤會（Clearing Up a Misunderstanding）

- **origin_id**：040
- **English（4句）**：I think there was a misunderstanding. I didn't mean to cancel the meeting. I only wanted to change the time. Sorry if my message wasn't clear enough.
- **T 時態**：過去式
- **L 邏輯**：指出誤會→澄清→致歉
- **E 表達**：misunderstanding；didn't mean to

### 030｜安排會議（Scheduling a Meeting）

- **origin_id**：044
- **English（4句）**：We need to discuss the new project. Are you available on Thursday afternoon? If that doesn't work, we can meet on Friday morning. Let me know which time is better for you.
- **T 時態**：現在式／條件句
- **L 邏輯**：目的→選項→替代方案
- **E 表達**：are you available；let me know

### 031｜說明議程（Explaining the Agenda）

- **origin_id**：045
- **English（4句）**：Today, we have three things to discuss. First, we'll review the project schedule. Next, we'll look at the main problems. Finally, we'll decide who will handle each task.
- **T 時態**：未來式
- **L 邏輯**：有序列舉→決策
- **E 表達**：first；next；finally

### 032｜工作優先順序（Setting Priorities）

- **origin_id**：048
- **English（4句）**：We have several tasks to finish this week. Some are urgent, but others can wait. I suggest we focus on the customer issue first. After that, we can work on the new features.
- **T 時態**：現在式／情態動詞
- **L 邏輯**：任務→分類→建議→次序
- **E 表達**：focus on；I suggest

### 033｜確認任務（Clarifying a Task）

- **origin_id**：050
- **English（4句）**：Before I start, I'd like to confirm the requirements. Do you need a short summary or a detailed report? I can prepare either one. I just want to make sure we're working toward the same goal.
- **T 時態**：現在式
- **L 邏輯**：確認→選項→原因
- **E 表達**：make sure；work toward

### 034｜尋求協助（Asking for Help）

- **origin_id**：049
- **English（4句）**：I'm having trouble understanding this report. I've checked the numbers, but something doesn't look right. Could you review it with me? I think a second opinion would be helpful.
- **T 時態**：現在進行式／現在完成式
- **L 邏輯**：困難→已採取行動→請求
- **E 表達**：having trouble；second opinion

### 035｜和朋友見面（Meeting an Old Friend）

- **origin_id**：017
- **English（4句）**：I met an old friend yesterday. We hadn't seen each other for years. We talked about our jobs and families. It felt as if no time had passed.
- **T 時態**：過去完成式／過去式
- **L 邏輯**：重逢→背景→交流→感受
- **E 表達**：each other；as if

### 036｜睡眠與健康（Getting Enough Sleep）

- **origin_id**：008
- **English（4句）**：I didn't sleep well last night. I stayed up late to finish some work. As a result, I felt tired this morning. Tonight, I'll try to go to bed earlier.
- **T 時態**：過去式／未來式
- **L 邏輯**：原因→結果→改善
- **E 表達**：stay up late；as a result

### 037｜運動習慣（Staying Active）

- **origin_id**：007
- **English（4句）**：I started walking every evening last month. At first, it was difficult to keep going. Now I feel stronger and sleep better. Small changes can make a big difference.
- **T 時態**：過去式與現在式
- **L 邏輯**：開始→困難→改善
- **E 表達**：at first；make a difference

### 038｜我的家鄉（My Hometown）

- **origin_id**：011
- **English（4句）**：I grew up in a small town. It was quiet and had many beautiful places. Although I live in a big city now, I still miss my hometown. I visit it whenever I have time.
- **T 時態**：過去式／現在式
- **L 邏輯**：過去→現在→情感
- **E 表達**：grew up；although；whenever

### 039｜面對壓力（Dealing with Stress）

- **origin_id**：019
- **English（4句）**：I sometimes feel stressed when I have too much work. When that happens, I take a short break. A few minutes of walking helps me think clearly. I've learned that rest is also important.
- **T 時態**：現在式／現在完成式
- **L 邏輯**：問題→應對→體會
- **E 表達**：when that happens；I've learned that

### 040｜錯過公車（Missing the Bus）

- **origin_id**：027
- **English（4句）**：I missed the bus this morning. I arrived at the stop just a minute too late. The next bus wasn't coming for another twenty minutes. So I decided to take a taxi instead.
- **T 時態**：過去式／過去進行式
- **L 邏輯**：失誤→後果→替代方案
- **E 表達**：just a minute too late；instead

## 第 3 階段｜描述經驗與工作／A2+→B1（新 041–060）

### 041｜每日工作會議（Daily Team Meeting）

- **origin_id**：043
- **English（4句）**：Yesterday, I finished the first version of the report. Today, I'll review it with the team. I still need some data from the sales department. Once I get it, I can finish the analysis.
- **T 時態**：過去式／未來式
- **L 邏輯**：昨日成果→今日安排→阻礙→條件
- **E 表達**：still need；once I get

### 042｜進度報告（Giving a Progress Update）

- **origin_id**：046
- **English（4句）**：The project is moving forward as planned. We've completed most of the testing. However, we still have a few technical issues. We expect to solve them by the end of the week.
- **T 時態**：現在進行式／現在完成式
- **L 邏輯**：進度→成果→問題→預期
- **E 表達**：as planned；expect to

### 043｜期限延後（Explaining a Delay）

- **origin_id**：047
- **English（4句）**：We may need two more days to finish the work. One of our suppliers delivered the materials late. As a result, we couldn't start testing on time. We're adjusting the schedule to reduce the delay.
- **T 時態**：過去式／現在進行式
- **L 邏輯**：延期→原因→影響→對策
- **E 表達**：as a result；on time

### 044｜回報問題（Reporting an Issue）

- **origin_id**：051
- **English（4句）**：We found a problem during yesterday's test. The system stopped responding after several hours. We haven't identified the cause yet. We're collecting more information before making changes.
- **T 時態**：過去式／現在完成式
- **L 邏輯**：發現→現象→未知→調查
- **E 表達**：identify the cause；before -ing

### 045｜提出解決方案（Suggesting a Solution）

- **origin_id**：052
- **English（4句）**：I think we should try a simpler approach. The current process takes too much time. If we automate one part of it, we could reduce manual work. Let's test the idea before making a larger change.
- **T 時態**：現在式／假設語氣
- **L 邏輯**：問題→方案→效益→驗證
- **E 表達**：should；if we；let's

### 046｜給予建設性回饋（Giving Feedback）

- **origin_id**：053
- **English（4句）**：Your presentation was clear and easy to follow. I especially liked the examples. One thing you could improve is the final summary. It might help to end with a clear recommendation.
- **T 時態**：過去式／情態動詞
- **L 邏輯**：肯定→具體優點→改善建議
- **E 表達**：one thing you could improve；might help

### 047｜接受批評（Receiving Feedback）

- **origin_id**：054
- **English（4句）**：Thank you for your feedback. I hadn't noticed that problem before. I'll review the presentation and make some changes. Please let me know if there's anything else I should improve.
- **T 時態**：過去完成式／未來式
- **L 邏輯**：感謝→理解→行動→確認
- **E 表達**：hadn't noticed；anything else

### 048｜說明數據（Explaining Data）

- **origin_id**：055
- **English（4句）**：Sales increased last month. However, our costs also went up. This means our profit didn't grow as much as expected. We need to understand what's driving the higher costs.
- **T 時態**：過去式
- **L 邏輯**：數據→對比→解讀→待研究問題
- **E 表達**：went up；as much as expected

### 049｜遠端協作（Working Remotely）

- **origin_id**：056
- **English（4句）**：Our team works in different cities. We use online tools to share files and discuss ideas. Sometimes communication takes longer than expected. That's why we write down important decisions after each meeting.
- **T 時態**：現在簡單式
- **L 邏輯**：工作模式→工具→問題→制度
- **E 表達**：write down；that's why

### 050｜了解客戶需求（Understanding a Customer）

- **origin_id**：057
- **English（4句）**：Before we suggest a solution, we need to understand the customer's problem. I'll ask how their current process works. Then I'll find out where they lose the most time. This information will help us design a better system.
- **T 時態**：現在式／未來式
- **L 邏輯**：先理解→訪談→找瓶頸→設計
- **E 表達**：find out；help us design

### 051｜產品展示（Demonstrating a Product）

- **origin_id**：058
- **English（4句）**：Let me show you how the system works. First, you connect the device to the network. The system then collects data automatically. If it detects a problem, it sends you a notification.
- **T 時態**：現在式／條件句
- **L 邏輯**：操作→資料→判斷→通知
- **E 表達**：let me show you；if it detects

### 052｜處理團隊意見分歧（Handling Disagreement）

- **origin_id**：059
- **English（4句）**：We have different opinions about this design. I understand why you prefer the first option. However, I'm concerned about its long-term cost. Could we compare both options before making a decision?
- **T 時態**：現在式
- **L 邏輯**：承認差異→理解→疑慮→比較
- **E 表達**：I'm concerned about；could we

### 053｜專案檢討（Reviewing a Project）

- **origin_id**：060
- **English（4句）**：We finished the project last week. Some parts went well, but others took longer than expected. We've learned several lessons from the experience. Next time, we'll spend more time checking the requirements at the beginning.
- **T 時態**：過去式／現在完成式／未來式
- **L 邏輯**：完成→檢討→學習→改進
- **E 表達**：lessons learned；next time

### 054｜學英文的原因（Why I Learn English）

- **origin_id**：009
- **English（4句）**：I've been learning English for several months. I want to speak more naturally. Sometimes I know the words but cannot make a sentence quickly. That's why I practice speaking every day.
- **T 時態**：現在完成進行式
- **L 邏輯**：學習背景→問題→行動
- **E 表達**：have been learning；that's why

### 055｜今年的目標（My Goals This Year）

- **origin_id**：020
- **English（4句）**：I set three goals at the beginning of this year. One of them was to improve my English. I've made some progress, but I still need more practice. By the end of the year, I hope to speak with more confidence.
- **T 時態**：過去式／現在完成式／未來目標
- **L 邏輯**：目標→進度→下一步
- **E 表達**：make progress；by the end of

### 056｜班機延誤（A Delayed Flight）

- **origin_id**：030
- **English（4句）**：My flight has been delayed by two hours. I was supposed to arrive before dinner. Now I need to change my plans. I'll let my friends know as soon as I have a new arrival time.
- **T 時態**：現在完成式／過去預期／未來式
- **L 邏輯**：變化→影響→應對
- **E 表達**：be supposed to；as soon as

### 057｜在藥局詢問（At the Pharmacy）

- **origin_id**：035
- **English（4句）**：I've had a sore throat since yesterday. I don't have a fever, but it hurts when I swallow. Is there anything that might help? Could you explain how to use it safely?
- **T 時態**：現在完成式
- **L 邏輯**：症狀→補充→詢問
- **E 表達**：I've had；anything that might help

### 058｜醫生看診（Visiting a Doctor）

- **origin_id**：036
- **English（4句）**：I've been feeling tired for several days. I've also been having trouble sleeping. I'm not sure whether the two problems are related. I'd like to know what I should do next.
- **T 時態**：現在完成進行式
- **L 邏輯**：症狀→疑問→求助
- **E 表達**：have trouble -ing；be related

### 059｜照顧寵物（Taking Care of a Pet）

- **origin_id**：014
- **English（4句）**：My cat usually eats twice a day. Recently, she has been eating less than usual. I've started keeping a record of her meals. I want to understand whether something has changed.
- **T 時態**：現在式／現在完成進行式
- **L 邏輯**：正常行為→變化→觀察
- **E 表達**：less than usual；keep a record

### 060｜天氣影響計畫（Weather and Plans）

- **origin_id**：013
- **English（4句）**：It was raining when I woke up. I had planned to ride my bike. Instead, I decided to stay home and read. Sometimes a change of plans can be relaxing.
- **T 時態**：過去進行式／過去完成式
- **L 邏輯**：預期→變化→替代方案
- **E 表達**：instead；decide to

## 第 4 階段｜經驗、比較與觀點／B1（新 061–080）

### 061｜第一份工作（My First Job）

- **origin_id**：061
- **English（4句）**：I got my first job when I was twenty-two. At that time, I didn't know much about business. My manager taught me how to solve problems step by step. That experience helped me become more confident.
- **T 時態**：過去式
- **L 邏輯**：背景→困難→學習→改變
- **E 表達**：at that time；step by step

### 062｜從錯誤中學習（Learning From Mistakes）

- **origin_id**：062
- **English（4句）**：I once made an important mistake at work. I didn't check the information carefully enough. After that, I started reviewing my work before sending it. I learned that small mistakes can have big consequences.
- **T 時態**：過去式
- **L 邏輯**：錯誤→原因→改善→教訓
- **E 表達**：carefully enough；after that

### 063｜面對失敗（Dealing With Failure）

- **origin_id**：063
- **English（4句）**：One of my projects failed a few years ago. We had a good idea, but we didn't understand the market well. Instead of giving up, we studied what went wrong. The experience changed how I approach new projects.
- **T 時態**：過去式
- **L 邏輯**：失敗→原因→反省→成長
- **E 表達**：instead of；what went wrong

### 064｜計畫突然改變（An Unexpected Change）

- **origin_id**：064
- **English（4句）**：We were preparing for an important event when the speaker canceled. Everyone was worried because we had little time. We quickly found another speaker and changed the schedule. In the end, the event went better than we expected.
- **T 時態**：過去進行式／過去式
- **L 邏輯**：意外→壓力→行動→結果
- **E 表達**：in the end；better than expected

### 065｜最有成就感的事情（A Personal Achievement）

- **origin_id**：065
- **English（4句）**：Last year, I completed a project that had taken months of work. There were many problems along the way. My team kept working together until we solved them. I was proud of what we had achieved.
- **T 時態**：過去完成式／過去式
- **L 邏輯**：挑戰→堅持→成果→感受
- **E 表達**：along the way；be proud of

### 066｜困難的選擇（Making a Difficult Decision）

- **origin_id**：066
- **English（4句）**：I once had to choose between two job opportunities. One offered more money, while the other offered better learning opportunities. I thought carefully about my long-term goals. Finally, I chose the job where I could learn more.
- **T 時態**：過去式
- **L 邏輯**：選項→比較→標準→決定
- **E 表達**：choose between；while

### 067｜兩種工作方式（Comparing Work Methods）

- **origin_id**：067
- **English（4句）**：Some people prefer working alone, while others enjoy teamwork. Working alone can help you focus. Teamwork allows people to share different ideas. I think the best choice depends on the task.
- **T 時態**：現在式
- **L 邏輯**：兩種方法→優缺點→條件判斷
- **E 表達**：while；depends on

### 068｜選擇工具（Choosing the Right Tool）

- **origin_id**：068
- **English（4句）**：There are many tools that can do similar things. The most expensive one isn't always the best. I usually compare cost, reliability, and ease of use. What matters most is whether the tool solves the real problem.
- **T 時態**：現在式
- **L 邏輯**：現象→反例→評估標準→原則
- **E 表達**：what matters most；whether

### 069｜別人的建議（Learning From Others）

- **origin_id**：069
- **English（4句）**：A friend once gave me advice about managing my time. At first, I didn't think it would help. However, I decided to try his method for a week. It worked better than I expected.
- **T 時態**：過去式
- **L 邏輯**：建議→懷疑→實驗→結果
- **E 表達**：at first；better than I expected

### 070｜遠端工作好不好（Is Remote Work Better?）

- **origin_id**：070
- **English（4句）**：Remote work gives people more flexibility. They can save time by avoiding long trips to the office. However, it can be harder to communicate with teammates. I believe a mix of remote and office work is often a good solution.
- **T 時態**：現在式
- **L 邏輯**：優點→原因→缺點→立場
- **E 表達**：flexibility；however；a mix of

### 071｜AI與學習（AI and Learning）

- **origin_id**：071
- **English（4句）**：AI has changed how people learn new skills. Students can now ask questions and get feedback quickly. However, getting an answer doesn't always mean understanding it. I think students still need to practice and explain things themselves.
- **T 時態**：現在完成式／現在式
- **L 邏輯**：改變→好處→限制→觀點
- **E 表達**：has changed；doesn't always mean

### 072｜再生能源（Renewable Energy）

- **origin_id**：072
- **English（4句）**：Solar energy is becoming more common in many places. It can help reduce the use of fossil fuels. However, solar panels don't produce the same amount of electricity all day. That's why energy storage and better planning are important.
- **T 時態**：現在進行式／現在式
- **L 邏輯**：趨勢→優點→限制→對策
- **E 表達**：become more common；that's why

### 073｜永續生活（Living More Sustainably）

- **origin_id**：073
- **English（4句）**：Many people want to reduce waste in their daily lives. Some bring reusable bags or avoid buying unnecessary things. These actions may seem small, but they can become good habits. I believe lasting change begins with simple decisions.
- **T 時態**：現在式
- **L 邏輯**：目標→行動→意義→觀點
- **E 表達**：reduce waste；lasting change

### 074｜城市與鄉村（City Life or Country Life）

- **origin_id**：074
- **English（4句）**：Living in a city offers more job opportunities. Public transportation is also more convenient. On the other hand, the countryside is often quieter and less crowded. I'd prefer the city for work but the countryside for relaxation.
- **T 時態**：現在式／偏好表達
- **L 邏輯**：城市優點→鄉村優點→個人選擇
- **E 表達**：on the other hand；I'd prefer

### 075｜公共運輸（Public Transportation）

- **origin_id**：075
- **English（4句）**：I used to drive to work every day. Recently, I've started taking the train more often. It takes about the same amount of time, but I can read during the trip. As a result, my journey feels less stressful.
- **T 時態**：used to／現在完成式
- **L 邏輯**：過去習慣→改變→比較→效果
- **E 表達**：used to；as a result

### 076｜消費與儲蓄（Spending and Saving）

- **origin_id**：076
- **English（4句）**：I try to save part of my income every month. Before buying something expensive, I ask myself whether I really need it. Sometimes waiting a few days helps me make a better decision. I've learned that careful spending is more important than buying things quickly.
- **T 時態**：現在式／現在完成式
- **L 邏輯**：習慣→判斷→方法→體會
- **E 表達**：ask myself whether；I've learned

### 077｜閱讀與思考（Reading and Thinking）

- **origin_id**：077
- **English（4句）**：I recently read a book about decision-making. The author explained why people sometimes make poor choices. One idea was especially interesting to me. We should question our first impression before making important decisions.
- **T 時態**：過去式／情態動詞
- **L 邏輯**：閱讀→重點→啟發→應用
- **E 表達**：especially；first impression

### 078｜難忘的旅行（A Memorable Trip）

- **origin_id**：078
- **English（4句）**：I visited Japan with my family a few years ago. We traveled through several cities and tried many local dishes. What impressed me most was how easy it was to use public transportation. I'd love to visit again someday.
- **T 時態**：過去式／未來意願
- **L 邏輯**：旅行→活動→印象→期待
- **E 表達**：what impressed me most；I'd love to

### 079｜文化差異（Cultural Differences）

- **origin_id**：079
- **English（4句）**：People in different countries may communicate in different ways. In some cultures, being direct is considered helpful. In others, people prefer softer expressions. Understanding these differences can help us avoid misunderstandings.
- **T 時態**：現在式／被動式
- **L 邏輯**：差異→對比→意義
- **E 表達**：in some cultures；in others

### 080｜改變自己的想法（Changing My Mind）

- **origin_id**：080
- **English（4句）**：I used to believe that working longer meant getting more done. Then I noticed that tired people often make more mistakes. I started focusing on results instead of working hours. Now I believe working smarter is more useful than simply working longer.
- **T 時態**：used to／過去式／現在式
- **L 邏輯**：原始信念→新證據→調整→新觀點
- **E 表達**：used to believe；instead of

## 第 5 階段｜專業溝通與進階思考／B1（新 081–100）

### 081｜一分鐘自我介紹（A Short Professional Introduction）

- **origin_id**：081
- **English（4句）**：I've been working in technology and business for several years. My main interest is using AI to solve practical problems. I enjoy turning new ideas into useful products. Today, I'd like to share one of the projects I'm working on.
- **T 時態**：現在完成進行式
- **L 邏輯**：背景→專長→價值→主題
- **E 表達**：my main interest；turn into

### 082｜說明市場問題（Explaining a Market Problem）

- **origin_id**：082
- **English（4句）**：Many small businesses want to use AI but don't know where to start. Existing solutions can be expensive or difficult to manage. As a result, some companies give up before seeing any benefits. We believe there is a better way to solve this problem.
- **T 時態**：現在式
- **L 邏輯**：需求→障礙→後果→機會
- **E 表達**：as a result；there is a better way

### 083｜訪談客戶（Interviewing a Customer）

- **origin_id**：083
- **English（4句）**：Before building our product, we talked to potential customers. We asked them about their daily work and biggest problems. Several people described the same difficulty. This helped us understand which problem we should solve first.
- **T 時態**：過去式／情態動詞
- **L 邏輯**：訪談→發現→問題確認
- **E 表達**：potential customers；help us understand

### 084｜最小可行產品（Building a Simple First Version）

- **origin_id**：084
- **English（4句）**：We don't need to build every feature at the beginning. Instead, we can start with a simple version of the product. This allows us to test whether customers actually need it. If the results are positive, we can add more features later.
- **T 時態**：現在式／條件句
- **L 邏輯**：簡化→測試→條件→擴展
- **E 表達**：instead；start with；if

### 085｜競爭優勢（Explaining Our Advantage）

- **origin_id**：085
- **English（4句）**：There are already several products in this market. However, most of them require expensive equipment. Our solution uses simpler hardware and a flexible software system. This could make it easier for small companies to get started.
- **T 時態**：現在式／情態動詞
- **L 邏輯**：競爭環境→差異→優勢→效益
- **E 表達**：most of them；make it easier to

### 086｜市場驗證（Showing Early Results）

- **origin_id**：086
- **English（4句）**：We tested our first product with a small group of users. Most of them were able to complete the main task. However, some users needed help during setup. We've used their feedback to improve the process.
- **T 時態**：過去式／現在完成式
- **L 邏輯**：測試→成果→問題→改善
- **E 表達**：were able to；feedback

### 087｜商業模式（Explaining How We Make Money）

- **origin_id**：087
- **English（4句）**：Our customers pay a monthly fee to use the service. The price depends on how many devices they connect. This gives small companies a lower starting cost. As their needs grow, they can upgrade to a larger plan.
- **T 時態**：現在式
- **L 邏輯**：收費方式→計價基礎→價值→擴展
- **E 表達**：depends on；as their needs grow

### 088｜評估風險（Understanding Business Risks）

- **origin_id**：088
- **English（4句）**：Every new business faces uncertainty. One major risk is that customers may not be willing to pay. To reduce this risk, we plan to test the pricing before expanding. We'd rather learn early than spend too much money on the wrong idea.
- **T 時態**：現在式／未來計畫
- **L 邏輯**：風險→原因→對策→原則
- **E 表達**：to reduce this risk；would rather

### 089｜長期願景（Sharing a Long-Term Vision）

- **origin_id**：089
- **English（4句）**：Today, our product solves one specific problem. In the future, we hope to connect several related services. This would allow customers to manage their work more easily. Our long-term goal is to build a system that grows with their needs.
- **T 時態**：現在式／未來式／假設語氣
- **L 邏輯**：現況→擴展→效益→願景
- **E 表達**：in the future；long-term goal

### 090｜資料隱私（Protecting User Data）

- **origin_id**：090
- **English（4句）**：AI systems often need data to provide useful services. However, users should know what information is collected. They should also be able to control who can access it. We believe trust is essential for long-term success.
- **T 時態**：現在式／被動式
- **L 邏輯**：需求→風險→權限→信任
- **E 表達**：should be able to；who can access

### 091｜介紹研究主題（Introducing My Research）

- **origin_id**：091
- **English（4句）**：My research focuses on understanding electrical equipment through power data. We collect signals from a main electricity meter. Then we use AI models to identify different operating patterns. The goal is to understand equipment behavior without installing sensors on every machine.
- **T 時態**：現在式
- **L 邏輯**：研究目的→資料→方法→價值
- **E 表達**：focus on；the goal is to

### 092｜提出研究假設（Explaining a Hypothesis）

- **origin_id**：092
- **English（4句）**：We believe that electrical signals contain useful information about machine behavior. If we analyze them carefully, we may be able to identify unusual patterns. These patterns could help us detect problems earlier. Our next step is to test this idea with real data.
- **T 時態**：現在式／條件句／情態動詞
- **L 邏輯**：假設→條件→可能效益→驗證
- **E 表達**：we believe that；may be able to

### 093｜說明研究方法（Explaining a Research Method）

- **origin_id**：093
- **English（4句）**：First, we collect electricity data from different machines. Next, we prepare the data and remove obvious errors. Then we train a model to recognize operating patterns. Finally, we evaluate how well the model works on unseen data.
- **T 時態**：現在式
- **L 邏輯**：資料→前處理→訓練→驗證
- **E 表達**：first；next；then；finally

### 094｜解釋意外的結果（Explaining an Unexpected Result）

- **origin_id**：094
- **English（4句）**：We expected the new model to perform better. However, the results were not as good as we hoped. After checking the data, we found differences between the training and testing conditions. This suggests that the model may need to be more reliable across environments.
- **T 時態**：過去式／情態動詞
- **L 邏輯**：預期→反差→發現→推論
- **E 表達**：not as good as；this suggests that

### 095｜研究限制（Discussing Research Limitations）

- **origin_id**：095
- **English（4句）**：Our results are promising, but the study has some limitations. We tested the model on only a few datasets. Therefore, we cannot assume it will work equally well everywhere. More experiments are needed before we can make a stronger claim.
- **T 時態**：現在式／過去式／被動式
- **L 邏輯**：成果→限制→推論邊界→後續
- **E 表達**：limitations；therefore；cannot assume

### 096｜回答聽眾問題（Answering a Difficult Question）

- **origin_id**：096
- **English（4句）**：Thank you for the question. That's an important point, and we haven't fully explored it yet. Based on our current results, we believe the method has potential. However, we need more evidence before reaching a final conclusion.
- **T 時態**：現在完成式／現在式
- **L 邏輯**：感謝→承認未知→現有證據→限制
- **E 表達**：based on；before reaching

### 097｜商業協商（Negotiating a Deal）

- **origin_id**：097
- **English（4句）**：We understand that the price is an important concern. However, we also need to maintain the quality of our service. If you can commit to a longer contract, we may be able to offer a discount. Would that be an acceptable option for your team?
- **T 時態**：現在式／條件句
- **L 邏輯**：理解→限制→交換條件→確認
- **E 表達**：commit to；offer a discount

### 098｜回應反對意見（Responding to an Objection）

- **origin_id**：098
- **English（4句）**：I understand your concern about the cost. However, we should also consider the time saved by automation. A lower purchase price doesn't always mean a lower total cost. That's why I suggest comparing the overall value rather than the initial price alone.
- **T 時態**：現在式／情態動詞
- **L 邏輯**：理解反對→增加觀點→重新比較
- **E 表達**：consider；doesn't always mean；rather than

### 099｜情境推演（Planning for Different Scenarios）

- **origin_id**：099
- **English（4句）**：Let's consider three possible outcomes. If demand grows quickly, we'll need more resources. If growth is slower than expected, we can control costs and improve the product. By preparing for both situations, we can make better decisions.
- **T 時態**：第一類條件句
- **L 邏輯**：情境→應對→風險管理
- **E 表達**：possible outcomes；slower than expected

### 100｜總結與下一步（Summarizing and Moving Forward）

- **origin_id**：100
- **English（4句）**：Today, we've discussed the problem, our solution, and the early results. We still have challenges to solve, but we've made meaningful progress. Our next step is to test the system with more users. I believe that by learning from real experience, we can build something truly useful.
- **T 時態**：現在完成式／未來計畫
- **L 邏輯**：回顧→進展→下一步→願景
- **E 表達**：meaningful progress；our next step

## 版本與驗收
- 本版：v1.1 / 2026-11-06 / 原創教材；從第一版100段**只重新編排**，保留原句作為基準原文。
- 計數驗證：100 個不同 origin_id；100 個新排序位置；每階段 20、20、20、20、20 段；4 句/段；每段 T/L/E 三項均具備。
- 尚需：語言難度評審、自然口語審稿、前置句型關係圖、聽力語音、提示版與不提示評量題、機器可讀教材檔及學習紀錄整合。教材初稿不等於已經部署 OLMCP。
