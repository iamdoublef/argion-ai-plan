# research-log — 说明书优化研究

## 研究目标

- 输入：亚俊氏真空设备产品说明书现状 + 竞品说明书标准
- 输出：优化方案报告（给管理者看）
- 为什么：品牌专业度提升 + 出海多语言 + 用户体验 + AI辅助生产

## 执行过程

### 2026-02-25 阶段0 — 初始化

- ✅ 建立 `research/yjs-manual-opt/` 目录结构
- ✅ 创建 `INDEX.md`
- ✅ 完成需求画像 `data/d0-research-brief.md`（用户确认）
- 工具：Write工具直接创建文件

## 关键决策

- 产出形式：优化方案报告（非模板、非SOP）
- 优先英文/出海版本，暂不做中文版
- 核心产品：真空封口机类

## 失败与教训

（待记录）

### 2026-02-25 阶段1 — 现状诊断

- ✅ 读取两份说明书原文（V23真空封口机、IMT050制冰机）
- ✅ 提取图片至 `images_v23/`、`images_imt050/` 目录
- ✅ 用subagent分析图片内容（线稿类型、质量、用途）
- ✅ 完成现状诊断报告 `data/d1-current-state.md`
- ✅ 完成AI流程方案初稿 `data/d2-ai-flow-proposal.md`
- 工具：zipfile提取docx内容、XML解析文字、subagent读图

**关键发现**：
- 图片是专业矢量线稿，AI无法替代，需建库复用
- 文字层AI可全覆盖（生成/翻译/多品牌变体）
- 当前文档存在多品牌混用、字段未填、安全标准不统一三个问题

**待确认（影响后续方案深度）**：
1. 新产品出图流程
2. 英文版现状
3. 每年SKU数量
4. 目标市场合规要求

## 后续待办

1. 大boss确认待确认事项后，深化方案
2. 可选：做一个prompt模板demo，验证AI生成内容质量
3. 可选：做一个python-docx脚本demo，验证自动化输出可行性

## 2026-03-01 MI 2.0 导出故障复盘
- 现象：`v23-mi-2.0-full-fixed.pdf` 出现图片缺失，部分页眉异常。
- 根因：
  - 图片路径误写为 `../output/images_v23/...`（应为 `../../output/images_v23/...`）。
  - HTML 存在损坏闭合标签（`?/li>`、`?/div>` 等）导致结构与分页异常。
- 修复：
  - 重建 `v23-mi-2.0-full.html`，保留 MI 风格并接入已验证正文结构。
  - 重导出 `v23-mi-2.0-full-fixed.pdf`，再生成 `v23-mi-2.0-full-fixed-booklet-A4.pdf`。
- 沉淀：
  - d5 增加导出链路门禁（路径、编码、结构、Playwright 预检、PDF 判定、booklet 联动）。
  - manual-auditor/manual-writer 同步新增必查项与开发约束。

## 2026-03-01 PDF Missing-Image Follow-up (SVG 0x0)
- User report: operation pages still missed images and some headers.
- Root cause confirmed:
  - Image assets were loadable (`naturalWidth>0`).
  - In `flex + print` layout, multiple SVG `<img>` nodes with only `max-width/max-height` rendered as `0x0`.
- Fix applied:
  - Updated 5 HTML files (`v23-manual-cn/en`, `v23-mi-2.0-full`, `v23-lifestyle-complete`, `v23-swiss-complete`) to explicit `width + height:auto` styles for affected SVG images.
  - Re-exported CN/EN PDFs and all 3 experiment PDFs.
  - Re-generated all booklet PDFs via `make-booklet.py`.
- Regression results:
  - Playwright render check: all 5 HTML files `zero_render=0`.
  - Visual page checks passed: MI pages 8/9/10/11, CN page 8, EN page 8 show both headers and images.
