# iter-01 plan

## 目标
- 评估 pandoc baseline 离目标多远
- 选定最终路径

## 评估
- 跑 `pandoc HTML→DOCX` 看 baseline 离目标多远（→ baseline.docx，16 页）
- 直接 inspect：
  - 文本可编辑性 ✓（pandoc 给的是真实段落）
  - 视觉：A4 默认页，所有 CSS 样式丢失，无 header/footer，无章节标题样式，TOC 平铺 ✗
- 决策：pandoc baseline 不够，**改用 python-docx 直接从 JSON 构建**，全权控制 OOXML。

## 实施
- 写 `build_docx.py`（约 700 行）
- 支持的 block types: paragraph / sub_title / bullet_list / warning_box / caution_box / notice_box / step_flow / figure / figure_row / table_ref / warranty_card
- 支持的命名表格: specs / parts / buttons / brand_info / manufacturer_info
- 支持的 inline markdown: `**bold**`、`\n` line break
- 支持的变量: `{{brand.display_name}}` / `{{brand.support_email}}` / `{{warranty.years}}` / `{{localized.product_name}}`

## 预期效果
首版预计 18-22 页，视觉接近 60-70%，之后迭代调整 spacing 与 layout 直至 ≤16 页。
