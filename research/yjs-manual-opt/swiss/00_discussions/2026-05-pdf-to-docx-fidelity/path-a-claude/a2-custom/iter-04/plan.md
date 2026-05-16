# iter-04 plan

## 目标
- 抛光视觉细节：警告图标 / 表格交替行底色 / 修步骤图被裁切

## 任务
1. `_render_box` 在标题旁渲染 `block.icon`（warning_icon = safety.warning_icon → image3.png）
2. `_render_warranty_card` / `_render_specs_table` / `_render_inline_table` 加偶数行底色
3. `_add_image_row` 按 aspect ratio 选 width/height（修 page 9 "FULL BUSKET" 被裁切）

## 预期
- 仍 15 页（视觉细节不应改变页数）
- 视觉 → 95% 接近目标
- 这版作为最终交付
