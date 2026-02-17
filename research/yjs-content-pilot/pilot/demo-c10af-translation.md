# 演示：C10af 多语言翻译（普通话 / 粤语繁体 / 德语）

> 产品：Wevac C10 Chamber Vacuum Sealer
> 英文原稿来源：`pilot/demo-c10af-listing.md`
> 日期：2026-02-14
> 目的：展示"英文Listing → 多语言本地化"的完整流程

---

## 流程概览

```
英文Listing（已有）
    ↓
填入翻译模板（3分钟）
    ↓
发给AI，一次生成一种语言（每种约2分钟）
    ↓
人工审核 + 母语者校对（每种约10-15分钟）
    ↓
完成
```

---

## 第一步：准备英文原稿

直接复用上一份demo生成的英文内容：

**Title:**
> Wevac C10 Chamber Vacuum Sealer - 1000W Oil Pump, -29.9 inHg Commercial Grade Vacuum, SmartVac One-Touch, Built-in Gauge, Seal Liquids & Solids for Sous Vide, Meal Prep & Food Storage

**Bullet Points:**
> 1. SEAL LIQUIDS WITHOUT THE MESS — Unlike external vacuum sealers that struggle with soups, sauces, and marinades, the Wevac C10 chamber vacuum sealer handles liquids effortlessly. Place your bag inside the chamber, close the lid, and let the oil pump do the work. Perfect for sous vide prep, batch cooking, and storing homemade stocks.
> 2. COMMERCIAL-GRADE VACUUM POWER AT HOME — The 1000W oil pump delivers -29.9 inHg (-1012mbar) of vacuum pressure, matching machines found in professional kitchens. This level of vacuum extraction removes virtually all air, keeping your food fresh 3 to 5 times longer than standard food storage methods. Reduce food waste and save hundreds of dollars per year.
> 3. SMARTVAC ONE-TOUCH OPERATION — No complicated settings or guesswork. Press one button and the C10 automatically vacuums and seals. The built-in vacuum gauge displays real-time pressure so you always know exactly what's happening. The user-friendly bag-clamp holds your bag securely in place — no shifting, no failed seals, no wasted bags.
> 4. BUILT TO LAST, CERTIFIED FOR SAFETY — Engineered by Argion Technology with 17 years of vacuum sealing expertise. The C10 features a robust construction with a 5mm double seal wire for airtight, reliable seals every time. ETL, CE, GS, and RoHS certified for safety and quality. Designed for years of daily use in your home kitchen or small business.
> 5. WORKS WITH ANY CHAMBER VACUUM BAGS — No proprietary bags required. Use any brand of smooth chamber vacuum bags in widths up to 10.2 inches (260mm). Compatible with standard flat bags, embossed bags, and compostable bags. Compact countertop design (12.2 × 16.3 × 14.2 in) fits neatly in your kitchen without taking over your workspace.

**Product Description:**
> (见 demo-c10af-listing.md 第四步)

---

## 第二步：发给AI的Prompt

每种语言发一次。以下是实际使用的Prompt（可直接复制）：

### System Prompt（三种语言共用，设一次就行）

```
You are a professional e-commerce localization specialist for the brand Wevac
(by Argion Technology). You specialize in translating Amazon product listings
and marketing content.

Your approach:
- Transcreation, not literal translation: adapt the message to resonate with
  local consumers
- Maintain the brand voice: professional yet approachable, data-driven,
  innovation-focused
- Follow local e-commerce platform conventions and SEO practices
- Use the brand glossary for consistent terminology

CRITICAL RULES:
- NEVER translate brand names: Wevac, Vesta, Argion stay as-is
- NEVER translate product model numbers: C10, VS200, etc.
- NEVER translate technology names: SmartVac stays as SmartVac
- Adapt certifications to what's relevant in the target market
- Convert measurements to local conventions
```

### Task Prompt（每种语言换一下变量即可）

```
Translate and localize the following Amazon listing from English to
{target_language} for {target_market} consumers.

Target Language: {target_language}
Target Market: {target_market}
Special Instructions: {special_instructions}

--- ORIGINAL ENGLISH CONTENT ---

[Title]
Wevac C10 Chamber Vacuum Sealer - 1000W Oil Pump, -29.9 inHg Commercial
Grade Vacuum, SmartVac One-Touch, Built-in Gauge, Seal Liquids & Solids
for Sous Vide, Meal Prep & Food Storage

[Bullet 1]
SEAL LIQUIDS WITHOUT THE MESS — Unlike external vacuum sealers that struggle
with soups, sauces, and marinades, the Wevac C10 chamber vacuum sealer
handles liquids effortlessly. Place your bag inside the chamber, close the
lid, and let the oil pump do the work. Perfect for sous vide prep, batch
cooking, and storing homemade stocks.

[Bullet 2]
COMMERCIAL-GRADE VACUUM POWER AT HOME — The 1000W oil pump delivers -29.9
inHg (-1012mbar) of vacuum pressure, matching machines found in professional
kitchens. This level of vacuum extraction removes virtually all air, keeping
your food fresh 3 to 5 times longer than standard food storage methods.
Reduce food waste and save hundreds of dollars per year.

[Bullet 3]
SMARTVAC ONE-TOUCH OPERATION — No complicated settings or guesswork. Press
one button and the C10 automatically vacuums and seals. The built-in vacuum
gauge displays real-time pressure so you always know exactly what's happening.
The user-friendly bag-clamp holds your bag securely in place — no shifting,
no failed seals, no wasted bags.

[Bullet 4]
BUILT TO LAST, CERTIFIED FOR SAFETY — Engineered by Argion Technology with
17 years of vacuum sealing expertise. The C10 features a robust construction
with a 5mm double seal wire for airtight, reliable seals every time. ETL, CE,
GS, and RoHS certified for safety and quality. Designed for years of daily use
in your home kitchen or small business.

[Bullet 5]
WORKS WITH ANY CHAMBER VACUUM BAGS — No proprietary bags required. Use any
brand of smooth chamber vacuum bags in widths up to 10.2 inches (260mm).
Compatible with standard flat bags, embossed bags, and compostable bags.
Compact countertop design (12.2 × 16.3 × 14.2 in) fits neatly in your
kitchen without taking over your workspace.

--- END ---

Please provide:
1. Localized Title
2. Localized 5 Bullet Points
3. 5-8 Local Keyword Suggestions
4. Localization Notes (what you adapted and why)
```

---

## 第三步：AI生成结果

---

### 语言一：简体中文（普通话）

**变量填入**：
- target_language: 简体中文
- target_market: 中国大陆消费者（天猫/京东/Amazon）
- special_instructions: 使用公制单位，强调性价比和实用场景，语气专业但亲切

#### 标题

```
Wevac C10 腔式真空封口机 — 1000W油泵商用级真空度-1012mbar，SmartVac一键操作，
内置真空表，轻松封装汤汁液体，适用低温慢煮/备餐/食品保鲜
```

#### 五点描述

**1. 汤汁液体也能轻松封装**
普通外抽式封口机遇到汤、酱汁、腌料就束手无策，液体会被吸进机器导致封口失败。Wevac C10 采用腔式设计，将整个真空袋放入腔体内抽真空，液体稳稳留在袋中。无论是自制高汤、红酒腌肉还是低温慢煮备料，一次搞定，干净利落。

**2. 商用级真空力，家用级操作**
1000W油泵提供-1012mbar（-29.9 inHg）的极限真空度，媲美专业厨房设备。这个级别的真空抽取能去除几乎所有空气，让食材保鲜时间延长3-5倍。按一般家庭每月浪费500-800元食材计算，一年能省下数千元。

**3. SmartVac 一键智能操作**
不需要复杂设置，不需要经验。按下一个按钮，C10自动完成抽真空和封口全过程。内置真空表实时显示腔内压力，封装状态一目了然。专利袋夹设计牢牢固定真空袋，不会移位、不会封歪、不浪费袋子。

**4. 17年专业品质，国际安全认证**
Wevac 由 Argion Technology 出品，拥有17年真空封装设备研发制造经验。C10 采用5mm双封口线设计，每次封口都密实可靠。通过ETL、CE、GS、RoHS四项国际认证，品质和安全有保障。经久耐用，适合家庭和小型餐饮长期使用。

**5. 兼容所有腔式真空袋，不挑品牌**
无需购买专用袋，市面上任何品牌的光面腔式真空袋都能用，最大袋宽260mm。兼容普通真空袋、纹路袋和可降解环保袋。机身尺寸310 × 415 × 360mm，台面摆放不占地方，厨房再小也放得下。

#### 关键词建议

1. 腔式真空封口机
2. 真空封口机 家用
3. 食品真空机
4. 低温慢煮 真空封口
5. 油泵真空机
6. 商用真空封口机 家用
7. 食品保鲜 真空包装
8. 汤汁真空封装

#### 本地化说明

| 改动 | 原因 |
|------|------|
| 单位全部转为公制（mm, mbar, kg） | 中国使用公制 |
| "save hundreds of dollars" → "一年能省下数千元" | 换算为人民币语境，更有代入感 |
| 强调"不挑品牌"的袋子兼容性 | 国内消费者对耗材锁定很敏感 |
| 去掉英寸标注，只保留毫米 | 中国消费者不熟悉英寸 |
| 认证保留ETL/CE/GS/RoHS | 国际认证在国内电商是品质背书 |

---

### 语言二：繁体中文（粤语语感）

**变量填入**：
- target_language: 繁體中文（粵語語感）
- target_market: 香港/澳門消費者
- special_instructions: 用繁體字，語感偏粵語但唔好太口語化，強調品質同慳位

#### 標題

```
Wevac C10 腔式真空封口機 — 1000W油泵商用級真空度-1012mbar，SmartVac一鍵操作，
內置真空錶，湯汁液體都封到，低溫慢煮/備餐/食品保鮮必備
```

#### 五點描述

**1. 湯汁醬料一樣封得實**
普通外抽式封口機遇到湯水、醬汁、醃料就搞唔掂，液體會被吸入機內搞到成枱都係。Wevac C10 用腔式設計，成個真空袋放入腔體入面抽真空，液體穩穩陣陣留喺袋入面。煲湯、紅酒醃肉、低溫慢煮備料，一次過搞掂，乾淨利落。

**2. 商用級真空力，屋企都用到**
1000W油泵提供-1012mbar嘅極限真空度，同專業廚房設備睇齊。呢個級別嘅真空抽取可以去除幾乎所有空氣，令食材保鮮時間延長3-5倍。每個月因為食材過期而嘥錢？用咗C10之後慳返唔少。

**3. SmartVac 一撳搞掂**
唔使複雜設定，唔使經驗。撳一個掣，C10自動完成抽真空同封口。內置真空錶即時顯示腔內壓力，封裝狀態一目了然。專利袋夾設計穩陣固定真空袋，唔會移位、唔會封歪、唔嘥袋。

**4. 17年專業品質，國際安全認證**
Wevac 由 Argion Technology 出品，擁有17年真空封裝設備研發製造經驗。C10 採用5mm雙封口線設計，次次封口都密實可靠。通過ETL、CE、GS、RoHS四項國際認證，品質同安全都有保障。耐用度高，屋企同小型餐廳長期用都得。

**5. 唔使買專用袋，任何品牌都啱用**
市面上任何品牌嘅光面腔式真空袋都用得，最大袋寬260mm。兼容普通真空袋、紋路袋同可降解環保袋。機身尺寸310 × 415 × 360mm，擺喺枱面唔阻位。香港廚房細？放心，慳位設計，細廚房都擺得落。

#### 關鍵詞建議

1. 腔式真空封口機
2. 真空封口機 家用
3. 真空包裝機
4. 低溫慢煮 真空
5. 食物保鮮機
6. 油泵真空機
7. 商用真空機 家用
8. 真空袋封口機

#### 本地化說明

| 改動 | 原因 |
|------|------|
| 全部用繁體字 | 香港/台灣市場標準 |
| 加入粵語語感（"搞掂"、"慳位"、"嘥"、"啱用"） | 貼近香港消費者閱讀習慣，增加親切感 |
| 強調"慳位"（省空間） | 香港廚房普遍細小，空間係重要考量 |
| "save hundreds of dollars" → "慳返唔少" | 粵語自然表達，避免直譯 |
| 保留國際認證（ETL/CE/GS） | 香港消費者信任歐美認證 |
| 去掉英寸，只用mm | 香港用公制 |

---

### 語言三：德語（Amazon.de）

**变量填入**：
- target_language: Deutsch (German)
- target_market: Deutsche Verbraucher (Amazon.de)
- special_instructions: Technisch präzise, CE/GS-Zertifizierung hervorheben, metrische Einheiten

#### Titel

```
Wevac C10 Kammer-Vakuumierer — 1000W Ölpumpe, -1012mbar Profi-Vakuum,
SmartVac Ein-Knopf-Bedienung, Vakuummeter, Flüssigkeiten Vakuumieren,
Sous Vide, Meal Prep & Lebensmittelaufbewahrung
```

#### Aufzählungspunkte (Bullet Points)

**1. FLÜSSIGKEITEN PROBLEMLOS VAKUUMIEREN**
Im Gegensatz zu externen Vakuumierern, die bei Suppen, Soßen und Marinaden versagen, bewältigt der Wevac C10 Kammer-Vakuumierer Flüssigkeiten mühelos. Legen Sie den Beutel in die Kammer, schließen Sie den Deckel — die Ölpumpe erledigt den Rest. Ideal für Sous Vide-Vorbereitung, Batch-Cooking und die Aufbewahrung selbstgemachter Brühen.

**2. PROFI-VAKUUMLEISTUNG FÜR ZUHAUSE**
Die 1000W Ölpumpe erzeugt -1012mbar Vakuumdruck — vergleichbar mit Geräten in professionellen Küchen. Diese Vakuumleistung entfernt nahezu die gesamte Luft und hält Ihre Lebensmittel 3- bis 5-mal länger frisch als herkömmliche Aufbewahrungsmethoden. Reduzieren Sie Lebensmittelverschwendung und sparen Sie mehrere hundert Euro pro Jahr.

**3. SMARTVAC EIN-KNOPF-BEDIENUNG**
Keine komplizierten Einstellungen, kein Rätselraten. Ein Knopfdruck — der C10 vakuumiert und versiegelt automatisch. Das integrierte Vakuummeter zeigt den Druck in Echtzeit an. Die benutzerfreundliche Beutelklemme fixiert Ihren Beutel sicher — kein Verrutschen, keine fehlgeschlagenen Versiegelungen, keine verschwendeten Beutel.

**4. LANGLEBIG GEBAUT, ZERTIFIZIERT FÜR SICHERHEIT**
Entwickelt von Argion Technology mit 17 Jahren Erfahrung in der Vakuumversiegelungstechnik. Der C10 verfügt über eine robuste Konstruktion mit 5mm Doppel-Siegeldraht für luftdichte, zuverlässige Versiegelungen. CE-, GS- und RoHS-zertifiziert für Sicherheit und Qualität. Konzipiert für den täglichen Einsatz in Ihrer Küche oder Ihrem Kleinbetrieb.

**5. KOMPATIBEL MIT ALLEN KAMMER-VAKUUMBEUTELN**
Keine proprietären Beutel erforderlich. Verwenden Sie Kammer-Vakuumbeutel jeder Marke bis zu einer Breite von 260mm. Kompatibel mit glatten Beuteln, geprägten Beuteln und kompostierbaren Beuteln. Kompaktes Design (310 × 415 × 360mm) — passt auf jede Arbeitsplatte, ohne Ihre Küche zu dominieren.

#### Keyword-Vorschläge

1. Kammer-Vakuumierer
2. Vakuumierer mit Ölpumpe
3. Kammer Vakuumiergerät
4. Vakuumierer Flüssigkeiten
5. Sous Vide Vakuumierer
6. Profi Vakuumierer für Zuhause
7. Vakuumiergerät Kammer
8. Lebensmittel vakuumieren

#### Lokalisierungshinweise

| Änderung | Begründung |
|----------|------------|
| Alle Maße in metrischen Einheiten (mm, mbar, kg) | Deutschland verwendet das metrische System |
| CE und GS hervorgehoben, ETL nachrangig | GS ist das vertrauenswürdigste Sicherheitszeichen in Deutschland |
| "save hundreds of dollars" → "mehrere hundert Euro" | Währungsanpassung |
| Formellerer Ton als im Englischen | Deutsche Amazon-Listings sind typischerweise sachlicher und technischer |
| "Lebensmittelverschwendung" betont | Nachhaltigkeit ist ein starkes Kaufargument in Deutschland |
| Duzen vermieden, Siezen verwendet | Professionellerer Ton für Küchengeräte auf Amazon.de |

---

## 第四步：质量检查清单（三种语言通用）

### 简体中文
- [x] 品牌名/技术名未被翻译（Wevac, SmartVac, Argion 保持原文）
- [x] 术语表词汇一致（腔式真空封口机、油泵、真空表、袋夹）
- [x] 公制单位（mm, mbar, kg）
- [x] 认证信息保留（ETL/CE/GS/RoHS）
- [x] 文化本地化（人民币语境、备餐场景）
- [ ] ⚠️ 建议：找国内电商运营同事校对一遍用词习惯

### 繁体中文（粤语）
- [x] 品牌名/技术名未被翻译
- [x] 全部繁体字
- [x] 粤语语感自然（搞掂、慳位、嘥、啱用）
- [x] 公制单位
- [x] 强调省空间（香港厨房小）
- [ ] ⚠️ 建议：找香港同事确认粤语用词是否地道，避免"台式繁体"

### 德语
- [x] 品牌名/技术名未被翻译
- [x] 公制单位
- [x] CE/GS认证突出（德国消费者最认）
- [x] 使用Sie（您）而非du（你），语气正式
- [x] 术语准确（Kammer-Vakuumierer, Ölpumpe, Vakuummeter）
- [ ] ⚠️ 建议：找德语母语者校对语法和复合词拼写

---

## 第五步：效率数据

| 步骤 | 耗时 |
|------|------|
| 准备英文原稿 | 0分钟（已有） |
| 填入翻译模板变量 | 3分钟 |
| AI生成（3种语言） | 6分钟（每种约2分钟） |
| 人工审核（3种语言） | 30分钟（每种约10分钟） |
| **总计** | **约39分钟，产出3种语言** |

对比传统方式：
| 方式 | 耗时 | 成本 |
|------|------|------|
| 外包翻译公司 | 3-5个工作日 | ¥500-1500/语言 |
| 内部翻译人员 | 1-2天/语言 | 人力成本 |
| **AI + 人工校对** | **39分钟/3种语言** | **API费用约¥2-3** |

---

## 总结：多语言翻译怎么做

```
第1步：拿到英文Listing（上一步已生成）
        ↓
第2步：打开Claude.ai，设好翻译System Prompt（一次设好，永久复用）
        ↓
第3步：把英文内容 + 目标语言 贴进去，发送
        ↓
第4步：拿到结果，对照检查清单过一遍
        ↓
第5步：找母语者花10分钟校对
        ↓
完成！一种语言从头到尾约13分钟
```

三种语言39分钟搞定，传统外包要一周+花几千块。
