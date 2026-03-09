---
name: swiss-manual-a5
description: Swiss 项目级 skill：用于 V23、IMT050 等 Swiss 系列说明书的 A5 小开本共享母版编写、重构、审校与 PDF 验收。适用于 shared base/shared CSS/product partial、booklet、目录/章节/保修卡、多语言长文本分页，以及真实 PDF 渲染核验。
---

# Swiss A5 说明书 Skill

当任务涉及 `research/yjs-manual-opt/swiss/` 下的说明书模板、共享母版、PDF 导出、booklet、对齐审校、`V23`、`IMT050` 时，先读本文件。

## 先读哪些文件

1. `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md`
2. `research/yjs-manual-opt/swiss/SOP-new-product.md`
3. 当前任务对应模板：
   - `research/yjs-manual-opt/swiss/template/*.html`
   - `research/yjs-manual-opt/swiss/template/shared/base/*.css`
4. 审校/导出相关工具：
   - `research/yjs-manual-opt/swiss/tools/build-variant.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf.js`
   - `research/yjs-manual-opt/swiss/tools/export-pdf-batch.js`
   - `research/yjs-manual-opt/swiss/tools/_audit-visual.js`

## Agent 路由

- 生成、重构、修复 Swiss 模板：使用 `.claude/agents/swiss-manual-writer.md`
- 审计、对齐、比较、PDF 核验：使用 `.claude/agents/swiss-content-auditor.md`
- 不要把 `.claude/agents/manual-writer.md` / `.claude/agents/manual-auditor.md` 当作 Swiss 当前标准；那两份只保留旧 A4 链路

## 硬规则

- 页面标准固定为 `A5 portrait 148mm x 210mm`
- Swiss 产品统一走 `shared base + shared CSS + product partial`，不允许再各做一套整页模板去手工模仿
- 可读性优先，允许页数增加；不允许靠全局压字号、压表格、压保修卡来控页数
- 长语种 `EN/DE/IT` 在 A5 下溢出时，优先拆页或续页，不优先压缩
- 禁止按页序号做 `zoom`、`nth-of-type` 打印补丁
- 安全须知图标必须独立成块，不能融入首行文字
- 步骤编号、按钮名、控制面板图、结构图、保修卡必须保证不变形、不裁切、不横向顶出
- 保修卡允许独立续页，优先完整可见
- 同一公司说明书优先统一视觉系统：字体体系、目录结构、章节标题、页眉页脚、表格、警示框、保修页结构
- 不要求不同产品或不同语言强行同页数；要求的是同一套 A5 品牌系统

## 标准流程

1. 先读 `DESIGN-STANDARD.md`，确认当前 A5 设计口径
2. 再选 writer 或 auditor agent
3. 构建 HTML
4. 导出 PDF
5. 运行 `_audit-visual.js`
6. 抽检真实 PDF 渲染图，不只看 HTML/DOM
7. 关键页通过后才算完成

## 必查关键页

- 封面
- 目录页
- 安全须知第一页
- 产品功能/控制面板页
- 操作页
- 最后一页保修页
- 保修卡续页

## 验收口径

- 先过结构：共享母版、目录、章节、页眉页脚、页码、续页逻辑
- 再过视觉：无 overflow、无图片失真、无横向裁切、无图标融字
- 最后过真实 PDF：关键页截图确认风格一致、信息完整、版式稳定

## 默认判断

- Swiss 当前标准以 `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md` 为准
- `V23` 是共享母版语言的参考基线，但不是要求所有产品强行做成相同页数
- 对齐判断以真实 PDF 渲染效果为准，不以单纯 DOM/源码“看起来像”作为完成标准
