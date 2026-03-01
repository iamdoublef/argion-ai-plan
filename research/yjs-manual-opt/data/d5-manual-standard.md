# 亚俊氏产品说明书编写规范

**版本**：v2.0
**日期**：2026-02-26
**参考标准**：小米（Xiaomi）国际版说明书规范（Smart Air Purifier Elite，ManualsLib #3185804）

> 本文件是说明书编写和审计的**唯一事实来源**。manual-writer 和 manual-auditor agent 均引用本文件，不重复定义规范细节。

---

## 一、整体原则

参照小米说明书的核心逻辑：**安全优先、结构线性、图文配合、语言简洁**。

每份说明书必须能回答用户三个问题：
1. 这个产品是什么、有哪些部件？
2. 怎么用？
3. 出问题了怎么办？

---

## 二、章节结构规范

### 标准章节顺序（所有产品统一）

| 序号 | 章节名称 | 说明 |
|------|---------|------|
| 1 | 安全须知 | 必须是第一章，独立成页 |
| 2 | 产品概览 | 产品外观图 + 零件标注 |
| 3 | 技术参数 | 规格表，按目标市场出对应版本 |
| 4 | 安装说明 | 开箱、安装、首次使用前准备 |
| 5 | 操作指引 | 按功能模块分节，每节配图 |
| 6 | 故障排除 | 问题 → 原因 → 解决方法，三列格式 |
| 7 | 维护保养 | 清洁频率、方法、注意事项 |
| 8 | 品牌与保修信息 | 制造商、品牌商、客服、保修条款 |

可选章节（根据产品特性添加，插入在第7章之后、第8章之前）：
- 产品功能 / Control Panel Functions
- 真空包装特性 / Vacuum Packaging Guide

### 章节标题命名规范（固定，不得随意修改）

| 中文标题 | 英文标题 |
|---------|---------|
| 安全须知 | Safety Instructions |
| 产品概览 | Product Overview |
| 技术参数 | Specifications |
| 安装说明 | Installation |
| 操作指引 | How to Use |
| 故障排除 | Troubleshooting |
| 维护保养 | Maintenance |
| 品牌与保修信息 | Brand & Warranty |

---

## 三、安全警示规范

### 三级体系（所有产品统一）

参照小米规范，统一使用以下三级，**不得混用、不得减少、不得自创**：

| 等级 | 标识 | 含义 | 使用场景 |
|------|------|------|---------|
| ⚠️ WARNING | 警告 | 可能导致人身伤害或死亡 | 触电、烫伤、火灾风险 |
| ⚠️ CAUTION | 注意 | 可能导致产品损坏或轻微伤害 | 操作不当、存储不当 |
| ℹ️ NOTICE | 提示 | 重要使用信息，不涉及安全 | 噪音等级、适用温度范围、食品储存提醒 |

**禁止使用非标准警示框**：不得使用"重要提示""IMPORTANT""注意事项"等自创标题的警示框。所有需要突出显示的提醒信息必须归入上述三级之一（通常归入 NOTICE）。

### 写作格式

每条警示独立成行，用 `·` 项目符号，**不合并两条内容为一句**：

```
✅ 正确：
· 请勿在高湿高温等环境中使用本机。
· 严禁在有易燃易爆气体的环境中使用。

❌ 错误：
· 请勿在高湿高温等环境中使用本机严禁在有易燃易爆气体的环境中使用。。
```

---

## 四、内容写作规范

### 操作步骤

- 用数字编号（1、2、3），每步一个动作
- 动词开头，祈使句：「按下按键」「将袋口放入」「关闭面盖」
- 每步配对应图示，图在上/左，文字在下/右
- 步骤中的按键名称用引号标注：点击「Seal」按键

### Note / 提示框

格式固定，不得随意变体：

```
Note：[内容]
```

- 每个 Note 只出现一次，不重复
- 放在相关步骤正下方
- 不用于安全警告（安全内容用 WARNING/CAUTION）

### 数值格式

| 类型 | 格式 | 示例 |
|------|------|------|
| 电压范围 | 用 `~` 连接 | 100~240 V |
| 尺寸 | 用 `×` 不用 `x` | 380×205×155 mm |
| 噪音 | 带单位括号 | ≤ 68 dB(A) |
| 温度 | 中文版用 `℃`，英文版同时标 `℉` | 10℃~32℃ / 50℉~89.6℉ |
| 间距要求 | 标注最小值 | ≥ 120 mm |
| 数值与单位 | 之间有空格 | 190 W、60 Hz |

### 禁止事项

- ❌ 禁止在正式文档中保留红色编辑注释
- ❌ 禁止在同一文档中保留多个品牌信息（交付前必须只保留对应品牌）
- ❌ 禁止客服邮箱等关键字段留空占位符
- ❌ 禁止同一条 Note 重复出现多次
- ❌ 禁止使用 emoji 图标（如 ⚠/⚡/📝）
- ❌ 禁止在 CN 版保留美标参数，EN 版保留欧标参数
- ❌ 禁止使用非标准警示框标题（如"重要提示""IMPORTANT"），必须归入三级体系
- ❌ 禁止在某个语言版本中遗漏制造商信息表格
- ❌ 禁止打印 CSS 使用 `height + overflow: hidden`（会截断大表格）

---

## 五、排版规范

### 页面设置

| 项目 | 规范值 |
|------|--------|
| 页面尺寸 | A4（210×297 mm） |
| 页边距 | 上下左右均为 12.7 mm（0.5"） |
| 页面方向 | 竖版 |

### 字体

| 用途 | 字体 | 字号 |
|------|------|------|
| 正文（中文） | HarmonyOS Sans SC | 14px |
| 正文（英文） | HarmonyOS Sans SC / Arial | 14px |
| 一级标题 | HarmonyOS Sans SC Bold | 18px |
| 二级标题 | HarmonyOS Sans SC Bold | 15px |
| 三级标题 | HarmonyOS Sans SC Bold | 14px |
| Note / 表格 | HarmonyOS Sans SC | 13px |
| 页脚 | HarmonyOS Sans SC | 11px |

### 颜色规范

| 用途 | 色值 |
|------|------|
| 主色（橙色） | #FF6900 |
| 正文 | #1A1A1A |
| 一级标题 | #1A1A1A |
| 次要文字/注释 | #666666 |
| WARNING 框背景 | #FFF3E0 |
| WARNING 框竖线 | #FF6900 |
| WARNING 标题色 | #E65100 |
| CAUTION 框背景 | #FFFDE7 |
| CAUTION 框竖线 | #FFC107 |
| CAUTION 标题色 | #F57F17 |
| NOTICE 框背景 | #F9F9F9 |
| NOTICE 框竖线 | #E5E5E5 |
| 表格表头背景 | #F2F2F2 |
| 表格边框 | #CCCCCC |
| 分隔线 | #E5E5E5 |
| 页码 | #999999 |

**禁止使用**：绿色（#00B050）表头、红色（#EE0000）正文文字

### 表格规范

- 所有表格统一使用同一样式
- 表头背景色：#F2F2F2，文字加粗
- 表格边框：1px solid #CCCCCC
- 技术参数如果只有两列（名称/值），可用无边框键值对格式

### 图片规范

| 项目 | 规范 |
|------|------|
| 格式优先级 | SVG > PNG（SVG 矢量清晰，PNG 仅作回退） |
| 图片锚定 | 统一使用嵌入式（inline），不用浮动 |
| 图片编号 | Figure 1（英文版）/ 图 1（中文版） |
| 零件标注 | 引线 + 编号，编号对应下方表格 |
| 警示图标 | 使用标准 ISO 7010 图标库 |

---

## 六、多版本管理规范

### 按市场出独立版本

| 版本 | 电压/频率 | 认证标志 | 语言 |
|------|---------|---------|------|
| 北美版（US） | 110~120V / 60Hz | UL/ETL | 英文 |
| 欧洲版（EU） | 220~240V / 50Hz | CE | 英文/多语言 |
| 澳洲版（AU） | 220~240V / 50Hz | SAA | 英文 |
| 中国版（CN） | 220V / 50Hz | CCC | 中文 |

### 品牌版本管理

同一产品的不同品牌版本通过 `product-config.json` 管理，**不在文档中保留多品牌信息**。

### 多语言一致性硬规则

- 品牌商和制造商信息必须在所有语言版本中同时出现
- EN 版制造商地址使用英文翻译，CN 版使用中文原文
- 不得在某个语言版本中遗漏制造商表格
- 数值、数量、按键名称在所有版本中必须完全一致
- 操作步骤数量和顺序在所有版本中必须一致

---

## 七、品牌与保修信息规范

末页固定包含（所有语言版本均不得遗漏）：
- 品牌商表格：名称、地址、网址、客服邮箱
- 制造商表格：公司名（中英双语）、地址、网址
- 保修信息：年限、条件
- 保修卡：必填字段表格

### 感谢语模板

CN：`感谢您购买 [品牌名] [产品名]。如有任何问题，请通过以下方式联系我们：[邮箱] | [网址]`

EN：`Thank you for choosing [Brand] [Product Name]. For support, contact us at: [email] | [website]`

### 保修卡必填字段

客户姓名、地址、城市/州/邮编、电话、邮箱、购买日期、产品型号、序列号、商户名称

---

## 八、已知陷阱（经验教训）

| # | 陷阱 | 后果 | 对策 |
|---|------|------|------|
| 1 | Word docx 中每张图存 SVG+PNG 两份，多个 Drawing 可能共用同一个 PNG 回退 | 提取图片时只取 PNG 会导致多张图完全相同 | 用 MD5 检测 PNG 重复，以 SVG 为准建立映射 |
| 2 | 原文中"重要提示""IMPORTANT"等非标准警示框 | 不属于三级体系，审计会报 ERROR | 编写时统一归入 NOTICE |
| 3 | EN 版遗漏制造商信息表格 | 多语言不一致，审计报 ERROR | 末页品牌商+制造商两个表格，所有版本都要有 |
| 4 | 打印 CSS 用 `height: 297mm; overflow: hidden` | 大表格（故障排除、食物保鲜表）内容被截断 | 必须用 `min-height: 297mm; overflow: visible` |
| 5 | 表头背景色/边框色与规范不一致 | 审计报 WARNING | 严格使用 #F2F2F2 / #CCCCCC |
| 6 | 原文双句号、两句合并为一条 | 安全警示不清晰 | 编写时拆分为独立条目 |
| 7 | 同一 Note 重复出现多次 | 冗余信息 | 每条 Note 只出现一次 |

---

## 九、HTML 模板库

### 页面容器

```html
<div class="page">...</div>           <!-- 普通页 -->
<div class="page page-cover">...</div> <!-- 封面页 -->
```

### 章节标题

```html
<h2 class="section-title"><span class="chapter-num">01</span>安全须知</h2>
<div class="sub-title">6.1 如何使用切袋刀</div>
```

### 安全警示三级体系

```html
<div class="warning-box">
  <div class="box-title">WARNING</div>
  <ul class="box-list"><li>...</li></ul>
</div>

<div class="caution-box">
  <div class="box-title">CAUTION</div>
  <ul class="box-list"><li>...</li></ul>
</div>

<div class="note-box">
  <div class="box-title">NOTICE</div>
  <ul class="box-list"><li>...</li></ul>
</div>
```

CN 版标题格式：`警告 WARNING` / `注意 CAUTION` / `提示 NOTICE`（无 emoji）。

### 操作步骤

```html
<ol class="steps">
  <li><span class="step-num">1</span>打开面盖。</li>
  <li><span class="step-num">2</span>打开切袋刀架。</li>
</ol>
```

步骤旁配图（flex 布局）：
```html
<div style="display:flex;gap:16px;align-items:flex-start">
  <div style="flex:1"><ol class="steps">...</ol></div>
  <div style="flex:0 0 auto">
    <img src="images_{型号}/xxx.svg" alt="..." style="max-height:45mm;max-width:45mm">
  </div>
</div>
```

### 图片

```html
<div class="fig-wrap">
  <img src="images_{型号}/{文件名}.svg" alt="描述">
  <div class="fig-caption">图 1 — 产品结构</div>
</div>
```

### 按键名称

```html
<span class="btn-name">Seal</span>
```

### 技术参数表

```html
<table>
  <thead><tr><th>参数</th><th>规格</th></tr></thead>
  <tbody>
    <tr><td class="spec-label">电压</td><td class="spec-value">220~240 Vac</td></tr>
  </tbody>
</table>
```

### 故障排除表

```html
<table>
  <thead><tr><th style="width:22%">故障现象</th><th style="width:40%">可能原因</th><th style="width:38%">解决方案</th></tr></thead>
  <tbody>
    <tr>
      <td rowspan="3"><b>不能开机</b></td>
      <td>电源线未正确插入</td>
      <td>确保电源线已正确插入。</td>
    </tr>
  </tbody>
</table>
```

### 品牌与保修（末页）

```html
<!-- CN 版 -->
<div class="sub-title">品牌商</div>
<table>
  <tbody>
    <tr><td class="spec-label" style="width:30%">品牌商</td><td class="spec-value">[品牌名]</td></tr>
    <tr><td class="spec-label">地址</td><td>[地址]</td></tr>
    <tr><td class="spec-label">网址</td><td>[网址]</td></tr>
    <tr><td class="spec-label">客服邮箱</td><td>[邮箱]</td></tr>
  </tbody>
</table>
<div class="sub-title">授权制造商</div>
<table>
  <tbody>
    <tr><td class="spec-label" style="width:30%">制造商</td><td class="spec-value">广州亚俊氏真空科技股份有限公司<br><span style="font-weight:400;font-size:12px;color:#666">Guangzhou Argion Electric Appliance Co., Ltd.</span></td></tr>
    <tr><td class="spec-label">地址</td><td>广东省广州市番禺区南村镇启业路1号</td></tr>
    <tr><td class="spec-label">网址</td><td>www.argiontechnology.com</td></tr>
  </tbody>
</table>

<!-- EN 版 -->
<div class="sub-title">Brand Information</div>
<table>
  <tbody>
    <tr><td class="spec-label" style="width:30%">Brand</td><td class="spec-value">[Brand Name]</td></tr>
    <tr><td class="spec-label">Address</td><td>[Address]</td></tr>
    <tr><td class="spec-label">Website</td><td>[Website]</td></tr>
    <tr><td class="spec-label">Customer Support</td><td>[Email]</td></tr>
  </tbody>
</table>
<div class="sub-title">Manufacturer</div>
<table>
  <tbody>
    <tr><td class="spec-label" style="width:30%">Manufacturer</td><td class="spec-value">Guangzhou Argion Electric Appliance Co., Ltd.<br><span style="font-weight:400;font-size:12px;color:#666">广州亚俊氏真空科技股份有限公司</span></td></tr>
    <tr><td class="spec-label">Address</td><td>No. 1, Qiye Road, Nancun Town, Panyu District, Guangzhou, Guangdong, China</td></tr>
    <tr><td class="spec-label">Website</td><td>www.argiontechnology.com</td></tr>
  </tbody>
</table>
```

### 页脚

```html
<div class="page-footer">
  <span>[品牌] [型号] 使用说明书</span>
  <span class="page-num">3</span>
</div>
```

---

## 十、CSS 设计系统

完整 CSS，直接内嵌在 HTML 的 `<style>` 标签中。所有色值、字号、间距以本文件第五章为准。

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #f0f0f0; font-family: "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif; }
.page { width: 210mm; min-height: 297mm; padding: 12.7mm; margin: 8mm auto; background: #fff; box-shadow: 0 2px 12px rgba(0,0,0,0.12); position: relative; page-break-after: always; font-size: 14px; line-height: 1.7; color: #1A1A1A; }

.page-cover { display: flex; flex-direction: column; justify-content: space-between; padding: 20mm 14mm 15mm; }
.cover-top { display: flex; justify-content: flex-start; align-items: center; }
.cover-brand { font-size: 13px; font-weight: 700; letter-spacing: 3px; color: #1A1A1A; text-transform: uppercase; }
.cover-brand span { display: inline-block; width: 28px; height: 4px; background: #FF6900; margin-right: 8px; vertical-align: middle; }
.cover-center { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 0 0 20mm; }
.cover-product-img { width: 100%; max-height: 80mm; object-fit: contain; margin-bottom: 16mm; }
.cover-model { font-size: 11px; font-weight: 600; letter-spacing: 4px; color: #FF6900; text-transform: uppercase; margin-bottom: 6px; }
.cover-title { font-size: 32px; font-weight: 700; color: #1A1A1A; line-height: 1.2; margin-bottom: 4px; }
.cover-subtitle { font-size: 16px; font-weight: 400; color: #666; }
.cover-divider { width: 40px; height: 3px; background: #FF6900; margin: 14px 0; }
.cover-bottom { border-top: 1px solid #E5E5E5; padding-top: 8px; font-size: 11px; color: #999; line-height: 1.6; }

.toc-title { font-size: 22px; font-weight: 700; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #FF6900; }
.toc-item { display: flex; justify-content: space-between; align-items: baseline; padding: 7px 0; border-bottom: 1px dotted #E5E5E5; font-size: 14px; }
.toc-item:last-child { border-bottom: none; }
.toc-chapter { color: #FF6900; font-weight: 700; margin-right: 8px; }
.toc-name { flex: 1; color: #1A1A1A; }
.toc-page { color: #999; font-size: 13px; min-width: 24px; text-align: right; }

.section-title { border-left: 4px solid #FF6900; padding-left: 12px; font-size: 18px; font-weight: 700; color: #1A1A1A; margin: 0 0 16px; line-height: 1.3; }
.section-title .chapter-num { color: #FF6900; margin-right: 6px; }
.sub-title { font-size: 15px; font-weight: 700; color: #1A1A1A; margin: 20px 0 10px; border-left: 3px solid #E5E5E5; padding-left: 10px; }

.warning-box { border-left: 4px solid #FF6900; background: #FFF3E0; padding: 12px 16px; margin: 14px 0; border-radius: 0 4px 4px 0; }
.warning-box .box-title { font-size: 13px; font-weight: 700; color: #E65100; margin-bottom: 8px; }
.caution-box { border-left: 4px solid #FFC107; background: #FFFDE7; padding: 12px 16px; margin: 14px 0; border-radius: 0 4px 4px 0; }
.caution-box .box-title { font-size: 13px; font-weight: 700; color: #F57F17; margin-bottom: 8px; }
.note-box { border-left: 4px solid #E5E5E5; background: #F9F9F9; padding: 10px 14px; margin: 12px 0; border-radius: 0 4px 4px 0; font-size: 13px; color: #555; }
.note-box .box-title { font-weight: 700; color: #444; margin-bottom: 4px; }
.box-list { list-style: none; padding: 0; }
.box-list li { padding: 2px 0 2px 16px; position: relative; font-size: 13px; line-height: 1.6; }
.box-list li::before { content: "·"; position: absolute; left: 4px; color: #FF6900; font-weight: 700; }

.steps { list-style: none; padding: 0; margin: 10px 0; }
.steps li { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; font-size: 14px; line-height: 1.6; }
.step-num { flex-shrink: 0; width: 24px; height: 24px; background: #FF6900; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; margin-top: 1px; }

.bullet-list { list-style: none; padding: 0; margin: 8px 0; }
.bullet-list li { padding: 3px 0 3px 18px; position: relative; font-size: 14px; line-height: 1.65; }
.bullet-list li::before { content: "·"; position: absolute; left: 4px; color: #FF6900; font-size: 18px; line-height: 1.3; }

.fig-wrap { text-align: center; margin: 14px 0; }
.fig-wrap img { max-width: 80%; max-height: 70mm; object-fit: contain; display: inline-block; }
.fig-caption { font-size: 12px; color: #888; margin-top: 5px; text-align: center; }

table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
th { background: #F2F2F2; font-weight: 700; padding: 8px 12px; text-align: left; border: 1px solid #CCCCCC; color: #333; }
td { padding: 7px 12px; border: 1px solid #CCCCCC; color: #1A1A1A; vertical-align: top; }
tr:nth-child(even) td { background: #FAFAFA; }
.spec-label { color: #666; font-size: 13px; }
.spec-value { font-weight: 600; }

.btn-name { display: inline-block; background: #F5F5F5; border: 1px solid #DDD; border-radius: 3px; padding: 1px 6px; font-size: 12px; font-family: monospace; color: #333; white-space: nowrap; }

.page-footer { position: absolute; bottom: 6mm; left: 12.7mm; right: 12.7mm; border-top: 1px solid #E5E5E5; padding-top: 6px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #BDBDBD; }
.page-num { font-size: 12px; color: #999; }

@media print {
  body { background: #fff; }
  .page { margin: 0; box-shadow: none; min-height: 297mm; overflow: visible; }
  table, .steps, .warning-box, .caution-box, .note-box { page-break-inside: avoid; }
  .section-title, .sub-title { page-break-after: avoid; }
}
```

---

## 十一、交付前检查清单

- [ ] 安全警示三级体系完整（WARNING / CAUTION / NOTICE），无自创警示框
- [ ] 无语法错误、错别字、双句号
- [ ] Note 无重复
- [ ] 按键名称与功能描述一致
- [ ] 红色编辑注释已全部删除
- [ ] 文档中只保留一个品牌的信息
- [ ] 客服邮箱已填写（非占位符）
- [ ] 技术参数与目标市场匹配（美标/欧标）
- [ ] 图片全部为嵌入式，优先 SVG
- [ ] 表格表头背景色 #F2F2F2，边框色 #CCCCCC
- [ ] 页边距上下左右均为 12.7 mm
- [ ] 章节标题符合命名规范
- [ ] 制造商信息在所有语言版本中均存在
- [ ] 品牌商信息在所有语言版本中完全一致
- [ ] 打印 CSS 使用 `min-height + overflow: visible`
- [ ] 大表格在合理位置允许分页
- [ ] 操作步骤数量和顺序在所有语言版本中一致
- [ ] 数值、按键名称在所有语言版本中完全一致
- [ ] 分页无孤立小节：`sub-title` 不得单独落在页底（其后正文少于 2 行视为不合格）
- [ ] 同一版本正文页页眉策略一致：要么统一有 running header，要么统一无；不得混用
- [ ] 同一章节同层级示意图图注策略一致：要么统一有图注，要么统一无图注
- [ ] 图内存在编号 callout（1..N）时，必须提供完整编号映射说明（表格或列表），不得缺号

---

## 十二、2026-03-01 导出链路与质量门禁补充

### 12.1 资源路径硬性规则
- 在 `experiments/2026-02-26_top-tier-styles/` 下的 HTML，图片相对路径必须使用：`../../output/images_v23/...`。
- 禁止使用 `../output/images_v23/...`（会被解析到 `experiments/output/...`，导致资源丢失）。
- 交付前必须逐条验证 `<img src>` 可解析到本地真实文件。

### 12.2 HTML 结构完整性规则
- 禁止出现损坏闭合标签，如 `?/li>`、`?/div>`、`?/h2>`、`?/td>`、`?/span>`。
- 所有页面容器必须是完整的 `<div class="page"> ... </div>` 结构。
- 页脚页码必须连续；当前 V23 完整版要求从 `2` 连续到 `18`。

### 12.3 文本编码规则
- HTML 与 Markdown 统一使用 UTF-8。
- 交付前需抽检关键术语，至少包括：`真空封口机`、`操作指引`、`故障排除`。
- 若出现乱码（如标题或章节名异常字符），必须先修复编码再导出 PDF。

### 12.4 导出前必做预检（Playwright）
- `page.goto(file://...)` 后监听 `requestfailed`，失败请求数必须为 `0`。
- 校验图片加载状态：`document.images` 中每张图应满足 `complete=true` 且 `naturalWidth>0`。
- 校验 DOM 页面数与预期一致（当前 V23 完整手册为 `18` 页容器）。

### 12.5 PDF 质检补充
- PDF 页数必须与 DOM 页数一致。
- 每个正文页顶部应可提取到章节号与章节名（如 `01 安全须知`）。
- 对 SVG 为主的文档，不得仅用 PDF 内嵌位图数量判断“无图”；需结合页面文本、矢量绘制对象、人工抽样联合判定。

### 12.6 Booklet 生成要求
- `make-booklet.py` 的 `jobs` 必须覆盖当次新增产物（包括实验风格产物）。
- 生成后验证 booklet 页数满足 `padded_pages / 2`（示例：18 页正文补齐到 20 页后，booklet 应为 10 页）。

### 12.7 SVG Zero-Size Risk (Added 2026-03-01)
- Experience: for SVG `<img>` inside `flex + print`, using only `max-width/max-height` can collapse rendered size to `0x0`, causing ?loaded but invisible? images in PDF.
- Development requirements:
  - For operation-page and cover SVG images, always set explicit `width` and `height:auto`, then keep `max-width/max-height` as upper bounds.
  - Standard styles:
    - Operation figures: `style="width:45mm;height:auto;max-height:40mm;max-width:45mm"`
    - Cover figures: `style="width:100%;height:auto;max-height:85mm;max-width:100%"`
  - Do not add new SVG `<img>` that has only `max-width/max-height` without explicit `width`.
- QA requirements:
  - Add Playwright zero-size gate: if `naturalWidth>0` but `getBoundingClientRect().width==0` or `height==0`, mark build as FAIL.
  - For current V23, screenshot-sample key operation pages (8~11) after PDF export.
  - Archive validation logs with image count, `zero_render` count, and failed entries.
- [ ] Playwright zero-size check passed (`zero_render = 0`)
- [ ] Key operation pages (8~11) screenshot spot-check passed (image + header both present)

### 12.8 Pagination / Header / Caption Consistency Gate (Added 2026-03-01)
- Pagination hard rules:
  - `sub-title` + 其后步骤正文必须作为一个最小块布局；若剩余空间不足，整体换页。
  - 同一章节跨页时，不得出现“前页大面积留白 + 后页仅延续少量内容”的分页。
  - 操作图与对应步骤优先同页；若必须跨页，图文需在相邻页且保持顺序一致。
- Header and vertical rhythm:
  - 正文页（封面/目录除外）首内容块顶部间距应在同一版本内保持稳定，允许误差不超过 2 mm。
  - 页眉/章节顶栏不得在同一版本中“部分页面有、部分页面无”。
- Figure caption and numbering:
  - 同层级操作示意图图注策略必须一致，不允许混用“部分有 Fig. 标注、部分无标注”。
  - 存在图内 callout 编号（如控制面板 1..7）时，正文必须给出同编号映射说明，且编号连续无缺失。

### 12.9 Reading PDF vs Booklet Acceptance Scope (Added 2026-03-01)
- 阅读审计对象必须是阅读版 PDF（`*-fixed.pdf` 或主输出 PDF），不得用 booklet 视觉顺序判定正文分页正确性。
- Booklet 仅审计印刷拼版正确性（页数、补页、正反面配对），不作为“阅读顺序”合规依据。

### 12.10 Print Layout Stability Gate (Added 2026-03-01 v2)
- 禁止在 `@media print` 中使用按页序号的 `zoom` 热修（如 `.page:nth-of-type(n)`）作为长期方案。
- 若出现分页溢出，必须优先使用“结构化修复”：
  - 拆分内容块，或
  - 对特定页面容器增加显式紧凑类（如 `compact-ops` / `compact-accessories` / `compact-warranty`），并保证语义清晰。
- 阅读版 PDF 的页数必须与设计页数一致（当前 V23 目标为 18 页）；禁止产生“无页脚的额外物理页”。
- 封面外（第 2 页起）每页必须存在统一页脚品牌线与页码，缺失即判定为分页溢出 ERROR。
- 控制面板 callout 映射建议使用可移植字符（ASCII `1..7`），避免使用可能出现字体回退的特殊圈号字符。
- 以 `V23-修正版-20260225.docx` 为基线时，每份 HTML 的图片加载验收应满足：
  - `document.images` 总数 = 15（13 SVG + 2 PNG）
  - `failed = 0` 且 `naturalWidth/naturalHeight` 均大于 0。
