# iter-02 — 紧凑化 + 修正 P0 bug

## 上轮改了什么
1. **修 caution_box 乱码**：`_render_box` 改为优先用 `text_id` 从 strings 查，避免落到 JSON 中乱码 `block["text"]`。
2. **修 parts 表排序**：列优先（1+5, 2+6, 3+7, 4+空），匹配目标 PDF。
3. **修封面 overflow**：disclaimer 移到 cover section 的 FOOTER（不是 body），保证停留在第 1 页。
4. **修页码起算**：TOC 段 `pgNumType w:start=2`；章节段 `pgNumType` 去掉 start，让 PAGE field 连续递增。
5. **全面紧凑化**：
   - section title 18/15pt → 15/13pt，after 6→4pt
   - paragraph line-spacing 1.4→1.3，size 9.5→9
   - bullet_list line-spacing 1.35→1.25，size 9.5→8.7
   - box list size 8.7→8.3，line-spacing 1.3→1.22
   - step flow line-spacing 1.35→1.25，行高 5.5→5mm
   - 表格 cell margin top/bottom 40→30，row line-spacing 1.3→1.2

## 结果
- 总页数 **16 页**（cover + 15 内容页 = 目标）
- 视觉：
  - 封面 ★★★★★（与目标对得很齐）
  - 目录 ★★★★★
  - 章节标题、警告框、注意框、提示框 ★★★★★
  - 步骤序号 ★★★★★
  - 表格 ★★★★★
  - 操作步骤 4-6 + status indicators + NOTICE ★★★★
- 页码：cover 不显示, TOC=2, ch01p1=3, ..., warranty p2=15 ✓

## 残留问题（→ iter-03）
1. **变量 `{{warranty.years}}` 没替换**（页 14 第一条 bullet）→ 还没在 `_render_bullet_list` 调 `_substitute_vars`。
2. **`warranty.separator.primary` 太大**（页 15 整页只有剪刀图）→ 默认 max_height=40mm 太大，且没识别它是 wide aspect ratio。
3. 因为 separator 占了 page 15，warranty p2 推到 page 16 → 总 16 页

## 修复方向（iter-03）
- bullet_list 调用 `_substitute_vars`
- `_render_figure` 检查 aspect ratio：>6 视为分隔线，限制 max-height=5mm, max-width=85% page width
- `_add_image_paragraph` 支持同时指定 max_w 和 max_h，取约束更紧的
