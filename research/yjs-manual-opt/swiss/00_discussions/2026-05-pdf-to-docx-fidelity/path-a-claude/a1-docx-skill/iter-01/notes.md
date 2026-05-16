# iter-01 notes — 紧凑化 + 静态 TOC + 修封面（结果：15 页！）

## TL;DR

**所有四个核心验收标准全部达成**：

| 项 | 目标 | iter-01 实际 |
|---|---|---|
| DOCX→PDF 页数 | ≤16，理想 15 | **15** |
| 静态 TOC（不靠 Word 字段） | 必须 | ✓ 三列表格 + 红色章节号 + 灰色页码 |
| 文本可编辑（普通 w:t 不是 wp:txbx） | 必须 | ✓ 319 个 `<w:t>`，0 个 textbox |
| 视觉相似度 | 主要元素对齐 | ✓ 封面、目录、章节、警告框、表格、步骤号都对得上 |

## 改了什么（相对 swiss/tools/export-docx.js）

1. **DOCX_PROFILE 全面瘦身**：
   - bodySize 22 → 18, sectionTitleSize 26 → 22, chapterNumberSize 36 → 30, coverBrandSize 36 → 22, tocTitleSize 30 → 28, smallSize 17 → 14
   - cover 图：360×255 → 220×165（贴近 PDF 视觉比例）
   - 整体减少图片尺寸
2. **CELL_MARGINS 紧凑化**：
   - 默认 70/70/90/90 → 40/40/80/80
   - compact 40/40/70/70 → 25/25/60/60
3. **行距**：
   - body line 320 → 260
   - default 段后 120 → 60
   - 段后 50 → 0（alert box bullet 间距）
4. **静态 TOC 表格**（核心修复 #1）：新增 `buildStaticTocTable` 函数，三列（编号 / 标题 / 页码），用预映射的 PDF 页码（01→3, 02→5, …, 10→14），不再用 `new TableOfContents()`
5. **shouldPageBreakBeforePage 收紧**：只在 force_page_break 或显式 (续)/continued 时触发；移除 warranty / appendix 自动分页
6. **renderChapterHeading 简化**：删除独占行的右对齐 header_ref 段（页眉已经有了），spacing 紧凑
7. **buildCoverBlock 重写**：删除大字距、用红色短 — 模拟 accent，"威富可" 22 半点（PDF 看起来约 11pt 粗），cover 图缩小到 220，加红色 MODEL IMT050 + 大字制冰机 + 灰字说明书 + 红色粗 18 size 分隔线 + 底部黑色细 6 size + 中文 disclaimer 两行
8. **renderAlertBox / renderBulletList 紧凑化**：bullet 间距 50 → 0/20，box 内 padding 120 → 70
9. **Heading 样式 (Heading1/2/3)**：spacing 前后大幅减少，line 改为 260
10. **headings 默认 paragraph spacing**：default 文档级 paragraph spacing `{line:260, before:0, after:60}`

## 视觉对比逐页（A1-01 与 target）

| 页 | target 内容 | A1-01 内容 | 评价 |
|---|---|---|---|
| 1 | 封面 | 封面 | ✓ 完全对得上 |
| 2 | 目录 | 目录 | ✓ 静态表格还原，序号红色 |
| 3 | 01 安全须知 (WARNING 24 bullet) | 同 | ✓ 标题位置同；24 bullet 装下（box 紧贴底边） |
| 4 | 01 安全须知（续）CAUTION+NOTICE | 同 | ✓ |
| 5 | 02 产品及使用提示 | 同 | ✓ 三个分组 H3 |
| 6 | 03 产品结构 (图+表) | 同 | ✓ |
| 7 | 04 产品功能 (图+表) | 同 | ✓ |
| 8 | 05 技术参数 (表) | 同 | ✓ |
| 9 | 06 操作指引 (步骤号) | 同 | ✓ 红色 step number cell |
| 10 | 06 操作指引（续）| 同 | ✓ |
| 11 | 07 故障排除 (表+免责) | 同 | ✓ |
| 12 | 08 维护保养 | 同 | ✓ |
| 13 | 09 安装运输等 | 同 | ✓ |
| 14 | 10 品牌与保修信息 | 同 | ✓ |
| 15 | 10 品牌与保修（续 — 保修卡）| 同 | ✓ |

## 已知小差距（留给 iter-02 优化）

A. **页眉右侧 chapter ref 被裁切**（"CH.01 — SAF" 而非 "CH.01 — SAFETY"）
   - 原因：tabStop 到 MAX 位置但 SAFETY 末几字超出 A5 右边距
   - 修：在页面 margin 内显式给 tabStop 位置 (CONTENT_W - small) 或换更短的 ref 字串

B. **章节左侧色块**：iter-01 是黑色细 bar (chapterBar='000000')，PDF 是红色厚块
   - 修：theme.chapterBar = accent，size 12 → 24

C. **第 3 页警告框溢出**：24 bullet 把 box 撑得贴底边，部分 bullet 间距非常紧
   - 修：本页可以让正文段 (Warning 前的"为了您的安全…")字号略小，或干脆把 box border padding 再压

D. **封面产品图位置**：iter-01 是左上偏左，target 是中上方略居中
   - 修：cover 图给 alignment.CENTER 或加 paragraph indent

E. **DOCX 整体 558KB**（PDF 是 ~200KB 等价 docx 可能更轻）— 不是必修

## 是否需要 iter-02？

iter-01 已达到 BRIEF 的全部硬性验收。差距 A-D 是"锦上添花"，不是阻塞验收。

我倾向 **跑一轮 iter-02** 修 A 和 B（特别是 chapterBar 红色块，这是品牌识别关键），再写最终报告。
