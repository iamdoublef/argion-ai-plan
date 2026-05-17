# IMT050 Word DOCX 视觉保真评分记录

## 当前最优：W27

- **文件**: `final/imt050-wevac-eu-cn.docx`
- **LibreOffice 渲染评分**: `8.67 / 12.35`（mean / max）
- **MS Word 渲染评分**: `9.16 / 15.27`（mean / max）⚠ Word 比 LO 渲染差，因为 Word 默认 CJK 字距/行距与 Adobe PDF 不一致
- **Anti-cheat**: PASS（wt_count=457, image_hack=false, text_ratio=1.0, drawings=16）
- **MS Word 可打开**: PASS（docx2pdf Word COM 渲染成功）
- **页数**: 15（与目标 PDF 一致）
- **可编辑性**: 100%（无 text_box / 图片 hack）

## 评分基准说明

`score_candidate.py` 用 LibreOffice headless 渲染 docx→PDF→PNG，与目标 PDF 的 PNG 比对 mean RGB 差。
- **优点**: 与目标 PDF 的 Adobe 渲染较接近（freetype 基础一致）
- **缺点**: 客户实际打开用 MS Word，Word 渲染中文字距/行距与 LibreOffice 不同

## 28 路径迭代历史（按 visualdiff 升序）

| Winner | Path | Visualdiff | 备注 |
|--------|------|-----------|------|
| W27 | codex-design-iter22-iter08 | 8.67 / 12.35 | **当前 final** |
| W28 | codex-design-iter24-pathA | 8.67 / OOXML autospace | ⚠ Word 报"文件损坏" — 已回退 |
| W26 | 双路并发 char-spacing + image | 8.69 / 12.40 | |
| W25 | per-page surgical | 8.71 / 12.40 | |
| W9 | design-iter02-iter05 | 12.88 | THRESHOLD_PASS |
| W2 | design-iter01-main-iter02 | 14.14 | FONTS_FIXED baseline |

详见 `final/candidates/`

## 硬瓶颈页（W27 LibreOffice 评分）

| 页 | diff | 内容类型 | 难点 |
|----|------|---------|------|
| p3 | 12.04 | 中文长段落 + 产品图 | CJK 段落字距 |
| p9 | 11.99 | 中文长段落 + 操作步骤 | 行高 + 字距 |
| p11 | 12.14 | 中文长段落 + 警告框 | 红色警告框 |
| p14 | 12.35 | 保修条款表格 | 表格密集中文 |

## 28 路径已尝试且失败的优化

字距 4-8 twips（5 最优）、页眉页脚 hairline、封面图位、step badge 大小、警告框 padding、line-spacing exact 模式、浮动表、字间距、autoSpace 关、East Asia font hint、gridCol 显式、JPEG 嵌图、anchored drawings、per-page section margin、numPr 真实 bullet、run vertical position offset、szCs 匹配、noWrap、显式 page margin、frame_pr、bookmark、contextualSpacing、char spacing 子像素调整、image DPI 99%/101%、tab_stops、tcMar tweaks、subtitle space_after 子点变化、body 7.05→7.00pt — 全部回归或中性。

## 当前后台任务

- **iter-29 path-codex**（PID 后台 `badya9dit`）：用 Word baseline 评分新角度（w:kern, hint=eastAsia, autoSpaceDE 仅 body 段、tcMar 紧缩硬页）。⚠ 需通过 Word-open 闸门。
- **cron**：每 5 小时第 13 分自动检查迭代进度（job 待重建）。

## 待办

- [ ] design-iter-30：调用官方 `/docx` skill 走另一路径
- [ ] 验证 W27 在 MS Word 里替换文字的可编辑性（"通过替换文字实现新版本快速交付"）
