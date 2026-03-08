# IMT050 模板审计报告：Word源文件 vs V23规范 vs 当前模板

**日期**：2026-03-08  
**审计对象**：`swiss/template/imt050-master-cn.html`（CN代表，其他语言同步）  
**参考基准**：
- Word源文件：`source/extracted_imt050.txt`（从 `_inbox/IMT050 说明书-通用-中文-A版-20260205.docx` 提取）
- V23模板：`swiss/template/v23-master-cn.html`（已投产的标准模板）
- 设计标准：`swiss/DESIGN-STANDARD.md` v1.1

---

## 一、审计发现汇总

| 编号 | 严重等级 | 类别 | 问题 |
|------|---------|------|------|
| A01 | ✅ RESOLVED | 内容缺失 | 保修卡字段已修复（9个字段完整） |
| A02 | ✅ RESOLVED | 内容缺失 | 安全须知已扩展至2页（24 WARNING + 7 CAUTION + 2 NOTICE = 33条） |
| A03 | 🟡 WARN | 术语不统一 | 章节标题与V23不统一（"保修条款" vs "品牌与保修信息"） |
| A04 | 🟡 WARN | 结构偏差 | 缺少"保修信息"独立小标题（V23有） |
| A05 | 🟡 WARN | 结构偏差 | 缺少保修邮箱单独段落（V23有） |
| A06 | 🟡 WARN | 结构偏差 | section-title 用 `<div>` 而V23用 `<h2>` + `chapter-num` |
| A07 | 🟡 WARN | 内容偏差 | 保修条件描述与源文件/V23不一致 |
| A08 | 🟡 WARN | 内容缺失 | 缺少"安装运输及搬运、存储、拆除"完整章节 |
| A09 | ℹ️ INFO | 内容简化 | 清洁章节简化了源文件详细步骤（合理简化） |
| A10 | ℹ️ INFO | 内容简化 | 故障排除合并了部分相近条目（合理简化） |
| A11 | 🟡 WARN | 内容缺失 | 源文件"提示 NOTICE"有2条（噪音/气候类型），模板安全页缺失 |
| A12 | 🟡 WARN | 结构偏差 | V23 TOC有章节编号 `<span class="toc-chapter">10</span>`，IMT050没有 |

---

## 二、逐项详细分析

### A01 ✅ 保修卡字段缺失 → 已修复

**修复方案**：保修卡已恢复为完整9个字段（4种语言模板均已更新）：
1. 客户名称 / Customer Name / Kundenname / Nome del cliente
2. 地址 / Address / Adresse / Indirizzo
3. 城市/州/邮政编码 / City/State/Zip / Stadt/Bundesland/PLZ / Città/Stato/CAP
4. 电话号码 / Phone Number / Telefonnummer / Numero di telefono
5. 电子邮件地址 / Email Address / E-Mail-Adresse / Indirizzo e-mail
6. 原始购买日期 / Original Purchase Date / Kaufdatum / Data di acquisto
7. 产品型号 / Product Model / Produktmodell / Modello del prodotto
8. 序列号 / Serial Number / Seriennummer / Numero di serie
9. 商户名称 / Merchant Name / Händlername / Nome del rivenditore

使用 compact-warranty CSS 类确保9字段在A5空间内排版良好。

---

### A02 ✅ 安全须知条目缺失 → 已修复

**修复方案**：安全须知扩展至2页（Page 3–4），完整收录源文件所有条目。

**修复后状态**（4种语言模板均已更新）：
- WARNING：24条（含制冷剂、通风、接地、灭火器等全部专业条目）
- CAUTION：7条（完整）
- NOTICE：2条（噪音等级 + 气候类型）
- 合计：33条，与源Word文件完全一致
- 使用 compact-safety CSS 类确保内容在A5双页内排版良好

---

### A03 🟡 章节标题术语不统一

| 章节 | 源文件 | V23模板 | IMT050模板 | 需统一 |
|------|--------|---------|-----------|--------|
| 安全 | `重要安全须知` | `安全须知` | `安全须知` | ⚠️ V23/IMT050一致，但与源文件不同 |
| 保修 | `保修信息` + `保修卡` | `品牌与保修信息` | `保修条款` | ✅ 应统一为V23的"品牌与保修信息" |
| 清洁 | `如何清洁` | — | `清洁保养` | ℹ️ 简化合理 |
| 操作 | `产品操作指引` | — | `操作指引` | ℹ️ 简化合理 |

---

### A04-A05 🟡 保修页结构偏差

**V23保修页结构**：
1. 联系方式段落
2. 品牌商信息表
3. 授权制造商表
4. **保修信息**（独立sub-title）
5. 保修条件列表
6. **保修邮箱**（独立段落："向我们发送电子邮件申请保修服务：{{email}}"）
7. 保修卡装饰图（image31.png）
8. **保修卡**（独立sub-title）
9. 9字段表格

**IMT050保修页结构**（当前）：
1. 联系方式段落 ✅
2. 品牌商信息表 ✅
3. 授权制造商表 ✅
4. ~~保修信息~~ — 缺少小标题
5. 保修条件列表 （内容不同）
6. ~~保修邮箱~~ — 缺少
7. ~~保修卡装饰图~~ — 缺少
8. 保修卡 ✅ 有小标题
9. 3字段表格 （缺少6个字段）

---

### A06 🟡 section-title标签差异

**V23**：`<h2 class="section-title"><span class="chapter-num">10</span>品牌与保修信息</h2>`
**IMT050**：`<div class="section-title">保修条款</div>`

V23使用语义化`<h2>`标签 + 红色章节编号span，IMT050使用普通`<div>`且无编号。

**建议**：暂不改（A5空间限制，chapter-num占空间），但记录为标准化差异。

---

### A07 🟡 保修条件内容不一致

**源文件/V23**：
1. 在过去X年内购买过产品
2. 有原始订单号或购买时使用的电子邮件
3. 如通过经销商购买，须提供原始收据的副本

**IMT050当前**：
1. 在过去X年内购买过产品 ✅
2. 提供有效的购买凭证（发票或收据）❌ 与源文件不同
3. 产品损坏非人为因素导致 ❌ 源文件无此条

**建议**：按源文件/V23统一。

---

### A08 🟡 缺少"安装运输及搬运、存储、拆除"章节

源文件有完整的"安装运输及搬运、存储、拆除"章节（含包装运输、安装、储存、拆除4节），IMT050模板将部分内容分散到"使用前准备"和"清洁保养"中，但以下内容完全缺失：

- 拆除章节（冷媒废料处理、电子废物处理、R600a处理要求）
- WEEE合规标志说明
- 运输后需静置4小时的说明

**建议**：在安全页或before_use页增加运输/废弃处理说明，或单独增设页面。

---

### A11 🟡 安全页缺少NOTICE框

源文件有2条NOTICE：
1. 产品噪音等级低于50 dB(A)
2. 气候类型SN，适合10℃~32℃

V23模板有NOTICE框，IMT050没有。

**建议**：在安全页添加note-box的NOTICE框，收录这2条。

---

## 三、修复优先级与方案

### 立即修复（ERROR）

1. **A01 保修卡字段**：恢复为9个字段，4语言同步
2. **A02 安全须知**：评估是否扩展至2页或标注参考

### 下一步修复（WARN）

3. **A03 章节标题**：WARRANTY页标题改为"品牌与保修信息"（4语言）
4. **A04-A05 保修页结构**：添加"保修信息"小标题、保修邮箱段落
5. **A07 保修条件**：按源文件统一
6. **A11 NOTICE框**：安全页添加note-box
7. **A06/A12 章节编号**：评估是否引入chapter-num系统

### 长期标准化

8. **A08 安装/废弃章节**：下一产品模板考虑加入
9. **建立跨产品术语表**：确保V23和IMT050使用相同术语

---

## 四、标准化建议：统一术语对照表

| 中文标准术语 | 英文 | 德文 | 意大利文 | 来源 |
|-------------|------|------|---------|------|
| 安全须知 | Safety Instructions | Sicherheitshinweise | Istruzioni di sicurezza | V23 |
| 警告 | WARNING | WARNUNG | AVVERTENZA | V23 |
| 注意 | CAUTION | VORSICHT | ATTENZIONE | V23 |
| 提示 | NOTICE | HINWEIS | AVVISO | V23 |
| 品牌与保修信息 | Brand & Warranty | Marken- und Garantieinformationen | Informazioni su marchio e garanzia | V23 |
| 品牌商信息 | Brand Information | Markeninformation | Informazioni sul marchio | V23 |
| 授权制造商 | Authorized Manufacturer | Autorisierter Hersteller | Produttore autorizzato | V23 |
| 保修信息 | Warranty Information | Garantieinformationen | Informazioni sulla garanzia | V23 |
| 保修卡 | Warranty Card | Garantiekarte | Scheda di garanzia | V23 |
| 免责声明 | DISCLAIMER | HAFTUNGSAUSSCHLUSS | ESCLUSIONE DI RESPONSABILITÀ | IMT050 |
| 使用前准备 | Before Use | Vor der Inbetriebnahme | Prima dell'uso | IMT050 |
| 产品结构 | Product Structure | Produktaufbau | Struttura del prodotto | IMT050 |
| 控制面板 | Control Panel | Bedienfeld | Pannello di controllo | IMT050 |
| 产品参数 | Specifications | Technische Daten | Specifiche tecniche | IMT050 |
| 操作指引 | Operation Guide | Bedienungsanleitung | Guida operativa | IMT050 |
| 清洁保养 | Cleaning & Maintenance | Reinigung & Wartung | Pulizia e manutenzione | IMT050 |
| 故障排除 | Troubleshooting | Fehlerbehebung | Risoluzione dei problemi | IMT050 |

### 保修卡字段术语对照

| 中文 | 英文 | 德文 | 意大利文 |
|------|------|------|---------|
| 客户名称 | Customer Name | Kundenname | Nome del cliente |
| 地址 | Address | Adresse | Indirizzo |
| 城市/州/邮政编码 | City / State / ZIP | Stadt / Bundesland / PLZ | Città / Provincia / CAP |
| 电话号码 | Phone Number | Telefonnummer | Numero di telefono |
| 电子邮件地址 | Email Address | E-Mail-Adresse | Indirizzo email |
| 原始购买日期 | Original Purchase Date | Ursprüngliches Kaufdatum | Data di acquisto originale |
| 产品型号 | Product Model | Produktmodell | Modello del prodotto |
| 序列号（如适用） | Serial Number (if applicable) | Seriennummer (falls zutreffend) | Numero di serie (se applicabile) |
| 商户名称 | Retailer Name | Händlername | Nome del rivenditore |

---

## 五、结论

IMT050模板的**CSS设计语言**已与V23对齐（v1.1标准），但**内容层面**存在显著偏差：

1. **保修卡缺6个字段**（最严重，直接影响合规性）
2. **安全须知缺14条**（安全相关，需评估法规风险）
3. **术语不统一**（影响品牌一致性）
4. **结构偏差**（影响跨产品可维护性）

建议优先修复A01（保修卡）和A03-A07（保修页结构），然后建立统一术语表防止后续产品再出现偏差。
