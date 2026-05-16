# iter-03 plan

## 目标
- 修 iter-02 残留：变量未替换 / 分隔图过大占满第 15 页 / 总 16 页
- 把页数降到 15

## 任务
1. `_render_bullet_list` 调 `_substitute_vars`，解决 `{{warranty.years}}` 没替换
2. `_render_figure` 检查 aspect ratio：>6 视为分隔线，max_height=5mm + max_width=85%
3. `_add_image_paragraph` 支持 max_w + max_h 同时指定，按 aspect 选更紧的

## 预期
- 15 页
- 视觉 → 90% 接近目标
