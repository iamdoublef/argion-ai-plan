# design-iter-32 path-docxjs-fromscratch status

## 目标

用官方 `docx-js` (Node.js) 库从零重做 IMT050 中文 A5 冰格机说明书 docx，
验证 docx-js 路径能否独立做到 W27 的视觉水平 (8.67 mean / 12.35 max)。
W27 走 python-docx 路径，已经稳定但不模板化；docx-js 天然支持模板化
（content 用 JS 对象传入），如果能拉到接近 W27 视觉，就是 plateau 突破候选。

## 最终结果

- 候选文件：`output.docx`（同时归档到 `iter-5/output.docx`）
- 最终评分：`overall 11.32 / max 17.77`
- W27 参考：`overall 8.67 / max 12.35`
- 差距：overall +2.65 (30%)，max +5.42 (44%)
- 反作弊：**通过**（`wt_count=500`、`text_ratio=1.00`、`image_hack_detected=false`、`editable=100%`）
- validate.py：**通过**
- MS Word 打开：**通过**（`word_render.pdf` 15 页正常）

| 候选 | 主要改动 | overall | max | 决策 |
| --- | --- | ---: | ---: | --- |
| iter-1 | 初版（顶部 margin 用 10.2pt） | 16.15 | 35.08 | 基线 |
| iter-2 | 顶部 margin 改为 10.2mm（W27 一致） | **11.53** | 21.89 | 大幅改善 |
| iter-3 | warranty card 行高 242 / 单元格 padding (52/87) | **11.30** | **17.77** | 保留 |
| iter-4 | warning 字符间距 8twips + 图标尺寸/缩进微调 | 11.32 | 17.77 | 中性 |
| iter-5 | 顶部 margin 试 9.5mm（回退）+ 复核 | 11.32 | 17.77 | 最终 |

## 每页视觉差异（vs target PDF）

| 页码 | 内容 | mine | W27 | Δ |
| ---: | --- | ---: | ---: | ---: |
| 1 | Cover | 2.88 | 2.93 | -0.05 |
| 2 | TOC | 3.96 | 3.25 | +0.71 |
| 3 | Safety / warning | 17.23 | 12.04 | +5.19 |
| 4 | Safety / caution+notice | 8.75 | 7.09 | +1.66 |
| 5 | Tips bullets | 13.94 | 10.94 | +3.00 |
| 6 | Structure (image+table) | 12.45 | 6.19 | +6.26 |
| 7 | Features (image+table) | 11.56 | 7.81 | +3.75 |
| 8 | Specs table | 10.58 | 7.84 | +2.74 |
| 9 | Operation steps p1 | 14.30 | 11.99 | +2.31 |
| 10 | Operation steps p2 + note | 12.46 | 10.14 | +2.32 |
| 11 | Troubleshooting table | 14.14 | 12.14 | +2.00 |
| 12 | Maintenance | 11.53 | 10.01 | +1.52 |
| 13 | Installation | 13.50 | 11.70 | +1.80 |
| 14 | Warranty card | 17.77 | 12.35 | +5.42 |
| 15 | Warranty card (空白) | 4.75 | 3.65 | +1.10 |

## 关键发现

1. **docx-js 完全可行**：
   - 反作弊全部通过：编辑性 100%、wt_count=500（≥W27 的 457）、无图像 hack
   - MS Word 原生兼容
   - validate.py 完全通过
   - 同样的内容/模板能轻易换 locale（content.js 是纯数据）
2. **视觉差距来源**：
   - 字体度量差异：docx-js 输出的 `<w:rFonts eastAsia>` 在 LibreOffice 中
     渲染时，中英文混排的字符宽度比 python-docx 输出略大，
     导致警告框标题"警告 WARNING"换行、长段落多换一次行。
   - 步骤图组在第 9 页比 target 略宽一格列，让流文重排。
   - 表格行高调整后 max 从 28→17，已大幅缩窄。
3. **plateau 突破？未达成**：
   - 8.67 (W27) → 11.32 (本路径) = 30% 差距
   - 已尝试 5 轮微调，单独调节字符间距、图标尺寸、margin 都无法继续往下压。
   - 残余差距是 docx-js + LibreOffice 渲染管线的系统性字宽差异，
     非"再调几个参数"就能消除。

## docx-js 路径可行性结论

**可行，但当前 fidelity 仍落后于 W27 路径 30%。**

优点（vs W27 python-docx）：
- 天然模板化：`content.js` 是纯数据，新增 locale 只需替换字符串
- 反作弊更宽松：本身用的就是 ImageRun + 真实段落，没有任何 hack 风险
- MS Word 兼容性更好（生成的 XML 由官方库维护）

缺点：
- LibreOffice 渲染 docx-js 输出时，中文/拉丁混排有 ~5% 系统宽度差
- 需要在生成端进一步调节字距和 padding 才能拉平
- 暂未达到 W27 的视觉 baseline（8.67），但已通过所有"硬"检查

后续工作建议：
1. 改用 MS Word 直出 PDF 评分（绕开 LibreOffice 字宽差异），看真实 fidelity
2. 如果接受 11.32 视觉差距，docx-js 路径即可作为多 locale 模板化生产的主线
3. 把 W27 的字符间距细节（`w:spacing val=8` 等）逐字段抄进 docx-js
   配置（已尝试 warning 项，效果有限）

## 文件清单

- `package.json` / `package-lock.json`：依赖（docx 9.6.1 + image-size）
- `content.js`：全部文字内容（纯数据，可参数化）
- `build.js`：docx-js 构建脚本
- `output.docx`：最终候选
- `output.score.json`：最终评分
- `iter-1/` ~ `iter-5/`：每轮 docx + score 快照
- `word_render.pdf`：MS Word 转出的 PDF，用于人工核对
