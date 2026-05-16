# design-iter-01 美感专项进度

> 大 boss 否定第 1 大轮（自动验收 PASS 但美感差），进入第 2 大轮专项修复。

## 当前 winner

`design-iter-01/path-claude-main/iter-02/output.docx`（视觉差 14.14，15 页）
也已 stage 到 `final/imt050-wevac-eu-cn.docx`。

## 修了什么（vs 第 1 大轮 winner）

### P0 字体修复（B1 codex 上一轮 +  我 + B1 codex v2 三方合力）
- `cjkFont: 'Microsoft YaHei'`（原 '宋体' → LibreOffice fallback 到 SimSun）
- `titleLatinFont: 'Arial Black'`（PDF 大标题用 Arial-Black）
- `monoFont: 'Courier New'`（新增，章节号 + MODEL 用）
- 实测验证：新版 PDF 内字体 = `MicrosoftYaHei / MicrosoftYaHei-Bold / Arial-Black / CourierNewPSMT / CourierNewPS-BoldMT / ArialMT` ✅ 与 target PDF 完全一致

### P0 封面颜色错位修复
- "威富可" 改 **黑色**（之前是红色）
- "MODEL IMT050" 保持红色 + Courier New 等宽
- 左上 "━━━ 威富可" inline 布局（短红线 + 黑字小标）
- 产品图缩小 + 居中偏下
- disclaimer 强制两行 + 顶部黑色 hairline

### P0 字号下调
- bodySize: 16 → 14（7pt 对齐 PDF）
- smallSize: 13 → 10
- coverProductSize 24 → 36（"制冰机" 大字）
- chapterNumberSize: 24 → 27（PDF Arial Black 13.5pt）

### P1 灰色色值精修
- light/muted/headerText/footerText: `#8A8A8A` → `#8E8E93`（PDF 实测）

### P1 表格 zebra striping
- `zebraShading` 现在返回 `#F4F4F4` 偶数行底
- 黑底白字表头 ✓

### P2 警告图标
- WARNING / CAUTION / NOTICE 框前加 `▲` 红色三角警告 ✓

## 逐页美感评估（vs PDF target）

| 页 | 内容 | 匹配度 | 备注 |
|---|---|---|---|
| 1 | 封面 | **95%** ✓ | 左上"━━━ 威富可"、产品图、MODEL 红、制冰机大字、底部 disclaimer 两行 + accent 线 — 几乎 1:1 |
| 2 | 目录 TOC | **99%** ✓ | 10 章红编号 + 加粗 + 灰页码，几乎完美 |
| 3 | 01 安全须知 | **95%** ✓ | "▲ 警告 WARNING" + 24 bullets，警告图标 ✓ |
| 4 | 01 续 | 90% | CAUTION / NOTICE 框 |
| 5 | 02 产品及使用提示 | 92% | sub_title + bullets |
| 6 | 03 产品结构 | **95%** ✓ | 产品爆炸图 + 1-10 编号 + 表格 (zebra) |
| 7 | 04 产品功能 | 90% | 按钮表 |
| 8 | 05 技术参数 | **99%** ✓ | 黑底表头 + 16 行规格表 |
| 9 | 06 操作指引 | **70%** ✗ | **step_flow 用了大红色列** vs PDF 小黑徽章 — 主要差距 |
| 10 | 06 续 | 70% | 同上 |
| 11 | 07 故障排除 | **95%** ✓ | 故障表 + ▲ DISCLAIMER |
| 12 | 08 维护保养 | 90% | step + figure_row |
| 13 | 09 安装运输 | 92% | bullets |
| 14 | 10 品牌与保修 | 90% | 品牌信息表（**缺"项目\|信息"表头**） |
| 15 | 10 续 保修卡 | 92% | 9 字段保修卡 |

**整体美感匹配度：~92%**

## 剩余差距

1. **Page 9-10 step_flow**：当前实现是 docx-js Table 每行左侧红色 cell（占整行高），PDF 是 13.5pt × 13.5pt 黑色小方块徽章 + 内联文字。
   - 修复方案 A：把 number cell verticalAlign 改 TOP + shading 改黑色 + margins 缩小，让小方块"贴顶"
   - 修复方案 B：放弃表格，用 unicode `❶❷❸` 圆圈数字或 inline shading TextRun
   - 待 Codex 完成后处理
2. **Page 14 品牌信息表缺表头**："项目|信息" 表头被 brand_info renderInfoTable 跳过了
   - 修复：renderBrandInfoTable / renderManufacturerTable 加表头行

## 工具沉淀

- `extract_spans.py`：抽取 PDF 每页每个 text span 的 (x,y,w,h,font,size,color,text) + drawings + images
- `diff_spans.py`：逐页对比 target vs candidate
- `design_diff_report.md`：当前差异详细数据
- `target_spans.json` / `winner_spans.json` / `iter-02 spans.json`：原始数据

## Codex 进展

Codex B1 v2 在背景跑（log 866KB+，仍在迭代），已做 iter-01..04，正在调封面间距 + headerSize。
- iter-01: 14.23 (15 pages)
- iter-02: 14.14 (15 pages) ← **当前 winner**
- iter-03: 16.04 (16 pages) — 退化
- iter-04: 15.13 (16 pages) — 退化

我的手动 iter-02 等于 codex iter-02。Codex 后续 iter 退化（多页）。

## 下一步

1. 等 codex 完成（最多再 30 分钟）
2. 修 step_flow（黑色小徽章 + TOP align）
3. 修 brand_info / manufacturer_info 表头
4. 重新生成 + 评分 + 视觉验证
5. Stage 最终 winner 到 final/
6. push 到 git
