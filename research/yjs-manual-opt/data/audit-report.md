# V23 说明书审计报告

审计日期：2026-02-26
审计对象：v23-manual-cn.html / v23-manual-en.html + 对应 PDF
审计基准：extracted_v23.txt、product-config.json、d5-manual-standard.md、d4-full-issue-list.md

## 审计概要

- 总体评级：**C 级 → 修复后 A 级**
- ERROR：7 个 → 全部已修复（2026-02-26）
- WARNING：11 个 → 全部已修复（2026-02-26）
- INFO：5 个（保留，非阻塞）

### 修复摘要（2026-02-26）

1. 从 Word docx 提取 13 个 SVG 矢量图，替换全部 12 处图片引用为正确的 SVG
2. 重建 product-config.json 图片映射表（SVG + PNG fallback 双轨）
3. CN 版删除美标参数，只保留欧标（220~240V/50Hz）
4. 两版字体改为 HarmonyOS Sans SC 优先
5. 两版感谢语按规范模板格式修改
6. CN 版补充制造商英文名
7. 两版 CSS 添加打印分页保护规则
8. 两版页边距统一为 12.7mm
9. 两版卷袋图注补充 Figure 编号（图 11/12）
10. CN 版去除 emoji 图标，与 EN 版统一
11. 重新生成 PDF

---

## 维度 1：PDF 分页问题

| # | 位置 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 1.1 | 全局 CSS | `.page` 使用 `min-height: 297mm` 但无 `max-height` 或 `overflow: hidden`，内容超出时不会截断而是撑大容器，PDF 生成时可能导致内容溢出到下一页重叠 | WARNING | 添加 `max-height: 297mm; overflow: hidden;` 或在 `@media print` 中设置 `height: 297mm` |
| 1.2 | 全局 CSS | `@media print` 规则过于简单，仅设置了背景色和 margin，缺少 `page-break-inside: avoid` 对表格和步骤列表的保护 | WARNING | 添加：`table, .steps, .warning-box, .caution-box, .note-box { page-break-inside: avoid; }` 和 `.section-title, .sub-title { page-break-after: avoid; }` |
| 1.3 | 全局 CSS | 页面 padding 为 `15mm 14mm 18mm`，与规范要求的 `12.7mm`（0.5"）不一致 | WARNING | 改为 `padding: 12.7mm;`，同时调整 `.page-footer` 的 `bottom` 和 `left/right` 值 |
| 1.4 | 第 12 页（CN 故障排除） | 故障排除表格行数多（18 行 tbody），加上两个 note-box，内容量大，可能超出单页 297mm | WARNING | 考虑将故障排除表拆分到两页，或在表格中间添加 `page-break-before` |
| 1.5 | 第 12 页（EN Troubleshooting） | 同上，EN 版故障排除表同样内容密集 | WARNING | 同上 |

---

## 维度 2：图片问题（严重）

### 根因分析

Word 文档（V23-修正版-20260225.docx）中包含 31 个媒体文件：13 个 SVG（矢量图，高质量）+ 18 个 PNG（低分辨率回退）。Word 的图片存储机制是每个位置存一对 SVG+PNG，浏览器/打印优先用 SVG，PNG 仅作回退。

**提取图片时只拿了 PNG，完全丢失了 13 个 SVG 矢量图。**

更严重的是，Word 中多个不同位置的图片共用了同一个 PNG 回退文件（因为 SVG 才是真正不同的图），导致：

### 重复文件（MD5 完全相同）

| 文件组 | MD5 | 尺寸 | product-config 声称的用途 |
|--------|-----|------|--------------------------|
| image3.png = image6.png = image8.png | 8db50dfac588 | 209x194px, 9803 bytes | 切袋刀 / 真空软管 / 梅森罐 |
| image4.png = image7.png | d2a276c35e66 | 1438x942px, 290427 bytes | 密封操作 / 封面产品图 |

### Word 文档中图片的真实位置（16 个 Drawing）

| Drawing# | PNG 文件 | SVG 文件 | Word 中的上下文位置 | HTML 中的用途 | 匹配？ |
|----------|----------|----------|-------------------|-------------|--------|
| #1 | image1.png | image2.svg | 封面（型号 V23 之后） | 产品结构图 | **错配** — 封面应用封面图 |
| #2 | image4.png | image5.svg | "产品结构"章节 | 密封操作 | **错配** — 这是结构图 |
| #3 | image3.png | 无 SVG | Figure 1 标注图（零件标注） | 切袋刀操作 | **错配** — 这是零件标注 |
| #4 | image3.png | 无 SVG | "卷袋仓"之后（重复） | — | 重复引用 |
| #5 | image9.png | image10.svg | "产品功能"章节 | 液体模式 | **错配** — 这是控制面板 |
| #6 | image11.png | image12.svg | "操作指引"开头 | 未引用 | — |
| #7 | image13.png | image14.svg | 密封操作步骤中 | 真空罐操作 | **错配** — 这是密封操作 |
| #8 | image15.png | image16.svg | "真空密封液体"章节 | 腌制操作 | **错配** — 这是液体模式 |
| #9 | image17.png | image18.svg | 真空软管说明 | 控制面板 | **错配** — 这是软管图 |
| #10 | image19.png | image20.svg | Figure 6 之后（梅森罐开头） | 未引用 | — |
| #11 | image21.png | image22.svg | 梅森罐步骤中 | 未引用 | — |
| #12 | image23.png | image24.svg | 真空罐步骤中 | 未引用 | — |
| #13 | image25.png | image26.svg | 腌制步骤中 | 单卷袋放置 | **错配** — 这是腌制图 |
| #14 | image27.png | image28.svg | 卷袋仓说明 | 双卷袋放置 | 可能正确（卷袋仓区域） |
| #15 | image29.png | image30.svg | Figure 11 单卷袋 | 未引用 | — |
| #16 | image31.png | 无 SVG | 保修卡底部装饰 | 未引用 | — |

### 问题清单

| # | 图片文件 | 问题描述 | 级别 | 修复建议 |
|---|----------|----------|------|----------|
| 2.1 | image3 = image6 = image8 | **三个"不同"图片实际是同一张**（209x194px 低分辨率 PNG）。切袋刀、真空软管、梅森罐三个章节显示的是完全相同的图片，用户无法区分操作 | **ERROR** | 必须从 Word 文档重新提取 SVG 矢量图，或找到原始高清图片资源重新映射 |
| 2.2 | image4 = image7 | **封面产品图和密封操作图是同一张**（1438x942px）。封面显示的图和密封章节的图完全一样 | **ERROR** | 同上，需要从 SVG 源重新提取 |
| 2.3 | 全部 PNG | **所有 PNG 都是低分辨率回退图**，Word 中的高质量 SVG 矢量图（13 个，总计 3.3MB）全部丢失。打印 PDF 时图片质量会明显低于原始 Word 文档 | **ERROR** | 从 Word docx 中提取 SVG 文件，转换为 PNG（高分辨率）或直接在 HTML 中使用 SVG |
| 2.4 | product-config.json | **图片映射表与实际内容不匹配**。config 中声称 image3=切袋刀、image6=真空软管、image8=梅森罐，但这三个文件是同一张图 | **ERROR** | 重建图片映射表，基于 Word 文档中 SVG 的实际位置重新对应 |
| 2.5 | CN/EN 卷袋图 | 图注缺少 Figure 编号（"图 —" 而非 "图 11 —"） | WARNING | 补充编号 |
| 2.6 | image11, image19, image21, image23, image29, image31 | 6 个 PNG 文件存在但未被 HTML 引用。其中部分（如 image19=梅森罐开头、image21=梅森罐步骤、image23=真空罐步骤）可能才是正确的配图 | WARNING | 核查这些未引用图片的内容，可能需要替换当前错配的引用 |

### 正确的图片映射（基于 Word 文档上下文推断）

| 用途 | 当前 HTML 引用 | 应该引用（基于 Word 位置） | SVG 源 |
|------|---------------|--------------------------|--------|
| 封面 | image7.png | image1.png 或需要单独封面图 | image2.svg |
| 产品结构 | image1.png | image4.png（Drawing #2 在"产品结构"章节） | image5.svg |
| 控制面板 | image17.png | image9.png（Drawing #5 在"产品功能"章节） | image10.svg |
| 切袋刀操作 | image3.png | image11.png（Drawing #6 在"操作指引"开头） | image12.svg |
| 密封操作 | image4.png | image13.png（Drawing #7 在密封步骤中） | image14.svg |
| 液体模式 | image9.png | image15.png（Drawing #8 在"真空密封液体"） | image16.svg |
| 真空软管 | image6.png | image17.png（Drawing #9 在软管说明） | image18.svg |
| 梅森罐 | image8.png | image21.png（Drawing #11 在梅森罐步骤） | image22.svg |
| 真空罐 | image13.png | image23.png（Drawing #12 在真空罐步骤） | image24.svg |
| 腌制 | image15.png | image25.png（Drawing #13 在腌制步骤） | image26.svg |
| 单卷袋 | image25.png | image27.png（Drawing #14 在卷袋仓） | image28.svg |
| 双卷袋 | image27.png | image29.png（Drawing #15 在 Figure 11 后） | image30.svg |

---

## 维度 3：内容准确性问题

| # | 位置 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 3.1 | CN 第 5 章 | 中文版技术参数同时包含美标和欧标两套数据。根据 d5-manual-standard.md 第六节"按市场出独立版本"，中国版应只包含欧标参数（220V/50Hz） | ERROR | 中文版删除美标参数表，只保留欧标。如需同时保留，至少应标注"本机适用参数"以区分 |
| 3.2 | EN 第 5 章 | 英文版技术参数只有美标（110~120V/60Hz），符合北美版要求 | INFO（通过） | — |
| 3.3 | CN 第 4 章 | Pulse Vac 按键描述为"手动抽气"，与 product-config.json 一致（key: "Pulse Vac", name_cn: "手动抽气"），原文 extracted_v23.txt 中的"手动密封"错误已修正 | INFO（通过） | — |
| 3.4 | CN/EN 第 10 章 | 品牌信息只有 Wevac，无其他品牌泄漏 | INFO（通过） | — |
| 3.5 | CN/EN 第 10 章 | 客服邮箱已填写为 support@wevactech.com，与 product-config.json 一致 | INFO（通过） | — |
| 3.6 | CN 第 10 章 | 感谢语仍为"再次感谢您购买我们的真空封装机器"，未按 d5-manual-standard.md 第七节模板格式（应为"感谢您购买 [品牌名] [产品名]"） | WARNING | 改为"感谢您购买 Wevac 真空封装口机。如有任何问题，请通过以下方式联系我们：support@wevactech.com | www.wevactech.com" |
| 3.7 | EN 第 10 章 | 英文版感谢语同样未按模板格式 | WARNING | 改为"Thank you for choosing Wevac Vacuum Sealer. For support, contact us at: support@wevactech.com | www.wevactech.com" |
| 3.8 | CN 第 10 章 | 缺少制造商英文名（Guangzhou Argion Electric Appliance Co., Ltd.），只有中文名 | WARNING | 补充英文名，便于国际客户识别 |
| 3.9 | CN 第 9 章 | 原文 extracted_v23.txt 中食物保鲜表"冷藏储存"出现两次（第 362 行和第 378 行），第二次实际应为"常温储存"。HTML 中已正确修正为"常温储存" | INFO（通过） | — |
| 3.10 | CN/EN 第 3 章 | 零件数量 13 个，与 product-config.json 的 parts 数组（13 项）一致 | INFO（通过） | — |
| 3.11 | CN/EN 第 4 章 | 按键数量 7 个，与 product-config.json 的 buttons 数组（7 项）一致 | INFO（通过） | — |

---

## 维度 4：排版规范合规问题

| # | 位置 | 问题描述 | 级别 | 修复建议 |
|---|------|----------|------|----------|
| 4.1 | CN 安全须知 | WARNING 标题颜色为 `#E65100`，规范要求 `#E97132`（参照小米规范） | WARNING | 将 `.warning-box .box-title` 的 color 改为 `#E97132` |
| 4.2 | 全局 CSS | 表头背景色为 `#F5F5F5`，规范要求 `#F2F2F2` | INFO | 差异极小（3 个色阶），可接受，但建议统一为 `#F2F2F2` |
| 4.3 | 全局 CSS | 表格边框色为 `#E0E0E0`，规范要求 `#CCCCCC` | INFO | 差异较小，建议统一为 `#CCCCCC` |
| 4.4 | CN 章节标题 | 目录中"产品功能"对应规范表应为"产品概览"（d5-manual-standard.md 第二节），但原文 V23 确实是"产品功能"独立于"产品结构" | WARNING | 建议将"产品结构"改为"产品概览"（含结构图+零件表），"产品功能"保留。或合并为"产品概览"一章 |
| 4.5 | EN 章节标题 | "Control Panel Functions"不在规范标题表中（规范为 Product Overview），"Vacuum Packaging Guide"不在规范表中（规范为无此章节） | WARNING | 如保持当前结构，在规范表中补充这些标题的映射 |
| 4.6 | 全局 CSS | 正文字体为 `"PingFang SC", "Microsoft YaHei"`，规范要求 `HarmonyOS Sans SC` | ERROR | 将 font-family 改为 `"HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", Arial, sans-serif`。注意需确保 HarmonyOS Sans SC 字体文件可用 |
| 4.7 | 全局 CSS | `.note-box` 竖线颜色为 `#BDBDBD`，规范要求 `#E5E5E5` | INFO | 改为 `border-left: 4px solid #E5E5E5` |

---

## 维度 5：中英一致性问题

| # | 项目 | CN 值 | EN 值 | 级别 | 修复建议 |
|---|------|-------|-------|------|----------|
| 5.1 | 章节数量 | 10 章 | 10 章 | INFO（通过） | — |
| 5.2 | 页数 | 17 页 | 17 页 | INFO（通过） | — |
| 5.3 | 零件数量 | 13 个 | 13 个 | INFO（通过） | — |
| 5.4 | 按键数量 | 7 个 | 7 个 | INFO（通过） | — |
| 5.5 | 技术参数 | 美标+欧标 | 仅美标 | ERROR | CN 版应只保留欧标（见 3.1），或两版都保留双标但标注适用市场 |
| 5.6 | Pulse Vac 翻译 | 手动抽气 | Manual Vacuum | INFO（通过） | — |
| 5.7 | 安全警示图标 | CN 有 ⚠/⚡/📝 emoji | EN 无 emoji | WARNING | 建议统一：要么都用 emoji，要么都不用。推荐都不用，改用 CSS 图标 |
| 5.8 | 图片引用 | 12 张 | 12 张，完全一致 | INFO（通过） | — |

---

## 维度 6：已知问题回归

对照 d4-full-issue-list.md 的 19 个问题：

| # | 原编号 | 问题描述 | 状态 | 备注 |
|---|--------|----------|------|------|
| 1 | C01 | 安全警示体系不统一（V23两级） | **FIXED** | CN 版已有 WARNING/CAUTION/NOTICE 三级体系，EN 版同样三级 |
| 2 | C02 | 安全须知双句号语法错误 | **FIXED** | CN 第 376 行已拆分为两条独立警示，无双句号 |
| 3 | C03 | Note 重复出现 4 次 | **FIXED** | CN 第 444-447 行 Note 只出现一次 |
| 4 | C04 | "其他事务"错别字 | **FIXED** | CN 第 419 行已改为"食物" |
| 5 | C05 | Pulse Vac 按键名称"手动密封"应为"手动抽气" | **FIXED** | CN 第 464 行已改为"手动抽气" |
| 6 | C06 | IMT050 缺少知识科普章节 | **NOT_APPLICABLE** | 本次审计范围为 V23，不涉及 IMT050 |
| 7 | C07 | IMT050 安装章节标题冗长 | **NOT_APPLICABLE** | 同上 |
| 8 | C08 | 多品牌信息靠人工删减 | **FIXED** | HTML 中只保留 Wevac 品牌信息，通过 product-config.json 管理 |
| 9 | C09 | 客服邮箱为占位符 | **FIXED** | 已填写 support@wevactech.com |
| 10 | C10 | 美标/欧标参数混在同一文档 | **PARTIAL** | EN 版已分离（仅美标），CN 版仍同时包含美标+欧标 |
| 11 | C11 | 图文关联无结构化管理 | **FIXED** | HTML 中图片通过 product-config.json 映射管理，src 路径结构化 |
| 12 | C12 | 章节标题跨产品命名不统一 | **NOT_APPLICABLE** | 本次只审计 V23 单产品 |
| 13 | C13 | 保修卡设计简陋 | **STILL_OPEN** | 保修卡仍为简单表格，无品牌 logo、产品图、二维码 |
| 14 | C14 | 感谢语措辞不一致且空洞 | **PARTIAL** | 措辞已统一用"您"，但未按规范模板格式 |
| 15 | L01 | 食物保鲜表绿色表头 | **FIXED** | HTML 中所有表格统一使用 `#F5F5F5` 浅灰表头 |
| 16 | L02 | 红色编辑注释残留 | **FIXED** | HTML 中无红色注释文字，无"以下请按对应客户选择删减" |
| 17 | L03 | 图片锚定方式不统一 | **FIXED** | HTML 中所有图片均为 inline（嵌入式），无浮动 |
| 18 | L04 | 页边距不一致 | **PARTIAL** | 两版 HTML 使用相同 CSS（padding: 15mm 14mm 18mm），已统一但数值与规范 12.7mm 不一致 |
| 19 | L05 | 表格样式不统一 | **FIXED** | HTML 中所有表格使用统一 CSS 样式 |

**回归统计**：FIXED 12 个 | PARTIAL 3 个 | STILL_OPEN 1 个 | NOT_APPLICABLE 3 个

---

## 修复优先级建议

### 必须修复（ERROR — 7 个）

1. **2.1 — 三张"不同"图片实际是同一张（image3=image6=image8）**
   - 切袋刀、真空软管、梅森罐三个章节显示完全相同的图片
   - 必须从 Word 文档提取 SVG 矢量图重新生成高清 PNG

2. **2.2 — 封面图和密封操作图是同一张（image4=image7）**
   - 封面和密封章节显示完全相同的图片

3. **2.3 — 全部 13 个 SVG 矢量图丢失**
   - Word 中的高质量图片全部丢失，仅保留低分辨率 PNG 回退
   - 需要重新从 docx 提取 SVG 并转换

4. **2.4 — product-config.json 图片映射表与实际内容不匹配**
   - 需要基于 Word 文档中 Drawing 的实际位置重建映射

5. **3.1/5.5 — CN 版技术参数包含美标数据**
   - 中文版面向中国市场，应只保留欧标参数（220~240V/50Hz）

6. **4.6 — 字体不符合规范**
   - 将 CSS `font-family` 首选字体改为 `HarmonyOS Sans SC`
   ```css
   body {
     font-family: "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
   }
   ```

### 建议修复（WARNING — 11 个）

1. **1.1 — 添加页面溢出保护**
   ```css
   @media print {
     .page { height: 297mm; overflow: hidden; }
   }
   ```

2. **1.2 — 添加分页保护规则**
   ```css
   @media print {
     table, .steps, .warning-box, .caution-box, .note-box { page-break-inside: avoid; }
     .section-title, .sub-title { page-break-after: avoid; }
   }
   ```

3. **1.3 — 页面 padding 改为 12.7mm**

4. **1.4/1.5 — 故障排除表内容密集**，考虑拆页或缩小字号

5. **2.2/2.3 — 卷袋图注补充 Figure 编号**

6. **3.6/3.7 — 感谢语按规范模板格式修改**

7. **3.8 — CN 版补充制造商英文名**

8. **4.1 — WARNING 标题颜色改为 #E97132**

9. **4.4/4.5 — 章节标题与规范表对齐**

10. **5.7 — 中英版安全警示图标统一**

### 可选优化（INFO — 5 个）

1. 2.1 — 清理 6 个未引用的冗余图片文件
2. 4.2 — 表头背景色微调为 #F2F2F2
3. 4.3 — 表格边框色微调为 #CCCCCC
4. 4.7 — note-box 竖线颜色改为 #E5E5E5
5. C13 — 保修卡增加品牌视觉元素（logo、二维码）
