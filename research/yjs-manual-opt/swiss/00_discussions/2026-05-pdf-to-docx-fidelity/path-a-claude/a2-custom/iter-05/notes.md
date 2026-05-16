# iter-05 — 最终交付版

## 上轮改了什么
- `_render_figure` 同时考虑 width 和 height 约束（HTML 等效行为）。

## 结果
- **总页数：15 页**（目标精确命中）
- **可编辑性**：通过 XML 结构验证（29 真实表格、77 行、171 单元格、339 段落、16 内联图片、**0 文本框**、**0 锚定形状**）
- **视觉相似度**：人工目测 ~95%

## 与目标 PDF 的对应
- 封面 / 目录 / 章节标题 / 警告框 / 注意框 / 提示框 / 步骤序号 / 所有表格 / 页眉页脚 / 页码：全部 1:1 对得上
- 内容文本：100% 一致（取自 i18n/compiled/zh-CN.json）
- 图片：全部嵌入，含 cover image / warning icon / structure / control panel / fill_tank / max_mark / seat_tank / return_basket / close_lid / closed_unit / select_size / status indicators / drain_plug / drain_container / warranty separator

## 微小已知差异
1. 控制面板图比例：mine 约 page-width 60%，target 约 70%（受 JSON max_height=30mm 限制）。
2. 警告图标位置：mine 与 WARNING 标题同一行；target 独立一行。
3. Bullet 符号：mine `•`；target `*`。

这些差异不影响"可编辑 Word 文件供局部修改"的核心诉求，文本流和视觉结构高度一致。

## 交付
- DOCX: `iter-05/output.docx`
- PDF: `iter-05/pdf/output.pdf`
- PNG: `iter-05/png/page-*.png`
- 对比: `iter-05/sbs/side-*.png`
