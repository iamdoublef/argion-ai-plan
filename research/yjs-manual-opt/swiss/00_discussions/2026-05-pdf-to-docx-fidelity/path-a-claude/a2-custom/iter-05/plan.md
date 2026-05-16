# iter-05 plan

## 目标
- 让 figure 渲染同时考虑 max-height 和 page-width 约束（接近 HTML 行为）
- 抛光页 7（产品功能）的图片显示比例

## 任务
1. `_render_figure`：即使 JSON 指定了 max_height，也额外传入 max_width=usable*0.85，让 `_add_image_paragraph` 按 aspect ratio 选更紧的约束（HTML max-width:100% + max-height: Xmm 等效行为）。
2. 其他 figure branch (aspect>6 / aspect>2 / 一般) 也都加 max_width 约束。

## 预期
- 仍 15 页
- 页 7 控制面板图比例更接近目标（依然受 max_height=30mm 限制，但只要 image natural aspect 让宽度也能用满，会显得更大）
