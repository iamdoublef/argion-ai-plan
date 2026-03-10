---
name: swiss-manual-a5
description: Swiss 项目级 skill：用于 V23、IMT050 等 Swiss 系列说明书的 A5 共享母版编写、重构、审校与 PDF 验收。
---

# Swiss A5 说明书 Skill

当任务涉及 `research/yjs-manual-opt/swiss/` 下的说明书模板、共享母版、A5 booklet、PDF 导出、`V23`、`IMT050`、排版、审校、保修卡、共享 CSS 时，先读本文件。

## 先读哪些文件

1. `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md`
2. `research/yjs-manual-opt/swiss/SOP-new-product.md`
3. 当前任务对应模板：
   - `research/yjs-manual-opt/swiss/template/*.html`
   - `research/yjs-manual-opt/swiss/template/shared/base/*.css`
4. 构建与审计工具：
   - `research/yjs-manual-opt/swiss/tools/build-variant.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf-batch.js`
   - `research/yjs-manual-opt/swiss/tools/_audit-visual.js`

## 当前正式输入契约

Swiss 现有产品只认下面 4 类正式输入：

- `products/<product>/product.json`
- `products/<product>/images.json`
- `products/<product>/content/<lang>/manifest.json`
- `products/<product>/content/<lang>/chapters/*.json`

不再把下面这些视为正式接口：

- `config.json`
- `content.<lang>.json`
- `CONTENT_BODY`
- 模板内写死正文

## Agent 路由

- 生成、重构、修复 Swiss 模板：`.claude/agents/swiss-manual-writer.md`
- 审计、对齐、比较、PDF 核验：`.claude/agents/swiss-content-auditor.md`
- 不要把 `.claude/agents/manual-writer.md` / `.claude/agents/manual-auditor.md` 当作 Swiss 当前标准；那两份只保留旧 A4 链路参考。

## 硬规则

- 页面标准固定为 `A5 portrait 148mm x 210mm`
- Swiss 统一走 `shared base + shared CSS + thin shell template`
- 产品差异只允许落在 JSON 数据和产品图片目录，不允许再复制整页模板或把正文写回模板
- 正式输出主链只有 `HTML + PDF`
- booklet 仅作兼容性附加产物，不再是硬验收项
- 可读性优先，允许页数增加；不允许靠全局压字号、压表格、压保修卡来控页数
- 长语种 `EN/DE/IT` 溢出时，优先拆页/续页，不优先压缩
- 禁止按页序号做 `zoom` / `nth-of-type` 打印补丁
- 安全须知图标必须独立成块，不能融入首行文字
- 步骤编号、按钮名、控制面板图、结构图、保修卡必须保证不变形、不裁切、不横向顶出
- 保修卡允许独立续页，优先完整可见
- 文本字段只允许轻量 token：
  - `**粗体**`
  - `[btn:按钮名]`
  - `\n` 换行
- 文本字段禁止内嵌原始 HTML
- PDF 可作为审稿和应急 hotfix 出口，但下一版必须回写 JSON，不能形成双轨版本
- 本轮不做 Excel 主源、不做 DOCX 主链、不做 AI 生产导入

## 正式 block 类型

正式内容 JSON 只允许这些 block：

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

`html_fragment` 不再允许进入正式内容；构建时一旦出现，直接视为错误。

## 标准流程

1. 先读 `DESIGN-STANDARD.md`，确认当前 A5 版式口径
2. 读 `product.json / images.json / manifest.json / chapters/*.json`
3. 构建 HTML
4. 导出 PDF
5. 运行 `_audit-visual.js`
6. 抽检真实 PDF 渲染图，不只看 HTML/DOM
7. 关键页通过后才算完成

## 必查关键页

- 封面
- 目录页
- 安全须知第一页
- 结构页 / 控制面板页
- 操作页
- 最后一页保修页
- 保修卡续页

## 验收口径

- 先过结构：共享母版、目录、章节、页眉页脚、页码、续页逻辑
- 再过视觉：无 overflow、无图片失真、无横向裁切、无图标融字
- 最后过真实 PDF：关键信息完整、风格统一、步骤与图片对应准确

## 已知边界

- `HK/TW` 继续基于 `CN` 内容派生
- `ZA` 继续基于 `EN` 内容派生
- 本轮优先把现有产品线收口为 JSON 单源；AI 新产品导入放到下一包
