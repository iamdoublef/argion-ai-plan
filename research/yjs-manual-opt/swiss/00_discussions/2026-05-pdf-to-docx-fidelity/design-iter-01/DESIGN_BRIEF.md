# design-iter-01 美感专项 — 精确修复清单

> 第 1 轮（4 路并行）虽然自动验收 PASS（视觉差 13.59-16.65），但用户判定"美感与 PDF 差距太大，完全不能接受"。
> 这一轮目标：**逐项消除像素级设计差异**，做到一眼看上去是同一份手册。

## 当前 winner (B1 iter-03) 与 PDF 的硬错误（精确分析）

来自 `extract_spans.py` 抽取的 PDF 内部元数据：

### 1. 字体严重错配（每一页都错）

| 角色 | PDF 实测 | 当前 WINNER | 修复 |
|---|---|---|---|
| 中文正文 | **MicrosoftYaHei** | SimSun（LibreOffice fallback） | docx `<w:rFonts eastAsia="Microsoft YaHei">` |
| 中文加粗 | **MicrosoftYaHei-Bold** | SimHei | 同上 + bold |
| 西文标题数字（大字号 13.5pt） | **Arial-Black** | ArialMT | latinFont 加粗版用 Arial Black |
| 西文正文 | ArialMT | ArialMT ✓ | OK |
| 等宽字体（章节号"01"等） | **CourierNewPSMT** | ArialMT | 章节编号用 Courier New |
| 中文兜底（小字 disclaimer） | NSimSun | SimSun | OK 近似 |

→ `swiss/tools/export-docx.js` `DEFAULT_DOCX_THEME` 改：
```js
latinFont: 'Arial',
cjkFont: 'Microsoft YaHei',     // 不要用 '宋体'
titleLatinFont: 'Arial Black',  // PDF 大标题用 Arial Black
titleCjkFont: 'Microsoft YaHei',  // PDF 中文大标题用 MicrosoftYaHei-Bold（同 YaHei + bold:true）
monoFont: 'Courier New',          // 新增等宽字体，章节号/MODEL 用
```

### 2. 字号全部偏大 7-15%

| PDF 实测 (pt) | WINNER 现在 | 修正 (half-pt) |
|---|---|---|
| 正文 6.6-7.5 | 8.0 | 14-15（不是 16） |
| 章节小标题 6.98 | 7.5+ | 14 |
| 章节大标题数字 13.5 | 12-14 | 27（13.5 × 2） |
| MODEL/标签 5.25-6.0 | 6.5 | 10-12 |
| 小字 disclaimer 5.4 | 6.5+ | 10-11 |

→ `DOCX_PROFILE.text`：
```js
bodySize: 14,           // was 16, target 7pt
subtitleSize: 14,
sectionTitleSize: 18,   // was 20
chapterNumberSize: 27,  // was 24 — 章节大数字 13.5pt
chapterTitleSize: 22,   // was 24 — 章节大标题 ~11pt
coverBrandSize: 28,
coverTypeSize: 11,      // was 16 — MODEL 标签 5.5pt
coverProductSize: 36,   // was 24 — 制冰机 18pt
coverModelSize: 11,
tocTitleSize: 26,
smallSize: 10,          // was 13 — 5pt
```

### 3. 封面颜色严重错配 ❗

PDF 设计语言：
- "威富可"（品牌名）= **#000000 黑色**（不是红色！）+ 顶部短红线
- "MODEL IMT050" = **#E63946 红色**（这才是红色突出）
- "制冰机"（产品名）= 主黑 #1A1A1A
- "说明书" = 灰色 #8E8E93
- 底部 disclaimer = 灰色 #8E8E93

当前 WINNER：
- "威富可" = 红色 ❌
- "MODEL IMT050" = 红色 ✓
- → 红色突出元素重复，失去层次

→ `swiss/tools/export-docx.js` `buildCoverBlock`：
- `text: ctx.brand.display_name` 的 TextRun，color 改为 `ACTIVE_THEME.primary`（#1A1A1A）
- 在品牌名前**加一条短红横线**（参考 PDF 顶部"━━ 威富可"的视觉）
- MODEL IMT050 保持红色 ✓

### 4. 灰色色值偏差

| 用途 | PDF | WINNER | 修正 |
|---|---|---|---|
| 次要文字（说明书/disclaimer/页脚） | **#8E8E93** | #8A8A8A | theme.light、theme.muted、headerText、footerText 全改 #8E8E93 |
| 主黑 | #1A1A1A | #1A1A1A | OK ✓ |
| accent 红 | #E63946 | #E63946 | OK ✓ |

### 5. 表格细节缺失（致命的"设计感"差异）

drawings 数量：
| 页 | 内容 | TARGET drawings | WINNER drawings | gap |
|---|---|---|---|---|
| 6 | 03 产品结构（爆炸图+编号表） | 57 | 41 | **-16** |
| 7 | 04 产品功能 | 48 | 28 | **-20** |
| 8 | **05 技术参数表** | 110 | 64 | **-46** ❗ |
| 11 | 07 故障排除表 | 87 | 55 | **-32** ❗ |
| 14 | 10 保修信息表 | 57 | 41 | -16 |
| 15 | 10 保修卡（续） | 61 | 39 | -22 |

→ PDF 表格有：
- 偶数行 zebra 底色 `#F4F4F4`（你之前 `tableLabelFill` 就是这个色，但只用在 label 列）
- 单元格底部细线（不是完整边框，只有底部）
- 表头深色背景 + 白字
- 行间距更紧凑

→ `swiss/tools/export-docx.js` 表格 helpers 改：
- `zebraShading(rowIndex)` 不要总返回 undefined，改成 rowIndex%2==1 时返回 light gray
- 单元格 border：top/bottom keep，left/right 改为 NO（横线表格风格，更像 PDF）
- 表头单元格 `<w:shd fill="1A1A1A">` 黑底白字

### 6. 章节首页缺设计层次

PDF 章节首页（如第 3 页 "01 安全须知"）：
- 左侧**黑色细 bar**（约 2pt）从章节号顶部延伸到标题底部
- 章节号 "01" 红色 Arial Black 13.5pt
- 章节名 "安全须知" 黑色 MicrosoftYaHei-Bold 13.5pt
- 右上角小字 "CH.01 — SAFETY" 灰色 ArialMT 5.25pt
- 章节号和标题水平对齐，bar 在最左

当前 WINNER：
- 黑色 bar 太粗（用了 size=12，约 1.5pt 还行但视觉差）
- 章节号字体用了 ArialMT（应是 Arial Black）
- 右上小字大小可能偏大

### 7. 警告框缺图标

PDF 警告/注意框：
- WARNING 标题左侧有 **⚠️ 三角警告图标**（红色，约 7×7pt）
- CAUTION 同样有图标，但黄色
- NOTICE 有 ℹ️ 图标，蓝色

当前 WINNER：
- 完全没有这些图标
- 框只有黑色边框 + 标题

→ 用 `swiss/products/imt050/images/safety.warning_icon.svg` 或 png（如果存在）；或者用 unicode `▲` + 红色 + size:18

### 8. 灰白条分隔线（subtle）

PDF 中很多地方有**极细的灰色分隔线**（比如 sub_title 下面、TOC 章节条目之间），WINNER 没有。

## 修复优先级（4 路必须做）

1. **P0 字体**：cjkFont 改 Microsoft YaHei，加 Arial Black 大标题，加 Courier New 等宽
2. **P0 封面**：威富可改黑色（不是红），加顶部短红线
3. **P0 字号**：全面下调（见上表），bodySize 14 不是 16
4. **P1 表格**：zebra striping + 横线表格风格 + 黑底白字表头
5. **P1 配色**：灰色 #8E8E93 不是 #8A8A8A
6. **P2 章节首页**：黑色 bar 厚度、Arial Black 字体、CH.XX 标签字号
7. **P2 警告框**：加 ▲ 图标

## 验收标准（这一轮）

1. 字体匹配：用 extract_spans.py 重新抽取，winner 字体清单 ≈ target（MicrosoftYaHei + Arial Black + Courier New 三家都在）
2. 字号匹配：winner 主字号 ≈ 7.0-7.5pt（不是 8.0）
3. 封面"威富可"黑色（不是红色），MODEL 红色
4. 表格 drawings 数 ≥ TARGET 的 80%（不再缺 46 个 drawings）
5. **目测**：打开 winner 和 target 第一眼觉得"是同一份手册"（这是主观但重要的标准）

## 4 路分工

- **A1**：用 docx skill 严格流程 unpack/edit XML，精确改 `word/document.xml` 的字体、字号、颜色
- **A2**：用 python-docx 重建，从 build_docx.py iter-05 继续优化，重点修字体（python-docx 设字体需用 `rFonts.set_eastAsia`）
- **B1**：在 `swiss/tools/export-docx.js` 主版本继续改（codex 上次已经修过一波），这次重点：字体 + 字号 + 封面颜色 + 表格 zebra
- **B2**：在 `build_b2_docx.py` 继续优化，重点修字体（OxmlElement 设 `w:rFonts`）+ 表格细节

## 共同要求

- 在 `design-iter-01/<slot>/iter-NN/` 留产物
- 每轮跑 `score_candidate.py` 验自动指标 + `extract_spans.py` 验字体/字号
- 关键：**生成 side-by-side 后让 Claude/Codex 看图自评**（不只看数值）
- 不达"美感接近"不停下来

