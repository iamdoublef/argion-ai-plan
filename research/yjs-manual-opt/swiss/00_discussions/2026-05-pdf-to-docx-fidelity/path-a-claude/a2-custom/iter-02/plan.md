# iter-02 plan

## 目标
- 修 iter-01 的 P0 阻塞问题：caution_box 乱码 / 总页数 21 / 封面 disclaimer overflow

## 任务
1. `_render_box` 改优先用 `text_id` 查 strings（解决 GBK-as-UTF8 乱码）
2. Parts 表改列优先（1+5, 2+6, 3+7, 4+空）
3. 封面 disclaimer 移到 cover section FOOTER（强制留在第 1 页）
4. 页码起算：TOC pgNumType.start=2，chapter sections 连续
5. 全面紧凑化：section title 18/15→15/13pt；bullet 1.35→1.25；表格 cell margin 40→30；步骤 5.5→5mm

## 预期
- 16 页（cover + 15 内容）
- 视觉 → 80% 接近目标
