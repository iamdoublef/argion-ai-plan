---
name: swiss-manual-a5
description: Swiss 项目级 skill：用于 Swiss 系列说明书的 A5 母版、JSON 单源、双轨交付、翻译工作簿和 PDF/DOCX 验收。
---

# Swiss A5 说明书 Skill

当任务涉及 `research/yjs-manual-opt/swiss/` 下的说明书模板、共享母版、A5 booklet、PDF、DOCX、V23、IMT050、排版、审校、保修卡、共享 CSS、翻译工作簿、本地化时，先读本文件。

## 先读哪些文件

1. `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md`
2. `research/yjs-manual-opt/swiss/SOP-new-product.md`
3. 当前产品数据：
   - `research/yjs-manual-opt/swiss/products/<product>/product.json`
   - `research/yjs-manual-opt/swiss/products/<product>/images.json`
   - `research/yjs-manual-opt/swiss/products/<product>/content/source/manifest.json`
   - `research/yjs-manual-opt/swiss/products/<product>/content/source/chapters/*.json`
   - `research/yjs-manual-opt/swiss/products/<product>/i18n/compiled/<locale>.json`
4. 当前翻译工作簿（如涉及翻译审核）：
   - `research/yjs-manual-opt/swiss/products/<product>/i18n/workbooks/<locale>.xlsx`
5. 当前模板与共享样式：
   - `research/yjs-manual-opt/swiss/template/*-master-*.html`
   - `research/yjs-manual-opt/swiss/template/shared/base/*.css`
   - `research/yjs-manual-opt/swiss/template/shared/base/brand-themes.json`
6. 构建与输出工具：
   - `research/yjs-manual-opt/swiss/tools/build-variant.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf-batch.js`
   - `research/yjs-manual-opt/swiss/tools/export-docx.js`
   - `research/yjs-manual-opt/swiss/tools/export-translation-workbook.js`
   - `research/yjs-manual-opt/swiss/tools/compile-translation-workbook.js`
   - `research/yjs-manual-opt/swiss/tools/_audit-visual.js`

## 当前正式输入契约

Swiss 当前正式结构源固定为：

- `products/<product>/product.json`
- `products/<product>/images.json`
- `products/<product>/content/source/manifest.json`
- `products/<product>/content/source/chapters/*.json`

Swiss 当前正式译文源固定为：

- `products/<product>/i18n/compiled/<locale>.json`

翻译人员的正式编辑面固定为：

- `products/<product>/i18n/workbooks/<locale>.xlsx`

不再把下面这些视为正式接口：

- `config.json`
- `content.<lang>.json`
- `CONTENT_BODY`
- 模板内写死正文
- 运行时逐字简转繁

## 当前正式输出

### 自有品牌线

- `HTML + PDF`

使用场景：

- 官网/商城内容
- 自有品牌包装内页
- 内部审稿与发布

### ODM 线

- `DOCX + PDF`

使用场景：

- 客户拿可编辑 Word/WPS 文件做二次风格化
- `PDF` 作为审稿稿和参考稿

## 硬规则

- 页面标准固定为 `A5 portrait 148mm x 210mm`
- Swiss 统一走 `shared base + shared CSS + thin shell template + brand theme`
- 产品差异只允许落在 JSON 数据、译文 catalog 和产品图片目录，不允许复制整页模板
- 模板只承载共享样式、品牌壳层和挂载点，不承载正文事实内容
- 自有品牌正式交付 `HTML + PDF`
- ODM 正式交付 `DOCX + PDF`
- 中文 DOCX 正式基线固定为：
  - `research/yjs-manual-opt/swiss/template/shared/docx/base-template-cn.docx`
  - `research/yjs-manual-opt/swiss/WORD-BASE-TEMPLATE-CN.md`
- `research/yjs-manual-opt/swiss/output/` 只保留少量中文基线样稿与代表稿；批量输出、审阅截图、缓存和 preview 一律视为可再生产物
- 翻译人员不改 HTML，不改 CSS，不改章节结构 JSON，只改译文工作簿
- `zh-HK` 和 `zh-TW` 必须是独立 locale catalog，不再用运行时逐字简转繁发布
- 模型不负责最终排版；模型只用于新产品草稿、翻译草稿、本地化和审计建议
- 长语种 `EN/DE/IT` 溢出时优先拆页、续页，不优先压缩
- 禁止按页序号做 `zoom` / `nth-of-type` 打印补丁
- 安全图标必须独立成块，不能融入正文
- 步骤编号、按钮名、控制面板图、结构图、保修卡必须不变形、不裁切、不横向顶出
- 保修卡允许独立续页，优先完整可见
- `PDF hotfix` 只允许作为应急出口；下一版必须回写 JSON/catelog/workbook，不能形成双轨版本

## 正式 block 类型

正式内容 JSON 只允许以下 block：

- `paragraph`
- `bullet_list`
- `warning_box`
- `caution_box`
- `notice_box`
- `sub_title`
- `figure`
- `figure_row`
- `step_flow`
- `table_ref`
- `qa_list`
- `contact_block`
- `warranty_card`
- `split_panel`

`html_fragment` 不再允许进入正式内容；构建时一旦发现，直接视为错误。

## 译文与本地化规则

- 所有可翻译文本必须有稳定 `text_id`
- 结构与译文分离：结构在 `content/source`，译文在 `i18n/compiled`
- `i18n/workbooks/<locale>.xlsx` 只是译文编辑面，不是结构源
- 规范资产优先来自：
  - `research/yjs-manual-opt/swiss/standards/brand-language-guide.md`
  - `research/yjs-manual-opt/swiss/standards/terminology-glossary.json`
  - `research/yjs-manual-opt/swiss/standards/unit-and-measurement-policy.md`
  - `research/yjs-manual-opt/swiss/standards/locale-guides.json`
  - `research/yjs-manual-opt/swiss/standards/warning-language-policy.md`
  - `research/yjs-manual-opt/swiss/standards/ai-new-product-structure-prompt.md`
  - `research/yjs-manual-opt/swiss/standards/ai-translation-draft-prompt.md`
  - `research/yjs-manual-opt/swiss/standards/ai-localization-audit-prompt.md`

## 标准流程

1. 先读 `DESIGN-STANDARD.md`
2. 再读产品结构源、译文 catalog、品牌主题和相关模板
3. 如涉及翻译审核，先导出或读取 `i18n/workbooks/<locale>.xlsx`
4. 构建 `HTML`
5. 导出 `PDF`
6. 如涉及 ODM，额外导出 `DOCX`
7. 运行 `_audit-visual.js`
8. 抽检真实 PDF；ODM 任务额外确认 DOCX 可打开、图文完整
9. 关键页通过后才算完成

## 必读验收页

- 封面
- 目录页
- 安全须知第一页
- 结构页 / 控制面板页
- 操作页
- 最后一页保修页
- 保修卡续页

## 验收口径

- 先过结构：目录、章节、页眉页脚、页码、续页逻辑
- 再过视觉：无 overflow、无图片失真、无横向裁切、无图标融字
- 再过本地化：术语、单位、品牌称呼、警示语符合规范资产
- 最后过真实 PDF；ODM 任务再核 DOCX 可编辑性

## 已知边界

- `HK/TW` 已切到独立 locale catalog，但当前种子译文仍需人工审核
- `ZA` 继续复用 `en` catalog
- 模型生成 Word 样式优化可以实验，但不进入正式主链
- 未来若某个 ODM 客户需要极特殊版式，再做客户级 Word 模板，不把客户差异写回通用母版

## 2026-03 Word 支线补充规则

- `DOCX` 为独立的 A5 可编辑支线，不再按“PDF 影子稿”导出。
- `HTML/PDF` 与 `DOCX` 共用同一份 JSON 内容源和译文 catalog，但排版引擎完全分开。
- `DOCX` 采用单一 Word 母版骨架 + 品牌主题包；不允许按产品复制 Word 模板。
- `DOCX` 的目标是“可编辑且体面”，不是 1:1 还原 `PDF`。
- 中文 Word 输出默认复用 `base-template-cn.docx` 骨架，后续新产品只微调内容和图片，不重做风格。
- 若目标 `DOCX` 正被 WPS/Word 占用，导出器允许落旁路文件 `.__staged.docx`，待锁释放后再替换正式文件。
