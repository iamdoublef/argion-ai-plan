# yjs-manual-opt — 说明书优化研究

## 项目概述

研究亚俊氏真空设备产品说明书的优化方向，提升用户体验和品牌专业度。

## 目录结构

```
research/yjs-manual-opt/
  INDEX.md                          ← 本文件
  research-log.md                   ← 研究过程日志
  _inbox/                           ← 原始说明书 docx（只读输入）
  data/                             ← 研究数据 + 规范
    d0-research-brief.md            ← 需求画像
    d1-current-state.md             ← 现状诊断
    d2-ai-flow-proposal.md          ← AI流程方案
    d3-problem-list.md              ← 问题清单（初版）
    d4-full-issue-list.md           ← 全量问题清单（19个）
    d5-manual-standard.md           ← 编写规范 v2.0（唯一事实来源）
    audit-report.md                 ← 最新审计报告
  source/                           ← 原始素材 + 中间产物
    extracted_v23.txt               ← V23 原文文本
    extracted_imt050.txt            ← IMT050 原文文本
    product-config.json             ← 产品配置（品牌、参数、图片映射）
    V23-修正版-20260225.docx        ← 修正版 Word 源文件
    images_v23_raw/                 ← V23 原始提取图片（18张 PNG）
    images_imt050_raw/              ← IMT050 原始提取图片（14张 PNG）
  output/                           ← 最终交付物
    v23-manual-cn.html              ← 中文版说明书（17页）
    v23-manual-en.html              ← 英文版说明书（17页，仅美标）
    V23-Manual-CN-Wevac.pdf         ← 中文 PDF
    V23-Manual-EN-Wevac.pdf         ← 英文 PDF
    generate-pdf.js                 ← Playwright PDF 生成脚本
    images_v23/                     ← SVG 矢量图（HTML 引用，13张）
  experiments/                      ← 实验/POC（归档）
    2026-02-26_top-tier-styles/     ← 三种高端风格探索（lifestyle/mi-2.0/swiss）
```

## 阶段索引

### 2026-02-25 阶段0完成：目录初始化 + 需求画像确认
commit: 8c8da28
- ptr: `git:8c8da28:research/yjs-manual-opt/data/d0-research-brief.md`
- ptr: `git:8c8da28:research/yjs-manual-opt/research-log.md`

### 2026-02-25 阶段3完成：说明书编写规范（对标小米）
commit: 8c8da28
- ptr: `git:8c8da28:research/yjs-manual-opt/data/d5-manual-standard.md`

### 2026-02-25 阶段2完成：全量问题清单（19个问题，含排版+内容）
commit: 8c8da28
- ptr: `git:8c8da28:research/yjs-manual-opt/data/d4-full-issue-list.md`

### 2026-02-25 阶段1完成：现状诊断 + AI流程方案初稿
commit: 8c8da28
核心结论：图片是难点（AI无法生成技术线稿），文字层AI可全覆盖；建议数据/模板/输出三层分离
- ptr: `git:8c8da28:research/yjs-manual-opt/data/d1-current-state.md`
- ptr: `git:8c8da28:research/yjs-manual-opt/data/d2-ai-flow-proposal.md`
- ptr: `git:8c8da28:research/yjs-manual-opt/images_v23/` （V23图片库，18张PNG）
- ptr: `git:8c8da28:research/yjs-manual-opt/images_imt050/` （IMT050图片库，14张PNG）

### 2026-02-26 V23 小米风格 HTML 说明书完成（中英双版本 + PDF）
commit: uncommitted
修复C05（Pulse Vac "手动密封"→"手动抽气"）、C01（补充NOTICE级别）；补全第7-10章；创建英文版（仅美标）；Playwright生成PDF。目录整理：source/中间产物、output/交付物。
- ptr: `file:research/yjs-manual-opt/output/v23-manual-cn.html`
- ptr: `file:research/yjs-manual-opt/output/v23-manual-en.html`
- ptr: `file:research/yjs-manual-opt/output/V23-Manual-CN-Wevac.pdf`
- ptr: `file:research/yjs-manual-opt/output/V23-Manual-EN-Wevac.pdf`
- ptr: `file:research/yjs-manual-opt/source/product-config.json`

### 2026-02-26 V23说明书完整交付 + 说明书agent体系建立
commit: 8c8da28
审计发现图片全部错位（Word SVG/PNG双存储陷阱），MD5分析后从docx提取13张SVG替换。修复：CN版去除美标参数、字体改HarmonyOS Sans SC、边距统一12.7mm、打印CSS增强。审计评级C→A。新建manual-auditor（7维度含多语言一致性8子维度）和manual-writer（小米风格生成）两个agent。
- ptr: `git:8c8da28:research/yjs-manual-opt/output/v23-manual-cn.html`
- ptr: `git:8c8da28:research/yjs-manual-opt/output/v23-manual-en.html`
- ptr: `git:8c8da28:research/yjs-manual-opt/output/V23-Manual-CN-Wevac.pdf`
- ptr: `git:8c8da28:research/yjs-manual-opt/output/V23-Manual-EN-Wevac.pdf`
- ptr: `git:8c8da28:research/yjs-manual-opt/data/audit-report.md`
- ptr: `git:8c8da28:.claude/agents/manual-auditor.md`
- ptr: `git:8c8da28:.claude/agents/manual-writer.md`
- ptr: `git:8c8da28:research/yjs-manual-opt/source/product-config.json`

### 2026-02-26 规范重构：d5升级为唯一事实来源 + 审计修复3ERROR
commit: 0914fd3
第二轮审计评级B（3 ERROR + 9 WARNING）。修复：EN版补制造商表格、非标准警示框归入NOTICE、overflow/表头色/边框色。重构三文件关系：d5 v2.0整合CSS设计系统+HTML模板库+已知陷阱+检查清单，writer 472→78行、auditor 335→137行，均改为引用d5。
- ptr: `git:0914fd3:research/yjs-manual-opt/data/d5-manual-standard.md`
- ptr: `git:0914fd3:.claude/agents/manual-writer.md`
- ptr: `git:0914fd3:.claude/agents/manual-auditor.md`
- ptr: `git:0914fd3:research/yjs-manual-opt/data/audit-report.md`
