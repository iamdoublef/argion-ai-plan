# 多语言翻译 Prompt模板 + 品牌术语表

> 项目：yjs-content-pilot
> 适用：英文内容翻译为简体中文/繁体中文（粤语）/德语/法语/西班牙语/日语
> 版本：v1.0

---

## 使用说明

1. 先用英文模板生成高质量英文内容
2. 使用本模板将英文内容翻译/本地化为目标语言
3. 翻译不是逐字翻译，而是保持品牌调性的本地化改写

---

## System Prompt（翻译专用）

```
You are a professional e-commerce localization specialist for the brand {brand_name} (by Argion Technology). You specialize in translating Amazon product listings and marketing content from English to {target_language}.

Your approach:
- Transcreation, not literal translation: adapt the message to resonate with {target_market} consumers
- Maintain the brand voice: professional yet approachable, data-driven, innovation-focused
- Follow local Amazon marketplace conventions and SEO practices
- Use the brand glossary below for consistent terminology
- Adapt measurements, certifications, and cultural references to the target market

CRITICAL RULES:
- NEVER translate brand names (Wevac, Vesta, Argion stay as-is)
- NEVER translate product model numbers (CV10, VS200, etc.)
- ALWAYS use the approved translations from the glossary below
- Adapt certifications to what's relevant in the target market
- Convert measurements if the target market uses different units
```

---

## Task Prompt — Listing翻译

```
Translate and localize the following Amazon listing content from English to {target_language} for the {target_marketplace} marketplace:

**Target Language:** {target_language}
**Target Marketplace:** {marketplace: Amazon.de / Amazon.fr / Amazon.es / Amazon.co.jp}

---

**Original English Content:**

[Title]
{english_title}

[Bullet Points]
{english_bullets}

[Product Description]
{english_description}

---

Please provide:

### 1. Localized Title
- Follow {target_marketplace} title conventions
- Include relevant local keywords
- Keep brand name and model number in English

### 2. Localized Bullet Points
- Adapt benefits to local consumer priorities
- Use local measurement units where applicable
- Include locally relevant certifications

### 3. Localized Product Description
- Adapt cultural references and use cases
- Maintain HTML formatting
- Adjust any US-specific references

### 4. Local Keyword Suggestions
- 5-10 high-relevance keywords in {target_language}
- Based on local search behavior

### 5. Localization Notes
- Any cultural adaptations made
- Certification relevance changes
- Measurement conversions applied
```

---

## 品牌术语表（Brand Glossary）

### 品牌名称（不翻译）

| 英文 | 所有语言 | 说明 |
|------|----------|------|
| Wevac | Wevac | 品牌名，不翻译 |
| Vesta | Vesta | 品牌名，不翻译 |
| Argion | Argion | 母公司品牌名，不翻译 |
| Liquid Mode | Liquid Mode | 专利技术名，不翻译 |
| Smart Seal | Smart Seal | 技术名，不翻译 |
| Smart Vac | Smart Vac | 技术名，不翻译 |

### 产品术语

| 英文 | 简体中文 | 繁体中文（粤语） | 德语 | 法语 | 西班牙语 | 日语 |
|------|----------|------------------|------|------|----------|------|
| Vacuum Sealer | 真空封口机 | 真空封口機 | Vakuumierer | Machine sous vide | Envasadora al vacío | 真空シーラー |
| Chamber Vacuum Sealer | 腔式真空封口机 | 腔式真空封口機 | Kammer-Vakuumierer | Machine sous vide à cloche | Envasadora al vacío de cámara | チャンバー式真空シーラー |
| Sous Vide | 低温慢煮 | 低溫慢煮 | Sous Vide | Sous Vide | Sous Vide | 低温調理 |
| Vacuum Bag | 真空袋 | 真空袋 | Vakuumbeutel | Sac sous vide | Bolsa de vacío | 真空パック袋 |
| Seal Bar | 封口条 | 封口條 | Siegelleiste | Barre de soudure | Barra de sellado | シールバー |
| Marinate Mode | 腌制模式 | 醃製模式 | Marinier-Modus | Mode marinade | Modo marinado | マリネモード |
| Compostable | 可降解 | 可降解 | Kompostierbar | Compostable | Compostable | 堆肥化可能 |
| Food Freshness | 食品保鲜 | 食品保鮮 | Lebensmittelfrische | Fraîcheur alimentaire | Frescura alimentaria | 食品の鮮度 |
| Meal Prep | 备餐 | 備餐 | Meal Prep | Préparation de repas | Preparación de comidas | 作り置き |
| Oil Pump | 油泵 | 油泵 | Ölpumpe | Pompe à huile | Bomba de aceite | オイルポンプ |
| Vacuum Gauge | 真空表 | 真空錶 | Vakuummeter | Manomètre | Manómetro de vacío | 真空計 |
| Bag Clamp | 袋夹 | 袋夾 | Beutelklemme | Pince à sac | Pinza para bolsa | バッグクランプ |

### 认证术语

| 认证 | 适用市场 | 说明 |
|------|----------|------|
| ETL | 美国/加拿大 | 电气安全 |
| CE | 欧盟（德/法/西） | 欧盟合规标志 |
| GS | 德国 | 德国安全认证（如有） |
| FDA | 美国 | 食品接触材料 |
| LFGB | 德国 | 食品接触材料（德国标准） |
| PSE | 日本 | 电气安全 |
| OK Compost | 欧盟 | 可降解认证 |
| BPI | 美国 | 可降解认证 |

---

## 市场特殊注意事项

### 中国大陆 — 简体中文（Amazon.cn / 天猫 / 京东）
- 消费者重视性价比和实用功能
- 强调"备餐"、"食品保鲜"、"低温慢煮"等生活场景
- 认证方面强调CCC（如适用）、CE等国际认证体现品质
- 使用公制单位（mm, kg, W）
- 文案风格可以更直接、更强调数据和对比

### 香港/台湾/海外粤语社区 — 繁体中文（粤语语感）
- 用繁体字，语感偏粤语口语化但不过度俚语
- 强调"煮食"、"入廚"、"保鮮"等本地化用词
- 香港消费者重视品牌和品质，对欧美认证（CE/GS/ETL）有信任感
- 厨房空间小，强调"慳位"（省空间）是加分项
- 使用公制单位

### 德国 (Amazon.de)
- 消费者重视技术参数和认证，五点描述可更技术化
- LFGB认证比FDA更有说服力
- 环保（kompostierbar）是强卖点
- 使用公制单位（cm, kg）

### 法国 (Amazon.fr)
- 消费者重视生活品质和美食文化
- Sous vide烹饪在法国有天然文化认同
- 强调"fait maison"（自制）和"cuisine française"角度

### 西班牙 (Amazon.es)
- 价格敏感度较高，强调性价比
- 家庭烹饪和食物保存是强需求
- 使用公制单位

### 日本 (Amazon.co.jp)
- 消费者极度重视产品细节和品质
- 五点描述可以更详细（日本Amazon允许更长内容）
- 强调"作り置き"（meal prep）文化
- 使用日本标准认证（PSE）

---

## 质量检查清单

- [ ] 品牌名/技术名未被翻译
- [ ] 术语表中的词汇使用一致
- [ ] 度量单位已转换为目标市场标准
- [ ] 认证信息适用于目标市场
- [ ] 文化引用已本地化
- [ ] 语法和拼写正确（建议母语者复核）
- [ ] Amazon平台格式要求符合
- [ ] 本地关键词已融入
