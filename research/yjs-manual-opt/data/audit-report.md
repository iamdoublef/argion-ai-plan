# V23 说明书审计报告（第二轮）

审计日期：2026-02-26
审计对象：v23-manual-cn.html / v23-manual-en.html + 对应 PDF
审计基准：extracted_v23.txt / product-config.json / d5-manual-standard.md / d4-full-issue-list.md
前次审计：本文件第一轮审计（2026-02-26），已全部修复

## 审计概要

- 总体评级：B 级（小幅修正后可发布）
- ERROR：3 个
- WARNING：9 个
- INFO：多个（不计入评级）

评级标准：
- A 级（可直接发布）：无 ERROR，WARNING < 3
- B 级（小幅修正后可发布）：ERROR < 3 且均为细节级，WARNING < 10
- C 级（需要较大修正）：有 ERROR 或 WARNING >= 10
- D 级（需要重做）：多处 ERROR，结构性问题

说明：第一轮审计发现的 7 个 ERROR + 11 个 WARNING 已全部修复（SVG 提取、图片映射重建、CN 版删除美标参数、字体修正、分页保护等）。本轮为修复后的全面复审。

---

## 维度 1：PDF 分页问题

| # | 页码 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 1.1 | 全局 | `@media print` 中 `.page` 设置 `height: 297mm; overflow: hidden`，超出内容会被截断而非分页 | WARNING | 改为 `min-height: 297mm; overflow: visible`，依赖 `page-break-after: always` 控制分页 |
| 1.2 | P12 CN/EN | 故障排除表格行数多（21 行 tbody + 2 个 note-box），可能超出单页 | WARNING | 在合理位置（第 3 个故障类别后）允许分页 |
| 1.3 | P16 CN/EN | 食物保鲜表 16+ 行，可能超出单页 | WARNING | 在"冷藏储存"和"常温储存"之间允许分页 |
| 1.4 | 全局 | `page-break-inside: avoid` 已正确应用于 table/steps/warning-box/caution-box/note-box | INFO | 通过 |
| 1.5 | 全局 | `section-title`/`sub-title` 已设置 `page-break-after: avoid` | INFO | 通过 |
| 1.6 | 全局 | 页码连续（2-17），位置正确（底部左右分布） | INFO | 通过 |

---

## 维度 2：图片问题

| # | 图片文件 | 问题描述 | 级别 | 修复建议 |
|---|----------|----------|------|----------|
| 2.1 | image3.png = image6.png = image8.png | MD5 完全相同（8DB50DFA...），均 9803 字节，Word 提取时的重复 PNG 回退 | WARNING | 确认后删除冗余文件，保留一个即可 |
| 2.2 | image4.png = image7.png | MD5 完全相同（D2A276C3...），均 290KB | WARNING | 同上 |
| 2.3 | 18 个 PNG 文件 | 存在但未被任何 HTML 引用（image1/3/4/6/7/8/9/11/13/15/17/19/21/23/25/27/29/31.png） | WARNING | 这些是 SVG 的 PNG 回退。如不需要可清理；如需保留建议用 `<picture>` 标签 |
| 2.4 | image20.svg | SVG 文件存在但未被任何 HTML 引用，product-config.json 中也无对应 | WARNING | 确认用途，无用则删除 |
| 2.5 | 全局 | 所有 HTML 引用的 12 个 SVG 文件均存在于磁盘，无缺失 | INFO | 通过 |
| 2.6 | 全局 | 所有 `<img>` 标签均有有意义的 alt 属性（CN 中文，EN 英文） | INFO | 通过 |
| 2.7 | 全局 | CN 和 EN 引用完全相同的 12 个图片文件，顺序一致 | INFO | 通过 |

---

## 维度 3：内容准确性问题

| # | 位置 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 3.1 | EN 第 10 章 | EN 版缺少制造商（Manufacturer）信息表格。CN 版有"授权制造商"表格含中英文名、地址、网址，EN 版没有 | ERROR | 在 EN 版 Brand Information 后添加 Manufacturer 表格：Guangzhou Argion Electric Appliance Co., Ltd. / 广东省广州市番禺区南村镇启业路1号 / www.argiontechnology.com |
| 3.2 | CN/EN 第 4 章 | Pulse Vac：CN "手动抽气"，EN "Manual Vacuum"，均正确 | INFO | 通过，原文 C05 已修复 |
| 3.3 | CN/EN 第 5 章 | 技术参数与 product-config.json 完全一致：CN=欧标，EN=美标 | INFO | 通过 |
| 3.4 | CN/EN 第 10 章 | 品牌信息只有 Wevac（active_brand），无其他品牌泄漏 | INFO | 通过 |
| 3.5 | CN/EN 第 10 章 | 客服邮箱 support@wevactech.com，非占位符 | INFO | 通过 |
| 3.6 | CN 第 2 章 | 原文错别字"其他事务"已修正为"食物" | INFO | 通过 |
| 3.7 | CN 第 9 章 | 原文"冷藏储存"重复已修正为"常温储存" | INFO | 通过 |

---

## 维度 4：排版规范合规问题

| # | 位置 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 4.1 | 全局 | 安全警示三级体系完整：WARNING + CAUTION + NOTICE，样式正确 | INFO | 通过 |
| 4.2 | CN/EN 目录 | 章节标题"产品功能/Control Panel Functions"和"真空包装特性/Vacuum Packaging Guide"不在规范标准表中 | WARNING | 可接受偏差，建议在规范中补充"可选章节"说明 |
| 4.3 | 全局 CSS | 表头背景色 #F5F5F5，规范要求 #F2F2F2 | WARNING | 修改 `th { background: #F2F2F2; }` |
| 4.4 | 全局 CSS | 表格边框色 #E0E0E0，规范要求 #CCCCCC | WARNING | 修改 `border: 1px solid #CCCCCC;` |
| 4.5 | 全局 | 无红色编辑注释残留 | INFO | 通过 |
| 4.6 | 全局 | 无绿色表头 | INFO | 通过 |
| 4.7 | 全局 | 字体已为 HarmonyOS Sans SC 优先 | INFO | 通过 |
| 4.8 | 全局 | 页边距统一 12.7mm | INFO | 通过 |

---

## 维度 5：多语言描述一致性

### 5A 结构一致性

| # | 项目 | CN 值 | EN 值 | 级别 | 备注 |
|---|------|-------|-------|------|------|
| 5A.1 | 章节数量 | 10 章 | 10 章 | INFO | 一致 |
| 5A.2 | 章节顺序 | 安全→提示→结构→功能→参数→操作→故障→维护→包装→品牌 | 对应英文 | INFO | 一致 |
| 5A.3 | 总页数 | 17 页 | 17 页 | INFO | 一致 |
| 5A.4 | 操作指引子节数 | 10 个（6.1-6.10） | 10 个（6.1-6.10） | INFO | 一致 |

### 5B 安全须知一致性

| # | 项目 | CN | EN | 一致？ | 级别 |
|---|------|----|----|--------|------|
| 5B.1 | WARNING 条目数 | 13 | 13 | 是 | INFO |
| 5B.2 | CAUTION 条目数 | 4 | 4 | 是 | INFO |
| 5B.3 | NOTICE 条目数 | 3 | 3 | 是 | INFO |
| 5B.4 | 双句号问题 | 已修复 | N/A | - | INFO |

### 5C 零件与按键一致性

| # | 项目 | CN | EN | 一致？ | 级别 |
|---|------|----|----|--------|------|
| 5C.1 | 零件数量 | 13 | 13 | 是 | INFO |
| 5C.2 | 锁扣把手 | 锁扣把手 | Latch Handle | 是 | INFO |
| 5C.3 | 面盖 | 面盖 | Top Lid | 是 | INFO |
| 5C.4 | 密封圈 | 密封圈 | Sealing Gasket | 是 | INFO |
| 5C.5 | 发热器 | 高温胶布与发热器 | Heat Tape & Heating Element | 是 | INFO |
| 5C.6 | Pulse Vac | 手动抽气 | Manual Vacuum | 是 | INFO |
| 5C.7 | 按键数量 | 7 | 7 | 是 | INFO |

### 5D 操作步骤一致性

| # | 章节 | CN 步骤数 | EN 步骤数 | 一致？ | 级别 |
|---|------|----------|----------|--------|------|
| 5D.1 | 6.1 切袋刀 | 5 | 5 | 是 | INFO |
| 5D.2 | 6.2 密封（制袋） | 4 | 4 | 是 | INFO |
| 5D.3 | 6.2 密封（单独） | 3 | 3 | 是 | INFO |
| 5D.4 | 6.4 真空密封固体 | 5 | 5 | 是 | INFO |
| 5D.5 | 6.4 真空密封液体 | 5 | 5 | 是 | INFO |
| 5D.6 | 6.5 手动真空方法一 | 3 | 3 | 是 | INFO |
| 5D.7 | 6.5 手动真空方法二 | 5 | 5 | 是 | INFO |
| 5D.8 | 6.7 梅森罐 | 9 | 9 | 是 | INFO |
| 5D.9 | 6.8 真空罐 | 8 | 8 | 是 | INFO |
| 5D.10 | 6.9 腌制 | 8 | 8 | 是 | INFO |
| 5D.11 | 配图引用 | 12 张 SVG | 12 张 SVG（同文件） | 是 | INFO |

### 5E 技术参数一致性

| # | 参数 | CN 值 | EN 值 | 级别 | 问题描述 |
|---|------|-------|-------|------|----------|
| 5E.1 | 电压 | 220~240 Vac | 110~120 Vac | INFO | 正确，CN=欧标，EN=美标 |
| 5E.2 | 频率 | 50 Hz | 60 Hz | INFO | 正确 |
| 5E.3 | 功率 | 190 W | 190 W | INFO | 一致 |
| 5E.4 | 泵 | 双泵 | Dual Pump | INFO | 一致 |
| 5E.5 | 真空压力 | -958 mbar | -28.3 inHg | INFO | 正确 |
| 5E.6 | 发热丝宽度 | 1.8 mm x 2 | 0.07 inch x 2 | INFO | 正确 |
| 5E.7 | 尺寸 | 380x205x155 mm | 15x8.1x6.1 inch | INFO | 正确 |
| 5E.8 | 重量 | 3.0 kg | 6.6 lb | INFO | 正确 |

### 5F 故障排除一致性

| # | 故障类别 | CN 条目数 | EN 条目数 | 一致？ | 级别 |
|---|---------|----------|----------|--------|------|
| 5F.1 | 不能开机 | 3 | 3 | 是 | INFO |
| 5F.2 | 抽气不干净 | 6 | 6 | 是 | INFO |
| 5F.3 | 不能密封 | 4 | 4 | 是 | INFO |
| 5F.4 | 袋子漏气 | 3 | 3 | 是 | INFO |
| 5F.5 | Accessories 无法抽气 | 3 | 3 | 是 | INFO |
| 5F.6 | 错误报警 | 2 | 2 | 是 | INFO |
| 5F.7 | 液体进入真空腔 | 6 步 | 6 步 | 是 | INFO |
| 5F.8 | 液体进入发热器 | 6 步 | 6 步 | 是 | INFO |

### 5G 品牌与保修一致性

| # | 字段 | CN 值 | EN 值 | 一致？ | 级别 |
|---|------|-------|-------|--------|------|
| 5G.1 | 品牌名 | WEVAC TECHNOLOGY CO., LIMITED | WEVAC TECHNOLOGY CO., LIMITED | 是 | INFO |
| 5G.2 | 地址 | FLAT/RM 404A... | FLAT/RM 404A... | 是 | INFO |
| 5G.3 | 网址 | www.wevactech.com | www.wevactech.com | 是 | INFO |
| 5G.4 | 邮箱 | support@wevactech.com | support@wevactech.com | 是 | INFO |
| 5G.5 | 保修年限 | 2 年 | 2 years | 是 | INFO |
| 5G.6 | 保修卡字段数 | 9 | 9 | 是 | INFO |
| 5G.7 | 制造商信息 | 有（广州亚俊氏+英文名） | **缺失** | 否 | ERROR |

### 5H 翻译质量抽查

| # | 中文术语 | 期望英文 | 实际英文 | 正确？ | 级别 |
|---|---------|---------|---------|--------|------|
| 5H.1 | 发热器 | heating element | Heating Element | 是 | INFO |
| 5H.2 | 密封圈 | sealing gasket | Sealing Gasket | 是 | INFO |
| 5H.3 | 真空腔 | vacuum chamber | vacuum chamber | 是 | INFO |
| 5H.4 | 面盖 | top lid | Top Lid | 是 | INFO |
| 5H.5 | 锁扣把手 | latch handle | Latch Handle | 是 | INFO |
| 5H.6 | 请勿/严禁 | Do not / Never | Do not / Never | 是 | INFO |
| 5H.7 | 操作步骤动词 | 祈使句 | Open/Place/Close/Press | 是 | INFO |
| 5H.8 | 温度 CN | °C | -4°C | 是 | INFO |
| 5H.9 | 温度 EN | °F + °C | 25 °F (-4 °C) | 是 | INFO |
| 5H.10 | 液体槽 | drip tray | Drip Tray | 是 | INFO |
| 5H.11 | CN 第 9 章"重要提示" | IMPORTANT | EN 用 "IMPORTANT" | - | ERROR | CN 用"重要提示"，EN 用"IMPORTANT"，但这个 warning-box 的 box-title 不是标准三级体系中的任何一级。应统一为 WARNING 或 NOTICE |

---

## 维度 6：已知问题回归

| # | 原编号 | 问题描述 | 状态 | 备注 |
|---|--------|----------|------|------|
| 6.1 | C01 | 安全警示体系不统一 | **FIXED** | CN/EN 均已实现三级体系 |
| 6.2 | C02 | 安全须知双句号 | **FIXED** | 已拆为两条独立警示 |
| 6.3 | C03 | Note 重复 4 次 | **FIXED** | 只出现 1 次 |
| 6.4 | C04 | "其他事务"错别字 | **FIXED** | 已改为"食物" |
| 6.5 | C05 | Pulse Vac "手动密封" | **FIXED** | 已改为"手动抽气" |
| 6.6 | C06 | IMT050 缺科普章节 | **N/A** | 不涉及 IMT050 |
| 6.7 | C07 | IMT050 标题冗长 | **N/A** | 不涉及 IMT050 |
| 6.8 | C08 | 多品牌信息人工删减 | **FIXED** | 通过 config 管理，只有 Wevac |
| 6.9 | C09 | 客服邮箱占位符 | **FIXED** | 已填写 support@wevactech.com |
| 6.10 | C10 | 美标/欧标混在一起 | **FIXED** | CN=欧标，EN=美标 |
| 6.11 | C12 | 章节标题跨产品不统一 | **N/A** | 只审计 V23 |
| 6.12 | C13 | 保修卡设计简陋 | **STILL_OPEN** | 仍为简单表格，无品牌 logo/二维码 |
| 6.13 | C14 | 感谢语不一致 | **FIXED** | 已按规范模板格式 |
| 6.14 | L01 | 绿色表头 | **FIXED** | 统一 #F5F5F5 |
| 6.15 | L02 | 红色编辑注释 | **FIXED** | 无残留 |
| 6.16 | L03 | 图片锚定不统一 | **FIXED** | 全部 inline |
| 6.17 | L04 | 页边距不一致 | **FIXED** | 统一 12.7mm |
| 6.18 | L05 | 表格样式不统一 | **FIXED** | 统一 CSS |

回归统计：FIXED 14 | STILL_OPEN 1 | N/A 3

---

## 维度 7：图片内容匹配

| # | 图片 | 所在章节 | 匹配？ | 级别 | 问题描述 |
|---|------|---------|--------|------|----------|
| 7.1 | image2.svg (160KB) | 封面 | 待人工确认 | INFO | 需确认为 V23 产品渲染图 |
| 7.2 | image5.svg (646KB) | 产品结构 | 待人工确认 | INFO | 文件最大，应为完整结构图 |
| 7.3 | image10.svg (82KB) | 控制面板 | 待人工确认 | INFO | 控制面板图 |
| 7.4 | image3/6/8.png | 未引用 | - | WARNING | 3 个 MD5 相同的 PNG，冗余文件 |
| 7.5 | image4/7.png | 未引用 | - | WARNING | 2 个 MD5 相同的 PNG，冗余文件 |
| 7.6 | image20.svg (70KB) | 未引用 | - | WARNING | 孤立 SVG 文件 |
| 7.7 | image31.png (2.6KB) | 未引用 | - | INFO | 极小文件，可能是装饰元素 |

---

## 修复优先级建议

### 必须修复（ERROR）

1. **3.1 / 5G.7** — EN 版添加 Manufacturer 信息表格（Guangzhou Argion Electric Appliance Co., Ltd. / 地址 / 网址）
2. **5H.11** — CN 第 9 章"重要提示"和 EN "IMPORTANT" 不属于标准三级体系。建议改为 WARNING 或在三级体系中增加 IMPORTANT 级别定义

### 建议修复（WARNING）

1. **1.1** — `@media print` 中 `overflow: hidden` 改为 `overflow: visible`
2. **1.2 / 1.3** — 大表格分页策略
3. **4.3** — 表头背景色 #F5F5F5 → #F2F2F2
4. **4.4** — 表格边框色 #E0E0E0 → #CCCCCC
5. **4.2** — 章节标题偏差，更新规范
6. **2.1 / 2.2 / 2.3 / 2.4 / 7.4-7.6** — 清理未引用的冗余图片文件

### 可选优化（INFO）

1. 图片内容需人工目视确认（7.1-7.3）
2. C13 保修卡增加品牌视觉元素
3. image31.png 确认用途

---

## 审计结论

V23 说明书经过第一轮审计修复后，质量已大幅提升。第一轮发现的 7 个 ERROR 全部修复（SVG 提取、图片映射重建、CN 删除美标参数、字体修正等）。本轮复审发现 3 个新 ERROR（EN 缺制造商信息、"重要提示"不在三级体系中），均为细节级问题。多语言一致性表现优秀：CN/EN 两版在结构、步骤数、数值、按键名称、故障排除条目等方面完全一致。d4 已知问题清单中涉及 V23 的 15 个问题，14 个已修复，1 个保留（保修卡设计）。
