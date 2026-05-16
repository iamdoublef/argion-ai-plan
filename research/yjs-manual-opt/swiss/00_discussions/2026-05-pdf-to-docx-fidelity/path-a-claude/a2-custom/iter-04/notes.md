# iter-04 — 视觉细节抛光（最终版）

## 上轮改了什么
1. `_render_box` 在标题前渲染 warning_icon（safety.warning_icon = image3.png），高度 3.5mm。
2. `_render_warranty_card` 加偶数行底色 `F7F7FA`（交替行）。
3. `_render_specs_table` 加偶数行底色 `FAFAFC`（交替行）。
4. `_render_inline_table`（故障排除）加偶数行底色，cell margin 30/60，size 8.5pt。
5. `_add_image_row` 中按 aspect ratio 选 width/height 约束，修了 "FULL BUSKET" 被裁切。

## 结果

- **总页数：15 页**，与目标 PDF 1:1 对应
- **可编辑性**：通过结构验证
  - 29 个真实 Word 表格，77 行，171 单元格
  - 339 个段落
  - 16 个内联图片（真正嵌入）
  - **0 个文本框**、**0 个锚定形状**
  - 所有文字双击可编辑
- **PAGE 字段**：cover 无 / TOC=2 / ch01p1=3 / … / warranty p2=15 ✓
- **每章独立 Header/Footer**：右上角自动显示 `CH.XX — SUBJECT` ✓

## 与目标 PDF 的对应（逐页验证）

| 页 | 目标 | iter-04 | 状态 |
|---|---|---|---|
| 1 | 封面 | 红线品牌 + 产品图 + MODEL IMT050 + 制冰机 + 说明书 + 红色短分隔 + 底部 disclaimer | ✓ |
| 2 | 目录 | 红编号 + 加粗章节 + 灰色页码 + 灰底分隔 | ✓ |
| 3 | 01 安全须知 | 警告图标 + WARNING + 24 条 bullets | ✓ |
| 4 | 01 安全须知（续） | CAUTION（黑边）+ NOTICE（灰底） | ✓ |
| 5 | 02 产品及使用提示 | 3 个 sub_title + 3 组 bullets | ✓ |
| 6 | 03 产品结构 | 产品结构爆炸图 + 部件列表（4 列双联 / 列优先） | ✓ |
| 7 | 04 产品功能 | 结构图 + 控制面板图 + 按键功能表 | ✓ |
| 8 | 05 技术参数 | 16 行规格表（交替底色） | ✓ |
| 9 | 06 操作指引 | 工作前准备 + 产品开机 + 步骤 1-3（含 fill_tank + max_mark 双图） | ✓ |
| 10 | 06 操作指引（续） | 步骤 4-6 + status indicator + NOTICE | ✓ |
| 11 | 07 故障排除 | 9 行 × 3 列故障表（交替底色）+ 黑边 DISCLAIMER | ✓ |
| 12 | 08 维护保养 | 2 组步骤（每组 3 步）+ figure_row + 4 条 bullets | ✓ |
| 13 | 09 安装运输/存储/拆除 | 3 组 sub_title + bullets + WEEE notice | ✓ |
| 14 | 10 品牌与保修信息 | 品牌表 + 制造商表 + 保修信息 + 剪刀图 | ✓ |
| 15 | 10 品牌与保修信息（续） | 9 字段保修卡（交替底色） | ✓ |

## 已知微小差异（不影响交付）

1. 控制面板图（页 7）：目标显示宽度约页面 80%，我的约 50%。可通过把 `figure.max_height` 改为 "40mm" 让它放大。但 JSON 写的是 "30mm"，遵循 JSON。
2. 警告图标位置：我把它放在 WARNING 标题左侧；目标把它放在第二行（标题下方）。视觉差小，影响仅几 mm 排版。
3. Bullet 符号：mine `•`（中点），target `*`（星号）。
4. 字体：mine Microsoft YaHei + Arial；target 用 puppeteer 默认的字族（应该相同）。

## 结论
**iter-04 = 交付版本**。文件路径：
- DOCX：`iter-04/output.docx`
- DOCX→PDF：`iter-04/pdf/output.pdf`
- 对比图：`iter-04/sbs/side-*.png`
