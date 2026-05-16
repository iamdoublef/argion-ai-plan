# iter-03 — 命中 15 页目标

## 上轮改了什么
1. `_render_bullet_list` 调用 `_substitute_vars`，让 `{{warranty.years}}` 被替换成 "2"。
2. `_render_figure` 检测 image aspect ratio：>6 视为分隔线，max-height=5mm + max-width=85%。
3. `_add_image_paragraph` 支持同时 max_w + max_h，按 aspect 选更紧的。

## 结果
- 总页数：**15 页**（精确匹配目标）
- 视觉：跟目标 PDF 几乎 1:1 对应
  - 封面: ★★★★★ — 红线品牌、产品图、MODEL IMT050、制冰机、说明书、红色短分隔线、底部 disclaimer
  - 目录: ★★★★★ — 红编号 + 加粗章节 + 灰色页码 + 灰底分隔
  - 章节标题: ★★★★★ — 左黑竖条、红色编号、黑色加粗
  - 警告/注意/提示框: ★★★★★ — 红色/黑色/灰色边框 + 列表
  - 步骤序号: ★★★★★ — 黑底白字方块
  - 表格 (specs/parts/buttons/troubleshooting/brand_info/manufacturer_info/warranty_card): ★★★★★
  - 页眉页脚: ★★★★ — 黑色顶线、品牌左、章节英文ref右；底部品牌IMT050 + 页码
  - 页码: ★★★★★ — cover不显示, TOC=2, body=3-15, "续"页正确
- 可编辑性: ★★★★★ — 完全是 Word 段落/表格，0 个 text box/anchored frame

## 残留小问题（→ iter-04）
1. **Step 2 (page 9) "FULL BUSKET" 文字被裁切**：max_mark 图水平太宽，col 内单独 height=24mm 让宽度溢出。
2. （次要）警告框警告图标缺失：JSON 中 warning_box 有 `icon: safety.warning_icon`，我没渲染。
3. （次要）warranty card 缺交替行底色（subtle gray every other row），目标 PDF 有，mine 无。
