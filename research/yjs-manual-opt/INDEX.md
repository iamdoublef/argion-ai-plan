# yjs-manual-opt — 说明书优化研究

## 项目概述

研究亚俊氏真空设备产品说明书的优化方向，提升用户体验和品牌专业度。

## 目录结构

```
research/yjs-manual-opt/
  INDEX.md                          ← 本文件
  research-log.md                   ← 研究过程日志
  _inbox/                           ← 原始说明书 docx（只读输入）
  data/                             ← 研究数据（需求画像、诊断、问题清单、规范）
  images_v23/                       ← V23 产品线稿图（18张 PNG，HTML 引用源）
  images_imt050/                    ← IMT050 产品线稿图（14张 PNG）
  source/                           ← 中间产物（提取文本、base64、缩略图、修正版 docx）
  output/                           ← 最终交付物（HTML + PDF + 生成脚本）
    v23-manual-cn.html              ← 中文版完整说明书（17页）
    v23-manual-en.html              ← 英文版完整说明书（17页，仅美标）
    V23-Manual-CN-Wevac.pdf         ← 中文 PDF
    V23-Manual-EN-Wevac.pdf         ← 英文 PDF
    generate-pdf.js                 ← Playwright PDF 生成脚本
    images_v23/                     ← 图片副本（HTML 相对路径引用）
```

## 阶段索引

### 2026-02-25 阶段0完成：目录初始化 + 需求画像确认
commit: uncommitted
- ptr: `file:research/yjs-manual-opt/data/d0-research-brief.md`
- ptr: `file:research/yjs-manual-opt/research-log.md`

### 2026-02-25 阶段3完成：说明书编写规范（对标小米）
commit: uncommitted
- ptr: `file:research/yjs-manual-opt/data/d5-manual-standard.md`

### 2026-02-25 阶段2完成：全量问题清单（19个问题，含排版+内容）
commit: uncommitted
- ptr: `file:research/yjs-manual-opt/data/d4-full-issue-list.md`

### 2026-02-25 阶段1完成：现状诊断 + AI流程方案初稿
commit: uncommitted
核心结论：图片是难点（AI无法生成技术线稿），文字层AI可全覆盖；建议数据/模板/输出三层分离
- ptr: `file:research/yjs-manual-opt/data/d1-current-state.md`
- ptr: `file:research/yjs-manual-opt/data/d2-ai-flow-proposal.md`
- ptr: `file:research/yjs-manual-opt/images_v23/` （V23图片库，18张PNG）
- ptr: `file:research/yjs-manual-opt/images_imt050/` （IMT050图片库，14张PNG）

### 2026-02-26 V23 小米风格 HTML 说明书完成（中英双版本 + PDF）
commit: uncommitted
修复C05（Pulse Vac "手动密封"→"手动抽气"）、C01（补充NOTICE级别）；补全第7-10章；创建英文版（仅美标）；Playwright生成PDF。目录整理：source/中间产物、output/交付物。
- ptr: `file:research/yjs-manual-opt/output/v23-manual-cn.html`
- ptr: `file:research/yjs-manual-opt/output/v23-manual-en.html`
- ptr: `file:research/yjs-manual-opt/output/V23-Manual-CN-Wevac.pdf`
- ptr: `file:research/yjs-manual-opt/output/V23-Manual-EN-Wevac.pdf`
- ptr: `file:research/yjs-manual-opt/source/product-config.json`
